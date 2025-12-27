# Noise Function Reference

Detailed implementations and parameter guidance for procedural noise.

## Noise Type Comparison

| Type | Pattern | Speed | Artifacts | Best For |
|------|---------|-------|-----------|----------|
| Perlin | Smooth, organic | Medium | Grid-aligned at 45 deg | Classic look, terrain |
| Simplex | Smooth, isotropic | Fast | None | Modern default, textures |
| Worley/Voronoi | Cellular | Slow | Sharp cell edges | Scales, crystals, cracks |
| Value | Blocky | Very fast | Visible grid | Retro look, fast preview |
| FBM | Layered detail | Slow | Depends on base | Complex surfaces, terrain |
| Domain Warping | Swirled | Very slow | None | Artistic effects, fire |

---

## Perlin Noise

Ken Perlin's original gradient noise (1983). Smooth but has slight grid bias.

### Implementation

```rust
fn perlin_2d(x: f32, y: f32, seed: u64) -> f32 {
    // Grid coordinates
    let x0 = x.floor() as i32;
    let y0 = y.floor() as i32;
    let x1 = x0 + 1;
    let y1 = y0 + 1;

    // Interpolation weights
    let sx = smootherstep(x - x0 as f32);
    let sy = smootherstep(y - y0 as f32);

    // Gradient vectors at corners
    let g00 = gradient_2d(x0, y0, seed);
    let g10 = gradient_2d(x1, y0, seed);
    let g01 = gradient_2d(x0, y1, seed);
    let g11 = gradient_2d(x1, y1, seed);

    // Dot products
    let n00 = dot2(g00, x - x0 as f32, y - y0 as f32);
    let n10 = dot2(g10, x - x1 as f32, y - y0 as f32);
    let n01 = dot2(g01, x - x0 as f32, y - y1 as f32);
    let n11 = dot2(g11, x - x1 as f32, y - y1 as f32);

    // Bilinear interpolation
    let nx0 = lerp(n00, n10, sx);
    let nx1 = lerp(n01, n11, sx);
    lerp(nx0, nx1, sy)
}

fn smootherstep(t: f32) -> f32 {
    t * t * t * (t * (t * 6.0 - 15.0) + 10.0)
}

fn gradient_2d(x: i32, y: i32, seed: u64) -> (f32, f32) {
    let hash = hash_2d(x, y, seed);
    let angle = (hash as f32 / u32::MAX as f32) * 2.0 * PI;
    (angle.cos(), angle.sin())
}
```

### Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| Frequency | 0.001-1.0 | Lower = larger features |
| Amplitude | 0.0-1.0 | Output range scaling |

### When to Use
- Classic procedural content (clouds, fire, water)
- When 45-degree artifacts are acceptable
- Legacy compatibility

---

## Simplex Noise

Ken Perlin's improved noise (2001). Faster, no grid artifacts, works in any dimension.

### Implementation

```rust
fn simplex_2d(x: f32, y: f32, seed: u64) -> f32 {
    const F2: f32 = 0.366025403784;  // (sqrt(3)-1)/2
    const G2: f32 = 0.211324865405;  // (3-sqrt(3))/6

    // Skew to simplex space
    let s = (x + y) * F2;
    let i = (x + s).floor();
    let j = (y + s).floor();

    // Unskew back
    let t = (i + j) * G2;
    let x0 = x - (i - t);
    let y0 = y - (j - t);

    // Determine which simplex
    let (i1, j1) = if x0 > y0 { (1, 0) } else { (0, 1) };

    let x1 = x0 - i1 as f32 + G2;
    let y1 = y0 - j1 as f32 + G2;
    let x2 = x0 - 1.0 + 2.0 * G2;
    let y2 = y0 - 1.0 + 2.0 * G2;

    // Contributions from corners
    let mut n = 0.0;
    n += contribution(x0, y0, i as i32, j as i32, seed);
    n += contribution(x1, y1, i as i32 + i1, j as i32 + j1, seed);
    n += contribution(x2, y2, i as i32 + 1, j as i32 + 1, seed);

    // Scale to [-1, 1]
    n * 70.0
}

fn contribution(x: f32, y: f32, gi: i32, gj: i32, seed: u64) -> f32 {
    let t = 0.5 - x * x - y * y;
    if t < 0.0 {
        return 0.0;
    }
    let t2 = t * t;
    let g = gradient_2d(gi, gj, seed);
    t2 * t2 * (g.0 * x + g.1 * y)
}
```

