# Color Palettes Reference

Classic game palettes and color quantization algorithms for pixel art generation.

## Classic Game Palettes

### PICO-8 (16 colors)

The popular fantasy console palette, excellent for retro games:

```rust
const PICO8_PALETTE: [u32; 16] = [
    0x000000FF,  // 0: Black
    0x1D2B53FF,  // 1: Dark Blue
    0x7E2553FF,  // 2: Dark Purple
    0x008751FF,  // 3: Dark Green
    0xAB5236FF,  // 4: Brown
    0x5F574FFF,  // 5: Dark Gray
    0xC2C3C7FF,  // 6: Light Gray
    0xFFF1E8FF,  // 7: White
    0xFF004DFF,  // 8: Red
    0xFFA300FF,  // 9: Orange
    0xFFEC27FF,  // 10: Yellow
    0x00E436FF,  // 11: Green
    0x29ADFFFF,  // 12: Blue
    0x83769CFF,  // 13: Lavender
    0xFF77A8FF,  // 14: Pink
    0xFFCCAAFF,  // 15: Peach
];
```

### NES (54 colors)

The Nintendo Entertainment System's PPU palette:

```rust
const NES_PALETTE: [u32; 54] = [
    // Grays
    0x666666FF, 0x002A88FF, 0x1412A7FF, 0x3B00A4FF,
    0x5C007EFF, 0x6E0040FF, 0x6C0600FF, 0x561D00FF,
    0x333500FF, 0x0B4800FF, 0x005200FF, 0x004F08FF,
    0x00404DFF, 0x000000FF, 0x000000FF, 0x000000FF,
    // Mid-tones
    0xADADADFF, 0x155FD9FF, 0x4240FFFF, 0x7527FEFF,
    0xA01ACCFF, 0xB71E7BFF, 0xB53120FF, 0x994E00FF,
    0x6B6D00FF, 0x388700FF, 0x0C9300FF, 0x008F32FF,
    0x007C8DFF, 0x000000FF, 0x000000FF, 0x000000FF,
    // Highlights
    0xFFFEFFFF, 0x64B0FFFF, 0x9290FFFF, 0xC676FFFF,
    0xF36AFFFF, 0xFE6ECCFF, 0xFE8170FF, 0xEA9E22FF,
    0xBCBE00FF, 0x88D800FF, 0x5CE430FF, 0x45E082FF,
    0x48CDDEFF, 0x4F4F4FFF, 0x000000FF, 0x000000FF,
    // Pastels
    0xFFFEFFFF, 0xC0DFFFFF, 0xD3D2FFFF, 0xE8C8FFFF,
    0xFBC2FFFF, 0xFEC4EAFF,
];
```

### Game Boy (4 colors)

The classic monochrome palette:

```rust
const GAMEBOY_PALETTE: [u32; 4] = [
    0x0F380FFF,  // Darkest green
    0x306230FF,  // Dark green
    0x8BAC0FFF,  // Light green
    0x9BBC0FFF,  // Lightest green
];

// Alternative "Pocket" palette
const GAMEBOY_POCKET: [u32; 4] = [
    0x000000FF,  // Black
    0x555555FF,  // Dark gray
    0xAAAAAAAA,  // Light gray
    0xFFFFFFFF,  // White
];
```

### CGA (16 colors)

IBM PC Color Graphics Adapter:

```rust
const CGA_PALETTE: [u32; 16] = [
    0x000000FF,  // Black
    0x0000AAFF,  // Blue
    0x00AA00FF,  // Green
    0x00AAAAFF,  // Cyan
    0xAA0000FF,  // Red
    0xAA00AAFF,  // Magenta
    0xAA5500FF,  // Brown
    0xAAAAAAFF,  // Light Gray
    0x555555FF,  // Dark Gray
    0x5555FFFF,  // Light Blue
    0x55FF55FF,  // Light Green
    0x55FFFFFF,  // Light Cyan
    0xFF5555FF,  // Light Red
    0xFF55FFFF,  // Light Magenta
    0xFFFF55FF,  // Yellow
    0xFFFFFFFF,  // White
];
```

