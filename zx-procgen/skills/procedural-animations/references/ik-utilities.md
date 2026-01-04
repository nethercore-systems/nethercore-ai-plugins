# IK Utilities for Procedural Animation

Reusable IK setup functions for locomotion and contact-based animations. IK simplifies foot placement and hand targeting, then gets baked to FK for export.

## When to Use IK

| Animation Type | Feet | Hands | Reason |
|---------------|------|-------|--------|
| Walk/run cycles | IK | FK | Precise ground contact |
| Idle/breathing | FK | FK | No contact points |
| Sword swings | FK or IK | FK | Feet may need planting |
| Climbing | IK | IK | Both need targets |
| Grabbing/reaching | FK | IK | Hand target position |

## Core Utilities

Add these to `lib/animation_utils.py`:

### setup_leg_ik

```python
def setup_leg_ik(armature, side='L'):
    """
    Sets up IK for a humanoid leg.

    Creates:
    - IK target bone at foot position
    - Pole target bone in front of knee
    - IK constraint on shin with chain_length=2

    Args:
        armature: Blender armature object
        side: 'L' or 'R'

    Returns:
        tuple: (ik_target_bone, pole_target_bone)

    Bone naming convention: thigh.{side}, shin.{side}, foot.{side}
    """
    import bpy

    # Enter edit mode to create control bones
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    # Get leg bones
    thigh = edit_bones.get(f"thigh.{side}")
    shin = edit_bones.get(f"shin.{side}")
    foot = edit_bones.get(f"foot.{side}")

    if not all([thigh, shin, foot]):
        raise ValueError(f"Missing leg bones for side {side}")

    # Create IK target at foot position
    ik_target = edit_bones.new(f"ik_foot.{side}")
    ik_target.head = foot.head.copy()
    ik_target.tail = foot.head.copy()
    ik_target.tail.y += 0.1  # Small bone pointing forward
    ik_target.parent = None  # Root level, not parented

    # Create pole target in front of knee
    pole = edit_bones.new(f"pole_knee.{side}")
    knee_pos = shin.head.copy()
    pole.head = knee_pos
    pole.head.y += 0.5  # In front of knee
    pole.tail = pole.head.copy()
    pole.tail.y += 0.1
    pole.parent = None

    # Exit edit mode
    bpy.ops.object.mode_set(mode='POSE')

    # Add IK constraint to shin
    pose_shin = armature.pose.bones[f"shin.{side}"]
    ik_constraint = pose_shin.constraints.new('IK')
    ik_constraint.target = armature
    ik_constraint.subtarget = f"ik_foot.{side}"
    ik_constraint.pole_target = armature
    ik_constraint.pole_subtarget = f"pole_knee.{side}"
    ik_constraint.pole_angle = 0  # May need adjustment: try math.radians(90) if knee bends wrong
    ik_constraint.chain_count = 2  # thigh + shin

    return (f"ik_foot.{side}", f"pole_knee.{side}")
```

### setup_arm_ik

```python
def setup_arm_ik(armature, side='L'):
    """
    Sets up IK for a humanoid arm.

    Creates:
    - IK target bone at hand position
    - Pole target bone behind elbow
    - IK constraint on forearm with chain_length=2

    Args:
        armature: Blender armature object
        side: 'L' or 'R'

    Returns:
        tuple: (ik_target_bone, pole_target_bone)

    Bone naming convention: upper_arm.{side}, forearm.{side}, hand.{side}
    """
    import bpy

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    upper_arm = edit_bones.get(f"upper_arm.{side}")
    forearm = edit_bones.get(f"forearm.{side}")
    hand = edit_bones.get(f"hand.{side}")

    if not all([upper_arm, forearm, hand]):
        raise ValueError(f"Missing arm bones for side {side}")

    # IK target at hand
    ik_target = edit_bones.new(f"ik_hand.{side}")
    ik_target.head = hand.head.copy()
    ik_target.tail = hand.head.copy()
    ik_target.tail.z += 0.1
    ik_target.parent = None

    # Pole behind elbow
    pole = edit_bones.new(f"pole_elbow.{side}")
    elbow_pos = forearm.head.copy()
    pole.head = elbow_pos
    pole.head.y -= 0.4  # Behind elbow
    pole.tail = pole.head.copy()
    pole.tail.y -= 0.1
    pole.parent = None

    bpy.ops.object.mode_set(mode='POSE')

    pose_forearm = armature.pose.bones[f"forearm.{side}"]
    ik_constraint = pose_forearm.constraints.new('IK')
    ik_constraint.target = armature
    ik_constraint.subtarget = f"ik_hand.{side}"
    ik_constraint.pole_target = armature
    ik_constraint.pole_subtarget = f"pole_elbow.{side}"
    ik_constraint.pole_angle = math.radians(180)  # Elbow bends back
    ik_constraint.chain_count = 2

    return (f"ik_hand.{side}", f"pole_elbow.{side}")
```

### setup_humanoid_ik

```python
def setup_humanoid_ik(armature, include_arms=False):
    """
    Sets up IK for a complete humanoid rig.

    Args:
        armature: Blender armature object
        include_arms: If True, also set up arm IK

    Returns:
        dict: Bone names for all IK controls
    """
    controls = {}

    # Always set up legs for locomotion
    controls['foot_l'], controls['pole_knee_l'] = setup_leg_ik(armature, 'L')
    controls['foot_r'], controls['pole_knee_r'] = setup_leg_ik(armature, 'R')

    if include_arms:
        controls['hand_l'], controls['pole_elbow_l'] = setup_arm_ik(armature, 'L')
        controls['hand_r'], controls['pole_elbow_r'] = setup_arm_ik(armature, 'R')

    return controls
```

