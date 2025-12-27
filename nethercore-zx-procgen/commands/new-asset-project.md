---
description: Scaffold a new procedural asset generation project with viewer
argument-hint: "[project-name]"
allowed-tools: ["AskUserQuestion", "Write", "Bash", "Read"]
---

# New Asset Generation Project

Create a complete procedural asset generation project with a ZX viewer for previewing assets in-engine.

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
  - **Rust + proc-gen (Recommended)** - Direct integration with Nethercore proc-gen library
  - **Python** - NumPy, PIL, audio libraries, great for rapid iteration
  - **Processing/p5.js** - Creative coding, generative art focus
  - **Any tool** - Just create the project structure, you'll add generation code

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
│   ├── Cargo.toml          # Generator crate
│   └── src/
│       └── main.rs         # Generation CLI
├── viewer/
│   ├── Cargo.toml          # ZX viewer game
│   ├── nether.toml         # Game manifest
│   └── src/
│       └── lib.rs          # Viewer with orbit camera
├── assets/                 # Generated assets (add to .gitignore)
│   ├── meshes/
│   ├── textures/
│   └── audio/
├── .gitignore
└── README.md
```

**Cargo.toml (workspace):**
```toml
[workspace]
members = ["generator", "viewer"]
resolver = "2"
```

**generator/Cargo.toml:**
```toml
[package]
name = "generator"
version = "0.1.0"
edition = "2021"

[dependencies]
proc-gen = { path = "../../nethercore/tools/proc-gen", features = ["wav-export"] }
glam = "0.27"
```

**generator/src/main.rs:**
Create a basic generator with functions for each selected asset type.

**viewer/nether.toml:**
```toml
[game]
id = "[project-name]-viewer"
title = "[Project Name] Asset Viewer"
author = "Developer"
version = "0.1.0"

# Assets will be added as they're generated
```

**viewer/src/lib.rs:**
Create a simple orbit camera viewer using the proc-gen-common macro pattern.

### For Python Projects

Create this structure:

```
[project-name]/
├── generate.py            # Main generation script
├── generators/
│   ├── __init__.py
│   ├── textures.py        # Texture generators
│   ├── meshes.py          # Mesh generators (if selected)
│   └── sounds.py          # Sound generators (if selected)
├── viewer/
│   ├── Cargo.toml         # ZX viewer game
│   ├── nether.toml
│   └── src/
│       └── lib.rs
├── assets/
│   ├── meshes/
│   ├── textures/
│   └── audio/
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
"""Generate all assets for the project."""

import os
from generators import textures, meshes, sounds  # based on selection

def main():
    os.makedirs("assets/textures", exist_ok=True)
    os.makedirs("assets/meshes", exist_ok=True)
    os.makedirs("assets/audio", exist_ok=True)

    print("Generating textures...")
    textures.generate_all()

    # Add mesh/sound generation based on selection

    print("Done! Run 'nether run viewer' to preview.")

if __name__ == "__main__":
    main()
```

### For Processing/p5.js Projects

Create this structure:

```
[project-name]/
├── sketch/
│   └── sketch.pde         # Processing sketch
├── viewer/
│   ├── Cargo.toml
│   ├── nether.toml
│   └── src/
│       └── lib.rs
├── assets/
│   ├── meshes/
│   ├── textures/
│   └── audio/
├── .gitignore
└── README.md
```

### For "Any Tool" Projects

Create minimal structure:

```
[project-name]/
├── viewer/
│   ├── Cargo.toml
│   ├── nether.toml
│   └── src/
│       └── lib.rs
├── assets/
│   ├── meshes/
│   ├── textures/
│   └── audio/
├── .gitignore
└── README.md
```

## Step 6: Create .gitignore

```
# Generated assets
assets/meshes/*.obj
assets/textures/*.png
assets/audio/*.wav

# Build outputs
/target
*.nczx

# Python
__pycache__/
*.pyc
.venv/

# Editor
.vscode/
.idea/
```

## Step 7: Create README

Create README.md with:
- Project description
- Generation instructions based on language
- How to run the viewer
- Asset format notes

## Step 8: Summary

After creating all files, report to the user:

**Project created successfully!**

Show:
- Directory location
- List of files created
- Language-specific next steps

**For Rust:**
```bash
cd [project-name]
cargo run -p generator      # Generate assets
nether run viewer           # Preview in ZX
```

**For Python:**
```bash
cd [project-name]
pip install -r requirements.txt
python generate.py          # Generate assets
nether run viewer           # Preview in ZX
```

**For Processing:**
```
1. Open sketch/sketch.pde in Processing
2. Run to generate (saves to assets/)
3. nether run viewer to preview
```

Tell them:
- Generated assets go to `assets/` directory
- The viewer auto-loads assets from `nether.toml`
- They can ask about specific procedural generation techniques
- Reference the proc-gen library at `nethercore/tools/proc-gen/` for patterns
