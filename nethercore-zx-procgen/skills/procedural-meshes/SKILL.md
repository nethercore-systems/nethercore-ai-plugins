---
name: Procedural Mesh Generation
description: This skill should be used when the user asks to "generate mesh", "create 3D model", "procedural geometry", "low-poly model", "mesh modifiers", "combine meshes", "subdivide", "mirror mesh", "generate character mesh", "create vehicle", "procedural prop", "vertex colors", "vertex color mesh", "color per vertex", or mentions mesh generation, geometry synthesis, vertex manipulation, vertex coloring, or procedural 3D modeling for game assets. Provides comprehensive guidance for creating procedural meshes with optional UV mapping and vertex colors using any language/tool that outputs OBJ files compatible with the Nethercore asset pipeline.
version: 1.1.0
---

# Procedural Mesh Generation

## Overview

Procedural meshes are generated algorithmically, enabling parametric control, infinite variation, and automated asset pipelines. The output must be OBJ files (or GLTF) that `nether pack` can convert and bundle into a ROM.

**Output Requirements for ZX:**
- Format: OBJ (preferred), GLTF, or .nczxmesh (native binary)
- Triangles only: Quads are auto-triangulated, but triangles are cleaner
- Vertex limit: ~65k vertices per mesh (u16 indices)
- Y-up coordinate system, right-handed

### Optional Vertex Attributes

ZX supports multiple vertex formats. Choose based on your needs:

| Attribute | Required? | Use When |
|-----------|-----------|----------|
| **Position** | Yes | Always needed |
| **Normal** | Optional | For lighting (Modes 1-3). Flat-shaded without. |
| **UV** | Optional | For textured materials. Skip for vertex-colored only. |
| **Vertex Color** | Optional | For per-vertex coloring, gradients, baked AO |

**Choose what you need:** Simple meshes can skip UVs (use `set_color()` tint). Stylized games may use only vertex colors. Detailed materials need UVs. Mix as appropriate.

**Poly Budget Guidelines:**
| Use Case | Triangle Budget | Notes |
|----------|-----------------|-------|
| Swarm/crowd entities | 50-150 tris | Many instances on screen |
| Characters | 200-500 tris | Balance detail vs. count |
| Vehicles | 300-800 tris | More detail acceptable |
| Props | 50-300 tris | Depends on prominence |
| Hero/close-up | 500-2000 tris | Fewer but more detailed |

## Language/Tool Options

Choose the tool that fits your workflow:

| Tool | Best For | Output |
|------|----------|--------|
| **Rust + proc-gen** | Integration with pipeline, modifiers | OBJ via `write_obj()` |
| **Python + trimesh** | Rapid prototyping, boolean ops | OBJ via `export()` |
| **Blender Python** | Complex procedural modeling | OBJ/GLTF export |
| **Houdini** | Professional procedural workflows | OBJ export |
| **Processing/p5.js** | Creative geometry experiments | Custom OBJ writer |
| **OpenSCAD** | CSG-based solid modeling | STL→OBJ conversion |

## Using the Rust proc-gen Library

The `nethercore/tools/proc-gen/` crate provides mesh primitives and modifiers.

### Source Files (Canonical Reference)

| File | Purpose |
|------|---------|
| `nethercore-zx/src/procedural/primitives.rs` | Basic shape generators |
| `nethercore-zx/src/procedural/types.rs` | MeshBuilder trait, UnpackedMesh |
| `nethercore-zx/src/procedural/export.rs` | OBJ file writing |
| `proc-gen/src/mesh/mod.rs` | Re-exports and module entry |
| `proc-gen/src/mesh/modifiers.rs` | Transform, Subdivide, Mirror, etc. |
| `proc-gen/src/mesh/combine.rs` | Mesh merging utilities |

### Quick Start (Rust)

```rust
use proc_gen::mesh::*;

fn main() {
    // Generate a sphere as UnpackedMesh (f32 format for modifiers)
    let mut mesh: UnpackedMesh = generate_sphere(1.0, 16, 8);

    // Apply modifiers
    mesh.apply(Transform::scale(1.0, 1.5, 1.0)); // Stretch vertically
    mesh.apply(SmoothNormals);

    // Export to OBJ
    write_obj(&mesh, "assets/meshes/egg.obj", "egg").unwrap();
}
```

### Cargo.toml Setup

