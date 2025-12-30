# UV Mapping and Island Detection

Working with mesh UV coordinates for texture generation.

## UV Bounds

```python
import numpy as np
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class UvBounds:
    min_u: float
    max_u: float
    min_v: float
    max_v: float

    @property
    def width(self) -> float:
        return self.max_u - self.min_u

    @property
    def height(self) -> float:
        return self.max_v - self.min_v

def get_uv_bounds(uvs: np.ndarray) -> UvBounds:
    """Get UV bounds from mesh UV coordinates.

    Args:
        uvs: Array of shape (N, 2) containing UV coordinates

    Returns:
        UvBounds with min/max U and V values
    """
    return UvBounds(
        min_u=float(np.min(uvs[:, 0])),
        max_u=float(np.max(uvs[:, 0])),
        min_v=float(np.min(uvs[:, 1])),
        max_v=float(np.max(uvs[:, 1])),
    )
```

## Texture Resolution Calculation

Match resolution to mesh detail level:

```python
import numpy as np

def triangle_area(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """Calculate the area of a triangle given three 3D points."""
    ab = b - a
    ac = c - a
    return float(np.linalg.norm(np.cross(ab, ac)) * 0.5)

def next_power_of_two(n: int) -> int:
    """Return the smallest power of 2 >= n."""
    return 1 << (n - 1).bit_length() if n > 0 else 1

def calculate_texture_resolution(
    positions: np.ndarray,
    triangles: np.ndarray,
    uvs: np.ndarray,
    target_texel_density: float,  # Texels per world unit
) -> tuple[int, int]:
    """Calculate optimal texture resolution based on mesh and target density.

    Args:
        positions: Array of shape (N, 3) containing vertex positions
        triangles: Array of shape (M, 3) containing triangle indices
        uvs: Array of shape (N, 2) containing UV coordinates
        target_texel_density: Desired texels per world unit

    Returns:
        Tuple of (width, height) for texture resolution
    """
    # Calculate world-space surface area (vectorized)
    v0 = positions[triangles[:, 0]]
    v1 = positions[triangles[:, 1]]
    v2 = positions[triangles[:, 2]]
    edges1 = v1 - v0
    edges2 = v2 - v0
    crosses = np.cross(edges1, edges2)
    triangle_areas = np.linalg.norm(crosses, axis=1) * 0.5
    total_area = float(np.sum(triangle_areas))

    # Calculate UV-space coverage
    bounds = get_uv_bounds(uvs)
    uv_coverage = bounds.width * bounds.height

    # Desired size based on density
    desired_texels = np.sqrt(total_area * (target_texel_density ** 2))
    raw_size = int(desired_texels / np.sqrt(uv_coverage)) if uv_coverage > 0 else 64

    # Snap to power of 2, respect ZX limits
    size = max(64, min(512, next_power_of_two(raw_size)))
    return (size, size)
```

## UV Island Detection

Identify connected UV regions:

```python
import numpy as np
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class UvIsland:
    triangle_indices: List[int] = field(default_factory=list)
    min_uv: np.ndarray = field(default_factory=lambda: np.array([0.0, 0.0]))
    max_uv: np.ndarray = field(default_factory=lambda: np.array([1.0, 1.0]))
    name: Optional[str] = None  # "body", "head", etc.

    def contains_uv(self, u: float, v: float) -> bool:
        """Check if UV coordinate is within this island's bounds."""
        return (self.min_uv[0] <= u <= self.max_uv[0] and
                self.min_uv[1] <= v <= self.max_uv[1])

class UvIslandMapper:
    def __init__(self, islands: List[UvIsland]):
        self.islands = islands

    @classmethod
    def from_mesh(cls, triangles: np.ndarray, uvs: np.ndarray) -> "UvIslandMapper":
        """Create UV island mapper from mesh data.

        Args:
            triangles: Array of shape (M, 3) containing triangle vertex indices
            uvs: Array of shape (N, 2) containing UV coordinates
        """
        num_triangles = len(triangles)
        visited = np.zeros(num_triangles, dtype=bool)
        islands = []

        for tri_idx in range(num_triangles):
            if visited[tri_idx]:
                continue
            island = flood_fill_uv_island(triangles, uvs, tri_idx, visited)
            islands.append(island)

        return cls(islands)

    def island_at(self, u: float, v: float) -> Optional[int]:
        """Find the island index containing the given UV coordinate."""
        for idx, island in enumerate(self.islands):
            if (island.min_uv[0] <= u <= island.max_uv[0] and
                island.min_uv[1] <= v <= island.max_uv[1]):
                if island.contains_uv(u, v):
                    return idx
        return None

def flood_fill_uv_island(
    triangles: np.ndarray,
    uvs: np.ndarray,
    start_idx: int,
    visited: np.ndarray
) -> UvIsland:
    """Flood fill to find connected UV island starting from a triangle."""
    island_tris = []
    stack = [start_idx]

    while stack:
        tri_idx = stack.pop()
        if visited[tri_idx]:
            continue
        visited[tri_idx] = True
        island_tris.append(tri_idx)

        # Find adjacent triangles (simplified - check for shared vertices)
        # In practice, use proper adjacency data structure
        for other_idx in range(len(triangles)):
            if not visited[other_idx]:
                if np.any(np.isin(triangles[tri_idx], triangles[other_idx])):
                    stack.append(other_idx)

    # Calculate bounds
    island_uvs = uvs[triangles[island_tris].flatten()]
    min_uv = np.min(island_uvs, axis=0)
    max_uv = np.max(island_uvs, axis=0)

    return UvIsland(
        triangle_indices=island_tris,
        min_uv=min_uv,
        max_uv=max_uv,
    )
```

## Per-Island Texture Generation

```python
import numpy as np
from PIL import Image
from typing import List, Callable

def generate_island_textured(
    islands: UvIslandMapper,
    width: int,
    height: int,
    material_samplers: List[Callable[[float, float], np.ndarray]],
) -> np.ndarray:
    """Generate texture with different materials per UV island.

    Args:
        islands: UvIslandMapper with detected islands
        width: Texture width in pixels
        height: Texture height in pixels
        material_samplers: List of functions that sample color at (u, v)

    Returns:
        RGBA texture array of shape (height, width, 4)
    """
    texture = np.zeros((height, width, 4), dtype=np.uint8)

    # Create UV coordinate grids (vectorized)
    v_coords, u_coords = np.mgrid[0:height, 0:width]
    u_normalized = u_coords.astype(np.float32) / width
    v_normalized = v_coords.astype(np.float32) / height

    # Process each pixel
    for y in range(height):
        for x in range(width):
            u = u_normalized[y, x]
            v = v_normalized[y, x]

            island_idx = islands.island_at(u, v)
            if island_idx is not None and island_idx < len(material_samplers):
                color = material_samplers[island_idx](u, v)
                texture[y, x] = (color * 255).astype(np.uint8)

    return texture

def texture_to_image(texture: np.ndarray) -> Image.Image:
    """Convert texture array to PIL Image."""
    return Image.fromarray(texture, mode='RGBA')
```
