---
name: Low-Poly Pixel Art 3D (Retro 3D Assets)
description: This skill should be used when the user asks to "generate low poly", "low-poly model", "retro 3D", "pixel art 3D", "90s 3D style", "32-bit era", "faceted mesh", "hard edge 3D", "chunky 3D", "retro style mesh", "PS1 style", "N64 aesthetic", "flat shaded", "no smoothing", or mentions low-poly mesh generation, retro 3D aesthetics, pixel art textures on 3D models, intentionally low polygon counts, hard edge modeling, faceted appearance, or era-appropriate material choices. Provides guidance for creating authentic retro 3D assets with intentionally low polygon counts and pixel art textures compatible with the Nethercore ZX asset pipeline.
version: 1.0.0
---

# Low-Poly Pixel Art 3D (Retro 3D Assets)

## Overview

Retro 3D combines intentionally low-poly meshes with pixel art textures to achieve the distinctive look of 32-bit era games (PS1, N64, Saturn). This aesthetic requires deliberate constraints on geometry complexity and texture resolution.

**Core Principles:**
- Embrace polygon limits, not fight them
- Hard edges and faceted surfaces define the style
- Pixel art textures use nearest-neighbor filtering
- Strategic detail placement maximizes visual impact

**ZX Compatibility:**
- Mode 0 (Lambert) for authentic flat shading
- `texture_filter(0)` for crisp pixel art (nearest-neighbor)
- Vertex colors for baked shadows/highlights
- Standard OBJ/GLTF output for asset pipeline

---

## Poly Budget Guidelines

Target specific triangle counts for authentic retro proportions:

| Asset Type | Triangle Budget | Notes |
|------------|-----------------|-------|
| Character (minimal) | 80-150 tris | Very blocky, expressive through texture |
| Character (standard) | 150-300 tris | Typical retro protagonist |
| Character (detailed) | 300-500 tris | Hero/boss level detail |
| Prop (simple) | 20-80 tris | Crates, barrels, pickups |
| Prop (detailed) | 80-200 tris | Weapons, key items |
| Vehicle | 150-400 tris | Cars, ships, mechs |
| Environment tile | 50-150 tris | Modular level pieces |

**Strategy:** Spend polys where silhouette matters most. Faces, hands, and distinctive features get more triangles. Hidden or distant areas stay minimal.

---

## Hard Edge Modeling

Retro 3D uses **face normals** exclusively. No smooth shading, no averaged vertex normals. Each polygon face is flat, creating the characteristic faceted look.

### Flat Normals in Rust

```rust
use proc_gen::mesh::*;

fn generate_lowpoly_sphere(radius: f32, segments: u32, rings: u32) -> UnpackedMesh {
    let mut mesh = UnpackedMesh::default();

    for ring in 0..rings {
        for seg in 0..segments {
            // Calculate quad corners
            let (v0, v1, v2, v3) = calculate_quad_positions(ring, seg, segments, rings, radius);

            // CRITICAL: Use face normal, not vertex normal
            let face_normal = calculate_face_normal(v0, v1, v2);

            // Add vertices with SAME normal for flat shading
            let i0 = mesh.add_vertex(v0, face_normal);
            let i1 = mesh.add_vertex(v1, face_normal);
            let i2 = mesh.add_vertex(v2, face_normal);
            let i3 = mesh.add_vertex(v3, face_normal);

            mesh.add_triangle(i0, i1, i2);
            mesh.add_triangle(i0, i2, i3);
        }
    }

    mesh
}

fn calculate_face_normal(v0: Vec3, v1: Vec3, v2: Vec3) -> Vec3 {
    let edge1 = v1 - v0;
    let edge2 = v2 - v0;
    edge1.cross(edge2).normalize()
}
```

### Using FlatNormals Modifier

```rust
let mut mesh: UnpackedMesh = generate_sphere(1.0, 8, 6);
mesh.apply(FlatNormals);  // Recalculate as face normals
write_obj(&mesh, "assets/meshes/retro_sphere.obj", "sphere").unwrap();
```

