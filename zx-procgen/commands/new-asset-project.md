---
description: Scaffold a new procedural asset generation project with viewer
argument-hint: "[project-name]"
allowed-tools: ["AskUserQuestion", "Write", "Bash", "Read"]
---

# New Asset Generation Project

Create a complete procedural asset generation project with automatic build integration.

## Key Architecture

**IMPORTANT:** Asset generators are **native binaries** that run on your development machine (not WASM). They:
1. Run **before** WASM compilation as part of `nether build`
2. Output to `assets/` directory (standard formats: PNG, OBJ, WAV)
3. Are referenced in `nether.toml` `[[assets.*]]` sections
4. Generated files are **gitignored** (regenerated from code)

This is achieved via the `[build]` section's `script` field which chains commands:
```toml
[build]
script = "cargo run -p generator --release && cargo build --target wasm32-unknown-unknown --release"
```

---

## Step 1: Gather Project Configuration

**If project name argument ($1) is not provided:**

Use AskUserQuestion to ask:

- Question: "What should we name your asset generation project?"
- Header: "Name"
- Options:
  - **my-assets** - Default project name
  - **showcase-assets** - For showcase game assets
  - (User can type a custom name)

## Step 2: Choose Generation Language

Use AskUserQuestion to ask:

- Question: "Which language/tool do you want to use for asset generation?"
- Header: "Language"
- Options:
  - **Rust + proc-gen (Recommended)** - Direct integration with Nethercore proc-gen library, runs as native binary
  - **Python** - NumPy, PIL, audio libraries, great for rapid iteration
  - **Processing/p5.js** - Creative coding, generative art focus
  - **Any tool** - Just create the project structure, you'll add generation code
- multiSelect: false

## Step 3: Choose Asset Types

Use AskUserQuestion to ask:

- Question: "Which asset types will you generate?"
- Header: "Assets"
- Options:
  - **All (textures, meshes, sounds)** - Complete asset generation suite
  - **Textures only** - Focus on procedural textures
  - **Meshes only** - Focus on 3D geometry
  - **Textures + Meshes** - Visual assets without audio
- multiSelect: false

## Step 4: Validate Project Location

Check if the target directory already exists:

```bash
test -d [project-name] && echo "EXISTS" || echo "OK"
```

If directory exists, inform the user and ask them to choose a different name.

## Step 5: Create Project Structure

Based on language choice, create the appropriate structure.

### For Rust Projects

Create this structure:

```
[project-name]/
├── Cargo.toml              # Workspace manifest
├── generator/
━E  ├── Cargo.toml          # Native binary crate (NOT WASM)
━E  └── src/
━E      └── main.rs         # Generation CLI
├── game/
━E  ├── Cargo.toml          # WASM game crate
━E  ├── nether.toml         # Game manifest with build.script
━E  └── src/
━E      └── lib.rs          # Game code (viewer or actual game)
├── assets/                 # Generated assets (gitignored)
━E  ├── meshes/
━E  ├── textures/
━E  └── audio/
├── .gitignore
└── README.md
```

**Cargo.toml (workspace):**
```toml
[workspace]
members = ["generator", "game"]
resolver = "2"
```

**generator/Cargo.toml:**
```toml
[package]
name = "generator"
version = "0.1.0"
edition = "2021"

# This is a NATIVE binary, not WASM
[[bin]]
name = "generator"
path = "src/main.rs"

[dependencies]
proc-gen = { path = "../../nethercore/tools/proc-gen", features = ["wav-export"] }
glam = "0.27"
```

**generator/src/main.rs:**
Create a basic Rust generator that outputs to `../assets/`:

```rust
//! Native asset generator - runs on dev machine, NOT WASM
use proc_gen::prelude::*;
use std::fs;
use std::path::Path;

fn main() {
    let assets_dir = Path::new("../assets");
    fs::create_dir_all(assets_dir.join("textures")).unwrap();
    fs::create_dir_all(assets_dir.join("meshes")).unwrap();
    fs::create_dir_all(assets_dir.join("audio")).unwrap();

    println!("Generating assets...");

    // Generate textures
    generate_textures(assets_dir);

    // Generate meshes
    generate_meshes(assets_dir);

    // Generate sounds
    generate_sounds(assets_dir);

    println!("Assets generated successfully!");
}

fn generate_textures(assets_dir: &Path) {
    // Brown base with Perlin noise variation
    let tex = TextureBuilder::new(256, 256)
        .fill([139, 69, 19, 255])  // Saddle brown base
        .noise(NoiseType::Perlin, 0.03, |base, n| {
            let variation = ((n + 1.0) * 0.5 * 64.0) as u8;
            [
                base[0].saturating_add(variation),
                base[1].saturating_add(variation / 2),
                base[2].saturating_add(variation / 4),
                255,
            ]
        })
        .build();

    tex.save_png(assets_dir.join("textures/example.png")).unwrap();
    println!("  Generated: textures/example.png");
}

fn generate_meshes(assets_dir: &Path) {
    // Simple cube with UVs
    let mesh = MeshBuilder::cube(2.0)
        .with_uvs()
        .build();

    mesh.save_obj(assets_dir.join("meshes/cube.obj")).unwrap();
    println!("  Generated: meshes/cube.obj");
}

fn generate_sounds(assets_dir: &Path) {
    // Coin pickup: ascending arpeggio C5-E5-G5
    let freqs = [523.0, 659.0, 784.0];
    let sample_rate = 22050;

    let audio = AudioBuilder::new(sample_rate)
        .arpeggio(&freqs, 0.08, |t, note_start| {
            // Exponential decay envelope
            (-20.0 * (t - note_start)).exp()
        })
        .normalize(0.9)
        .build();

    audio.save_wav(assets_dir.join("audio/coin.wav")).unwrap();
    println!("  Generated: audio/coin.wav");
}
```

