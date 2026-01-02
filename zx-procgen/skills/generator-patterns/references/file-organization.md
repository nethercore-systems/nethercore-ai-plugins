# File Organization for Procedural Generators

This guide establishes the standard file organization pattern for procedural asset generation in Nethercore ZX projects.

## Why Per-Asset Files?

Traditional approaches often put all assets in one large generator file:

```python
# BAD: Everything in one file
def generate_barrel(): ...
def generate_crate(): ...
def generate_chair(): ...
def generate_table(): ...
# 500+ lines, hard to maintain
```

This causes problems:
- LLMs must load entire file to modify one asset
- Changes to one asset risk breaking others
- Merge conflicts when multiple agents work in parallel
- Hard to test individual assets
- File grows unboundedly

## The Per-Asset Pattern

Instead, each asset gets its own file:

```
generation/meshes/
├── barrel.py       # 80 lines
├── crate.py        # 65 lines
├── chair.py        # 120 lines
└── table.py        # 90 lines
```

Benefits:
- **Context efficient**: Load lib/ + one file (~150 lines total)
- **Isolated changes**: Edit barrel.py without touching crate.py
- **Parallel work**: Multiple agents, no conflicts
- **Easy testing**: `python barrel.py` to test one asset
- **Clear inventory**: File list = asset list

## Standard Directory Structure

```
my-game/
├── generation/
│   ├── lib/                      # Shared utilities
│   │   ├── __init__.py           # Re-exports
│   │   ├── bpy_utils.py          # Mesh: clear_scene, export_glb
│   │   ├── texture_buffer.py     # Texture: TextureBuffer class
│   │   ├── sprite_utils.py       # Sprite: palettes, dithering
│   │   └── animation_utils.py    # Animation: keyframes, timing
│   │
│   ├── meshes/                   # One .py per mesh
│   │   ├── barrel.py
│   │   ├── crate.py
│   │   ├── chair.py
│   │   └── table.py
│   │
│   ├── textures/                 # One .py per texture
│   │   ├── wood_plank.py
│   │   ├── metal_brushed.py
│   │   ├── stone_cobble.py
│   │   └── brick_wall.py
│   │
│   ├── sprites/                  # One .py per sprite/sheet
│   │   ├── player_idle.py
│   │   ├── player_walk.py
│   │   ├── enemy_slime.py
│   │   └── ui_buttons.py
│   │
│   ├── animations/               # One .py per animation
│   │   ├── walk_cycle.py
│   │   ├── run_cycle.py
│   │   └── attack_slash.py
│   │
│   └── generate_all.py           # Batch runner
│
├── generated/                    # Generated output
│   ├── meshes/
│   │   ├── barrel.glb
│   │   └── crate.glb
│   ├── textures/
│   │   ├── wood_plank_albedo.png
│   │   └── wood_plank_mre.png
│   ├── sprites/
│   │   └── player_idle.png
│   └── animations/
│       └── walk_cycle.glb
│
└── nether.toml
```

## Asset File Template

Each asset file should follow this structure:

```python
#!/usr/bin/env python3
"""Generate [asset description].

Output: ../generated/[type]/[name].[ext]
"""
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from [relevant_lib] import [helpers]

# Configuration
OUTPUT_DIR = Path(__file__).parent.parent.parent / "generated" / "[type]"
OUTPUT_NAME = "[asset_name]"

def generate():
    """Generate the asset."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Asset-specific generation logic here

    output_path = OUTPUT_DIR / f"{OUTPUT_NAME}.[ext]"
    # Save asset
    print(f"Generated: {output_path}")
    return output_path

if __name__ == "__main__":
    generate()
```

## Mesh File Example

```python
#!/usr/bin/env python3
"""Generate wooden barrel mesh.

Output: ../generated/meshes/barrel.glb
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from bpy_utils import clear_scene, export_glb, apply_modifiers
import bpy

OUTPUT_DIR = Path(__file__).parent.parent.parent / "generated" / "meshes"
OUTPUT_NAME = "barrel"

def generate():
    """Generate barrel mesh."""
    clear_scene()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Create cylinder body
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.4, depth=1.0, vertices=12
    )
    barrel = bpy.context.active_object
    barrel.name = "Barrel"

    # Add bevel for rounded edges
    bevel = barrel.modifiers.new("Bevel", 'BEVEL')
    bevel.width = 0.02
    bevel.segments = 2

    apply_modifiers(barrel)

    output_path = OUTPUT_DIR / f"{OUTPUT_NAME}.glb"
    export_glb(str(output_path))
    print(f"Generated: {output_path}")
    return output_path

if __name__ == "__main__":
    generate()
```

