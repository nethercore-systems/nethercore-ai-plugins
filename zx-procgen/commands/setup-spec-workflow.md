---
description: Add spec-driven workflow infrastructure to an existing project
argument-hint: "[asset-type: textures|sounds|characters|animations|normals|all]"
allowed-tools: ["Read", "Write", "Glob", "Bash", "AskUserQuestion"]
---

# Setup Spec Workflow

Add spec-driven procedural generation infrastructure to an existing project. This sets up the parser files and creates example specs so you can use the declarative spec format instead of inline Python code.

## Why Spec-Driven?

| Aspect | Old Inline Style | New Spec Style |
|--------|------------------|----------------|
| Config | Hardcoded in Python | Separate `.spec.py` files |
| Reuse | Copy-paste | Parser handles all specs |
| Iteration | Edit Python logic | Edit just parameters |
| AI-friendly | Generate full code | Generate just config |

## Step 1: Determine Asset Types

**If asset-type argument ($1) is not provided:**

Use AskUserQuestion to ask:

- Question: "Which asset types should we set up for spec-driven generation?"
- Header: "Assets"
- Options:
  - **All** - Full suite (textures, sounds, characters, animations, normals)
  - **Textures** - Layer-based procedural textures
  - **Sounds** - SFX and instrument synthesis
  - **Characters** - Mesh generation with rigs
  - **Animations** - Motion specs for Blender
- multiSelect: true

## Step 2: Check Project Structure

Look for existing generation infrastructure:

```bash
ls -la generation/ 2>/dev/null || echo "No generation/ directory"
ls -la lib/ 2>/dev/null || echo "No lib/ directory"
```

## Step 3: Create Lib Directory

Create `lib/` directory for parsers if it doesn't exist:

```
project/
├── lib/                    # Shared parser infrastructure
│   ├── texture_parser.py
│   ├── sound_parser.py
│   ├── character_parser.py
│   ├── motion_parser.py
│   └── normal_parser.py
├── specs/                  # Asset specifications
│   ├── textures/
│   │   └── example.texture.spec.py
│   ├── sounds/
│   │   └── example.spec.py
│   └── ...
└── generated/              # Output directory
```

## Step 4: Copy Parsers

For each selected asset type, copy the parser from the plugin's references:

| Asset Type | Parser Source |
|------------|---------------|
| Textures | `zx-procgen/skills/procedural-textures/references/texture_parser.py` |
| Sounds | `zx-procgen/skills/procedural-sounds/references/sound_parser.py` |
| Characters | `zx-procgen/skills/procedural-characters/references/character_parser.py` |
| Animations | `zx-procgen/skills/procedural-animations/references/motion_parser.py` |
| Normals | `zx-procgen/skills/procedural-normal-maps/references/normal_parser.py` |

Read each parser file and write it to the project's `lib/` directory.

## Step 5: Create Example Specs

For each selected asset type, create an example `.spec.py` file:

### Texture Example (`specs/textures/stone.texture.spec.py`)

```python
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

## Step 6: Create Generator Script

Create `generate_specs.py` that uses the parsers:

```python
#!/usr/bin/env python3
"""Generate assets from spec files using parsers."""

import os
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

def generate_textures():
    from texture_parser import load_spec, generate_texture, write_png

    specs_dir = Path('specs/textures')
    output_dir = Path('generated/textures')
    output_dir.mkdir(parents=True, exist_ok=True)

    for spec_file in specs_dir.glob('*.texture.spec.py'):
        print(f"Generating {spec_file.stem}...")
        spec = load_spec(spec_file)
        result = generate_texture(spec)
        output_path = output_dir / f"{spec_file.stem.replace('.texture.spec', '')}.png"
        write_png(str(output_path), result)
        print(f"  → {output_path}")

def generate_sounds():
    from sound_parser import load_spec, generate_sfx, write_wav

    specs_dir = Path('specs/sounds')
    output_dir = Path('generated/sounds')
    output_dir.mkdir(parents=True, exist_ok=True)

    for spec_file in specs_dir.glob('*.spec.py'):
        print(f"Generating {spec_file.stem}...")
        spec = load_spec(spec_file)
        signal = generate_sfx(spec)
        output_path = output_dir / f"{spec_file.stem.replace('.spec', '')}.wav"
        write_wav(str(output_path), signal)
        print(f"  → {output_path}")

if __name__ == '__main__':
    print("=== Generating from specs ===")
    generate_textures()
    generate_sounds()
    print("Done!")
```

## Step 7: Summary

After setup, report to the user:

**Spec workflow set up successfully!**

Show:
- List of parsers copied to `lib/`
- List of example specs created
- How to generate: `python generate_specs.py`

**Next steps:**
1. Edit specs in `specs/` to customize
2. Run `python generate_specs.py` to generate
3. Use `/migrate-to-specs` to convert existing generators

**Benefits:**
- Specs are just Python dicts - easy to edit
- Parsers handle all the complex generation logic
- AI can generate specs without writing complex Python
- Parameters separated from implementation