**Note:** If `proc-gen` is not available, you can use standard Rust crates:
- `image` for textures
- `noise` for Perlin noise
- `hound` for WAV export
- Manual OBJ writing for meshes

**game/nether.toml (with build.script chaining):**
```toml
[game]
id = "[project-name]"
title = "[Project Name]"
author = "Developer"
version = "0.1.0"

# Build pipeline: generate assets THEN compile WASM
[build]
script = "cargo run -p generator --release && cargo build -p game --target wasm32-unknown-unknown --release"
wasm = "target/wasm32-unknown-unknown/release/game.wasm"

# Declare generated assets (paths relative to game/ directory)
[[assets.textures]]
id = "example"
path = "../assets/textures/example.png"

[[assets.meshes]]
id = "cube"
path = "../assets/meshes/cube.obj"

[[assets.sounds]]
id = "coin"
path = "../assets/audio/coin.wav"
```

**game/Cargo.toml:**
```toml
[package]
name = "game"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
# No proc-gen dependency - this is WASM code
```

**game/src/lib.rs:**
Create a simple viewer or game that loads assets via ROM functions:

```rust
#[no_mangle]
pub extern "C" fn init() {
    // Load generated assets from ROM (bundled by nether pack)
    let tex = rom_texture(b"example".as_ptr(), 7);
    let mesh = rom_mesh(b"cube".as_ptr(), 4);
    let sound = rom_sound(b"coin".as_ptr(), 4);

    // Store handles for use in render()
}

#[no_mangle]
pub extern "C" fn update() {}

#[no_mangle]
pub extern "C" fn render() {
    // Draw using loaded assets
}
```

### For Python Projects

Create this structure:

```
[project-name]/
├── generate.py            # Main generation script (runs natively)
├── generators/
━E  ├── __init__.py
━E  ├── textures.py        # Texture generators
━E  ├── meshes.py          # Mesh generators (if selected)
━E  └── sounds.py          # Sound generators (if selected)
├── game/
━E  ├── Cargo.toml         # WASM game crate
━E  ├── nether.toml        # With custom build script
━E  └── src/
━E      └── lib.rs
├── assets/                # Generated assets (gitignored)
━E  ├── meshes/
━E  ├── textures/
━E  └── audio/
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

**requirements.txt:**
```
numpy
Pillow
scipy  # for audio
noise  # for Perlin noise
trimesh  # for mesh generation (if selected)
```

**generate.py:**
```python
#!/usr/bin/env python3
"""Generate all assets for the project.

This script runs NATIVELY before WASM compilation.
Run via: python generate.py
Or integrate into nether.toml build.script
"""

import os
from generators import textures, meshes, sounds  # based on selection

def main():
    os.makedirs("assets/textures", exist_ok=True)
    os.makedirs("assets/meshes", exist_ok=True)
    os.makedirs("assets/audio", exist_ok=True)

    print("Generating assets...")

    textures.generate_all()
    meshes.generate_all()  # if selected
    sounds.generate_all()  # if selected

    print("Assets generated! Now run: cd game && nether build")

if __name__ == "__main__":
    main()
```

**game/nether.toml (Python + Rust WASM):**
```toml
[game]
id = "[project-name]"
title = "[Project Name]"
author = "Developer"
version = "0.1.0"

# Build pipeline: Python generates, then Cargo compiles WASM
[build]
script = "python ../generate.py && cargo build --target wasm32-unknown-unknown --release"

[[assets.textures]]
id = "example"
path = "../assets/textures/example.png"
```

### For Processing/p5.js Projects

Create this structure:

```
[project-name]/
├── sketch/
━E  └── sketch.pde         # Processing sketch (runs in Processing IDE)
├── game/
━E  ├── Cargo.toml
━E  ├── nether.toml
━E  └── src/
━E      └── lib.rs
├── assets/                # Output from Processing (gitignored)
━E  ├── meshes/
━E  ├── textures/
━E  └── audio/
├── .gitignore
└── README.md
```

**game/nether.toml:**
```toml
[game]
id = "[project-name]"
title = "[Project Name]"
author = "Developer"
version = "0.1.0"

