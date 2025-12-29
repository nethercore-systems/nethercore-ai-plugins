# Matcap Generation (Complete Library)

Matcaps are spherical textures that encode lighting. They're sampled using view-space normals for fast, consistent lighting.

## How Matcaps Work

```
For each pixel (x, y) in the matcap:
    nx = (x / size) * 2 - 1     # [-1, 1]
    ny = 1 - (y / size) * 2     # [-1, 1] (Y flipped)
    dist = sqrt(nx² + ny²)

    if dist <= 1.0:
        nz = sqrt(1 - dist²)    # Z component of normal
        # (nx, ny, nz) is the view-space normal at this point
        # Apply lighting calculations to determine color
```

## Base Matcap Generator

```python
import numpy as np
from PIL import Image
import math

def generate_matcap_base(size: int = 128):
    """Generate base sphere normal data for matcap generation."""
    normals = np.zeros((size, size, 3), dtype=np.float32)
    valid = np.zeros((size, size), dtype=bool)

    center = size / 2
    for y in range(size):
        for x in range(size):
            nx = (x - center) / center
            ny = (center - y) / center  # Flip Y
            dist = math.sqrt(nx*nx + ny*ny)

            if dist <= 1.0:
                nz = math.sqrt(1.0 - dist*dist)
                normals[y, x] = [nx, ny, nz]
                valid[y, x] = True

    return normals, valid
```

---

## Base Matcaps (Standalone Materials)

These matcaps define complete lighting. Use in slot 1 alone or as a base layer.

### Studio Warm

```python
def generate_studio_warm(size: int = 128):
    """3-point lighting with warm key, cool fill."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    # Light directions
    key_dir = np.array([0.5, 0.5, 0.7])    # Warm key light
    fill_dir = np.array([-0.4, 0.3, 0.6])  # Cool fill
    rim_dir = np.array([0.0, -0.8, 0.3])   # Rim light

    key_dir /= np.linalg.norm(key_dir)
    fill_dir /= np.linalg.norm(fill_dir)
    rim_dir /= np.linalg.norm(rim_dir)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (128, 128, 128, 255)  # Neutral outside
                continue

            n = normals[y, x]
            key = max(0, np.dot(n, key_dir))
            fill = max(0, np.dot(n, fill_dir)) * 0.4
            rim = max(0, np.dot(n, rim_dir)) ** 4 * 0.3

            # Warm key + cool fill
            r = int(min(255, (0.3 + key * 0.6 + fill * 0.3 + rim) * 255))
            g = int(min(255, (0.28 + key * 0.55 + fill * 0.35 + rim) * 255))
            b = int(min(255, (0.25 + key * 0.5 + fill * 0.4 + rim) * 255))
            img[y, x] = (r, g, b, 255)

    Image.fromarray(img, 'RGBA').save("matcap_studio_warm.png")
```

### Studio Cool

```python
def generate_studio_cool(size: int = 128):
    """Cool-tinted studio lighting."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    key_dir = np.array([0.5, 0.6, 0.6])
    fill_dir = np.array([-0.5, 0.2, 0.5])

    key_dir /= np.linalg.norm(key_dir)
    fill_dir /= np.linalg.norm(fill_dir)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (128, 128, 128, 255)
                continue

            n = normals[y, x]
            key = max(0, np.dot(n, key_dir))
            fill = max(0, np.dot(n, fill_dir)) * 0.35

            r = int(min(255, (0.25 + key * 0.5 + fill * 0.4) * 255))
            g = int(min(255, (0.28 + key * 0.55 + fill * 0.35) * 255))
            b = int(min(255, (0.32 + key * 0.6 + fill * 0.3) * 255))
            img[y, x] = (r, g, b, 255)

    Image.fromarray(img, 'RGBA').save("matcap_studio_cool.png")
```

### Clay Gray (ZBrush Style)

```python
def generate_clay_gray(size: int = 128):
    """Neutral clay/sculpt preview style."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    light_dir = np.array([0.3, 0.7, 0.6])
    light_dir /= np.linalg.norm(light_dir)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (128, 128, 128, 255)
                continue

            n = normals[y, x]
            diffuse = max(0, np.dot(n, light_dir))
            ambient = 0.35

            val = int((ambient + diffuse * 0.65) * 255)
            img[y, x] = (val, val, val, 255)

    Image.fromarray(img, 'RGBA').save("matcap_clay_gray.png")
```

