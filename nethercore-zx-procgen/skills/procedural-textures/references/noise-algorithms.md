# Noise Algorithms Reference

Procedural noise functions for texture generation. These algorithms are language-agnostic and can be implemented in any language.

## Core Noise Types

### Perlin Noise

Classic gradient noise for organic surfaces.

**Parameters:**
| Parameter | Description | Range |
|-----------|-------------|-------|
| Scale | Feature size | 0.01 (large) to 0.2 (fine) |
| Seed | Reproducibility | Any integer |
| Color low | Minimum output color | RGBA |
| Color high | Maximum output color | RGBA |

**Use for:** Clouds, water, organic materials, terrain

**Algorithm (pseudocode):**
```
function perlin_2d(x, y, seed):
    # Get grid cell coordinates
    x0 = floor(x)
    y0 = floor(y)
    x1 = x0 + 1
    y1 = y0 + 1

    # Get interpolation weights
    sx = x - x0
    sy = y - y0

    # Get gradient vectors at corners (hash-based)
    g00 = gradient_at(x0, y0, seed)
    g10 = gradient_at(x1, y0, seed)
    g01 = gradient_at(x0, y1, seed)
    g11 = gradient_at(x1, y1, seed)

    # Compute dot products with distance vectors
    n00 = dot(g00, (x - x0, y - y0))
    n10 = dot(g10, (x - x1, y - y0))
    n01 = dot(g01, (x - x0, y - y1))
    n11 = dot(g11, (x - x1, y - y1))

    # Smooth interpolation (fade function)
    u = smoothstep(sx)
    v = smoothstep(sy)

    # Bilinear interpolation
    return lerp(
        lerp(n00, n10, u),
        lerp(n01, n11, u),
        v
    )

function smoothstep(t):
    return t * t * t * (t * (t * 6 - 15) + 10)
```

---

### Simplex Noise

Faster than Perlin, fewer directional artifacts.

**Parameters:** Same as Perlin

**Advantages:**
- O(n) complexity vs O(2^n) for Perlin in higher dimensions
- No visible grid alignment artifacts
- Better gradient distribution

**Use for:** Same as Perlin, preferred for real-time generation

---

### Voronoi (Cellular) Noise

Cell-like patterns for scales, crystals, cracks.

**Parameters:**
| Parameter | Description | Range |
|-----------|-------------|-------|
| Cell count | Number of cells | 4-32 typical |
| Seed | Reproducibility | Any integer |
| Cell color | Color inside cells | RGBA |
| Edge color | Color at cell edges | RGBA |

**Use for:** Scales, crystals, cracks, organic cells, leather, stone

**Algorithm (pseudocode):**
```
function voronoi_2d(x, y, cell_count, seed):
    # Find containing cell
    cell_x = floor(x * cell_count)
    cell_y = floor(y * cell_count)

    min_dist = infinity
    second_dist = infinity

    # Check 3x3 neighborhood
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            nx = cell_x + dx
            ny = cell_y + dy

            # Get random point in this cell
            point = hash_to_point(nx, ny, seed)
            point.x = (nx + point.x) / cell_count
            point.y = (ny + point.y) / cell_count

            dist = distance(x, y, point.x, point.y)

            if dist < min_dist:
                second_dist = min_dist
                min_dist = dist
            else if dist < second_dist:
                second_dist = dist

    # Return distance to nearest cell center
    # Or (second_dist - min_dist) for edge detection
    return min_dist
```

---

### Fractal Brownian Motion (FBM)

Layered noise for complex organic patterns.

**Parameters:**
| Parameter | Description | Range |
|-----------|-------------|-------|
| Scale | Base feature size | 0.01-0.1 |
| Octaves | Number of layers | 1-8 |
| Persistence | Amplitude falloff | 0.3-0.7 |
| Lacunarity | Frequency multiplier | 2.0 typical |
| Seed | Reproducibility | Any integer |

**Use for:** Terrain, clouds, complex organic textures, weathering

**Algorithm (pseudocode):**
```
function fbm_2d(x, y, octaves, persistence, lacunarity, seed):
    total = 0
    amplitude = 1.0
    frequency = 1.0
    max_value = 0.0  # For normalization

    for i in range(octaves):
        total += perlin_2d(x * frequency, y * frequency, seed + i) * amplitude
        max_value += amplitude

        amplitude *= persistence  # Decrease amplitude
        frequency *= lacunarity   # Increase frequency

    return total / max_value  # Normalize to [-1, 1]
```

