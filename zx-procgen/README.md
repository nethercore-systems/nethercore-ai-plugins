# Nethercore ZX Procgen Plugin

Procedural asset generation plugin for Nethercore ZX. Create beautiful textures, meshes, animations, and sounds using any language or tool. Fully supports all ZX rendering features including render modes 0-3, matcaps, dither transparency, and vertex colors.

## Features

- **Knowledge Skills**: Comprehensive guidance for textures, meshes, animations, sounds, and more
- **SADL (Semantic Asset Description Language)**: AI-first creative pipeline with style tokens, color palettes, materials, and quality heuristics
- **Full ZX Render Mode Support**: Modes 0-3 (Lambert, Matcap, Metallic-Roughness, Specular-Shininess)
- **Matcap Generation**: Shadow, highlight, and HSV matcaps with blend modes (Multiply, Add, HSV Modulate)
- **Alpha/Dither Transparency**: Bayer 4x4 dithered transparency via alpha channel
- **Vertex Color Meshes**: Per-vertex coloring, gradients, baked AO
- **Skeletal Animation**: GPU skinning, bone weights, walk cycles, attacks, IK systems
- **Rigid Body Animation**: Vehicle physics, robots, mechanical systems
- **Quality Tier System**: Placeholder → Temp → Final → Hero progression for assets
- **4 Commands**: `/new-asset-project`, `/generate-asset`, `/generate-sfx`, `/improve-assets`
- **9 Agents**: Creative pipeline + quality analysis + quality enhancement
- **Language Agnostic**: Use Rust, Python, Processing, Blender, or any tool that outputs standard formats

## Installation

### Global Installation

Add to `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "nethercore-ai-plugins": {
      "source": {
        "source": "github",
        "repo": "nethercore-systems/nethercore-ai-plugins"
      }
    }
  },
  "enabledPlugins": {
    "zx-procgen@nethercore-ai-plugins": true
  }
}
```

### Workspace Installation

Add to `.claude/settings.local.json`:

```json
{
  "extraKnownMarketplaces": {
    "nethercore-ai-plugins": {
      "source": {
        "source": "directory",
        "path": "./nethercore-ai-plugins"
      }
    }
  },
  "enabledPlugins": {
    "zx-procgen@nethercore-ai-plugins": true
  }
}
```

## Quick Start

### Create a New Asset Project

```
/new-asset-project my-game-assets
```

This scaffolds a complete project with:
- Asset generator (Rust, Python, or Processing)
- ZX viewer for previewing assets in-engine
- Proper directory structure for the asset pipeline

### Generate Single Assets

```
/generate-asset texture "mossy stone wall"
/generate-asset mesh "low-poly spaceship"
/generate-asset sound "retro coin pickup"
```

### Ask About Techniques

The skills auto-trigger when you ask:
- "How do I generate a procedural texture?"
- "Create a mesh with voronoi noise pattern"
- "Generate a laser sound effect"
- "What's the best way to create tileable textures?"

## Skills

### Procedural Textures

Full ZX material system support:
- **Mode 0 (Lambert)**: Albedo with optional alpha for dither transparency
- **Mode 1 (Matcap)**: Albedo + up to 3 matcap textures with blend modes
- **Mode 2 (MRE)**: Albedo + Metallic/Roughness/Emissive packed texture
- **Mode 3 (SSE)**: Albedo + Specular Reduction/Shininess/Emissive + Specular color

Plus: Noise algorithms (Perlin, Simplex, Voronoi, FBM), patterns, material presets, and clear guidance on uniform vs texture properties.

**Trigger phrases**: "generate texture", "matcap", "MRE texture", "dither transparency", "procedural material"

### Procedural Meshes

Primitives (cube, sphere, cylinder, etc.), modifiers (subdivide, mirror, smooth), mesh combining, UV mapping (optional), and vertex colors (optional).

**Note**: UVs and vertex colors are optional - choose based on your art style needs.

**Trigger phrases**: "generate mesh", "vertex colors", "3D model", "low-poly character"

### Procedural Animations (v2.0)

Comprehensive animation generation with three paradigms:

**Skeletal Animation:**
- GPU skinning with 3x4 bone matrices
- Procedural bone weight generation (distance, heat diffusion, geodesic)
- Character locomotion (walk cycles, runs, idles, attacks, jumps)
- Creature animation (quadrupeds, spiders, flying creatures)
- Inverse kinematics (two-bone, FABRIK, CCD, foot IK, look-at)

**Rigid Body Animation:**
- Vehicle physics (suspension, steering, wheel rotation)
- Robot arms and mechanical systems
- Gears, doors, cranes, and articulated objects

**Transform-based:**
- Oscillations, rotations, bounces
- Tree/plant wind animation
- Easing functions library

**Trigger phrases**: "generate animation", "walk cycle", "skeletal animation", "bone weights", "IK", "vehicle suspension", "robot animation", "rig character"

### Procedural Sounds (v3.0 - NumPy/SciPy)

Production-quality sound effects using **NumPy**, **SciPy**, and **soundfile** - lightweight, pure-Python audio synthesis with no external audio dependencies:

**Synthesis Building Blocks:**
- **Oscillators**: Sine, Square, Sawtooth, Triangle, SuperSaw (np.sin, np.sign)
- **Noise**: White (np.random.randn), Pink (FFT shaping), Brown (cumulative sum)
- **Envelopes**: ADSR, exponential decay (np.exp), linear/exponential segments
- **Filters**: Butterworth LP/HP/BP (scipy.signal.butter + filtfilt)
- **FM Synthesis**: Direct formula (sin(phase + index * sin(mod_phase)))
- **Effects**: Delay, Reverb (comb filters), Distortion (tanh), Compression

**Technique Guide:**
| Technique | Best For | Functions |
|-----------|----------|-----------|
| Subtractive | Bassy, warm, explosive | noise → butter → filtfilt |
| FM | Metallic, bells, digital | sin(phase + β*sin(mod)) |
| Additive | Organs, complex tones | Sum of sine waves |
| Filtered Noise | Impacts, footsteps, texture | randn → butter filter |

**Production-Ready Recipes:**
8 complete SFX scripts with customization parameters:
- Laser/Zap, Explosion, Coin/Pickup, Jump
- Hit/Punch, Powerup, Footstep, UI Click

**Prerequisites**: `pip install numpy scipy soundfile`

**Trigger phrases**: "generate sound", "numpy synthesis", "procedural audio", "SFX", "FM synthesis", "WAV generation"

### Semantic Asset Language (SADL)

AI-first creative asset pipeline that bridges creative intent and procedural generation:

**Core Components:**
- **Style Tokens**: Visual style descriptors (Rustic, Cyberpunk, Organic, Gothic, Steampunk, etc.) with automatic parameter modifiers
- **Color Palettes**: Semantic color schemes (WarmEarthy, Neon, Pastel, Muted, Vibrant, etc.) with HSL ranges
- **Material Database**: 40+ PBR material presets (metal.rusted, wood.weathered, crystal.magical, etc.)
- **Quality Heuristics**: Self-assessment metrics for textures, meshes, and animations

**Workflow:**
1. Describe assets naturally ("weathered medieval barrel", "sleek sci-fi console")
2. SADL translates to concrete generation parameters
3. Generate assets with quality self-checks
4. Iterate until quality targets are met

**Trigger phrases**: "SADL", "style token", "semantic asset", "design asset", "creative pipeline", "quality heuristics"

### Asset Quality Tiers

A four-tier quality system for progressive asset improvement:

**Tier System:**
- **Placeholder** (30-50%): Blocking, scale testing, rapid iteration
- **Temp** (50-70%): Development testing, internal builds
- **Final** (70-90%): Ship-ready, production quality
- **Hero** (90-100%): Maximum quality for marketing, cutscenes, closeups

**Enhancement Strategies:**
- Mesh: Add UVs → Add bevels → Add edge loops and detail
- Texture: Add noise → Add contrast/layers → Add wear/all channels
- Audio: Add envelope → Add layers → Add variation/richness
- Animation: Add keyframes → Add easing → Add anticipation/follow-through