### Red Wax (Subsurface Approximation)

```python
def generate_red_wax(size: int = 128):
    """Warm wax/subsurface scattering look."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    light_dir = np.array([0.4, 0.6, 0.7])
    light_dir /= np.linalg.norm(light_dir)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (128, 64, 64, 255)
                continue

            n = normals[y, x]
            diffuse = max(0, np.dot(n, light_dir))
            wrap = (np.dot(n, light_dir) + 0.5) / 1.5  # Wrap lighting

            r = int(min(255, (0.5 + diffuse * 0.4 + wrap * 0.2) * 255))
            g = int(min(255, (0.25 + diffuse * 0.25 + wrap * 0.1) * 255))
            b = int(min(255, (0.2 + diffuse * 0.2 + wrap * 0.08) * 255))
            img[y, x] = (r, g, b, 255)

    Image.fromarray(img, 'RGBA').save("matcap_red_wax.png")
```

### Jade

```python
def generate_jade(size: int = 128):
    """Banded green jade stone."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    light_dir = np.array([0.3, 0.6, 0.7])
    light_dir /= np.linalg.norm(light_dir)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (100, 140, 100, 255)
                continue

            n = normals[y, x]
            diffuse = max(0, np.dot(n, light_dir))
            fresnel = 1.0 - max(0, n[2]) ** 0.5  # Edge brightening

            r = int(min(255, (0.2 + diffuse * 0.3 + fresnel * 0.15) * 255))
            g = int(min(255, (0.35 + diffuse * 0.45 + fresnel * 0.2) * 255))
            b = int(min(255, (0.25 + diffuse * 0.3 + fresnel * 0.15) * 255))
            img[y, x] = (r, g, b, 255)

    Image.fromarray(img, 'RGBA').save("matcap_jade.png")
```

### Gold/Chrome/Copper

```python
def generate_metallic_matcap(name: str, color: tuple, size: int = 128):
    """Metallic matcap with sharp specular."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    light_dir = np.array([0.5, 0.5, 0.7])
    light_dir /= np.linalg.norm(light_dir)
    view_dir = np.array([0, 0, 1])
    half_vec = light_dir + view_dir
    half_vec /= np.linalg.norm(half_vec)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (128, 128, 128, 255)
                continue

            n = normals[y, x]
            diffuse = max(0, np.dot(n, light_dir))
            spec = max(0, np.dot(n, half_vec)) ** 64

            r = int(min(255, (color[0]/255 * (0.2 + diffuse * 0.5) + spec * 0.6) * 255))
            g = int(min(255, (color[1]/255 * (0.2 + diffuse * 0.5) + spec * 0.6) * 255))
            b = int(min(255, (color[2]/255 * (0.2 + diffuse * 0.5) + spec * 0.6) * 255))
            img[y, x] = (r, g, b, 255)

    Image.fromarray(img, 'RGBA').save(f"matcap_{name}.png")

# Generate metallic matcaps
generate_metallic_matcap("gold", (255, 200, 80))
generate_metallic_matcap("chrome", (220, 220, 220))
generate_metallic_matcap("copper", (200, 140, 100))
```

### Pearl (Iridescent White)

```python
def generate_pearl(size: int = 128):
    """Iridescent pearl with subtle color shifts."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (230, 230, 230, 255)
                continue

            n = normals[y, x]
            fresnel = 1.0 - abs(n[2])

            # Angle-based iridescence
            angle = math.atan2(n[1], n[0])
            hue_shift = (angle / math.pi + 1) / 2

            base = 0.85 + n[2] * 0.15
            r = int(min(255, (base + fresnel * 0.1 * math.sin(hue_shift * math.pi * 2)) * 255))
            g = int(min(255, (base + fresnel * 0.1 * math.sin(hue_shift * math.pi * 2 + 2)) * 255))
            b = int(min(255, (base + fresnel * 0.1 * math.sin(hue_shift * math.pi * 2 + 4)) * 255))
            img[y, x] = (r, g, b, 255)

    Image.fromarray(img, 'RGBA').save("matcap_pearl.png")
```

