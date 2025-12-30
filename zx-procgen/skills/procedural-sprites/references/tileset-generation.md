# Tileset Generation

Generate tilesets including autotiles, variations, and animated tiles.

## Autotile Generation (47-tile)

Generate tiles that automatically connect based on neighbors:

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

## Tile Variations

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

## Animated Tiles

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

## Autotile Systems Comparison

| System | Tiles | Bits | Use Case |
|--------|-------|------|----------|
| 2-corner (16) | 16 | 4 | Basic, minimal |
| 4-corner (47) | 47 | 8 | Standard RPG |
| Blob (256) | 256 | 8 | Smooth, complete |

## Data Tables (Keep Separate!)

**Important:** Store autotile neighbor maps in separate data modules:

```rust
// data/autotile_47.rs - DATA ONLY
pub const AUTOTILE_47_MAP: [Neighbors; 47] = [
    Neighbors { n: false, s: false, e: false, w: false, .. },
    // ... all 47 entries
];
```

See `references/autotile-patterns.md` for complete neighbor mapping tables.
