---
description: Initialize procgen spec-driven workflow infrastructure with zero-token file copying
argument-hint: "[asset-types: textures|sounds|characters|animations|normals|all] [project-dir]"
allowed-tools: ["Bash", "Write", "Glob", "AskUserQuestion"]
color: blue
---

# Init Procgen Infrastructure

Copies parser files directly using native OS commands instead of reading them into context.

## Step 1: Parse Asset Types

**If asset-types argument ($1) is provided:**
- Split by comma: "textures,sounds" → ["textures", "sounds"]
- Convert "all" → ["textures", "sounds", "characters", "animations", "normals"]

**If not provided:**
- Use AskUserQuestion to ask:
  - Question: "Which asset types should we set up?"
  - Header: "Asset Types"
  - Options:
    - **All (Recommended)** - Full suite (textures, sounds, characters, animations, normals)
    - **Textures + Sounds** - Common combination for games
    - **Textures only** - Layer-based procedural textures
    - **Sounds only** - SFX and instrument synthesis
  - multiSelect: false

Parse the result into an array of asset types.

## Step 2: Determine Project Directory

**If project-dir argument ($2) is provided:**
- Use it as the target directory
- Create it if it doesn't exist: `mkdir -p "$2"`

**If not provided:**
- Use current directory (`.`)
- Validate it looks like a project directory (has common files or is empty)

## Step 3: Validate Plugin Root

Check that `CLAUDE_PLUGIN_ROOT` environment variable exists:

```bash
if [ -z "$CLAUDE_PLUGIN_ROOT" ]; then
  echo "❌ Error: CLAUDE_PLUGIN_ROOT not set"
  echo "This command requires the zx-procgen plugin to be installed."
  exit 1
fi
```

On Windows, use:
```cmd
if not defined CLAUDE_PLUGIN_ROOT (
  echo ❌ Error: CLAUDE_PLUGIN_ROOT not set
  echo This command requires the zx-procgen plugin to be installed.
  exit /b 1
)
```

## Step 4: Create Directory Structure

Create all necessary directories:

```bash
mkdir -p lib
mkdir -p specs/textures
mkdir -p specs/sounds
mkdir -p specs/characters
mkdir -p specs/animations
mkdir -p specs/normals
mkdir -p generated/textures
mkdir -p generated/sounds
mkdir -p generated/characters
mkdir -p generated/animations
mkdir -p generated/normals
```

On Windows:
```cmd
mkdir lib 2>nul
mkdir specs\textures 2>nul
mkdir specs\sounds 2>nul
mkdir specs\characters 2>nul
mkdir specs\animations 2>nul
mkdir specs\normals 2>nul
mkdir generated\textures 2>nul
mkdir generated\sounds 2>nul
mkdir generated\characters 2>nul
mkdir generated\animations 2>nul
mkdir generated\normals 2>nul
```

## Step 5: Copy Parsers (Zero Tokens)

Use native OS commands to copy parser files directly from plugin references to `lib/`.

**Detect platform:**

```bash
# Unix/macOS/Linux detection
case "$OSTYPE" in
  linux*|darwin*|*bsd*)
    IS_UNIX=true
    ;;
  msys*|mingw*|cygwin*|win32)
    IS_UNIX=false
    ;;
esac
```

**Build copy commands based on selected asset types:**

| Asset Type | Source File |
|------------|-------------|
| textures | `procedural-textures/references/texture_parser.py` |
| sounds | `procedural-sounds/references/sound_parser.py` |
| characters | `procedural-characters/references/character_parser.py` |
| animations | `procedural-animations/references/motion_parser.py` |
| normals | `procedural-normal-maps/references/normal_parser.py` |

**Unix/macOS copy commands:**

