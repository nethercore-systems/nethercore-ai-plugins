# Sprite Sheet Organization

Organize sprites into sheets for characters, animations, and palette swaps.

## Character Sprite Layout

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

## Palette Swaps

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
```

## Example: Enemy Variants

```rust
let base_slime = load_sprite("slime_green.png");
let green_palette = [0x22AA22FF, 0x118811FF, 0x005500FF];
let red_palette = [0xAA2222FF, 0x881111FF, 0x550000FF];
let blue_palette = [0x2222AAFF, 0x111188FF, 0x000055FF];

let red_slime = generate_palette_swap(&base_slime, &green_palette, &red_palette);
let blue_slime = generate_palette_swap(&base_slime, &green_palette, &blue_palette);
```

## Common Sheet Layouts

| Type | Layout | Typical Size |
|------|--------|--------------|
| 4-dir character | 4 cols x 4 rows | 128x128 (32x32 sprites) |
| 8-dir character | 4 cols x 8 rows | 128x256 (32x32 sprites) |
| Attack anim | 6-8 cols x 1 row | 192x32 |
| Death anim | 4-6 cols x 1 row | 128x32 |
| Effect/particle | 4-8 cols x 1 row | Variable |

## Animation Frame Order

Standard RPG Maker convention:

| Row | Direction |
|-----|-----------|
| 0 | Down |
| 1 | Left |
| 2 | Right |
| 3 | Up |

| Column | Frame |
|--------|-------|
| 0 | Idle / Stand |
| 1 | Walk 1 |
| 2 | Walk 2 |
| 3 | Walk 3 |

## ZX Usage

```rust
fn draw_character(x: f32, y: f32, direction: u32, frame: u32) {
    draw_sprite_region(
        CHARACTER_SHEET,
        x, y,
        frame * SPRITE_WIDTH,
        direction * SPRITE_HEIGHT,
        SPRITE_WIDTH, SPRITE_HEIGHT,
    );
}
```
