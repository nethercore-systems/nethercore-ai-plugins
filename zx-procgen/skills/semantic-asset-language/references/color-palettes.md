# Color Palettes Reference

Complete color palette definitions for SADL. Each palette defines HSL ranges for consistent, harmonious color schemes.

## Palette Structure

```rust
pub enum ColorPalette {
    // Warm palettes
    WarmEarthy,
    Autumn,
    Sunset,
    Fire,

    // Cool palettes
    CoolMetal,
    Ocean,
    Arctic,
    Night,

    // Vibrant palettes
    Neon,
    Vibrant,
    Tropical,
    Rainbow,

    // Muted palettes
    Muted,
    Grayscale,
    Sepia,
    Dusty,

    // Soft palettes
    Pastel,
    Cotton,
    Dawn,
    Lavender,

    // Monochromatic
    Monochrome,
    BloodRed,
    ForestGreen,
    RoyalBlue,
}

pub struct PaletteSpec {
    pub name: &'static str,
    pub hue_ranges: Vec<(f32, f32)>,      // Allowed hue ranges (0-360)
    pub saturation_range: (f32, f32),     // Min-max saturation (0-1)
    pub lightness_range: (f32, f32),      // Min-max lightness (0-1)
    pub accent_hue_offset: f32,           // Offset for accent colors (degrees)
    pub primary_weight: f32,              // Weight for primary vs accent (0-1)
    pub contrast_preference: f32,         // 0 = low contrast, 1 = high contrast
}
```

---

## Warm Palettes

### WarmEarthy

Natural browns, oranges, and tans for organic materials.

```rust
ColorPalette::WarmEarthy => PaletteSpec {
    name: "warm_earthy",
    hue_ranges: vec![(15.0, 45.0)],       // Orange-brown range
    saturation_range: (0.3, 0.6),
    lightness_range: (0.2, 0.5),
    accent_hue_offset: 30.0,              // Yellow accents
    primary_weight: 0.8,
    contrast_preference: 0.4,
}
```

| Role | HSL Range | Hex Examples |
|------|-----------|--------------|
| Primary | H:20-35, S:40-55%, L:25-40% | #8B4513, #A0522D, #6B4423 |
| Accent | H:45-60, S:50-70%, L:40-55% | #DAA520, #CD853F, #D2691E |
| Dark | H:20-30, S:30-40%, L:15-25% | #3D2817, #4A3728, #2F1E0E |
| Light | H:30-45, S:25-40%, L:55-70% | #DEB887, #D2B48C, #C4A35A |

**Use for:** Wood, leather, earth, sand, clay, rope, burlap.

---

### Autumn

Fall foliage - reds, oranges, yellows, browns.

```rust
ColorPalette::Autumn => PaletteSpec {
    name: "autumn",
    hue_ranges: vec![(0.0, 50.0)],        // Red through yellow
    saturation_range: (0.5, 0.8),
    lightness_range: (0.3, 0.55),
    accent_hue_offset: -20.0,             // Deep red accents
    primary_weight: 0.6,
    contrast_preference: 0.5,
}
```

| Role | HSL Range | Hex Examples |
|------|-----------|--------------|
| Primary | H:25-40, S:60-75%, L:40-50% | #D2691E, #CD853F, #E67E22 |
| Accent | H:0-15, S:65-80%, L:35-45% | #B22222, #A52A2A, #8B0000 |
| Gold | H:45-55, S:70-85%, L:45-55% | #DAA520, #FFD700, #F4A460 |

**Use for:** Forests, harvest themes, cozy interiors, seasonal content.

---

### Sunset

Warm gradient from yellow through orange to purple.

```rust
ColorPalette::Sunset => PaletteSpec {
    name: "sunset",
    hue_ranges: vec![(0.0, 60.0), (280.0, 320.0)],  // Warm + purple
    saturation_range: (0.6, 0.9),
    lightness_range: (0.4, 0.65),
    accent_hue_offset: 180.0,             // Complementary
    primary_weight: 0.5,
    contrast_preference: 0.6,
}
```

**Use for:** Skies, magical effects, romantic scenes, warm lighting.

