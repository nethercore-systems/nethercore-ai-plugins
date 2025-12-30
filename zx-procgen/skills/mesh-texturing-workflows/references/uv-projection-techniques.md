# UV Projection Techniques

Detailed implementations of UV projection methods for procedural meshes.

## Overview

UV projection maps 3D coordinates to 2D texture coordinates. Choose the projection that minimizes distortion for your mesh shape.

| Projection | Best For | Distortion Pattern |
|------------|----------|-------------------|
| **Planar** | Flat surfaces, floors, walls | Stretches on non-perpendicular faces |
| **Box/Triplanar** | Complex shapes, terrain | Seams at angle boundaries |
| **Cylindrical** | Pillars, barrels, characters | Polar distortion at caps |
| **Spherical** | Round objects, planets | Seams and polar pinching |

## Planar Projection

Projects UVs along a single axis.

```python
import numpy as np
from enum import Enum
from typing import Tuple

class Axis(Enum):
    X = 'x'
    Y = 'y'
    Z = 'z'

def planar_projection(
    positions: np.ndarray,
    axis: Axis,
    scale: float,
    offset: Tuple[float, float] = (0.0, 0.0),
) -> np.ndarray:
    """Apply planar UV projection along a single axis.

    Args:
        positions: Array of shape (N, 3) containing vertex positions
        axis: Projection axis (X, Y, or Z)
        scale: Scale factor for UV coordinates
        offset: UV offset (u_offset, v_offset)

    Returns:
        Array of shape (N, 2) containing UV coordinates
    """
    uvs = np.zeros((len(positions), 2), dtype=np.float32)

    if axis == Axis.Y:
        uvs[:, 0] = positions[:, 0] / scale + offset[0] + 0.5
        uvs[:, 1] = positions[:, 2] / scale + offset[1] + 0.5
    elif axis == Axis.X:
        uvs[:, 0] = positions[:, 2] / scale + offset[0] + 0.5
        uvs[:, 1] = positions[:, 1] / scale + offset[1] + 0.5
    else:  # Axis.Z
        uvs[:, 0] = positions[:, 0] / scale + offset[0] + 0.5
        uvs[:, 1] = positions[:, 1] / scale + offset[1] + 0.5

    return uvs
```

### Rotated Planar

Project along arbitrary direction:

```python
import numpy as np

def normalize(v: np.ndarray) -> np.ndarray:
    """Normalize a vector."""
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

def rotated_planar_projection(
    positions: np.ndarray,
    forward: np.ndarray,  # Projection direction
    up: np.ndarray,       # Up reference
    scale: float,
) -> np.ndarray:
    """Apply planar UV projection along arbitrary direction.

    Args:
        positions: Array of shape (N, 3) containing vertex positions
        forward: Projection direction (3D vector)
        up: Up reference vector (3D vector)
        scale: Scale factor for UV coordinates

    Returns:
        Array of shape (N, 2) containing UV coordinates
    """
    right = normalize(np.cross(forward, up))
    proj_up = normalize(np.cross(right, forward))

    uvs = np.zeros((len(positions), 2), dtype=np.float32)
    uvs[:, 0] = np.dot(positions, right) / scale + 0.5
    uvs[:, 1] = np.dot(positions, proj_up) / scale + 0.5

    return uvs
```

## Box/Triplanar Projection

Projects based on face normal direction - best for complex shapes.

```python
import numpy as np

def box_projection(
    positions: np.ndarray,
    normals: np.ndarray,
    scale: float = 1.0,
) -> np.ndarray:
    """Apply box/triplanar UV projection based on face normals.

    Args:
        positions: Array of shape (N, 3) containing vertex positions
        normals: Array of shape (N, 3) containing vertex normals
        scale: Scale factor for UV coordinates

    Returns:
        Array of shape (N, 2) containing UV coordinates
    """
    uvs = np.zeros((len(positions), 2), dtype=np.float32)
    abs_normals = np.abs(normals)

    # X-dominant: project onto YZ plane
    x_mask = (abs_normals[:, 0] >= abs_normals[:, 1]) & (abs_normals[:, 0] >= abs_normals[:, 2])
    uvs[x_mask, 0] = positions[x_mask, 2] / scale + 0.5
    uvs[x_mask, 1] = positions[x_mask, 1] / scale + 0.5

    # Y-dominant: project onto XZ plane
    y_mask = ~x_mask & (abs_normals[:, 1] >= abs_normals[:, 2])
    uvs[y_mask, 0] = positions[y_mask, 0] / scale + 0.5
    uvs[y_mask, 1] = positions[y_mask, 2] / scale + 0.5

    # Z-dominant: project onto XY plane
    z_mask = ~x_mask & ~y_mask
    uvs[z_mask, 0] = positions[z_mask, 0] / scale + 0.5
    uvs[z_mask, 1] = positions[z_mask, 1] / scale + 0.5

    return uvs
```

