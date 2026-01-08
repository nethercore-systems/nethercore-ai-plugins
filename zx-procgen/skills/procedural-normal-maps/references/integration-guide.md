# Normal Map Integration Guide

Complete workflow for integrating normal maps with ZX meshes and materials.

## Prerequisites

Normal maps require:

1. **Mesh with tangent vertex data** (FORMAT_TANGENT flag)
2. **Mesh with UVs** (FORMAT_UV flag)
3. **Mesh with normals** (FORMAT_NORMAL flag)
4. **Normal map texture** (BC5 or RGBA format)

---

## Vertex Format Flags

```rust
// Vertex format flags (from FFI)
pub const FORMAT_UV: u8 = 1;          // Bit 0
pub const FORMAT_COLOR: u8 = 2;       // Bit 1
pub const FORMAT_NORMAL: u8 = 4;      // Bit 2
pub const FORMAT_SKINNED: u8 = 8;     // Bit 3
pub const FORMAT_TANGENT: u8 = 16;    // Bit 4 (NEW)
```

**Dependency:** FORMAT_TANGENT requires FORMAT_NORMAL. You cannot have tangents without normals.

### Common Format Combinations

| Format | Value | Description |
|--------|-------|-------------|
| POS_UV | 1 | Basic textured |
| POS_UV_NORMAL | 5 | Lit, no normal map |
| POS_UV_NORMAL_TANGENT | 21 | Lit with normal map |
| POS_UV_COLOR_NORMAL | 7 | Lit with vertex colors |
| POS_UV_COLOR_NORMAL_TANGENT | 23 | Full featured |

---

## Blender Export for Tangents

### GLB Export Settings

```python
import bpy

def export_mesh_with_tangents(obj, output_path: str):
    """Export mesh with tangent data for normal mapping."""

    # Select only this object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Calculate tangents (requires UVs)
    mesh = obj.data
    if not mesh.uv_layers:
        raise ValueError("Mesh must have UVs for tangent calculation")

    mesh.calc_tangents()

    # Export with tangents enabled
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        use_selection=True,
        export_apply_modifiers=True,
        export_normals=True,
        export_tangents=True,     # CRITICAL: Enable tangent export
        export_colors='ACTIVE',
        export_attributes=True,
        export_yup=True,
    )

    print(f"Exported with tangents: {output_path}")
```

### Post-Processing Checklist

Before export, ensure:

```python
def prepare_mesh_for_normal_mapping(obj):
    """Prepare mesh for normal map export."""
    mesh = obj.data

    # 1. Apply all modifiers
    bpy.context.view_layer.objects.active = obj
    for modifier in obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=modifier.name)

    # 2. Apply transforms
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # 3. Ensure UVs exist
    if not mesh.uv_layers:
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)

    # 4. Ensure normals are correct
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    # 5. Set smooth shading (optional but recommended)
    for face in mesh.polygons:
        face.use_smooth = True

    # 6. Calculate tangents
    mesh.calc_tangents()

    return obj
```

---

## FFI Material Binding

### Binding Normal Maps

```rust
use zx::*;

fn setup_material_with_normal_map(
    albedo_id: u32,
    mre_id: u32,
    normal_id: u32,
) {
    // Bind albedo to slot 0
    material_albedo(albedo_id);

    // Bind MRE to slot 1
    material_mre(mre_id);

    // Bind normal map to slot 3
    material_normal(normal_id);

    // Normal mapping is auto-enabled when:
    // - material_normal() is called
    // - Mesh has tangent data (FORMAT_TANGENT)
}
```

### Skipping Normal Maps

For meshes without tangent data:

```rust
// Skip normal map sampling (use vertex normal instead)
skip_normal_map(1);

// Re-enable
skip_normal_map(0);
```

### Complete Material Setup

```rust
fn init() {
    // Load textures
    let albedo = load_texture(include_bytes!("brick_albedo.png"));
    let mre = load_texture(include_bytes!("brick_mre.png"));
    let normal = load_texture(include_bytes!("brick_normal.png"));

    // Load mesh WITH tangent data
    let mesh = load_mesh_from_file(include_bytes!("brick_wall.glb"));

    // Set render mode (Mode 2: MR Blinn-Phong)
    render_mode(2);

    // Bind material
    material_albedo(albedo);
    material_mre(mre);
    material_normal(normal);
}

fn tick() {
    // Draw mesh - normal mapping applied automatically
    draw_mesh(mesh);
}
```

---

## nether.toml Configuration

### Asset Registration

```toml
# Mesh with tangent data
[[assets.meshes]]
id = "brick_wall"
path = "generated/meshes/brick_wall.glb"

# Albedo texture (BC7 compressed)
[[assets.textures]]
id = "brick_albedo"
path = "generated/textures/brick_albedo.png"

# MRE texture (BC7 compressed)
[[assets.textures]]
id = "brick_mre"
path = "generated/textures/brick_mre.png"

# Normal map (auto-BC5 due to _normal suffix)
[[assets.textures]]
id = "brick_normal"
path = "generated/textures/brick_normal.png"
```

### Build Script Integration

```toml
[build]
script = """
# Generate textures
python .studio/generate.py --only textures

# Generate normals
python .studio/generate.py --only normals

# Generate meshes (Blender)
blender --background --python .studio/generate.py -- --only meshes

# Build game
cargo build --release
"""
```