---

### Fire

Intense flames - reds, oranges, yellows, whites.

```rust
ColorPalette::Fire => PaletteSpec {
    name: "fire",
    hue_ranges: vec![(0.0, 45.0)],        // Red to yellow
    saturation_range: (0.8, 1.0),
    lightness_range: (0.4, 0.7),
    accent_hue_offset: 0.0,
    primary_weight: 0.4,                  // Lots of variation
    contrast_preference: 0.8,
}
```

**Use for:** Flames, explosions, lava, emissive materials.

---

## Cool Palettes

### CoolMetal

Silvers, blues, and grays for metallic surfaces.

```rust
ColorPalette::CoolMetal => PaletteSpec {
    name: "cool_metal",
    hue_ranges: vec![(200.0, 240.0)],     // Blue-gray range
    saturation_range: (0.1, 0.3),
    lightness_range: (0.4, 0.7),
    accent_hue_offset: 30.0,              // Cyan accents
    primary_weight: 0.85,
    contrast_preference: 0.5,
}
```

| Role | HSL Range | Hex Examples |
|------|-----------|--------------|
| Primary | H:210-230, S:10-25%, L:50-65% | #708090, #778899, #6B7B8C |
| Highlight | H:200-220, S:5-15%, L:75-90% | #C0C0C0, #D3D3D3, #E8E8E8 |
| Shadow | H:220-240, S:15-25%, L:25-40% | #2F4F4F, #3D4F5F, #4A5568 |
| Accent | H:180-200, S:30-50%, L:50-60% | #5F9EA0, #4682B4, #6495ED |

**Use for:** Steel, chrome, iron, aluminum, sci-fi tech.

---

### Ocean

Deep blues and teals with foam highlights.

```rust
ColorPalette::Ocean => PaletteSpec {
    name: "ocean",
    hue_ranges: vec![(180.0, 220.0)],     // Cyan to blue
    saturation_range: (0.4, 0.7),
    lightness_range: (0.25, 0.55),
    accent_hue_offset: -30.0,             // Green-teal accents
    primary_weight: 0.7,
    contrast_preference: 0.6,
}
```

**Use for:** Water, underwater scenes, nautical themes, ice.

---

### Arctic

Icy blues, whites, and pale cyans.

```rust
ColorPalette::Arctic => PaletteSpec {
    name: "arctic",
    hue_ranges: vec![(190.0, 210.0)],     // Pale cyan-blue
    saturation_range: (0.15, 0.4),
    lightness_range: (0.7, 0.95),
    accent_hue_offset: 20.0,
    primary_weight: 0.8,
    contrast_preference: 0.3,             // Low contrast
}
```

**Use for:** Snow, ice, frozen environments, winter themes.

---

### Night

Deep blues and purples with star-like highlights.

```rust
ColorPalette::Night => PaletteSpec {
    name: "night",
    hue_ranges: vec![(220.0, 280.0)],     // Blue to purple
    saturation_range: (0.3, 0.6),
    lightness_range: (0.1, 0.3),
    accent_hue_offset: 60.0,              // Cyan stars
    primary_weight: 0.75,
    contrast_preference: 0.7,
}
```

**Use for:** Night skies, dark environments, shadows, mystery.

---

## Vibrant Palettes

### Neon

High-saturation magentas, cyans, and greens.

```rust
ColorPalette::Neon => PaletteSpec {
    name: "neon",
    hue_ranges: vec![(280.0, 320.0), (160.0, 200.0)],  // Magenta + Cyan
    saturation_range: (0.8, 1.0),
    lightness_range: (0.5, 0.7),
    accent_hue_offset: 120.0,             // Complementary neon
    primary_weight: 0.5,                  // Equal distribution
    contrast_preference: 0.9,             // High contrast
}
```

| Role | HSL Range | Hex Examples |
|------|-----------|--------------|
| Magenta | H:290-315, S:85-100%, L:55-65% | #FF00FF, #FF1493, #DA70D6 |
| Cyan | H:170-195, S:85-100%, L:50-60% | #00FFFF, #00CED1, #40E0D0 |
| Green | H:100-140, S:80-100%, L:45-55% | #00FF00, #32CD32, #39FF14 |

