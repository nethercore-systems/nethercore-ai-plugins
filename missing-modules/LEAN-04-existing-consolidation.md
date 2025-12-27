# Existing Plugin Consolidation (Conservative)

Targeted cleanup preserving implementation detail. Skills only load when triggered by keywords, so size matters less than we initially thought.

**Principle:** Delete redundant content, don't compress valuable reference material.

---

## Plugins Requiring No Changes

- **game-design** (11 skills) - Well-designed conceptual plugin, complements zx-game-design
- **zx-publish** (2 skills) - Already lean
- **zx-orchestrator** (1 agent) - Already minimal

---

## Execution Order (Plugins Needing Work)

1. **zx-procgen** (-3 skills) - Remove redundant only
2. **zx-game-design** (-3 skills) - Merge true overlaps
3. **zx-dev** (-2 skills) - Merge small related skills

---

## 1. nethercore-zx-procgen Cleanup

### Current: 13 skills → Target: 10 skills

**KEEP AS-IS (valuable distinct content):**
- procedural-textures (940 lines) - Complete texture generation
- procedural-meshes (926 lines) - Mesh algorithms, formats
- procedural-sounds (443 lines) - Synthesis, ADSR, filters
- procedural-music (254 lines) - XM tracker, composition
- procedural-animations (521 lines) - Motion, locomotion
- skeletal-rigging (458 lines) - Bones, weights, algorithms
- mocap-integration (385 lines) - BVH, retargeting
- procedural-sprites (600 lines) - 2D, tilesets, UI
- semantic-asset-language (382 lines) - SADL specs
- mesh-texturing-workflows (636 lines) - UV projection

**DELETE (redundant or misplaced):**

```
nethercore-ai-plugins/nethercore-zx-procgen/skills/
├── retro-3d-assets/       # DELETE - covered by SADL + textures + meshes
├── advanced-techniques/   # DELETE - too vague, content belongs in specific skills
└── character-pipeline/    # DELETE as skill - keep character-generator AGENT
```

### Step 1: Delete redundant skills

```bash
rm -rf nethercore-ai-plugins/nethercore-zx-procgen/skills/retro-3d-assets
rm -rf nethercore-ai-plugins/nethercore-zx-procgen/skills/advanced-techniques
rm -rf nethercore-ai-plugins/nethercore-zx-procgen/skills/character-pipeline
```

### Step 2: Update plugin.json

Remove the three deleted skills from the skills array. Keep `character-generator` agent.

### Result: 13 → 10 skills
No loss of implementation detail. Removed only redundant/vague content.

---

## 2. nethercore-zx-game-design Consolidation

### Current: 13 skills → Target: 10 skills

These three skills genuinely overlap (all about multiplayer rendering):
- multiplayer-design
- multiplayer-rendering
- split-screen-rendering

### Step 1: Create multiplayer-patterns skill

```
PROMPT FOR CONSOLIDATION:

Read these three skill files:
- nethercore-ai-plugins/nethercore-zx-game-design/skills/multiplayer-design/SKILL.md
- nethercore-ai-plugins/nethercore-zx-game-design/skills/multiplayer-rendering/SKILL.md
- nethercore-ai-plugins/nethercore-zx-game-design/skills/split-screen-rendering/SKILL.md

These skills genuinely overlap - they all cover multiplayer game development.
Create a consolidated skill called "multiplayer-patterns" that combines them.

Requirements:
- Version: 2.0.0
- Structure:
  1. Netcode Fundamentals (GGRS, determinism)
  2. State Design (rollback-safe patterns)
  3. Viewport Management (split-screen layouts)
  4. Rendering Strategies (per-player cameras)
- PRESERVE all code examples and tables
- Remove only duplicate explanations of the same concept
- Keywords: multiplayer, netcode, rollback, split-screen, coop, versus, determinism, viewport

Write to: nethercore-ai-plugins/nethercore-zx-game-design/skills/multiplayer-patterns/SKILL.md
```

### Step 2: Move perspective-patterns to zx-dev

