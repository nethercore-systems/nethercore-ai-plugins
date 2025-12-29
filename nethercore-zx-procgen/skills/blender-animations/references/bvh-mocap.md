# BVH Motion Capture Reference

Import, process, and retarget BVH motion capture data in Blender.

## BVH Format Overview

BVH (Biovision Hierarchy) is the standard motion capture format:

```
HIERARCHY
ROOT Hips
{
    OFFSET 0.00 0.00 0.00
    CHANNELS 6 Xposition Yposition Zposition Xrotation Yrotation Zrotation
    JOINT Spine
    {
        OFFSET 0.00 10.00 0.00
        CHANNELS 3 Xrotation Yrotation Zrotation
        ...
    }
}
MOTION
Frames: 120
Frame Time: 0.033333
0.00 90.00 0.00 0.00 0.00 0.00 ...
```

**Key Points:**
- HIERARCHY defines skeleton structure
- MOTION contains per-frame channel data
- Rotations typically in ZXY Euler order
- Positions often in centimeters (divide by 100 for meters)

---

## Basic BVH Import

```python
import bpy

def import_bvh(filepath, scale=0.01, rotation_mode='QUATERNION'):
    """Import BVH file with common settings."""
    bpy.ops.import_anim.bvh(
        filepath=filepath,
        global_scale=scale,           # Convert cm to m
        rotate_mode=rotation_mode,    # 'QUATERNION' or 'NATIVE'
        use_fps_scale=True,           # Adjust to scene FPS
        update_scene_fps=False,       # Keep current scene FPS
        update_scene_duration=True,   # Set timeline to match
    )
    return bpy.context.active_object
```

### Import Settings

| Setting | Value | Purpose |
|---------|-------|---------|
| `global_scale` | 0.01 | Convert cm to meters (CMU data) |
| `rotate_mode` | 'QUATERNION' | Avoids gimbal lock |
| `use_fps_scale` | True | Matches animation to scene FPS |
| `use_cyclic` | False | Don't auto-loop |

---

## Open-Source Motion Capture Databases

### CMU Motion Capture Database

**URL:** https://mocap.cs.cmu.edu/

- 2,605 clips from 144 subjects
- BVH files available
- Free for research, commercial requires attribution

**Recommended Clips:**

| Subject | Description | Game Use |
|---------|-------------|----------|
| 01-05 | Basic locomotion | Walk, run, jump |
| 13-14 | Martial arts/boxing | Combat |
| 35 | Various actions | General animation |
| 49 | Sports | Athletic games |
| 85-86 | Dancing | Rhythm games |
| 91 | Sitting, standing | Idle, transitions |

### Mixamo

**URL:** https://www.mixamo.com/

- Game-ready animations
- Requires Adobe account (free)
- Export FBX, convert to BVH via Blender

**FBX to BVH Conversion:**
```python
# Import FBX
bpy.ops.import_scene.fbx(filepath="animation.fbx")
armature = bpy.context.active_object

# Export as BVH
bpy.ops.export_anim.bvh(
    filepath="animation.bvh",
    global_scale=1.0,
    rotate_mode='NATIVE'
)
```

### Other Sources

- **Truebones:** https://truebones.gumroad.com/ (free packs)
- **Bandai Namco Research:** Various academic datasets
- **LAFAN1:** High-quality locomotion data

---

## Coordinate System Conversion

Different sources use different conventions:

| Source | Up | Forward | Scale |
|--------|-----|---------|-------|
| CMU | Y | -Z | cm |
| Mixamo | Y | Z | cm |
| Blender | Z | -Y | m |

```python
def convert_coordinate_system(armature, source='cmu'):
    """Apply coordinate conversion after import."""
    if source == 'cmu':
        # CMU uses Y-up, -Z forward (matches Blender well)
        pass
    elif source == 'mixamo':
        # Mixamo uses Y-up, Z forward
        armature.rotation_euler.x = 0  # May need adjustment
```

---

## Retargeting

Map motion capture skeleton to your game skeleton.

### Basic Bone Mapping

