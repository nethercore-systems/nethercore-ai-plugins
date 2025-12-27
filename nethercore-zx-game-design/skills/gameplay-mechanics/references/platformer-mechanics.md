# Platformer Mechanics Reference

Complete rollback-safe implementations for 2D/2.5D platformers on Nethercore ZX.

## Variable-Height Jump (Complete)

Gravity scaling based on jump button state creates responsive variable-height jumps.

```rust
use crate::ffi::*;

const GRAVITY: f32 = 0.6;
const FAST_FALL_GRAVITY: f32 = 1.2;  // When falling or button released
const JUMP_VELOCITY: f32 = -12.0;
const MAX_FALL_SPEED: f32 = 15.0;

struct Player {
    x: f32,
    y: f32,
    vel_x: f32,
    vel_y: f32,
    grounded: bool,
    was_grounded: bool,
}

fn update_jump_physics(player: &mut Player) {
    // Track grounded transition for coyote time
    player.was_grounded = player.grounded;

    // Apply gravity - use stronger gravity when falling or button released
    let gravity = if player.vel_y > 0.0 || !button_held(0, button::A) {
        FAST_FALL_GRAVITY
    } else {
        GRAVITY
    };

    player.vel_y += gravity;
    player.vel_y = player.vel_y.min(MAX_FALL_SPEED);

    // Apply velocity
    player.y += player.vel_y;
}

fn try_jump(player: &mut Player) -> bool {
    if button_pressed(0, button::A) && player.grounded {
        player.vel_y = JUMP_VELOCITY;
        player.grounded = false;
        return true;
    }
    false
}
```

### Tuning Variable Jump

| Parameter | Effect | Typical Range |
|-----------|--------|---------------|
| `GRAVITY` | Base fall speed | 0.4–0.8 |
| `FAST_FALL_GRAVITY` | Fall speed when not holding jump | 1.0–1.5 |
| `JUMP_VELOCITY` | Initial upward velocity | -10 to -15 |
| `MAX_FALL_SPEED` | Terminal velocity cap | 12–18 |

**Feel Tips:**
- Higher gravity ratio (fast/normal) = more control over jump height
- Lower `MAX_FALL_SPEED` = floatier feel
- Negative jump velocity because Y increases downward in screen space

---

## Coyote Time (Complete)

Allow jumps for a few frames after leaving a platform edge.

```rust
const COYOTE_FRAMES: u32 = 6;  // ~100ms at 60fps

struct Player {
    x: f32,
    y: f32,
    vel_y: f32,
    grounded: bool,
    was_grounded: bool,
    coyote_timer: u32,
}

fn update_coyote_time(player: &mut Player) {
    if player.grounded {
        // Reset timer when grounded
        player.coyote_timer = COYOTE_FRAMES;
    } else if player.was_grounded && player.vel_y >= 0.0 {
        // Just left ground (walked off, not jumped)
        // Timer already set, will count down
    }

    // Count down when airborne
    if !player.grounded && player.coyote_timer > 0 {
        player.coyote_timer -= 1;
    }
}

fn can_jump(player: &Player) -> bool {
    player.grounded || player.coyote_timer > 0
}

fn try_jump_with_coyote(player: &mut Player) -> bool {
    if button_pressed(0, button::A) && can_jump(player) {
        player.vel_y = JUMP_VELOCITY;
        player.grounded = false;
        player.coyote_timer = 0;  // Consume coyote time
        return true;
    }
    false
}
```

**Why coyote time matters:**
- Players visually perceive platform edges slightly after the character leaves
- 4–8 frames is the sweet spot (too long feels floaty, too short feels punishing)
- Only apply when walking off, not when jumping

---

## Jump Buffering (Complete)

Queue jump input before landing to ensure responsive landings.

