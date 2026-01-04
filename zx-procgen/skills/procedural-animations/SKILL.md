---
name: Procedural Animation Generation
description: |
  Create animations for ZX game assets using Blender bpy.

  **Triggers:** "animate mesh", "walk cycle", "skeletal animation", "rig character", "keyframe", "spinning pickup"

  **Before animating:** Check `.studio/visual-style.md` for animation feel.

  **Workflow:**
  - `motion-describer` agent → Produces `.motion.py` spec
  - `motion_parser.py` → Interprets spec in Blender

  **Load references when:**
  - Motion spec format → `references/motion-description-format.md`
  - Motion parser → `references/motion_parser.py`
  - IK setup → `references/ik-utilities.md`
  - Object animation → `references/object-animation.md`
  - Armature/rigs → `references/armature-creation.md`
  - Walk/attack cycles → `references/keyframe-patterns.md`
  - Export settings → `references/gltf-export.md`
  - ZX limits → `references/zx-constraints.md`

  **Related skills:**
  - MESH GENERATION: `procedural-meshes`
  - CHARACTER RIGS: `procedural-characters`
version: 4.1.0
---

# Procedural Animation Generation

Create animated 3D objects using Blender's Python API in headless mode.

## Prerequisites

Blender 3.0+ in PATH: `blender --version`

## Animation Type Decision

| Does mesh deform? | Approach |
|-------------------|----------|
| No (spinning, bobbing) | Object animation |
| Yes (bending, stretching) | Skeletal animation |

## Animation Approach Quick Reference

| Animation | Approach | Why |
|-----------|----------|-----|
| Walk/run | IK feet + FK upper | Foot placement |
| Idle/breathing | FK only | No contact |
| Sword swings | FK only | Rotational arcs |
| Climbing | IK hands + feet | Goal positions |
| Spinning pickups | Object animation | No deformation |

## Motion Spec Pipeline

```
motion-describer agent → .motion.py spec → motion_parser.py → .glb
```

**Why this architecture:**
- No PyYAML dependency (Python literals)
- Parser is deterministic, reusable
- Skeleton-agnostic (any armature)
- Explicit rotations (degrees)

## Motion Spec Format

```python
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
            },
        },
        "phases": [
            {"name": "neutral", "frames": [0, 59], "pose": "idle_base"},
        ],
    }
}
```

See `references/motion-description-format.md` for complete spec.

## Rotation Convention

| Term | Axis | Example |
|------|------|---------|
| pitch | X | Nodding, elbow bend |
| yaw | Y | Twisting, turning |
| roll | Z | Tilting, side-bend |

All values in degrees. Parser converts to radians.

## Object Animation (Simple)

```python
import bpy, math

obj = bpy.context.active_object
obj.rotation_euler = (0, 0, 0)
obj.keyframe_insert(data_path="rotation_euler", frame=1)
obj.rotation_euler = (0, 0, math.radians(360))
obj.keyframe_insert(data_path="rotation_euler", frame=60)

for fc in obj.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'LINEAR'
```

See `references/object-animation.md` for bobbing, doors, etc.

## ZX Constraints

| Constraint | Limit |
|------------|-------|
| Bones per mesh | ~30 max |
| Keyframes | Keep minimal |
| Actions per mesh | 1-4 clips |

See `references/zx-constraints.md` for optimization.

## Export

```python
bpy.ops.export_scene.gltf(
    filepath="output.glb",
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_skins=True,
    export_all_influences=False,  # Max 4 bones/vertex
)
```

## Running the Parser

```bash
blender --background --python motion_parser.py -- \
    spec.motion.py input.glb output.glb
```

## File Organization

```
.studio/animations/
├── knight_idle.motion.py
├── knight_walk.motion.py
└── knight_attack.motion.py

generation/lib/
├── animation_utils.py
└── motion_parser.py

assets/animations/
├── knight_idle.glb
└── knight_walk.glb
```
