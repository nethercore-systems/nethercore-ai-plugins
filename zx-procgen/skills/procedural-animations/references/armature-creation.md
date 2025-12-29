# Armature Creation Reference

Complete skeleton presets and programmatic armature construction in Blender.

## Core Concept

An armature is a hierarchy of bones that deform a mesh. Each bone has:
- **Head**: Base/parent end of the bone
- **Tail**: Tip/child end of the bone
- **Parent**: Bone it's connected to (None for root)

## Programmatic Armature Creation

### Basic Pattern

```python
import bpy
from mathutils import Vector

def create_armature(name, bone_definitions):
    """
    Create armature from bone definitions.

    bone_definitions: list of (name, parent_name, head, tail)
    """
    # Create armature data and object
    armature = bpy.data.armatures.new(name)
    rig = bpy.data.objects.new(name, armature)
    bpy.context.collection.objects.link(rig)

    # Enter edit mode
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')

    bone_map = {}

    for bone_name, parent_name, head, tail in bone_definitions:
        bone = armature.edit_bones.new(bone_name)
        bone.head = Vector(head)
        bone.tail = Vector(tail)

        if parent_name and parent_name in bone_map:
            bone.parent = bone_map[parent_name]

        bone_map[bone_name] = bone

    bpy.ops.object.mode_set(mode='OBJECT')
    return rig
```

---

## Skeleton Presets

### Humanoid (20 bones)

Standard bipedal character suitable for most games.

```python
HUMANOID_20 = [
    # name, parent, head, tail
    # Core
    ("root", None, (0, 0, 0), (0, 0, 0.1)),
    ("hips", "root", (0, 0, 1.0), (0, 0, 1.15)),
    ("spine", "hips", (0, 0, 1.15), (0, 0, 1.35)),
    ("chest", "spine", (0, 0, 1.35), (0, 0, 1.55)),
    ("neck", "chest", (0, 0, 1.55), (0, 0, 1.65)),
    ("head", "neck", (0, 0, 1.65), (0, 0, 1.85)),

    # Left arm
    ("l_shoulder", "chest", (-0.15, 0, 1.5), (-0.2, 0, 1.5)),
    ("l_upper_arm", "l_shoulder", (-0.2, 0, 1.5), (-0.45, 0, 1.5)),
    ("l_lower_arm", "l_upper_arm", (-0.45, 0, 1.5), (-0.7, 0, 1.5)),
    ("l_hand", "l_lower_arm", (-0.7, 0, 1.5), (-0.8, 0, 1.5)),

    # Right arm
    ("r_shoulder", "chest", (0.15, 0, 1.5), (0.2, 0, 1.5)),
    ("r_upper_arm", "r_shoulder", (0.2, 0, 1.5), (0.45, 0, 1.5)),
    ("r_lower_arm", "r_upper_arm", (0.45, 0, 1.5), (0.7, 0, 1.5)),
    ("r_hand", "r_lower_arm", (0.7, 0, 1.5), (0.8, 0, 1.5)),

    # Left leg
    ("l_upper_leg", "hips", (-0.1, 0, 1.0), (-0.1, 0, 0.55)),
    ("l_lower_leg", "l_upper_leg", (-0.1, 0, 0.55), (-0.1, 0, 0.1)),
    ("l_foot", "l_lower_leg", (-0.1, 0, 0.1), (-0.1, 0.1, 0)),

    # Right leg
    ("r_upper_leg", "hips", (0.1, 0, 1.0), (0.1, 0, 0.55)),
    ("r_lower_leg", "r_upper_leg", (0.1, 0, 0.55), (0.1, 0, 0.1)),
    ("r_foot", "r_lower_leg", (0.1, 0, 0.1), (0.1, 0.1, 0)),
]

rig = create_armature("HumanoidRig", HUMANOID_20)
```

**Bone Index Reference:**

