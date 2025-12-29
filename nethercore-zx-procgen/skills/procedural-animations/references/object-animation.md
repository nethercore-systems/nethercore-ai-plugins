# Object/Transform Animation Reference

Complete patterns for animating rigid objects in Blender without armatures.

## Core Concept

Object animation keyframes the object's transform properties directly. No armature needed—the mesh moves/rotates/scales as a whole unit.

## Animatable Properties

### Location

```python
obj.location = (x, y, z)
obj.keyframe_insert(data_path="location", frame=frame)

# Single axis only
obj.location.z = value
obj.keyframe_insert(data_path="location", index=2, frame=frame)
```

### Rotation (Euler)

```python
import math

obj.rotation_mode = 'XYZ'  # or 'ZXY', 'YXZ', etc.
obj.rotation_euler = (rx, ry, rz)  # radians
obj.keyframe_insert(data_path="rotation_euler", frame=frame)

# Example: 45 degree Z rotation
obj.rotation_euler.z = math.radians(45)
obj.keyframe_insert(data_path="rotation_euler", index=2, frame=frame)
```

### Rotation (Quaternion)

```python
from mathutils import Quaternion
import math

obj.rotation_mode = 'QUATERNION'
obj.rotation_quaternion = Quaternion((1, 0, 0, 0))  # identity
obj.keyframe_insert(data_path="rotation_quaternion", frame=frame)

# Rotate around axis
axis = (0, 0, 1)  # Z axis
angle = math.radians(90)
obj.rotation_quaternion = Quaternion(axis, angle)
```

### Scale

```python
obj.scale = (sx, sy, sz)
obj.keyframe_insert(data_path="scale", frame=frame)

# Uniform scale
obj.scale = (1.5, 1.5, 1.5)
```

## Interpolation Modes

Control how Blender interpolates between keyframes:

```python
# After inserting keyframes
for fcurve in obj.animation_data.action.fcurves:
    for kp in fcurve.keyframe_points:
        kp.interpolation = 'BEZIER'  # Smooth (default)
        # kp.interpolation = 'LINEAR'  # Constant speed
        # kp.interpolation = 'CONSTANT'  # Snap between values
```

### Common Interpolation Settings

| Mode | Use Case |
|------|----------|
| `BEZIER` | Organic motion, ease in/out |
| `LINEAR` | Mechanical rotation, constant speed |
| `CONSTANT` | Abrupt changes, sprite-like |

## Complete Animation Patterns

### Spinning Object (Continuous Loop)

```python
import bpy
import math

def animate_spin(obj, duration_frames=60, axis='Z', direction=1):
    """Continuous rotation around axis."""
    if not obj.animation_data:
        obj.animation_data_create()

    action = bpy.data.actions.new(f"{obj.name}_Spin")
    obj.animation_data.action = action

    # Start
    obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert(data_path="rotation_euler", frame=1)

    # End (360 degrees)
    angle = math.radians(360 * direction)
    if axis == 'X':
        obj.rotation_euler = (angle, 0, 0)
    elif axis == 'Y':
        obj.rotation_euler = (0, angle, 0)
    else:  # Z
        obj.rotation_euler = (0, 0, angle)
    obj.keyframe_insert(data_path="rotation_euler", frame=duration_frames)

    # Make linear for smooth loop
    for fcurve in action.fcurves:
        for kp in fcurve.keyframe_points:
            kp.interpolation = 'LINEAR'

    return action
```

### Bobbing/Floating Motion

```python
import bpy
import math

def animate_bob(obj, duration_frames=60, amplitude=0.3, base_height=0):
    """Sine wave vertical motion."""
    if not obj.animation_data:
        obj.animation_data_create()

    action = bpy.data.actions.new(f"{obj.name}_Bob")
    obj.animation_data.action = action

    for frame in range(1, duration_frames + 1):
        t = (frame - 1) / duration_frames
        obj.location.z = base_height + math.sin(t * 2 * math.pi) * amplitude
        obj.keyframe_insert(data_path="location", index=2, frame=frame)

    return action
```

### Platform Movement (A to B)

