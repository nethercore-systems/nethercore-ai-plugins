# Decal and Detail Projection

Apply decals, damage, and wear to textures.

## Planar Decal Projection

```python
import numpy as np
from PIL import Image
from typing import Optional, Callable

def normalize(v: np.ndarray) -> np.ndarray:
    """Normalize a vector."""
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

def project_decal(
    uv_to_world_fn: Callable[[float, float], Optional[np.ndarray]],
    decal: np.ndarray,
    projection_origin: np.ndarray,
    projection_dir: np.ndarray,
    projection_size: float,
    target_texture: np.ndarray,
) -> np.ndarray:
    """Project a decal onto a texture using planar projection.

    Args:
        uv_to_world_fn: Function mapping (u, v) to world position or None
        decal: RGBA decal texture array
        projection_origin: 3D origin point of projection
        projection_dir: 3D direction of projection (normalized)
        projection_size: Size of projection area
        target_texture: Target RGBA texture to modify (modified in place)

    Returns:
        Modified target texture
    """
    height, width = target_texture.shape[:2]
    decal_h, decal_w = decal.shape[:2]

    # Calculate projection basis
    up = np.array([0.0, 1.0, 0.0])
    right = normalize(np.cross(projection_dir, up))
    proj_up = normalize(np.cross(right, projection_dir))

    for y in range(height):
        for x in range(width):
            u = x / width
            v = y / height

            # Find world position for this UV
            world_pos = uv_to_world_fn(u, v)
            if world_pos is None:
                continue

            # Project onto decal plane
            to_point = world_pos - projection_origin
            dist = float(np.dot(to_point, projection_dir))

            # Check if within projection range
            if 0.0 < dist < projection_size:
                # Calculate decal UV
                proj_u = float(np.dot(to_point, right)) / projection_size + 0.5
                proj_v = float(np.dot(to_point, proj_up)) / projection_size + 0.5

                if 0.0 <= proj_u <= 1.0 and 0.0 <= proj_v <= 1.0:
                    # Sample decal
                    dx = int(proj_u * (decal_w - 1))
                    dy = int(proj_v * (decal_h - 1))
                    decal_color = decal[dy, dx]

                    # Alpha threshold check
                    if decal_color[3] > 128:
                        target_texture[y, x] = decal_color

    return target_texture
```

## Damage/Wear Overlay

```python
import numpy as np
from typing import Optional, Callable

def fbm_noise(x: float, y: float, octaves: int, seed: int) -> float:
    """Fractional Brownian Motion noise (simplified implementation)."""
    np.random.seed(seed)
    value = 0.0
    amplitude = 1.0
    frequency = 1.0
    max_value = 0.0

    for _ in range(octaves):
        # Simple value noise approximation
        ix, iy = int(x * frequency), int(y * frequency)
        np.random.seed(seed + ix * 1000 + iy)
        value += np.random.random() * amplitude
        max_value += amplitude
        amplitude *= 0.5
        frequency *= 2.0

    return value / max_value if max_value > 0 else 0.0

def darken(color: np.ndarray, amount: float) -> np.ndarray:
    """Darken a color by the given amount."""
    result = color.copy().astype(np.float32)
    result[:3] = result[:3] * (1.0 - amount)
    return np.clip(result, 0, 255).astype(np.uint8)

def desaturate(color: np.ndarray, amount: float) -> np.ndarray:
    """Desaturate a color by the given amount."""
    result = color.copy().astype(np.float32)
    gray = 0.299 * result[0] + 0.587 * result[1] + 0.114 * result[2]
    result[:3] = result[:3] * (1.0 - amount) + gray * amount
    return np.clip(result, 0, 255).astype(np.uint8)

def apply_wear_overlay(
    base_texture: np.ndarray,
    wear_intensity: float,
    edge_wear: bool = False,
    edge_distance_fn: Optional[Callable[[float, float], float]] = None,
    seed: int = 42,
) -> np.ndarray:
    """Apply wear and damage overlay to a texture.

    Args:
        base_texture: RGBA texture array (modified in place)
        wear_intensity: Intensity of wear effect (0.0-1.0)
        edge_wear: Whether to increase wear at edges
        edge_distance_fn: Optional function returning edge distance at (u, v)
        seed: Random seed for noise generation

    Returns:
        Modified texture
    """
    height, width = base_texture.shape[:2]

    for y in range(height):
        for x in range(width):
            u = x / width
            v = y / height

            # Generate wear noise
            noise = fbm_noise(u * 10.0, v * 10.0, 4, seed)
            wear = 1.0 if noise > (1.0 - wear_intensity) else 0.0

            # Optional: more wear at edges
            edge_factor = 1.0
            if edge_wear and edge_distance_fn is not None:
                edge_factor = edge_distance_fn(u, v)

            if wear * edge_factor > 0.5:
                base = base_texture[y, x]
                # Darken and desaturate
                worn = desaturate(darken(base, 0.3), 0.5)
                base_texture[y, x] = worn

    return base_texture
```

## Wear Intensity Presets

| Intensity | Use Case |
|-----------|----------|
| 0.0-0.1 | New/pristine |
| 0.1-0.3 | Light wear |
| 0.3-0.5 | Moderate use |
| 0.5-0.7 | Heavy wear |
| 0.7-1.0 | Battle-damaged |

## Edge Wear Pattern

Focus wear on convex edges (using mesh curvature):

```python
import numpy as np
from typing import Optional

def sample_edge_distance(
    triangles: np.ndarray,
    uvs: np.ndarray,
    normals: np.ndarray,
    u: float,
    v: float,
) -> float:
    """Sample edge distance/curvature at a UV coordinate.

    Args:
        triangles: Array of triangle indices (M, 3)
        uvs: Array of UV coordinates (N, 2)
        normals: Array of vertex normals (N, 3)
        u, v: UV coordinate to sample

    Returns:
        Edge factor from 0.0 (flat) to 1.0 (sharp edge)
    """
    # Find nearest triangle for this UV
    # Calculate curvature at that point
    # Higher curvature = more wear likelihood
    # Returns 0.0 (flat) to 1.0 (sharp edge)

    # Simplified implementation - find closest UV vertex and estimate curvature
    uv_point = np.array([u, v])
    distances = np.linalg.norm(uvs - uv_point, axis=1)
    nearest_idx = np.argmin(distances)

    # Find triangles containing this vertex
    tri_mask = np.any(triangles == nearest_idx, axis=1)
    adjacent_tris = triangles[tri_mask]

    if len(adjacent_tris) < 2:
        return 0.0

    # Estimate curvature from normal variation
    adjacent_normals = normals[adjacent_tris.flatten()]
    normal_variance = np.var(adjacent_normals, axis=0).sum()

    # Map variance to 0-1 range (higher variance = sharper edge)
    return min(1.0, normal_variance * 10.0)
```