```toml
[package]
name = "my-mesh-gen"
version = "0.1.0"
edition = "2021"

[dependencies]
proc-gen = { path = "../nethercore/tools/proc-gen" }
glam = "0.27"
```

## Primitive Generators

All primitives are generic over `MeshBuilder` trait, outputting either:
- `MeshData`: Packed GPU format (for runtime FFI)
- `UnpackedMesh`: f32 format (for modifiers and OBJ export)

### Cube

```rust
let mesh: UnpackedMesh = generate_cube(size_x, size_y, size_z);
```

Creates a box with specified dimensions centered at origin.

### Sphere

```rust
let mesh: UnpackedMesh = generate_sphere(radius, segments, rings);
```

**Parameters:**
- `segments`: Horizontal divisions (8-32 typical)
- `rings`: Vertical divisions (4-16 typical)

**Poly count:** ~`segments × rings × 2` triangles

### Cylinder

```rust
let mesh: UnpackedMesh = generate_cylinder(
    radius_bottom,
    radius_top,  // Different radii = cone
    height,
    segments,
);
```

### Capsule

```rust
let mesh: UnpackedMesh = generate_capsule(radius, height, segments, rings);
```

Sphere-capped cylinder. Great for characters and collision volumes.

### Torus

```rust
let mesh: UnpackedMesh = generate_torus(
    major_radius,  // Ring radius
    minor_radius,  // Tube radius
    major_segments,
    minor_segments,
);
```

### Plane

```rust
let mesh: UnpackedMesh = generate_plane(
    size_x,
    size_z,
    subdivisions_x,
    subdivisions_z,
);
```

Flat surface in XZ plane, centered at origin.

## Mesh Modifiers

Modifiers operate on `UnpackedMesh` and can be chained:

### Transform

```rust
use glam::{Mat4, Vec3};

mesh.apply(Transform::translate(0.0, 1.0, 0.0));
mesh.apply(Transform::rotate_y(45.0_f32.to_radians()));
mesh.apply(Transform::scale(2.0, 1.0, 2.0));
mesh.apply(Transform::from_matrix(Mat4::from_rotation_x(0.5)));
```

### Subdivide

```rust
mesh.apply(Subdivide { iterations: 1 });
```

Midpoint subdivision. Each iteration quadruples triangle count.

**Use cases:** Smoothing low-poly base shapes, organic surfaces

### Mirror

```rust
mesh.apply(Mirror {
    axis: Axis::X,
    merge_threshold: 0.001,
});
```

Mirrors geometry across axis plane, merging vertices at seam.

**Use cases:** Symmetric characters, vehicles, buildings

### SmoothNormals / FlatNormals

```rust
mesh.apply(SmoothNormals);  // Averaged normals for smooth shading
mesh.apply(FlatNormals);    // Face normals for faceted look
```

### Chamfer

```rust
mesh.apply(Chamfer {
    amount: 0.1,
    segments: 2,
});
```

Rounds hard edges. Great for armor, vehicles, industrial props.

## Combining Meshes

### Simple Combine

```rust
let combined = combine(&[&mesh1, &mesh2, &mesh3]);
```

Merges meshes at their current positions.

### Transformed Combine

```rust
let parts = vec![
    (&torso, Mat4::IDENTITY),
    (&head, Mat4::from_translation(Vec3::new(0.0, 1.5, 0.0))),
    (&arm_l, Mat4::from_translation(Vec3::new(-0.8, 1.0, 0.0))),
    (&arm_r, Mat4::from_translation(Vec3::new(0.8, 1.0, 0.0))),
];
let character = combine_transformed(&parts);
```

## Building Custom Geometry

When primitives aren't enough, build from triangles:

```rust
fn generate_pyramid(base: f32, height: f32) -> UnpackedMesh {
    let mut mesh = UnpackedMesh::default();

    // Base vertices (square in XZ plane)
    let half = base / 2.0;
    let v0 = mesh.add_vertex(Vec3::new(-half, 0.0, -half), Vec3::Y);
    let v1 = mesh.add_vertex(Vec3::new(half, 0.0, -half), Vec3::Y);
    let v2 = mesh.add_vertex(Vec3::new(half, 0.0, half), Vec3::Y);
    let v3 = mesh.add_vertex(Vec3::new(-half, 0.0, half), Vec3::Y);

    // Apex
    let apex = mesh.add_vertex(Vec3::new(0.0, height, 0.0), Vec3::Y);

    // Base triangles
    mesh.add_triangle(v0, v2, v1);
    mesh.add_triangle(v0, v3, v2);

    // Side faces (calculate proper normals for each)
    // ... add side triangles with face normals

    mesh.apply(FlatNormals); // Recalculate normals
    mesh
}
```

