#!/usr/bin/env blender --background --python
"""
Walk Cycle Animation

Creates a simple humanoid with a procedural walk cycle animation.
Demonstrates skeletal animation workflow.

Usage:
    blender --background --python walk-cycle.py

Output: /tmp/walk_cycle.glb
"""

import bpy
import math
from mathutils import Vector

# =============================================================================
# SCENE SETUP
# =============================================================================

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 30
scene.render.fps = 30

# =============================================================================
# CREATE SIMPLE RIG
# =============================================================================

BONES = [
    ("root", None, (0, 0, 0), (0, 0, 0.1)),
    ("hips", "root", (0, 0, 1.0), (0, 0, 1.15)),
    ("spine", "hips", (0, 0, 1.15), (0, 0, 1.4)),
    ("l_thigh", "hips", (-0.1, 0, 1.0), (-0.1, 0, 0.55)),
    ("l_shin", "l_thigh", (-0.1, 0, 0.55), (-0.1, 0, 0.1)),
    ("l_foot", "l_shin", (-0.1, 0, 0.1), (-0.1, 0.1, 0)),
    ("r_thigh", "hips", (0.1, 0, 1.0), (0.1, 0, 0.55)),
    ("r_shin", "r_thigh", (0.1, 0, 0.55), (0.1, 0, 0.1)),
    ("r_foot", "r_shin", (0.1, 0, 0.1), (0.1, 0.1, 0)),
]

# Create armature
armature = bpy.data.armatures.new("WalkRig")
rig = bpy.data.objects.new("WalkRig", armature)
bpy.context.collection.objects.link(rig)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='EDIT')

bone_map = {}
for bone_name, parent_name, head, tail in BONES:
    bone = armature.edit_bones.new(bone_name)
    bone.head = Vector(head)
    bone.tail = Vector(tail)
    if parent_name:
        bone.parent = bone_map[parent_name]
    bone_map[bone_name] = bone

bpy.ops.object.mode_set(mode='OBJECT')

# =============================================================================
# CREATE SIMPLE MESH
# =============================================================================

# Body
bpy.ops.mesh.primitive_cube_add(size=0.3, location=(0, 0, 1.25))
body = bpy.context.active_object
body.scale.z = 0.4
bpy.ops.object.transform_apply(scale=True)

# Legs
for side, x in [("L", -0.1), ("R", 0.1)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.9, location=(x, 0, 0.55))
    leg = bpy.context.active_object
    leg.name = f"{side}_leg"

# Join meshes
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.join()
mesh = bpy.context.active_object
mesh.name = "WalkMesh"

# =============================================================================
# BIND MESH
# =============================================================================

mesh.select_set(True)
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# Cleanup weights
bpy.context.view_layer.objects.active = mesh
bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
bpy.ops.object.vertex_group_normalize_all()
bpy.ops.object.vertex_group_limit_total(limit=4)
bpy.ops.object.mode_set(mode='OBJECT')

# =============================================================================
# CREATE WALK CYCLE
# =============================================================================

print("Creating walk cycle animation...")

rig.animation_data_create()
walk_action = bpy.data.actions.new("Walk")
rig.animation_data.action = walk_action

bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')

# Get pose bones
l_thigh = rig.pose.bones["l_thigh"]
r_thigh = rig.pose.bones["r_thigh"]
l_shin = rig.pose.bones["l_shin"]
r_shin = rig.pose.bones["r_shin"]
hips = rig.pose.bones["hips"]
spine = rig.pose.bones["spine"]

# Set rotation mode
for bone in [l_thigh, r_thigh, l_shin, r_shin, hips, spine]:
    bone.rotation_mode = 'XYZ'

# Animation parameters
DURATION = 30  # frames
SWING_ANGLE = 0.5  # radians (~28 degrees)
KNEE_BEND = 0.7  # radians (~40 degrees)
BOB_HEIGHT = 0.02  # meters
SPINE_TWIST = 0.1  # radians

# Generate keyframes
for frame in range(1, DURATION + 1):
    bpy.context.scene.frame_set(frame)
    t = (frame - 1) / DURATION
    phase = t * 2 * math.pi

    # Thigh swing (opposite phases)
    l_thigh.rotation_euler.x = math.sin(phase) * SWING_ANGLE
    r_thigh.rotation_euler.x = math.sin(phase + math.pi) * SWING_ANGLE

    # Knee bend (only during forward swing)
    l_shin.rotation_euler.x = max(0, math.sin(phase + math.pi/2)) * KNEE_BEND
    r_shin.rotation_euler.x = max(0, math.sin(phase + math.pi + math.pi/2)) * KNEE_BEND

    # Hip vertical bob (two peaks per cycle)
    hips.location.z = abs(math.sin(phase * 2)) * BOB_HEIGHT

    # Spine counter-twist
    spine.rotation_euler.z = math.sin(phase) * SPINE_TWIST

    # Insert keyframes
    l_thigh.keyframe_insert(data_path="rotation_euler", frame=frame)
    r_thigh.keyframe_insert(data_path="rotation_euler", frame=frame)
    l_shin.keyframe_insert(data_path="rotation_euler", frame=frame)
    r_shin.keyframe_insert(data_path="rotation_euler", frame=frame)
    hips.keyframe_insert(data_path="location", frame=frame)
    spine.keyframe_insert(data_path="rotation_euler", frame=frame)

bpy.ops.object.mode_set(mode='OBJECT')

print(f"Created {DURATION} keyframes for walk cycle")

# =============================================================================
# CREATE IDLE ANIMATION
# =============================================================================

idle_action = bpy.data.actions.new("Idle")
rig.animation_data.action = idle_action

bpy.ops.object.mode_set(mode='POSE')

IDLE_DURATION = 60  # 2 seconds at 30fps

for frame in range(1, IDLE_DURATION + 1):
    bpy.context.scene.frame_set(frame)
    t = (frame - 1) / IDLE_DURATION
    breath = math.sin(t * 2 * math.pi)

    # Subtle breathing
    spine.scale.y = 1.0 + breath * 0.01
    spine.keyframe_insert(data_path="scale", frame=frame)

    # Tiny hip sway
    hips.location.x = math.sin(t * math.pi) * 0.005
    hips.keyframe_insert(data_path="location", frame=frame)

bpy.ops.object.mode_set(mode='OBJECT')

print(f"Created {IDLE_DURATION} keyframes for idle animation")

# =============================================================================
# EXPORT
# =============================================================================

output_path = "/tmp/walk_cycle.glb"

bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_skins=True,
    export_all_influences=False,
)

print(f"\nExported: {output_path}")
print("\nAnimations included:")
for action in bpy.data.actions:
    frames = action.frame_range[1] - action.frame_range[0]
    print(f"  - {action.name}: {frames:.0f} frames")
