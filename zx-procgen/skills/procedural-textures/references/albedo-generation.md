# Albedo Texture Generation

Albedo is the base diffuse color without lighting. Generate with noise, patterns, or layered composition.

## Simple Albedo with Noise Variation

```python
import numpy as np
from PIL import Image
from pyfastnoiselite import FastNoiseLite, NoiseType, FractalType

def generate_albedo(name: str, base_color: tuple, variation: float = 0.2,
                    size: int = 256, seed: int = 42):
    """Generate albedo texture with noise-based color variation.

    Args:
        name: Output filename (without extension)
        base_color: (R, G, B, A) base color tuple
        variation: How much noise affects color (0.0 - 1.0)
        size: Texture size (power of 2)
        seed: Random seed for noise
    """
    img = np.zeros((size, size, 4), dtype=np.uint8)

    # Setup noise
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.03
    noise.fractal_type = FractalType.FractalType_FBm
    noise.fractal_octaves = 4

    r, g, b, a = base_color

    for y in range(size):
        for x in range(size):
            # Get noise value [0, 1]
            n = (noise.get_noise(x, y) + 1) / 2

            # Modulate color by noise
            factor = 1.0 - variation + variation * n
            img[y, x] = [
                int(min(255, r * factor)),
                int(min(255, g * factor)),
                int(min(255, b * factor)),
                a
            ]

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")

# Examples
generate_albedo("bark", (139, 69, 19, 255), variation=0.3)
generate_albedo("stone", (128, 128, 128, 255), variation=0.2)
generate_albedo("grass", (34, 139, 34, 255), variation=0.25)
```

---

## Two-Color Noise Blend

```python
def generate_two_color_albedo(name: str, color_a: tuple, color_b: tuple,
                               size: int = 256, scale: float = 0.05, seed: int = 42):
    """Generate albedo blending between two colors based on noise."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = scale

    for y in range(size):
        for x in range(size):
            t = (noise.get_noise(x, y) + 1) / 2  # [0, 1]

            for c in range(4):
                img[y, x, c] = int(color_a[c] * (1 - t) + color_b[c] * t)

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")

# Example: Mossy stone
generate_two_color_albedo("mossy_stone",
    (100, 100, 100, 255),  # Gray stone
    (60, 90, 40, 255),      # Green moss
    scale=0.08
)
```

---

## Multi-Color Palette Blend

```python
def generate_palette_albedo(name: str, palette: list[tuple],
                            size: int = 256, seed: int = 42):
    """Generate albedo using a color palette with noise selection."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.04
    noise.fractal_type = FractalType.FractalType_FBm
    noise.fractal_octaves = 3

    num_colors = len(palette)

    for y in range(size):
        for x in range(size):
            n = (noise.get_noise(x, y) + 1) / 2  # [0, 1]

            # Map to palette
            idx = min(int(n * num_colors), num_colors - 1)
            img[y, x] = palette[idx]

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")

# Desert sand palette
desert_palette = [
    (194, 178, 128, 255),  # Light sand
    (180, 160, 110, 255),  # Medium sand
    (160, 140, 95, 255),   # Dark sand
    (140, 120, 80, 255),   # Shadow
]
generate_palette_albedo("desert", desert_palette)
```

---

## Layered Albedo (Professional Quality)

```python
def generate_layered_albedo(name: str, base_color: tuple, dark_color: tuple,
                            light_color: tuple, size: int = 256, seed: int = 42):
    """Generate professional albedo with multiple noise layers."""
    img = np.zeros((size, size, 4), dtype=np.float32)

    # Base layer
    img[:, :] = [c / 255.0 for c in base_color]

    # Layer 1: Large-scale variation
    noise1 = FastNoiseLite(seed)
    noise1.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise1.frequency = 0.02

    for y in range(size):
        for x in range(size):
            n = (noise1.get_noise(x, y) + 1) / 2
            # Darken or lighten based on noise
            factor = 0.85 + n * 0.3  # 0.85 to 1.15
            img[y, x, :3] *= factor

    # Layer 2: Fine detail
    noise2 = FastNoiseLite(seed + 1)
    noise2.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise2.frequency = 0.08
    noise2.fractal_type = FractalType.FractalType_FBm
    noise2.fractal_octaves = 3

    for y in range(size):
        for x in range(size):
            n = (noise2.get_noise(x, y) + 1) / 2
            factor = 0.95 + n * 0.1  # Subtle variation
            img[y, x, :3] *= factor

    # Layer 3: Occasional dark spots
    noise3 = FastNoiseLite(seed + 2)
    noise3.noise_type = NoiseType.NoiseType_Cellular
    noise3.frequency = 0.15

    for y in range(size):
        for x in range(size):
            n = (noise3.get_noise(x, y) + 1) / 2
            if n < 0.15:  # 15% dark spots
                blend = 1 - (0.15 - n) / 0.15 * 0.3
                img[y, x, :3] *= blend

    # Clamp and convert to uint8
    img = np.clip(img, 0, 1)
    result = (img * 255).astype(np.uint8)
    Image.fromarray(result, 'RGBA').save(f"{name}_albedo.png")

# Example: Rich bark texture
generate_layered_albedo("bark",
    base_color=(110, 70, 45, 255),
    dark_color=(60, 35, 20, 255),
    light_color=(150, 100, 70, 255)
)
```

---

## Pattern-Based Albedo

### Brick Pattern

```python
def generate_brick_albedo(name: str, brick_color: tuple, mortar_color: tuple,
                          brick_w: int = 32, brick_h: int = 16,
                          mortar_size: int = 2, size: int = 256, seed: int = 42):
    """Generate brick pattern albedo."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.1

    for y in range(size):
        for x in range(size):
            # Offset every other row
            row = y // brick_h
            offset = (brick_w // 2) if row % 2 == 1 else 0

            local_x = (x + offset) % brick_w
            local_y = y % brick_h

            # Check if in mortar
            if local_x < mortar_size or local_y < mortar_size:
                img[y, x] = mortar_color
            else:
                # Brick with noise variation
                n = (noise.get_noise(x, y) + 1) / 2
                factor = 0.85 + n * 0.3
                img[y, x] = [
                    int(min(255, brick_color[0] * factor)),
                    int(min(255, brick_color[1] * factor)),
                    int(min(255, brick_color[2] * factor)),
                    255
                ]

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")

generate_brick_albedo("red_brick",
    brick_color=(180, 80, 60, 255),
    mortar_color=(180, 170, 160, 255)
)
```

---

## Color Palettes

Common albedo color palettes:

```python
# Metals (mode 2/3 - needs MRE/SSE)
CHROME = (200, 200, 200, 255)
GOLD = (255, 200, 50, 255)
COPPER = (184, 115, 51, 255)
BRONZE = (205, 127, 50, 255)
RUST = (183, 65, 14, 255)

# Organic
BARK_DARK = (60, 35, 20, 255)
BARK_LIGHT = (139, 90, 43, 255)
LEAF_GREEN = (34, 139, 34, 255)
GRASS = (86, 125, 70, 255)

# Stone
GRANITE = (128, 128, 128, 255)
MARBLE_WHITE = (240, 235, 230, 255)
SANDSTONE = (194, 178, 128, 255)
SLATE = (47, 79, 79, 255)

# Skin tones
SKIN_LIGHT = (255, 224, 189, 255)
SKIN_MEDIUM = (224, 172, 105, 255)
SKIN_DARK = (139, 90, 43, 255)

# Fantasy
CRYSTAL_BLUE = (100, 180, 255, 255)
MAGIC_PURPLE = (147, 112, 219, 255)
LAVA = (255, 100, 0, 255)
```
