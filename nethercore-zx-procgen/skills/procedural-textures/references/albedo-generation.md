# Albedo Texture Generation

Albedo is the base color without lighting. Generate with noise, patterns, or painted styles.

## Rust Example

```rust
use proc_gen::texture::*;

fn generate_albedo(name: &str, base_color: u32, variation: f32, seed: u64) {
    let mut tex = TextureBuffer::new(256, 256);

    // Base color with subtle noise variation
    tex.solid(base_color);

    // Add color variation using noise
    let mut noise_tex = TextureBuffer::new(256, 256);
    noise_tex.fbm(0.03, 4, 0.5, seed, 0x000000FF, 0xFFFFFFFF);

    // Blend noise with base (variation controls strength)
    for y in 0..256 {
        for x in 0..256 {
            let base = tex.get(x, y);
            let noise_val = noise_tex.get(x, y);

            // Modulate base color by noise
            let r = ((base >> 24) as f32 * (1.0 - variation + variation * (noise_val >> 24) as f32 / 255.0)) as u8;
            let g = (((base >> 16) & 0xFF) as f32 * (1.0 - variation + variation * ((noise_val >> 16) & 0xFF) as f32 / 255.0)) as u8;
            let b = (((base >> 8) & 0xFF) as f32 * (1.0 - variation + variation * ((noise_val >> 8) & 0xFF) as f32 / 255.0)) as u8;

            tex.set(x, y, ((r as u32) << 24) | ((g as u32) << 16) | ((b as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_albedo.png", name)).unwrap();
}
```

## Python Example

```python
import numpy as np
from PIL import Image
from noise import snoise2

def generate_albedo(name, base_color, variation=0.2, seed=42, size=256):
    """Generate an albedo texture with noise-based color variation."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    # Parse base color (0xRRGGBBAA)
    r = (base_color >> 24) & 0xFF
    g = (base_color >> 16) & 0xFF
    b = (base_color >> 8) & 0xFF

    for y in range(size):
        for x in range(size):
            # Generate noise value [0, 1]
            n = (snoise2(x * 0.03, y * 0.03, octaves=4, base=seed) + 1) / 2

            # Modulate color by noise
            factor = 1.0 - variation + variation * n
            img[y, x] = [
                int(r * factor),
                int(g * factor),
                int(b * factor),
                255
            ]

    Image.fromarray(img).save(f"assets/textures/{name}_albedo.png")

# Example: Rusty metal
generate_albedo("rust", 0x8B4513FF, variation=0.3, seed=42)
```