```python
# CMU skeleton to game skeleton mapping
BONE_MAP = {
    # CMU name : Game name
    "Hips": "root",
    "Spine": "spine",
    "Spine1": "chest",
    "Neck": "neck",
    "Head": "head",
    "LeftShoulder": "l_shoulder",
    "LeftArm": "l_upper_arm",
    "LeftForeArm": "l_lower_arm",
    "LeftHand": "l_hand",
    "RightShoulder": "r_shoulder",
    "RightArm": "r_upper_arm",
    "RightForeArm": "r_lower_arm",
    "RightHand": "r_hand",
    "LeftUpLeg": "l_upper_leg",
    "LeftLeg": "l_lower_leg",
    "LeftFoot": "l_foot",
    "RightUpLeg": "r_upper_leg",
    "RightLeg": "r_lower_leg",
    "RightFoot": "r_foot",
}
```

### Constraint-Based Retargeting

```python
import bpy

def setup_retarget_constraints(source_rig, target_rig, bone_map):
    """Add copy rotation constraints for retargeting."""
    bpy.context.view_layer.objects.active = target_rig
    bpy.ops.object.mode_set(mode='POSE')

    for src_name, tgt_name in bone_map.items():
        src_bone = source_rig.pose.bones.get(src_name)
        tgt_bone = target_rig.pose.bones.get(tgt_name)

        if src_bone and tgt_bone:
            # Add copy rotation constraint
            constraint = tgt_bone.constraints.new('COPY_ROTATION')
            constraint.target = source_rig
            constraint.subtarget = src_name
            constraint.target_space = 'LOCAL'
            constraint.owner_space = 'LOCAL'

    bpy.ops.object.mode_set(mode='OBJECT')


def bake_retargeted_animation(target_rig, frame_start, frame_end):
    """Bake constraints to keyframes."""
    bpy.context.view_layer.objects.active = target_rig
    bpy.ops.object.mode_set(mode='POSE')

    bpy.ops.nla.bake(
        frame_start=frame_start,
        frame_end=frame_end,
        only_selected=False,
        visual_keying=True,
        clear_constraints=True,
        bake_types={'POSE'}
    )

    bpy.ops.object.mode_set(mode='OBJECT')
```

### Manual Keyframe Copy

```python
def copy_animation_data(source_rig, target_rig, bone_map, frame_start, frame_end):
    """Manually copy animation from source to target."""
    bpy.context.view_layer.objects.active = target_rig
    bpy.ops.object.mode_set(mode='POSE')

    # Create new action for target
    action = bpy.data.actions.new(f"{source_rig.name}_retarget")
    if not target_rig.animation_data:
        target_rig.animation_data_create()
    target_rig.animation_data.action = action

    for frame in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(frame)

        for src_name, tgt_name in bone_map.items():
            src_bone = source_rig.pose.bones.get(src_name)
            tgt_bone = target_rig.pose.bones.get(tgt_name)

            if src_bone and tgt_bone:
                # Copy rotation
                tgt_bone.rotation_quaternion = src_bone.rotation_quaternion.copy()
                tgt_bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)

                # Copy location only for root
                if tgt_name == "root":
                    tgt_bone.location = src_bone.location.copy()
                    tgt_bone.keyframe_insert(data_path="location", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
    return action
```

---

## Proportional Retargeting

Adjust for different body proportions:

```python
def calculate_limb_ratio(source_rig, target_rig, limb_bones):
    """Calculate length ratio between source and target limb."""
    def get_chain_length(rig, bones):
        total = 0
        for bone_name in bones:
            bone = rig.data.bones.get(bone_name)
            if bone:
                total += bone.length
        return total

    source_len = get_chain_length(source_rig, limb_bones)
    target_len = get_chain_length(target_rig, limb_bones)

    if source_len > 0:
        return target_len / source_len
    return 1.0


def apply_proportional_retarget(target_rig, source_rig, frame_start, frame_end):
    """Retarget with proportional scaling for different body types."""
    # Calculate ratios for each limb
    arm_bones = ["l_upper_arm", "l_lower_arm"]
    leg_bones = ["l_upper_leg", "l_lower_leg"]

    arm_ratio = calculate_limb_ratio(source_rig, target_rig, arm_bones)
    leg_ratio = calculate_limb_ratio(source_rig, target_rig, leg_bones)

    # Apply scaled locations to root/hip motion
    root = target_rig.pose.bones.get("root")
    source_root = source_rig.pose.bones.get("Hips")

    if root and source_root:
        for frame in range(frame_start, frame_end + 1):
            bpy.context.scene.frame_set(frame)

            # Scale root motion
            root.location = source_root.location * ((arm_ratio + leg_ratio) / 2)
            root.keyframe_insert(data_path="location", frame=frame)
```

