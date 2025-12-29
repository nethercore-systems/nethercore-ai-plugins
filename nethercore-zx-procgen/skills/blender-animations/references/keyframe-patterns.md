# Keyframe Animation Patterns Reference

Common animation recipes for skeletal and object animation in Blender.

## Keyframing Basics

### Bone Animation Pattern

```python
import bpy
import math

def keyframe_bone_rotation(rig, bone_name, frame, rotation, mode='QUATERNION'):
    """Keyframe bone rotation at specified frame."""
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='POSE')

    bone = rig.pose.bones[bone_name]
    bone.rotation_mode = mode

    bpy.context.scene.frame_set(frame)

    if mode == 'QUATERNION':
        bone.rotation_quaternion = rotation
        bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)
    else:
        bone.rotation_euler = rotation
        bone.keyframe_insert(data_path="rotation_euler", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
```

### Creating Actions

```python
import bpy

def create_action(rig, action_name):
    """Create new action and assign to rig."""
    action = bpy.data.actions.new(action_name)

    if not rig.animation_data:
        rig.animation_data_create()
    rig.animation_data.action = action

    return action
```

---

## Locomotion Patterns

### Walk Cycle (Humanoid)

```python
import bpy
import math

def create_walk_cycle(rig, duration_frames=30):
    """Create basic humanoid walk cycle."""
    action = create_action(rig, "Walk")

    bpy.ops.object.mode_set(mode='POSE')

    # Bone references
    l_thigh = rig.pose.bones["l_upper_leg"]
    r_thigh = rig.pose.bones["r_upper_leg"]
    l_shin = rig.pose.bones["l_lower_leg"]
    r_shin = rig.pose.bones["r_lower_leg"]
    hips = rig.pose.bones["hips"]
    spine = rig.pose.bones["spine"]

    for bone in [l_thigh, r_thigh, l_shin, r_shin, hips, spine]:
        bone.rotation_mode = 'XYZ'

    for frame in range(1, duration_frames + 1):
        bpy.context.scene.frame_set(frame)
        t = (frame - 1) / duration_frames
        phase = t * 2 * math.pi

        # Thigh swing (opposite phases)
        swing_angle = 0.5  # radians
        l_thigh.rotation_euler.x = math.sin(phase) * swing_angle
        r_thigh.rotation_euler.x = math.sin(phase + math.pi) * swing_angle

        # Knee bend (only during swing forward)
        knee_bend = 0.6
        l_shin.rotation_euler.x = max(0, math.sin(phase + math.pi/2)) * knee_bend
        r_shin.rotation_euler.x = max(0, math.sin(phase + math.pi/2 + math.pi)) * knee_bend

        # Vertical bob (two peaks per cycle)
        bob = abs(math.sin(phase * 2)) * 0.02
        hips.location.z = bob

        # Counter-rotation in spine
        spine.rotation_euler.z = math.sin(phase) * 0.05

        # Insert keyframes
        for bone in [l_thigh, r_thigh, l_shin, r_shin, spine]:
            bone.keyframe_insert(data_path="rotation_euler", frame=frame)
        hips.keyframe_insert(data_path="location", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
    return action
```

### Run Cycle

```python
def create_run_cycle(rig, duration_frames=20):
    """Faster, more exaggerated walk cycle."""
    action = create_action(rig, "Run")

    bpy.ops.object.mode_set(mode='POSE')

    l_thigh = rig.pose.bones["l_upper_leg"]
    r_thigh = rig.pose.bones["r_upper_leg"]
    l_shin = rig.pose.bones["l_lower_leg"]
    r_shin = rig.pose.bones["r_lower_leg"]
    hips = rig.pose.bones["hips"]
    chest = rig.pose.bones["chest"]

    for bone in [l_thigh, r_thigh, l_shin, r_shin, hips, chest]:
        bone.rotation_mode = 'XYZ'

    for frame in range(1, duration_frames + 1):
        bpy.context.scene.frame_set(frame)
        t = (frame - 1) / duration_frames
        phase = t * 2 * math.pi

        # Larger thigh swing
        swing = 0.8
        l_thigh.rotation_euler.x = math.sin(phase) * swing
        r_thigh.rotation_euler.x = math.sin(phase + math.pi) * swing

        # More knee bend
        knee = 0.9
        l_shin.rotation_euler.x = max(0, math.sin(phase + math.pi/2)) * knee
        r_shin.rotation_euler.x = max(0, math.sin(phase + math.pi/2 + math.pi)) * knee

        # Higher bob
        bob = abs(math.sin(phase * 2)) * 0.05
        hips.location.z = bob

        # Forward lean
        chest.rotation_euler.x = 0.15

        for bone in [l_thigh, r_thigh, l_shin, r_shin, chest]:
            bone.keyframe_insert(data_path="rotation_euler", frame=frame)
        hips.keyframe_insert(data_path="location", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
    return action
```

