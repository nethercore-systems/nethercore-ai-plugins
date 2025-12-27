# Missing Modules - Nethercore AI Plugins

This directory contains specifications for plugins and plugin enhancements that address gaps in the current Nethercore ZX game development workflow.

> **IMPORTANT**: See [00-CRITICAL-ANALYSIS.md](./00-CRITICAL-ANALYSIS.md) for context efficiency analysis. The original specs were too bloated. Use the **LEAN-** prefixed versions for actual implementation.

## Quick Start

**Recommended approach:**
1. First consolidate existing plugins → [LEAN-04-existing-consolidation.md](./LEAN-04-existing-consolidation.md)
2. Then add only critical new plugins:
   - [LEAN-01-nethercore-zx-test.md](./LEAN-01-nethercore-zx-test.md) (2 skills, 2 agents)
   - [LEAN-02-nethercore-zx-optimize.md](./LEAN-02-nethercore-zx-optimize.md) (2 skills, 2 agents)
   - [LEAN-03-nethercore-zx-cicd.md](./LEAN-03-nethercore-zx-cicd.md) (1 skill, 1 agent)

**Total new content**: 5 skills, 5 agents
**After consolidation**: 46 → 38 existing, +5 new = 43 total (-3 net)

> **Note:** The new `game-design` plugin (11 skills) fills the accessibility gap we identified. No consolidation needed for it - well-designed conceptual/implementation split with `zx-game-design`.

---

## Overview

After thorough analysis of the existing 5 plugins (28 skills, 8 commands, 10 agents), these gaps were identified:

| Area | Current Coverage | Gap Level |
|------|------------------|-----------|
| Concept/Design | 95% | Low |
| Asset Creation | 85% | Low-Medium |
| Implementation | 70% | Medium |
| **Testing/QA** | **20%** | **Critical** |
| **Debugging** | **40%** | **High** |
| **Optimization** | **10%** | **Critical** |
| **CI/CD** | **0%** | **High** |
| Publishing | 75% | Medium |

---

## New Plugins (Critical Priority)

### 1. [nethercore-zx-test](./01-nethercore-zx-test.md)
**Priority: CRITICAL**

Automated testing and quality assurance:
- Sync test automation
- Replay-based regression testing
- Performance benchmarking
- Determinism verification
- Test generation agents

### 2. [nethercore-zx-optimize](./02-nethercore-zx-optimize.md)
**Priority: CRITICAL**

Performance optimization and resource management:
- Memory profiling (RAM/VRAM analysis)
- ROM size optimization
- WASM code optimization
- Asset optimization pipelines
- Budget tracking and enforcement

### 3. [nethercore-zx-debug](./03-nethercore-zx-debug.md)
**Priority: HIGH**

Advanced debugging workflows:
- Visual debug overlays
- Memory inspection
- State snapshots
- Hot reload workflow
- Desync deep debugging

### 4. [nethercore-zx-cicd](./04-nethercore-zx-cicd.md)
**Priority: HIGH**

CI/CD and release automation:
- GitHub Actions setup
- Automated testing pipelines
- Release management
- Quality gates
- Deployment automation

### 5. [nethercore-zx-network](./05-nethercore-zx-network.md)
**Priority: MEDIUM-HIGH**

Advanced multiplayer development:
- Network condition testing
- Rollback parameter tuning
- Latency compensation
- Netplay debugging
- Session recording/analysis

### 6. [nethercore-zx-accessibility](./06-nethercore-zx-accessibility.md)
**Priority: MEDIUM**

Accessibility and localization:
- Visual/audio/motor/cognitive accessibility
- Localization workflow
- Accessibility settings patterns
- Compliance auditing

---

## Plugin Enhancements

### 7. [nethercore-zx-dev Enhancements](./07-zx-dev-enhancements.md)
**Priority: HIGH**

Additional skills for core development:
- Game architecture patterns (ECS, etc.)
- State machine implementations
- Input handling and buffering
- Physics integration
- Scene management
- Audio integration

### 8. [nethercore-zx-game-design Enhancements](./08-game-design-enhancements.md)
**Priority: MEDIUM**

Additional design workflow capabilities:
- Playtesting workflow
- Game balancing methodology
- Narrative design patterns
- Onboarding design
- Content planning

### 9. [nethercore-zx-publish Enhancements](./09-publish-enhancements.md)
**Priority: MEDIUM**

Version management and updates:
- Semantic versioning
- Update workflow
- Platform API integration
- Release planning
- Game analytics

---

## How to Use These Specs

Each document contains a complete prompt that can be provided to the `plugin-dev:create-plugin` skill:

```
/plugin-dev:create-plugin
```

Then paste the content from the "Plugin Creation Prompt" section of the relevant document.

For enhancement documents, the prompts are designed to extend existing plugins rather than create new ones.

---

## Implementation Priority

### Phase 1 - Critical (Immediate)
1. `nethercore-zx-test` - Testing is foundational
2. `nethercore-zx-optimize` - Resource management affects all games
3. `zx-dev` enhancements - Core architecture patterns

### Phase 2 - High (Next Sprint)
4. `nethercore-zx-debug` - Developer productivity
5. `nethercore-zx-cicd` - Automation reduces errors
6. `nethercore-zx-network` - Multiplayer is a key feature

### Phase 3 - Medium (Following)
7. `nethercore-zx-accessibility` - Broader reach
8. `game-design` enhancements - Design iteration
9. `publish` enhancements - Long-term maintenance

---

## Success Metrics

After implementing these modules, a developer should be able to:

- [ ] Run automated sync tests with actionable feedback
- [ ] Get detailed ROM/RAM/VRAM breakdown with optimization suggestions
- [ ] Set up CI/CD with a single command
- [ ] Debug desyncs with guided workflows
- [ ] Test multiplayer under various network conditions
- [ ] Add accessibility features with generated code
- [ ] Manage game updates with proper versioning
- [ ] Track and interpret game analytics

---

---

## File Index

### Lean Versions (RECOMMENDED)
| File | Content | Token Budget |
|------|---------|--------------|
| [00-CRITICAL-ANALYSIS.md](./00-CRITICAL-ANALYSIS.md) | Why lean matters, bloat analysis | N/A |
| [LEAN-01-nethercore-zx-test.md](./LEAN-01-nethercore-zx-test.md) | Testing plugin | ~2000 |
| [LEAN-02-nethercore-zx-optimize.md](./LEAN-02-nethercore-zx-optimize.md) | Optimization plugin | ~2100 |
| [LEAN-03-nethercore-zx-cicd.md](./LEAN-03-nethercore-zx-cicd.md) | CI/CD plugin | ~1500 |
| [LEAN-04-existing-consolidation.md](./LEAN-04-existing-consolidation.md) | Consolidate existing plugins | N/A |

---

## Contributing

When creating these plugins:

1. **Follow lean principles** - max 2-3 skills per plugin
2. **Skills are reference, agents are workflow** - don't mix concerns
3. **Set token budgets** - aim for <1000 tokens per skill
4. **Consolidate first** - check if content belongs in existing plugin
5. **Test context usage** - verify skills don't bloat conversations
6. Reference documentation in `nethercore/docs/`
