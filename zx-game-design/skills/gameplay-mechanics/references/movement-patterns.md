# Movement Patterns Reference

Rollback-safe movement implementations for various game styles on Nethercore ZX.

## Coordinate Systems

**This file uses 2D coordinates for top-down games:**
- X: horizontal (positive = right)
- Y: vertical (positive = down in screen space)
- Angles: 0° = right (+X), 90° = down (+Y in screen), counter-clockwise positive

**For 3D coordinate conventions (Y-up, -Z forward), see:**
`zx-game-development/references/coordinate-conventions.md`

---

## 8-Directional Movement (Complete)

Standard top-down movement with proper diagonal normalization.

```rust
use crate::ffi::*;

const MOVE_SPEED: f32 = 4.0;

struct Player {
    x: f32,
    y: f32,
    facing_angle: f32,  // In radians for smooth rotation
}

fn update_8dir_movement(player: &mut Player) {
    let mut dx: f32 = 0.0;
    let mut dy: f32 = 0.0;

    // D-pad input
    if button_held(0, button::LEFT)  { dx -= 1.0; }
    if button_held(0, button::RIGHT) { dx += 1.0; }
    if button_held(0, button::UP)    { dy -= 1.0; }
    if button_held(0, button::DOWN)  { dy += 1.0; }

    // Normalize diagonal movement (prevent faster diagonal speed)
    let len_sq = dx * dx + dy * dy;
    if len_sq > 0.0 {
        let len = len_sq.sqrt();
        dx = dx / len * MOVE_SPEED;
        dy = dy / len * MOVE_SPEED;

        // Update facing direction
        player.facing_angle = dy.atan2(dx);
    }

    player.x += dx;
    player.y += dy;
}
```

### Analog Stick Movement

```rust
const DEADZONE: f32 = 0.15;
const MAX_SPEED: f32 = 5.0;

fn update_analog_movement(player: &mut Player) {
    let stick_x = left_stick_x(0);
    let stick_y = left_stick_y(0);

    let magnitude = (stick_x * stick_x + stick_y * stick_y).sqrt();

    if magnitude > DEADZONE {
        // Normalize and apply speed based on stick deflection
        let norm_x = stick_x / magnitude;
        let norm_y = stick_y / magnitude;

        // Remap magnitude from deadzone-1.0 to 0.0-1.0
        let adjusted_mag = ((magnitude - DEADZONE) / (1.0 - DEADZONE)).min(1.0);

        let speed = adjusted_mag * MAX_SPEED;

        player.x += norm_x * speed;
        player.y += norm_y * speed;

        player.facing_angle = stick_y.atan2(stick_x);
    }
}
```

---

## Tank Controls

Character rotates in place, moves forward/backward relative to facing.

```rust
const ROTATION_SPEED: f32 = 3.0;  // Degrees per frame
const FORWARD_SPEED: f32 = 3.0;
const BACKWARD_SPEED: f32 = 1.5;

struct TankPlayer {
    x: f32,
    y: f32,
    angle: f32,  // Degrees, 0 = right (+X), 90 = down (+Y screen space)
}

fn update_tank_movement(player: &mut TankPlayer) {
    // Rotation with left/right
    if button_held(0, button::LEFT) {
        player.angle -= ROTATION_SPEED;
    }
    if button_held(0, button::RIGHT) {
        player.angle += ROTATION_SPEED;
    }

    // Normalize angle
    while player.angle < 0.0 { player.angle += 360.0; }
    while player.angle >= 360.0 { player.angle -= 360.0; }

    // Forward/backward movement
    let rad = player.angle.to_radians();
    let cos_a = rad.cos();
    let sin_a = rad.sin();

    if button_held(0, button::UP) {
        player.x += cos_a * FORWARD_SPEED;
        player.y += sin_a * FORWARD_SPEED;
    }
    if button_held(0, button::DOWN) {
        player.x -= cos_a * BACKWARD_SPEED;
        player.y -= sin_a * BACKWARD_SPEED;
    }
}
```

### Tank Controls with Strafing

Add L1/R1 for side-stepping while maintaining facing:

```rust
const STRAFE_SPEED: f32 = 2.5;

fn update_tank_with_strafe(player: &mut TankPlayer) {
    // ... rotation and forward/back as above ...

    // Strafe perpendicular to facing
    let rad = player.angle.to_radians();
    let strafe_x = -rad.sin();  // Perpendicular to facing
    let strafe_y = rad.cos();

    if button_held(0, button::L1) {
        player.x += strafe_x * STRAFE_SPEED;
        player.y += strafe_y * STRAFE_SPEED;
    }
    if button_held(0, button::R1) {
        player.x -= strafe_x * STRAFE_SPEED;
        player.y -= strafe_y * STRAFE_SPEED;
    }
}
```

---

## Acceleration and Deceleration Curves

Smooth movement with momentum.

```rust
const MAX_SPEED: f32 = 6.0;
const ACCELERATION: f32 = 0.6;
const DECELERATION: f32 = 0.4;  // Applied when changing direction
const FRICTION: f32 = 0.85;      // Applied when no input

struct MomentumPlayer {
    x: f32,
    y: f32,
    vel_x: f32,
    vel_y: f32,
}

fn update_momentum_movement(player: &mut MomentumPlayer) {
    let input_x = if button_held(0, button::RIGHT) { 1.0 }
                  else if button_held(0, button::LEFT) { -1.0 }
                  else { 0.0 };

    let input_y = if button_held(0, button::DOWN) { 1.0 }
                  else if button_held(0, button::UP) { -1.0 }
                  else { 0.0 };

    if input_x != 0.0 {
        // Check if changing direction (apply stronger decel)
        let changing_dir = (input_x > 0.0 && player.vel_x < 0.0) ||
                           (input_x < 0.0 && player.vel_x > 0.0);

        let accel = if changing_dir { DECELERATION } else { ACCELERATION };
        player.vel_x += input_x * accel;
    } else {
        // Apply friction when no input
        player.vel_x *= FRICTION;
        if player.vel_x.abs() < 0.1 { player.vel_x = 0.0; }
    }

    // Same for Y axis
    if input_y != 0.0 {
        let changing_dir = (input_y > 0.0 && player.vel_y < 0.0) ||
                           (input_y < 0.0 && player.vel_y > 0.0);
        let accel = if changing_dir { DECELERATION } else { ACCELERATION };
        player.vel_y += input_y * accel;
    } else {
        player.vel_y *= FRICTION;
        if player.vel_y.abs() < 0.1 { player.vel_y = 0.0; }
    }

    // Clamp to max speed
    player.vel_x = player.vel_x.clamp(-MAX_SPEED, MAX_SPEED);
    player.vel_y = player.vel_y.clamp(-MAX_SPEED, MAX_SPEED);

    // Apply velocity
    player.x += player.vel_x;
    player.y += player.vel_y;
}
```

### Speed Curves

Different acceleration feel profiles:

```rust
enum SpeedCurve {
    Linear,      // Constant acceleration
    EaseIn,      // Slow start, fast end
    EaseOut,     // Fast start, slow end
    Custom(fn(f32) -> f32),
}

fn apply_curve(input: f32, current_speed: f32, max_speed: f32, curve: SpeedCurve) -> f32 {
    let target = input * max_speed;
    let diff = target - current_speed;

    match curve {
        SpeedCurve::Linear => {
            current_speed + diff.signum() * ACCELERATION.min(diff.abs())
        }
        SpeedCurve::EaseIn => {
            // Accelerate faster as we approach target speed
            let progress = current_speed.abs() / max_speed;
            let accel = ACCELERATION * (0.3 + 0.7 * progress);
            current_speed + diff.signum() * accel.min(diff.abs())
        }
        SpeedCurve::EaseOut => {
            // Accelerate slower as we approach target speed
            let remaining = 1.0 - (current_speed.abs() / max_speed);
            let accel = ACCELERATION * (0.3 + 0.7 * remaining);
            current_speed + diff.signum() * accel.min(diff.abs())
        }
        SpeedCurve::Custom(f) => {
            let t = current_speed.abs() / max_speed;
            let factor = f(t);
            current_speed + diff.signum() * (ACCELERATION * factor).min(diff.abs())
        }
    }
}
```

---

## Dash Mechanics (Complete)

Quick directional burst with cooldown and i-frames.