# Processing generates assets externally, we just compile
# Run Processing sketch manually before: nether build
[build]
script = "cargo build --target wasm32-unknown-unknown --release"

[[assets.textures]]
id = "generated"
path = "../assets/textures/generated.png"
```

### For "Any Tool" Projects

Create minimal structure:

```
[project-name]/
├── game/
━E  ├── Cargo.toml
━E  ├── nether.toml
━E  └── src/
━E      └── lib.rs
├── assets/                # Put generated assets here (gitignored)
━E  ├── meshes/
━E  ├── textures/
━E  └── audio/
├── .gitignore
└── README.md
```

**game/nether.toml:**
```toml
[game]
id = "[project-name]"
title = "[Project Name]"
author = "Developer"
version = "0.1.0"

# Customize this to run your generator before WASM compilation
[build]
script = "./generate.sh && cargo build --target wasm32-unknown-unknown --release"

# Add your generated assets here
# [[assets.textures]]
# id = "my-texture"
# path = "../assets/textures/my-texture.png"
```

## Step 6: Create .gitignore

Create a comprehensive .gitignore that covers all generated content:

```gitignore
# ============================================
# GENERATED ASSETS - Regenerate from source code
# ============================================
# These are procedurally generated and should NOT be committed.
# Run the generator to recreate them.

# All generated asset formats
assets/**/*.png
assets/**/*.jpg
assets/**/*.obj
assets/**/*.gltf
assets/**/*.glb
assets/**/*.wav
assets/**/*.ogg
assets/**/*.xm

# Nethercore binary formats
assets/**/*.nczxmesh
assets/**/*.nczxtex
assets/**/*.nczxsnd
assets/**/*.nczxskel
assets/**/*.nczxanim

# Keep directory structure
!assets/**/
!assets/**/.gitkeep

# ============================================
# BUILD OUTPUTS
# ============================================
/target/
*.nczx

# ============================================
# LANGUAGE-SPECIFIC
# ============================================

# Rust
Cargo.lock

# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
*.egg-info/

# Node.js
node_modules/
dist/
*.log

# Processing
*.class

# ============================================
# EDITOR & OS
# ============================================
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db
```

## Step 7: Create README

Create README.md with clear documentation:

```markdown
# [Project Name]

Procedural asset generation project for Nethercore ZX.

## Architecture

This project uses **native binaries** to generate assets at build time:

```
generator/     ↁENative binary (Rust/Python/etc)
    ↁEruns before WASM compilation
assets/        ↁEGenerated files (PNG, OBJ, WAV)
    ↁEreferenced in nether.toml
game/          ↁEWASM game code
    ↁEbundled into
game.nczx      ↁEFinal ROM file
```

## Quick Start

### One Command Build

From the `game/` directory:
```bash
cd game
nether build
```

This automatically:
1. Runs the generator (via `build.script`)
2. Compiles WASM
3. Bundles assets into `.nczx` ROM

### Run the Game

```bash
nether run
```

## Development Workflow

### Modify Generation Code

1. Edit `generator/src/main.rs` (or Python/etc)
2. Run `nether build` in `game/` - regenerates everything

### Modify Game Code

1. Edit `game/src/lib.rs`
2. Run `nether build --no-compile` to skip regeneration
   OR just run `nether build` (generator is fast)

### Add New Assets

1. Add generation code to `generator/`
2. Add `[[assets.*]]` entry to `game/nether.toml`
3. Load in game via `rom_texture()`, `rom_mesh()`, etc.

## Asset Formats

| Type | Generated Format | ZX Format |
|------|------------------|-----------|
| Textures | PNG (RGBA) | RGBA8 or BC7 |
| Meshes | OBJ/glTF | Packed vertices |
| Sounds | WAV (22050Hz mono) | PCM i16 |

## Files NOT Committed

Generated assets in `assets/` are **gitignored**. They are:
- Regenerated from procedural code
- Bundled into `.nczx` ROM during build
- Deterministic (same code = same output)

To regenerate after cloning:
```bash
cd game && nether build
```
```

## Step 8: Summary

After creating all files, report to the user:

**Project created successfully!**

Show:
- Directory location
- List of files created
- The key insight: generators are native binaries

**For Rust:**
```bash
cd [project-name]/game
nether build        # Runs generator + compiles WASM + packs ROM
nether run          # Build and launch
```

**For Python:**
```bash
cd [project-name]
pip install -r requirements.txt   # One-time setup
cd game
nether build        # Runs generate.py + compiles WASM + packs ROM
```

**For Processing:**
```
1. Open sketch/sketch.pde in Processing
2. Run to generate (saves to assets/)
3. cd game && nether build
```

**Key Points:**
- Generators run **natively** (not WASM) via `nether.toml` `build.script`
- Generated assets are **gitignored** - regenerate with `nether build`
- Assets declared in `[[assets.*]]` are bundled into the final ROM
- Use zx.rs module - fetch from GitHub, NEVER copy FFI inline
- ALL loading in init() - rom_texture(), rom_mesh(), rom_sound() only in init()
