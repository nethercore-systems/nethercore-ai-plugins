---
name: Camera Systems
description: This skill should be used when the user asks about "camera follow", "orbit camera", "third person camera", "first person camera", "camera collision", "screen shake", "camera lerp", "camera implementation", "smooth camera", "camera dead zone", "look-ahead camera", "fixed camera", "rail camera", "camera zoom", "camera FOV", or mentions implementing camera systems, camera movement, camera effects, or 3D camera control for Nethercore ZX games.
version: 1.0.0
---

# Camera Systems for Nethercore ZX

Implement camera systems using the ZX FFI camera functions. All camera state should be stored in static variables for rollback safety.

## Camera FFI Functions

Reference `nethercore/include/zx.rs` lines 173-201 for complete signatures:

| Function | Purpose |
|----------|---------|
| `camera_set(x, y, z, tx, ty, tz)` | Position camera, look at target |
| `camera_fov(degrees)` | Set field of view (default 60) |
| `push_view_matrix(m0..m15)` | Custom 4x4 view matrix |
| `push_projection_matrix(m0..m15)` | Custom projection matrix |

## Camera Type Selection

| Camera Type | Best For | Complexity |
|-------------|----------|------------|
| Follow | Platformers, racing | Simple |
| Orbit | Action-adventure, RPGs | Medium |
| First-Person | FPS, exploration | Medium |
| Fixed | Puzzle, cinematic | Simple |
| Rail | Cutscenes, on-rails shooters | Medium |

## Follow Camera

Tracks a target with smooth interpolation and optional offset:

```rust
static mut CAM_X: f32 = 0.0;
static mut CAM_Y: f32 = 5.0;
static mut CAM_Z: f32 = 10.0;

fn update_follow_camera(target_x: f32, target_y: f32, target_z: f32) {
    const OFFSET_Y: f32 = 5.0;   // Height above target
    const OFFSET_Z: f32 = 10.0;  // Distance behind target
    const SMOOTH: f32 = 5.0;     // Smoothing factor

    let dt = unsafe { delta_time() };
    let t = (SMOOTH * dt).min(1.0);

    unsafe {
        // Lerp camera position toward target + offset
        CAM_X = lerp(CAM_X, target_x, t);
        CAM_Y = lerp(CAM_Y, target_y + OFFSET_Y, t);
        CAM_Z = lerp(CAM_Z, target_z + OFFSET_Z, t);
    }
}

fn lerp(a: f32, b: f32, t: f32) -> f32 {
    a + (b - a) * t
}
```

In `render()`:
```rust
camera_set(CAM_X, CAM_Y, CAM_Z, target_x, target_y, target_z);
```

### Dead Zone

Prevent camera jitter by only moving when target exceeds threshold:

```rust
fn update_with_dead_zone(target_x: f32, target_z: f32) {
    const DEAD_ZONE: f32 = 2.0;

    unsafe {
        let dx = target_x - CAM_X;
        let dz = target_z - (CAM_Z - OFFSET_Z);
        let dist = (dx*dx + dz*dz).sqrt();

        if dist > DEAD_ZONE {
            let excess = dist - DEAD_ZONE;
            let t = (excess / dist) * 0.1;
            CAM_X = lerp(CAM_X, target_x, t);
            CAM_Z = lerp(CAM_Z, target_z + OFFSET_Z, t);
        }
    }
}
```

## Orbit Camera

Third-person camera controlled by right stick:

```rust
static mut CAM_YAW: f32 = 0.0;    // Horizontal rotation
static mut CAM_PITCH: f32 = 20.0; // Vertical rotation (degrees)
static mut CAM_DIST: f32 = 8.0;   // Distance from target

fn update_orbit_camera(player: u32) {
    const SENSITIVITY: f32 = 120.0;
    const PITCH_MIN: f32 = -30.0;
    const PITCH_MAX: f32 = 60.0;

    let dt = unsafe { delta_time() };
    let rx = unsafe { right_stick_x(player) };
    let ry = unsafe { right_stick_y(player) };

    unsafe {
        CAM_YAW += rx * SENSITIVITY * dt;
        CAM_PITCH -= ry * SENSITIVITY * dt;
        CAM_PITCH = CAM_PITCH.clamp(PITCH_MIN, PITCH_MAX);
    }
}

fn get_orbit_position(target_x: f32, target_y: f32, target_z: f32) -> (f32, f32, f32) {
    unsafe {
        let yaw_rad = CAM_YAW.to_radians();
        let pitch_rad = CAM_PITCH.to_radians();

        let x = target_x + CAM_DIST * yaw_rad.sin() * pitch_rad.cos();
        let y = target_y + CAM_DIST * pitch_rad.sin();
        let z = target_z + CAM_DIST * yaw_rad.cos() * pitch_rad.cos();

        (x, y, z)
    }
}
```