### Skin

```python
def generate_skin(size: int = 128):
    """Skin-like subsurface matcap."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    light_dir = np.array([0.3, 0.5, 0.8])
    light_dir /= np.linalg.norm(light_dir)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (200, 160, 140, 255)
                continue

            n = normals[y, x]
            diffuse = max(0, np.dot(n, light_dir))
            sss = (np.dot(n, light_dir) + 0.6) / 1.6  # Soft wrap

            r = int(min(255, (0.6 + diffuse * 0.3 + sss * 0.15) * 255))
            g = int(min(255, (0.45 + diffuse * 0.25 + sss * 0.1) * 255))
            b = int(min(255, (0.4 + diffuse * 0.2 + sss * 0.08) * 255))
            img[y, x] = (r, g, b, 255)

    Image.fromarray(img, 'RGBA').save("matcap_skin.png")
```

---

## Blending Matcaps (for Layering)

Use with blend modes: Multiply (0), Add (1), HSV (2).

### Rim Light (Add Blend)

```python
def generate_rim_light(size: int = 128, color: tuple = (255, 255, 255)):
    """Rim/edge lighting. Use with Add blend mode."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (0, 0, 0, 255)
                continue

            n = normals[y, x]
            rim = (1.0 - abs(n[2])) ** 2  # Edges bright

            r = int(color[0] * rim)
            g = int(color[1] * rim)
            b = int(color[2] * rim)
            img[y, x] = (r, g, b, 255)

    Image.fromarray(img, 'RGBA').save("matcap_rim_light.png")
```

### Cyan Glow (Add Blend)

```python
def generate_cyan_glow(size: int = 128):
    """Cyan-tinted rim glow."""
    generate_rim_light(size, color=(100, 200, 255))
    # Rename output
    import os
    os.rename("matcap_rim_light.png", "matcap_cyan_glow.png")
```

### Top Light (Multiply Blend)

```python
def generate_top_light(size: int = 128):
    """Top-down lighting. Use with Multiply blend mode."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (255, 255, 255, 255)  # Neutral for multiply
                continue

            n = normals[y, x]
            top = (n[1] + 1) / 2  # Top surfaces bright

            val = int((0.4 + top * 0.6) * 255)
            img[y, x] = (val, val, val, 255)

    Image.fromarray(img, 'RGBA').save("matcap_top_light.png")
```

### Specular Dot (Add Blend)

```python
def generate_specular_dot(size: int = 128, tightness: float = 64):
    """Sharp specular highlight. Use with Add blend mode."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    light_dir = np.array([0.5, 0.5, 0.7])
    light_dir /= np.linalg.norm(light_dir)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (0, 0, 0, 255)
                continue

            n = normals[y, x]
            spec = max(0, np.dot(n, light_dir)) ** tightness

            val = int(spec * 255)
            img[y, x] = (val, val, val, 255)

    Image.fromarray(img, 'RGBA').save("matcap_specular_dot.png")
```

### Ambient Occlusion (Multiply Blend)

```python
def generate_ao_matcap(size: int = 128):
    """Edge darkening/AO. Use with Multiply blend mode."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (255, 255, 255, 255)
                continue

            n = normals[y, x]
            ao = n[2] ** 0.5  # Edges dark, center bright

            val = int((0.5 + ao * 0.5) * 255)
            img[y, x] = (val, val, val, 255)

    Image.fromarray(img, 'RGBA').save("matcap_ao.png")
```

### Inner Glow (Add Blend)

```python
def generate_inner_glow(size: int = 128, color: tuple = (255, 255, 200)):
    """Center glow, dark edges. Use with Add blend mode."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (0, 0, 0, 255)
                continue

            n = normals[y, x]
            glow = n[2] ** 2  # Center bright

            r = int(color[0] * glow * 0.5)
            g = int(color[1] * glow * 0.5)
            b = int(color[2] * glow * 0.5)
            img[y, x] = (r, g, b, 255)

    Image.fromarray(img, 'RGBA').save("matcap_inner_glow.png")
```

