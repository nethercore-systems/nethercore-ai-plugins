#!/usr/bin/env blender --background --python
"""
BVH Motion Capture Import and Retargeting

Demonstrates importing BVH motion capture data and retargeting
it to a game-ready skeleton. Creates placeholder source motion
since we can't bundle CMU data.

Usage:
    blender --background --python bvh-import-retarget.py

    # With actual BVH file:
    blender --background --python bvh-import-retarget.py -- /path/to/mocap.bvh

Output: /tmp/retargeted_mocap.glb
"""

import bpy
import math
import sys
from mathutils import Vector

# =============================================================================
# SCENE SETUP
# =============================================================================

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 60
scene.render.fps = 30

# =============================================================================
# CREATE TARGET SKELETON (Game-ready humanoid)
# =============================================================================

TARGET_BONES = [
    ("root", None, (0, 0, 0), (0, 0, 0.1)),
    ("hips", "root", (0, 0, 1.0), (0, 0, 1.15)),
    ("spine", "hips", (0, 0, 1.15), (0, 0, 1.35)),
    ("chest", "spine", (0, 0, 1.35), (0, 0, 1.55)),
    ("neck", "chest", (0, 0, 1.55), (0, 0, 1.65)),
    ("head", "neck", (0, 0, 1.65), (0, 0, 1.85)),
    ("l_upper_arm", "chest", (-0.2, 0, 1.5), (-0.45, 0, 1.5)),
    ("l_lower_arm", "l_upper_arm", (-0.45, 0, 1.5), (-0.7, 0, 1.5)),
    ("l_hand", "l_lower_arm", (-0.7, 0, 1.5), (-0.8, 0, 1.5)),
    ("r_upper_arm", "chest", (0.2, 0, 1.5), (0.45, 0, 1.5)),
    ("r_lower_arm", "r_upper_arm", (0.45, 0, 1.5), (0.7, 0, 1.5)),
    ("r_hand", "r_lower_arm", (0.7, 0, 1.5), (0.8, 0, 1.5)),
    ("l_upper_leg", "hips", (-0.1, 0, 1.0), (-0.1, 0, 0.55)),
    ("l_lower_leg", "l_upper_leg", (-0.1, 0, 0.55), (-0.1, 0, 0.1)),
    ("l_foot", "l_lower_leg", (-0.1, 0, 0.1), (-0.1, 0.1, 0)),
    ("r_upper_leg", "hips", (0.1, 0, 1.0), (0.1, 0, 0.55)),
    ("r_lower_leg", "r_upper_leg", (0.1, 0, 0.55), (0.1, 0, 0.1)),
    ("r_foot", "r_lower_leg", (0.1, 0, 0.1), (0.1, 0.1, 0)),
]


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


print("Creating target skeleton...")
target_rig = create_armature("TargetRig", TARGET_BONES)
target_rig.location = (0, 0, 0)

# =============================================================================
# BVH IMPORT (or create placeholder source)
# =============================================================================

# Check for BVH file argument
bvh_file = None
if "--" in sys.argv:
    args = sys.argv[sys.argv.index("--") + 1:]
    if args:
        bvh_file = args[0]

if bvh_file:
    print(f"Importing BVH: {bvh_file}")
    bpy.ops.import_anim.bvh(
        filepath=bvh_file,
        filter_glob="*.bvh",
        target='ARMATURE',
        global_scale=0.01,  # CMU data is in centimeters
        frame_start=1,
        use_fps_scale=True,
        rotate_mode='NATIVE',
    )
    source_rig = bpy.context.active_object
    source_rig.name = "SourceRig"
