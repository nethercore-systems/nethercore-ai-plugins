# MRE and SSE Texture Generation

Material property maps for Mode 2 (Metallic-Roughness) and Mode 3 (Specular-Shininess).

## MRE Textures (Mode 2)

MRE packs three properties into RGB channels:

| Channel | Property | 0 | 255 |
|---------|----------|---|-----|
| R | Metallic | Dielectric (plastic) | Full metal |
| G | Roughness | Mirror smooth | Fully diffuse |
| B | Emissive | No glow | Max glow |

### Basic MRE Generation

```python
import numpy as np
from PIL import Image
from pyfastnoiselite import FastNoiseLite, NoiseType

def generate_mre(name: str, metallic: float, roughness: float, emissive: float = 0.0,
                 roughness_variation: float = 0.1, size: int = 256, seed: int = 42):
    """Generate MRE texture with optional roughness variation.

    Args:
        metallic: 0.0 (plastic) to 1.0 (metal)
        roughness: 0.0 (smooth) to 1.0 (rough)
        emissive: 0.0 (none) to 1.0 (max glow)
        roughness_variation: How much noise affects roughness
    """
    img = np.zeros((size, size, 4), dtype=np.uint8)

    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.05

    for y in range(size):
        for x in range(size):
            n = (noise.get_noise(x, y) + 1) / 2  # [0, 1]

            # Roughness varies with noise
            r_varied = roughness + (n - 0.5) * roughness_variation * 2
            r_varied = max(0, min(1, r_varied))

            img[y, x] = [
                int(metallic * 255),
                int(r_varied * 255),
                int(emissive * 255),
                255
            ]

    Image.fromarray(img, 'RGBA').save(f"{name}_mre.png")

# Examples
generate_mre("chrome", metallic=1.0, roughness=0.1)
generate_mre("brushed_steel", metallic=1.0, roughness=0.4, roughness_variation=0.15)
generate_mre("rubber", metallic=0.0, roughness=0.9)
generate_mre("plastic", metallic=0.0, roughness=0.5)
generate_mre("glowing_crystal", metallic=0.2, roughness=0.3, emissive=0.8)
```

### MRE Material Presets

| Material | Metallic | Roughness | Emissive |
|----------|----------|-----------|----------|
| Polished Chrome | 1.0 | 0.05-0.15 | 0.0 |
| Brushed Steel | 1.0 | 0.3-0.5 | 0.0 |
| Gold | 1.0 | 0.15-0.25 | 0.0 |
| Copper | 1.0 | 0.25-0.35 | 0.0 |
| Aluminum | 1.0 | 0.4-0.5 | 0.0 |
| Plastic | 0.0 | 0.3-0.6 | 0.0 |
| Rubber | 0.0 | 0.8-1.0 | 0.0 |
| Glass | 0.0 | 0.0-0.1 | 0.0 |
| Leather | 0.0 | 0.6-0.8 | 0.0 |
| LED/Neon | 0.0 | 0.2-0.4 | 0.5-1.0 |
| Lava | 0.0 | 0.7 | 0.9 |

---

## SSE Textures (Mode 3)

SSE packs three properties into RGB channels:

| Channel | Property | 0 | 255 |
|---------|----------|---|-----|
| R | Specular Damping | Full specular | No specular |
| G | Shininess | Soft (exp=1) | Sharp (exp=256) |
| B | Emissive | No glow | Max glow |

**Important:** Specular Damping (R) should be **0** for most materials. Only increase for worn/dirty areas.

### Basic SSE Generation

```python
def generate_sse(name: str, shininess: float, specular_damping: float = 0.0,
                 emissive: float = 0.0, shininess_variation: float = 0.1,
                 size: int = 256, seed: int = 42):
    """Generate SSE texture with optional variation.

    Args:
        shininess: 0.0 (diffuse) to 1.0 (mirror-like)
        specular_damping: 0.0 (full specular) to 1.0 (no specular)
        emissive: 0.0 (none) to 1.0 (max glow)
    """
    img = np.zeros((size, size, 4), dtype=np.uint8)

    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.08

    for y in range(size):
        for x in range(size):
            n = (noise.get_noise(x, y) + 1) / 2

            sh_varied = shininess + (n - 0.5) * shininess_variation * 2
            sh_varied = max(0, min(1, sh_varied))

            img[y, x] = [
                int(specular_damping * 255),
                int(sh_varied * 255),
                int(emissive * 255),
                255
            ]

    Image.fromarray(img, 'RGBA').save(f"{name}_sse.png")

# Examples
generate_sse("polished_gold", shininess=0.85)
generate_sse("worn_brass", shininess=0.6, specular_damping=0.3)
generate_sse("cloth", shininess=0.1)
```

### Shininess Reference

| Shininess Value | Exponent | Appearance |
|-----------------|----------|------------|
| 0.0-0.2 | 1-52 | Very soft (cloth, skin) |
| 0.2-0.4 | 52-103 | Broad (leather, wood) |
| 0.4-0.6 | 103-154 | Medium (plastic) |
| 0.6-0.8 | 154-205 | Tight (polished metal) |
| 0.8-1.0 | 205-256 | Mirror (chrome, glass) |

---

## Specular Color Texture (Mode 3, Slot 2)

The specular color tints highlight reflections.

