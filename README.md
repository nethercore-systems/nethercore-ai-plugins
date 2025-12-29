# Nethercore AI Plugins

Official AI-powered development plugins for Nethercore game development. Currently supports Claude Code, with potential for other AI tools in the future.

## Available Plugins

| Plugin | Description | Skills |
|--------|-------------|--------|
| [nethercore-zx-dev](./nethercore-zx-dev/) | Core game development - FFI specs, cameras, rendering | 6 |
| [nethercore-zx-game-design](./nethercore-zx-game-design/) | Game design workflow - GDDs, multiplayer, mechanics | 10 |
| [nethercore-zx-procgen](./nethercore-zx-procgen/) | Procedural asset generation - textures, meshes, sounds | 10 |
| [nethercore-zx-publish](./nethercore-zx-publish/) | Publishing workflow - ROM packaging, platform upload | 2 |
| [nethercore-zx-orchestrator](./nethercore-zx-orchestrator/) | Meta-orchestration - coordinates full pipeline | 0 |
| [nethercore-zx-test](./nethercore-zx-test/) | Testing and QA - sync tests, replay regression | 2 |
| [nethercore-zx-optimize](./nethercore-zx-optimize/) | Optimization - resource budgets, performance tuning | 2 |
| [nethercore-zx-cicd](./nethercore-zx-cicd/) | CI/CD automation - GitHub Actions, quality gates | 1 |
| [game-design](./game-design/) | Platform-agnostic design - world building, narrative | 11 |
| [creative-direction](./creative-direction/) | Creative oversight - art, sound, tech direction | 5 |
| [sound-design](./sound-design/) | Audio design - Sonic Style Language, synthesis, composition | 5 |
| [ai-game-studio](./ai-game-studio/) | Intelligent routing - request dispatch, completion verification, workflow continuity | 3 |

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
    "game-design@nethercore-ai-plugins": true,
    "creative-direction@nethercore-ai-plugins": true,
    "sound-design@nethercore-ai-plugins": true,
    "ai-game-studio@nethercore-ai-plugins": true
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
    "game-design@nethercore-ai-plugins": true,
    "creative-direction@nethercore-ai-plugins": true,
    "sound-design@nethercore-ai-plugins": true,
    "ai-game-studio@nethercore-ai-plugins": true
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

**Skills (6):**
- `zx-game-development` - FFI specifications, project templates, CLI tooling
- `bindings-fetcher` - Fetch/update FFI bindings from GitHub
- `camera-systems` - 3D camera implementation and perspective-based design
- `rendering-techniques` - Stencil effects, custom fonts, billboard particles
- `debugging-guide` - Debugging and sync testing workflows
- `environment-effects` - Fog, lighting, and atmospheric effects

**Commands:**
- `/new-game` - Scaffold a new ZX game project

**Agents:**
- `rollback-reviewer` - Reviews code for GGRS rollback netcode compatibility
- `code-scaffolder` - Generates boilerplate game code for common patterns
- `feature-implementer` - Implements complete game features end-to-end
- `integration-assistant` - Connects generated assets to game code

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
- `gdd-generator` - Autonomously generates complete Game Design Documents
- `mechanic-designer` - Designs detailed game mechanics
- `scope-advisor` - Assesses project scope and defines MVPs
- `gdd-implementation-tracker` - Compares GDD to implementation

### nethercore-zx-procgen

Procedural asset generation plugin.

**Skills (10):**
- `procedural-textures` - Texture generation (Albedo, MRE, SSE, Matcaps)
- `procedural-meshes` - 3D mesh generation with UVs and vertex colors
- `procedural-sounds` - Audio synthesis and SFX
- `procedural-music` - XM tracker music composition
- `procedural-animations` - Walk cycles, attacks, locomotion (includes skeletal rigging and mocap)
- `procedural-sprites` - 2D sprites, pixel art, tilesets, UI elements
- `semantic-asset-language` - SADL for AI-first creative workflows
- `mesh-texturing-workflows` - UV projection techniques
- `asset-quality-tiers` - Tier system (Placeholder→Temp→Final→Hero)
- `native-asset-pipeline` - Native ZX asset format pipeline

**Commands:**
- `/generate-asset` - Quick single-asset generation
- `/generate-sfx` - Quick sound effect generation
- `/new-asset-project` - Scaffold asset generation project
- `/improve-assets` - Guided quality improvement workflow

**Agents:**
- `asset-designer` - Translates creative vision to SADL specs
- `asset-generator` - Produces procedural generation code
- `asset-critic` - Reviews asset quality against specs
- `asset-quality-reviewer` - Validates assets meet ZX budgets
- `procgen-optimizer` - Optimizes generation code and output
- `creative-orchestrator` - Coordinates full asset pipeline
- `character-generator` - End-to-end character creation
- `quality-analyzer` - Holistic asset quality assessment
- `quality-enhancer` - Autonomous asset quality improvement

### nethercore-zx-publish

Publishing workflow plugin.

**Skills (2):**
- `publishing-workflow` - ROM packaging and platform upload
- `platform-assets` - Marketing assets (thumbnails, screenshots)

