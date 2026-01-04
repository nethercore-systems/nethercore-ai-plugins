---
name: Procedural Animation Generation
description: |
  Use this skill to CREATE ANIMATIONS for ZX game assets.

  **Triggers:** "animate mesh", "walk cycle", "skeletal animation", "rig character", "bone weights", "keyframe animation", "spinning pickup"

  **Before animating:** Check `.studio/visual-style.local.md` for animation feel.

  **Two-Stage Workflow:**
  1. `motion-describer` agent → Semantic motion description (YAML)
  2. `animation-coder` agent → Blender bpy code with coordinate reasoning

  **Load references when:**
  - Motion description format → `references/motion-description-format.md`
  - IK setup for locomotion → `references/ik-utilities.md`
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
version: 3.0.0
---

# Procedural Animation Generation

Create animated 3D objects using Blender's Python API (bpy) in headless mode.

## Two-Stage Animation Pipeline

Complex animations use a two-stage approach to avoid coordinate confusion:

```
┌─────────────────────────────────────────────────────────────┐
│  Stage 1: motion-describer agent                            │
│  ─────────────────────────────────────────────────          │
│  Input: "Create aggressive overhead sword slash"            │
│  Output: Motion description YAML (semantic, no coordinates) │
│                                                             │
│  Uses: Animation principles, anatomy knowledge              │
│  Does NOT: Write code or specify rotation values            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Stage 2: animation-coder agent                             │
│  ───────────────────────────────────────────────            │
│  Input: Motion description YAML                             │
│  Output: Blender bpy Python code                            │
│                                                             │
│  Uses: Coordinate reasoning protocol, IK utilities          │
│  Produces: Working animation script with reasoning comments │
└─────────────────────────────────────────────────────────────┘
```

**Why two stages?** LLMs confuse coordinate spaces when translating motion intent directly to rotation values. Separating semantic description from coordinate math prevents errors.

## Prerequisites

Blender 3.0+ installed and accessible via PATH:
```bash
blender --version
```

## Decision Trees

### Animation Type

```
Does the mesh need to DEFORM (bend/stretch)?
    │
    ├── NO → OBJECT ANIMATION (Workflow 1)
    │        Transform object as whole, no armature
    │
    └── YES → SKELETAL ANIMATION (Workflow 2)
              Bones move vertices, requires armature + skinning
```

### IK vs FK

```
Does animation involve ground contact or reaching targets?
    │
    ├── LOCOMOTION (walk/run) → Use IK for feet, FK for upper body
    │   Bake IK to FK before export
    │
    ├── CLIMBING/GRABBING → Use IK for hands and/or feet
    │   Bake IK to FK before export
    │
    └── ATTACKS/GESTURES/IDLE → Use FK only
        Arcs and rotations are naturally FK
```

## Quick Reference

| Animation Type | Approach | Reason |
|---------------|----------|--------|
| Walk/run cycles | IK feet + FK upper | Precise foot placement |
| Idle/breathing | FK only | No contact points |
| Sword swings | FK only | Arcs are rotational |
| Climbing | IK hands + IK feet | Goal positions matter |
| Jumping | IK feet (land) + FK | Contact frames need precision |
| Spinning pickups | Object animation | No deformation |

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

## Skeletal Animation with Coordinate Reasoning

**CRITICAL:** Always reason through coordinates before writing rotation values:

```python
# COORDINATE REASONING:
# 1. INTENT: I want the upper arm to pull back behind the shoulder
# 2. BONE: upper_arm.R controls the right shoulder joint
# 3. CONVENTION: Blender armatures are Z-up, bones have Y along axis
# 4. AXIS: For upper arm, local X rotation = forward/back pitch
# 5. SIGN: Pulling BACK = negative X rotation
# 6. VALUE: -45 degrees is a reasonable pull-back

upper_arm.rotation_euler.x = math.radians(-45)
```

Every rotation value must have this reasoning as a comment.

## Locomotion with IK

For walk/run cycles, use IK for feet to prevent sliding:

```python
from lib.animation_utils import setup_leg_ik, keyframe_ik_target, bake_ik_to_fk

# Set up IK
setup_leg_ik(armature, 'L')
setup_leg_ik(armature, 'R')

# Keyframe foot POSITIONS (IK solver handles rotations)
keyframe_ik_target(armature, "ik_foot.R", 0, (0.1, 0.3, 0))   # Right forward
keyframe_ik_target(armature, "ik_foot.L", 0, (-0.1, -0.2, 0)) # Left back
# ... more keyframes

# Bake to FK and remove IK (ZX only supports FK)
bake_ik_to_fk(armature, 0, 24)
```

See `references/ik-utilities.md` for complete setup functions.

## Motion Description Format

For the two-stage pipeline, motion is described semantically:

```yaml
animation:
  name: overhead_sword_slash
  duration_frames: 24
  fps: 30
  loop: false

  style:
    weight: heavy
    energy: explosive

  phases:
    - name: anticipation
      frames: [0, 8]
      description: "Sword pulled back over right shoulder, elbow high"

    - name: strike
      frames: [8, 14]
      description: "Explosive diagonal swing from high-right to low-left"

  ik_hints:
    feet: ground_contact
    hands: null
```

See `references/motion-description-format.md` for complete spec.

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
    export_animation_mode='ACTIONS',  # Separate clips
    export_skins=True,
    export_all_influences=False,      # Max 4 bones/vertex
)
```

See `references/gltf-export.md` for full export settings.

## File Organization

**One animation per file.** Each animation should have its own Python script:

```
generation/
├── lib/
│   ├── bpy_utils.py          # Mesh helpers (from generator-patterns)
│   └── animation_utils.py    # Keyframe + IK helpers
├── animations/
│   ├── walk_cycle.py         # One file per animation
│   ├── run_cycle.py
│   ├── attack_slash.py
│   └── pickup_spin.py
└── generate_all.py           # Batch runner
```

**File size limit:** ≤150 lines per animation file. Extract reusable patterns to `lib/animation_utils.py`.

## References

- `references/motion-description-format.md` - Semantic animation spec
- `references/ik-utilities.md` - IK setup and baking functions
- `references/object-animation.md` - Rigid transforms
- `references/armature-creation.md` - Rig setup
- `references/skinning-weights.md` - Bone weights
- `references/keyframe-patterns.md` - Walk cycles, attacks
- `references/bvh-mocap.md` - Motion capture import
- `references/gltf-export.md` - Export settings
- `references/zx-constraints.md` - Platform limits

## Examples

- `examples/walk-cycle-ik.py` - IK-based walk cycle (recommended)
- `examples/walk-cycle.py` - FK-only walk cycle (simpler)
- `examples/spinning-pickup.py` - Object animation
- `examples/door-open-close.py` - Multi-action object
- `examples/humanoid-rig.py` - Full humanoid skeleton

## Related

- `motion-describer` agent - Stage 1: semantic motion descriptions
- `animation-coder` agent - Stage 2: coordinate-aware code generation
- `procedural-meshes` skill - Generate the mesh to animate
- `character-generator` agent - Complete character pipeline
