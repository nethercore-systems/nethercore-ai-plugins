# Noise Algorithms Reference (FastNoiseLite)

FastNoiseLite provides high-quality, consistent noise across all algorithms.

## Setup

```python
from pyfastnoiselite import FastNoiseLite, NoiseType, FractalType, CellularDistanceFunction, CellularReturnType
```

## Noise Types

### Perlin Noise

Classic gradient noise for organic surfaces.

```python
def create_perlin(seed: int = 42, scale: float = 0.05) -> FastNoiseLite:
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_Perlin
    noise.frequency = scale
    return noise

# Usage
noise = create_perlin(42, 0.05)
value = noise.get_noise(x, y)  # Returns [-1, 1]
```

| Scale | Effect |
|-------|--------|
| 0.01 | Very large features |
| 0.03 | Large features |
| 0.05 | Medium features |
| 0.1 | Small features |
| 0.2 | Fine detail |

**Best for:** Clouds, water, organic materials, terrain height

---

### Simplex Noise (OpenSimplex2)

Faster than Perlin, fewer directional artifacts.

```python
def create_simplex(seed: int = 42, scale: float = 0.05) -> FastNoiseLite:
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = scale
    return noise
```

**Best for:** Same as Perlin, preferred for real-time or when speed matters

---

### Cellular Noise (Voronoi)

Cell-like patterns. FastNoiseLite provides multiple return types.

```python
def create_cellular(seed: int = 42, scale: float = 0.1,
                    return_type: CellularReturnType = CellularReturnType.CellularReturnType_Distance) -> FastNoiseLite:
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_Cellular
    noise.frequency = scale
    noise.cellular_return_type = return_type
    noise.cellular_distance_function = CellularDistanceFunction.CellularDistanceFunction_EuclideanSq
    return noise
```

**Cellular Return Types:**

| Type | Effect |
|------|--------|
| `CellularReturnType_CellValue` | Random value per cell (flat regions) |
| `CellularReturnType_Distance` | Distance to nearest cell center |
| `CellularReturnType_Distance2` | Distance to 2nd nearest cell |
| `CellularReturnType_Distance2Add` | Sum of D1 + D2 |
| `CellularReturnType_Distance2Sub` | D2 - D1 (edges/cracks) |
| `CellularReturnType_Distance2Mul` | D1 * D2 |
| `CellularReturnType_Distance2Div` | D1 / D2 |

**Best for:** Scales, crystals, cracks, organic cells, leather, cobblestone

---

### Value Noise

Hard-edged, blocky noise.

```python
def create_value(seed: int = 42, scale: float = 0.05) -> FastNoiseLite:
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_Value
    noise.frequency = scale
    return noise
```

**Best for:** Pixelated effects, rough surfaces, deliberate blockiness

---

### Value Cubic

Smoother version of Value noise.

```python
def create_value_cubic(seed: int = 42, scale: float = 0.05) -> FastNoiseLite:
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_ValueCubic
    noise.frequency = scale
    return noise
```

---

## Fractal Noise (FBM)

Layer multiple noise octaves for complex detail.

```python
def create_fbm(seed: int = 42, scale: float = 0.03,
               octaves: int = 4, persistence: float = 0.5,
               lacunarity: float = 2.0) -> FastNoiseLite:
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_Perlin  # Base noise type
    noise.frequency = scale
    noise.fractal_type = FractalType.FractalType_FBm
    noise.fractal_octaves = octaves
    noise.fractal_gain = persistence  # Amplitude multiplier per octave
    noise.fractal_lacunarity = lacunarity  # Frequency multiplier per octave
    return noise
```

**Fractal Types:**

| Type | Effect |
|------|--------|
| `FractalType_None` | No fractal (single layer) |
| `FractalType_FBm` | Standard layered noise |
| `FractalType_Ridged` | Inverted, sharp ridges |
| `FractalType_PingPong` | Ping-pong effect for terraced look |

**Octave Effects:**

| Octaves | Result |
|---------|--------|
| 1 | Smooth, simple |
| 2-3 | Basic detail |
| 4-6 | Rich complexity |
| 7-8 | Maximum detail |

---

## Domain Warp

Distort coordinates for more organic shapes.