## Python Alternative

Using trimesh for procedural modeling:

```python
import trimesh
import numpy as np

def generate_crystal(height, radius, facets):
    """Generate a double-ended crystal shape."""
    # Create base hexagonal prism
    angles = np.linspace(0, 2 * np.pi, facets, endpoint=False)
    base_verts = np.column_stack([
        radius * np.cos(angles),
        np.zeros(facets),
        radius * np.sin(angles)
    ])

    # Add top and bottom points
    top = np.array([[0, height * 0.7, 0]])
    bottom = np.array([[0, -height * 0.3, 0]])
    vertices = np.vstack([base_verts, top, bottom])

    # Create faces (triangles from base to tips)
    faces = []
    for i in range(facets):
        next_i = (i + 1) % facets
        faces.append([i, next_i, facets])      # Top cone
        faces.append([next_i, i, facets + 1])  # Bottom cone

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.export("assets/meshes/crystal.obj")
    return mesh

generate_crystal(2.0, 0.5, 6)
```

## Blender Python

For complex procedural modeling in Blender:

```python
import bpy
import bmesh
import math

def generate_gear(teeth, radius, thickness):
    bm = bmesh.new()

    angle_step = 2 * math.pi / teeth
    for i in range(teeth):
        angle = i * angle_step
        # Tooth geometry...
        # (complex geometry code)

    mesh = bpy.data.meshes.new("gear")
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("gear", mesh)
    bpy.context.collection.objects.link(obj)

    # Export
    bpy.ops.export_scene.obj(
        filepath="//assets/meshes/gear.obj",
        use_selection=True,
        use_triangles=True
    )

generate_gear(12, 1.0, 0.2)
```

## Integration with Nethercore

### Asset Pipeline

1. Generate OBJ files to `assets/meshes/`
2. Reference in `nether.toml`:
```toml
[[assets.meshes]]
id = "my-mesh"
path = "assets/meshes/my-mesh.obj"
```
3. Run `nether pack` (auto-converts OBJ to packed format)
4. Load in game with `rom_mesh_str("my-mesh")`

### Best Practices

1. **Respect poly budgets**: Count triangles, not quads
2. **Triangulate before export**: Avoid quad-to-tri artifacts
3. **Center at origin**: Makes transforms predictable
4. **Y-up convention**: Nethercore uses Y-up coordinate system
5. **Merge close vertices**: Avoid seam artifacts
6. **Test in viewer**: Use proc-gen-viewer to preview

## Modifier Chaining Pattern

Build complex shapes from simple operations:

```rust
fn generate_character_body() -> UnpackedMesh {
    // Start with capsule torso
    let mut torso: UnpackedMesh = generate_capsule(0.4, 0.8, 8, 4);
    torso.apply(Transform::scale(1.0, 1.2, 0.8));

    // Head (sphere)
    let mut head: UnpackedMesh = generate_sphere(0.25, 8, 6);
    head.apply(Transform::translate(0.0, 1.0, 0.0));

    // Combine and smooth
    let mut body = combine(&[&torso, &head]);
    body.apply(SmoothNormals);

    body
}
```

## UV Mapping for Textured Meshes

Procedural meshes need proper UV coordinates to display textures correctly. ZX uses UV coordinates in the standard [0,1] range.

### UV-Mapped Primitive Variants

All primitives have `_uv` variants that include UV coordinates:

```rust
// Standard variants (no UVs)
let cube: UnpackedMesh = generate_cube(1.0, 1.0, 1.0);
let sphere: UnpackedMesh = generate_sphere(1.0, 16, 8);

// UV-mapped variants
let cube_uv: UnpackedMeshUV = generate_cube_uv(1.0, 1.0, 1.0);
let sphere_uv: UnpackedMeshUV = generate_sphere_uv(1.0, 16, 8);
let cylinder_uv: UnpackedMeshUV = generate_cylinder_uv(0.5, 0.5, 2.0, 16);
let plane_uv: UnpackedMeshUV = generate_plane_uv(4.0, 4.0, 4, 4);
```

### Default UV Layouts

