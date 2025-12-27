# Custom Font Examples

Complete working implementations of custom font systems for Nethercore ZX.

## Retro Pixel Font

Simple fixed-width pixel font setup:

```rust
#![no_std]
#![no_main]

mod ffi;
use ffi::*;

static mut PIXEL_FONT: u32 = 0;

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        render_mode(2);
        set_clear_color(0x1a1a2eFF);

        // Load 8x8 pixel font texture from ROM
        // Atlas: 128x48 pixels (16 columns x 6 rows of 8x8 glyphs)
        let font_tex = rom_texture_str("pixel_font");

        PIXEL_FONT = load_font(
            font_tex,
            8,   // Each glyph is 8 pixels wide
            8,   // Each glyph is 8 pixels tall
            32,  // First character is space (ASCII 32)
            96   // 96 printable ASCII characters
        );
    }
}

#[no_mangle]
pub extern "C" fn update() {}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        font_bind(PIXEL_FONT);

        // Different sizes (scale from base 8x8)
        draw_text_str("1X SCALE", 10.0, 10.0, 8.0, 0xFFFFFFFF);
        draw_text_str("2X SCALE", 10.0, 30.0, 16.0, 0xFFFFFFFF);
        draw_text_str("3X SCALE", 10.0, 60.0, 24.0, 0xFFFFFFFF);
        draw_text_str("4X SCALE", 10.0, 100.0, 32.0, 0xFFFFFFFF);

        // Colored text
        draw_text_str("RED", 10.0, 150.0, 16.0, 0xFF0000FF);
        draw_text_str("GREEN", 60.0, 150.0, 16.0, 0x00FF00FF);
        draw_text_str("BLUE", 130.0, 150.0, 16.0, 0x0000FFFF);

        // Return to built-in font
        font_bind(0);
        draw_text_str("Built-in 8x8 font", 10.0, 200.0, 16.0, 0x888888FF);
    }
}
```

## Game HUD with Multiple Fonts

Different fonts for different purposes:

```rust
#![no_std]
#![no_main]

mod ffi;
use ffi::*;

static mut TITLE_FONT: u32 = 0;    // Large decorative
static mut HUD_FONT: u32 = 0;      // Clean, readable
static mut SMALL_FONT: u32 = 0;    // Tiny for numbers

static mut SCORE: u32 = 0;
static mut HIGH_SCORE: u32 = 9999;

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        render_mode(2);
        set_clear_color(0x000000FF);

        // Load different font textures
        let title_tex = rom_texture_str("title_font");     // 16x16 decorative
        let hud_tex = rom_texture_str("hud_font");         // 8x10 clean
        let small_tex = rom_texture_str("numbers_font");   // 4x6 tiny

        TITLE_FONT = load_font(title_tex, 16, 16, 32, 96);
        HUD_FONT = load_font(hud_tex, 8, 10, 32, 96);
        SMALL_FONT = load_font(small_tex, 4, 6, 48, 10);  // Just 0-9 (ASCII 48-57)
    }
}

#[no_mangle]
pub extern "C" fn update() {
    unsafe {
        SCORE += 10;  // Demo increment
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        // Game title (large, decorative)
        font_bind(TITLE_FONT);
        draw_centered("SPACE BLASTER", 30.0, 32.0, 0xFFD700FF);

        // HUD elements (clean, readable)
        font_bind(HUD_FONT);
        draw_text_str("SCORE", 10.0, 500.0, 16.0, 0xFFFFFFFF);
        draw_text_str("HIGH", 800.0, 500.0, 16.0, 0xFFFFFFFF);

        // Score numbers (small font, numbers only)
        font_bind(SMALL_FONT);
        draw_number(SCORE, 10.0, 520.0, 12.0, 0x00FF00FF);
        draw_number(HIGH_SCORE, 800.0, 520.0, 12.0, 0xFFFF00FF);

        font_bind(0);
    }
}

fn draw_centered(text: &str, y: f32, size: f32, color: u32) {
    unsafe {
        let width = text_width(text.as_ptr(), text.len() as u32, size);
        let x = (960.0 - width) / 2.0;
        draw_text(text.as_ptr(), text.len() as u32, x, y, size, color);
    }
}

// Helper for numeric rendering with small_font
fn draw_number(mut n: u32, x: f32, y: f32, size: f32, color: u32) {
    unsafe {
        // Convert number to string in buffer
        let mut buf: [u8; 10] = [0; 10];
        let mut i = 9;

        if n == 0 {
            buf[i] = b'0';
            i -= 1;
        } else {
            while n > 0 {
                buf[i] = b'0' + (n % 10) as u8;
                n /= 10;
                i -= 1;
            }
        }

        let start = i + 1;
        let len = 10 - start;
        draw_text(buf[start..].as_ptr(), len as u32, x, y, size, color);
    }
}
```