---

## Root Motion Extraction

Extract character movement from animation for game controller:

```python
def extract_root_motion(rig, frame_start, frame_end):
    """Extract root bone motion as world-space deltas."""
    root = rig.pose.bones.get("root") or rig.pose.bones.get("Hips")
    if not root:
        return None

    motion_data = []

    prev_pos = None
    prev_rot = None

    for frame in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(frame)

        # Get world position
        world_pos = rig.matrix_world @ root.matrix @ root.location

        if prev_pos:
            delta_pos = world_pos - prev_pos
            motion_data.append({
                "frame": frame,
                "position_delta": list(delta_pos),
            })

        prev_pos = world_pos.copy()

    return motion_data


def remove_root_motion(rig, frame_start, frame_end):
    """Zero out root XZ position to keep character in place."""
    root = rig.pose.bones.get("root") or rig.pose.bones.get("Hips")
    if not root:
        return

    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='POSE')

    for frame in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(frame)

        # Zero X and Z, keep Y (vertical)
        root.location.x = 0
        root.location.z = 0
        root.keyframe_insert(data_path="location", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
```

---

## Animation Cleanup

### Smoothing Jittery Motion

```python
def smooth_animation(action, factor=0.5):
    """Apply simple smoothing to reduce mocap jitter."""
    for fcurve in action.fcurves:
        points = fcurve.keyframe_points

        if len(points) < 3:
            continue

        # Store smoothed values
        smoothed = []
        for i in range(len(points)):
            if i == 0 or i == len(points) - 1:
                smoothed.append(points[i].co[1])
            else:
                # Average with neighbors
                avg = (points[i-1].co[1] + points[i].co[1] + points[i+1].co[1]) / 3
                smoothed.append(points[i].co[1] * (1 - factor) + avg * factor)

        # Apply smoothed values
        for i, value in enumerate(smoothed):
            points[i].co[1] = value
```

### Reducing Keyframes

```python
def reduce_keyframes(action, threshold=0.01):
    """Remove redundant keyframes within threshold."""
    for fcurve in action.fcurves:
        # Use Blender's built-in decimation
        fcurve.convert_to_samples(start=fcurve.range()[0], end=fcurve.range()[1])
        fcurve.convert_to_keyframes(start=fcurve.range()[0], end=fcurve.range()[1])

        # Or manual threshold-based removal
        points_to_remove = []
        for i in range(1, len(fcurve.keyframe_points) - 1):
            prev_val = fcurve.keyframe_points[i-1].co[1]
            curr_val = fcurve.keyframe_points[i].co[1]
            next_val = fcurve.keyframe_points[i+1].co[1]

            # If middle point is redundant
            if abs(curr_val - (prev_val + next_val) / 2) < threshold:
                points_to_remove.append(i)

        for i in reversed(points_to_remove):
            fcurve.keyframe_points.remove(fcurve.keyframe_points[i])
```

---

## Complete Workflow Example

```python
import bpy

def mocap_to_game_animation(bvh_path, target_rig, output_name):
    """Complete mocap import and retarget workflow."""
    # 1. Import BVH
    bpy.ops.import_anim.bvh(
        filepath=bvh_path,
        global_scale=0.01,
        rotate_mode='QUATERNION'
    )
    source_rig = bpy.context.active_object

    # 2. Set up bone mapping
    bone_map = {
        "Hips": "root",
        "Spine": "spine",
        # ... complete mapping
    }

    # 3. Retarget
    setup_retarget_constraints(source_rig, target_rig, bone_map)

    # 4. Determine frame range
    frame_start = int(source_rig.animation_data.action.frame_range[0])
    frame_end = int(source_rig.animation_data.action.frame_range[1])

    # 5. Bake to keyframes
    bake_retargeted_animation(target_rig, frame_start, frame_end)

    # 6. Rename action
    target_rig.animation_data.action.name = output_name

    # 7. Optional: Remove root motion for in-place animation
    remove_root_motion(target_rig, frame_start, frame_end)

    # 8. Cleanup: Delete source rig
    bpy.data.objects.remove(source_rig, do_unlink=True)

    return target_rig.animation_data.action
```