| Primitive | UV Mapping |
|-----------|------------|
| **Cube** | Each face mapped [0,1]×[0,1], unfolded (6 separate texture regions) |
| **Sphere** | Equirectangular (longitude/latitude), seam at back |
| **Cylinder** | Cylindrical for sides (wrapped), planar for caps |
| **Plane** | Direct XZ to UV mapping, origin at center |
| **Capsule** | Cylindrical for body, spherical for caps |
| **Torus** | Two-parameter surface mapping |

### UV Projection Techniques

#### Planar Projection

Best for flat or mostly-flat surfaces:

```rust
fn apply_planar_uv(mesh: &mut UnpackedMeshUV, axis: Axis, scale: f32) {
    for i in 0..mesh.positions.len() {
        let pos = mesh.positions[i];
        let uv = match axis {
            Axis::Y => [(pos[0] / scale + 0.5), (pos[2] / scale + 0.5)],
            Axis::X => [(pos[2] / scale + 0.5), (pos[1] / scale + 0.5)],
            Axis::Z => [(pos[0] / scale + 0.5), (pos[1] / scale + 0.5)],
        };
        mesh.uvs[i] = uv;
    }
}

// Usage: floor, walls, terrain patches
let mut floor = generate_plane_uv(10.0, 10.0, 1, 1);
apply_planar_uv(&mut floor, Axis::Y, 2.0); // Tile texture every 2 units
```

#### Cylindrical Projection

Best for curved surfaces like barrels, pillars, characters:

```rust
fn apply_cylindrical_uv(mesh: &mut UnpackedMeshUV, axis: Axis, scale: f32) {
    for i in 0..mesh.positions.len() {
        let pos = mesh.positions[i];

        // Calculate angle around axis
        let (angle, height) = match axis {
            Axis::Y => (pos[0].atan2(pos[2]), pos[1]),
            Axis::X => (pos[1].atan2(pos[2]), pos[0]),
            Axis::Z => (pos[0].atan2(pos[1]), pos[2]),
        };

        // Map angle to U [0,1], height to V
        let u = (angle / (2.0 * PI) + 0.5).fract();
        let v = height / scale + 0.5;

        mesh.uvs[i] = [u, v];
    }
}
```

#### Spherical Projection

Best for round objects:

```rust
fn apply_spherical_uv(mesh: &mut UnpackedMeshUV) {
    for i in 0..mesh.positions.len() {
        let pos = Vec3::from(mesh.positions[i]).normalize();

        // Equirectangular projection
        let u = 0.5 + pos.x.atan2(pos.z) / (2.0 * PI);
        let v = 0.5 - pos.y.asin() / PI;

        mesh.uvs[i] = [u, v];
    }
}
```

#### Box Projection (Triplanar)

Best for complex shapes, avoids stretching:

```rust
fn apply_box_uv(mesh: &mut UnpackedMeshUV, scale: f32) {
    for i in 0..mesh.positions.len() {
        let pos = mesh.positions[i];
        let normal = mesh.normals[i];

        // Project based on dominant normal axis
        let abs_normal = [normal[0].abs(), normal[1].abs(), normal[2].abs()];

        let uv = if abs_normal[0] >= abs_normal[1] && abs_normal[0] >= abs_normal[2] {
            // X-facing: use Y,Z
            [pos[2] / scale, pos[1] / scale]
        } else if abs_normal[1] >= abs_normal[2] {
            // Y-facing: use X,Z
            [pos[0] / scale, pos[2] / scale]
        } else {
            // Z-facing: use X,Y
            [pos[0] / scale, pos[1] / scale]
        };

        mesh.uvs[i] = [(uv[0] + 0.5).fract(), (uv[1] + 0.5).fract()];
    }
}
```

### Building Custom Geometry with UVs

```rust
fn generate_textured_ramp(width: f32, height: f32, depth: f32) -> UnpackedMeshUV {
    let mut mesh = UnpackedMeshUV::default();

    // Front face (sloped)
    let v0 = mesh.add_vertex_uv(
        Vec3::new(-width/2.0, 0.0, depth/2.0),
        [0.0, 0.0],
        Vec3::new(0.0, depth, height).normalize()
    );
    let v1 = mesh.add_vertex_uv(
        Vec3::new(width/2.0, 0.0, depth/2.0),
        [1.0, 0.0],
        Vec3::new(0.0, depth, height).normalize()
    );
    let v2 = mesh.add_vertex_uv(
        Vec3::new(width/2.0, height, -depth/2.0),
        [1.0, 1.0],
        Vec3::new(0.0, depth, height).normalize()
    );
    let v3 = mesh.add_vertex_uv(
        Vec3::new(-width/2.0, height, -depth/2.0),
        [0.0, 1.0],
        Vec3::new(0.0, depth, height).normalize()
    );

    mesh.add_triangle(v0, v1, v2);
    mesh.add_triangle(v0, v2, v3);

    // Add other faces with appropriate UVs...

    mesh
}
```

