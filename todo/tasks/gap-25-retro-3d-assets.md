# Gap 25: Low-Poly Pixel Art 3D (Retro 3D Style)

**Status:** `[ ]` Not Started
**Priority:** MEDIUM
**Plugin:** nethercore-zx-procgen
**Type:** Skill

---

## Problem

NOT covered. Procedural-meshes covers geometry but not retro 3D aesthetics.

A popular modern aesthetic combining low-poly 3D meshes with pixel art textures. This is distinct from both high-poly 3D (covered by procedural-meshes) and pure 2D (covered by Gap 24).

User asks: *"Generate a character in that retro low-poly style with chunky geometry and pixelated textures."*

Currently, there's no guidance for:
- Intentionally low-poly mesh topology
- Pixel art textures on 3D meshes
- Era-appropriate material/lighting choices
- Achieving the retro 3D aesthetic with modern rendering

## What's Missing

### Low-Poly Mesh Generation
- **Poly budget targeting** - Deliberately limiting to 100-500 triangles per object
- **Hard edge modeling** - No smoothing groups, faceted appearance
- **Simplified silhouettes** - Readable shapes at low poly counts
- **Strategic detail placement** - Where to spend polys for maximum impact
- **LOD-0 as final** - No LOD chain, embrace the low-poly look

### Pixel Art Textures for 3D
- **Low-resolution textures** - 32x32, 64x64, 128x128 max
- **Nearest-neighbor filtering** - Crisp pixels, no bilinear blur
- **Limited palette per texture** - 16-64 colors typical
- **Hand-painted look** - Noise patterns mimicking manual pixel placement
- **UV efficiency** - Maximizing texture space at low resolutions

### Character Modeling for Retro 3D
- **Blocky proportions** - Simplified anatomy, chunky limbs
- **Minimal face detail** - 2-3 poly faces, expression via texture
- **T-pose for easy rigging** - Simple bone structures
- **Separate body parts** - Head, torso, limbs as discrete meshes (era-authentic)

### Environment Modeling
- **Modular architecture** - Repeating wall/floor segments
- **Simple geometry** - Convex shapes for level building
- **Pre-baked shadows** - Vertex colors or shadow textures

## Code Examples

### Low-Poly Mesh Generation

```rust
/// Generate a low-poly character with retro-style topology
pub fn generate_lowpoly_humanoid(
    height: f32,
    detail_level: LowPolyDetail,
) -> UnpackedMesh {
    let mut mesh = UnpackedMesh::new();

    // Detail levels with poly budgets
    let (body_segments, limb_segments) = match detail_level {
        LowPolyDetail::Minimal => (4, 3),    // ~100 tris
        LowPolyDetail::Standard => (6, 4),   // ~200 tris
        LowPolyDetail::Detailed => (8, 6),   // ~400 tris
    };

    // Torso - simple box with beveled edges
    let torso = generate_beveled_box(
        height * 0.3,  // width
        height * 0.35, // height
        height * 0.2,  // depth
        1,             // bevel segments (keep low)
    );
    mesh.merge(&torso, Vec3::new(0.0, height * 0.4, 0.0));

    // Head - slightly deformed sphere
    let head = generate_lowpoly_sphere(
        height * 0.12,  // radius
        limb_segments,  // segments (low!)
        limb_segments / 2,
    );
    mesh.merge(&head, Vec3::new(0.0, height * 0.85, 0.0));

    // Limbs - tapered cylinders
    let arm = generate_tapered_cylinder(
        height * 0.05,  // top radius
        height * 0.04,  // bottom radius
        height * 0.25,  // length
        limb_segments,
    );

    // ... add limbs at appropriate positions

    mesh
}

/// Low-poly sphere with hard edges (no smoothing)
pub fn generate_lowpoly_sphere(
    radius: f32,
    segments: u32,
    rings: u32,
) -> UnpackedMesh {
    let mut mesh = UnpackedMesh::new();

    // Generate vertices
    for ring in 0..=rings {
        let v = ring as f32 / rings as f32;
        let phi = v * PI;

        for seg in 0..=segments {
            let u = seg as f32 / segments as f32;
            let theta = u * TAU;

            let x = radius * phi.sin() * theta.cos();
            let y = radius * phi.cos();
            let z = radius * phi.sin() * theta.sin();

            // IMPORTANT: Use face normals, not smooth normals
            // This creates the faceted retro look
            mesh.positions.push([x, y, z]);
        }
    }

    // Generate faces with flat normals
    for ring in 0..rings {
        for seg in 0..segments {
            let a = ring * (segments + 1) + seg;
            let b = a + 1;
            let c = a + segments + 1;
            let d = c + 1;

            // Calculate face normal (flat shading)
            let face_normal = calculate_face_normal(
                mesh.positions[a as usize],
                mesh.positions[b as usize],
                mesh.positions[c as usize],
            );

            // Each vertex gets the face normal (not averaged)
            mesh.add_triangle_flat(a, b, c, face_normal);
            mesh.add_triangle_flat(b, d, c, face_normal);
        }
    }

    mesh
}

#[derive(Clone, Copy)]
pub enum LowPolyDetail {
    Minimal,   // ~100 tris - very chunky
    Standard,  // ~200 tris - typical retro
    Detailed,  // ~400 tris - detailed retro
}
```

### Pixel Art Texture for 3D

