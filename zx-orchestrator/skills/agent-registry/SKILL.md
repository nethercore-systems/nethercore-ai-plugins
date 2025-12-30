---
name: Agent Registry
description: |
  Use this skill for agent discovery, routing decisions, and understanding what specialists are available.

  **Triggers:** "which agent", "find agent for", "route to", "specialist for", "who handles"

  Contains the complete registry of all Task tool subagent_types across all plugins.
version: 1.0.0
---

# Agent Registry

Complete registry of Task tool `subagent_type` values for agent invocation.

## Quick Lookup by Task Type

| Task | Agent | Plugin |
|------|-------|--------|
| **Design & Planning** |||
| Game concept → GDD | `zx-game-design:gdd-generator` | zx-game-design |
| Mechanic deep-dive | `zx-game-design:mechanic-designer` | zx-game-design |
| Scope/feasibility check | `zx-game-design:scope-advisor` | zx-game-design |
| Balance analysis | `game-design:balance-analyzer` | game-design |
| Accessibility audit | `game-design:accessibility-auditor` | game-design |
| **Creative Direction** |||
| Visual coherence | `creative-direction:art-director` | creative-direction |
| Audio coherence | `creative-direction:sound-director` | creative-direction |
| Code architecture | `creative-direction:tech-director` | creative-direction |
| Holistic vision | `creative-direction:creative-director` | creative-direction |
| **Asset Generation** |||
| Style specs from concept | `zx-procgen:asset-designer` | zx-procgen |
| Code from specs | `zx-procgen:asset-generator` | zx-procgen |
| Spec compliance check | `zx-procgen:asset-critic` | zx-procgen |
| ZX budget validation | `zx-procgen:asset-quality-reviewer` | zx-procgen |
| Quality improvement | `zx-procgen:quality-enhancer` | zx-procgen |
| Full character pipeline | `zx-procgen:character-generator` | zx-procgen |
| Full asset pipeline | `zx-procgen:creative-orchestrator` | zx-procgen |
| **Sound Design** |||
| Creative → audio specs | `sound-design:sonic-designer` | sound-design |
| SFX implementation | `sound-design:sfx-architect` | sound-design |
| Music composition | `sound-design:music-architect` | sound-design |
| Audio coherence review | `sound-design:audio-coherence-reviewer` | sound-design |
| **Code Development** |||
| Scaffold game systems | `zx-dev:code-scaffolder` | zx-dev |
| Full feature implementation | `zx-dev:feature-implementer` | zx-dev |
| Asset integration | `zx-dev:integration-assistant` | zx-dev |
| Rollback safety review | `zx-dev:rollback-reviewer` | zx-dev |
| **Testing & QA** |||
| Run test suite | `zx-test:test-runner` | zx-test |
| Debug desync issues | `zx-test:desync-investigator` | zx-test |
| **Optimization** |||
| Analyze build size | `zx-optimize:build-analyzer` | zx-optimize |
| Apply optimizations | `zx-optimize:optimizer` | zx-optimize |
| **Publishing** |||
| Release validation | `zx-publish:release-validator` | zx-publish |
| Autonomous publish prep | `zx-publish:publish-preparer` | zx-publish |
| **CI/CD** |||
| Set up GitHub Actions | `zx-cicd:ci-scaffolder` | zx-cicd |
| Optimize pipeline | `zx-cicd:pipeline-optimizer` | zx-cicd |
| Add quality gates | `zx-cicd:quality-gate-enforcer` | zx-cicd |
| **Orchestration** |||
| Full game pipeline | `zx-orchestrator:game-orchestrator` | zx-orchestrator |
| Parallel task coordination | `zx-orchestrator:parallel-coordinator` | zx-orchestrator |
| Request routing | `ai-game-studio:request-dispatcher` | ai-game-studio |
| Completion verification | `ai-game-studio:completion-auditor` | ai-game-studio |
| Next step suggestion | `ai-game-studio:next-step-suggester` | ai-game-studio |
| Project health check | `ai-game-studio:project-health-monitor` | ai-game-studio |

## Invocation Patterns

### Single Agent
```
Task tool with subagent_type="zx-procgen:asset-generator"
```

### Parallel Agents
Send multiple Task tool calls in a single message:
```
Task 1: subagent_type="zx-procgen:asset-generator", prompt="Generate mesh..."
Task 2: subagent_type="sound-design:sfx-architect", prompt="Create SFX..."
```

### Background Agent
```
Task tool with subagent_type="zx-test:test-runner", run_in_background=true
```

### Resume Agent
```
Task tool with resume="{agent_id_from_previous_run}"
```

## Agent Categories

### Proactive Agents
These should be invoked automatically when conditions are met:
- `ai-game-studio:completion-auditor` - After any significant work
- `zx-publish:release-validator` - After builds, before release
- `zx-game-design:scope-advisor` - When design seems ambitious
- `game-design:accessibility-auditor` - When reviewing designs

### Domain Experts
Route based on domain:
- **Visual**: art-director, asset-designer, asset-generator
- **Audio**: sound-director, sonic-designer, sfx-architect, music-architect
- **Code**: tech-director, code-scaffolder, feature-implementer
- **Design**: gdd-generator, mechanic-designer, balance-analyzer

### Meta-Orchestrators
For complex multi-domain requests:
- `ai-game-studio:request-dispatcher` - Parses intent, routes to experts
- `zx-orchestrator:game-orchestrator` - Full pipeline coordination
- `zx-procgen:creative-orchestrator` - Asset pipeline coordination
