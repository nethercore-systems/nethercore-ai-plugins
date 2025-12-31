# Nethercore AI Plugins

Official AI-powered development plugins for Nethercore ZX game development. These plugins provide Claude Code with comprehensive knowledge of game development workflows, procedural asset generation, and the ZX fantasy console platform.

## How the Plugin System Works

These plugins follow a **What → How → Why** pattern:

| Layer | Purpose | Example |
|-------|---------|---------|
| **Why** | Conceptual frameworks, design theory | `game-design`, `sound-design`, `creative-direction` |
| **What** | Platform-specific patterns, constraints | `zx-game-design`, `console-constraints` |
| **How** | Implementation, generation, tooling | `zx-dev`, `zx-procgen`, FFI specs |

**Skills** provide knowledge (auto-load based on context).
**Commands** are explicit actions you invoke (`/command-name`).
**Agents** are specialized sub-processes for complex tasks.

---

## Quick Start

### Starting a New Project

**Option A: Full Guided Experience** (recommended for first game)
```
ai-game-studio:setup-project
```
This wizard walks you through GDD creation, creative vision, and sonic identity in one flow.

**Option B: Quick Scaffold** (experienced developers)
```
zx-dev:new-game rust my-game
cd my-game
nether run
```

**Option C: Full Orchestration** (let AI drive the pipeline)
```
zx-orchestrator:orchestrate
```
The `game-orchestrator` agent guides you through all 7 phases with checkpoints.

### Continuing Work on an Existing Project

```
ai-game-studio:continue           # Check status, recommend next step
ai-game-studio:continue --quick   # Just show pending tasks
ai-game-studio:continue --full    # Comprehensive health analysis
```

### Resuming After a Break

The plugins persist state to `.studio/`:
- `project-status.md` - Current phase and progress
- `dispatch-queue.md` - Pending tasks
- `creative-direction.local.md` - Vision documents

On session start, the system reads these files and can resume from where you left off.

---

## Choosing Your Entry Point

### Decision Tree

```
What do you need?
│
├── "I have a vague idea" ────────→ ai-game-studio:setup-project
│   (walks through GDD, vision, audio direction)
│
├── "I have a GDD, make the game" → zx-orchestrator:orchestrate
│   (full 7-phase pipeline with checkpoints)
│
├── "I need ONE specific thing" ──→ Use the specific command/agent:
│   │
│   ├── Generate assets ──────────→ zx-procgen:generate-asset
│   ├── Design a character ───────→ game-design:character
│   ├── Create game music ────────→ sound-design:design-soundtrack
│   ├── Review code quality ──────→ tech-director agent
│   └── Check ZX constraints ─────→ zx-game-design:validate-design
│
├── "I don't know what I need" ───→ Just describe your problem
│   (request-dispatcher routes to the right expert)
│
└── "I'm stuck / what's next?" ───→ "what next?" or ai-game-studio:continue
```

### Orchestrator Comparison

| Orchestrator | Scope | When to Use |
|--------------|-------|-------------|
| `game-orchestrator` | Full 7-phase pipeline | Building complete game from scratch |
| `creative-orchestrator` | Asset generation pipeline | Generating assets for existing project |
| `request-dispatcher` | Single request routing | Have a vague/complex request |
| `parallel-coordinator` | Task parallelization | 4+ independent tasks to run |

---

## Common Workflows

### Workflow 1: New Game from Concept

```
1. ai-game-studio:setup-project        # Define GDD + creative vision
2. zx-game-design:validate-design      # Check against ZX constraints
3. zx-game-design:plan-assets          # Extract asset requirements
4. [Asset generation phase]
5. zx-dev:new-game rust my-game        # Scaffold project
6. [Implementation phase]
7. zx-publish:publish-game             # Package and upload
```

### Workflow 2: Add Assets to Existing Game

```
1. Describe what you need: "I need a player character with idle and run animations"
2. asset-designer agent → Creates style spec
3. character-generator agent → Generates mesh, rig, animations
4. integration-assistant agent → Connects to game code
5. completion-auditor agent → Verifies everything works
```

### Workflow 3: Create Game Music

```
1. sound-design:establish-sonic-identity   # Define audio style (audio style)
2. sound-design:design-soundtrack          # Plan tracks
3. music-architect agent → Design individual tracks
4. zx-procgen:generate-instrument          # Create instrument samples
5a. tracker-music:generate-song            # Programmatic XM/IT generation
5b. OR: Use MilkyTracker/OpenMPT to compose manually
6. integration-assistant → Add to nether.toml
```

