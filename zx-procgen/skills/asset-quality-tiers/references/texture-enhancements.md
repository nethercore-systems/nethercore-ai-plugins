# Texture Enhancement Techniques

Detailed techniques for upgrading texture quality through the tier system.

## Placeholder → Temp Upgrades

### Add Noise Variation

Transform flat colors into textured surfaces:

```python
import numpy as np
from PIL import Image

def fbm_noise(width: int, height: int, scale: float, octaves: int,
              persistence: float, seed: int) -> np.ndarray:
    """Generate Fractional Brownian Motion noise.

    Args:
        width, height: Texture dimensions
        scale: Base frequency scale
        octaves: Number of noise layers
        persistence: Amplitude decay per octave
        seed: Random seed

    Returns:
        Noise array of shape (height, width) with values 0-1
    """
    np.random.seed(seed)
    result = np.zeros((height, width), dtype=np.float32)

    frequency = scale
    amplitude = 1.0
    max_value = 0.0

    for _ in range(octaves):
        # Generate noise at this octave
        y_coords, x_coords = np.mgrid[0:height, 0:width]
        noise = np.sin(x_coords * frequency / width * 2 * np.pi) * \
                np.sin(y_coords * frequency / height * 2 * np.pi)
        noise = (noise + 1) / 2  # Normalize to 0-1

        result += noise * amplitude
        max_value += amplitude

        frequency *= 2
        amplitude *= persistence

    return result / max_value

def add_noise_variation(texture: np.ndarray, base_color: np.ndarray,
                       scale: float = 8.0, intensity: float = 0.1,
                       seed: int = 42) -> np.ndarray:
    """Add noise variation to texture.

    Args:
        texture: RGBA texture array
        base_color: Base RGBA color (0-255)
        scale: Noise scale
        intensity: Variation intensity
        seed: Random seed

    Returns:
        Modified texture
    """
    h, w = texture.shape[:2]
    noise = fbm_noise(w, h, scale, 3, 0.5, seed)

    # Apply noise to modulate color
    for c in range(3):  # RGB channels
        variation = (noise - 0.5) * 2 * intensity * 255
        texture[:, :, c] = np.clip(texture[:, :, c].astype(np.float32) + variation, 0, 255)

    return texture.astype(np.uint8)
```

### Establish Color Palette

Move from random colors to coherent palette:

```python
import numpy as np
from typing import List

def remap_to_palette(texture: np.ndarray, palette: List[np.ndarray]) -> np.ndarray:
    """Remap texture colors to nearest palette colors.

    Args:
        texture: RGBA texture array
        palette: List of RGBA color arrays

    Returns:
        Remapped texture
    """
    h, w = texture.shape[:2]
    result = texture.copy()

    for y in range(h):
        for x in range(w):
            pixel = texture[y, x, :3]

            # Find nearest palette color
            min_dist = float('inf')
            nearest = palette[0]

            for color in palette:
                dist = np.sum((pixel.astype(np.float32) - color[:3].astype(np.float32)) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    nearest = color

            result[y, x, :3] = nearest[:3]

    return result

# Example palette
RUSTIC_WOOD_PALETTE = [
    np.array([139, 90, 43, 255]),   # Dark wood
    np.array([160, 120, 70, 255]),  # Medium wood
    np.array([185, 150, 100, 255]), # Light wood
    np.array([120, 80, 40, 255]),   # Dark grain
]
```

### Basic Detail Addition

Add fundamental surface detail:

```python
import numpy as np

def add_wood_grain(texture: np.ndarray, density: float = 0.5,
                   waviness: float = 0.3, direction: tuple = (0, 1)) -> np.ndarray:
    """Add wood grain pattern to texture.

    Args:
        texture: RGBA texture array
        density: Grain line density
        waviness: Amount of grain waviness
        direction: Grain direction (dx, dy)

    Returns:
        Modified texture
    """
    h, w = texture.shape[:2]
    y_coords, x_coords = np.mgrid[0:h, 0:w]

    # Calculate grain lines
    dx, dy = direction
    grain_coord = (x_coords * dx + y_coords * dy) * density

    # Add waviness
    wave = np.sin(y_coords * 0.1) * waviness * 10
    grain_coord += wave

    # Create grain pattern
    grain = np.sin(grain_coord * 2 * np.pi / 10)
    grain = (grain + 1) / 2  # Normalize to 0-1

    # Darken texture in grain lines
    for c in range(3):
        texture[:, :, c] = np.clip(
            texture[:, :, c].astype(np.float32) * (0.8 + grain * 0.2),
            0, 255
        ).astype(np.uint8)

    return texture

def add_mottled_variation(texture: np.ndarray, scale: float = 4.0,
                          intensity: float = 0.2, seed: int = 42) -> np.ndarray:
    """Add mottled/stone-like variation.

    Args:
        texture: RGBA texture array
        scale: Variation scale
        intensity: Variation intensity

    Returns:
        Modified texture
    """
    h, w = texture.shape[:2]
    noise = fbm_noise(w, h, scale, 4, 0.6, seed)

    for c in range(3):
        variation = (noise - 0.5) * 2 * intensity * 255
        texture[:, :, c] = np.clip(
            texture[:, :, c].astype(np.float32) + variation,
            0, 255
        ).astype(np.uint8)

    return texture

def add_linear_brushing(texture: np.ndarray, direction: float = 45.0,
                        density: float = 0.8) -> np.ndarray:
    """Add linear brushing effect (for metal).

    Args:
        texture: RGBA texture array
        direction: Brush direction in degrees
        density: Brush line density

    Returns:
        Modified texture
    """
    h, w = texture.shape[:2]
    y_coords, x_coords = np.mgrid[0:h, 0:w]

    # Calculate brush direction
    angle_rad = direction * np.pi / 180
    brush_coord = x_coords * np.cos(angle_rad) + y_coords * np.sin(angle_rad)

    # Create brush lines
    brush = np.sin(brush_coord * density * 0.5) * 0.5 + 0.5

    # Apply subtle variation
    for c in range(3):
        texture[:, :, c] = np.clip(
            texture[:, :, c].astype(np.float32) * (0.95 + brush * 0.1),
            0, 255
        ).astype(np.uint8)

    return texture
```

