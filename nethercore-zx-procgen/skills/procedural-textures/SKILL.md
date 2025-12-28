---
name: Procedural Texture Generation for ZX
description: This skill should be used when the user asks to "generate a texture", "create procedural texture", "make a noise pattern", "perlin noise texture", "voronoi pattern", "tile texture", "seamless texture", "material texture", "gradient texture", "generate tileable image", "procedural material", "MRE texture", "metallic roughness", "specular map", "albedo texture", "SSE texture", "Mode 2 textures", "Mode 3 textures", "generate PBR textures", "matcap texture", "generate matcap", "dither transparency", "alpha texture", or mentions texture generation, noise algorithms, pattern generation, UV mapping, or material channels for ZX game assets.
version: 1.3.0
---

# Procedural Texture Generation

## Build Integration

Texture generators are **native binaries** (not WASM). They run at build time via `nether.toml`'s `build.script`:

```toml
[build]
script = "cargo run -p generator --release && cargo build -p game --target wasm32-unknown-unknown --release"

[[assets.textures]]
id = "bark"
path = "../assets/textures/bark_albedo.png"
```

See the **Native Asset Pipeline** skill for full architecture details.

## Output Requirements

- Format: PNG (RGBA or RGB)
- Resolution: Power of 2 (64, 128, 256, 512 max)
- Color: RGBA8 format (0xRRGGBBAA)

---

## ZX Material Texture System

### Mode 0: Lambert (Flat/Diffuse)

| Slot | Texture | Description |
|------|---------|-------------|
| 0 | Albedo | Base color + Alpha for dither transparency |

Use for flat-shaded retro looks, UI, sprites, unlit objects.

### Mode 1: Matcap (Pre-baked Lighting)

| Slot | Texture | Description |
|------|---------|-------------|
| 0 | Albedo | Base color (UV-mapped) |
| 1-3 | Matcaps | Spherical lighting captures (normal-mapped) |

**Blend Modes:** Multiply (shadows), Add (highlights), HSV Modulate (iridescence)

```rust
render_mode(1);
texture_bind(albedo_tex);
matcap_set(1, shadow_matcap);
matcap_blend_mode(1, 0);  // 0=Multiply, 1=Add, 2=HSV
```

### Mode 2: Metallic-Roughness (MRE)

| Slot | Texture | Channels |
|------|---------|----------|
| 0 | Albedo | RGB base color |
| 1 | MRE | R: Metallic, G: Roughness, B: Emissive |

```rust
texture_bind(albedo_tex);
material_mre(mre_tex);
// Or uniform values:
material_metallic(0.8);
material_roughness(0.3);
```

### Mode 3: Specular-Shininess (SSE)

| Slot | Texture | Channels |
|------|---------|----------|
| 0 | Albedo | RGB base color |
| 1 | SSE | R: Specular Reduction (usually 0), G: Shininess, B: Emissive |
| 2 | Specular | RGB highlight color |

```rust
texture_bind(albedo_tex);
material_shininess(0.7);
material_specular(0xFFD700FF);  // Gold highlight
```

---

## Texture Generation Quick Reference

### Albedo Textures

Base color with noise variation. See `references/albedo-generation.md` for full examples.

```rust
let mut tex = TextureBuffer::new(256, 256);
tex.solid(0x8B4513FF);  // Base color
tex.fbm(0.03, 4, 0.5, seed, 0x000000FF, 0xFFFFFFFF);  // Noise variation
tex.write_png("assets/textures/bark_albedo.png").unwrap();
```

### MRE Textures (Mode 2)

Pack metallic, roughness, emissive into RGB. See `references/mre-sse-generation.md`.

| Material | Metallic | Roughness |
|----------|----------|-----------|
| Chrome | 1.0 | 0.1 |
| Brushed Steel | 1.0 | 0.4 |
| Plastic | 0.0 | 0.5 |
| Rubber | 0.0 | 0.9 |

### SSE Textures (Mode 3)

Pack specular reduction, shininess, emissive into RGB. See `references/mre-sse-generation.md`.

**Note:** Specular Reduction (R channel) should be **0** for most materials. Only increase for worn/dirty areas.

### Matcap Textures (Mode 1)

Spherical lighting captures. See `references/matcap-generation.md`.

- Shadow matcap: Light gray sphere, multiply blend
- Highlight matcap: White specular dot, add blend
- HSV matcap: Color gradient for iridescence

### Alpha/Dither Transparency

ZX uses Bayer dithering for order-independent transparency. See `references/alpha-dither.md`.

Common patterns: Radial (particles), EdgeFade (foliage), NoiseHoles (decay)

---

## Noise Algorithms

