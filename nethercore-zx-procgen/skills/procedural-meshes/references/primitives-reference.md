# Mesh Primitives Quick Reference

## All Primitives

```rust
use proc_gen::mesh::*;

// All return UnpackedMesh by default
let cube: UnpackedMesh = generate_cube(size_x, size_y, size_z);
let sphere: UnpackedMesh = generate_sphere(radius, segments, rings);
let cylinder: UnpackedMesh = generate_cylinder(r_bottom, r_top, height, segments);
let capsule: UnpackedMesh = generate_capsule(radius, height, segments, rings);
let torus: UnpackedMesh = generate_torus(major_r, minor_r, major_segs, minor_segs);
let plane: UnpackedMesh = generate_plane(size_x, size_z, subdiv_x, subdiv_z);
```

## Triangle Counts

| Primitive | Low | Medium | High | Formula |
|-----------|-----|--------|------|---------|
| Cube | 12 | 12 | 12 | Fixed |
| Sphere | 64 | 256 | 1024 | `segs × rings × 2` |
| Cylinder | 28 | 60 | 124 | `segs × 3 + segs × 2` |
| Capsule | 80 | 288 | 1088 | Complex |
| Torus | 64 | 256 | 1024 | `major × minor × 2` |
| Plane | 8 | 32 | 128 | `subdiv_x × subdiv_z × 2` |

## Recommended Parameters

### Low Poly (Swarm/Crowd)

```rust
generate_sphere(1.0, 8, 4);      // 64 tris
generate_cube(1.0, 1.0, 1.0);    // 12 tris
generate_capsule(0.5, 1.0, 6, 2); // ~48 tris
```

### Medium Poly (Characters/Props)

```rust
generate_sphere(1.0, 12, 8);     // ~192 tris
generate_cylinder(0.5, 0.5, 2.0, 12); // ~60 tris
generate_capsule(0.5, 1.0, 12, 4); // ~160 tris
```

### High Poly (Hero Objects)

```rust
generate_sphere(1.0, 24, 12);    // ~576 tris
generate_torus(1.0, 0.3, 24, 12); // ~576 tris
generate_capsule(0.5, 1.0, 24, 8); // ~576 tris
```

## UV-Mapped Variants

For textured meshes:

```rust
let cube_uv: UnpackedMeshUV = generate_cube_uv(1.0, 1.0, 1.0);
let sphere_uv: UnpackedMeshUV = generate_sphere_uv(1.0, 16, 8);
// etc.
```

## Coordinate System

- Y-up, right-handed
- Origin at center (except plane at Y=0)
- Cube: from `-size/2` to `+size/2`
- Sphere: centered at origin
- Cylinder: bottom at Y=0, top at Y=height
- Plane: in XZ plane, centered at origin

## Source Location

`nethercore/nethercore-zx/src/procedural/primitives.rs`