### Commodore 64 (16 colors)

```rust
const C64_PALETTE: [u32; 16] = [
    0x000000FF,  // Black
    0xFFFFFFFF,  // White
    0x880000FF,  // Red
    0xAAFFEEFF,  // Cyan
    0xCC44CCFF,  // Purple
    0x00CC55FF,  // Green
    0x0000AAFF,  // Blue
    0xEEEE77FF,  // Yellow
    0xDD8855FF,  // Orange
    0x664400FF,  // Brown
    0xFF7777FF,  // Light Red
    0x333333FF,  // Dark Gray
    0x777777FF,  // Medium Gray
    0xAAFF66FF,  // Light Green
    0x0088FFFF,  // Light Blue
    0xBBBBBBFF,  // Light Gray
];
```

### Endesga 32 (32 colors)

Modern pixel art palette by Endesga, popular for indie games:

```rust
const ENDESGA32_PALETTE: [u32; 32] = [
    0xBE4A2FFF, 0xD77643FF, 0xEAD4AAFF, 0xE4A672FF,
    0xB86F50FF, 0x733E39FF, 0x3E2731FF, 0xA22633FF,
    0xE43B44FF, 0xF77622FF, 0xFEAE34FF, 0xFEE761FF,
    0x63C74DFF, 0x3E8948FF, 0x265C42FF, 0x193C3EFF,
    0x124E89FF, 0x0099DBFF, 0x2CE8F5FF, 0xFFFFFFFF,
    0xC0CBDCFF, 0x8B9BB4FF, 0x5A6988FF, 0x3A4466FF,
    0x262B44FF, 0x181425FF, 0xFF0044FF, 0x68386CFF,
    0xB55088FF, 0xF6757AFF, 0xE8B796FF, 0xC28569FF,
];
```

---

## Palette Utility Functions

### Color Quantization

```rust
fn quantize_to_palette(color: u32, palette: &[u32]) -> u32 {
    palette.iter()
        .min_by_key(|&&p| color_distance_squared(color, p))
        .copied()
        .unwrap_or(color)
}

fn color_distance_squared(a: u32, b: u32) -> u32 {
    let dr = ((a >> 24) & 0xFF) as i32 - ((b >> 24) & 0xFF) as i32;
    let dg = ((a >> 16) & 0xFF) as i32 - ((b >> 16) & 0xFF) as i32;
    let db = ((a >> 8) & 0xFF) as i32 - ((b >> 8) & 0xFF) as i32;

    // Weighted distance (human eye more sensitive to green)
    (dr * dr * 2 + dg * dg * 4 + db * db * 3) as u32
}
```

### Palette Extraction (Median Cut)

