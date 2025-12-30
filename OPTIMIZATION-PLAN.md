# Nethercore AI Plugins Optimization Plan

## ✅ COMPLETED - December 2024

All phases have been implemented. See results below.

## Results Summary

| Phase | Status | Key Changes |
|-------|--------|-------------|
| Phase 1: Split SKILL.md files | ✅ Complete | 5 skills split, 19 new reference files |
| Phase 2: Agent registry | ✅ Complete | Created `agent-registry` skill (114 lines) |
| Phase 3: Slim orchestrators | ✅ Complete | ~98 lines removed from 3 agents |
| Phase 4: Split mega references | ✅ Complete | material-database.md: 1068→65 lines |
| Phase 5: Loading hints | ✅ Complete | 3+ skills updated with hints |
| Phase 6: Verification | ✅ Complete | All files valid |

### Phase 1 Results

| File | Before | After | New References |
|------|--------|-------|----------------|
| procedural-sprites | 687 | 130 | 5 files |
| mesh-texturing-workflows | 635 | 140 | 4 files |
| procedural-instruments | 576 | 141 | 5 files |
| procedural-animations | 548 | 137 | existing |
| game-feel | 556 | 176 | existing |

### Phase 4 Results

| File | Before | After | Split Into |
|------|--------|-------|------------|
| material-database.md | 1068 | 65 | materials-metals.md (111), materials-natural.md (124), materials-soft.md (108), materials-specialty.md (108) |

---

## Original Plan

This plan addresses context bloat and improves agentic efficiency across all plugins.

**Goals:**
- Reduce average SKILL.md size from ~350 to <250 lines
- Reduce agent prompt size from ~400 to <200 lines
- Eliminate duplicate content across agents
- No single file over 400 lines

---

## Phase 1: Split Oversized SKILL.md Files

**Priority:** HIGH (largest context savings)

### 1.1 procedural-sprites/SKILL.md (687 → ~180 lines)

**Current structure:** Monolithic with inline code

**New structure:**
```
skills/procedural-sprites/
├── SKILL.md                    # Overview + patterns (180 lines)
├── references/
│   ├── palette-algorithms.md   # Median cut, quantization (~150 lines)
│   ├── dithering-patterns.md   # Floyd-Steinberg, ordered (~120 lines)
│   └── sprite-organization.md  # Sheets, autotiles, 9-slice (~100 lines)
└── examples/
    ├── indexed-sprite.md       # Complete indexed palette example
    └── tileset-generator.md    # Tileset generation example
```

### 1.2 mesh-texturing-workflows/SKILL.md (635 → ~200 lines)

**New structure:**
```
skills/mesh-texturing-workflows/
├── SKILL.md                    # Overview + workflow selection (200 lines)
├── references/
│   ├── uv-projection.md        # Projection algorithms (~150 lines)
│   ├── atlas-packing.md        # Atlas generation (~100 lines)
│   └── baking-workflows.md     # AO, normal, curvature (~150 lines)
└── examples/
    └── complete-workflow.md    # End-to-end example
```

### 1.3 procedural-instruments/SKILL.md (576 → ~200 lines)

**New structure:**
```
skills/procedural-instruments/
├── SKILL.md                    # Overview + instrument types (200 lines)
├── references/
│   ├── synthesis-algorithms.md # FM, additive, subtractive (~200 lines)
│   ├── envelope-patterns.md    # ADSR, multi-stage (~100 lines)
│   └── instrument-presets.md   # Common instrument recipes (~150 lines)
└── examples/
    └── piano-synthesis.md      # Complete piano example
```

### 1.4 procedural-animations/SKILL.md (548 → ~200 lines)

**New structure:**
```
skills/procedural-animations/
├── SKILL.md                    # Overview + animation types (200 lines)
├── references/
│   ├── keyframe-math.md        # Interpolation, easing (~100 lines)
│   ├── skeletal-rigging.md     # Bone setup, skinning (~150 lines)
│   └── cycle-patterns.md       # Walk, run, attack cycles (~150 lines)
└── examples/
    └── walk-cycle.md           # Complete walk cycle
```

### 1.5 game-feel/SKILL.md (556 → ~200 lines)

**New structure:**
```
skills/game-feel/
├── SKILL.md                    # Core concepts + quick reference (200 lines)
├── references/
│   ├── juice-techniques.md     # Screen shake, particles, etc. (~150 lines)
│   ├── timing-curves.md        # Easing, anticipation (~100 lines)
│   └── feedback-patterns.md    # Hit stops, flashes (~100 lines)
```

---

## Phase 2: Create Shared Agent Registry Skill

**Priority:** HIGH (eliminates duplication across 3+ agents)

### 2.1 Create new skill: zx-orchestrator/skills/agent-registry/

```
skills/agent-registry/
├── SKILL.md                    # When to use which agent (~150 lines)
└── references/
    └── full-registry.md        # Complete table with subagent_types (~200 lines)
```

**SKILL.md content:**
- Quick decision tree for agent selection
- Agent categories (Analysis, Implementation, Assets, Audio, Review, Testing)
- Links to full-registry.md for complete list

