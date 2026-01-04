# BC5 Texture Format for Normal Maps

BC5 is the optimal compression format for normal maps, providing high quality with efficient storage.

## Why BC5?

| Format | BPP | Channels | Quality for Normals |
|--------|-----|----------|---------------------|
| RGBA8 | 32 | 4 | Perfect but huge |
| BC7 | 8 | 4 | Good but overkill (has alpha) |
| **BC5** | **8** | **2** | **Optimal** (RG only, high quality) |

**Key insight:** Normal maps only need X and Y. Z is reconstructed mathematically:

```
z = sqrt(1 - x² - y²)
```

BC5 dedicates all bits to RG channels, giving better quality than BC7 for the same file size.

---

## Channel Encoding

### Tangent Space Mapping

| Channel | Axis | Stored Value | Decoded Range |
|---------|------|--------------|---------------|
| R | X (Tangent) | 0-255 | [-1, +1] |
| G | Y (Bitangent) | 0-255 | [-1, +1] |
| (B) | Z (Normal) | *Reconstructed* | [0, +1] |

**Encoding formula:** `stored = (value + 1) * 0.5 * 255`
**Decoding formula:** `value = stored / 255 * 2 - 1`

### Neutral Normal

A flat surface pointing straight out has:
- X = 0 (no left/right deviation)
- Y = 0 (no up/down deviation)
- Z = 1 (pointing forward)

**Encoded as:** RGB(128, 128, 255)

In BC5: RG(128, 128) → X=0, Y=0 → Z = sqrt(1 - 0 - 0) = 1

---

## Compression Details

### Block Structure

BC5 compresses 4×4 pixel blocks into 16 bytes:
- 8 bytes for R channel (same as BC4)
- 8 bytes for G channel (same as BC4)

Each channel uses 2 reference values + 48 bits of indices (3 bits per pixel).

### Quality Characteristics

- **High precision:** 8 interpolated values per channel
- **No cross-channel artifacts:** R and G compressed independently
- **Block artifacts:** Visible on extreme gradients (rare in normal maps)

### Size Calculation

```python
def bc5_size(width: int, height: int) -> int:
    """Calculate BC5 compressed texture size in bytes.

    BC5 uses 16 bytes per 4x4 block.
    """
    blocks_x = (width + 3) // 4
    blocks_y = (height + 3) // 4
    return blocks_x * blocks_y * 16


# Examples:
# 64 × 64   = 16 × 16 blocks × 16 bytes = 4,096 bytes (4 KB)
# 128 × 128 = 32 × 32 blocks × 16 bytes = 16,384 bytes (16 KB)
# 256 × 256 = 64 × 64 blocks × 16 bytes = 65,536 bytes (64 KB)
```

**Note:** The spec says BC5 = (width × height) / 2 bytes, which is equivalent for power-of-2 textures.

---

## Auto-Detection in Asset Pipeline

The `nether-cli` asset pipeline auto-selects BC5 for normal maps:

### Detection Rules

1. **Filename convention:** Files ending in `_normal.png` or `_n.png`
2. **Channel count:** 2-3 channel images (no alpha)
3. **Compression enabled:** `compress = true` in nether.toml (default)

### nether.toml Configuration

```toml
# Normal map with auto-detection
[[assets.textures]]
id = "brick_normal"
path = "assets/textures/brick_normal.png"  # Name triggers BC5

# Explicit format override (rarely needed)
[[assets.textures]]
id = "special_normal"
path = "assets/textures/special.png"
format = "bc5"  # Force BC5 even without naming convention
```

### Compression Matrix

| Channels | Filename | Compress Flag | Result |
|----------|----------|---------------|--------|
| 4 | any | true | BC7 (color) |
| 3-4 | `*_normal.png` | true | BC5 (normal) |
| 2-3 | any | true | BC5 (normal) |
| any | any | false | RGBA8 (uncompressed) |

---

## Shader Reconstruction

### WGSL Implementation

```wgsl
fn sample_normal_map(uv: vec2<f32>, tbn: mat3x3<f32>) -> vec3<f32> {
    // Check if normal map is bound (material flag)
    if ((material.flags & FLAG_USE_NORMAL_MAP) == 0u) {
        return tbn[2]; // Return vertex normal (Z column)
    }

    // Sample BC5 texture (RG channels)
    let normal_sample = textureSample(normal_texture, sampler_linear, uv).rg;

    // Decode from [0,1] to [-1,1]
    let xy = normal_sample * 2.0 - 1.0;

    // Reconstruct Z from unit sphere constraint
    // z² = 1 - x² - y²
    let z = sqrt(max(0.0, 1.0 - dot(xy, xy)));

    // Build tangent-space normal
    let tangent_normal = vec3<f32>(xy, z);

    // Transform to world space using TBN matrix
    return normalize(tbn * tangent_normal);
}
```

### Why max(0.0, ...)?

Due to compression artifacts, x² + y² can slightly exceed 1.0, making the sqrt argument negative. The `max(0.0, ...)` clamps this to prevent NaN.

---

## Quality Comparison

### BC5 vs BC7 for Normals

| Aspect | BC5 | BC7 |
|--------|-----|-----|
| Bits per channel | 8 effective | 5-7 effective |
| Total size | 16 bytes/block | 16 bytes/block |
| Channels stored | 2 (RG) | 4 (RGBA) |
| Quality for normals | Excellent | Good |
| Alpha support | No | Yes |

**Conclusion:** BC5 provides ~30% better normal quality than BC7 at the same size because all bits serve the two channels we care about.

### BC5 vs Uncompressed

| Aspect | BC5 | RGBA8 |
|--------|-----|-------|
| Size per pixel | 1 byte | 4 bytes |
| Compression ratio | 4:1 | 1:1 |
| Quality loss | Minimal | None |
| Block artifacts | Slight | None |

**Conclusion:** BC5 is 4× smaller with imperceptible quality loss for normal maps.

---

## Best Practices

### Do:
- Use `*_normal.png` naming for auto-detection
- Generate RGB normals, let pipeline compress to BC5
- Use power-of-2 resolutions (required for BC5)
- Verify neutral areas are close to (128, 128, 255)

### Don't:
- Store normal maps as RGBA (wastes memory)
- Use BC7 for normal maps (BC5 is better)
- Apply gamma correction (normals are linear data)
- Mix normal maps with color textures in atlases

---

## Memory Budget Reference

| Resolution | BC5 Size | Recommended Use |
|------------|----------|-----------------|
| 64 × 64 | 4 KB | Props, distant objects |
| 128 × 128 | 16 KB | Standard objects |
| 256 × 256 | 64 KB | Hero objects, characters |
| 512 × 512 | 256 KB | Rare, terrain tiles |

**ZX VRAM Budget:** 4MB total. Plan normal map usage within this limit.
