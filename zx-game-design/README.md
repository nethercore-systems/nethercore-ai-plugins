# Nethercore ZX Game Design Plugin

Game design workflow for Nethercore ZX console. Create Game Design Documents (GDDs), validate against console constraints, and plan asset requirements for the procgen plugin.

## Overview

This plugin bridges the gap between game concept and implementation by providing:

- **Constraint-aware design**: Understand what's possible within ZX's 16MB ROM, 4MB RAM limits
- **Modular GDD templates**: Quick, Standard, or Comprehensive documentation
- **Perspective-based patterns**: Side-scroller, Top-down, Third-person, First-person templates
- **Physics & collision**: AABB, SAT, spatial partitioning, and rollback-safe patterns

## Plugin Suite Integration

```
[Game Concept]
      ↓
┌─────────────────────────────────────┐
│  zx-game-design          │  ← This plugin
│  • Validate constraints             │
│  • Create GDD                       │
│  • Plan asset budgets               │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│  zx-procgen              │
│  • Generate textures/meshes         │
│  • Create sounds/animations         │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│  zx-dev                  │
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

### multiplayer-patterns
Auto-triggers on: "multiplayer design", "online play", "netcode", "rollback", "determinism"

GGRS rollback netcode patterns, determinism requirements, and multiplayer testing strategies.

### physics-collision
Auto-triggers on: "collision", "physics", "AABB", "spatial partitioning"

Collision detection patterns, physics systems, and rollback-safe implementations.

### gameplay-mechanics
Auto-triggers on: "movement", "combat", "inventory", "dialogue system"

Movement patterns, combat systems, inventory management, and dialogue trees.

### ui-patterns
Auto-triggers on: "UI", "menus", "HUD", "user interface"

UI/UX design patterns for ZX games including menus, HUDs, and input handling.

### game-feel
Auto-triggers on: "juice", "polish", "game feel", "feedback"

Screen shake, hit pause, particles, and other polish techniques.

### ai-patterns
Auto-triggers on: "AI", "enemy behavior", "pathfinding", "state machine"

FSM, behavior trees, pathfinding algorithms, and enemy AI patterns.

### level-design
Auto-triggers on: "level design", "procedural generation", "tile maps"

Level design patterns, procedural generation, and spatial design.

### save-systems
Auto-triggers on: "save", "load", "serialization", "persistence"

Save/load patterns and state serialization for ZX games.

## Commands

Commands are documented in `plugin:command` form (e.g. `zx-game-design:design-game`). Depending on your Claude/Codex client, they may also appear as slash commands (e.g. `/design-game`).

### zx-game-design:design-game [perspective]
Interactive GDD builder wizard. Walks through the full design process and outputs to `docs/design/`.

```
zx-game-design:design-game side-scroller
zx-game-design:design-game third-person
zx-game-design:design-game  # Interactive selection
```

### zx-game-design:validate-design [file-path]
Check a game design against ZX constraints. Defaults to `docs/design/game-design.md`.

```
zx-game-design:validate-design
zx-game-design:validate-design docs/design/my-game.md
```

### zx-game-design:plan-assets [gdd-path]
Extract asset requirements from GDD and generate specs for the procgen plugin.

```
zx-game-design:plan-assets
zx-game-design:plan-assets docs/design/game-design.md
```

## Agents

### constraint-analyzer
Proactively validates game concepts against ZX limits when constraint issues are detected in conversation.

### gdd-generator
Autonomously generates complete Game Design Documents from brief concepts.

### mechanic-designer
Designs detailed game mechanics with physics, timing, and feel parameters.

### scope-advisor
Assesses project scope, identifies overambition, and helps define MVPs.

### gdd-implementation-tracker
Compares GDD to actual implementation and identifies feature gaps.

> **Note:** For full workflow orchestration across all ZX plugins, use the `zx-orchestrator` plugin.

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
        "path": "zx-game-design"
      }
    }
  },
  "enabledPlugins": {
    "zx-game-design@nethercore-ai-plugins": true
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
    "zx-game-design@nethercore-ai-plugins": true
  }
}
```

## Requirements

For full end-to-end game development, install the complete plugin suite:
- `zx-game-design` - This plugin (design phase)
- `zx-procgen` - Procedural asset generation (asset phase)
- `zx-dev` - Implementation and code scaffolding (implementation phase)
- `zx-orchestrator` - Coordinates the full workflow across all plugins

All plugins are available from the same marketplace.

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

4. For full workflow orchestration, use the orchestrator plugin:
   ```
   "I want to build my game from start to finish"
   ```
   (Requires `zx-orchestrator` plugin)

## Plugin Files

```
zx-game-design/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── README.md                    # This file
├── skills/
│   ├── console-constraints/     # ZX hardware specs
│   ├── game-design-documents/   # GDD templates
│   ├── multiplayer-patterns/    # Netcode patterns
│   ├── physics-collision/       # Physics & collision patterns
│   ├── gameplay-mechanics/      # Combat, platformer, dialogue
│   ├── ui-patterns/             # UI/UX design
│   ├── game-feel/               # Juice and polish
│   ├── ai-patterns/             # AI and behavior
│   ├── level-design/            # Level design patterns
│   └── save-systems/            # Serialization patterns
├── commands/
│   ├── design-game.md           # /design-game
│   ├── validate-design.md       # /validate-design
│   └── plan-assets.md           # /plan-assets
└── agents/
    ├── constraint-analyzer.md   # Validates constraints
    ├── gdd-generator.md         # Generates GDDs
    ├── mechanic-designer.md     # Designs mechanics
    ├── scope-advisor.md         # Scope assessment
    └── gdd-implementation-tracker.md  # Tracks implementation
```

## License

MIT
