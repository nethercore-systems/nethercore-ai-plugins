# Retro Color Palettes for Pixel Art 3D

Era-authentic and stylized palettes for retro 3D texture generation.

## Classic 16-Color Palettes

### PICO-8 Style
Warm, saturated, highly readable.

```rust
fn pico8_palette() -> Vec<u32> {
    vec![
        0x000000FF, // 0  Black
        0x1D2B53FF, // 1  Dark Blue
        0x7E2553FF, // 2  Dark Purple
        0x008751FF, // 3  Dark Green
        0xAB5236FF, // 4  Brown
        0x5F574FFF, // 5  Dark Gray
        0xC2C3C7FF, // 6  Light Gray
        0xFFF1E8FF, // 7  White
        0xFF004DFF, // 8  Red
        0xFFA300FF, // 9  Orange
        0xFFEC27FF, // 10 Yellow
        0x00E436FF, // 11 Green
        0x29ADFFFF, // 12 Blue
        0x83769CFF, // 13 Lavender
        0xFF77A8FF, // 14 Pink
        0xFFCCAAFF, // 15 Peach
    ]
}
```

### CGA-Inspired
High contrast, limited but bold.

```rust
fn cga_palette() -> Vec<u32> {
    vec![
        0x000000FF, // Black
        0x0000AAFF, // Blue
        0x00AA00FF, // Green
        0x00AAAAFF, // Cyan
        0xAA0000FF, // Red
        0xAA00AAFF, // Magenta
        0xAA5500FF, // Brown
        0xAAAAAAFF, // Light Gray
        0x555555FF, // Dark Gray
        0x5555FFFF, // Light Blue
        0x55FF55FF, // Light Green
        0x55FFFFFF, // Light Cyan
        0xFF5555FF, // Light Red
        0xFF55FFFF, // Light Magenta
        0xFFFF55FF, // Yellow
        0xFFFFFFFF, // White
    ]
}
```

### Gameboy (4 Colors)
Monochrome green, extremely limited.

```rust
fn gameboy_palette() -> Vec<u32> {
    vec![
        0x0F380FFF, // Darkest green
        0x306230FF, // Dark green
        0x8BAC0FFF, // Light green
        0x9BBC0FFF, // Lightest green
    ]
}
```

---

## 32-Color Palettes

### PS1/Saturn Era
Extended range with industrial and natural tones.

```rust
fn ps1_palette() -> Vec<u32> {
    vec![
        // Neutrals
        0x000000FF, 0x1A1A1AFF, 0x333333FF, 0x4D4D4DFF,
        0x666666FF, 0x808080FF, 0xB3B3B3FF, 0xFFFFFFFF,
        // Warm
        0x800000FF, 0xCC0000FF, 0xFF4444FF, 0xFF8888FF,
        0x804000FF, 0xCC6600FF, 0xFFAA00FF, 0xFFDD88FF,
        // Cool
        0x000080FF, 0x0000CCFF, 0x4444FFFF, 0x8888FFFF,
        0x008080FF, 0x00CCCCFF, 0x44FFFFFF, 0x88FFFFFF,
        // Earth/Nature
        0x004000FF, 0x008000FF, 0x44CC44FF, 0x88FF88FF,
        0x402000FF, 0x804020FF, 0xCC8844FF, 0xFFCC88FF,
    ]
}
```

### N64 Era
Slightly more saturated, fog-friendly.

```rust
fn n64_palette() -> Vec<u32> {
    vec![
        // Base
        0x101020FF, 0x202040FF, 0x404060FF, 0x606080FF,
        0x8080A0FF, 0xA0A0C0FF, 0xC0C0E0FF, 0xE0E0FFFF,
        // Primary
        0xCC2222FF, 0xFF4444FF, 0x22CC22FF, 0x44FF44FF,
        0x2222CCFF, 0x4444FFFF, 0xCCCC22FF, 0xFFFF44FF,
        // Secondary
        0xCC22CCFF, 0xFF44FFFF, 0x22CCCCFF, 0x44FFFFFF,
        0xCC8822FF, 0xFFAA44FF, 0x88CC22FF, 0xAAFF44FF,
        // Accent
        0x886644FF, 0xAA8866FF, 0xCCAA88FF, 0xEECCAAFF,
        0x446688FF, 0x6688AAFF, 0x88AACCFF, 0xAACCEEFF,
    ]
}
```

---

## Material-Specific Palettes

### Skin Tones (8 colors)

```rust
fn skin_palette() -> Vec<u32> {
    vec![
        0x3C2415FF, // Very dark
        0x6B4423FF, // Dark brown
        0x8B6844FF, // Medium brown
        0xC68642FF, // Tan
        0xE0AC69FF, // Light tan
        0xF1C27DFF, // Fair
        0xFFDBACFF, // Light
        0xFFE4C4FF, // Very light
    ]
}
```

### Metal Tones (8 colors)

```rust
fn metal_palette() -> Vec<u32> {
    vec![
        0x404050FF, // Dark steel
        0x606070FF, // Steel
        0x808090FF, // Light steel
        0xA0A0B0FF, // Silver
        0xB8860BFF, // Dark gold
        0xDAA520FF, // Goldenrod
        0xFFD700FF, // Gold
        0xB87333FF, // Copper
    ]
}
```