### UV Tiling and Scale

Control texture repetition with UV scale:

```rust
fn scale_uvs(mesh: &mut UnpackedMeshUV, scale_u: f32, scale_v: f32) {
    for uv in &mut mesh.uvs {
        uv[0] *= scale_u;
        uv[1] *= scale_v;
    }
}

// Tile texture 4x4 across surface
let mut wall = generate_plane_uv(8.0, 8.0, 1, 1);
scale_uvs(&mut wall, 4.0, 4.0);  // Texture repeats 4 times in each direction
```

### UV Export in OBJ

```rust
fn write_obj_uv(mesh: &UnpackedMeshUV, path: &str, name: &str) -> std::io::Result<()> {
    let mut file = File::create(path)?;

    writeln!(file, "# {}", name)?;

    // Vertices
    for pos in &mesh.positions {
        writeln!(file, "v {} {} {}", pos[0], pos[1], pos[2])?;
    }

    // Texture coordinates
    for uv in &mesh.uvs {
        writeln!(file, "vt {} {}", uv[0], uv[1])?;
    }

    // Normals
    for normal in &mesh.normals {
        writeln!(file, "vn {} {} {}", normal[0], normal[1], normal[2])?;
    }

    // Faces (v/vt/vn format)
    for tri in mesh.triangles.chunks(3) {
        writeln!(file, "f {0}/{0}/{0} {1}/{1}/{1} {2}/{2}/{2}",
            tri[0] + 1, tri[1] + 1, tri[2] + 1)?;
    }

    Ok(())
}
```

### Python UV Generation

```python
import trimesh
import numpy as np

def create_uv_mapped_mesh(vertices, faces, projection='box'):
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    if projection == 'box':
        # Box/triplanar projection
        uvs = np.zeros((len(vertices), 2))
        for i, (v, n) in enumerate(zip(vertices, mesh.vertex_normals)):
            abs_n = np.abs(n)
            if abs_n[0] >= abs_n[1] and abs_n[0] >= abs_n[2]:
                uvs[i] = [v[2], v[1]]
            elif abs_n[1] >= abs_n[2]:
                uvs[i] = [v[0], v[2]]
            else:
                uvs[i] = [v[0], v[1]]
        mesh.visual = trimesh.visual.TextureVisuals(uv=uvs)

    elif projection == 'cylindrical':
        angles = np.arctan2(vertices[:, 0], vertices[:, 2])
        uvs = np.column_stack([
            (angles / (2 * np.pi) + 0.5) % 1.0,
            vertices[:, 1]
        ])
        mesh.visual = trimesh.visual.TextureVisuals(uv=uvs)

    return mesh
```

### UV Best Practices

1. **Minimize stretching**: Use appropriate projection for surface orientation
2. **Consistent texel density**: Keep UV scale uniform across the mesh
3. **Seam placement**: Hide UV seams on less visible areas
4. **Margin for mip-mapping**: Leave small gaps between UV islands
5. **Atlas packing**: Combine small UV islands efficiently

### Integration with ZX Material Textures

When using Mode 2 (MRE) or Mode 3 (SSE) materials, all textures share the same UV coordinates:

```rust
// Load a UV-mapped mesh
let mesh = rom_mesh_str("character");
mesh_draw(mesh);

// All material textures use the mesh's UVs
texture_bind(albedo_tex);       // Slot 0
material_mre(mre_tex);          // Slot 1 - uses same UVs as albedo

// Or for Mode 3:
texture_bind(albedo_tex);       // Slot 0
// SSE and specular textures also share UVs
```

**Tip:** Generate all material textures at the same resolution and with matching features so they align properly on the UV-mapped mesh.

---

## Vertex Colors

Vertex colors store RGBA values per-vertex, enabling per-vertex tinting, gradients, baked lighting, and stylized art without textures.

### When to Use Vertex Colors

