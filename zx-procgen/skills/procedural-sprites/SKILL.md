---
name: Procedural 2D Sprites & Pixel Art
description: |
  Use this skill to GENERATE 2D assets for ZX games. Trigger phrases: "pixel art", "sprite sheet", "tileset", "autotile", "9-slice", "UI sprite", "health bar", "dithering", "indexed palette".

  **Before generating:** Check `.studio/visual-style.local.md` for project style specs (color palette, pixel density, dithering style). Apply those constraints for consistent sprites. If no style exists, ask about visual style.

  Covers palette quantization, dithering algorithms, tilesets, UI elements, character sheets.

  For 3D TEXTURES (render modes, MRE/SSE): use procedural-textures.
  For NOISE ALGORITHMS (base patterns for sprites): see procedural-textures noise reference.
version: 1.2.0
---

# Procedural 2D Sprites & Pixel Art

## Overview

Generate 2D pixel art assets for ZX games including sprites, UI elements, tilesets, and sprite sheets. This skill covers color quantization, dithering algorithms, and sprite organization patterns.

**Output Requirements:**
- Format: PNG (RGBA or indexed)
- Color: Indexed palettes (4-256 colors) or full RGBA
- Compatible with: `draw_sprite()`, `draw_sprite_region()`

**Key Difference from 3D Textures:** Sprites use indexed color palettes and dithering for authentic pixel art aesthetics, while 3D textures use continuous color gradients.

---

## Indexed Palette Generation

Reduce full-color images to limited palettes using color quantization algorithms.

### Median Cut Algorithm

Split color space recursively along the widest channel:

```rust
/// Generate indexed palette using median cut
fn generate_palette(colors: &[u32], max_colors: usize) -> Vec<u32> {
    let mut buckets = vec![colors.to_vec()];

    while buckets.len() < max_colors {
        // Find bucket with widest color range
        let (idx, axis) = find_widest_bucket(&buckets);
        let bucket = buckets.remove(idx);

        // Split along widest axis (R, G, or B)
        let (low, high) = split_bucket(&bucket, axis);
        buckets.push(low);
        buckets.push(high);
    }

    // Average each bucket to get palette color
    buckets.iter().map(|b| average_color(b)).collect()
}

fn find_widest_bucket(buckets: &[Vec<u32>]) -> (usize, usize) {
    buckets.iter().enumerate()
        .map(|(i, b)| (i, channel_range(b)))
        .max_by_key(|(_, (_, range))| *range)
        .map(|(i, (axis, _))| (i, axis))
        .unwrap_or((0, 0))
}
```

### Python Palette Generation

```python
from PIL import Image
import numpy as np

def generate_palette(image_path, num_colors=16):
    """Extract palette using PIL's quantize."""
    img = Image.open(image_path).convert('RGB')
    quantized = img.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette()[:num_colors * 3]

    # Convert to 0xRRGGBBAA format
    return [
        (palette[i] << 24) | (palette[i+1] << 16) | (palette[i+2] << 8) | 0xFF
        for i in range(0, len(palette), 3)
    ]
```

### Quantizing Pixels to Palette

```rust
fn quantize_to_palette(color: u32, palette: &[u32]) -> u32 {
    palette.iter()
        .min_by_key(|&&p| color_distance(color, p))
        .copied()
        .unwrap_or(color)
}

fn color_distance(a: u32, b: u32) -> u32 {
    let dr = ((a >> 24) & 0xFF) as i32 - ((b >> 24) & 0xFF) as i32;
    let dg = ((a >> 16) & 0xFF) as i32 - ((b >> 16) & 0xFF) as i32;
    let db = ((a >> 8) & 0xFF) as i32 - ((b >> 8) & 0xFF) as i32;
    (dr * dr + dg * dg + db * db) as u32
}
```

---

## Dithering Algorithms

Simulate more colors with limited palettes by distributing quantization error.

### Ordered Dithering (Bayer Matrix)

Predictable, fast, no error propagation. Creates characteristic crosshatch patterns:

```rust
/// Bayer 4x4 dither matrix (normalized 0-1)
const BAYER_4X4: [f32; 16] = [
     0.0/16.0,  8.0/16.0,  2.0/16.0, 10.0/16.0,
    12.0/16.0,  4.0/16.0, 14.0/16.0,  6.0/16.0,
     3.0/16.0, 11.0/16.0,  1.0/16.0,  9.0/16.0,
    15.0/16.0,  7.0/16.0, 13.0/16.0,  5.0/16.0,
];

fn apply_ordered_dither(tex: &mut TextureBuffer, palette: &[u32], matrix_size: usize) {
    let bayer = match matrix_size {
        2 => &BAYER_2X2,
        4 => &BAYER_4X4,
        8 => &BAYER_8X8,
        _ => &BAYER_4X4,
    };

    for y in 0..tex.height {
        for x in 0..tex.width {
            let pixel = tex.get(x, y);
            let threshold = bayer[(y % matrix_size) * matrix_size + (x % matrix_size)];

            // Adjust pixel brightness by threshold before quantizing
            let adjusted = adjust_by_threshold(pixel, threshold - 0.5);
            let nearest = quantize_to_palette(adjusted, palette);
            tex.set(x, y, nearest);
        }
    }
}
```

### Error Diffusion (Floyd-Steinberg)

Distributes quantization error to neighboring pixels for smoother gradients:

```rust
/// Floyd-Steinberg error diffusion weights
///        X   7/16
/// 3/16  5/16  1/16

fn apply_floyd_steinberg(tex: &mut TextureBuffer, palette: &[u32]) {
    let (w, h) = (tex.width as i32, tex.height as i32);
    let mut errors = vec![[0i32; 3]; (w * h) as usize];

    for y in 0..h {
        for x in 0..w {
            let idx = (y * w + x) as usize;
            let pixel = tex.get(x as u32, y as u32);

            // Add accumulated error
            let adjusted = add_error(pixel, errors[idx]);
            let quantized = quantize_to_palette(adjusted, palette);
            tex.set(x as u32, y as u32, quantized);

            // Calculate and distribute error
            let err = calculate_error(adjusted, quantized);
            if x + 1 < w { distribute_error(&mut errors, w, x+1, y, err, 7.0/16.0); }
            if y + 1 < h {
                if x > 0 { distribute_error(&mut errors, w, x-1, y+1, err, 3.0/16.0); }
                distribute_error(&mut errors, w, x, y+1, err, 5.0/16.0);
                if x + 1 < w { distribute_error(&mut errors, w, x+1, y+1, err, 1.0/16.0); }
            }
        }
    }
}
```

### Python Dithering

```python
from PIL import Image

def ordered_dither(img, palette, matrix_size=4):
    """Apply Bayer ordered dithering."""
    bayer_4x4 = np.array([
        [0, 8, 2, 10], [12, 4, 14, 6],
        [3, 11, 1, 9], [15, 7, 13, 5]
    ]) / 16.0

    pixels = np.array(img, dtype=np.float32)
    h, w = pixels.shape[:2]

    for y in range(h):
        for x in range(w):
            threshold = bayer_4x4[y % 4, x % 4] - 0.5
            pixels[y, x] += threshold * 32  # Adjust strength
            pixels[y, x] = find_nearest_palette(pixels[y, x], palette)

    return Image.fromarray(pixels.astype(np.uint8))
```

---

## UI Sprite Generation

### 9-Slice Panel Generation

Generate UI panels that can be scaled without stretching corners. **Note:** ZX has no runtime 9-slice support; generate pre-scaled variants or implement slicing in game code.

```rust
fn generate_9slice_panel(
    width: u32, height: u32,
    corner_size: u32,
    border_color: u32,
    fill_color: u32,
    shadow_color: u32,
) -> TextureBuffer {
    let mut tex = TextureBuffer::new(width, height);
    tex.solid(fill_color);

    // Draw border (1px)
    for x in 0..width {
        tex.set(x, 0, border_color);              // Top
        tex.set(x, height - 1, shadow_color);     // Bottom (shadow)
    }
    for y in 0..height {
        tex.set(0, y, border_color);              // Left
        tex.set(width - 1, y, shadow_color);      // Right (shadow)
    }

    // Inner highlight (optional)
    for x in 1..(width - 1) {
        tex.set(x, 1, lighten(fill_color, 0.2));
    }

    tex
}

/// 9-slice regions for game code slicing
pub struct NineSlice {
    pub left: u32, pub right: u32, pub top: u32, pub bottom: u32,
}

impl NineSlice {
    pub fn uniform(border: u32) -> Self {
        Self { left: border, right: border, top: border, bottom: border }
    }
}
```