### Python Flat Shading

```python
import trimesh

def make_flat_shaded(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """Convert mesh to flat-shaded by duplicating vertices per face."""
    # Unmerge vertices so each face has unique vertices
    mesh.unmerge_vertices()
    # Recalculate to use face normals
    mesh.fix_normals()
    return mesh

# Example usage
mesh = trimesh.creation.icosphere(subdivisions=1, radius=1.0)
flat_mesh = make_flat_shaded(mesh)
flat_mesh.export("assets/meshes/retro_sphere.obj")
```

---

## Low-Poly Character Topology

Retro characters use simplified anatomy with blocky proportions. Body parts often remain separate meshes (era-authentic) or merge with visible seams.

### Body Part Budgets

| Part | Triangles | Approach |
|------|-----------|----------|
| Head | 20-50 | Box or low-poly sphere, expression via texture |
| Torso | 30-60 | Beveled box or tapered cylinder |
| Arms (each) | 15-30 | Tapered cylinders, 4-6 sides |
| Legs (each) | 15-30 | Tapered cylinders, 4-6 sides |
| Hands | 8-20 | Box or simple mitten shape |
| Feet | 8-15 | Box or wedge |

### Rust Character Example

```rust
pub enum LowPolyDetail {
    Minimal,   // ~100 tris - very chunky
    Standard,  // ~200 tris - typical retro
    Detailed,  // ~400 tris - detailed retro
}

fn generate_lowpoly_humanoid(height: f32, detail: LowPolyDetail) -> UnpackedMesh {
    let (body_segs, limb_segs) = match detail {
        LowPolyDetail::Minimal => (4, 3),
        LowPolyDetail::Standard => (6, 4),
        LowPolyDetail::Detailed => (8, 6),
    };

    let mut mesh = UnpackedMesh::default();

    // Torso - beveled box
    let torso = generate_beveled_box(
        height * 0.3,   // width
        height * 0.35,  // height
        height * 0.2,   // depth
        0,              // NO bevel segments (keep faceted)
    );
    mesh.merge(&torso, Vec3::new(0.0, height * 0.4, 0.0));

    // Head - low-poly sphere
    let mut head = generate_sphere(height * 0.12, limb_segs, limb_segs / 2);
    head.apply(FlatNormals);
    mesh.merge(&head, Vec3::new(0.0, height * 0.85, 0.0));

    // Limbs - tapered cylinders
    // ... add arms, legs at appropriate positions

    mesh.apply(FlatNormals);
    mesh
}
```

---

## Pixel Art Textures for 3D

Retro 3D textures are **low resolution** with **nearest-neighbor filtering**. This creates crisp, visible pixels that complement the faceted geometry.

### Texture Size Guidelines

| Resolution | Use Case |
|------------|----------|
| 16x16 | Tiny props, UI elements |
| 32x32 | Small props, tileable patterns |
| 64x64 | Standard props and characters |
| 128x128 | Hero characters, large props |
| 256x256 | Maximum for environment atlases |

### Limited Color Palettes

Authentic retro uses 16-64 colors per texture. Constrain your generation to a fixed palette:

```rust
fn retro_palette_16() -> Vec<u32> {
    vec![
        0x000000FF, 0x1D2B53FF, 0x7E2553FF, 0x008751FF,
        0xAB5236FF, 0x5F574FFF, 0xC2C3C7FF, 0xFFF1E8FF,
        0xFF004DFF, 0xFFA300FF, 0xFFEC27FF, 0x00E436FF,
        0x29ADFFFF, 0x83769CFF, 0xFF77A8FF, 0xFFCCAAFF,
    ]
}

fn quantize_to_palette(color: u32, palette: &[u32]) -> u32 {
    palette.iter()
        .min_by_key(|&&p| color_distance(color, p))
        .copied()
        .unwrap_or(color)
}
```

### Rust Pixel Art Texture

