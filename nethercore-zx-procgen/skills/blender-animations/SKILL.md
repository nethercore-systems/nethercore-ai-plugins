---
name: Blender Animation Generation
description: This skill should be used when the user asks to "animate mesh", "create animation", "rig character", "add bones", "skeletal animation", "walk cycle", "idle animation", "attack animation", "spinning pickup", "bobbing item", "door animation", "platform animation", "export GLB with animation", "keyframe animation", "armature", "bone weights", "skinning", "motion capture", "BVH import", "Rigify", "animation clip", or mentions animating 3D objects, creating skeletal rigs, generating animation clips for glTF export, or procedural motion for game assets. Provides comprehensive Blender bpy workflow for both object/transform animations (rigid objects) and skeletal animations (deforming meshes), outputting game-ready .glb files.
version: 1.0.0
---

# Blender Animation Generation

Create animated 3D objects and characters using Blender's Python API (bpy) in headless mode. Output game-ready `.glb` files with animation clips targeting N64/PS1/PS2 era aesthetics.

## Decision Tree: Object vs Skeletal Animation

When asked to animate something, **first determine which workflow applies**:

```
Does the mesh need to DEFORM (bend/stretch)?
    │
    ├── NO → Use OBJECT ANIMATION (Workflow 1)
    │        Transform the object as a whole
    │        No armature needed
    │
    └── YES → Use SKELETAL ANIMATION (Workflow 2)
              Bones move vertices
              Requires armature + skinning
```

### Quick Reference

| Object Animation | Skeletal Animation |
|------------------|-------------------|
| Spinning pickups | Walking characters |
| Bobbing items | Waving arms |
| Opening doors | Facial expressions |
| Moving platforms | Creature locomotion |
| Rotating fans | Bending limbs |
| Pulsing scale effects | Tail/tentacle physics |
| Camera movements | Any mesh deformation |
| UI element transforms | |

---

## Workflow 1: Object/Transform Animation

**Use for:** Rigid objects that move, rotate, or scale without mesh deformation.

No armature needed. Keyframe the object's transform properties directly.

### Animatable Properties

| Property | Data Path | Description |
|----------|-----------|-------------|
| Position | `location` | XYZ world position |
| Rotation | `rotation_euler` | XYZ rotation in radians |
| Rotation | `rotation_quaternion` | WXYZ quaternion (no gimbal lock) |
| Scale | `scale` | XYZ scale factors |

### Basic Pattern

```python
import bpy
import math

obj = bpy.context.active_object

# Set timeline
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 60

# Keyframe at frame 1
bpy.context.scene.frame_set(1)
obj.location = (0, 0, 0)
obj.keyframe_insert(data_path="location", frame=1)

# Keyframe at frame 30
bpy.context.scene.frame_set(30)
obj.location = (0, 0, 2)
obj.keyframe_insert(data_path="location", frame=30)

# Keyframe at frame 60 (return to start for loop)
bpy.context.scene.frame_set(60)
obj.location = (0, 0, 0)
obj.keyframe_insert(data_path="location", frame=60)
```

### Common Recipes

**Spinning Pickup (constant rotation):**
```python
obj.rotation_euler = (0, 0, 0)
obj.keyframe_insert(data_path="rotation_euler", frame=1)
obj.rotation_euler = (0, 0, math.radians(360))
obj.keyframe_insert(data_path="rotation_euler", frame=60)

# Make linear (no ease in/out)
for fcurve in obj.animation_data.action.fcurves:
    for kp in fcurve.keyframe_points:
        kp.interpolation = 'LINEAR'
```

**Bobbing Item (sine wave):**
```python
for frame in range(1, 61):
    t = (frame - 1) / 60.0
    obj.location.z = math.sin(t * 2 * math.pi) * 0.3
    obj.keyframe_insert(data_path="location", index=2, frame=frame)
```