| Use Case | Description |
|----------|-------------|
| **Stylized/Low-Poly** | No UVs needed, color directly on geometry |
| **Baked Ambient Occlusion** | Store AO in vertex alpha or as grayscale |
| **Color Gradients** | Smooth color transitions (sky, lava, etc.) |
| **Terrain Blending** | Blend weights for multi-texture terrain |
| **Team Colors** | Tint regions differently at runtime |
| **Performance** | Avoid texture sampling overhead |

### Vertex Color Format

ZX uses RGBA8 vertex colors (4 bytes per vertex):
- **R, G, B**: Color channels (0-255)
- **A**: Alpha (can be used for transparency or data)

Vertex colors are **multiplied** with the albedo texture (or base `set_color()`).

### Rust: Vertex-Colored Mesh Generation

```rust
use proc_gen::mesh::*;

/// Mesh with vertex colors (no UVs)
struct UnpackedMeshColor {
    positions: Vec<[f32; 3]>,
    normals: Vec<[f32; 3]>,
    colors: Vec<[u8; 4]>,  // RGBA per vertex
    triangles: Vec<u16>,
}

impl UnpackedMeshColor {
    fn add_vertex_color(
        &mut self,
        pos: Vec3,
        normal: Vec3,
        color: u32,  // 0xRRGGBBAA
    ) -> u16 {
        let idx = self.positions.len() as u16;
        self.positions.push(pos.into());
        self.normals.push(normal.into());
        self.colors.push([
            ((color >> 24) & 0xFF) as u8,
            ((color >> 16) & 0xFF) as u8,
            ((color >> 8) & 0xFF) as u8,
            (color & 0xFF) as u8,
        ]);
        idx
    }
}

fn generate_gradient_cube() -> UnpackedMeshColor {
    let mut mesh = UnpackedMeshColor::default();

    // Bottom vertices (dark blue)
    let bottom_color = 0x2244AAFF;
    // Top vertices (light cyan)
    let top_color = 0x88EEFFFF;

    // Create cube with vertical gradient
    let positions = [
        // Bottom face (y = -0.5)
        (Vec3::new(-0.5, -0.5, -0.5), bottom_color),
        (Vec3::new( 0.5, -0.5, -0.5), bottom_color),
        (Vec3::new( 0.5, -0.5,  0.5), bottom_color),
        (Vec3::new(-0.5, -0.5,  0.5), bottom_color),
        // Top face (y = 0.5)
        (Vec3::new(-0.5,  0.5, -0.5), top_color),
        (Vec3::new( 0.5,  0.5, -0.5), top_color),
        (Vec3::new( 0.5,  0.5,  0.5), top_color),
        (Vec3::new(-0.5,  0.5,  0.5), top_color),
    ];

    // Add vertices with colors...
    // (Add triangles for all 6 faces)

    mesh
}
```

### Height-Based Coloring

Common pattern for terrain and props:

```rust
fn apply_height_gradient(
    mesh: &mut UnpackedMeshColor,
    low_color: u32,
    high_color: u32,
    min_y: f32,
    max_y: f32,
) {
    for i in 0..mesh.positions.len() {
        let y = mesh.positions[i][1];
        let t = ((y - min_y) / (max_y - min_y)).clamp(0.0, 1.0);

        // Lerp colors
        let lr = ((low_color >> 24) & 0xFF) as f32;
        let lg = ((low_color >> 16) & 0xFF) as f32;
        let lb = ((low_color >> 8) & 0xFF) as f32;
        let hr = ((high_color >> 24) & 0xFF) as f32;
        let hg = ((high_color >> 16) & 0xFF) as f32;
        let hb = ((high_color >> 8) & 0xFF) as f32;

        mesh.colors[i] = [
            (lr + (hr - lr) * t) as u8,
            (lg + (hg - lg) * t) as u8,
            (lb + (hb - lb) * t) as u8,
            255,
        ];
    }
}

// Example: Mountain with snow peaks
let mut mountain = generate_terrain_mesh();
apply_height_gradient(
    &mut mountain,
    0x4A6B35FF,  // Green at base
    0xFFFFFFFF,  // White at peaks
    0.0,         // Base height
    10.0,        // Peak height
);
```

### Baked Ambient Occlusion

Store AO in vertex colors for cheap shadowing:

```rust
fn bake_vertex_ao(mesh: &mut UnpackedMeshColor, ray_count: u32) {
    for i in 0..mesh.positions.len() {
        let pos = Vec3::from(mesh.positions[i]);
        let normal = Vec3::from(mesh.normals[i]);

        // Cast rays in hemisphere above vertex
        let mut occlusion = 0.0;
        for _ in 0..ray_count {
            let ray_dir = random_hemisphere_direction(normal);
            if mesh_ray_intersects(mesh, pos + normal * 0.01, ray_dir, 2.0) {
                occlusion += 1.0 / ray_count as f32;
            }
        }

        // Store AO as grayscale (darker = more occluded)
        let ao = ((1.0 - occlusion) * 255.0) as u8;
        mesh.colors[i] = [ao, ao, ao, 255];
    }
}
```

### Python Vertex Colors

Using trimesh with vertex colors:

```python
import trimesh
import numpy as np

def create_gradient_sphere(radius, segments, color_bottom, color_top):
    """Create sphere with vertical color gradient."""
    mesh = trimesh.creation.icosphere(subdivisions=2, radius=radius)

    # Calculate colors based on vertex height
    heights = mesh.vertices[:, 1]  # Y coordinate
    min_h, max_h = heights.min(), heights.max()
    t = (heights - min_h) / (max_h - min_h)

    # Interpolate colors
    cb = np.array([(color_bottom >> 24) & 0xFF,
                   (color_bottom >> 16) & 0xFF,
                   (color_bottom >> 8) & 0xFF, 255]) / 255.0
    ct = np.array([(color_top >> 24) & 0xFF,
                   (color_top >> 16) & 0xFF,
                   (color_top >> 8) & 0xFF, 255]) / 255.0

    colors = np.outer(1 - t, cb) + np.outer(t, ct)
    mesh.visual.vertex_colors = (colors * 255).astype(np.uint8)

    return mesh

# Fiery orb: red at bottom, yellow at top
orb = create_gradient_sphere(1.0, 16, 0xFF2200FF, 0xFFDD00FF)
orb.export("assets/meshes/fire_orb.glb")  # GLTF preserves vertex colors
```

### Export Formats with Vertex Colors

| Format | Vertex Color Support | Notes |
|--------|---------------------|-------|
| **OBJ** | ❌ No | Standard OBJ has no vertex color |
| **OBJ (extended)** | ⚠️ Unofficial | Some tools support `v x y z r g b` |
| **GLTF/GLB** | ✅ Yes | Full RGBA support, recommended |
| **PLY** | ✅ Yes | Common for scanned meshes |
| **FBX** | ✅ Yes | Full support |

**Recommendation:** Use GLTF/GLB for vertex-colored meshes. The `nether pack` tool handles GLTF properly.

### GLTF Export with Vertex Colors (Python)

```python
import trimesh

def export_colored_mesh(mesh, path):
    """Export mesh with vertex colors to GLTF."""
    # Ensure vertex colors are set
    if mesh.visual.vertex_colors is None:
        raise ValueError("Mesh has no vertex colors")

    # Export as GLB (binary GLTF)
    mesh.export(path, file_type='glb')

# Usage
mesh = create_gradient_sphere(1.0, 16, 0xFF0000FF, 0x00FF00FF)
export_colored_mesh(mesh, "assets/meshes/gradient_sphere.glb")
```

### Vertex Colors + Textures

You can combine vertex colors with textures. The final color is:
```
final_color = texture_color × vertex_color × set_color()
```

This enables:
- Tinting textured meshes per-vertex
- AO baked in vertex alpha with full-color texture
- Team colors on textured characters

```rust
// In game code:
texture_bind(character_albedo);  // Base texture
// Vertex colors from mesh tint/darken the texture
mesh_draw(character_mesh);  // Mesh has per-vertex team colors baked in
```

### Vertex Color Best Practices

1. **Consistent lighting direction**: When baking AO/shadows, use consistent light direction across all assets
2. **Smooth gradients**: Use enough vertices for smooth color transitions
3. **Gamma awareness**: ZX uses linear color space internally; consider this when baking
4. **Alpha channel**: Use alpha for data (AO, blend weights) when RGB is for color
5. **Test without textures**: Verify vertex colors look correct before adding textures

---

## Additional Resources

- `references/primitives-reference.md` - All primitives with parameters
- `references/modifiers-reference.md` - Modifier chain patterns
- `references/uv-projections.md` - UV projection techniques
- `examples/` - Character, vehicle, prop generation examples
