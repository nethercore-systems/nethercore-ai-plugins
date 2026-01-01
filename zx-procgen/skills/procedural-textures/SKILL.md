---
name: Procedural Texture Generation for ZX
description: |
  Use this skill to GENERATE textures for ZX 3D meshes. Trigger phrases: "generate texture", "procedural texture", "noise pattern", "MRE texture", "albedo", "matcap", "seamless texture", "material recipe".

  **Before generating:** Check `.studio/visual-style.local.md` for project style specs (palette, materials, damage level). Apply those constraints for consistent assets. If no style exists, ask about style or suggest `/establish-visual-style`.

  **Load references when:**
  - Project structure, multiple textures → `generator-patterns` skill
  - TextureBuffer class → `references/texture-api.md`
  - Noise algorithms → `references/noise-algorithms.md`
  - Material recipes → `references/material-recipes.md`

  Covers ZX render modes 0-3, noise algorithms, material layers, atlas packing.

  For UV-AWARE TEXTURING (projecting onto meshes): use mesh-texturing-workflows.
  For 2D SPRITES (pixel art, tilesets): use procedural-sprites.
version: 2.2.0
---

# Procedural Texture Generation

Generate game-ready textures procedurally using Python with Pillow (PIL), NumPy, and FastNoiseLite.

## Technology Stack

| Library | Purpose |
|---------|---------|
| **PIL (Pillow)** | Image I/O, basic operations |
| **NumPy** | Fast array math, blending |
| **FastNoiseLite** | High-quality noise (Perlin, Simplex, Cellular, etc.) |

```bash
pip install pillow numpy pyfastnoiselite
```

## Output Requirements

- **Format:** PNG (RGBA or RGB)
- **Resolution:** Power of 2 (64, 128, 256, 512 max)
- **Target Aesthetic:** Low Poly / N64 / PS1 / PS2 era

---

## Nethercore ZX Render Modes

**Critical:** Each render mode requires different texture maps. Render mode is set once in `init()` via `render_mode(mode)`.

### Mode 0: Lambert/Unlit (1 map)

The simplest mode — texture multiplied by vertex color. Automatic Lambert shading when mesh has normals.

| Slot | Texture | Purpose |
|------|---------|---------|
| 0 | Albedo | RGB base color |

**Shading Behavior:**
- Without normals: `final_color = texture × vertex_color`
- With normals: Simple Lambert with sun direction and sky ambient

**Use Cases:** UI, sprites, flat-shaded retro graphics, performance-critical scenes

---

### Mode 1: Matcap (up to 4 maps with layering)

View-space normal sampling from matcap textures. Lighting is "baked" into the matcap.

| Slot | Texture | Sampled By |
|------|---------|------------|
| 0 | Albedo | UV coordinates |
| 1 | Matcap 1 | View-space normal |
| 2 | Matcap 2 | View-space normal |
| 3 | Matcap 3 | View-space normal |

**Matcap Blend Modes:**

| Mode | Value | Effect | Use Case |
|------|-------|--------|----------|
| Multiply | 0 | Darkens | Shadows, AO, toon bands |
| Add | 1 | Brightens | Highlights, rim, glow |
| HSV Modulate | 2 | Hue/saturation shift | Iridescence, rainbow |

**How Matcaps Work:**
```
view_normal = transform_to_view_space(surface_normal)
matcap_uv = view_normal.xy * 0.5 + 0.5
final = albedo × vertex_color × matcap1 × matcap2 × matcap3
```

See `references/matcap-generation.md` for the complete matcap library (20+ types).

---

### Mode 2: Metallic-Roughness Blinn-Phong (2 maps)

PBR-inspired normalized Blinn-Phong with energy conservation.

| Slot | Texture | Channels |
|------|---------|----------|
| 0 | Albedo | RGB: Diffuse color |
| 1 | MRE | R: Metallic, G: Roughness, B: Emissive |

**MRE Channel Values:**

| Channel | 0.0 | 1.0 |
|---------|-----|-----|
| Metallic (R) | Dielectric (plastic) | Full metal |
| Roughness (G) | Mirror smooth | Fully diffuse |
| Emissive (B) | No glow | Max self-illumination |

**Common Material Presets:**

| Material | Metallic | Roughness |
|----------|----------|-----------|
| Polished metal | 0.9 | 0.2 |
| Brushed metal | 0.9 | 0.4 |
| Plastic | 0.0 | 0.5 |
| Rubber | 0.0 | 0.9 |
| Glass | 0.0 | 0.1 |

See `references/mre-sse-generation.md` for complete examples.

---

### Mode 3: Specular-Shininess Blinn-Phong (3 maps)

Classic Blinn-Phong with explicit specular control. Era-authentic for PS1/N64/Saturn aesthetic.

| Slot | Texture | Channels |
|------|---------|----------|
| 0 | Albedo | RGB: Diffuse color |
| 1 | SSE | R: Specular Damping, G: Shininess, B: Emissive |
| 2 | Specular | RGB: Specular highlight tint |

**SSE Channel Values:**

| Channel | 0.0 | 1.0 |
|---------|-----|-----|
| Specular Damping (R) | Full specular | No specular |
| Shininess (G) | Diffuse (exp=1) | Mirror (exp=256) |
| Emissive (B) | No glow | Max glow |