## Variable-Width Font for Dialogue

Proportional text for natural reading:

```rust
#![no_std]
#![no_main]

mod ffi;
use ffi::*;

static mut DIALOGUE_FONT: u32 = 0;

// Width of each character (space through ~)
static CHAR_WIDTHS: [u8; 96] = [
    4,  // space
    2,  // !
    4,  // "
    6,  // #
    5,  // $
    7,  // %
    6,  // &
    2,  // '
    3,  // (
    3,  // )
    4,  // *
    5,  // +
    2,  // ,
    4,  // -
    2,  // .
    4,  // /
    5, 4, 5, 5, 5, 5, 5, 5, 5, 5,  // 0-9
    2,  // :
    2,  // ;
    4,  // <
    5,  // =
    4,  // >
    5,  // ?
    7,  // @
    6, 5, 5, 5, 5, 4, 5, 5, 2, 4,  // A-J
    5, 4, 7, 5, 5, 5, 5, 5, 5, 5,  // K-T
    5, 6, 7, 5, 5, 5,              // U-Z
    3, 4, 3, 5, 5, 2,              // [ \ ] ^ _ `
    5, 5, 4, 5, 5, 3, 5, 5, 2, 2,  // a-j
    4, 2, 6, 5, 5, 5, 5, 3, 4, 3,  // k-t
    5, 5, 7, 5, 5, 4,              // u-z
    3, 2, 3, 6,                     // { | } ~
];

static mut DIALOGUE_TEXT: &str = "The ancient artifact glows with mysterious power...";
static mut CHAR_INDEX: usize = 0;
static mut CHAR_TIMER: f32 = 0.0;

const CHAR_DELAY: f32 = 0.05;  // Time between characters

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        render_mode(2);
        set_clear_color(0x000000FF);

        let font_tex = rom_texture_str("dialogue_font");  // Variable-width glyphs

        DIALOGUE_FONT = load_font_ex(
            font_tex,
            CHAR_WIDTHS.as_ptr(),
            12,  // All glyphs 12px tall
            32,
            96
        );
    }
}

#[no_mangle]
pub extern "C" fn update() {
    unsafe {
        let dt = delta_time();

        // Typewriter effect
        CHAR_TIMER += dt;
        if CHAR_TIMER >= CHAR_DELAY {
            CHAR_TIMER = 0.0;
            if CHAR_INDEX < DIALOGUE_TEXT.len() {
                CHAR_INDEX += 1;
            }
        }

        // Skip with A button
        if button_pressed(0, button::A) != 0 {
            CHAR_INDEX = DIALOGUE_TEXT.len();
        }
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        // Dialogue box background
        draw_rect(40.0, 400.0, 880.0, 120.0, 0x222244FF);
        draw_rect(44.0, 404.0, 872.0, 112.0, 0x111122FF);

        // Dialogue text (typewriter reveal)
        font_bind(DIALOGUE_FONT);

        let visible_text = &DIALOGUE_TEXT[..CHAR_INDEX];
        draw_text(
            visible_text.as_ptr(),
            visible_text.len() as u32,
            60.0, 420.0,
            24.0,
            0xFFFFFFFF
        );

        // "Press A" indicator when complete
        if CHAR_INDEX >= DIALOGUE_TEXT.len() {
            font_bind(0);
            draw_text_str("Press A", 800.0, 490.0, 12.0, 0x888888FF);
        }
    }
}
```

## Multi-Language Support

Using different fonts for different character sets:

```rust
static mut ASCII_FONT: u32 = 0;
static mut CYRILLIC_FONT: u32 = 0;
static mut JAPANESE_FONT: u32 = 0;

