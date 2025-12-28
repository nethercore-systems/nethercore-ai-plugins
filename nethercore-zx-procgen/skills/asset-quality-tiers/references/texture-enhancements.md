# Texture Enhancement Techniques

Detailed techniques for upgrading texture quality through the tier system.

## Placeholder → Temp Upgrades

### Add Noise Variation

Transform flat colors into textured surfaces:

```rust
// Base noise layer
tex.fbm(
    scale: 8.0,
    octaves: 3,
    persistence: 0.5,
    seed: rng.next(),
    low: base_color.darken(0.1),
    high: base_color.lighten(0.1),
);

// Add subtle color variation
tex.blend(
    &secondary_noise,
    BlendMode::Overlay,
    opacity: 0.3,
);
```

### Establish Color Palette

Move from random colors to coherent palette:

```rust
// Define palette from style
let palette = Palette::from_style_token("rustic_wood");

// Constrain all colors to palette
tex.remap_to_palette(&palette, RemapMethod::Nearest);
```

### Basic Detail Addition

Add fundamental surface detail:

```rust
// Wood grain
tex.add_grain(GrainType::Wood {
    density: 0.5,
    waviness: 0.3,
    direction: Vec2::new(0.0, 1.0),
});

// Stone variation
tex.add_variation(VariationType::Mottled {
    scale: 4.0,
    intensity: 0.2,
});

// Metal brushing
tex.add_brushing(BrushType::Linear {
    direction: 45.0,
    density: 0.8,
});
```

---

## Temp → Final Upgrades

### Increase Contrast

Final-tier textures need dynamic range:

```rust
// Measure current contrast
let histogram = tex.histogram();
let contrast = histogram.max - histogram.min;
println!("Current contrast: {:.2}", contrast);

// Target: 0.4-0.6 dynamic range
if contrast < 0.4 {
    // Expand range
    tex.apply_curves(|v| {
        // S-curve for contrast boost
        let mid = 0.5;
        let factor = 1.5;
        mid + (v - mid) * factor
    });
}
```

### Add Multiple Detail Layers

Layer details at different scales:

```rust
// Layer 1: Large-scale variation (base)
tex.layer(
    noise: Simplex::new(seed),
    scale: 2.0,
    amplitude: 0.3,
    blend: BlendMode::Normal,
);

// Layer 2: Medium detail
tex.layer(
    noise: Perlin::new(seed + 1),
    scale: 8.0,
    amplitude: 0.2,
    blend: BlendMode::Overlay,
);

// Layer 3: Fine detail
tex.layer(
    noise: Perlin::new(seed + 2),
    scale: 32.0,
    amplitude: 0.1,
    blend: BlendMode::SoftLight,
);
```

### Color Richness

Add color depth through subtle hue variation:

```rust
// Hue shift based on value
tex.apply_per_pixel(|color, uv| {
    let noise = simplex_noise(uv * 4.0, seed);
    let hue_shift = noise * 0.05;  // ±5% hue variation
    color.shift_hue(hue_shift)
});

// Warm shadows, cool highlights
tex.color_balance(
    shadows: Color::new(1.05, 0.95, 0.9),   // Warm
    highlights: Color::new(0.95, 0.98, 1.05), // Cool
);
```

### Add MRE Channel

Create material response textures:

```rust
// Generate MRE from albedo analysis
let mre = TextureBuffer::new(tex.width(), tex.height());

for (x, y) in tex.pixels() {
    let albedo = tex.get(x, y);

    // Metallic: based on saturation (low sat = metallic)
    let metallic = 1.0 - albedo.saturation();

    // Roughness: based on detail/noise
    let roughness = calculate_local_variance(tex, x, y, 3);

    // Emission: none for most materials
    let emission = 0.0;

    mre.set(x, y, Color::new(metallic, roughness, emission));
}
```

### Improve Edge Definition

Sharpen important edges:

```rust
// Unsharp mask for detail enhancement
tex.unsharp_mask(
    radius: 1.0,
    amount: 0.5,
    threshold: 0.01,
);

// Edge-aware sharpening (preserves smooth gradients)
tex.smart_sharpen(
    radius: 0.5,
    amount: 0.3,
    edge_threshold: 0.1,
);
```

---

## Final → Hero Upgrades

### Add Wear and Damage

Hero textures show signs of use:

```rust
// Edge wear (lighter on edges)
tex.apply_edge_wear(EdgeWear {
    detection_radius: 2,
    intensity: 0.3,
    color_shift: Color::WHITE * 0.2,
});

// Cavity darkening (dirt in recesses)
tex.apply_cavity_dirt(CavityDirt {
    detection_radius: 3,
    intensity: 0.4,
    dirt_color: base_color.darken(0.3).desaturate(0.5),
});

// Scratches
tex.add_scratches(Scratches {
    density: 0.3,
    length_range: (0.1, 0.4),
    width: 1,  // pixels
    depth: 0.2,
    direction_bias: None,  // Random
});
```

### Add All Material Channels

Complete material description:

```rust
// SSE (Subsurface Scattering + Extra)
let sse = generate_sse(&tex, material_type);

// Matcap for specific lighting scenarios
let matcap = generate_matcap(material_type, lighting_style);

// Detail normal map
let detail_normal = generate_detail_normal(&tex, DetailLevel::High);

// Height map for parallax
let height = generate_height_from_albedo(&tex);
```

### Subtle Variations

No two areas should look identical:

```rust
// Per-pixel unique noise
tex.add_micro_variation(MicroVariation {
    scale: 64.0,  // High frequency
    amplitude: 0.03,  // Subtle
    mode: VariationMode::Value,  // Just brightness
});

// Larger-scale color pooling
tex.add_color_pools(ColorPools {
    scale: 4.0,
    hue_variance: 0.02,
    saturation_variance: 0.05,
});
```