```bash
if [ "$IS_UNIX" = true ]; then
  # Copy parsers based on selected types
  if [[ " ${ASSET_TYPES[@]} " =~ " textures " ]]; then
    cp "$CLAUDE_PLUGIN_ROOT/zx-procgen/skills/procedural-textures/references/texture_parser.py" lib/
  fi

  if [[ " ${ASSET_TYPES[@]} " =~ " sounds " ]]; then
    cp "$CLAUDE_PLUGIN_ROOT/zx-procgen/skills/procedural-sounds/references/sound_parser.py" lib/
  fi

  if [[ " ${ASSET_TYPES[@]} " =~ " characters " ]]; then
    cp "$CLAUDE_PLUGIN_ROOT/zx-procgen/skills/procedural-characters/references/character_parser.py" lib/
  fi

  if [[ " ${ASSET_TYPES[@]} " =~ " animations " ]]; then
    cp "$CLAUDE_PLUGIN_ROOT/zx-procgen/skills/procedural-animations/references/motion_parser.py" lib/
  fi

  if [[ " ${ASSET_TYPES[@]} " =~ " normals " ]]; then
    cp "$CLAUDE_PLUGIN_ROOT/zx-procgen/skills/procedural-normal-maps/references/normal_parser.py" lib/
  fi
fi
```

**Windows copy commands:**

```cmd
if [ "$IS_UNIX" = false ]; then
  # Copy parsers based on selected types (Windows)
  for TYPE in textures sounds characters animations normals; do
    case $TYPE in
      textures)
        xcopy /Y "%CLAUDE_PLUGIN_ROOT%\zx-procgen\skills\procedural-textures\references\texture_parser.py" lib\
        ;;
      sounds)
        xcopy /Y "%CLAUDE_PLUGIN_ROOT%\zx-procgen\skills\procedural-sounds\references\sound_parser.py" lib\
        ;;
      characters)
        xcopy /Y "%CLAUDE_PLUGIN_ROOT%\zx-procgen\skills\procedural-characters\references\character_parser.py" lib\
        ;;
      animations)
        xcopy /Y "%CLAUDE_PLUGIN_ROOT%\zx-procgen\skills\procedural-animations\references\motion_parser.py" lib\
        ;;
      normals)
        xcopy /Y "%CLAUDE_PLUGIN_ROOT%\zx-procgen\skills\procedural-normal-maps\references\normal_parser.py" lib\
        ;;
    esac
  done
fi
```

**Simplified cross-platform approach (Recommended):**

Since Claude Code runs in a Unix-like shell on all platforms, use Unix commands:

```bash
# Textures
cp "$CLAUDE_PLUGIN_ROOT/zx-procgen/skills/procedural-textures/references/texture_parser.py" lib/ 2>/dev/null

# Sounds
cp "$CLAUDE_PLUGIN_ROOT/zx-procgen/skills/procedural-sounds/references/sound_parser.py" lib/ 2>/dev/null

# Characters
cp "$CLAUDE_PLUGIN_ROOT/zx-procgen/skills/procedural-characters/references/character_parser.py" lib/ 2>/dev/null

# Animations
cp "$CLAUDE_PLUGIN_ROOT/zx-procgen/skills/procedural-animations/references/motion_parser.py" lib/ 2>/dev/null

# Normals
cp "$CLAUDE_PLUGIN_ROOT/zx-procgen/skills/procedural-normal-maps/references/normal_parser.py" lib/ 2>/dev/null
```

Only copy the files for selected asset types. Redirect errors to /dev/null for clean output.

## Step 6: Validate Copies

Count copied files to ensure success:

```bash
COPIED_COUNT=$(ls -1 lib/*.py 2>/dev/null | wc -l)
echo "✅ Successfully copied $COPIED_COUNT parser(s) to lib/"
```

If count is 0, report error:
```bash
if [ "$COPIED_COUNT" -eq 0 ]; then
  echo "❌ Error: No parsers were copied. Check CLAUDE_PLUGIN_ROOT path."
  exit 1
fi
```

## Step 7: Create Example Specs (Small Files - OK to Use Write)

Create minimal example spec files for each selected asset type.

### Texture Example (`specs/textures/stone.texture.spec.py`)

