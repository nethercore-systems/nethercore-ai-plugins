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
script = "python generator/generate_all.py && cargo build -p game --target wasm32-unknown-unknown --release"
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

### Python Generator Structure (Recommended)

Use a modular Python structure with shared lib/ for all asset types:

```
my-game/
├── generator/
│   ├── lib/                # Shared libraries (scaffold once)
│   │   ├── __init__.py
│   │   ├── texture_buffer.py  # Texture generation helpers
│   │   ├── bpy_utils.py       # Blender mesh utilities
│   │   ├── synthesis.py       # Audio: ADSR, FM, Karplus-Strong
│   │   └── xm_writer.py       # XM file generation
│   ├── textures/           # One .py per texture (~100 lines each)
│   │   ├── wood_plank.py
│   │   └── metal_rust.py
│   ├── meshes/             # One .py per mesh (~100 lines each)
│   │   ├── barrel.py
│   │   └── crate.py
│   ├── sounds/             # One .py per sound (~50 lines each)
│   │   ├── laser.py
│   │   └── coin.py
│   └── generate_all.py     # Runs all generators
├── game/
│   ├── Cargo.toml          # WASM library (cdylib)
│   ├── nether.toml         # Build config
│   └── src/
│       ├── lib.rs          # Game code (compiles to WASM)
│       └── zx.rs           # FFI module (fetch from GitHub)
├── assets/                 # Generated output (gitignored)
│   ├── textures/
│   ├── meshes/
│   └── audio/
└── .gitignore
```

### generate_all.py Pattern

Run all asset generators with a single script:

```python
#!/usr/bin/env python3
"""Generate all assets for the project."""
import subprocess
from pathlib import Path

generator_dir = Path(__file__).parent

# Ensure output directories exist
(generator_dir.parent / "assets/textures").mkdir(parents=True, exist_ok=True)
(generator_dir.parent / "assets/meshes").mkdir(parents=True, exist_ok=True)
(generator_dir.parent / "assets/audio").mkdir(parents=True, exist_ok=True)

# Generate textures (PIL/numpy)
for script in sorted((generator_dir / "textures").glob("*.py")):
    if script.name != "__init__.py":
        print(f"Generating texture: {script.stem}...")
        subprocess.run(["python", str(script)], check=True)

# Generate meshes (Blender bpy)
for script in sorted((generator_dir / "meshes").glob("*.py")):
    if script.name != "__init__.py":
        print(f"Generating mesh: {script.stem}...")
        subprocess.run(["blender", "--background", "--python", str(script)], check=True)

# Generate sounds (numpy/scipy)
for script in sorted((generator_dir / "sounds").glob("*.py")):
    if script.name != "__init__.py":
        print(f"Generating sound: {script.stem}...")
        subprocess.run(["python", str(script)], check=True)

print("All assets generated!")
```

nether.toml runs Python generators before WASM compilation:

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

# Run generators only (debug)
python generator/generate_all.py

# Regenerate after git clone
cd game && nether build
```

---

## Key Principles

1. **Generators are Python scripts** - they run natively on your development machine
2. **Build.script chains commands** - run generator THEN WASM compilation
3. **Assets go to disk** - standard formats (PNG, OBJ, WAV) in `assets/` directory
4. **nether.toml declares assets** - `[[assets.*]]` entries reference generated files
5. **ROM functions load assets** - `rom_texture()`, `rom_mesh()`, `rom_sound()`
6. **ALL loading in init()** - Never load resources in update() or render()
7. **Use zx.rs module** - Never copy FFI declarations inline
8. **Generated files are gitignored** - code is source of truth