In `render()`:
```rust
let (cx, cy, cz) = get_orbit_position(player_x, player_y, player_z);
camera_set(cx, cy, cz, player_x, player_y + 1.0, player_z);
```

## First-Person Camera

Camera at player position, looking in player direction:

```rust
static mut LOOK_YAW: f32 = 0.0;
static mut LOOK_PITCH: f32 = 0.0;

fn update_first_person(player: u32) {
    const SENSITIVITY: f32 = 90.0;
    const PITCH_LIMIT: f32 = 85.0;

    let dt = unsafe { delta_time() };
    let rx = unsafe { right_stick_x(player) };
    let ry = unsafe { right_stick_y(player) };

    unsafe {
        LOOK_YAW += rx * SENSITIVITY * dt;
        LOOK_PITCH -= ry * SENSITIVITY * dt;
        LOOK_PITCH = LOOK_PITCH.clamp(-PITCH_LIMIT, PITCH_LIMIT);
    }
}

fn get_look_direction() -> (f32, f32, f32) {
    unsafe {
        let yaw = LOOK_YAW.to_radians();
        let pitch = LOOK_PITCH.to_radians();

        let x = yaw.sin() * pitch.cos();
        let y = pitch.sin();
        let z = yaw.cos() * pitch.cos();

        (x, y, z)
    }
}
```

In `render()`:
```rust
let (dx, dy, dz) = get_look_direction();
camera_set(
    player_x, player_y + EYE_HEIGHT, player_z,
    player_x + dx, player_y + EYE_HEIGHT + dy, player_z + dz
);
```

## Camera Collision

Prevent camera clipping through walls by pulling it forward:

```rust
fn apply_camera_collision(
    target: (f32, f32, f32),
    cam_pos: (f32, f32, f32),
) -> (f32, f32, f32) {
    // Raycast from target to camera position
    // If hit, position camera at hit point + small offset toward target

    let dir = (
        cam_pos.0 - target.0,
        cam_pos.1 - target.1,
        cam_pos.2 - target.2,
    );
    let dist = (dir.0*dir.0 + dir.1*dir.1 + dir.2*dir.2).sqrt();

    // Your collision detection here - check against scene geometry
    // Return adjusted position if collision found

    cam_pos // No collision
}
```

**Note:** ZX doesn't have built-in raycast. Use simple sphere checks against level geometry or implement spatial partitioning. See `references/camera-math.md` for collision approaches.

## Screen Shake

Add trauma-based shake effect:

```rust
static mut SHAKE_TRAUMA: f32 = 0.0;

fn add_shake(amount: f32) {
    unsafe {
        SHAKE_TRAUMA = (SHAKE_TRAUMA + amount).min(1.0);
    }
}

fn update_shake() {
    let dt = unsafe { delta_time() };
    unsafe {
        SHAKE_TRAUMA = (SHAKE_TRAUMA - dt * 2.0).max(0.0);
    }
}

fn get_shake_offset() -> (f32, f32) {
    unsafe {
        let shake = SHAKE_TRAUMA * SHAKE_TRAUMA; // Square for feel
        let max_offset = 10.0 * shake;

        // Use random() for rollback-safe randomness
        let rx = (random_f32() - 0.5) * 2.0 * max_offset;
        let ry = (random_f32() - 0.5) * 2.0 * max_offset;

        (rx, ry)
    }
}
```

Apply in 2D drawing or as camera position offset for 3D.

## Zoom Transitions

Smooth FOV changes:

```rust
static mut CURRENT_FOV: f32 = 60.0;
static mut TARGET_FOV: f32 = 60.0;

fn set_zoom(fov: f32) {
    unsafe { TARGET_FOV = fov; }
}

fn update_zoom() {
    let dt = unsafe { delta_time() };
    unsafe {
        CURRENT_FOV = lerp(CURRENT_FOV, TARGET_FOV, 5.0 * dt);
    }
}
```

In `render()`:
```rust
camera_fov(CURRENT_FOV);
```

## Custom View Matrix

For advanced control, construct view matrix manually:

```rust
fn look_at_matrix(
    eye: (f32, f32, f32),
    target: (f32, f32, f32),
    up: (f32, f32, f32)
) -> [f32; 16] {
    // See references/camera-math.md for full implementation
    // Returns column-major 4x4 matrix
}
```

Use with `push_view_matrix()` for effects like camera roll.

## Rollback Safety

All camera state must be in static variables (auto-snapshotted):
- Use `delta_time()` for frame-rate independence
- Use `random()` functions for shake, not external RNG
- Camera state persists through rollback/replay

## Additional Resources

- **`examples/camera-examples.md`** - Complete working implementations
- **`references/camera-math.md`** - Matrix math, lerp/slerp, collision detection
- **`nethercore/include/zx.rs`** - Camera FFI signatures (lines 173-201)
- **Gap 9 (Split-Screen)** - Per-viewport camera setup
- **Gap 5 (Game Feel)** - Screen shake integration with juice effects