### Gradient Bands / Toon Steps (Multiply Blend)

```python
def generate_gradient_bands(size: int = 128, bands: int = 4):
    """Stepped/toon shading. Use with Multiply blend mode."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    light_dir = np.array([0.3, 0.6, 0.7])
    light_dir /= np.linalg.norm(light_dir)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (255, 255, 255, 255)
                continue

            n = normals[y, x]
            light = (np.dot(n, light_dir) + 1) / 2  # [0, 1]

            # Quantize to bands
            band = int(light * bands) / bands
            val = int((0.3 + band * 0.7) * 255)
            img[y, x] = (val, val, val, 255)

    Image.fromarray(img, 'RGBA').save("matcap_gradient_bands.png")
```

### Rainbow / HSV Shift (HSV Blend)

```python
def generate_rainbow_matcap(size: int = 128):
    """Prismatic/rainbow effect. Use with HSV blend mode."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (128, 128, 128, 255)  # Neutral
                continue

            n = normals[y, x]
            angle = math.atan2(n[1], n[0])
            hue = (angle / math.pi + 1) / 2  # [0, 1]

            # HSV matcap: R=hue shift, G=saturation, B=value
            img[y, x] = (int(hue * 255), 180, 128, 255)

    Image.fromarray(img, 'RGBA').save("matcap_rainbow.png")
```

### Hue Shift Warm/Cool (HSV Blend)

```python
def generate_hue_shift(size: int = 128, shift_range: float = 0.1, warm: bool = True):
    """Subtle hue temperature shift. Use with HSV blend mode."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    normals, valid = generate_matcap_base(size)

    for y in range(size):
        for x in range(size):
            if not valid[y, x]:
                img[y, x] = (128, 128, 128, 255)
                continue

            n = normals[y, x]
            # Shift based on facing direction
            shift = n[2] * shift_range
            if warm:
                hue = 0.5 + shift  # Shift toward warm
            else:
                hue = 0.5 - shift  # Shift toward cool

            img[y, x] = (int(hue * 255), 60, 128, 255)

    name = "warm" if warm else "cool"
    Image.fromarray(img, 'RGBA').save(f"matcap_hue_shift_{name}.png")

generate_hue_shift(warm=True)
generate_hue_shift(warm=False)
```

---

## Matcap Library Summary

| Name | Blend Mode | Purpose |
|------|------------|---------|
| Studio Warm | Base | 3-point warm key lighting |
| Studio Cool | Base | Cool-tinted studio |
| Clay Gray | Base | Neutral sculpt preview |
| Red Wax | Base | Subsurface scattering |
| Jade | Base | Green stone |
| Gold | Base | Metallic gold |
| Chrome | Base | Metallic chrome |
| Copper | Base | Metallic copper |
| Pearl | Base | Iridescent white |
| Skin | Base | Subsurface flesh tones |
| Rim Light | Add | Bright edges |
| Cyan Glow | Add | Colored rim |
| Top Light | Multiply | Top-down shading |
| Specular Dot | Add | Sharp highlight |
| Ambient Occlusion | Multiply | Edge darkening |
| Inner Glow | Add | Center brightness |
| Gradient Bands | Multiply | Toon steps |
| Rainbow | HSV | Prismatic shift |
| Hue Shift Warm | HSV | Warm color shift |
| Hue Shift Cool | HSV | Cool color shift |

---

## Typical Layering Setups

### Toon Character
1. Slot 0: Albedo (UV-mapped)
2. Slot 1: Gradient Bands (Multiply) - Stepped shading
3. Slot 2: Rim Light (Add) - Edge pop
4. Slot 3: Specular Dot (Add) - Highlight

### Metallic Object
1. Slot 0: Albedo
2. Slot 1: Chrome matcap (base, or Multiply)
3. Slot 2: AO (Multiply) - Ground shadows
4. Slot 3: Specular Dot (Add) - Sharp highlight

### Iridescent Surface
1. Slot 0: Albedo (neutral gray)
2. Slot 1: Pearl (base)
3. Slot 2: Rainbow (HSV) - Color shift
4. Slot 3: Rim Light (Add) - Edge pop