### Perfect Tiling

Ensure seamless tiling at hero quality:

```rust
// Analyze tile seams
let seam_visibility = tex.analyze_seams();
if seam_visibility > 0.02 {
    // Blend edges
    tex.blend_edges(BlendEdges {
        width: tex.width() / 8,
        falloff: Falloff::Smooth,
    });

    // Re-add detail to blended areas
    tex.add_seam_detail(SeamDetail {
        noise_scale: 16.0,
        intensity: 0.15,
    });
}

// Final seam check
tex.verify_tileable(tolerance: 0.01);
```

### Resolution Upgrade

Increase resolution for hero assets:

```rust
// Upscale with detail preservation
tex.upscale(
    factor: 2,  // 256 → 512
    method: UpscaleMethod::Lanczos,
);

// Add high-frequency detail lost in upscale
tex.add_detail_layer(DetailLayer {
    scale: tex.width() as f32 / 4.0,
    amplitude: 0.05,
    blend: BlendMode::Overlay,
});
```

---

## Contrast Enhancement Techniques

### Histogram Analysis

```rust
fn analyze_contrast(tex: &TextureBuffer) -> ContrastReport {
    let histogram = tex.histogram_luminance();

    ContrastReport {
        min: histogram.percentile(1),   // Ignore outliers
        max: histogram.percentile(99),
        range: histogram.percentile(99) - histogram.percentile(1),
        mean: histogram.mean(),
        std_dev: histogram.std_dev(),
    }
}

// Target values by tier
// Placeholder: range 0.1-0.2
// Temp: range 0.2-0.4
// Final: range 0.4-0.6
// Hero: range 0.5-0.7
```

### Contrast Correction

```rust
fn enhance_contrast(tex: &mut TextureBuffer, target_range: f32) {
    let current = analyze_contrast(tex);

    if current.range < target_range * 0.8 {
        // Need more contrast
        let factor = target_range / current.range;

        tex.apply_levels(Levels {
            input_black: current.min,
            input_white: current.max,
            output_black: 0.5 - target_range / 2.0,
            output_white: 0.5 + target_range / 2.0,
            gamma: 1.0,
        });
    }
}
```

---

## Color Richness Techniques

### Saturation by Tier

| Tier | Saturation Range | Notes |
|------|------------------|-------|
| Placeholder | 0.0-0.3 | Grayscale or muted |
| Temp | 0.2-0.5 | Basic color |
| Final | 0.3-0.6 | Rich but not garish |
| Hero | 0.4-0.7 | Full color depth |

### Adding Color Depth

```rust
// Vibrance (boost low-saturation colors)
tex.apply_vibrance(0.3);

// Color grading
tex.apply_lut(lut: &style_lut);

// Complementary color in shadows
tex.split_tone(
    highlights: Color::from_hsl(warm_hue, 0.3, 0.7),
    shadows: Color::from_hsl(cool_hue, 0.2, 0.3),
    balance: 0.0,  // Neutral
);
```

---

## Detail Layer System

### Layer Stack Structure

```
Layer 4: Micro detail (64x scale) - 5%
Layer 3: Fine detail (32x scale) - 10%
Layer 2: Medium detail (8x scale) - 20%
Layer 1: Large variation (2x scale) - 30%
Layer 0: Base color - 100%
```

### Implementation

```rust
fn build_layered_texture(
    base_color: Color,
    style: &StyleToken,
    tier: Tier,
) -> TextureBuffer {
    let size = tier.texture_resolution();
    let mut tex = TextureBuffer::new(size, size);

    // Base fill
    tex.fill(base_color);

    // Large variation (all tiers)
    tex.blend(
        &generate_noise(2.0, style.seed),
        BlendMode::Overlay,
        0.3,
    );

    if tier >= Tier::Temp {
        // Medium detail
        tex.blend(
            &generate_noise(8.0, style.seed + 1),
            BlendMode::SoftLight,
            0.2,
        );
    }

    if tier >= Tier::Final {
        // Fine detail
        tex.blend(
            &generate_noise(32.0, style.seed + 2),
            BlendMode::Overlay,
            0.1,
        );
    }

    if tier >= Tier::Hero {
        // Micro detail
        tex.blend(
            &generate_noise(64.0, style.seed + 3),
            BlendMode::SoftLight,
            0.05,
        );

        // Wear and imperfections
        tex.apply_wear_layer(style.wear_amount);
    }

    tex
}
```

---

## Resolution Guidelines

### Resolution by Tier and Asset Size

| Asset Size | Placeholder | Temp | Final | Hero |
|------------|-------------|------|-------|------|
| Tiny (< 0.5m) | 32x32 | 64x64 | 128x128 | 256x256 |
| Small (0.5-1m) | 64x64 | 128x128 | 256x256 | 512x512 |
| Medium (1-2m) | 64x64 | 128x128 | 256x256 | 512x512 |
| Large (2-5m) | 128x128 | 256x256 | 512x512 | 512x512 |
| Huge (> 5m) | 128x128 | 256x256 | 512x512 | 512x512* |

*Hero huge assets may need tiling or detail textures.

### Memory Budget Check

```rust
fn check_texture_budget(tex: &TextureBuffer, tier: Tier) -> bool {
    let max_bytes = match tier {
        Tier::Placeholder => 16 * 1024,   // 16 KB
        Tier::Temp => 64 * 1024,          // 64 KB
        Tier::Final => 256 * 1024,        // 256 KB
        Tier::Hero => 1024 * 1024,        // 1 MB
    };

    let tex_bytes = tex.width() * tex.height() * 4;  // RGBA
    tex_bytes <= max_bytes
}
```
