# Material Recipes

Complete texture generation recipes for common materials using PIL, NumPy, and FastNoiseLite.

## Brushed Metal

```python
import numpy as np
from PIL import Image
from pyfastnoiselite import FastNoiseLite, NoiseType, FractalType

def generate_brushed_metal(name: str, base_color: tuple = (180, 180, 185, 255),
                           direction: str = 'horizontal', size: int = 256, seed: int = 42):
    """Generate brushed metal albedo with directional grain."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    # Directional noise for brushing
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_Perlin
    noise.frequency = 0.02

    for y in range(size):
        for x in range(size):
            if direction == 'horizontal':
                n = (noise.get_noise(x, y * 0.1) + 1) / 2
            else:  # vertical
                n = (noise.get_noise(x * 0.1, y) + 1) / 2

            factor = 0.85 + n * 0.3
            img[y, x] = [
                int(min(255, base_color[0] * factor)),
                int(min(255, base_color[1] * factor)),
                int(min(255, base_color[2] * factor)),
                255
            ]

    # Add fine grain scratches
    noise2 = FastNoiseLite(seed + 1)
    noise2.noise_type = NoiseType.NoiseType_Perlin
    noise2.frequency = 0.15

    for y in range(size):
        for x in range(size):
            if direction == 'horizontal':
                n = (noise2.get_noise(x * 3, y * 0.05) + 1) / 2
            else:
                n = (noise2.get_noise(x * 0.05, y * 3) + 1) / 2

            if n > 0.7:  # Occasional scratch
                brightness = 1.0 + (n - 0.7) * 0.3
                img[y, x, :3] = np.clip(img[y, x, :3] * brightness, 0, 255).astype(np.uint8)

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")

generate_brushed_metal("brushed_steel")
generate_brushed_metal("brushed_aluminum", base_color=(200, 200, 205, 255))
```

---

## Wood Grain

```python
def generate_wood_grain(name: str, base_color: tuple = (139, 90, 43, 255),
                        dark_color: tuple = (80, 50, 25, 255),
                        ring_scale: float = 0.02, size: int = 256, seed: int = 42):
    """Generate wood grain texture with rings and fiber."""
    img = np.zeros((size, size, 4), dtype=np.float32)
    img[:, :] = [c / 255.0 for c in base_color]

    # Ring pattern
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_Perlin
    noise.frequency = 0.01

    for y in range(size):
        for x in range(size):
            # Distort coordinates for organic feel
            distort = noise.get_noise(x * 0.5, y * 0.5) * 20
            ring_val = np.sin((x + distort) * ring_scale * 2 * np.pi)
            ring_val = (ring_val + 1) / 2  # [0, 1]

            # Dark rings
            ring_intensity = ring_val ** 2 * 0.3
            for c in range(3):
                img[y, x, c] = img[y, x, c] * (1 - ring_intensity) + dark_color[c]/255 * ring_intensity

    # Fine grain/fiber
    noise2 = FastNoiseLite(seed + 1)
    noise2.noise_type = NoiseType.NoiseType_Perlin
    noise2.frequency = 0.15

    for y in range(size):
        for x in range(size):
            n = (noise2.get_noise(x * 0.2, y) + 1) / 2  # Stretched vertically
            img[y, x, :3] *= 0.9 + n * 0.2

    # Knots (occasional dark spots)
    noise3 = FastNoiseLite(seed + 2)
    noise3.noise_type = NoiseType.NoiseType_Cellular
    noise3.frequency = 0.03

    for y in range(size):
        for x in range(size):
            n = (noise3.get_noise(x, y) + 1) / 2
            if n < 0.1:
                factor = 0.5 + n * 5  # Darken knot areas
                img[y, x, :3] *= factor

    result = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(result, 'RGBA').save(f"{name}_albedo.png")

generate_wood_grain("oak")
generate_wood_grain("walnut", base_color=(100, 60, 30, 255), dark_color=(50, 30, 15, 255))
```

---

## Stone / Concrete

