---
name: Procedural Texture Generation for ZX
description: This skill should be used when the user asks to "generate a texture", "create procedural texture", "make a noise pattern", "perlin noise texture", "voronoi pattern", "tile texture", "seamless texture", "material texture", "gradient texture", "generate tileable image", "procedural material", "MRE texture", "metallic roughness", "specular map", "albedo texture", "SSE texture", "Mode 2 textures", "Mode 3 textures", "generate PBR textures", "matcap texture", "generate matcap", "dither transparency", "alpha texture", or mentions texture generation, noise algorithms, pattern generation, UV mapping, or material channels for ZX game assets. Provides comprehensive guidance for creating procedural textures including ZX-specific material texture sets (Albedo, MRE, SSE, Specular, Matcaps) compatible with the Nethercore asset pipeline.
version: 1.1.0
---

# Procedural Texture Generation

## Overview

Procedural textures are generated algorithmically. For ZX, you need to understand both basic texture generation AND the material system which uses multiple texture channels.

**Output Requirements for ZX:**
- Format: PNG (RGBA or RGB)
- Resolution: Power of 2 (64, 128, 256, 512)
- Color: RGBA8 format (0xRRGGBBAA)
- Max dimension: 512x512 for VRAM efficiency

---

## ZX Material Texture System

ZX uses multi-texture materials. Each render mode has specific texture slot requirements:

### Mode 0: Lambert (Flat/Diffuse)

| Slot | Texture | Channels | Description |
|------|---------|----------|-------------|
| 0 | **Albedo** | RGBA | Base color + Alpha for dither transparency |

Mode 0 is the simplest - just albedo texture with optional `set_color()` tint. Use for flat-shaded retro looks, UI, sprites, and unlit objects.

### Mode 1: Matcap (Pre-baked Lighting)

| Slot | Texture | Channels | Description |
|------|---------|----------|-------------|
| 0 | **Albedo** | RGBA | Base color (UV-mapped) |
| 1 | **Matcap 1** | RGB | Spherical lighting capture (normal-mapped) |
| 2 | **Matcap 2** | RGB | Additional matcap layer |
| 3 | **Matcap 3** | RGB | Additional matcap layer |

**Matcap Blend Modes (per slot):**
| Mode | Value | Effect | Use For |
|------|-------|--------|---------|
| Multiply | 0 | Darkens base color | Shadows, ambient occlusion |
| Add | 1 | Brightens base color | Highlights, rim light, glow |
| HSV Modulate | 2 | Shifts hue/saturation | Iridescence, color effects |

**FFI Usage:**
```rust
render_mode(1);  // Set in init()

texture_bind(albedo_tex);           // Slot 0 (albedo, UV-mapped)
matcap_set(1, shadow_matcap);       // Slot 1 (matcap, normal-mapped)
matcap_blend_mode(1, 0);            // Multiply for shadows
matcap_set(2, highlight_matcap);    // Slot 2
matcap_blend_mode(2, 1);            // Add for highlights
```

### Mode 2: Metallic-Roughness (MRE)

| Slot | Texture | Channels | Description |
|------|---------|----------|-------------|
| 0 | **Albedo** | RGB | Base diffuse color |
| 1 | **MRE** | R: Metallic, G: Roughness, B: Emissive | Packed material properties |

**FFI Usage:**
```rust
texture_bind(albedo_tex);      // Slot 0 (albedo)
material_mre(mre_tex);         // Slot 1 (MRE map)
// Or use uniform values:
material_metallic(0.8);        // 0.0 = dielectric, 1.0 = metal
material_roughness(0.3);       // 0.0 = mirror, 1.0 = rough
material_emissive(0.0);        // 0.0 = none, >1.0 = HDR glow
```

### Mode 3: Specular-Shininess (SSE)

| Slot | Texture | Channels | Description |
|------|---------|----------|-------------|
| 0 | **Albedo** | RGB | Base diffuse color |
| 1 | **SSE** | R: Specular Reduction, G: Shininess, B: Emissive | Packed material properties |
| 2 | **Specular** | RGB | Specular highlight color |

**Note:** The Specular Reduction channel (R) should typically be **0** for most materials. It's used to dampen specular reflections in specific areas (dirt, scratches, weathering).