## Texture File Example

```python
#!/usr/bin/env python3
"""Generate wood plank texture.

Output: ../generated/textures/wood_plank_albedo.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from texture_buffer import TextureBuffer

OUTPUT_DIR = Path(__file__).parent.parent.parent / "generated" / "textures"
OUTPUT_NAME = "wood_plank"

def generate():
    """Generate wood plank textures."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    buf = TextureBuffer(256, 256)

    # Base wood color
    buf.fill((139, 90, 43, 255))

    # Add grain noise
    buf.add_perlin_noise(
        scale=0.05, intensity=30, seed=42,
        blend_mode='add'
    )

    # Add horizontal lines for planks
    for y in range(0, 256, 32):
        buf.draw_line(0, y, 255, y, (80, 50, 25, 255), width=2)

    output_path = OUTPUT_DIR / f"{OUTPUT_NAME}_albedo.png"
    buf.save(str(output_path))
    print(f"Generated: {output_path}")
    return output_path

if __name__ == "__main__":
    generate()
```

## Batch Runner (generate_all.py)

```python
#!/usr/bin/env python3
"""Run all procedural generators.

Usage:
    python generate_all.py           # Generate all
    python generate_all.py meshes    # Generate meshes only
    python generate_all.py textures  # Generate textures only
"""
import subprocess
import sys
from pathlib import Path

# Map folder to runner command
RUNNERS = {
    "meshes": ["blender", "--background", "--python"],
    "textures": ["python"],
    "sprites": ["python"],
    "animations": ["blender", "--background", "--python"],
}

def run_generators(folder: str, runner: list[str]):
    """Run all generators in a folder."""
    folder_path = Path(__file__).parent / folder
    if not folder_path.exists():
        return

    for file in sorted(folder_path.glob("*.py")):
        if file.name.startswith("_"):
            continue
        print(f"\n{'='*60}")
        print(f"Generating: {folder}/{file.name}")
        print('='*60)

        cmd = runner + [str(file)]
        result = subprocess.run(cmd, capture_output=False)

        if result.returncode != 0:
            print(f"FAILED: {file.name}")
            sys.exit(1)

def main():
    # Parse arguments
    if len(sys.argv) > 1:
        folders = sys.argv[1:]
    else:
        folders = list(RUNNERS.keys())

    # Run generators
    for folder in folders:
        if folder not in RUNNERS:
            print(f"Unknown folder: {folder}")
            continue
        run_generators(folder, RUNNERS[folder])

    print("\n" + "="*60)
    print("All generators completed successfully!")
    print("="*60)

if __name__ == "__main__":
    main()
```

## Integration with nether.toml

Add generators to your build pipeline:

```toml
[build]
pre_build = [
    "python generation/generate_all.py"
]

# Or run specific types
[build.assets]
meshes = "python generation/generate_all.py meshes"
textures = "python generation/generate_all.py textures"
```

## File Size Guidelines

| Limit | Lines | Action |
|-------|-------|--------|
| Target | ≤150 | Ideal for single asset |
| Soft | 200 | Consider extracting to lib/ |
| Hard | 300 | MUST split or refactor |

When a file exceeds limits:
1. Extract reusable helpers to `lib/`
2. Split complex assets into base + variants
3. Use parameterized functions for similar assets

## Naming Conventions

| Type | File Pattern | Output Pattern |
|------|--------------|----------------|
| Mesh | `barrel.py` | `barrel.glb` |
| Texture | `wood_plank.py` | `wood_plank_albedo.png`, `wood_plank_mre.png` |
| Sprite | `player_idle.py` | `player_idle.png` |
| Animation | `walk_cycle.py` | `walk_cycle.glb` or applied to mesh |

Use snake_case for all file names. Use descriptive names that indicate what the asset is.

## Handling Variants

For assets with variations (e.g., barrel_small, barrel_large):

Option 1: Separate files
```
meshes/
├── barrel_small.py
├── barrel_medium.py
└── barrel_large.py
```

Option 2: Parameterized single file
```python
# barrel.py
def generate(size='medium'):
    scales = {'small': 0.5, 'medium': 1.0, 'large': 1.5}
    # Use scales[size] in generation

if __name__ == "__main__":
    for size in ['small', 'medium', 'large']:
        generate(size)
```

Prefer separate files unless variations share 80%+ code.