**Use for:** Cyberpunk, arcade, signs, UI highlights, tech.

---

### Vibrant

High-saturation, full spectrum colors.

```rust
ColorPalette::Vibrant => PaletteSpec {
    name: "vibrant",
    hue_ranges: vec![(0.0, 360.0)],       // Full spectrum
    saturation_range: (0.7, 1.0),
    lightness_range: (0.4, 0.6),
    accent_hue_offset: 180.0,             // Complementary
    primary_weight: 0.5,
    contrast_preference: 0.7,
}
```

**Use for:** Cartoons, fantasy, toys, celebrations.

---

### Tropical

Bright greens, blues, pinks, and yellows.

```rust
ColorPalette::Tropical => PaletteSpec {
    name: "tropical",
    hue_ranges: vec![(80.0, 180.0), (320.0, 360.0)],  // Greens/cyans + pinks
    saturation_range: (0.6, 0.9),
    lightness_range: (0.45, 0.65),
    accent_hue_offset: 40.0,
    primary_weight: 0.6,
    contrast_preference: 0.6,
}
```

**Use for:** Jungles, beaches, exotic locations, summer themes.

---

### Rainbow

Full spectrum with even distribution.

```rust
ColorPalette::Rainbow => PaletteSpec {
    name: "rainbow",
    hue_ranges: vec![(0.0, 360.0)],       // Full spectrum
    saturation_range: (0.75, 0.95),
    lightness_range: (0.5, 0.6),
    accent_hue_offset: 30.0,              // Adjacent colors
    primary_weight: 0.3,                  // Highly varied
    contrast_preference: 0.5,
}
```

**Use for:** Pride themes, magical effects, color variety.

---

## Muted Palettes

### Muted

Low saturation, any hue - worn, aged look.

```rust
ColorPalette::Muted => PaletteSpec {
    name: "muted",
    hue_ranges: vec![(0.0, 360.0)],       // Any hue
    saturation_range: (0.1, 0.3),
    lightness_range: (0.3, 0.6),
    accent_hue_offset: 180.0,
    primary_weight: 0.7,
    contrast_preference: 0.4,
}
```

**Use for:** Stone, concrete, old fabric, faded materials.

---

### Grayscale

Pure black to white, no color.

```rust
ColorPalette::Grayscale => PaletteSpec {
    name: "grayscale",
    hue_ranges: vec![(0.0, 0.0)],         // No hue
    saturation_range: (0.0, 0.0),
    lightness_range: (0.0, 1.0),
    accent_hue_offset: 0.0,
    primary_weight: 0.5,
    contrast_preference: 0.6,
}
```

**Use for:** Noir, sketches, shadows, colorblind-friendly.

---

### Sepia

Warm brown monochrome, vintage feel.

```rust
ColorPalette::Sepia => PaletteSpec {
    name: "sepia",
    hue_ranges: vec![(30.0, 45.0)],       // Warm brown
    saturation_range: (0.2, 0.4),
    lightness_range: (0.2, 0.7),
    accent_hue_offset: 0.0,
    primary_weight: 0.9,
    contrast_preference: 0.5,
}
```

**Use for:** Old photos, vintage, historical, paper.

---

### Dusty

Desaturated, slightly warm - desert/dust feel.

```rust
ColorPalette::Dusty => PaletteSpec {
    name: "dusty",
    hue_ranges: vec![(20.0, 60.0)],       // Warm beiges
    saturation_range: (0.15, 0.35),
    lightness_range: (0.4, 0.65),
    accent_hue_offset: 180.0,
    primary_weight: 0.8,
    contrast_preference: 0.3,
}
```

**Use for:** Deserts, dusty roads, old west, archaeological.

---

## Soft Palettes

### Pastel

Soft, light, low-saturation pastels.

```rust
ColorPalette::Pastel => PaletteSpec {
    name: "pastel",
    hue_ranges: vec![(0.0, 360.0)],       // Any hue
    saturation_range: (0.3, 0.5),
    lightness_range: (0.7, 0.85),
    accent_hue_offset: 30.0,
    primary_weight: 0.6,
    contrast_preference: 0.2,             // Low contrast
}
```

