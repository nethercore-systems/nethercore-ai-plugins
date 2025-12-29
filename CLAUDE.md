# Nethercore AI Plugins

Claude Code plugins for Nethercore fantasy console game development.

## Overview

This repository contains Claude Code plugins for developing games on Nethercore fantasy consoles. Plugins are organized into:

- **Platform-specific** (ZX): Implementation-focused plugins for the ZX console
- **Platform-agnostic**: Conceptual design frameworks applicable to all Nethercore consoles

The plugins provide skills, commands, and agents covering the full game development lifecycle from concept to publication.

## Plugins

### nethercore-zx-dev

Core game development plugin for Nethercore ZX.

**Skills (6):**
- `zx-game-development` - FFI specifications (Rust/C/Zig), project templates, CLI tooling
- `bindings-fetcher` - Fetch/update FFI bindings from GitHub, proper module organization
- `camera-systems` - 3D camera implementation and perspective-based design patterns
- `rendering-techniques` - Stencil effects, custom fonts, billboard particles
- `debugging-guide` - Debugging and sync testing workflows
- `environment-effects` - Fog, lighting, and atmospheric effects

**Commands:**
- `/new-game` - Scaffold a new ZX game project

**Agents:**
- `rollback-reviewer` - Reviews code for GGRS rollback netcode compatibility
- `code-scaffolder` - Generates boilerplate game code for common patterns (player controllers, state machines, entity pools)
- `feature-implementer` - Implements complete game features end-to-end across multiple files and systems
- `integration-assistant` - Connects generated assets to game code with nether.toml and handle constants

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
- `gdd-generator` - Autonomously generates complete Game Design Documents from concepts
- `mechanic-designer` - Designs detailed game mechanics with physics, timing, and feel parameters
- `scope-advisor` - Assesses project scope, identifies overambition, defines MVPs
- `gdd-implementation-tracker` - Compares GDD to implementation, identifies missing features, prioritizes remaining work

### nethercore-zx-procgen

Procedural asset generation plugin.

**Skills (11):**
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
- `asset-quality-tiers` - Tier system (Placeholder→Temp→Final→Hero) and enhancement strategies

**Commands:**
- `/generate-asset` - Quick single-asset generation
- `/new-asset-project` - Scaffold asset generation project
- `/improve-assets` - Guided quality improvement workflow with tier upgrades

**Agents:**
- `asset-designer` - Translates creative vision to SADL specs
- `asset-generator` - Produces procedural generation code
- `asset-critic` - Reviews asset quality against specs
- `asset-quality-reviewer` - Validates assets meet ZX budgets
- `procgen-optimizer` - Optimizes generation code and output
- `creative-orchestrator` - Coordinates full asset pipeline
- `character-generator` - End-to-end character creation
- `quality-analyzer` - Holistic asset quality assessment with actionable recommendations and auto-dispatch support
- `quality-enhancer` - Autonomous asset quality improvement, upgrades assets to higher tiers

### nethercore-zx-publish

Publishing workflow plugin.

**Skills (2):**
- `publishing-workflow` - ROM packaging and platform upload
- `platform-assets` - Marketing assets (thumbnails, screenshots)

**Commands:**
- `/publish-game` - Full publishing workflow
- `/prepare-platform-assets` - Generate marketing assets

**Agents:**
- `publish-preparer` - Autonomously prepares games for release (validation, optimization, packaging)
- `release-validator` - Validates all release requirements and identifies blockers

### nethercore-zx-orchestrator

Meta-orchestration plugin coordinating multi-plugin workflows.

**Agents:**
- `game-orchestrator` - Coordinates full development pipeline from GDD to published ROM
- `parallel-coordinator` - Analyzes task dependencies and coordinates parallel agent execution

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
- `/worldbuild` - Interactive world building wizard
- `/character` - Character design worksheet wizard
- `/design-loop` - Core loop analysis and design tool
- `/balance-review` - Game balance review framework

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
- `/establish-vision` - Interactive wizard to establish project creative direction

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

Platform-agnostic game audio design with Sonic Style Language (SSL) - the audio equivalent of SADL for visual assets.

**Skills (5):**
- `sonic-style-language` - SSL specification: styles, moods, instruments, processing signatures
- `synthesis-techniques` - FM, wavetable, granular, physical modeling, Karplus-Strong
- `music-composition` - Theory, chord progressions, structure, adaptive music, leitmotifs
- `sfx-design` - Layering, archetypes, impact design, UI audio, variation
- `audio-integration` - Mix architecture, priorities, spatial audio, ducking, states

**Commands:**
- `/establish-sonic-identity` - Interactive wizard to create SSL specification
- `/design-soundtrack` - Design music tracks with structure and harmony
- `/design-sfx` - Design sound effects with layering specs

**Agents:**
- `sonic-designer` - Translates creative audio intent to SSL specifications
- `sfx-architect` - Designs effects with layers and synthesis code
- `music-architect` - Designs tracks with harmony, structure, and adaptivity
- `audio-coherence-reviewer` - Validates audio consistency with sonic identity

### ai-game-studio

Intelligent game development studio providing request routing, quality analysis, and completion verification across all plugins.

**Skills (3):**
- `request-patterns` - Patterns for classifying and routing game development requests to appropriate expert agents
- `dependency-chains` - What must be completed before other tasks can begin; blocking dependencies and parallelizable work
- `verification-checklists` - Checklists for verifying assets, features, and systems are truly complete

**Commands:**
- `/setup-project` - Complete project setup wizard orchestrating GDD, creative vision, and sonic identity in one flow

**Agents:**
- `request-dispatcher` - Intelligent routing for any development request; parses intent, routes to appropriate experts, ensures completion
- `completion-auditor` - Semantic verification that work is actually complete; catches "generated but not integrated" and "coded but not rendered" issues
- `project-health-monitor` - Comprehensive project health assessment; coordinates all analysis agents, produces unified health dashboard with prioritized tasks

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
    "nethercore-zx-dev@nethercore-ai-plugins": true,
    "nethercore-zx-game-design@nethercore-ai-plugins": true,
    "nethercore-zx-procgen@nethercore-ai-plugins": true,
    "nethercore-zx-publish@nethercore-ai-plugins": true,
    "nethercore-zx-orchestrator@nethercore-ai-plugins": true,
    "nethercore-zx-test@nethercore-ai-plugins": true,
    "nethercore-zx-optimize@nethercore-ai-plugins": true,
    "nethercore-zx-cicd@nethercore-ai-plugins": true,
    "game-design@nethercore-ai-plugins": true,
    "creative-direction@nethercore-ai-plugins": true,
    "sound-design@nethercore-ai-plugins": true,
    "ai-game-studio@nethercore-ai-plugins": true
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