### Health Bar Generation

```rust
fn generate_health_bar(
    width: u32, height: u32,
    segments: u32,
    fill_color: u32,
    empty_color: u32,
    border_color: u32,
) -> TextureBuffer {
    let mut tex = TextureBuffer::new(width, height);
    tex.solid(border_color);

    let inner_width = width - 2;
    let segment_width = inner_width / segments;

    for seg in 0..segments {
        let x = 1 + seg * segment_width;
        // First half filled, second half empty (for demonstration)
        let color = if seg < segments / 2 { fill_color } else { empty_color };

        for sy in 1..(height - 1) {
            for sx in x..(x + segment_width - 1) {
                tex.set(sx, sy, color);
            }
        }
    }

    tex
}
```

### Button States

Generate sprite sheet with 4 states (normal, hover, pressed, disabled):

```rust
fn generate_button_sheet(
    button_width: u32, button_height: u32,
    base_color: u32,
    text_area: bool,
) -> TextureBuffer {
    // 4 states arranged horizontally
    let sheet_width = button_width * 4;
    let mut tex = TextureBuffer::new(sheet_width, button_height);

    let states = [
        (base_color, 0.0, 0.2),      // Normal: base, no darken, slight highlight
        (base_color, 0.0, 0.3),      // Hover: brighter highlight
        (darken(base_color, 0.15), 0.0, 0.0),  // Pressed: darker, no highlight
        (desaturate(base_color, 0.5), 0.2, 0.0), // Disabled: desaturated
    ];

    for (i, (color, shadow, highlight)) in states.iter().enumerate() {
        let x_offset = i as u32 * button_width;
        draw_button_state(&mut tex, x_offset, button_width, button_height,
                         *color, *shadow, *highlight);
    }

    tex
}
```

---

## Tileset Generation

### Autotile Patterns

Generate tiles that automatically connect based on neighbors. Three common systems:

| System | Tiles | Complexity | Use Case |
|--------|-------|------------|----------|
| 2-corner (16) | 16 | Simple | Basic terrain |
| 4-corner (47) | 47 | Medium | Standard RPG tiles |
| Blob (256) | 256 | Complex | Smooth transitions |

```rust
/// Generate 47-tile autotile set (4-corner blob style)
fn generate_autotile_set(
    tile_size: u32,
    terrain_color: u32,
    edge_color: u32,
    corner_style: CornerStyle,
) -> TextureBuffer {
    let atlas_width = tile_size * 8;  // 8 columns
    let atlas_height = tile_size * 6; // 6 rows = 48 slots
    let mut atlas = TextureBuffer::new(atlas_width, atlas_height);

    for tile_id in 0..47 {
        let neighbors = AUTOTILE_47_MAP[tile_id];
        let tile = generate_single_autotile(
            tile_size, terrain_color, edge_color, neighbors, corner_style,
        );

        let col = tile_id % 8;
        let row = tile_id / 8;
        atlas.blit(&tile, col as u32 * tile_size, row as u32 * tile_size);
    }

    atlas
}

#[derive(Clone, Copy)]
pub enum CornerStyle { Square, Rounded, Beveled }

/// Neighbor flags for autotiling
pub struct Neighbors {
    pub n: bool, pub s: bool, pub e: bool, pub w: bool,
    pub ne: bool, pub nw: bool, pub se: bool, pub sw: bool,
}
```

### Tile Variations

Add visual interest with randomized variations:

```rust
fn generate_tile_variations(
    base_tile: &TextureBuffer,
    variation_count: u32,
    noise_intensity: f32,
    seed: u64,
) -> TextureBuffer {
    let tile_size = base_tile.width;
    let mut atlas = TextureBuffer::new(tile_size * variation_count, tile_size);

    for v in 0..variation_count {
        let mut variant = base_tile.clone();
        let var_seed = seed + v as u64;

        // Add subtle noise variation
        for y in 0..tile_size {
            for x in 0..tile_size {
                let noise = snoise2(x as f32 * 0.1, y as f32 * 0.1, var_seed);
                let pixel = variant.get(x, y);
                variant.set(x, y, vary_brightness(pixel, noise * noise_intensity));
            }
        }

        atlas.blit(&variant, v * tile_size, 0);
    }

    atlas
}
```

### Animated Tiles

Generate animation frames for water, lava, etc.:

```rust
fn generate_animated_tile(
    tile_size: u32,
    frame_count: u32,
    base_color: u32,
    animation_type: AnimationType,
    seed: u64,
) -> TextureBuffer {
    let mut atlas = TextureBuffer::new(tile_size * frame_count, tile_size);

    for frame in 0..frame_count {
        let phase = frame as f32 / frame_count as f32 * std::f32::consts::TAU;
        let mut tile = TextureBuffer::new(tile_size, tile_size);

        match animation_type {
            AnimationType::Water => {
                // Scrolling sine wave pattern
                for y in 0..tile_size {
                    for x in 0..tile_size {
                        let wave = ((x as f32 * 0.3 + phase).sin() * 0.5 + 0.5);
                        tile.set(x, y, blend_colors(base_color, darken(base_color, 0.3), wave));
                    }
                }
            }
            AnimationType::Lava => {
                // Bubbling noise
                for y in 0..tile_size {
                    for x in 0..tile_size {
                        let n = snoise3(x as f32 * 0.1, y as f32 * 0.1, phase, seed);
                        let glow = if n > 0.3 { lighten(base_color, n * 0.5) } else { base_color };
                        tile.set(x, y, glow);
                    }
                }
            }
        }

        atlas.blit(&tile, frame * tile_size, 0);
    }

    atlas
}

enum AnimationType { Water, Lava, Sparkle }
```

---

## Sprite Sheet Organization

### Character Sprite Layout

Standard layout for character sprite sheets:

```rust
/// Generate character sprite sheet layout
/// Rows: directions (down, left, right, up)
/// Columns: animation frames
fn generate_character_sheet_template(
    sprite_width: u32,
    sprite_height: u32,
    directions: u32,      // 4 or 8
    frames_per_dir: u32,  // typically 4 (idle, walk1, walk2, walk3)
) -> (u32, u32, CharacterLayout) {
    let sheet_width = sprite_width * frames_per_dir;
    let sheet_height = sprite_height * directions;

    let layout = CharacterLayout {
        sprite_size: (sprite_width, sprite_height),
        directions,
        frames_per_dir,
        // Direction row indices (standard RPG order)
        down: 0, left: 1, right: 2, up: 3,
    };

    (sheet_width, sheet_height, layout)
}

struct CharacterLayout {
    sprite_size: (u32, u32),
    directions: u32,
    frames_per_dir: u32,
    down: u32, left: u32, right: u32, up: u32,
}
```

### Palette Swaps

Generate color variants for enemy types:

```rust
fn generate_palette_swap(
    source: &TextureBuffer,
    source_palette: &[u32],
    target_palette: &[u32],
) -> TextureBuffer {
    assert_eq!(source_palette.len(), target_palette.len());

    let mut result = source.clone();
    let palette_map: HashMap<u32, u32> = source_palette.iter()
        .zip(target_palette.iter())
        .map(|(&s, &t)| (s, t))
        .collect();

    for y in 0..result.height {
        for x in 0..result.width {
            let pixel = result.get(x, y);
            if let Some(&replacement) = palette_map.get(&pixel) {
                result.set(x, y, replacement);
            }
        }
    }

    result
}

// Example: Generate enemy variants
let base_slime = load_sprite("slime_green.png");
let green_palette = [0x22AA22FF, 0x118811FF, 0x005500FF];
let red_palette = [0xAA2222FF, 0x881111FF, 0x550000FF];
let blue_palette = [0x2222AAFF, 0x111188FF, 0x000055FF];

let red_slime = generate_palette_swap(&base_slime, &green_palette, &red_palette);
let blue_slime = generate_palette_swap(&base_slime, &green_palette, &blue_palette);
```

---

## ZX Integration

### Using Generated Sprites

```rust
fn init() {
    // Load sprite sheet
    let sprites = asset_load("sprites/ui_elements.png");
}

fn draw() {
    // Draw full sprite
    draw_sprite(sprites, x, y);

    // Draw region from sprite sheet (button state 2 = pressed)
    draw_sprite_region(
        sprites,
        x, y,                    // screen position
        button_width * 2, 0,     // source x, y (3rd button state)
        button_width, button_height,  // source width, height
    );
}
```

### nether.toml Configuration

