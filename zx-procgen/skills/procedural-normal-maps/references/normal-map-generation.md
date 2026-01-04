# Normal Map Generation Techniques

Detailed algorithms and patterns for procedural normal map generation.

## Height-to-Normal Algorithm

### Sobel Filter Method

The standard approach uses Sobel-like gradients for accurate edge detection:

```python
import numpy as np
from PIL import Image

def height_to_normal_sobel(height_map: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """Convert height map to normal map using Sobel gradient estimation.

    The Sobel operator provides better gradient estimation than simple
    finite differences, especially for noisy height maps.

    Args:
        height_map: 2D float array [0, 1]
        strength: Normal intensity multiplier

    Returns:
        3D uint8 array (H, W, 3)
    """
    # Sobel kernels
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]], dtype=np.float32) / 8.0

    sobel_y = np.array([[-1, -2, -1],
                        [ 0,  0,  0],
                        [ 1,  2,  1]], dtype=np.float32) / 8.0

    from scipy.ndimage import convolve

    # Compute gradients (using wrap mode for seamless)
    dx = convolve(height_map, sobel_x, mode='wrap') * strength
    dy = convolve(height_map, sobel_y, mode='wrap') * strength

    # Build normals
    normal = np.zeros((*height_map.shape, 3), dtype=np.float32)
    normal[:, :, 0] = -dx
    normal[:, :, 1] = -dy
    normal[:, :, 2] = 1.0

    # Normalize
    length = np.sqrt(np.sum(normal ** 2, axis=2, keepdims=True))
    normal /= np.maximum(length, 1e-8)

    # Convert to [0, 255]
    return ((normal + 1.0) * 0.5 * 255).astype(np.uint8)
```

### Simple Finite Differences

For performance when Sobel isn't needed:

```python
def height_to_normal_simple(height_map: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """Fast height-to-normal using simple finite differences.

    Less accurate than Sobel but faster for real-time or batch processing.
    """
    # Central differences with wraparound
    dx = np.roll(height_map, -1, axis=1) - np.roll(height_map, 1, axis=1)
    dy = np.roll(height_map, -1, axis=0) - np.roll(height_map, 1, axis=0)

    dx *= strength * 0.5  # 0.5 because we span 2 pixels
    dy *= strength * 0.5

    normal = np.zeros((*height_map.shape, 3), dtype=np.float32)
    normal[:, :, 0] = -dx
    normal[:, :, 1] = -dy
    normal[:, :, 2] = 1.0

    length = np.sqrt(np.sum(normal ** 2, axis=2, keepdims=True))
    normal /= np.maximum(length, 1e-8)

    return ((normal + 1.0) * 0.5 * 255).astype(np.uint8)
```

---

## Seamless Normal Maps

For tileable textures, use 4D torus mapping:

```python
from pyfastnoiselite import FastNoiseLite, NoiseType
import numpy as np

def generate_seamless_height(width: int, height: int,
                              scale: float = 1.0,
                              seed: int = 42) -> np.ndarray:
    """Generate seamless tileable height map using 4D torus mapping.

    Maps 2D coordinates to a 4D torus to ensure seamless wraparound
    in both X and Y directions.
    """
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_Perlin

    heightmap = np.zeros((height, width), dtype=np.float32)

    for y in range(height):
        for x in range(width):
            # Map to [0, 2π]
            s = x / width * 2 * np.pi
            t = y / height * 2 * np.pi

            # 4D torus coordinates
            nx = np.cos(s) * scale
            ny = np.sin(s) * scale
            nz = np.cos(t) * scale
            nw = np.sin(t) * scale

            # Sample 4D noise
            value = noise.get_noise(nx * 10, ny * 10, nz * 10, nw * 10)
            heightmap[y, x] = (value + 1.0) * 0.5

    return heightmap


def generate_seamless_normal(width: int, height: int,
                              scale: float = 1.0,
                              strength: float = 1.0,
                              seed: int = 42) -> np.ndarray:
    """Generate seamless normal map from 4D noise."""
    heightmap = generate_seamless_height(width, height, scale, seed)
    return height_to_normal_simple(heightmap, strength)
```

