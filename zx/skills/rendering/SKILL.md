---
name: ZX Rendering
description: |
  ZX rendering techniques: cameras, stencil effects, particles, fonts. Triggers on "ZX camera", "orbit camera", "stencil buffer", "portal", "billboard", "particles", "custom font", "render pass".

  **Load references when:**
  - Camera implementations -> `references/camera-systems.md`
  - Stencil/portal effects -> `references/effects.md`
version: 1.0.0
---

# ZX Rendering Techniques

## Camera Systems

All camera state in static variables for rollback safety.

### Camera FFI

| Function | Purpose |
|----------|---------|
| `camera_set(x,y,z, tx,ty,tz)` | Position + look-at |
| `camera_fov(degrees)` | Field of view (default 60) |

### Follow Camera (Core)

```rust
static mut CAM_X: f32 = 0.0;
static mut CAM_Y: f32 = 5.0;
static mut CAM_Z: f32 = 10.0;

fn update_follow_camera(tx: f32, ty: f32, tz: f32) {
    let dt = delta_time();
    let t = (5.0 * dt).min(1.0);
    unsafe {
        CAM_X += (tx - CAM_X) * t;
        CAM_Y += (ty + 5.0 - CAM_Y) * t;
        CAM_Z += (tz + 10.0 - CAM_Z) * t;
    }
}
```

## Render Passes & Stencil

Create portals, scopes, masks using render passes.

| Function | Purpose |
|----------|---------|
| `begin_pass(clear_depth)` | New pass |
| `begin_pass_stencil_write(ref, clear)` | Create mask |
| `begin_pass_stencil_test(ref, clear)` | Render in mask |

### Basic Stencil Flow

```rust
// 1. Create mask
begin_pass_stencil_write(1, 0);
draw_circle(SCREEN_CX, SCREEN_CY, 200.0);

// 2. Render inside mask
begin_pass_stencil_test(1, 0);
draw_scene();

// 3. Return to normal
begin_pass(0);
```

## Billboard Particles

| Function | Mode | Use |
|----------|------|-----|
| `draw_billboard(w, h, 1, color)` | Spherical | Particles |
| `draw_billboard(w, h, 2, color)` | Cylindrical | Trees |

### Particle System Core

```rust
#[derive(Copy, Clone, Default)]
struct Particle { x: f32, y: f32, z: f32, vx: f32, vy: f32, vz: f32, life: f32 }

static mut PARTICLES: [Particle; 256] = [...];

fn render_particles(tex: u32) {
    texture_bind(tex);
    for p in unsafe { PARTICLES.iter() } {
        if p.life > 0.0 {
            push_translate(p.x, p.y, p.z);
            draw_billboard(1.0, 1.0, 1, 0xFFFFFFFF);
            push_identity();
        }
    }
}
```

## Custom Fonts

```rust
let tex = rom_texture_str("pixel_font");
let font = load_font(tex, 8, 12, 32, 96);  // 8x12 glyphs

// In render:
font_bind(font);
draw_text_str("SCORE", 10.0, 10.0, 24.0, 0xFFFFFFFF);
font_bind(0);  // Back to default
```

## Coordinate Convention

Y-up, right-handed, -Z forward. When yaw=0, camera looks toward -Z.
