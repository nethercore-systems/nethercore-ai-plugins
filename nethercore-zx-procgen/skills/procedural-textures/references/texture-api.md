# Texture API Quick Reference

## TextureBuffer

```rust
// Create buffer
let mut tex = TextureBuffer::new(width, height);

// Get pixel
let color = tex.get(x, y);

// Set pixel
tex.set(x, y, 0xRRGGBBAA);

// Export
tex.write_png("path/to/output.png")?;
```

## Pattern Generators

```rust
// Solid fill
tex.solid(color);

// Checkerboard
tex.checker(tile_size, color_a, color_b);

// Gradients
tex.gradient_vertical(top, bottom);
tex.gradient_horizontal(left, right);
tex.gradient_radial(center, edge);
```

## Noise Functions

```rust
// Perlin noise
tex.perlin(scale, seed, color_low, color_high);

// Simplex noise (faster)
tex.simplex(scale, seed, color_low, color_high);

// Voronoi/cellular
tex.voronoi(cell_count, seed, cell_color, edge_color);

// Fractal Brownian Motion
tex.fbm(scale, octaves, persistence, seed, color_low, color_high);
```

## Material Presets

```rust
tex.metal(base_color, seed);   // Brushed metal
tex.stone(base_color, seed);   // Rock/stone
tex.crystal(base, edge, seed); // Crystalline
```

## Modifiers

```rust
tex.brightness(amount);  // -1.0 to 1.0
tex.contrast(amount);    // 0.0 to 2.0
tex.posterize(levels);   // 2-16
tex.invert();
```

## Color Format

Colors are 32-bit RGBA: `0xRRGGBBAA`

```rust
0xFF0000FF  // Red, fully opaque
0x00FF00FF  // Green, fully opaque
0x0000FFFF  // Blue, fully opaque
0xFFFFFF80  // White, 50% transparent
0x00000000  // Transparent
```

## Typical Parameters

| Noise Type | Scale Range | Notes |
|------------|-------------|-------|
| Perlin | 0.01 - 0.2 | Lower = larger features |
| Voronoi | 4 - 32 cells | Higher = more cells |
| FBM | 0.01 - 0.1 | With 4-8 octaves |

## Source Location

`nethercore/tools/proc-gen/src/texture/`
