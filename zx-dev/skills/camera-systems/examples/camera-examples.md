# Camera System Examples

Complete, working Rust implementations for common camera patterns.

## Follow Camera (Platformer Style)

```rust
#![no_std]
#![no_main]

mod ffi;
use ffi::*;

// Game state
static mut PLAYER_X: f32 = 0.0;
static mut PLAYER_Y: f32 = 0.0;
static mut PLAYER_Z: f32 = 0.0;
static mut PLAYER_VX: f32 = 0.0;
static mut PLAYER_VZ: f32 = 0.0;

// Camera state
static mut CAM_X: f32 = 0.0;
static mut CAM_Y: f32 = 8.0;
static mut CAM_Z: f32 = 15.0;

// Camera config
const CAM_OFFSET_Y: f32 = 8.0;
const CAM_OFFSET_Z: f32 = 15.0;
const CAM_SMOOTH: f32 = 4.0;
const LOOK_AHEAD: f32 = 3.0;
const DEAD_ZONE: f32 = 1.5;

static mut MESH_PLAYER: u32 = 0;
static mut MESH_GROUND: u32 = 0;

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        set_clear_color(0x2a2a4aFF);
        render_mode(2);

        MESH_PLAYER = cube(0.5, 1.0, 0.5);
        MESH_GROUND = plane(50.0, 50.0, 1, 1);
    }
}

#[no_mangle]
pub extern "C" fn update() {
    let dt = unsafe { delta_time() };

    unsafe {
        // Player movement
        let move_x = left_stick_x(0);
        let move_z = -left_stick_y(0); // Invert for forward = up

        const SPEED: f32 = 10.0;
        PLAYER_VX = move_x * SPEED;
        PLAYER_VZ = move_z * SPEED;

        PLAYER_X += PLAYER_VX * dt;
        PLAYER_Z += PLAYER_VZ * dt;

        // Follow camera with dead zone and look-ahead
        let target_x = PLAYER_X + PLAYER_VX * LOOK_AHEAD * 0.1;
        let target_z = PLAYER_Z + PLAYER_VZ * LOOK_AHEAD * 0.1;

        let dx = target_x - CAM_X;
        let dz = (target_z + CAM_OFFSET_Z) - CAM_Z;
        let dist = (dx * dx + dz * dz).sqrt();

        if dist > DEAD_ZONE {
            let t = (CAM_SMOOTH * dt).min(1.0);
            CAM_X = lerp(CAM_X, target_x, t);
            CAM_Z = lerp(CAM_Z, target_z + CAM_OFFSET_Z, t);
        }

        CAM_Y = lerp(CAM_Y, PLAYER_Y + CAM_OFFSET_Y, CAM_SMOOTH * dt);
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        draw_env();

        // Set camera
        camera_set(CAM_X, CAM_Y, CAM_Z, PLAYER_X, PLAYER_Y + 1.0, PLAYER_Z);

        // Set up lighting
        light_set(0, 0.5, -1.0, 0.3);
        light_intensity(0, 1.5);

        // Draw ground
        material_metallic(0.0);
        material_roughness(0.8);
        set_color(0x445566FF);
        push_translate(0.0, -0.1, 0.0);
        draw_mesh(MESH_GROUND);

        // Draw player
        set_color(0xFF6644FF);
        push_translate(PLAYER_X, PLAYER_Y + 1.0, PLAYER_Z);
        draw_mesh(MESH_PLAYER);

        push_identity();
    }
}

fn lerp(a: f32, b: f32, t: f32) -> f32 {
    a + (b - a) * t
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! { loop {} }
```

## Orbit Camera (Third-Person Action)

