# Nethercore ZX Coordinate Conventions

**This document is the authoritative reference for coordinate systems in Nethercore ZX.** All skills, examples, and generated code MUST follow these conventions.

## 3D World Space

Nethercore ZX uses a **Y-up, right-handed coordinate system** consistent with OpenGL, glTF, and Blender:

```
        +Y (up)
         │
         │
         │
         └────────── +X (right)
        /
       /
      /
    +Z (towards viewer / out of screen)
```

### Axis Definitions

| Axis | Direction | Common Usage |
|------|-----------|--------------|
| **+X** | Right | Strafe right, camera pan right |
| **-X** | Left | Strafe left, camera pan left |
| **+Y** | Up | Jump, camera tilt up |
| **-Y** | Down | Fall, camera tilt down |
| **+Z** | Towards viewer | Camera is here, "backwards" |
| **-Z** | Into screen | **Forward direction**, where characters face |

### Key Convention: -Z is Forward

When a character or camera has yaw = 0 (facing forward):
- They look towards **-Z**
- Their right side points to **+X**
- Up is **+Y**

This matches:
- OpenGL/WebGL default
- glTF specification
- Blender's front view (Numpad 1)
- Most 3D game engines

## Angle Conventions

### Yaw (Horizontal Rotation)

Yaw rotates around the Y axis:

| Yaw | Direction Faced | Camera Position (orbit) |
|-----|-----------------|-------------------------|
| 0° | -Z (into screen) | +Z (behind character) |
| 90° | -X (left) | +X (right of character) |
| 180° | +Z (out of screen) | -Z (in front of character) |
| 270° | +X (right) | -X (left of character) |

**Sign convention:** Positive yaw rotates counter-clockwise when viewed from above (right-hand rule around +Y).

### Pitch (Vertical Tilt)

Pitch rotates around the X axis:

| Pitch | Direction |
|-------|-----------|
| 0° | Horizontal (looking at horizon) |
| +45° | Looking up 45° |
| -45° | Looking down 45° |
| +90° | Looking straight up |
| -90° | Looking straight down |

**Sign convention:** Positive pitch tilts up (right-hand rule around +X, but we flip for intuitive controls).

## Camera Formulas

### Orbit Camera (Third-Person)

Position camera at distance `d` behind a target at origin:

```rust
// Camera orbits around target
// When yaw=0, pitch=0: camera is at (0, 0, d), looking at origin along -Z
let yaw_rad = yaw_degrees.to_radians();
let pitch_rad = pitch_degrees.to_radians();

let cam_x = target_x - d * yaw_rad.sin() * pitch_rad.cos();
let cam_y = target_y + d * pitch_rad.sin();
let cam_z = target_z + d * yaw_rad.cos() * pitch_rad.cos();

camera_set(cam_x, cam_y, cam_z, target_x, target_y, target_z);
```

### First-Person Camera

Calculate look direction from yaw/pitch:

```rust
// When yaw=0: looking towards -Z
// When yaw=90°: looking towards -X
let yaw_rad = yaw_degrees.to_radians();
let pitch_rad = pitch_degrees.to_radians();

let look_x = -yaw_rad.sin() * pitch_rad.cos();
let look_y = pitch_rad.sin();
let look_z = -yaw_rad.cos() * pitch_rad.cos();

camera_set(
    player_x, player_y + eye_height, player_z,
    player_x + look_x, player_y + eye_height + look_y, player_z + look_z
);
```

### Movement Relative to Camera

Move a character based on camera yaw:

```rust
let yaw_rad = camera_yaw.to_radians();

// Forward direction (towards -Z when yaw=0)
let forward_x = -yaw_rad.sin();
let forward_z = -yaw_rad.cos();

// Right direction (towards +X when yaw=0)
let right_x = yaw_rad.cos();
let right_z = -yaw_rad.sin();

// Apply stick input
let move_x = stick_x * right_x + stick_y * forward_x;
let move_z = stick_x * right_z + stick_y * forward_z;
```

## 2D Screen Space

For 2D drawing (sprites, UI, text), screen coordinates use:

```
(0,0) ─────────────────── +X (right)
  │
  │
  │
  │
 +Y (down)
```

| Coordinate | Range | Notes |
|------------|-------|-------|
| X | 0-960 | Left to right |
| Y | 0-540 | Top to bottom |

**Note:** This is standard screen coordinates where Y increases downward, different from world Y which increases upward.

## 2D World Space (Top-Down Games)

For 2D top-down games rendered in 3D (using the XZ plane with fixed Y camera):

```
    -Z (up on screen / forward in world)
     │
     │
     └────── +X (right)
```

| Angle | Direction on Screen | Equivalent in 3D |
|-------|---------------------|------------------|
| 0° | Up | -Z direction |
| 90° | Right | +X direction |
| 180° | Down | +Z direction |
| 270° | Left | -X direction |

For pure 2D games (Mode 0 with sprites), use the XY plane:

| Angle | Direction |
|-------|-----------|
| 0° | Right (+X) |
| 90° | Up (+Y in world, but -Y on screen!) |

**Warning:** Be careful with angle conventions when mixing 2D and 3D. Document which convention you're using.

## Skeletal Animation

Bone local axes follow the same convention:
- **+Y** is the bone's length axis (towards the child bone)
- **-Z** is the bone's forward direction
- **+X** is the bone's right direction

When building a humanoid facing -Z:
- Arms extend along ±X
- Legs extend along -Y (down)
- Spine extends along +Y (up)

## Asset Export

When exporting from 3D software:

### Blender
- Export with **+Y Up, -Z Forward** (matches ZX directly)
- glTF 2.0 export defaults are correct

### Maya
- Use Y-up, -Z forward export settings
- May need to rotate models 180° if exported facing +Z

### 3ds Max
- Convert from Z-up to Y-up on export
- Verify forward direction after import

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Using +Z as forward | Characters face backwards | Negate Z in forward calculations |
| Wrong orbit camera formula | Camera in front of character | Use `+d * cos` for Z, not `-d * cos` |
| Mixing 2D screen Y with 3D Y | UI upside down or movement inverted | Keep them separate; screen Y is down |
| Yaw rotation direction wrong | Left stick turns right | Check sign on yaw delta |
| Pitch calculation with wrong sign | Looking down when pushing up | Negate pitch from stick input |

## Quick Reference

```rust
// Forward direction from yaw (3D)
let forward = Vec3::new(-yaw.sin(), 0.0, -yaw.cos());

// Right direction from yaw (3D)
let right = Vec3::new(yaw.cos(), 0.0, -yaw.sin());

// Up is always (0, 1, 0) in world space

// Orbit camera position at distance d
let cam = target + Vec3::new(
    -d * yaw.sin() * pitch.cos(),
    d * pitch.sin(),
    d * yaw.cos() * pitch.cos(),
);

// Look direction from yaw/pitch
let look = Vec3::new(
    -yaw.sin() * pitch.cos(),
    pitch.sin(),
    -yaw.cos() * pitch.cos(),
);
```
