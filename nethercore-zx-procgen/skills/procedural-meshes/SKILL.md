---
name: Procedural Mesh Generation
description: This skill should be used when the user asks to "generate mesh", "create 3D model", "procedural geometry", "low-poly model", "mesh modifiers", "combine meshes", "subdivide", "mirror mesh", "generate character mesh", "create vehicle", "procedural prop", "vertex colors", or mentions mesh generation, geometry synthesis, vertex manipulation, or procedural 3D modeling for game assets.
version: 1.2.0
---

# Procedural Mesh Generation

## Output Requirements

- Format: OBJ (preferred), GLTF, or .nczxmesh
- Triangles only (quads auto-triangulated)
- Vertex limit: ~65k per mesh (u16 indices)
- Y-up coordinate system, right-handed

## Vertex Attributes

| Attribute | Required? | Use When |
|-----------|-----------|----------|
| Position | Yes | Always |
| Normal | Optional | For lighting (Modes 1-3) |
| UV | Optional | For textured materials |
| Vertex Color | Optional | Per-vertex coloring, baked AO |

## Poly Budget Guidelines

| Use Case | Triangle Budget |
|----------|-----------------|
| Swarm entities | 50-150 |
| Characters | 200-500 |
| Vehicles | 300-800 |
| Props | 50-300 |
| Hero/close-up | 500-2000 |

---

## Rust Quick Start

```rust
use proc_gen::mesh::*;

fn main() {
    let mut mesh: UnpackedMesh = generate_sphere(1.0, 16, 8);
    mesh.apply(Transform::scale(1.0, 1.5, 1.0));
    mesh.apply(SmoothNormals);
    write_obj(&mesh, "assets/meshes/egg.obj", "egg").unwrap();
}
```

**Cargo.toml:**
```toml
[dependencies]
proc-gen = { path = "../nethercore/tools/proc-gen" }
glam = "0.27"
```

---

## Primitive Generators

| Primitive | Code | Notes |
|-----------|------|-------|
| Cube | `generate_cube(x, y, z)` | Box centered at origin |
| Sphere | `generate_sphere(r, segs, rings)` | ~segs×rings×2 tris |
| Cylinder | `generate_cylinder(r_bot, r_top, h, segs)` | Different radii = cone |
| Capsule | `generate_capsule(r, h, segs, rings)` | Sphere-capped, great for characters |
| Torus | `generate_torus(major_r, minor_r, maj_segs, min_segs)` | Ring shape |
| Plane | `generate_plane(x, z, subdiv_x, subdiv_z)` | Flat XZ surface |

**UV Variants:** Add `_uv` suffix: `generate_cube_uv()`, `generate_sphere_uv()`, etc.

---

## Key Modifiers

| Modifier | Effect |
|----------|--------|
| `Transform::translate/rotate_y/scale` | Position, orient, size |
| `Subdivide { iterations: N }` | Quadruples tris per iteration |
| `Mirror { axis, merge_threshold }` | Create symmetric meshes |
| `NoiseDisplace { amplitude, frequency, seed }` | Organic surface variation |
| `SmoothNormals` / `FlatNormals` | Shading style |
| `WeldVertices { threshold }` | Merge nearby verts |

For detailed modifier examples, see `references/modifiers.md`.

---

## Combining Meshes

Build complex models from parts:

```rust
use proc_gen::mesh::combine;

let head = generate_sphere(0.5, 16, 8);
let body = generate_capsule(0.3, 1.0, 12, 6);

head.apply(Transform::translate(0.0, 1.5, 0.0));
let character = combine::merge(vec![head, body]);
character.apply(WeldVertices { threshold: 0.001 });
```

For part library patterns, see `references/combining-meshes.md`.

---

## Vertex Colors

Per-vertex colors multiply with material/texture:

```rust
let mut mesh: UnpackedMeshUV = generate_cube_uv(1.0, 1.0, 1.0);
mesh.apply(VertexColorGradient {
    start_color: [64, 64, 64, 255],
    end_color: [255, 255, 255, 255],
    axis: Axis::Y,
});
```

For baked AO and color techniques, see `references/vertex-colors.md`.

---

## Python Alternative (trimesh)

```python
import trimesh

sphere = trimesh.primitives.Sphere(radius=1.0, subdivisions=2)
sphere.export("assets/meshes/sphere.obj")

# Boolean operations
a = trimesh.primitives.Sphere(radius=1.0)
b = trimesh.primitives.Box(extents=[1.5, 1.5, 1.5])
carved = a.difference(b)
carved.export("assets/meshes/carved.obj")
```

---

## nether.toml Configuration

```toml
[[assets.meshes]]
id = "player"
path = "assets/meshes/player.obj"

[[assets.meshes]]
id = "enemy"
path = "assets/meshes/enemy.gltf"
```

---

## Reference Files

- `references/primitives-reference.md` - All primitive parameters
- `references/modifiers.md` - Modifier examples and usage
- `references/vertex-colors.md` - Vertex color techniques
- `references/combining-meshes.md` - Part assembly patterns