```python
# Procedural stone texture specification
# Edit this to customize the texture parameters

TEXTURE = {
    'texture': {
        'name': 'stone',
        'size': [256, 256],
        'layers': [
            {
                'type': 'noise',
                'noise_type': 'perlin',
                'scale': 0.05,
                'octaves': 4,
                'blend': 'normal',
                'opacity': 1.0,
            },
            {
                'type': 'noise',
                'noise_type': 'voronoi',
                'scale': 0.1,
                'blend': 'overlay',
                'opacity': 0.3,
            },
        ],
        'color_ramp': ['#3A3A3A', '#5A5A5A', '#7A7A7A'],
    }
}
```

### Sound Example (`specs/sounds/laser.spec.py`)

```python
# Procedural laser sound specification
# Edit this to customize the sound parameters

SOUND = {
    'sound': {
        'name': 'laser',
        'duration': 0.3,
        'sample_rate': 22050,
        'layers': [
            {
                'type': 'sine',
                'freq': 800,
                'freq_end': 200,
                'amplitude': 0.8,
                'duration': 0.3,
            },
        ],
        'envelope': {
            'attack': 0.01,
            'decay': 0.1,
            'sustain': 0.5,
            'release': 0.2,
        },
        'normalize': True,
    }
}
```

### Character Example (`specs/characters/player.spec.py`)

```python
# Procedural character mesh specification
# Edit this to customize the character design

SPEC = {
    'character': {
        'name': 'player',
        'tri_budget': 500,
        'skeleton': [
            {'bone': 'root', 'head': [0, 0, 0], 'tail': [0, 0, 0.5]},
            {'bone': 'spine', 'parent': 'root', 'head': [0, 0, 0.5], 'tail': [0, 0, 1.2]},
            {'bone': 'head', 'parent': 'spine', 'head': [0, 0, 1.2], 'tail': [0, 0, 1.5]},
        ],
        'parts': {
            'torso': {
                'bone': 'spine',
                'base': 'hexagon(6)',
                'base_radius': 0.15,
                'steps': [
                    {'extrude': 0.7, 'scale': 1.0},
                ],
            },
        },
        'texturing': {'uv_mode': 'smart_project'},
    }
}
```

### Animation Example (`specs/animations/walk.motion.py`)

```python
# Procedural animation specification for Blender
# Edit this to customize the motion parameters

MOTION = {
    'motion': {
        'name': 'walk',
        'fps': 24,
        'duration': 1.0,
        'style': 'walk',
        'params': {
            'speed': 1.0,
            'stride_length': 0.8,
            'bounce': 0.05,
        },
    }
}
```

### Normal Map Example (`specs/normals/brick.normal.spec.py`)

```python
# Procedural normal map specification
# Edit this to customize the normal map parameters

NORMAL = {
    'normal': {
        'name': 'brick',
        'size': [512, 512],
        'height_source': {
            'type': 'noise',
            'noise_type': 'perlin',
            'scale': 0.02,
            'octaves': 4,
        },
        'strength': 1.0,
    }
}
```

Use the Write tool to create these example files for each selected asset type.

## Step 8: Create Generator Script

Create `generate_specs.py` wrapper that uses the parsers:

```python
#!/usr/bin/env python3
"""Generate assets from spec files using parsers."""

import os
import sys
from pathlib import Path

# Add lib to path so we can import parsers
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

def generate_textures():
    """Generate textures from specs/textures/*.texture.spec.py"""
    try:
        from texture_parser import load_spec, generate_texture, write_png
    except ImportError:
        print("⚠️ Skipping textures (texture_parser.py not in lib/)")
        return

    specs_dir = Path('specs/textures')
    output_dir = Path('generated/textures')
    output_dir.mkdir(parents=True, exist_ok=True)

    spec_files = list(specs_dir.glob('*.texture.spec.py'))
    if not spec_files:
        print("ℹ️ No texture specs found in specs/textures/")
        return

    print(f"\n=== Generating {len(spec_files)} texture(s) ===")
    for spec_file in spec_files:
        print(f"  {spec_file.stem}...", end=' ')
        try:
            spec = load_spec(spec_file)
            result = generate_texture(spec)
            name = spec_file.stem.replace('.texture.spec', '')
            output_path = output_dir / f"{name}.png"
            write_png(str(output_path), result)
            print(f"✅ → {output_path}")
        except Exception as e:
            print(f"❌ Error: {e}")

def generate_sounds():
    """Generate sounds from specs/sounds/*.spec.py"""
    try:
        from sound_parser import load_spec, generate_sfx, write_wav
    except ImportError:
        print("⚠️ Skipping sounds (sound_parser.py not in lib/)")
        return

    specs_dir = Path('specs/sounds')
    output_dir = Path('generated/sounds')
    output_dir.mkdir(parents=True, exist_ok=True)

    spec_files = list(specs_dir.glob('*.spec.py'))
    if not spec_files:
        print("ℹ️ No sound specs found in specs/sounds/")
        return

    print(f"\n=== Generating {len(spec_files)} sound(s) ===")
    for spec_file in spec_files:
        print(f"  {spec_file.stem}...", end=' ')
        try:
            spec = load_spec(spec_file)
            signal = generate_sfx(spec)
            name = spec_file.stem.replace('.spec', '')
            output_path = output_dir / f"{name}.wav"
            write_wav(str(output_path), signal, spec.get('sound', {}).get('sample_rate', 22050))
            print(f"✅ → {output_path}")
        except Exception as e:
            print(f"❌ Error: {e}")

def generate_characters():
    """Generate characters from specs/characters/*.spec.py"""
    try:
        from character_parser import load_spec, generate_character, write_mesh
    except ImportError:
        print("⚠️ Skipping characters (character_parser.py not in lib/)")
        return

    specs_dir = Path('specs/characters')
    output_dir = Path('generated/characters')
    output_dir.mkdir(parents=True, exist_ok=True)

    spec_files = list(specs_dir.glob('*.spec.py'))
    if not spec_files:
        print("ℹ️ No character specs found in specs/characters/")
        return

    print(f"\n=== Generating {len(spec_files)} character(s) ===")
    for spec_file in spec_files:
        print(f"  {spec_file.stem}...", end=' ')
        try:
            spec = load_spec(spec_file)
            mesh_data = generate_character(spec)
            name = spec_file.stem.replace('.spec', '')
            output_path = output_dir / f"{name}.nczxmesh"
            write_mesh(str(output_path), mesh_data)
            print(f"✅ → {output_path}")
        except Exception as e:
            print(f"❌ Error: {e}")

def generate_animations():
    """Generate animations from specs/animations/*.motion.py"""
    try:
        from motion_parser import load_motion_spec, generate_animation
    except ImportError:
        print("⚠️ Skipping animations (motion_parser.py not in lib/)")
        return

    specs_dir = Path('specs/animations')
    output_dir = Path('generated/animations')
    output_dir.mkdir(parents=True, exist_ok=True)

    spec_files = list(specs_dir.glob('*.motion.py'))
    if not spec_files:
        print("ℹ️ No animation specs found in specs/animations/")
        return

    print(f"\n=== Generating {len(spec_files)} animation(s) ===")
    for spec_file in spec_files:
        print(f"  {spec_file.stem}...", end=' ')
        try:
            spec = load_motion_spec(spec_file)
            name = spec_file.stem.replace('.motion', '')
            output_path = output_dir / f"{name}.blend"
            generate_animation(spec, str(output_path))
            print(f"✅ → {output_path}")
        except Exception as e:
            print(f"❌ Error: {e}")

def generate_normals():
    """Generate normal maps from specs/normals/*.normal.spec.py"""
    try:
        from normal_parser import load_spec, generate_normal_map, write_png
    except ImportError:
        print("⚠️ Skipping normals (normal_parser.py not in lib/)")
        return

    specs_dir = Path('specs/normals')
    output_dir = Path('generated/normals')
    output_dir.mkdir(parents=True, exist_ok=True)

    spec_files = list(specs_dir.glob('*.normal.spec.py'))
    if not spec_files:
        print("ℹ️ No normal map specs found in specs/normals/")
        return

    print(f"\n=== Generating {len(spec_files)} normal map(s) ===")
    for spec_file in spec_files:
        print(f"  {spec_file.stem}...", end=' ')
        try:
            spec = load_spec(spec_file)
            result = generate_normal_map(spec)
            name = spec_file.stem.replace('.normal.spec', '')
            output_path = output_dir / f"{name}.png"
            write_png(str(output_path), result)
            print(f"✅ → {output_path}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("╔════════════════════════════════════════════╗")
    print("║   Nethercore ZX Procgen Asset Generator   ║")
    print("║        Spec-Driven Workflow (v2.0)        ║")
    print("╚════════════════════════════════════════════╝")

    generate_textures()
    generate_sounds()
    generate_characters()
    generate_animations()
    generate_normals()

    print("\n✨ Generation complete!")
    print("\nNext steps:")
    print("  1. Review generated assets in generated/ directory")
    print("  2. Edit specs in specs/ to customize")
    print("  3. Run this script again to regenerate")
```

