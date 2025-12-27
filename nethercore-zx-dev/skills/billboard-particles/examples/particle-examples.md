# Particle System Examples

Complete working implementations of particle effects for Nethercore ZX.

## Complete Particle System

Full-featured particle system with multiple effect types:

```rust
#![no_std]
#![no_main]

mod ffi;
use ffi::*;

const MAX_PARTICLES: usize = 512;

#[derive(Clone, Copy)]
#[repr(C)]
struct Particle {
    // Position
    x: f32, y: f32, z: f32,
    // Velocity
    vx: f32, vy: f32, vz: f32,
    // Appearance
    size: f32,
    size_end: f32,
    color_start: u32,
    color_end: u32,
    // Timing
    life: f32,
    max_life: f32,
    // Animation
    frame: u8,
    frame_count: u8,
    frame_rate: f32,
    frame_timer: f32,
    // Physics
    gravity: f32,
    drag: f32,
}

impl Default for Particle {
    fn default() -> Self {
        Self {
            x: 0.0, y: 0.0, z: 0.0,
            vx: 0.0, vy: 0.0, vz: 0.0,
            size: 1.0, size_end: 0.0,
            color_start: 0xFFFFFFFF, color_end: 0xFFFFFF00,
            life: 0.0, max_life: 1.0,
            frame: 0, frame_count: 1, frame_rate: 10.0, frame_timer: 0.0,
            gravity: 0.0, drag: 0.0,
        }
    }
}

static mut PARTICLES: [Particle; MAX_PARTICLES] = [Particle {
    x: 0.0, y: 0.0, z: 0.0,
    vx: 0.0, vy: 0.0, vz: 0.0,
    size: 1.0, size_end: 0.0,
    color_start: 0xFFFFFFFF, color_end: 0xFFFFFF00,
    life: 0.0, max_life: 1.0,
    frame: 0, frame_count: 1, frame_rate: 10.0, frame_timer: 0.0,
    gravity: 0.0, drag: 0.0,
}; MAX_PARTICLES];

static mut PARTICLE_TEX: u32 = 0;
static mut SPARK_TEX: u32 = 0;
static mut SMOKE_TEX: u32 = 0;

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        render_mode(2);
        set_clear_color(0x1a1a2eFF);

        PARTICLE_TEX = rom_texture_str("particle_atlas");  // 4x4 sprite sheet
        SPARK_TEX = rom_texture_str("spark");
        SMOKE_TEX = rom_texture_str("smoke");
    }
}

#[no_mangle]
pub extern "C" fn update() {
    unsafe {
        let dt = delta_time();
        update_particles(dt);

        // Demo: spawn effects on button press
        if button_pressed(0, button::A) != 0 {
            spawn_explosion(0.0, 1.0, 0.0);
        }
        if button_pressed(0, button::B) != 0 {
            spawn_fire_burst(0.0, 0.0, 0.0);
        }
        if button_pressed(0, button::X) != 0 {
            spawn_magic_sparkle(0.0, 1.0, 0.0);
        }
    }
}

unsafe fn update_particles(dt: f32) {
    for p in PARTICLES.iter_mut() {
        if p.life <= 0.0 { continue; }

        // Physics
        p.vx *= 1.0 - p.drag * dt;
        p.vy *= 1.0 - p.drag * dt;
        p.vz *= 1.0 - p.drag * dt;

        p.vy -= p.gravity * dt;

        p.x += p.vx * dt;
        p.y += p.vy * dt;
        p.z += p.vz * dt;

        // Animation
        if p.frame_count > 1 {
            p.frame_timer += dt;
            if p.frame_timer >= 1.0 / p.frame_rate {
                p.frame_timer = 0.0;
                p.frame = (p.frame + 1) % p.frame_count;
            }
        }

        // Lifetime
        p.life -= dt;
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        // Scene
        camera_set(0.0, 3.0, 8.0, 0.0, 1.0, 0.0);
        draw_env();

        // Ground plane
        push_identity();
        set_color(0x333344FF);
        draw_mesh(plane(10.0, 10.0, 1, 1));
        set_color(0xFFFFFFFF);

        // Render all particles
        render_particles();
    }
}

unsafe fn render_particles() {
    // Sort by distance for proper alpha blending (simplified: skip for now)

    texture_bind(PARTICLE_TEX);

    for p in PARTICLES.iter() {
        if p.life <= 0.0 { continue; }

        let t = p.life / p.max_life;  // 1.0 → 0.0

        // Interpolate size
        let size = p.size * t + p.size_end * (1.0 - t);

        // Interpolate color
        let color = lerp_color(p.color_end, p.color_start, t);

        push_identity();
        push_translate(p.x, p.y, p.z);

        // Draw with sprite sheet frame
        let frame = p.frame as u32;
        let col = frame % 4;
        let row = frame / 4;
        let u = col as f32 * 0.25;
        let v = row as f32 * 0.25;

        draw_billboard_region(
            size, size,
            u, v, 0.25, 0.25,
            billboard::SPHERICAL,
            color
        );
    }
}

fn lerp_color(a: u32, b: u32, t: f32) -> u32 {
    let ar = ((a >> 24) & 0xFF) as f32;
    let ag = ((a >> 16) & 0xFF) as f32;
    let ab = ((a >> 8) & 0xFF) as f32;
    let aa = (a & 0xFF) as f32;

    let br = ((b >> 24) & 0xFF) as f32;
    let bg = ((b >> 16) & 0xFF) as f32;
    let bb = ((b >> 8) & 0xFF) as f32;
    let ba = (b & 0xFF) as f32;

    let r = (ar + (br - ar) * t) as u32;
    let g = (ag + (bg - ag) * t) as u32;
    let bl = (ab + (bb - ab) * t) as u32;
    let a = (aa + (ba - aa) * t) as u32;

    (r << 24) | (g << 16) | (bl << 8) | a
}

// ============ EFFECT SPAWNERS ============

unsafe fn spawn_particle(config: Particle) -> bool {
    for p in PARTICLES.iter_mut() {
        if p.life <= 0.0 {
            *p = config;
            return true;
        }
    }
    false
}

unsafe fn spawn_explosion(x: f32, y: f32, z: f32) {
    // Central flash
    spawn_particle(Particle {
        x, y, z,
        vx: 0.0, vy: 0.0, vz: 0.0,
        size: 2.0, size_end: 4.0,
        color_start: 0xFFFFFFFF, color_end: 0xFFFF0000,
        life: 0.3, max_life: 0.3,
        gravity: 0.0, drag: 0.0,
        ..Particle::default()
    });

    // Debris
    for _ in 0..30 {
        let angle = random_f32() * 6.28;
        let speed = random_f32_range(3.0, 8.0);
        let up = random_f32_range(2.0, 6.0);

        spawn_particle(Particle {
            x: x + random_f32_range(-0.2, 0.2),
            y: y + random_f32_range(-0.2, 0.2),
            z: z + random_f32_range(-0.2, 0.2),
            vx: angle.cos() * speed,
            vy: up,
            vz: angle.sin() * speed,
            size: random_f32_range(0.1, 0.3),
            size_end: 0.0,
            color_start: 0xFF8800FF,
            color_end: 0x44220000,
            life: random_f32_range(0.5, 1.5),
            max_life: 1.5,
            gravity: 12.0,
            drag: 0.5,
            ..Particle::default()
        });
    }

    // Smoke trail
    for _ in 0..20 {
        spawn_particle(Particle {
            x: x + random_f32_range(-0.5, 0.5),
            y: y + random_f32_range(-0.5, 0.5),
            z: z + random_f32_range(-0.5, 0.5),
            vx: random_f32_range(-1.0, 1.0),
            vy: random_f32_range(1.0, 3.0),
            vz: random_f32_range(-1.0, 1.0),
            size: random_f32_range(0.3, 0.8),
            size_end: random_f32_range(1.0, 2.0),
            color_start: 0x888888FF,
            color_end: 0x44444400,
            life: random_f32_range(1.0, 2.0),
            max_life: 2.0,
            gravity: -0.5,  // rises
            drag: 2.0,
            ..Particle::default()
        });
    }
}

unsafe fn spawn_fire_burst(x: f32, y: f32, z: f32) {
    for _ in 0..15 {
        // Core (white/yellow)
        spawn_particle(Particle {
            x: x + random_f32_range(-0.1, 0.1),
            y,
            z: z + random_f32_range(-0.1, 0.1),
            vx: random_f32_range(-0.5, 0.5),
            vy: random_f32_range(2.0, 4.0),
            vz: random_f32_range(-0.5, 0.5),
            size: random_f32_range(0.2, 0.4),
            size_end: 0.0,
            color_start: 0xFFFF88FF,
            color_end: 0xFF440000,
            life: random_f32_range(0.3, 0.6),
            max_life: 0.6,
            gravity: -2.0,  // fire rises
            drag: 1.0,
            ..Particle::default()
        });

        // Outer (orange/red)
        spawn_particle(Particle {
            x: x + random_f32_range(-0.3, 0.3),
            y,
            z: z + random_f32_range(-0.3, 0.3),
            vx: random_f32_range(-1.0, 1.0),
            vy: random_f32_range(1.5, 3.0),
            vz: random_f32_range(-1.0, 1.0),
            size: random_f32_range(0.3, 0.6),
            size_end: 0.1,
            color_start: 0xFF6600FF,
            color_end: 0x88000000,
            life: random_f32_range(0.4, 0.8),
            max_life: 0.8,
            gravity: -1.5,
            drag: 1.5,
            ..Particle::default()
        });
    }
}

unsafe fn spawn_magic_sparkle(x: f32, y: f32, z: f32) {
    for _ in 0..25 {
        let angle = random_f32() * 6.28;
        let radius = random_f32_range(0.5, 2.0);
        let height = random_f32_range(-0.5, 1.5);

        spawn_particle(Particle {
            x: x + angle.cos() * radius * 0.3,
            y: y + height,
            z: z + angle.sin() * radius * 0.3,
            vx: angle.cos() * random_f32_range(0.5, 1.5),
            vy: random_f32_range(0.5, 2.0),
            vz: angle.sin() * random_f32_range(0.5, 1.5),
            size: random_f32_range(0.05, 0.15),
            size_end: 0.0,
            color_start: if random() % 2 == 0 { 0x88FFFFFF } else { 0xFF88FFFF },
            color_end: 0x4400FF00,
            life: random_f32_range(0.5, 1.2),
            max_life: 1.2,
            gravity: -0.5,
            drag: 0.8,
            ..Particle::default()
        });
    }
}
```

