# Nethercore ZX Procgen Plugin

Procedural asset generation plugin for Nethercore ZX. Create beautiful textures, meshes, animations, and sounds using any language or tool. Fully supports all ZX rendering features including render modes 0-3, matcaps, dither transparency, and vertex colors.

## Audio Synthesis Role

For audio assets, this plugin handles **synthesis** - converting design specs into actual audio files.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ sound-design│ → │  zx-procgen │ → │tracker-music│
│   DESIGN    │    │  SYNTHESIS  │    │ COMPOSITION │
│             │    │  ← AUDIO    │    │             │
│             │    │     HERE    │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Audio commands:**
- `zx-procgen:generate-sfx` - Quick SFX generation from type
- `zx-procgen:generate-instrument` - Instrument sample synthesis

**Audio agents:**
- `instrument-architect` - Designs and implements instrument synthesis

**Audio skills:**
- `procedural-sounds` - NumPy/SciPy SFX synthesis
- `procedural-instruments` - FM, Karplus-Strong, wavetable synthesis

See [Audio Pipeline Guide](../docs/audio-pipeline.md) for complete workflows.

## Features

- **Knowledge Skills**: Comprehensive guidance for textures, meshes, animations, sounds, and more
- **visual style guide**: AI-first creative pipeline with style tokens, color palettes, materials, and quality heuristics
- **Full ZX Render Mode Support**: Modes 0-3 (Lambert, Matcap, Metallic-Roughness, Specular-Shininess)
- **Matcap Generation**: Shadow, highlight, and HSV matcaps with blend modes (Multiply, Add, HSV Modulate)
- **Alpha/Dither Transparency**: Bayer 4x4 dithered transparency via alpha channel
- **Vertex Color Meshes**: Per-vertex coloring, gradients, baked AO
- **Skeletal Animation**: GPU skinning, bone weights, walk cycles, attacks, IK systems
- **Rigid Body Animation**: Vehicle physics, robots, mechanical systems
- **Quality Tier System**: Placeholder → Temp → Final → Hero progression for assets
- **Procedural Instruments**: High-quality instrument samples via Karplus-Strong, FM, wavetable, additive synthesis
- **Procedural Characters**: Full character generation with meshes, rigs, and animations
- **Spec-Driven Parsers**: Declarative `.spec.py` files + reusable parsers for textures, sounds, characters, animations, normals
- **10 Commands**: `zx-procgen:init-procgen` (⚡ recommended), `zx-procgen:new-asset-project`, `zx-procgen:generate-asset`, `zx-procgen:generate-sfx`, `zx-procgen:generate-instrument`, `zx-procgen:improve-assets`, `zx-procgen:establish-visual-style`, `zx-procgen:generate-all`, `zx-procgen:setup-spec-workflow`, `zx-procgen:migrate-to-specs`
- **11 Agents**: Creative pipeline + character generation + animation specs + normal maps + unified quality review + enhancement + instrument design
- **Python-Based Generators**: Use Python with PIL, Blender bpy, numpy/scipy, or any tool that outputs standard formats

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

### Option 1: Token-Efficient Setup (Recommended) ⚡

**Best for:** New projects, token-conscious workflows, fast setup

```
zx-procgen:init-procgen
```

Installs/updates the unified `.studio/` scaffold (wrapper around `ai-studio init`):
- Installs/overwrites `.studio/generate.py` and `.studio/parsers/**`
- Preserves existing `.studio/specs/**`, `.studio/direction/**`, `.studio/designs/**`, `.studio/analysis/**`
- Ensures output folders under `generated/` and a `generated/.gitignore`
- Writes/updates `ai_studio.toml` with a pinned `core_version`

**Token savings:** avoids “Read/Write” copying large scaffolds into context.

### Option 2: Full Asset Project Scaffold

**Best for:** Complete project with game integration, viewer, build system

```
zx-procgen:new-asset-project my-game-assets
```

This scaffolds a complete project with:
- Python asset generators (PIL for textures, Blender bpy for meshes, numpy/scipy for audio)
- ZX viewer for previewing assets in-engine
- Proper directory structure for the asset pipeline

### Generate Single Assets

```
zx-procgen:generate-asset texture "mossy stone wall"
zx-procgen:generate-asset mesh "low-poly spaceship"
zx-procgen:generate-asset sound "retro coin pickup"
```

### Ask About Techniques