```rust
const DASH_SPEED: f32 = 18.0;
const DASH_DURATION: u32 = 8;      // Frames of dash movement
const DASH_COOLDOWN: u32 = 45;     // Frames before can dash again
const DASH_IFRAMES: u32 = 6;       // Invincibility at start of dash

#[derive(Clone, Copy, PartialEq)]
enum DashState {
    Ready,
    Dashing { frames_left: u32, dir_x: f32, dir_y: f32 },
    Cooldown(u32),
}

struct DashPlayer {
    x: f32,
    y: f32,
    dash_state: DashState,
    iframes: u32,
}

impl DashPlayer {
    fn try_dash(&mut self) {
        if self.dash_state != DashState::Ready {
            return;
        }

        if !button_pressed(0, button::L1) {
            return;
        }

        // Get dash direction from stick or facing
        let mut dir_x = left_stick_x(0);
        let mut dir_y = left_stick_y(0);

        let magnitude = (dir_x * dir_x + dir_y * dir_y).sqrt();
        if magnitude < 0.3 {
            // No stick input, dash in facing direction
            dir_x = 1.0;  // Default right, or use player.facing
            dir_y = 0.0;
        } else {
            dir_x /= magnitude;
            dir_y /= magnitude;
        }

        self.dash_state = DashState::Dashing {
            frames_left: DASH_DURATION,
            dir_x,
            dir_y,
        };
        self.iframes = DASH_IFRAMES;
    }

    fn update_dash(&mut self) {
        match self.dash_state {
            DashState::Ready => {}

            DashState::Dashing { frames_left, dir_x, dir_y } => {
                // Move in dash direction
                self.x += dir_x * DASH_SPEED;
                self.y += dir_y * DASH_SPEED;

                if frames_left > 1 {
                    self.dash_state = DashState::Dashing {
                        frames_left: frames_left - 1,
                        dir_x,
                        dir_y,
                    };
                } else {
                    self.dash_state = DashState::Cooldown(DASH_COOLDOWN);
                }
            }

            DashState::Cooldown(frames) => {
                if frames > 1 {
                    self.dash_state = DashState::Cooldown(frames - 1);
                } else {
                    self.dash_state = DashState::Ready;
                }
            }
        }

        // Update i-frames
        if self.iframes > 0 {
            self.iframes -= 1;
        }
    }

    fn is_dashing(&self) -> bool {
        matches!(self.dash_state, DashState::Dashing { .. })
    }

    fn can_act(&self) -> bool {
        !self.is_dashing()
    }
}
```

### Dash Variants

```rust
// Ground dash with afterimage
fn update_ground_dash(player: &mut DashPlayer, afterimages: &mut Vec<AfterImage>) {
    if player.is_dashing() {
        // Spawn afterimage every 2 frames
        if player.dash_frames_left() % 2 == 0 {
            afterimages.push(AfterImage {
                x: player.x,
                y: player.y,
                alpha: 0.7,
                decay: 0.1,
            });
        }
    }
}

// Air dash (can only dash once until landing)
struct AirDashPlayer {
    can_air_dash: bool,
    grounded: bool,
    // ... other fields
}

impl AirDashPlayer {
    fn try_air_dash(&mut self) {
        if self.grounded {
            self.can_air_dash = true;
            return;
        }

        if !self.can_air_dash {
            return;
        }

        if button_pressed(0, button::L1) {
            self.can_air_dash = false;
            self.start_dash();
        }
    }
}
```

---

## Dodge Roll

Rolling dodge with movement and i-frames.

