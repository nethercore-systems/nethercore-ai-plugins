# Dithering Patterns

Simulate more colors with limited palettes by distributing quantization error.

## Ordered Dithering (Bayer Matrix)

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

## Floyd-Steinberg Error Diffusion

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

## Python Ordered Dithering

```python
from PIL import Image
import numpy as np

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

## Algorithm Comparison

| Algorithm | Look | Speed | Use Case |
|-----------|------|-------|----------|
| Ordered (Bayer) | Patterned | Fast | Retro pixel art |
| Floyd-Steinberg | Smooth | Medium | Photos, gradients |
| Atkinson | Lighter | Medium | Mac classic style |
| No dithering | Banded | Fastest | UI, sharp edges |

## Dithering Strength

Control dithering intensity for different effects:

```rust
fn adjust_by_threshold(pixel: u32, threshold: f32, strength: f32) -> u32 {
    // strength: 0.0 = no dithering, 1.0 = full dithering
    let adjusted_threshold = threshold * strength;
    // Apply to each channel...
}
```

- `strength = 0.0`: No dithering (hard quantization)
- `strength = 0.5`: Subtle dithering
- `strength = 1.0`: Full dithering effect
