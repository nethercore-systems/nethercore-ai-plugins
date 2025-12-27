# Nethercore AI Plugins

Claude Code plugins for Nethercore ZX game development.

## Overview

This repository contains a collection of Claude Code plugins that assist with developing games for the Nethercore ZX fantasy console. The plugins provide skills, commands, and agents covering the full game development lifecycle.

## Plugins

### nethercore-zx-dev

Core game development plugin for Nethercore ZX.

**Skills:**
- `zx-game-development` - FFI specifications (Rust/C/Zig), project templates, CLI tooling
- `camera-systems` - 3D camera implementation patterns
- `debugging-guide` - Debugging and sync testing workflows
- `environment-effects` - Fog, lighting, and atmospheric effects
- `stencil-effects` - Stencil buffer techniques
- `custom-fonts` - Font rendering and text display
- `billboard-particles` - 3D billboards and particle systems

**Commands:**
- `/new-game` - Scaffold a new ZX game project

**Agents:**
- `rollback-reviewer` - Reviews code for GGRS rollback netcode compatibility

### nethercore-zx-game-design

Game design workflow plugin.

**Skills:**
- `game-design-documents` - GDD templates and examples
- `console-constraints` - ZX hardware limits and budgets
- `multiplayer-design` - Netplay patterns and determinism
- `multiplayer-rendering` - Split-screen and viewport layouts
- `perspective-patterns` - Camera and perspective design
- `physics-collision` - Collision detection patterns
- `gameplay-mechanics` - Movement, combat, inventory, dialogue
- `ui-patterns` - UI/UX design for ZX
- `game-feel` - Juice, polish, and feedback
- `save-systems` - Serialization and save patterns
- `ai-patterns` - FSM, pathfinding, behavior trees
- `split-screen-rendering` - Multi-viewport rendering
- `level-design` - Level design patterns and procedural generation

**Commands:**
- `/design-game` - Interactive GDD builder wizard
- `/plan-assets` - Generate asset specs from GDD
- `/validate-design` - Validate design against ZX constraints

**Agents:**
- `constraint-analyzer` - Proactively checks design feasibility

### nethercore-zx-procgen

Procedural asset generation plugin.

**Skills:**
- `procedural-textures` - Texture generation (Albedo, MRE, SSE, Matcaps)
- `procedural-meshes` - 3D mesh generation with UVs and vertex colors
- `procedural-sounds` - Audio synthesis and SFX
- `procedural-music` - XM tracker music composition
- `procedural-animations` - Walk cycles, attacks, locomotion
- `procedural-sprites` - 2D sprites, pixel art, tilesets, UI elements
- `skeletal-rigging` - Bone weights and skinning
- `mocap-integration` - BVH parsing and retargeting
- `advanced-techniques` - Algorithm selection and quality benchmarks
- `semantic-asset-language` - SADL for AI-first creative workflows
- `retro-3d-assets` - Low-poly and pixel art 3D styles
- `mesh-texturing-workflows` - UV projection techniques
- `character-pipeline` - Full character creation workflow

**Commands:**
- `/generate-asset` - Quick single-asset generation
- `/new-asset-project` - Scaffold asset generation project

**Agents:**
- `asset-designer` - Translates creative vision to SADL specs
- `asset-generator` - Produces procedural generation code
- `asset-critic` - Reviews asset quality against specs
- `asset-quality-reviewer` - Validates assets meet ZX budgets
- `procgen-optimizer` - Optimizes generation code and output
- `creative-orchestrator` - Coordinates full asset pipeline
- `character-generator` - End-to-end character creation

### nethercore-zx-publish

Publishing workflow plugin.

**Skills:**
- `publishing-workflow` - ROM packaging and platform upload
- `platform-assets` - Marketing assets (thumbnails, screenshots)

**Commands:**
- `/publish-game` - Full publishing workflow
- `/prepare-platform-assets` - Generate marketing assets

### nethercore-zx-orchestrator

Meta-orchestration plugin coordinating multi-plugin workflows.

**Agents:**
- `game-orchestrator` - Coordinates full development pipeline

## Installation

Add to your `.claude/settings.local.json`:

```json
{
  "extraKnownMarketplaces": {
    "nethercore-ai-plugins": {
      "source": {
        "source": "github",
        "repo": "nethercore-systems/nethercore-ai-plugins",
        "path": "."
      }
    }
  },
  "enabledPlugins": {
    "nethercore-zx-dev@nethercore-ai-plugins": true,
    "nethercore-zx-game-design@nethercore-ai-plugins": true,
    "nethercore-zx-procgen@nethercore-ai-plugins": true,
    "nethercore-zx-publish@nethercore-ai-plugins": true,
    "nethercore-zx-orchestrator@nethercore-ai-plugins": true
  }
}
```

## License

Licensed under either of:

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT license ([LICENSE-MIT](LICENSE-MIT))

at your option.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