| Index | Bone | Purpose |
|-------|------|---------|
| 0 | root | World anchor, root motion |
| 1 | hips | Body center, locomotion |
| 2 | spine | Lower torso twist |
| 3 | chest | Upper torso, arm attachment |
| 4 | neck | Head rotation base |
| 5 | head | Look direction |
| 6-9 | l_* arm | Left arm chain |
| 10-13 | r_* arm | Right arm chain |
| 14-16 | l_* leg | Left leg chain |
| 17-19 | r_* leg | Right leg chain |

---

### Quadruped (18 bones)

Four-legged creature (dog, cat, horse, wolf).

```python
QUADRUPED_18 = [
    # Core
    ("root", None, (0, 0, 0), (0, 0.1, 0)),
    ("pelvis", "root", (0, 0, 0.8), (0, 0.15, 0.8)),
    ("spine_01", "pelvis", (0, 0.15, 0.8), (0, 0.3, 0.85)),
    ("spine_02", "spine_01", (0, 0.3, 0.85), (0, 0.45, 0.9)),
    ("chest", "spine_02", (0, 0.45, 0.9), (0, 0.6, 0.95)),
    ("neck", "chest", (0, 0.6, 0.95), (0, 0.75, 1.1)),
    ("head", "neck", (0, 0.75, 1.1), (0, 0.9, 1.15)),

    # Front left leg
    ("fl_upper", "chest", (-0.15, 0.55, 0.7), (-0.15, 0.55, 0.4)),
    ("fl_lower", "fl_upper", (-0.15, 0.55, 0.4), (-0.15, 0.6, 0.1)),
    ("fl_paw", "fl_lower", (-0.15, 0.6, 0.1), (-0.15, 0.65, 0)),

    # Front right leg
    ("fr_upper", "chest", (0.15, 0.55, 0.7), (0.15, 0.55, 0.4)),
    ("fr_lower", "fr_upper", (0.15, 0.55, 0.4), (0.15, 0.6, 0.1)),
    ("fr_paw", "fr_lower", (0.15, 0.6, 0.1), (0.15, 0.65, 0)),

    # Back left leg
    ("bl_upper", "pelvis", (-0.12, 0.05, 0.6), (-0.12, -0.1, 0.35)),
    ("bl_lower", "bl_upper", (-0.12, -0.1, 0.35), (-0.12, 0.05, 0.1)),
    ("bl_paw", "bl_lower", (-0.12, 0.05, 0.1), (-0.12, 0.1, 0)),

    # Back right leg
    ("br_upper", "pelvis", (0.12, 0.05, 0.6), (0.12, -0.1, 0.35)),
    ("br_lower", "br_upper", (0.12, -0.1, 0.35), (0.12, 0.05, 0.1)),
    ("br_paw", "br_lower", (0.12, 0.05, 0.1), (0.12, 0.1, 0)),

    # Tail
    ("tail_01", "pelvis", (0, -0.1, 0.75), (0, -0.25, 0.7)),
    ("tail_02", "tail_01", (0, -0.25, 0.7), (0, -0.4, 0.65)),
]

rig = create_armature("QuadrupedRig", QUADRUPED_18)
```

---

### Simple Prop (4 bones)

Hinged objects like doors, chests, levers.

```python
PROP_HINGE = [
    ("root", None, (0, 0, 0), (0, 0, 0.1)),
    ("pivot", "root", (0, 0, 0), (0, 0, 0.1)),
    ("moving_part", "pivot", (0, 0, 0), (0.5, 0, 0)),
    ("detail", "moving_part", (0.5, 0, 0), (0.6, 0, 0)),
]

# For a door:
DOOR_RIG = [
    ("root", None, (0, 0, 0), (0, 0.05, 0)),
    ("hinge", "root", (-0.5, 0, 0), (-0.5, 0, 1.0)),  # Hinge axis
    ("door", "hinge", (-0.5, 0, 0.5), (0.5, 0, 0.5)),
    ("handle", "door", (0.4, -0.05, 0.5), (0.4, -0.1, 0.5)),
]
```

