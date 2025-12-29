---
name: Rendering Techniques
description: This skill should be used when the user asks about "stencil buffer", "stencil_begin", "portal rendering", "mirror reflection", "masked rendering", "custom font", "bitmap font", "load_font", "font_bind", "text rendering", "font atlas", "billboard", "particles", "draw_billboard", "particle system", "smoke effect", "fire effect", "sparks", "explosion effect", "camera-facing quad", "3D sprite", "vignette", "scope effect", or mentions implementing advanced rendering effects, text display, particle systems, or stencil-based masking for Nethercore ZX games.
version: 1.0.0
---

# Rendering Techniques for Nethercore ZX

Advanced rendering techniques including stencil buffer effects, custom fonts, and billboard particles. These techniques share a common theme: specialized rendering beyond basic mesh and sprite drawing.

---

## Part 1: Stencil Buffer Effects

Implement masked rendering using the ZX stencil buffer. Create portals, scopes, mirrors, and shaped UI elements.

### Stencil FFI Functions

Reference `nethercore/include/zx.rs` lines 419-471:

| Function | Purpose |
|----------|---------|
| `stencil_begin()` | Start writing to stencil buffer (mask creation) |
| `stencil_end()` | End mask creation, begin stencil testing |
| `stencil_clear()` | Return to normal rendering |
| `stencil_invert()` | Render outside the mask instead of inside |

### Stencil Flow

The stencil buffer works in three phases:

1. **Mask Creation** - Draw shapes that define the visible area
2. **Masked Rendering** - Only pixels inside mask are drawn
3. **Cleanup** - Return to normal rendering

```
stencil_begin()     → Draw mask shape (color buffer ignored)
stencil_end()       → Activate testing (draw only where mask exists)
[draw scene]        → Scene only visible inside mask
stencil_clear()     → Back to normal rendering
```

### Circular Scope Effect

```rust
static mut CIRCLE_MESH: u32 = 0;

fn init() {
    unsafe {
        CIRCLE_MESH = sphere(1.0, 32, 16);
    }
}

fn render() {
    unsafe {
        // 1. Draw scope mask
        stencil_begin();
        push_identity();
        push_translate(0.0, 0.0, 0.0);
        push_scale_uniform(0.8);
        draw_mesh(CIRCLE_MESH);
        stencil_end();

        // 2. Draw world (only visible inside circle)
        camera_set(cam_x, cam_y, cam_z, target_x, target_y, target_z);
        draw_env();
        draw_mesh(WORLD_MESH);

        // 3. Clear stencil for HUD
        stencil_clear();

        // Draw scope overlay texture on top
        texture_bind(SCOPE_TEXTURE);
        draw_sprite(0.0, 0.0, 960.0, 540.0, 0xFFFFFFFF);
    }
}
```

### Portal/Window Effect

Render a different scene through a portal:

```rust
fn render_portal() {
    unsafe {
        // 1. Draw portal frame shape to stencil
        stencil_begin();
        push_identity();
        push_translate(portal_x, portal_y, portal_z);
        draw_mesh(PORTAL_FRAME_MESH);
        stencil_end();

        // 2. Render "other side" scene inside portal
        camera_set(other_cam_x, other_cam_y, other_cam_z,
                   other_target_x, other_target_y, other_target_z);
        draw_env();
        draw_mesh(OTHER_WORLD_MESH);

        stencil_clear();

        // 3. Render main scene
        camera_set(cam_x, cam_y, cam_z, target_x, target_y, target_z);
        draw_env();
        draw_mesh(MAIN_WORLD_MESH);
    }
}
```

### Mirror Reflection

Use stencil with flipped camera:

```rust
fn render_mirror() {
    unsafe {
        stencil_begin();
        push_translate(mirror_x, mirror_y, mirror_z);
        draw_mesh(MIRROR_QUAD);
        stencil_end();

        // Flip camera Y around mirror plane
        let reflected_y = 2.0 * mirror_y - cam_y;
        camera_set(cam_x, reflected_y, cam_z, target_x, target_y, target_z);

        cull_mode(2);  // Front-face culling for reflected geometry
        draw_mesh(SCENE_MESH);
        cull_mode(1);  // Back to normal

        stencil_clear();

        // Render normal scene
        camera_set(cam_x, cam_y, cam_z, target_x, target_y, target_z);
        draw_mesh(SCENE_MESH);
    }
}
```

### Vignette Effect

Use inverted stencil for screen edges:

```rust
fn render_vignette() {
    unsafe {
        stencil_begin();
        draw_mesh(ROUNDED_RECT_MESH);

        stencil_invert();  // Render OUTSIDE the mask

        set_color(0x00000080);
        draw_rect(0.0, 0.0, 960.0, 540.0, 0x000000C0);

        stencil_clear();
    }
}
```

---

## Part 2: Custom Fonts

Load and render custom bitmap fonts. ZX provides a built-in 8x8 monospace font but supports custom fixed-width and variable-width bitmap fonts.

### Font FFI Functions

Reference `nethercore/include/zx.rs` lines 751-784:

| Function | Purpose |
|----------|---------|
| `load_font(texture, width, height, first_codepoint, count)` | Load fixed-width bitmap font |
| `load_font_ex(texture, widths_ptr, height, first_codepoint, count)` | Load variable-width font |
| `font_bind(handle)` | Bind font for draw_text() |
| `rom_font(id_ptr, id_len)` | Load font atlas from ROM |

### Font Atlas Format

Font textures contain glyphs arranged in a grid, row-major order:

```
+---+---+---+---+---+---+---+---+   ← Row 0: glyphs 0-7
| ! | " | # | $ | % | & | ' | ( |
+---+---+---+---+---+---+---+---+
| ) | * | + | , | - | . | / | 0 |   ← Row 1: glyphs 8-15
+---+---+---+---+---+---+---+---+
```

For ASCII printable characters (space through ~):
- `first_codepoint = 32` (space character)
- `char_count = 95` (32 to 126 inclusive)

### Fixed-Width Font

```rust
static mut GAME_FONT: u32 = 0;

fn init() {
    unsafe {
        let font_texture = rom_texture_str("pixel_font");

        // Create font: 8px wide, 12px tall glyphs
        GAME_FONT = load_font(
            font_texture,
            8,   // char_width
            12,  // char_height
            32,  // first_codepoint (space)
            96   // char_count
        );
    }
}

fn render() {
    unsafe {
        font_bind(GAME_FONT);
        draw_text_str("SCORE: 1000", 10.0, 10.0, 24.0, 0xFFFFFFFF);
        font_bind(0);  // Return to built-in font
    }
}
```

### Variable-Width Font

```rust
static GLYPH_WIDTHS: [u8; 96] = [
    4, 3, 5, 7, 6, 8, 7, 3, 4, 4, 5, 6, 3, 5, 3, 5,  // space ! " # ...
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6,  // 0-9
    // ... continue for all characters
];

fn init() {
    unsafe {
        let font_texture = rom_texture_str("proportional_font");

        PROP_FONT = load_font_ex(
            font_texture,
            GLYPH_WIDTHS.as_ptr(),
            16,  // char_height
            32,  // first_codepoint
            96   // char_count
        );
    }
}
```

### Font Scaling and Measurement

```rust
// Scale is relative to glyph height
font_bind(GAME_FONT);
draw_text_str("Small", 10.0, 10.0, 12.0, 0xFFFFFFFF);
draw_text_str("Large", 10.0, 30.0, 48.0, 0xFFFFFFFF);

// Measure for centering
fn draw_centered_text(text: &str, y: f32, size: f32, color: u32) {
    unsafe {
        let width = text_width(text.as_ptr(), text.len() as u32, size);
        let x = (960.0 - width) / 2.0;
        draw_text(text.as_ptr(), text.len() as u32, x, y, size, color);
    }
}
```

### Recommended Font Dimensions

| Style | Glyph Size | Atlas Size | Characters |
|-------|------------|------------|------------|
| Tiny | 4x6 | 64x36 | 96 |
| Small | 8x8 | 128x48 | 96 |
| Medium | 8x12 | 128x72 | 96 |
| Large | 16x16 | 256x96 | 96 |

---

## Part 3: Billboard Particles

Implement camera-facing sprites and particle systems. Billboards always face the camera, ideal for particles, foliage, and impostor sprites.

### Billboard FFI Functions

Reference `nethercore/include/zx.rs` lines 644-662:

| Function | Purpose |
|----------|---------|
| `draw_billboard(w, h, mode, color)` | Draw camera-facing quad with full texture |
| `draw_billboard_region(w, h, src_x, src_y, src_w, src_h, mode, color)` | Draw with UV region |

### Billboard Modes

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

### Basic Billboard Usage