**Door Open/Close:**
```python
# Create two Actions: "Open" and "Close"
door_open = bpy.data.actions.new("Door_Open")
door_close = bpy.data.actions.new("Door_Close")

# Animate open
obj.animation_data.action = door_open
obj.rotation_euler = (0, 0, 0)
obj.keyframe_insert(data_path="rotation_euler", frame=1)
obj.rotation_euler = (0, 0, math.radians(90))
obj.keyframe_insert(data_path="rotation_euler", frame=30)

# Animate close
obj.animation_data.action = door_close
obj.rotation_euler = (0, 0, math.radians(90))
obj.keyframe_insert(data_path="rotation_euler", frame=1)
obj.rotation_euler = (0, 0, 0)
obj.keyframe_insert(data_path="rotation_euler", frame=30)
```

### Multiple Actions per Object

Each Action becomes a separate animation clip in the exported glTF:

```python
# Create action
action = bpy.data.actions.new("MyAnimation")

# Assign to object
if not obj.animation_data:
    obj.animation_data_create()
obj.animation_data.action = action

# Keyframe within this action
obj.keyframe_insert(data_path="location", frame=1)
```

See `references/object-animation.md` for complete patterns.
See `examples/spinning-pickup.py`, `examples/bobbing-item.py`, `examples/door-open-close.py` for runnable scripts.

---

## Workflow 2: Skeletal Animation

**Use for:** Characters, creatures, and anything that deforms—mesh vertices move with bones.

### Pipeline Stages

```
1. CREATE ARMATURE    →  Bone hierarchy (skeleton)
2. BIND MESH          →  Skinning (weights)
3. KEYFRAME BONES     →  Animation data
4. EXPORT GLB         →  Game-ready file
```

### Stage 1: Armature Creation

Create bones programmatically:

```python
import bpy
from mathutils import Vector

# Create armature
armature = bpy.data.armatures.new("CharacterRig")
rig_obj = bpy.data.objects.new("CharacterRig", armature)
bpy.context.collection.objects.link(rig_obj)

# Enter edit mode to add bones
bpy.context.view_layer.objects.active = rig_obj
bpy.ops.object.mode_set(mode='EDIT')

# Root bone
root = armature.edit_bones.new("root")
root.head = Vector((0, 0, 0))
root.tail = Vector((0, 0.1, 0))

# Spine
spine = armature.edit_bones.new("spine")
spine.head = Vector((0, 0, 0))
spine.tail = Vector((0, 0, 0.3))
spine.parent = root

# Continue building hierarchy...
bpy.ops.object.mode_set(mode='OBJECT')
```

**Simple Rig Templates:**

| Template | Bones | Use Case |
|----------|-------|----------|
| Humanoid | ~20 | Bipedal characters |
| Quadruped | ~18 | Dogs, cats, horses |
| Simple Prop | ~4 | Hinged objects |
| Serpent/Fish | ~10 | Spine-based creatures |

See `references/armature-creation.md` for complete skeleton presets.

**Rigify (for complex humanoids):**
Blender's Rigify addon generates production-quality rigs. Use "Encode Metarig to Python" operator for reproducible generation:

```python
bpy.ops.object.armature_human_metarig_add()
metarig = bpy.context.active_object
bpy.ops.pose.rigify_generate()
```

### Stage 2: Mesh Binding (Skinning)

**Automatic Weights (usually sufficient):**

```python
# Select mesh, then armature (armature active)
bpy.ops.object.select_all(action='DESELECT')
mesh_obj.select_set(True)
rig_obj.select_set(True)
bpy.context.view_layer.objects.active = rig_obj

# Parent with automatic weights
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
```

**Manual Vertex Groups (when auto fails):**

```python
# Create vertex group matching bone name
vg = mesh_obj.vertex_groups.new(name="spine")

# Assign vertices with weights
vg.add([0, 1, 2, 3], 1.0, 'REPLACE')  # Full weight
vg.add([4, 5, 6], 0.5, 'REPLACE')      # Partial weight
```

**Weight Cleanup (glTF requirement: max 4 influences per vertex):**

```python
bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
bpy.ops.object.vertex_group_normalize_all()
bpy.ops.object.vertex_group_limit_total(limit=4)
bpy.ops.object.mode_set(mode='OBJECT')
```

See `references/skinning-weights.md` for detailed skinning techniques.

### Stage 3: Keyframe Animation

**Basic Bone Animation:**

