# Normal Map Pattern Generators

Python functions for generating common normal map patterns from height maps.

## Height to Normal Conversion

```python
import numpy as np
from PIL import Image

def height_to_normal(height_map: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """Convert grayscale height map to tangent-space normal map.

    Args:
        height_map: 2D float array [0, 1] where 1 = high, 0 = low
        strength: Normal intensity (0.5 = subtle, 2.0 = dramatic)

    Returns:
        3D uint8 array (H, W, 3) ready to save as PNG
    """
    # Calculate gradients using Sobel-like finite differences
    # Roll gives us seamless wrapping at edges
    dx = np.roll(height_map, -1, axis=1) - np.roll(height_map, 1, axis=1)
    dy = np.roll(height_map, -1, axis=0) - np.roll(height_map, 1, axis=0)

    # Scale by strength
    dx *= strength
    dy *= strength

    # Build normal vectors (dx points right, dy points down)
    normal = np.zeros((*height_map.shape, 3), dtype=np.float32)
    normal[:, :, 0] = -dx  # X (tangent direction)
    normal[:, :, 1] = -dy  # Y (bitangent direction)
    normal[:, :, 2] = 1.0  # Z (surface normal)

    # Normalize to unit vectors
    length = np.sqrt(np.sum(normal ** 2, axis=2, keepdims=True))
    length = np.maximum(length, 1e-8)  # Avoid division by zero
    normal /= length

    # Convert [-1, 1] -> [0, 255]
    return ((normal + 1.0) * 0.5 * 255).astype(np.uint8)


def generate_normal_from_height(height_path: str, output_path: str, strength: float = 1.0):
    """Generate normal map from grayscale height image."""
    img = Image.open(height_path).convert('L')
    height = np.array(img, dtype=np.float32) / 255.0
    normal = height_to_normal(height, strength)
    Image.fromarray(normal, 'RGB').save(output_path)
```

## Brick Pattern

```python
def generate_brick_normals(width: int, height: int,
                           brick_w: int = 32, brick_h: int = 16,
                           mortar_depth: float = 0.3) -> np.ndarray:
    """Generate brick pattern normal map."""
    heightmap = np.ones((height, width), dtype=np.float32)

    mortar_size = 2
    for y in range(height):
        for x in range(width):
            # Offset every other row
            row = y // brick_h
            offset = (brick_w // 2) if row % 2 == 1 else 0

            # Mortar lines
            local_x = (x + offset) % brick_w
            local_y = y % brick_h

            if local_x < mortar_size or local_y < mortar_size:
                heightmap[y, x] = 1.0 - mortar_depth

    return height_to_normal(heightmap, strength=1.0)
```

## Tile Pattern

```python
def generate_tile_normals(width: int, height: int,
                          tile_size: int = 64,
                          gap_depth: float = 0.4) -> np.ndarray:
    """Generate square tile floor normal map."""
    heightmap = np.ones((height, width), dtype=np.float32)

    gap = 2
    for y in range(height):
        for x in range(width):
            local_x = x % tile_size
            local_y = y % tile_size

            if local_x < gap or local_y < gap:
                heightmap[y, x] = 1.0 - gap_depth

    return height_to_normal(heightmap, strength=1.2)
```

## Noise-Based Detail

```python
from pyfastnoiselite import FastNoiseLite, NoiseType

def generate_noise_normals(width: int, height: int,
                           scale: float = 0.05,
                           strength: float = 0.5) -> np.ndarray:
    """Generate noise-based surface detail normal map."""
    noise = FastNoiseLite()
    noise.noise_type = NoiseType.NoiseType_Perlin

    heightmap = np.zeros((height, width), dtype=np.float32)
    for y in range(height):
        for x in range(width):
            heightmap[y, x] = (noise.get_noise(x * scale, y * scale) + 1.0) * 0.5

    return height_to_normal(heightmap, strength=strength)
```

## Metal Scratches

```python
import random

def generate_scratch_normals(width: int, height: int,
                             num_scratches: int = 20,
                             depth: float = 0.1) -> np.ndarray:
    """Generate directional scratch pattern normal map."""
    heightmap = np.ones((height, width), dtype=np.float32)

    for _ in range(num_scratches):
        # Random horizontal scratch
        y = random.randint(0, height - 1)
        length = random.randint(width // 4, width)
        x_start = random.randint(0, width - length)

        for x in range(x_start, x_start + length):
            heightmap[y, x] = 1.0 - depth
            # Slight blur above/below
            if y > 0:
                heightmap[y-1, x] = min(heightmap[y-1, x], 1.0 - depth * 0.5)
            if y < height - 1:
                heightmap[y+1, x] = min(heightmap[y+1, x], 1.0 - depth * 0.5)

    return height_to_normal(heightmap, strength=2.0)
```

## Rivet Pattern

```python
def generate_rivet_normals(width: int, height: int,
                           spacing: int = 32,
                           radius: int = 4,
                           rivet_height: float = 0.3) -> np.ndarray:
    """Generate raised rivet pattern normal map."""
    heightmap = np.zeros((height, width), dtype=np.float32)

    for cy in range(spacing // 2, height, spacing):
        for cx in range(spacing // 2, width, spacing):
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    dist = (dx * dx + dy * dy) ** 0.5
                    if dist <= radius:
                        y = (cy + dy) % height
                        x = (cx + dx) % width
                        # Smooth falloff
                        falloff = 1.0 - (dist / radius)
                        heightmap[y, x] = max(heightmap[y, x], rivet_height * falloff)

    return height_to_normal(heightmap, strength=1.5)
```

## Fabric Weave

```python
def generate_weave_normals(width: int, height: int,
                           thread_width: int = 4,
                           gap: int = 1) -> np.ndarray:
    """Generate woven fabric pattern normal map."""
    heightmap = np.zeros((height, width), dtype=np.float32)

    period = thread_width + gap

    for y in range(height):
        for x in range(width):
            local_x = x % period
            local_y = y % period

            # Horizontal thread
            if local_y < thread_width:
                h_val = 0.6
            else:
                h_val = 0.0

            # Vertical thread
            if local_x < thread_width:
                v_val = 0.6
            else:
                v_val = 0.0

            # Weave pattern (over/under)
            cell_x = x // period
            cell_y = y // period
            if (cell_x + cell_y) % 2 == 0:
                heightmap[y, x] = max(h_val, v_val * 0.8)
            else:
                heightmap[y, x] = max(v_val, h_val * 0.8)

    return height_to_normal(heightmap, strength=0.8)
```

## Combined Patterns

```python
def combine_normals(base: np.ndarray, detail: np.ndarray,
                    detail_strength: float = 0.3) -> np.ndarray:
    """Blend two normal maps together."""
    # Convert back to [-1, 1]
    base_n = (base.astype(np.float32) / 255.0) * 2.0 - 1.0
    detail_n = (detail.astype(np.float32) / 255.0) * 2.0 - 1.0

    # Blend XY, reconstruct Z
    result = np.zeros_like(base_n)
    result[:, :, 0] = base_n[:, :, 0] + detail_n[:, :, 0] * detail_strength
    result[:, :, 1] = base_n[:, :, 1] + detail_n[:, :, 1] * detail_strength
    result[:, :, 2] = 1.0  # Will be normalized

    # Normalize
    length = np.sqrt(np.sum(result ** 2, axis=2, keepdims=True))
    length = np.maximum(length, 1e-8)
    result /= length

    return ((result + 1.0) * 0.5 * 255).astype(np.uint8)
```