```rust
fn extract_palette(image: &TextureBuffer, max_colors: usize) -> Vec<u32> {
    // Collect all unique colors
    let mut colors: Vec<u32> = Vec::new();
    for y in 0..image.height {
        for x in 0..image.width {
            let c = image.get(x, y) | 0xFF; // Ignore alpha
            if !colors.contains(&c) {
                colors.push(c);
            }
        }
    }

    if colors.len() <= max_colors {
        return colors;
    }

    // Median cut algorithm
    let mut buckets = vec![colors];

    while buckets.len() < max_colors {
        // Find bucket with widest range
        let (bucket_idx, axis) = find_widest_bucket(&buckets);
        let bucket = buckets.remove(bucket_idx);

        // Sort by the widest axis and split
        let (low, high) = split_bucket_by_axis(bucket, axis);
        buckets.push(low);
        buckets.push(high);
    }

    // Average each bucket
    buckets.iter()
        .map(|b| average_color(b))
        .collect()
}

fn find_widest_bucket(buckets: &[Vec<u32>]) -> (usize, usize) {
    let mut max_range = 0;
    let mut result = (0, 0);

    for (i, bucket) in buckets.iter().enumerate() {
        for axis in 0..3 {
            let range = color_range(bucket, axis);
            if range > max_range {
                max_range = range;
                result = (i, axis);
            }
        }
    }

    result
}

fn color_range(colors: &[u32], axis: usize) -> u32 {
    let shift = (2 - axis) * 8 + 8; // R=24, G=16, B=8
    let values: Vec<u32> = colors.iter()
        .map(|&c| (c >> shift) & 0xFF)
        .collect();

    values.iter().max().unwrap_or(&0) - values.iter().min().unwrap_or(&0)
}

fn split_bucket_by_axis(mut bucket: Vec<u32>, axis: usize) -> (Vec<u32>, Vec<u32>) {
    let shift = (2 - axis) * 8 + 8;
    bucket.sort_by_key(|&c| (c >> shift) & 0xFF);

    let mid = bucket.len() / 2;
    let high = bucket.split_off(mid);
    (bucket, high)
}

fn average_color(colors: &[u32]) -> u32 {
    if colors.is_empty() { return 0x000000FF; }

    let (mut r, mut g, mut b) = (0u64, 0u64, 0u64);
    for &c in colors {
        r += ((c >> 24) & 0xFF) as u64;
        g += ((c >> 16) & 0xFF) as u64;
        b += ((c >> 8) & 0xFF) as u64;
    }

    let n = colors.len() as u64;
    let ar = (r / n) as u32;
    let ag = (g / n) as u32;
    let ab = (b / n) as u32;

    (ar << 24) | (ag << 16) | (ab << 8) | 0xFF
}
```

---

## Python Implementations

### Using PIL for Quantization

```python
from PIL import Image
import numpy as np

def quantize_image(image_path, palette_name="pico8"):
    """Quantize image to a predefined palette."""
    palettes = {
        "pico8": PICO8_PALETTE,
        "gameboy": GAMEBOY_PALETTE,
        "nes": NES_PALETTE[:16],  # Use first 16 for simplicity
    }

    palette = palettes.get(palette_name, PICO8_PALETTE)
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img)

    # Quantize each pixel
    result = np.zeros_like(pixels)
    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            original = pixels[y, x]
            closest = find_closest_color(original, palette)
            result[y, x] = closest

    return Image.fromarray(result)

def find_closest_color(rgb, palette):
    """Find closest palette color using weighted distance."""
    min_dist = float('inf')
    closest = palette[0]

    for color in palette:
        # Parse 0xRRGGBBAA format
        pr = (color >> 24) & 0xFF
        pg = (color >> 16) & 0xFF
        pb = (color >> 8) & 0xFF

        # Weighted distance
        dr = rgb[0] - pr
        dg = rgb[1] - pg
        db = rgb[2] - pb
        dist = dr*dr*2 + dg*dg*4 + db*db*3

        if dist < min_dist:
            min_dist = dist
            closest = [pr, pg, pb]

    return closest

# Palettes in Python format
PICO8_PALETTE = [
    0x000000FF, 0x1D2B53FF, 0x7E2553FF, 0x008751FF,
    0xAB5236FF, 0x5F574FFF, 0xC2C3C7FF, 0xFFF1E8FF,
    0xFF004DFF, 0xFFA300FF, 0xFFEC27FF, 0x00E436FF,
    0x29ADFFFF, 0x83769CFF, 0xFF77A8FF, 0xFFCCAAFF,
]

GAMEBOY_PALETTE = [
    0x0F380FFF, 0x306230FF, 0x8BAC0FFF, 0x9BBC0FFF,
]
```

### K-Means Palette Extraction