**FFI Usage:**
```rust
texture_bind(albedo_tex);       // Slot 0 (albedo)
// SSE is set via uniforms or texture
material_shininess(0.7);        // 0.0-1.0 → maps to 1-256
material_specular(0xFFD700FF);  // Specular highlight color (gold)
material_emissive(0.0);
```

---

## Generating Albedo Textures

Albedo is the base color without lighting. Generate with noise, patterns, or painted styles.

### Rust Example

```rust
use proc_gen::texture::*;

fn generate_albedo(name: &str, base_color: u32, variation: f32, seed: u64) {
    let mut tex = TextureBuffer::new(256, 256);

    // Base color with subtle noise variation
    tex.solid(base_color);

    // Add color variation using noise
    let mut noise_tex = TextureBuffer::new(256, 256);
    noise_tex.fbm(0.03, 4, 0.5, seed, 0x000000FF, 0xFFFFFFFF);

    // Blend noise with base (variation controls strength)
    for y in 0..256 {
        for x in 0..256 {
            let base = tex.get(x, y);
            let noise_val = noise_tex.get(x, y);

            // Modulate base color by noise
            let r = ((base >> 24) as f32 * (1.0 - variation + variation * (noise_val >> 24) as f32 / 255.0)) as u8;
            let g = (((base >> 16) & 0xFF) as f32 * (1.0 - variation + variation * ((noise_val >> 16) & 0xFF) as f32 / 255.0)) as u8;
            let b = (((base >> 8) & 0xFF) as f32 * (1.0 - variation + variation * ((noise_val >> 8) & 0xFF) as f32 / 255.0)) as u8;

            tex.set(x, y, ((r as u32) << 24) | ((g as u32) << 16) | ((b as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_albedo.png", name)).unwrap();
}
```

### Python Example

```python
import numpy as np
from PIL import Image
from noise import snoise2

def generate_albedo(name, base_color, variation=0.2, seed=42, size=256):
    """Generate an albedo texture with noise-based color variation."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    # Parse base color (0xRRGGBBAA)
    r = (base_color >> 24) & 0xFF
    g = (base_color >> 16) & 0xFF
    b = (base_color >> 8) & 0xFF

    for y in range(size):
        for x in range(size):
            # Generate noise value [0, 1]
            n = (snoise2(x * 0.03, y * 0.03, octaves=4, base=seed) + 1) / 2

            # Modulate color by noise
            factor = 1.0 - variation + variation * n
            img[y, x] = [
                int(r * factor),
                int(g * factor),
                int(b * factor),
                255
            ]

    Image.fromarray(img).save(f"assets/textures/{name}_albedo.png")

# Example: Rusty metal
generate_albedo("rust", 0x8B4513FF, variation=0.3, seed=42)
```

---

## Generating MRE Textures (Mode 2)

MRE packs three material properties into RGB channels:
- **R (Red):** Metallic (0 = dielectric, 255 = metal)
- **G (Green):** Roughness (0 = smooth/mirror, 255 = rough)
- **B (Blue):** Emissive intensity (0 = none, 255 = max glow)

### Rust Example

```rust
fn generate_mre(name: &str, metallic: f32, roughness: f32, emissive: f32, seed: u64) {
    let mut tex = TextureBuffer::new(256, 256);

    for y in 0..256 {
        for x in 0..256 {
            // Add noise variation to roughness (common for worn surfaces)
            let noise = snoise2(x as f32 * 0.05, y as f32 * 0.05, seed);
            let rough_varied = (roughness + noise * 0.15).clamp(0.0, 1.0);

            let m = (metallic * 255.0) as u8;
            let r = (rough_varied * 255.0) as u8;
            let e = (emissive * 255.0) as u8;

            // Pack into RGB (A is ignored but set to 255)
            tex.set(x, y, ((m as u32) << 24) | ((r as u32) << 16) | ((e as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_mre.png", name)).unwrap();
}

// Examples:
generate_mre("chrome", 1.0, 0.1, 0.0, 42);     // Shiny metal
generate_mre("brushed_metal", 1.0, 0.4, 0.0, 42); // Brushed metal
generate_mre("rubber", 0.0, 0.9, 0.0, 42);    // Rough plastic
generate_mre("glowing_crystal", 0.2, 0.3, 0.8, 42); // Emissive
```