```python
def generate_stone(name: str, base_color: tuple = (128, 128, 128, 255),
                   variation: float = 0.25, size: int = 256, seed: int = 42):
    """Generate stone/concrete texture with FBM noise."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    # Multi-octave FBM for organic stone
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.02
    noise.fractal_type = FractalType.FractalType_FBm
    noise.fractal_octaves = 5
    noise.fractal_gain = 0.5

    for y in range(size):
        for x in range(size):
            n = (noise.get_noise(x, y) + 1) / 2
            factor = 1.0 - variation/2 + variation * n

            img[y, x] = [
                int(min(255, base_color[0] * factor)),
                int(min(255, base_color[1] * factor)),
                int(min(255, base_color[2] * factor)),
                255
            ]

    # Add occasional dark pits
    noise2 = FastNoiseLite(seed + 1)
    noise2.noise_type = NoiseType.NoiseType_Cellular
    noise2.frequency = 0.1

    for y in range(size):
        for x in range(size):
            n = (noise2.get_noise(x, y) + 1) / 2
            if n < 0.15:
                factor = 0.6 + n * 2.5
                img[y, x, :3] = (img[y, x, :3] * factor).astype(np.uint8)

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")

generate_stone("granite")
generate_stone("concrete", base_color=(160, 155, 150, 255))
generate_stone("slate", base_color=(70, 75, 80, 255))
```

---

## Rust / Corrosion

```python
def generate_rust(name: str, metal_color: tuple = (100, 100, 105, 255),
                  rust_color: tuple = (140, 60, 20, 255),
                  rust_amount: float = 0.4, size: int = 256, seed: int = 42):
    """Generate rusted metal texture."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    # Base metal
    noise1 = FastNoiseLite(seed)
    noise1.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise1.frequency = 0.04

    # Rust mask
    noise2 = FastNoiseLite(seed + 1)
    noise2.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise2.frequency = 0.03
    noise2.fractal_type = FractalType.FractalType_FBm
    noise2.fractal_octaves = 4

    for y in range(size):
        for x in range(size):
            n1 = (noise1.get_noise(x, y) + 1) / 2
            n2 = (noise2.get_noise(x, y) + 1) / 2

            # Metal base with variation
            metal = [
                metal_color[0] * (0.9 + n1 * 0.2),
                metal_color[1] * (0.9 + n1 * 0.2),
                metal_color[2] * (0.9 + n1 * 0.2)
            ]

            # Rust where noise exceeds threshold
            rust_threshold = 1.0 - rust_amount
            if n2 > rust_threshold:
                rust_blend = (n2 - rust_threshold) / rust_amount
                rust_blend = min(1.0, rust_blend * 1.5)  # Sharp transition

                # Rust color with variation
                rust = [
                    rust_color[0] * (0.8 + n1 * 0.4),
                    rust_color[1] * (0.8 + n1 * 0.4),
                    rust_color[2] * (0.8 + n1 * 0.4)
                ]

                final = [
                    metal[0] * (1 - rust_blend) + rust[0] * rust_blend,
                    metal[1] * (1 - rust_blend) + rust[1] * rust_blend,
                    metal[2] * (1 - rust_blend) + rust[2] * rust_blend
                ]
            else:
                final = metal

            img[y, x] = [int(min(255, c)) for c in final] + [255]

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")

generate_rust("rusty_metal", rust_amount=0.3)
generate_rust("heavily_rusted", rust_amount=0.6)
```

---

## Fabric / Cloth

```python
def generate_fabric(name: str, base_color: tuple = (80, 60, 100, 255),
                    weave_scale: int = 4, size: int = 256, seed: int = 42):
    """Generate fabric texture with weave pattern."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.1

    for y in range(size):
        for x in range(size):
            # Weave pattern
            wx = (x // weave_scale) % 2
            wy = (y // weave_scale) % 2
            weave = 0.95 if (wx + wy) % 2 == 0 else 1.05

            # Thread variation
            thread_x = (x % weave_scale) / weave_scale
            thread_y = (y % weave_scale) / weave_scale
            thread = 0.95 + 0.1 * np.sin(thread_x * np.pi) * np.sin(thread_y * np.pi)

            # Random variation
            n = (noise.get_noise(x, y) + 1) / 2
            variation = 0.9 + n * 0.2

            factor = weave * thread * variation

            img[y, x] = [
                int(min(255, base_color[0] * factor)),
                int(min(255, base_color[1] * factor)),
                int(min(255, base_color[2] * factor)),
                255
            ]

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")

generate_fabric("purple_cloth")
generate_fabric("burlap", base_color=(180, 160, 120, 255), weave_scale=8)
```

