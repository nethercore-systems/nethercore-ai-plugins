# Gap 24: 2D Sprite & Pixel Art Generation

**Status:** `[ ]` Not Started
**Priority:** MEDIUM
**Plugin:** nethercore-zx-procgen
**Type:** Skill

---

## Problem

NOT covered. The procgen plugin focuses on 3D assets. 2D pixel art for UI, sprites, and tilemaps is completely missing.

## What's Missing

### Pixel Art Fundamentals
- Indexed palette generation (median cut, k-means)
- Ordered dithering (Bayer 2x2, 4x4, 8x8)
- Error diffusion dithering (Floyd-Steinberg, Atkinson)
- Outline generation (1px, selective, anti-aliased)

### UI Sprites
- 9-slice/9-patch panel generation
- Health bars (solid, segmented, gradient)
- Button states (normal, hover, pressed, disabled)
- Icon generation patterns

### Tilesets
- Autotile patterns (2-corner/16-tile, 4-corner/47-tile, blob/256)
- Terrain transitions
- Tile variations for visual interest
- Animated tiles (water, lava)

### Sprite Sheets
- Character sprite organization
- Directional sprites (4-way, 8-way)
- Animation frame layout
- Palette swaps for enemy variants

## Integration with Existing Skills

| Existing Skill | Gap 24 Addition |
|----------------|-----------------|
| procedural-textures | Uses noise but adds color reduction + dithering |
| Gap 4 (UI Patterns) | Gap 4 covers *code patterns*; Gap 24 covers *asset creation* |
| Gap 7 (Level Design) | Gap 7 covers *design patterns*; Gap 24 covers *tileset creation* |

## Code Examples

### Indexed Palette Generation

```rust
/// Generate an indexed color palette using median cut algorithm
pub fn generate_palette(colors: &[u32], max_colors: usize) -> Vec<u32> {
    let mut buckets = vec![colors.to_vec()];

    while buckets.len() < max_colors {
        let (idx, axis) = find_widest_bucket(&buckets);
        let bucket = buckets.remove(idx);
        let (low, high) = split_bucket(&bucket, axis);
        buckets.push(low);
        buckets.push(high);
    }

    buckets.iter().map(|b| average_color(b)).collect()
}
```

### Ordered Dithering (Bayer)

```rust
/// Apply ordered Bayer dithering to reduce colors
pub fn apply_ordered_dither(
    tex: &mut TextureBuffer,
    palette: &[u32],
    matrix_size: usize,
) {
    let bayer = match matrix_size {
        2 => BAYER_2X2,
        4 => BAYER_4X4,
        8 => BAYER_8X8,
        _ => BAYER_4X4,
    };

    for y in 0..tex.height {
        for x in 0..tex.width {
            let pixel = tex.get(x, y);
            let threshold = bayer[(y % matrix_size) * matrix_size + (x % matrix_size)];
            let adjusted = adjust_by_threshold(pixel, threshold);
            let nearest = find_nearest_palette_color(adjusted, palette);
            tex.set(x, y, nearest);
        }
    }
}

// Bayer 4x4 dither matrix (normalized 0-15)
const BAYER_4X4: [f32; 16] = [
     0.0/16.0,  8.0/16.0,  2.0/16.0, 10.0/16.0,
    12.0/16.0,  4.0/16.0, 14.0/16.0,  6.0/16.0,
     3.0/16.0, 11.0/16.0,  1.0/16.0,  9.0/16.0,
    15.0/16.0,  7.0/16.0, 13.0/16.0,  5.0/16.0,
];
```

### 9-Slice Panel Generation

```rust
/// Generate a 9-slice compatible UI panel texture
pub fn generate_9slice_panel(
    width: u32,
    height: u32,
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

    tex
}

/// 9-slice regions for runtime slicing
pub struct NineSlice {
    pub left: u32, pub right: u32, pub top: u32, pub bottom: u32,
}

impl NineSlice {
    pub fn panel(border: u32) -> Self {
        Self { left: border, right: border, top: border, bottom: border }
    }
}
```

### Autotile Generation (47-tile blob style)

```rust
/// Generate a 47-tile autotile set (4-corner blob style)
pub fn generate_autotile_set(
    tile_size: u32,
    terrain_color: u32,
    edge_color: u32,
    corner_style: CornerStyle,
) -> TextureBuffer {
    let atlas_width = tile_size * 8;  // 8 columns
    let atlas_height = tile_size * 6; // 6 rows = 48 slots

    let mut atlas = TextureBuffer::new(atlas_width, atlas_height);

    for tile_id in 0..47 {
        let neighbors = AUTOTILE_NEIGHBOR_MAP[tile_id];
        let tile = generate_single_autotile(
            tile_size, terrain_color, edge_color, neighbors, corner_style,
        );

        let col = tile_id % 8;
        let row = tile_id / 8;
        atlas.blit(&tile, col as u32 * tile_size, row as u32 * tile_size);
    }

    atlas
}

/// Neighbor flags for autotiling
pub struct Neighbors {
    pub n: bool, pub s: bool, pub e: bool, pub w: bool,
    pub ne: bool, pub nw: bool, pub se: bool, pub sw: bool,
}

pub enum CornerStyle { Square, Rounded, Beveled }
```

### Health Bar Generation

```rust
/// Generate a segmented health bar sprite
pub fn generate_health_bar(
    width: u32,
    height: u32,
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

## Prompt for Implementation

```
Add skill "procedural-sprites" to nethercore-zx-procgen. Triggers: "pixel art",
"sprite", "2D sprite", "9-slice", "9-patch", "nine slice", "tile set", "tileset",
"tilemap", "autotile", "wang tiles", "blob tiles", "health bar", "UI sprite",
"indexed palette", "color palette", "pixel dithering", "ordered dither",
"floyd-steinberg", "sprite sheet", "2D assets", "retro sprites", "button sprite",
"icon generation".

Cover:
- Pixel art fundamentals: indexed palettes (median cut, k-means), ordered dithering
  (Bayer 2x2/4x4/8x8), error diffusion (Floyd-Steinberg, Atkinson), outlines (1px,
  selective, anti-aliased)
- UI sprites: 9-slice/9-patch generation, health bars (solid, segmented, gradient),
  button states (normal/hover/pressed/disabled), icons
- Tilesets: autotile patterns (2-corner/16, 4-corner/47, blob/256), terrain
  transitions, tile variations, animated tiles
- Sprite sheets: organization, directional sprites (4-way, 8-way), animation frames,
  palette swaps

Integration: Uses procedural-textures noise algorithms as base, applies color reduction
and dithering. Reference Gap 4 for UI usage patterns, Gap 7 for level design patterns.
Include Rust and Python examples. Provide autotile neighbor mapping tables.

Output: PNG files compatible with ZX sprite rendering (draw_sprite, draw_sprite_region).
Note that 9-slice is NOT a ZX runtime feature - generate pre-scaled variants or
implement slicing in game code.

~2500 words.
```

## Dependencies

- None

## Related Gaps

- Gap 4 (UI Patterns) uses generated UI sprites
- Gap 7 (Level Design) uses generated tilesets
- Gap 11 (Custom Fonts) for pixel font generation
