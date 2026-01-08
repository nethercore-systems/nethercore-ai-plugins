# Canonical Mesh Modeling Coordinates (Characters)

> Status: Implemented
> Last reviewed: 2026-01-08

This document is the single source of truth for **character mesh construction** axes and operations (extrude+scale) as implemented by:
- `nethercore-ai-plugins/zx-procgen/scaffold/.studio/parsers/character.py`
- `nethercore-ai-plugins/zx-procgen/skills/procedural-characters/references/bpy-implementation.md`

**Important:** This is **not** the same thing as animation pose-bone rotation axes. Animation `pitch/yaw/roll` semantics are defined by the animation pipeline (`animation.py`) and related docs; do not reuse this table for animation.

## Coordinate Convention (Mesh Local Space → Bone Space)

All step operations (`extrude`, `scale`, `translate`, `bulge`, `tilt`, `rotate`) happen in **mesh local space** while the part is being built. After the part is built, the entire object is aligned to the target bone via `get_bone_transform()`.

For a given bone, `get_bone_transform()` constructs a per-bone basis:

| Mesh Local Axis | Meaning in character generator | Code definition |
|-----------------|--------------------------------|----------------|
| **+Z** | Extrusion axis | `bone_dir = normalize(tail - head)` |
| **+Y** | “Forward” axis for bulge/translate | `bone_forward = project(world_forward, plane ⟂ bone_dir)`; fallback to projecting `world_up` if degenerate |
| **+X** | Lateral axis (completes the basis) | `bone_lateral = bone_dir × bone_forward` |

**Notes (critical for avoiding regressions):**
- “Forward” is derived from world +Y **unless** the bone is near-parallel to world +Y, in which case the fallback uses world +Z. This fallback is part of the convention.
- The +X axis is derived from a cross product; do **not** assume it always matches world +X (“character right”) for every bone direction.

## Operation Reference (Character Specs)

### Scale
```python
scale: 0.9           # Uniform 0.9x in local X and Y (Z unaffected)
scale: [1.2, 0.8]    # 1.2x along local X, 0.8x along local Y
```

### Translate
```python
translate: [0.01, 0, 0]    # Shift along local +X (lateral)
translate: [0, 0.02, 0]    # Shift along local +Y (“forward” for this bone)
translate: [0, 0, 0.01]    # Shift along local +Z (bone direction)
```

### Bulge
```python
bulge: 0.03               # Bulge toward local +Y
bulge: -0.02              # Bulge toward local -Y
bulge: [0.01, -0.02]      # [side_bulge, forward_back_bulge]
```

**Anatomical examples (assuming the bone uses world-forward as +Y):**
- Chest: `bulge: 0.02` (forward)
- Glutes: `bulge: -0.02` (backward)
- Calves: `bulge: -0.015` (backward)

### Tilt
```python
tilt: 5                   # Tilt around local +X (sideways)
tilt: [0, 10]             # Tilt around local +Y (forward/back)
```

### Rotate
```python
rotate: 15                # Rotate around local +Z (extrusion axis), degrees
```

## Implementation Anchor (Why This Works)

The implementation intentionally uses fixed local axes when applying bulge/tilt:

```python
# In apply_bulge() and apply_tilt():
forward = Vector((0, 1, 0))  # Always +Y in mesh local space
right = Vector((1, 0, 0))    # Always +X in mesh local space
```

Those local axes only have stable meaning because `get_bone_transform()` defines how the part’s local frame maps to the bone’s oriented frame.