The skills auto-trigger when you ask:
- "How do I generate a procedural texture?"
- "Create a mesh with voronoi noise pattern"
- "Generate a laser sound effect"
- "What's the best way to create tileable textures?"

## Skills (13)

All skills follow the **progressive disclosure pattern** for LLM context efficiency:
- SKILL.md files are lean (100-170 lines) with decision tables and quick references
- Detailed code and examples are in `references/` directories
- Frontmatter includes "Load references when:" directives for on-demand loading
- Large reference files (1000+ lines) have index files for routing

### Procedural Textures

Full ZX material system support (render mode configured in `nether.toml`):
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

### Procedural Animations (v5.0)

Comprehensive animation generation with **structured animation specs** and the unified generator:

**Animation Spec Pipeline:**
1. `animation-describer` agent → Structured animation spec (`.spec.py`) with bone rotations
2. `ai-studio generate --only animations` → Interprets specs in Blender (legacy: `blender --background --python .studio/generate.py -- --only animations`)

**Why Animation Specs?** Python dict literals work natively in Blender (no PyYAML dependency). Explicit bone rotations in degrees (pitch/yaw/roll) eliminate coordinate confusion. The parser is deterministic and skeleton-agnostic.

**Skeletal Animation:**
- GPU skinning with 3x4 bone matrices
- Procedural bone weight generation (distance, heat diffusion, geodesic)
- Character locomotion (walk cycles, runs, idles, attacks, jumps)
- Creature animation (quadrupeds, spiders, flying creatures)
- **IK utilities for locomotion** - Foot IK prevents sliding, baked to FK for export
- Coordinate reasoning protocol for accurate FK rotations

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

### Procedural Instruments (NEW)

Production-quality instrument synthesis for game music. Solves the "chiptuney" problem by implementing advanced synthesis techniques that create realistic, evolving timbres instead of basic oscillator sounds.

**Synthesis Techniques:**
| Technique | Best For | Example Instruments |
|-----------|----------|---------------------|
| Karplus-Strong | Plucked strings | Acoustic guitar, bass, harp, koto |
| FM Synthesis | Keys, bells | Electric piano (DX7), tubular bells, vibraphone |
| Wavetable | Pads, evolving sounds | String ensemble, synth pads |
| Additive | Organs | Hammond organ with drawbars |
| Subtractive | Leads, bass | Synth bass, brass, supersaw leads |

**Why It's Better Than Raw Oscillators:**
- Multi-stage envelopes (not just ADSR)
- Attack transients with noise bursts
- Evolving timbres via modulation envelopes
- Detuned unison voices for richness
- Physical modeling for realistic strings

**8 Complete Recipes:**
- `acoustic-guitar.py` - Karplus-Strong with body resonance
- `electric-piano.py` - FM synthesis (Rhodes/Wurlitzer)
- `synth-bass.py` - Subtractive (punchy, reese, sub)
- `strings-pad.py` - Wavetable with unison detuning
- `organ.py` - Additive with Hammond drawbars
- `brass-lead.py` - Subtractive with breath noise
- `fm-bell.py` - FM inharmonic (tubular, church, glockenspiel)
- `pluck-synth.py` - Various plucks (harp, koto, kalimba, marimba)

**Trigger phrases**: "generate instrument", "synthesize piano", "Karplus-Strong", "FM electric piano", "realistic instrument", "not chiptuney", "high quality sample", "wavetable pad"

### Visual Style Guide

AI-first creative asset pipeline that bridges creative intent and procedural generation:

**Core Components:**
- **Style Tokens**: Visual style descriptors (Rustic, Cyberpunk, Organic, Gothic, Steampunk, etc.) with automatic parameter modifiers
- **Color Palettes**: Semantic color schemes (WarmEarthy, Neon, Pastel, Muted, Vibrant, etc.) with HSL ranges
- **Material Database**: 40+ PBR material presets (metal.rusted, wood.weathered, crystal.magical, etc.)
- **Quality Heuristics**: Self-assessment metrics for textures, meshes, and animations

**Workflow:**
1. Describe assets naturally ("weathered medieval barrel", "sleek sci-fi console")
2. Style guide translates to concrete generation parameters
3. Generate assets with quality self-checks
4. Iterate until quality targets are met

**Trigger phrases**: "style guide", "style token", "semantic asset", "design asset", "creative pipeline", "quality heuristics"

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

### Procedural Characters

End-to-end character generation with meshes, rigs, and animations:

**Pipeline:**
1. **character-designer** agent gathers requirements → produces `.spec.py` file
2. **character-generator** agent builds mesh from spec using Blender bpy

**Character Types:**
- Humanoid (bipedal with standard skeleton)
- Quadruped (4 legs, horizontal spine)
- Creatures (spider, serpent, bird, custom)

**Style Presets:**
- Mecha (sharp angles, blocky)
- Organic (smooth curves)
- Armored (plate flares, hard edges)
- Robed (flowing fabric)
- Chibi (large head, short limbs)

**Output:**
- GLB mesh with embedded armature
- Automatic bone weights
- 300-700 triangle budget

**Trigger phrases**: "generate character", "create player mesh", "enemy model", "NPC with animations", "character rig", "skeletal mesh"

### Procedural Normal Maps

Generate tangent-space normal maps for surface detail without additional geometry:

**Features:**
- Height-to-normal conversion (Sobel gradients)
- Procedural patterns (brick, tile, fabric, metal scratches, noise)
- Seamless tileable generation (4D torus mapping)
- BC5 format compression (auto-triggered by `_normal.png` naming)

**Integration:**
- Meshes must have tangent data (`export_tangents=True` in Blender)
- Material binding via `material_normal(texture_id)`
- Works with all render modes (0-3)

**Trigger phrases**: "generate normal map", "normal map", "bump map", "height to normal", "surface detail", "BC5 texture"
### Generator Patterns

Common patterns for procedural generation code:

- Noise-based generation (Perlin, Simplex, Voronoi)
- Modular mesh construction
- Material layering systems
- Asset variation from parameters

**Trigger phrases**: "generator pattern", "noise algorithm", "procedural pattern", "generation code structure"

## Agents

### Creative Pipeline Agents

Five specialized agents for end-to-end asset creation:

| Agent | Purpose | Triggers |
|-------|---------|----------|
| **asset-designer** | Translates creative descriptions to style specs | "design asset", "I want X style" |
| **asset-generator** | Produces procedural generation code | "generate code for spec", "create mesh generator" |
| **creative-orchestrator** | Coordinates full pipeline (design→generate→validate→refine) | "create assets for my game", "full asset pipeline" |
| **character-designer** | Gathers character requirements and produces `.spec.py` files | "design character", "character spec", "plan character mesh" |
| **character-generator** | Builds character meshes from `.spec.py` files using Blender bpy | "generate character", "create player", "animated NPC" |

### Quality Agents

| Agent | Purpose | Triggers |
|-------|---------|----------|
| **asset-quality-reviewer** | Unified quality assessment (technical + creative + holistic) | "check quality", "review assets", "ZX limits", "match spec" |
| **quality-enhancer** | Upgrades assets through tier system | "improve assets", "quality up pass", "upgrade to final" |
| **procgen-optimizer** | Reduces asset sizes and improves performance | "optimize generation", "reduce poly count", "ROM too big" |

### Animation Agent

| Agent | Purpose | Triggers |
|-------|---------|----------|
| **animation-describer** | Produces structured `.spec.py` specs with bone rotations | "describe animation", "animation spec", "animation description", "animate character" |

### Specialty Agents

| Agent | Purpose | Triggers |
|-------|---------|----------|
| **instrument-architect** | Synthesizes high-quality instrument samples | "generate instrument", "synthesize piano", "not chiptuney" |
| **normal-map-generator** | Generates procedural normal maps from height patterns | "generate normal map", "normal map for", "height to normal", "surface detail" |

## Commands

Commands are documented in `plugin:command` form (e.g. `zx-procgen:init-procgen`). Depending on your Claude/Codex client, they may also appear as slash commands (e.g. `/init-procgen`).

### `zx-procgen:init-procgen [project-dir]` ⚡ (Recommended)

**Token-efficient infrastructure setup** - Installs/updates the `.studio/` scaffold via `ai-studio init` (fast local file copy).

**Usage:**
```bash
zx-procgen:init-procgen                    # Set up in current directory
zx-procgen:init-procgen ./my-project       # Set up in specific directory
```

**What it does:**
1. Installs `.studio/generate.py` and `.studio/parsers/**` (overwritten), preserving `.studio/specs/**` etc.
2. Ensures `.studio/` directory structure (`specs/*/`, `direction/`, `designs/`, `analysis/`)
3. Ensures `generated/` output folders (gitignored) match the generator conventions
4. Writes/updates `ai_studio.toml` with a pinned `core_version`