**Note:** Specular Damping (R) should usually be **0**. Only increase for worn/dirty areas.

See `references/mre-sse-generation.md` for complete examples.

---

## Quick Start: TextureBuffer Class

All examples use a helper class. See `references/texture-api.md` for the complete implementation.

```python
from texture_buffer import TextureBuffer

# Create and save a simple texture
tex = TextureBuffer(256, 256)
tex.fill((139, 69, 19, 255))  # Brown base
tex.add_perlin_noise(scale=0.03, intensity=0.2, seed=42)
tex.save("bark_albedo.png")
```

---

## Noise Algorithms (FastNoiseLite)

| Algorithm | Best For | Parameters |
|-----------|----------|------------|
| Perlin | Smooth organic patterns | scale, seed |
| Simplex | Faster Perlin, fewer artifacts | scale, seed |
| Cellular (Voronoi) | Cells, cracks, scales | cell_count, seed |
| Value | Hard-edged noise | scale, seed |
| Fractal (FBM) | Complex organic detail | octaves, persistence |

See `references/noise-algorithms.md` for the complete noise reference.

---

## Material Recipes

Common material patterns using layered noise:

| Material | Technique |
|----------|-----------|
| Brushed metal | Directional stretched noise + grain |
| Wood grain | Elongated Perlin + ring pattern |
| Stone/concrete | Multi-octave FBM + subtle color variation |
| Rust patches | Thresholded cellular noise |
| Fabric/cloth | Fine weave pattern + noise |

See `references/material-recipes.md` for complete recipes with code.

---

## Multi-Layer Composition

Professional textures are built from multiple layers:

```
1. BASE: Solid color + subtle noise variation
2. DETAIL: Perlin/Simplex noise overlay
3. FEATURES: Scratches, cracks, grain
4. WEATHERING: Rust, stains, dust
5. FINAL: Contrast boost, color grading
```

See `references/layer-system.md` for the complete layer system.

---

## Texture Atlas Packing

**ZX binds one texture per slot.** Multiple materials require atlas packing.

**Workflow:**
1. Generate individual material textures
2. Pack into atlas (2x2, 4x4 grid)
3. Generate matching atlas for each required slot (Albedo, MRE, SSE, Specular)
4. Remap mesh UVs to atlas quadrants

See `references/atlas-packing.md` for atlas utilities.

---

## Seamless/Tileable Textures

For tileable textures, use 4D noise with circular coordinates:

```python
# Map 2D to 4D torus for seamless tiling
s, t = x / width, y / height
nx = cos(s * 2 * PI) * scale
ny = sin(s * 2 * PI) * scale
nz = cos(t * 2 * PI) * scale
nw = sin(t * 2 * PI) * scale
value = noise.get_noise_4d(nx, ny, nz, nw)
```

See `references/seamless-textures.md` for tileable texture techniques.

---

## Console Constraints

| Constraint | Limit |
|------------|-------|
| Max texture resolution | 512 x 512 |
| Required sizes | Power of 2 |
| VRAM budget | 4MB total |
| Matcap resolution | Typically 64x64 or 128x128 |

---

## Reference Files

| Reference | Contents |
|-----------|----------|
| `texture-api.md` | TextureBuffer class implementation |
| `noise-algorithms.md` | FastNoiseLite noise reference |
| `albedo-generation.md` | Albedo texture examples |
| `mre-sse-generation.md` | MRE and SSE map generation |
| `matcap-generation.md` | Complete matcap library (20+ types) |
| `material-recipes.md` | Material presets with code |
| `layer-system.md` | Multi-layer composition system |
| `atlas-packing.md` | Texture atlas utilities |
| `seamless-textures.md` | Tileable texture techniques |
| `alpha-dither.md` | Dither transparency patterns |

---

## File Organization

**One texture per file.** Each texture material should have its own Python script:

```
generator/
├── lib/
│   └── texture_buffer.py     # TextureBuffer class (from generator-patterns)
├── textures/
│   ├── wood_plank.py         # One file per texture
│   ├── metal_brushed.py
│   ├── stone_cobble.py
│   ├── brick_wall.py
│   └── rust_patches.py
└── generate_all.py           # Batch runner
```

Each texture file generates all required maps (albedo, MRE/SSE, etc.):

```python
#!/usr/bin/env python3
"""Generate wood plank texture set."""
from lib.texture_buffer import TextureBuffer

OUTPUT_DIR = "../assets/textures"

def generate():
    # Generate albedo
    albedo = TextureBuffer(256, 256)
    albedo.fill((139, 90, 43, 255))
    albedo.add_perlin_noise(scale=0.05, intensity=30)
    albedo.save(f"{OUTPUT_DIR}/wood_plank_albedo.png")

    # Generate MRE
    mre = TextureBuffer(256, 256)
    mre.fill((0, 128, 0, 255))  # Non-metal, medium rough
    mre.save(f"{OUTPUT_DIR}/wood_plank_mre.png")

if __name__ == "__main__":
    generate()
```

**File Size Limits:**

| Limit | Lines | Action |
|-------|-------|--------|
| Target | ≤150 | Ideal for single texture |
| Soft | 200 | Consider splitting |
| Hard | 300 | Extract helpers to lib/ |

For complete setup, see the `generator-patterns` skill.
