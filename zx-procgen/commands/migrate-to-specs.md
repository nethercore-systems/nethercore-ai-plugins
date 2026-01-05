---
description: Convert existing Python generator code to spec-driven format
argument-hint: "[path-to-generator.py | --upgrade]"
allowed-tools: ["Read", "Write", "Glob", "Bash", "AskUserQuestion"]
---

# Migrate to Specs

Two modes:
1. **Upgrade mode** (`/migrate-to-specs --upgrade`) - Upgrade legacy project to current naming conventions
2. **Migration mode** (`/migrate-to-specs [file.py]`) - Convert inline Python code to spec format

## Step 0: Detect and Upgrade Legacy Structure

**Always run this step first.** Check if the project uses old naming conventions:

**Detect old patterns:**
```bash
# Check for old animation format
find . -name "*.motion.py" 2>/dev/null
# Check for old MOTION dict
grep -r "MOTION\s*=" --include="*.py" .
# Check for old parser locations
ls lib/*_parser.py 2>/dev/null
# Check for missing .studio/
ls .studio/generate.py 2>/dev/null || echo "No .studio/ found"
```

**If old patterns found OR .studio/ missing, upgrade:**

1. **Rename `.motion.py` → `.spec.py`:**
   ```bash
   for f in $(find . -name "*.motion.py"); do
     mv "$f" "${f%.motion.py}.spec.py"
   done
   ```

2. **Update MOTION → ANIMATION in spec files:**
   ```bash
   sed -i 's/MOTION\s*=/ANIMATION =/g' *.spec.py
   ```

3. **Replace old parsers with new unified system:**
   - Delete old `lib/*_parser.py` files
   - Copy new `.studio/` scaffold from plugin:
   ```bash
   cp -r $CLAUDE_PLUGIN_ROOT/zx-procgen/scaffold/.studio .
   ```

4. **Move specs to new location (if needed):**
   ```bash
   # If specs exist in old location, move them
   if [ -d "specs" ] && [ ! -d ".studio/specs" ]; then
     mv specs/* .studio/specs/ 2>/dev/null
   fi
   ```

5. **Update generator imports in any custom scripts:**
   - Old: `from lib.motion_parser import ...`
   - New: `from .studio.parsers.animation import ...`

**Summary of naming changes:**
| Old | New |
|-----|-----|
| `.motion.py` | `.spec.py` |
| `MOTION = {...}` | `ANIMATION = {...}` |
| `motion_parser.py` | `animation.py` |
| `lib/` | `.studio/parsers/` |
| `specs/` | `.studio/specs/` |
| `motion-describer` agent | `animation-describer` agent |

---

## Step 0.5: Check for Upgrade-Only Mode

**If argument is `--upgrade` OR no generators to migrate:**

Report upgrade summary and stop:

```
Upgrade complete!

Changes made:
- Renamed X .motion.py files to .spec.py
- Updated MOTION → ANIMATION in Y files
- Installed/updated .studio/ scaffold
- Moved specs to .studio/specs/

To generate assets:
  python .studio/generate.py

To migrate inline Python generators:
  /migrate-to-specs path/to/generator.py
```

**If user wants to also migrate generators, continue to Step 1.**

---

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
| PIL texture | `.texture.spec.py` (TEXTURE) | texture.py |
| numpy/scipy audio | `.spec.py` (SOUND) | sound.py |
| Blender mesh | `.spec.py` (CHARACTER) | character.py |
| Blender animation | `.spec.py` (ANIMATION) | animation.py |
| Normal map | `.normal.spec.py` (NORMAL) | normal.py |

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

- `.studio/specs/textures/{name}.texture.spec.py`
- `.studio/specs/sounds/{name}.spec.py`
- `.studio/specs/characters/{name}.spec.py`
- `.studio/specs/animations/{name}.spec.py`
- `.studio/specs/normals/{name}.normal.spec.py`

## Step 6: Create Wrapper Script (Optional)

If the original generator had custom logic that can't be captured in the spec, create a thin wrapper:

```python
#!/usr/bin/env python3
"""Generate wood texture from spec."""

import sys
from pathlib import Path

# Add .studio to path
sys.path.insert(0, str(Path(__file__).parent / '.studio'))

from parsers.texture import load_spec, generate_texture, write_png

spec = load_spec('.studio/specs/textures/wood.texture.spec.py')
result = generate_texture(spec)
write_png('assets/textures/wood.png', result)
```

**Recommended:** Use the unified generator instead:
```bash
python .studio/generate.py --only textures
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
- Spec created: `.studio/specs/textures/wood.texture.spec.py`
- Parser used: `.studio/parsers/texture.py`

**Extracted parameters:**
- Size: 256x256
- Seed: 42
- Layers: 1 (wood_grain)
- Colors: #4A3728 → #6A5748

**To generate:**
```bash
python .studio/generate.py --only textures
```

Or generate all assets:
```bash
python .studio/generate.py
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
