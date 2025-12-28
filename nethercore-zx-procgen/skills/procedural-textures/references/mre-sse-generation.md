# MRE and SSE Texture Generation

## MRE Textures (Mode 2)

MRE packs three material properties into RGB channels:
- **R (Red):** Metallic (0 = dielectric, 255 = metal)
- **G (Green):** Roughness (0 = smooth/mirror, 255 = rough)
- **B (Blue):** Emissive intensity (0 = none, 255 = max glow)

### Rust MRE Example

```rust
fn generate_mre(name: &str, metallic: f32, roughness: f32, emissive: f32, seed: u64) {
    let mut tex = TextureBuffer::new(256, 256);

    for y in 0..256 {
        for x in 0..256 {
            let noise = snoise2(x as f32 * 0.05, y as f32 * 0.05, seed);
            let rough_varied = (roughness + noise * 0.15).clamp(0.0, 1.0);

            let m = (metallic * 255.0) as u8;
            let r = (rough_varied * 255.0) as u8;
            let e = (emissive * 255.0) as u8;

            tex.set(x, y, ((m as u32) << 24) | ((r as u32) << 16) | ((e as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_mre.png", name)).unwrap();
}

// Examples:
generate_mre("chrome", 1.0, 0.1, 0.0, 42);
generate_mre("rubber", 0.0, 0.9, 0.0, 42);
generate_mre("glowing_crystal", 0.2, 0.3, 0.8, 42);
```

### MRE Value Guide

| Material | Metallic | Roughness | Emissive |
|----------|----------|-----------|----------|
| Polished Chrome | 1.0 | 0.05-0.15 | 0.0 |
| Brushed Steel | 1.0 | 0.3-0.5 | 0.0 |
| Gold | 1.0 | 0.15-0.25 | 0.0 |
| Plastic | 0.0 | 0.3-0.6 | 0.0 |
| Rubber | 0.0 | 0.8-1.0 | 0.0 |
| Glass | 0.0 | 0.0-0.1 | 0.0 |
| LED/Neon | 0.0 | 0.2-0.4 | 0.5-1.0 |

---

## SSE Textures (Mode 3)

SSE packs three material properties into RGB channels:
- **R (Red):** Specular Reduction (0 = full specular, 255 = no specular)
- **G (Green):** Shininess (0 = very soft, 255 = mirror-like)
- **B (Blue):** Emissive intensity

**Note:** Specular reduction should typically be **0** for most materials. Only increase it where you want to dampen specular highlights (dirt, scratches, weathering).

### Rust SSE Example

```rust
fn generate_sse(name: &str, specular_reduction: f32, shininess: f32, emissive: f32, seed: u64) {
    let mut tex = TextureBuffer::new(256, 256);

    for y in 0..256 {
        for x in 0..256 {
            let noise = snoise2(x as f32 * 0.08, y as f32 * 0.08, seed);
            let reduction = if specular_reduction > 0.0 {
                (specular_reduction + noise.max(0.0) * 0.2).clamp(0.0, 1.0)
            } else {
                0.0
            };

            let sr = (reduction * 255.0) as u8;
            let sh = (shininess * 255.0) as u8;
            let e = (emissive * 255.0) as u8;

            tex.set(x, y, ((sr as u32) << 24) | ((sh as u32) << 16) | ((e as u32) << 8) | 0xFF);
        }
    }

    tex.write_png(&format!("assets/textures/{}_sse.png", name)).unwrap();
}

generate_sse("polished_gold", 0.0, 0.85, 0.0, 42);
generate_sse("worn_brass", 0.3, 0.6, 0.0, 42);
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

## Complete Material Set Generation

### Mode 2 Material Set

```rust
fn generate_mode2_material(
    name: &str,
    albedo_color: u32,
    metallic: f32,
    roughness: f32,
    emissive: f32,
    variation: f32,
    seed: u64,
) {
    let size = 256;
    let mut albedo = TextureBuffer::new(size, size);
    let mut mre = TextureBuffer::new(size, size);

    for y in 0..size {
        for x in 0..size {
            let noise = snoise2(x as f32 * 0.05, y as f32 * 0.05, seed);
            let r_val = (roughness + noise * variation * 0.3).clamp(0.0, 1.0);

            mre.set(x, y,
                ((metallic * 255.0) as u32) << 24 |
                ((r_val * 255.0) as u32) << 16 |
                ((emissive * 255.0) as u32) << 8 |
                0xFF
            );
        }
    }

    albedo.write_png(&format!("assets/textures/{}_albedo.png", name)).unwrap();
    mre.write_png(&format!("assets/textures/{}_mre.png", name)).unwrap();
}
```

### Mode 3 Material Set

```rust
fn generate_mode3_material(
    name: &str,
    albedo_color: u32,
    specular_reduction: f32,
    shininess: f32,
    specular_color: u32,
    emissive: f32,
    seed: u64,
) {
    let size = 256;
    let mut albedo = TextureBuffer::new(size, size);
    let mut sse = TextureBuffer::new(size, size);
    let mut spec = TextureBuffer::new(size, size);

    for y in 0..size {
        for x in 0..size {
            sse.set(x, y,
                ((specular_reduction * 255.0) as u32) << 24 |
                ((shininess * 255.0) as u32) << 16 |
                ((emissive * 255.0) as u32) << 8 |
                0xFF
            );
        }
    }
    spec.solid(specular_color);

    albedo.write_png(&format!("assets/textures/{}_albedo.png", name)).unwrap();
    sse.write_png(&format!("assets/textures/{}_sse.png", name)).unwrap();
    spec.write_png(&format!("assets/textures/{}_specular.png", name)).unwrap();
}
```
