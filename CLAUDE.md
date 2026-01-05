# Nethercore AI Plugins

Claude Code plugins for Nethercore fantasy console game development.

## Overview

This repository contains Claude Code plugins for developing games on Nethercore fantasy consoles. Plugins are organized into:

- **Platform-specific** (ZX): Implementation-focused plugins for the ZX console
- **Platform-agnostic**: Conceptual design frameworks applicable to all Nethercore consoles

The plugins provide skills, commands, and agents covering the full game development lifecycle from concept to publication.

## Plugins

### zx-dev

Core game development plugin for Nethercore ZX.

**Skills (6):**
- `zx-game-development` - FFI specifications (Rust/C/Zig), project templates, CLI tooling
- `bindings-fetcher` - Fetch/update FFI bindings from GitHub, proper module organization
- `camera-systems` - 3D camera implementation and perspective-based design patterns
- `rendering-techniques` - Stencil effects, custom fonts, billboard particles
- `debugging-guide` - Debugging and sync testing workflows
- `environment-effects` - Fog, lighting, and atmospheric effects

**Commands:**
- `zx-dev:new-game` - Scaffold a new ZX game project

**Agents:**
- `rollback-reviewer` - Reviews code for GGRS rollback netcode compatibility
- `code-scaffolder` - Generates boilerplate game code for common patterns (player controllers, state machines, entity pools)
- `feature-implementer` - Implements complete game features end-to-end across multiple files and systems
- `integration-assistant` - Connects generated assets to game code with nether.toml and handle constants

### zx-game-design

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
- `zx-game-design:design-game` - Interactive GDD builder wizard
- `zx-game-design:plan-assets` - Generate asset specs from GDD
- `zx-game-design:validate-design` - Validate design against ZX constraints

**Agents:**
- `constraint-analyzer` - Proactively checks design feasibility
- `gdd-generator` - Autonomously generates complete Game Design Documents from concepts
- `mechanic-designer` - Designs detailed game mechanics with physics, timing, and feel parameters
- `scope-advisor` - Assesses project scope, identifies overambition, defines MVPs
- `gdd-implementation-tracker` - Compares GDD to implementation, identifies missing features, prioritizes remaining work

### zx-procgen

Procedural asset generation plugin.

**Skills (13):**
- `procedural-textures` - Texture generation (Albedo, MRE, SSE, Matcaps)
- `procedural-meshes` - 3D mesh generation with UVs and vertex colors
- `procedural-sounds` - Audio synthesis (FM, Karplus-Strong, subtractive) and SFX
- `procedural-instruments` - Instrument sample synthesis for tracker modules
- `procedural-animations` - Walk cycles, attacks, skeletal rigging, IK utilities
- `procedural-sprites` - 2D sprites, pixel art, tilesets, UI elements
- `procedural-characters` - Character mesh generation with rigs (Python specs + Blender bpy)
- `procedural-normal-maps` - Normal map generation (height-to-normal, BC5 format, tangent export)
- `semantic-asset-language` - Style guide for AI-first creative workflows
- `mesh-texturing-workflows` - UV projection techniques
- `asset-quality-tiers` - Tier system (Placeholder→Temp→Final→Hero)
- `native-asset-pipeline` - nether.toml integration, build-time generation
- `generator-patterns` - Common patterns for procedural generation code

**Commands:**
- `zx-procgen:init-procgen` - Initialize .studio/ with unified generator and all parsers
- `zx-procgen:generate-asset` - Quick single-asset generation
- `zx-procgen:generate-sfx` - Quick SFX generation with NumPy/SciPy
- `zx-procgen:generate-instrument` - High-quality instrument sample synthesis
- `zx-procgen:new-asset-project` - Scaffold asset generation project
- `zx-procgen:improve-assets` - Guided quality improvement workflow with tier upgrades
- `zx-procgen:establish-visual-style` - Interactive visual style wizard
- `zx-procgen:generate-all` - Run `python .studio/generate.py` to generate all assets

**Unified Generator:**
All parsers are now modules in `.studio/parsers/`, invoked via `generate.py`:
- `texture.py` - Layer-based texture generation
- `sound.py` - SFX and instrument synthesis
- `character.py` - Character mesh + rig
- `animation.py` - Skeletal animation (was motion_parser.py)
- `normal.py` - Normal map patterns
- `music.py` - Tracker music (XM/IT)

