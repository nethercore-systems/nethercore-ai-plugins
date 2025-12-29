---
name: Nethercore ZX Game Development
description: This skill should be used when the user asks to "create a Nethercore ZX game", "develop a ZX example", "build a ZX showcase", "write ZX game code", "use ZX FFI functions", "create nether.toml", "build WASM game for Nethercore", "implement ZX graphics", "add ZX audio", or mentions Nethercore ZX development, zx.rs, zx.h, zx.zig, nether build, nether init, nether run, ZX FFI, fantasy console game development, rollback netcode game, or WASM game with assets. Provides comprehensive Nethercore ZX game development guidance including FFI specifications for Rust/C/Zig, asset pipeline, project structure, and CLI tooling.
version: 1.0.0
---

# Nethercore ZX Game Development

## Overview

Nethercore ZX is a fantasy console targeting 5th-generation aesthetics (PS1/N64/Saturn) with modern rollback netcode. Games compile to WebAssembly and run in the Nethercore player with automatic state synchronization for multiplayer.

**Console Specifications:**
- Resolution: 960×540 (fixed, 16:9)
- Color: RGBA8 format (0xRRGGBBAA)
- Tick Rate: 24/30/60/120 fps (configurable)
- ROM Size: 16MB max (WASM + assets)
- WASM Memory: 4MB (auto-snapshotted for rollback)
- VRAM: 4MB (textures, meshes, audio)
- Players: 1-4 (local + remote mix)
- Netcode: GGRS deterministic rollback

**Coordinate System:** Y-up, right-handed. Forward is **-Z**, right is **+X**, up is **+Y**.
See `references/coordinate-conventions.md` for camera formulas and angle conventions.

## Source Files for Current FFI Specs

**IMPORTANT:** For complete and current FFI specifications, read the source files directly:

| File | Language | Purpose |
|------|----------|---------|
| `nethercore/include/zx.rs` | Rust | **Canonical FFI source of truth** (~1700 lines) |
| `nethercore/include/zx.h` | C/C++ | Generated header with NCZX_ prefixes |
| `nethercore/include/zx.zig` | Zig | Generated module with slice helpers |
| `nethercore/docs/book/src/cheat-sheet.md` | All | Quick function reference |
| `nethercore/docs/book/src/api/` | All | Detailed API documentation by category |

When implementing FFI functions, always read the relevant source file to get accurate signatures and documentation.

## Required Game Exports

Every game must export exactly three functions:

### Rust
```rust
#[no_mangle]
pub extern "C" fn init() {
    // Called once at startup - configure render mode, load assets
}

#[no_mangle]
pub extern "C" fn update() {
    // Called every tick - deterministic game logic (rollback-safe)
}

#[no_mangle]
pub extern "C" fn render() {
    // Called every frame - drawing only (skipped during rollback)
}
```

### C/C++
```c
#include "zx.h"

void init(void) { /* configuration and asset loading */ }
void update(void) { /* deterministic game logic */ }
void render(void) { /* drawing commands */ }
```

### Zig
```zig
const zx = @import("zx");

export fn init() void { }
export fn update() void { }
export fn render() void { }
```

## Rollback Safety Rules

The `update()` function must be deterministic for rollback netcode:

1. **All state in WASM memory** - Use static variables, automatically snapshotted
2. **Use `random()` functions** - Never external randomness (read zx.rs for RNG functions)
3. **No time checks in update()** - Use `tick_count()` for frame-based logic
4. **render() is display-only** - Never modify game state in render

## Project Structure

**CRITICAL: Proper File Organization**

Keep `lib.rs`/`game.c`/`main.zig` minimal (~50 lines max). All FFI bindings in a separate module file. Never copy FFI functions inline.

### Rust Project (Recommended)
```
my-game/
├── Cargo.toml          # [lib] crate-type = ["cdylib"]
├── nether.toml         # Game manifest with assets
├── src/
│   ├── lib.rs          # MINIMAL: mod declarations + entry points only
│   ├── zx.rs           # FFI bindings - NEVER EDIT (fetched from GitHub)
│   ├── player.rs       # Game systems in separate files
│   └── enemies.rs      # Target 200 lines per file, max 300
└── assets/             # Optional: textures, meshes, sounds
```

**lib.rs (keep minimal ~30-50 lines):**
```rust
#![no_std]

mod zx;       // FFI bindings module
mod player;   // Game modules

use zx::*;
use player::*;

static mut STATE: Option<GameState> = None;

#[no_mangle]
pub extern "C" fn init() { /* initialize state */ }

#[no_mangle]
pub extern "C" fn update() { /* call state.update() */ }

#[no_mangle]
pub extern "C" fn render() { /* call state.render() */ }
```

**src/zx.rs:** Fetch complete bindings from GitHub (see below)

