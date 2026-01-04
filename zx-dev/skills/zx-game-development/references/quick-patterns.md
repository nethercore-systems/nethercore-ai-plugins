# Quick Patterns

Common code patterns for Nethercore ZX development. For exact function signatures, read the source files.

## Game Structure

### Minimal Game (Rust)
```rust
#![no_std]
#![no_main]

mod zx;
use zx::*;

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! { loop {} }

#[no_mangle]
pub extern "C" fn init() {
    set_clear_color(0x1a1a2eFF);
}

#[no_mangle]
pub extern "C" fn update() {}

#[no_mangle]
pub extern "C" fn render() {
    draw_text_str("Hello ZX!", 400.0, 260.0, 32.0, 0xFFFFFFFF);
}
```

### Minimal Game (C)
```c
#include "zx.h"

void init(void) {
    set_clear_color(nczx_rgba(26, 26, 46, 255));
}

void update(void) {}

void render(void) {
    NCZX_DRAW_TEXT("Hello ZX!", 400.0f, 260.0f, 32.0f, NCZX_COLOR_WHITE);
}
```

### Minimal Game (Zig)
```zig
const zx = @import("zx");

export fn init() void {
    zx.set_clear_color(zx.rgba(26, 26, 46, 255));
}

export fn update() void {}

export fn render() void {
    zx.drawTextStr("Hello ZX!", 400.0, 260.0, 32.0, zx.color.white);
}
```

## Input Patterns

### D-Pad Movement
```rust
let mut dx: f32 = 0.0;
let mut dy: f32 = 0.0;

if button_held(0, button::LEFT) != 0 { dx -= 1.0; }
if button_held(0, button::RIGHT) != 0 { dx += 1.0; }
if button_held(0, button::UP) != 0 { dy -= 1.0; }
if button_held(0, button::DOWN) != 0 { dy += 1.0; }

// Normalize diagonal
let len = (dx * dx + dy * dy).sqrt();
if len > 0.0 {
    dx /= len;
    dy /= len;
}

player_x += dx * SPEED * delta_time();
player_y += dy * SPEED * delta_time();
```

### Analog Stick Movement
```rust
let x = left_stick_x(0);
let y = left_stick_y(0);
player_x += x * SPEED * delta_time();
player_y += y * SPEED * delta_time();
```

### Jump on Button Press
```rust
if button_pressed(0, button::A) != 0 && on_ground {
    velocity_y = -JUMP_FORCE;
    on_ground = false;
}
```

## Rendering Patterns

### 2D Game Setup
```rust
fn init() {
    set_clear_color(0x000000FF);
    render_mode(0);  // Lambert for 2D
}

fn render() {
    // Layer 0: Background (use z_index for 2D ordering)
    z_index(0);
    set_color(bg_color);
    draw_sprite(0.0, 0.0, 960.0, 540.0);

    // Layer 1: Game objects
    z_index(1);
    set_color(0xFFFFFFFF);
    draw_sprite(player_x, player_y, 32.0, 32.0);

    // Layer 2: UI
    z_index(2);
    set_color(0xFFFFFFFF);
    draw_text_str(&format!("Score: {}", score), 10.0, 10.0, 16.0);
}
```

### 3D Scene Setup
```rust
fn init() {
    set_clear_color(0x87CEEBFF);  // Sky blue
    render_mode(2);  // PBR
}

fn render() {
    draw_env();  // Draw procedural environment/sky
    camera_set(cam_x, cam_y, cam_z, look_x, look_y, look_z);

    // Draw world
    push_identity();
    draw_mesh(ground_mesh);

    push_translate(player_x, player_y, player_z);
    push_rotate_y(player_rotation);
    draw_mesh(player_mesh);

    push_identity();
}
```