**Agents:**
- `asset-designer` - Translates creative vision to style specs
- `asset-generator` - Produces procedural generation code
- `asset-quality-reviewer` - Validates assets meet ZX budgets and match specs
- `procgen-optimizer` - Optimizes generation code and output
- `creative-orchestrator` - Coordinates full asset pipeline
- `character-designer` - Gathers requirements and produces character specs (.spec.py)
- `character-generator` - Builds character meshes from specs using Blender bpy
- `animation-describer` - Produces structured animation specs (.spec.py) with bone rotations
- `normal-map-generator` - Generates procedural normal maps from patterns or height maps
- `quality-enhancer` - Autonomous asset quality improvement, upgrades assets to higher tiers
- `instrument-architect` - Designs and implements instrument synthesis

### zx-publish

Publishing workflow plugin.

**Skills (2):**
- `publishing-workflow` - ROM packaging and platform upload
- `platform-assets` - Marketing assets (thumbnails, screenshots)

**Commands:**
- `zx-publish:publish-game` - Full publishing workflow
- `zx-publish:prepare-platform-assets` - Generate marketing assets

**Agents:**
- `publish-preparer` - Autonomously prepares games for release (validation, optimization, packaging)
- `release-validator` - Validates all release requirements and identifies blockers

### zx-orchestrator

Meta-orchestration plugin coordinating multi-plugin workflows.

**Skills (2):**
- `agent-registry` - Complete Task tool subagent_type lookup (shared by all orchestrators)
- `project-status` - Session continuity and progress tracking

**Agents:**
- `game-orchestrator` - Coordinates full development pipeline from GDD to published ROM
- `parallel-coordinator` - Analyzes task dependencies and coordinates parallel agent execution

### zx-test

Testing and quality assurance plugin for ZX games.

**Skills (2):**
- `testing-fundamentals` - Sync testing, replay regression, determinism rules
- `benchmarking` - Performance metrics, profiling, state size analysis

**Agents:**
- `test-runner` - Runs sync tests and replay regression tests
- `desync-investigator` - Analyzes sync failures to find non-deterministic code

### zx-optimize

Optimization plugin for ZX games.

**Skills (2):**
- `resource-budgets` - Console limits, budget templates, state sizing
- `optimization-techniques` - WASM, textures, meshes, audio, state optimization

**Agents:**
- `build-analyzer` - Analyzes build output to identify largest assets
- `optimizer` - Applies optimization techniques and reports savings

### zx-cicd

CI/CD automation plugin for ZX games.

**Skills (1):**
- `ci-automation` - GitHub Actions workflows, quality gates, release automation

**Agents:**
- `ci-scaffolder` - Creates `.github/workflows/` with build and release pipelines
- `pipeline-optimizer` - Optimizes CI/CD pipeline performance with caching and parallelization
- `quality-gate-enforcer` - Adds and configures quality checks to prevent bad code from merging

### game-design

Platform-agnostic game design frameworks for fantasy console development. Companion to zx-game-design for conceptual design work.

**Skills (11):**
- `world-building` - World design, lore, factions, geography, consistency
- `character-design` - Player characters, NPCs, antagonists, companions
- `narrative-design` - Story structure, quests, dialogue, environmental storytelling
- `core-loop-design` - Gameplay loops, progression, economy systems
- `level-design` - Flow, pacing, challenge curves, spatial design
- `game-balance` - Difficulty, stat scaling, playtesting frameworks
- `player-psychology` - Motivation, engagement, onboarding, retention
- `genre-patterns` - RPG, platformer, roguelike, metroidvania conventions
- `multiplayer-design` - Co-op, competitive, asymmetric, controller sharing
- `accessibility-ux` - Controls, difficulty options, UI/UX accessibility
- `replayability-engineering` - Run-based design, meta-progression, emergent systems, procedural variety

**Commands:**
- `game-design:worldbuild` - Interactive world building wizard
- `game-design:character` - Character design worksheet wizard
- `game-design:design-loop` - Core loop analysis and design tool
- `game-design:balance-review` - Game balance review framework

**Agents:**
- `design-reviewer` - Reviews GDDs for coherence, completeness, scope
- `genre-advisor` - Suggests genre-appropriate design patterns
- `narrative-generator` - Generates story content, dialogue, lore, and item descriptions
- `balance-analyzer` - Analyzes game balance (stats, difficulty curves, economy)
- `accessibility-auditor` - Audits designs for accessibility barriers and suggests improvements

### creative-direction