```python
def create_warped_noise(seed: int = 42) -> FastNoiseLite:
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.02

    # Enable domain warp
    noise.domain_warp_type = FastNoiseLite.DomainWarpType.DomainWarpType_OpenSimplex2
    noise.domain_warp_amp = 50.0  # Warp strength
    noise.domain_warp_frequency = 0.01
    return noise

# Usage with warp
x_warped, y_warped = noise.domain_warp(x, y)
value = noise.get_noise(x_warped, y_warped)
```

---

## Complete Texture Generation

```python
import numpy as np
from pyfastnoiselite import FastNoiseLite, NoiseType, FractalType

def generate_noise_texture(width: int, height: int, noise_type: str = 'perlin',
                           scale: float = 0.05, seed: int = 42,
                           color_low: tuple = (0, 0, 0, 255),
                           color_high: tuple = (255, 255, 255, 255)) -> np.ndarray:
    """Generate a noise texture with color mapping."""

    noise = FastNoiseLite(seed)
    noise.frequency = scale

    if noise_type == 'perlin':
        noise.noise_type = NoiseType.NoiseType_Perlin
    elif noise_type == 'simplex':
        noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    elif noise_type == 'cellular':
        noise.noise_type = NoiseType.NoiseType_Cellular
    elif noise_type == 'value':
        noise.noise_type = NoiseType.NoiseType_Value
    elif noise_type == 'fbm':
        noise.noise_type = NoiseType.NoiseType_Perlin
        noise.fractal_type = FractalType.FractalType_FBm
        noise.fractal_octaves = 4
        noise.fractal_gain = 0.5

    data = np.zeros((height, width, 4), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            # Get noise value and map to [0, 1]
            val = (noise.get_noise(x, y) + 1) / 2

            # Interpolate between colors
            for c in range(4):
                data[y, x, c] = int(color_low[c] * (1 - val) + color_high[c] * val)

    return data
```

---

## Tileable Noise (4D Sampling)

For seamlessly tileable textures, sample 4D noise with circular coordinates:

```python
import math

def generate_tileable_noise(width: int, height: int, scale: float = 1.0,
                            seed: int = 42) -> np.ndarray:
    """Generate seamlessly tileable noise texture."""
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_Perlin
    noise.frequency = 1.0  # Scale handled in coordinates

    data = np.zeros((height, width, 4), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            # Map 2D to 4D torus
            s = x / width
            t = y / height

            nx = math.cos(s * 2 * math.pi) * scale
            ny = math.sin(s * 2 * math.pi) * scale
            nz = math.cos(t * 2 * math.pi) * scale
            nw = math.sin(t * 2 * math.pi) * scale

            # Sample 4D noise (tiles seamlessly)
            val = (noise.get_noise_4d(nx, ny, nz, nw) + 1) / 2
            gray = int(val * 255)
            data[y, x] = (gray, gray, gray, 255)

    return data
```

---

## Common Presets

### Terrain
```python
noise.noise_type = NoiseType.NoiseType_Perlin
noise.frequency = 0.01
noise.fractal_type = FractalType.FractalType_FBm
noise.fractal_octaves = 6
noise.fractal_gain = 0.5
```

### Clouds
```python
noise.noise_type = NoiseType.NoiseType_OpenSimplex2
noise.frequency = 0.02
noise.fractal_type = FractalType.FractalType_FBm
noise.fractal_octaves = 4
noise.fractal_gain = 0.6
```

### Scales/Cells
```python
noise.noise_type = NoiseType.NoiseType_Cellular
noise.frequency = 0.08
noise.cellular_return_type = CellularReturnType.CellularReturnType_Distance
```

### Cracks
```python
noise.noise_type = NoiseType.NoiseType_Cellular
noise.frequency = 0.1
noise.cellular_return_type = CellularReturnType.CellularReturnType_Distance2Sub
```

### Wood Grain
```python
# Stretch noise in one direction
noise.noise_type = NoiseType.NoiseType_Perlin
noise.frequency = 0.02
# Sample with stretched Y: noise.get_noise(x, y * 0.2)
```

### Marble Veins
```python
noise.noise_type = NoiseType.NoiseType_Perlin
noise.frequency = 0.03
noise.fractal_type = FractalType.FractalType_FBm
noise.fractal_octaves = 3
# Apply: sin(x * 0.1 + noise_value * 4.0) for veins
```
