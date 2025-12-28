# Nethercore ZX Orchestrator

Game development orchestrator for Nethercore ZX. Coordinates the full development pipeline across all nethercore plugins - from creative vision through published game.

## Overview

The orchestrator manages end-to-end ZX game development across 7 phases:

```
Phase 0: CREATIVE FOUNDATION (creative-direction, sound-design)
├── Establish creative vision
├── Define audio direction (SSL)
└── Validate vision coherence
         ↓
Phase 1: DESIGN (game-design, nethercore-zx-game-design)
├── World building, character design
├── Create Game Design Document
├── Validate ZX constraints
└── Plan asset requirements
         ↓
Phase 2: VISUAL ASSETS (nethercore-zx-procgen)
├── Generate textures
├── Generate meshes
├── Generate characters
└── Art direction review
         ↓
Phase 3: AUDIO ASSETS (sound-design)
├── Compose music tracks
├── Synthesize sound effects
└── Audio direction review
         ↓
Phase 4: IMPLEMENTATION (nethercore-zx-dev)
├── Scaffold project
├── Implement game systems
├── Integrate assets
└── Technical review
         ↓
Phase 5: TESTING & OPTIMIZATION (nethercore-zx-test, nethercore-zx-optimize)
├── Sync tests
├── Build analysis
└── Apply optimizations
         ↓
Phase 6: PUBLISH (nethercore-zx-publish, nethercore-zx-cicd)
├── Marketing assets
├── ROM packaging
├── Platform upload
└── CI/CD setup
         ↓
[Published Game on nethercore.systems]
```

## Features

- **Human-driven workflow**: Asks for decisions at each major step
- **7-phase pipeline**: Full coverage from vision to publication
- **Quality checkpoints**: Director agents review at each phase transition
- **Cross-plugin coordination**: Invokes commands and agents from all 9 plugins
- **Progress tracking**: Maintains project state in `.claude/project-status.md`
- **Session continuity**: Resume from where you left off across sessions
- **Parallel coordination**: Run independent tasks concurrently for faster development

## Commands

### /orchestrate

Launch the orchestrator with optional action:

```bash
/orchestrate           # Check status or start
/orchestrate start     # Begin new project
/orchestrate continue  # Resume existing project
/orchestrate status    # Show progress
/orchestrate review    # Run quality checkpoints
/orchestrate design    # Jump to design phase
/orchestrate audio     # Jump to audio phase
/orchestrate publish   # Jump to publish phase
```

## Agents

### game-orchestrator

**Trigger phrases:**
- "I want to make a game for ZX"
- "Can you handle the whole process?"
- "Now make the game" (after GDD)
- "What's the workflow for building a ZX game?"
- "How do the plugins work together?"

**Capabilities:**
- Coordinates full 7-phase game development pipeline
- Invokes commands from all plugins
- Delegates to specialized agents for each phase
- Tracks progress and manages phase transitions
- Runs quality checkpoints with director agents

### parallel-coordinator

**Trigger phrases:**
- "Run these in parallel"
- "Do these tasks simultaneously"
- "Speed up development"

**Capabilities:**
- Analyzes task dependencies
- Launches independent tasks concurrently
- Tracks parallel execution progress
- Aggregates results from multiple agents

## Skills

### agent-registry

Complete registry of all available agents with their fully-qualified subagent_type identifiers. Essential for Task tool invocation patterns.

**Trigger phrases:**
- "How do I spawn agents?"
- "What agents are available?"
- "Agent registry"
- "Subagent types"

**Use this skill when:**
- You need to know the correct subagent_type for an agent
- You want to see all available agents organized by plugin
- You need to understand parallel execution patterns

## Quality Review Checkpoints

| Checkpoint | After Phase | Agents |
|------------|-------------|--------|
| Vision Check | Creative Foundation | creative-director |
| Design Review | Design | design-reviewer, accessibility-auditor |
| Art Review | Visual Assets | art-director, asset-quality-reviewer |
| Audio Review | Audio Assets | sound-director |
| Tech Review | Implementation | tech-director, rollback-reviewer |
| Release Review | Pre-Publish | release-validator, creative-director |

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

For full functionality, install all nethercore plugins:

| Plugin | Purpose |
|--------|---------|
| `creative-direction` | Vision, art/sound/tech direction |
| `sound-design` | Audio direction, music, SFX |
| `game-design` | World building, characters, narrative |
| `nethercore-zx-game-design` | GDD, constraints, multiplayer |
| `nethercore-zx-procgen` | Procedural asset generation |
| `nethercore-zx-dev` | Project scaffolding, FFI |
| `nethercore-zx-test` | Sync testing, regression |
| `nethercore-zx-optimize` | Build analysis, optimization |
| `nethercore-zx-publish` | Marketing assets, ROM packaging |
| `nethercore-zx-cicd` | GitHub Actions, quality gates |

## Usage

Start by describing your game idea:

```
"I want to make a fighting game for Nethercore ZX. Can you help me through the whole process?"
```

The orchestrator will guide you through:
1. Establishing creative vision and audio direction
2. Building the world and characters
3. Creating a Game Design Document
4. Validating against ZX constraints
5. Generating visual assets
6. Composing audio assets
7. Scaffolding and implementing the project
8. Testing and optimizing
9. Publishing to nethercore.systems

## Session Continuity

The orchestrator persists progress to `.claude/project-status.md`. When you start a new session, it automatically:

1. Detects existing project state
2. Summarizes where you left off
3. Asks if you want to continue

This ensures seamless development across multiple sessions.

## License

MIT/Apache-2.0