---

## Procedural Patterns

### Brick/Tile Pattern

```python
def generate_brick_height(width: int, height: int,
                          brick_w: int = 32, brick_h: int = 16,
                          mortar_width: int = 2,
                          mortar_depth: float = 0.3,
                          brick_roughness: float = 0.05) -> np.ndarray:
    """Generate brick pattern height map with mortar lines.

    Args:
        brick_w, brick_h: Brick dimensions in pixels
        mortar_width: Width of mortar lines
        mortar_depth: Depth of mortar (0 = flush, 1 = deep)
        brick_roughness: Random variation on brick surfaces
    """
    import random

    heightmap = np.ones((height, width), dtype=np.float32)
    noise = np.random.rand(height, width) * brick_roughness

    for y in range(height):
        row = y // brick_h
        offset = (brick_w // 2) if row % 2 == 1 else 0

        for x in range(width):
            local_x = (x + offset) % brick_w
            local_y = y % brick_h

            # Mortar lines
            if local_x < mortar_width or local_y < mortar_width:
                heightmap[y, x] = 1.0 - mortar_depth
            else:
                # Add brick surface variation
                heightmap[y, x] = 1.0 - noise[y, x]

    return heightmap
```

### Fabric Weave

```python
def generate_weave_height(width: int, height: int,
                          thread_size: int = 4,
                          weave_depth: float = 0.1) -> np.ndarray:
    """Generate fabric weave pattern height map.

    Creates a simple over/under weave pattern typical of canvas or linen.
    """
    heightmap = np.ones((height, width), dtype=np.float32) * 0.5

    for y in range(height):
        for x in range(width):
            # Determine weave cell
            cell_x = x // thread_size
            cell_y = y // thread_size

            # Alternate over/under pattern
            if (cell_x + cell_y) % 2 == 0:
                # Horizontal thread on top
                if (y % thread_size) < thread_size // 2:
                    heightmap[y, x] = 0.5 + weave_depth
                else:
                    heightmap[y, x] = 0.5 - weave_depth
            else:
                # Vertical thread on top
                if (x % thread_size) < thread_size // 2:
                    heightmap[y, x] = 0.5 + weave_depth
                else:
                    heightmap[y, x] = 0.5 - weave_depth

    return heightmap
```

### Cellular/Voronoi

```python
from pyfastnoiselite import FastNoiseLite, NoiseType, CellularDistanceFunction

def generate_cellular_height(width: int, height: int,
                              cell_scale: float = 0.02,
                              seed: int = 42) -> np.ndarray:
    """Generate cellular/Voronoi pattern height map.

    Good for scales, tiles, cracked surfaces, or organic cells.
    """
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_Cellular
    noise.cellular_distance_function = CellularDistanceFunction.CellularDistanceFunction_Euclidean

    heightmap = np.zeros((height, width), dtype=np.float32)

    for y in range(height):
        for x in range(width):
            value = noise.get_noise(x * cell_scale, y * cell_scale)
            heightmap[y, x] = (value + 1.0) * 0.5

    return heightmap
```

### Directional Scratches