**Cargo.toml:**
```toml
[package]
name = "my-game"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[profile.release]
opt-level = "z"
lto = true
```

### C Project
```
my-game/
├── Makefile            # clang --target=wasm32 compilation
├── nether.toml         # Game manifest
├── zx.h                # FFI bindings - NEVER EDIT (fetched from GitHub)
├── game.c              # MINIMAL: includes + entry points
├── player.c/h          # Game systems in separate files
└── enemies.c/h         # Target 200 lines per file, max 300
```

### Zig Project
```
my-game/
├── build.zig           # Zig build configuration
├── nether.toml         # Game manifest
└── src/
    ├── main.zig        # MINIMAL: imports + entry points only
    ├── zx.zig          # FFI bindings - NEVER EDIT (fetched from GitHub)
    ├── player.zig      # Game systems in separate files
    └── enemies.zig     # Target 200 lines per file, max 300
```

## Fetching FFI Bindings

**IMPORTANT:** Always fetch complete, up-to-date bindings from GitHub. Never copy individual functions inline.

| Language | GitHub URL |
|----------|------------|
| Rust | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.rs` |
| C | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.h` |
| Zig | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.zig` |

**Fetch command:**
```bash
# Rust
curl -o src/zx.rs https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.rs

# C
curl -o zx.h https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.h

# Zig
curl -o src/zx.zig https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.zig
```

**In module files, access FFI via:**
```rust
// src/player.rs
use crate::zx::*;  // Access FFI through crate root
```

## Build Workflow

### Create New Project
```bash
mkdir my-game && cd my-game
cargo init --lib --name my_game

# Initialize nether manifest
nether init --id my-game --title "My Game"
```

### Build and Run
```bash
nether build              # Compile WASM + pack assets into ROM
nether run                # Build and launch in player
nether run --debug        # Debug build
nether run --sync-test    # Test rollback determinism
nether run --p2p-test     # Two-instance netplay test
```

### Manifest Format (nether.toml)
```toml
[game]
id = "my-game"
title = "My Game"
author = "Developer"
version = "1.0.0"

[build]
# Optional: defaults to cargo for Rust projects
# script = "cargo build --target wasm32-unknown-unknown --release"
# wasm = "target/wasm32-unknown-unknown/release/my_game.wasm"

[[assets.textures]]
id = "player"
path = "assets/player.png"

[[assets.meshes]]
id = "level"
path = "assets/level.obj"

[[assets.sounds]]
id = "jump"
path = "assets/jump.wav"

[[assets.trackers]]
id = "music"
path = "assets/music.xm"
```

## FFI Function Categories

The FFI provides 250+ functions. **Read the source files for complete signatures.**

| Category | Key Functions | Source Location |
|----------|--------------|-----------------|
| System | `delta_time`, `elapsed_time`, `tick_count`, `log` | zx.rs lines 1-100 |
| Random | `random`, `random_range`, `random_f32` | zx.rs (search "random") |
| Config | `set_tick_rate`, `set_clear_color`, `render_mode` | zx.rs (init-only) |
| Input | `button_held`, `button_pressed`, `left_stick_x/y` | zx.rs (search "button") |
| Camera | `camera_set`, `camera_fov`, `push_view_matrix` | zx.rs (search "camera") |
| Transforms | `push_translate`, `push_rotate_y`, `push_scale` | zx.rs (search "push_") |
| Meshes | `load_mesh`, `draw_mesh`, `cube`, `sphere` | zx.rs (search "mesh") |
| Textures | `load_texture`, `texture_bind` | zx.rs (search "texture") |
| Audio | `load_sound`, `play_sound`, `music_play` | zx.rs (search "sound\|music") |
| 2D Drawing | `draw_sprite`, `draw_text`, `draw_rect` | zx.rs (search "draw_") |
| Environment | `draw_env`, `env_gradient`, `env_scatter` | zx.rs (search "env_") |
| Materials | `material_metallic`, `light_set` | zx.rs (search "material\|light") |
| ROM Loading | `rom_texture`, `rom_mesh`, `rom_sound` | zx.rs (search "rom_") |
| Debug | `debug_register_f32`, `debug_watch_i32` | zx.rs (search "debug_") |

## Init-Only Functions

These functions must only be called during `init()`:

- `set_tick_rate(rate)` - 0=24fps, 1=30fps, 2=60fps, 3=120fps
- `set_clear_color(color)` - Background color (0xRRGGBBAA)
- `render_mode(mode)` - 0=Lambert, 1=Matcap, 2=PBR, 3=Hybrid
- All `rom_*()` functions - Asset loading from ROM
- All procedural mesh functions - `cube()`, `sphere()`, etc.
- `load_sound()`, `load_texture()`, `load_mesh()`

## Render Modes

| Mode | Name | Use Case |
|------|------|----------|
| 0 | Lambert | Flat colors, 2D games, stylized |
| 1 | Matcap | Sculpted look, toon shading |
| 2 | PBR | Realistic materials (default) |
| 3 | Hybrid | PBR + matcap blend |

## Asset Pipeline

### Supported Formats

| Type | Input Formats | Notes |
|------|---------------|-------|
| Textures | PNG, JPG | Auto-converted to RGBA8 or BC7 |
| Meshes | .obj, .gltf, .glb, .nczxmesh | Auto-converted |
| Sounds | .wav | 22050Hz, 16-bit mono |
| Music | .xm | XM tracker modules |
| Data | Any binary | Raw bytes |

### Loading Assets

```rust
// From ROM data pack (recommended)
let tex = rom_texture_str("player");
let mesh = rom_mesh_str("level");
let sound = rom_sound_str("jump");
```

## Common Patterns

### Basic Game Loop
```rust
static mut PLAYER_X: f32 = 480.0;
static mut PLAYER_Y: f32 = 270.0;