```python
# Enter pose mode
bpy.context.view_layer.objects.active = rig_obj
bpy.ops.object.mode_set(mode='POSE')

# Get bone
bone = rig_obj.pose.bones["spine"]

# Keyframe rotation
bpy.context.scene.frame_set(1)
bone.rotation_quaternion = (1, 0, 0, 0)
bone.keyframe_insert(data_path="rotation_quaternion", frame=1)

bpy.context.scene.frame_set(15)
bone.rotation_quaternion = (0.966, 0.259, 0, 0)  # ~30 degree X rotation
bone.keyframe_insert(data_path="rotation_quaternion", frame=15)

bpy.ops.object.mode_set(mode='OBJECT')
```

**Animatable Bone Properties:**

| Property | Data Path | Notes |
|----------|-----------|-------|
| Rotation | `rotation_quaternion` | Recommended (no gimbal lock) |
| Rotation | `rotation_euler` | Simpler but can gimbal lock |
| Location | `location` | For root motion |
| Scale | `scale` | Rarely used |

**Creating Multiple Animation Clips:**

```python
# Walk cycle
walk_action = bpy.data.actions.new("Walk")
rig_obj.animation_data.action = walk_action
# ... keyframe walk poses ...

# Run cycle
run_action = bpy.data.actions.new("Run")
rig_obj.animation_data.action = run_action
# ... keyframe run poses ...

# Attack
attack_action = bpy.data.actions.new("Attack")
rig_obj.animation_data.action = attack_action
# ... keyframe attack poses ...
```

Each Action exports as a separate animation clip in glTF.

See `references/keyframe-patterns.md` for common animation recipes.
See `examples/walk-cycle.py` for a complete walk cycle implementation.

### Stage 4: BVH Motion Capture (Optional)

Import motion capture data:

```python
bpy.ops.import_anim.bvh(
    filepath="/path/to/motion.bvh",
    global_scale=0.01,  # Convert cm to meters
    rotate_mode='QUATERNION'
)
```

**Retargeting (when bone names differ):**

```python
# Map source bones to target bones
bone_map = {
    "Hips": "root",
    "Spine": "spine_01",
    "Spine1": "spine_02",
    # ...
}

# Copy keyframes with remapping
for src_name, tgt_name in bone_map.items():
    src_bone = source_rig.pose.bones.get(src_name)
    tgt_bone = target_rig.pose.bones.get(tgt_name)
    if src_bone and tgt_bone:
        # Copy animation data...
```

See `references/bvh-mocap.md` for motion capture workflow.
See `examples/bvh-import-retarget.py` for complete retargeting script.

---

## Export (Both Workflows)

Export to glTF with animations:

```python
bpy.ops.export_scene.gltf(
    filepath="/path/to/output.glb",
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS',  # Each Action = clip
    export_skins=True,                # Include skinning
    export_all_influences=False,      # Limit to 4 per vertex
    export_morph=False,               # No shape keys
)
```

**Key Export Settings:**

| Setting | Value | Purpose |
|---------|-------|---------|
| `export_animations` | `True` | Include animation data |
| `export_animation_mode` | `'ACTIONS'` | Each Action = separate clip |
| `export_skins` | `True` | Include skeletal skinning |
| `export_all_influences` | `False` | Limit bone influences to 4 |

See `references/gltf-export.md` for export validation and troubleshooting.

---

## ZX Console Constraints

Reference these limits when creating animations:

| Constraint | Limit | Notes |
|------------|-------|-------|
| Max bones per skeleton | 256 | Practical: 20-50 |
| Bones per vertex | 4 | glTF/ZX requirement |
| Player character bones | 15-25 | Performance sweet spot |
| NPC/enemy bones | 10-20 | Simpler rigs |
| Prop bones | 1-6 | Minimal rigs |

**Animation Frame Budgets (30 FPS):**

| Animation Type | Frames | Duration |
|----------------|--------|----------|
| Idle loop | 30-60 | 1-2 sec |
| Walk cycle | 20-30 | 0.7-1 sec |
| Run cycle | 15-20 | 0.5-0.7 sec |
| Attack | 15-30 | 0.5-1 sec |
| Jump | 20-40 | 0.7-1.3 sec |
| Death | 30-60 | 1-2 sec |

See `references/zx-constraints.md` for complete budget guidelines.