---

### Serpent/Fish (10 bones)

Spine-based creature for swimming, slithering.

```python
SERPENT_10 = [
    ("root", None, (0, 0, 0), (0, 0.1, 0)),
    ("head", "root", (0, 0.3, 0), (0, 0.4, 0)),
    ("seg_01", "root", (0, -0.1, 0), (0, -0.2, 0)),
    ("seg_02", "seg_01", (0, -0.2, 0), (0, -0.35, 0)),
    ("seg_03", "seg_02", (0, -0.35, 0), (0, -0.5, 0)),
    ("seg_04", "seg_03", (0, -0.5, 0), (0, -0.65, 0)),
    ("seg_05", "seg_04", (0, -0.65, 0), (0, -0.8, 0)),
    ("seg_06", "seg_05", (0, -0.8, 0), (0, -0.95, 0)),
    ("seg_07", "seg_06", (0, -0.95, 0), (0, -1.1, 0)),
    ("tail_tip", "seg_07", (0, -1.1, 0), (0, -1.2, 0)),
]
```

---

### Bird/Flying (14 bones)

Winged creature with simplified legs.

```python
BIRD_14 = [
    # Core
    ("root", None, (0, 0, 0), (0, 0.05, 0)),
    ("body", "root", (0, 0, 0.3), (0, 0.15, 0.3)),
    ("chest", "body", (0, 0.15, 0.35), (0, 0.25, 0.4)),
    ("neck", "chest", (0, 0.25, 0.45), (0, 0.3, 0.55)),
    ("head", "neck", (0, 0.3, 0.55), (0, 0.35, 0.65)),

    # Left wing
    ("l_wing_01", "chest", (-0.1, 0.2, 0.35), (-0.3, 0.2, 0.35)),
    ("l_wing_02", "l_wing_01", (-0.3, 0.2, 0.35), (-0.55, 0.2, 0.3)),
    ("l_wing_03", "l_wing_02", (-0.55, 0.2, 0.3), (-0.75, 0.2, 0.25)),

    # Right wing
    ("r_wing_01", "chest", (0.1, 0.2, 0.35), (0.3, 0.2, 0.35)),
    ("r_wing_02", "r_wing_01", (0.3, 0.2, 0.35), (0.55, 0.2, 0.3)),
    ("r_wing_03", "r_wing_02", (0.55, 0.2, 0.3), (0.75, 0.2, 0.25)),

    # Legs (simplified)
    ("l_leg", "body", (-0.08, 0.05, 0.2), (-0.08, 0.05, 0)),
    ("r_leg", "body", (0.08, 0.05, 0.2), (0.08, 0.05, 0)),

    # Tail
    ("tail", "body", (0, -0.05, 0.25), (0, -0.15, 0.2)),
]
```

---

### Spider/Hexapod (18 bones)

Multi-legged creature (simplified 2-bone legs).

