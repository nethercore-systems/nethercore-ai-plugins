# Nethercore AI Plugins

Official AI-powered development plugins for Nethercore game development. Currently supports Claude Code, with potential for other AI tools in the future.

## Available Plugins

| Plugin | Description | Skills |
|--------|-------------|--------|
| [nethercore-zx-dev](./nethercore-zx-dev/) | Core game development - FFI specs, cameras, rendering | 5 |
| [nethercore-zx-game-design](./nethercore-zx-game-design/) | Game design workflow - GDDs, multiplayer, mechanics | 10 |
| [nethercore-zx-procgen](./nethercore-zx-procgen/) | Procedural asset generation - textures, meshes, sounds | 10 |
| [nethercore-zx-publish](./nethercore-zx-publish/) | Publishing workflow - ROM packaging, platform upload | 2 |
| [nethercore-zx-orchestrator](./nethercore-zx-orchestrator/) | Meta-orchestration - coordinates full pipeline | 0 |
| [nethercore-zx-test](./nethercore-zx-test/) | Testing and QA - sync tests, replay regression | 2 |
| [nethercore-zx-optimize](./nethercore-zx-optimize/) | Optimization - resource budgets, performance tuning | 2 |
| [nethercore-zx-cicd](./nethercore-zx-cicd/) | CI/CD automation - GitHub Actions, quality gates | 1 |
| [game-design](./game-design/) | Platform-agnostic design - world building, narrative | 11 |

## Installation

### Global Installation (Recommended)

Add to your global Claude settings (`~/.claude/settings.json` on macOS/Linux, `%USERPROFILE%\.claude\settings.json` on Windows):

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
    "nethercore-zx-dev@nethercore-ai-plugins": true,
    "nethercore-zx-game-design@nethercore-ai-plugins": true,
    "nethercore-zx-procgen@nethercore-ai-plugins": true,
    "nethercore-zx-publish@nethercore-ai-plugins": true,
    "nethercore-zx-orchestrator@nethercore-ai-plugins": true,
    "nethercore-zx-test@nethercore-ai-plugins": true,
    "nethercore-zx-optimize@nethercore-ai-plugins": true,
    "nethercore-zx-cicd@nethercore-ai-plugins": true,
    "game-design@nethercore-ai-plugins": true
  }
}
```

### Workspace Installation

For nethercore contributors who have cloned the workspace, add to `.claude/settings.local.json`:

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
    "nethercore-zx-dev@nethercore-ai-plugins": true,
    "nethercore-zx-game-design@nethercore-ai-plugins": true,
    "nethercore-zx-procgen@nethercore-ai-plugins": true,
    "nethercore-zx-publish@nethercore-ai-plugins": true,
    "nethercore-zx-orchestrator@nethercore-ai-plugins": true,
    "nethercore-zx-test@nethercore-ai-plugins": true,
    "nethercore-zx-optimize@nethercore-ai-plugins": true,
    "nethercore-zx-cicd@nethercore-ai-plugins": true,
    "game-design@nethercore-ai-plugins": true
  }
}
```

## Quick Start

Once installed, you can start building ZX games anywhere:

```
/new-game rust my-game    # Create a new Rust game project
cd my-game
nether run                # Build and launch
```

## Plugin Details

### nethercore-zx-dev

Core game development plugin for Nethercore ZX.

**Skills (5):**
- `zx-game-development` - FFI specifications, project templates, CLI tooling
- `camera-systems` - 3D camera implementation and perspective-based design
- `rendering-techniques` - Stencil effects, custom fonts, billboard particles
- `debugging-guide` - Debugging and sync testing workflows
- `environment-effects` - Fog, lighting, and atmospheric effects

**Commands:**
- `/new-game` - Scaffold a new ZX game project

**Agents:**
- `rollback-reviewer` - Reviews code for GGRS rollback netcode compatibility

### nethercore-zx-game-design

Game design workflow plugin.

**Skills (10):**
- `game-design-documents` - GDD templates and examples
- `console-constraints` - ZX hardware limits and budgets
- `multiplayer-patterns` - Netcode, determinism, viewport management, split-screen
- `physics-collision` - Collision detection patterns
- `gameplay-mechanics` - Movement, combat, inventory, dialogue
- `ui-patterns` - UI/UX design for ZX
- `game-feel` - Juice, polish, and feedback
- `save-systems` - Serialization and save patterns
- `ai-patterns` - FSM, pathfinding, behavior trees
- `level-design` - Level design patterns and procedural generation