### Workflow 4: Fix Performance Issues

```
1. build-analyzer agent → Identify largest assets
2. optimizer agent → Apply optimization techniques
3. test-runner agent → Verify still works
```

### Workflow 5: Prepare for Release

```
1. release-validator agent → Check all requirements
2. creative-director agent → Final vision review
3. zx-publish:prepare-platform-assets → Marketing images
4. zx-publish:publish-game → Package ROM and upload
```

---

## Plugin Organization

### Platform-Agnostic Plugins (Conceptual "Why")

These provide universal game design knowledge not tied to ZX:

| Plugin | Focus | Use When |
|--------|-------|----------|
| `game-design` | Design frameworks, psychology, balance | Designing gameplay, story, world |
| `sound-design` | Audio theory, composition, audio style | Designing audio direction |
| `tracker-music` | XM/IT tracker generation, pattern design | Creating tracker module music |
| `creative-direction` | Vision alignment, style guides | Establishing creative pillars |
| `ai-game-studio` | Workflow orchestration, routing | Meta-coordination |

### ZX-Specific Plugins (Technical "What" and "How")

These provide ZX-specific implementation details:

| Plugin | Focus | Use When |
|--------|-------|----------|
| `zx-dev` | FFI, cameras, rendering, debugging | Writing game code |
| `zx-game-design` | Constraints, mechanics, GDDs | Designing for ZX limits |
| `zx-procgen` | Asset generation, style guide | Creating assets |
| `zx-test` | Sync tests, determinism | Testing multiplayer |
| `zx-optimize` | Budgets, optimization | Performance tuning |
| `zx-publish` | ROM packaging, upload | Publishing |
| `zx-cicd` | GitHub Actions | CI/CD setup |
| `zx-orchestrator` | Full pipeline coordination | End-to-end development |

---

## Agent Quick Reference

### Analysis Agents (Understand State)
| Agent | Plugin | Purpose |
|-------|--------|---------|
| `project-health-monitor` | ai-game-studio | Overall project health dashboard |
| `gdd-implementation-tracker` | zx-game-design | GDD vs code comparison |
| `quality-analyzer` | zx-procgen | Asset quality assessment |
| `completion-auditor` | ai-game-studio | Verify work is truly complete |
| `build-analyzer` | zx-optimize | Find largest assets |

### Direction Agents (Review Quality)
| Agent | Plugin | Purpose |
|-------|--------|---------|
| `creative-director` | creative-direction | Holistic vision alignment |
| `art-director` | creative-direction | Visual coherence |
| `sound-director` | creative-direction | Audio coherence |
| `tech-director` | creative-direction | Code quality, architecture |

### Generation Agents (Create Things)
| Agent | Plugin | Purpose |
|-------|--------|---------|
| `asset-generator` | zx-procgen | Procedural generation code |
| `character-generator` | zx-procgen | Full animated characters |
| `sfx-architect` | sound-design | Sound effect design |
| `music-architect` | sound-design | Music track design |
| `code-scaffolder` | zx-dev | Boilerplate game systems |
| `feature-implementer` | zx-dev | Complete feature implementation |
| `song-generator` | tracker-music | End-to-end tracker module generation |

### Validation Agents (Check Correctness)
| Agent | Plugin | Purpose |
|-------|--------|---------|
| `rollback-reviewer` | zx-dev | Netcode safety check |
| `constraint-analyzer` | zx-game-design | ZX feasibility check |
| `release-validator` | zx-publish | Release readiness |
| `desync-investigator` | zx-test | Find non-deterministic code |

---

## Key Commands

### Project Setup
| Command | Purpose |
|---------|---------|
| `ai-game-studio:setup-project` | Full project wizard (GDD + vision + audio) |
| `zx-dev:new-game` | Scaffold game project (Rust/C/Zig) |
| `zx-procgen:new-asset-project` | Scaffold asset generation project |

### Design Phase
| Command | Purpose |
|---------|---------|
| `zx-game-design:design-game` | Interactive GDD builder |
| `zx-game-design:plan-assets` | Extract asset specs from GDD |
| `zx-game-design:validate-design` | Check against ZX constraints |
| `game-design:worldbuild` | World building wizard |
| `game-design:character` | Character design worksheet |
| `creative-direction:establish-vision` | Define creative pillars |

