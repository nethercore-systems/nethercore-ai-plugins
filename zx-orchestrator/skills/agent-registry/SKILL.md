# Agent Registry

This skill provides the complete registry of available agents for orchestration tasks. Use this when spawning sub-agents with the Task tool.

## CRITICAL: Fully-Qualified Agent Names

When using the Task tool, you MUST use the **fully-qualified subagent_type** format:
```
plugin-name:agent-name
```

Do NOT use short names like `asset-designer`. Use `zx-procgen:asset-designer`.

## Complete Agent Registry

### Creative Direction (`creative-direction`)

| Agent | subagent_type | Purpose |
|-------|---------------|---------|
| Creative Director | `creative-direction:creative-director` | Meta-director for overall vision alignment |
| Art Director | `creative-direction:art-director` | Visual coherence and style consistency |
| Sound Director | `creative-direction:sound-director` | Audio coherence and sonic identity |
| Tech Director | `creative-direction:tech-director` | Architecture, code quality, file organization |

### Game Design (`game-design`)

| Agent | subagent_type | Purpose |
|-------|---------------|---------|
| Design Reviewer | `game-design:design-reviewer` | GDD coherence and completeness |
| Genre Advisor | `game-design:genre-advisor` | Genre-appropriate design patterns |
| Accessibility Auditor | `game-design:accessibility-auditor` | Accessibility barriers and improvements |
| Balance Analyzer | `game-design:balance-analyzer` | Stats, difficulty curves, economy balance |
| Narrative Generator | `game-design:narrative-generator` | Story content, dialogue, lore |

### ZX Game Design (`zx-game-design`)

| Agent | subagent_type | Purpose |
|-------|---------------|---------|
| GDD Generator | `zx-game-design:gdd-generator` | Autonomous GDD creation |
| Mechanic Designer | `zx-game-design:mechanic-designer` | Detailed mechanic specs |
| Constraint Analyzer | `zx-game-design:constraint-analyzer` | ZX feasibility checking |
| Scope Advisor | `zx-game-design:scope-advisor` | Project scope assessment |

### Procedural Generation (`zx-procgen`)

| Agent | subagent_type | Purpose |
|-------|---------------|---------|
| Asset Designer | `zx-procgen:asset-designer` | Creative vision → style specs |
| Asset Generator | `zx-procgen:asset-generator` | style specs → procedural code |
| Character Generator | `zx-procgen:character-generator` | Complete animated character creation |
| Asset Critic | `zx-procgen:asset-critic` | Spec compliance review |
| Asset Quality Reviewer | `zx-procgen:asset-quality-reviewer` | ZX budget compliance |
| Procgen Optimizer | `zx-procgen:procgen-optimizer` | Generation optimization |
| Creative Orchestrator | `zx-procgen:creative-orchestrator` | Full asset pipeline coordination |

### Sound Design (`sound-design`)

| Agent | subagent_type | Purpose |
|-------|---------------|---------|
| Sonic Designer | `sound-design:sonic-designer` | Audio intent → audio style specs |
| SFX Architect | `sound-design:sfx-architect` | Sound effect synthesis |
| Music Architect | `sound-design:music-architect` | Music composition |
| Audio Coherence Reviewer | `sound-design:audio-coherence-reviewer` | Sonic identity validation |

### ZX Development (`zx-dev`)

| Agent | subagent_type | Purpose |
|-------|---------------|---------|
| Code Scaffolder | `zx-dev:code-scaffolder` | Boilerplate code generation |
| Feature Implementer | `zx-dev:feature-implementer` | Complete feature implementation |
| Integration Assistant | `zx-dev:integration-assistant` | Asset-to-code connection |
| Rollback Reviewer | `zx-dev:rollback-reviewer` | Netcode safety analysis |

### Testing (`zx-test`)

| Agent | subagent_type | Purpose |
|-------|---------------|---------|
| Test Runner | `zx-test:test-runner` | Sync and regression tests |
| Desync Investigator | `zx-test:desync-investigator` | Non-determinism debugging |

### Optimization (`zx-optimize`)

| Agent | subagent_type | Purpose |
|-------|---------------|---------|
| Build Analyzer | `zx-optimize:build-analyzer` | Build size analysis |
| Optimizer | `zx-optimize:optimizer` | Apply optimizations |

### Publishing (`zx-publish`)

| Agent | subagent_type | Purpose |
|-------|---------------|---------|
| Release Validator | `zx-publish:release-validator` | Release requirements check |
| Publish Preparer | `zx-publish:publish-preparer` | Autonomous release preparation |

### CI/CD (`zx-cicd`)

| Agent | subagent_type | Purpose |
|-------|---------------|---------|
| CI Scaffolder | `zx-cicd:ci-scaffolder` | GitHub Actions setup |
| Pipeline Optimizer | `zx-cicd:pipeline-optimizer` | CI performance tuning |
| Quality Gate Enforcer | `zx-cicd:quality-gate-enforcer` | Quality check configuration |

### Orchestration (`zx-orchestrator`)

| Agent | subagent_type | Purpose |
|-------|---------------|---------|
| Game Orchestrator | `zx-orchestrator:game-orchestrator` | Full development pipeline |
| Parallel Coordinator | `zx-orchestrator:parallel-coordinator` | Parallel task execution |

## Task Tool Usage

### Single Agent

```
Task tool call:
  subagent_type: "zx-procgen:asset-designer"
  description: "Design character specs"
  prompt: "Create style specifications for..."
```

### Parallel Agents

Send ONE message with MULTIPLE Task tool calls:

```
Message containing:
  Task #1: subagent_type="creative-direction:art-director", ...
  Task #2: subagent_type="creative-direction:sound-director", ...
  Task #3: subagent_type="creative-direction:tech-director", ...

→ All execute concurrently
```

### Background Agent

```
Task tool call:
  subagent_type: "zx-procgen:character-generator"
  description: "Generate player"
  prompt: "..."
  run_in_background: true

→ Returns task_id immediately
→ Use TaskOutput to retrieve results later
```

## Common Parallel Patterns

### Quality Review Suite
- `creative-direction:art-director`
- `creative-direction:sound-director`
- `creative-direction:tech-director`
- Then: `creative-direction:creative-director` (after individual reviews)

### Asset Generation Pipeline
- Wave 1: Multiple `zx-procgen:asset-designer` (parallel)
- Wave 2: Multiple `zx-procgen:asset-generator` (parallel)
- Wave 3: `zx-procgen:asset-critic` + `asset-quality-reviewer` (parallel)

### Validation Suite
- `zx-test:test-runner`
- `zx-optimize:build-analyzer`
- `zx-dev:rollback-reviewer`
- `zx-publish:release-validator`

### Design Review
- `game-design:design-reviewer`
- `game-design:accessibility-auditor`
- `zx-game-design:constraint-analyzer`
- `zx-game-design:scope-advisor`