### When to Use
- Default choice for most applications
- Higher dimensions (3D, 4D)
- When isotropy matters

---

## Worley/Voronoi Noise

Cellular patterns based on distance to random points.

### Implementation

```rust
fn worley_2d(x: f32, y: f32, cell_count: u32, seed: u64) -> f32 {
    let cell_x = (x * cell_count as f32).floor() as i32;
    let cell_y = (y * cell_count as f32).floor() as i32;

    let mut min_dist = f32::MAX;

    // Check 3x3 neighborhood
    for dy in -1..=1 {
        for dx in -1..=1 {
            let cx = cell_x + dx;
            let cy = cell_y + dy;

            // Random point in cell
            let hash = hash_2d(cx, cy, seed);
            let px = (cx as f32 + random_from_hash(hash, 0)) / cell_count as f32;
            let py = (cy as f32 + random_from_hash(hash, 1)) / cell_count as f32;

            let dist = ((x - px).powi(2) + (y - py).powi(2)).sqrt();
            min_dist = min_dist.min(dist);
        }
    }

    min_dist * cell_count as f32  // Normalize
}

// Variants
fn worley_f2(x: f32, y: f32, ...) -> f32 {
    // Second closest distance
}

fn worley_f2_minus_f1(x: f32, y: f32, ...) -> f32 {
    // Edge detection pattern
}
```

### Variants

| Variant | Pattern | Use For |
|---------|---------|---------|
| F1 | Filled cells | Stones, scales, skin |
| F2 | Larger cells | Larger patterns |
| F2-F1 | Cell edges | Cracks, veins |
| F1*F2 | Mixed | Interesting combinations |

### When to Use
- Scales, reptile skin, dragon hide
- Crystal formations
- Cracked earth, dried mud
- Cell biology (microscope look)
- Stained glass effect

---

## Fractal Brownian Motion (FBM)

Layers multiple octaves of noise for complex detail.

### Implementation

```rust
fn fbm(
    x: f32,
    y: f32,
    octaves: u32,
    lacunarity: f32,  // Frequency multiplier per octave
    persistence: f32,  // Amplitude multiplier per octave
    seed: u64,
) -> f32 {
    let mut value = 0.0;
    let mut amplitude = 1.0;
    let mut frequency = 1.0;
    let mut max_value = 0.0;

    for i in 0..octaves {
        value += amplitude * simplex_2d(x * frequency, y * frequency, seed + i as u64);
        max_value += amplitude;
        amplitude *= persistence;
        frequency *= lacunarity;
    }

    value / max_value  // Normalize to [-1, 1]
}
```

### Parameters

| Parameter | Typical Range | Effect |
|-----------|---------------|--------|
| Octaves | 1-8 | More = more detail, slower |
| Lacunarity | 1.5-3.0 | 2.0 = each octave doubles frequency |
| Persistence | 0.3-0.7 | Lower = smoother, higher = rougher |

### Presets

```rust
// Smooth clouds
fbm(x, y, 4, 2.0, 0.5, seed)

// Rough terrain
fbm(x, y, 6, 2.0, 0.6, seed)

// Very rough rock
fbm(x, y, 8, 2.5, 0.65, seed)

// Smooth gradient
fbm(x, y, 2, 2.0, 0.4, seed)
```

---

## Domain Warping

Distorts coordinates before noise evaluation for artistic effects.

### Implementation

```rust
fn domain_warp(x: f32, y: f32, strength: f32, seed: u64) -> f32 {
    // First layer of noise to warp coordinates
    let warp_x = simplex_2d(x, y, seed) * strength;
    let warp_y = simplex_2d(x + 5.2, y + 1.3, seed) * strength;

    // Evaluate noise at warped coordinates
    simplex_2d(x + warp_x, y + warp_y, seed + 1)
}

// Multi-layer domain warping for complex effects
fn domain_warp_fbm(x: f32, y: f32, iterations: u32, strength: f32, seed: u64) -> f32 {
    let mut px = x;
    let mut py = y;

    for i in 0..iterations {
        let offset = i as f32 * 100.0;
        let warp_x = fbm(px, py, 4, 2.0, 0.5, seed) * strength;
        let warp_y = fbm(px + offset, py + offset, 4, 2.0, 0.5, seed) * strength;
        px += warp_x;
        py += warp_y;
    }

    fbm(px, py, 4, 2.0, 0.5, seed)
}
```

### When to Use
- Fire and smoke effects
- Marble and wood grain
- Swirling abstract patterns
- Alien/organic surfaces
- Magical effects

---