### Python Example

```python
def generate_mre(name, metallic, roughness, emissive, seed=42, size=256):
    """Generate MRE texture (Metallic, Roughness, Emissive in RGB)."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    for y in range(size):
        for x in range(size):
            # Add noise to roughness for surface variation
            noise = (snoise2(x * 0.05, y * 0.05, base=seed) + 1) / 2
            rough_varied = np.clip(roughness + (noise - 0.5) * 0.3, 0, 1)

            img[y, x] = [
                int(metallic * 255),      # R = Metallic
                int(rough_varied * 255),  # G = Roughness
                int(emissive * 255),      # B = Emissive
                255
            ]

    Image.fromarray(img).save(f"assets/textures/{name}_mre.png")

# Material presets
generate_mre("gold", metallic=1.0, roughness=0.2, emissive=0.0)
generate_mre("plastic", metallic=0.0, roughness=0.5, emissive=0.0)
generate_mre("neon", metallic=0.0, roughness=0.3, emissive=1.0)
```

### MRE Value Guide

| Material | Metallic | Roughness | Emissive |
|----------|----------|-----------|----------|
| Polished Chrome | 1.0 | 0.05-0.15 | 0.0 |
| Brushed Steel | 1.0 | 0.3-0.5 | 0.0 |
| Gold | 1.0 | 0.15-0.25 | 0.0 |
| Copper (worn) | 0.9 | 0.4-0.6 | 0.0 |
| Plastic | 0.0 | 0.3-0.6 | 0.0 |
| Rubber | 0.0 | 0.8-1.0 | 0.0 |
| Skin | 0.0 | 0.5-0.7 | 0.0 |
| Glass | 0.0 | 0.0-0.1 | 0.0 |
| LED/Neon | 0.0 | 0.2-0.4 | 0.5-1.0 |
| Lava | 0.0 | 0.7-0.9 | 0.8-1.0 |

---

## Generating SSE Textures (Mode 3)

SSE packs three material properties into RGB channels:
- **R (Red):** Specular Reduction (damping factor, 0 = full specular, 255 = no specular)
- **G (Green):** Shininess (0 = very soft, 255 = mirror-like)
- **B (Blue):** Emissive intensity

**Note:** The specular reduction channel should typically be **0** for most use cases. It allows per-pixel reduction of specular reflection (e.g., for dirt, scratches, or weathered areas). Only increase it where you want to dampen specular highlights.

### Rust Example

```rust
fn generate_sse(name: &str, specular_reduction: f32, shininess: f32, emissive: f32, seed: u64) {
    let mut tex = TextureBuffer::new(256, 256);

    for y in 0..256 {
        for x in 0..256 {
            // Specular reduction is usually 0, but can vary for worn surfaces
            // Higher values = less specular reflection at that pixel
            let noise = snoise2(x as f32 * 0.08, y as f32 * 0.08, seed);

            // Only add reduction in "worn" areas (typically keep at 0)
            let reduction = if specular_reduction > 0.0 {
                (specular_reduction + noise.max(0.0) * 0.2).clamp(0.0, 1.0)
            } else {
                0.0
            };

            let sr = (reduction * 255.0) as u8;
            let sh = (shininess * 255.0) as u8;
            let e = (emissive * 255.0) as u8;

            tex.set(x, y, ((sr as u32) << 24) | ((sh as u32) << 16) | ((e as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_sse.png", name)).unwrap();
}

// Examples:
generate_sse("polished_gold", 0.0, 0.85, 0.0, 42);  // Full specular, tight highlight
generate_sse("worn_brass", 0.3, 0.6, 0.0, 42);      // Reduced specular in worn areas
generate_sse("glowing_gem", 0.0, 0.9, 0.7, 42);     // Full specular + emissive
```

### Shininess Reference

| Shininess Value | Exponent | Appearance |
|-----------------|----------|------------|
| 0.0-0.2 | 1-52 | Very soft (cloth, skin) |
| 0.2-0.4 | 52-103 | Broad (leather, wood) |
| 0.4-0.6 | 103-154 | Medium (plastic) |
| 0.6-0.8 | 154-205 | Tight (polished metal) |
| 0.8-1.0 | 205-256 | Mirror (chrome, glass) |