### Asset Generation
| Command | Purpose |
|---------|---------|
| `zx-procgen:generate-asset` | Single asset generation |
| `zx-procgen:generate-sfx` | Sound effect generation |
| `zx-procgen:generate-instrument` | Instrument sample synthesis |
| `zx-procgen:improve-assets` | Quality improvement workflow |

### Audio Design
| Command | Purpose |
|---------|---------|
| `sound-design:establish-sonic-identity` | Create audio style specification |
| `sound-design:design-soundtrack` | Design music tracks |
| `sound-design:design-sfx` | Design sound effects |
| `tracker-music:generate-song` | Generate XM/IT tracker modules |

### Publishing
| Command | Purpose |
|---------|---------|
| `zx-publish:publish-game` | Full publishing workflow |
| `zx-publish:prepare-platform-assets` | Marketing assets |

### Workflow Control
| Command | Purpose |
|---------|---------|
| `zx-orchestrator:orchestrate` | Launch full pipeline orchestrator |
| `ai-game-studio:continue` | Resume from where you left off |

---

## ZX Console Constraints

Key limits to remember (detailed in `console-constraints` skill):

| Resource | Limit |
|----------|-------|
| ROM size | 16 MB |
| VRAM | 4 MB |
| WASM memory | 4 MB |
| Resolution | 960×540 |
| Tick rates | 24, 30, 60, 120 fps |
| Players | 1-4 (local/online) |
| Audio channels | 16 simultaneous |
| Sample rate | 22,050 Hz |

State size for rollback: Target < 100 KB for smooth netplay.

---

## Installation

### Global Installation (Recommended)

Add to `~/.claude/settings.json` (macOS/Linux) or `%USERPROFILE%\.claude\settings.json` (Windows):

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

### Workspace Installation (Contributors)

For contributors with the nethercore workspace, add to `.claude/settings.local.json`:

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

---

## Plugin Details

### zx-dev

Core game development plugin for Nethercore ZX.

**Skills (6):**
- `zx-game-development` - FFI specifications, project templates, CLI tooling
- `bindings-fetcher` - Fetch/update FFI bindings from GitHub
- `camera-systems` - 3D camera implementation and perspective-based design
- `rendering-techniques` - Stencil effects, custom fonts, billboard particles
- `debugging-guide` - Debugging and sync testing workflows
- `environment-effects` - Fog, lighting, and atmospheric effects

**Commands:** `zx-dev:new-game`

**Agents:** `rollback-reviewer`, `code-scaffolder`, `feature-implementer`, `integration-assistant`

### zx-game-design

ZX-specific game design workflow plugin.

**Skills (10):** GDD templates, console constraints, multiplayer patterns, physics/collision, gameplay mechanics, UI patterns, game feel, save systems, AI patterns, level design

**Commands:** `design-game`, `plan-assets`, `validate-design`

**Agents:** `constraint-analyzer`, `gdd-generator`, `mechanic-designer`, `scope-advisor`, `gdd-implementation-tracker`

### zx-procgen

Procedural asset generation plugin.

**Skills (12):** Textures, meshes, sounds, instruments, music (XM), animations, sprites, style guide, texturing workflows, quality tiers, native pipeline

**Commands:** `generate-asset`, `generate-sfx`, `generate-instrument`, `new-asset-project`, `improve-assets`

**Agents:** `asset-designer`, `asset-generator`, `character-generator`, `quality-analyzer`, `quality-enhancer`, `asset-critic`, `asset-quality-reviewer`, `procgen-optimizer`, `creative-orchestrator`, `instrument-architect`

### zx-publish

Publishing workflow plugin.

**Skills (2):** Publishing workflow, platform assets

**Commands:** `publish-game`, `prepare-platform-assets`

**Agents:** `publish-preparer`, `release-validator`

### zx-orchestrator

Meta-orchestration plugin coordinating multi-plugin workflows.

**Skills (2):**
- `agent-registry` - Complete Task tool subagent_type lookup (shared by all orchestrators)
- `project-status` - Session continuity and progress tracking

**Commands:** `orchestrate`

**Agents:** `game-orchestrator` (7-phase pipeline), `parallel-coordinator`

### zx-test

Testing and QA plugin.

**Skills (2):** Testing fundamentals, benchmarking

**Agents:** `test-runner`, `desync-investigator`

### zx-optimize

Optimization plugin.

**Skills (2):** Resource budgets, optimization techniques

**Agents:** `build-analyzer`, `optimizer`

### zx-cicd

CI/CD automation plugin.

