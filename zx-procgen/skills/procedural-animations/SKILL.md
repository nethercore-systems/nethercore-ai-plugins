---
name: Procedural Animation Generation
description: |
  Use this skill to CREATE ANIMATIONS for ZX game assets.

  **Triggers:** "animate mesh", "walk cycle", "skeletal animation", "rig character", "bone weights", "keyframe animation", "spinning pickup"

  **Before animating:** Check `.studio/visual-style.local.md` for animation feel.

  **Load references when:**
  - Project structure, multiple animations → `generator-patterns` skill
  - Rigid objects (spinning, bobbing) → `references/object-animation.md`
  - Character rigs → `references/armature-creation.md`
  - Bone weights → `references/skinning-weights.md`
  - Walk/attack cycles → `references/keyframe-patterns.md`
  - Mocap import → `references/bvh-mocap.md`
  - Export settings → `references/gltf-export.md`
  - ZX limits → `references/zx-constraints.md`

  For MESH GENERATION: use `procedural-meshes` skill.
  For CHARACTER RIGS: see `procedural-characters → skeleton-presets.md`.
  For COMPLETE CHARACTERS: use `character-designer` + `character-generator` agents.
version: 2.0.0
---

# Procedural Animation Generation

Create animated 3D objects using Blender's Python API (bpy) in headless mode.

## Prerequisites

Blender 3.0+ installed and accessible via PATH:
```bash
blender --version
```

## Decision Tree

```
Does the mesh need to DEFORM (bend/stretch)?
    │
    ├── NO → OBJECT ANIMATION (Workflow 1)
    │        Transform object as whole, no armature
    │
    └── YES → SKELETAL ANIMATION (Workflow 2)
              Bones move vertices, requires armature + skinning
```

## Quick Reference

| Object Animation | Skeletal Animation |
|------------------|-------------------|
| Spinning pickups | Walking characters |
| Bobbing items | Waving arms |
| Opening doors | Facial expressions |
| Moving platforms | Creature locomotion |
| Rotating fans | Bending limbs |

## Basic Object Animation

```python
import bpy, math

obj = bpy.context.active_object
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 60

# Spinning (linear interpolation)
obj.rotation_euler = (0, 0, 0)
obj.keyframe_insert(data_path="rotation_euler", frame=1)
obj.rotation_euler = (0, 0, math.radians(360))
obj.keyframe_insert(data_path="rotation_euler", frame=60)

# Make linear
for fc in obj.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'LINEAR'
```

See `references/object-animation.md` for bobbing, doors, and more patterns.

## Basic Skeletal Animation

```python
# Create armature
bpy.ops.object.armature_add()
armature = bpy.context.active_object

# Add bones in Edit Mode
bpy.ops.object.mode_set(mode='EDIT')
# ... create bone hierarchy

# Animate in Pose Mode
bpy.ops.object.mode_set(mode='POSE')
bone = armature.pose.bones["Spine"]
bone.rotation_quaternion = (1, 0, 0, 0)
bone.keyframe_insert(data_path="rotation_quaternion", frame=1)
```

See `references/armature-creation.md` for complete rig setup.

## ZX Animation Constraints

| Constraint | Limit | Why |
|------------|-------|-----|
| Bones per mesh | ~30 max | GPU skinning limit |
| Keyframes | Keep minimal | State size |
| Actions per mesh | 1-4 clips | ROM size |
| Frame rate | Match tick rate | Sync with gameplay |

See `references/zx-constraints.md` for optimization techniques.

## Export Pattern

```python
bpy.ops.export_scene.gltf(
    filepath="output.glb",
    export_format='GLB',
    export_animations=True,
    export_skins=True,
)
```

See `references/gltf-export.md` for full export settings.

## File Organization

**One animation per file.** Each animation should have its own Python script:

```
generation/
├── lib/
│   ├── bpy_utils.py          # Mesh helpers (from generator-patterns)
│   └── animation_utils.py    # Keyframe helpers (from generator-patterns)
├── animations/
│   ├── walk_cycle.py         # One file per animation
│   ├── run_cycle.py
│   ├── attack_slash.py
│   ├── pickup_spin.py
│   └── door_open.py
└── generate_all.py           # Batch runner
```

**File size limit:** ≤150 lines per animation file. Extract reusable keyframe patterns to `lib/animation_utils.py`.

For complete setup, see the `generator-patterns` skill.

## References

- `references/object-animation.md` - Rigid transforms
- `references/armature-creation.md` - Rig setup
- `references/skinning-weights.md` - Bone weights
- `references/keyframe-patterns.md` - Walk cycles, attacks
- `references/bvh-mocap.md` - Motion capture import
- `references/gltf-export.md` - Export settings
- `references/zx-constraints.md` - Platform limits

## Related Skills

- `procedural-meshes` - Generate the mesh to animate
- `character-generator` agent - Complete character pipeline