**Commands:**
- `/publish-game` - Full publishing workflow
- `/prepare-platform-assets` - Generate marketing assets

**Agents:**
- `publish-preparer` - Autonomously prepares games for release
- `release-validator` - Validates all release requirements

### nethercore-zx-orchestrator

Meta-orchestration plugin coordinating multi-plugin workflows.

**Commands:**
- `/orchestrate` - Launch the game development orchestrator

**Agents:**
- `game-orchestrator` - Coordinates full development pipeline from GDD to playable ROM
- `parallel-coordinator` - Analyzes task dependencies and coordinates parallel execution

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
- `pipeline-optimizer` - Optimizes CI/CD pipeline performance
- `quality-gate-enforcer` - Adds and configures quality checks

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
- `narrative-generator` - Generates story content, dialogue, lore
- `balance-analyzer` - Analyzes game balance and difficulty curves
- `accessibility-auditor` - Audits designs for accessibility barriers

### creative-direction

Quality assurance and coherence plugin providing "director" level oversight.

**Skills (5):**
- `art-vision` - Visual style bible, color theory, composition
- `sound-vision` - Audio style guide, mixing, sonic identity
- `tech-vision` - Architecture patterns, file splitting, module organization
- `creative-vision` - Creative pillars, experience promise, vision alignment
- `project-memory` - Persistent direction files, session context

**Commands:**
- `/establish-vision` - Interactive wizard to establish project creative direction

**Agents:**
- `art-director` - Reviews visual coherence across all assets
- `sound-director` - Reviews audio coherence and mix balance
- `tech-director` - Reviews architecture and code quality
- `creative-director` - Meta-director for holistic vision alignment

### sound-design

Platform-agnostic game audio design with Sonic Style Language (SSL).

**Skills (5):**
- `sonic-style-language` - SSL specification: styles, moods, instruments, processing
- `synthesis-techniques` - FM, wavetable, granular, physical modeling
- `music-composition` - Theory, chord progressions, structure, adaptive music
- `sfx-design` - Layering, archetypes, impact design, UI audio
- `audio-integration` - Mix architecture, spatial audio, ducking

**Commands:**
- `/establish-sonic-identity` - Create SSL specification
- `/design-soundtrack` - Design music tracks
- `/design-sfx` - Design sound effects with layering specs

**Agents:**
- `sonic-designer` - Translates creative audio intent to SSL
- `sfx-architect` - Designs effects with synthesis code
- `music-architect` - Designs tracks with harmony and structure
- `audio-coherence-reviewer` - Validates audio consistency

### ai-game-studio

Intelligent game development studio providing request routing, quality analysis, and continuous workflow guidance.

**Skills (4):**
- `request-patterns` - Classifying and routing development requests
- `dependency-chains` - Blocking dependencies and parallelizable work
- `verification-checklists` - Verifying assets and features are complete
- `dispatch-queue` - Task queue pattern for session continuity

**Commands:**
- `/setup-project` - Complete project setup wizard (GDD + creative vision + sonic identity)
- `/continue` - Resume development from where you left off (--quick, --full, --auto)

**Agents:**
- `request-dispatcher` - Intelligent routing for any development request
- `completion-auditor` - Semantic verification that work is complete
- `project-health-monitor` - Comprehensive project health assessment
- `next-step-suggester` - Fast, focused "what next?" recommendations

## Continuous Workflow

The plugins feature automatic "what's next?" guidance to maintain development momentum:

### Automatic Next-Step Suggestions

When any agent completes its work, a hook automatically suggests 2-3 logical next actions:

```
WORK COMPLETED - SUGGEST NEXT STEPS

An agent just finished work. Suggested next actions:
- After asset generation → verify integration or generate related assets
- After feature implementation → test, polish, or add sounds
- After scaffolding → implement actual game logic

Would you like me to continue with [recommended action]?
```

### Quick "What Next?" Agent

When you're unsure what to do, ask "what next?" or "I'm stuck" to get fast, focused recommendations:

```
**Current State:** Player movement implemented, no assets connected yet.

**Recommended Next Step:**
→ Run integration-assistant to connect player mesh and textures
   Agent: nethercore-zx-dev:integration-assistant

**Why:** Assets exist but aren't wired up - player won't render until integrated.

**Alternative:** Generate placeholder assets if none exist yet.

Ready to proceed? Say "yes" or specify what you'd prefer.
```

### Agent Continuation Prompts

All major agents end their output with clear next-step options:

```
**Next Steps:**
1. Run completion-auditor to verify full integration --> ai-game-studio:completion-auditor
2. Generate sound effects for the feature --> nethercore-zx-procgen:sfx-architect

Continue with #1? (yes/no/other)
```

This ensures you always know what to do after any task completes.

### The `/continue` Command

For explicit session resumption, use the `/continue` command:

```
/continue          → Check pending tasks, recommend next step, ask before dispatching
/continue --quick  → Just show dispatch queue and project status
/continue --full   → Run comprehensive project health analysis
/continue --auto   → Auto-dispatch first pending task without asking
```

The command reads `.studio/dispatch-queue.md` and `.studio/project-status.md` to understand your current state and recommend the next action.

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
