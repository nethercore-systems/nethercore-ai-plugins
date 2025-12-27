# Plugin Architecture Analysis

## Key Insight

Skills only load **when triggered by keywords**, not all at once. Large skills with implementation code are fine.

**Principle:** Delete redundant content, don't compress valuable reference material.

---

## Existing Plugin Assessment

### procgen: 13 → 10 skills
Delete only truly redundant:
- retro-3d-assets (covered by SADL + textures + meshes)
- advanced-techniques (too vague)
- character-pipeline (keep as agent only)

Keep all others - they contain 250-940 lines of implementation code each.

### game-design: 13 → 10 skills
Merge genuinely overlapping:
- multiplayer-design + multiplayer-rendering + split-screen → multiplayer-patterns
- perspective-patterns → move to zx-dev/camera-systems

### zx-dev: 7 → 5 skills
Merge small related skills:
- stencil-effects + custom-fonts + billboard-particles → rendering-techniques

### publish: 2 skills - no changes
### orchestrator: 1 agent - no changes

### game-design (NEW): 11 skills - no changes needed
Platform-agnostic conceptual design. Well-designed split from zx-game-design:
- game-design = "what to design" (conceptual)
- zx-game-design = "how to implement for ZX" (technical)

Example: Both have `multiplayer-design` but:
- game-design version: co-op patterns, screen sharing, mode selection
- zx-game-design version: GGRS rollback, determinism code, FFI usage

**Fills previously identified gap:** accessibility-ux skill now exists.

---

## New Plugins

Create only what's critically missing:
1. **nethercore-zx-test** - Testing gap is critical
2. **nethercore-zx-optimize** - Resource management gap is critical
3. **nethercore-zx-cicd** - Automation gap is high priority

---

## Totals

| Plugin | Current | After |
|--------|---------|-------|
| zx-dev | 7 | 5 |
| zx-game-design | 13 | 10 |
| zx-procgen | 13 | 10 |
| zx-publish | 2 | 2 |
| zx-orchestrator | 0 | 0 |
| game-design (new) | 11 | 11 |
| **Subtotal existing** | **46** | **38** |
| New: zx-test | - | +2 |
| New: zx-optimize | - | +2 |
| New: zx-cicd | - | +1 |
| **Total** | **46** | **43** |

Net change: -3 skills while adding testing, optimization, and CI/CD.
Accessibility gap now filled by game-design plugin.