### 2.2 Update agents to reference skill

Remove inline agent tables from:
- `game-orchestrator.md`
- `request-dispatcher.md`
- `parallel-coordinator.md`

Replace with: "For complete agent registry, see agent-registry skill."

---

## Phase 3: Slim Down Orchestrator Agents

**Priority:** HIGH

### 3.1 game-orchestrator.md (606 → ~250 lines)

**Remove:**
- Inline agent registry (lines 481-522) → reference skill
- Full progress tracking template (lines 298-344) → reference project-status skill
- Detailed plugin invocation examples (lines 227-292) → can be inferred

**Keep:**
- Core orchestration philosophy
- 7-phase pipeline overview (compact)
- When to ask user (CRITICAL section)
- Verification requirements

### 3.2 request-dispatcher.md (406 → ~200 lines)

**Remove:**
- Agent registry tables (lines 119-164) → reference skill
- Detailed output format templates (lines 315-366) → keep only one example

**Keep:**
- Request classification logic
- Dispatch patterns
- Auto-dispatch rules
- Context propagation requirements

### 3.3 creative-orchestrator.md (559 → ~200 lines)

**Remove:**
- Duplicate pipeline information
- Detailed agent descriptions → reference skills

**Keep:**
- Orchestration logic
- Quality checkpoints
- Asset pipeline coordination

### 3.4 parallel-coordinator.md (480 → ~200 lines)

**Remove:**
- Agent registry duplicates
- Verbose examples

**Keep:**
- Parallelization logic
- Dependency detection
- Coordination patterns

---

## Phase 4: Split Mega Reference Files

**Priority:** MEDIUM

### 4.1 material-database.md (1068 lines)

Split into:
- `materials-metals.md` (~200 lines)
- `materials-organics.md` (~200 lines)
- `materials-stone-earth.md` (~150 lines)
- `materials-fantasy.md` (~150 lines)
- `materials-industrial.md` (~150 lines)

Update parent SKILL.md to reference appropriate section.

### 4.2 quality-heuristics.md (823 lines)

Split into:
- `mesh-quality-heuristics.md` (~250 lines)
- `texture-quality-heuristics.md` (~250 lines)
- `audio-quality-heuristics.md` (~150 lines)
- `animation-quality-heuristics.md` (~150 lines)

### 4.3 dialogue-systems.md (761 lines)

Split into:
- `dialogue-patterns.md` (~250 lines) - Design patterns
- `dialogue-implementation.md` (~250 lines) - Code patterns
- `dialogue-examples.md` (~200 lines) - Complete examples

### 4.4 Other files 500-700 lines

Apply same pattern to:
- `gdd-template-comprehensive.md` (667) → Keep as-is (template file, loaded on demand)
- `procedural-generation.md` (663) → Split if contains multiple topics
- `color-palettes.md` (685) → Split by palette category
- `style-tokens.md` (639) → Split by token type

---

## Phase 5: Add Progressive Loading Hints

**Priority:** MEDIUM

Update skill descriptions to guide Claude on when to load references:

### Pattern:
```yaml
description: |
  Basic [topic] for ZX games.

  **Load references when:**
  - Complex [subtopic A] → references/subtopic-a.md
  - Advanced [subtopic B] → references/subtopic-b.md

  **Quick tasks:** Use patterns in main skill.
  **Deep tasks:** Load appropriate reference.
```

Apply to all skills with multiple reference files.

---

## Phase 6: Verification

### 6.1 File Size Audit

Run after all changes:
```bash
find . -name "*.md" -exec wc -l {} \; | sort -n | tail -20
```

**Targets:**
- No SKILL.md over 300 lines
- No agent .md over 300 lines
- No reference over 400 lines (except templates)

### 6.2 Reference Integrity

Verify all references in SKILL.md files point to existing files:
```bash
grep -r "references/" skills/ | grep -v "^Binary"
```

### 6.3 Plugin Loading Test

Test each plugin loads correctly:
```bash
# Verify plugin.json is valid
for f in */.claude-plugin/plugin.json; do
  python -c "import json; json.load(open('$f'))" && echo "OK: $f"
done
```

---

## Execution Order

1. **Phase 1.1-1.5** - Split skills (parallel, independent)
2. **Phase 2** - Create agent-registry (enables Phase 3)
3. **Phase 3** - Slim orchestrators (depends on Phase 2)
4. **Phase 4** - Split references (parallel, independent)
5. **Phase 5** - Add loading hints (after splits complete)
6. **Phase 6** - Verify everything

---

## Rollback Strategy

Before each phase, the changes are isolated to specific files. If issues arise:
1. Git status shows all modified files
2. Git checkout to revert specific files
3. Each phase is independently revertable

---

## Success Metrics

| Metric | Before | Target |
|--------|--------|--------|
| Avg SKILL.md size | ~350 lines | <250 lines |
| Avg agent size | ~400 lines | <200 lines |
| Files >500 lines | 15+ | 0 (except templates) |
| Duplicate agent registries | 3 | 0 |