| Role | HSL Range | Hex Examples |
|------|-----------|--------------|
| Pink | H:330-350, S:35-45%, L:75-82% | #FFB6C1, #FFC0CB, #FFD1DC |
| Blue | H:200-220, S:35-50%, L:75-85% | #ADD8E6, #B0E0E6, #87CEEB |
| Green | H:100-140, S:30-45%, L:70-80% | #98FB98, #90EE90, #8FBC8F |
| Yellow | H:45-60, S:40-55%, L:75-85% | #FFFACD, #FAFAD2, #FFFFE0 |
| Purple | H:270-290, S:35-50%, L:75-82% | #DDA0DD, #E6E6FA, #D8BFD8 |

**Use for:** Soft UI, cute characters, dreamy scenes, kawaii aesthetic.

---

### Cotton

Soft whites and very pale colors.

```rust
ColorPalette::Cotton => PaletteSpec {
    name: "cotton",
    hue_ranges: vec![(0.0, 360.0)],
    saturation_range: (0.05, 0.2),
    lightness_range: (0.85, 0.98),
    accent_hue_offset: 60.0,
    primary_weight: 0.9,
    contrast_preference: 0.1,
}
```

**Use for:** Clouds, soft fabrics, minimal UI, clean spaces.

---

### Dawn

Soft pinks, oranges, and pale blues of sunrise.

```rust
ColorPalette::Dawn => PaletteSpec {
    name: "dawn",
    hue_ranges: vec![(320.0, 60.0), (200.0, 220.0)],  // Pinks/oranges + pale blue
    saturation_range: (0.25, 0.5),
    lightness_range: (0.65, 0.85),
    accent_hue_offset: 180.0,
    primary_weight: 0.5,
    contrast_preference: 0.3,
}
```

**Use for:** Sunrise, soft lighting, peaceful scenes.

---

### Lavender

Soft purples and pinks.

```rust
ColorPalette::Lavender => PaletteSpec {
    name: "lavender",
    hue_ranges: vec![(260.0, 310.0)],     // Purple-pink range
    saturation_range: (0.25, 0.45),
    lightness_range: (0.65, 0.82),
    accent_hue_offset: 40.0,
    primary_weight: 0.75,
    contrast_preference: 0.25,
}
```

**Use for:** Flowers, soft magic, relaxing scenes.

---

## Monochromatic Palettes

### Monochrome

Single hue with varied saturation and lightness.

```rust
ColorPalette::Monochrome => PaletteSpec {
    name: "monochrome",
    // Hue is set dynamically based on user choice
    hue_ranges: vec![(0.0, 0.0)],         // Single hue (configurable)
    saturation_range: (0.2, 0.8),
    lightness_range: (0.15, 0.85),
    accent_hue_offset: 0.0,               // Same hue
    primary_weight: 0.5,
    contrast_preference: 0.6,
}

impl Monochrome {
    pub fn with_hue(hue: f32) -> PaletteSpec {
        PaletteSpec {
            hue_ranges: vec![(hue, hue)],
            ..Monochrome::default()
        }
    }
}
```

---

### BloodRed

Deep reds monochrome.

```rust
ColorPalette::BloodRed => PaletteSpec {
    name: "blood_red",
    hue_ranges: vec![(350.0, 10.0)],      // Red
    saturation_range: (0.5, 0.9),
    lightness_range: (0.15, 0.5),
    accent_hue_offset: 0.0,
    primary_weight: 0.7,
    contrast_preference: 0.7,
}
```

**Use for:** Horror, violence, danger, passion.

---

### ForestGreen

Deep greens monochrome.

```rust
ColorPalette::ForestGreen => PaletteSpec {
    name: "forest_green",
    hue_ranges: vec![(100.0, 150.0)],     // Green
    saturation_range: (0.3, 0.7),
    lightness_range: (0.15, 0.45),
    accent_hue_offset: 0.0,
    primary_weight: 0.7,
    contrast_preference: 0.5,
}
```

