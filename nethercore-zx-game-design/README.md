# Nethercore ZX Game Design Plugin

Game design workflow for Nethercore ZX console. Create Game Design Documents (GDDs), validate against console constraints, and orchestrate full game development across the nethercore plugin suite.

## Overview

This plugin bridges the gap between game concept and implementation by providing:

- **Constraint-aware design**: Understand what's possible within ZX's 16MB ROM, 4MB RAM limits
- **Modular GDD templates**: Quick, Standard, or Comprehensive documentation
- **Perspective-based patterns**: Side-scroller, Top-down, Third-person, First-person templates
- **Full orchestration**: Coordinate design → procgen assets → zx-dev implementation

## Plugin Suite Integration

```
[Game Concept]
      ↓
┌─────────────────────────────────────┐
│  nethercore-zx-game-design          │  ← This plugin
│  • Validate constraints             │
│  • Create GDD                       │
│  • Plan asset budgets               │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│  nethercore-zx-procgen              │
│  • Generate textures/meshes         │
│  • Create sounds/animations         │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│  nethercore-zx-dev                  │
│  • Scaffold project                 │
│  • Implement game logic             │
│  • Validate rollback safety         │
└─────────────────────────────────────┘
      ↓
[Playable Game]
```

## Skills

### console-constraints
Auto-triggers on: "ZX capabilities", "memory limits", "render mode", "console specs"

Provides comprehensive knowledge of ZX hardware constraints including display, memory, audio, and input specifications.

### game-design-documents
Auto-triggers on: "game design document", "GDD", "design my game"

Guidance for creating modular GDDs at three depth levels:
- **Quick** (1 page): Core concept, constraints, asset list
- **Standard** (3-5 pages): Mechanics, levels, render mode, memory budget
- **Comprehensive** (full doc): All sections including narrative, multiplayer, milestones

### multiplayer-design
Auto-triggers on: "multiplayer design", "online play", "netcode", "rollback", "determinism"

GGRS rollback netcode patterns, determinism requirements, and multiplayer testing strategies.

### perspective-patterns
Auto-triggers on: "side-scroller", "top-down", "third-person", "first-person", "camera style"

Camera/perspective-based design templates with render mode recommendations, memory budgets, and control schemes.

## Commands

### /design-game [perspective]
Interactive GDD builder wizard. Walks through the full design process and outputs to `docs/design/`.

```
/design-game side-scroller
/design-game third-person
/design-game  # Interactive selection
```

### /validate-design [file-path]
Check a game design against ZX constraints. Defaults to `docs/design/game-design.md`.

```
/validate-design
/validate-design docs/design/my-game.md
```

### /plan-assets [gdd-path]
Extract asset requirements from GDD and generate specs for the procgen plugin.

```
/plan-assets
/plan-assets docs/design/game-design.md
```

## Agents

### constraint-analyzer
Proactively validates game concepts against ZX limits when constraint issues are detected in conversation.

### game-orchestrator
Coordinates full agentic game development workflow across all three nethercore plugins.

## Output Location

All design documents are saved to `docs/design/` by default.

## Installation

### From GitHub (External Projects)

Add to your project's `.claude/settings.local.json`:

```json
{
  "extraKnownMarketplaces": {
    "nethercore-ai-plugins": {
      "source": {
        "source": "github",
        "repo": "nethercore-systems/nethercore-ai-plugins",
        "path": "nethercore-zx-game-design"
      }
    }
  },
  "enabledPlugins": {
    "nethercore-zx-game-design@nethercore-ai-plugins": true
  }
}
```

### From Local Directory (Nethercore Workspace)

If working within the nethercore-project workspace, the plugin is pre-configured:

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
    "nethercore-zx-game-design@nethercore-ai-plugins": true
  }
}
```

## Requirements

For full orchestration, install the complete plugin suite:
- `nethercore-zx-game-design` - This plugin (design phase)
- `nethercore-zx-procgen` - Procedural asset generation (asset phase)
- `nethercore-zx-dev` - Implementation and code scaffolding (implementation phase)

All three plugins are available from the same marketplace.

## Quick Start

1. Start a new game design:
   ```
   /design-game
   ```

2. Validate your design against ZX constraints:
   ```
   /validate-design
   ```

3. Generate asset specifications for procgen:
   ```
   /plan-assets
   ```

4. Let the game-orchestrator coordinate the full workflow:
   ```
   "I want to build my game agentically"
   ```

## Plugin Files

```
nethercore-zx-game-design/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── README.md                    # This file
├── skills/
│   ├── console-constraints/     # ZX hardware specs
│   ├── game-design-documents/   # GDD templates
│   ├── multiplayer-design/      # Netcode patterns
│   └── perspective-patterns/    # Camera/view patterns
├── commands/
│   ├── design-game.md           # /design-game
│   ├── validate-design.md       # /validate-design
│   └── plan-assets.md           # /plan-assets
└── agents/
    ├── constraint-analyzer.md   # Validates constraints
    └── game-orchestrator.md     # Full workflow coordination
```

## License

MIT