| Algorithm | Use For | Code |
|-----------|---------|------|
| Perlin | Organic surfaces, clouds | `tex.perlin(scale, seed, low, high)` |
| Simplex | Faster Perlin alternative | `tex.simplex(scale, seed, low, high)` |
| Voronoi | Cells, scales, crystals | `tex.voronoi(cells, seed, cell, edge)` |
| FBM | Complex terrain, clouds | `tex.fbm(scale, octaves, persist, seed, low, high)` |

For tileable patterns, use periodic 4D noise. See `references/noise-algorithms.md`.

---

## UV Mapping

Procedural meshes need proper UVs:

```rust
let cube: UnpackedMeshUV = generate_cube_uv(1.0, 1.0, 1.0);
let sphere: UnpackedMeshUV = generate_sphere_uv(1.0, 16, 8);
```

---

## nether.toml Configuration

```toml
# Mode 2 material
[[assets.textures]]
id = "armor_albedo"
path = "assets/textures/armor_albedo.png"

[[assets.textures]]
id = "armor_mre"
path = "assets/textures/armor_mre.png"
```

---

## Uniform vs Texture Properties

**Texture-based (per-pixel):**
- Albedo, MRE channels, SSE channels, Specular color, Matcaps

**Uniform-only (per-draw-call):**
- `material_rim(intensity, power)` - Rim lighting
- `set_color(rgba)` - Color tint
- `set_alpha(a)` - Alpha multiplier

**Rim lighting is NOT a texture** - it's calculated from view angle vs normal.

---

## Multi-Layer Texture System

**For professional quality, always use multi-layer composition instead of single-pass noise.**

The workflow:
```
1. BASE: Solid color + subtle noise variation
2. DETAIL: Perlin noise overlay for texture
3. FEATURES: Scratches, cracks, grain (as appropriate)
4. WEATHERING: Rust, stains, dust (based on style)
5. EDGE WEAR: Curvature-based highlights (if available)
6. FINAL: Dust + contrast boost
7. QUALITY CHECK: Validate metrics
```

See `references/layer-system.md` for the complete layer system documentation including:
- All layer types (base, noise, features, weathering, edge wear, final)
- Feature generators: scratches, cracks, grain, pores, rust, dust, stains
- Quality metrics and validation
- Language-agnostic examples

---

## CRITICAL: Code Organization & File Size Limits

**Generated code MUST follow these file size limits to prevent context bloat:**

| Limit | Lines | Action |
|-------|-------|--------|
| Target | ≤300 | Ideal file size |
| Soft limit | 400 | Consider splitting |
| Hard limit | 500 | MUST split immediately |
| Unacceptable | >500 | Never generate |

### Mandatory Splitting Strategy

When generating texture code, use this module structure:

```
generator/src/
├── main.rs              # Entry point only (~50 lines)
├── lib.rs               # Module exports (~30 lines)
├── textures/
│   ├── mod.rs           # Re-exports (~20 lines)
│   ├── albedo.rs        # Albedo generation (~150-200 lines)
│   ├── mre.rs           # MRE generation (~100-150 lines)
│   ├── matcap.rs        # Matcap generation (~100-150 lines)
│   └── noise.rs         # Noise utilities (~150-200 lines)
├── layers/
│   ├── mod.rs           # Layer system exports
│   ├── base.rs          # Base layer
│   ├── features.rs      # Scratches, cracks, grain
│   └── weathering.rs    # Rust, stains, dust
└── constants.rs         # Palettes, presets (~100 lines)
```

### What to Extract

| Extract Into | Content |
|--------------|---------|
| `constants.rs` | Color palettes, material presets, noise parameters |
| `noise.rs` | Perlin, simplex, voronoi, FBM functions |
| `layers/*.rs` | Individual layer generators |
| `materials/*.rs` | Per-material-type generators |

### Large Function Pattern

**NEVER** generate functions over 100 lines. Split into helpers:

```rust
// BAD: 200-line function
fn generate_bark_texture(...) { /* everything inline */ }

// GOOD: Composed from small functions
fn generate_bark_texture(size: u32, seed: u64) -> TextureBuffer {
    let mut tex = create_base_layer(size, BARK_COLORS);
    add_noise_layer(&mut tex, seed);
    add_crack_details(&mut tex, seed + 1);
    add_weathering(&mut tex, seed + 2);
    tex
}
```

### Module Re-export Pattern

```rust
// generator/src/lib.rs
pub mod textures;
pub mod layers;
pub mod constants;

pub use textures::{generate_albedo, generate_mre};
pub use constants::*;
```

---

## Reference Files

- `references/layer-system.md` - **Multi-layer composition system (START HERE)**
- `references/texture-api.md` - API quick reference
- `references/albedo-generation.md` - Albedo generation examples
- `references/mre-sse-generation.md` - Material texture examples
- `references/matcap-generation.md` - Matcap generation examples
- `references/alpha-dither.md` - Alpha transparency examples
- `references/noise-algorithms.md` - Noise function reference
