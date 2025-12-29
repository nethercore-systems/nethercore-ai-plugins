# Seamless/Tileable Textures

Techniques for creating textures that tile without visible seams.

## Method 1: 4D Noise Sampling

The most robust method. Sample 4D noise using circular coordinates that wrap around.

```python
import numpy as np
from PIL import Image
from pyfastnoiselite import FastNoiseLite, NoiseType, FractalType
import math

def generate_tileable_noise(width: int, height: int, scale: float = 1.0,
                            noise_type: str = 'perlin', seed: int = 42) -> np.ndarray:
    """Generate seamlessly tileable noise texture using 4D sampling."""
    noise = FastNoiseLite(seed)
    noise.frequency = 1.0  # Scale handled in coordinates

    if noise_type == 'perlin':
        noise.noise_type = NoiseType.NoiseType_Perlin
    elif noise_type == 'simplex':
        noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    elif noise_type == 'value':
        noise.noise_type = NoiseType.NoiseType_Value

    data = np.zeros((height, width, 4), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            # Map 2D coordinates to 4D torus
            s = x / width
            t = y / height

            # Circular coordinates in 4D
            nx = math.cos(s * 2 * math.pi) * scale
            ny = math.sin(s * 2 * math.pi) * scale
            nz = math.cos(t * 2 * math.pi) * scale
            nw = math.sin(t * 2 * math.pi) * scale

            # Sample 4D noise (tiles seamlessly in 2D)
            val = (noise.get_noise_4d(nx, ny, nz, nw) + 1) / 2
            gray = int(val * 255)
            data[y, x] = (gray, gray, gray, 255)

    return data


def generate_tileable_albedo(name: str, base_color: tuple, scale: float = 1.0,
                             variation: float = 0.2, size: int = 256, seed: int = 42):
    """Generate tileable albedo texture."""
    noise_data = generate_tileable_noise(size, size, scale, 'perlin', seed)

    img = np.zeros((size, size, 4), dtype=np.uint8)

    for y in range(size):
        for x in range(size):
            n = noise_data[y, x, 0] / 255.0  # [0, 1]
            factor = 1.0 - variation/2 + variation * n

            img[y, x] = [
                int(min(255, base_color[0] * factor)),
                int(min(255, base_color[1] * factor)),
                int(min(255, base_color[2] * factor)),
                255
            ]

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")


# Examples
generate_tileable_albedo("tile_stone", (128, 128, 128, 255), scale=2.0)
generate_tileable_albedo("tile_sand", (194, 178, 128, 255), scale=1.5)
```

---

## Method 2: Edge Blending

Blend texture edges with mirrored versions to create seams.

```python
def make_tileable_blend(input_path: str, output_path: str, blend_width: int = 32):
    """Make an existing texture tileable by blending edges."""
    img = Image.open(input_path).convert('RGBA')
    data = np.array(img).astype(np.float32)
    height, width = data.shape[:2]

    result = data.copy()

    # Blend left-right edges
    for x in range(blend_width):
        alpha = x / blend_width
        for y in range(height):
            # Left edge: blend with right side
            result[y, x] = data[y, x] * alpha + data[y, width - blend_width + x] * (1 - alpha)
            # Right edge: blend with left side
            result[y, width - blend_width + x] = data[y, width - blend_width + x] * alpha + data[y, x] * (1 - alpha)

    # Blend top-bottom edges
    for y in range(blend_width):
        alpha = y / blend_width
        for x in range(width):
            # Top edge: blend with bottom side
            result[y, x] = result[y, x] * alpha + result[height - blend_width + y, x] * (1 - alpha)
            # Bottom edge: blend with top side
            result[height - blend_width + y, x] = result[height - blend_width + y, x] * alpha + result[y, x] * (1 - alpha)

    Image.fromarray(result.astype(np.uint8), 'RGBA').save(output_path)


# Usage
make_tileable_blend("non_tileable.png", "tileable.png", blend_width=64)
```

---

## Method 3: Mirrored Quadrant

Create a quarter texture and mirror it to create perfect tiling.

```python
def generate_mirrored_tileable(name: str, base_color: tuple,
                               size: int = 256, seed: int = 42):
    """Generate tileable texture using mirrored quadrants."""
    half = size // 2
    quarter = np.zeros((half, half, 4), dtype=np.uint8)

    # Generate one quarter
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.04
    noise.fractal_type = FractalType.FractalType_FBm
    noise.fractal_octaves = 4

    for y in range(half):
        for x in range(half):
            n = (noise.get_noise(x, y) + 1) / 2
            factor = 0.85 + n * 0.3

            quarter[y, x] = [
                int(min(255, base_color[0] * factor)),
                int(min(255, base_color[1] * factor)),
                int(min(255, base_color[2] * factor)),
                255
            ]

    # Mirror to create full texture
    full = np.zeros((size, size, 4), dtype=np.uint8)

    # Top-left: original
    full[:half, :half] = quarter
    # Top-right: horizontal flip
    full[:half, half:] = np.flip(quarter, axis=1)
    # Bottom-left: vertical flip
    full[half:, :half] = np.flip(quarter, axis=0)
    # Bottom-right: both flips
    full[half:, half:] = np.flip(np.flip(quarter, axis=0), axis=1)

    Image.fromarray(full, 'RGBA').save(f"{name}_albedo.png")


generate_mirrored_tileable("mirror_tile", (100, 80, 60, 255))
```

