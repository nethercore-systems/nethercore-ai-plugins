# Noise Algorithms Reference

## Perlin Noise

Classic gradient noise for organic surfaces.

```rust
tex.perlin(scale, seed, color_low, color_high);
```

- `scale`: 0.01 (large features) to 0.2 (fine detail)
- Use for: clouds, water, organic materials

## Simplex Noise

Faster than Perlin, fewer artifacts.

```rust
tex.simplex(scale, seed, color_low, color_high);
```

## Voronoi (Cellular)

Cell-like patterns for scales, crystals, cracks.

```rust
tex.voronoi(cell_count, seed, cell_color, edge_color);
```

- `cell_count`: 4-32 typical

## Fractal Brownian Motion (FBM)

Layered noise for complex organic patterns.

```rust
tex.fbm(scale, octaves, persistence, seed, color_low, color_high);
```

- `octaves`: 1-8 (more = more detail)
- `persistence`: 0.3-0.7 (amplitude falloff)

## Tileable Noise

For seamless tiling, use periodic noise:

```rust
fn tileable_noise(x: f32, y: f32, size: f32, seed: u64) -> f32 {
    // Use 4D noise with circular coordinates for seamless tiling
    let s = x / size;
    let t = y / size;

    let nx = (s * 2.0 * PI).cos();
    let ny = (s * 2.0 * PI).sin();
    let nz = (t * 2.0 * PI).cos();
    let nw = (t * 2.0 * PI).sin();

    snoise4(nx, ny, nz, nw, seed)
}
```