```python
SPIDER_18 = [
    # Core
    ("root", None, (0, 0, 0), (0, 0, 0.05)),
    ("cephalothorax", "root", (0, 0, 0.15), (0, 0, 0.25)),
    ("abdomen", "cephalothorax", (0, -0.15, 0.15), (0, -0.3, 0.12)),

    # Legs (8 legs, 2 bones each = 16 bones)
    # Left side
    ("l1_upper", "cephalothorax", (-0.05, 0.08, 0.2), (-0.2, 0.15, 0.1)),
    ("l1_lower", "l1_upper", (-0.2, 0.15, 0.1), (-0.3, 0.2, 0)),
    ("l2_upper", "cephalothorax", (-0.06, 0.02, 0.2), (-0.22, 0.08, 0.1)),
    ("l2_lower", "l2_upper", (-0.22, 0.08, 0.1), (-0.32, 0.12, 0)),
    ("l3_upper", "cephalothorax", (-0.06, -0.04, 0.2), (-0.22, -0.08, 0.1)),
    ("l3_lower", "l3_upper", (-0.22, -0.08, 0.1), (-0.32, -0.12, 0)),
    ("l4_upper", "cephalothorax", (-0.05, -0.1, 0.2), (-0.2, -0.18, 0.1)),
    ("l4_lower", "l4_upper", (-0.2, -0.18, 0.1), (-0.3, -0.25, 0)),

    # Right side
    ("r1_upper", "cephalothorax", (0.05, 0.08, 0.2), (0.2, 0.15, 0.1)),
    ("r1_lower", "r1_upper", (0.2, 0.15, 0.1), (0.3, 0.2, 0)),
    ("r2_upper", "cephalothorax", (0.06, 0.02, 0.2), (0.22, 0.08, 0.1)),
    ("r2_lower", "r2_upper", (0.22, 0.08, 0.1), (0.32, 0.12, 0)),
    ("r3_upper", "cephalothorax", (0.06, -0.04, 0.2), (0.22, -0.08, 0.1)),
    ("r3_lower", "r3_upper", (0.22, -0.08, 0.1), (0.32, -0.12, 0)),
    ("r4_upper", "cephalothorax", (0.05, -0.1, 0.2), (0.2, -0.18, 0.1)),
    ("r4_lower", "r4_upper", (0.2, -0.18, 0.1), (0.3, -0.25, 0)),
]
```

---

## Rigify Integration

For production-quality humanoid rigs, use Blender's Rigify addon.

### Basic Rigify Workflow

```python
import bpy

# Enable Rigify addon (if not already enabled)
bpy.ops.preferences.addon_enable(module='rigify')

# Add human meta-rig
bpy.ops.object.armature_human_metarig_add()
metarig = bpy.context.active_object

# Scale to match your character
metarig.scale = (1.0, 1.0, 1.0)

# Generate final rig
bpy.ops.pose.rigify_generate()
rig = bpy.context.active_object  # This is now the Rigify rig
```

### Export Rigify Rig

Rigify creates complex control rigs. For game export, use the DEF- (deformation) bones only:

```python
# Select only deformation bones for export
bpy.ops.object.mode_set(mode='POSE')
for bone in rig.pose.bones:
    bone.bone.select = bone.name.startswith("DEF-")
bpy.ops.object.mode_set(mode='OBJECT')
```

### Encode Metarig to Python

For reproducible generation:

1. Create/modify metarig in Blender
2. In Pose Mode, select all bones
3. Run: Armature > Rigify > Encode Metarig to Python

This generates Python code to recreate the metarig.

---

## Scaling Skeletons

Adjust skeleton size for different character scales:

```python
def scale_armature(rig, factor):
    """Scale armature uniformly."""
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')

    for bone in rig.data.edit_bones:
        bone.head *= factor
        bone.tail *= factor

    bpy.ops.object.mode_set(mode='OBJECT')


def scale_armature_to_height(rig, target_height):
    """Scale armature to specific height."""
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')

    # Find current height
    min_z = min(b.head.z for b in rig.data.edit_bones)
    max_z = max(b.tail.z for b in rig.data.edit_bones)
    current_height = max_z - min_z

    if current_height > 0:
        factor = target_height / current_height
        for bone in rig.data.edit_bones:
            bone.head *= factor
            bone.tail *= factor

    bpy.ops.object.mode_set(mode='OBJECT')
```

---

## Bone Properties

### Roll and Orientation

Bone roll affects how rotations work:

```python
bpy.ops.object.mode_set(mode='EDIT')

# Recalculate bone rolls
bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')

bpy.ops.object.mode_set(mode='OBJECT')
```

### Connected vs Non-Connected

```python
# Connected: child head snaps to parent tail
bone.use_connect = True

# Non-connected: child can be positioned anywhere
bone.use_connect = False
```

### Bone Layers

Organize complex rigs:

```python
# In edit mode
bone = armature.edit_bones["spine"]
bone.layers[0] = True   # Main layer
bone.layers[1] = False  # Secondary layer
```
