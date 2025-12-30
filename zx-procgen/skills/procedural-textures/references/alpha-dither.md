# Alpha Channel and Dither Transparency

ZX uses **dithered transparency** via the alpha channel. Instead of true alpha blending (which is order-dependent), ZX uses a Bayer dither pattern to create stippled transparency.

## How Dither Transparency Works

- Alpha value is compared against a Bayer 4x4 dither threshold per pixel
- Below threshold = fragment discarded (fully transparent)
- Above threshold = fragment kept (fully opaque)
- Result: Order-independent "screen door" transparency

---

## Alpha Pattern Generators

```python
import numpy as np
from PIL import Image
from pyfastnoiselite import FastNoiseLite, NoiseType
import math

def generate_solid_alpha(size: int = 256, alpha: int = 255) -> np.ndarray:
    """Generate solid alpha channel."""
    return np.full((size, size), alpha, dtype=np.uint8)


def generate_radial_alpha(size: int = 256, falloff: float = 1.0) -> np.ndarray:
    """Generate radial gradient alpha (center opaque, edges transparent)."""
    alpha = np.zeros((size, size), dtype=np.uint8)
    center = size / 2

    for y in range(size):
        for x in range(size):
            dx = (x - center) / center
            dy = (y - center) / center
            dist = min(1.0, math.sqrt(dx*dx + dy*dy))
            alpha[y, x] = int((1.0 - dist ** falloff) * 255)

    return alpha


def generate_edge_fade_alpha(size: int = 256, fade_width: float = 0.25) -> np.ndarray:
    """Generate edge-fading alpha (opaque center, faded edges)."""
    alpha = np.zeros((size, size), dtype=np.uint8)
    fade_pixels = int(size * fade_width)

    for y in range(size):
        for x in range(size):
            # Distance to nearest edge
            edge_dist = min(x, size - 1 - x, y, size - 1 - y)
            if edge_dist < fade_pixels:
                alpha[y, x] = int((edge_dist / fade_pixels) * 255)
            else:
                alpha[y, x] = 255

    return alpha


def generate_noise_holes_alpha(size: int = 256, threshold: float = 0.3,
                                seed: int = 42) -> np.ndarray:
    """Generate alpha with noise-based holes."""
    alpha = np.zeros((size, size), dtype=np.uint8)

    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.08

    for y in range(size):
        for x in range(size):
            n = (noise.get_noise(x, y) + 1) / 2

            if n > threshold:
                alpha[y, x] = 255
            else:
                alpha[y, x] = 0

    return alpha


def generate_gradient_alpha(size: int = 256, start: int = 255, end: int = 0,
                            direction: str = 'vertical') -> np.ndarray:
    """Generate linear gradient alpha."""
    alpha = np.zeros((size, size), dtype=np.uint8)

    for y in range(size):
        for x in range(size):
            if direction == 'vertical':
                t = y / (size - 1)
            else:  # horizontal
                t = x / (size - 1)

            alpha[y, x] = int(start * (1 - t) + end * t)

    return alpha


def generate_cellular_alpha(size: int = 256, cell_scale: float = 0.1,
                            seed: int = 42) -> np.ndarray:
    """Generate cell-based alpha pattern."""
    alpha = np.zeros((size, size), dtype=np.uint8)

    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_Cellular
    noise.frequency = cell_scale

    for y in range(size):
        for x in range(size):
            n = (noise.get_noise(x, y) + 1) / 2
            alpha[y, x] = int(n * 255)

    return alpha
```

---

## Complete Albedo with Alpha

```python
def generate_albedo_with_alpha(name: str, base_color: tuple, alpha_type: str,
                                size: int = 256, seed: int = 42, **kwargs):
    """Generate complete albedo texture with alpha channel.

    Args:
        alpha_type: 'solid', 'radial', 'edge_fade', 'noise_holes',
                    'gradient_v', 'gradient_h', 'cellular'
        **kwargs: Additional parameters for specific alpha types
    """
    img = np.zeros((size, size, 4), dtype=np.uint8)

    # Generate albedo
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.03

    for y in range(size):
        for x in range(size):
            n = (noise.get_noise(x, y) + 1) / 2
            factor = 0.85 + n * 0.3

            img[y, x, 0] = int(min(255, base_color[0] * factor))
            img[y, x, 1] = int(min(255, base_color[1] * factor))
            img[y, x, 2] = int(min(255, base_color[2] * factor))

    # Generate alpha
    if alpha_type == 'solid':
        alpha = generate_solid_alpha(size, kwargs.get('alpha', 255))
    elif alpha_type == 'radial':
        alpha = generate_radial_alpha(size, kwargs.get('falloff', 1.0))
    elif alpha_type == 'edge_fade':
        alpha = generate_edge_fade_alpha(size, kwargs.get('fade_width', 0.25))
    elif alpha_type == 'noise_holes':
        alpha = generate_noise_holes_alpha(size, kwargs.get('threshold', 0.3), seed)
    elif alpha_type == 'gradient_v':
        alpha = generate_gradient_alpha(size, kwargs.get('start', 255),
                                        kwargs.get('end', 0), 'vertical')
    elif alpha_type == 'gradient_h':
        alpha = generate_gradient_alpha(size, kwargs.get('start', 255),
                                        kwargs.get('end', 0), 'horizontal')
    elif alpha_type == 'cellular':
        alpha = generate_cellular_alpha(size, kwargs.get('cell_scale', 0.1), seed)
    else:
        alpha = generate_solid_alpha(size)

    img[:, :, 3] = alpha

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")


# Examples
generate_albedo_with_alpha("particle", (255, 200, 100, 255), 'radial', falloff=2.0)
generate_albedo_with_alpha("foliage", (60, 120, 40, 255), 'edge_fade', fade_width=0.15)
generate_albedo_with_alpha("decay", (80, 60, 40, 255), 'noise_holes', threshold=0.4)
generate_albedo_with_alpha("smoke", (200, 200, 200, 255), 'gradient_v', start=200, end=0)
```

