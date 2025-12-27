---
name: Custom Fonts
description: This skill should be used when the user asks about "custom font", "bitmap font", "load_font", "load_font_ex", "font_bind", "game font", "pixel font", "text rendering", "font atlas", "variable width font", "rom_font", "font texture", "glyph", "character mapping", "first_codepoint", or mentions implementing custom text rendering, creating bitmap fonts, or loading font atlases for Nethercore ZX games.
version: 1.0.0
---

# Custom Fonts for Nethercore ZX

Load and render custom bitmap fonts. ZX provides a built-in 8x8 monospace font but supports custom fixed-width and variable-width bitmap fonts.

## Font FFI Functions

Reference `nethercore/include/zx.rs` lines 751-784 for complete signatures:

| Function | Purpose |
|----------|---------|
| `load_font(texture, width, height, first_codepoint, count)` | Load fixed-width bitmap font |
| `load_font_ex(texture, widths_ptr, height, first_codepoint, count)` | Load variable-width font |
| `font_bind(handle)` | Bind font for draw_text() |
| `rom_font(id_ptr, id_len)` | Load font atlas from ROM |

## Font Atlas Format

Font textures contain glyphs arranged in a grid, row-major order:

```
+---+---+---+---+---+---+---+---+   ← Row 0: glyphs 0-7
| ! | " | # | $ | % | & | ' | ( |
+---+---+---+---+---+---+---+---+
| ) | * | + | , | - | . | / | 0 |   ← Row 1: glyphs 8-15
+---+---+---+---+---+---+---+---+
| 1 | 2 | 3 | 4 | ...             ← Continues...
```

For ASCII printable characters (space through ~), use:
- `first_codepoint = 32` (space character)
- `char_count = 95` (32 to 126 inclusive)

## Fixed-Width Font

All glyphs share the same dimensions:

```rust
static mut GAME_FONT: u32 = 0;

fn init() {
    unsafe {
        // Load font texture (16x6 grid of 8x12 glyphs = 128x72 pixels)
        let font_texture = rom_texture_str("pixel_font");

        // Create font: 8px wide, 12px tall glyphs
        // Starting at ASCII 32 (space), 96 characters total
        GAME_FONT = load_font(
            font_texture,
            8,   // char_width
            12,  // char_height
            32,  // first_codepoint (space)
            96   // char_count (space through DEL)
        );
    }
}

fn render() {
    unsafe {
        font_bind(GAME_FONT);
        draw_text_str("SCORE: 1000", 10.0, 10.0, 24.0, 0xFFFFFFFF);

        // Return to built-in font
        font_bind(0);
    }
}
```

## Variable-Width Font

Each glyph has individual width for proportional text:

```rust
static mut PROP_FONT: u32 = 0;

// Width of each glyph in pixels (index 0 = first_codepoint)
static GLYPH_WIDTHS: [u8; 96] = [
    4,  // space
    3,  // !
    5,  // "
    7,  // #
    6,  // $
    8,  // %
    7,  // &
    3,  // '
    4,  // (
    4,  // )
    5,  // *
    6,  // +
    3,  // ,
    5,  // -
    3,  // .
    5,  // /
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6,  // 0-9
    3,  // :
    3,  // ;
    5,  // <
    6,  // =
    5,  // >
    6,  // ?
    8,  // @
    7, 6, 6, 6, 5, 5, 6, 6, 3, 5,  // A-J
    6, 5, 8, 7, 7, 6, 7, 6, 6, 6,  // K-T
    6, 7, 9, 7, 6, 6,              // U-Z
    4, 5, 4, 6, 6, 3,              // [ \ ] ^ _ `
    6, 6, 5, 6, 6, 4, 6, 6, 3, 4,  // a-j
    5, 3, 8, 6, 6, 6, 6, 4, 5, 4,  // k-t
    6, 6, 8, 6, 6, 5,              // u-z
    4, 3, 4, 7,                     // { | } ~
];

fn init() {
    unsafe {
        let font_texture = rom_texture_str("proportional_font");

        // Variable-width: pass widths array
        PROP_FONT = load_font_ex(
            font_texture,
            GLYPH_WIDTHS.as_ptr(),
            16,  // char_height (same for all)
            32,  // first_codepoint
            96   // char_count
        );
    }
}
```

## Loading from ROM

Bundle font atlas in ROM data pack:

```toml
# nether.toml
[[assets.textures]]
id = "game_font"
path = "assets/fonts/pixel_font.png"
```

```rust
fn init() {
    unsafe {
        let font_tex = rom_texture_str("game_font");
        GAME_FONT = load_font(font_tex, 8, 8, 32, 96);
    }
}
```

## Built-in Font

Pass 0 to `font_bind()` for the default 8x8 monospace font:

```rust
font_bind(0);  // Use built-in font
draw_text_str("Default Font", 10.0, 10.0, 16.0, 0xFFFFFFFF);
```

## Font Scaling

The `size` parameter in `draw_text()` scales the font:

```rust
// Same font, different sizes
font_bind(GAME_FONT);
draw_text_str("Small", 10.0, 10.0, 12.0, 0xFFFFFFFF);
draw_text_str("Medium", 10.0, 30.0, 24.0, 0xFFFFFFFF);
draw_text_str("Large", 10.0, 60.0, 48.0, 0xFFFFFFFF);
```

Scale is relative to glyph height. Size 16 with 8px tall glyphs = 2x scale.

## Measuring Text

Use `text_width()` for alignment:

```rust
fn draw_centered_text(text: &str, y: f32, size: f32, color: u32) {
    unsafe {
        let width = text_width(text.as_ptr(), text.len() as u32, size);
        let x = (960.0 - width) / 2.0;  // Center on 960px screen
        draw_text(text.as_ptr(), text.len() as u32, x, y, size, color);
    }
}
```

## Creating Font Atlases

### Tools

| Tool | Type | Platform |
|------|------|----------|
| **BMFont** | Fixed/Variable | Windows |
| **Hiero** | Variable | Cross-platform (Java) |
| **FontForge** | Any | Cross-platform |
| **Hand-drawn** | Pixel art | Image editor |

### Manual Creation (Pixel Art)

1. Create image with glyph grid
2. Consistent cell size (e.g., 8x8, 8x12, 16x16)
3. Row-major layout starting at first_codepoint
4. Transparent background or solid color

Example 8x8 ASCII font texture: 128x48 pixels (16 cols x 6 rows)

### Recommended Dimensions

| Style | Glyph Size | Atlas Size | Characters |
|-------|------------|------------|------------|
| Tiny | 4x6 | 64x36 | 96 |
| Small | 8x8 | 128x48 | 96 |
| Medium | 8x12 | 128x72 | 96 |
| Large | 16x16 | 256x96 | 96 |

## Unicode Support

`first_codepoint` supports any Unicode starting point:

```rust
// Japanese Hiragana (starts at U+3041)
let hiragana_font = load_font(
    hiragana_texture,
    16,      // char_width
    16,      // char_height
    0x3041,  // first_codepoint (ぁ)
    83       // char_count (hiragana block)
);
```

Multiple fonts can cover different Unicode ranges.

## Rollback Safety

Font handles are created in `init()` and never change. Font state is render-only - no rollback concerns.

## Additional Resources

- **`examples/font-examples.md`** - Complete font setup examples
- **`references/font-creation.md`** - Detailed atlas creation guide
- **`nethercore/include/zx.rs`** lines 751-784 - Font FFI signatures
- **Gap 24 (2D Sprites)** - Procedural pixel font generation
- **BMFont** - http://www.angelcode.com/products/bmfont/