```rust
const BUFFER_FRAMES: u32 = 8;  // ~133ms at 60fps

struct Player {
    grounded: bool,
    vel_y: f32,
    jump_buffer: u32,
}

fn update_jump_buffer(player: &mut Player) {
    // Set buffer when jump pressed
    if button_pressed(0, button::A) {
        player.jump_buffer = BUFFER_FRAMES;
    }

    // Count down buffer
    if player.jump_buffer > 0 {
        player.jump_buffer -= 1;
    }
}

fn try_buffered_jump(player: &mut Player) -> bool {
    // Check buffer on landing
    if player.grounded && player.jump_buffer > 0 {
        player.vel_y = JUMP_VELOCITY;
        player.grounded = false;
        player.jump_buffer = 0;  // Consume buffer
        return true;
    }
    false
}
```

### Combined Coyote + Buffer System

```rust
struct JumpState {
    coyote_timer: u32,
    jump_buffer: u32,
}

impl JumpState {
    fn update(&mut self, grounded: bool, was_grounded: bool) {
        // Coyote time
        if grounded {
            self.coyote_timer = COYOTE_FRAMES;
        } else if !grounded && self.coyote_timer > 0 {
            self.coyote_timer -= 1;
        }

        // Jump buffer
        if button_pressed(0, button::A) {
            self.jump_buffer = BUFFER_FRAMES;
        } else if self.jump_buffer > 0 {
            self.jump_buffer -= 1;
        }
    }

    fn try_jump(&mut self, grounded: bool) -> bool {
        let can_jump = grounded || self.coyote_timer > 0;
        let wants_jump = button_pressed(0, button::A) || self.jump_buffer > 0;

        if can_jump && wants_jump {
            self.coyote_timer = 0;
            self.jump_buffer = 0;
            return true;
        }
        false
    }
}
```

---

## Wall Sliding and Wall Jumping

Cling to walls and kick off for advanced platforming.

```rust
const WALL_SLIDE_SPEED: f32 = 2.0;
const WALL_JUMP_VEL_X: f32 = 8.0;
const WALL_JUMP_VEL_Y: f32 = -11.0;
const WALL_STICK_FRAMES: u32 = 6;  // Frames before sliding starts

#[derive(Clone, Copy, PartialEq)]
enum WallSide {
    None,
    Left,
    Right,
}

struct Player {
    x: f32,
    y: f32,
    vel_x: f32,
    vel_y: f32,
    grounded: bool,
    wall_touching: WallSide,
    wall_stick_timer: u32,
    wall_jump_lockout: u32,  // Prevent input override after wall jump
}

fn update_wall_slide(player: &mut Player) {
    // Only wall slide when falling
    if player.wall_touching != WallSide::None && !player.grounded && player.vel_y > 0.0 {
        // Initial stick before sliding
        if player.wall_stick_timer < WALL_STICK_FRAMES {
            player.wall_stick_timer += 1;
            player.vel_y = 0.0;
        } else {
            // Cap fall speed during wall slide
            player.vel_y = player.vel_y.min(WALL_SLIDE_SPEED);
        }
    } else {
        player.wall_stick_timer = 0;
    }

    // Wall jump lockout countdown
    if player.wall_jump_lockout > 0 {
        player.wall_jump_lockout -= 1;
    }
}

fn try_wall_jump(player: &mut Player) -> bool {
    if !button_pressed(0, button::A) || player.grounded {
        return false;
    }

    match player.wall_touching {
        WallSide::Left => {
            player.vel_x = WALL_JUMP_VEL_X;   // Kick away from left wall
            player.vel_y = WALL_JUMP_VEL_Y;
            player.wall_jump_lockout = 10;    // Frames of forced movement
            player.wall_touching = WallSide::None;
            true
        }
        WallSide::Right => {
            player.vel_x = -WALL_JUMP_VEL_X;  // Kick away from right wall
            player.vel_y = WALL_JUMP_VEL_Y;
            player.wall_jump_lockout = 10;
            player.wall_touching = WallSide::None;
            true
        }
        WallSide::None => false,
    }
}

fn apply_movement_input(player: &mut Player) {
    // Skip input during wall jump lockout
    if player.wall_jump_lockout > 0 {
        return;
    }

    // Normal horizontal movement...
    if button_held(0, button::LEFT) {
        player.vel_x -= ACCEL;
    }
    if button_held(0, button::RIGHT) {
        player.vel_x += ACCEL;
    }
}
```

---

## Moving Platforms

