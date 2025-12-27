# Refactor A3: Mocap Integration Skill

**Status:** `[ ]` Not Started
**Priority:** HIGH
**Action:** Create NEW mocap-integration skill for BVH parsing, databases, retargeting

---

## Problem

Motion capture integration doesn't exist. Gap 21 defines what should be covered, this refactor is the implementation action.

## Proposed Skill

- Plugin: `nethercore-zx-procgen`
- Skill: `mocap-integration` (NEW)

## Content

### BVH File Format
- HIERARCHY section parsing
- MOTION section parsing
- Channel ordering (ZXY, XYZ, etc.)
- Coordinate system conversion

### Open Source Databases
- CMU Motion Capture Database (2,605 clips)
- Mixamo (FBX → BVH workflow)
- Truebones free packs
- LaFAN1 research dataset

### Retargeting
- Bone name mapping
- Proportional scaling
- IK for endpoint preservation
- Root motion extraction

### ZX Integration
- BVH → 3x4 matrix conversion
- Animation state machine
- Blending with procedural

## Implementation Steps

1. Create skill file following Gap 21 specification
2. Add BVH parser code examples
3. Add database references with recommended clips
4. Add retargeting algorithms
5. Add ZX conversion code

## Dependencies

- A2 (Skeletal Rigging) provides bone hierarchy context

## Related Gaps

- Gap 21 (BVH/Motion Capture) - this is the implementation of Gap 21