```python
from sklearn.cluster import KMeans
import numpy as np
from PIL import Image

def extract_palette_kmeans(image_path, num_colors=16):
    """Extract palette using K-means clustering."""
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img).reshape(-1, 3)

    # K-means clustering
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)

    # Get cluster centers as palette
    palette = []
    for center in kmeans.cluster_centers_:
        r, g, b = int(center[0]), int(center[1]), int(center[2])
        palette.append((r << 24) | (g << 16) | (b << 8) | 0xFF)

    return palette

def apply_palette(image_path, palette, output_path):
    """Apply extracted palette to image."""
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img)

    result = np.zeros_like(pixels)
    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            result[y, x] = find_closest_color(pixels[y, x], palette)

    Image.fromarray(result).save(output_path)
```

---

## Color Manipulation

### Lighten/Darken

```rust
fn lighten(color: u32, amount: f32) -> u32 {
    let r = ((color >> 24) & 0xFF) as f32;
    let g = ((color >> 16) & 0xFF) as f32;
    let b = ((color >> 8) & 0xFF) as f32;
    let a = color & 0xFF;

    let nr = (r + (255.0 - r) * amount).min(255.0) as u32;
    let ng = (g + (255.0 - g) * amount).min(255.0) as u32;
    let nb = (b + (255.0 - b) * amount).min(255.0) as u32;

    (nr << 24) | (ng << 16) | (nb << 8) | a
}

fn darken(color: u32, amount: f32) -> u32 {
    let r = ((color >> 24) & 0xFF) as f32;
    let g = ((color >> 16) & 0xFF) as f32;
    let b = ((color >> 8) & 0xFF) as f32;
    let a = color & 0xFF;

    let nr = (r * (1.0 - amount)) as u32;
    let ng = (g * (1.0 - amount)) as u32;
    let nb = (b * (1.0 - amount)) as u32;

    (nr << 24) | (ng << 16) | (nb << 8) | a
}
```

### Desaturate

```rust
fn desaturate(color: u32, amount: f32) -> u32 {
    let r = ((color >> 24) & 0xFF) as f32;
    let g = ((color >> 16) & 0xFF) as f32;
    let b = ((color >> 8) & 0xFF) as f32;
    let a = color & 0xFF;

    // Luminance
    let lum = r * 0.299 + g * 0.587 + b * 0.114;

    let nr = (r + (lum - r) * amount) as u32;
    let ng = (g + (lum - g) * amount) as u32;
    let nb = (b + (lum - b) * amount) as u32;

    (nr << 24) | (ng << 16) | (nb << 8) | a
}
```

### Hue Shift

```rust
fn hue_shift(color: u32, degrees: f32) -> u32 {
    let r = ((color >> 24) & 0xFF) as f32 / 255.0;
    let g = ((color >> 16) & 0xFF) as f32 / 255.0;
    let b = ((color >> 8) & 0xFF) as f32 / 255.0;
    let a = color & 0xFF;

    // RGB to HSV
    let (h, s, v) = rgb_to_hsv(r, g, b);

    // Shift hue
    let new_h = (h + degrees / 360.0).fract();
    if new_h < 0.0 { new_h += 1.0; }

    // HSV to RGB
    let (nr, ng, nb) = hsv_to_rgb(new_h, s, v);

    ((nr * 255.0) as u32) << 24 |
    ((ng * 255.0) as u32) << 16 |
    ((nb * 255.0) as u32) << 8 |
    a
}
```

---

## Dithering Matrices

### Bayer Matrices