Quality assurance and coherence plugin providing "director" level oversight across all disciplines.

**Skills (5):**
- `art-vision` - Visual style bible, color theory, composition, style spectrums
- `sound-vision` - Audio style guide, mixing, sonic identity, adaptive music
- `tech-vision` - Architecture patterns, file splitting, module organization
- `creative-vision` - Creative pillars, experience promise, vision alignment
- `project-memory` - Persistent direction files, session context, ADR templates

**Commands:**
- `creative-direction:establish-vision` - Interactive wizard to establish project creative direction

**Agents:**
- `art-director` - Reviews visual coherence across all assets, validates style consistency
- `sound-director` - Reviews audio coherence, mix balance, sonic identity
- `tech-director` - Reviews architecture, code quality, file size compliance
- `creative-director` - Meta-director for holistic vision alignment, coordinates other directors

**Hooks:**
- PostToolUse file-size guards (warns when files exceed limits)
- SessionStart direction context loading
- Stop checkpoint for documenting decisions

### sound-design

Platform-agnostic game audio design with audio style guide - the audio equivalent of the visual style guide for visual assets.

**Skills (4):**
- `sonic-style-language` - audio style specification: styles, moods, instruments, processing signatures
- `music-composition` - Reference tables: modes, keys by genre, tempos, chord progressions by emotion
- `sfx-design` - Layering patterns, UI sound archetypes, ambient layer recipes
- `audio-integration` - Mix architecture, bus structure, priorities, ducking

**Commands:**
- `sound-design:establish-sonic-identity` - Interactive wizard to create audio style specification
- `sound-design:design-soundtrack` - Design music tracks with structure and harmony
- `sound-design:design-sfx` - Design sound effects with layering specs

**Agents:**
- `sonic-designer` - Translates creative audio intent to audio style specifications
- `sfx-architect` - Designs effects with layers and synthesis code
- `music-architect` - Designs tracks with harmony, structure, and adaptivity
- `audio-coherence-reviewer` - Validates audio consistency with sonic identity

### tracker-music

Platform-agnostic tracker music generation for all Nethercore consoles. Covers XM (FastTracker 2) and IT (Impulse Tracker) formats with programmatic generation.

**Skills (4):**
- `tracker-fundamentals` - Philosophy, polish techniques, when/why to use effects (the "secret sauce")
- `pattern-design` - Song structure, genre templates, loop techniques, channel allocation
- `xm-format` - XM file generation, effects, Python writer library
- `it-format` - IT file generation, NNA, pitch envelopes, filters, Python writer library

**Commands:**
- `tracker-music:generate-song` - Interactive song generation wizard from mood/style description

**Agents:**
- `song-generator` - End-to-end song generation from mood description to polished .xm/.it file

### ai-game-studio

Intelligent game development studio providing request routing, quality analysis, and completion verification across all plugins. Optimized for context efficiency with lean skills and progressive disclosure.

**Skills (4):**
- `request-patterns` - Request classification and agent routing (lean core + references/)
- `dependency-chains` - Task dependencies and blocking relationships (lean core + references/)
- `dispatch-queue` - Session continuity and pending task tracking
- `verification-checklists` - Completion checklists for assets/features/systems (lean core + references/)

**Commands:**
- `ai-game-studio:setup-project` - Complete project setup wizard orchestrating GDD, creative vision, and sonic identity in one flow
- `ai-game-studio:continue` - Resume development from where you left off

**Agents:**
- `request-dispatcher` - Intelligent routing for any development request; parses intent, routes to experts, ensures completion
- `completion-auditor` - Semantic verification that work is complete; catches "generated but not integrated" issues
- `project-health-monitor` - Comprehensive project health assessment; coordinates analysis agents, produces health dashboard
- `next-step-suggester` - Fast, focused next-action recommendations (uses haiku for speed)