### keyframe_ik_target

```python
def keyframe_ik_target(armature, target_name, frame, location):
    """
    Keyframes an IK target's location.

    Args:
        armature: Blender armature object
        target_name: Name of IK target bone (e.g., "ik_foot.L")
        frame: Frame number
        location: (x, y, z) tuple in world space
    """
    import bpy

    bpy.ops.object.mode_set(mode='POSE')
    target = armature.pose.bones[target_name]
    target.location = location
    target.keyframe_insert('location', frame=frame)
```

### bake_ik_to_fk

```python
def bake_ik_to_fk(armature, frame_start, frame_end, remove_ik=True):
    """
    Bakes IK-driven animation to FK keyframes.

    After baking, the animation is pure FK rotations,
    compatible with ZX runtime (which doesn't support IK).

    Args:
        armature: Blender armature object
        frame_start: First frame to bake
        frame_end: Last frame to bake
        remove_ik: If True, removes IK constraints after baking
    """
    import bpy

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    # Select all pose bones
    bpy.ops.pose.select_all(action='SELECT')

    # Bake action
    bpy.ops.nla.bake(
        frame_start=frame_start,
        frame_end=frame_end,
        only_selected=True,
        visual_keying=True,  # Captures IK result
        clear_constraints=remove_ik,
        bake_types={'POSE'}
    )

    # Optionally remove IK control bones
    if remove_ik:
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones

        # Remove IK bones (they're not needed after baking)
        for bone_name in list(edit_bones.keys()):
            if bone_name.startswith('ik_') or bone_name.startswith('pole_'):
                edit_bones.remove(edit_bones[bone_name])

        bpy.ops.object.mode_set(mode='OBJECT')
```

## Preset-Specific Setup

### Quadruped IK

```python
def setup_quadruped_ik(armature):
    """
    Sets up IK for a quadruped rig (4 legs).

    Bone naming: front_thigh.{side}, front_shin.{side}, front_foot.{side}
                 back_thigh.{side}, back_shin.{side}, back_foot.{side}
    """
    controls = {}

    for side in ['L', 'R']:
        # Front legs
        controls[f'front_foot_{side.lower()}'] = setup_leg_ik_generic(
            armature,
            thigh=f"front_thigh.{side}",
            shin=f"front_shin.{side}",
            foot=f"front_foot.{side}",
            ik_name=f"ik_front_foot.{side}",
            pole_name=f"pole_front_knee.{side}"
        )

        # Back legs
        controls[f'back_foot_{side.lower()}'] = setup_leg_ik_generic(
            armature,
            thigh=f"back_thigh.{side}",
            shin=f"back_shin.{side}",
            foot=f"back_foot.{side}",
            ik_name=f"ik_back_foot.{side}",
            pole_name=f"pole_back_knee.{side}"
        )

    return controls
```

## Complete Locomotion Example

```python
"""Walk cycle with IK feet"""

import bpy
import math

# Import utilities
from lib.animation_utils import (
    setup_humanoid_ik,
    keyframe_ik_target,
    bake_ik_to_fk
)

# Setup
armature = bpy.data.objects["Armature"]
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = 24

# Set up leg IK
controls = setup_humanoid_ik(armature, include_arms=False)

# Walk cycle foot positions (simplified)
# Frame 0: Right foot forward, left foot back
keyframe_ik_target(armature, "ik_foot.R", 0, (0.1, 0.4, 0))
keyframe_ik_target(armature, "ik_foot.L", 0, (-0.1, -0.3, 0))

# Frame 6: Right foot passing
keyframe_ik_target(armature, "ik_foot.R", 6, (0.1, 0.1, 0.1))  # Lift
keyframe_ik_target(armature, "ik_foot.L", 6, (-0.1, 0, 0))

# Frame 12: Left foot forward, right foot back
keyframe_ik_target(armature, "ik_foot.R", 12, (0.1, -0.3, 0))
keyframe_ik_target(armature, "ik_foot.L", 12, (-0.1, 0.4, 0))

# Frame 18: Left foot passing
keyframe_ik_target(armature, "ik_foot.R", 18, (0.1, 0, 0))
keyframe_ik_target(armature, "ik_foot.L", 18, (-0.1, 0.1, 0.1))

# Frame 24: Back to start
keyframe_ik_target(armature, "ik_foot.R", 24, (0.1, 0.4, 0))
keyframe_ik_target(armature, "ik_foot.L", 24, (-0.1, -0.3, 0))

# Bake to FK and remove IK
bake_ik_to_fk(armature, 0, 24, remove_ik=True)

# Export
bpy.ops.export_scene.gltf(
    filepath="walk_cycle.glb",
    export_format='GLB',
    export_animations=True,
)
```

## Troubleshooting

### Knee/Elbow Bends Wrong Direction

Adjust `pole_angle` on the IK constraint:

```python
ik_constraint.pole_angle = math.radians(90)  # Try 0, 90, 180, -90
```

### Foot Slides During Walk

Ensure IK targets are keyframed at ground level (Z=0) during contact phases.

### Weird Poses After Baking

Check that `visual_keying=True` in the bake operation — this captures the actual posed result, not just constraint values.

### IK Bones Still in Export

Make sure `remove_ik=True` when calling `bake_ik_to_fk`, or manually delete IK/pole bones before export.
