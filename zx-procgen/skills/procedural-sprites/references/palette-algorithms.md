# Palette Algorithms

Color quantization algorithms for reducing full-color images to limited palettes.

## Median Cut Algorithm

Split color space recursively along the widest channel:

```python
import numpy as np

def generate_palette(colors: np.ndarray, max_colors: int) -> np.ndarray:
    """
    Generate indexed palette using median cut algorithm.

    Args:
        colors: Array of RGB colors, shape (N, 3)
        max_colors: Maximum number of palette colors

    Returns:
        Palette array of shape (max_colors, 3)
    """
    buckets = [colors.copy()]

    while len(buckets) < max_colors:
        # Find bucket with widest color range
        idx, axis = find_widest_bucket(buckets)
        bucket = buckets.pop(idx)

        # Split along widest axis (R=0, G=1, B=2)
        low, high = split_bucket(bucket, axis)
        buckets.append(low)
        buckets.append(high)

    # Average each bucket to get palette color
    return np.array([bucket.mean(axis=0) for bucket in buckets], dtype=np.uint8)

def find_widest_bucket(buckets: list[np.ndarray]) -> tuple[int, int]:
    """Find bucket with widest color range and return (bucket_idx, axis)."""
    best_idx, best_axis, best_range = 0, 0, 0

    for i, bucket in enumerate(buckets):
        for axis in range(3):  # R, G, B
            channel_range = bucket[:, axis].max() - bucket[:, axis].min()
            if channel_range > best_range:
                best_idx, best_axis, best_range = i, axis, channel_range

    return best_idx, best_axis

def split_bucket(bucket: np.ndarray, axis: int) -> tuple[np.ndarray, np.ndarray]:
    """Split bucket at median along specified axis."""
    median = np.median(bucket[:, axis])
    low = bucket[bucket[:, axis] <= median]
    high = bucket[bucket[:, axis] > median]
    return low, high
```

## Python Implementation

```python
from PIL import Image
import numpy as np

def generate_palette(image_path, num_colors=16):
    """Extract palette using PIL's quantize."""
    img = Image.open(image_path).convert('RGB')
    quantized = img.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette()[:num_colors * 3]

    # Convert to 0xRRGGBBAA format
    return [
        (palette[i] << 24) | (palette[i+1] << 16) | (palette[i+2] << 8) | 0xFF
        for i in range(0, len(palette), 3)
    ]
```

## Quantizing Pixels to Palette

```python
import numpy as np

def quantize_to_palette(color: np.ndarray, palette: np.ndarray) -> np.ndarray:
    """
    Find nearest palette color for a given color.

    Args:
        color: RGB color as array of shape (3,) or (H, W, 3)
        palette: Palette colors as array of shape (N, 3)

    Returns:
        Nearest palette color(s)
    """
    if color.ndim == 1:
        # Single color
        distances = color_distance(color, palette)
        return palette[np.argmin(distances)]
    else:
        # Image array - vectorized quantization
        h, w = color.shape[:2]
        flat = color.reshape(-1, 3)
        distances = np.linalg.norm(flat[:, np.newaxis] - palette, axis=2)
        indices = np.argmin(distances, axis=1)
        return palette[indices].reshape(h, w, 3)

def color_distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Calculate squared Euclidean distance between colors.

    Args:
        a: Single color (3,) or multiple colors (N, 3)
        b: Palette colors (M, 3)

    Returns:
        Distance array
    """
    # Squared Euclidean distance (no sqrt needed for comparison)
    diff = a.astype(np.int32) - b.astype(np.int32)
    return np.sum(diff ** 2, axis=-1)
```

## Algorithm Comparison

| Algorithm | Quality | Speed | Best For |
|-----------|---------|-------|----------|
| Median Cut | Good | Fast | General purpose |
| K-means | Better | Slow | When quality matters |
| Octree | Good | Fast | Large images |
| Popularity | Fair | Fast | Simple cases |

## K-means Refinement

For higher quality, refine median cut with k-means iterations:

```python
def kmeans_refine(image, initial_palette, iterations=10):
    """Refine palette using k-means clustering."""
    pixels = np.array(image).reshape(-1, 3)
    centers = np.array(initial_palette)

    for _ in range(iterations):
        # Assign pixels to nearest center
        distances = np.linalg.norm(pixels[:, None] - centers, axis=2)
        labels = np.argmin(distances, axis=1)

        # Update centers to cluster means
        for i in range(len(centers)):
            mask = labels == i
            if mask.any():
                centers[i] = pixels[mask].mean(axis=0)

    return centers.astype(np.uint8)
```