### Quadruped Walk

```python
def create_quadruped_walk(rig, duration_frames=30):
    """Four-legged walk with diagonal pairs."""
    action = create_action(rig, "Walk")

    bpy.ops.object.mode_set(mode='POSE')

    # Diagonal pairs: FL+BR and FR+BL
    fl = rig.pose.bones["fl_upper"]
    br = rig.pose.bones["br_upper"]
    fr = rig.pose.bones["fr_upper"]
    bl = rig.pose.bones["bl_upper"]
    spine = rig.pose.bones.get("spine_01")

    for bone in [fl, br, fr, bl]:
        bone.rotation_mode = 'XYZ'
    if spine:
        spine.rotation_mode = 'XYZ'

    for frame in range(1, duration_frames + 1):
        bpy.context.scene.frame_set(frame)
        t = (frame - 1) / duration_frames
        phase = t * 2 * math.pi

        swing = 0.4

        # Diagonal pair 1: FL + BR
        fl.rotation_euler.x = math.sin(phase) * swing
        br.rotation_euler.x = math.sin(phase) * swing

        # Diagonal pair 2: FR + BL (offset by half cycle)
        fr.rotation_euler.x = math.sin(phase + math.pi) * swing
        bl.rotation_euler.x = math.sin(phase + math.pi) * swing

        # Spine flex
        if spine:
            spine.rotation_euler.x = math.sin(phase * 2) * 0.05

        for bone in [fl, br, fr, bl]:
            bone.keyframe_insert(data_path="rotation_euler", frame=frame)
        if spine:
            spine.keyframe_insert(data_path="rotation_euler", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
    return action
```

---

## Idle Animations

### Breathing Idle

```python
def create_breathing_idle(rig, duration_frames=60):
    """Subtle breathing animation."""
    action = create_action(rig, "Idle")

    bpy.ops.object.mode_set(mode='POSE')

    chest = rig.pose.bones["chest"]
    spine = rig.pose.bones["spine"]
    head = rig.pose.bones.get("head")

    for bone in [chest, spine]:
        bone.rotation_mode = 'XYZ'

    for frame in range(1, duration_frames + 1):
        bpy.context.scene.frame_set(frame)
        t = (frame - 1) / duration_frames
        breath = math.sin(t * 2 * math.pi)

        # Chest expands on inhale
        chest.scale.y = 1.0 + breath * 0.02
        chest.scale.x = 1.0 + breath * 0.01

        # Slight spine movement
        spine.rotation_euler.x = breath * 0.02

        # Head micro-movement
        if head:
            head.rotation_euler.z = math.sin(t * 4 * math.pi) * 0.01

        chest.keyframe_insert(data_path="scale", frame=frame)
        spine.keyframe_insert(data_path="rotation_euler", frame=frame)
        if head:
            head.keyframe_insert(data_path="rotation_euler", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
    return action
```

### Weight Shift Idle

```python
def create_weight_shift_idle(rig, duration_frames=90):
    """Shifting weight between feet."""
    action = create_action(rig, "Idle_WeightShift")

    bpy.ops.object.mode_set(mode='POSE')

    hips = rig.pose.bones["hips"]
    l_leg = rig.pose.bones["l_upper_leg"]
    r_leg = rig.pose.bones["r_upper_leg"]

    for bone in [hips, l_leg, r_leg]:
        bone.rotation_mode = 'XYZ'

    for frame in range(1, duration_frames + 1):
        bpy.context.scene.frame_set(frame)
        t = (frame - 1) / duration_frames
        shift = math.sin(t * 2 * math.pi)

        # Hip sway
        hips.location.x = shift * 0.03
        hips.rotation_euler.z = shift * 0.03

        # Leg adjustments
        l_leg.rotation_euler.x = shift * 0.05
        r_leg.rotation_euler.x = -shift * 0.05

        hips.keyframe_insert(data_path="location", frame=frame)
        hips.keyframe_insert(data_path="rotation_euler", frame=frame)
        l_leg.keyframe_insert(data_path="rotation_euler", frame=frame)
        r_leg.keyframe_insert(data_path="rotation_euler", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
    return action
```

---

## Combat Animations

### Attack Swing

