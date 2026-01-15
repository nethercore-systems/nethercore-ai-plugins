# ZX Camera Systems

## Camera Types

| Type | Best For | Complexity |
|------|----------|------------|
| Follow | Platformers, racing | Simple |
| Orbit | Action-adventure, RPGs | Medium |
| First-Person | FPS, exploration | Medium |
| Fixed | Puzzle, cinematic | Simple |

## Orbit Camera

```rust
static mut CAM_YAW: f32 = 0.0;
static mut CAM_PITCH: f32 = 20.0;
static mut CAM_DIST: f32 = 8.0;

fn update_orbit(player: u32) {
    let dt = delta_time();
    unsafe {
        CAM_YAW += right_stick_x(player) * 120.0 * dt;
        CAM_PITCH = (CAM_PITCH - right_stick_y(player) * 120.0 * dt)
            .clamp(-30.0, 60.0);
    }
}

fn get_orbit_pos(tx: f32, ty: f32, tz: f32) -> (f32, f32, f32) {
    unsafe {
        let yaw = CAM_YAW.to_radians();
        let pitch = CAM_PITCH.to_radians();
        (
            tx - CAM_DIST * yaw.sin() * pitch.cos(),
            ty + CAM_DIST * pitch.sin(),
            tz + CAM_DIST * yaw.cos() * pitch.cos(),
        )
    }
}
```

## First-Person Camera

```rust
static mut LOOK_YAW: f32 = 0.0;
static mut LOOK_PITCH: f32 = 0.0;

fn update_first_person(player: u32) {
    let dt = delta_time();
    unsafe {
        LOOK_YAW += right_stick_x(player) * 90.0 * dt;
        LOOK_PITCH = (LOOK_PITCH - right_stick_y(player) * 90.0 * dt)
            .clamp(-85.0, 85.0);
    }
}

fn get_look_dir() -> (f32, f32, f32) {
    unsafe {
        let yaw = LOOK_YAW.to_radians();
        let pitch = LOOK_PITCH.to_radians();
        (-yaw.sin() * pitch.cos(), pitch.sin(), -yaw.cos() * pitch.cos())
    }
}
```

## Screen Shake

```rust
static mut SHAKE_TRAUMA: f32 = 0.0;

fn add_shake(amount: f32) {
    unsafe { SHAKE_TRAUMA = (SHAKE_TRAUMA + amount).min(1.0); }
}

fn update_shake() {
    unsafe { SHAKE_TRAUMA = (SHAKE_TRAUMA - delta_time() * 2.0).max(0.0); }
}

fn get_shake_offset() -> (f32, f32) {
    unsafe {
        let shake = SHAKE_TRAUMA * SHAKE_TRAUMA * 10.0;
        ((random_f32() - 0.5) * shake, (random_f32() - 0.5) * shake)
    }
}
```

## Dead Zone

Prevents jitter when target is near camera center:

```rust
fn update_with_dead_zone(tx: f32, tz: f32) {
    let dx = tx - CAM_X;
    let dz = tz - (CAM_Z - OFFSET_Z);
    let dist = (dx*dx + dz*dz).sqrt();
    if dist > 2.0 {  // DEAD_ZONE
        let t = ((dist - 2.0) / dist) * 0.1;
        CAM_X += dx * t;
        CAM_Z += dz * t;
    }
}
```