**Trigger phrases**: "quality tiers", "upgrade to final", "hero quality", "placeholder vs final", "asset polish"

## Agents

### Creative Pipeline Agents (SADL)

Four specialized agents that work together for end-to-end asset creation:

#### Asset Designer
Interprets creative descriptions into SADL specifications. Translates "weathered medieval barrel" into concrete style tokens, palettes, materials, and parameters.

**Trigger**: "design assets for", "I want a rusty barrel", "cyberpunk aesthetic"

#### Asset Generator
Produces working procedural generation code from SADL specifications. Outputs complete, runnable Rust/Python code with quality self-checks.

**Trigger**: "generate code for this spec", "create the mesh generator", "implement this recipe"

#### Asset Critic
Evaluates generated assets against quality heuristics and SADL specifications. Reports issues by severity (Critical/Error/Warning/Info) with actionable fixes.

**Modes**: Lenient (blockers only), Normal (default), Strict (all issues)

**Trigger**: "review this asset", "check quality", "critique my mesh"

#### Creative Orchestrator
Coordinates the full pipeline from creative vision to validated, production-ready assets. Manages iterative refinement until quality targets are met.

**Modes**: Interactive (with approval steps) or Autonomous (hands-off)

**Trigger**: "create assets for my game", "build a complete asset set", "orchestrate asset creation"

### Asset Quality Reviewer

Analyzes generated assets for ZX compliance:
- Texture dimensions and file sizes
- Mesh polygon counts
- Audio sample rates and durations

**Trigger**: "review my assets", "check asset quality"

### Procgen Optimizer

Suggests optimizations for smaller/faster assets:
- Lower subdivision levels
- Simpler noise parameters
- Audio compression

**Trigger**: "optimize my assets", "reduce file size"

### Quality Enhancer

Autonomous asset quality improvement through the tier system. Takes existing assets and upgrades them to higher quality tiers.

**Capabilities:**
- Assess current tier of all project assets
- Apply enhancement strategies per asset type
- Upgrade meshes (bevels, silhouettes, edge loops)
- Upgrade textures (contrast, layers, material channels)
- Upgrade audio (envelopes, layers, variation)

**Trigger**: "improve my assets", "quality up pass", "make assets better", "upgrade to final", "hero quality"

### Quality Analyzer

Holistic asset quality assessment with scoring, issue identification, and auto-dispatch support for fixes.

**Trigger**: "analyze asset quality", "quality report", "are these production-ready"

### Character Generator

End-to-end animated character creation pipeline, producing mesh, skeleton, skinning, and animations.

**Trigger**: "generate character", "create player character", "make animated NPC"

## Commands

### `/new-asset-project [name]`
Scaffold a complete procedural asset project with generator code and ZX viewer.

### `/generate-asset [type] [description]`
Quick single-asset generation (texture, mesh, or sound) with inline code.

### `/generate-sfx <type> [output-path]`
Quick SFX generation with NumPy/SciPy. Types: laser, explosion, coin, jump, hit, powerup, footstep, click. Generates a Python script with customizable parameters.

### `/improve-assets [target-tier]`
Interactive quality improvement workflow. Scans assets, assesses current tiers, and guides upgrades to the target tier (Temp, Final, or Hero).

## Output Formats

The asset pipeline accepts standard formats:

| Type | Format | Specs |
|------|--------|-------|
| Textures | PNG | Power of 2, max 512x512 |
| Meshes | OBJ, GLTF | Triangulated, Y-up |
| Sounds | WAV | 22050 Hz, 16-bit mono |

## Integration with Nethercore

Generated assets integrate with the standard workflow:

1. Generate assets to `assets/` directory
2. Reference in `nether.toml`:
```toml
[[assets.textures]]
id = "my-texture"
path = "assets/textures/my-texture.png"
```
3. Run `nether pack` to bundle into ROM
4. Load in game with `rom_texture_str("my-texture")`

## Related

- **zx-dev**: Game development fundamentals
- **proc-gen library**: `nethercore/tools/proc-gen/`
- **Showcase workflow**: `SHOWCASE_TEMPLATE.md`

## License

Part of the Nethercore project.
