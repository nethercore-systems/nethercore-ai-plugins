#!/usr/bin/env blender --background --python
"""
Walk Cycle Animation (IK Approach)

Creates a humanoid walk cycle using IK for foot placement, then bakes to FK.
Demonstrates the two-stage animation workflow with coordinate reasoning.

Workflow:
1. Create rig with standard bone naming
2. Set up leg IK (feet + pole targets)
3. Keyframe IK targets (positions, not rotations)
4. Add FK for upper body (hips, spine, arms)
5. Bake IK to FK
6. Export pure FK animation

Usage:
    blender --background --python walk-cycle-ik.py

Output: /tmp/walk_cycle_ik.glb
"""

import bpy
import math
from mathutils import Vector

# =============================================================================
# IK UTILITIES (normally in lib/animation_utils.py)
# =============================================================================

def setup_leg_ik(armature, side='L'):
    """Sets up IK for a humanoid leg with pole target."""
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    thigh = edit_bones.get(f"thigh.{side}")
    shin = edit_bones.get(f"shin.{side}")
    foot = edit_bones.get(f"foot.{side}")

    # IK target at foot
    ik_target = edit_bones.new(f"ik_foot.{side}")
    ik_target.head = foot.head.copy()
    ik_target.tail = foot.head.copy()
    ik_target.tail.y += 0.1
    ik_target.parent = None

    # Pole target in front of knee
    pole = edit_bones.new(f"pole_knee.{side}")
    pole.head = shin.head.copy()
    pole.head.y += 0.4
    pole.tail = pole.head.copy()
    pole.tail.y += 0.1
    pole.parent = None

    bpy.ops.object.mode_set(mode='POSE')

    # Add IK constraint
    pose_shin = armature.pose.bones[f"shin.{side}"]
    ik = pose_shin.constraints.new('IK')
    ik.target = armature
    ik.subtarget = f"ik_foot.{side}"
    ik.pole_target = armature
    ik.pole_subtarget = f"pole_knee.{side}"
    ik.pole_angle = 0
    ik.chain_count = 2

    return f"ik_foot.{side}", f"pole_knee.{side}"


def keyframe_ik_target(armature, target_name, frame, location):
    """Keyframes an IK target's world position."""
    bpy.ops.object.mode_set(mode='POSE')
    target = armature.pose.bones[target_name]
    target.location = Vector(location)
    target.keyframe_insert('location', frame=frame)


def bake_ik_to_fk(armature, frame_start, frame_end):
    """Bakes IK animation to FK keyframes and removes IK."""
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')

    bpy.ops.nla.bake(
        frame_start=frame_start,
        frame_end=frame_end,
        only_selected=True,
        visual_keying=True,
        clear_constraints=True,
        bake_types={'POSE'}
    )

    # Remove IK bones
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones
    for name in list(edit_bones.keys()):
        if name.startswith('ik_') or name.startswith('pole_'):
            edit_bones.remove(edit_bones[name])
    bpy.ops.object.mode_set(mode='OBJECT')


# =============================================================================
# SCENE SETUP
# =============================================================================

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = 24
scene.render.fps = 30

# =============================================================================
# CREATE RIG (standard naming for IK compatibility)
# =============================================================================

BONES = [
    # Core
    ("root", None, (0, 0, 0), (0, 0, 0.1)),
    ("hips", "root", (0, 0, 1.0), (0, 0, 1.15)),
    ("spine", "hips", (0, 0, 1.15), (0, 0, 1.4)),

    # Left leg (standard naming: thigh.L, shin.L, foot.L)
    ("thigh.L", "hips", (-0.1, 0, 1.0), (-0.1, 0, 0.55)),
    ("shin.L", "thigh.L", (-0.1, 0, 0.55), (-0.1, 0, 0.1)),
    ("foot.L", "shin.L", (-0.1, 0, 0.1), (-0.1, 0.15, 0)),

    # Right leg
    ("thigh.R", "hips", (0.1, 0, 1.0), (0.1, 0, 0.55)),
    ("shin.R", "thigh.R", (0.1, 0, 0.55), (0.1, 0, 0.1)),
    ("foot.R", "shin.R", (0.1, 0, 0.1), (0.1, 0.15, 0)),
]

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
# CREATE MESH (simplified body)
# =============================================================================

bpy.ops.mesh.primitive_cube_add(size=0.3, location=(0, 0, 1.25))
body = bpy.context.active_object
body.scale.z = 0.4
bpy.ops.object.transform_apply(scale=True)

