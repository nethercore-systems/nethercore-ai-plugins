---
description: This skill provides patterns for classifying and routing game development requests to appropriate expert agents. Use when parsing vague requests like "improve the game", "fix bugs", "make it better", or any multi-domain request that needs intelligent dispatch.
---

# Game Development Request Patterns

Patterns for classifying user requests and routing them to the correct expert agents in the Nethercore plugin ecosystem.

## Request Classification

### Type 1: Quality Improvement Requests

**Trigger phrases:** "improve", "better", "polish", "enhance", "fix quality"

**Classification flow:**
1. Identify domain: visual / audio / code / gameplay
2. Identify scope: specific assets / category / everything
3. Route to appropriate analyzer first, then implementer

**Routing:**
| Domain | Analyzer | Implementer |
|--------|----------|-------------|
| Visual (textures/meshes) | `quality-analyzer` | `asset-generator` |
| Audio | `sound-director` | `sfx-architect` / `music-architect` |
| Code | `tech-director` | `feature-implementer` |
| Gameplay | `design-reviewer` | `feature-implementer` |

**Example:**
```
"Improve the texture quality"
→ Domain: Visual
→ Scope: Textures
→ Route: quality-analyzer (assess) → asset-generator (fix)
```

### Type 2: Bug Fix Requests

**Trigger phrases:** "fix", "broken", "doesn't work", "bug", "issue", "problem"

**Classification by symptom:**
| Symptom | Likely Domain | Route To |
|---------|---------------|----------|
| "Falls through", "clips", "collision" | Physics | `feature-implementer` |
| "Doesn't appear", "invisible", "missing" | Rendering | `completion-auditor` → `feature-implementer` |
| "Sound doesn't play" | Audio integration | `integration-assistant` |
| "Crashes", "panic", "error" | Code | `tech-director` → `feature-implementer` |
| "Desyncs", "rollback issues" | Netcode | `rollback-reviewer` → `desync-investigator` |
| "Slow", "lag", "stutters" | Performance | `build-analyzer` → `optimizer` |

### Type 3: Feature Requests

**Trigger phrases:** "add", "implement", "create", "build", "make"

**Classification flow:**
1. Check if feature is in GDD → `gdd-implementation-tracker`
2. Identify required components (code, assets, audio)
3. Route to appropriate implementers

**Routing by feature type:**
| Feature Type | Primary Agent | Supporting Agents |
|--------------|---------------|-------------------|
| Game mechanic | `feature-implementer` | - |
| Visual feature | `feature-implementer` | `asset-generator`, `integration-assistant` |
| Audio feature | `feature-implementer` | `sfx-architect`, `integration-assistant` |
| UI element | `feature-implementer` | - |
| Complete system | `feature-implementer` | Multiple as needed |

### Type 4: Discovery Requests

**Trigger phrases:** "what's missing", "status", "progress", "what should I", "next steps"

**Route directly to:**
- `project-health-monitor` for comprehensive status
- `gdd-implementation-tracker` for feature gaps specifically

### Type 5: Asset Requests

**Trigger phrases:** "generate", "create asset", "make texture/mesh/sound"

**Routing:**
| Asset Type | Design Agent | Generation Agent |
|------------|--------------|------------------|
| Texture | `asset-designer` | `asset-generator` |
| Mesh | `asset-designer` | `asset-generator` |
| Character | `asset-designer` | `character-generator` |
| Sound effect | `sonic-designer` | `sfx-architect` |
| Music | `sonic-designer` | `music-architect` |

**Always follow with:** `integration-assistant` to connect assets to game

### Type 6: Review Requests

**Trigger phrases:** "review", "check", "audit", "validate"

**Routing:**
| Review Type | Agent |
|-------------|-------|
| Code quality | `tech-director` |
| Visual coherence | `art-director` |
| Audio coherence | `sound-director` |
| Overall vision | `creative-director` |
| GDD alignment | `gdd-implementation-tracker` |
| Release readiness | `release-validator` |
| Netcode safety | `rollback-reviewer` |

## Vague Request Handling

When requests are vague, gather requirements before routing:

### "Make it better"
Ask:
1. What feels wrong? (gameplay / visuals / audio / performance)
2. Any specific examples of what's not working?
3. What would "better" look like?

### "Fix the bugs"
Ask:
1. What symptoms are you seeing?
2. When does it happen? (specific action/trigger)
3. Is it consistent or intermittent?

### "Improve quality"
Ask:
1. Which assets/features need improvement?
2. What aspect of quality? (detail / performance / style)
3. Any reference for target quality?

## Multi-Domain Request Decomposition

For requests spanning multiple domains:

1. **Identify all domains** involved
2. **Check dependencies** between domains
3. **Order tasks** by dependency (design → generate → integrate)
4. **Parallelize** independent tasks
5. **Verify** each domain before declaring complete

**Example: "Add a power-up system with visual effects and sounds"**
```
Domains: Gameplay + Visual + Audio

Tasks:
1. [Parallel] Design power-up mechanics (mechanic-designer)
2. [Parallel] Design power-up visuals (asset-designer)
3. [Parallel] Design power-up sounds (sonic-designer)
4. [After 2] Generate visual assets (asset-generator)
5. [After 3] Generate audio assets (sfx-architect)
6. [After 1,4,5] Implement system (feature-implementer)
7. [After 6] Integrate assets (integration-assistant)
8. [After 7] Verify completion (completion-auditor)
```

## Agent Quick Reference

### Analysis Agents
- `project-health-monitor` - Overall project health
- `gdd-implementation-tracker` - Feature gap analysis
- `quality-analyzer` - Asset quality assessment
- `completion-auditor` - Semantic verification

### Direction Agents
- `creative-director` - Overall vision
- `art-director` - Visual coherence
- `sound-director` - Audio coherence
- `tech-director` - Code quality

### Implementation Agents
- `feature-implementer` - Complete features
- `code-scaffolder` - Boilerplate code
- `integration-assistant` - Asset hookup

### Asset Agents
- `asset-designer` - SADL specs
- `asset-generator` - Procedural code
- `character-generator` - Full characters
- `sfx-architect` - Sound effects
- `music-architect` - Music tracks

### Validation Agents
- `rollback-reviewer` - Netcode safety
- `release-validator` - Release readiness
- `test-runner` - Sync tests
