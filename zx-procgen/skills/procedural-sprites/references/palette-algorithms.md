# Palette Algorithms

Color quantization algorithms for reducing full-color images to limited palettes.

## Median Cut Algorithm

Split color space recursively along the widest channel:

```rust
/// Generate indexed palette using median cut
fn generate_palette(colors: &[u32], max_colors: usize) -> Vec<u32> {
    let mut buckets = vec![colors.to_vec()];

    while buckets.len() < max_colors {
        // Find bucket with widest color range
        let (idx, axis) = find_widest_bucket(&buckets);
        let bucket = buckets.remove(idx);

        // Split along widest axis (R, G, or B)
        let (low, high) = split_bucket(&bucket, axis);
        buckets.push(low);
        buckets.push(high);
    }

    // Average each bucket to get palette color
    buckets.iter().map(|b| average_color(b)).collect()
}

fn find_widest_bucket(buckets: &[Vec<u32>]) -> (usize, usize) {
    buckets.iter().enumerate()
        .map(|(i, b)| (i, channel_range(b)))
        .max_by_key(|(_, (_, range))| *range)
        .map(|(i, (axis, _))| (i, axis))
        .unwrap_or((0, 0))
}
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

```rust
fn quantize_to_palette(color: u32, palette: &[u32]) -> u32 {
    palette.iter()
        .min_by_key(|&&p| color_distance(color, p))
        .copied()
        .unwrap_or(color)
}

fn color_distance(a: u32, b: u32) -> u32 {
    let dr = ((a >> 24) & 0xFF) as i32 - ((b >> 24) & 0xFF) as i32;
    let dg = ((a >> 16) & 0xFF) as i32 - ((b >> 16) & 0xFF) as i32;
    let db = ((a >> 8) & 0xFF) as i32 - ((b >> 8) & 0xFF) as i32;
    (dr * dr + dg * dg + db * db) as u32
}
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