### Blended Triplanar

Smooth transitions between projections:

```python
import numpy as np
from typing import Tuple

def triplanar_blend(
    pos: np.ndarray,
    normal: np.ndarray,
    scale: float,
    blend_sharpness: float,
) -> Tuple[float, float]:
    """Calculate blended triplanar UV for a single vertex.

    Args:
        pos: 3D position vector
        normal: 3D normal vector
        scale: UV scale factor
        blend_sharpness: Sharpness of blend between projections

    Returns:
        Tuple of (u, v) coordinates
    """
    # Calculate blend weights from normal
    abs_n = np.abs(normal)
    weights = np.power(abs_n, blend_sharpness)
    weights = weights / np.sum(weights)  # Normalize

    # Sample each projection
    uv_x = np.array([pos[2] / scale, pos[1] / scale])  # YZ plane
    uv_y = np.array([pos[0] / scale, pos[2] / scale])  # XZ plane
    uv_z = np.array([pos[0] / scale, pos[1] / scale])  # XY plane

    # Blend UVs
    blended_u = uv_x[0] * weights[0] + uv_y[0] * weights[1] + uv_z[0] * weights[2]
    blended_v = uv_x[1] * weights[0] + uv_y[1] * weights[1] + uv_z[1] * weights[2]

    return (float(blended_u), float(blended_v))

def triplanar_blend_vectorized(
    positions: np.ndarray,
    normals: np.ndarray,
    scale: float,
    blend_sharpness: float,
) -> np.ndarray:
    """Calculate blended triplanar UVs for all vertices (vectorized).

    Args:
        positions: Array of shape (N, 3) containing vertex positions
        normals: Array of shape (N, 3) containing vertex normals
        scale: UV scale factor
        blend_sharpness: Sharpness of blend between projections

    Returns:
        Array of shape (N, 2) containing UV coordinates
    """
    # Calculate blend weights from normals
    abs_n = np.abs(normals)
    weights = np.power(abs_n, blend_sharpness)
    weights = weights / np.sum(weights, axis=1, keepdims=True)

    # Calculate projections for all axes
    uv_x = np.column_stack([positions[:, 2] / scale, positions[:, 1] / scale])
    uv_y = np.column_stack([positions[:, 0] / scale, positions[:, 2] / scale])
    uv_z = np.column_stack([positions[:, 0] / scale, positions[:, 1] / scale])

    # Blend UVs
    uvs = (uv_x * weights[:, 0:1] +
           uv_y * weights[:, 1:2] +
           uv_z * weights[:, 2:3])

    return uvs.astype(np.float32)
```

## Cylindrical Projection

Best for pillars, barrels, and character torsos.

```python
import numpy as np

def cylindrical_projection(
    positions: np.ndarray,
    axis: Axis,
    height_scale: float,
    seam_angle: float = 0.0,  # Radians, where to place the UV seam
) -> np.ndarray:
    """Apply cylindrical UV projection around an axis.

    Args:
        positions: Array of shape (N, 3) containing vertex positions
        axis: Central axis of the cylinder (X, Y, or Z)
        height_scale: Scale factor for height (V coordinate)
        seam_angle: Angle in radians where to place the UV seam

    Returns:
        Array of shape (N, 2) containing UV coordinates
    """
    uvs = np.zeros((len(positions), 2), dtype=np.float32)

    if axis == Axis.Y:
        angles = np.arctan2(positions[:, 0], positions[:, 2])
        heights = positions[:, 1]
    elif axis == Axis.X:
        angles = np.arctan2(positions[:, 1], positions[:, 2])
        heights = positions[:, 0]
    else:  # Axis.Z
        angles = np.arctan2(positions[:, 0], positions[:, 1])
        heights = positions[:, 2]

    # Normalize angle to [0, 1], accounting for seam
    u = (angles - seam_angle) / (2.0 * np.pi)
    u = np.where(u < 0.0, u + 1.0, u)

    v = heights / height_scale + 0.5

    uvs[:, 0] = u
    uvs[:, 1] = v

    return uvs
```

### Handling Seams

Duplicate vertices along seams for proper texture continuity:

```python
import numpy as np
from typing import Tuple
from dataclasses import dataclass

@dataclass
class MeshData:
    positions: np.ndarray
    normals: np.ndarray
    uvs: np.ndarray
    triangles: np.ndarray

def fix_cylindrical_seam(mesh: MeshData, seam_threshold: float = 0.5) -> MeshData:
    """Fix UV seams by duplicating vertices that cross the seam.

    Args:
        mesh: MeshData with positions, normals, uvs, and triangles
        seam_threshold: Threshold for detecting seam crossing

    Returns:
        New MeshData with fixed seams
    """
    positions = list(mesh.positions)
    normals = list(mesh.normals)
    uvs = list(mesh.uvs)
    triangles = mesh.triangles.copy()

    num_triangles = len(triangles) // 3

    for tri_idx in range(num_triangles):
        base = tri_idx * 3
        i0, i1, i2 = triangles[base], triangles[base + 1], triangles[base + 2]

        # Check for UV discontinuity (crosses seam)
        u_values = [uvs[i0][0], uvs[i1][0], uvs[i2][0]]
        max_u = max(u_values)
        min_u = min(u_values)

        if max_u - min_u > seam_threshold:
            # Duplicate vertices with low U and shift to U+1
            for local_idx, vertex_idx in enumerate([i0, i1, i2]):
                if uvs[vertex_idx][0] < 0.5:
                    # Duplicate vertex
                    new_idx = len(positions)
                    positions.append(positions[vertex_idx].copy())
                    normals.append(normals[vertex_idx].copy())
                    new_uv = uvs[vertex_idx].copy()
                    new_uv[0] += 1.0
                    uvs.append(new_uv)

                    # Update triangle index
                    triangles[base + local_idx] = new_idx

    return MeshData(
        positions=np.array(positions),
        normals=np.array(normals),
        uvs=np.array(uvs),
        triangles=triangles,
    )
```

## Spherical Projection

For planets, orbs, and rounded objects.

```python
import numpy as np

def spherical_projection(positions: np.ndarray) -> np.ndarray:
    """Apply spherical (equirectangular) UV projection.

    Args:
        positions: Array of shape (N, 3) containing vertex positions

    Returns:
        Array of shape (N, 2) containing UV coordinates
    """
    # Normalize positions to unit sphere
    norms = np.linalg.norm(positions, axis=1, keepdims=True)
    normalized = positions / (norms + 1e-8)

    # Equirectangular projection
    u = 0.5 + np.arctan2(normalized[:, 0], normalized[:, 2]) / (2.0 * np.pi)
    v = 0.5 - np.arcsin(np.clip(normalized[:, 1], -1.0, 1.0)) / np.pi

    return np.column_stack([u, v]).astype(np.float32)
```

### Polar Fix

Reduce pinching at poles by averaging:

```python
import numpy as np
from typing import List

def find_connected_vertices(triangles: np.ndarray, vertex_idx: int) -> List[int]:
    """Find all vertices connected to a given vertex via triangles."""
    # Find triangles containing this vertex
    tri_mask = np.any(triangles == vertex_idx, axis=1)
    connected_tris = triangles[tri_mask]

    # Get unique vertices from those triangles (excluding the query vertex)
    connected = set(connected_tris.flatten()) - {vertex_idx}
    return list(connected)

def fix_polar_pinching(
    positions: np.ndarray,
    uvs: np.ndarray,
    triangles: np.ndarray,
    pole_threshold: float = 0.1,
) -> np.ndarray:
    """Fix UV pinching at poles by averaging U coordinates.

    Args:
        positions: Array of shape (N, 3) containing vertex positions
        uvs: Array of shape (N, 2) containing UV coordinates (modified in place)
        triangles: Array of shape (M, 3) containing triangle indices
        pole_threshold: How close to pole to apply fix (0-1)

    Returns:
        Modified UV array
    """
    # Normalize positions
    norms = np.linalg.norm(positions, axis=1, keepdims=True)
    normalized = positions / (norms + 1e-8)

    # Find vertices near poles
    for i in range(len(positions)):
        if abs(normalized[i, 1]) > 1.0 - pole_threshold:
            # At pole - average U from connected vertices
            connected = find_connected_vertices(triangles, i)
            if connected:
                avg_u = np.mean([uvs[j, 0] for j in connected])
                uvs[i, 0] = avg_u

    return uvs
```

## Per-Face Projection

Each face gets [0,1] UV range - good for cube-style texturing.