---

## Texture Slot Architecture

Normal maps always use **slot 3** regardless of render mode:

| Mode | Slot 0 | Slot 1 | Slot 2 | Slot 3 |
|------|--------|--------|--------|--------|
| 0 (Lambert) | Albedo | - | - | **Normal** |
| 1 (Matcap) | Albedo | Matcap 1 | Matcap 2 | **Normal** |
| 2 (MR) | Albedo | MRE | - | **Normal** |
| 3 (SS) | Albedo | SSE | Specular | **Normal** |

**Consistency:** Same slot across all modes simplifies material management.

---

## Render Mode Compatibility

### Mode 0 (Lambert)

Normal maps perturb basic Lambert shading:

```rust
render_mode(0);
material_albedo(albedo);
material_normal(normal);
```

**Effect:** Adds surface detail to simple diffuse lighting.

### Mode 1 (Matcap)

Normal maps perturb the view-space normal used for matcap UV lookup:

```rust
render_mode(1);
material_albedo(albedo);
bind_matcap(1, matcap1);
material_normal(normal);
```

**Effect:** Matcap highlights/shadows shift with normal map detail.

### Mode 2 (MR Blinn-Phong)

Full tangent-space normal mapping with specular:

```rust
render_mode(2);
material_albedo(albedo);
material_mre(mre);
material_normal(normal);
```

**Effect:** Physically-based specular responds to normal map details.

### Mode 3 (SS Blinn-Phong)

Full tangent-space normal mapping with explicit specular:

```rust
render_mode(3);
material_albedo(albedo);
material_sse(sse);
material_specular(specular);
material_normal(normal);
```

**Effect:** Classic specular highlights respond to normal details.

---

## Troubleshooting

### Normal Map Appears Flat

**Cause:** Mesh doesn't have tangent data.
**Solution:** Export with `export_tangents=True` in Blender.

### Normals Look Inverted

**Cause:** Tangent space mismatch (DirectX vs OpenGL convention).
**Solution:** Invert the G channel of your normal map:

```python
normal[:, :, 1] = 255 - normal[:, :, 1]  # Flip Y
```

### Visible Seams on UV Islands

**Cause:** Tangent discontinuities at UV seams.
**Solution:**
1. Minimize UV seams (larger islands)
2. Use soft normals across seams
3. Consider tangent-space blending in shader (advanced)

### Artifacts on Curved Surfaces

**Cause:** Low mesh resolution or tangent interpolation issues.
**Solution:**
1. Add more geometry at curved areas
2. Use smoother UV unwrapping
3. Reduce normal map strength

---

## Performance Considerations

### Memory Cost

| Component | Size |
|-----------|------|
| Tangent attribute | +4 bytes/vertex |
| 128×128 BC5 normal | +16 KB |
| 256×256 BC5 normal | +64 KB |

### When to Skip Normal Maps

1. **Distant objects** - Detail not visible
2. **Fast-moving objects** - Detail hard to see
3. **Memory-constrained** - Prioritize core assets
4. **Flat surfaces** - No benefit

Use `skip_normal_map(1)` dynamically for LOD systems.

---

## Complete Example

```python
#!/usr/bin/env python3
"""Generate brick wall with normal map - complete example."""

import numpy as np
from PIL import Image
import bpy

# === Texture Generation ===

def height_to_normal(height_map, strength=1.0):
    dx = np.roll(height_map, -1, axis=1) - np.roll(height_map, 1, axis=1)
    dy = np.roll(height_map, -1, axis=0) - np.roll(height_map, 1, axis=0)
    dx *= strength
    dy *= strength
    normal = np.zeros((*height_map.shape, 3), dtype=np.float32)
    normal[:, :, 0] = -dx
    normal[:, :, 1] = -dy
    normal[:, :, 2] = 1.0
    length = np.sqrt(np.sum(normal ** 2, axis=2, keepdims=True))
    normal /= np.maximum(length, 1e-8)
    return ((normal + 1.0) * 0.5 * 255).astype(np.uint8)


def generate_brick_normal(width=256, height=256):
    heightmap = np.ones((height, width), dtype=np.float32)
    brick_w, brick_h = 32, 16
    mortar = 2

    for y in range(height):
        row = y // brick_h
        offset = (brick_w // 2) if row % 2 == 1 else 0
        for x in range(width):
            local_x = (x + offset) % brick_w
            local_y = y % brick_h
            if local_x < mortar or local_y < mortar:
                heightmap[y, x] = 0.7

    return height_to_normal(heightmap, strength=1.2)


# Generate and save
normal = generate_brick_normal()
Image.fromarray(normal, 'RGB').save('assets/textures/brick_normal.png')


# === Mesh Generation ===

def create_brick_wall():
    bpy.ops.mesh.primitive_plane_add(size=2)
    obj = bpy.context.active_object

    # Subdivide for better normal interpolation
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=4)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Calculate tangents
    obj.data.calc_tangents()

    # Export with tangents
    bpy.ops.export_scene.gltf(
        filepath='assets/meshes/brick_wall.glb',
        export_format='GLB',
        export_tangents=True,
        export_normals=True,
    )


create_brick_wall()
```