for side, x in [("L", -0.1), ("R", 0.1)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.9, location=(x, 0, 0.55))

bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.join()
mesh = bpy.context.active_object
mesh.name = "WalkMesh"

# Bind mesh to rig
mesh.select_set(True)
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# =============================================================================
# SET UP LEG IK
# =============================================================================

print("Setting up leg IK...")
setup_leg_ik(rig, 'L')
setup_leg_ik(rig, 'R')

# =============================================================================
# CREATE WALK CYCLE ANIMATION
# =============================================================================

print("Creating walk cycle with IK feet...")

rig.animation_data_create()
walk_action = bpy.data.actions.new("Walk")
rig.animation_data.action = walk_action

bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')

# Get FK bones for upper body
hips = rig.pose.bones["hips"]
spine = rig.pose.bones["spine"]
hips.rotation_mode = 'XYZ'
spine.rotation_mode = 'XYZ'

# Walk cycle parameters
STRIDE = 0.35      # Forward distance per step
LIFT = 0.08        # Foot lift height during swing
HIP_BOB = 0.03     # Vertical hip motion
SPINE_TWIST = 0.08 # Counter-rotation in radians

# Define foot positions at key frames
# Using IK means we specify WHERE feet go, not HOW legs rotate

FOOT_POSITIONS = {
    # Frame 0: Right foot forward (contact), left foot back (push-off)
    0: {
        'R': (0.1, STRIDE/2, 0),      # Right foot forward, on ground
        'L': (-0.1, -STRIDE/2, 0),    # Left foot back, on ground
    },
    # Frame 6: Right foot flat (passing), left foot swinging
    6: {
        'R': (0.1, STRIDE/4, 0),      # Right foot under body
        'L': (-0.1, 0, LIFT),         # Left foot lifted, passing
    },
    # Frame 12: Left foot forward (contact), right foot back
    12: {
        'R': (0.1, -STRIDE/2, 0),     # Right foot back
        'L': (-0.1, STRIDE/2, 0),     # Left foot forward
    },
    # Frame 18: Left foot flat, right foot swinging
    18: {
        'R': (0.1, 0, LIFT),          # Right foot lifted
        'L': (-0.1, STRIDE/4, 0),     # Left foot under body
    },
    # Frame 24: Back to start (looping)
    24: {
        'R': (0.1, STRIDE/2, 0),
        'L': (-0.1, -STRIDE/2, 0),
    },
}

# Keyframe IK targets (just positions - IK solver handles rotations)
for frame, positions in FOOT_POSITIONS.items():
    keyframe_ik_target(rig, "ik_foot.R", frame, positions['R'])
    keyframe_ik_target(rig, "ik_foot.L", frame, positions['L'])

# Add upper body FK animation with coordinate reasoning
for frame in range(0, 25, 6):
    bpy.context.scene.frame_set(frame)
    t = frame / 24
    phase = t * 2 * math.pi

    # COORDINATE REASONING for hip bob:
    # 1. INTENT: Hips dip when foot contacts ground, rise during swing
    # 2. BONE: hips bone controls pelvis position
    # 3. CONVENTION: Z is up in Blender
    # 4. AXIS: location.z for vertical motion
    # 5. VALUE: Two dips per cycle (at frame 0 and 12)
    hips.location.z = abs(math.sin(phase * 2)) * HIP_BOB
    hips.keyframe_insert('location', frame=frame)

    # COORDINATE REASONING for spine twist:
    # 1. INTENT: Spine counter-rotates against leg swing for balance
    # 2. BONE: spine bone
    # 3. CONVENTION: Z-up, Y-forward
    # 4. AXIS: Z rotation = twist around vertical axis
    # 5. SIGN: When right leg forward, twist left (negative Z)
    spine.rotation_euler.z = math.sin(phase) * SPINE_TWIST
    spine.keyframe_insert('rotation_euler', frame=frame)

bpy.ops.object.mode_set(mode='OBJECT')

# =============================================================================
# BAKE IK TO FK
# =============================================================================

print("Baking IK to FK...")
bake_ik_to_fk(rig, 0, 24)
print("IK baked and removed. Animation is now pure FK.")

# =============================================================================
# EXPORT
# =============================================================================

output_path = "/tmp/walk_cycle_ik.glb"

bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_skins=True,
    export_all_influences=False,
)

print(f"\nExported: {output_path}")
print("\nBenefits of IK approach:")
print("  - Feet stay planted (no sliding)")
print("  - Easier to specify foot positions than leg rotations")
print("  - Baked result is pure FK (ZX runtime compatible)")
