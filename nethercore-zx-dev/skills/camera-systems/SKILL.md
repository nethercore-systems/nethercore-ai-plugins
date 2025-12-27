---
name: Camera Systems
description: This skill should be used when the user asks about "camera follow", "orbit camera", "third person camera", "first person camera", "camera collision", "screen shake", "camera lerp", "camera implementation", "smooth camera", "camera dead zone", "look-ahead camera", "fixed camera", "rail camera", "camera zoom", "camera FOV", "side-scroller design", "top-down game", "perspective choice", "camera style", "2D game design", "3D game design", or mentions implementing camera systems, camera movement, camera effects, perspective design, or 3D camera control for Nethercore ZX games.
version: 2.0.0
---

# Camera Systems for Nethercore ZX

Implement camera systems using the ZX FFI camera functions. All camera state should be stored in static variables for rollback safety. Includes perspective-based design patterns for optimal camera choices.

## Camera FFI Functions

Reference `nethercore/include/zx.rs` lines 173-201 for complete signatures:

| Function | Purpose |
|----------|---------|
| `camera_set(x, y, z, tx, ty, tz)` | Position camera, look at target |
| `camera_fov(degrees)` | Set field of view (default 60) |
| `push_view_matrix(m0..m15)` | Custom 4x4 view matrix |
| `push_projection_matrix(m0..m15)` | Custom projection matrix |

---

## Part 1: Camera Type Selection

| Camera Type | Best For | Complexity | Perspective |
|-------------|----------|------------|-------------|
| Follow | Platformers, racing | Simple | Side-scroll, 3rd person |
| Orbit | Action-adventure, RPGs | Medium | Third-person |
| First-Person | FPS, exploration | Medium | First-person |
| Fixed | Puzzle, cinematic | Simple | Any |
| Rail | Cutscenes, on-rails shooters | Medium | Any |
| 2D Side-Scroll | Platformer, fighter | Simple | 2D/2.5D |
| Top-Down | Racing, strategy | Simple | 2D/2.5D |

---

## Part 2: 3D Camera Implementations

### Follow Camera

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

### Orbit Camera

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

### First-Person Camera

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

---

## Part 3: Camera Effects

### Screen Shake

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
        let shake = SHAKE_TRAUMA * SHAKE_TRAUMA;
        let max_offset = 10.0 * shake;

        let rx = (random_f32() - 0.5) * 2.0 * max_offset;
        let ry = (random_f32() - 0.5) * 2.0 * max_offset;

        (rx, ry)
    }
}
```

### Zoom Transitions

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

---

## Part 4: Perspective-Based Design

### Perspective Overview

| Perspective | Dimensions | Render Modes | Common Genres |
|-------------|------------|--------------|---------------|
| Side-Scroller | 2D/2.5D | 0, 1, 3 | Platformer, Fighter, Puzzle |
| Top-Down | 2D/2.5D | 0, 1, 2 | Racing, Shooter, Strategy |
| Third-Person | Full 3D | 1, 2, 3 | Action, Adventure, Platformer |
| First-Person | Full 3D | 2, 3 | Shooter, Exploration |

### Side-Scroller Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| Render Mode | 0 (Lambert) or 3 (Blinn-Phong) | 0 for sprites, 3 for 2.5D |
| Tick Rate | 60 fps | Smooth platforming |
| Camera | Fixed on one axis | Usually horizontal scroll |

**Camera Behavior:**
- Follow player with slight lead
- Lock during boss encounters
- Vertical scroll for climbing sections

### Top-Down Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| Render Mode | 0 or 2 | 0 for sprites, 2 for 3D top-down |
| Tick Rate | 60 fps | Standard for action |
| Camera | Overhead, possibly dynamic zoom |

**View Distance:**
- Fixed zoom (consistent scale)
- Dynamic zoom (show more during speed)
- Minimap for navigation

### Third-Person Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| Render Mode | 2 or 3 | 2 for modern, 3 for retro |
| Tick Rate | 60 fps | Smooth 3D movement |
| Camera | Follow/orbit behind player |

**Camera Systems:**
- Follow cam (offset behind player)
- Orbit cam (player rotates, camera follows)
- Context-sensitive (tightens in combat)
- Collision avoidance (push through walls)

### First-Person Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| Render Mode | 2 or 3 | Lighting important for atmosphere |
| Tick Rate | 60 or 120 fps | Smooth look essential |
| Camera | Player head position |

**View Considerations:**
- Limited peripheral vision
- Audio cues for off-screen threats
- Minimap or compass for navigation
- Look sensitivity is critical — allow configuration

### Perspective Selection Guide

```
What's the core experience?

├── Character-focused action/story
│   ├── Need to see character? → Third-Person
│   └── Immersive world? → First-Person
│
├── Precision platforming
│   └── → Side-Scroller
│
├── Vehicle/overhead action
│   └── → Top-Down
│
└── Tactical/strategic view
    └── → Top-Down
```

### Perspective Tradeoffs

| Aspect | Side-Scroll | Top-Down | Third-Person | First-Person |
|--------|-------------|----------|--------------|--------------|
| Asset complexity | Low | Low-Med | High | Medium |
| Camera complexity | Low | Low | High | Low |
| Control complexity | Low | Medium | High | Medium |
| Immersion | Low | Low | Medium | High |
| Spatial awareness | High | High | Medium | Low |
| Motion sickness risk | None | None | Low | Medium |

---

## Part 5: Camera Collision

Prevent camera clipping through walls by pulling it forward:

```rust
fn apply_camera_collision(
    target: (f32, f32, f32),
    cam_pos: (f32, f32, f32),
) -> (f32, f32, f32) {
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

---

## Part 6: Custom View Matrix

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

---

## Rollback Safety

All camera state must be in static variables (auto-snapshotted):
- Use `delta_time()` for frame-rate independence
- Use `random()` functions for shake, not external RNG
- Camera state persists through rollback/replay

---

## Additional Resources

- **`examples/camera-examples.md`** - Complete working implementations
- **`references/camera-math.md`** - Matrix math, lerp/slerp, collision detection
- **`references/side-scroller-patterns.md`** - 2D camera, parallax, level design
- **`nethercore/include/zx.rs`** - Camera FFI signatures (lines 173-201)
- **`multiplayer-patterns`** skill - Per-viewport camera setup for split-screen
- **`game-feel`** skill - Screen shake integration with juice effects