```
PROMPT:

Read: nethercore-ai-plugins/nethercore-zx-game-design/skills/perspective-patterns/SKILL.md
Read: nethercore-ai-plugins/nethercore-zx-dev/skills/camera-systems/SKILL.md

Perspective patterns ARE camera patterns. Merge perspective-patterns INTO camera-systems.
- Add perspective content as a new section
- Update camera-systems to version 2.0.0
- Preserve all code examples from both files
```

### Step 3: Delete merged skills

```bash
rm -rf nethercore-ai-plugins/nethercore-zx-game-design/skills/multiplayer-design
rm -rf nethercore-ai-plugins/nethercore-zx-game-design/skills/multiplayer-rendering
rm -rf nethercore-ai-plugins/nethercore-zx-game-design/skills/split-screen-rendering
rm -rf nethercore-ai-plugins/nethercore-zx-game-design/skills/perspective-patterns
```

### Step 4: Update plugin.json

Remove deleted skills, add multiplayer-patterns.

### Result: 13 → 10 skills
Merged truly overlapping content. No loss of unique information.

---

## 3. nethercore-zx-dev Consolidation

### Current: 7 skills → Target: 5 skills

These three are small and closely related (all advanced rendering):
- stencil-effects
- custom-fonts
- billboard-particles

### Step 1: Create rendering-techniques skill

```
PROMPT FOR CONSOLIDATION:

Read these three skill files:
- nethercore-ai-plugins/nethercore-zx-dev/skills/stencil-effects/SKILL.md
- nethercore-ai-plugins/nethercore-zx-dev/skills/custom-fonts/SKILL.md
- nethercore-ai-plugins/nethercore-zx-dev/skills/billboard-particles/SKILL.md

These are all advanced rendering techniques. Combine into one skill.

Requirements:
- Version: 1.0.0
- Structure:
  1. Stencil Buffer (masking, portals, outlines)
  2. Text Rendering (fonts, glyph atlases)
  3. Billboards & Particles (camera-facing, effects)
- PRESERVE all code examples
- Keywords: stencil, font, text, billboard, particle, render, effect, mask

Write to: nethercore-ai-plugins/nethercore-zx-dev/skills/rendering-techniques/SKILL.md
```

### Step 2: Delete merged skills

```bash
rm -rf nethercore-ai-plugins/nethercore-zx-dev/skills/stencil-effects
rm -rf nethercore-ai-plugins/nethercore-zx-dev/skills/custom-fonts
rm -rf nethercore-ai-plugins/nethercore-zx-dev/skills/billboard-particles
```

### Step 3: Update plugin.json

### Result: 7 → 5 skills

---

## Summary

| Plugin | Before | After | Deleted | Merged |
|--------|--------|-------|---------|--------|
| procgen | 13 | 10 | 3 | 0 |
| game-design | 13 | 10 | 4 | 3→1 |
| zx-dev | 7 | 5 | 3 | 3→1 |
| publish | 2 | 2 | 0 | 0 |
| orchestrator | 0 | 0 | 0 | 0 |
| **Total** | **35** | **27** | **10** | **6→2** |

**Net reduction: 8 skills (23%)**

---

## Validation Checklist

After consolidation:
- [x] All plugin.json files updated
- [x] No broken skill references
- [x] Keywords cover all merged content
- [x] Code examples preserved
- [ ] Test skill triggering works
- [x] Agents still reference correct skills

## Consolidation Status

**COMPLETED** - December 2024

The following consolidations have been implemented:

### zx-procgen: 13 → 10 skills
- Deleted: `retro-3d-assets`, `advanced-techniques`, `character-pipeline` (skill only, agent preserved)

### zx-game-design: 14 → 10 skills
- Created: `multiplayer-patterns` (merged from `multiplayer-design`, `multiplayer-rendering`, `split-screen-rendering`)
- Moved: `perspective-patterns` content merged into `zx-dev/camera-systems`
- Deleted: `multiplayer-design`, `multiplayer-rendering`, `split-screen-rendering`, `perspective-patterns`

### zx-dev: 7 → 5 skills
- Created: `rendering-techniques` (merged from `stencil-effects`, `custom-fonts`, `billboard-particles`)
- Updated: `camera-systems` (now includes perspective-based design patterns)
- Deleted: `stencil-effects`, `custom-fonts`, `billboard-particles`

**Net result: 35 → 25 skills across consolidated plugins (29% reduction)**
