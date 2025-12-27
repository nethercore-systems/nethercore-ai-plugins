---
name: Billboard Particles
description: This skill should be used when the user asks about "billboard", "particles", "draw_billboard", "particle system", "particle emitter", "sprite 3D", "smoke effect", "fire effect", "sparks", "dust particles", "rain particles", "explosion effect", "spherical billboard", "cylindrical billboard", "camera-facing quad", "3D sprite", "billboard_region", or mentions implementing particle effects, billboard rendering, VFX systems, or camera-facing sprites for Nethercore ZX games.
version: 1.0.0
---

# Billboard Particles for Nethercore ZX

Implement camera-facing sprites and particle systems using ZX billboard rendering. Billboards always face the camera, ideal for particles, foliage, and impostor sprites.

## Billboard FFI Functions

Reference `nethercore/include/zx.rs` lines 644-662 for complete signatures:

| Function | Purpose |
|----------|---------|
| `draw_billboard(w, h, mode, color)` | Draw camera-facing quad with full texture |
| `draw_billboard_region(w, h, src_x, src_y, src_w, src_h, mode, color)` | Draw with UV region |

## Billboard Modes

```rust
pub mod billboard {
    pub const SPHERICAL: u32 = 1;      // Fully faces camera (particles)
    pub const CYLINDRICAL_Y: u32 = 2;  // Rotates Y axis only (trees)
    pub const CYLINDRICAL_X: u32 = 3;  // Rotates X axis only
    pub const CYLINDRICAL_Z: u32 = 4;  // Rotates Z axis only
}
```

| Mode | Use Case | Behavior |
|------|----------|----------|
| Spherical | Particles, point sprites | Always faces camera |
| Cylindrical Y | Trees, grass, pillars | Upright, rotates horizontally |
| Cylindrical X | Horizontal bands | Fixed vertical, rotates around X |
| Cylindrical Z | Depth-aligned sprites | Rotates around Z axis |

## Basic Billboard Usage

Billboards use the transform stack for position and bound texture:

```rust
static mut PARTICLE_TEX: u32 = 0;

fn init() {
    unsafe {
        PARTICLE_TEX = rom_texture_str("particle");
    }
}

fn render() {
    unsafe {
        texture_bind(PARTICLE_TEX);

        // Position via transform
        push_identity();
        push_translate(5.0, 2.0, 0.0);

        // Draw 1x1 unit billboard facing camera
        draw_billboard(1.0, 1.0, billboard::SPHERICAL, 0xFFFFFFFF);
    }
}
```

## Sprite Sheet Animation

Use `draw_billboard_region` for animated particles:

```rust
// 4x4 sprite sheet (16 frames)
const SHEET_COLS: u32 = 4;
const SHEET_ROWS: u32 = 4;

fn draw_animated_billboard(frame: u32, x: f32, y: f32, z: f32, size: f32, color: u32) {
    unsafe {
        let col = frame % SHEET_COLS;
        let row = frame / SHEET_COLS;

        // Calculate UV region (normalized 0.0-1.0)
        let u = col as f32 / SHEET_COLS as f32;
        let v = row as f32 / SHEET_ROWS as f32;
        let uw = 1.0 / SHEET_COLS as f32;
        let vh = 1.0 / SHEET_ROWS as f32;

        push_identity();
        push_translate(x, y, z);

        draw_billboard_region(
            size, size,
            u, v, uw, vh,           // UV region
            billboard::SPHERICAL,
            color
        );
    }
}
```

## Particle Emitter Pattern

Basic particle system structure:

```rust
const MAX_PARTICLES: usize = 256;

#[derive(Clone, Copy)]
struct Particle {
    x: f32, y: f32, z: f32,
    vx: f32, vy: f32, vz: f32,
    life: f32,
    max_life: f32,
    size: f32,
    color: u32,
    frame: u32,
}

impl Default for Particle {
    fn default() -> Self {
        Particle {
            x: 0.0, y: 0.0, z: 0.0,
            vx: 0.0, vy: 0.0, vz: 0.0,
            life: 0.0, max_life: 1.0,
            size: 1.0, color: 0xFFFFFFFF,
            frame: 0,
        }
    }
}

static mut PARTICLES: [Particle; MAX_PARTICLES] = [Particle {
    x: 0.0, y: 0.0, z: 0.0,
    vx: 0.0, vy: 0.0, vz: 0.0,
    life: 0.0, max_life: 1.0,
    size: 1.0, color: 0xFFFFFFFF,
    frame: 0,
}; MAX_PARTICLES];

fn update_particles() {
    unsafe {
        let dt = delta_time();

        for p in PARTICLES.iter_mut() {
            if p.life > 0.0 {
                // Physics
                p.x += p.vx * dt;
                p.y += p.vy * dt;
                p.z += p.vz * dt;

                // Gravity
                p.vy -= 9.8 * dt;

                // Lifetime
                p.life -= dt;
            }
        }
    }
}

fn render_particles() {
    unsafe {
        texture_bind(PARTICLE_TEX);

        for p in PARTICLES.iter() {
            if p.life > 0.0 {
                let t = p.life / p.max_life;  // 1.0 → 0.0

                // Fade out
                let alpha = (t * 255.0) as u8;
                let color = (p.color & 0xFFFFFF00) | alpha as u32;

                // Shrink over lifetime
                let size = p.size * t;

                push_identity();
                push_translate(p.x, p.y, p.z);
                draw_billboard(size, size, billboard::SPHERICAL, color);
            }
        }
    }
}
```

## Particle Spawning