Use the Write tool to create `generate_specs.py`.

## Step 9: Create .gitignore

Create `.gitignore` for the project:

```
# Generated assets (regenerate from specs)
generated/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Virtual environments
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

## Step 10: Report Success

After all steps complete, report to the user:

```
✅ Procgen infrastructure initialized successfully!

📦 Copied parsers to lib/:
  - texture_parser.py (658 lines)
  - sound_parser.py (804 lines)
  - character_parser.py (720 lines)
  - motion_parser.py (341 lines)
  - normal_parser.py (571 lines)

📝 Created example specs in specs/:
  - textures/stone.texture.spec.py
  - sounds/laser.spec.py
  - characters/player.spec.py
  - animations/walk.motion.py
  - normals/brick.normal.spec.py

🔧 Created generator script: generate_specs.py

Next steps:
  1. Edit specs in specs/ to customize your assets
  2. Run: python generate_specs.py
  3. Check generated/ directory for output assets
  4. Integrate assets into your game

Need help?
  - /generate-all - Run generator and handle errors
  - /migrate-to-specs - Convert existing inline generators
  - /improve-assets - Quality improvement workflow
```

Include actual counts based on what was set up (e.g., if only textures+sounds, show only those 2 parsers).

## Edge Cases

### Plugin Not Installed
If `CLAUDE_PLUGIN_ROOT` is not set:
```
❌ Error: zx-procgen plugin not found

The CLAUDE_PLUGIN_ROOT environment variable is not set. This means
the zx-procgen plugin is not installed or not loaded.

To install:
  1. Add nethercore-ai-plugins to your Claude Code settings
  2. Enable the zx-procgen plugin
  3. Restart Claude Code

See: https://github.com/nethercore-systems/nethercore-ai-plugins
```

### Parser Files Missing
If source parser files don't exist:
```
❌ Error: Parser file not found

Expected: $CLAUDE_PLUGIN_ROOT/zx-procgen/skills/procedural-textures/references/texture_parser.py
Found: (file does not exist)

This may indicate:
  - Plugin is outdated (update to latest version)
  - Plugin installation is corrupted (reinstall)
  - Wrong CLAUDE_PLUGIN_ROOT path
```

### Permission Errors
If cannot write to lib/:
```
❌ Error: Permission denied writing to lib/

Check:
  - Do you have write permissions in this directory?
  - Is lib/ owned by another user?
  - Are you running in a read-only filesystem?

Try:
  - Run with appropriate permissions
  - Choose a different project directory
```

### Existing Files
If `lib/` already contains parser files:
```
⚠️ Warning: lib/ directory already contains parser files

Found:
  - lib/texture_parser.py
  - lib/sound_parser.py

These will be overwritten. Continue? [y/N]
```

Use AskUserQuestion with:
- Question: "lib/ already contains parser files. Overwrite?"
- Options: ["Yes, overwrite", "No, skip existing files", "Abort setup"]