```python
def create_attack_swing(rig, duration_frames=20, arm_bone="r_upper_arm"):
    """Simple overhead/side attack swing."""
    action = create_action(rig, "Attack")

    bpy.ops.object.mode_set(mode='POSE')

    arm = rig.pose.bones[arm_bone]
    forearm = rig.pose.bones[arm_bone.replace("upper", "lower")]
    chest = rig.pose.bones["chest"]
    hips = rig.pose.bones["hips"]

    for bone in [arm, forearm, chest, hips]:
        bone.rotation_mode = 'XYZ'

    # Key poses
    poses = {
        1: {"arm_x": -2.0, "forearm_x": 0.5, "chest_z": -0.3, "hips_z": -0.1},  # Wind up
        8: {"arm_x": -2.5, "forearm_x": 0.8, "chest_z": -0.4, "hips_z": -0.15}, # Peak
        12: {"arm_x": 0.5, "forearm_x": 0.2, "chest_z": 0.2, "hips_z": 0.1},    # Swing
        16: {"arm_x": 0.8, "forearm_x": 0.1, "chest_z": 0.3, "hips_z": 0.15},   # Follow through
        20: {"arm_x": 0, "forearm_x": 0, "chest_z": 0, "hips_z": 0},            # Recovery
    }

    for frame, pose in poses.items():
        bpy.context.scene.frame_set(frame)

        arm.rotation_euler.x = pose["arm_x"]
        forearm.rotation_euler.x = pose["forearm_x"]
        chest.rotation_euler.z = pose["chest_z"]
        hips.rotation_euler.z = pose["hips_z"]

        for bone in [arm, forearm, chest, hips]:
            bone.keyframe_insert(data_path="rotation_euler", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
    return action
```

### Hit Reaction

```python
def create_hit_reaction(rig, duration_frames=20, direction='front'):
    """Flinch/stagger from being hit."""
    action = create_action(rig, "HitReact")

    bpy.ops.object.mode_set(mode='POSE')

    hips = rig.pose.bones["hips"]
    spine = rig.pose.bones["spine"]
    head = rig.pose.bones["head"]

    for bone in [hips, spine, head]:
        bone.rotation_mode = 'XYZ'

    # Impact at frame 1, recovery over remaining frames
    impact_dir = -1 if direction == 'front' else 1

    poses = {
        1: {"spine_x": 0, "head_x": 0, "hips_y": 0},
        4: {"spine_x": impact_dir * 0.4, "head_x": impact_dir * 0.3, "hips_y": impact_dir * 0.1},
        8: {"spine_x": impact_dir * 0.3, "head_x": impact_dir * 0.2, "hips_y": impact_dir * 0.05},
        14: {"spine_x": impact_dir * 0.1, "head_x": impact_dir * 0.05, "hips_y": 0},
        20: {"spine_x": 0, "head_x": 0, "hips_y": 0},
    }

    for frame, pose in poses.items():
        bpy.context.scene.frame_set(frame)

        spine.rotation_euler.x = pose["spine_x"]
        head.rotation_euler.x = pose["head_x"]
        hips.location.y = pose["hips_y"]

        spine.keyframe_insert(data_path="rotation_euler", frame=frame)
        head.keyframe_insert(data_path="rotation_euler", frame=frame)
        hips.keyframe_insert(data_path="location", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
    return action
```

---

## Mechanical Animations

### Door Open

```python
def create_door_open(rig, duration_frames=30, open_angle=90):
    """Door swing on hinge."""
    action = create_action(rig, "Open")

    bpy.ops.object.mode_set(mode='POSE')

    door = rig.pose.bones["door"]
    door.rotation_mode = 'XYZ'

    # Start closed
    bpy.context.scene.frame_set(1)
    door.rotation_euler.z = 0
    door.keyframe_insert(data_path="rotation_euler", frame=1)

    # End open
    bpy.context.scene.frame_set(duration_frames)
    door.rotation_euler.z = math.radians(open_angle)
    door.keyframe_insert(data_path="rotation_euler", frame=duration_frames)

    # Add ease in/out
    for fcurve in rig.animation_data.action.fcurves:
        for kp in fcurve.keyframe_points:
            kp.interpolation = 'BEZIER'
            kp.easing = 'AUTO'

    bpy.ops.object.mode_set(mode='OBJECT')
    return action
```

### Lever Pull