## Campfire Effect

Continuous fire with smoke:

```rust
static mut FIRE_TIMER: f32 = 0.0;

fn update() {
    unsafe {
        let dt = delta_time();
        FIRE_TIMER += dt;

        // Spawn fire particles continuously
        if FIRE_TIMER >= 0.05 {
            FIRE_TIMER = 0.0;
            spawn_campfire_particles(0.0, 0.0, 0.0);
        }
    }
}

unsafe fn spawn_campfire_particles(x: f32, y: f32, z: f32) {
    // Embers (small, fast, short-lived)
    for _ in 0..2 {
        spawn_particle(Particle {
            x: x + random_f32_range(-0.3, 0.3),
            y: y + 0.1,
            z: z + random_f32_range(-0.3, 0.3),
            vx: random_f32_range(-0.3, 0.3),
            vy: random_f32_range(2.0, 4.0),
            vz: random_f32_range(-0.3, 0.3),
            size: 0.08,
            size_end: 0.02,
            color_start: 0xFFCC00FF,
            color_end: 0xFF440000,
            life: random_f32_range(0.3, 0.6),
            max_life: 0.6,
            gravity: -3.0,
            drag: 0.5,
            ..Particle::default()
        });
    }

    // Flames (larger, billowy)
    spawn_particle(Particle {
        x: x + random_f32_range(-0.2, 0.2),
        y: y + 0.2,
        z: z + random_f32_range(-0.2, 0.2),
        vx: random_f32_range(-0.2, 0.2),
        vy: random_f32_range(1.0, 2.0),
        vz: random_f32_range(-0.2, 0.2),
        size: random_f32_range(0.3, 0.5),
        size_end: 0.1,
        color_start: 0xFF6600FF,
        color_end: 0x88000000,
        life: random_f32_range(0.5, 0.8),
        max_life: 0.8,
        gravity: -2.0,
        drag: 2.0,
        ..Particle::default()
    });

    // Occasional smoke
    if random() % 10 == 0 {
        spawn_particle(Particle {
            x: x + random_f32_range(-0.1, 0.1),
            y: y + 0.5,
            z: z + random_f32_range(-0.1, 0.1),
            vx: random_f32_range(-0.5, 0.5),
            vy: random_f32_range(0.5, 1.5),
            vz: random_f32_range(-0.5, 0.5),
            size: 0.3,
            size_end: 1.5,
            color_start: 0x66666688,
            color_end: 0x44444400,
            life: random_f32_range(2.0, 4.0),
            max_life: 4.0,
            gravity: -0.3,
            drag: 1.0,
            ..Particle::default()
        });
    }
}
```

