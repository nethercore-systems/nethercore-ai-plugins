# Nethercore ZX Orchestrator

Game development orchestrator for Nethercore ZX. Coordinates the full development pipeline across game-design, procgen, and zx-dev plugins.

## Overview

The orchestrator manages end-to-end ZX game development, coordinating three phases:

```
Phase 1: DESIGN (nethercore-zx-game-design)
├── Create Game Design Document
├── Validate console constraints
└── Plan asset requirements
         ↓
Phase 2: ASSETS (nethercore-zx-procgen)
├── Generate textures
├── Generate meshes
├── Generate sounds
└── Generate animations
         ↓
Phase 3: IMPLEMENTATION (nethercore-zx-dev)
├── Scaffold project
├── Implement game logic
└── Build ROM
         ↓
[Playable Game]
```

## Features

- **Human-driven workflow**: Asks for decisions at each major step
- **Cross-plugin coordination**: Seamlessly invokes commands from all ZX plugins
- **Progress tracking**: Maintains project state across development phases
- **Phase transitions**: Guides smooth handoffs between design, assets, and implementation

## Agent

### game-orchestrator

**Trigger phrases:**
- "I want to make a game for ZX"
- "Can you handle the whole process?"
- "Now make the game" (after GDD is complete)
- "What's the workflow for building a ZX game?"
- "How do game-design, procgen, and zx-dev work together?"

**Capabilities:**
- Coordinates full game development pipeline
- Invokes /design-game, /validate-design, /plan-assets from game-design
- Coordinates asset generation with procgen agents
- Scaffolds projects with /new-game from zx-dev
- Tracks progress and manages phase transitions

## Installation

Add to your `.claude/settings.json`:

```json
{
  "plugins": {
    "nethercore-zx-orchestrator@nethercore-ai-plugins": {
      "enabled": true
    }
  }
}
```

## Prerequisites

For full functionality, install all ZX plugins:

- `nethercore-zx-game-design` - GDD creation and constraint validation
- `nethercore-zx-procgen` - Procedural asset generation
- `nethercore-zx-dev` - Project scaffolding and FFI guidance

## Usage

Start by describing your game idea:

```
"I want to make a fighting game for Nethercore ZX. Can you help me through the whole process?"
```

The orchestrator will guide you through:
1. Gathering your game concept
2. Creating a Game Design Document
3. Validating against ZX constraints
4. Planning and generating assets
5. Scaffolding the project
6. Implementing game logic

## License

MIT