Platforms that carry the player.

```rust
struct MovingPlatform {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
    vel_x: f32,
    vel_y: f32,
    // Waypoint data for patrol...
}

fn update_player_on_platform(player: &mut Player, platform: &MovingPlatform) {
    // Check if player is standing on platform
    let on_platform = player.y + PLAYER_HEIGHT >= platform.y &&
                      player.y + PLAYER_HEIGHT <= platform.y + 4.0 &&
                      player.x + PLAYER_WIDTH > platform.x &&
                      player.x < platform.x + platform.width &&
                      player.vel_y >= 0.0;

    if on_platform {
        // Inherit platform velocity
        player.x += platform.vel_x;
        player.y += platform.vel_y;
        player.grounded = true;
    }
}

// Patrol between waypoints
fn update_platform_patrol(platform: &mut MovingPlatform, waypoints: &[(f32, f32)],
                          current_waypoint: &mut usize, speed: f32) {
    let (target_x, target_y) = waypoints[*current_waypoint];
    let dx = target_x - platform.x;
    let dy = target_y - platform.y;
    let dist = (dx * dx + dy * dy).sqrt();

    if dist < speed {
        // Reached waypoint, move to next
        *current_waypoint = (*current_waypoint + 1) % waypoints.len();
    } else {
        // Move toward waypoint
        platform.vel_x = dx / dist * speed;
        platform.vel_y = dy / dist * speed;
        platform.x += platform.vel_x;
        platform.y += platform.vel_y;
    }
}
```

---

## One-Way Platforms

Platforms you can jump through from below.

```rust
struct OneWayPlatform {
    x: f32,
    y: f32,
    width: f32,
}

fn check_one_way_collision(player: &mut Player, platform: &OneWayPlatform) -> bool {
    let player_bottom = player.y + PLAYER_HEIGHT;
    let player_bottom_prev = player_bottom - player.vel_y;

    // Only collide if:
    // 1. Falling (vel_y > 0)
    // 2. Was above platform last frame
    // 3. Is at or below platform this frame
    // 4. Horizontally overlapping
    if player.vel_y > 0.0 &&
       player_bottom_prev <= platform.y &&
       player_bottom >= platform.y &&
       player.x + PLAYER_WIDTH > platform.x &&
       player.x < platform.x + platform.width
    {
        // Snap to platform top
        player.y = platform.y - PLAYER_HEIGHT;
        player.vel_y = 0.0;
        player.grounded = true;
        return true;
    }
    false
}

// Optional: Drop through platform
const DROP_THROUGH_FRAMES: u32 = 10;

fn try_drop_through(player: &mut Player, platform: &OneWayPlatform,
                    drop_timer: &mut u32) -> bool {
    if button_held(0, button::DOWN) && button_pressed(0, button::A) {
        *drop_timer = DROP_THROUGH_FRAMES;
    }

    if *drop_timer > 0 {
        *drop_timer -= 1;
        player.grounded = false;
        return true;  // Skip collision this frame
    }
    false
}
```

---

## Complete Platformer Player Update

Putting it all together:

```rust
fn update_player(player: &mut Player, platforms: &[Platform],
                 moving_platforms: &[MovingPlatform]) {
    // 1. Update jump helpers
    player.jump_state.update(player.grounded, player.was_grounded);
    player.was_grounded = player.grounded;

    // 2. Wall slide
    update_wall_slide(player);

    // 3. Handle jump (ground, coyote, wall)
    if player.jump_state.try_jump(player.grounded) {
        player.vel_y = JUMP_VELOCITY;
        player.grounded = false;
    } else if try_wall_jump(player) {
        // Wall jump handled
    }

    // 4. Horizontal input
    apply_movement_input(player);

    // 5. Apply physics
    update_jump_physics(player);
    apply_friction(player);

    // 6. Move and collide
    player.x += player.vel_x;
    resolve_horizontal_collisions(player, platforms);

    player.y += player.vel_y;
    resolve_vertical_collisions(player, platforms);

    // 7. Moving platform inheritance
    for mp in moving_platforms {
        update_player_on_platform(player, mp);
    }
}
```