---

## Temp → Final Upgrades

### Increase Contrast

Final-tier textures need dynamic range:

```python
import numpy as np
from dataclasses import dataclass

@dataclass
class HistogramStats:
    min_val: float
    max_val: float
    mean: float
    contrast: float

def analyze_histogram(texture: np.ndarray) -> HistogramStats:
    """Analyze texture histogram for contrast.

    Args:
        texture: RGBA texture array

    Returns:
        HistogramStats with min, max, mean, contrast
    """
    # Convert to grayscale for analysis
    gray = 0.299 * texture[:, :, 0] + 0.587 * texture[:, :, 1] + 0.114 * texture[:, :, 2]
    gray = gray / 255.0

    return HistogramStats(
        min_val=float(np.min(gray)),
        max_val=float(np.max(gray)),
        mean=float(np.mean(gray)),
        contrast=float(np.max(gray) - np.min(gray)),
    )

def apply_s_curve_contrast(texture: np.ndarray, factor: float = 1.5) -> np.ndarray:
    """Apply S-curve contrast enhancement.

    Args:
        texture: RGBA texture array
        factor: Contrast factor (>1 increases contrast)

    Returns:
        Contrast-enhanced texture
    """
    result = texture.copy().astype(np.float32)
    mid = 127.5

    for c in range(3):
        result[:, :, c] = mid + (result[:, :, c] - mid) * factor

    return np.clip(result, 0, 255).astype(np.uint8)

def enhance_contrast_if_needed(texture: np.ndarray, target_contrast: float = 0.4) -> np.ndarray:
    """Enhance contrast if below target.

    Args:
        texture: RGBA texture array
        target_contrast: Target contrast level (0-1)

    Returns:
        Enhanced texture
    """
    stats = analyze_histogram(texture)
    print(f"Current contrast: {stats.contrast:.2f}")

    if stats.contrast < target_contrast:
        factor = target_contrast / stats.contrast if stats.contrast > 0 else 1.5
        return apply_s_curve_contrast(texture, min(factor, 2.0))

    return texture
```

### Add Multiple Detail Layers

Layer details at different scales:

```python
import numpy as np
from enum import Enum

class BlendMode(Enum):
    NORMAL = 'normal'
    OVERLAY = 'overlay'
    SOFT_LIGHT = 'soft_light'

def blend_overlay(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    """Apply overlay blend mode."""
    mask = base < 128
    result = np.where(
        mask,
        (2 * base * blend) / 255,
        255 - (2 * (255 - base) * (255 - blend)) / 255
    )
    return np.clip(result, 0, 255).astype(np.uint8)

def blend_soft_light(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    """Apply soft light blend mode."""
    blend_norm = blend / 255.0
    base_norm = base / 255.0
    result = (1 - 2 * blend_norm) * base_norm ** 2 + 2 * blend_norm * base_norm
    return (result * 255).astype(np.uint8)

def add_detail_layer(texture: np.ndarray, scale: float, amplitude: float,
                     blend_mode: BlendMode, seed: int) -> np.ndarray:
    """Add a noise-based detail layer.

    Args:
        texture: RGBA texture array
        scale: Noise frequency scale
        amplitude: Layer opacity (0-1)
        blend_mode: How to blend the layer
        seed: Random seed

    Returns:
        Texture with added detail layer
    """
    h, w = texture.shape[:2]
    noise = fbm_noise(w, h, scale, 3, 0.5, seed)
    noise_rgb = (noise * 255).astype(np.uint8)

    result = texture.copy()

    for c in range(3):
        if blend_mode == BlendMode.NORMAL:
            result[:, :, c] = (texture[:, :, c] * (1 - amplitude) +
                              noise_rgb * amplitude).astype(np.uint8)
        elif blend_mode == BlendMode.OVERLAY:
            blended = blend_overlay(texture[:, :, c], noise_rgb)
            result[:, :, c] = (texture[:, :, c] * (1 - amplitude) +
                              blended * amplitude).astype(np.uint8)
        elif blend_mode == BlendMode.SOFT_LIGHT:
            blended = blend_soft_light(texture[:, :, c], noise_rgb)
            result[:, :, c] = (texture[:, :, c] * (1 - amplitude) +
                              blended * amplitude).astype(np.uint8)

    return result

def add_multi_layer_detail(texture: np.ndarray, seed: int = 42) -> np.ndarray:
    """Add multiple detail layers at different scales.

    Args:
        texture: RGBA texture array
        seed: Base random seed

    Returns:
        Texture with multi-scale detail
    """
    # Layer 1: Large-scale variation (base)
    texture = add_detail_layer(texture, 2.0, 0.3, BlendMode.NORMAL, seed)

    # Layer 2: Medium detail
    texture = add_detail_layer(texture, 8.0, 0.2, BlendMode.OVERLAY, seed + 1)

    # Layer 3: Fine detail
    texture = add_detail_layer(texture, 32.0, 0.1, BlendMode.SOFT_LIGHT, seed + 2)

    return texture
```

### Color Richness

Add color depth through subtle hue variation:

```python
import numpy as np
import colorsys

def rgb_to_hsv(rgb: np.ndarray) -> tuple:
    """Convert RGB (0-255) to HSV (0-1)."""
    r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    return colorsys.rgb_to_hsv(r, g, b)

def hsv_to_rgb(h: float, s: float, v: float) -> np.ndarray:
    """Convert HSV (0-1) to RGB (0-255)."""
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return np.array([int(r * 255), int(g * 255), int(b * 255)], dtype=np.uint8)

def add_hue_variation(texture: np.ndarray, hue_range: float = 0.05,
                      seed: int = 42) -> np.ndarray:
    """Add subtle hue variation based on noise.

    Args:
        texture: RGBA texture array
        hue_range: Maximum hue shift (fraction of color wheel)
        seed: Random seed

    Returns:
        Texture with hue variation
    """
    h, w = texture.shape[:2]
    noise = fbm_noise(w, h, 4.0, 2, 0.5, seed)
    noise = (noise - 0.5) * 2 * hue_range  # -hue_range to +hue_range

    result = texture.copy()

    for y in range(h):
        for x in range(w):
            rgb = texture[y, x, :3]
            hsv = rgb_to_hsv(rgb)
            new_h = (hsv[0] + noise[y, x]) % 1.0
            new_rgb = hsv_to_rgb(new_h, hsv[1], hsv[2])
            result[y, x, :3] = new_rgb

    return result

def apply_color_balance(texture: np.ndarray,
                       shadow_tint: tuple = (1.05, 0.95, 0.9),
                       highlight_tint: tuple = (0.95, 0.98, 1.05)) -> np.ndarray:
    """Apply warm shadows and cool highlights.

    Args:
        texture: RGBA texture array
        shadow_tint: RGB multipliers for shadows
        highlight_tint: RGB multipliers for highlights

    Returns:
        Color-balanced texture
    """
    result = texture.copy().astype(np.float32)

    # Calculate luminance
    lum = 0.299 * result[:, :, 0] + 0.587 * result[:, :, 1] + 0.114 * result[:, :, 2]
    lum_norm = lum / 255.0

    for c in range(3):
        # Blend between shadow and highlight tint based on luminance
        tint = shadow_tint[c] * (1 - lum_norm) + highlight_tint[c] * lum_norm
        result[:, :, c] = result[:, :, c] * tint

    return np.clip(result, 0, 255).astype(np.uint8)
```

### Add MRE Channel

Create material response textures:

```python
import numpy as np

def calculate_local_variance(texture: np.ndarray, x: int, y: int, radius: int) -> float:
    """Calculate local variance around a pixel for roughness estimation."""
    h, w = texture.shape[:2]
    x_start = max(0, x - radius)
    x_end = min(w, x + radius + 1)
    y_start = max(0, y - radius)
    y_end = min(h, y + radius + 1)

    region = texture[y_start:y_end, x_start:x_end, :3].astype(np.float32)
    return float(np.var(region))

def rgb_to_saturation(rgb: np.ndarray) -> float:
    """Calculate saturation from RGB values (0-255)."""
    r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    return (max_c - min_c) / max_c if max_c > 0 else 0

def generate_mre_from_albedo(albedo: np.ndarray) -> np.ndarray:
    """Generate MRE (Metallic, Roughness, Emission) texture from albedo.

    Args:
        albedo: RGBA albedo texture

    Returns:
        MRE texture (R=Metallic, G=Roughness, B=Emission, A=255)
    """
    h, w = albedo.shape[:2]
    mre = np.zeros((h, w, 4), dtype=np.uint8)
    mre[:, :, 3] = 255  # Full alpha

    for y in range(h):
        for x in range(w):
            pixel = albedo[y, x, :3]

            # Metallic: based on saturation (low sat = potentially metallic)
            saturation = rgb_to_saturation(pixel)
            metallic = int((1.0 - saturation) * 255 * 0.5)  # Scale down, most things aren't metal

            # Roughness: based on local variance (more detail = rougher)
            variance = calculate_local_variance(albedo, x, y, 2)
            roughness = int(min(1.0, variance / 1000) * 255)

            # Emission: none for most materials
            emission = 0

            mre[y, x, 0] = metallic
            mre[y, x, 1] = max(64, roughness)  # Minimum roughness
            mre[y, x, 2] = emission

    return mre
```

### Improve Edge Definition

Sharpen important edges:

```python
import numpy as np
from scipy import ndimage

def unsharp_mask(texture: np.ndarray, radius: float = 1.0,
                 amount: float = 0.5, threshold: int = 3) -> np.ndarray:
    """Apply unsharp mask for detail enhancement.

    Args:
        texture: RGBA texture array
        radius: Blur radius for mask
        amount: Sharpening amount
        threshold: Minimum difference to sharpen

    Returns:
        Sharpened texture
    """
    result = texture.copy().astype(np.float32)

    for c in range(3):
        channel = result[:, :, c]

        # Create blurred version
        blurred = ndimage.gaussian_filter(channel, sigma=radius)

        # Calculate difference
        diff = channel - blurred

        # Apply threshold
        mask = np.abs(diff) > threshold

        # Apply sharpening
        channel[mask] = channel[mask] + diff[mask] * amount

        result[:, :, c] = channel

    return np.clip(result, 0, 255).astype(np.uint8)

def smart_sharpen(texture: np.ndarray, radius: float = 0.5,
                  amount: float = 0.3, edge_threshold: float = 0.1) -> np.ndarray:
    """Edge-aware sharpening that preserves smooth gradients.

    Args:
        texture: RGBA texture array
        radius: Sharpening radius
        amount: Sharpening strength
        edge_threshold: Edge detection threshold

    Returns:
        Sharpened texture
    """
    result = texture.copy().astype(np.float32)

    for c in range(3):
        channel = result[:, :, c]

        # Detect edges using Sobel
        sobel_x = ndimage.sobel(channel, axis=1)
        sobel_y = ndimage.sobel(channel, axis=0)
        edges = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
        edge_mask = edges > (edge_threshold * 255)

        # Apply sharpening only at edges
        blurred = ndimage.gaussian_filter(channel, sigma=radius)
        diff = channel - blurred
        channel[edge_mask] = channel[edge_mask] + diff[edge_mask] * amount

        result[:, :, c] = channel

    return np.clip(result, 0, 255).astype(np.uint8)
```

---

## Final → Hero Upgrades

### Add Wear and Damage

Hero textures show signs of use:

```python
import numpy as np
from scipy import ndimage

def apply_edge_wear(texture: np.ndarray, detection_radius: int = 2,
                    intensity: float = 0.3) -> np.ndarray:
    """Apply edge wear effect (lighter on edges).

    Args:
        texture: RGBA texture array
        detection_radius: Radius for edge detection
        intensity: Wear intensity (0-1)

    Returns:
        Texture with edge wear applied
    """
    result = texture.copy().astype(np.float32)

    # Detect edges using gradient magnitude
    gray = 0.299 * result[:, :, 0] + 0.587 * result[:, :, 1] + 0.114 * result[:, :, 2]
    sobel_x = ndimage.sobel(gray, axis=1)
    sobel_y = ndimage.sobel(gray, axis=0)
    edges = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
    edges = ndimage.gaussian_filter(edges, sigma=detection_radius)
    edges = edges / (edges.max() + 1e-8)  # Normalize

    # Lighten edges
    for c in range(3):
        result[:, :, c] += edges * intensity * 255

    return np.clip(result, 0, 255).astype(np.uint8)

def apply_cavity_dirt(texture: np.ndarray, detection_radius: int = 3,
                      intensity: float = 0.4,
                      dirt_color: tuple = (50, 40, 30)) -> np.ndarray:
    """Apply cavity darkening (dirt in recesses).

    Args:
        texture: RGBA texture array
        detection_radius: Radius for cavity detection
        intensity: Dirt intensity (0-1)
        dirt_color: RGB color for dirt

    Returns:
        Texture with cavity dirt applied
    """
    result = texture.copy().astype(np.float32)

    # Detect cavities using inverted edge detection
    gray = 0.299 * result[:, :, 0] + 0.587 * result[:, :, 1] + 0.114 * result[:, :, 2]
    blurred = ndimage.gaussian_filter(gray, sigma=detection_radius)
    cavities = np.maximum(0, blurred - gray)
    cavities = cavities / (cavities.max() + 1e-8)

    # Blend dirt color into cavities
    for c in range(3):
        result[:, :, c] = result[:, :, c] * (1 - cavities * intensity) + dirt_color[c] * cavities * intensity

    return np.clip(result, 0, 255).astype(np.uint8)

def add_scratches(texture: np.ndarray, density: float = 0.3,
                  length_range: tuple = (0.1, 0.4), width: int = 1,
                  depth: float = 0.2, seed: int = 42) -> np.ndarray:
    """Add random scratches to texture.

    Args:
        texture: RGBA texture array
        density: Scratch density (0-1)
        length_range: Min/max scratch length as fraction of texture size
        width: Scratch width in pixels
        depth: Scratch darkness (0-1)
        seed: Random seed

    Returns:
        Texture with scratches
    """
    h, w = texture.shape[:2]
    result = texture.copy()
    np.random.seed(seed)

    num_scratches = int(density * 50)
    min_len = int(length_range[0] * min(h, w))
    max_len = int(length_range[1] * min(h, w))

    for _ in range(num_scratches):
        # Random start point and direction
        x0 = np.random.randint(0, w)
        y0 = np.random.randint(0, h)
        angle = np.random.uniform(0, 2 * np.pi)
        length = np.random.randint(min_len, max_len + 1)

        # Draw scratch line
        for i in range(length):
            x = int(x0 + i * np.cos(angle))
            y = int(y0 + i * np.sin(angle))
            if 0 <= x < w and 0 <= y < h:
                for dx in range(-width // 2, width // 2 + 1):
                    for dy in range(-width // 2, width // 2 + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            result[ny, nx, :3] = (result[ny, nx, :3].astype(np.float32) * (1 - depth)).astype(np.uint8)

    return result
```

### Add All Material Channels

Complete material description:

```python
import numpy as np
from scipy import ndimage

def generate_height_from_albedo(albedo: np.ndarray) -> np.ndarray:
    """Generate height map from albedo (luminance-based).

    Args:
        albedo: RGBA albedo texture

    Returns:
        Single-channel height map (0-255)
    """
    # Convert to grayscale
    gray = 0.299 * albedo[:, :, 0] + 0.587 * albedo[:, :, 1] + 0.114 * albedo[:, :, 2]
    return gray.astype(np.uint8)

def generate_detail_normal(albedo: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """Generate normal map from albedo using Sobel operators.

    Args:
        albedo: RGBA albedo texture
        strength: Normal map strength

    Returns:
        RGB normal map (128,128,255 = flat)
    """
    h, w = albedo.shape[:2]
    gray = 0.299 * albedo[:, :, 0] + 0.587 * albedo[:, :, 1] + 0.114 * albedo[:, :, 2]

    # Calculate gradients
    dx = ndimage.sobel(gray, axis=1) * strength
    dy = ndimage.sobel(gray, axis=0) * strength

    # Create normal map
    normal = np.zeros((h, w, 4), dtype=np.uint8)
    normal[:, :, 0] = np.clip(128 + dx, 0, 255).astype(np.uint8)
    normal[:, :, 1] = np.clip(128 + dy, 0, 255).astype(np.uint8)
    normal[:, :, 2] = 255  # Z always pointing out
    normal[:, :, 3] = 255

    return normal

def generate_sse(albedo: np.ndarray, subsurface_intensity: float = 0.3) -> np.ndarray:
    """Generate SSE (Subsurface Scattering) texture.

    Args:
        albedo: RGBA albedo texture
        subsurface_intensity: SSE intensity

    Returns:
        SSE texture (R=Subsurface, G=Specular, B=Emission, A=255)
    """
    h, w = albedo.shape[:2]
    sse = np.zeros((h, w, 4), dtype=np.uint8)

    # Subsurface from warm colors
    warmth = (albedo[:, :, 0].astype(np.float32) - albedo[:, :, 2]) / 255
    sse[:, :, 0] = (np.clip(warmth * subsurface_intensity, 0, 1) * 255).astype(np.uint8)

    # Specular from saturation
    sse[:, :, 1] = 128  # Default mid specular

    # Emission (none by default)
    sse[:, :, 2] = 0
    sse[:, :, 3] = 255

    return sse
```

### Subtle Variations

No two areas should look identical:

```python
import numpy as np

def add_micro_variation(texture: np.ndarray, scale: float = 64.0,
                        amplitude: float = 0.03, seed: int = 42) -> np.ndarray:
    """Add high-frequency micro variation.

    Args:
        texture: RGBA texture array
        scale: Noise frequency (higher = finer detail)
        amplitude: Variation amplitude (0-1)
        seed: Random seed

    Returns:
        Texture with micro variation
    """
    h, w = texture.shape[:2]
    noise = fbm_noise(w, h, scale, 2, 0.5, seed)
    noise = (noise - 0.5) * 2 * amplitude * 255

    result = texture.copy().astype(np.float32)
    for c in range(3):
        result[:, :, c] += noise
    return np.clip(result, 0, 255).astype(np.uint8)

def add_color_pools(texture: np.ndarray, scale: float = 4.0,
                    hue_var: float = 0.02, sat_var: float = 0.05,
                    seed: int = 42) -> np.ndarray:
    """Add larger-scale color pooling variation.

    Args:
        texture: RGBA texture array
        scale: Pool scale
        hue_var: Hue variance
        sat_var: Saturation variance
        seed: Random seed

    Returns:
        Texture with color pools
    """
    # Uses add_hue_variation with low frequency
    return add_hue_variation(texture, hue_var, seed)
```

### Perfect Tiling

Ensure seamless tiling at hero quality:

```python
import numpy as np

def analyze_seam_visibility(texture: np.ndarray) -> float:
    """Analyze how visible the texture seams are.

    Args:
        texture: RGBA texture array

    Returns:
        Seam visibility score (0 = seamless, higher = more visible)
    """
    h, w = texture.shape[:2]

    # Compare left edge to right edge
    left = texture[:, 0, :3].astype(np.float32)
    right = texture[:, -1, :3].astype(np.float32)
    h_diff = np.mean(np.abs(left - right)) / 255

    # Compare top edge to bottom edge
    top = texture[0, :, :3].astype(np.float32)
    bottom = texture[-1, :, :3].astype(np.float32)
    v_diff = np.mean(np.abs(top - bottom)) / 255

    return float((h_diff + v_diff) / 2)

def blend_edges_for_tiling(texture: np.ndarray, blend_width: int = None) -> np.ndarray:
    """Blend texture edges for seamless tiling.

    Args:
        texture: RGBA texture array
        blend_width: Width of blend region (default: width/8)

    Returns:
        Texture with blended edges
    """
    h, w = texture.shape[:2]
    if blend_width is None:
        blend_width = w // 8

    result = texture.copy().astype(np.float32)

    # Horizontal blend
    for x in range(blend_width):
        t = x / blend_width
        result[:, x] = texture[:, x] * (1 - t) + np.roll(texture, -w, axis=1)[:, x] * t
        result[:, -x - 1] = texture[:, -x - 1] * (1 - t) + np.roll(texture, w, axis=1)[:, -x - 1] * t

    # Vertical blend
    for y in range(blend_width):
        t = y / blend_width
        result[y, :] = result[y, :] * (1 - t) + np.roll(result, -h, axis=0)[y, :] * t
        result[-y - 1, :] = result[-y - 1, :] * (1 - t) + np.roll(result, h, axis=0)[-y - 1, :] * t

    return np.clip(result, 0, 255).astype(np.uint8)
```

### Resolution Upgrade

Increase resolution for hero assets:

```python
import numpy as np
from PIL import Image

def upscale_texture(texture: np.ndarray, factor: int = 2,
                    method: str = 'lanczos') -> np.ndarray:
    """Upscale texture with detail preservation.

    Args:
        texture: RGBA texture array
        factor: Scale factor (2 = double size)
        method: Resampling method ('lanczos', 'bicubic', 'bilinear')

    Returns:
        Upscaled texture
    """
    h, w = texture.shape[:2]
    new_w, new_h = w * factor, h * factor

    resample_methods = {
        'lanczos': Image.LANCZOS,
        'bicubic': Image.BICUBIC,
        'bilinear': Image.BILINEAR,
    }
    resample = resample_methods.get(method.lower(), Image.LANCZOS)

    img = Image.fromarray(texture)
    upscaled = img.resize((new_w, new_h), resample=resample)

    return np.array(upscaled)

def add_post_upscale_detail(texture: np.ndarray, amplitude: float = 0.05,
                            seed: int = 42) -> np.ndarray:
    """Add high-frequency detail after upscaling.

    Args:
        texture: RGBA upscaled texture
        amplitude: Detail amplitude
        seed: Random seed

    Returns:
        Texture with added detail
    """
    h, w = texture.shape[:2]
    scale = w / 4.0
    return add_detail_layer(texture, scale, amplitude, BlendMode.OVERLAY, seed)
```

---

## Contrast Enhancement Techniques

### Histogram Analysis

