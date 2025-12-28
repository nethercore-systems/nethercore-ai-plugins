# Matcap Texture Generation

Matcaps are spherical lighting captures - a 2D image that encodes how light appears on a sphere. ZX uses matcaps for stylized, fast lighting without runtime calculations.

## How Matcaps Work

The shader samples the matcap texture using view-space normals:
- Normal pointing at camera → center of matcap (u=0.5, v=0.5)
- Normal pointing left → left edge (u=0, v=0.5)
- Normal pointing up → top edge (u=0.5, v=0)

## Shadow Matcap (Multiply Blend)

Shadow matcaps darken the base color. White areas preserve base, dark areas shadow.

```rust
fn generate_shadow_matcap(name: &str, shadow_intensity: f32) {
    let size = 256;
    let center = size as f32 / 2.0;
    let mut tex = TextureBuffer::new(size, size);

    for y in 0..size {
        for x in 0..size {
            let dx = (x as f32 - center) / center;
            let dy = (y as f32 - center) / center;
            let dist = (dx * dx + dy * dy).sqrt();

            if dist > 1.0 {
                tex.set(x, y, 0xFFFFFFFF);
                continue;
            }

            let z = (1.0 - dist * dist).sqrt();
            let light_dot = (dx * -0.5 + dy * -0.7 + z * 0.5).max(0.0);
            let val = 1.0 - shadow_intensity * (1.0 - light_dot);
            let v = (val * 255.0) as u8;

            tex.set(x, y, ((v as u32) << 24) | ((v as u32) << 16) | ((v as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_shadow_matcap.png", name)).unwrap();
}
```

## Highlight Matcap (Add Blend)

Highlight matcaps add brightness. Black areas add nothing, bright areas add glow.

```rust
fn generate_highlight_matcap(name: &str, highlight_color: u32, intensity: f32, tightness: f32) {
    let size = 256;
    let center = size as f32 / 2.0;
    let mut tex = TextureBuffer::new(size, size);

    let hr = ((highlight_color >> 24) & 0xFF) as f32 / 255.0;
    let hg = ((highlight_color >> 16) & 0xFF) as f32 / 255.0;
    let hb = ((highlight_color >> 8) & 0xFF) as f32 / 255.0;

    for y in 0..size {
        for x in 0..size {
            let dx = (x as f32 - center) / center;
            let dy = (y as f32 - center) / center;
            let dist = (dx * dx + dy * dy).sqrt();

            if dist > 1.0 {
                tex.set(x, y, 0x000000FF);
                continue;
            }

            let z = (1.0 - dist * dist).sqrt();
            let light_dot = (dx * 0.6 + dy * -0.6 + z * 0.5).max(0.0);
            let spec = light_dot.powf(tightness * 32.0) * intensity;

            let r = (hr * spec * 255.0).min(255.0) as u8;
            let g = (hg * spec * 255.0).min(255.0) as u8;
            let b = (hb * spec * 255.0).min(255.0) as u8;

            tex.set(x, y, ((r as u32) << 24) | ((g as u32) << 16) | ((b as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_highlight_matcap.png", name)).unwrap();
}
```

## HSV Modulation Matcap

HSV matcaps shift the hue/saturation of the base color. Great for iridescence.

```rust
fn generate_hsv_matcap(name: &str, hue_shift_range: f32) {
    let size = 256;
    let center = size as f32 / 2.0;
    let mut tex = TextureBuffer::new(size, size);

    for y in 0..size {
        for x in 0..size {
            let dx = (x as f32 - center) / center;
            let dy = (y as f32 - center) / center;
            let dist = (dx * dx + dy * dy).sqrt();

            if dist > 1.0 {
                tex.set(x, y, 0x808080FF);
                continue;
            }

            let angle = dy.atan2(dx);
            let hue_shift = (angle / std::f32::consts::PI) * hue_shift_range;
            let h = ((hue_shift + 0.5).clamp(0.0, 1.0) * 255.0) as u8;
            let s = 128u8;
            let v = 128u8;

            tex.set(x, y, ((h as u32) << 24) | ((s as u32) << 16) | ((v as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_hsv_matcap.png", name)).unwrap();
}
```

## Python Matcap Example

```python
import numpy as np
from PIL import Image

def generate_matcap(name, matcap_type="shadow", intensity=0.5, size=256):
    """Generate a matcap texture for ZX Mode 1."""
    img = np.zeros((size, size, 4), dtype=np.uint8)
    center = size / 2

    for y in range(size):
        for x in range(size):
            dx = (x - center) / center
            dy = (y - center) / center
            dist = np.sqrt(dx*dx + dy*dy)

            if dist > 1.0:
                if matcap_type == "shadow":
                    img[y, x] = [255, 255, 255, 255]
                else:
                    img[y, x] = [0, 0, 0, 255]
                continue

            z = np.sqrt(1.0 - dist*dist)

            if matcap_type == "shadow":
                light = max(0, -0.5*dx - 0.7*dy + 0.5*z)
                val = int((1.0 - intensity * (1.0 - light)) * 255)
                img[y, x] = [val, val, val, 255]
            else:
                light = max(0, 0.6*dx - 0.6*dy + 0.5*z)
                spec = (light ** 16) * intensity
                val = int(min(spec * 255, 255))
                img[y, x] = [val, val, val, 255]

    Image.fromarray(img).save(f"assets/textures/{name}_matcap.png")
```
