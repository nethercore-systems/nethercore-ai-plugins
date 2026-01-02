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
  - **Python (Recommended)** - PIL/NumPy for textures, Blender bpy for meshes, scipy for audio
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

### For Python Projects (Recommended)

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
pyfastnoiselite  # for Perlin/Simplex noise
scipy  # for audio
soundfile  # for WAV export
# For mesh generation, use Blender bpy (system install, not pip)
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

This project uses **Python scripts** to generate assets at build time:

```
generator/     ↁE Python scripts (PIL, Blender bpy, numpy/scipy)
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

1. Edit Python scripts in `generator/` (textures.py, meshes.py, sounds.py)
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
- The key insight: generators are Python scripts that run natively

**For Python (Recommended):**
```bash
cd [project-name]
pip install -r requirements.txt   # One-time setup
cd game
nether build        # Runs generate.py + compiles WASM + packs ROM
nether run          # Build and launch
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