```python
import numpy as np
from dataclasses import dataclass

@dataclass
class ContrastReport:
    min_val: float
    max_val: float
    range_val: float
    mean: float
    std_dev: float

def analyze_contrast(texture: np.ndarray) -> ContrastReport:
    """Analyze texture contrast using histogram.

    Args:
        texture: RGBA texture array

    Returns:
        ContrastReport with percentile-based statistics
    """
    # Convert to luminance
    gray = (0.299 * texture[:, :, 0] + 0.587 * texture[:, :, 1] +
            0.114 * texture[:, :, 2]) / 255.0

    return ContrastReport(
        min_val=float(np.percentile(gray, 1)),   # Ignore outliers
        max_val=float(np.percentile(gray, 99)),
        range_val=float(np.percentile(gray, 99) - np.percentile(gray, 1)),
        mean=float(np.mean(gray)),
        std_dev=float(np.std(gray)),
    )

# Target values by tier
# Placeholder: range 0.1-0.2
# Temp: range 0.2-0.4
# Final: range 0.4-0.6
# Hero: range 0.5-0.7
```

### Contrast Correction

```python
import numpy as np
from dataclasses import dataclass

@dataclass
class Levels:
    input_black: float
    input_white: float
    output_black: float
    output_white: float
    gamma: float = 1.0

def apply_levels(texture: np.ndarray, levels: Levels) -> np.ndarray:
    """Apply levels adjustment to texture.

    Args:
        texture: RGBA texture array
        levels: Levels parameters

    Returns:
        Adjusted texture
    """
    result = texture.copy().astype(np.float32) / 255.0

    for c in range(3):
        # Normalize input range
        channel = result[:, :, c]
        channel = (channel - levels.input_black) / (levels.input_white - levels.input_black + 1e-8)
        channel = np.clip(channel, 0, 1)

        # Apply gamma
        channel = np.power(channel, levels.gamma)

        # Map to output range
        channel = channel * (levels.output_white - levels.output_black) + levels.output_black

        result[:, :, c] = channel

    return (np.clip(result, 0, 1) * 255).astype(np.uint8)

def enhance_contrast(texture: np.ndarray, target_range: float) -> np.ndarray:
    """Enhance texture contrast to target range.

    Args:
        texture: RGBA texture array
        target_range: Target contrast range (0-1)

    Returns:
        Contrast-enhanced texture
    """
    current = analyze_contrast(texture)

    if current.range_val < target_range * 0.8:
        # Need more contrast
        levels = Levels(
            input_black=current.min_val,
            input_white=current.max_val,
            output_black=0.5 - target_range / 2.0,
            output_white=0.5 + target_range / 2.0,
            gamma=1.0,
        )
        return apply_levels(texture, levels)

    return texture
```

---

## Color Richness Techniques

### Saturation by Tier

| Tier | Saturation Range | Notes |
|------|------------------|-------|
| Placeholder | 0.0-0.3 | Grayscale or muted |
| Temp | 0.2-0.5 | Basic color |
| Final | 0.3-0.6 | Rich but not garish |
| Hero | 0.4-0.7 | Full color depth |

### Adding Color Depth

```python
import numpy as np
import colorsys

def apply_vibrance(texture: np.ndarray, amount: float = 0.3) -> np.ndarray:
    """Boost low-saturation colors (vibrance).

    Args:
        texture: RGBA texture array
        amount: Vibrance amount (0-1)

    Returns:
        Vibrance-adjusted texture
    """
    result = texture.copy()
    h, w = texture.shape[:2]

    for y in range(h):
        for x in range(w):
            r, g, b = texture[y, x, :3] / 255.0
            h_val, s, v = colorsys.rgb_to_hsv(r, g, b)

            # Boost more for low saturation colors
            boost = amount * (1.0 - s)
            new_s = min(1.0, s + boost)

            r, g, b = colorsys.hsv_to_rgb(h_val, new_s, v)
            result[y, x, :3] = np.array([r, g, b]) * 255

    return result.astype(np.uint8)

def split_tone(texture: np.ndarray,
               highlight_hsl: tuple = (0.1, 0.3, 0.7),
               shadow_hsl: tuple = (0.6, 0.2, 0.3),
               balance: float = 0.0) -> np.ndarray:
    """Apply split toning (warm highlights, cool shadows).

    Args:
        texture: RGBA texture array
        highlight_hsl: HSL tuple for highlights (h, s, l)
        shadow_hsl: HSL tuple for shadows (h, s, l)
        balance: Balance between shadows and highlights (-1 to 1)

    Returns:
        Split-toned texture
    """
    result = texture.copy().astype(np.float32)

    # Calculate luminance
    lum = (0.299 * result[:, :, 0] + 0.587 * result[:, :, 1] +
           0.114 * result[:, :, 2]) / 255.0

    # Convert HSL to RGB for tint colors
    h_r, h_g, h_b = colorsys.hls_to_rgb(highlight_hsl[0], highlight_hsl[2], highlight_hsl[1])
    s_r, s_g, s_b = colorsys.hls_to_rgb(shadow_hsl[0], shadow_hsl[2], shadow_hsl[1])

    highlight_rgb = np.array([h_r, h_g, h_b]) * 255
    shadow_rgb = np.array([s_r, s_g, s_b]) * 255

    # Apply tinting based on luminance
    for c in range(3):
        shadow_amount = (1 - lum) * (0.5 - balance * 0.5) * 0.2
        highlight_amount = lum * (0.5 + balance * 0.5) * 0.2

        result[:, :, c] = (result[:, :, c] +
                          shadow_rgb[c] * shadow_amount +
                          highlight_rgb[c] * highlight_amount)

    return np.clip(result, 0, 255).astype(np.uint8)

# Example usage:
# texture = apply_vibrance(texture, 0.3)
# texture = split_tone(texture,
#     highlight_hsl=(0.08, 0.3, 0.7),  # Warm highlights
#     shadow_hsl=(0.58, 0.2, 0.3),     # Cool shadows
#     balance=0.0)
```

