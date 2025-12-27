# Gap 11: Custom Fonts

**Status:** `[x]` Completed
**Priority:** LOW
**Plugin:** nethercore-zx-dev
**Type:** Skill

---

## Problem

FFI exists for font loading, only default font documented. Games often need custom bitmap fonts for style, but font creation isn't covered.

## FFI Functions (from zx.rs)

### Fixed-Width Bitmap Font
```rust
/// Load a fixed-width bitmap font.
/// - texture: Texture atlas handle (from load_texture or rom_texture)
/// - char_width, char_height: Glyph dimensions in pixels
/// - first_codepoint: Unicode codepoint of first glyph (e.g., 32 for ASCII space)
/// - char_count: Number of glyphs in the atlas
/// Returns: Font handle for use with font_bind()
pub fn load_font(texture: u32, char_width: u32, char_height: u32, first_codepoint: u32, char_count: u32) -> u32;
```

### Variable-Width Bitmap Font
```rust
/// Load a variable-width bitmap font.
/// - texture: Texture atlas handle
/// - widths_ptr: Pointer to array of char_count u8 widths (one per glyph)
/// - char_height: Glyph height in pixels (width varies per glyph)
/// - first_codepoint: Unicode codepoint of first glyph
/// - char_count: Number of glyphs in the atlas
/// Returns: Font handle for use with font_bind()
pub fn load_font_ex(texture: u32, widths_ptr: *const u8, char_height: u32, first_codepoint: u32, char_count: u32) -> u32;
```

### Font Binding & ROM Loading
```rust
/// Bind a font for subsequent draw_text() calls.
/// Pass 0 for the built-in 8x8 monospace font.
pub fn font_bind(font_handle: u32);

/// Load a font atlas from ROM data pack by ID.
pub fn rom_font(id_ptr: u32, id_len: u32) -> u32;
```

## What's Missing

- Bitmap font creation workflow (grid layout, character mapping)
- Font texture format requirements (glyphs arranged in rows)
- Variable-width font setup (widths array)
- Font atlas packing tools and techniques
- Integration with procgen for procedural fonts

## Prompt for Implementation

```
Add skill "custom-fonts" to nethercore-zx-dev. Triggers: "custom font", "bitmap
font", "load_font", "font_bind", "game font", "pixel font". Cover: font texture
format (glyphs in grid, row-major order), load_font for fixed-width fonts,
load_font_ex for variable-width fonts with widths array, first_codepoint mapping
(e.g., 32 for ASCII printable chars), rom_font for bundled fonts, font_bind(0)
for built-in 8x8 font. Creation tools (Hiero, BMFont, hand-drawn). Tie to
procedural-textures for font atlas creation. ~800 words.
```

## Dependencies

- None

## Related Gaps

- Gap 24 (2D Sprites) for pixel font generation techniques