## Seamless/Tileable Noise

Generate noise that tiles perfectly.

### Implementation

```rust
fn tileable_noise(x: f32, y: f32, size: f32, seed: u64) -> f32 {
    // Map 2D coordinates to 4D torus
    let s = x / size;
    let t = y / size;

    let nx = (s * 2.0 * PI).cos();
    let ny = (s * 2.0 * PI).sin();
    let nz = (t * 2.0 * PI).cos();
    let nw = (t * 2.0 * PI).sin();

    simplex_4d(nx, ny, nz, nw, seed)
}

fn tileable_fbm(x: f32, y: f32, size: f32, octaves: u32, seed: u64) -> f32 {
    let mut value = 0.0;
    let mut amplitude = 1.0;
    let mut frequency = 1.0;
    let mut max_value = 0.0;

    for i in 0..octaves {
        value += amplitude * tileable_noise(
            x * frequency,
            y * frequency,
            size / frequency,  // Scale size with frequency
            seed + i as u64
        );
        max_value += amplitude;
        amplitude *= 0.5;
        frequency *= 2.0;
    }

    value / max_value
}
```

---

## Noise Derivatives

Compute noise gradient for normal mapping and other effects.

```rust
fn simplex_2d_deriv(x: f32, y: f32, seed: u64) -> (f32, f32, f32) {
    // Returns (value, dx, dy)
    let h = 0.001;

    let v = simplex_2d(x, y, seed);
    let vx = simplex_2d(x + h, y, seed);
    let vy = simplex_2d(x, y + h, seed);

    let dx = (vx - v) / h;
    let dy = (vy - v) / h;

    (v, dx, dy)
}

// Use for normal map generation
fn noise_to_normal(dx: f32, dy: f32, strength: f32) -> [u8; 3] {
    let nx = -dx * strength;
    let ny = -dy * strength;
    let nz = 1.0;
    let len = (nx * nx + ny * ny + nz * nz).sqrt();

    [
        ((nx / len * 0.5 + 0.5) * 255.0) as u8,
        ((ny / len * 0.5 + 0.5) * 255.0) as u8,
        ((nz / len * 0.5 + 0.5) * 255.0) as u8,
    ]
}
```

---

## Performance Tips

### Frequency Scaling

```rust
// Avoid: Computing at very high frequencies
let bad = simplex_2d(x * 1000.0, y * 1000.0, seed);

// Better: Use appropriate scale from the start
const SCALE: f32 = 0.01;
let good = simplex_2d(x * SCALE, y * SCALE, seed);
```

### Caching for FBM

```rust
// Pre-compute permutation table once
struct NoiseGenerator {
    perm: [u8; 512],
    seed: u64,
}

impl NoiseGenerator {
    fn new(seed: u64) -> Self {
        let mut perm = [0u8; 512];
        // Initialize permutation table from seed
        Self { perm, seed }
    }

    fn simplex_2d(&self, x: f32, y: f32) -> f32 {
        // Use self.perm instead of hashing each time
    }
}
```

### Vectorization (SIMD)

```rust
// Process 4 samples at once using SIMD
#[cfg(target_arch = "x86_64")]
use std::arch::x86_64::*;

unsafe fn simplex_2d_x4(x: __m128, y: __m128, seed: u64) -> __m128 {
    // SIMD implementation
}
```

---

## Common Recipes

### Clouds

```rust
let density = fbm(x * 0.01, y * 0.01, 4, 2.0, 0.5, seed);
let cloud = (density * 2.0).clamp(0.0, 1.0);
```

### Terrain Height

```rust
let base = fbm(x * 0.001, y * 0.001, 6, 2.0, 0.6, seed);
let detail = fbm(x * 0.01, y * 0.01, 4, 2.0, 0.5, seed) * 0.1;
let height = base + detail;
```

### Marble

```rust
let warp = domain_warp(x * 0.02, y * 0.02, 0.5, seed);
let veins = (x * 0.1 + warp * 3.0).sin() * 0.5 + 0.5;
```

### Wood Grain

```rust
let dist = ((x * x + y * y).sqrt() * 0.1).fract();
let warp = simplex_2d(x * 0.05, y * 0.05, seed) * 0.1;
let rings = ((dist + warp) * 20.0).fract();
```

### Fire/Smoke

```rust
let warp = domain_warp_fbm(x * 0.03, y * 0.03 - time * 0.5, 2, 0.5, seed);
let flame = (warp + 1.0) * 0.5 * (1.0 - y / height);  // Fade at top
```
