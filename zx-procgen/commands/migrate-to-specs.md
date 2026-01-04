---
description: Convert existing Python generator code to spec-driven format
argument-hint: "[path-to-generator.py]"
allowed-tools: ["Read", "Write", "Glob", "AskUserQuestion"]
---

# Migrate to Specs

Convert existing Python generator code to the spec-driven format. Analyzes your generator, extracts configuration into a `.spec.py` file, and creates a wrapper that uses the parser.

## Why Migrate?

| Before | After |
|--------|-------|
| All logic inline | Logic in reusable parser |
| Hardcoded params | Params in spec file |
| Difficult to iterate | Edit just the spec |
| AI generates full code | AI generates just config |

## Step 1: Get Generator Path

**If path argument ($1) is not provided:**

Use AskUserQuestion to ask:

- Question: "Which generator file do you want to migrate?"
- Header: "File"
- Options:
  - (Let user type the path)

Then use Glob to find `.py` files in `generation/` if user wants to browse:

```bash
find generation/ -name "*.py" -type f 2>/dev/null | head -20
```

## Step 2: Analyze Generator

Read the generator file and identify:

1. **Asset type** - texture, sound, mesh, animation based on:
   - Imports (PIL/numpy → texture, scipy/soundfile → sound, bpy → mesh/animation)
   - Output format (`.png` → texture, `.wav` → sound, `.glb` → mesh)

2. **Configuration parameters**:
   - Numeric literals (dimensions, frequencies, scales)
   - String literals (colors, paths, names)
   - Array/list literals (color palettes, layer configs)

3. **Generation logic**:
   - Noise generation
   - Layer composition
   - Filters and effects

## Step 3: Determine Spec Type

Based on analysis, determine which spec format to use:

| Generator Type | Spec Format | Parser |
|---------------|-------------|--------|
| PIL texture | `.texture.spec.py` (TEXTURE) | texture_parser.py |
| numpy/scipy audio | `.spec.py` (SOUND) | sound_parser.py |
| Blender mesh | `.spec.py` (SPEC) | character_parser.py |
| Blender animation | `.motion.py` (MOTION) | motion_parser.py |
| Normal map | `.normal.spec.py` (NORMAL) | normal_parser.py |

## Step 4: Extract Parameters

Analyze the code and extract hardcoded values into spec structure.

### Example: Texture Migration

**Before (`generation/textures/wood.py`):**
```python
from PIL import Image
import numpy as np
from pyfastnoiselite import FastNoiseLite

def generate():
    width, height = 256, 256
    noise = FastNoiseLite()
    noise.seed = 42
    noise.noise_type = "Perlin"
    noise.frequency = 0.02

    # Generate base wood grain
    data = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            val = noise.get_noise(x, y) * 0.5 + 0.5
            # Wood grain distortion
            val += 0.3 * noise.get_noise(x * 5, y * 0.1)
            val = val % 1.0
            # Apply wood colors
            r = int(74 + val * 40)
            g = int(55 + val * 30)
            b = int(40 + val * 20)
            data[y, x] = [r, g, b]

    img = Image.fromarray(data)
    img.save("generated/textures/wood.png")
```

**After (`specs/textures/wood.texture.spec.py`):**
```python
TEXTURE = {
    'texture': {
        'name': 'wood',
        'size': [256, 256],
        'layers': [
            {
                'type': 'wood_grain',
                'scale': 0.02,
                'grain_scale': 5.0,
                'seed': 42,
                'blend': 'normal',
                'opacity': 1.0,
            },
        ],
        'color_ramp': ['#4A3728', '#5A4738', '#6A5748'],
    }
}
```

### Example: Sound Migration

**Before (`generation/sounds/laser.py`):**
```python
import numpy as np
from scipy.io import wavfile

def generate():
    sr = 22050
    duration = 0.3
    t = np.linspace(0, duration, int(sr * duration))

    freq_start = 800
    freq_end = 200
    freq = np.linspace(freq_start, freq_end, len(t))
    wave = np.sin(2 * np.pi * freq * t) * 0.8

    # Apply envelope
    attack = int(0.01 * sr)
    decay = int(0.1 * sr)
    env = np.ones_like(wave)
    env[:attack] = np.linspace(0, 1, attack)
    env[-decay:] = np.linspace(1, 0, decay)
    wave *= env

    wavfile.write("laser.wav", sr, (wave * 32767).astype(np.int16))
```

**After (`specs/sounds/laser.spec.py`):**
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
            'sustain': 1.0,
            'release': 0.0,
        },
        'normalize': True,
    }
}
```

## Step 5: Create Spec File

Write the extracted spec to the appropriate location:

- `specs/textures/{name}.texture.spec.py`
- `specs/sounds/{name}.spec.py`
- `specs/characters/{name}.spec.py`
- `specs/animations/{name}.motion.py`
- `specs/normals/{name}.normal.spec.py`

## Step 6: Create Wrapper Script (Optional)

If the original generator had custom logic that can't be captured in the spec, create a thin wrapper:

```python
#!/usr/bin/env python3
"""Generate wood texture from spec."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))

from texture_parser import load_spec, generate_texture, write_png

spec = load_spec('specs/textures/wood.texture.spec.py')
result = generate_texture(spec)
write_png('generated/textures/wood.png', result)
```

## Step 7: Validate Migration

Compare old and new outputs:

1. Run original generator (if possible)
2. Run new spec-based generation
3. Report any significant differences

If outputs differ, identify what wasn't captured in the spec and either:
- Adjust spec parameters
- Note limitations for user to handle

## Step 8: Summary

After migration, report:

**Migration complete!**

- Original: `generation/textures/wood.py`
- Spec created: `specs/textures/wood.texture.spec.py`
- Parser used: `lib/texture_parser.py`

**Extracted parameters:**
- Size: 256x256
- Seed: 42
- Layers: 1 (wood_grain)
- Colors: #4A3728 → #6A5748

**To generate:**
```bash
python -c "
from lib.texture_parser import load_spec, generate_texture, write_png
spec = load_spec('specs/textures/wood.texture.spec.py')
write_png('generated/textures/wood.png', generate_texture(spec))
"
```

**Notes:**
- Original file kept as backup
- Review spec and adjust parameters as needed
- Some custom logic may need manual porting

## Limitations

Not all generators can be fully migrated:

| Can Migrate | Cannot Migrate |
|-------------|----------------|
| Standard noise patterns | Custom algorithms |
| Common layer types | Unique blend modes |
| ADSR envelopes | Complex modulation |
| Basic geometries | Procedural meshes |

For complex generators, the migration provides a starting point that may need manual refinement.