### Stone/Rock (8 colors)

```rust
fn stone_palette() -> Vec<u32> {
    vec![
        0x2F2F2FFF, // Dark slate
        0x484848FF, // Charcoal
        0x696969FF, // Dim gray
        0x808080FF, // Gray
        0x989898FF, // Dark silver
        0xA9A9A9FF, // Light gray
        0xC0C0C0FF, // Silver
        0xD3D3D3FF, // Gainsboro
    ]
}
```

### Foliage (8 colors)

```rust
fn foliage_palette() -> Vec<u32> {
    vec![
        0x1A3300FF, // Deep forest
        0x2D5016FF, // Dark green
        0x3D6B1DFF, // Forest green
        0x4A8522FF, // Medium green
        0x5CA028FF, // Grass green
        0x7CC032FF, // Light green
        0xA0D84AFF, // Lime
        0xCCEE88FF, // Pale lime
    ]
}
```

---

## Palette Quantization

### Rust Implementation

```rust
fn color_distance_squared(c1: u32, c2: u32) -> u32 {
    let r1 = ((c1 >> 24) & 0xFF) as i32;
    let g1 = ((c1 >> 16) & 0xFF) as i32;
    let b1 = ((c1 >> 8) & 0xFF) as i32;

    let r2 = ((c2 >> 24) & 0xFF) as i32;
    let g2 = ((c2 >> 16) & 0xFF) as i32;
    let b2 = ((c2 >> 8) & 0xFF) as i32;

    let dr = r1 - r2;
    let dg = g1 - g2;
    let db = b1 - b2;

    // Weighted for human perception
    ((2 * dr * dr) + (4 * dg * dg) + (3 * db * db)) as u32
}

fn quantize_to_palette(color: u32, palette: &[u32]) -> u32 {
    palette.iter()
        .min_by_key(|&&p| color_distance_squared(color, p))
        .copied()
        .unwrap_or(color)
}

fn quantize_texture(tex: &mut TextureBuffer, palette: &[u32]) {
    for y in 0..tex.height {
        for x in 0..tex.width {
            let original = tex.get(x, y);
            let quantized = quantize_to_palette(original, palette);
            tex.set(x, y, quantized);
        }
    }
}
```

### Python Implementation

```python
import numpy as np

def quantize_to_palette(img, palette):
    """Quantize image to nearest palette colors."""
    # palette: list of (R, G, B) tuples
    palette_arr = np.array(palette, dtype=np.float32)
    result = np.zeros_like(img[:, :, :3])

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            pixel = img[y, x, :3].astype(np.float32)
            # Weighted distance (perceptual)
            weights = np.array([2, 4, 3])
            distances = np.sum(weights * (palette_arr - pixel) ** 2, axis=1)
            nearest = np.argmin(distances)
            result[y, x] = palette[nearest]

    return result.astype(np.uint8)
```

---

## Dithering for Extended Range

When 16 colors aren't enough, use ordered dithering:

```rust
const BAYER_4X4: [[f32; 4]; 4] = [
    [0.0/16.0,  8.0/16.0,  2.0/16.0, 10.0/16.0],
    [12.0/16.0, 4.0/16.0, 14.0/16.0,  6.0/16.0],
    [3.0/16.0, 11.0/16.0,  1.0/16.0,  9.0/16.0],
    [15.0/16.0, 7.0/16.0, 13.0/16.0,  5.0/16.0],
];

fn dither_quantize(tex: &mut TextureBuffer, palette: &[u32]) {
    for y in 0..tex.height {
        for x in 0..tex.width {
            let threshold = BAYER_4X4[(y % 4) as usize][(x % 4) as usize];
            let color = tex.get(x, y);

            // Add dither offset before quantizing
            let r = (((color >> 24) & 0xFF) as f32 + (threshold - 0.5) * 32.0).clamp(0.0, 255.0) as u32;
            let g = (((color >> 16) & 0xFF) as f32 + (threshold - 0.5) * 32.0).clamp(0.0, 255.0) as u32;
            let b = (((color >> 8) & 0xFF) as f32 + (threshold - 0.5) * 32.0).clamp(0.0, 255.0) as u32;

            let dithered = (r << 24) | (g << 16) | (b << 8) | 0xFF;
            let quantized = quantize_to_palette(dithered, palette);
            tex.set(x, y, quantized);
        }
    }
}
```

---

## Palette Selection Guide

| Asset Type | Recommended Palette Size | Notes |
|------------|-------------------------|-------|
| Character skin | 4-8 colors | Subtle gradients |
| Character clothes | 4-8 colors | Per material |
| Props | 8-16 colors | Mixed materials |
| Environment tiles | 8-16 colors | Consistent set |
| UI elements | 4-8 colors | High contrast |
| Effects/particles | 4-8 colors | Bright, saturated |

**Tip:** Use a unified palette across related assets for visual cohesion. A 32-color master palette works well for entire game.