#[no_mangle]
pub extern "C" fn init() {
    set_clear_color(0x1a1a2eFF);
    render_mode(2);
}

#[no_mangle]
pub extern "C" fn update() {
    unsafe {
        let speed = 200.0 * delta_time();
        PLAYER_X += left_stick_x(0) * speed;
        PLAYER_Y += left_stick_y(0) * speed;
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        draw_rect(PLAYER_X - 16.0, PLAYER_Y - 16.0, 32.0, 32.0, 0xFF0000FF);
    }
}
```

### 3D Scene
```rust
#[no_mangle]
pub extern "C" fn render() {
    draw_env();  // Draw procedural environment/sky
    camera_set(0.0, 5.0, 10.0, 0.0, 0.0, 0.0);

    push_translate(0.0, 0.0, 0.0);
    draw_mesh(mesh_handle);
    push_identity();
}
```

## Language-Specific Notes

### Rust
- **Fetch `zx.rs` to `src/zx.rs`** - Never copy functions inline
- **Use `mod zx;` in lib.rs** - Access via `use zx::*;` or `use crate::zx::*;`
- Helper functions: `log_str()`, `draw_text_str()`, `rom_texture_str()`
- Use `#![no_std]` for smaller WASM

### C/C++
- **Fetch `zx.h` to project root** - Include with `#include "zx.h"`
- NCZX_ prefixed constants: `NCZX_BUTTON_A`, `NCZX_RENDER_PBR`
- Helper macros: `NCZX_LOG()`, `NCZX_DRAW_TEXT()`, `NCZX_ROM_TEXTURE()`

### Zig
- **Fetch `zx.zig` to `src/zx.zig`** - Import with `const zx = @import("zx.zig");`
- Namespace access: `zx.Button.a`, `zx.Render.pbr`
- Slice helpers: `zx.logStr()`, `zx.drawTextStr()`, `zx.romTexture()`

## Documentation Resources

For detailed documentation, consult these locations in the nethercore repository:

### FFI Source (Always Current)
- **`nethercore/include/zx.rs`** - Rust FFI with full documentation comments
- **`nethercore/include/zx.h`** - C header with inline helpers
- **`nethercore/include/zx.zig`** - Zig module with slice-based helpers

### Developer Guide (mdBook)
- **`nethercore/docs/book/src/`** - Comprehensive game developer guide
- **`nethercore/docs/book/src/cheat-sheet.md`** - Quick FFI reference
- **`nethercore/docs/book/src/tutorials/paddle/`** - 8-part tutorial
- **`nethercore/docs/book/src/api/`** - Detailed API docs by category

### Examples
- **`nethercore/examples/`** - Working example projects
- **`nethercore/examples/1-getting-started/`** - Hello world in Rust, C, Zig
- **`nethercore/examples/7-games/`** - Complete game examples

### CLI Tools
- **`nethercore/tools/nether-cli/`** - nether CLI source
- Run `nether --help` for command reference

## Additional Resources

### Reference Files (in this skill)
- **`references/source-guide.md`** - Guide to reading source files
- **`references/quick-patterns.md`** - Common code patterns

### Example Files (in this skill)
- **`examples/hello-world-rust.md`** - Complete Rust hello world
- **`examples/hello-world-c.md`** - Complete C hello world
- **`examples/hello-world-zig.md`** - Complete Zig hello world
- **`examples/game-with-assets.md`** - Game with textures, meshes, sounds
- **`examples/nether-toml-examples.md`** - Manifest examples

### Publishing Your Game

When your game is ready for release, use the `zx-publish` plugin:
- **`/prepare-platform-assets`** - Create icon (64x64), screenshots, and banner
- **`/publish-game`** - Package ROM with `nether pack` and guide platform upload
- **`publishing-workflow` skill** - ROM packaging and nethercore.systems upload
- **`platform-assets` skill** - Marketing asset specifications
