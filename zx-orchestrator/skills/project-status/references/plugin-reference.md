# Nethercore Plugin Reference

Complete reference for orchestrating all nethercore plugins.

---

## creative-direction

**Purpose:** Establish and maintain creative vision, coordinate art/sound/tech direction

### Commands
| Command | Description |
|---------|-------------|
| `/establish-vision` | Interactive wizard to establish project creative pillars |

### Agents
| Agent | When to Use |
|-------|-------------|
| creative-director | Meta-director for overall vision coherence (coordinates art, sound, tech) |
| art-director | Review visual coherence, validate art style consistency |
| sound-director | Review audio coherence, validate sonic consistency |
| tech-director | Review architecture, validate code patterns and quality |

---

## sound-design

**Purpose:** Audio direction, sound effects, and music composition

### Commands
| Command | Description |
|---------|-------------|
| `/establish-sonic-identity` | Create Sonic Style Language (SSL) for project audio direction |
| `/design-soundtrack` | Interactive music track composition planning |
| `/design-sfx` | Interactive sound effect design wizard |

### Agents
| Agent | When to Use |
|-------|-------------|
| sonic-designer | Translate creative vision to SSL specifications |
| music-architect | Compose music tracks, chord progressions, melodies |
| sfx-architect | Design and synthesize sound effects |

---

## game-design (Platform-Agnostic)

**Purpose:** Conceptual game design frameworks

### Commands
| Command | Description |
|---------|-------------|
| `/worldbuild` | Interactive world building wizard |
| `/character` | Character design worksheet |
| `/design-loop` | Core loop analysis tool |
| `/balance-review` | Game balance review framework |

### Key Skills
| Skill | Triggers |
|-------|----------|
| world-building | "world design", "lore", "factions" |
| character-design | "player character", "NPC", "antagonist" |
| narrative-design | "story", "quests", "dialogue" |
| core-loop-design | "gameplay loop", "progression" |
| game-balance | "difficulty", "stats", "economy" |
| replayability-engineering | "roguelike", "meta-progression" |

### Agents
| Agent | When to Use |
|-------|-------------|
| design-reviewer | Review GDDs for coherence, completeness |
| genre-advisor | Suggest genre-appropriate patterns |
| narrative-generator | Generate story content |
| balance-analyzer | Analyze game balance |
| accessibility-auditor | Check accessibility, inclusive design |

---

## zx-game-design

**Purpose:** Game design workflow, GDDs, constraints, multiplayer patterns

### Commands
| Command | Description |
|---------|-------------|
| `/design-game` | Interactive GDD builder wizard |
| `/plan-assets` | Generate asset specs from GDD |
| `/validate-design` | Check design against ZX constraints |

### Key Skills
| Skill | Triggers |
|-------|----------|
| game-design-documents | "GDD", "game design document", "design template" |
| console-constraints | "ZX limits", "memory budget", "ROM size" |
| multiplayer-patterns | "netcode", "split-screen", "rollback" |
| gameplay-mechanics | "movement", "combat", "inventory", "dialogue" |
| game-feel | "juice", "polish", "screen shake", "impact" |

### Agents
| Agent | When to Use |
|-------|-------------|
| constraint-analyzer | Check if design is feasible on ZX |
| gdd-generator | Create complete GDD from concept |
| mechanic-designer | Design detailed mechanics with parameters |
| scope-advisor | Assess scope, identify MVP |

---

## zx-procgen

**Purpose:** Procedural asset generation (textures, meshes, sounds, animations)

### Commands
| Command | Description |
|---------|-------------|
| `/generate-asset` | Quick single-asset generation |
| `/new-asset-project` | Scaffold asset generation project |

### Key Skills
| Skill | Triggers |
|-------|----------|
| procedural-textures | "generate texture", "MRE", "matcap", "albedo" |
| procedural-meshes | "generate mesh", "3D model", "low-poly" |
| procedural-sounds | "generate sound", "SFX", "audio synthesis" |
| procedural-animations | "walk cycle", "attack animation" |
| semantic-asset-language | "SADL", "style token", "creative workflow" |

### Agents
| Agent | When to Use |
|-------|-------------|
| asset-designer | Translate creative vision to SADL specs |
| asset-generator | Produce procedural code from specs |
| asset-critic | Validate assets against SADL specs |
| asset-quality-reviewer | Validate assets against ZX budget constraints |
| creative-orchestrator | End-to-end asset creation pipeline |
| character-generator | Complete animated character creation |
| procgen-optimizer | Optimize generation code and reduce asset sizes |

---

## zx-dev

**Purpose:** Core game development, FFI, project scaffolding

### Commands
| Command | Description |
|---------|-------------|
| `/new-game` | Scaffold new ZX game project |

### Key Skills
| Skill | Triggers |
|-------|----------|
| zx-game-development | "ZX FFI", "init/update/render", "nether build" |
| camera-systems | "camera follow", "orbit camera", "third person" |
| rendering-techniques | "stencil", "particles", "custom font" |
| debugging-guide | "debug panel", "sync test", "desync" |
| environment-effects | "fog", "atmosphere", "EPU" |

### Agents
| Agent | When to Use |
|-------|-------------|
| rollback-reviewer | Check code for rollback netcode safety |
| code-scaffolder | Generate boilerplate code patterns |
| feature-implementer | Implement complete features |
| integration-assistant | Connect assets to game code |

---

## zx-test

**Purpose:** Testing, sync verification, replay regression