**Octave Effects:**
| Octaves | Result |
|---------|--------|
| 1 | Smooth, simple |
| 2-3 | Basic detail |
| 4-6 | Rich complexity |
| 7-8 | Maximum detail (expensive) |

---

## Tileable (Seamless) Noise

For textures that tile seamlessly, use 4D noise with circular coordinates.

**Algorithm (pseudocode):**
```
function tileable_noise_2d(x, y, width, height, seed):
    # Map 2D coordinates to 4D torus
    s = x / width
    t = y / height

    # Create circular coordinates
    nx = cos(s * 2 * PI)
    ny = sin(s * 2 * PI)
    nz = cos(t * 2 * PI)
    nw = sin(t * 2 * PI)

    # Sample 4D noise (result tiles seamlessly in 2D)
    return perlin_4d(nx, ny, nz, nw, seed)
```

**Why it works:** The 4D coordinates wrap around like a torus, so opposite edges sample the same noise values.

---

## Language Examples

### Rust (proc-gen)

```rust
use proc_gen::texture::*;

let mut tex = TextureBuffer::new(256, 256);

// Basic Perlin
tex.perlin(0.05, 42, 0x000000FF, 0xFFFFFFFF);

// FBM for complex patterns
tex.fbm(0.03, 4, 0.5, 42, 0x2F1810FF, 0x5A3A28FF);

// Voronoi for cells
tex.voronoi(16, 42, 0x8B4513FF, 0x2F1810FF);

tex.write_png("output.png").unwrap();
```

### Python (noise library)

```python
from noise import snoise2, pnoise2
import numpy as np
from PIL import Image

def generate_perlin_texture(width, height, scale=0.05, seed=42):
    img = np.zeros((height, width, 4), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            value = pnoise2(x * scale, y * scale, base=seed)
            # Map [-1, 1] to [0, 255]
            byte = int((value + 1) * 0.5 * 255)
            img[y, x] = [byte, byte, byte, 255]

    return Image.fromarray(img)

def generate_fbm_texture(width, height, scale=0.03, octaves=4, persistence=0.5):
    img = np.zeros((height, width, 4), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            value = pnoise2(x * scale, y * scale, octaves=octaves,
                           persistence=persistence)
            byte = int((value + 1) * 0.5 * 255)
            img[y, x] = [byte, byte, byte, 255]

    return Image.fromarray(img)
```

### JavaScript (simplex-noise)

```javascript
import { createNoise2D, createNoise4D } from 'simplex-noise';

function generateTexture(width, height, scale = 0.05, seed = 42) {
    const noise2D = createNoise2D(() => seed);
    const imageData = new ImageData(width, height);

    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const value = noise2D(x * scale, y * scale);
            const byte = Math.floor((value + 1) * 0.5 * 255);
            const i = (y * width + x) * 4;
            imageData.data[i] = byte;
            imageData.data[i + 1] = byte;
            imageData.data[i + 2] = byte;
            imageData.data[i + 3] = 255;
        }
    }

    return imageData;
}

// Tileable version using 4D noise
function generateTileableTexture(width, height, scale = 0.05, seed = 42) {
    const noise4D = createNoise4D(() => seed);
    const imageData = new ImageData(width, height);

    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const s = x / width;
            const t = y / height;

            const nx = Math.cos(s * 2 * Math.PI) * scale;
            const ny = Math.sin(s * 2 * Math.PI) * scale;
            const nz = Math.cos(t * 2 * Math.PI) * scale;
            const nw = Math.sin(t * 2 * Math.PI) * scale;

            const value = noise4D(nx, ny, nz, nw);
            const byte = Math.floor((value + 1) * 0.5 * 255);
            const i = (y * width + x) * 4;
            imageData.data[i] = byte;
            imageData.data[i + 1] = byte;
            imageData.data[i + 2] = byte;
            imageData.data[i + 3] = 255;
        }
    }

    return imageData;
}
```

---

## Common Presets

### Terrain
```
FBM: scale=0.01, octaves=6, persistence=0.5
```

### Clouds
```
FBM: scale=0.02, octaves=4, persistence=0.6
```

### Wood Grain
```
Perlin: scale=0.02 (stretched in one axis)
```

### Marble
```
Perlin + sin(x + perlin_value) for veins
```

### Scales/Cells
```
Voronoi: cell_count=16-32
```