```python
import numpy as np
from typing import Tuple

def calculate_face_uvs(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    """Calculate UVs for a single triangle face.

    Args:
        p0, p1, p2: 3D vertex positions

    Returns:
        Array of shape (3, 2) containing UV coordinates for the face
    """
    # Use edge vectors to determine UV orientation
    e1 = p1 - p0
    e2 = p2 - p0
    normal = np.cross(e1, e2)
    norm_len = np.linalg.norm(normal)
    if norm_len > 0:
        normal = normal / norm_len

    # Choose UV axes based on face orientation
    abs_normal = np.abs(normal)
    if abs_normal[1] > abs_normal[0] and abs_normal[1] > abs_normal[2]:
        u_axis = np.array([1, 0, 0], dtype=np.float32)
        v_axis = np.array([0, 0, 1], dtype=np.float32)
    elif abs_normal[0] > abs_normal[2]:
        u_axis = np.array([0, 0, 1], dtype=np.float32)
        v_axis = np.array([0, 1, 0], dtype=np.float32)
    else:
        u_axis = np.array([1, 0, 0], dtype=np.float32)
        v_axis = np.array([0, 1, 0], dtype=np.float32)

    # Project vertices onto UV plane
    return np.array([
        [np.dot(p0, u_axis), np.dot(p0, v_axis)],
        [np.dot(p1, u_axis), np.dot(p1, v_axis)],
        [np.dot(p2, u_axis), np.dot(p2, v_axis)],
    ], dtype=np.float32)

def per_face_projection(mesh: MeshData) -> MeshData:
    """Apply per-face UV projection, duplicating vertices for unique UVs.

    Args:
        mesh: MeshData with positions, normals, and triangles

    Returns:
        New MeshData with duplicated vertices and per-face UVs
    """
    num_triangles = len(mesh.triangles) // 3

    new_positions = []
    new_normals = []
    new_uvs = []
    new_triangles = []

    for tri_idx in range(num_triangles):
        base = tri_idx * 3
        i0, i1, i2 = mesh.triangles[base], mesh.triangles[base + 1], mesh.triangles[base + 2]

        base_idx = len(new_positions)

        # Duplicate vertices
        new_positions.append(mesh.positions[i0])
        new_positions.append(mesh.positions[i1])
        new_positions.append(mesh.positions[i2])

        new_normals.append(mesh.normals[i0])
        new_normals.append(mesh.normals[i1])
        new_normals.append(mesh.normals[i2])

        # Calculate face-local UVs
        face_uvs = calculate_face_uvs(
            mesh.positions[i0],
            mesh.positions[i1],
            mesh.positions[i2],
        )
        new_uvs.extend(face_uvs)

        new_triangles.extend([base_idx, base_idx + 1, base_idx + 2])

    return MeshData(
        positions=np.array(new_positions),
        normals=np.array(new_normals),
        uvs=np.array(new_uvs),
        triangles=np.array(new_triangles, dtype=np.int32),
    )
```

## Python Implementations

```python
import numpy as np

def cylindrical_uv(vertices, axis='y', height_scale=2.0):
    """Apply cylindrical UV projection."""
    uvs = np.zeros((len(vertices), 2))

    for i, v in enumerate(vertices):
        if axis == 'y':
            angle = np.arctan2(v[0], v[2])
            height = v[1]
        elif axis == 'x':
            angle = np.arctan2(v[1], v[2])
            height = v[0]
        else:  # z
            angle = np.arctan2(v[0], v[1])
            height = v[2]

        uvs[i, 0] = (angle / (2 * np.pi) + 0.5) % 1.0
        uvs[i, 1] = height / height_scale + 0.5

    return uvs


def spherical_uv(vertices):
    """Apply spherical UV projection."""
    # Normalize to unit sphere
    norms = np.linalg.norm(vertices, axis=1, keepdims=True)
    normalized = vertices / (norms + 1e-8)

    u = 0.5 + np.arctan2(normalized[:, 0], normalized[:, 2]) / (2 * np.pi)
    v = 0.5 - np.arcsin(np.clip(normalized[:, 1], -1, 1)) / np.pi

    return np.column_stack([u, v])


def box_uv(vertices, normals, scale=1.0):
    """Apply box/triplanar UV projection."""
    uvs = np.zeros((len(vertices), 2))
    abs_normals = np.abs(normals)

    for i, (v, n) in enumerate(zip(vertices, abs_normals)):
        if n[0] >= n[1] and n[0] >= n[2]:
            uvs[i] = [v[2] / scale + 0.5, v[1] / scale + 0.5]
        elif n[1] >= n[2]:
            uvs[i] = [v[0] / scale + 0.5, v[2] / scale + 0.5]
        else:
            uvs[i] = [v[0] / scale + 0.5, v[1] / scale + 0.5]

    return uvs
```

## Choosing a Projection

| Mesh Shape | Recommended | Alternative |
|------------|-------------|-------------|
| Floor/wall | Planar | - |
| Cube/box | Per-face or Box | - |
| Cylinder/pillar | Cylindrical | Box for caps |
| Sphere/planet | Spherical | Cube-mapped |
| Character torso | Cylindrical | Manual UV |
| Complex prop | Box (triplanar) | - |
| Terrain | Planar (Y-axis) | Triplanar blend |

## Best Practices

1. **Consistent texel density**: Scale UVs so texture pixels are similar size across mesh
2. **Hide seams**: Place cylindrical/spherical seams on less visible areas
3. **Avoid stretching**: Use box projection for varied surfaces
4. **Test with checker**: Apply checkerboard texture to visualize distortion
5. **Consider tiling**: For seamless textures, ensure UVs tile properly