### Split-Screen
```rust
fn render() {
    // Player 1 (left half)
    viewport(0, 0, 480, 540);
    camera_set(p1_cam_x, p1_cam_y, p1_cam_z, p1_look_x, p1_look_y, p1_look_z);
    draw_scene();

    // Player 2 (right half)
    viewport(480, 0, 480, 540);
    camera_set(p2_cam_x, p2_cam_y, p2_cam_z, p2_look_x, p2_look_y, p2_look_z);
    draw_scene();

    // UI (fullscreen)
    viewport_clear();
    draw_hud();
}
```

## Asset Loading

### From ROM (Recommended)
```rust
static mut PLAYER_TEX: u32 = 0;
static mut LEVEL_MESH: u32 = 0;
static mut JUMP_SFX: u32 = 0;

fn init() {
    unsafe {
        PLAYER_TEX = rom_texture_str("player");
        LEVEL_MESH = rom_mesh_str("level");
        JUMP_SFX = rom_sound_str("jump");
    }
}

fn render() {
    unsafe {
        texture_bind(PLAYER_TEX);
        draw_mesh(LEVEL_MESH);
    }
}

fn play_jump() {
    unsafe { play_sound(JUMP_SFX, 1.0, 0.0); }
}
```

### Procedural Meshes
```rust
static mut CUBE: u32 = 0;
static mut SPHERE: u32 = 0;

fn init() {
    unsafe {
        CUBE = cube_uv(1.0, 1.0, 1.0);
        SPHERE = sphere_uv(1.0, 16, 8);
    }
}
```

## Audio Patterns

### Sound Effects
```rust
// Fire and forget
play_sound(sound_handle, 1.0, 0.0);  // volume, pan

// Positional audio (using channels)
channel_play(0, sound_handle, 1.0, calculate_pan(source_x), 0);  // no loop
channel_set(0, 1.0, calculate_pan(source_x));  // update position each frame
```

### Music
```rust
// Play XM tracker
let music = rom_tracker_str("bgm");
music_play(music, 0.8, 1);  // volume, looping

// Control
music_pause(1);  // pause
music_pause(0);  // resume
music_stop();
```

## State Machine Pattern
```rust
#[derive(Copy, Clone, PartialEq)]
enum GameState {
    Title,
    Playing,
    Paused,
    GameOver,
}

static mut STATE: GameState = GameState::Title;

fn update() {
    unsafe {
        match STATE {
            GameState::Title => {
                if button_pressed(0, button::START) != 0 {
                    STATE = GameState::Playing;
                }
            }
            GameState::Playing => {
                update_gameplay();
                if button_pressed(0, button::START) != 0 {
                    STATE = GameState::Paused;
                }
            }
            GameState::Paused => {
                if button_pressed(0, button::START) != 0 {
                    STATE = GameState::Playing;
                }
            }
            GameState::GameOver => {
                if button_pressed(0, button::A) != 0 {
                    reset_game();
                    STATE = GameState::Title;
                }
            }
        }
    }
}
```

## Collision Detection (AABB)
```rust
fn aabb_overlap(
    x1: f32, y1: f32, w1: f32, h1: f32,
    x2: f32, y2: f32, w2: f32, h2: f32
) -> bool {
    x1 < x2 + w2 && x1 + w1 > x2 && y1 < y2 + h2 && y1 + h1 > y2
}

// Usage
if aabb_overlap(player_x, player_y, 32.0, 32.0, enemy_x, enemy_y, 32.0, 32.0) {
    // Collision!
}
```

## Multiplayer Pattern
```rust
fn update() {
    let count = player_count();

    for p in 0..count {
        let x = left_stick_x(p);
        let y = left_stick_y(p);

        // Move player p
        players[p as usize].x += x * SPEED * delta_time();
        players[p as usize].y += y * SPEED * delta_time();

        if button_pressed(p, button::A) != 0 {
            player_action(p);
        }
    }
}
```

## Debug Registration
```rust
fn init() {
    unsafe {
        debug_group("Player");
        debug_f32("X Position", &PLAYER_X);
        debug_f32("Y Position", &PLAYER_Y);
        debug_f32_range("Speed", &PLAYER_SPEED, 0.0, 500.0);
        debug_group_close();
    }
}
```

Press F3 in-game to open the debug panel.
