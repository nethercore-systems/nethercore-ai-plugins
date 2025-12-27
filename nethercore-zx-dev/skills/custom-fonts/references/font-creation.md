# Font Atlas Creation Guide

Detailed instructions for creating bitmap font atlases compatible with Nethercore ZX.

## Atlas Layout Requirements

### Grid Structure

Glyphs must be arranged in a rectangular grid, row-major order:

```
Col:  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
R0  |SPC| ! | " | # | $ | % | & | ' | ( | ) | * | + | , | - | . | / |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
R1  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | : | ; | < | = | > | ? |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
R2  | @ | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
R3  | P | Q | R | S | T | U | V | W | X | Y | Z | [ | \ | ] | ^ | _ |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
R4  | ` | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
R5  | p | q | r | s | t | u | v | w | x | y | z | { | | | } | ~ |DEL|
    +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### ASCII Mapping

Standard printable ASCII (most common):
- `first_codepoint = 32` (space)
- `char_count = 95` (space through ~)
- Grid: 16 columns x 6 rows = 96 cells

### Calculating Atlas Size

```
atlas_width  = char_width × columns
atlas_height = char_height × rows

Example 8×8 font, 96 characters:
  96 chars ÷ 16 cols = 6 rows
  atlas = 128×48 pixels
```

## Creating with Image Editors

### Pixel Art (Aseprite, GIMP, Photoshop)

1. **Create canvas**: width × height matching atlas dimensions
2. **Set up grid**: View → Grid (cell size = glyph dimensions)
3. **Draw glyphs**: One per cell, snap to grid
4. **Export**: PNG with transparency (or solid background color)

### Tips

- **Transparency**: Transparent background recommended
- **Anti-aliasing**: Avoid for pixel fonts (pure black/white)
- **Baseline**: Keep consistent across all glyphs
- **Padding**: Glyphs should not touch cell edges

## Variable-Width Fonts

For proportional fonts, each glyph can have different width:

### Measuring Widths

1. Create font with uniform cell width (for texture layout)
2. Measure actual pixel width of each glyph
3. Create widths array in code

```rust
// Cell size in texture is 8x12, but actual widths vary
static WIDTHS: [u8; 96] = [
    4,  // space (narrow)
    2,  // ! (very narrow)
    // ... measure each glyph
    6,  // M (wide)
    2,  // l (very narrow)
    // ...
];
```

### Texture Layout Options

**Option A: Uniform cells (easier)**
- All cells same size in texture
- Widths only affect text layout, not texture sampling
- ZX uses width for kerning, samples full cell

**Option B: Packed (smaller texture)**
- Variable cell widths in texture
- Requires custom texture generation tool
- Not directly supported by `load_font_ex`

## Using BMFont

BMFont generates bitmap fonts from TrueType/OpenType fonts.

### Export Settings

1. Open BMFont, load a font
2. Settings:
   - **Texture size**: Power of 2 (128, 256, 512)
   - **Bit depth**: 32 (for alpha)
   - **Channels**: RGBA
   - **Font descriptor**: Text or XML
3. Export

### Converting BMFont Output

BMFont exports:
- `.png` texture atlas
- `.fnt` descriptor file

For ZX, you need to:
1. Use the PNG directly as texture
2. Parse `.fnt` to extract widths array for variable-width

```
# Example .fnt parsing
char id=32   x=0   y=0   width=4   ...  # space
char id=33   x=4   y=0   width=2   ...  # !
```

Build widths array from the `width` values.

## Using Hiero (Java)

LibGDX's Hiero tool works cross-platform.

1. Select font and size
2. Choose characters (ASCII is default)
3. Effects: None for pixel art, padding as needed
4. Export as PNG + .fnt

Same conversion process as BMFont.

## Hand-Drawing Pixel Fonts

### Planning

1. Decide glyph size (8×8, 8×12, etc.)
2. Sketch alphabet on paper
3. Plan for consistency:
   - Cap height (top of capitals)
   - X-height (top of lowercase)
   - Baseline
   - Descender line (bottom of g, p, y)

### Drawing Order

1. Draw guide lines in separate layer
2. Start with simple shapes: O, I, L
3. Build complex from simple: B = I + bumps
4. Numbers after letters (similar strokes)
5. Punctuation last

### Common Issues

| Issue | Solution |
|-------|----------|
| Inconsistent height | Use guide lines |
| Kerning looks wrong | Adjust widths array |
| Characters blur at scale | Avoid anti-aliasing |
| Hard to read | Increase contrast, simplify shapes |

## Power-of-Two Textures

GPU efficiency prefers power-of-two dimensions:

| Glyph | Count | Grid | Atlas |
|-------|-------|------|-------|
| 8×8 | 96 | 16×6 | 128×48 → pad to 128×64 |
| 8×12 | 96 | 16×6 | 128×72 → pad to 128×128 |
| 16×16 | 96 | 8×12 | 128×192 → pad to 128×256 |

Padding is just empty space - glyphs don't need to fill entire texture.

## Testing Your Font

```rust
fn init() {
    let tex = rom_texture_str("test_font");
    let font = load_font(tex, GLYPH_W, GLYPH_H, 32, 96);
    // ...
}

fn render() {
    // Test all characters
    font_bind(font);
    draw_text_str(" !\"#$%&'()*+,-./", 10.0, 10.0, 16.0, 0xFFFFFFFF);
    draw_text_str("0123456789:;<=>?", 10.0, 30.0, 16.0, 0xFFFFFFFF);
    draw_text_str("@ABCDEFGHIJKLMNO", 10.0, 50.0, 16.0, 0xFFFFFFFF);
    draw_text_str("PQRSTUVWXYZ[\\]^_", 10.0, 70.0, 16.0, 0xFFFFFFFF);
    draw_text_str("`abcdefghijklmno", 10.0, 90.0, 16.0, 0xFFFFFFFF);
    draw_text_str("pqrstuvwxyz{|}~", 10.0, 110.0, 16.0, 0xFFFFFFFF);
}
```

Verify:
- All characters render correctly
- Spacing looks natural
- No texture bleeding between glyphs
- Scaling doesn't cause artifacts

## Recommended Tools

| Tool | Best For | Platform |
|------|----------|----------|
| Aseprite | Pixel art fonts | All |
| BMFont | Converting TTF | Windows |
| Hiero | Converting TTF | All (Java) |
| FontForge | Advanced editing | All |
| GIMP | Free bitmap editing | All |

## File Formats

ZX accepts standard image formats for textures:
- PNG (recommended - supports transparency)
- BMP
- TGA

Export as PNG 32-bit RGBA for best results.