### Key Skills
| Skill | Triggers |
|-------|----------|
| testing-fundamentals | "sync test", "determinism", "replay" |
| benchmarking | "performance", "profiling", "state size" |

### Agents
| Agent | When to Use |
|-------|-------------|
| test-runner | Run sync tests and replay regression |
| desync-investigator | Analyze sync failures |

---

## zx-optimize

**Purpose:** Optimization, resource budgets, performance tuning

### Key Skills
| Skill | Triggers |
|-------|----------|
| resource-budgets | "ROM size", "VRAM", "state budget" |
| optimization-techniques | "WASM optimization", "texture compression" |

### Agents
| Agent | When to Use |
|-------|-------------|
| build-analyzer | Analyze build output, identify largest assets |
| optimizer | Apply optimizations, report savings |

---

## zx-publish

**Purpose:** Publishing workflow, ROM packaging, platform upload

### Commands
| Command | Description |
|---------|-------------|
| `/prepare-platform-assets` | Create icon, screenshots, banner |
| `/publish-game` | Package ROM and guide upload |

### Key Skills
| Skill | Triggers |
|-------|----------|
| publishing-workflow | "ROM packaging", "nether pack", "upload" |
| platform-assets | "thumbnail", "screenshots", "marketing" |

### Agents
| Agent | When to Use |
|-------|-------------|
| publish-preparer | Prepare game for release |
| release-validator | Validate all release requirements |

---

## zx-cicd

**Purpose:** CI/CD automation, GitHub Actions, quality gates

### Key Skills
| Skill | Triggers |
|-------|----------|
| ci-automation | "GitHub Actions", "CI/CD", "quality gates" |

### Agents
| Agent | When to Use |
|-------|-------------|
| ci-scaffolder | Create CI/CD workflows |
| pipeline-optimizer | Optimize CI performance |
| quality-gate-enforcer | Add quality checks |

---

## Orchestration Patterns

### Full Game Development (7 Phases)

```
Phase 0: CREATIVE FOUNDATION
├── /establish-vision → Core creative pillars
├── /establish-sonic-identity → Audio direction (SSL)
└── creative-director → Validate vision coherence

Phase 1: DESIGN
├── /worldbuild → World design (optional)
├── /character → Character sheets (optional)
├── /design-game → Game Design Document
├── /validate-design → Check ZX constraints
├── /plan-assets → Asset specifications
├── accessibility-auditor → Check inclusive design
└── design-reviewer → Review GDD quality

Phase 2: VISUAL ASSETS
├── asset-designer → SADL specs from vision
├── asset-generator → Procedural generation code
├── character-generator → Animated characters
├── asset-critic → Validate against specs
├── asset-quality-reviewer → Check ZX budgets
├── procgen-optimizer → Optimize if needed
└── art-director → Review visual coherence

Phase 3: AUDIO ASSETS
├── /design-soundtrack → Plan music tracks
├── /design-sfx → Plan sound effects
├── music-architect → Compose tracks
├── sfx-architect → Synthesize effects
└── sound-director → Review audio coherence

Phase 4: IMPLEMENTATION
├── /new-game → Scaffold project
├── code-scaffolder → Generate systems
├── feature-implementer → Complete features
├── integration-assistant → Connect assets
├── rollback-reviewer → Check netcode safety
└── tech-director → Review architecture

Phase 5: TESTING & OPTIMIZATION
├── test-runner → Sync tests, regression
├── desync-investigator → Fix sync issues
├── build-analyzer → Identify optimization targets
└── optimizer → Apply optimizations

Phase 6: PUBLISH
├── /prepare-platform-assets → Marketing assets
├── /publish-game → Package and upload
├── release-validator → Final checks
├── creative-director → Final vision review
└── ci-scaffolder → Set up CI/CD (optional)
```

### Quick Start Workflow

```
1. /establish-vision → Creative pillars
2. /design-game → GDD
3. /plan-assets → Asset specs
4. creative-orchestrator → Generate all assets
5. /new-game → Scaffold project
6. Implement game logic
7. test-runner → Verify determinism
8. optimizer → Optimize build
9. /publish-game → Release
```

### Asset-Only Workflow

```
1. asset-designer → SADL specs
2. asset-generator → Procedural code
3. asset-critic → Spec compliance
4. asset-quality-reviewer → ZX budget check
5. procgen-optimizer → Optimize if needed
6. Integrate into game
```

### Audio-Only Workflow

```
1. /establish-sonic-identity → SSL specification
2. /design-soundtrack → Plan music
3. /design-sfx → Plan effects
4. music-architect → Compose
5. sfx-architect → Synthesize
6. sound-director → Review coherence
```

### Design-Only Workflow

```
1. /establish-vision → Creative pillars
2. /worldbuild → World design
3. /character → Character sheets
4. /design-game → GDD
5. /validate-design → Constraints check
6. accessibility-auditor → Inclusive design
7. design-reviewer → Quality review
```

### Quality Review Checkpoints

| Checkpoint | After Phase | Agents to Invoke |
|------------|-------------|------------------|
| Vision Check | Creative Foundation | creative-director |
| Design Review | Design | design-reviewer, accessibility-auditor |
| Art Review | Visual Assets | art-director, asset-quality-reviewer |
| Audio Review | Audio Assets | sound-director |
| Tech Review | Implementation | tech-director, rollback-reviewer |
| Release Review | Pre-Publish | release-validator, creative-director |