---

## Particle/Billboard Textures

```python
def generate_particle_texture(name: str, color: tuple, glow_falloff: float = 2.0,
                               size: int = 64, seed: int = 42):
    """Generate particle/billboard texture with radial alpha."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    center = size / 2

    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.1

    for y in range(size):
        for x in range(size):
            dx = (x - center) / center
            dy = (y - center) / center
            dist = math.sqrt(dx*dx + dy*dy)

            if dist <= 1.0:
                # Color with noise variation
                n = (noise.get_noise(x, y) + 1) / 2
                factor = 0.9 + n * 0.2

                img[y, x, 0] = int(min(255, color[0] * factor))
                img[y, x, 1] = int(min(255, color[1] * factor))
                img[y, x, 2] = int(min(255, color[2] * factor))

                # Radial alpha falloff
                alpha = (1.0 - dist ** glow_falloff) ** 0.5
                img[y, x, 3] = int(alpha * 255)
            else:
                img[y, x] = (0, 0, 0, 0)

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")


# Examples
generate_particle_texture("fire_particle", (255, 150, 50, 255), glow_falloff=1.5)
generate_particle_texture("smoke_particle", (180, 180, 180, 255), glow_falloff=2.5)
generate_particle_texture("magic_particle", (100, 200, 255, 255), glow_falloff=1.0)
```

---

## Foliage/Vegetation Alpha

```python
def generate_foliage_alpha(name: str, leaf_color: tuple, stem_color: tuple,
                           leaf_density: float = 0.5, size: int = 256, seed: int = 42):
    """Generate foliage texture with organic alpha cutout."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    # Noise for leaf shapes
    noise1 = FastNoiseLite(seed)
    noise1.noise_type = NoiseType.NoiseType_Cellular
    noise1.frequency = 0.12

    # Noise for color variation
    noise2 = FastNoiseLite(seed + 1)
    noise2.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise2.frequency = 0.05

    for y in range(size):
        for x in range(size):
            n1 = (noise1.get_noise(x, y) + 1) / 2
            n2 = (noise2.get_noise(x, y) + 1) / 2

            # Leaf cutout based on cellular noise
            if n1 < leaf_density:
                # Inside a leaf
                factor = 0.8 + n2 * 0.4

                img[y, x, 0] = int(min(255, leaf_color[0] * factor))
                img[y, x, 1] = int(min(255, leaf_color[1] * factor))
                img[y, x, 2] = int(min(255, leaf_color[2] * factor))
                img[y, x, 3] = 255
            else:
                # Transparent background
                img[y, x] = (0, 0, 0, 0)

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")


generate_foliage_alpha("leaves", (60, 120, 40, 255), (80, 60, 30, 255), leaf_density=0.6)
```

---

## Common Alpha Patterns

| Pattern | Use Case | Key Parameter |
|---------|----------|---------------|
| Radial | Particles, lights, explosions | falloff (1.0-3.0) |
| Edge Fade | Foliage, cloth edges | fade_width (0.1-0.3) |
| Noise Holes | Decay, damage, organic | threshold (0.3-0.6) |
| Gradient | Fog, smoke, clouds | direction, start, end |
| Cellular | Organic patterns, scales | cell_scale |

---

## Runtime Alpha Control

Beyond texture alpha, control transparency via uniforms:

```python
# Game code
set_alpha(0.5)  # 50% overall transparency (multiplied with texture alpha)
```

---

## Dither Pattern Preview

```python
def preview_dither_effect(texture_path: str, output_path: str, threshold_level: float = 0.5):
    """Preview how alpha will look with dithering applied."""
    img = Image.open(texture_path).convert('RGBA')
    data = np.array(img)

    # 4x4 Bayer matrix
    bayer = np.array([
        [0, 8, 2, 10],
        [12, 4, 14, 6],
        [3, 11, 1, 9],
        [15, 7, 13, 5]
    ]) / 16.0

    height, width = data.shape[:2]
    result = data.copy()

    for y in range(height):
        for x in range(width):
            alpha_normalized = data[y, x, 3] / 255.0
            threshold = bayer[y % 4, x % 4]

            if alpha_normalized < threshold * threshold_level:
                result[y, x, 3] = 0  # Fully transparent
            else:
                result[y, x, 3] = 255  # Fully opaque

    Image.fromarray(result, 'RGBA').save(output_path)


# Preview dither effect
preview_dither_effect("particle_albedo.png", "particle_dithered.png")
```

**Note:** Dither transparency works best with moving objects or at a distance. Close-up static objects may show visible dither patterns (intentional retro aesthetic).
