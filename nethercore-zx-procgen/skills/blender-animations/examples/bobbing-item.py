#!/usr/bin/env blender --background --python
"""
Bobbing Item Animation

Creates an object with smooth sine wave vertical motion.
Classic floating collectible/power-up animation.

Usage:
    blender --background --python bobbing-item.py

Output: /tmp/bobbing_item.glb
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
# CREATE MESH
# =============================================================================

# Create a simple gem/crystal shape
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.2,
    segments=8,
    ring_count=4,
    location=(0, 0, 0.5)
)
gem = bpy.context.active_object
gem.name = "PowerUp"

# Stretch into gem shape
gem.scale = (0.5, 0.5, 1.0)
bpy.ops.object.transform_apply(scale=True)

# =============================================================================
# CREATE BOBBING ANIMATION
# =============================================================================

gem.animation_data_create()

# Single bobbing action
bob_action = bpy.data.actions.new("Bob")
gem.animation_data.action = bob_action

# Animation parameters
DURATION = 60        # frames (2 seconds at 30fps)
AMPLITUDE = 0.15     # meters
BASE_HEIGHT = 0.5    # meters

# Generate smooth sine wave motion
for frame in range(1, DURATION + 1):
    t = (frame - 1) / DURATION
    # Sine wave for smooth up/down motion
    gem.location.z = BASE_HEIGHT + math.sin(t * 2 * math.pi) * AMPLITUDE
    gem.keyframe_insert(data_path="location", index=2, frame=frame)

# Ensure smooth interpolation
for fcurve in bob_action.fcurves:
    for kp in fcurve.keyframe_points:
        kp.interpolation = 'BEZIER'
        kp.easing = 'AUTO'

print(f"Created bobbing animation: {DURATION} frames")

# =============================================================================
# ALTERNATIVE: BOB WITH SLIGHT ROTATION
# =============================================================================

gem.rotation_mode = 'XYZ'

bob_rotate_action = bpy.data.actions.new("BobRotate")
gem.animation_data.action = bob_rotate_action

for frame in range(1, DURATION + 1):
    t = (frame - 1) / DURATION
    phase = t * 2 * math.pi

    # Vertical bob
    gem.location.z = BASE_HEIGHT + math.sin(phase) * AMPLITUDE
    gem.keyframe_insert(data_path="location", index=2, frame=frame)

    # Slow Y rotation
    gem.rotation_euler.z = phase * 0.5  # Half rotation per cycle
    gem.keyframe_insert(data_path="rotation_euler", index=2, frame=frame)

    # Slight wobble
    gem.rotation_euler.x = math.sin(phase * 2) * 0.05
    gem.keyframe_insert(data_path="rotation_euler", index=0, frame=frame)

# Make rotation linear for smooth spin
for fcurve in bob_rotate_action.fcurves:
    if 'rotation' in fcurve.data_path:
        for kp in fcurve.keyframe_points:
            kp.interpolation = 'LINEAR'

print(f"Created bob+rotate animation: {DURATION} frames")

# =============================================================================
# ALTERNATIVE: FIGURE-8 MOTION
# =============================================================================

figure8_action = bpy.data.actions.new("Figure8")
gem.animation_data.action = figure8_action

for frame in range(1, DURATION + 1):
    t = (frame - 1) / DURATION
    phase = t * 2 * math.pi

    # Figure-8 pattern (Lissajous curve)
    gem.location.x = math.sin(phase) * 0.1
    gem.location.y = math.sin(phase * 2) * 0.05
    gem.location.z = BASE_HEIGHT + math.sin(phase) * AMPLITUDE * 0.5

    gem.keyframe_insert(data_path="location", frame=frame)

print(f"Created figure-8 animation: {DURATION} frames")

# =============================================================================
# EXPORT
# =============================================================================

# Reset to default position
gem.location = (0, 0, BASE_HEIGHT)
gem.rotation_euler = (0, 0, 0)

output_path = "/tmp/bobbing_item.glb"

bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_skins=False,
)

print(f"\nExported: {output_path}")
print("\nAnimations included:")
for action in bpy.data.actions:
    print(f"  - {action.name}")