```python
def generate_scratch_height(width: int, height: int,
                            num_scratches: int = 30,
                            scratch_depth: float = 0.15,
                            direction: str = 'horizontal') -> np.ndarray:
    """Generate directional scratch pattern height map.

    Args:
        direction: 'horizontal', 'vertical', or 'diagonal'
    """
    import random

    heightmap = np.ones((height, width), dtype=np.float32)

    for _ in range(num_scratches):
        if direction == 'horizontal':
            y = random.randint(0, height - 1)
            x_start = random.randint(0, width // 2)
            x_end = random.randint(x_start + 10, width)

            for x in range(x_start, min(x_end, width)):
                # Scratch with soft edges
                heightmap[y, x] = 1.0 - scratch_depth
                if y > 0:
                    heightmap[y-1, x] = min(heightmap[y-1, x], 1.0 - scratch_depth * 0.3)
                if y < height - 1:
                    heightmap[y+1, x] = min(heightmap[y+1, x], 1.0 - scratch_depth * 0.3)

        elif direction == 'vertical':
            x = random.randint(0, width - 1)
            y_start = random.randint(0, height // 2)
            y_end = random.randint(y_start + 10, height)

            for y in range(y_start, min(y_end, height)):
                heightmap[y, x] = 1.0 - scratch_depth
                if x > 0:
                    heightmap[y, x-1] = min(heightmap[y, x-1], 1.0 - scratch_depth * 0.3)
                if x < width - 1:
                    heightmap[y, x+1] = min(heightmap[y, x+1], 1.0 - scratch_depth * 0.3)

        else:  # diagonal
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            length = random.randint(20, 60)
            dx = random.choice([-1, 1])

            for i in range(length):
                px = x + i * dx
                py = y + i
                if 0 <= px < width and 0 <= py < height:
                    heightmap[py, px] = 1.0 - scratch_depth

    return heightmap
```

---

## Detail Layering

Combine multiple patterns for realistic surfaces:

```python
def blend_heightmaps(base: np.ndarray, detail: np.ndarray,
                     blend: float = 0.5) -> np.ndarray:
    """Blend two height maps together.

    Args:
        base: Base height map
        detail: Detail height map to add
        blend: Blend factor (0 = base only, 1 = detail only)
    """
    return base * (1 - blend) + detail * blend


def generate_worn_metal_height(width: int, height: int) -> np.ndarray:
    """Generate worn metal surface with scratches and pitting."""
    # Base: smooth metal
    base = np.ones((height, width), dtype=np.float32) * 0.8

    # Layer 1: Fine grain
    grain = generate_seamless_height(width, height, scale=0.1, seed=1)
    surface = blend_heightmaps(base, grain, 0.1)

    # Layer 2: Scratches
    scratches = generate_scratch_height(width, height, num_scratches=15, direction='horizontal')
    surface = blend_heightmaps(surface, scratches, 0.3)

    # Layer 3: Random pitting
    pits = generate_cellular_height(width, height, cell_scale=0.05, seed=2)
    surface = blend_heightmaps(surface, pits, 0.15)

    return surface
```

---

## Output Considerations

### Two-Channel Output

For optimal BC5 compression, output only RG channels:

```python
def save_normal_rg(normal_rgb: np.ndarray, output_path: str):
    """Save normal map as 2-channel (RG) PNG for BC5 compression.

    Z channel is reconstructed in shader, so we only store X and Y.
    """
    # Extract RG channels only
    rg = normal_rgb[:, :, :2]

    # Save as RGB (BC5 expects RG, B channel ignored)
    # Using LA (luminance + alpha) mode for true 2-channel
    from PIL import Image
    img = Image.fromarray(rg[:, :, 0], 'L')
    alpha = Image.fromarray(rg[:, :, 1], 'L')

    # Combine as LA
    la_img = Image.merge('LA', (img, alpha))
    la_img.save(output_path)
```

### Standard 3-Channel Output

The simpler approach - nether-cli auto-detects and compresses:

```python
def save_normal_rgb(normal_rgb: np.ndarray, output_path: str):
    """Save normal map as 3-channel RGB PNG.

    nether-cli will auto-detect *_normal.png naming and compress to BC5.
    """
    from PIL import Image
    Image.fromarray(normal_rgb, 'RGB').save(output_path)
```

**Recommendation:** Use 3-channel RGB with `*_normal.png` naming. The asset pipeline handles BC5 conversion automatically.