---

## Generating Specular Color Maps (Mode 3)

Mode 3 supports colored specular highlights via a separate RGB texture.

### Common Specular Colors

| Material | Specular Color | Hex |
|----------|---------------|-----|
| Default (white) | White | 0xFFFFFFFF |
| Gold | Gold | 0xFFD700FF |
| Copper | Orange-brown | 0xB87333FF |
| Iron | Gray-blue | 0xA0A0B0FF |
| Skin (wet) | Pink-white | 0xFFE0E0FF |
| Plastic | Pure white | 0xFFFFFFFF |

### Rust Example

```rust
fn generate_specular_color(name: &str, base_color: u32, seed: u64) {
    let mut tex = TextureBuffer::new(256, 256);

    // Specular maps are usually fairly uniform with subtle variation
    for y in 0..256 {
        for x in 0..256 {
            // Subtle noise variation
            let noise = snoise2(x as f32 * 0.02, y as f32 * 0.02, seed);
            let factor = 1.0 + noise * 0.05;

            let r = (((base_color >> 24) & 0xFF) as f32 * factor).clamp(0.0, 255.0) as u8;
            let g = (((base_color >> 16) & 0xFF) as f32 * factor).clamp(0.0, 255.0) as u8;
            let b = (((base_color >> 8) & 0xFF) as f32 * factor).clamp(0.0, 255.0) as u8;

            tex.set(x, y, ((r as u32) << 24) | ((g as u32) << 16) | ((b as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_specular.png", name)).unwrap();
}
```

---

## Complete Material Set Generation

Generate a full texture set for a material in one function:

### Mode 2 Material Set

```rust
fn generate_mode2_material(
    name: &str,
    albedo_color: u32,
    metallic: f32,
    roughness: f32,
    emissive: f32,
    variation: f32,
    seed: u64,
) {
    let size = 256;

    // Generate albedo
    let mut albedo = TextureBuffer::new(size, size);
    // ... albedo generation with variation

    // Generate MRE
    let mut mre = TextureBuffer::new(size, size);
    for y in 0..size {
        for x in 0..size {
            let noise = snoise2(x as f32 * 0.05, y as f32 * 0.05, seed);
            let r_val = (roughness + noise * variation * 0.3).clamp(0.0, 1.0);

            mre.set(x, y,
                ((metallic * 255.0) as u32) << 24 |
                ((r_val * 255.0) as u32) << 16 |
                ((emissive * 255.0) as u32) << 8 |
                0xFF
            );
        }
    }

    albedo.write_png(&format!("assets/textures/{}_albedo.png", name)).unwrap();
    mre.write_png(&format!("assets/textures/{}_mre.png", name)).unwrap();
}

// Usage:
generate_mode2_material("steel_armor", 0xB0B0B8FF, 1.0, 0.35, 0.0, 0.2, 42);
```

### Mode 3 Material Set

```rust
fn generate_mode3_material(
    name: &str,
    albedo_color: u32,
    specular_reduction: f32,  // Usually 0.0 for most materials
    shininess: f32,
    specular_color: u32,
    emissive: f32,
    seed: u64,
) {
    let size = 256;

    // Generate albedo
    let mut albedo = TextureBuffer::new(size, size);
    // ... albedo generation with noise variation

    // Generate SSE (Specular Reduction, Shininess, Emissive)
    let mut sse = TextureBuffer::new(size, size);
    for y in 0..size {
        for x in 0..size {
            // Specular reduction is typically 0 (no damping)
            // Only add reduction for worn/dirty areas
            sse.set(x, y,
                ((specular_reduction * 255.0) as u32) << 24 |
                ((shininess * 255.0) as u32) << 16 |
                ((emissive * 255.0) as u32) << 8 |
                0xFF
            );
        }
    }

    // Generate specular color map
    let mut spec = TextureBuffer::new(size, size);
    spec.solid(specular_color);

    albedo.write_png(&format!("assets/textures/{}_albedo.png", name)).unwrap();
    sse.write_png(&format!("assets/textures/{}_sse.png", name)).unwrap();
    spec.write_png(&format!("assets/textures/{}_specular.png", name)).unwrap();
}

// Usage:
// Note: specular_reduction is 0.0 for clean, polished surfaces
generate_mode3_material("gold_trim", 0xE6B84DFF, 0.0, 0.8, 0xFFD700FF, 0.0, 42);
generate_mode3_material("worn_copper", 0xB87333FF, 0.4, 0.5, 0xCC8844FF, 0.0, 42);
```

