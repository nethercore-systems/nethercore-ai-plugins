---
name: Agent Registry
description: |
  Use this skill for agent discovery, routing decisions, and understanding what specialists are available.

  **Triggers:** "which agent", "find agent for", "route to", "specialist for", "who handles"

  Contains the complete registry of all Task tool subagent_types across all plugins.
version: 1.0.0
---

# Agent Registry

Complete lookup table for Task tool `subagent_type` values.

## Quick Lookup by Domain

### Design & Planning
| Task | subagent_type |
|------|---------------|
| Concept → GDD | `zx-game-design:gdd-generator` |
| Mechanic design | `zx-game-design:mechanic-designer` |
| Scope check | `zx-game-design:scope-advisor` |
| Balance analysis | `game-design:balance-analyzer` |
| Accessibility | `game-design:accessibility-auditor` |
| Design review | `game-design:design-reviewer` |
| Genre patterns | `game-design:genre-advisor` |
| Narrative content | `game-design:narrative-generator` |

### Creative Direction
| Task | subagent_type |
|------|---------------|
| Visual coherence | `creative-direction:art-director` |
| Audio coherence | `creative-direction:sound-director` |
| Code architecture | `creative-direction:tech-director` |
| Holistic vision | `creative-direction:creative-director` |

### Asset Generation
| Task | subagent_type |
|------|---------------|
| Style specs | `zx-procgen:asset-designer` |
| Procgen code | `zx-procgen:asset-generator` |
| Spec compliance | `zx-procgen:asset-critic` |
| ZX budget check | `zx-procgen:asset-quality-reviewer` |
| Quality upgrade | `zx-procgen:quality-enhancer` |
| Full character | `zx-procgen:character-generator` |
| Asset pipeline | `zx-procgen:creative-orchestrator` |
| Quality analysis | `zx-procgen:quality-analyzer` |

### Sound Design
| Task | subagent_type |
|------|---------------|
| Audio specs | `sound-design:sonic-designer` |
| SFX synthesis | `sound-design:sfx-architect` |
| Music composition | `sound-design:music-architect` |
| Audio review | `sound-design:audio-coherence-reviewer` |

### Code Development
| Task | subagent_type |
|------|---------------|
| System scaffold | `zx-dev:code-scaffolder` |
| Full feature | `zx-dev:feature-implementer` |
| Asset integration | `zx-dev:integration-assistant` |
| Rollback safety | `zx-dev:rollback-reviewer` |
| Replay debugging | `zx-dev:replay-debugger` |

### Testing & Optimization
| Task | subagent_type |
|------|---------------|
| Run tests | `zx-test:test-runner` |
| Debug desync | `zx-test:desync-investigator` |
| Build analysis | `zx-optimize:build-analyzer` |
| Apply optimizations | `zx-optimize:optimizer` |

### Publishing & CI
| Task | subagent_type |
|------|---------------|
| Release check | `zx-publish:release-validator` |
| Publish prep | `zx-publish:publish-preparer` |
| CI setup | `zx-cicd:ci-scaffolder` |
| CI optimization | `zx-cicd:pipeline-optimizer` |
| Quality gates | `zx-cicd:quality-gate-enforcer` |

### Orchestration
| Task | subagent_type |
|------|---------------|
| Full pipeline | `zx-orchestrator:game-orchestrator` |
| Parallel tasks | `zx-orchestrator:parallel-coordinator` |
| Request routing | `ai-game-studio:request-dispatcher` |
| Completion check | `ai-game-studio:completion-auditor` |
| Next step | `ai-game-studio:next-step-suggester` |
| Health check | `ai-game-studio:project-health-monitor` |

### Tracker Music
| Task | subagent_type |
|------|---------------|
| Song generation | `tracker-music:song-generator` |

## Invocation Patterns

**Single:** `Task tool with subagent_type="plugin:agent-name"`

**Parallel:** Send multiple Task calls in ONE message

**Background:** `run_in_background: true`, retrieve with TaskOutput

**Resume:** `resume="{agent_id}"` from previous run

## By Development Phase

| Phase | Primary Agents |
|-------|----------------|
| Creative | creative-director, sonic-designer |
| Design | gdd-generator, mechanic-designer, accessibility-auditor |
| Visual | asset-designer, asset-generator, art-director |
| Audio | sfx-architect, music-architect, sound-director |
| Code | code-scaffolder, feature-implementer, tech-director |
| Test | test-runner, build-analyzer, optimizer |
| Publish | release-validator, publish-preparer |

## Proactive Agents

Auto-invoke when conditions match:
- `completion-auditor` - After any significant work
- `release-validator` - After builds, before release
- `scope-advisor` - When design seems ambitious
- `accessibility-auditor` - When reviewing designs
