# Plugin Coverage Gaps - Task Index

Identified gaps in the nethercore-ai-plugins suite for complete end-to-end ZX game development.

## Quick Reference

| Status | Meaning |
|--------|---------|
| `[ ]` | Not started |
| `[~]` | In progress |
| `[x]` | Completed |

---

## Gap Summary

| # | Gap | Priority | Plugin | Type | Task File |
|---|-----|----------|--------|------|-----------|
| 1 | XM Tracker Music | HIGH | procgen | Skill | [gap-01-procedural-music.md](tasks/gap-01-procedural-music.md) |
| 2 | Publishing Workflow | HIGH | NEW | Plugin | [gap-02-publishing-workflow.md](tasks/gap-02-publishing-workflow.md) |
| 3 | Platform Page Assets | HIGH | publish | Skill | [gap-03-platform-assets.md](tasks/gap-03-platform-assets.md) |
| 4 | UI/UX Patterns | MEDIUM | game-design | Skill | [gap-04-ui-patterns.md](tasks/gap-04-ui-patterns.md) |
| 5 | Game Feel / Polish | MEDIUM | game-design | Skill | [gap-05-game-feel.md](tasks/gap-05-game-feel.md) |
| 6 | Testing & Debug | MEDIUM | zx-dev | Skill | [gap-06-debugging-guide.md](tasks/gap-06-debugging-guide.md) |
| 7 | Level Design | LOW | game-design | Skill | [gap-07-level-design.md](tasks/gap-07-level-design.md) |
| 8 | EPU (Environment Processing) | MEDIUM | zx-dev | Skill | [gap-08-environment-effects.md](tasks/gap-08-environment-effects.md) |
| 9 | Split-Screen / Viewport | MEDIUM | game-design | Skill | [gap-09-split-screen.md](tasks/gap-09-split-screen.md) |
| 10 | Stencil / Masked Rendering | LOW | zx-dev | Skill | [gap-10-stencil-effects.md](tasks/gap-10-stencil-effects.md) |
| 11 | Custom Fonts | LOW | zx-dev | Skill | [gap-11-custom-fonts.md](tasks/gap-11-custom-fonts.md) |
| 12 | Save Data Patterns | MEDIUM | game-design | Skill | [gap-12-save-systems.md](tasks/gap-12-save-systems.md) |
| 13 | 3D Billboards & Particles | LOW | zx-dev | Skill | [gap-13-billboard-particles.md](tasks/gap-13-billboard-particles.md) |
| 14 | UV-Aware Texturing & Atlasing | MEDIUM | procgen | Skill | [gap-14-mesh-texturing.md](tasks/gap-14-mesh-texturing.md) |
| 15 | Animated Character Pipeline | HIGH | procgen | Skill+Agent | [gap-15-character-pipeline.md](tasks/gap-15-character-pipeline.md) |
| 16 | Physics & Collision | HIGH | game-design | Skill | [gap-16-physics-collision.md](tasks/gap-16-physics-collision.md) |
| 17 | Camera Implementation | MEDIUM | zx-dev | Skill | [gap-17-camera-systems.md](tasks/gap-17-camera-systems.md) |
| 18 | Gameplay Mechanics Library | MEDIUM | game-design | Skill | [gap-18-gameplay-mechanics.md](tasks/gap-18-gameplay-mechanics.md) |
| 19 | AI & Behavior Patterns | LOW | game-design | Skill | [gap-19-ai-patterns.md](tasks/gap-19-ai-patterns.md) |
| 20 | Multiplayer Rendering Patterns | HIGH | game-design | Skill | [gap-20-multiplayer-rendering.md](tasks/gap-20-multiplayer-rendering.md) |
| 21 | BVH/Motion Capture Integration | HIGH | procgen | Skill | [gap-21-mocap-integration.md](tasks/gap-21-mocap-integration.md) |
| 22 | AI-First Creative Asset Pipeline | HIGH | procgen | Skill+Agents | [gap-22-creative-pipeline.md](tasks/gap-22-creative-pipeline.md) |
| 23 | Advanced Techniques & Decision Guides | MEDIUM | procgen | Skill | [gap-23-advanced-techniques.md](tasks/gap-23-advanced-techniques.md) |
| 24 | 2D Sprite & Pixel Art Generation | MEDIUM | procgen | Skill | [gap-24-procedural-sprites.md](tasks/gap-24-procedural-sprites.md) |
| 25 | Low-Poly Pixel Art 3D | MEDIUM | procgen | Skill | [gap-25-retro-3d-assets.md](tasks/gap-25-retro-3d-assets.md) |

