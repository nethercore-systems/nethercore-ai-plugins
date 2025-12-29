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

```rust
use glam::Vec3;

fn planar_projection(
    mesh: &mut MeshUV,
    axis: Axis,
    scale: f32,
    offset: [f32; 2],
) {
    for i in 0..mesh.positions.len() {
        let pos = Vec3::from(mesh.positions[i]);

        let uv = match axis {
            Axis::Y => [
                pos.x / scale + offset[0] + 0.5,
                pos.z / scale + offset[1] + 0.5,
            ],
            Axis::X => [
                pos.z / scale + offset[0] + 0.5,
                pos.y / scale + offset[1] + 0.5,
            ],
            Axis::Z => [
                pos.x / scale + offset[0] + 0.5,
                pos.y / scale + offset[1] + 0.5,
            ],
        };

        mesh.uvs[i] = uv;
    }
}
```

### Rotated Planar

Project along arbitrary direction:

```rust
fn rotated_planar_projection(
    mesh: &mut MeshUV,
    forward: Vec3,  // Projection direction
    up: Vec3,       // Up reference
    scale: f32,
) {
    let right = forward.cross(up).normalize();
    let proj_up = right.cross(forward).normalize();

    for i in 0..mesh.positions.len() {
        let pos = Vec3::from(mesh.positions[i]);

        mesh.uvs[i] = [
            pos.dot(right) / scale + 0.5,
            pos.dot(proj_up) / scale + 0.5,
        ];
    }
}
```

## Box/Triplanar Projection

Projects based on face normal direction - best for complex shapes.

```rust
fn box_projection(mesh: &mut MeshUV, scale: f32) {
    for i in 0..mesh.positions.len() {
        let pos = Vec3::from(mesh.positions[i]);
        let normal = Vec3::from(mesh.normals[i]);

        let abs_normal = normal.abs();

        // Choose projection axis based on dominant normal
        let uv = if abs_normal.x >= abs_normal.y && abs_normal.x >= abs_normal.z {
            // X-facing: project onto YZ plane
            [pos.z / scale + 0.5, pos.y / scale + 0.5]
        } else if abs_normal.y >= abs_normal.z {
            // Y-facing: project onto XZ plane
            [pos.x / scale + 0.5, pos.z / scale + 0.5]
        } else {
            // Z-facing: project onto XY plane
            [pos.x / scale + 0.5, pos.y / scale + 0.5]
        };

        mesh.uvs[i] = uv;
    }
}
```

### Blended Triplanar

Smooth transitions between projections:

```rust
fn triplanar_blend(
    pos: Vec3,
    normal: Vec3,
    scale: f32,
    blend_sharpness: f32,
) -> [f32; 2] {
    // Calculate blend weights from normal
    let abs_n = normal.abs();
    let mut weights = Vec3::new(
        abs_n.x.powf(blend_sharpness),
        abs_n.y.powf(blend_sharpness),
        abs_n.z.powf(blend_sharpness),
    );
    weights /= weights.x + weights.y + weights.z;  // Normalize

    // Sample each projection
    let uv_x = [pos.z / scale, pos.y / scale];  // YZ plane
    let uv_y = [pos.x / scale, pos.z / scale];  // XZ plane
    let uv_z = [pos.x / scale, pos.y / scale];  // XY plane

    // Blend UVs
    [
        uv_x[0] * weights.x + uv_y[0] * weights.y + uv_z[0] * weights.z,
        uv_x[1] * weights.x + uv_y[1] * weights.y + uv_z[1] * weights.z,
    ]
}
```

## Cylindrical Projection

Best for pillars, barrels, and character torsos.

```rust
use std::f32::consts::PI;

fn cylindrical_projection(
    mesh: &mut MeshUV,
    axis: Axis,
    height_scale: f32,
    seam_angle: f32,  // Radians, where to place the UV seam
) {
    for i in 0..mesh.positions.len() {
        let pos = Vec3::from(mesh.positions[i]);

        let (angle, height) = match axis {
            Axis::Y => (pos.x.atan2(pos.z), pos.y),
            Axis::X => (pos.y.atan2(pos.z), pos.x),
            Axis::Z => (pos.x.atan2(pos.y), pos.z),
        };

        // Normalize angle to [0, 1], accounting for seam
        let mut u = (angle - seam_angle) / (2.0 * PI);
        if u < 0.0 { u += 1.0; }

        let v = height / height_scale + 0.5;

        mesh.uvs[i] = [u, v];
    }
}
```

### Handling Seams

Duplicate vertices along seams for proper texture continuity:

```rust
fn fix_cylindrical_seam(mesh: &mut MeshUV, seam_threshold: f32) {
    let original_count = mesh.positions.len();

    for tri_idx in (0..mesh.triangles.len()).step_by(3) {
        let i0 = mesh.triangles[tri_idx] as usize;
        let i1 = mesh.triangles[tri_idx + 1] as usize;
        let i2 = mesh.triangles[tri_idx + 2] as usize;

        // Check for UV discontinuity (crosses seam)
        let u0 = mesh.uvs[i0][0];
        let u1 = mesh.uvs[i1][0];
        let u2 = mesh.uvs[i2][0];

        let max_u = u0.max(u1).max(u2);
        let min_u = u0.min(u1).min(u2);

        if max_u - min_u > seam_threshold {
            // Duplicate vertices with low U and shift to U+1
            for idx in [i0, i1, i2] {
                if mesh.uvs[idx][0] < 0.5 {
                    // Duplicate vertex
                    let new_idx = mesh.positions.len() as u16;
                    mesh.positions.push(mesh.positions[idx]);
                    mesh.normals.push(mesh.normals[idx]);
                    mesh.uvs.push([mesh.uvs[idx][0] + 1.0, mesh.uvs[idx][1]]);

                    // Update triangle index
                    if mesh.triangles[tri_idx] as usize == idx {
                        mesh.triangles[tri_idx] = new_idx;
                    } else if mesh.triangles[tri_idx + 1] as usize == idx {
                        mesh.triangles[tri_idx + 1] = new_idx;
                    } else {
                        mesh.triangles[tri_idx + 2] = new_idx;
                    }
                }
            }
        }
    }
}
```

## Spherical Projection

For planets, orbs, and rounded objects.

```rust
fn spherical_projection(mesh: &mut MeshUV) {
    for i in 0..mesh.positions.len() {
        let pos = Vec3::from(mesh.positions[i]).normalize();

        // Equirectangular projection
        let u = 0.5 + pos.x.atan2(pos.z) / (2.0 * PI);
        let v = 0.5 - pos.y.asin() / PI;

        mesh.uvs[i] = [u, v];
    }
}
```

### Polar Fix

Reduce pinching at poles by averaging:

```rust
fn fix_polar_pinching(mesh: &mut MeshUV, pole_threshold: f32) {
    // Find vertices near poles
    for i in 0..mesh.positions.len() {
        let pos = Vec3::from(mesh.positions[i]).normalize();

        if pos.y.abs() > 1.0 - pole_threshold {
            // At pole - average U from connected vertices
            let connected = find_connected_vertices(mesh, i);
            let avg_u: f32 = connected.iter()
                .map(|&j| mesh.uvs[j][0])
                .sum::<f32>() / connected.len() as f32;

            mesh.uvs[i][0] = avg_u;
        }
    }
}
```

## Per-Face Projection

Each face gets [0,1] UV range - good for cube-style texturing.

```rust
fn per_face_projection(mesh: &mut MeshUV) {
    // Need to duplicate vertices for unique UVs per face
    let mut new_positions = Vec::new();
    let mut new_normals = Vec::new();
    let mut new_uvs = Vec::new();
    let mut new_triangles = Vec::new();

    for tri_idx in (0..mesh.triangles.len()).step_by(3) {
        let i0 = mesh.triangles[tri_idx] as usize;
        let i1 = mesh.triangles[tri_idx + 1] as usize;
        let i2 = mesh.triangles[tri_idx + 2] as usize;

        let base_idx = new_positions.len() as u16;

        // Duplicate vertices
        new_positions.push(mesh.positions[i0]);
        new_positions.push(mesh.positions[i1]);
        new_positions.push(mesh.positions[i2]);

        new_normals.push(mesh.normals[i0]);
        new_normals.push(mesh.normals[i1]);
        new_normals.push(mesh.normals[i2]);

        // Calculate face-local UVs
        let uvs = calculate_face_uvs(
            &mesh.positions[i0],
            &mesh.positions[i1],
            &mesh.positions[i2],
        );
        new_uvs.extend_from_slice(&uvs);

        new_triangles.push(base_idx);
        new_triangles.push(base_idx + 1);
        new_triangles.push(base_idx + 2);
    }

    mesh.positions = new_positions;
    mesh.normals = new_normals;
    mesh.uvs = new_uvs;
    mesh.triangles = new_triangles;
}

fn calculate_face_uvs(p0: &[f32; 3], p1: &[f32; 3], p2: &[f32; 3]) -> [[f32; 2]; 3] {
    let v0 = Vec3::from(*p0);
    let v1 = Vec3::from(*p1);
    let v2 = Vec3::from(*p2);

    // Use edge vectors to determine UV orientation
    let e1 = v1 - v0;
    let e2 = v2 - v0;
    let normal = e1.cross(e2).normalize();

    // Choose UV axes based on face orientation
    let (u_axis, v_axis) = if normal.y.abs() > normal.x.abs() && normal.y.abs() > normal.z.abs() {
        (Vec3::X, Vec3::Z)
    } else if normal.x.abs() > normal.z.abs() {
        (Vec3::Z, Vec3::Y)
    } else {
        (Vec3::X, Vec3::Y)
    };

    // Project vertices onto UV plane
    [
        [v0.dot(u_axis), v0.dot(v_axis)],
        [v1.dot(u_axis), v1.dot(v_axis)],
        [v2.dot(u_axis), v2.dot(v_axis)],
    ]
}
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
