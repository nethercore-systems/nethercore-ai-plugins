---
name: Native Asset Pipeline for ZX
description: This skill should be used when the user asks about "asset pipeline", "build process", "generator binary", "native vs WASM", "build.script", "nether.toml build", "how to integrate generators", "asset generation workflow", "procedural assets build", "compile time assets", "gitignore generated assets", "regenerate assets", or needs to understand how procedural asset generators integrate with the Nethercore ZX build system.
version: 1.0.0
---

# Native Asset Pipeline

## Core Concept

Asset generators are **native binaries** that run on your development machine during the build process. They are NOT WASM and do NOT run in the ZX console.

```
┌─────────────────────────────────────────────────────────────┐
│                    BUILD TIME (Native)                      │
│                                                             │
│  generator/          →  assets/           →  game.nczx     │
│  (Rust/Python/etc)      (PNG, OBJ, WAV)      (bundled ROM) │
│  Runs on your CPU       Standard formats      Final output  │
└─────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────┐
│                    RUN TIME (WASM)                          │
│                                                             │
│  game.nczx  →  ZX Console  →  rom_texture(), rom_mesh()    │
│  All assets pre-bundled      Assets loaded from ROM pack   │
└─────────────────────────────────────────────────────────────┘
```

---

## CRITICAL: FFI Module Usage

**NEVER copy FFI declarations inline.** Always use the canonical zx.rs module:

```bash
# Fetch the FFI module (do this once per project)
curl -o src/zx.rs https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.rs
```

Then in your code:
```rust
mod zx;       // FFI module - NEVER edit or copy inline
use zx::*;    // Access all FFI functions
```

## CRITICAL: Init-Only Resource Loading

**ALL resource loading MUST happen in `init()` ONLY!**

Loading resources in `update()` or `render()` will **CRASH** the game.

Init-only functions include:
- `rom_texture()`, `rom_texture_str()` - texture loading
- `rom_mesh()`, `rom_mesh_str()` - mesh loading  
- `rom_sound()`, `rom_sound_str()` - sound loading
- All procedural mesh functions: `cube()`, `sphere()`, `cylinder()`, etc.

---

## nether.toml Build Integration

The `[build]` section's `script` field chains commands. Generator runs BEFORE WASM compilation:

```toml
[game]
id = "my-game"
title = "My Game"
author = "Developer"
version = "1.0.0"

# Build pipeline: generate assets THEN compile WASM
[build]
script = "cargo run -p generator --release && cargo build -p game --target wasm32-unknown-unknown --release"
wasm = "target/wasm32-unknown-unknown/release/game.wasm"

# Declare generated assets
[[assets.textures]]
id = "player"
path = "../assets/textures/player.png"

[[assets.meshes]]
id = "level"
path = "../assets/meshes/level.obj"

[[assets.sounds]]
id = "jump"
path = "../assets/audio/jump.wav"
```

---

## Project Structure

### Rust Workspace (Recommended)

```
my-game/
├── Cargo.toml              # Workspace manifest
├── generator/
│   ├── Cargo.toml          # Native binary (NOT WASM target)
│   └── src/
│       └── main.rs         # Generates assets to ../assets/
├── game/
│   ├── Cargo.toml          # WASM library (cdylib)
│   ├── nether.toml         # Build config with script chaining
│   └── src/
│       ├── lib.rs          # Game code - minimal entry points
│       └── zx.rs           # FFI module - fetched from GitHub
├── assets/                 # Generated output (gitignored)
│   ├── textures/
│   ├── meshes/
│   └── audio/
└── .gitignore
```

### Python Generator Structure (For Audio/Music)

For audio synthesis, use a modular Python structure with shared lib/:

```
my-game/
├── generator/
│   ├── lib/                # Shared synthesis library (scaffold once)
│   │   ├── __init__.py
│   │   ├── synthesis.py    # ADSR, FM, Karplus-Strong
│   │   ├── waveforms.py    # Oscillators, noise
│   │   ├── drums.py        # Kick, snare, hat
│   │   ├── effects.py      # Reverb, filters
│   │   └── xm_writer.py    # XM file generation
│   ├── instruments/        # One .py per instrument (~50 lines each)
│   │   ├── rhodes.py
│   │   └── guitar.py
│   ├── songs/              # One .py per song (~80 lines each)
│   │   ├── boss_theme.py
│   │   └── menu_music.py
│   └── generate_all.py     # Runs all generators
├── assets/audio/           # Generated output
└── nether.toml
```

### generate_all.py Pattern

Run all audio generators with a single script:

```python
#!/usr/bin/env python3
"""Generate all audio assets."""
import subprocess
from pathlib import Path

generator_dir = Path(__file__).parent

# Generate instruments
for script in sorted((generator_dir / "instruments").glob("*.py")):
    print(f"Running {script.name}...")
    subprocess.run(["python", str(script)], check=True)

# Generate songs
for script in sorted((generator_dir / "songs").glob("*.py")):
    print(f"Running {script.name}...")
    subprocess.run(["python", str(script)], check=True)

print("Audio generation complete!")
```

Update nether.toml to run Python generators:

```toml
[build]
script = "python generator/generate_all.py && cargo build -p game --target wasm32-unknown-unknown --release"
```

---

## Loading Assets in Game (WASM)

**CRITICAL: Use the canonical zx.rs FFI module.** Never copy FFI declarations inline.

First, fetch the FFI bindings:
```bash
curl -o src/zx.rs https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.rs
```

**CRITICAL: ALL resource loading MUST happen in `init()` ONLY!**

```rust
// game/src/lib.rs
#![no_std]

mod zx;  // FFI module - fetched from GitHub, NEVER edit or copy inline
use zx::*;

static mut PLAYER_TEX: u32 = 0;
static mut LEVEL_MESH: u32 = 0;
static mut JUMP_SFX: u32 = 0;

#[no_mangle]
pub extern "C" fn init() {
    // CRITICAL: ALL rom_*() calls MUST be in init() - nowhere else!
    unsafe {
        PLAYER_TEX = rom_texture_str("player");
        LEVEL_MESH = rom_mesh_str("level");
        JUMP_SFX = rom_sound_str("jump");
    }
}

#[no_mangle]
pub extern "C" fn update() {
    // Game logic only - NO resource loading here!
}

#[no_mangle]
pub extern "C" fn render() {
    // Drawing only - NO resource loading here!
}
```

---

## Workflow Commands

```bash
# Full build (generate + compile + pack)
cd game
nether build

# Run game
nether run

# Skip generation (just recompile WASM)
nether build --no-compile
cargo build -p game --target wasm32-unknown-unknown --release
nether pack

# Run generator only (debug)
cargo run -p generator

# Regenerate after git clone
cd game && nether build
```

---

## Key Principles

1. **Generators are native binaries** - they compile for your host OS, not WASM
2. **Build.script chains commands** - run generator THEN WASM compilation
3. **Assets go to disk** - standard formats (PNG, OBJ, WAV) in `assets/` directory
4. **nether.toml declares assets** - `[[assets.*]]` entries reference generated files
5. **ROM functions load assets** - `rom_texture()`, `rom_mesh()`, `rom_sound()`
6. **ALL loading in init()** - Never load resources in update() or render()
7. **Use zx.rs module** - Never copy FFI declarations inline
8. **Generated files are gitignored** - code is source of truth
