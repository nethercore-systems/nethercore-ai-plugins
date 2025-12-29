#!/usr/bin/env blender --background --python
"""
Humanoid Rig Creation

Creates a 20-bone humanoid skeleton with a simple placeholder mesh,
binds them together with automatic weights.

Usage:
    blender --background --python humanoid-rig.py

Output: /tmp/humanoid_rig.glb
"""

import bpy
from mathutils import Vector

# =============================================================================
# SCENE SETUP
# =============================================================================

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 1
scene.render.fps = 30

# =============================================================================
# BONE DEFINITIONS
# =============================================================================

# Each bone: (name, parent_name, head_xyz, tail_xyz)
HUMANOID_BONES = [
    # Core
    ("root", None, (0, 0, 0), (0, 0, 0.1)),
    ("hips", "root", (0, 0, 1.0), (0, 0, 1.15)),
    ("spine", "hips", (0, 0, 1.15), (0, 0, 1.35)),
    ("chest", "spine", (0, 0, 1.35), (0, 0, 1.55)),
    ("neck", "chest", (0, 0, 1.55), (0, 0, 1.65)),
    ("head", "neck", (0, 0, 1.65), (0, 0, 1.85)),

    # Left arm
    ("l_shoulder", "chest", (-0.15, 0, 1.5), (-0.22, 0, 1.5)),
    ("l_upper_arm", "l_shoulder", (-0.22, 0, 1.5), (-0.47, 0, 1.5)),
    ("l_lower_arm", "l_upper_arm", (-0.47, 0, 1.5), (-0.72, 0, 1.5)),
    ("l_hand", "l_lower_arm", (-0.72, 0, 1.5), (-0.82, 0, 1.5)),

    # Right arm
    ("r_shoulder", "chest", (0.15, 0, 1.5), (0.22, 0, 1.5)),
    ("r_upper_arm", "r_shoulder", (0.22, 0, 1.5), (0.47, 0, 1.5)),
    ("r_lower_arm", "r_upper_arm", (0.47, 0, 1.5), (0.72, 0, 1.5)),
    ("r_hand", "r_lower_arm", (0.72, 0, 1.5), (0.82, 0, 1.5)),

    # Left leg
    ("l_upper_leg", "hips", (-0.1, 0, 1.0), (-0.1, 0, 0.55)),
    ("l_lower_leg", "l_upper_leg", (-0.1, 0, 0.55), (-0.1, 0, 0.1)),
    ("l_foot", "l_lower_leg", (-0.1, 0, 0.1), (-0.1, 0.1, 0)),

    # Right leg
    ("r_upper_leg", "hips", (0.1, 0, 1.0), (0.1, 0, 0.55)),
    ("r_lower_leg", "r_upper_leg", (0.1, 0, 0.55), (0.1, 0, 0.1)),
    ("r_foot", "r_lower_leg", (0.1, 0, 0.1), (0.1, 0.1, 0)),
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

    # Recalculate bone rolls for consistent orientation
    bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')

    bpy.ops.object.mode_set(mode='OBJECT')
    return rig


print("Creating humanoid armature...")
rig = create_armature("HumanoidRig", HUMANOID_BONES)

# =============================================================================
# CREATE PLACEHOLDER MESH
# =============================================================================

def create_humanoid_mesh():
    """Create simple mesh for testing skinning."""
    # Body (capsule-like)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.15,
        depth=0.6,
        location=(0, 0, 1.25)
    )
    body = bpy.context.active_object
    body.name = "Body"

    # Head (sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.12,
        location=(0, 0, 1.75)
    )
    head = bpy.context.active_object
    head.name = "Head_mesh"

    # Arms (cylinders)
    for side, x_mult in [("L", -1), ("R", 1)]:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.05,
            depth=0.5,
            location=(x_mult * 0.45, 0, 1.5),
            rotation=(0, 1.57, 0)  # 90 degrees on Y
        )
        arm = bpy.context.active_object
        arm.name = f"{side}_Arm_mesh"

    # Legs (cylinders)
    for side, x_offset in [("L", -0.1), ("R", 0.1)]:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.06,
            depth=0.9,
            location=(x_offset, 0, 0.5)
        )
        leg = bpy.context.active_object
        leg.name = f"{side}_Leg_mesh"

    # Join all meshes
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.select_set(True)

    bpy.context.view_layer.objects.active = bpy.data.objects["Body"]
    bpy.ops.object.join()

    mesh = bpy.context.active_object
    mesh.name = "CharacterMesh"

    return mesh


print("Creating placeholder mesh...")
mesh = create_humanoid_mesh()

# =============================================================================
# BIND MESH TO ARMATURE
# =============================================================================

def bind_mesh_to_armature(mesh_obj, armature_obj):
    """Bind mesh to armature with automatic weights."""
    bpy.ops.object.select_all(action='DESELECT')

    mesh_obj.select_set(True)
    armature_obj.select_set(True)
    bpy.context.view_layer.objects.active = armature_obj

    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    print(f"Bound {mesh_obj.name} to {armature_obj.name}")


print("Binding mesh to armature...")
bind_mesh_to_armature(mesh, rig)

# =============================================================================
# WEIGHT CLEANUP
# =============================================================================

def cleanup_weights(mesh_obj):
    """Normalize and limit weights for glTF export."""
    bpy.context.view_layer.objects.active = mesh_obj
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

    bpy.ops.object.vertex_group_normalize_all(lock_active=False)
    bpy.ops.object.vertex_group_limit_total(limit=4)

    bpy.ops.object.mode_set(mode='OBJECT')
    print("Weights cleaned up")


cleanup_weights(mesh)

# =============================================================================
# PRINT SKELETON INFO
# =============================================================================

print("\nSkeleton created with bones:")
for i, bone in enumerate(rig.data.bones):
    parent = bone.parent.name if bone.parent else "None"
    print(f"  {i:2d}: {bone.name:20s} (parent: {parent})")

# =============================================================================
# EXPORT
# =============================================================================

output_path = "/tmp/humanoid_rig.glb"

bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    export_animations=False,  # No animations yet
    export_skins=True,
    export_all_influences=False,  # Limit to 4
)

print(f"\nExported: {output_path}")
print(f"Total bones: {len(rig.data.bones)}")
print(f"Total vertices: {len(mesh.data.vertices)}")