---

## Architectural Refactors

| # | Refactor | Priority | Action | Task File |
|---|----------|----------|--------|-----------|
| A1 | Orchestrator Plugin | MEDIUM | Move game-orchestrator to NEW plugin | [refactor-a1-orchestrator.md](tasks/refactor-a1-orchestrator.md) |
| A2 | Skeletal Rigging Skill | MEDIUM | Split from procedural-animations | [refactor-a2-skeletal-rigging.md](tasks/refactor-a2-skeletal-rigging.md) |
| A3 | Mocap Integration Skill | HIGH | NEW skill for BVH parsing | [refactor-a3-mocap-skill.md](tasks/refactor-a3-mocap-skill.md) |
| A4 | Semantic Asset Language | HIGH | NEW SADL skill | [refactor-a4-sadl-skill.md](tasks/refactor-a4-sadl-skill.md) |
| A5 | Creative Agents Suite | HIGH | NEW agent suite | [refactor-a5-creative-agents.md](tasks/refactor-a5-creative-agents.md) |

---

## Minor Improvements

See [minor-improvements.md](tasks/minor-improvements.md) for:
- Set all plugins to version 1.0
- Set all licenses to MIT & Apache
- Ensure all docs/marketplace/claude.md files are up to date

---

## Implementation Order

### Phase 1: Core Game Development (Must-Have)
- [ ] **Gap 16** - Physics & Collision (CRITICAL)
- [ ] **Gap 20** - Multiplayer Rendering (CRITICAL)
- [ ] **Gap 17** - Camera Implementation
- [ ] **Gap 18** - Gameplay Mechanics

### Phase 1.5: Animation & Creative Infrastructure
- [ ] **Gap 21** - BVH/Motion Capture
- [ ] **Gap 22** - AI-First Creative Pipeline
- [ ] **Gap 23** - Advanced Techniques
- [ ] **A3 + A4 + A5** - Mocap + SADL + Creative Agents

### Phase 2: Asset Pipeline Completion
- [ ] **Gap 1** - Procedural Music
- [ ] **Gap 15 + Gap 14 + A2** - Character Pipeline + UV Texturing + Rigging

### Phase 2.5: 2D & Retro 3D Asset Creation
- [ ] **Gap 24** - 2D Sprites & Pixel Art
- [ ] **Gap 25** - Low-Poly Pixel Art 3D

### Phase 3: End-to-End Workflow
- [ ] **Gaps 2+3** - Publishing + Platform Assets
- [ ] **Gaps 4+5** - UI + Game Feel

### Phase 4: Developer Experience
- [ ] **Gap 6** - Debug Guide
- [ ] **Gap 12** - Save Data Patterns

### Phase 5: Advanced Features
- [ ] **Gaps 8+9** - EPU + Split-Screen
- [ ] **Gap 19** - AI Patterns
- [ ] **Gap 7** - Level Design
- [ ] **Gaps 10+11+13** - Stencil + Fonts + Billboards

### Phase 6: Architectural Cleanup
- [ ] **A1** - Move Orchestrator to dedicated plugin

---

## How to Use This System

1. **Pick a task** from the implementation order above
2. **Open the task file** in `tasks/` directory
3. **Follow the prompt** included in each task file
4. **Mark as complete** in both the task file and this INDEX

Each task file contains:
- Status and priority
- What's missing (the problem)
- The prompt to give to Claude for implementation
- Any related dependencies
