---
name: Procedural Normal Map Generation for ZX
description: |
  Use this skill to GENERATE normal maps for ZX 3D meshes. Trigger phrases: "generate normal map", "normal map", "bump map", "surface detail", "tangent space", "height to normal", "BC5 texture".

  **Before generating:** Check `.studio/visual-style.local.md` for project style specs. Apply relief intensity and detail level constraints for consistent assets.

  **Load references when:**
  - Height-to-normal conversion → `references/normal-map-generation.md`
  - BC5 format, 2-channel encoding → `references/bc5-format.md`
  - Mesh integration, FFI usage → `references/integration-guide.md`

  Normal maps add surface detail without increasing geometry. Requires mesh with tangent vertex data (FORMAT_TANGENT).

  For ALBEDO/MRE/SSE textures: use `procedural-textures`.
  For MESH generation with tangents: use `procedural-meshes` (enable tangent export).
version: 1.0.0
---

# Procedural Normal Map Generation

Generate tangent-space normal maps procedurally using Python with Pillow (PIL) and NumPy.

## Technology Stack

| Library | Purpose |
|---------|---------|
| **PIL (Pillow)** | Image I/O |
| **NumPy** | Gradient calculation, normalization |
| **FastNoiseLite** | Procedural height patterns |

```bash
pip install pillow numpy pyfastnoiselite
```

## Output Requirements

- **Format:** PNG (RGB or RG - 2-3 channels)
- **Resolution:** Power of 2 (64, 128, 256, 512 max)
- **Naming:** `*_normal.png` or `*_n.png` (triggers auto-BC5 compression)
- **Color Space:** Linear (NOT sRGB)

---

## What Normal Maps Do

Normal maps encode surface direction variations that affect lighting without adding geometry:

```
Vertex normals:  Flat surface = uniform lighting
Normal map:      Per-pixel normal = detailed lighting
```

**Benefits:**
- Add detail to low-poly meshes (scratches, pores, fabric weave)
- No additional triangles
- Enhances specular highlights and shadows

**Costs:**
- Requires tangent vertex data (+4 bytes/vertex)
- Texture slot 3 (shared across modes)
- Memory: BC5 = (width × height) / 2 bytes

---

## Tangent Space Normals

ZX uses **tangent-space** normal maps (not object-space or world-space).

**Channel Mapping:**

| Channel | Axis | Range | Meaning |
|---------|------|-------|---------|
| R | X (tangent) | 0-255 → [-1, 1] | Left/Right deviation |
| G | Y (bitangent) | 0-255 → [-1, 1] | Up/Down deviation |
| B | Z (normal) | Reconstructed | Forward (always positive) |

**Output Format:** Only R and G channels are stored. Z is reconstructed in shader:
```
z = sqrt(1 - x² - y²)
```

**Neutral Normal:** RGB(128, 128, 255) = pointing straight out (no deviation)

---

## Quick Start: Height to Normal

The most common workflow converts a grayscale height map to a normal map:

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

    # Convert [-1, 1] → [0, 255]
    return ((normal + 1.0) * 0.5 * 255).astype(np.uint8)


def generate_normal_from_height(height_path: str, output_path: str, strength: float = 1.0):
    """Generate normal map from grayscale height image."""
    # Load height map
    img = Image.open(height_path).convert('L')
    height = np.array(img, dtype=np.float32) / 255.0

    # Convert to normal
    normal = height_to_normal(height, strength)

    # Save as RGB PNG (will auto-compress to BC5)
    Image.fromarray(normal, 'RGB').save(output_path)
    print(f"Generated: {output_path}")


# Example usage
if __name__ == "__main__":
    generate_normal_from_height(
        "heightmap.png",
        "surface_normal.png",
        strength=1.5
    )
```

---

## Common Patterns

### Brick/Tile Pattern

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

### Noise-Based Detail

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

### Metal Scratches

```python
def generate_scratch_normals(width: int, height: int,
                             num_scratches: int = 20,
                             depth: float = 0.1) -> np.ndarray:
    """Generate directional scratch pattern normal map."""
    import random

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

---

## Strength Guidelines

| Material | Strength | Effect |
|----------|----------|--------|
| Smooth plastic | 0.3 | Subtle surface variation |
| Fabric/cloth | 0.5 - 0.8 | Visible weave pattern |
| Stone/concrete | 1.0 | Medium relief |
| Brick/tile | 1.0 - 1.5 | Pronounced edges |
| Metal scratches | 1.5 - 2.5 | Sharp grooves |
| Organic (bark, skin) | 0.8 - 1.2 | Natural variation |

**Rule of thumb:** Start at 1.0, adjust based on visual result.

---

## ZX Render Mode Support

Normal maps work in **all lit render modes**:

| Mode | Name | Normal Map Effect |
|------|------|-------------------|
| 0 | Lambert | Perturbs Lambert shading |
| 1 | Matcap | Perturbs matcap UV lookup |
| 2 | MR Blinn-Phong | Full tangent-space lighting |
| 3 | SS Blinn-Phong | Full tangent-space lighting |

**Texture Slot:** Always slot 3 (consistent across modes)

---

## Memory Budget

| Resolution | BC5 Size | Use Case |
|------------|----------|----------|
| 64 × 64 | 2 KB | Distant objects, low detail |
| 128 × 128 | 8 KB | Standard objects |
| 256 × 256 | 32 KB | Hero/focal objects |
| 512 × 512 | 128 KB | Rare, high-detail surfaces |

**Vertex Cost:** +4 bytes/vertex for tangent data

---

## File Organization

```
generation/
├── lib/
│   └── normal_utils.py       # height_to_normal(), patterns
├── textures/
│   ├── brick_normal.py       # One file per normal map
│   ├── metal_scratched_normal.py
│   └── fabric_weave_normal.py
└── generated/
    └── textures/
        ├── brick_normal.png  # Output (2-3 channel PNG)
        └── ...
```

---

## Integration Checklist

1. **Mesh has tangent data** - Export with `export_tangents=True`
2. **Mesh has UVs** - Required for texture mapping
3. **Mesh has normals** - Tangents depend on normals
4. **Texture named correctly** - `*_normal.png` triggers BC5
5. **FFI binds normal map** - `material_normal(texture_id)`

See `references/integration-guide.md` for complete integration workflow.

---

## Reference Files

| Reference | Contents |
|-----------|----------|
| `normal-map-generation.md` | Detailed algorithms, seamless techniques |
| `bc5-format.md` | BC5 compression, channel encoding |
| `integration-guide.md` | Mesh requirements, FFI binding |
