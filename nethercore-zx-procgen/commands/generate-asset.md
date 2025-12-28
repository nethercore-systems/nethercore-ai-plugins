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

Based on the type and description, generate appropriate Rust code using the proc-gen library.

### For Textures

Generate code using `proc_gen::texture::*`:

```rust
use proc_gen::texture::*;

fn main() {
    let mut tex = TextureBuffer::new(256, 256);

    // [Generated based on description]
    // Example for "mossy stone":
    tex.stone(0x606050FF, 42);
    tex.perlin(0.1, 123, 0x00000000, 0x2a4a2aFF); // Green moss overlay

    tex.write_png("assets/textures/mossy_stone.png").unwrap();
    println!("Generated: assets/textures/mossy_stone.png");
}
```

### For Meshes

Generate code using `proc_gen::mesh::*`:

```rust
use proc_gen::mesh::*;
use glam::Vec3;

fn main() {
    // [Generated based on description]
    // Example for "rounded cube":
    let mut mesh: UnpackedMesh = generate_cube(1.0, 1.0, 1.0);
    mesh.apply(Subdivide { iterations: 2 });
    mesh.apply(SmoothNormals);

    write_obj(&mesh, "assets/meshes/rounded_cube.obj", "rounded_cube").unwrap();
    println!("Generated: assets/meshes/rounded_cube.obj");
}
```

### For Sounds

Generate code using `proc_gen::audio::*`:

```rust
use proc_gen::audio::*;

fn main() {
    let synth = Synth::new(SAMPLE_RATE);

    // [Generated based on description]
    // Example for "laser shot":
    let samples = synth.sweep(
        Waveform::Saw,
        2000.0,  // Start high
        200.0,   // End low
        0.15,    // Quick
        Envelope::zap(),
    );

    let pcm = to_pcm_i16(&samples);
    write_wav(&pcm, SAMPLE_RATE, "assets/audio/laser.wav").unwrap();
    println!("Generated: assets/audio/laser.wav");
}
```

## Step 4: Provide the Code

Output the generated code with:

1. The complete Rust code block
2. Required Cargo.toml dependencies:
```toml
[dependencies]
proc-gen = { path = "../nethercore/tools/proc-gen", features = ["wav-export"] }
glam = "0.27"  # if mesh
```

3. How to run it:
```bash
# Save the code as gen_asset.rs, then:
cargo run
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