```python
import bpy

def animate_platform(obj, start, end, duration_frames=60, pause_frames=30):
    """Move between two positions with pauses at each end."""
    if not obj.animation_data:
        obj.animation_data_create()

    action = bpy.data.actions.new(f"{obj.name}_Move")
    obj.animation_data.action = action

    total = duration_frames + pause_frames * 2

    # Start position (hold)
    obj.location = start
    obj.keyframe_insert(data_path="location", frame=1)
    obj.keyframe_insert(data_path="location", frame=pause_frames)

    # Move to end
    obj.location = end
    obj.keyframe_insert(data_path="location", frame=pause_frames + duration_frames)

    # Hold at end
    obj.keyframe_insert(data_path="location", frame=pause_frames * 2 + duration_frames)

    # Return to start
    obj.location = start
    obj.keyframe_insert(data_path="location", frame=total)

    return action
```

### Pulsing Scale

```python
import bpy
import math

def animate_pulse(obj, duration_frames=30, min_scale=0.9, max_scale=1.1):
    """Breathing/pulsing scale effect."""
    if not obj.animation_data:
        obj.animation_data_create()

    action = bpy.data.actions.new(f"{obj.name}_Pulse")
    obj.animation_data.action = action

    for frame in range(1, duration_frames + 1):
        t = (frame - 1) / duration_frames
        # Smooth sine wave between min and max
        scale = min_scale + (max_scale - min_scale) * (math.sin(t * 2 * math.pi) * 0.5 + 0.5)
        obj.scale = (scale, scale, scale)
        obj.keyframe_insert(data_path="scale", frame=frame)

    return action
```

### Combined Motion (Spin + Bob)

```python
import bpy
import math

def animate_pickup(obj, duration_frames=60):
    """Classic pickup animation: spin + bob."""
    if not obj.animation_data:
        obj.animation_data_create()

    action = bpy.data.actions.new(f"{obj.name}_Pickup")
    obj.animation_data.action = action

    base_z = obj.location.z

    for frame in range(1, duration_frames + 1):
        t = (frame - 1) / duration_frames

        # Spin around Y axis
        obj.rotation_euler.y = t * 2 * math.pi
        obj.keyframe_insert(data_path="rotation_euler", index=1, frame=frame)

        # Bob up and down
        obj.location.z = base_z + math.sin(t * 4 * math.pi) * 0.1
        obj.keyframe_insert(data_path="location", index=2, frame=frame)

    # Make rotation linear
    for fcurve in action.fcurves:
        if 'rotation' in fcurve.data_path:
            for kp in fcurve.keyframe_points:
                kp.interpolation = 'LINEAR'

    return action
```

## Multiple Actions Per Object

Export different animations as separate clips:

```python
import bpy

obj = bpy.context.active_object

# Ensure animation data exists
if not obj.animation_data:
    obj.animation_data_create()

# Create multiple actions
actions = {
    "Idle": create_idle_animation,
    "Open": create_open_animation,
    "Close": create_close_animation,
    "Locked": create_locked_animation,
}

for name, create_func in actions.items():
    action = bpy.data.actions.new(name)
    obj.animation_data.action = action
    create_func(obj)
    # Action is now stored in bpy.data.actions
```

When exported with `export_animation_mode='ACTIONS'`, each Action becomes a separate animation clip.

## Animation Modifiers

Add procedural effects on top of keyframes:

```python
# Get fcurve
fcurve = obj.animation_data.action.fcurves.find('location', index=2)

# Add noise modifier
noise = fcurve.modifiers.new('NOISE')
noise.scale = 3.0
noise.strength = 0.1
noise.phase = 0
```

**Common Modifiers:**

| Modifier | Effect |
|----------|--------|
| `NOISE` | Random variation |
| `CYCLES` | Auto-loop animation |
| `LIMITS` | Clamp values |
| `STEPPED` | Quantize to steps |

## Transform Origin

Animation happens around the object's origin. To animate around a different point:

```python
# Method 1: Move origin
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

# Method 2: Parent to empty at desired pivot
pivot = bpy.data.objects.new("Pivot", None)
bpy.context.collection.objects.link(pivot)
pivot.location = (0, 0, 0)  # Pivot point
obj.parent = pivot
# Animate pivot instead of obj
```

## Export Considerations

### Looping Animations

For seamless loops, ensure first and last keyframes match:

```python
# Copy first keyframe to last
first_frame_value = obj.location.copy()
# ... animate ...
obj.location = first_frame_value
obj.keyframe_insert(data_path="location", frame=last_frame)
```

### Frame Rate

Set scene frame rate to match target:

```python
bpy.context.scene.render.fps = 30  # 30 FPS for games
```

### Object Naming

Object name determines animation clip association in glTF:

```python
obj.name = "Coin"  # Results in "Coin" animation clips
```
