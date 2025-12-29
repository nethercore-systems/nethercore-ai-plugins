#!/usr/bin/env blender --background --python
"""
Door Open/Close Animation

Creates a door with frame, animated on hinge.
Demonstrates multiple Actions for the same object.

Usage:
    blender --background --python door-open-close.py

Output: /tmp/door.glb
"""

import bpy
import math

# =============================================================================
# SCENE SETUP
# =============================================================================

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 30
scene.render.fps = 30

# =============================================================================
# CREATE DOOR GEOMETRY
# =============================================================================

# Door frame (static reference)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1))
frame = bpy.context.active_object
frame.name = "DoorFrame"
frame.scale = (0.1, 0.9, 2.0)
bpy.ops.object.transform_apply(scale=True)

# Door panel
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.4, 0, 1))
door = bpy.context.active_object
door.name = "Door"
door.scale = (0.05, 0.8, 1.9)
bpy.ops.object.transform_apply(scale=True)

# Move origin to hinge edge
bpy.context.view_layer.objects.active = door
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')  # Cursor at 0,0,0
# Manually set origin to hinge position
door.location = (0.05, -0.4, 1)  # Hinge on left edge

# Handle
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.03,
    depth=0.08,
    location=(0.6, -0.35, 1)
)
handle = bpy.context.active_object
handle.name = "Handle"
handle.rotation_euler.x = math.radians(90)

# Parent handle to door
handle.parent = door
handle.matrix_parent_inverse = door.matrix_world.inverted()

# =============================================================================
# CREATE ANIMATIONS
# =============================================================================

door.animation_data_create()
door.rotation_mode = 'XYZ'

# -----------------------------------------------------------------------------
# Action 1: Open
# -----------------------------------------------------------------------------

open_action = bpy.data.actions.new("Open")
door.animation_data.action = open_action

# Closed position
bpy.context.scene.frame_set(1)
door.rotation_euler = (0, 0, 0)
door.keyframe_insert(data_path="rotation_euler", frame=1)

# Open position (90 degrees on Z)
bpy.context.scene.frame_set(30)
door.rotation_euler = (0, 0, math.radians(-90))
door.keyframe_insert(data_path="rotation_euler", frame=30)

# Add easing
for fcurve in open_action.fcurves:
    for kp in fcurve.keyframe_points:
        kp.interpolation = 'BEZIER'
        kp.easing = 'EASE_OUT'

# -----------------------------------------------------------------------------
# Action 2: Close
# -----------------------------------------------------------------------------

close_action = bpy.data.actions.new("Close")
door.animation_data.action = close_action

# Open position
bpy.context.scene.frame_set(1)
door.rotation_euler = (0, 0, math.radians(-90))
door.keyframe_insert(data_path="rotation_euler", frame=1)

# Closed position
bpy.context.scene.frame_set(30)
door.rotation_euler = (0, 0, 0)
door.keyframe_insert(data_path="rotation_euler", frame=30)

# Add easing with slight bounce
for fcurve in close_action.fcurves:
    for kp in fcurve.keyframe_points:
        kp.interpolation = 'BEZIER'
        kp.easing = 'EASE_IN_OUT'

# -----------------------------------------------------------------------------
# Action 3: Locked (shake)
# -----------------------------------------------------------------------------

locked_action = bpy.data.actions.new("Locked")
door.animation_data.action = locked_action

# Small shake animation
shake_frames = [1, 4, 7, 10, 13, 16]
shake_angles = [0, 5, -5, 4, -3, 0]

for frame, angle in zip(shake_frames, shake_angles):
    bpy.context.scene.frame_set(frame)
    door.rotation_euler = (0, 0, math.radians(angle))
    door.keyframe_insert(data_path="rotation_euler", frame=frame)

# =============================================================================
# EXPORT
# =============================================================================

# Reset door rotation for export
door.rotation_euler = (0, 0, 0)

output_path = "/tmp/door.glb"

bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_skins=False,
)

print(f"Exported: {output_path}")
print("Actions exported:")
for action in bpy.data.actions:
    print(f"  - {action.name}")
    print(f"    Frames: {action.frame_range[0]:.0f} - {action.frame_range[1]:.0f}")
