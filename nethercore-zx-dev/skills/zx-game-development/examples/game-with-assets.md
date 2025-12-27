# Game with Assets

Example game using textures, meshes, sounds, and music.

## Project Structure

```
my-game/
├── Cargo.toml
├── nether.toml
├── src/
│   └── lib.rs
└── assets/
    ├── player.png          # 64x64 player sprite
    ├── tileset.png         # Texture atlas
    ├── level.obj           # 3D level mesh
    ├── jump.wav            # Jump sound effect
    ├── coin.wav            # Pickup sound
    └── bgm.xm              # Background music (XM tracker)
```

## nether.toml

```toml
[game]
id = "my-game"
title = "My Game"
author = "Developer"
version = "1.0.0"

[build]
# Uses cargo defaults

# Textures - PNG/JPG, auto-converted
[[assets.textures]]
id = "player"
path = "assets/player.png"

[[assets.textures]]
id = "tileset"
path = "assets/tileset.png"

# Meshes - OBJ/GLTF/GLB, auto-converted
[[assets.meshes]]
id = "level"
path = "assets/level.obj"

# Sounds - WAV (22050Hz, 16-bit mono)
[[assets.sounds]]
id = "jump"
path = "assets/jump.wav"

[[assets.sounds]]
id = "coin"
path = "assets/coin.wav"

# Music - XM tracker files
[[assets.trackers]]
id = "bgm"
path = "assets/bgm.xm"
```

## src/lib.rs

```rust
mod zx;
use zx::*;

// Asset handles (loaded once in init)
static mut PLAYER_TEX: u32 = 0;
static mut TILESET_TEX: u32 = 0;
static mut LEVEL_MESH: u32 = 0;
static mut JUMP_SFX: u32 = 0;
static mut COIN_SFX: u32 = 0;
static mut BGM: u32 = 0;

// Game state
static mut PLAYER_X: f32 = 480.0;
static mut PLAYER_Y: f32 = 400.0;
static mut PLAYER_VY: f32 = 0.0;
static mut ON_GROUND: bool = true;
static mut SCORE: u32 = 0;
static mut CAMERA_Y: f32 = 0.0;

const GRAVITY: f32 = 800.0;
const JUMP_FORCE: f32 = 400.0;
const MOVE_SPEED: f32 = 200.0;
const GROUND_Y: f32 = 450.0;

#[no_mangle]
pub extern "C" fn init() {
    // Configure rendering
    set_clear_color(0x87CEEBFF);  // Sky blue
    render_mode(2);               // PBR for 3D elements

    unsafe {
        // Load textures
        PLAYER_TEX = rom_texture_str("player");
        TILESET_TEX = rom_texture_str("tileset");

        // Load mesh
        LEVEL_MESH = rom_mesh_str("level");

        // Load sounds
        JUMP_SFX = rom_sound_str("jump");
        COIN_SFX = rom_sound_str("coin");

        // Load and start music
        BGM = rom_tracker_str("bgm");
        music_play(BGM, 0.7, 1);  // 70% volume, loop

        log_str("Game initialized!");
    }
}

#[no_mangle]
pub extern "C" fn update() {
    unsafe {
        let dt = delta_time();

        // Horizontal movement
        let input_x = left_stick_x(0);
        PLAYER_X += input_x * MOVE_SPEED * dt;
        PLAYER_X = PLAYER_X.clamp(32.0, 928.0);

        // D-pad fallback
        if button_held(0, button::LEFT) != 0 {
            PLAYER_X -= MOVE_SPEED * dt;
        }
        if button_held(0, button::RIGHT) != 0 {
            PLAYER_X += MOVE_SPEED * dt;
        }

        // Jump
        if button_pressed(0, button::A) != 0 && ON_GROUND {
            PLAYER_VY = -JUMP_FORCE;
            ON_GROUND = false;
            play_sound(JUMP_SFX, 1.0, 0.0);
        }

        // Gravity
        if !ON_GROUND {
            PLAYER_VY += GRAVITY * dt;
            PLAYER_Y += PLAYER_VY * dt;

            // Land on ground
            if PLAYER_Y >= GROUND_Y {
                PLAYER_Y = GROUND_Y;
                PLAYER_VY = 0.0;
                ON_GROUND = true;
            }
        }

        // Collect coins (example collision)
        check_coin_collision();

        // Camera follow
        CAMERA_Y = PLAYER_Y - 270.0;
    }
}

fn check_coin_collision() {
    // Example: check collision with coins at fixed positions
    unsafe {
        // Simplified coin pickup
        if button_pressed(0, button::B) != 0 {
            SCORE += 10;
            play_sound(COIN_SFX, 0.8, 0.0);
        }
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        // 3D background with environment
        draw_env();
        camera_set(0.0, 5.0, 15.0, 0.0, 0.0, 0.0);

        // Draw 3D level
        texture_bind(TILESET_TEX);
        push_identity();
        draw_mesh(LEVEL_MESH);

        // Switch to 2D overlay
        layer(10);

        // Draw player sprite
        texture_bind(PLAYER_TEX);
        draw_sprite(
            PLAYER_X - 32.0,
            PLAYER_Y - 64.0 - CAMERA_Y,
            64.0,
            64.0,
            0xFFFFFFFF
        );

        // UI Layer
        layer(20);

        // Score display
        draw_rect(10.0, 10.0, 150.0, 40.0, 0x00000080);
        draw_text_str("SCORE:", 20.0, 20.0, 20.0, 0xFFFFFFFF);
        // Note: For dynamic score display, use a pre-formatted buffer

        // Controls hint
        draw_text_str("A: Jump  B: Collect", 10.0, 510.0, 14.0, 0xFFFFFF80);
    }
}
```

## Asset Creation Notes

### Textures
- **Format:** PNG or JPG
- **Size:** Power of 2 recommended (64x64, 128x128, 256x256)
- **Compression:** Auto-converted to BC7 for modes 1-3, RGBA8 for mode 0

### Meshes
- **Format:** OBJ, GLTF, or GLB
- **Requirements:** Triangulated, UV-mapped for textures
- **Tools:** Blender export to OBJ/GLTF

### Sounds
- **Format:** WAV
- **Sample Rate:** 22050 Hz
- **Bit Depth:** 16-bit
- **Channels:** Mono
- **Tools:** Audacity for conversion

### Music (XM Tracker)
- **Format:** FastTracker II (.xm)
- **Tools:** MilkyTracker, OpenMPT
- **Note:** Sample data stripped during ROM packing

## Build and Run

```bash
# Build ROM with assets
nether build

# Run game
nether run

# Debug mode
nether run --debug
```

## Testing

```bash
# Test rollback determinism
nether run --sync-test

# Test 2-player netplay locally
nether run --p2p-test
```