**Note:** This method creates obvious symmetry. Best for abstract patterns or as a base for further processing.

---

## Tileable FBM with 4D Sampling

```python
def generate_tileable_fbm(name: str, base_color: tuple, dark_color: tuple,
                          scale: float = 2.0, octaves: int = 4,
                          size: int = 256, seed: int = 42):
    """Generate tileable FBM texture."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_Perlin
    noise.frequency = 1.0
    noise.fractal_type = FractalType.FractalType_FBm
    noise.fractal_octaves = octaves
    noise.fractal_gain = 0.5

    for y in range(size):
        for x in range(size):
            s = x / size
            t = y / size

            # 4D torus sampling
            nx = math.cos(s * 2 * math.pi) * scale
            ny = math.sin(s * 2 * math.pi) * scale
            nz = math.cos(t * 2 * math.pi) * scale
            nw = math.sin(t * 2 * math.pi) * scale

            val = (noise.get_noise_4d(nx, ny, nz, nw) + 1) / 2

            # Interpolate colors
            for c in range(3):
                img[y, x, c] = int(dark_color[c] * (1 - val) + base_color[c] * val)
            img[y, x, 3] = 255

    Image.fromarray(img, 'RGBA').save(f"{name}_albedo.png")


generate_tileable_fbm("tile_rock",
    base_color=(150, 145, 140, 255),
    dark_color=(80, 75, 70, 255)
)
```

---

## Tileable Material Example

```python
def generate_tileable_mode2_material(name: str, albedo_color: tuple,
                                     metallic: float, roughness: float,
                                     scale: float = 2.0, size: int = 256, seed: int = 42):
    """Generate complete tileable Mode 2 material."""
    # Tileable albedo
    albedo = np.zeros((size, size, 4), dtype=np.uint8)

    noise1 = FastNoiseLite(seed)
    noise1.noise_type = NoiseType.NoiseType_Perlin
    noise1.frequency = 1.0

    for y in range(size):
        for x in range(size):
            s, t = x / size, y / size
            nx = math.cos(s * 2 * math.pi) * scale
            ny = math.sin(s * 2 * math.pi) * scale
            nz = math.cos(t * 2 * math.pi) * scale
            nw = math.sin(t * 2 * math.pi) * scale

            n = (noise1.get_noise_4d(nx, ny, nz, nw) + 1) / 2
            factor = 0.85 + n * 0.3

            albedo[y, x] = [
                int(min(255, albedo_color[0] * factor)),
                int(min(255, albedo_color[1] * factor)),
                int(min(255, albedo_color[2] * factor)),
                255
            ]

    Image.fromarray(albedo, 'RGBA').save(f"{name}_albedo.png")

    # Tileable MRE
    mre = np.zeros((size, size, 4), dtype=np.uint8)

    noise2 = FastNoiseLite(seed + 1)
    noise2.noise_type = NoiseType.NoiseType_Perlin
    noise2.frequency = 1.0

    for y in range(size):
        for x in range(size):
            s, t = x / size, y / size
            nx = math.cos(s * 2 * math.pi) * scale
            ny = math.sin(s * 2 * math.pi) * scale
            nz = math.cos(t * 2 * math.pi) * scale
            nw = math.sin(t * 2 * math.pi) * scale

            n = (noise2.get_noise_4d(nx, ny, nz, nw) + 1) / 2
            r_varied = roughness + (n - 0.5) * 0.2

            mre[y, x] = [
                int(metallic * 255),
                int(max(0, min(1, r_varied)) * 255),
                0,
                255
            ]

    Image.fromarray(mre, 'RGBA').save(f"{name}_mre.png")


generate_tileable_mode2_material("tile_metal",
    albedo_color=(180, 180, 185, 255),
    metallic=1.0,
    roughness=0.4
)
```

---

## Testing Tileability

```python
def test_tileable(texture_path: str, output_path: str, tiles: int = 3):
    """Create a tiled preview to verify seamlessness."""
    img = Image.open(texture_path).convert('RGBA')
    width, height = img.size

    preview = Image.new('RGBA', (width * tiles, height * tiles))

    for ty in range(tiles):
        for tx in range(tiles):
            preview.paste(img, (tx * width, ty * height))

    preview.save(output_path)


# Test your tileable texture
test_tileable("tile_stone_albedo.png", "tile_stone_preview.png")
```

---

## Scale Guidelines

| Scale | Feature Size | Use For |
|-------|--------------|---------|
| 0.5 | Very large | Distant terrain, sky |
| 1.0 | Large | Ground textures |
| 2.0 | Medium | Standard materials |
| 3.0-4.0 | Small | Detailed surfaces |
| 5.0+ | Fine | Close-up detail |

**Tip:** Use higher octave counts with larger scales for more detail.
