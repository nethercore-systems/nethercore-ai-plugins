# Mesh Modifiers Reference

Modifiers operate on `UnpackedMesh` and can be chained.

## Transform

```rust
use glam::{Mat4, Vec3};

mesh.apply(Transform::translate(0.0, 1.0, 0.0));
mesh.apply(Transform::rotate_y(45.0_f32.to_radians()));
mesh.apply(Transform::scale(2.0, 1.0, 2.0));
mesh.apply(Transform::from_matrix(Mat4::from_rotation_x(0.5)));
```

## Subdivide

Midpoint subdivision. Each iteration quadruples triangle count.

```rust
mesh.apply(Subdivide { iterations: 1 });
```

**Use cases:** Smoothing low-poly base shapes, organic surfaces

## Mirror

Create symmetric meshes from one half.

```rust
mesh.apply(Mirror {
    axis: Axis::X,
    merge_threshold: 0.001,
});
```

## Bend

Curve mesh along an axis.

```rust
mesh.apply(Bend {
    axis: Axis::Y,
    angle: 45.0_f32.to_radians(),
    center: 0.5,  // 0.0 = bottom, 1.0 = top
});
```

## Twist

Rotate progressively along an axis.

```rust
mesh.apply(Twist {
    axis: Axis::Y,
    angle: 90.0_f32.to_radians(),
    center: 0.5,
});
```

## Taper

Scale progressively along an axis (creates cones, tapered cylinders).

```rust
mesh.apply(Taper {
    axis: Axis::Y,
    factor: 0.5,  // 1.0 = no taper, 0.0 = point
    center: 0.0,  // Where taper is 1.0
});
```

## Noise Displacement

Add organic surface variation.

```rust
mesh.apply(NoiseDisplace {
    amplitude: 0.1,
    frequency: 2.0,
    seed: 42,
});
```

## Normals

Control shading style.

```rust
mesh.apply(SmoothNormals);   // Interpolated normals (smooth shading)
mesh.apply(FlatNormals);      // Per-face normals (faceted look)
mesh.apply(RecalculateNormals); // Recompute from geometry
```

## Weld Vertices

Merge nearby vertices (after combining meshes).

```rust
mesh.apply(WeldVertices { threshold: 0.001 });
```