---

## UV Mapping Considerations

Procedural meshes need proper UV coordinates for textures to display correctly.

### UV-Mapped Mesh Generation

```rust
// Use UV variants of primitives
let cube: UnpackedMeshUV = generate_cube_uv(1.0, 1.0, 1.0);
let sphere: UnpackedMeshUV = generate_sphere_uv(1.0, 16, 8);

// UVs are automatically generated:
// - Cube: Each face gets [0,0] to [1,1] UVs (6 separate faces)
// - Sphere: Equirectangular mapping
// - Cylinder: Cylindrical projection for sides, planar for caps
```

### Custom UV Mapping

```rust
impl UnpackedMeshUV {
    fn add_vertex_uv(&mut self, pos: Vec3, uv: (f32, f32), normal: Vec3) -> u16 {
        // Add vertex with explicit UV coordinates
    }
}

// Example: Planar projection
fn add_planar_uv(mesh: &mut UnpackedMeshUV, scale: f32) {
    for i in 0..mesh.positions.len() {
        let pos = mesh.positions[i];
        mesh.uvs[i] = [pos[0] / scale + 0.5, pos[2] / scale + 0.5];
    }
}
```

### Tiling Textures

For seamless tiling, generate with periodic noise:

```rust
fn tileable_noise(x: f32, y: f32, size: f32, seed: u64) -> f32 {
    // Use 4D noise with circular coordinates for seamless tiling
    let s = x / size;
    let t = y / size;

    let nx = (s * 2.0 * PI).cos();
    let ny = (s * 2.0 * PI).sin();
    let nz = (t * 2.0 * PI).cos();
    let nw = (t * 2.0 * PI).sin();

    snoise4(nx, ny, nz, nw, seed)
}
```

---

## Noise Algorithms Reference

### Perlin Noise

Classic gradient noise for organic surfaces.

```rust
tex.perlin(scale, seed, color_low, color_high);
```

- `scale`: 0.01 (large features) to 0.2 (fine detail)
- Use for: clouds, water, organic materials

### Simplex Noise

Faster than Perlin, fewer artifacts.

```rust
tex.simplex(scale, seed, color_low, color_high);
```

### Voronoi (Cellular)

Cell-like patterns for scales, crystals, cracks.

```rust
tex.voronoi(cell_count, seed, cell_color, edge_color);
```

- `cell_count`: 4-32 typical

### Fractal Brownian Motion (FBM)

Layered noise for complex organic patterns.

```rust
tex.fbm(scale, octaves, persistence, seed, color_low, color_high);
```

- `octaves`: 1-8 (more = more detail)
- `persistence`: 0.3-0.7 (amplitude falloff)

---

## nether.toml Configuration

Reference material textures in your game manifest:

```toml
[game]
id = "my-game"
title = "My Game"

# Mode 2 material (Albedo + MRE)
[[assets.textures]]
id = "armor_albedo"
path = "assets/textures/armor_albedo.png"

[[assets.textures]]
id = "armor_mre"
path = "assets/textures/armor_mre.png"

# Mode 3 material (Albedo + SSE + Specular)
[[assets.textures]]
id = "gold_albedo"
path = "assets/textures/gold_albedo.png"

[[assets.textures]]
id = "gold_sse"
path = "assets/textures/gold_sse.png"

[[assets.textures]]
id = "gold_specular"
path = "assets/textures/gold_specular.png"
```

---

## Generating Matcap Textures (Mode 1)

Matcaps are spherical lighting captures - a 2D image that encodes how light appears on a sphere. ZX uses matcaps for stylized, fast lighting without runtime calculations.

### How Matcaps Work

The shader samples the matcap texture using view-space normals:
- Normal pointing at camera → center of matcap (u=0.5, v=0.5)
- Normal pointing left → left edge (u=0, v=0.5)
- Normal pointing up → top edge (u=0.5, v=0)

### Creating Shadow Matcaps (Multiply Blend)

