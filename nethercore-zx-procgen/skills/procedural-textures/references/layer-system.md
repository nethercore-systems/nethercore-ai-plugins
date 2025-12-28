# Multi-Layer Texture System

Professional textures are built from multiple layers, not single noise passes. This mimics how artists work in Photoshop/Substance and produces dramatically better results.

## Why Layers Matter

Single-pass noise = obvious programmer art
Multi-layer composition = professional quality

Real materials have:
- Base color with subtle variation
- Surface features (scratches, cracks, pores)
- Weathering (rust, stains, dust)
- Edge wear and corner dirt
- Final polish (contrast, color grading)

## Layer Types

### 1. Base Layer
The foundation color with subtle noise variation.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Color | Base RGBA color |
| Noise scale | Size of variation (0.02-0.1) |
| Noise intensity | Strength of variation (0.1-0.3) |

### 2. Noise Layers
Add texture complexity with blended noise.

**Blend Modes:**
| Mode | Effect | Use For |
|------|--------|---------|
| Normal | Replace | Base layers |
| Multiply | Darken | Shadows, dirt |
| Add | Lighten | Highlights |
| Overlay | Contrast | Detail enhancement |
| Screen | Lighten (softer) | Glow, light areas |

### 3. Feature Layers
Actual surface details, not just noise.

#### Scratches
Linear marks from wear and handling.

**Parameters:**
| Parameter | Description | Range |
|-----------|-------------|-------|
| Density | How many scratches | 0.1-0.3 |
| Length | Scratch length range | (0.1, 0.4) |
| Depth | Visual depth/darkness | 0.3-0.8 |
| Direction | Random, Horizontal, Vertical, Diagonal | - |

**Algorithm:**
```
for each scratch:
    start = random_point_on_texture()
    angle = direction_to_angle()
    length = random_in_range(length_min, length_max)
    end = start + direction(angle) * length

    draw_line(start, end, color=darken_base, width=1-3px)
    add_noise_to_line()  # Makes it look natural
```

#### Cracks
Fracture patterns for damaged materials.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Density | Crack coverage (0.1-0.3) |
| Pattern | Organic, Radial, Grid |
| Depth | Visual depth (0.3-0.6) |
| Color | Crack interior color (usually dark) |

**Algorithm:**
```
# Use Voronoi-based distance field
for each pixel:
    noise1 = perlin(x, y)
    noise2 = perlin(x + offset, y + offset)
    crack_value = abs(noise1 - noise2)

    if crack_value < threshold:
        pixel = lerp(pixel, crack_color, (threshold - crack_value) / threshold)
```

#### Grain
Material-specific linear patterns (wood, brushed metal).

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Scale | Grain width |
| Intensity | Visibility (0.2-0.5) |
| Direction | Horizontal, Vertical, Angled |

#### Pores
Small surface pitting for skin, stone, leather.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Density | Pore frequency (0.2-0.5) |
| Size | Pore size range |
| Depth | How dark pores appear |

**Algorithm:**
```
# Use Worley noise (cell/Voronoi)
for each pixel:
    cell_distance = worley_noise(x, y)

    if cell_distance < pore_threshold:
        darkness = 1 - (cell_distance / pore_threshold)
        pixel = darken(pixel, darkness * depth)
```

### 4. Weathering Layers
Environmental damage and aging.

#### Rust
Oxidation for metal surfaces.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Amount | Coverage (0.2-0.6) |
| Color | OrangeRust, RedRust, BrownRust |
| Pattern | Patchy, Streaked, Edge |

**Algorithm:**
```
rust_mask = fbm_noise(x, y, octaves=4)
rust_color = [180, 80, 30]  # Orange-brown

if rust_mask > (1 - amount):
    rust_intensity = (rust_mask - (1 - amount)) / amount
    pixel = lerp(pixel, rust_color, rust_intensity)
```

#### Water Stains
Mineral deposits and water marks.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Intensity | Stain visibility (0.1-0.3) |
| Color | Usually white/gray |

