# Multi-Layer Texture System

Professional textures are built from multiple layers, not single noise passes. This mimics how artists work in Photoshop/Substance and produces dramatically better results.

## Why Layers Matter

```
Single-pass noise = obvious programmer art
Multi-layer composition = professional quality
```

Real materials have:
- Base color with subtle variation
- Surface features (scratches, cracks, pores)
- Weathering (rust, stains, dust)
- Edge wear and corner dirt
- Final polish (contrast, color grading)

---

## Layer Workflow

```
1. BASE: Solid color + subtle noise variation
2. DETAIL: Perlin/Simplex noise overlay
3. FEATURES: Scratches, cracks, grain
4. WEATHERING: Rust, stains, dust
5. FINAL: Contrast boost, color grading
```

---

## Complete Layered Texture Generator

```python
import numpy as np
from PIL import Image
from pyfastnoiselite import FastNoiseLite, NoiseType, FractalType, CellularReturnType
import math

class LayeredTextureBuilder:
    """Build textures through layered composition."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Float buffer for precision during composition
        self.data = np.zeros((height, width, 4), dtype=np.float32)
        self.seed_counter = 0

    def _next_seed(self, base_seed: int) -> int:
        """Get incrementing seed for consistent randomness."""
        self.seed_counter += 1
        return base_seed + self.seed_counter

    # === Base Layer ===

    def base(self, color: tuple, seed: int = 42) -> 'LayeredTextureBuilder':
        """Fill with base color and subtle noise variation."""
        self.data[:, :] = [c / 255.0 for c in color]

        noise = FastNoiseLite(seed)
        noise.noise_type = NoiseType.NoiseType_OpenSimplex2
        noise.frequency = 0.02

        for y in range(self.height):
            for x in range(self.width):
                n = (noise.get_noise(x, y) + 1) / 2
                factor = 0.95 + n * 0.1
                self.data[y, x, :3] *= factor

        return self

    # === Noise Layers ===

    def noise_layer(self, noise_type: str = 'perlin', scale: float = 0.05,
                    intensity: float = 0.2, blend_mode: str = 'overlay',
                    seed: int = 42) -> 'LayeredTextureBuilder':
        """Add a noise layer with blending."""
        noise = FastNoiseLite(self._next_seed(seed))
        noise.frequency = scale

        if noise_type == 'perlin':
            noise.noise_type = NoiseType.NoiseType_Perlin
        elif noise_type == 'simplex':
            noise.noise_type = NoiseType.NoiseType_OpenSimplex2
        elif noise_type == 'cellular':
            noise.noise_type = NoiseType.NoiseType_Cellular
        elif noise_type == 'fbm':
            noise.noise_type = NoiseType.NoiseType_Perlin
            noise.fractal_type = FractalType.FractalType_FBm
            noise.fractal_octaves = 4

        for y in range(self.height):
            for x in range(self.width):
                n = (noise.get_noise(x, y) + 1) / 2

                if blend_mode == 'overlay':
                    for c in range(3):
                        base = self.data[y, x, c]
                        if base < 0.5:
                            result = 2 * base * n
                        else:
                            result = 1 - 2 * (1 - base) * (1 - n)
                        self.data[y, x, c] = base * (1 - intensity) + result * intensity

                elif blend_mode == 'multiply':
                    self.data[y, x, :3] *= (1 - intensity) + n * intensity

                elif blend_mode == 'add':
                    self.data[y, x, :3] += n * intensity

        self.data[:, :, :3] = np.clip(self.data[:, :, :3], 0, 1)
        return self

    # === Feature Layers ===

    def scratches(self, density: float = 0.15, length_range: tuple = (0.1, 0.3),
                  depth: float = 0.4, direction: str = 'random',
                  seed: int = 42) -> 'LayeredTextureBuilder':
        """Add scratch marks to the texture."""
        import random
        random.seed(seed)

        num_scratches = int(density * self.width * self.height / 100)

        for _ in range(num_scratches):
            # Random start point
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)

            # Random length
            length = random.uniform(length_range[0], length_range[1]) * self.width

            # Direction
            if direction == 'random':
                angle = random.uniform(0, 2 * math.pi)
            elif direction == 'horizontal':
                angle = random.uniform(-0.2, 0.2)
            elif direction == 'vertical':
                angle = random.uniform(math.pi/2 - 0.2, math.pi/2 + 0.2)
            else:  # diagonal
                angle = random.uniform(math.pi/4 - 0.2, math.pi/4 + 0.2)

            # Draw scratch
            steps = int(length)
            for i in range(steps):
                x = int(start_x + math.cos(angle) * i)
                y = int(start_y + math.sin(angle) * i)

                if 0 <= x < self.width and 0 <= y < self.height:
                    # Darken for scratch
                    self.data[y, x, :3] *= (1 - depth * 0.5)

        return self

    def cracks(self, density: float = 0.1, depth: float = 0.4,
               seed: int = 42) -> 'LayeredTextureBuilder':
        """Add crack patterns using Voronoi edges."""
        noise = FastNoiseLite(self._next_seed(seed))
        noise.noise_type = NoiseType.NoiseType_Cellular
        noise.frequency = 0.08
        noise.cellular_return_type = CellularReturnType.CellularReturnType_Distance2Sub

        for y in range(self.height):
            for x in range(self.width):
                n = (noise.get_noise(x, y) + 1) / 2

                # Cracks at low values (cell edges)
                if n < density:
                    crack_intensity = (density - n) / density * depth
                    self.data[y, x, :3] *= (1 - crack_intensity)

        return self

    def grain(self, scale: float = 0.1, intensity: float = 0.2,
              direction: str = 'horizontal', seed: int = 42) -> 'LayeredTextureBuilder':
        """Add directional grain pattern."""
        noise = FastNoiseLite(self._next_seed(seed))
        noise.noise_type = NoiseType.NoiseType_Perlin
        noise.frequency = scale

        for y in range(self.height):
            for x in range(self.width):
                if direction == 'horizontal':
                    n = (noise.get_noise(x, y * 0.1) + 1) / 2
                else:  # vertical
                    n = (noise.get_noise(x * 0.1, y) + 1) / 2

                factor = 1.0 - intensity/2 + intensity * n
                self.data[y, x, :3] *= factor

        return self

    def pores(self, density: float = 0.3, size: float = 0.1, depth: float = 0.3,
              seed: int = 42) -> 'LayeredTextureBuilder':
        """Add pore/pit patterns."""
        noise = FastNoiseLite(self._next_seed(seed))
        noise.noise_type = NoiseType.NoiseType_Cellular
        noise.frequency = density
        noise.cellular_return_type = CellularReturnType.CellularReturnType_Distance

        for y in range(self.height):
            for x in range(self.width):
                n = (noise.get_noise(x, y) + 1) / 2

                if n < size:
                    pore_intensity = (size - n) / size * depth
                    self.data[y, x, :3] *= (1 - pore_intensity)

        return self

    # === Weathering Layers ===

    def rust(self, amount: float = 0.3, color: tuple = (140, 60, 20),
             seed: int = 42) -> 'LayeredTextureBuilder':
        """Add rust/oxidation patches."""
        noise = FastNoiseLite(self._next_seed(seed))
        noise.noise_type = NoiseType.NoiseType_OpenSimplex2
        noise.frequency = 0.03
        noise.fractal_type = FractalType.FractalType_FBm
        noise.fractal_octaves = 4

        rust_color = [c / 255.0 for c in color]

        for y in range(self.height):
            for x in range(self.width):
                n = (noise.get_noise(x, y) + 1) / 2

                if n > (1 - amount):
                    rust_blend = (n - (1 - amount)) / amount
                    rust_blend = min(1.0, rust_blend * 1.5)

                    for c in range(3):
                        self.data[y, x, c] = self.data[y, x, c] * (1 - rust_blend) + rust_color[c] * rust_blend

        return self

    def dust(self, density: float = 0.2, color: tuple = (180, 170, 150),
             seed: int = 42) -> 'LayeredTextureBuilder':
        """Add dust/dirt overlay."""
        noise = FastNoiseLite(self._next_seed(seed))
        noise.noise_type = NoiseType.NoiseType_OpenSimplex2
        noise.frequency = 0.06

        dust_color = [c / 255.0 for c in color]

        for y in range(self.height):
            for x in range(self.width):
                n = (noise.get_noise(x, y) + 1) / 2

                if n > (1 - density):
                    dust_blend = (n - (1 - density)) / density * 0.3

                    for c in range(3):
                        self.data[y, x, c] = self.data[y, x, c] * (1 - dust_blend) + dust_color[c] * dust_blend

        return self

    def stains(self, intensity: float = 0.2, color: tuple = (200, 190, 170),
               seed: int = 42) -> 'LayeredTextureBuilder':
        """Add water stain patterns."""
        noise = FastNoiseLite(self._next_seed(seed))
        noise.noise_type = NoiseType.NoiseType_Cellular
        noise.frequency = 0.04
        noise.cellular_return_type = CellularReturnType.CellularReturnType_Distance

        stain_color = [c / 255.0 for c in color]

        for y in range(self.height):
            for x in range(self.width):
                n = (noise.get_noise(x, y) + 1) / 2

                # Stains at cell edges
                if n > 0.4 and n < 0.5:
                    stain_blend = intensity * (1 - abs(n - 0.45) / 0.05)

                    for c in range(3):
                        self.data[y, x, c] = self.data[y, x, c] * (1 - stain_blend) + stain_color[c] * stain_blend

        return self

    # === Final Pass ===

    def contrast(self, factor: float = 1.1) -> 'LayeredTextureBuilder':
        """Adjust contrast."""
        self.data[:, :, :3] = (self.data[:, :, :3] - 0.5) * factor + 0.5
        self.data[:, :, :3] = np.clip(self.data[:, :, :3], 0, 1)
        return self

    def brightness(self, amount: float = 0.0) -> 'LayeredTextureBuilder':
        """Adjust brightness."""
        self.data[:, :, :3] += amount
        self.data[:, :, :3] = np.clip(self.data[:, :, :3], 0, 1)
        return self

    # === Output ===

    def build(self) -> np.ndarray:
        """Convert to uint8 array."""
        self.data[:, :, 3] = 1.0  # Ensure alpha is 1
        return (np.clip(self.data, 0, 1) * 255).astype(np.uint8)

    def save(self, path: str):
        """Save texture to file."""
        Image.fromarray(self.build(), 'RGBA').save(path)
```

