# Stencil Effect Examples

Complete working implementations of stencil-based effects for Nethercore ZX.

## Sniper Scope

Full implementation with zoom transition and scope overlay:

```rust
#![no_std]
#![no_main]

mod ffi;
use ffi::*;

static mut SCOPE_MESH: u32 = 0;
static mut SCOPE_TEXTURE: u32 = 0;
static mut WORLD_MESH: u32 = 0;

static mut SCOPED: bool = false;
static mut SCOPE_ZOOM: f32 = 1.0;
static mut TARGET_FOV: f32 = 60.0;
static mut CURRENT_FOV: f32 = 60.0;

const NORMAL_FOV: f32 = 60.0;
const SCOPED_FOV: f32 = 20.0;

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        render_mode(2);
        set_clear_color(0x1a1a2eFF);

        // Circle mesh for scope mask (use sphere, camera sees circular silhouette)
        SCOPE_MESH = sphere(1.0, 32, 16);
        SCOPE_TEXTURE = rom_texture_str("scope_overlay");
        WORLD_MESH = rom_mesh_str("level");
    }
}

#[no_mangle]
pub extern "C" fn update() {
    unsafe {
        let dt = delta_time();

        // Toggle scope with R1
        if button_pressed(0, button::R1) != 0 {
            SCOPED = !SCOPED;
            TARGET_FOV = if SCOPED { SCOPED_FOV } else { NORMAL_FOV };
        }

        // Smooth FOV transition
        let lerp_speed = 8.0 * dt;
        CURRENT_FOV += (TARGET_FOV - CURRENT_FOV) * lerp_speed.min(1.0);

        // Scope zoom for visual scaling
        SCOPE_ZOOM = NORMAL_FOV / CURRENT_FOV;
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        if SCOPED {
            render_scoped_view();
        } else {
            render_normal_view();
        }
    }
}

unsafe fn render_scoped_view() {
    // 1. Create circular mask
    stencil_begin();

    // Draw sphere at origin - camera looks straight at it = circle
    push_identity();
    push_scale_uniform(0.4);  // Adjust for scope size
    draw_mesh(SCOPE_MESH);

    stencil_end();

    // 2. Render world through scope (zoomed FOV)
    camera_fov(CURRENT_FOV);
    camera_set(0.0, 1.6, 5.0, 0.0, 1.0, 0.0);
    draw_env();
    draw_mesh(WORLD_MESH);

    stencil_clear();

    // 3. Draw scope overlay on top (crosshairs, edge ring)
    texture_bind(SCOPE_TEXTURE);
    draw_sprite(0.0, 0.0, 960.0, 540.0, 0xFFFFFFFF);

    // Black bars outside scope
    draw_rect(0.0, 0.0, 280.0, 540.0, 0x000000FF);      // Left
    draw_rect(680.0, 0.0, 280.0, 540.0, 0x000000FF);    // Right
    draw_rect(280.0, 0.0, 400.0, 70.0, 0x000000FF);     // Top
    draw_rect(280.0, 470.0, 400.0, 70.0, 0x000000FF);   // Bottom
}

unsafe fn render_normal_view() {
    camera_fov(CURRENT_FOV);
    camera_set(0.0, 1.6, 5.0, 0.0, 1.0, 0.0);
    draw_env();
    draw_mesh(WORLD_MESH);

    // Simple crosshair when not scoped
    let cx = 480.0;
    let cy = 270.0;
    draw_line(cx - 10.0, cy, cx + 10.0, cy, 2.0, 0xFFFFFFFF);
    draw_line(cx, cy - 10.0, cx, cy + 10.0, 2.0, 0xFFFFFFFF);
}
```

## Magic Portal Between Worlds

Two-way portal connecting different environments:

```rust
#![no_std]
#![no_main]

mod ffi;
use ffi::*;

static mut PORTAL_QUAD: u32 = 0;
static mut PORTAL_FRAME: u32 = 0;
static mut WORLD_A_MESH: u32 = 0;
static mut WORLD_B_MESH: u32 = 0;

// Player in world A
static mut PLAYER_X: f32 = 0.0;
static mut PLAYER_Z: f32 = 5.0;
static mut IN_WORLD_A: bool = true;

// Portal position
const PORTAL_X: f32 = 0.0;
const PORTAL_Y: f32 = 1.5;
const PORTAL_Z: f32 = 0.0;

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        render_mode(2);

        // Portal is a vertical quad
        PORTAL_QUAD = plane_uv(1.5, 2.0, 1, 1);
        PORTAL_FRAME = torus(1.6, 0.1, 32, 8);

        WORLD_A_MESH = rom_mesh_str("forest");
        WORLD_B_MESH = rom_mesh_str("dungeon");
    }
}

#[no_mangle]
pub extern "C" fn update() {
    unsafe {
        let dt = delta_time();
        let speed = 5.0 * dt;

        // Movement
        if button_held(0, button::UP) != 0 { PLAYER_Z -= speed; }
        if button_held(0, button::DOWN) != 0 { PLAYER_Z += speed; }
        if button_held(0, button::LEFT) != 0 { PLAYER_X -= speed; }
        if button_held(0, button::RIGHT) != 0 { PLAYER_X += speed; }

        // Check portal collision
        let dx = PLAYER_X - PORTAL_X;
        let dz = PLAYER_Z - PORTAL_Z;
        if dx*dx + dz*dz < 1.0 {
            // Stepped through portal
            IN_WORLD_A = !IN_WORLD_A;
            PLAYER_Z = if IN_WORLD_A { 5.0 } else { -5.0 };
        }
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        let cam_y = 2.0;
        let cam_z_offset = 8.0;

        let (current_world, other_world) = if IN_WORLD_A {
            (WORLD_A_MESH, WORLD_B_MESH)
        } else {
            (WORLD_B_MESH, WORLD_A_MESH)
        };

        // 1. Draw portal mask
        stencil_begin();
        push_identity();
        push_translate(PORTAL_X, PORTAL_Y, PORTAL_Z);
        push_rotate_x(90.0);  // Stand portal upright
        draw_mesh(PORTAL_QUAD);
        stencil_end();

        // 2. Render other world through portal
        // Camera looks through portal to other side
        camera_set(
            PLAYER_X, cam_y, PLAYER_Z,
            PORTAL_X, PORTAL_Y, PORTAL_Z
        );

        // Different environment for other world
        if IN_WORLD_A {
            env_gradient(0, 0x2a0a3aFF, 0x4a1a5aFF, 0x1a0a2aFF, 0x0a0010FF, 0.0, 0.0);
        } else {
            env_gradient(0, 0x87CEEBFF, 0xADD8E6FF, 0x228B22FF, 0x006400FF, 0.0, 0.0);
        }
        draw_env();
        draw_mesh(other_world);

        stencil_clear();

        // 3. Render current world
        camera_set(
            PLAYER_X, cam_y, PLAYER_Z + cam_z_offset,
            PLAYER_X, 1.0, PLAYER_Z
        );

        if IN_WORLD_A {
            env_gradient(0, 0x87CEEBFF, 0xADD8E6FF, 0x228B22FF, 0x006400FF, 0.0, 0.0);
        } else {
            env_gradient(0, 0x2a0a3aFF, 0x4a1a5aFF, 0x1a0a2aFF, 0x0a0010FF, 0.0, 0.0);
        }
        draw_env();
        draw_mesh(current_world);

        // 4. Draw portal frame (decorative)
        push_identity();
        push_translate(PORTAL_X, PORTAL_Y, PORTAL_Z);
        push_rotate_x(90.0);
        set_color(0x8844FFFF);  // Purple glow
        material_emissive(0.5);
        draw_mesh(PORTAL_FRAME);
        material_emissive(0.0);
        set_color(0xFFFFFFFF);
    }
}
```

## Rear-View Mirror

Racing game rear-view mirror using stencil:

```rust
// In render():
unsafe fn render_with_mirror() {
    // Main view first
    camera_set(car_x, car_y + 1.0, car_z,
               car_x + forward_x * 10.0, car_y + 1.0, car_z + forward_z * 10.0);
    draw_env();
    draw_mesh(TRACK_MESH);
    draw_mesh(OTHER_CARS_MESH);

    // Mirror in top-center of screen
    let mirror_x = 380.0;
    let mirror_y = 20.0;
    let mirror_w = 200.0;
    let mirror_h = 60.0;

    // 1. Stencil mask for mirror shape
    stencil_begin();
    draw_rect(mirror_x, mirror_y, mirror_w, mirror_h, 0xFFFFFFFF);
    stencil_end();

    // 2. Render rear view (flipped direction)
    camera_set(car_x, car_y + 1.0, car_z,
               car_x - forward_x * 10.0, car_y + 1.0, car_z - forward_z * 10.0);

    // Use viewport to map 3D to mirror area
    viewport(mirror_x as u32, mirror_y as u32, mirror_w as u32, mirror_h as u32);
    draw_env();
    draw_mesh(TRACK_MESH);
    draw_mesh(OTHER_CARS_MESH);
    viewport_clear();

    stencil_clear();

    // 3. Mirror frame
    draw_rect(mirror_x - 2.0, mirror_y - 2.0, mirror_w + 4.0, mirror_h + 4.0, 0x333333FF);
}
```

## Spotlight Effect

Illuminate only a circular area (horror game style):

```rust
unsafe fn render_spotlight() {
    // Dark ambient everywhere
    env_gradient(0, 0x0a0a0aFF, 0x050505FF, 0x020202FF, 0x000000FF, 0.0, 0.0);

    // 1. Stencil for spotlight area
    stencil_begin();
    // Spotlight follows mouse/stick position
    draw_circle(spotlight_x, spotlight_y, 80.0, 0xFFFFFFFF);
    stencil_end();

    // 2. Render scene normally (lit) in spotlight
    light_set(0, 0.0, -1.0, 0.0);
    light_intensity(0, 1.0);
    draw_env();
    draw_mesh(SCENE_MESH);

    stencil_clear();

    // 3. Render scene very dark outside spotlight
    stencil_begin();
    draw_circle(spotlight_x, spotlight_y, 80.0, 0xFFFFFFFF);
    stencil_invert();  // Outside the circle

    light_intensity(0, 0.05);  // Very dim
    draw_mesh(SCENE_MESH);

    stencil_clear();

    // 4. Soft edge gradient (optional)
    uniform_alpha(4);
    draw_circle(spotlight_x, spotlight_y, 90.0, 0x000000FF);
    uniform_alpha(15);
}
```

## Picture-in-Picture

Security camera view in corner:

```rust
unsafe fn render_pip_camera() {
    // Main player view
    camera_set(player_x, player_y + 1.6, player_z,
               player_x + look_x, player_y + 1.6 + look_y, player_z + look_z);
    draw_env();
    draw_mesh(LEVEL_MESH);

    // PIP in bottom-left corner
    let pip_x = 20.0;
    let pip_y = 380.0;
    let pip_w = 200.0;
    let pip_h = 150.0;

    // 1. Stencil mask
    stencil_begin();
    draw_rect(pip_x, pip_y, pip_w, pip_h, 0xFFFFFFFF);
    stencil_end();

    // 2. Security camera view
    camera_set(
        SECURITY_CAM_X, SECURITY_CAM_Y, SECURITY_CAM_Z,
        SECURITY_CAM_TARGET_X, SECURITY_CAM_TARGET_Y, SECURITY_CAM_TARGET_Z
    );
    viewport(pip_x as u32, pip_y as u32, pip_w as u32, pip_h as u32);

    // Grainy security cam look
    set_color(0xAAAAAAFF);
    draw_mesh(LEVEL_MESH);
    set_color(0xFFFFFFFF);

    viewport_clear();
    stencil_clear();

    // 3. PIP border and label
    draw_rect(pip_x - 2.0, pip_y - 2.0, pip_w + 4.0, pip_h + 4.0, 0x00FF00FF);
    draw_text_str("CAM 01", pip_x + 5.0, pip_y + 5.0, 12.0, 0x00FF00FF);

    // Scanline effect
    for i in 0..10 {
        let y = pip_y + (i as f32) * 15.0;
        draw_line(pip_x, y, pip_x + pip_w, y, 1.0, 0x00FF0020);
    }
}
```