```rust
#![no_std]
#![no_main]

mod ffi;
use ffi::*;

// Player state
static mut PLAYER_X: f32 = 0.0;
static mut PLAYER_Y: f32 = 0.0;
static mut PLAYER_Z: f32 = 0.0;
static mut PLAYER_YAW: f32 = 0.0;

// Orbit camera state
static mut CAM_YAW: f32 = 0.0;
static mut CAM_PITCH: f32 = 25.0;
static mut CAM_DIST: f32 = 10.0;
static mut CAM_DIST_TARGET: f32 = 10.0;

// Camera config
const SENSITIVITY: f32 = 120.0;
const PITCH_MIN: f32 = -20.0;
const PITCH_MAX: f32 = 70.0;
const DIST_MIN: f32 = 3.0;
const DIST_MAX: f32 = 20.0;
const ZOOM_SPEED: f32 = 10.0;

static mut MESH_PLAYER: u32 = 0;
static mut MESH_GROUND: u32 = 0;

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        set_clear_color(0x1a2a3aFF);
        render_mode(2);

        MESH_PLAYER = capsule(0.5, 1.0, 16, 4);
        MESH_GROUND = plane(40.0, 40.0, 8, 8);
    }
}

#[no_mangle]
pub extern "C" fn update() {
    let dt = unsafe { delta_time() };

    unsafe {
        // Camera rotation via right stick
        let rx = right_stick_x(0);
        let ry = right_stick_y(0);

        CAM_YAW += rx * SENSITIVITY * dt;
        CAM_PITCH -= ry * SENSITIVITY * dt;
        CAM_PITCH = clamp(CAM_PITCH, PITCH_MIN, PITCH_MAX);

        // Zoom via triggers
        let zoom_in = trigger_right(0);
        let zoom_out = trigger_left(0);
        CAM_DIST_TARGET -= (zoom_in - zoom_out) * ZOOM_SPEED * dt;
        CAM_DIST_TARGET = clamp(CAM_DIST_TARGET, DIST_MIN, DIST_MAX);
        CAM_DIST = lerp(CAM_DIST, CAM_DIST_TARGET, 5.0 * dt);

        // Player movement relative to camera
        let move_x = left_stick_x(0);
        let move_z = -left_stick_y(0);

        if move_x.abs() > 0.1 || move_z.abs() > 0.1 {
            // Move relative to camera yaw
            // Forward is -Z when yaw=0, so negate sin/cos
            let yaw_rad = CAM_YAW.to_radians();
            let forward_x = -yaw_rad.sin();
            let forward_z = -yaw_rad.cos();
            let right_x = yaw_rad.cos();
            let right_z = -yaw_rad.sin();

            let dx = move_x * right_x + move_z * forward_x;
            let dz = move_x * right_z + move_z * forward_z;

            const SPEED: f32 = 8.0;
            PLAYER_X += dx * SPEED * dt;
            PLAYER_Z += dz * SPEED * dt;

            // Face movement direction
            PLAYER_YAW = dx.atan2(dz).to_degrees();
        }
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        draw_env();

        // Calculate orbit camera position
        // Camera behind player: use -sin for X to orbit correctly
        // When yaw=0: camera at +Z (behind player facing -Z)
        let yaw_rad = CAM_YAW.to_radians();
        let pitch_rad = CAM_PITCH.to_radians();

        let cam_x = PLAYER_X - CAM_DIST * yaw_rad.sin() * pitch_rad.cos();
        let cam_y = PLAYER_Y + 1.5 + CAM_DIST * pitch_rad.sin();
        let cam_z = PLAYER_Z + CAM_DIST * yaw_rad.cos() * pitch_rad.cos();

        camera_set(cam_x, cam_y, cam_z, PLAYER_X, PLAYER_Y + 1.5, PLAYER_Z);

        // Lighting
        light_set(0, 0.3, -0.8, 0.5);
        light_intensity(0, 1.2);

        // Ground
        material_roughness(0.9);
        set_color(0x334455FF);
        push_translate(0.0, 0.0, 0.0);
        draw_mesh(MESH_GROUND);

        // Player
        material_roughness(0.4);
        set_color(0x44AA88FF);
        push_translate(PLAYER_X, PLAYER_Y, PLAYER_Z);
        push_rotate_y(PLAYER_YAW);
        draw_mesh(MESH_PLAYER);

        push_identity();
    }
}

fn lerp(a: f32, b: f32, t: f32) -> f32 { a + (b - a) * t }
fn clamp(v: f32, min: f32, max: f32) -> f32 {
    if v < min { min } else if v > max { max } else { v }
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! { loop {} }
```