Shadow matcaps darken the base color. White areas preserve base, dark areas shadow.

```rust
fn generate_shadow_matcap(name: &str, shadow_intensity: f32) {
    let size = 256;
    let center = size as f32 / 2.0;
    let mut tex = TextureBuffer::new(size, size);

    for y in 0..size {
        for x in 0..size {
            // Distance from center (normalized 0-1)
            let dx = (x as f32 - center) / center;
            let dy = (y as f32 - center) / center;
            let dist = (dx * dx + dy * dy).sqrt();

            if dist > 1.0 {
                // Outside sphere - full brightness (no effect when multiplied)
                tex.set(x, y, 0xFFFFFFFF);
                continue;
            }

            // Shadow comes from upper-left (simulating key light)
            // Brighter where facing light, darker in shadow
            let z = (1.0 - dist * dist).sqrt(); // Sphere surface normal Z
            let light_dot = (dx * -0.5 + dy * -0.7 + z * 0.5).max(0.0);

            // Value: 1.0 = no shadow, lower = darker shadow
            let val = 1.0 - shadow_intensity * (1.0 - light_dot);
            let v = (val * 255.0) as u8;

            tex.set(x, y, ((v as u32) << 24) | ((v as u32) << 16) | ((v as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_shadow_matcap.png", name)).unwrap();
}

// Usage: Creates a subtle ambient shadow
generate_shadow_matcap("soft", 0.4);
```

### Creating Highlight Matcaps (Add Blend)

Highlight matcaps add brightness. Black areas add nothing, bright areas add glow.

```rust
fn generate_highlight_matcap(name: &str, highlight_color: u32, intensity: f32, tightness: f32) {
    let size = 256;
    let center = size as f32 / 2.0;
    let mut tex = TextureBuffer::new(size, size);

    let hr = ((highlight_color >> 24) & 0xFF) as f32 / 255.0;
    let hg = ((highlight_color >> 16) & 0xFF) as f32 / 255.0;
    let hb = ((highlight_color >> 8) & 0xFF) as f32 / 255.0;

    for y in 0..size {
        for x in 0..size {
            let dx = (x as f32 - center) / center;
            let dy = (y as f32 - center) / center;
            let dist = (dx * dx + dy * dy).sqrt();

            if dist > 1.0 {
                tex.set(x, y, 0x000000FF); // Black = no addition
                continue;
            }

            // Highlight from upper-right (different from shadow for rim effect)
            let z = (1.0 - dist * dist).sqrt();
            let light_dot = (dx * 0.6 + dy * -0.6 + z * 0.5).max(0.0);

            // Tightness controls specular spread
            let spec = light_dot.powf(tightness * 32.0) * intensity;

            let r = (hr * spec * 255.0).min(255.0) as u8;
            let g = (hg * spec * 255.0).min(255.0) as u8;
            let b = (hb * spec * 255.0).min(255.0) as u8;

            tex.set(x, y, ((r as u32) << 24) | ((g as u32) << 16) | ((b as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_highlight_matcap.png", name)).unwrap();
}

// Usage: Creates a warm specular highlight
generate_highlight_matcap("warm", 0xFFEEDDFF, 1.0, 0.7);
```

### Creating HSV Modulation Matcaps

HSV matcaps shift the hue/saturation of the base color. Great for iridescence.

```rust
fn generate_hsv_matcap(name: &str, hue_shift_range: f32) {
    let size = 256;
    let center = size as f32 / 2.0;
    let mut tex = TextureBuffer::new(size, size);

    for y in 0..size {
        for x in 0..size {
            let dx = (x as f32 - center) / center;
            let dy = (y as f32 - center) / center;
            let dist = (dx * dx + dy * dy).sqrt();

            if dist > 1.0 {
                // Neutral gray = no HSV shift
                tex.set(x, y, 0x808080FF);
                continue;
            }

            // Hue shift based on angle around center
            let angle = dy.atan2(dx);
            let hue_shift = (angle / std::f32::consts::PI) * hue_shift_range;

            // Encode hue shift in R channel (0.5 = no shift)
            // Saturation in G, Value in B
            let h = ((hue_shift + 0.5).clamp(0.0, 1.0) * 255.0) as u8;
            let s = 128u8; // 0.5 = no saturation change
            let v = 128u8; // 0.5 = no value change

            tex.set(x, y, ((h as u32) << 24) | ((s as u32) << 16) | ((v as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_hsv_matcap.png", name)).unwrap();
}

// Usage: Iridescent color shift
generate_hsv_matcap("iridescent", 0.3);
```

