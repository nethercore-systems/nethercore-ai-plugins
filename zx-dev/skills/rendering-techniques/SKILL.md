---
name: Rendering Techniques
description: |
  This skill covers advanced ZX rendering: stencil effects, custom fonts, billboard particles. Triggers on "stencil buffer", "portal rendering", "mirror", "custom font", "bitmap font", "billboard", "particles", "smoke/fire effect", "text rendering".

  **Load references when:**
  - Particle system examples → Reference skill body (core patterns below)
  - Font atlas creation → See details below
  - FFI details → Read `nethercore/include/zx.rs` lines 419-471 (stencil), 751-784 (font), 644-662 (billboard)
version: 2.0.0
---

# Rendering Techniques for Nethercore ZX

Advanced rendering: stencil buffer, custom fonts, billboard particles.

## Stencil Buffer Effects

Create portals, scopes, mirrors, and masked UI elements.

### Stencil FFI

| Function | Purpose |
|----------|---------|
| `stencil_begin()` | Start mask creation |
| `stencil_end()` | Activate mask testing |
| `stencil_clear()` | Return to normal |
| `stencil_invert()` | Render outside mask |

### Stencil Flow

```
stencil_begin()  → Draw mask shape (colors ignored)
stencil_end()    → Scene only draws inside mask
[draw scene]
stencil_clear()  → Normal rendering resumes
```

### Scope Effect (Circular Mask)

```rust
fn render_scoped_view() {
    stencil_begin();
    push_scale_uniform(0.8);
    draw_mesh(CIRCLE_MESH);  // Creates circular mask
    stencil_end();

    // World only visible inside circle
    camera_set(cam_x, cam_y, cam_z, tx, ty, tz);
    draw_env();
    draw_mesh(WORLD_MESH);

    stencil_clear();
    texture_bind(SCOPE_OVERLAY);
    draw_sprite(0.0, 0.0, 960.0, 540.0, 0xFFFFFFFF);
}
```

### Portal Effect

```rust
fn render_portal() {
    stencil_begin();
    push_translate(portal_x, portal_y, portal_z);
    draw_mesh(PORTAL_FRAME);
    stencil_end();

    // Other world inside portal
    camera_set(other_cam...);
    draw_mesh(OTHER_WORLD);

    stencil_clear();

    // Main world
    camera_set(main_cam...);
    draw_mesh(MAIN_WORLD);
}
```

### Vignette (Inverted Mask)

```rust
stencil_begin();
draw_mesh(ROUNDED_RECT);
stencil_invert();  // Render OUTSIDE mask
draw_rect(0.0, 0.0, 960.0, 540.0, 0x000000C0);  // Darken edges
stencil_clear();
```

## Custom Fonts

Load bitmap fonts for styled text rendering.

### Font FFI

| Function | Purpose |
|----------|---------|
| `load_font(tex, w, h, first, count)` | Fixed-width font |
| `load_font_ex(tex, widths, h, first, count)` | Variable-width |
| `font_bind(handle)` | Bind for draw_text |

### Font Atlas Format

Glyphs in row-major grid. For ASCII printables: `first_codepoint=32`, `count=96`.

### Fixed-Width Font

```rust
static mut GAME_FONT: u32 = 0;

fn init() {
    let tex = rom_texture_str("pixel_font");
    GAME_FONT = load_font(tex, 8, 12, 32, 96);  // 8x12 glyphs
}

fn render() {
    font_bind(GAME_FONT);
    draw_text_str("SCORE: 1000", 10.0, 10.0, 24.0, 0xFFFFFFFF);
    font_bind(0);  // Back to default
}
```

### Recommended Sizes

| Style | Glyph | Atlas |
|-------|-------|-------|
| Tiny | 4x6 | 64x36 |
| Small | 8x8 | 128x48 |
| Medium | 8x12 | 128x72 |
| Large | 16x16 | 256x96 |

## Billboard Particles

Camera-facing sprites for effects.

### Billboard FFI

| Function | Purpose |
|----------|---------|
| `draw_billboard(w, h, mode, color)` | Full texture |
| `draw_billboard_region(w,h, sx,sy,sw,sh, mode, color)` | UV region |

### Billboard Modes

| Mode | Constant | Use |
|------|----------|-----|
| 1 | SPHERICAL | Particles (faces camera) |
| 2 | CYLINDRICAL_Y | Trees, grass (upright) |

### Particle System (Core Pattern)

```rust
const MAX: usize = 256;

#[derive(Copy, Clone, Default)]
struct Particle { x: f32, y: f32, z: f32, vx: f32, vy: f32, vz: f32, life: f32, size: f32, color: u32 }

static mut PARTICLES: [Particle; MAX] = [Particle { x:0.0, y:0.0, z:0.0, vx:0.0, vy:0.0, vz:0.0, life:0.0, size:1.0, color:0xFFFFFFFF }; MAX];

fn update_particles() {
    let dt = delta_time();
    for p in unsafe { PARTICLES.iter_mut() } {
        if p.life > 0.0 {
            p.x += p.vx * dt; p.y += p.vy * dt; p.z += p.vz * dt;
            p.vy -= 9.8 * dt;
            p.life -= dt;
        }
    }
}

fn render_particles(tex: u32) {
    texture_bind(tex);
    for p in unsafe { PARTICLES.iter() } {
        if p.life > 0.0 {
            let alpha = ((p.life / 1.0) * 255.0) as u8;
            push_translate(p.x, p.y, p.z);
            draw_billboard(p.size, p.size, 1, (p.color & 0xFFFFFF00) | alpha as u32);
            push_identity();
        }
    }
}
```

### Effect Recipes

**Smoke:** `vx/vz = ±0.5`, `vy = 1-2`, `life = 1-3s`, `color = 0x888888FF`
**Fire:** `vy = 2-3`, `life = 0.3-0.7s`, `colors = 0xFFFF88/FF8800/FF4400`
**Sparks:** `vx/vy/vz = ±5`, `life = 0.2-0.5s`, `size = 0.05-0.15`, `color = 0xFFFF00FF`

### Performance

| Particles | Impact |
|-----------|--------|
| 0-100 | Excellent |
| 100-500 | Good |
| 500-1000 | Moderate |
| 1000+ | Optimize |

**Tips:** Pool particles, LOD at distance, texture atlas, cull behind camera.

## Rollback Safety

All rendering is display-only. Particle state in static variables (auto-snapshotted). Use FFI `random()` for spawn variation.