**Token savings:** 95% reduction vs manual setup

**When to use:**
- ✅ Setting up a new project (fast, efficient)
- ✅ Default configuration is acceptable

**When to use `zx-procgen:setup-spec-workflow` instead:**
- Interactive setup with customization
- Need to review parser code before copying
- Educational/learning context

### `zx-procgen:new-asset-project [name]`
Scaffold a complete procedural asset project with generator code and ZX viewer.

### `zx-procgen:generate-asset [type] [description]`
Quick single-asset generation (texture, mesh, or sound) with inline code.

### `zx-procgen:generate-sfx <type> [output-path]`
Quick SFX generation with NumPy/SciPy. Types: laser, explosion, coin, jump, hit, powerup, footstep, click. Generates a Python script with customizable parameters.

### `zx-procgen:generate-instrument <instrument> [style]`
Generate high-quality instrument samples using advanced synthesis. Examples:
- `zx-procgen:generate-instrument guitar acoustic` - Karplus-Strong acoustic guitar
- `zx-procgen:generate-instrument piano electric` - FM synthesis Rhodes
- `zx-procgen:generate-instrument bass punchy` - Subtractive synth bass
- `zx-procgen:generate-instrument pad warm` - Wavetable string pad
- `zx-procgen:generate-instrument bell tubular` - FM tubular bell

### `zx-procgen:improve-assets [target-tier]`
Interactive quality improvement workflow. Scans assets, assesses current tiers, and guides upgrades to the target tier (Temp, Final, or Hero).

### `zx-procgen:establish-visual-style`
Interactive wizard to establish the visual style for a game project. Creates a style guide specification with color palettes, material presets, and aesthetic guidelines.

### `zx-procgen:generate-all`
Run all procedural generators in a project. Scans for generator scripts and executes them in dependency order.

### `zx-procgen:setup-spec-workflow [asset-type]`
Compatibility alias for installing the unified `.studio/` scaffold (preferred: `ai-studio init`).

### `zx-procgen:migrate-to-specs [generator.py]`
Convert existing Python generator code to the spec-driven format. Analyzes code, extracts parameters into `.spec.py` files, and creates wrappers that use the parsers.

## Spec-Driven Parsers

The unified generator uses parsers installed into `.studio/parsers/` (canonical source: `ai-studio-core/ai_studio_core/templates/project/studio/parsers/`):

| Parser | Spec Format | Purpose |
|--------|-------------|---------|
| `texture.py` | `.texture.spec.py` (TEXTURE) | Layer-based texture generation |
| `sound.py` | `.spec.py` (SOUND/INSTRUMENT) | SFX and instrument synthesis |
| `character.py` | `.spec.py` (CHARACTER) | Character mesh + rig |
| `animation.py` | `.spec.py` (ANIMATION) | Skeletal animation |
| `normal.py` | `.normal.spec.py` (NORMAL) | Normal map patterns |
| `music.py` | `.spec.py` (SONG) | Tracker music (XM/IT) |

**Benefits:**
- Separate configuration from implementation
- AI generates specs, parsers handle complexity
- Easy iteration - just edit parameters
- Reusable across projects

**Locations:**
- Canonical source (core repo): `ai-studio-core/ai_studio_core/templates/project/studio/parsers/`
- Installed into projects: `.studio/parsers/` (via `ai-studio init` or `zx-procgen:init-procgen`)
- Examples: `skills/procedural-*/examples/*.spec.py`

See [PARSER_ROADMAP.md](PARSER_ROADMAP.md) for planned enhancements.

## Output Formats

The asset pipeline accepts standard formats:

| Type | Format | Specs |
|------|--------|-------|
| Textures | PNG | Power of 2, max 512x512 |
| Meshes | OBJ, GLTF | Triangulated, Y-up |
| Sounds | WAV | 22050 Hz, 16-bit mono |

## Integration with Nethercore

Generated assets integrate with the standard workflow:

1. Generate assets to `generated/` directory
2. Reference in `nether.toml`:
```toml
[[assets.textures]]
id = "my-texture"
path = "generated/textures/my-texture.png"
```
3. Run `nether pack` to bundle into ROM
4. Load in game with `rom_texture_str("my-texture")`

## Related

- **zx-dev**: Game development fundamentals
- **sound-design**: Audio design and sonic identity
- **tracker-music**: Tracker module music generation

## License

Part of the Nethercore project.