fn init() {
    unsafe {
        // ASCII (Latin alphabet)
        let ascii_tex = rom_texture_str("latin_font");
        ASCII_FONT = load_font(ascii_tex, 8, 12, 32, 96);

        // Cyrillic (Russian alphabet) - starts at U+0410
        let cyrillic_tex = rom_texture_str("cyrillic_font");
        CYRILLIC_FONT = load_font(cyrillic_tex, 8, 12, 0x0410, 64);

        // Japanese Hiragana - starts at U+3040
        let japanese_tex = rom_texture_str("hiragana_font");
        JAPANESE_FONT = load_font(japanese_tex, 12, 12, 0x3040, 96);
    }
}

fn render_localized(text: &str, lang: u32, x: f32, y: f32) {
    unsafe {
        match lang {
            0 => font_bind(ASCII_FONT),
            1 => font_bind(CYRILLIC_FONT),
            2 => font_bind(JAPANESE_FONT),
            _ => font_bind(0),
        }
        draw_text(text.as_ptr(), text.len() as u32, x, y, 24.0, 0xFFFFFFFF);
    }
}
```

## Text Effects

### Wavy Text

```rust
fn draw_wavy_text(text: &str, base_x: f32, base_y: f32, size: f32, color: u32) {
    unsafe {
        font_bind(GAME_FONT);

        let mut x = base_x;
        let time = elapsed_time();

        for (i, c) in text.chars().enumerate() {
            // Calculate wave offset for this character
            let wave = (time * 5.0 + i as f32 * 0.5).sin() * 4.0;
            let y = base_y + wave;

            // Draw single character
            let char_str = [c as u8];
            draw_text(char_str.as_ptr(), 1, x, y, size, color);

            // Advance x (estimate fixed width, or use text_width for variable)
            x += size * 0.6;  // Approximate character width
        }
    }
}
```

### Rainbow Text

```rust
fn draw_rainbow_text(text: &str, x: f32, y: f32, size: f32) {
    unsafe {
        font_bind(GAME_FONT);

        let mut current_x = x;
        let time = elapsed_time();

        for (i, c) in text.chars().enumerate() {
            // Cycle through rainbow colors
            let hue = ((time + i as f32 * 0.1) % 1.0) * 6.0;
            let color = hue_to_rgb(hue);

            let char_str = [c as u8];
            draw_text(char_str.as_ptr(), 1, current_x, y, size, color);

            current_x += size * 0.6;
        }
    }
}

fn hue_to_rgb(h: f32) -> u32 {
    let (r, g, b) = match h as u32 {
        0 => (255, (h.fract() * 255.0) as u8, 0),
        1 => ((255.0 - h.fract() * 255.0) as u8, 255, 0),
        2 => (0, 255, (h.fract() * 255.0) as u8),
        3 => (0, (255.0 - h.fract() * 255.0) as u8, 255),
        4 => ((h.fract() * 255.0) as u8, 0, 255),
        _ => (255, 0, (255.0 - h.fract() * 255.0) as u8),
    };
    rgba(r, g, b, 255)
}
```

### Outline Text

```rust
fn draw_outlined_text(text: &str, x: f32, y: f32, size: f32, color: u32, outline: u32) {
    unsafe {
        // Draw outline in 8 directions
        let offsets = [(1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0),
                       (1.0, 1.0), (-1.0, -1.0), (1.0, -1.0), (-1.0, 1.0)];

        for (ox, oy) in offsets {
            draw_text(text.as_ptr(), text.len() as u32, x + ox, y + oy, size, outline);
        }

        // Draw main text on top
        draw_text(text.as_ptr(), text.len() as u32, x, y, size, color);
    }
}
```