## First-Person Camera

```rust
#![no_std]
#![no_main]

mod ffi;
use ffi::*;

// Player position
static mut PLAYER_X: f32 = 0.0;
static mut PLAYER_Y: f32 = 0.0;
static mut PLAYER_Z: f32 = 0.0;

// Look direction
static mut LOOK_YAW: f32 = 0.0;
static mut LOOK_PITCH: f32 = 0.0;

// Config
const EYE_HEIGHT: f32 = 1.7;
const MOVE_SPEED: f32 = 6.0;
const LOOK_SENSITIVITY: f32 = 90.0;
const PITCH_LIMIT: f32 = 85.0;

static mut MESH_PILLAR: u32 = 0;
static mut MESH_GROUND: u32 = 0;

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        set_clear_color(0x202030FF);
        render_mode(2);
        camera_fov(75.0); // Wider FOV for first-person

        MESH_PILLAR = cylinder(0.3, 0.3, 3.0, 12);
        MESH_GROUND = plane(30.0, 30.0, 1, 1);
    }
}

#[no_mangle]
pub extern "C" fn update() {
    let dt = unsafe { delta_time() };

    unsafe {
        // Mouse look via right stick
        let rx = right_stick_x(0);
        let ry = right_stick_y(0);

        LOOK_YAW += rx * LOOK_SENSITIVITY * dt;
        LOOK_PITCH -= ry * LOOK_SENSITIVITY * dt;
        LOOK_PITCH = clamp(LOOK_PITCH, -PITCH_LIMIT, PITCH_LIMIT);

        // WASD-style movement relative to look direction
        let move_x = left_stick_x(0);
        let move_z = -left_stick_y(0);

        if move_x.abs() > 0.1 || move_z.abs() > 0.1 {
            let yaw_rad = LOOK_YAW.to_radians();

            // Forward is -Z when yaw=0, so negate sin/cos
            let fwd_x = -yaw_rad.sin();
            let fwd_z = -yaw_rad.cos();

            // Strafe (right is +X when yaw=0)
            let right_x = yaw_rad.cos();
            let right_z = -yaw_rad.sin();

            let dx = move_x * right_x + move_z * fwd_x;
            let dz = move_x * right_z + move_z * fwd_z;

            PLAYER_X += dx * MOVE_SPEED * dt;
            PLAYER_Z += dz * MOVE_SPEED * dt;
        }
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        draw_env();

        // Calculate look direction
        // Forward is -Z when yaw=0, so negate sin/cos
        let yaw_rad = LOOK_YAW.to_radians();
        let pitch_rad = LOOK_PITCH.to_radians();

        let look_x = -yaw_rad.sin() * pitch_rad.cos();
        let look_y = pitch_rad.sin();
        let look_z = -yaw_rad.cos() * pitch_rad.cos();

        // Set camera at eye position looking in that direction
        let eye_y = PLAYER_Y + EYE_HEIGHT;
        camera_set(
            PLAYER_X, eye_y, PLAYER_Z,
            PLAYER_X + look_x, eye_y + look_y, PLAYER_Z + look_z
        );

        // Lighting
        light_set(0, 0.3, -0.7, 0.5);

        // Ground
        set_color(0x444455FF);
        material_roughness(0.9);
        draw_mesh(MESH_GROUND);

        // Pillars for reference
        set_color(0x666688FF);
        material_roughness(0.5);
        for i in 0..4 {
            let angle = (i as f32) * 1.57;
            let px = angle.cos() * 8.0;
            let pz = angle.sin() * 8.0;
            push_translate(px, 1.5, pz);
            draw_mesh(MESH_PILLAR);
        }

        push_identity();
    }
}

fn clamp(v: f32, min: f32, max: f32) -> f32 {
    if v < min { min } else if v > max { max } else { v }
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! { loop {} }
```

## Screen Shake System

Add to any camera:

```rust
// Shake state
static mut SHAKE_TRAUMA: f32 = 0.0;
static mut SHAKE_OFFSET_X: f32 = 0.0;
static mut SHAKE_OFFSET_Y: f32 = 0.0;

const MAX_SHAKE: f32 = 0.5;  // World units
const TRAUMA_DECAY: f32 = 2.0;

/// Add trauma (0.0 to 1.0) from impacts, explosions, etc.
fn add_shake(amount: f32) {
    unsafe {
        SHAKE_TRAUMA = (SHAKE_TRAUMA + amount).min(1.0);
    }
}

/// Call in update() to decay trauma and compute offset
fn update_shake() {
    let dt = unsafe { delta_time() };

    unsafe {
        // Decay trauma over time
        SHAKE_TRAUMA = (SHAKE_TRAUMA - TRAUMA_DECAY * dt).max(0.0);

        // Square trauma for nice falloff feel
        let shake = SHAKE_TRAUMA * SHAKE_TRAUMA;

        // Use rollback-safe random for offset
        SHAKE_OFFSET_X = (random_f32() - 0.5) * 2.0 * MAX_SHAKE * shake;
        SHAKE_OFFSET_Y = (random_f32() - 0.5) * 2.0 * MAX_SHAKE * shake;
    }
}

/// Apply shake offset to camera position
fn apply_shake_to_camera(
    mut cam_x: f32,
    mut cam_y: f32,
    cam_z: f32
) -> (f32, f32, f32) {
    unsafe {
        cam_x += SHAKE_OFFSET_X;
        cam_y += SHAKE_OFFSET_Y;
    }
    (cam_x, cam_y, cam_z)
}
```

Usage in render:
```rust
let (cam_x, cam_y, cam_z) = get_orbit_position(...);
let (cam_x, cam_y, cam_z) = apply_shake_to_camera(cam_x, cam_y, cam_z);
camera_set(cam_x, cam_y, cam_z, target_x, target_y, target_z);
```

## Fixed Camera (Room-Based)

```rust
// Room camera positions (predefined)
struct CameraPreset {
    pos: (f32, f32, f32),
    target: (f32, f32, f32),
    fov: f32,
}

static ROOM_CAMERAS: [CameraPreset; 3] = [
    CameraPreset {
        pos: (0.0, 5.0, 12.0),
        target: (0.0, 0.0, 0.0),
        fov: 60.0,
    },
    CameraPreset {
        pos: (10.0, 8.0, 0.0),
        target: (0.0, 0.0, 0.0),
        fov: 50.0,
    },
    CameraPreset {
        pos: (0.0, 15.0, 0.1),
        target: (0.0, 0.0, 0.0),
        fov: 45.0,
    },
];

static mut CURRENT_ROOM: usize = 0;
static mut CAM_TRANSITION: f32 = 0.0;

fn switch_room(room: usize) {
    unsafe {
        if room < ROOM_CAMERAS.len() {
            CURRENT_ROOM = room;
            CAM_TRANSITION = 0.0;
        }
    }
}

// Smooth transition between fixed cameras
fn get_fixed_camera() -> ((f32, f32, f32), (f32, f32, f32), f32) {
    unsafe {
        let cam = &ROOM_CAMERAS[CURRENT_ROOM];

        // Smooth transition
        CAM_TRANSITION = (CAM_TRANSITION + delta_time() * 2.0).min(1.0);

        (cam.pos, cam.target, cam.fov)
    }
}
```

## Smooth FOV Transitions (Zoom/Aim)

```rust
static mut CURRENT_FOV: f32 = 60.0;
static mut TARGET_FOV: f32 = 60.0;

const FOV_NORMAL: f32 = 60.0;
const FOV_ZOOM: f32 = 35.0;
const FOV_SPEED: f32 = 8.0;

fn update_fov() {
    let dt = unsafe { delta_time() };

    unsafe {
        // Check aim button (e.g., L2/left trigger)
        let aiming = trigger_left(0) > 0.5;
        TARGET_FOV = if aiming { FOV_ZOOM } else { FOV_NORMAL };

        // Smooth transition
        CURRENT_FOV = lerp(CURRENT_FOV, TARGET_FOV, FOV_SPEED * dt);
    }
}

// In render():
fn apply_fov() {
    unsafe {
        camera_fov(CURRENT_FOV);
    }
}
```