#### Dust
Surface dust accumulation.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Density | Coverage (0.1-0.3) |
| Color | Dust color (tan, gray) |

### 5. Edge Wear Layer
Highlights edges and darkens corners (requires curvature data).

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Edge threshold | Curvature cutoff for edges |
| Edge color | Worn edge color (lighter/metallic) |
| Corner color | Dirt color (darker) |

### 6. Final Pass
Polish the texture for consistency.

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| Dust density | Light overall dust |
| Contrast boost | Increase pop (1.0-1.2) |

---

## Complete Workflow

```
1. BASE: Solid color + subtle noise variation
2. DETAIL: Perlin noise overlay for texture
3. FEATURES: Scratches, cracks, grain (as appropriate)
4. WEATHERING: Rust, stains, dust (based on style)
5. EDGE WEAR: Curvature-based highlights (if available)
6. FINAL: Dust + contrast boost
7. QUALITY CHECK: Validate metrics
```

---

## Language Examples

### Conceptual (any language)

```
texture = new_texture(256, 256)

# 1. Base layer
texture.fill(base_color)
texture.add_noise(scale=0.05, intensity=0.15, blend="overlay")

# 2. Features
texture.add_scratches(density=0.15, depth=0.4)
texture.add_cracks(density=0.1, color=dark_color)

# 3. Weathering
if damage > 0.3:
    texture.add_rust(amount=damage * 0.5)
texture.add_dust(density=damage * 0.2)

# 4. Final pass
texture.adjust_contrast(1.1)

# 5. Quality check
report = assess_quality(texture)
if not report.is_good():
    print(report.issues)
```

### Rust (proc-gen)

```rust
use proc_gen::texture::*;

let texture = LayeredTextureBuilder::new(256, 256)
    .base(colors.primary)
    .noise_layer(PerlinConfig::default(), colors.dark, colors.light, BlendMode::Overlay, 0.3)
    .scratches(Scratches { density: 0.15, depth: 0.4, ..Default::default() })
    .cracks(Cracks { density: 0.1, color: colors.dark, ..Default::default() })
    .weathering_pass(damage_amount, colors.dark, seed)
    .final_pass(0.1, colors.dark, 1.05, seed)
    .build();
```

### Python

```python
def create_layered_texture(width, height, colors, damage=0.3, seed=42):
    tex = np.zeros((height, width, 4), dtype=np.uint8)

    # Base
    tex[:] = colors['primary']
    tex = add_noise_layer(tex, colors['dark'], colors['light'], blend='overlay', opacity=0.3)

    # Features
    tex = add_scratches(tex, density=0.15, depth=0.4, seed=seed)
    tex = add_cracks(tex, density=0.1, color=colors['dark'], seed=seed+1)

    # Weathering
    if damage > 0.3:
        tex = add_rust(tex, amount=damage * 0.5, seed=seed+2)
    tex = add_dust(tex, density=damage * 0.2, color=colors['dust'], seed=seed+3)

    # Final
    tex = adjust_contrast(tex, 1.05)

    return tex
```

---

## Quality Metrics

After generating, validate quality:

| Metric | Minimum | Good | Fail Action |
|--------|---------|------|-------------|
| Contrast | 0.15 | 0.3+ | Add more layers/features |
| Unique colors | 50 | 200+ | Increase noise/variation |
| Noise coherence | 0.4 | 0.6+ | Reduce octaves or frequency |
| Histogram balance | 0.3 | 0.5+ | Adjust base color |

---

## Common Presets

### Worn Metal
```
base: gray metal color
features: scratches (high), cracks (low)
weathering: rust (medium), dust (light)
edge_wear: bright edges
```

### Weathered Wood
```
base: brown wood color
features: grain (medium), scratches (light)
weathering: water stains (low), dust (medium)
```

### Clean Sci-Fi
```
base: blue-gray metal
features: panel lines (medium), NO scratches
weathering: NONE (pristine)
final: high contrast
```

### Ancient Stone
```
base: gray stone
features: cracks (high), pores (medium)
weathering: water stains (high), dust (high)
edge_wear: dark corners
```