**Hooks:**
- SubagentStop verification prompts (ensures follow-up actions aren't forgotten)
- SessionStart health check reminder
- Stop checkpoint for documenting incomplete work

**Key Capabilities:**
- **Intelligent Dispatch:** Parses vague requests like "improve mesh quality" and routes to correct experts
- **Dependency Tracking:** Ensures tasks are completed in correct order (design → generate → integrate)
- **Semantic Verification:** Verifies features actually work, not just that code exists
- **Auto-Dispatch:** Can automatically queue and dispatch fixes for identified issues (with approval)
- **GDD Cross-Reference:** Tracks which GDD features are implemented vs missing
- **Quality Analysis:** Assesses asset quality and identifies improvement opportunities

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
    "zx-dev@nethercore-ai-plugins": true,
    "zx-game-design@nethercore-ai-plugins": true,
    "zx-procgen@nethercore-ai-plugins": true,
    "zx-publish@nethercore-ai-plugins": true,
    "zx-orchestrator@nethercore-ai-plugins": true,
    "zx-test@nethercore-ai-plugins": true,
    "zx-optimize@nethercore-ai-plugins": true,
    "zx-cicd@nethercore-ai-plugins": true,
    "game-design@nethercore-ai-plugins": true,
    "creative-direction@nethercore-ai-plugins": true,
    "sound-design@nethercore-ai-plugins": true,
    "tracker-music@nethercore-ai-plugins": true,
    "ai-game-studio@nethercore-ai-plugins": true
  }
}
```

## License

Licensed under either of:

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT license ([LICENSE-MIT](LICENSE-MIT))

at your option.

## Skill Architecture

### Progressive Disclosure Pattern

Skills follow a **lean core + detailed references** pattern for context efficiency:

```
skill/
├── SKILL.md           # Lean overview (~150-250 lines)
│   └── "Load references when:" directives
└── references/
    ├── topic-a.md     # Detailed implementation (~100-300 lines)
    └── topic-b.md
```

Skill descriptions include loading hints:
```yaml
description: |
  **Load references when:**
  - Platformer physics → `references/platformer-mechanics.md`
  - Combat/damage systems → `references/combat-mechanics.md`
```

### Agent Registry

The `agent-registry` skill provides a single source of truth for all Task tool `subagent_type` values. Orchestrator agents reference this instead of duplicating lookup tables.

### `.studio/` Directory Structure

All plugins write specifications and reports to the `.studio/` directory (committed to git):

```
.studio/
├── generate.py                   # Unified asset generator
├── parsers/                      # Parser modules (copied via /init-procgen)
│   ├── texture.py
│   ├── sound.py
│   ├── character.py
│   ├── animation.py
│   ├── normal.py
│   └── music.py                  # XM/IT writer (optional)
│
├── direction/                    # Creative direction (Markdown)
│   ├── creative.md               # Vision, pillars, audience
│   ├── visual.md                 # Art style, palette, spectrums
│   ├── sonic.md                  # Audio identity, music style
│   └── tech.md                   # Architecture, constraints
│
├── specs/                        # Parsable specifications (*.spec.py)
│   ├── characters/               # Character meshes + rigs
│   ├── textures/                 # Albedo, patterns
│   ├── meshes/                   # Static meshes
│   ├── sounds/                   # SFX synthesis
│   ├── instruments/              # Instrument samples
│   ├── music/                    # Tracker songs (XM/IT)
│   └── animations/               # Skeletal animations
│
├── designs/                      # Human-readable design docs (NOT parsed)
│   ├── mechanics/                # Combat, movement, progression
│   ├── levels/                   # Level layouts, flow
│   └── systems/                  # Inventory, dialogue, etc.
│
├── analysis/                     # Generated reports
│   ├── scope.md                  # Scope assessment
│   ├── coverage.md               # GDD implementation tracking
│   └── quality.md                # Asset quality audit
│
└── status.md                     # Project progress tracking
```

**Key Concepts:**

| Folder | Contains | Purpose |
|--------|----------|---------|
| `specs/` | `*.spec.py` | Machine-parsable Python dicts fed to parsers |
| `designs/` | `*.md` | Human-readable design docs for reference |
| `direction/` | `*.md` | Global creative vision documents |
| `parsers/` | `*.py` | Generation code (copied from plugin) |

**Usage:**
```bash
python .studio/generate.py              # Generate all assets
python .studio/generate.py --only textures  # Generate one category
python .studio/generate.py --dry-run    # Preview changes
```

**Spec-Driven Development:** All specifications use `.spec.py` extension and contain Python dicts that parsers interpret. This ensures:
- Specifications persist across sessions
- Other agents can read and build upon previous work
- Users can review and modify specs directly
- Single `generate.py` command regenerates all assets

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Skill Guidelines

1. **Keep SKILL.md lean** - Target 150-250 lines
2. **Use references/** - Extract detailed code/tables to reference files
3. **Add loading hints** - Use "Load references when:" in descriptions
4. **Reference shared skills** - Use `agent-registry` for agent lookups