## Waterfall Splash

```rust
unsafe fn spawn_waterfall_splash(x: f32, y: f32, z: f32) {
    // Mist cloud
    for _ in 0..5 {
        spawn_particle(Particle {
            x: x + random_f32_range(-1.0, 1.0),
            y: y + random_f32_range(0.0, 0.5),
            z: z + random_f32_range(-0.5, 0.5),
            vx: random_f32_range(-1.0, 1.0),
            vy: random_f32_range(0.5, 2.0),
            vz: random_f32_range(-0.3, 0.3),
            size: random_f32_range(0.5, 1.0),
            size_end: random_f32_range(1.5, 2.5),
            color_start: 0xAADDFF66,
            color_end: 0xAADDFF00,
            life: random_f32_range(1.0, 2.0),
            max_life: 2.0,
            gravity: 0.0,
            drag: 0.5,
            ..Particle::default()
        });
    }

    // Water droplets
    for _ in 0..8 {
        let angle = random_f32() * 6.28;
        let speed = random_f32_range(2.0, 5.0);

        spawn_particle(Particle {
            x,
            y: y + random_f32_range(0.0, 0.3),
            z,
            vx: angle.cos() * speed,
            vy: random_f32_range(3.0, 6.0),
            vz: angle.sin() * speed,
            size: random_f32_range(0.05, 0.12),
            size_end: 0.02,
            color_start: 0x88CCFFFF,
            color_end: 0x4488CC88,
            life: random_f32_range(0.5, 1.0),
            max_life: 1.0,
            gravity: 15.0,
            drag: 0.2,
            ..Particle::default()
        });
    }
}
```