---

## Usage Examples

### Worn Metal

```python
tex = LayeredTextureBuilder(256, 256)
tex.base((180, 180, 185, 255), seed=42)
tex.noise_layer('simplex', scale=0.05, intensity=0.15, blend_mode='overlay')
tex.scratches(density=0.2, depth=0.3, direction='random')
tex.rust(amount=0.25, color=(140, 60, 20))
tex.dust(density=0.15)
tex.contrast(1.1)
tex.save("worn_metal_albedo.png")
```

### Weathered Wood

```python
tex = LayeredTextureBuilder(256, 256)
tex.base((100, 70, 45, 255), seed=42)
tex.grain(scale=0.08, intensity=0.25, direction='vertical')
tex.noise_layer('fbm', scale=0.03, intensity=0.2, blend_mode='multiply')
tex.scratches(density=0.1, depth=0.2)
tex.stains(intensity=0.15)
tex.contrast(1.05)
tex.save("weathered_wood_albedo.png")
```

### Ancient Stone

```python
tex = LayeredTextureBuilder(256, 256)
tex.base((130, 125, 120, 255), seed=42)
tex.noise_layer('fbm', scale=0.02, intensity=0.25, blend_mode='overlay')
tex.cracks(density=0.15, depth=0.4)
tex.pores(density=0.4, size=0.15, depth=0.25)
tex.stains(intensity=0.2)
tex.dust(density=0.3)
tex.contrast(1.05)
tex.save("ancient_stone_albedo.png")
```