else:
    # Create placeholder "mocap" skeleton with simple animation
    print("No BVH provided - creating placeholder source animation")

    SOURCE_BONES = [
        ("Hips", None, (0, 0, 1.0), (0, 0, 1.1)),
        ("Spine", "Hips", (0, 0, 1.1), (0, 0, 1.3)),
        ("Spine1", "Spine", (0, 0, 1.3), (0, 0, 1.5)),
        ("Neck", "Spine1", (0, 0, 1.5), (0, 0, 1.6)),
        ("Head", "Neck", (0, 0, 1.6), (0, 0, 1.8)),
        ("LeftShoulder", "Spine1", (-0.15, 0, 1.45), (-0.25, 0, 1.45)),
        ("LeftArm", "LeftShoulder", (-0.25, 0, 1.45), (-0.5, 0, 1.45)),
        ("LeftForeArm", "LeftArm", (-0.5, 0, 1.45), (-0.75, 0, 1.45)),
        ("LeftHand", "LeftForeArm", (-0.75, 0, 1.45), (-0.85, 0, 1.45)),
        ("RightShoulder", "Spine1", (0.15, 0, 1.45), (0.25, 0, 1.45)),
        ("RightArm", "RightShoulder", (0.25, 0, 1.45), (0.5, 0, 1.45)),
        ("RightForeArm", "RightArm", (0.5, 0, 1.45), (0.75, 0, 1.45)),
        ("RightHand", "RightForeArm", (0.75, 0, 1.45), (0.85, 0, 1.45)),
        ("LeftUpLeg", "Hips", (-0.1, 0, 1.0), (-0.1, 0, 0.55)),
        ("LeftLeg", "LeftUpLeg", (-0.1, 0, 0.55), (-0.1, 0, 0.1)),
        ("LeftFoot", "LeftLeg", (-0.1, 0, 0.1), (-0.1, 0.1, 0)),
        ("RightUpLeg", "Hips", (0.1, 0, 1.0), (0.1, 0, 0.55)),
        ("RightLeg", "RightUpLeg", (0.1, 0, 0.55), (0.1, 0, 0.1)),
        ("RightFoot", "RightLeg", (0.1, 0, 0.1), (0.1, 0.1, 0)),
    ]

    source_rig = create_armature("SourceRig", SOURCE_BONES)
    source_rig.location = (2, 0, 0)  # Offset for visibility

    # Create simple walk animation on source
    source_rig.animation_data_create()
    source_action = bpy.data.actions.new("SourceWalk")
    source_rig.animation_data.action = source_action

    bpy.context.view_layer.objects.active = source_rig
    bpy.ops.object.mode_set(mode='POSE')

    # Animate source bones
    left_arm = source_rig.pose.bones["LeftArm"]
    right_arm = source_rig.pose.bones["RightArm"]
    left_leg = source_rig.pose.bones["LeftUpLeg"]
    right_leg = source_rig.pose.bones["RightUpLeg"]

    for bone in [left_arm, right_arm, left_leg, right_leg]:
        bone.rotation_mode = 'XYZ'

    for frame in range(1, 61):
        bpy.context.scene.frame_set(frame)
        t = (frame - 1) / 60
        phase = t * 2 * math.pi

        # Arms swing opposite to legs
        left_arm.rotation_euler.x = math.sin(phase + math.pi) * 0.4
        right_arm.rotation_euler.x = math.sin(phase) * 0.4
        left_leg.rotation_euler.x = math.sin(phase) * 0.5
        right_leg.rotation_euler.x = math.sin(phase + math.pi) * 0.5

        left_arm.keyframe_insert(data_path="rotation_euler", frame=frame)
        right_arm.keyframe_insert(data_path="rotation_euler", frame=frame)
        left_leg.keyframe_insert(data_path="rotation_euler", frame=frame)
        right_leg.keyframe_insert(data_path="rotation_euler", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
    print("Created placeholder source animation")

# =============================================================================
# BONE MAPPING (Source -> Target)
# =============================================================================

# Standard CMU/BVH to game skeleton mapping
BONE_MAP = {
    # Source bone name -> Target bone name
    "Hips": "hips",
    "Spine": "spine",
    "Spine1": "chest",
    "Neck": "neck",
    "Head": "head",
    "LeftArm": "l_upper_arm",
    "LeftForeArm": "l_lower_arm",
    "LeftHand": "l_hand",
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


def retarget_animation(source_rig, target_rig, bone_map, action_name="Retargeted"):
    """
    Copy animation from source to target using bone mapping.
    This is a simplified retarget - production would use constraints.
    """
    print(f"Retargeting animation to '{action_name}'...")

    # Create action on target
    target_rig.animation_data_create()
    target_action = bpy.data.actions.new(action_name)
    target_rig.animation_data.action = target_action

    # Get source action
    if not source_rig.animation_data or not source_rig.animation_data.action:
        print("  No source animation found!")
        return

    source_action = source_rig.animation_data.action
    frame_start = int(source_action.frame_range[0])
    frame_end = int(source_action.frame_range[1])

    print(f"  Source frames: {frame_start} - {frame_end}")

    # Set up pose mode
    bpy.context.view_layer.objects.active = target_rig
    bpy.ops.object.mode_set(mode='POSE')

    # Set rotation mode for all target bones
    for bone in target_rig.pose.bones:
        bone.rotation_mode = 'XYZ'

    bpy.context.view_layer.objects.active = source_rig
    bpy.ops.object.mode_set(mode='POSE')

    for bone in source_rig.pose.bones:
        bone.rotation_mode = 'XYZ'

    # Copy keyframes frame by frame
    for frame in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(frame)

        for source_name, target_name in bone_map.items():
            if source_name not in source_rig.pose.bones:
                continue
            if target_name not in target_rig.pose.bones:
                continue

            source_bone = source_rig.pose.bones[source_name]
            target_bone = target_rig.pose.bones[target_name]

            # Copy rotation (with potential scale adjustment)
            target_bone.rotation_euler = source_bone.rotation_euler.copy()

            # Copy location for root bone only
            if target_name == "hips":
                target_bone.location = source_bone.location.copy()
                target_bone.keyframe_insert(data_path="location", frame=frame)

            target_bone.keyframe_insert(data_path="rotation_euler", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
    print(f"  Retargeted {len(bone_map)} bones across {frame_end - frame_start + 1} frames")


# =============================================================================
# PERFORM RETARGETING
# =============================================================================

retarget_animation(source_rig, target_rig, BONE_MAP, "Walk_Retargeted")

# =============================================================================
# ROOT MOTION EXTRACTION (Optional)
# =============================================================================

def extract_root_motion(rig, action_name):
    """
    Extract root motion into separate action for in-place animation.
    Useful for games that handle movement in code.
    """
    print(f"Extracting root motion from '{action_name}'...")

    if not rig.animation_data or not rig.animation_data.action:
        return

    source_action = rig.animation_data.action

    # Create in-place version
    inplace_action = bpy.data.actions.new(f"{action_name}_InPlace")

    # Copy action
    for fcurve in source_action.fcurves:
        new_fc = inplace_action.fcurves.new(
            data_path=fcurve.data_path,
            index=fcurve.array_index
        )

        for kp in fcurve.keyframe_points:
            new_fc.keyframe_points.insert(kp.co[0], kp.co[1])

        # Zero out root XY translation
        if 'hips' in fcurve.data_path and 'location' in fcurve.data_path:
            if fcurve.array_index in [0, 1]:  # X or Y
                for kp in new_fc.keyframe_points:
                    kp.co[1] = 0

    print(f"  Created '{inplace_action.name}' with zeroed root XY")
    return inplace_action


# Switch to target rig for root motion extraction
bpy.context.view_layer.objects.active = target_rig
extract_root_motion(target_rig, "Walk_Retargeted")

# =============================================================================
# CREATE SIMPLE MESH FOR TARGET
# =============================================================================

print("Creating target mesh...")

bpy.ops.mesh.primitive_cylinder_add(
    radius=0.15,
    depth=0.6,
    location=(0, 0, 1.25)
)
body = bpy.context.active_object
body.name = "TargetBody"

# Bind to target rig
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
target_rig.select_set(True)
bpy.context.view_layer.objects.active = target_rig
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# Cleanup weights
bpy.context.view_layer.objects.active = body
bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
bpy.ops.object.vertex_group_normalize_all(lock_active=False)
bpy.ops.object.vertex_group_limit_total(limit=4)
bpy.ops.object.mode_set(mode='OBJECT')

# =============================================================================
# CLEANUP SOURCE (Don't export)
# =============================================================================

# Delete source rig (we only want target)
bpy.ops.object.select_all(action='DESELECT')
source_rig.select_set(True)
bpy.ops.object.delete()

# Clean up source actions
for action in list(bpy.data.actions):
    if "Source" in action.name:
        bpy.data.actions.remove(action)

# =============================================================================
# EXPORT
# =============================================================================

output_path = "/tmp/retargeted_mocap.glb"

# Select only target for export
bpy.ops.object.select_all(action='DESELECT')
target_rig.select_set(True)
body.select_set(True)

bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_skins=True,
    export_all_influences=False,
    use_selection=True,
)

print(f"\nExported: {output_path}")
print(f"Total bones: {len(target_rig.data.bones)}")
print("\nAnimations included:")
for action in bpy.data.actions:
    frames = action.frame_range[1] - action.frame_range[0]
    print(f"  - {action.name}: {frames:.0f} frames")

print("\n" + "=" * 60)
print("MOCAP RETARGETING NOTES:")
print("=" * 60)
print("""
1. CMU Motion Capture Database:
   - Free BVH files: http://mocap.cs.cmu.edu/
   - Common clips: 01_01 (walk), 02_01 (run), 16_15 (jump)

2. BVH Import Settings:
   - global_scale=0.01 for CMU data (centimeters to meters)
   - use_fps_scale=True to match frame rates
   - rotate_mode='NATIVE' preserves original rotations

3. Retargeting Improvements:
   - Use bone constraints for runtime retargeting
   - Apply rotation offsets for different rest poses
   - Handle different bone roll conventions

4. Root Motion:
   - Extract for in-place animations (loops)
   - Keep for cinematic sequences
   - Store delta as separate data for game code
""")
