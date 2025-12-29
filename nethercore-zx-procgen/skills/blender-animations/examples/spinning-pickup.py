#!/usr/bin/env blender --background --python
"""
Spinning Pickup Animation

Creates a simple mesh with constant rotation animation.
Classic collectible item spinning on Y axis.

Usage:
    blender --background --python spinning-pickup.py

Output: /tmp/spinning_pickup.glb
"""

import bpy
import math

# =============================================================================
# SCENE SETUP
# =============================================================================

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 60
scene.render.fps = 30

# =============================================================================
# CREATE MESH (Simple Octahedron Coin)
# =============================================================================

bpy.ops.mesh.primitive_cylinder_add(
    radius=0.3,
    depth=0.08,
    vertices=8,
    location=(0, 0, 0)
)
coin = bpy.context.active_object
coin.name = "Coin"

# Optional: Add bevel for rounded edges
bpy.ops.object.modifier_add(type='BEVEL')
coin.modifiers["Bevel"].segments = 2
coin.modifiers["Bevel"].width = 0.02
bpy.ops.object.modifier_apply(modifier="Bevel")

# =============================================================================
# CREATE SPINNING ANIMATION
# =============================================================================

# Create animation data
coin.animation_data_create()

# Create action
spin_action = bpy.data.actions.new("Spin")
coin.animation_data.action = spin_action

# Set rotation mode to Euler for simple rotation
coin.rotation_mode = 'XYZ'

# Frame 1: Starting rotation
coin.rotation_euler = (0, 0, 0)
coin.keyframe_insert(data_path="rotation_euler", frame=1)

# Frame 60: Full rotation (will loop seamlessly back to frame 1)
coin.rotation_euler = (0, math.radians(360), 0)  # Y-axis spin
coin.keyframe_insert(data_path="rotation_euler", frame=60)

# Make rotation LINEAR for constant speed
for fcurve in spin_action.fcurves:
    for keyframe in fcurve.keyframe_points:
        keyframe.interpolation = 'LINEAR'

# =============================================================================
# OPTIONAL: ADD BOBBING
# =============================================================================

# Create second action for bob (or combine into one)
bob_action = bpy.data.actions.new("SpinBob")
coin.animation_data.action = bob_action

# Re-add spin keyframes
coin.rotation_euler = (0, 0, 0)
coin.keyframe_insert(data_path="rotation_euler", frame=1)
coin.rotation_euler = (0, math.radians(360), 0)
coin.keyframe_insert(data_path="rotation_euler", frame=60)

# Add bobbing on Z axis
base_z = coin.location.z
for frame in range(1, 61):
    t = (frame - 1) / 60.0
    coin.location.z = base_z + math.sin(t * 2 * math.pi) * 0.1
    coin.keyframe_insert(data_path="location", index=2, frame=frame)

# Make rotation LINEAR, keep location BEZIER for smooth bob
for fcurve in bob_action.fcurves:
    if 'rotation' in fcurve.data_path:
        for kp in fcurve.keyframe_points:
            kp.interpolation = 'LINEAR'

# =============================================================================
# EXPORT
# =============================================================================

output_path = "/tmp/spinning_pickup.glb"

bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS',  # Both "Spin" and "SpinBob" exported
    export_skins=False,  # No armature
)

print(f"Exported: {output_path}")
print("Actions exported:")
for action in bpy.data.actions:
    print(f"  - {action.name}")
