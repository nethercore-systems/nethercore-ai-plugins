---
name: Procedural Animation Generation
description: |
  Use this skill to CREATE ANIMATIONS for ZX game assets.

  **Triggers:** "animate mesh", "walk cycle", "skeletal animation", "rig character", "bone weights", "keyframe animation", "spinning pickup"

  **Before animating:** Check `.studio/visual-style.md` for animation feel.

  **Workflow:**
  - `motion-describer` agent → Produces `.motion.py` spec with poses
  - `motion_parser.py` → Interprets spec in Blender (no LLM needed)

  **Load references when:**
  - Motion spec format → `references/motion-description-format.md`
  - Motion parser script → `references/motion_parser.py`
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
version: 4.0.0
---

# Procedural Animation Generation

Create animated 3D objects using Blender's Python API (bpy) in headless mode.

## Animation Pipeline

Skeletal animations use a spec-based approach with a reusable parser:

```
┌─────────────────────────────────────────────────────────────┐
│  motion-describer agent                                      │
│  ───────────────────────────────────────────────             │
│  Input: "Create idle animation for knight"                   │
│  Output: .studio/animations/knight_idle.motion.py            │
│                                                              │
│  Produces structured poses with bone rotations (degrees)    │
│  Uses: Animation principles, character personality          │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  motion_parser.py (reusable script)                          │
│  ────────────────────────────────────                        │
│  Input: .motion.py spec + armature .glb                      │
│  Output: Animated .glb with keyframes                        │
│                                                              │
│  blender --background --python motion_parser.py -- \         │
│      spec.motion.py armature.glb output.glb                  │
└─────────────────────────────────────────────────────────────┘
```

**Why this architecture?**

1. **No PyYAML dependency** — Python literals work natively in Blender
2. **No LLM in generation loop** — Parser is deterministic, reusable
3. **Skeleton-agnostic** — Works with any armature if bone names match
4. **Explicit rotations** — No coordinate confusion from natural language

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

## Motion Spec Format

Motion specs are Python files (`.motion.py`) with structured pose data:

```python
# Idle Animation - Knight character
# Duration: 120 frames @ 60fps

MOTION = {
    "animation": {
        "name": "knight_idle",
        "duration_frames": 120,
        "fps": 60,
        "loop": True,

        "poses": {
            "idle_base": {
                "Hips": {"pitch": -3, "yaw": 0, "roll": 0},
                "Spine": {"pitch": 2, "yaw": 0, "roll": 0},
                "Head": {"pitch": -2, "yaw": 0, "roll": 0},
                # ... more bones with pitch/yaw/roll in degrees
            },
            "breath_peak": {
                "Chest": {"pitch": 3, "yaw": 0, "roll": 0},
            },
        },

        "phases": [
            {
                "name": "neutral",
                "frames": [0, 29],
                "pose": "idle_base",
                "timing_curve": "linear"
            },
            {
                "name": "inhale",
                "frames": [30, 59],
                "pose": "breath_peak",
                "timing_curve": "ease_in_out"
            },
        ],

        "procedural_layers": [
            {
                "type": "breathing",
                "target": "Chest",
                "period_frames": 90,
                "amplitude": 0.02,
                "axis": "pitch"
            },
        ],

        "ik_hints": {
            "feet": None,
            "hands": None
        },

        "style": {
            "weight": "medium",
            "energy": "calm",
            "intent": "idle"
        }
    }
}
```

See `references/motion-description-format.md` for complete spec.

## Basic Object Animation

For rigid objects (no skeleton):

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

## Rotation Convention

All rotations in motion specs use **degrees** with **pitch/yaw/roll**:

| Term | Axis | Humanoid Example |
|------|------|------------------|
| **pitch** | X | Nodding head, bending elbow |
| **yaw** | Y | Twisting spine, turning head |
| **roll** | Z | Tilting head, side-bending |

The parser converts degrees to radians automatically.

## Locomotion with IK

For walk/run cycles, use IK for feet to prevent sliding:

```python
from lib.animation_utils import setup_leg_ik, keyframe_ik_target, bake_ik_to_fk

# Set up IK
setup_leg_ik(armature, 'L')
setup_leg_ik(armature, 'R')

# Keyframe foot POSITIONS (IK solver handles rotations)
keyframe_ik_target(armature, "ik_foot.R", 0, (0.1, 0.3, 0))
keyframe_ik_target(armature, "ik_foot.L", 0, (-0.1, -0.2, 0))

# Bake to FK and remove IK (ZX only supports FK)
bake_ik_to_fk(armature, 0, 24)
```

See `references/ik-utilities.md` for complete setup functions.

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

```
.studio/
└── animations/
    ├── knight_idle.motion.py     # Motion specs
    ├── knight_walk.motion.py
    └── knight_attack.motion.py

generation/
├── lib/
│   ├── bpy_utils.py              # Mesh helpers
│   ├── animation_utils.py        # Keyframe + IK helpers
│   └── motion_parser.py          # Motion spec parser
└── animations/
    └── object_spin.py            # Object animation scripts

assets/
└── animations/
    ├── knight_idle.glb           # Generated animations
    ├── knight_walk.glb
    └── knight_attack.glb
```

## Running the Parser

```bash
blender --background --python generation/lib/motion_parser.py -- \
    .studio/animations/knight_idle.motion.py \
    assets/characters/knight.glb \
    assets/animations/knight_idle.glb
```

Or batch process:
```bash
python generation/generate_all_animations.py
```

## References

- `references/motion-description-format.md` - Motion spec format (`.motion.py`)
- `references/motion_parser.py` - Reusable Blender parser script
- `references/ik-utilities.md` - IK setup and baking functions
- `references/object-animation.md` - Rigid transforms
- `references/armature-creation.md` - Rig setup
- `references/skinning-weights.md` - Bone weights
- `references/keyframe-patterns.md` - Walk cycles, attacks
- `references/bvh-mocap.md` - Motion capture import
- `references/gltf-export.md` - Export settings
- `references/zx-constraints.md` - Platform limits

## Examples

- `examples/idle.motion.py` - Idle animation motion spec
- `examples/spinning-pickup.py` - Object animation
- `examples/door-open-close.py` - Multi-action object
- `examples/humanoid-rig.py` - Full humanoid skeleton

## Related

- `motion-describer` agent - Produces `.motion.py` specs from descriptions
- `procedural-meshes` skill - Generate the mesh to animate
- `character-generator` agent - Complete character pipeline
