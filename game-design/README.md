# Game Design Plugin

Platform-agnostic game design frameworks for Nethercore Systems fantasy consoles. Practical templates, worksheets, and design patterns for solo indie devs, hobbyists, and small teams.

## Overview

This plugin provides conceptual design frameworks that apply across all Nethercore fantasy consoles. It focuses on the **"why"** and **"what"** of game design rather than platform-specific implementation details.

**Target audience:**
- Solo indie developers
- Hobbyists and game jam participants
- Small indie teams (2-5 people)

**Design context:**
- Controller-based gameplay (d-pad, face buttons, triggers)
- Local and online multiplayer (1-4 players, rollback netcode provided)
- Fantasy console constraints encourage focused, creative designs

## Relationship to Other Plugins

```
┌─────────────────────────────────────┐
│  game-design                        │  ← This plugin
│  • Conceptual frameworks            │
│  • Templates and worksheets         │
│  • Design theory and patterns       │
└─────────────────────────────────────┘
              ↓ informs
┌─────────────────────────────────────┐
│  zx-game-design          │  ← Platform-specific
│  • ZX constraint validation         │
│  • Implementation patterns          │
│  • Memory budgets, render modes     │
└─────────────────────────────────────┘
              ↓ feeds into
┌─────────────────────────────────────┐
│  zx-procgen              │
│  zx-dev                  │
└─────────────────────────────────────┘
```

Use `game-design` for conceptual design work, then apply platform-specific plugins for implementation.

## Skills

### world-building
Auto-triggers on: "world design", "lore", "world map", "factions", "cultures"

Frameworks for creating coherent game worlds: geography, history, cultures, factions, and internal consistency rules.

### character-design
Auto-triggers on: "character design", "player character", "NPC design", "antagonist"

Templates for player characters, NPCs, antagonists, and party dynamics. Covers archetypes, progression arcs, and visual design language.

### narrative-design
Auto-triggers on: "story structure", "quest design", "dialogue writing", "branching narrative"

Story structure templates, quest design patterns, and dialogue craft for games with narrative elements.

### core-loop-design
Auto-triggers on: "core loop", "gameplay loop", "progression system", "game economy"

Frameworks for designing engaging core loops, progression systems, economies, and feedback mechanisms.

### level-design
Auto-triggers on: "level design", "level flow", "challenge curve", "player guidance"

Spatial design principles, flow planning, challenge curves, and teaching-through-design techniques.

### game-balance
Auto-triggers on: "game balance", "difficulty curve", "stat scaling", "playtesting"

Difficulty curve templates, stat scaling worksheets, and systematic playtesting methodologies.

### player-psychology
Auto-triggers on: "player motivation", "player types", "engagement", "onboarding"

Understanding player motivations, engagement patterns, onboarding design, and flow state optimization.

### genre-patterns
Auto-triggers on: "RPG design", "platformer design", "roguelike", "metroidvania"

Genre-specific design conventions and templates for RPG, platformer, roguelike, metroidvania, action, puzzle, and adventure games.

### multiplayer-design
Auto-triggers on: "multiplayer design", "co-op design", "competitive design", "local multiplayer"

Frameworks for co-op and competitive design, controller sharing patterns, and asymmetric multiplayer.

### accessibility-ux
Auto-triggers on: "accessibility", "control scheme", "difficulty options", "UI design"

Controller mapping templates, difficulty options frameworks, and accessibility best practices.

### replayability-engineering
Auto-triggers on: "replayability", "roguelike design", "meta-progression", "procedural generation", "emergent gameplay"

Comprehensive frameworks for run-based design, meta-progression, emergent systems, procedural variety, and randomness design. The "force multiplier" patterns that let small teams create games with massive replay value.

## Commands

### /worldbuild [scope]
Interactive world building wizard. Generates a structured world design document.

```
/worldbuild           # Interactive scope selection
/worldbuild small     # Contained world (single location)
/worldbuild medium    # Regional world (multiple areas)
/worldbuild large     # Expansive world (multiple regions)
```

### /character [type]
Character design worksheet wizard.

```
/character player      # Player character design
/character npc         # NPC design
/character antagonist  # Villain/antagonist design
/character party       # Party/companion design
```

### /design-loop
Core loop analysis and design tool. Maps your game's core loop, progression systems, and feedback mechanisms.

```
/design-loop
```

### /balance-review [target]
Game balance review framework. Analyzes difficulty curves, stat scaling, and economy balance.

```
/balance-review                           # Review current project
/balance-review docs/design/game.md       # Review specific document
```

## Agents

### design-reviewer
Proactively reviews game designs for coherence, missing elements, and scope issues. Triggers after GDD creation or when reviewing game concepts.

### genre-advisor
Suggests genre-appropriate patterns based on game concepts. Helps identify which design conventions apply to your game idea.

## Output Location

All design documents are saved to `docs/design/` by default:
```
project/
└── docs/
    └── design/
        ├── world-design.md
        ├── core-loop.md
        └── characters/
            └── [character-name].md
```

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
        "path": "game-design"
      }
    }
  },
  "enabledPlugins": {
    "game-design@nethercore-ai-plugins": true
  }
}
```

### From Local Directory (Nethercore Workspace)

If working within the nethercore-project workspace:

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
    "game-design@nethercore-ai-plugins": true
  }
}
```

## Quick Start

1. Start with world building:
   ```
   /worldbuild
   ```

2. Design your core loop:
   ```
   /design-loop
   ```

3. Create characters:
   ```
   /character player
   ```

4. Review your design:
   ```
   Ask: "Review my game design for coherence"
   ```

## License

MIT/Apache-2.0