### Clean Sci-Fi

```python
tex = LayeredTextureBuilder(256, 256)
tex.base((70, 80, 95, 255), seed=42)
tex.noise_layer('simplex', scale=0.03, intensity=0.1, blend_mode='overlay')
# No weathering for pristine look
tex.contrast(1.15)
tex.save("scifi_panel_albedo.png")
```

---

## Quality Metrics

After generating, validate quality:

| Metric | Minimum | Good |
|--------|---------|------|
| Contrast | 0.15 | 0.3+ |
| Unique colors | 50 | 200+ |
| Histogram balance | 0.3 | 0.5+ |

```python
def assess_quality(texture_path: str) -> dict:
    """Assess texture quality metrics."""
    img = Image.open(texture_path).convert('RGB')
    data = np.array(img)

    # Contrast (standard deviation)
    contrast = np.std(data) / 255.0

    # Unique colors
    flat = data.reshape(-1, 3)
    unique = len(np.unique(flat, axis=0))

    # Histogram balance
    hist, _ = np.histogram(data.flatten(), bins=256, range=(0, 256))
    hist = hist / hist.sum()
    entropy = -np.sum(hist * np.log2(hist + 1e-10))
    balance = entropy / 8.0  # Normalize to [0, 1]

    return {
        'contrast': contrast,
        'unique_colors': unique,
        'histogram_balance': balance,
        'is_good': contrast > 0.15 and unique > 50 and balance > 0.3
    }
```