---

## Complete Example: Character with Walk Cycle

```python
#!/usr/bin/env blender --background --python

import bpy
import math
from mathutils import Vector, Quaternion

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# === 1. CREATE SIMPLE HUMANOID ARMATURE ===
armature = bpy.data.armatures.new("CharacterRig")
rig = bpy.data.objects.new("CharacterRig", armature)
bpy.context.collection.objects.link(rig)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='EDIT')

# Bone definitions: (name, parent, head, tail)
bones_def = [
    ("root", None, (0, 0, 0), (0, 0.1, 0)),
    ("hips", "root", (0, 0, 1.0), (0, 0, 1.15)),
    ("spine", "hips", (0, 0, 1.15), (0, 0, 1.4)),
    ("l_thigh", "hips", (-0.1, 0, 1.0), (-0.1, 0, 0.5)),
    ("l_shin", "l_thigh", (-0.1, 0, 0.5), (-0.1, 0, 0.1)),
    ("r_thigh", "hips", (0.1, 0, 1.0), (0.1, 0, 0.5)),
    ("r_shin", "r_thigh", (0.1, 0, 0.5), (0.1, 0, 0.1)),
]

bone_map = {}
for name, parent, head, tail in bones_def:
    bone = armature.edit_bones.new(name)
    bone.head = Vector(head)
    bone.tail = Vector(tail)
    if parent:
        bone.parent = bone_map[parent]
    bone_map[name] = bone

bpy.ops.object.mode_set(mode='OBJECT')

# === 2. CREATE SIMPLE MESH (placeholder) ===
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 1.2))
body = bpy.context.active_object
body.name = "Body"

# === 3. BIND MESH TO ARMATURE ===
body.select_set(True)
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# === 4. CREATE WALK CYCLE ===
walk = bpy.data.actions.new("Walk")
rig.animation_data_create()
rig.animation_data.action = walk

bpy.ops.object.mode_set(mode='POSE')

# Simple walk: alternate leg rotations
for frame in range(1, 31):
    bpy.context.scene.frame_set(frame)
    phase = (frame - 1) / 30.0 * 2 * math.pi

    # Left leg swings forward/back
    l_thigh = rig.pose.bones["l_thigh"]
    l_thigh.rotation_mode = 'XYZ'
    l_thigh.rotation_euler.x = math.sin(phase) * 0.5
    l_thigh.keyframe_insert(data_path="rotation_euler", frame=frame)

    # Right leg opposite phase
    r_thigh = rig.pose.bones["r_thigh"]
    r_thigh.rotation_mode = 'XYZ'
    r_thigh.rotation_euler.x = math.sin(phase + math.pi) * 0.5
    r_thigh.keyframe_insert(data_path="rotation_euler", frame=frame)

bpy.ops.object.mode_set(mode='OBJECT')

# === 5. EXPORT ===
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 30

bpy.ops.export_scene.gltf(
    filepath="/tmp/character_walk.glb",
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_skins=True,
)

print("Exported: /tmp/character_walk.glb")
```

---

## Additional Resources

### Reference Files

- **`references/object-animation.md`** — Complete object animation patterns
- **`references/skeletal-animation.md`** — Skeletal pipeline overview
- **`references/armature-creation.md`** — Skeleton presets (humanoid, quadruped, etc.)
- **`references/skinning-weights.md`** — Mesh binding techniques
- **`references/keyframe-patterns.md`** — Common animation recipes
- **`references/bvh-mocap.md`** — Motion capture import and retargeting
- **`references/gltf-export.md`** — Export settings and validation
- **`references/zx-constraints.md`** — Console-specific limits

### Example Scripts

All examples are CLI-ready: `blender --background --python script.py`

- **`examples/spinning-pickup.py`** — Constant rotation loop
- **`examples/bobbing-item.py`** — Sine wave location
- **`examples/door-open-close.py`** — Multiple Actions per object
- **`examples/humanoid-rig.py`** — 20-bone skeleton creation
- **`examples/walk-cycle.py`** — Complete character walk
- **`examples/quadruped-rig.py`** — Four-legged skeleton
- **`examples/bvh-import-retarget.py`** — Motion capture workflow