## Footstep Dust

```rust
unsafe fn spawn_footstep_dust(x: f32, y: f32, z: f32, move_dir_x: f32, move_dir_z: f32) {
    for _ in 0..4 {
        spawn_particle(Particle {
            x: x + random_f32_range(-0.2, 0.2),
            y: y + 0.05,
            z: z + random_f32_range(-0.2, 0.2),
            // Particles move opposite to movement direction
            vx: -move_dir_x * random_f32_range(0.5, 1.0) + random_f32_range(-0.3, 0.3),
            vy: random_f32_range(0.3, 0.8),
            vz: -move_dir_z * random_f32_range(0.5, 1.0) + random_f32_range(-0.3, 0.3),
            size: random_f32_range(0.1, 0.2),
            size_end: random_f32_range(0.3, 0.5),
            color_start: 0x998866AA,
            color_end: 0x88775500,
            life: random_f32_range(0.4, 0.8),
            max_life: 0.8,
            gravity: 0.5,
            drag: 3.0,
            ..Particle::default()
        });
    }
}
```

## Trail Effect

Particles following a moving object:

```rust
static mut LAST_X: f32 = 0.0;
static mut LAST_Y: f32 = 0.0;
static mut LAST_Z: f32 = 0.0;
static mut TRAIL_TIMER: f32 = 0.0;

unsafe fn update_trail(obj_x: f32, obj_y: f32, obj_z: f32) {
    let dt = delta_time();
    TRAIL_TIMER += dt;

    if TRAIL_TIMER >= 0.02 {  // 50 particles/sec
        TRAIL_TIMER = 0.0;

        // Spawn at interpolated position for smooth trail
        let mid_x = (obj_x + LAST_X) * 0.5;
        let mid_y = (obj_y + LAST_Y) * 0.5;
        let mid_z = (obj_z + LAST_Z) * 0.5;

        spawn_particle(Particle {
            x: mid_x + random_f32_range(-0.1, 0.1),
            y: mid_y + random_f32_range(-0.1, 0.1),
            z: mid_z + random_f32_range(-0.1, 0.1),
            vx: 0.0, vy: 0.0, vz: 0.0,
            size: 0.2,
            size_end: 0.0,
            color_start: 0x00FFFFFF,  // Cyan
            color_end: 0x0044FF00,
            life: 0.5,
            max_life: 0.5,
            gravity: 0.0,
            drag: 0.0,
            ..Particle::default()
        });
    }

    LAST_X = obj_x;
    LAST_Y = obj_y;
    LAST_Z = obj_z;
}
```