**Skills (1):** CI automation (GitHub Actions)

**Agents:** `ci-scaffolder`, `pipeline-optimizer`, `quality-gate-enforcer`

### game-design

Platform-agnostic game design frameworks.

**Skills (11):** World building, character design, narrative, core loops, level design, balance, player psychology, genre patterns, multiplayer design, accessibility, replayability

**Commands:** `worldbuild`, `character`, `design-loop`, `balance-review`

**Agents:** `design-reviewer`, `genre-advisor`, `narrative-generator`, `balance-analyzer`, `accessibility-auditor`

### creative-direction

Director-level oversight plugin.

**Skills (5):** Art vision, sound vision, tech vision, creative vision, project memory

**Commands:** `establish-vision`

**Agents:** `art-director`, `sound-director`, `tech-director`, `creative-director`

### sound-design

Audio design with audio style guide.

**Skills (5):** audio style specification, synthesis techniques, music composition, SFX design, audio integration

**Commands:** `establish-sonic-identity`, `design-soundtrack`, `design-sfx`

**Agents:** `sonic-designer`, `sfx-architect`, `music-architect`, `audio-coherence-reviewer`

### tracker-music

Tracker module music generation (XM/IT formats).

**Skills (4):** Tracker fundamentals, pattern design, XM format, IT format

**Commands:** `generate-song`

**Agents:** `song-generator`

### ai-game-studio

Intelligent routing and workflow continuity.

**Skills (4):** Request patterns, dependency chains, verification checklists, dispatch queue

**Commands:** `setup-project`, `continue`

**Agents:** `request-dispatcher`, `completion-auditor`, `project-health-monitor`, `next-step-suggester`

---

## Troubleshooting

### "I don't know which agent to use"
Just describe what you need. The `request-dispatcher` agent or skills auto-loading will route you to the right place.

### "I'm lost in the workflow"
Run `ai-game-studio:continue --full` for a comprehensive project health check.

### "My request spans multiple domains"
The `game-orchestrator` or `request-dispatcher` can decompose multi-domain requests and coordinate the right agents.

### "Skills keep loading that aren't relevant"
Skills auto-load based on keywords. Be specific in your request to avoid triggering unrelated skills.

### "The build fails"
Check `nether build` output. Common issues:
- Missing asset references in `nether.toml`
- Non-deterministic code (for multiplayer)
- Exceeding ROM/VRAM budgets

### "Assets aren't appearing in-game"
Use `integration-assistant` to verify assets are wired up in `nether.toml` and loaded in code.

---

## Skill Architecture

### Progressive Disclosure Pattern

Skills follow a **lean core + detailed references** pattern for context efficiency:

```
skill/
├── SKILL.md           # Lean overview (~150-250 lines)
│   └── "Load references when:" directives
└── references/
    ├── topic-a.md     # Detailed implementation (~100-300 lines)
    ├── topic-b.md
    └── topic-c.md
```

**Why?** Agentic AI loads only what's needed per task instead of 700+ line monoliths.

**Example from `gameplay-mechanics`:**
```yaml
description: |
  **Load references when:**
  - Platformer physics → `references/platformer-mechanics.md`
  - Combat/damage systems → `references/combat-mechanics.md`
  - Items, equipment → `references/inventory-systems.md`
```

### Agent Registry

The `agent-registry` skill (`zx-orchestrator`) provides a single source of truth for all Task tool `subagent_type` values across all plugins. Orchestrator agents reference this skill instead of duplicating agent lookup tables.

```
agent-registry
├── Quick lookup by task type (design, assets, audio, code, test, publish)
├── Invocation patterns (single, parallel, background, resume)
└── Agent categories (proactive, domain experts, meta-orchestrators)
```

---

## Contributing

Plugins are developed in this repository. Each plugin has:
- `.claude-plugin/plugin.json` - Plugin manifest
- `skills/` - Auto-triggering knowledge skills
- `commands/` - Slash commands
- `agents/` - Specialized sub-agents
- `hooks.json` - (optional) Lifecycle hooks

### Skill Guidelines

1. **Keep SKILL.md lean** - Target 150-250 lines for core content
2. **Use references/** - Extract detailed code/tables to reference files
3. **Add loading hints** - Use "Load references when:" in descriptions
4. **Reference shared skills** - Use `agent-registry` instead of duplicating agent tables

## License

Licensed under either of:
- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT license ([LICENSE-MIT](LICENSE-MIT))

at your option.