```rust
fn render() {
    unsafe {
        texture_bind(PARTICLE_TEX);
        push_identity();
        push_translate(5.0, 2.0, 0.0);
        draw_billboard(1.0, 1.0, billboard::SPHERICAL, 0xFFFFFFFF);
    }
}
```

### Particle System

```rust
const MAX_PARTICLES: usize = 256;

#[derive(Clone, Copy, Default)]
struct Particle {
    x: f32, y: f32, z: f32,
    vx: f32, vy: f32, vz: f32,
    life: f32, max_life: f32,
    size: f32, color: u32,
}

static mut PARTICLES: [Particle; MAX_PARTICLES] = [Particle {
    x: 0.0, y: 0.0, z: 0.0,
    vx: 0.0, vy: 0.0, vz: 0.0,
    life: 0.0, max_life: 1.0,
    size: 1.0, color: 0xFFFFFFFF,
}; MAX_PARTICLES];

fn update_particles() {
    unsafe {
        let dt = delta_time();
        for p in PARTICLES.iter_mut() {
            if p.life > 0.0 {
                p.x += p.vx * dt;
                p.y += p.vy * dt;
                p.z += p.vz * dt;
                p.vy -= 9.8 * dt;  // Gravity
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
                let t = p.life / p.max_life;
                let alpha = (t * 255.0) as u8;
                let color = (p.color & 0xFFFFFF00) | alpha as u32;
                let size = p.size * t;

                push_identity();
                push_translate(p.x, p.y, p.z);
                draw_billboard(size, size, billboard::SPHERICAL, color);
            }
        }
    }
}
```

### Common Particle Effects

**Smoke:**
```rust
fn spawn_smoke(x: f32, y: f32, z: f32) {
    spawn_particle(x, y, z,
        random_f32_range(-0.5, 0.5),   // vx
        random_f32_range(1.0, 2.0),    // vy
        random_f32_range(-0.5, 0.5),   // vz
        random_f32_range(1.0, 3.0),    // life
        random_f32_range(0.5, 1.5),    // size
        0x888888FF);                   // gray
}
```

**Fire:**
```rust
fn spawn_fire(x: f32, y: f32, z: f32) {
    spawn_particle(x, y, z, 0.0, 3.0, 0.0, 0.3, 0.4, 0xFFFF88FF);  // Core
    spawn_particle(x, y, z, random_f32_range(-1.0, 1.0), 2.5, 0.0, 0.5, 0.6, 0xFF8800FF);  // Mid
    spawn_particle(x, y, z, random_f32_range(-1.5, 1.5), 2.0, 0.0, 0.7, 0.8, 0xFF4400FF);  // Outer
}
```

**Sparks:**
```rust
fn spawn_sparks(x: f32, y: f32, z: f32) {
    for _ in 0..10 {
        spawn_particle(x, y, z,
            random_f32_range(-5.0, 5.0),
            random_f32_range(2.0, 8.0),
            random_f32_range(-5.0, 5.0),
            random_f32_range(0.2, 0.5),
            random_f32_range(0.05, 0.15),
            0xFFFF00FF);
    }
}
```

### Foliage Billboards

Use cylindrical Y for upright vegetation:

```rust
fn render_tree(x: f32, y: f32, z: f32) {
    unsafe {
        texture_bind(TREE_TEXTURE);
        push_identity();
        push_translate(x, y + 2.0, z);
        draw_billboard(2.0, 4.0, billboard::CYLINDRICAL_Y, 0xFFFFFFFF);
    }
}
```

### Performance Guidelines

| Particle Count | Performance |
|----------------|-------------|
| 0-100 | Excellent |
| 100-500 | Good |
| 500-1000 | Moderate |
| 1000+ | Consider optimization |

**Optimization Tips:**
- Pool particles: Reuse dead particles
- LOD: Reduce particle count at distance
- Texture atlas: Single bind for all particle types
- Skip invisible: Don't render particles behind camera

---

## Rollback Safety

All techniques are render-only:
- Stencil state resets each frame
- Font handles created in `init()` never change
- Particle state in static variables auto-snapshots
- Use `random()` FFI for particle randomness

---

## Additional Resources

- **`nethercore/include/zx.rs`** lines 419-471 - Stencil FFI
- **`nethercore/include/zx.rs`** lines 751-784 - Font FFI
- **`nethercore/include/zx.rs`** lines 644-662 - Billboard FFI
- **`game-feel`** skill - Particle integration with juice effects
- **`camera-systems`** skill - Camera flip for mirror reflections
