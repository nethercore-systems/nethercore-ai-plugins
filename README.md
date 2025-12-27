# Nethercore AI Plugins

Official AI-powered development plugins for Nethercore game development. Currently supports Claude Code, with potential for other AI tools in the future.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [nethercore-zx-dev](./nethercore-zx-dev/) | Core game development - FFI specs, project templates, debugging |
| [nethercore-zx-game-design](./nethercore-zx-game-design/) | Game design workflow - GDDs, constraints, multiplayer patterns |
| [nethercore-zx-procgen](./nethercore-zx-procgen/) | Procedural asset generation - textures, meshes, sounds, animations |
| [nethercore-zx-publish](./nethercore-zx-publish/) | Publishing workflow - ROM packaging, platform upload |
| [nethercore-zx-orchestrator](./nethercore-zx-orchestrator/) | Meta-orchestration - coordinates full development pipeline |

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
    "nethercore-zx-orchestrator@nethercore-ai-plugins": true
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
    "nethercore-zx-orchestrator@nethercore-ai-plugins": true
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

**Skills:** `zx-game-development`, `camera-systems`, `debugging-guide`, `environment-effects`, `stencil-effects`, `custom-fonts`

**Commands:**
- `/new-game` - Scaffold a new ZX game project

**Agents:**
- `rollback-reviewer` - Reviews code for GGRS rollback netcode compatibility

### nethercore-zx-game-design

Game design workflow plugin.

**Skills:** `game-design-documents`, `console-constraints`, `multiplayer-design`, `multiplayer-rendering`, `perspective-patterns`, `physics-collision`, `gameplay-mechanics`, `ui-patterns`, `game-feel`, `save-systems`, `ai-patterns`, `split-screen-rendering`

**Commands:**
- `/design-game` - Interactive GDD builder wizard
- `/plan-assets` - Generate asset specs from GDD
- `/validate-design` - Validate design against ZX constraints

**Agents:**
- `constraint-analyzer` - Proactively checks design feasibility

### nethercore-zx-procgen

Procedural asset generation plugin.

**Skills:** `procedural-textures`, `procedural-meshes`, `procedural-sounds`, `procedural-music`, `procedural-animations`, `skeletal-rigging`, `mocap-integration`, `advanced-techniques`, `semantic-asset-language`, `retro-3d-assets`, `mesh-texturing-workflows`, `character-pipeline`

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

**Skills:** `publishing-workflow`, `platform-assets`

**Commands:**
- `/publish-game` - Full publishing workflow
- `/prepare-platform-assets` - Generate marketing assets

### nethercore-zx-orchestrator

Meta-orchestration plugin coordinating multi-plugin workflows.

**Agents:**
- `game-orchestrator` - Coordinates full development pipeline from GDD to playable ROM

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
