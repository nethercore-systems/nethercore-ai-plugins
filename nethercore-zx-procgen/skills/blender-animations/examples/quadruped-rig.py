#!/usr/bin/env blender --background --python
"""
Quadruped Rig Creation

Creates an 18-bone quadruped skeleton suitable for dogs, wolves,
horses, or other four-legged creatures. Includes a simple mesh
and basic walk cycle animation.

Usage:
    blender --background --python quadruped-rig.py

Output: /tmp/quadruped_rig.glb
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
# BONE DEFINITIONS
# =============================================================================

# Quadruped skeleton (dog/wolf proportions)
# Each bone: (name, parent_name, head_xyz, tail_xyz)
QUADRUPED_BONES = [
    # Core spine
    ("root", None, (0, 0, 0), (0, 0, 0.1)),
    ("hips", "root", (0, -0.4, 0.5), (0, -0.2, 0.55)),
    ("spine", "hips", (0, -0.2, 0.55), (0, 0.1, 0.6)),
    ("chest", "spine", (0, 0.1, 0.6), (0, 0.35, 0.55)),
    ("neck", "chest", (0, 0.35, 0.55), (0, 0.5, 0.7)),
    ("head", "neck", (0, 0.5, 0.7), (0, 0.7, 0.7)),

    # Tail
    ("tail_1", "hips", (0, -0.4, 0.5), (0, -0.55, 0.45)),
    ("tail_2", "tail_1", (0, -0.55, 0.45), (0, -0.7, 0.35)),

    # Front left leg
    ("fl_shoulder", "chest", (-0.12, 0.3, 0.5), (-0.12, 0.3, 0.3)),
    ("fl_foreleg", "fl_shoulder", (-0.12, 0.3, 0.3), (-0.12, 0.35, 0.1)),
    ("fl_paw", "fl_foreleg", (-0.12, 0.35, 0.1), (-0.12, 0.4, 0)),

    # Front right leg
    ("fr_shoulder", "chest", (0.12, 0.3, 0.5), (0.12, 0.3, 0.3)),
    ("fr_foreleg", "fr_shoulder", (0.12, 0.3, 0.3), (0.12, 0.35, 0.1)),
    ("fr_paw", "fr_foreleg", (0.12, 0.35, 0.1), (0.12, 0.4, 0)),

    # Back left leg
    ("bl_thigh", "hips", (-0.12, -0.35, 0.45), (-0.12, -0.3, 0.25)),
    ("bl_shin", "bl_thigh", (-0.12, -0.3, 0.25), (-0.12, -0.35, 0.1)),
    ("bl_paw", "bl_shin", (-0.12, -0.35, 0.1), (-0.12, -0.3, 0)),

    # Back right leg
    ("br_thigh", "hips", (0.12, -0.35, 0.45), (0.12, -0.3, 0.25)),
    ("br_shin", "br_thigh", (0.12, -0.3, 0.25), (0.12, -0.35, 0.1)),
    ("br_paw", "br_shin", (0.12, -0.35, 0.1), (0.12, -0.3, 0)),
]

# =============================================================================
# CREATE ARMATURE
# =============================================================================

def create_armature(name, bone_definitions):
    """Create armature from bone definitions."""
    armature = bpy.data.armatures.new(name)
    rig = bpy.data.objects.new(name, armature)
    bpy.context.collection.objects.link(rig)

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

    bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')
    bpy.ops.object.mode_set(mode='OBJECT')
    return rig


print("Creating quadruped armature...")
rig = create_armature("QuadrupedRig", QUADRUPED_BONES)

# =============================================================================
# CREATE SIMPLE MESH
# =============================================================================

def create_quadruped_mesh():
    """Create simple quadruped body mesh."""
    # Body (elongated capsule)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.12,
        depth=0.7,
        location=(0, 0, 0.55),
        rotation=(1.57, 0, 0)  # Rotate to horizontal
    )
    body = bpy.context.active_object
    body.name = "Body"

    # Head (sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.1,
        segments=8,
        ring_count=6,
        location=(0, 0.6, 0.7)
    )
    head = bpy.context.active_object
    head.name = "Head_mesh"

    # Legs (4 cylinders)
    leg_positions = [
        ("FL", -0.12, 0.3),   # Front left
        ("FR", 0.12, 0.3),    # Front right
        ("BL", -0.12, -0.35), # Back left
        ("BR", 0.12, -0.35),  # Back right
    ]

    for name, x, y in leg_positions:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.04,
            depth=0.5,
            location=(x, y, 0.25)
        )
        leg = bpy.context.active_object
        leg.name = f"{name}_Leg_mesh"

    # Tail (thin cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.02,
        depth=0.3,
        location=(0, -0.55, 0.4),
        rotation=(0.5, 0, 0)
    )
    tail = bpy.context.active_object
    tail.name = "Tail_mesh"

    # Join all meshes
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.select_set(True)

    bpy.context.view_layer.objects.active = bpy.data.objects["Body"]
    bpy.ops.object.join()

    mesh = bpy.context.active_object
    mesh.name = "QuadrupedMesh"
    return mesh


print("Creating placeholder mesh...")
mesh = create_quadruped_mesh()

# =============================================================================
# BIND MESH TO ARMATURE
# =============================================================================

bpy.ops.object.select_all(action='DESELECT')
mesh.select_set(True)
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# Cleanup weights
bpy.context.view_layer.objects.active = mesh
bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
bpy.ops.object.vertex_group_normalize_all(lock_active=False)
bpy.ops.object.vertex_group_limit_total(limit=4)
bpy.ops.object.mode_set(mode='OBJECT')

print("Mesh bound to armature")

# =============================================================================
# CREATE WALK CYCLE
# =============================================================================

print("Creating quadruped walk cycle...")

rig.animation_data_create()
walk_action = bpy.data.actions.new("Walk")
rig.animation_data.action = walk_action

bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')

# Get pose bones
fl_shoulder = rig.pose.bones["fl_shoulder"]
fr_shoulder = rig.pose.bones["fr_shoulder"]
bl_thigh = rig.pose.bones["bl_thigh"]
br_thigh = rig.pose.bones["br_thigh"]
spine = rig.pose.bones["spine"]
tail_1 = rig.pose.bones["tail_1"]

# Set rotation mode
for bone in [fl_shoulder, fr_shoulder, bl_thigh, br_thigh, spine, tail_1]:
    bone.rotation_mode = 'XYZ'

# Animation parameters
DURATION = 30  # frames (1 second at 30fps)
LEG_SWING = 0.4  # radians
SPINE_SWAY = 0.05
TAIL_WAG = 0.2

# Quadruped walk: diagonal pairs move together
# FL + BR, then FR + BL (trot gait)
for frame in range(1, DURATION + 1):
    bpy.context.scene.frame_set(frame)
    t = (frame - 1) / DURATION
    phase = t * 2 * math.pi

    # Diagonal pair 1: Front-left + Back-right
    fl_shoulder.rotation_euler.x = math.sin(phase) * LEG_SWING
    br_thigh.rotation_euler.x = math.sin(phase) * LEG_SWING

    # Diagonal pair 2: Front-right + Back-left (opposite phase)
    fr_shoulder.rotation_euler.x = math.sin(phase + math.pi) * LEG_SWING
    bl_thigh.rotation_euler.x = math.sin(phase + math.pi) * LEG_SWING

    # Spine lateral sway
    spine.rotation_euler.z = math.sin(phase * 2) * SPINE_SWAY

    # Tail wag
    tail_1.rotation_euler.z = math.sin(phase * 2) * TAIL_WAG

    # Insert keyframes
    fl_shoulder.keyframe_insert(data_path="rotation_euler", frame=frame)
    fr_shoulder.keyframe_insert(data_path="rotation_euler", frame=frame)
    bl_thigh.keyframe_insert(data_path="rotation_euler", frame=frame)
    br_thigh.keyframe_insert(data_path="rotation_euler", frame=frame)
    spine.keyframe_insert(data_path="rotation_euler", frame=frame)
    tail_1.keyframe_insert(data_path="rotation_euler", frame=frame)

bpy.ops.object.mode_set(mode='OBJECT')
print(f"Created {DURATION} keyframes for walk cycle")

# =============================================================================
# CREATE IDLE ANIMATION
# =============================================================================

idle_action = bpy.data.actions.new("Idle")
rig.animation_data.action = idle_action

bpy.ops.object.mode_set(mode='POSE')

head = rig.pose.bones["head"]
head.rotation_mode = 'XYZ'

IDLE_DURATION = 60  # 2 seconds

for frame in range(1, IDLE_DURATION + 1):
    bpy.context.scene.frame_set(frame)
    t = (frame - 1) / IDLE_DURATION
    breath = math.sin(t * 2 * math.pi)

    # Subtle breathing
    spine.location.z = breath * 0.005
    spine.keyframe_insert(data_path="location", frame=frame)

    # Occasional head look
    head.rotation_euler.z = math.sin(t * math.pi * 0.5) * 0.1
    head.keyframe_insert(data_path="rotation_euler", frame=frame)

    # Gentle tail sway
    tail_1.rotation_euler.z = math.sin(t * 4 * math.pi) * 0.1
    tail_1.keyframe_insert(data_path="rotation_euler", frame=frame)

bpy.ops.object.mode_set(mode='OBJECT')
print(f"Created {IDLE_DURATION} keyframes for idle animation")

# =============================================================================
# CREATE RUN CYCLE
# =============================================================================

run_action = bpy.data.actions.new("Run")
rig.animation_data.action = run_action

bpy.ops.object.mode_set(mode='POSE')

RUN_DURATION = 20  # Faster than walk
RUN_SWING = 0.6  # Larger swing

for frame in range(1, RUN_DURATION + 1):
    bpy.context.scene.frame_set(frame)
    t = (frame - 1) / RUN_DURATION
    phase = t * 2 * math.pi

    # Gallop: front legs together, back legs together
    fl_shoulder.rotation_euler.x = math.sin(phase) * RUN_SWING
    fr_shoulder.rotation_euler.x = math.sin(phase) * RUN_SWING

    bl_thigh.rotation_euler.x = math.sin(phase + math.pi * 0.7) * RUN_SWING
    br_thigh.rotation_euler.x = math.sin(phase + math.pi * 0.7) * RUN_SWING

    # More pronounced spine movement
    spine.rotation_euler.x = math.sin(phase * 2) * 0.1
    spine.rotation_euler.z = math.sin(phase * 2) * 0.03

    # Tail streams behind
    tail_1.rotation_euler.x = 0.3 + math.sin(phase * 2) * 0.1

    # Insert keyframes
    fl_shoulder.keyframe_insert(data_path="rotation_euler", frame=frame)
    fr_shoulder.keyframe_insert(data_path="rotation_euler", frame=frame)
    bl_thigh.keyframe_insert(data_path="rotation_euler", frame=frame)
    br_thigh.keyframe_insert(data_path="rotation_euler", frame=frame)
    spine.keyframe_insert(data_path="rotation_euler", frame=frame)
    tail_1.keyframe_insert(data_path="rotation_euler", frame=frame)

bpy.ops.object.mode_set(mode='OBJECT')
print(f"Created {RUN_DURATION} keyframes for run cycle")

# =============================================================================
# PRINT SKELETON INFO
# =============================================================================

print("\nSkeleton created with bones:")
for i, bone in enumerate(rig.data.bones):
    parent = bone.parent.name if bone.parent else "None"
    print(f"  {i:2d}: {bone.name:15s} (parent: {parent})")

# =============================================================================
# EXPORT
# =============================================================================

output_path = "/tmp/quadruped_rig.glb"

bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_skins=True,
    export_all_influences=False,
)

print(f"\nExported: {output_path}")
print(f"Total bones: {len(rig.data.bones)}")
print(f"Total vertices: {len(mesh.data.vertices)}")
print("\nAnimations included:")
for action in bpy.data.actions:
    frames = action.frame_range[1] - action.frame_range[0]
    print(f"  - {action.name}: {frames:.0f} frames")