### Python Matcap Example

```python
import numpy as np
from PIL import Image

def generate_matcap(name, matcap_type="shadow", intensity=0.5, size=256):
    """Generate a matcap texture for ZX Mode 1."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    center = size / 2

    for y in range(size):
        for x in range(size):
            dx = (x - center) / center
            dy = (y - center) / center
            dist = np.sqrt(dx*dx + dy*dy)

            if dist > 1.0:
                if matcap_type == "shadow":
                    img[y, x] = [255, 255, 255, 255]  # No darkening
                else:
                    img[y, x] = [0, 0, 0, 255]  # No addition
                continue

            z = np.sqrt(1.0 - dist*dist)

            if matcap_type == "shadow":
                # Light from upper-left
                light = max(0, -0.5*dx - 0.7*dy + 0.5*z)
                val = int((1.0 - intensity * (1.0 - light)) * 255)
                img[y, x] = [val, val, val, 255]
            else:  # highlight
                # Light from upper-right
                light = max(0, 0.6*dx - 0.6*dy + 0.5*z)
                spec = (light ** 16) * intensity
                val = int(min(spec * 255, 255))
                img[y, x] = [val, val, val, 255]

    Image.fromarray(img).save(f"assets/textures/{name}_matcap.png")

generate_matcap("ambient", "shadow", 0.4)
generate_matcap("specular", "highlight", 0.8)
```

---

## Alpha Channel and Dither Transparency

ZX uses **dithered transparency** via the alpha channel. Instead of true alpha blending (which is order-dependent), ZX uses a Bayer 4x4 dither pattern to create stippled transparency.

### How Dither Transparency Works

- Alpha value is compared against a Bayer dither threshold per pixel
- Below threshold = fragment discarded (fully transparent)
- Above threshold = fragment kept (fully opaque)
- Result: Order-independent "screen door" transparency

### Generating Textures with Alpha

```rust
fn generate_albedo_with_alpha(name: &str, base_color: u32, alpha_pattern: AlphaPattern, seed: u64) {
    let size = 256;
    let mut tex = TextureBuffer::new(size, size);

    for y in 0..size {
        for x in 0..size {
            // Base color (RGB)
            let r = (base_color >> 24) & 0xFF;
            let g = (base_color >> 16) & 0xFF;
            let b = (base_color >> 8) & 0xFF;

            // Generate alpha based on pattern
            let alpha = match alpha_pattern {
                AlphaPattern::Solid => 255,
                AlphaPattern::EdgeFade => {
                    // Fade at edges (for foliage, particles)
                    let edge_dist = (x.min(size - 1 - x).min(y).min(size - 1 - y)) as f32 / (size as f32 / 4.0);
                    (edge_dist.min(1.0) * 255.0) as u8
                }
                AlphaPattern::NoiseHoles => {
                    // Noise-based holes (for decay, damage)
                    let noise = snoise2(x as f32 * 0.08, y as f32 * 0.08, seed);
                    if noise > 0.3 { 255 } else { 0 }
                }
                AlphaPattern::Gradient(start, end) => {
                    // Linear gradient (for fadeout effects)
                    let t = y as f32 / size as f32;
                    ((1.0 - t) * start as f32 + t * end as f32) as u8
                }
                AlphaPattern::Radial => {
                    // Radial gradient from center (for particles)
                    let dx = (x as f32 - size as f32 / 2.0) / (size as f32 / 2.0);
                    let dy = (y as f32 - size as f32 / 2.0) / (size as f32 / 2.0);
                    let dist = (dx * dx + dy * dy).sqrt();
                    ((1.0 - dist.min(1.0)) * 255.0) as u8
                }
            };

            tex.set(x, y, (r << 24) | (g << 16) | (b << 8) | alpha as u32);
        }
    }

    tex.write_png(&format!("assets/textures/{}_albedo.png", name)).unwrap();
}

enum AlphaPattern {
    Solid,
    EdgeFade,
    NoiseHoles,
    Gradient(u8, u8),  // start_alpha, end_alpha
    Radial,
}
```

