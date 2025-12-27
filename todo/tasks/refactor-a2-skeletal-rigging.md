# Refactor A2: Skeletal Rigging Skill

**Status:** `[x]` COMPLETED
**Priority:** MEDIUM
**Action:** Split procedural-animations into separate skeletal-rigging skill

---

## Problem

The procedural-animations skill currently mixes:
1. Skeleton creation and bone hierarchy
2. Skinning / weight painting
3. Animation generation (motion)

This makes it hard to:
- Use rigging without animation
- Understand the animation-ready mesh requirements
- Find specific rigging information

## Current State

- Plugin: `nethercore-zx-procgen`
- Skill: `procedural-animations` (covers everything)

## Proposed Change

Split into:
- `skeletal-rigging` - Skeleton creation, bone weights, skinning
- `procedural-animations` - Motion generation, animation clips (keeps name)

## Content Distribution

### skeletal-rigging (NEW)
- Bone hierarchy creation
- Inverse bind matrix calculation
- Bone weight algorithms (distance, heat diffusion, geodesic)
- 4-bones-per-vertex ZX constraint
- Skinned mesh export format

### procedural-animations (UPDATED)
- Procedural motion generation
- Walk/run/idle cycles
- Animation state machines
- Blending and transitions

## Implementation Steps

1. Create new skill file `skeletal-rigging.md`
2. Move rigging content from procedural-animations
3. Update procedural-animations to focus on motion
4. Add cross-references between skills
5. Update triggers for both skills

## Dependencies

- Gap 15 (Character Pipeline) benefits from this split
- Gap 21 (Mocap) uses skeletal-rigging for retargeting

## Related Gaps

- Gap 15 (Character Pipeline)
- Gap 21 (Mocap Integration)