```python
def generate_specular_color(name: str, specular_color: tuple, size: int = 256):
    """Generate specular color texture for Mode 3.

    Args:
        specular_color: (R, G, B, A) specular tint
    """
    img = np.zeros((size, size, 4), dtype=np.uint8)
    img[:, :] = specular_color
    Image.fromarray(img, 'RGBA').save(f"{name}_specular.png")

# Examples
generate_specular_color("neutral", (255, 255, 255, 255))  # White - neutral
generate_specular_color("gold", (255, 200, 100, 255))      # Gold tint
generate_specular_color("copper", (255, 180, 150, 255))    # Copper tint
generate_specular_color("cold", (200, 220, 255, 255))      # Cold/blue
```

---

## Complete Mode 2 Material Set

```python
def generate_mode2_material(name: str, albedo_color: tuple,
                            metallic: float, roughness: float,
                            emissive: float = 0.0, variation: float = 0.2,
                            size: int = 256, seed: int = 42):
    """Generate complete Mode 2 material (Albedo + MRE)."""
    # Generate albedo
    albedo = np.zeros((size, size, 4), dtype=np.uint8)
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.03

    for y in range(size):
        for x in range(size):
            n = (noise.get_noise(x, y) + 1) / 2
            factor = 1.0 - variation/2 + variation * n
            albedo[y, x] = [
                int(min(255, albedo_color[0] * factor)),
                int(min(255, albedo_color[1] * factor)),
                int(min(255, albedo_color[2] * factor)),
                255
            ]

    Image.fromarray(albedo, 'RGBA').save(f"{name}_albedo.png")

    # Generate MRE
    mre = np.zeros((size, size, 4), dtype=np.uint8)
    noise2 = FastNoiseLite(seed + 1)
    noise2.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise2.frequency = 0.05

    for y in range(size):
        for x in range(size):
            n = (noise2.get_noise(x, y) + 1) / 2
            r_varied = roughness + (n - 0.5) * variation

            mre[y, x] = [
                int(metallic * 255),
                int(max(0, min(1, r_varied)) * 255),
                int(emissive * 255),
                255
            ]

    Image.fromarray(mre, 'RGBA').save(f"{name}_mre.png")

# Example: Brushed copper
generate_mode2_material("copper",
    albedo_color=(184, 115, 51, 255),
    metallic=1.0,
    roughness=0.35
)
```

---

## Complete Mode 3 Material Set

```python
def generate_mode3_material(name: str, albedo_color: tuple,
                            shininess: float, specular_color: tuple,
                            specular_damping: float = 0.0, emissive: float = 0.0,
                            variation: float = 0.2, size: int = 256, seed: int = 42):
    """Generate complete Mode 3 material (Albedo + SSE + Specular)."""
    # Albedo
    albedo = np.zeros((size, size, 4), dtype=np.uint8)
    noise = FastNoiseLite(seed)
    noise.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise.frequency = 0.03

    for y in range(size):
        for x in range(size):
            n = (noise.get_noise(x, y) + 1) / 2
            factor = 1.0 - variation/2 + variation * n
            albedo[y, x] = [
                int(min(255, albedo_color[0] * factor)),
                int(min(255, albedo_color[1] * factor)),
                int(min(255, albedo_color[2] * factor)),
                255
            ]

    Image.fromarray(albedo, 'RGBA').save(f"{name}_albedo.png")

    # SSE
    sse = np.zeros((size, size, 4), dtype=np.uint8)
    sse[:, :] = [
        int(specular_damping * 255),
        int(shininess * 255),
        int(emissive * 255),
        255
    ]
    Image.fromarray(sse, 'RGBA').save(f"{name}_sse.png")

    # Specular color
    spec = np.zeros((size, size, 4), dtype=np.uint8)
    spec[:, :] = specular_color
    Image.fromarray(spec, 'RGBA').save(f"{name}_specular.png")

# Example: Gold material
generate_mode3_material("gold",
    albedo_color=(255, 200, 50, 255),
    shininess=0.8,
    specular_color=(255, 220, 130, 255)
)
```

---

## Worn/Weathered Materials

Add wear patterns by varying specular damping (SSE) or roughness (MRE):

```python
def generate_worn_mre(name: str, metallic: float, base_roughness: float,
                      wear_amount: float = 0.3, size: int = 256, seed: int = 42):
    """Generate MRE with edge wear and scratches."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    # Base noise for roughness variation
    noise1 = FastNoiseLite(seed)
    noise1.noise_type = NoiseType.NoiseType_OpenSimplex2
    noise1.frequency = 0.05

    # Cellular noise for wear patterns
    noise2 = FastNoiseLite(seed + 1)
    noise2.noise_type = NoiseType.NoiseType_Cellular
    noise2.frequency = 0.08

    for y in range(size):
        for x in range(size):
            n1 = (noise1.get_noise(x, y) + 1) / 2
            n2 = (noise2.get_noise(x, y) + 1) / 2

            # Base roughness with variation
            roughness = base_roughness + (n1 - 0.5) * 0.2

            # Add wear in cell edges
            if n2 < 0.2:
                roughness += wear_amount * (0.2 - n2) / 0.2

            roughness = max(0, min(1, roughness))

            img[y, x] = [
                int(metallic * 255),
                int(roughness * 255),
                0,
                255
            ]

    Image.fromarray(img, 'RGBA').save(f"{name}_mre.png")

generate_worn_mre("worn_steel", metallic=1.0, base_roughness=0.3, wear_amount=0.4)
```
