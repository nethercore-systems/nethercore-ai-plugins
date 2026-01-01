# TextureBuffer API Reference

A Python class wrapping Pillow (PIL) and NumPy for procedural texture generation.

## Dependencies

```bash
pip install pillow numpy pyfastnoiselite
```

## TextureBuffer Class

```python
import numpy as np
from PIL import Image
from pyfastnoiselite import FastNoiseLite, NoiseType, FractalType

class TextureBuffer:
    """Buffer for procedural texture generation using PIL + NumPy."""

    def __init__(self, width: int, height: int):
        """Create RGBA texture buffer."""
        self.width = width
        self.height = height
        self.data = np.zeros((height, width, 4), dtype=np.uint8)
        self.data[:, :, 3] = 255  # Default opaque

    # === Pixel Access ===

    def get(self, x: int, y: int) -> tuple[int, int, int, int]:
        """Get pixel as (R, G, B, A) tuple."""
        return tuple(self.data[y, x])

    def set(self, x: int, y: int, color: tuple[int, int, int, int]):
        """Set pixel from (R, G, B, A) tuple."""
        self.data[y, x] = color

    # === Fill Operations ===

    def fill(self, color: tuple[int, int, int, int]):
        """Fill entire buffer with solid color."""
        self.data[:, :] = color

    def fill_rgb(self, r: int, g: int, b: int, a: int = 255):
        """Fill with separate RGB(A) values."""
        self.fill((r, g, b, a))

    # === Gradient Operations ===

    def gradient_vertical(self, top: tuple, bottom: tuple):
        """Vertical gradient from top to bottom color."""
        for y in range(self.height):
            t = y / (self.height - 1)
            color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(4))
            self.data[y, :] = color

    def gradient_horizontal(self, left: tuple, right: tuple):
        """Horizontal gradient from left to right color."""
        for x in range(self.width):
            t = x / (self.width - 1)
            color = tuple(int(left[i] * (1 - t) + right[i] * t) for i in range(4))
            self.data[:, x] = color

    def gradient_radial(self, center: tuple, edge: tuple):
        """Radial gradient from center to edge."""
        cx, cy = self.width / 2, self.height / 2
        max_dist = np.sqrt(cx**2 + cy**2)

        for y in range(self.height):
            for x in range(self.width):
                dist = np.sqrt((x - cx)**2 + (y - cy)**2)
                t = min(1.0, dist / max_dist)
                color = tuple(int(center[i] * (1 - t) + edge[i] * t) for i in range(4))
                self.data[y, x] = color

    # === Pattern Operations ===

    def checker(self, tile_size: int, color_a: tuple, color_b: tuple):
        """Checkerboard pattern."""
        for y in range(self.height):
            for x in range(self.width):
                if ((x // tile_size) + (y // tile_size)) % 2 == 0:
                    self.data[y, x] = color_a
                else:
                    self.data[y, x] = color_b

    # === I/O ===

    def save(self, path: str):
        """Save texture as PNG."""
        Image.fromarray(self.data, 'RGBA').save(path)

    def load(self, path: str):
        """Load texture from image file."""
        img = Image.open(path).convert('RGBA')
        self.data = np.array(img)
        self.width, self.height = img.size

    def to_image(self) -> Image.Image:
        """Convert to PIL Image."""
        return Image.fromarray(self.data, 'RGBA')

    # === Blending ===

    def blend(self, other: 'TextureBuffer', mode: str = 'normal', opacity: float = 1.0):
        """Blend another texture onto this one.

        Modes: normal, multiply, add, overlay, screen
        """
        src = other.data.astype(np.float32) / 255.0
        dst = self.data.astype(np.float32) / 255.0

        if mode == 'normal':
            result = src
        elif mode == 'multiply':
            result = src * dst
        elif mode == 'add':
            result = np.clip(src + dst, 0, 1)
        elif mode == 'overlay':
            mask = dst < 0.5
            result = np.where(mask, 2 * src * dst, 1 - 2 * (1 - src) * (1 - dst))
        elif mode == 'screen':
            result = 1 - (1 - src) * (1 - dst)
        else:
            result = src

        # Apply opacity and blend
        blended = dst * (1 - opacity) + result * opacity
        self.data = (np.clip(blended, 0, 1) * 255).astype(np.uint8)

    # === Color Adjustments ===

    def brightness(self, amount: float):
        """Adjust brightness. amount: -1.0 to 1.0"""
        self.data[:, :, :3] = np.clip(
            self.data[:, :, :3].astype(np.float32) + amount * 255, 0, 255
        ).astype(np.uint8)

    def contrast(self, factor: float):
        """Adjust contrast. factor: 0.0 to 2.0 (1.0 = no change)"""
        rgb = self.data[:, :, :3].astype(np.float32)
        rgb = (rgb - 128) * factor + 128
        self.data[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)

    def invert(self):
        """Invert colors (keep alpha)."""
        self.data[:, :, :3] = 255 - self.data[:, :, :3]

    def posterize(self, levels: int):
        """Reduce color levels (2-256)."""
        step = 256 // levels
        self.data[:, :, :3] = (self.data[:, :, :3] // step) * step
```