```python
def create_lever_pull(rig, duration_frames=20):
    """Lever rotation from off to on."""
    action = create_action(rig, "Pull")

    bpy.ops.object.mode_set(mode='POSE')

    lever = rig.pose.bones["lever"]
    lever.rotation_mode = 'XYZ'

    # Start position
    bpy.context.scene.frame_set(1)
    lever.rotation_euler.x = math.radians(-30)
    lever.keyframe_insert(data_path="rotation_euler", frame=1)

    # Quick pull
    bpy.context.scene.frame_set(10)
    lever.rotation_euler.x = math.radians(30)
    lever.keyframe_insert(data_path="rotation_euler", frame=10)

    # Slight bounce back
    bpy.context.scene.frame_set(14)
    lever.rotation_euler.x = math.radians(25)
    lever.keyframe_insert(data_path="rotation_euler", frame=14)

    # Settle
    bpy.context.scene.frame_set(20)
    lever.rotation_euler.x = math.radians(30)
    lever.keyframe_insert(data_path="rotation_euler", frame=20)

    bpy.ops.object.mode_set(mode='OBJECT')
    return action
```

---

## Organic Motion

### Tail Wag

```python
def create_tail_wag(rig, duration_frames=30, tail_bones=None):
    """Wagging motion propagating down tail."""
    if tail_bones is None:
        tail_bones = ["tail_01", "tail_02"]

    action = create_action(rig, "TailWag")

    bpy.ops.object.mode_set(mode='POSE')

    bones = [rig.pose.bones[name] for name in tail_bones]
    for bone in bones:
        bone.rotation_mode = 'XYZ'

    for frame in range(1, duration_frames + 1):
        bpy.context.scene.frame_set(frame)
        t = (frame - 1) / duration_frames
        base_phase = t * 4 * math.pi  # Two full wags per cycle

        for i, bone in enumerate(bones):
            # Delay and amplify toward tip
            delay = i * 0.3
            amplitude = 0.3 + i * 0.2
            bone.rotation_euler.z = math.sin(base_phase - delay) * amplitude
            bone.keyframe_insert(data_path="rotation_euler", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
    return action
```

### Wing Flap

```python
def create_wing_flap(rig, duration_frames=20):
    """Simple up-down wing flap."""
    action = create_action(rig, "Fly")

    bpy.ops.object.mode_set(mode='POSE')

    l_wing = rig.pose.bones["l_wing_01"]
    r_wing = rig.pose.bones["r_wing_01"]

    for bone in [l_wing, r_wing]:
        bone.rotation_mode = 'XYZ'

    for frame in range(1, duration_frames + 1):
        bpy.context.scene.frame_set(frame)
        t = (frame - 1) / duration_frames
        flap = math.sin(t * 2 * math.pi)

        # Wings mirror
        l_wing.rotation_euler.y = flap * 0.8
        r_wing.rotation_euler.y = -flap * 0.8

        l_wing.keyframe_insert(data_path="rotation_euler", frame=frame)
        r_wing.keyframe_insert(data_path="rotation_euler", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
    return action
```

---

## Interpolation Control

### Setting Interpolation Mode

```python
def set_interpolation(action, mode='BEZIER'):
    """Set interpolation mode for all keyframes."""
    for fcurve in action.fcurves:
        for kp in fcurve.keyframe_points:
            kp.interpolation = mode  # 'BEZIER', 'LINEAR', 'CONSTANT'


def set_easing(action, easing='EASE_IN_OUT'):
    """Set easing for all keyframes."""
    for fcurve in action.fcurves:
        for kp in fcurve.keyframe_points:
            kp.easing = easing  # 'AUTO', 'EASE_IN', 'EASE_OUT', 'EASE_IN_OUT'
```

### Custom Easing

```python
def ease_out_elastic(t):
    """Elastic ease out for bouncy motion."""
    if t == 0 or t == 1:
        return t
    return math.pow(2, -10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi) / 3) + 1


def apply_custom_easing(values, ease_func):
    """Apply custom easing to keyframe values."""
    result = []
    for i, t in enumerate(values):
        normalized_t = i / (len(values) - 1)
        result.append(ease_func(normalized_t))
    return result
```

---

## Looping Animations

```python
def ensure_loop(action, frame_end):
    """Ensure animation loops seamlessly."""
    for fcurve in action.fcurves:
        if len(fcurve.keyframe_points) > 0:
            # Copy first keyframe value to last frame
            first_value = fcurve.keyframe_points[0].co[1]
            fcurve.keyframe_points.insert(frame_end, first_value)

            # Make linear at loop point
            fcurve.keyframe_points[-1].interpolation = 'LINEAR'


def add_cycle_modifier(action):
    """Add cycle modifier for infinite looping."""
    for fcurve in action.fcurves:
        cycle = fcurve.modifiers.new('CYCLES')
        cycle.mode_before = 'REPEAT'
        cycle.mode_after = 'REPEAT'
```