**Commands:**
- `/design-game` - Interactive GDD builder wizard
- `/plan-assets` - Generate asset specs from GDD
- `/validate-design` - Validate design against ZX constraints

**Agents:**
- `constraint-analyzer` - Proactively checks design feasibility

### nethercore-zx-procgen

Procedural asset generation plugin.

**Skills (10):**
- `procedural-textures` - Texture generation (Albedo, MRE, SSE, Matcaps)
- `procedural-meshes` - 3D mesh generation with UVs and vertex colors
- `procedural-sounds` - Audio synthesis and SFX
- `procedural-music` - XM tracker music composition
- `procedural-animations` - Walk cycles, attacks, locomotion
- `procedural-sprites` - 2D sprites, pixel art, tilesets, UI elements
- `skeletal-rigging` - Bone weights and skinning
- `mocap-integration` - BVH parsing and retargeting
- `semantic-asset-language` - SADL for AI-first creative workflows
- `mesh-texturing-workflows` - UV projection techniques

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

**Skills (2):**
- `publishing-workflow` - ROM packaging and platform upload
- `platform-assets` - Marketing assets (thumbnails, screenshots)

**Commands:**
- `/publish-game` - Full publishing workflow
- `/prepare-platform-assets` - Generate marketing assets

### nethercore-zx-orchestrator

Meta-orchestration plugin coordinating multi-plugin workflows.

**Agents:**
- `game-orchestrator` - Coordinates full development pipeline from GDD to playable ROM

### nethercore-zx-test

Testing and quality assurance plugin for ZX games.

**Skills (2):**
- `testing-fundamentals` - Sync testing, replay regression, determinism rules
- `benchmarking` - Performance metrics, profiling, state size analysis

**Agents:**
- `test-runner` - Runs sync tests and replay regression tests
- `desync-investigator` - Analyzes sync failures to find non-deterministic code

### nethercore-zx-optimize

Optimization plugin for ZX games.

**Skills (2):**
- `resource-budgets` - Console limits, budget templates, state sizing
- `optimization-techniques` - WASM, textures, meshes, audio, state optimization

**Agents:**
- `build-analyzer` - Analyzes build output to identify largest assets
- `optimizer` - Applies optimization techniques and reports savings

### nethercore-zx-cicd

CI/CD automation plugin for ZX games.

**Skills (1):**
- `ci-automation` - GitHub Actions workflows, quality gates, release automation

**Agents:**
- `ci-scaffolder` - Creates `.github/workflows/` with build and release pipelines

### game-design

Platform-agnostic game design frameworks for fantasy console development.

**Skills (11):**
- `world-building` - World design, lore, factions, geography
- `character-design` - Player characters, NPCs, antagonists
- `narrative-design` - Story structure, quests, dialogue
- `core-loop-design` - Gameplay loops, progression, economy
- `level-design` - Flow, pacing, challenge curves
- `game-balance` - Difficulty, stat scaling, playtesting
- `player-psychology` - Motivation, engagement, onboarding
- `genre-patterns` - RPG, platformer, roguelike conventions
- `multiplayer-design` - Co-op, competitive, asymmetric
- `accessibility-ux` - Controls, difficulty options, UI/UX
- `replayability-engineering` - Run-based design, meta-progression

**Commands:**
- `/worldbuild` - Interactive world building wizard
- `/character` - Character design worksheet wizard
- `/design-loop` - Core loop analysis and design tool
- `/balance-review` - Game balance review framework

**Agents:**
- `design-reviewer` - Reviews GDDs for coherence, completeness, scope
- `genre-advisor` - Suggests genre-appropriate design patterns

## Contributing

Plugins are developed in this repository. Each plugin has its own directory with:
- `.claude-plugin/plugin.json` - Plugin manifest
- `skills/` - Auto-triggering knowledge skills
- `commands/` - Slash commands
- `agents/` - Specialized sub-agents

## License

Licensed under either of:

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT license ([LICENSE-MIT](LICENSE-MIT))

at your option.