```rust
/// Generate a low-res pixel art texture suitable for 3D
pub fn generate_lowres_texture(
    size: u32,  // 32, 64, or 128
    base_color: u32,
    detail_level: f32,  // 0.0-1.0, controls noise amount
    palette: &[u32],    // Limited color palette
) -> TextureBuffer {
    let mut tex = TextureBuffer::new(size, size);

    for y in 0..size {
        for x in 0..size {
            // Base color with noise variation
            let noise = snoise2(
                x as f32 * 0.1,
                y as f32 * 0.1,
                42,
            );

            let varied = vary_color(base_color, noise * detail_level);

            // Quantize to palette
            let final_color = find_nearest_palette_color(varied, palette);
            tex.set(x, y, final_color);
        }
    }

    tex
}

/// Retro palette: limited, saturated colors
pub fn retro_palette() -> Vec<u32> {
    vec![
        0x000000FF, // Black
        0x101030FF, // Dark blue
        0x303050FF, // Blue-gray
        0x505070FF, // Light blue-gray
        0x808080FF, // Gray
        0xA0A0A0FF, // Light gray
        0xC0C0C0FF, // Silver
        0xFFFFFFFF, // White
        0x800000FF, // Dark red
        0xFF0000FF, // Red
        0xFF8080FF, // Pink
        0x804000FF, // Brown
        0xFF8000FF, // Orange
        0xFFFF00FF, // Yellow
        0x008000FF, // Dark green
        0x00FF00FF, // Green
        0x008080FF, // Teal
        0x0000FFFF, // Blue
        0x8000FFFF, // Purple
        0xFF00FFFF, // Magenta
    ]
}
```

### Complete Low-Poly Asset Pipeline

```rust
/// Full pipeline: Generate a retro-style prop
pub fn generate_retro_prop(
    prop_type: PropType,
    texture_size: u32,
    palette: &[u32],
) -> (UnpackedMesh, TextureBuffer) {
    // 1. Generate low-poly mesh
    let mesh = match prop_type {
        PropType::Crate => generate_beveled_box(1.0, 1.0, 1.0, 0),
        PropType::Barrel => generate_lowpoly_cylinder(0.4, 1.0, 6),
        PropType::Tree => generate_lowpoly_tree(2.0, 4),
        PropType::Rock => generate_lowpoly_rock(0.8, 6),
    };

    // 2. Generate matching low-res texture
    let texture = generate_prop_texture(prop_type, texture_size, palette);

    // 3. Ensure UVs are simple (box/planar projection)
    let mesh = apply_simple_uv_projection(&mesh, prop_type);

    (mesh, texture)
}

pub enum PropType {
    Crate,
    Barrel,
    Tree,
    Rock,
}
```

### Python Examples

```python
import numpy as np
import trimesh

def generate_lowpoly_mesh(base_mesh: trimesh.Trimesh, target_faces: int) -> trimesh.Trimesh:
    """Reduce mesh to low-poly count with hard edges."""
    # Decimate to target
    simplified = base_mesh.simplify_quadric_decimation(target_faces)

    # Remove smooth normals - use face normals only
    simplified.face_normals  # This forces face normal calculation
    simplified.vertex_normals = None  # Remove smooth normals

    return simplified

def generate_lowres_texture_for_3d(
    size: int,
    base_color: tuple,
    noise_scale: float = 0.1,
) -> np.ndarray:
    """Generate pixel art texture for 3D models."""
    from noise import snoise2

    img = np.zeros((size, size, 4), dtype=np.uint8)

    for y in range(size):
        for x in range(size):
            # Noise variation
            n = (snoise2(x * noise_scale, y * noise_scale) + 1) / 2

            # Vary base color
            r = int(base_color[0] * (0.7 + 0.6 * n))
            g = int(base_color[1] * (0.7 + 0.6 * n))
            b = int(base_color[2] * (0.7 + 0.6 * n))

            img[y, x] = [min(r, 255), min(g, 255), min(b, 255), 255]

    return img
```

### ZX-Specific Settings

```rust
// In init():
render_mode(0);  // Lambert for flat shading feel

// For each low-poly model:
texture_bind(lowres_tex);
texture_filter(0);  // 0=nearest (crisp pixels), 1=linear (smooth)
```

### nether.toml Configuration

```toml
# Low-poly character
[[assets.meshes]]
id = "player-lowpoly"
path = "assets/models/player_lowpoly.gltf"

# Pixel art texture (low-res)
[[assets.textures]]
id = "player-tex"
path = "assets/textures/player_64x64.png"
filter = "nearest"  # Critical for pixel art look
```

## Prompt for Implementation

```
Add skill "retro-3d-assets" to nethercore-zx-procgen. Triggers: "low poly",
"low-poly", "retro 3D", "pixel art 3D", "90s 3D", "32-bit era", "faceted",
"hard edge 3D", "chunky 3D", "retro style mesh".

Cover:
- Low-poly mesh generation: poly budgets (100-500 tris), hard edges (face normals
  only, no smoothing), simplified topology, strategic detail placement
- Flat shading aesthetic: using face normals instead of smooth vertex normals,
  vertex colors for pre-baked lighting
- Pixel art textures for 3D: low-res (32-128px), nearest filtering, limited palettes,
  UV efficiency at low resolution
- Character/environment patterns: blocky proportions, modular architecture,
  pre-baked shadows via vertex colors

Integration: Builds on procedural-meshes for geometry, procedural-textures for
base patterns. Reference Gap 24 for palette techniques. ZX uses fixed-function
rendering (Mode 0 Lambert, Mode 1 Matcap, Mode 2 MR Blinn-Phong, Mode 3 SS
Blinn-Phong) - no custom shaders. Use texture_filter(0) for crisp pixels (0=nearest).

~1500 words.
```

## Dependencies

- None

## Related Gaps

- Gap 24 (2D Sprites) shares palette/dithering techniques
- procedural-meshes for base geometry generation
- procedural-textures for base texture generation
