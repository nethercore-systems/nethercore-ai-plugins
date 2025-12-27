# Advanced Particle Patterns

Reference guide for optimized particle systems and advanced techniques in Nethercore ZX.

## Particle Pool Management

### Fixed-Size Pool

```rust
const POOL_SIZE: usize = 512;

static mut PARTICLES: [Particle; POOL_SIZE] = [...];
static mut ACTIVE_COUNT: usize = 0;

// Fast spawn: O(1) with free list
static mut FREE_HEAD: i32 = 0;
static mut NEXT_FREE: [i32; POOL_SIZE] = [...];

fn init_pool() {
    unsafe {
        for i in 0..POOL_SIZE-1 {
            NEXT_FREE[i] = (i + 1) as i32;
        }
        NEXT_FREE[POOL_SIZE-1] = -1;  // End of list
        FREE_HEAD = 0;
    }
}

fn alloc_particle() -> Option<usize> {
    unsafe {
        if FREE_HEAD < 0 { return None; }
        let idx = FREE_HEAD as usize;
        FREE_HEAD = NEXT_FREE[idx];
        ACTIVE_COUNT += 1;
        Some(idx)
    }
}

fn free_particle(idx: usize) {
    unsafe {
        NEXT_FREE[idx] = FREE_HEAD;
        FREE_HEAD = idx as i32;
        ACTIVE_COUNT -= 1;
    }
}
```

### Priority-Based Culling

When pool is full, remove least important particles:

```rust
fn spawn_with_priority(priority: u8, config: Particle) -> bool {
    // Try normal allocation
    if let Some(idx) = alloc_particle() {
        PARTICLES[idx] = config;
        PARTICLES[idx].priority = priority;
        return true;
    }

    // Pool full: find lower priority particle to replace
    let mut lowest_priority = priority;
    let mut replace_idx = None;

    for (i, p) in PARTICLES.iter().enumerate() {
        if p.life > 0.0 && p.priority < lowest_priority {
            lowest_priority = p.priority;
            replace_idx = Some(i);
        }
    }

    if let Some(idx) = replace_idx {
        PARTICLES[idx] = config;
        PARTICLES[idx].priority = priority;
        return true;
    }

    false  // All particles higher priority
}
```

Priority guidelines:
- 255: Critical (player effects, UI feedback)
- 200: Important (enemy hits, explosions)
- 100: Normal (environmental)
- 50: Ambient (background dust, fog)

## Distance-Based LOD

Reduce particle count for distant effects:

```rust
fn spawn_effect_lod(x: f32, y: f32, z: f32, cam_x: f32, cam_y: f32, cam_z: f32) {
    let dx = x - cam_x;
    let dy = y - cam_y;
    let dz = z - cam_z;
    let dist_sq = dx*dx + dy*dy + dz*dz;

    // Full detail
    let particle_count = if dist_sq < 100.0 {  // < 10 units
        20
    // Medium detail
    } else if dist_sq < 400.0 {  // < 20 units
        10
    // Low detail
    } else if dist_sq < 900.0 {  // < 30 units
        5
    // Minimal
    } else {
        2
    };

    for _ in 0..particle_count {
        spawn_particle(...);
    }
}
```

## Texture Atlas Organization

Single texture for all particle types:

```
+-------+-------+-------+-------+
| Smoke | Fire  | Spark | Dust  |  Row 0
+-------+-------+-------+-------+
| Water | Magic | Glow  | Ring  |  Row 1
+-------+-------+-------+-------+
| Anim  | Frame | Frame | Frame |  Row 2 (animated)
|   0   |   1   |   2   |   3   |
+-------+-------+-------+-------+
| Blood | Leaf  | Snow  | Star  |  Row 3
+-------+-------+-------+-------+
```

```rust
// UV regions for each particle type
const UV_SMOKE: (f32, f32, f32, f32) = (0.0, 0.0, 0.25, 0.25);
const UV_FIRE: (f32, f32, f32, f32) = (0.25, 0.0, 0.25, 0.25);
const UV_SPARK: (f32, f32, f32, f32) = (0.5, 0.0, 0.25, 0.25);

fn get_uv_for_type(particle_type: u8, frame: u8) -> (f32, f32, f32, f32) {
    match particle_type {
        0 => UV_SMOKE,
        1 => UV_FIRE,
        2 => UV_SPARK,
        3 => {  // Animated (row 2, frames 0-3)
            let u = (frame % 4) as f32 * 0.25;
            (u, 0.5, 0.25, 0.25)
        }
        _ => (0.0, 0.0, 0.25, 0.25)
    }
}
```

## Sorting for Transparency

Billboard transparency requires back-to-front rendering:

```rust
// Simple distance-based sort (for small particle counts)
fn sort_particles_by_distance(cam_x: f32, cam_y: f32, cam_z: f32) {
    unsafe {
        // Insertion sort is fine for mostly-sorted data
        for i in 1..ACTIVE_COUNT {
            let mut j = i;
            while j > 0 {
                let dist_a = distance_sq(&PARTICLES[SORT_ORDER[j-1]], cam_x, cam_y, cam_z);
                let dist_b = distance_sq(&PARTICLES[SORT_ORDER[j]], cam_x, cam_y, cam_z);

                if dist_b > dist_a {  // Further particles first
                    SORT_ORDER.swap(j-1, j);
                    j -= 1;
                } else {
                    break;
                }
            }
        }
    }
}

fn distance_sq(p: &Particle, cx: f32, cy: f32, cz: f32) -> f32 {
    let dx = p.x - cx;
    let dy = p.y - cy;
    let dz = p.z - cz;
    dx*dx + dy*dy + dz*dz
}
```

**Note:** For additive particles (sparks, glow), sorting isn't needed.

## Frustum Culling

Skip particles outside camera view:

```rust
fn is_visible(p: &Particle, cam_forward_x: f32, cam_forward_z: f32,
              cam_x: f32, cam_z: f32) -> bool {
    // Simple cone test (ignores Y for performance)
    let dx = p.x - cam_x;
    let dz = p.z - cam_z;

    // Dot product with camera forward
    let dot = dx * cam_forward_x + dz * cam_forward_z;

    // Behind camera
    if dot < 0.0 { return false; }

    // Too far to side (90 degree FOV approximation)
    let perp = dx * (-cam_forward_z) + dz * cam_forward_x;
    if perp.abs() > dot { return false; }

    true
}
```

## Emitter Patterns

### Point Emitter
```rust
fn spawn_point(x: f32, y: f32, z: f32) {
    spawn_particle(x, y, z, ...);
}
```

### Sphere Emitter
```rust
fn spawn_sphere(cx: f32, cy: f32, cz: f32, radius: f32) {
    // Random point on sphere surface
    let theta = random_f32() * 6.28;
    let phi = (random_f32() * 2.0 - 1.0).acos();

    let x = cx + radius * phi.sin() * theta.cos();
    let y = cy + radius * phi.cos();
    let z = cz + radius * phi.sin() * theta.sin();

    spawn_particle(x, y, z, ...);
}
```

### Ring Emitter
```rust
fn spawn_ring(cx: f32, cy: f32, cz: f32, radius: f32) {
    let theta = random_f32() * 6.28;

    let x = cx + radius * theta.cos();
    let y = cy;
    let z = cz + radius * theta.sin();

    // Velocity outward
    let vx = theta.cos() * 2.0;
    let vz = theta.sin() * 2.0;

    spawn_particle_with_velocity(x, y, z, vx, 1.0, vz);
}
```

### Cone Emitter
```rust
fn spawn_cone(x: f32, y: f32, z: f32, angle: f32, speed: f32) {
    // Random angle within cone
    let spread = random_f32() * angle;
    let rotation = random_f32() * 6.28;

    let vx = spread.sin() * rotation.cos() * speed;
    let vy = spread.cos() * speed;
    let vz = spread.sin() * rotation.sin() * speed;

    spawn_particle_with_velocity(x, y, z, vx, vy, vz);
}
```

### Line Emitter
```rust
fn spawn_line(x1: f32, y1: f32, z1: f32, x2: f32, y2: f32, z2: f32) {
    let t = random_f32();

    let x = x1 + (x2 - x1) * t;
    let y = y1 + (y2 - y1) * t;
    let z = z1 + (z2 - z1) * t;

    spawn_particle(x, y, z, ...);
}
```

## Physics Variations

### Wind
```rust
fn apply_wind(p: &mut Particle, wind_x: f32, wind_z: f32, dt: f32) {
    p.vx += wind_x * dt;
    p.vz += wind_z * dt;
}
```

### Turbulence
```rust
fn apply_turbulence(p: &mut Particle, time: f32, strength: f32, dt: f32) {
    // Simple noise-based turbulence
    let noise_x = ((p.x + time * 2.0).sin() * (p.z * 3.0).cos()) * strength;
    let noise_z = ((p.z + time * 2.0).cos() * (p.x * 3.0).sin()) * strength;

    p.vx += noise_x * dt;
    p.vz += noise_z * dt;
}
```

### Attractor
```rust
fn apply_attractor(p: &mut Particle, ax: f32, ay: f32, az: f32, strength: f32, dt: f32) {
    let dx = ax - p.x;
    let dy = ay - p.y;
    let dz = az - p.z;
    let dist = (dx*dx + dy*dy + dz*dz).sqrt().max(0.1);

    let force = strength / (dist * dist);

    p.vx += (dx / dist) * force * dt;
    p.vy += (dy / dist) * force * dt;
    p.vz += (dz / dist) * force * dt;
}
```

## Performance Budgets

| Scenario | Max Particles | Target FPS |
|----------|---------------|------------|
| Mobile/Low | 256 | 60 |
| Standard | 512 | 60 |
| Effects-Heavy | 1024 | 60 |
| Showcase | 2048 | 30 |

### Profiling Tips

1. **Count active particles** each frame
2. **Measure spawn rate** (particles/second)
3. **Track texture binds** (batch by texture)
4. **Monitor fill rate** (large particles cost more)

## Rollback Considerations

- All particle state in static arrays
- Use `random()` family, not external RNG
- Spawn particles in `update()`, not `render()`
- Particle count affects save state size
- Consider deterministic spawning patterns
