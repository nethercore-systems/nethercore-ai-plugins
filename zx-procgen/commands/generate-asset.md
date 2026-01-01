---
description: Quick single-asset generation with inline code
argument-hint: "[type] [description]"
allowed-tools: ["AskUserQuestion", "Write", "Read"]
---

# Generate Asset

Generate a single procedural asset (texture, mesh, or sound) with inline code.

## Step 1: Determine Asset Type

**If type argument ($1) is not provided or not one of "texture", "mesh", "sound":**

Use AskUserQuestion to ask:

- Question: "What type of asset do you want to generate?"
- Header: "Type"
- Options:
  - **Texture** - Procedural image (noise, patterns, gradients)
  - **Mesh** - 3D geometry (primitives, modifiers, custom shapes)
  - **Sound** - Audio synthesis (tones, sweeps, noise, presets)

## Step 2: Get Description

**If description argument ($2) is not provided:**

Use AskUserQuestion to ask:

- Question: "Describe the asset you want to generate:"
- Header: "Describe"
- Options (vary by type):

**For Textures:**
  - **Noise pattern** - Perlin, simplex, or voronoi noise
  - **Checker/grid** - Tiled pattern
  - **Gradient** - Smooth color transition
  - **Material** - Metal, stone, crystal preset

**For Meshes:**
  - **Primitive** - Sphere, cube, cylinder, etc.
  - **Character** - Humanoid body parts
  - **Vehicle** - Car, ship, spaceship parts
  - **Prop** - Environmental objects

**For Sounds:**
  - **Pickup** - Coin, powerup collection
  - **Action** - Jump, shoot, hit
  - **Environment** - Explosion, ambient
  - **UI** - Click, menu navigation

## Step 3: Generate Code

Based on the type and description, generate appropriate Python code using numpy, Pillow (imported as PIL), scipy, and bpy.

### For Textures

Generate code using numpy and PIL:

```python
import numpy as np
from PIL import Image
from pyfastnoiselite import FastNoiseLite, NoiseType

def main():
    # Create texture buffer
    width, height = 256, 256
    tex = np.zeros((height, width, 4), dtype=np.uint8)

    # [Generated based on description]
    # Example for "mossy stone":
    # Stone base with Perlin noise
    noise = FastNoiseLite(seed=42)
    noise.noise_type = NoiseType.NoiseType_Perlin
    for y in range(height):
        for x in range(width):
            n = noise.get_noise_2d(x * 0.1, y * 0.1)
            gray = int((n + 1.0) * 0.5 * 96) + 96  # 96-192 range
            tex[y, x] = [gray, gray - 16, gray - 16, 255]  # Stone color

    # Green moss overlay
    for y in range(height):
        for x in range(width):
            n = noise.get_noise_2d(x * 0.05, y * 0.05)
            if n > 0.3:
                blend = (n - 0.3) * 0.5
                tex[y, x] = [
                    int(tex[y, x, 0] * (1 - blend) + 42 * blend),
                    int(tex[y, x, 1] * (1 - blend) + 74 * blend),
                    int(tex[y, x, 2] * (1 - blend) + 42 * blend),
                    255
                ]

    img = Image.fromarray(tex, 'RGBA')
    img.save("assets/textures/mossy_stone.png")
    print("Generated: assets/textures/mossy_stone.png")

if __name__ == "__main__":
    main()
```

### For Meshes

Generate code using Blender bpy:

```python
import bpy
import os

def main():
    # Clear scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # [Generated based on description]
    # Example for "rounded cube":
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    obj = bpy.context.active_object

    # Add subdivision for roundness
    mod = obj.modifiers.new("Subsurf", type='SUBSURF')
    mod.levels = 2
    bpy.ops.object.modifier_apply(modifier=mod.name)

    # Smooth normals
    bpy.ops.object.shade_smooth()

    # Export as OBJ
    bpy.ops.export_scene.obj(
        filepath="assets/meshes/rounded_cube.obj",
        use_selection=True
    )
    print("Generated: assets/meshes/rounded_cube.obj")

if __name__ == "__main__":
    main()
```

### For Sounds

Generate code using numpy and scipy:

```python
import numpy as np
import soundfile as sf
from scipy import signal

SAMPLE_RATE = 22050

def main():
    # [Generated based on description]
    # Example for "laser shot":
    duration = 0.15
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Descending saw wave sweep
    start_freq = 2000.0
    end_freq = 200.0
    freq_sweep = np.linspace(start_freq, end_freq, len(t))
    phase = np.cumsum(2 * np.pi * freq_sweep / SAMPLE_RATE)
    samples = signal.sawtooth(phase)

    # Zap envelope (quick decay)
    envelope = np.exp(-t * 15)
    samples = samples * envelope

    # Normalize and export
    samples = samples / np.max(np.abs(samples)) * 0.9
    sf.write("assets/audio/laser.wav", samples, SAMPLE_RATE, subtype='PCM_16')
    print("Generated: assets/audio/laser.wav")

if __name__ == "__main__":
    main()
```

## Step 4: Provide the Code

Output the generated code with:

1. The complete Python code block
2. Required pip dependencies:
```bash
pip install numpy pillow pyfastnoiselite scipy soundfile
# For mesh generation, requires Blender with Python API (bpy)
```

3. How to run it:
```bash
# Save the code as gen_asset.py, then:
python gen_asset.py
# Or for mesh generation with Blender:
blender --background --python gen_asset.py
```

4. How to use in a game:
```toml
# In nether.toml
[[assets.textures]]  # or meshes/sounds
id = "asset-name"
path = "assets/[type]/asset-name.[ext]"
```

## Generation Guidelines

### Texture Generation Patterns

| Description Keywords | Technique |
|---------------------|-----------|
| "noise", "organic" | `tex.perlin()` or `tex.simplex()` |
| "cells", "scales", "crystal" | `tex.voronoi()` |
| "checker", "grid" | `tex.checker()` |
| "gradient", "fade" | `tex.gradient_*()` |
| "metal", "metallic" | `tex.metal()` |
| "stone", "rock" | `tex.stone()` |
| "glow", "emissive" | Bright colors + radial gradient |

### Mesh Generation Patterns

| Description Keywords | Technique |
|---------------------|-----------|
| "sphere", "ball", "orb" | `generate_sphere()` |
| "cube", "box", "crate" | `generate_cube()` |
| "character", "body" | Combine capsules, spheres |
| "vehicle", "car" | Combine boxes, cylinders |
| "smooth", "rounded" | `Subdivide` + `SmoothNormals` |
| "faceted", "low-poly" | `FlatNormals` |
| "symmetric" | `Mirror` modifier |

### Sound Generation Patterns

| Description Keywords | Technique |
|---------------------|-----------|
| "coin", "pickup" | `synth.coin()` or ascending arpeggio |
| "jump" | `synth.jump()` or upward sweep |
| "laser", "shoot", "zap" | `synth.laser()` or downward saw sweep |
| "explosion", "boom" | `synth.explosion()` or noise burst + sine |
| "hit", "damage" | `synth.hit()` or short noise + square |
| "click", "menu" | `synth.click()` or short beep |
| "powerup" | `synth.powerup()` or ascending arpeggio |
| "death", "game over" | `synth.death()` or descending notes |

## Step 5: Offer Variations

After providing the code, offer:

"Would you like me to:
1. Generate variations with different parameters?
2. Show the Python equivalent?
3. Add this to an existing project's generator?
4. Create a batch generator for multiple assets?"

## Tips for Claude

- Interpret creative descriptions liberally (e.g., "alien crystal" → voronoi + unusual colors)
- Suggest appropriate parameters based on ZX budget (256x256 textures, 200-500 tri meshes)
- Include comments explaining the generation technique
- Provide both simple and layered examples when relevant
- Reference the proc-gen source for advanced patterns

## Gitignore Requirement

**IMPORTANT:** Generated assets should NOT be committed to git.

After generating any asset, ensure the project's `.gitignore` includes:
```
# Generated assets (can be regenerated from procedural code)
assets/meshes/*.obj
assets/meshes/*.gltf
assets/textures/*.png
assets/audio/*.wav
output/**
generated/**
```

If `.gitignore` doesn't exist or is missing these patterns, create/update it.