```toml
# Sprite sheets
[[assets.textures]]
id = "ui-sprites"
path = "assets/sprites/ui_elements.png"
filter = "nearest"  # Critical for pixel art

[[assets.textures]]
id = "tileset"
path = "assets/sprites/terrain_autotile.png"
filter = "nearest"

[[assets.textures]]
id = "player"
path = "assets/sprites/player_sheet.png"
filter = "nearest"
```

---

## Quick Reference

| Task | Algorithm | When to Use |
|------|-----------|-------------|
| Color reduction | Median cut | General purpose, good quality |
| Color reduction | K-means | Better quality, slower |
| Smooth gradients | Floyd-Steinberg | Photos, gradients |
| Retro patterns | Bayer ordered | Authentic pixel art look |
| Sharp edges | No dithering | UI, text, icons |

| Sprite Type | Typical Size | Notes |
|-------------|--------------|-------|
| UI icon | 16x16, 32x32 | Power of 2 for efficiency |
| Character | 32x32, 64x64 | 4-8 directions, 3-4 frames each |
| Tile | 16x16, 32x32 | Must tile seamlessly |
| Health bar | 64x8, 128x12 | Segmented or continuous |

---

## CRITICAL: Code Organization & File Size Limits

**Sprite generation code (especially autotile) bloats RAPIDLY. Strict limits required:**

| Limit | Lines | Action |
|-------|-------|--------|
| Target | ≤300 | Ideal file size |
| Soft limit | 400 | Consider splitting |
| Hard limit | 500 | MUST split immediately |
| Unacceptable | >500 | Never generate |

### Mandatory Splitting Strategy

Sprite code has massive data tables. Use this structure:

```
generator/src/
├── main.rs              # Entry point only (~50 lines)
├── lib.rs               # Module exports (~30 lines)
├── sprites/
│   ├── mod.rs           # Re-exports (~20 lines)
│   ├── ui.rs            # Buttons, panels, bars (~150 lines)
│   ├── tiles.rs         # Basic tile generation (~100 lines)
│   ├── autotile.rs      # Autotile logic (~150 lines)
│   └── characters.rs    # Sprite sheet generation (~150 lines)
├── palette/
│   ├── mod.rs           # Palette exports
│   ├── quantize.rs      # Median cut, k-means (~100 lines)
│   └── dither.rs        # Bayer, Floyd-Steinberg (~100 lines)
├── data/
│   ├── mod.rs           # Data exports
│   ├── autotile_47.rs   # 47-tile neighbor map (~80 lines, DATA ONLY)
│   ├── autotile_256.rs  # 256-tile blob map (~150 lines, DATA ONLY)
│   └── palettes.rs      # NES, PICO-8, etc (~80 lines, DATA ONLY)
└── constants.rs         # Dimensions, colors (~50 lines)
```

### CRITICAL: Data vs Code Separation

Autotile neighbor maps and palettes are **DATA**, not code. Extract them:

```rust
// data/autotile_47.rs - DATA ONLY
pub const AUTOTILE_47_MAP: [Neighbors; 47] = [
    Neighbors { n: false, s: false, e: false, w: false, .. },
    Neighbors { n: true,  s: false, e: false, w: false, .. },
    // ... all 47 entries
];

// data/palettes.rs - DATA ONLY
pub const PICO8_PALETTE: [u32; 16] = [
    0x000000FF, 0x1D2B53FF, 0x7E2553FF, ...
];
```

### Large Table Pattern

**NEVER inline large lookup tables.** 47-tile and 256-tile maps go in data modules:

```rust
// BAD: Inline 256-entry table in function
fn get_tile_index(neighbors: u8) -> usize {
    match neighbors {
        0b00000000 => 0,
        0b00000001 => 1,
        // ... 256 lines of matches
    }
}

// GOOD: Lookup table in data module
use crate::data::autotile_256::BLOB_TILE_MAP;

fn get_tile_index(neighbors: u8) -> usize {
    BLOB_TILE_MAP[neighbors as usize]
}
```

---

## Additional Resources

### Reference Files

For detailed patterns and data tables:
- **`references/autotile-patterns.md`** - Complete neighbor mapping tables for 16/47/256 tile systems
- **`references/palettes.md`** - Classic game palettes (NES, PICO-8, etc.) and quantization details

### Related Skills

- **`procedural-textures`** - Noise algorithms used as base for sprite generation
- **`retro-3d-assets`** - Low-poly 3D with pixel art textures