## Noise Methods

Add these methods to TextureBuffer for noise generation:

```python
class TextureBuffer:
    # ... (previous methods) ...

    def add_perlin_noise(self, scale: float = 0.05, intensity: float = 0.3,
                         seed: int = 42, blend_mode: str = 'overlay'):
        """Add Perlin noise layer."""
        noise = FastNoiseLite(seed)
        noise.noise_type = NoiseType.NoiseType_Perlin
        noise.frequency = scale

        noise_tex = TextureBuffer(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                val = (noise.get_noise(x, y) + 1) / 2  # [0, 1]
                gray = int(val * 255)
                noise_tex.data[y, x] = (gray, gray, gray, 255)

        self.blend(noise_tex, blend_mode, intensity)

    def add_simplex_noise(self, scale: float = 0.05, intensity: float = 0.3,
                          seed: int = 42, blend_mode: str = 'overlay'):
        """Add Simplex noise layer."""
        noise = FastNoiseLite(seed)
        noise.noise_type = NoiseType.NoiseType_OpenSimplex2
        noise.frequency = scale

        noise_tex = TextureBuffer(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                val = (noise.get_noise(x, y) + 1) / 2
                gray = int(val * 255)
                noise_tex.data[y, x] = (gray, gray, gray, 255)

        self.blend(noise_tex, blend_mode, intensity)

    def add_cellular_noise(self, scale: float = 0.05, intensity: float = 0.3,
                           seed: int = 42, blend_mode: str = 'overlay'):
        """Add Cellular/Voronoi noise layer."""
        noise = FastNoiseLite(seed)
        noise.noise_type = NoiseType.NoiseType_Cellular
        noise.frequency = scale

        noise_tex = TextureBuffer(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                val = (noise.get_noise(x, y) + 1) / 2
                gray = int(val * 255)
                noise_tex.data[y, x] = (gray, gray, gray, 255)

        self.blend(noise_tex, blend_mode, intensity)

    def add_fbm_noise(self, scale: float = 0.03, octaves: int = 4,
                      persistence: float = 0.5, intensity: float = 0.3,
                      seed: int = 42, blend_mode: str = 'overlay'):
        """Add Fractal Brownian Motion noise layer."""
        noise = FastNoiseLite(seed)
        noise.noise_type = NoiseType.NoiseType_Perlin
        noise.frequency = scale
        noise.fractal_type = FractalType.FractalType_FBm
        noise.fractal_octaves = octaves
        noise.fractal_gain = persistence

        noise_tex = TextureBuffer(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                val = (noise.get_noise(x, y) + 1) / 2
                gray = int(val * 255)
                noise_tex.data[y, x] = (gray, gray, gray, 255)

        self.blend(noise_tex, blend_mode, intensity)
```

## Quick Examples

### Simple Albedo

```python
tex = TextureBuffer(256, 256)
tex.fill((139, 69, 19, 255))  # Brown
tex.add_perlin_noise(scale=0.03, intensity=0.2)
tex.save("bark_albedo.png")
```

### Gradient with Noise

```python
tex = TextureBuffer(256, 256)
tex.gradient_vertical((100, 150, 200, 255), (30, 60, 90, 255))
tex.add_fbm_noise(scale=0.02, octaves=4, intensity=0.15)
tex.save("sky_gradient.png")
```

### MRE Map

```python
# Create MRE map: R=Metallic, G=Roughness, B=Emissive
tex = TextureBuffer(256, 256)
metallic = 0.8
roughness = 0.4
emissive = 0.0

for y in range(256):
    for x in range(256):
        tex.set(x, y, (
            int(metallic * 255),
            int(roughness * 255),
            int(emissive * 255),
            255
        ))

tex.save("metal_mre.png")
```

## Color Format

Colors are RGBA tuples: `(R, G, B, A)` with values 0-255.

```python
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
TRANSPARENT = (0, 0, 0, 0)
HALF_ALPHA = (255, 255, 255, 128)
```