```rust
fn spawn_particle(x: f32, y: f32, z: f32) {
    unsafe {
        // Find dead particle slot
        for p in PARTICLES.iter_mut() {
            if p.life <= 0.0 {
                p.x = x;
                p.y = y;
                p.z = z;

                // Random velocity (use rollback-safe random)
                p.vx = random_f32_range(-2.0, 2.0);
                p.vy = random_f32_range(3.0, 6.0);
                p.vz = random_f32_range(-2.0, 2.0);

                p.life = random_f32_range(0.5, 1.5);
                p.max_life = p.life;
                p.size = random_f32_range(0.3, 0.8);
                p.color = 0xFFFFFFFF;

                break;
            }
        }
    }
}
```

## Common Effects

### Smoke

```rust
fn spawn_smoke(x: f32, y: f32, z: f32) {
    for _ in 0..3 {
        spawn_particle_config(
            x + random_f32_range(-0.2, 0.2),
            y,
            z + random_f32_range(-0.2, 0.2),
            random_f32_range(-0.5, 0.5),  // vx (drift)
            random_f32_range(1.0, 2.0),    // vy (rise)
            random_f32_range(-0.5, 0.5),  // vz
            random_f32_range(1.0, 3.0),    // life
            random_f32_range(0.5, 1.5),    // size
            0x888888FF                      // gray
        );
    }
}
```

### Fire

```rust
fn spawn_fire(x: f32, y: f32, z: f32) {
    // Core (yellow/white)
    spawn_particle_config(x, y, z, 0.0, 3.0, 0.0, 0.3, 0.4, 0xFFFF88FF);
    // Mid (orange)
    spawn_particle_config(x, y, z, random_f32_range(-1.0, 1.0), 2.5, 0.0, 0.5, 0.6, 0xFF8800FF);
    // Outer (red)
    spawn_particle_config(x, y, z, random_f32_range(-1.5, 1.5), 2.0, 0.0, 0.7, 0.8, 0xFF4400FF);
}
```

### Sparks

```rust
fn spawn_sparks(x: f32, y: f32, z: f32) {
    for _ in 0..10 {
        spawn_particle_config(
            x, y, z,
            random_f32_range(-5.0, 5.0),
            random_f32_range(2.0, 8.0),
            random_f32_range(-5.0, 5.0),
            random_f32_range(0.2, 0.5),
            random_f32_range(0.05, 0.15),
            0xFFFF00FF  // bright yellow
        );
    }
}
```

### Dust

```rust
fn spawn_dust(x: f32, y: f32, z: f32) {
    for _ in 0..5 {
        spawn_particle_config(
            x + random_f32_range(-0.5, 0.5),
            y,
            z + random_f32_range(-0.5, 0.5),
            random_f32_range(-1.0, 1.0),
            random_f32_range(0.5, 1.5),
            random_f32_range(-1.0, 1.0),
            random_f32_range(0.3, 0.8),
            random_f32_range(0.1, 0.3),
            0xAA9977FF  // tan/brown
        );
    }
}
```

### Rain

```rust
// Spawn rain at regular intervals across area
fn spawn_rain() {
    for _ in 0..5 {
        let x = random_f32_range(-20.0, 20.0);
        let z = random_f32_range(-20.0, 20.0);

        spawn_particle_config(
            x, 15.0, z,  // Spawn high
            0.0, -20.0, 0.0,  // Fast downward velocity
            1.5,  // life (reaches ground)
            0.02, // tiny size
            0x4488CCFF
        );
    }
}
```

## Performance Guidelines

| Particle Count | Performance |
|----------------|-------------|
| 0-100 | Excellent |
| 100-500 | Good |
| 500-1000 | Moderate |
| 1000+ | Consider optimization |

### Optimization Tips

- **Pool particles**: Reuse dead particles instead of allocating
- **LOD**: Reduce particle count at distance
- **Texture atlas**: Single bind for all particle types
- **Skip invisible**: Don't render particles behind camera
- **Batch by texture**: Group particles using same texture

## Foliage Billboards

Use cylindrical Y for upright vegetation:

```rust
fn render_tree(x: f32, y: f32, z: f32) {
    unsafe {
        texture_bind(TREE_TEXTURE);
        push_identity();
        push_translate(x, y + 2.0, z);  // Center vertically

        // Cylindrical Y: rotates to face camera but stays upright
        draw_billboard(2.0, 4.0, billboard::CYLINDRICAL_Y, 0xFFFFFFFF);
    }
}

fn render_grass_patch(x: f32, z: f32) {
    unsafe {
        texture_bind(GRASS_TEXTURE);

        // Cross-billboard (two intersecting quads)
        push_identity();
        push_translate(x, 0.5, z);
        draw_billboard(1.0, 1.0, billboard::CYLINDRICAL_Y, 0xFFFFFFFF);

        push_rotate_y(90.0);
        draw_billboard(1.0, 1.0, billboard::CYLINDRICAL_Y, 0xFFFFFFFF);
    }
}
```

## Rollback Safety

All particle state must be in static variables:
- Particle arrays auto-snapshot with game state
- Use `random()` family for randomness (not external RNG)
- Particle spawning in `update()`, rendering in `render()`

## Additional Resources

- **`examples/particle-examples.md`** - Complete effect implementations
- **`references/particle-patterns.md`** - Advanced patterns and optimization
- **`nethercore/include/zx.rs`** lines 644-662 - Billboard FFI signatures
- **Gap 5 (Game Feel)** - Particle integration with screen shake, impact effects
- **Gap 22 (Creative Pipeline)** - Procedural particle texture generation