```rust
fn generate_lowres_texture(
    size: u32,
    base_color: u32,
    noise_intensity: f32,
    palette: &[u32],
    seed: u64,
) -> TextureBuffer {
    let mut tex = TextureBuffer::new(size, size);

    for y in 0..size {
        for x in 0..size {
            // Base color with noise variation
            let noise = snoise2(x as f32 * 0.15, y as f32 * 0.15, seed);
            let varied = vary_color(base_color, noise * noise_intensity);

            // Quantize to palette
            let final_color = quantize_to_palette(varied, palette);
            tex.set(x, y, final_color);
        }
    }

    tex
}
```

### Python Pixel Art Texture

```python
import numpy as np
from PIL import Image
from noise import snoise2

def generate_lowres_texture(size, base_color, palette, noise_scale=0.15, seed=42):
    """Generate a low-resolution pixel art texture."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    for y in range(size):
        for x in range(size):
            # Noise variation
            n = (snoise2(x * noise_scale, y * noise_scale, base=seed) + 1) / 2

            # Vary base color
            r = int(((base_color >> 24) & 0xFF) * (0.7 + 0.6 * n))
            g = int(((base_color >> 16) & 0xFF) * (0.7 + 0.6 * n))
            b = int(((base_color >> 8) & 0xFF) * (0.7 + 0.6 * n))

            # Quantize to nearest palette color
            color = find_nearest_palette(r, g, b, palette)
            img[y, x] = [color[0], color[1], color[2], 255]

    return Image.fromarray(img)
```

---

## ZX-Specific Setup

Configure ZX for authentic retro rendering:

```rust
fn init() {
    render_mode(0);  // Lambert for flat diffuse shading
}

fn draw_retro_asset(mesh: u32, texture: u32) {
    texture_bind(texture);
    texture_filter(0);  // 0 = nearest (crisp pixels), 1 = linear
    mesh_draw(mesh);
}
```

### nether.toml Configuration

```toml
# Low-poly character mesh
[[assets.meshes]]
id = "player-lowpoly"
path = "assets/meshes/player_lowpoly.obj"

# Pixel art texture with nearest filtering
[[assets.textures]]
id = "player-tex"
path = "assets/textures/player_64x64.png"
filter = "nearest"  # Critical for pixel art
```

---

## Vertex Color Baked Shadows

Instead of runtime lighting, bake shadows into vertex colors for authentic retro look:

```rust
fn bake_simple_ao(mesh: &mut UnpackedMeshColor) {
    for i in 0..mesh.positions.len() {
        let y = mesh.positions[i][1];
        let y_normalized = (y - mesh.min_y()) / (mesh.max_y() - mesh.min_y());

        // Simple height-based AO: darker at bottom
        let ao = 0.6 + 0.4 * y_normalized;
        let gray = (ao * 255.0) as u8;

        mesh.colors[i] = [gray, gray, gray, 255];
    }
}
```

For vertex colors, export as GLTF (OBJ doesn't support vertex colors):

```python
mesh.export("assets/meshes/character.glb")  # GLB preserves vertex colors
```

---

## Environment Modeling

Retro environments use modular, simple geometry:

### Modular Pieces
- Wall segments (4-8 tris)
- Floor tiles (2 tris)
- Corner pieces (6-12 tris)
- Pillars/columns (8-16 tris)
- Stairs (steps as separate quads)

### Pre-baked Shadows
Use vertex colors or shadow textures instead of real-time shadows. Bake a simple directional shadow assuming light from above-left.

---

## Quick Reference

| Aspect | Retro 3D Approach |
|--------|-------------------|
| Polygons | 100-500 tris per object |
| Shading | Flat (face normals only) |
| Textures | 32-128px, nearest filter |
| Colors | 16-64 color palette |
| Shadows | Baked (vertex colors or texture) |
| ZX Mode | Mode 0 (Lambert) |
| Filter | `texture_filter(0)` |

---

## Additional Resources

- `references/poly-budgets.md` - Detailed budget breakdowns by asset type
- `references/retro-palettes.md` - Era-authentic color palettes
- `procedural-meshes` skill - Base mesh generation techniques
- `procedural-textures` skill - Noise and pattern generation
