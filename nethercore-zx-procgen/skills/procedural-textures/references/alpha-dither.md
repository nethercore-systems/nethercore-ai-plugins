# Alpha Channel and Dither Transparency

ZX uses **dithered transparency** via the alpha channel. Instead of true alpha blending (which is order-dependent), ZX uses a Bayer 4x4 dither pattern to create stippled transparency.

## How Dither Transparency Works

- Alpha value is compared against a Bayer dither threshold per pixel
- Below threshold = fragment discarded (fully transparent)
- Above threshold = fragment kept (fully opaque)
- Result: Order-independent "screen door" transparency

## Generating Textures with Alpha

```rust
fn generate_albedo_with_alpha(name: &str, base_color: u32, alpha_pattern: AlphaPattern, seed: u64) {
    let size = 256;
    let mut tex = TextureBuffer::new(size, size);

    for y in 0..size {
        for x in 0..size {
            let r = (base_color >> 24) & 0xFF;
            let g = (base_color >> 16) & 0xFF;
            let b = (base_color >> 8) & 0xFF;

            let alpha = match alpha_pattern {
                AlphaPattern::Solid => 255,
                AlphaPattern::EdgeFade => {
                    let edge_dist = (x.min(size - 1 - x).min(y).min(size - 1 - y)) as f32 / (size as f32 / 4.0);
                    (edge_dist.min(1.0) * 255.0) as u8
                }
                AlphaPattern::NoiseHoles => {
                    let noise = snoise2(x as f32 * 0.08, y as f32 * 0.08, seed);
                    if noise > 0.3 { 255 } else { 0 }
                }
                AlphaPattern::Gradient(start, end) => {
                    let t = y as f32 / size as f32;
                    ((1.0 - t) * start as f32 + t * end as f32) as u8
                }
                AlphaPattern::Radial => {
                    let dx = (x as f32 - size as f32 / 2.0) / (size as f32 / 2.0);
                    let dy = (y as f32 - size as f32 / 2.0) / (size as f32 / 2.0);
                    let dist = (dx * dx + dy * dy).sqrt();
                    ((1.0 - dist.min(1.0)) * 255.0) as u8
                }
            };

            tex.set(x, y, (r << 24) | (g << 16) | (b << 8) | alpha as u32);
        }
    }

    tex.write_png(&format!("assets/textures/{}_albedo.png", name)).unwrap();
}

enum AlphaPattern {
    Solid,
    EdgeFade,
    NoiseHoles,
    Gradient(u8, u8),  // start_alpha, end_alpha
    Radial,
}
```

## Python Alpha Example

```python
def generate_alpha_texture(name, base_color, alpha_type="radial", size=256):
    """Generate albedo texture with alpha for dither transparency."""
    img = np.zeros((size, size, 4), dtype=np.uint8)

    r = (base_color >> 24) & 0xFF
    g = (base_color >> 16) & 0xFF
    b = (base_color >> 8) & 0xFF

    for y in range(size):
        for x in range(size):
            if alpha_type == "radial":
                dx = (x - size/2) / (size/2)
                dy = (y - size/2) / (size/2)
                dist = min(1.0, np.sqrt(dx*dx + dy*dy))
                alpha = int((1.0 - dist) * 255)
            elif alpha_type == "edge_fade":
                edge = min(x, size-1-x, y, size-1-y) / (size/4)
                alpha = int(min(1.0, edge) * 255)
            else:
                alpha = 255

            img[y, x] = [r, g, b, alpha]

    Image.fromarray(img).save(f"assets/textures/{name}_albedo.png")
```

## Runtime Alpha Control

Beyond texture alpha, you can also control transparency via uniforms:

```rust
set_alpha(0.5);  // 50% overall transparency (multiplied with texture alpha)
```

**Note:** Dither transparency works best with moving objects or at a distance. Close-up static objects may show visible dither patterns (intentional retro aesthetic).