**Use for:** Forests, nature, camouflage, elves.

---

### RoyalBlue

Deep blues monochrome.

```rust
ColorPalette::RoyalBlue => PaletteSpec {
    name: "royal_blue",
    hue_ranges: vec![(220.0, 250.0)],     // Blue
    saturation_range: (0.5, 0.8),
    lightness_range: (0.2, 0.5),
    accent_hue_offset: 0.0,
    primary_weight: 0.7,
    contrast_preference: 0.6,
}
```

**Use for:** Royalty, night, water, tech interfaces.

---

## Utility Functions

### HSL to RGB Conversion

```rust
pub fn hsl_to_rgb(h: f32, s: f32, l: f32) -> [f32; 3] {
    let c = (1.0 - (2.0 * l - 1.0).abs()) * s;
    let x = c * (1.0 - ((h / 60.0) % 2.0 - 1.0).abs());
    let m = l - c / 2.0;

    let (r, g, b) = match (h as i32) / 60 {
        0 => (c, x, 0.0),
        1 => (x, c, 0.0),
        2 => (0.0, c, x),
        3 => (0.0, x, c),
        4 => (x, 0.0, c),
        _ => (c, 0.0, x),
    };

    [r + m, g + m, b + m]
}
```

### Palette Sampling

```rust
impl ColorPalette {
    /// Sample a random color from this palette
    pub fn sample(&self, rng: &mut impl Rng) -> [f32; 3] {
        let spec = self.spec();
        let range_idx = rng.gen_range(0..spec.hue_ranges.len());
        let (h_min, h_max) = spec.hue_ranges[range_idx];

        let h = rng.gen_range(h_min..h_max);
        let s = rng.gen_range(spec.saturation_range.0..spec.saturation_range.1);
        let l = rng.gen_range(spec.lightness_range.0..spec.lightness_range.1);

        hsl_to_rgb(h, s, l)
    }

    /// Sample a contrasting pair (primary + accent)
    pub fn sample_pair(&self, rng: &mut impl Rng) -> ([f32; 3], [f32; 3]) {
        let spec = self.spec();
        let primary = self.sample(rng);

        // Sample accent with hue offset
        let (h_min, h_max) = spec.hue_ranges[0];
        let accent_h = ((h_min + h_max) / 2.0 + spec.accent_hue_offset) % 360.0;
        let accent_s = rng.gen_range(spec.saturation_range.0..spec.saturation_range.1);
        let accent_l = rng.gen_range(spec.lightness_range.0..spec.lightness_range.1);

        (primary, hsl_to_rgb(accent_h, accent_s, accent_l))
    }

    /// Sample a full palette (primary, secondary, accent, dark, light)
    pub fn sample_full(&self, rng: &mut impl Rng) -> FullPalette {
        let spec = self.spec();

        FullPalette {
            primary: self.sample(rng),
            secondary: self.sample(rng),
            accent: self.sample_accent(rng),
            dark: self.sample_dark(rng),
            light: self.sample_light(rng),
        }
    }
}
```

### Blending Palettes

```rust
pub fn blend_palettes(a: &PaletteSpec, b: &PaletteSpec, weight: f32) -> PaletteSpec {
    let w = weight.clamp(0.0, 1.0);
    let inv = 1.0 - w;

    PaletteSpec {
        name: "blended",
        hue_ranges: blend_hue_ranges(&a.hue_ranges, &b.hue_ranges, w),
        saturation_range: (
            a.saturation_range.0 * inv + b.saturation_range.0 * w,
            a.saturation_range.1 * inv + b.saturation_range.1 * w,
        ),
        lightness_range: (
            a.lightness_range.0 * inv + b.lightness_range.0 * w,
            a.lightness_range.1 * inv + b.lightness_range.1 * w,
        ),
        accent_hue_offset: a.accent_hue_offset * inv + b.accent_hue_offset * w,
        primary_weight: a.primary_weight * inv + b.primary_weight * w,
        contrast_preference: a.contrast_preference * inv + b.contrast_preference * w,
    }
}
```