```rust
// 2x2 Bayer matrix
const BAYER_2X2: [f32; 4] = [
    0.0/4.0, 2.0/4.0,
    3.0/4.0, 1.0/4.0,
];

// 4x4 Bayer matrix
const BAYER_4X4: [f32; 16] = [
     0.0/16.0,  8.0/16.0,  2.0/16.0, 10.0/16.0,
    12.0/16.0,  4.0/16.0, 14.0/16.0,  6.0/16.0,
     3.0/16.0, 11.0/16.0,  1.0/16.0,  9.0/16.0,
    15.0/16.0,  7.0/16.0, 13.0/16.0,  5.0/16.0,
];

// 8x8 Bayer matrix
const BAYER_8X8: [f32; 64] = [
     0.0/64.0, 32.0/64.0,  8.0/64.0, 40.0/64.0,  2.0/64.0, 34.0/64.0, 10.0/64.0, 42.0/64.0,
    48.0/64.0, 16.0/64.0, 56.0/64.0, 24.0/64.0, 50.0/64.0, 18.0/64.0, 58.0/64.0, 26.0/64.0,
    12.0/64.0, 44.0/64.0,  4.0/64.0, 36.0/64.0, 14.0/64.0, 46.0/64.0,  6.0/64.0, 38.0/64.0,
    60.0/64.0, 28.0/64.0, 52.0/64.0, 20.0/64.0, 62.0/64.0, 30.0/64.0, 54.0/64.0, 22.0/64.0,
     3.0/64.0, 35.0/64.0, 11.0/64.0, 43.0/64.0,  1.0/64.0, 33.0/64.0,  9.0/64.0, 41.0/64.0,
    51.0/64.0, 19.0/64.0, 59.0/64.0, 27.0/64.0, 49.0/64.0, 17.0/64.0, 57.0/64.0, 25.0/64.0,
    15.0/64.0, 47.0/64.0,  7.0/64.0, 39.0/64.0, 13.0/64.0, 45.0/64.0,  5.0/64.0, 37.0/64.0,
    63.0/64.0, 31.0/64.0, 55.0/64.0, 23.0/64.0, 61.0/64.0, 29.0/64.0, 53.0/64.0, 21.0/64.0,
];
```

### Error Diffusion Kernels

```rust
// Floyd-Steinberg (right, bottom-left, bottom, bottom-right)
const FLOYD_STEINBERG: [(i32, i32, f32); 4] = [
    (1, 0, 7.0/16.0),
    (-1, 1, 3.0/16.0),
    (0, 1, 5.0/16.0),
    (1, 1, 1.0/16.0),
];

// Atkinson (6 neighbors, each 1/8)
const ATKINSON: [(i32, i32, f32); 6] = [
    (1, 0, 1.0/8.0),
    (2, 0, 1.0/8.0),
    (-1, 1, 1.0/8.0),
    (0, 1, 1.0/8.0),
    (1, 1, 1.0/8.0),
    (0, 2, 1.0/8.0),
];

// Jarvis-Judice-Ninke (12 neighbors)
const JJN: [(i32, i32, f32); 12] = [
    (1, 0, 7.0/48.0), (2, 0, 5.0/48.0),
    (-2, 1, 3.0/48.0), (-1, 1, 5.0/48.0), (0, 1, 7.0/48.0), (1, 1, 5.0/48.0), (2, 1, 3.0/48.0),
    (-2, 2, 1.0/48.0), (-1, 2, 3.0/48.0), (0, 2, 5.0/48.0), (1, 2, 3.0/48.0), (2, 2, 1.0/48.0),
];
```

---

## Choosing Algorithms

| Goal | Palette Algorithm | Dither Algorithm |
|------|-------------------|------------------|
| Speed | Predefined palette | Ordered (Bayer) |
| Quality | K-means | Floyd-Steinberg |
| Retro look | Predefined (PICO-8, etc.) | Ordered (Bayer 4x4) |
| Photos | Median cut | Floyd-Steinberg |
| Icons/UI | Predefined | None or minimal |
| High contrast | K-means | Atkinson |

**Recommendations:**
- Use predefined palettes (PICO-8, NES) for authentic retro aesthetics
- Use Bayer ordered dithering for consistent, predictable patterns
- Use Floyd-Steinberg for smoother gradients in photos
- Skip dithering for sharp UI elements and text