---

## Leather

```python
def generate_leather(name: str, base_color: tuple = (100, 60, 40, 255),
                     size: int = 256, seed: int = 42):
    """Generate leather texture with pores and creases."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    # Base variation
    noise1 = FastNoiseLite(seed)
    noise1.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise1.frequency = 0.03

    # Pores (cellular)
    noise2 = FastNoiseLite(seed + 1)
    noise2.noise_type = NoiseType.NoiseType_Cellular
    noise2.frequency = 0.15

    # Creases
    noise3 = FastNoiseLite(seed + 2)
    noise3.noise_type = NoiseType.NoiseType_Cellular
    noise3.frequency = 0.05

    for y in range(size):
        for x in range(size):
            n1 = (noise1.get_noise(x, y) + 1) / 2
            n2 = (noise2.get_noise(x, y) + 1) / 2
            n3 = (noise3.get_noise(x, y) + 1) / 2

            # Base with variation
            factor = 0.85 + n1 * 0.3

            # Pores darken
            if n2 < 0.2:
                factor *= 0.7 + n2 * 1.5

            # Creases at cell edges
            if n3 < 0.1:
                factor *= 0.6 + n3 * 4

            img[y, x] = [
                int(min(255, base_color[0] * factor)),
                int(min(255, base_color[1] * factor)),
                int(min(255, base_color[2] * factor)),
                255
            ]

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")

generate_leather("brown_leather")
generate_leather("black_leather", base_color=(40, 35, 35, 255))
```

---

## Brick

```python
def generate_brick(name: str, brick_color: tuple = (180, 80, 60, 255),
                   mortar_color: tuple = (180, 170, 160, 255),
                   brick_w: int = 32, brick_h: int = 16,
                   mortar_size: int = 2, size: int = 256, seed: int = 42):
    """Generate brick wall texture."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    # Noise for brick variation
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.08

    # Noise for mortar variation
    noise2 = FastNoiseLite(seed + 1)
    noise2.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise2.frequency = 0.15

    for y in range(size):
        for x in range(size):
            row = y // brick_h
            offset = (brick_w // 2) if row % 2 == 1 else 0

            local_x = (x + offset) % brick_w
            local_y = y % brick_h

            if local_x < mortar_size or local_y < mortar_size:
                # Mortar
                n = (noise2.get_noise(x, y) + 1) / 2
                factor = 0.9 + n * 0.2
                img[y, x] = [
                    int(min(255, mortar_color[0] * factor)),
                    int(min(255, mortar_color[1] * factor)),
                    int(min(255, mortar_color[2] * factor)),
                    255
                ]
            else:
                # Brick
                n = (noise.get_noise(x, y) + 1) / 2
                factor = 0.8 + n * 0.4
                img[y, x] = [
                    int(min(255, brick_color[0] * factor)),
                    int(min(255, brick_color[1] * factor)),
                    int(min(255, brick_color[2] * factor)),
                    255
                ]

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")

generate_brick("red_brick")
generate_brick("old_brick", brick_color=(150, 90, 70, 255))
```

---

## Scales / Dragon Skin

```python
def generate_scales(name: str, base_color: tuple = (40, 80, 60, 255),
                    highlight_color: tuple = (80, 140, 100, 255),
                    size: int = 256, seed: int = 42):
    """Generate scale/reptile skin pattern."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    # Cellular noise for scale pattern
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_Cellular
    noise.frequency = 0.08
    noise.cellular_return_type = noise.CellularReturnType.CellularReturnType_Distance

    for y in range(size):
        for x in range(size):
            n = (noise.get_noise(x, y) + 1) / 2

            # Center of cell = highlight, edge = base
            for c in range(3):
                img[y, x, c] = int(base_color[c] * (1 - n) + highlight_color[c] * n)
            img[y, x, 3] = 255

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")

generate_scales("green_scales")
generate_scales("dragon_scales", base_color=(80, 30, 30, 255), highlight_color=(150, 80, 60, 255))
```