---

## Detail Layer System

### Layer Stack Structure

```
Layer 4: Micro detail (64x scale) - 5%
Layer 3: Fine detail (32x scale) - 10%
Layer 2: Medium detail (8x scale) - 20%
Layer 1: Large variation (2x scale) - 30%
Layer 0: Base color - 100%
```

### Implementation

```python
import numpy as np
from enum import Enum, auto
from dataclasses import dataclass

class Tier(Enum):
    PLACEHOLDER = auto()
    TEMP = auto()
    FINAL = auto()
    HERO = auto()

@dataclass
class StyleToken:
    seed: int
    wear_amount: float = 0.2

def get_texture_resolution(tier: Tier) -> int:
    """Get texture resolution for tier."""
    resolutions = {
        Tier.PLACEHOLDER: 64,
        Tier.TEMP: 128,
        Tier.FINAL: 256,
        Tier.HERO: 512,
    }
    return resolutions.get(tier, 128)

def generate_noise(scale: float, seed: int, size: int) -> np.ndarray:
    """Generate noise texture at given scale."""
    return fbm_noise(size, size, scale, 3, 0.5, seed)

def build_layered_texture(base_color: np.ndarray, style: StyleToken,
                          tier: Tier) -> np.ndarray:
    """Build a layered texture with tier-appropriate detail.

    Args:
        base_color: RGBA base color (0-255)
        style: Style token with seed and parameters
        tier: Target quality tier

    Returns:
        Layered RGBA texture
    """
    size = get_texture_resolution(tier)
    texture = np.zeros((size, size, 4), dtype=np.uint8)

    # Base fill
    texture[:, :] = base_color

    # Large variation (all tiers)
    texture = add_detail_layer(texture, 2.0, 0.3, BlendMode.OVERLAY, style.seed)

    if tier.value >= Tier.TEMP.value:
        # Medium detail
        texture = add_detail_layer(texture, 8.0, 0.2, BlendMode.SOFT_LIGHT,
                                   style.seed + 1)

    if tier.value >= Tier.FINAL.value:
        # Fine detail
        texture = add_detail_layer(texture, 32.0, 0.1, BlendMode.OVERLAY,
                                   style.seed + 2)

    if tier.value >= Tier.HERO.value:
        # Micro detail
        texture = add_detail_layer(texture, 64.0, 0.05, BlendMode.SOFT_LIGHT,
                                   style.seed + 3)

        # Wear and imperfections
        texture = apply_edge_wear(texture, intensity=style.wear_amount)
        texture = apply_cavity_dirt(texture, intensity=style.wear_amount * 0.5)

    return texture
```

---

## Resolution Guidelines

### Resolution by Tier and Asset Size

| Asset Size | Placeholder | Temp | Final | Hero |
|------------|-------------|------|-------|------|
| Tiny (< 0.5m) | 32x32 | 64x64 | 128x128 | 256x256 |
| Small (0.5-1m) | 64x64 | 128x128 | 256x256 | 512x512 |
| Medium (1-2m) | 64x64 | 128x128 | 256x256 | 512x512 |
| Large (2-5m) | 128x128 | 256x256 | 512x512 | 512x512 |
| Huge (> 5m) | 128x128 | 256x256 | 512x512 | 512x512* |

*Hero huge assets may need tiling or detail textures.

### Memory Budget Check

```python
import numpy as np
from enum import Enum, auto

class Tier(Enum):
    PLACEHOLDER = auto()
    TEMP = auto()
    FINAL = auto()
    HERO = auto()

def check_texture_budget(texture: np.ndarray, tier: Tier) -> bool:
    """Check if texture fits within tier memory budget.

    Args:
        texture: RGBA texture array
        tier: Target quality tier

    Returns:
        True if texture fits budget, False otherwise
    """
    max_bytes = {
        Tier.PLACEHOLDER: 16 * 1024,   # 16 KB
        Tier.TEMP: 64 * 1024,          # 64 KB
        Tier.FINAL: 256 * 1024,        # 256 KB
        Tier.HERO: 1024 * 1024,        # 1 MB
    }

    h, w = texture.shape[:2]
    tex_bytes = w * h * 4  # RGBA
    return tex_bytes <= max_bytes.get(tier, 64 * 1024)
```