### Python Alpha Example

```python
def generate_alpha_texture(name, base_color, alpha_type="radial", size=256):
    """Generate albedo texture with alpha for dither transparency."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    r = (base_color >> 24) & 0xFF
    g = (base_color >> 16) & 0xFF
    b = (base_color >> 8) & 0xFF

    for y in range(size):
        for x in range(size):
            if alpha_type == "radial":
                dx = (x - size/2) / (size/2)
                dy = (y - size/2) / (size/2)
                dist = min(1.0, np.sqrt(dx*dx + dy*dy))
                alpha = int((1.0 - dist) * 255)
            elif alpha_type == "edge_fade":
                edge = min(x, size-1-x, y, size-1-y) / (size/4)
                alpha = int(min(1.0, edge) * 255)
            else:  # solid
                alpha = 255

            img[y, x] = [r, g, b, alpha]

    Image.fromarray(img).save(f"assets/textures/{name}_albedo.png")

# Particle with radial fadeout
generate_alpha_texture("spark", 0xFFDD00FF, "radial")
# Foliage with edge fade
generate_alpha_texture("leaves", 0x228822FF, "edge_fade")
```

### Runtime Alpha Control

Beyond texture alpha, you can also control transparency via uniforms:

```rust
// In draw code:
set_alpha(0.5);  // 50% overall transparency (multiplied with texture alpha)
```

**Note:** Dither transparency works best with moving objects or at a distance. Close-up static objects may show visible dither patterns (intentional retro aesthetic).

---

## Uniform vs Texture Properties

ZX materials combine **uniforms** (per-draw-call values) and **textures** (per-pixel values). Understanding which properties are which is crucial.

### Properties That Are TEXTURE-BASED

| Property | Texture | Modes | Notes |
|----------|---------|-------|-------|
| Base Color | Albedo (Slot 0) | All | RGBA, alpha for dither transparency |
| Metallic | MRE R-channel | Mode 2 | Per-pixel metal/dielectric |
| Roughness | MRE G-channel | Mode 2 | Per-pixel surface roughness |
| Emissive Intensity | MRE B or SSE B | Mode 2, 3 | Per-pixel glow intensity |
| Specular Reduction | SSE R-channel | Mode 3 | Per-pixel specular damping |
| Shininess | SSE G-channel | Mode 3 | Per-pixel highlight tightness |
| Specular Color | Specular (Slot 2) | Mode 3 | Per-pixel highlight color |
| Pre-baked Lighting | Matcaps (Slots 1-3) | Mode 1 | Spherical lighting captures |

### Properties That Are UNIFORM-ONLY

| Property | FFI Function | Notes |
|----------|--------------|-------|
| **Rim Lighting** | `material_rim(intensity, power)` | Edge glow effect, NOT a texture |
| Color Tint | `set_color(rgba)` | Multiplies with albedo |
| Alpha Override | `set_alpha(a)` | Multiplies with texture alpha |
| Metallic (uniform) | `material_metallic(f)` | Used when no MRE texture |
| Roughness (uniform) | `material_roughness(f)` | Used when no MRE texture |
| Emissive (uniform) | `material_emissive(f)` | Additive with texture emissive |
| Shininess (uniform) | `material_shininess(f)` | Used when no SSE texture |
| Specular (uniform) | `material_specular(rgba)` | Highlight color when no texture |
| Matcap Blend Mode | `matcap_blend_mode(slot, mode)` | Multiply/Add/HSV per slot |

### Example: Rim Lighting is NOT a Texture

```rust
// ✅ CORRECT: Rim lighting via uniform
material_rim(0.5, 2.0);  // intensity=0.5, power=2.0 (edge falloff)

// ❌ WRONG: There is no "rim lighting texture"
// material_rim_texture(tex);  // This does not exist!
```

Rim lighting is calculated from view angle vs surface normal in the shader. It cannot be baked into a texture.

---

## Additional Resources

- `references/texture-api.md` - Texture API quick reference
- `references/material-presets.md` - Common material values
- `nethercore/docs/book/src/guides/render-modes.md` - Full render mode documentation