```rust
const ROLL_SPEED: f32 = 8.0;
const ROLL_DURATION: u32 = 20;
const ROLL_IFRAMES_START: u32 = 3;   // Frames before i-frames kick in
const ROLL_IFRAMES_END: u32 = 15;    // Frames where i-frames end
const ROLL_COOLDOWN: u32 = 10;

struct RollState {
    rolling: bool,
    frame: u32,
    dir_x: f32,
    dir_y: f32,
    cooldown: u32,
}

impl RollState {
    fn try_roll(&mut self, input_x: f32, input_y: f32) -> bool {
        if self.rolling || self.cooldown > 0 {
            return false;
        }

        if !button_pressed(0, button::B) {
            return false;
        }

        // Roll in input direction or facing direction
        let magnitude = (input_x * input_x + input_y * input_y).sqrt();
        if magnitude > 0.3 {
            self.dir_x = input_x / magnitude;
            self.dir_y = input_y / magnitude;
        } else {
            self.dir_x = 1.0;  // Default
            self.dir_y = 0.0;
        }

        self.rolling = true;
        self.frame = 0;
        true
    }

    fn update(&mut self, player_x: &mut f32, player_y: &mut f32) -> bool {
        // Is player invulnerable?
        let invulnerable;

        if self.rolling {
            self.frame += 1;

            // Movement with ease-out curve
            let progress = self.frame as f32 / ROLL_DURATION as f32;
            let speed = ROLL_SPEED * (1.0 - progress * 0.5);  // Slow down toward end

            *player_x += self.dir_x * speed;
            *player_y += self.dir_y * speed;

            // I-frames active in middle of roll
            invulnerable = self.frame >= ROLL_IFRAMES_START &&
                           self.frame <= ROLL_IFRAMES_END;

            if self.frame >= ROLL_DURATION {
                self.rolling = false;
                self.cooldown = ROLL_COOLDOWN;
            }
        } else {
            invulnerable = false;

            if self.cooldown > 0 {
                self.cooldown -= 1;
            }
        }

        invulnerable
    }
}
```

---

## Sprint Mechanic

Hold button to move faster with stamina management.

```rust
const WALK_SPEED: f32 = 3.0;
const SPRINT_SPEED: f32 = 6.0;
const STAMINA_MAX: f32 = 100.0;
const STAMINA_DRAIN: f32 = 1.0;    // Per frame while sprinting
const STAMINA_REGEN: f32 = 0.5;    // Per frame while not sprinting
const STAMINA_MIN_TO_START: f32 = 20.0;  // Need this much to start sprinting

struct SprintPlayer {
    x: f32,
    y: f32,
    stamina: f32,
    sprinting: bool,
}

impl SprintPlayer {
    fn update_movement(&mut self) {
        let input_x = left_stick_x(0);
        let input_y = left_stick_y(0);

        let magnitude = (input_x * input_x + input_y * input_y).sqrt();

        // Sprint toggle with L3 (left stick click)
        if button_pressed(0, button::L3) && self.stamina >= STAMINA_MIN_TO_START {
            self.sprinting = !self.sprinting;
        }

        // Stop sprinting if out of stamina
        if self.stamina <= 0.0 {
            self.sprinting = false;
        }

        if magnitude > 0.15 {
            let speed = if self.sprinting { SPRINT_SPEED } else { WALK_SPEED };
            let norm_x = input_x / magnitude;
            let norm_y = input_y / magnitude;

            self.x += norm_x * speed;
            self.y += norm_y * speed;

            // Drain stamina while sprinting and moving
            if self.sprinting {
                self.stamina = (self.stamina - STAMINA_DRAIN).max(0.0);
            }
        } else {
            // Not moving, stop sprinting
            self.sprinting = false;
        }

        // Regenerate stamina when not sprinting
        if !self.sprinting {
            self.stamina = (self.stamina + STAMINA_REGEN).min(STAMINA_MAX);
        }
    }
}
```

---

## Complete Movement System

Combining multiple mechanics:

```rust
fn update_player_movement(player: &mut FullPlayer) {
    // Priority: Dash > Roll > Normal movement

    // Try dash first
    player.try_dash();
    if player.is_dashing() {
        player.update_dash();
        return;
    }

    // Try roll
    let input_x = left_stick_x(0);
    let input_y = left_stick_y(0);
    if player.roll.try_roll(input_x, input_y) {
        // Roll started
    }
    player.invulnerable = player.roll.update(&mut player.x, &mut player.y);
    if player.roll.rolling {
        return;
    }

    // Normal movement with momentum
    update_momentum_movement(player);

    // Sprint modifier
    if button_held(0, button::L3) && player.stamina > 0.0 {
        player.vel_x *= 1.5;
        player.vel_y *= 1.5;
        player.stamina -= STAMINA_DRAIN;
    } else {
        player.stamina = (player.stamina + STAMINA_REGEN).min(STAMINA_MAX);
    }
}
```
