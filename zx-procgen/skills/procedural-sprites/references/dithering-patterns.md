# Dithering Patterns

Simulate more colors with limited palettes by distributing quantization error.

## Ordered Dithering (Bayer Matrix)

Predictable, fast, no error propagation. Creates characteristic crosshatch patterns:

```python
import numpy as np
from PIL import Image

# Bayer 4x4 dither matrix (normalized 0-1)
BAYER_4X4 = np.array([
    [ 0,  8,  2, 10],
    [12,  4, 14,  6],
    [ 3, 11,  1,  9],
    [15,  7, 13,  5]
], dtype=np.float32) / 16.0

def apply_ordered_dither(img: Image.Image, palette: np.ndarray, matrix_size: int = 4) -> Image.Image:
    """Apply ordered (Bayer) dithering to an image."""
    pixels = np.array(img, dtype=np.float32)
    h, w = pixels.shape[:2]

    # Select Bayer matrix based on size
    bayer_matrices = {2: BAYER_2X2, 4: BAYER_4X4, 8: BAYER_8X8}
    bayer = bayer_matrices.get(matrix_size, BAYER_4X4)

    # Create threshold map using broadcasting (vectorized)
    y_indices = np.arange(h) % matrix_size
    x_indices = np.arange(w) % matrix_size
    threshold = bayer[y_indices][:, x_indices] - 0.5

    # Adjust pixel brightness by threshold before quantizing
    adjusted = pixels + threshold[..., np.newaxis] * 32  # Scale factor for adjustment

    # Quantize each pixel to nearest palette color
    result = quantize_to_palette(adjusted, palette)

    return Image.fromarray(result.astype(np.uint8))
```

## Floyd-Steinberg Error Diffusion

Distributes quantization error to neighboring pixels for smoother gradients:

```python
import numpy as np
from PIL import Image

def apply_floyd_steinberg(img: Image.Image, palette: np.ndarray) -> Image.Image:
    """
    Floyd-Steinberg error diffusion dithering.

    Error distribution weights:
           X   7/16
    3/16  5/16  1/16
    """
    pixels = np.array(img, dtype=np.float32)
    h, w = pixels.shape[:2]

    for y in range(h):
        for x in range(w):
            old_pixel = pixels[y, x].copy()
            new_pixel = quantize_pixel_to_palette(old_pixel, palette)
            pixels[y, x] = new_pixel

            # Calculate quantization error
            error = old_pixel - new_pixel

            # Distribute error to neighboring pixels
            if x + 1 < w:
                pixels[y, x + 1] += error * (7 / 16)
            if y + 1 < h:
                if x > 0:
                    pixels[y + 1, x - 1] += error * (3 / 16)
                pixels[y + 1, x] += error * (5 / 16)
                if x + 1 < w:
                    pixels[y + 1, x + 1] += error * (1 / 16)

    # Clip values to valid range
    pixels = np.clip(pixels, 0, 255)
    return Image.fromarray(pixels.astype(np.uint8))
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

```python
import numpy as np

def adjust_by_threshold(pixel: np.ndarray, threshold: float, strength: float) -> np.ndarray:
    """
    Adjust pixel brightness by threshold with controllable strength.

    Args:
        pixel: RGB(A) pixel values as numpy array
        threshold: Bayer threshold value (-0.5 to 0.5)
        strength: Dithering intensity (0.0 = none, 1.0 = full)

    Returns:
        Adjusted pixel values
    """
    adjusted_threshold = threshold * strength
    # Apply adjustment to RGB channels (scale by ~32 for visible effect)
    adjustment = adjusted_threshold * 32
    return np.clip(pixel[:3] + adjustment, 0, 255)
```

- `strength = 0.0`: No dithering (hard quantization)
- `strength = 0.5`: Subtle dithering
- `strength = 1.0`: Full dithering effect
