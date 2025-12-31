---
description: Generate asset specifications from GDD for procgen pipeline
argument-hint: "[gdd-path]"
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
  - Task
---

# Asset Planning

Extract asset requirements from a Game Design Document and generate specifications compatible with the zx-procgen plugin.

## Input

GDD file path: $ARGUMENTS

If no path provided, default to: `docs/design/game-design.md`

## Process

### Step 1: Load and Parse GDD

Read the GDD and extract all asset-related information:
- Characters/entities with mesh and texture requirements
- Environments/levels with size and detail estimates
- UI elements and fonts
- Audio (music tracks and sound effects)
- Animation requirements
- Effects and particles

### Step 2: Categorize Assets

Organize assets by type for procgen compatibility:

**Textures**
- Diffuse/Albedo textures
- Material textures (MRE for mode 2, SSE for mode 3)
- UI and sprite textures
- Environment/tileable textures

**Meshes**
- Character meshes (with skeleton if animated)
- Environment geometry
- Props and objects
- Effect meshes

**Audio**
- Sound effects (22,050 Hz, 16-bit mono)
- Music tracks (loop points, duration)

**Animations**
- Character animations (keyframe counts, bone structure)
- Object animations

### Step 3: Determine Procgen Suitability

For each asset, evaluate if it's suitable for procedural generation:

**Good candidates for procgen:**
- Tileable textures (rock, metal, fabric patterns)
- Noise-based backgrounds
- Simple geometric props
- Synthesized sound effects (hits, beeps, ambient)
- Procedural mesh primitives

**Manual creation needed:**
- Character designs with specific art direction
- Unique hero assets
- Story-specific visuals
- Licensed or branded content
- Complex organic meshes

### Step 4: Generate Asset Specification Document

Create `docs/design/asset-specs.md` with:

```markdown
# Asset Specifications

Generated from: [GDD filename]
Date: [timestamp]
Render Mode: [X]

## Summary

| Category | Count | Procgen | Manual | Est. Size |
|----------|-------|---------|--------|-----------|
| Textures | X | Y | Z | X MB |
| Meshes | X | Y | Z | X MB |
| Audio | X | Y | Z | X MB |
| Animations | X | Y | Z | X KB |
| **Total** | | | | X MB |

---

## Textures

### Characters

| Asset | Resolution | Type | Procgen | Notes |
|-------|------------|------|---------|-------|
| player_diffuse | 512×512 | Albedo | No | Hero character |
| player_mre | 256×256 | MRE | No | Material properties |
| ... | | | | |

### Environments

| Asset | Resolution | Type | Procgen | Technique |
|-------|------------|------|---------|-----------|
| rock_tile | 256×256 | Albedo+MRE | Yes | Noise: perlin, fbm |
| metal_floor | 256×256 | Albedo+MRE | Yes | Pattern: grid + noise |
| ... | | | | |

### Procgen Texture Specs

For each procgen texture, provide parameters:

#### rock_tile
- **Technique:** Noise-based stone
- **Base:** Perlin noise, scale 0.1
- **Detail:** FBM 4 octaves
- **Colors:** #5A5A5A → #3A3A3A
- **MRE:** R=0.0, G=0.8, B=0.0

---

## Meshes

### Characters

| Asset | Triangles | Format | Skinned | Procgen |
|-------|-----------|--------|---------|---------|
| player | ~3000 | POS_UV_NORMAL_SKINNED | Yes | No |
| ... | | | | |

### Environment

| Asset | Triangles | Format | Procgen | Technique |
|-------|-----------|--------|---------|-----------|
| rock_cluster | ~200 | POS_UV_NORMAL | Yes | Primitives + noise displacement |
| ... | | | | |

### Procgen Mesh Specs

For each procgen mesh, provide parameters:

#### rock_cluster
- **Base:** Sphere primitive
- **Modifier:** Noise displacement, amplitude 0.3
- **Subdivisions:** 2
- **UV:** Triplanar projection

---

## Audio

### Sound Effects

| Asset | Duration | Procgen | Technique |
|-------|----------|---------|-----------|
| jump | 0.3s | Yes | Synth: sine sweep up |
| hit | 0.2s | Yes | Synth: noise burst + decay |
| explosion | 1.0s | Yes | Synth: layered noise |
| ... | | | |

### Music

| Track | Duration | Loop | Procgen | Notes |
|-------|----------|------|---------|-------|
| main_theme | 60s | Yes | No | Composer needed |
| ... | | | | |

### Procgen Audio Specs

For each procgen sound, provide parameters:

#### jump
- **Waveform:** Sine
- **Frequency:** 200Hz → 600Hz sweep
- **Duration:** 0.3s
- **Envelope:** Attack 0.01s, Decay 0.29s

---

## Animations

### Character Animations

| Character | Animation | Frames | Loop | Notes |
|-----------|-----------|--------|------|-------|
| player | idle | 30 | Yes | Subtle breathing |
| player | walk | 24 | Yes | 8-frame cycle at 60fps |
| ... | | | | |

---

## Procgen Task List

Assets ready for zx-procgen:

### High Priority (blocking)
1. [ ] rock_tile texture (256×256, noise-based)
2. [ ] metal_floor texture (256×256, pattern-based)
3. [ ] jump sound (synth)

### Medium Priority
4. [ ] rock_cluster mesh (procedural primitive)
5. [ ] hit sound (synth)

### Low Priority
6. [ ] ambient_loop sound (synth)

---

## Manual Asset List

Assets requiring manual creation:

### Art Direction Needed
1. [ ] player_diffuse (512×512) - hero character design
2. [ ] player_mre (256×256) - material properties

### Audio Production Needed
1. [ ] main_theme (60s) - composer assignment

```

### Step 5: Integration Guidance

After generating the asset spec, provide guidance:

**For Procgen Assets:**
- Suggest using `/generate-asset` from zx-procgen
- Group similar assets for batch generation
- Note any procgen skill to invoke for specific techniques

**For Manual Assets:**
- Provide clear specifications for artists/audio designers
- Note format requirements (BC7, 22kHz PCM, etc.)
- Include reference images or audio examples if mentioned in GDD

**For Implementation:**
- Note which assets are blocking for prototype
- Suggest asset creation order
- Highlight dependencies (e.g., skeleton before animations)

### Step 6: Save and Report

Save the asset specification to `docs/design/asset-specs.md`

Provide summary:
- Total assets identified
- Procgen vs manual ratio
- Estimated production effort
- Suggested next steps
