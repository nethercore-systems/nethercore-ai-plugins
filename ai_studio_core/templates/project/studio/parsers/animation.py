"""
Animation Parser - Interprets .spec.py animation specs in Blender.

Applies structured animation specifications to armatures, creating keyframed
animations. Skeleton-agnostic: works with any armature if bone names match.

Usage (via unified generator):
    Place .spec.py files in .studio/specs/animations/
    Run: blender --background --python .studio/generate.py -- --only animations

Outputs:
    generated/animations/*.glb
"""

import math
import random
import sys


# =============================================================================
# PRESET BONE REQUIREMENTS
# =============================================================================
# Documents what bones each preset expects to find in the armature.
# Used by validation to catch mismatches before animation generation.

PRESET_REQUIREMENTS = {
    "humanoid_legs": {
        "required": [
            "leg_upper_L", "leg_lower_L", "foot_L",
            "leg_upper_R", "leg_lower_R", "foot_R",
        ],
        "optional": ["toe_L", "toe_R", "leg_twist_L", "leg_twist_R"],
        "creates": ["ik_foot_L", "ik_foot_R", "pole_knee_L", "pole_knee_R"],
    },
    "humanoid_arms": {
        "required": [
            "arm_upper_L", "arm_lower_L",
            "arm_upper_R", "arm_lower_R",
        ],
        "optional": ["hand_L", "hand_R", "arm_twist_L", "arm_twist_R"],
        "creates": ["ik_hand_L", "ik_hand_R", "pole_elbow_L", "pole_elbow_R"],
    },
    "spider_legs": {
        "required": [
            f"leg_{pos}_{seg}_{side}"
            for pos in ["front", "mid_front", "mid_back", "back"]
            for seg in ["upper", "lower"]
            for side in ["L", "R"]
        ],
        "optional": [],
        "creates": [
            f"ik_leg_{pos}_{side}"
            for pos in ["front", "mid_front", "mid_back", "back"]
            for side in ["L", "R"]
        ],
    },
    "quadruped_legs": {
        "required": [
            f"leg_{pos}_{seg}_{side}"
            for pos in ["front", "back"]
            for seg in ["upper", "lower"]
            for side in ["L", "R"]
        ],
        "optional": [],
        "creates": [
            f"ik_foot_{pos}_{side}"
            for pos in ["front", "back"]
            for side in ["L", "R"]
        ],
    },
    "basic_spine": {
        "required": [],  # Will look for any of: spine_01, spine_02, spine, etc.
        "optional": ["spine_01", "spine_02", "spine_03", "spine", "spine_1", "spine_2"],
        "creates": ["ik_spine_tip"],
    },
    "head_look": {
        "required": ["head"],
        "optional": ["eye_L", "eye_R"],
        "creates": ["look_target"],
    },
}


class AnimationValidationError(Exception):
    """Raised when animation spec references bones not in armature."""
    pass


def get_armature_bones(armature):
    """Extract all bone names from a Blender armature."""
    return set(bone.name for bone in armature.data.bones)


def collect_referenced_bones(spec):
    """
    Collect all bone names referenced in an animation spec.

    Returns dict mapping bone_name -> list of reference locations (for error messages).
    """
    referenced = {}

    def add_ref(bone_name, location):
        if bone_name not in referenced:
            referenced[bone_name] = []
        referenced[bone_name].append(location)

    anim = spec.get('animation', spec)
    rig_setup = anim.get('rig_setup', {})

    # Check ik_chains
    for i, chain in enumerate(rig_setup.get('ik_chains', [])):
        for bone in chain.get('bones', []):
            add_ref(bone, f"rig_setup.ik_chains[{i}].bones")

    # Check constraints
    for i, constraint in enumerate(rig_setup.get('constraints', [])):
        bone = constraint.get('bone')
        if bone:
            add_ref(bone, f"rig_setup.constraints[{i}].bone")

    # Check twist_bones
    for i, twist in enumerate(rig_setup.get('twist_bones', [])):
        source = twist.get('source')
        target = twist.get('target')
        if source:
            add_ref(source, f"rig_setup.twist_bones[{i}].source")
        if target:
            add_ref(target, f"rig_setup.twist_bones[{i}].target")

    # Check aim_constraints
    for i, aim in enumerate(rig_setup.get('aim_constraints', [])):
        bone = aim.get('bone')
        if bone:
            add_ref(bone, f"rig_setup.aim_constraints[{i}].bone")

    # Check foot_systems
    for i, foot in enumerate(rig_setup.get('foot_systems', [])):
        bones = foot.get('bones', {})
        for key, bone in bones.items():
            if bone:
                add_ref(bone, f"rig_setup.foot_systems[{i}].bones.{key}")

    # Check poses
    poses = anim.get('poses', {})
    for pose_name, pose_data in poses.items():
        for bone_name in pose_data.keys():
            add_ref(bone_name, f"poses.{pose_name}")

    return referenced


def get_preset_required_bones(presets, armature_bones):
    """
    Get all bones required by enabled presets.

    Returns dict mapping bone_name -> preset_name for missing required bones.
    """
    missing = {}

    for preset_name, enabled in presets.items():
        if not enabled:
            continue

        requirements = PRESET_REQUIREMENTS.get(preset_name, {})
        required = requirements.get('required', [])

        for bone in required:
            if bone not in armature_bones:
                if bone not in missing:
                    missing[bone] = []
                missing[bone].append(f"preset '{preset_name}'")

    return missing


def validate_against_armature(spec, armature):
    """
    Validate animation spec against armature bones.

    Raises AnimationValidationError if spec references bones not in armature.
    Lists ALL missing bones, not just the first one found.

    Args:
        spec: ANIMATION dict from .spec.py file
        armature: Blender armature object
    """
    armature_bones = get_armature_bones(armature)
    anim = spec.get('animation', spec)
    rig_setup = anim.get('rig_setup', {})
    presets = rig_setup.get('presets', {})

    # Collect all referenced bones
    referenced = collect_referenced_bones(spec)

    # Check explicit bone references
    missing_explicit = {}
    for bone, locations in referenced.items():
        if bone not in armature_bones:
            missing_explicit[bone] = locations

    # Check preset requirements
    missing_from_presets = get_preset_required_bones(presets, armature_bones)

    # Combine all missing bones
    all_missing = {}

    for bone, locations in missing_explicit.items():
        all_missing[bone] = locations

    for bone, preset_names in missing_from_presets.items():
        if bone in all_missing:
            all_missing[bone].extend(preset_names)
        else:
            all_missing[bone] = preset_names

    if all_missing:
        # Build detailed error message
        lines = [
            f"Animation spec references bones not in armature '{armature.name}':",
            "",
            "Missing bones:"
        ]

        for bone, locations in sorted(all_missing.items()):
            loc_str = ", ".join(locations[:3])  # Show first 3 locations
            if len(locations) > 3:
                loc_str += f", ... ({len(locations)} total)"
            lines.append(f"  - {bone} (referenced in: {loc_str})")

        lines.extend([
            "",
            f"Available bones in armature ({len(armature_bones)}):",
            "  " + ", ".join(sorted(armature_bones)),
            "",
            "Fix: Either add missing bones to character spec, or remove references from animation spec."
        ])

        raise AnimationValidationError("\n".join(lines))


def get_action_fcurves(action):
    """
    Get FCurves from action, handling Blender 4.x vs 5.0+ API differences.

    Blender 5.0 changed from action.fcurves to action.layers[].strips[].channelbags[].fcurves
    """
    import bpy

    is_blender_5_plus = bpy.app.version[0] >= 5
    if is_blender_5_plus:
        # Blender 5.0+ layered animation system
        fcurves = []
        for layer in action.layers:
            for strip in layer.strips:
                for channelbag in strip.channelbags:
                    fcurves.extend(channelbag.fcurves)
        return fcurves
    else:
        # Blender 4.x and earlier
        return action.fcurves


def load_spec(spec_path):
    """Load animation spec from .spec.py file.
    """
    with open(spec_path, 'r') as f:
        code = f.read()

    # Execute the spec file to get ANIMATION dict
    namespace = {}
    exec(code, namespace)

    if 'ANIMATION' in namespace:
        return namespace['ANIMATION']
    else:
        raise ValueError(f"No ANIMATION dict found in {spec_path}")


def find_armature():
    """Find the armature object in the scene."""
    import bpy

    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE':
            return obj
    raise ValueError("No armature found in scene")


def reset_pose_to_rest(armature):
    """Reset all bones to rest pose (neutral rotation)."""
    import bpy
    for bone in armature.pose.bones:
        bone.rotation_mode = 'XYZ'
        bone.rotation_euler = (0, 0, 0)
        bone.location = (0, 0, 0)
        bone.scale = (1, 1, 1)


def apply_pose(armature, pose_data, frame, lock_root_location=True, ground_offset=0.0, is_first_pose=False):
    """
    Apply a pose to armature at specified frame.

    Args:
        armature: Blender armature object
        pose_data: Dict of {bone_name: {pitch, yaw, roll}}
        frame: Frame number for keyframe
        lock_root_location: If True, keyframe armature location at (0,0,0)
        is_first_pose: If True, keyframe ALL bones (first pose establishes base)
    """
    import bpy

    bpy.context.scene.frame_set(frame)

    # Lock armature location to prevent root motion
    # Offset armature vertically to put feet/legs at ground level (z=0)
    if lock_root_location:
        armature.rotation_mode = 'XYZ'
        armature.location = (0, 0, ground_offset)
        armature.keyframe_insert(data_path='location', frame=frame)
        armature.rotation_euler = (0, 0, 0)
        armature.keyframe_insert(data_path='rotation_euler', frame=frame)

    # For first pose, reset all bones to establish base state
    # For subsequent poses, only modify defined bones (others interpolate)
    if is_first_pose:
        reset_pose_to_rest(armature)

    # Apply the pose data to defined bones
    for bone_name, bone_data in pose_data.items():
        if bone_name not in armature.pose.bones:
            print(f"Warning: Bone '{bone_name}' not found in armature, skipping")
            continue

        bone = armature.pose.bones[bone_name]
        bone.rotation_mode = 'XYZ'

        # Convert degrees to radians (pitch=X, yaw=Y, roll=Z)
        pitch = math.radians(bone_data.get('pitch', 0))
        yaw = math.radians(bone_data.get('yaw', 0))
        roll = math.radians(bone_data.get('roll', 0))

        bone.rotation_euler = (pitch, yaw, roll)

        # Apply location offset if specified (for body bounce, etc.)
        if 'location' in bone_data:
            loc = bone_data['location']
            bone.location = (loc[0], loc[1], loc[2])

    # Keyframe strategy:
    # - First pose: keyframe ALL bones to establish base
    # - Subsequent poses: only keyframe DEFINED bones (others interpolate)
    if is_first_pose:
        for bone in armature.pose.bones:
            bone.keyframe_insert(data_path='rotation_euler', frame=frame)
            bone.keyframe_insert(data_path='location', frame=frame)
    else:
        for bone_name in pose_data.keys():
            if bone_name in armature.pose.bones:
                bone = armature.pose.bones[bone_name]
                bone.keyframe_insert(data_path='rotation_euler', frame=frame)
                bone.keyframe_insert(data_path='location', frame=frame)


def apply_timing_curve(action, timing_curve, start_frame, end_frame):
    """
    Apply interpolation mode to FCurves in frame range.

    Args:
        action: Blender action containing FCurves
        timing_curve: String like 'linear', 'ease_in', 'ease_out', etc.
        start_frame: Start of frame range
        end_frame: End of frame range
    """
    # Map timing_curve strings to Blender interpolation settings
    curve_settings = {
        'linear': ('LINEAR', None),
        'ease_in': ('SINE', 'EASE_IN'),
        'ease_out': ('SINE', 'EASE_OUT'),
        'ease_in_out': ('SINE', 'AUTO'),
        'exponential_in': ('EXPO', 'EASE_IN'),
        'exponential_out': ('EXPO', 'EASE_OUT'),
        'constant': ('CONSTANT', None),
    }

    interp, easing = curve_settings.get(timing_curve, ('LINEAR', None))

    for fcurve in get_action_fcurves(action):
        for keyframe in fcurve.keyframe_points:
            # Apply to keyframes in the phase's frame range
            if start_frame <= keyframe.co[0] <= end_frame:
                keyframe.interpolation = interp
                if easing and hasattr(keyframe, 'easing'):
                    keyframe.easing = easing


def create_sine_sampler(layer):
    """Create sine wave sampling function for breathing/sway/bob effects."""
    period_frames = layer.get('period_frames', 60)
    amplitude = layer.get('amplitude', 0.01)  # Already in radians, NO scaling!
    phase_offset = layer.get('phase_offset', 0)

    def sample(frame):
        t = frame / period_frames
        angle = t * 2 * math.pi + phase_offset
        return math.sin(angle) * amplitude

    return sample


def bake_noise_layer(action, layer, duration_frames):
    """
    Bake noise as sparse keyframes with Bezier interpolation.

    Instead of sampling every frame (causes jitter), sample at intervals
    and let Blender interpolate for smooth micro-motion.
    """
    target_bone = layer.get('target')
    axis = layer.get('axis', 'pitch')
    amplitude = layer.get('amplitude', 0.005)
    frequency = layer.get('frequency', 0.3)  # Controls sample density

    axis_map = {'pitch': 0, 'yaw': 1, 'roll': 2}
    axis_index = axis_map.get(axis, 0)

    # Find target FCurve
    target_path = f'pose.bones["{target_bone}"].rotation_euler'
    fcurve = None
    for fc in get_action_fcurves(action):
        if fc.data_path == target_path and fc.array_index == axis_index:
            fcurve = fc
            break

    if fcurve is None:
        print(f"Warning: No FCurve for {target_bone}.{axis}, skipping noise layer")
        return

    # Calculate sample interval (lower frequency = sparser samples = smoother)
    # frequency 0.3 = sample every ~33 frames for smooth motion
    sample_interval = max(15, int(1.0 / frequency * 10))

    # Seed for reproducibility
    seed = hash(target_bone) % 10000
    random.seed(seed)

    # Generate all noise values first (for loop continuity)
    noise_values = []
    for i in range(0, duration_frames + sample_interval, sample_interval):
        noise_values.append((random.random() - 0.5) * 2 * amplitude)

    # Sample at sparse keyframes
    keyframe_count = 0
    for i, frame in enumerate(range(0, duration_frames + 1, sample_interval)):
        if i < len(noise_values):
            existing_value = fcurve.evaluate(frame)
            fcurve.keyframe_points.insert(frame, existing_value + noise_values[i])
            keyframe_count += 1

    # Ensure end frame has keyframe matching start for clean loop
    if duration_frames % sample_interval != 0:
        existing_value = fcurve.evaluate(duration_frames)
        # Use first noise value for loop continuity
        fcurve.keyframe_points.insert(duration_frames, existing_value + noise_values[0])
        keyframe_count += 1

    # BEZIER interpolation for smooth motion between sparse keyframes
    for kf in fcurve.keyframe_points:
        kf.interpolation = 'BEZIER'
        # Blender 5.x uses separate handle_left_type/handle_right_type
        kf.handle_left_type = 'AUTO_CLAMPED'
        kf.handle_right_type = 'AUTO_CLAMPED'

    print(f"  Baked noise on {target_bone}.{axis} ({keyframe_count} sparse keyframes, interval={sample_interval})")


def bake_procedural_layer(action, layer, duration_frames, fps):
    """
    Bake procedural motion into keyframes (replaces FCurve modifier approach).

    Samples procedural function at each frame and combines additively with
    existing keyframes. Ensures clean glTF export without modifiers.

    Args:
        action: Blender action to modify
        layer: Layer specification dict
        duration_frames: Total animation duration
        fps: Frames per second
    """
    layer_type = layer.get('type')

    # Noise uses sparse keyframe sampling for smooth micro-motion
    if layer_type == 'noise':
        bake_noise_layer(action, layer, duration_frames)
        return

    target_bone = layer.get('target')
    axis = layer.get('axis', 'pitch')

    # Map axis to rotation_euler index
    axis_map = {'pitch': 0, 'yaw': 1, 'roll': 2}
    axis_index = axis_map.get(axis, 0)

    # Find the FCurve for this bone's rotation axis
    target_path = f'pose.bones["{target_bone}"].rotation_euler'
    fcurve = None

    for fc in get_action_fcurves(action):
        if fc.data_path == target_path and fc.array_index == axis_index:
            fcurve = fc
            break

    if fcurve is None:
        print(f"Warning: No FCurve for {target_bone}.{axis}, skipping procedural layer")
        return

    # Create sampling function based on layer type (sine-based layers)
    if layer_type in ('breathing', 'sway', 'bob'):
        sample_func = create_sine_sampler(layer)
    else:
        print(f"Warning: Unknown procedural layer type '{layer_type}'")
        return

    # Bake procedural motion into keyframes
    for frame in range(duration_frames + 1):
        procedural_offset = sample_func(frame)
        existing_value = fcurve.evaluate(frame)
        new_value = existing_value + procedural_offset
        fcurve.keyframe_points.insert(frame, new_value, options={'FAST'})

    # Set linear interpolation for smooth playback
    for kf in fcurve.keyframe_points:
        kf.interpolation = 'LINEAR'

    print(f"  Baked {layer_type} on {target_bone}.{axis} ({duration_frames + 1} keyframes)")


# =============================================================================
# PROFESSIONAL DECLARATIVE RIGGING SYSTEM
# =============================================================================
# Generic IK/constraint setup for ANY skeleton. Everything bakes to FK for export.
# Blender does all IK solving - we just create bones and constraints.
# =============================================================================


def setup_ik_chain(armature, chain_spec):
    """
    Set up IK for ANY bone chain. Blender's IK solver does all the math.

    Works with any chain length (2-bone limbs, N-bone tails, single-bone, etc.)
    We just create:
    - Target bone (where the chain reaches toward)
    - Pole bone (optional, gives stable bend direction for 2+ bone chains)
    - IK constraint with chain_count

    Args:
        armature: Blender armature object
        chain_spec: Dict with chain definition:
            {
                "name": "leg_L",
                "bones": ["leg_upper_L", "leg_lower_L"],  # Any length
                "target": {"name": "ik_foot_L", "at": "tip"},
                "pole": {"name": "pole_knee_L", "offset": [0, 0.3, 0]},  # Optional
                "stretch": {"enabled": False, "limit": 1.5},  # Optional
                "rotation_limits": {"pitch": [-45, 45], ...},  # Optional
            }

    Returns:
        Dict with created bone names: {'target': ..., 'pole': ...} or None
    """
    import bpy
    import mathutils

    bones = chain_spec.get('bones', [])
    chain_length = len(bones)

    if chain_length == 0:
        print(f"Warning: Empty bone list for chain '{chain_spec.get('name')}'")
        return None

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    # Validate all chain bones exist
    chain_bones = [edit_bones.get(name) for name in bones]
    missing = [n for n, b in zip(bones, chain_bones) if b is None]
    if missing:
        print(f"Warning: Missing bones {missing} for chain '{chain_spec.get('name')}', skipping")
        bpy.ops.object.mode_set(mode='OBJECT')
        return None

    # --- Create IK target bone ---
    target_spec = chain_spec.get('target', {})
    target_name = target_spec.get('name', f"ik_{chain_spec.get('name', 'chain')}")
    at = target_spec.get('at', 'tip')

    ik_target = edit_bones.new(target_name)
    tip_bone = chain_bones[-1]

    # Position target at tip, head, or custom location
    if at == 'tip':
        ik_target.head = tip_bone.tail.copy()
    elif at == 'head':
        ik_target.head = tip_bone.head.copy()
    elif isinstance(at, (list, tuple)) and len(at) == 3:
        ik_target.head = mathutils.Vector(at)
    else:
        ik_target.head = tip_bone.tail.copy()

    # Tail points FORWARD (+Y) so bone local coords align with world coords
    # This ensures pose_bone.location values map correctly to world space
    ik_target.tail = ik_target.head.copy()
    ik_target.tail.y += 0.05
    ik_target.parent = None  # IK targets are root-level
    ik_target.use_deform = False  # IK controls don't deform mesh

    # --- Create pole target (optional) ---
    pole_spec = chain_spec.get('pole')
    pole_name = None

    if pole_spec:
        pole_name = pole_spec.get('name', f"pole_{chain_spec.get('name', 'chain')}")
        offset = pole_spec.get('offset', [0, 0.3, 0])

        pole = edit_bones.new(pole_name)

        # Position pole relative to chain midpoint
        if pole_spec.get('auto_place', False) and chain_length >= 2:
            # Auto-place in front of the bend (mid bone)
            mid_idx = chain_length // 2
            mid_bone = chain_bones[mid_idx]
            pole.head = mid_bone.head.copy()
        else:
            # Use first bone head as reference
            pole.head = chain_bones[0].head.copy()

        # Apply offset
        pole.head.x += offset[0]
        pole.head.y += offset[1]
        pole.head.z += offset[2]
        pole.tail = pole.head.copy()
        pole.tail.y += 0.1
        pole.parent = None
        pole.use_deform = False  # Pole targets don't deform mesh

    bpy.ops.object.mode_set(mode='POSE')

    # --- Add IK constraint to end bone ---
    pose_tip = armature.pose.bones[bones[-1]]
    ik = pose_tip.constraints.new('IK')
    ik.target = armature
    ik.subtarget = target_name
    ik.chain_count = chain_length

    # Pole (optional)
    if pole_name:
        ik.pole_target = armature
        ik.pole_subtarget = pole_name

        # Calculate pole angle dynamically if 'auto'
        pole_angle = pole_spec.get('angle', 0)
        if pole_angle == 'auto':
            # Get pole bone position
            pole_bone = armature.data.bones[pole_name]
            pole_pos = pole_bone.head_local.copy()
            # Calculate correct angle to preserve rest pose
            pole_angle = calculate_pole_angle(armature, bones[0], bones[-1], pole_pos)
            print(f"    Auto pole angle for {pole_name}: {pole_angle:.4f} rad ({pole_angle * 57.2958:.1f}°)")

        ik.pole_angle = pole_angle

    # Stretch (optional, default OFF for games)
    stretch_spec = chain_spec.get('stretch', {})
    if stretch_spec.get('enabled', False):
        ik.use_stretch = True

    # --- Apply rotation limits (optional) ---
    limits = chain_spec.get('rotation_limits')
    if limits:
        for bone_name in bones:
            add_rotation_limits(armature, bone_name, limits)

    # --- IK/FK Switch (always enabled) ---
    # Create a custom property on the armature to control IK influence
    chain_name = chain_spec.get('name', 'unnamed')
    prop_name = f"IK_{chain_name}"  # e.g., "IK_leg_L"

    # Add custom property (0.0 = FK, 1.0 = IK)
    armature[prop_name] = 1.0  # Default to IK mode

    # Set up property UI hints
    id_props = armature.id_properties_ui(prop_name)
    id_props.update(min=0.0, max=1.0, soft_min=0.0, soft_max=1.0,
                    description=f"IK/FK blend for {chain_name} (0=FK, 1=IK)")

    # Drive the IK constraint influence with this property
    driver = ik.driver_add('influence').driver
    driver.type = 'AVERAGE'
    var = driver.variables.new()
    var.name = 'ik_fk'
    var.type = 'SINGLE_PROP'
    var.targets[0].id_type = 'OBJECT'
    var.targets[0].id = armature
    var.targets[0].data_path = f'["{prop_name}"]'

    print(f"  IK chain '{chain_name}': {chain_length} bones -> {target_name}" +
          (f" (pole: {pole_name})" if pole_name else "") +
          f" [IK/FK: {prop_name}]")

    return {'target': target_name, 'pole': pole_name, 'ikfk_prop': prop_name}


def add_rotation_limits(armature, bone_name, limits):
    """
    Add rotation limits to a bone via Limit Rotation constraint.

    Args:
        armature: Blender armature
        bone_name: Bone to constrain
        limits: Dict with pitch/yaw/roll min/max in degrees:
            {"pitch": [-45, 45], "yaw": [-30, 30], "roll": [-15, 15]}
    """
    import bpy
    import math

    bpy.ops.object.mode_set(mode='POSE')
    pose_bone = armature.pose.bones.get(bone_name)
    if not pose_bone:
        return

    constraint = pose_bone.constraints.new('LIMIT_ROTATION')
    constraint.owner_space = 'LOCAL'

    if 'pitch' in limits:
        constraint.use_limit_x = True
        constraint.min_x = math.radians(limits['pitch'][0])
        constraint.max_x = math.radians(limits['pitch'][1])

    if 'yaw' in limits:
        constraint.use_limit_y = True
        constraint.min_y = math.radians(limits['yaw'][0])
        constraint.max_y = math.radians(limits['yaw'][1])

    if 'roll' in limits:
        constraint.use_limit_z = True
        constraint.min_z = math.radians(limits['roll'][0])
        constraint.max_z = math.radians(limits['roll'][1])


def setup_aim_constraint(armature, aim_spec):
    """
    Set up aim/look-at constraint on a bone.

    Args:
        aim_spec: Dict with aim definition:
            {
                "name": "head_look",
                "bone": "head",
                "target": "look_target",
                "aim_axis": "+Y",
                "up_axis": "+Z",
                "clamp": {"pitch": [-60, 80], "yaw": [-90, 90]}
            }
    """
    import bpy

    bone_name = aim_spec.get('bone')
    target_name = aim_spec.get('target')

    if not bone_name or not target_name:
        return None

    bpy.ops.object.mode_set(mode='POSE')
    pose_bone = armature.pose.bones.get(bone_name)
    if not pose_bone:
        print(f"Warning: Bone '{bone_name}' not found for aim constraint")
        return None

    # Check if target exists
    if target_name not in armature.pose.bones:
        # Create target bone if it doesn't exist
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones
        source = edit_bones.get(bone_name)
        if source:
            target = edit_bones.new(target_name)
            target.head = source.head.copy()
            target.head.y += 1.0  # In front of bone
            target.tail = target.head.copy()
            target.tail.y += 0.1
            target.parent = None
        bpy.ops.object.mode_set(mode='POSE')
        pose_bone = armature.pose.bones.get(bone_name)

    # Add damped track constraint
    constraint = pose_bone.constraints.new('DAMPED_TRACK')
    constraint.target = armature
    constraint.subtarget = target_name

    # Map axis string to Blender enum
    axis_map = {
        '+X': 'TRACK_X', '-X': 'TRACK_NEGATIVE_X',
        '+Y': 'TRACK_Y', '-Y': 'TRACK_NEGATIVE_Y',
        '+Z': 'TRACK_Z', '-Z': 'TRACK_NEGATIVE_Z',
    }
    aim_axis = aim_spec.get('aim_axis', '+Y')
    constraint.track_axis = axis_map.get(aim_axis, 'TRACK_Y')

    # Add rotation limits for clamping
    clamp = aim_spec.get('clamp', {})
    if clamp:
        add_rotation_limits(armature, bone_name, clamp)

    print(f"  Aim constraint '{aim_spec.get('name')}': {bone_name} -> {target_name}")
    return {'bone': bone_name, 'target': target_name}


def apply_constraint_preset(armature, constraint_spec):
    """
    Apply intent-based constraint (hinge, ball, planar).

    Args:
        constraint_spec: Dict with constraint definition:
            {"bone": "arm_lower_L", "type": "hinge", "axis": "X", "limits": [0, 145]}
            {"bone": "arm_upper_L", "type": "ball", "limits": {"pitch": [-90, 180], ...}}
    """
    import bpy
    import math

    ctype = constraint_spec.get('type')
    bone_name = constraint_spec.get('bone')

    if not bone_name:
        return

    bpy.ops.object.mode_set(mode='POSE')
    pose_bone = armature.pose.bones.get(bone_name)
    if not pose_bone:
        print(f"Warning: Bone '{bone_name}' not found for constraint")
        return

    if ctype == 'hinge':
        # Single-axis rotation (elbows, knees)
        axis = constraint_spec.get('axis', 'X')
        limits = constraint_spec.get('limits', [0, 160])

        constraint = pose_bone.constraints.new('LIMIT_ROTATION')
        constraint.owner_space = 'LOCAL'

        # Lock all axes except the hinge axis
        constraint.use_limit_x = True
        constraint.use_limit_y = True
        constraint.use_limit_z = True
        constraint.min_x = 0
        constraint.max_x = 0
        constraint.min_y = 0
        constraint.max_y = 0
        constraint.min_z = 0
        constraint.max_z = 0

        # Set the hinge axis range
        if axis.upper() == 'X':
            constraint.min_x = math.radians(limits[0])
            constraint.max_x = math.radians(limits[1])
        elif axis.upper() == 'Y':
            constraint.min_y = math.radians(limits[0])
            constraint.max_y = math.radians(limits[1])
        elif axis.upper() == 'Z':
            constraint.min_z = math.radians(limits[0])
            constraint.max_z = math.radians(limits[1])

    elif ctype == 'ball':
        # Multi-axis clamped rotation (shoulders, hips)
        limits = constraint_spec.get('limits', {})
        add_rotation_limits(armature, bone_name, limits)

    elif ctype == 'planar':
        # Constrain to a plane (not commonly needed, but available)
        limits = constraint_spec.get('limits', [0, 160])
        # For planar, we lock one rotation axis completely
        constraint = pose_bone.constraints.new('LIMIT_ROTATION')
        constraint.owner_space = 'LOCAL'
        normal = constraint_spec.get('plane_normal', [1, 0, 0])

        # Lock the axis perpendicular to the plane
        if normal[0] != 0:
            constraint.use_limit_x = True
            constraint.min_x = 0
            constraint.max_x = 0
        if normal[1] != 0:
            constraint.use_limit_y = True
            constraint.min_y = 0
            constraint.max_y = 0
        if normal[2] != 0:
            constraint.use_limit_z = True
            constraint.min_z = 0
            constraint.max_z = 0

    elif ctype == 'soft':
        # Soft limit - spring-like resistance to rest pose
        # Uses Copy Rotation with influence < 1 to blend toward rest
        stiffness = constraint_spec.get('stiffness', 0.5)
        rest_pose = constraint_spec.get('rest_pose', {'pitch': 0, 'yaw': 0, 'roll': 0})

        # Store rest pose rotation
        pose_bone.rotation_mode = 'XYZ'
        pose_bone.rotation_euler = (
            math.radians(rest_pose.get('pitch', 0)),
            math.radians(rest_pose.get('yaw', 0)),
            math.radians(rest_pose.get('roll', 0))
        )

        # Add damped track to rest - influence controls stiffness
        # Higher stiffness = stronger pull to rest pose
        constraint = pose_bone.constraints.new('COPY_ROTATION')
        constraint.target = armature
        constraint.subtarget = pose_bone.name
        constraint.influence = stiffness
        constraint.mix_mode = 'ADD'
        constraint.owner_space = 'LOCAL'
        constraint.target_space = 'LOCAL'

    print(f"  Constraint '{ctype}' on {bone_name}")


# =============================================================================
# HINGE JOINT CALIBRATION
# =============================================================================

def calibrate_hinge_joints(armature, rig_setup):
    """
    Calibrate hinge joints to determine flexion axis and sign from rest geometry.

    For each hinge joint (parent -> child), determines:
    - Which local axis (X or Z) is the flexion axis
    - Whether positive or negative rotation represents flexion

    Args:
        armature: Blender armature object
        rig_setup: Rig setup dict containing constraints and ik_chains

    Returns:
        Dict mapping bone_name to calibration info:
        {
            "leg_lower_L": {
                "axis": "X",
                "flexion_sign": "+",
                "range_deg": [0, 160],
                "parent": "leg_upper_L",
                "calibrated": True,
                "method": "geometry"
            }
        }
    """
    import bpy
    from mathutils import Vector

    if not rig_setup:
        return {}

    calibration = {}

    # Collect hinge bones from explicit constraints
    hinge_bones = {}
    for c in rig_setup.get('constraints', []):
        if c.get('type') == 'hinge':
            bone_name = c.get('bone')
            if bone_name:
                hinge_bones[bone_name] = {
                    'declared_axis': c.get('axis', 'X'),
                    'limits': c.get('limits', [0, 160])
                }

    # Infer hinges from IK chains (middle bones are typically hinges)
    for chain in rig_setup.get('ik_chains', []):
        bones = chain.get('bones', [])
        if len(bones) >= 2:
            # All bones except tip are potential hinges
            # For spine/tail chains (3+ bones), use wider limits to allow natural sway
            is_spine_chain = len(bones) >= 3
            chain_limits = [-45, 160] if is_spine_chain else [0, 160]
            for bone_name in bones[:-1]:
                if bone_name not in hinge_bones:
                    hinge_bones[bone_name] = {
                        'declared_axis': None,
                        'limits': chain_limits
                    }

    # Infer from presets
    # Anatomical limits: knees can hyperextend ~10°, so [-10, 160] not [0, 160]
    presets = rig_setup.get('presets', {})
    if presets.get('humanoid_legs'):
        for side in ['L', 'R']:
            lower = f'leg_lower_{side}'
            if lower not in hinge_bones:
                hinge_bones[lower] = {'declared_axis': 'X', 'limits': [-10, 160]}
    if presets.get('humanoid_arms'):
        for side in ['L', 'R']:
            lower = f'arm_lower_{side}'
            if lower not in hinge_bones:
                # Elbows can hyperextend ~5-10° in some people
                hinge_bones[lower] = {'declared_axis': 'X', 'limits': [-10, 145]}
    if presets.get('spider_legs'):
        # Spider legs should NOT hyperextend - limits [-3, 140]
        # -3° tolerance accounts for IK solver precision
        # Anything beyond -3° is a real bug (leg bending wrong way)
        positions = ['front', 'mid_front', 'mid_back', 'back']
        for pos in positions:
            for side in ['L', 'R']:
                lower = f'leg_{pos}_lower_{side}'
                if lower not in hinge_bones:
                    hinge_bones[lower] = {'declared_axis': 'X', 'limits': [-3, 140]}
    if presets.get('quadruped_legs'):
        # Quadruped legs should NOT hyperextend - limits [-3, 140]
        # -3° tolerance accounts for IK solver precision
        for pos in ['front', 'back']:
            for side in ['L', 'R']:
                lower = f'leg_{pos}_lower_{side}'
                if lower not in hinge_bones:
                    hinge_bones[lower] = {'declared_axis': 'X', 'limits': [-3, 140]}

    if not hinge_bones:
        return {}

    # Calibrate each hinge bone
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    for bone_name, info in hinge_bones.items():
        bone = edit_bones.get(bone_name)
        if not bone or not bone.parent:
            # Can't calibrate without parent
            if bone_name in hinge_bones:
                calibration[bone_name] = {
                    'axis': info['declared_axis'] or 'X',
                    'flexion_sign': '+',
                    'range_deg': info['limits'],
                    'parent': None,
                    'calibrated': False,
                    'method': 'default',
                    'warning': 'No parent bone for calibration'
                }
            continue

        parent = bone.parent

        # Compute rest pose directions
        p = parent.tail - parent.head  # Parent direction
        c = bone.tail - bone.head      # Child direction

        # Check if rest pose is straight (can't calibrate)
        p_norm = p.normalized()
        c_norm = c.normalized()
        dot = p_norm.dot(c_norm)

        if abs(dot) > 0.98:  # Nearly straight (< ~11.5 degrees bend)
            # Cannot calibrate from geometry - use declared or default
            # NOTE: Character specs should have sufficient knee bend (~12°) for calibration
            # If hitting this code path, consider increasing knee bend in character spec
            if info['declared_axis']:
                calibration[bone_name] = {
                    'axis': info['declared_axis'],
                    'flexion_sign': '+',
                    'range_deg': info['limits'],
                    'parent': parent.name,
                    'calibrated': False,
                    'method': 'declared',
                    'warning': 'Rest pose is straight; using declared axis. Increase knee bend in character spec for proper calibration.'
                }
            else:
                calibration[bone_name] = {
                    'axis': 'X',
                    'flexion_sign': '+',
                    'range_deg': info['limits'],
                    'parent': parent.name,
                    'calibrated': False,
                    'method': 'default',
                    'warning': 'Rest pose is straight; calibration skipped. Increase knee bend in character spec for proper calibration.'
                }
            continue

        # Compute bend normal (perpendicular to both bone directions)
        n = p.cross(c).normalized()

        # Determine which child local axis is closest to bend normal
        bone_matrix = bone.matrix
        local_x = Vector((bone_matrix[0][0], bone_matrix[1][0], bone_matrix[2][0])).normalized()
        local_z = Vector((bone_matrix[0][2], bone_matrix[1][2], bone_matrix[2][2])).normalized()

        dot_x = abs(n.dot(local_x))
        dot_z = abs(n.dot(local_z))

        if dot_x > dot_z:
            axis = 'X'
            axis_vec = local_x
        else:
            axis = 'Z'
            axis_vec = local_z

        # Determine sign: positive rotation should increase flexion (decrease angle)
        # The bend normal points in the direction of flexion
        sign = '+' if n.dot(axis_vec) > 0 else '-'

        # Compute rest pose angle (angle from straight)
        # dot = cos(angle), so angle = arccos(dot)
        # This is the flexion angle in the rest pose
        import math
        rest_angle_rad = math.acos(max(-1, min(1, dot)))  # Clamp to avoid domain errors
        rest_angle_deg = math.degrees(rest_angle_rad)

        # Adjust range based on rest pose:
        # - Range is [min_hyperextension, max_flexion] relative to anatomical straight
        # - Rest pose is at rest_angle_deg flexion
        # - Pose rotations are relative to rest, so:
        #   - 0° pose = rest_angle_deg anatomical flexion
        #   - -rest_angle_deg pose = 0° anatomical (straight)
        #   - -(rest_angle_deg + 10) pose = -10° anatomical (10° hyperextension)
        # Store rest_angle so validation can convert pose angles to anatomical angles
        calibration[bone_name] = {
            'axis': axis,
            'flexion_sign': sign,
            'range_deg': info['limits'],  # Anatomical limits (e.g., [0, 160] for knee)
            'rest_angle_deg': rest_angle_deg,  # Flexion in rest pose
            'parent': parent.name,
            'calibrated': True,
            'method': 'geometry'
        }

    bpy.ops.object.mode_set(mode='OBJECT')
    return calibration


# =============================================================================
# MOTION VALIDATION
# =============================================================================

def validate_motion(armature, calibration, frame_start, frame_end, strict=False):
    """
    Validate baked animation against hinge joint constraints.

    Checks each frame for:
    - Rotation outside declared limits (hyperextension/overflexion)
    - Significant rotation on non-hinge axes

    Args:
        armature: Blender armature with baked animation
        calibration: Output from calibrate_hinge_joints()
        frame_start: First frame to validate
        frame_end: Last frame to validate
        strict: If True, raise exception on violations

    Returns:
        ValidationReport dict with status, hinges, and summary

    Raises:
        AnimationValidationError: If strict=True and violations found
    """
    import bpy
    import math

    report = {
        'version': '2026-01-08',
        'armature': armature.name,
        'status': 'pass',
        'hinges': {},
        'summary': {
            'frames_checked': frame_end - frame_start + 1,
            'total_violations': 0,
            'bones_with_violations': []
        }
    }

    if not calibration:
        return report

    bpy.ops.object.mode_set(mode='POSE')

    for bone_name, cal in calibration.items():
        hinge_report = {
            'axis': cal['axis'],
            'flexion_sign': cal['flexion_sign'],
            'range_deg': cal['range_deg'],
            'rest_angle_deg': round(cal.get('rest_angle_deg', 0), 1),
            'calibrated': cal.get('calibrated', False),
            'violations': []
        }

        pose_bone = armature.pose.bones.get(bone_name)
        if not pose_bone:
            continue

        # Validate ALL joints - calibrated or not
        # For uncalibrated joints, rest_angle defaults to 0 (straight)
        # This still catches gross violations like backward bends

        axis_idx = {'X': 0, 'Y': 1, 'Z': 2}[cal['axis']]
        min_deg, max_deg = cal['range_deg']
        rest_angle = cal.get('rest_angle_deg', 0)  # Rest pose flexion angle

        for frame in range(frame_start, frame_end + 1):
            bpy.context.scene.frame_set(frame)

            # Get rotation on flexion axis (relative to rest pose)
            pose_bone.rotation_mode = 'XYZ'
            angle_rad = pose_bone.rotation_euler[axis_idx]
            pose_angle_deg = math.degrees(angle_rad)

            # Adjust for flexion sign
            if cal['flexion_sign'] == '-':
                pose_angle_deg = -pose_angle_deg

            # Convert to anatomical angle:
            # pose_angle = 0 means at rest pose, which has rest_angle flexion
            # pose_angle > 0 means more flexion than rest
            # pose_angle < 0 means less flexion (extending toward straight or hyperextended)
            # anatomical_angle = rest_angle + pose_angle
            anatomical_angle_deg = rest_angle + pose_angle_deg

            # Check for violations (with 0.5 degree tolerance)
            # Limits are anatomical: [min_hyperextension, max_flexion]
            # Typically [-10, 160] for knee (allowing 10° hyperextension)
            violation = None

            if anatomical_angle_deg < min_deg - 0.5:
                violation = {
                    'frame': frame,
                    'angle': round(anatomical_angle_deg, 1),
                    'type': 'hyperextension',
                    'message': f'frame {frame}: anatomical angle {anatomical_angle_deg:.1f}° < min {min_deg}°'
                }
            elif anatomical_angle_deg > max_deg + 0.5:
                violation = {
                    'frame': frame,
                    'angle': round(anatomical_angle_deg, 1),
                    'type': 'overflexion',
                    'message': f'frame {frame}: anatomical angle {anatomical_angle_deg:.1f}° > max {max_deg}°'
                }

            if violation:
                hinge_report['violations'].append(violation)

        report['hinges'][bone_name] = hinge_report

        if hinge_report['violations']:
            report['summary']['bones_with_violations'].append(bone_name)
            report['summary']['total_violations'] += len(hinge_report['violations'])

    # Determine overall status
    if report['summary']['total_violations'] > 0:
        report['status'] = 'errors'
    elif any(not h.get('calibrated', False) for h in report['hinges'].values()):
        report['status'] = 'warnings'

    # Handle strict mode
    if strict and report['status'] == 'errors':
        violations = []
        for bone_name, hinge in report['hinges'].items():
            for v in hinge['violations']:
                violations.append(f"  {bone_name}: {v['message']}")

        raise AnimationValidationError(
            f"Motion validation failed ({report['summary']['total_violations']} violations):\n" +
            "\n".join(violations[:10]) +
            (f"\n  ... and {len(violations) - 10} more" if len(violations) > 10 else "")
        )

    return report


def write_validation_report(report, output_path):
    """
    Write validation report as JSON.

    Args:
        report: ValidationReport dict from validate_motion()
        output_path: Path for JSON output
    """
    import json
    import os

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"  Validation report: {output_path}")


# =============================================================================
# FOOT ROLL SYSTEM
# =============================================================================

def create_pivot_bone(armature, name, position, parent_bone=None):
    """
    Create a pivot bone at the specified position.

    Args:
        armature: Blender armature
        name: Name for the pivot bone
        position: [x, y, z] local position
        parent_bone: Optional parent bone name

    Returns:
        Name of created bone
    """
    import bpy
    import mathutils

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    pivot = edit_bones.new(name)
    pivot.head = mathutils.Vector(position)
    pivot.tail = pivot.head.copy()
    pivot.tail.z += 0.02  # Small bone for visibility
    pivot.use_deform = False  # Pivot bones don't deform mesh

    if parent_bone and parent_bone in edit_bones:
        pivot.parent = edit_bones[parent_bone]

    bpy.ops.object.mode_set(mode='OBJECT')
    return name


def parent_pivot_chain(armature, pivot_names):
    """
    Create parent hierarchy for pivot bones.

    Args:
        armature: Blender armature
        pivot_names: List of bone names in order [parent, child, grandchild, ...]
    """
    import bpy

    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    for i in range(1, len(pivot_names)):
        child = edit_bones.get(pivot_names[i])
        parent = edit_bones.get(pivot_names[i - 1])
        if child and parent:
            child.parent = parent

    bpy.ops.object.mode_set(mode='OBJECT')


def add_roll_driver(armature, foot_spec):
    """
    Add drivers to connect foot roll attribute to pivot rotations.

    This creates the heel-to-toe roll behavior where:
    - Negative roll rotates heel pivot (heel lift)
    - Positive roll rotates toe pivot (toe lift)
    - Ball pivot handles the transition

    Args:
        armature: Blender armature
        foot_spec: Foot system specification
    """
    import bpy
    import math

    foot_name = foot_spec.get('name', 'foot')
    attrs = foot_spec.get('attributes', {})
    roll_range = attrs.get('roll', {'min': -45, 'max': 90})

    # Get pivot bones
    heel_pivot = f"pivot_heel_{foot_name}"
    toe_pivot = f"pivot_toe_{foot_name}"
    ball_pivot = f"pivot_ball_{foot_name}"

    bpy.ops.object.mode_set(mode='POSE')

    # Create custom property for roll control on the foot control bone
    control_name = foot_spec.get('control', f"ctrl_{foot_name}")
    if control_name in armature.pose.bones:
        ctrl = armature.pose.bones[control_name]
        ctrl['foot_roll'] = 0.0

        # Add driver for heel pivot (activates on negative roll)
        if heel_pivot in armature.pose.bones:
            heel = armature.pose.bones[heel_pivot]
            fcurve = heel.driver_add('rotation_euler', 0)  # X rotation
            driver = fcurve.driver
            driver.type = 'SCRIPTED'

            var = driver.variables.new()
            var.name = 'roll'
            var.type = 'SINGLE_PROP'
            var.targets[0].id = armature
            var.targets[0].data_path = f'pose.bones["{control_name}"]["foot_roll"]'

            # Heel rotates when roll is negative
            driver.expression = f'min(0, roll) * {math.pi/180}'

        # Add driver for toe pivot (activates on positive roll)
        if toe_pivot in armature.pose.bones:
            toe = armature.pose.bones[toe_pivot]
            fcurve = toe.driver_add('rotation_euler', 0)  # X rotation
            driver = fcurve.driver
            driver.type = 'SCRIPTED'

            var = driver.variables.new()
            var.name = 'roll'
            var.type = 'SINGLE_PROP'
            var.targets[0].id = armature
            var.targets[0].data_path = f'pose.bones["{control_name}"]["foot_roll"]'

            # Toe rotates when roll is positive
            driver.expression = f'max(0, roll) * {math.pi/180}'

    print(f"  Foot roll drivers added for {foot_name}")


def setup_foot_roll(armature, foot_spec):
    """
    Set up professional foot roll system with heel/toe/ball pivots.

    Creates a hierarchy of pivot bones that allow natural foot rolling
    from heel strike through toe-off.

    Args:
        foot_spec: Dict with foot system definition:
            {
                "name": "foot_L",
                "control": "ctrl_foot_L",
                "bones": {"foot": "foot_L", "toe": "toe_L"},
                "pivots": {
                    "heel": [0, -0.08, 0],
                    "toe": [0, 0.12, 0],
                    "ball": [0, 0.06, 0],
                },
                "attributes": {"roll": {"min": -45, "max": 90}, ...}
            }

    Returns:
        Dict with created bone names
    """
    import bpy

    foot_name = foot_spec.get('name', 'foot')
    pivots = foot_spec.get('pivots', {})

    # Default pivot positions if not specified
    heel_pos = pivots.get('heel', [0, -0.08, 0])
    toe_pos = pivots.get('toe', [0, 0.12, 0])
    ball_pos = pivots.get('ball', [0, 0.06, 0])

    # Create pivot bones
    heel_pivot = create_pivot_bone(armature, f"pivot_heel_{foot_name}", heel_pos)
    toe_pivot = create_pivot_bone(armature, f"pivot_toe_{foot_name}", toe_pos)
    ball_pivot = create_pivot_bone(armature, f"pivot_ball_{foot_name}", ball_pos)

    # Create hierarchy: heel -> toe -> ball
    # This order allows heel to rotate first, then toe, then ball
    parent_pivot_chain(armature, [heel_pivot, toe_pivot, ball_pivot])

    # Add roll drivers
    add_roll_driver(armature, foot_spec)

    print(f"  Foot roll system '{foot_name}': heel -> toe -> ball pivots")

    return {
        'pivots': [heel_pivot, toe_pivot, ball_pivot],
        'control': foot_spec.get('control'),
    }


# =============================================================================
# TWIST BONES
# =============================================================================

def setup_twist_bone(armature, twist_spec):
    """
    Set up a twist bone that copies partial rotation from a source bone.

    Twist bones help distribute deformation along limbs, preventing
    candy-wrapper effects at shoulders and hips.

    Args:
        twist_spec: Dict with twist bone definition:
            {
                "name": "upperarm_twist_L",
                "source": "arm_upper_L",
                "target": "arm_twist_L",
                "axis": "Y",
                "influence": 0.5,
            }

    Returns:
        Target bone name or None
    """
    import bpy

    source_name = twist_spec.get('source')
    target_name = twist_spec.get('target')
    axis = twist_spec.get('axis', 'Y').upper()
    influence = twist_spec.get('influence', 0.5)

    if not source_name or not target_name:
        return None

    bpy.ops.object.mode_set(mode='POSE')

    source = armature.pose.bones.get(source_name)
    target = armature.pose.bones.get(target_name)

    if not source or not target:
        print(f"Warning: Twist bones not found: source={source_name}, target={target_name}")
        return None

    # Add Copy Rotation constraint for the twist axis only
    constraint = target.constraints.new('COPY_ROTATION')
    constraint.target = armature
    constraint.subtarget = source_name
    constraint.influence = influence
    constraint.owner_space = 'LOCAL'
    constraint.target_space = 'LOCAL'
    constraint.mix_mode = 'REPLACE'

    # Only copy the twist axis
    constraint.use_x = (axis == 'X')
    constraint.use_y = (axis == 'Y')
    constraint.use_z = (axis == 'Z')

    print(f"  Twist bone '{target_name}': {influence*100:.0f}% of {source_name}.{axis}")

    return target_name


def setup_all_twist_bones(armature, twist_bones):
    """
    Set up all twist bones from a list of specifications.

    Args:
        armature: Blender armature
        twist_bones: List of twist bone specs
    """
    for twist_spec in twist_bones:
        setup_twist_bone(armature, twist_spec)


# =============================================================================
# BAKE UTILITIES
# =============================================================================

def clean_fcurves(armature, tolerance=0.001):
    """
    Remove redundant keyframes from animation curves.

    Analyzes each FCurve and removes keyframes that don't significantly
    affect the animation (within tolerance).

    Args:
        armature: Blender armature with animation
        tolerance: Maximum deviation to consider keyframe redundant
    """
    import bpy

    if not armature.animation_data or not armature.animation_data.action:
        return

    action = armature.animation_data.action
    removed_count = 0

    for fcurve in get_action_fcurves(action):
        keyframes = fcurve.keyframe_points
        if len(keyframes) < 3:
            continue

        # Find removable keyframes (those that lie on interpolation line)
        to_remove = []
        for i in range(1, len(keyframes) - 1):
            prev_kf = keyframes[i - 1]
            curr_kf = keyframes[i]
            next_kf = keyframes[i + 1]

            # Calculate interpolated value at current frame
            t = (curr_kf.co[0] - prev_kf.co[0]) / (next_kf.co[0] - prev_kf.co[0])
            interpolated = prev_kf.co[1] + t * (next_kf.co[1] - prev_kf.co[1])

            # If actual value is within tolerance of interpolated, mark for removal
            if abs(curr_kf.co[1] - interpolated) < tolerance:
                to_remove.append(i)

        # Remove keyframes in reverse order to preserve indices
        for i in reversed(to_remove):
            keyframes.remove(keyframes[i])
            removed_count += 1

    if removed_count > 0:
        print(f"  Cleaned {removed_count} redundant keyframes (tolerance={tolerance})")


# =============================================================================
# ANIMATOR-READY RIG FEATURES
# Widget shapes, bone collections, colors for human-friendly .blend files
# =============================================================================

def create_widget_shapes():
    """
    Create reusable custom bone shape mesh objects.
    Returns dict of shape name -> mesh object.

    All shapes are WIREFRAME (edges only, no faces) for clean Rigify-style display.
    Shapes are hidden from render but visible in viewport.
    """
    import bpy
    import bmesh
    from math import pi, sin, cos

    shapes = {}

    # Create a collection to hold widget shapes (hidden)
    widget_collection = bpy.data.collections.get("WGT_Widgets")
    if not widget_collection:
        widget_collection = bpy.data.collections.new("WGT_Widgets")
        bpy.context.scene.collection.children.link(widget_collection)
    widget_collection.hide_viewport = True
    widget_collection.hide_render = True

    # --- Wireframe sphere for IK targets (feet, hands) ---
    # Use latitude/longitude lines instead of filled sphere
    sphere_mesh = bpy.data.meshes.new("WGT_sphere_mesh")
    sphere_obj = bpy.data.objects.new("WGT_sphere", sphere_mesh)
    widget_collection.objects.link(sphere_obj)

    bm = bmesh.new()
    # Create 3 circles: XY, XZ, YZ planes (wireframe sphere)
    segments = 16
    for plane in range(3):
        verts = []
        for i in range(segments):
            angle = 2 * pi * i / segments
            if plane == 0:  # XY plane (horizontal)
                v = bm.verts.new((cos(angle), sin(angle), 0))
            elif plane == 1:  # XZ plane
                v = bm.verts.new((cos(angle), 0, sin(angle)))
            else:  # YZ plane
                v = bm.verts.new((0, cos(angle), sin(angle)))
            verts.append(v)
        bm.verts.ensure_lookup_table()
        for i in range(segments):
            bm.edges.new([verts[i], verts[(i + 1) % segments]])
    bm.to_mesh(sphere_mesh)
    bm.free()
    shapes["sphere"] = sphere_obj

    # --- Wireframe diamond for pole vectors (octahedron edges only) ---
    diamond_mesh = bpy.data.meshes.new("WGT_diamond_mesh")
    diamond_obj = bpy.data.objects.new("WGT_diamond", diamond_mesh)
    widget_collection.objects.link(diamond_obj)

    bm = bmesh.new()
    # Create octahedron vertices
    verts = [
        bm.verts.new((0, 0, 1)),      # top
        bm.verts.new((1, 0, 0)),      # +X
        bm.verts.new((0, 1, 0)),      # +Y
        bm.verts.new((-1, 0, 0)),     # -X
        bm.verts.new((0, -1, 0)),     # -Y
        bm.verts.new((0, 0, -1)),     # bottom
    ]
    bm.verts.ensure_lookup_table()
    # Edges only (wireframe) - top to middle ring
    bm.edges.new([verts[0], verts[1]])
    bm.edges.new([verts[0], verts[2]])
    bm.edges.new([verts[0], verts[3]])
    bm.edges.new([verts[0], verts[4]])
    # Middle ring
    bm.edges.new([verts[1], verts[2]])
    bm.edges.new([verts[2], verts[3]])
    bm.edges.new([verts[3], verts[4]])
    bm.edges.new([verts[4], verts[1]])
    # Bottom to middle ring
    bm.edges.new([verts[5], verts[1]])
    bm.edges.new([verts[5], verts[2]])
    bm.edges.new([verts[5], verts[3]])
    bm.edges.new([verts[5], verts[4]])
    bm.to_mesh(diamond_mesh)
    bm.free()
    shapes["diamond"] = diamond_obj

    # --- Circle for root/COG (flat on ground - XZ plane) ---
    circle_mesh = bpy.data.meshes.new("WGT_circle_mesh")
    circle_obj = bpy.data.objects.new("WGT_circle", circle_mesh)
    widget_collection.objects.link(circle_obj)

    bm = bmesh.new()
    segments = 16
    circle_verts = []
    for i in range(segments):
        angle = 2 * pi * i / segments
        # XZ plane (flat on ground)
        v = bm.verts.new((cos(angle), 0, sin(angle)))
        circle_verts.append(v)
    bm.verts.ensure_lookup_table()
    # Create edges forming the circle
    for i in range(segments):
        bm.edges.new([circle_verts[i], circle_verts[(i + 1) % segments]])
    # Add forward direction indicator (arrow pointing +Y from center)
    center = bm.verts.new((0, 0, 0))
    arrow_tip = bm.verts.new((0, 1.3, 0))
    arrow_left = bm.verts.new((-0.2, 1.0, 0))
    arrow_right = bm.verts.new((0.2, 1.0, 0))
    bm.verts.ensure_lookup_table()
    # Line from center to arrow tip
    bm.edges.new([center, arrow_tip])
    # Arrowhead
    bm.edges.new([arrow_tip, arrow_left])
    bm.edges.new([arrow_tip, arrow_right])
    bm.to_mesh(circle_mesh)
    bm.free()
    shapes["circle"] = circle_obj

    # --- Wireframe pyramid for aim/look targets ---
    pyramid_mesh = bpy.data.meshes.new("WGT_pyramid_mesh")
    pyramid_obj = bpy.data.objects.new("WGT_pyramid", pyramid_mesh)
    widget_collection.objects.link(pyramid_obj)

    bm = bmesh.new()
    # Pyramid pointing forward (+Y)
    verts = [
        bm.verts.new((0, 1.5, 0)),      # tip (forward)
        bm.verts.new((-0.5, 0, 0.5)),   # back top left
        bm.verts.new((0.5, 0, 0.5)),    # back top right
        bm.verts.new((0.5, 0, -0.5)),   # back bottom right
        bm.verts.new((-0.5, 0, -0.5)),  # back bottom left
    ]
    bm.verts.ensure_lookup_table()
    # Edges only (wireframe)
    bm.edges.new([verts[0], verts[1]])
    bm.edges.new([verts[0], verts[2]])
    bm.edges.new([verts[0], verts[3]])
    bm.edges.new([verts[0], verts[4]])
    # Base edges
    bm.edges.new([verts[1], verts[2]])
    bm.edges.new([verts[2], verts[3]])
    bm.edges.new([verts[3], verts[4]])
    bm.edges.new([verts[4], verts[1]])
    bm.to_mesh(pyramid_mesh)
    bm.free()
    shapes["pyramid"] = pyramid_obj

    # --- Wireframe cube for FK controls ---
    cube_mesh = bpy.data.meshes.new("WGT_cube_mesh")
    cube_obj = bpy.data.objects.new("WGT_cube", cube_mesh)
    widget_collection.objects.link(cube_obj)

    bm = bmesh.new()
    # Create cube vertices
    s = 0.5
    cube_verts = [
        bm.verts.new((-s, -s, -s)),
        bm.verts.new((s, -s, -s)),
        bm.verts.new((s, s, -s)),
        bm.verts.new((-s, s, -s)),
        bm.verts.new((-s, -s, s)),
        bm.verts.new((s, -s, s)),
        bm.verts.new((s, s, s)),
        bm.verts.new((-s, s, s)),
    ]
    bm.verts.ensure_lookup_table()
    # Bottom edges
    bm.edges.new([cube_verts[0], cube_verts[1]])
    bm.edges.new([cube_verts[1], cube_verts[2]])
    bm.edges.new([cube_verts[2], cube_verts[3]])
    bm.edges.new([cube_verts[3], cube_verts[0]])
    # Top edges
    bm.edges.new([cube_verts[4], cube_verts[5]])
    bm.edges.new([cube_verts[5], cube_verts[6]])
    bm.edges.new([cube_verts[6], cube_verts[7]])
    bm.edges.new([cube_verts[7], cube_verts[4]])
    # Vertical edges
    bm.edges.new([cube_verts[0], cube_verts[4]])
    bm.edges.new([cube_verts[1], cube_verts[5]])
    bm.edges.new([cube_verts[2], cube_verts[6]])
    bm.edges.new([cube_verts[3], cube_verts[7]])
    bm.to_mesh(cube_mesh)
    bm.free()
    shapes["cube"] = cube_obj

    return shapes


def organize_bone_collections(armature, rig_setup):
    """
    Organize armature bones into collections for easy show/hide.

    Collections:
    - IK Controls: IK targets (ik_foot_*, ik_hand_*, ik_tail_*, etc.)
    - Poles: Pole vectors (pole_*)
    - Mechanism: Pivots, look targets, helpers (pivot_*, look_target, *_twist_*)
    - Deform: All bones with use_deform=True
    """
    import bpy

    armature_data = armature.data

    # Create collections
    collection_names = ["IK Controls", "Poles", "Mechanism", "Deform"]
    collections = {}

    for name in collection_names:
        coll = armature_data.collections.get(name)
        if not coll:
            coll = armature_data.collections.new(name)
        collections[name] = coll

    # Categorize bones
    ik_targets = []
    poles = []
    mechanism = []
    deform = []

    for bone in armature_data.bones:
        bone_name = bone.name

        # IK targets: ik_*
        if bone_name.startswith('ik_'):
            ik_targets.append(bone_name)
        # Poles: pole_*
        elif bone_name.startswith('pole_'):
            poles.append(bone_name)
        # Mechanism: pivot_*, look_target, twist bones
        elif (bone_name.startswith('pivot_') or
              bone_name == 'look_target' or
              '_twist_' in bone_name):
            mechanism.append(bone_name)
        # Deform: bones that deform mesh
        elif bone.use_deform:
            deform.append(bone_name)

    # Assign bones to collections
    for bone_name in ik_targets:
        bone = armature_data.bones.get(bone_name)
        if bone:
            collections["IK Controls"].assign(bone)

    for bone_name in poles:
        bone = armature_data.bones.get(bone_name)
        if bone:
            collections["Poles"].assign(bone)

    for bone_name in mechanism:
        bone = armature_data.bones.get(bone_name)
        if bone:
            collections["Mechanism"].assign(bone)

    for bone_name in deform:
        bone = armature_data.bones.get(bone_name)
        if bone:
            collections["Deform"].assign(bone)

    # Set default visibility
    collections["IK Controls"].is_visible = True
    collections["Poles"].is_visible = True
    collections["Mechanism"].is_visible = False  # Hidden by default
    collections["Deform"].is_visible = True

    print(f"  Bone collections: {len(ik_targets)} IK, {len(poles)} poles, "
          f"{len(mechanism)} mechanism, {len(deform)} deform")


def apply_bone_colors(armature, rig_setup):
    """
    Color-code bones by function and laterality (Rigify convention).

    Colors:
    - IK targets: Red (left) / Blue (right) / Yellow (center)
    - Poles: Darker red/blue
    - Deform: Green
    - Mechanism: Gray
    """
    import bpy

    # Ensure pose mode
    bpy.ops.object.mode_set(mode='POSE')

    # Color definitions (normal, select, active)
    colors = {
        'ik_left': ((0.8, 0.2, 0.2), (1.0, 0.5, 0.5), (1.0, 0.6, 0.6)),
        'ik_right': ((0.2, 0.2, 0.8), (0.5, 0.5, 1.0), (0.6, 0.6, 1.0)),
        'ik_center': ((0.8, 0.8, 0.2), (1.0, 1.0, 0.5), (1.0, 1.0, 0.6)),
        'pole_left': ((0.6, 0.1, 0.1), (0.9, 0.4, 0.4), (0.95, 0.5, 0.5)),
        'pole_right': ((0.1, 0.1, 0.6), (0.4, 0.4, 0.9), (0.5, 0.5, 0.95)),
        'pole_center': ((0.5, 0.5, 0.5), (0.7, 0.7, 0.7), (0.8, 0.8, 0.8)),
        'deform': ((0.35, 0.35, 0.35), (0.5, 0.5, 0.5), (0.6, 0.6, 0.6)),  # Neutral gray, not distracting
        'mechanism': ((0.5, 0.5, 0.5), (0.7, 0.7, 0.7), (0.8, 0.8, 0.8)),
    }

    def get_side(bone_name):
        """Determine if bone is left, right, or center."""
        if bone_name.endswith('_L') or '_L_' in bone_name:
            return 'left'
        elif bone_name.endswith('_R') or '_R_' in bone_name:
            return 'right'
        else:
            return 'center'

    def set_bone_color(pose_bone, color_key):
        """Apply color preset to pose bone."""
        if color_key not in colors:
            return
        normal, select, active = colors[color_key]

        pose_bone.color.palette = 'CUSTOM'
        pose_bone.color.custom.normal = normal
        pose_bone.color.custom.select = select
        pose_bone.color.custom.active = active

    colored_count = 0

    for pose_bone in armature.pose.bones:
        bone_name = pose_bone.name
        side = get_side(bone_name)

        # IK targets
        if bone_name.startswith('ik_'):
            set_bone_color(pose_bone, f'ik_{side}')
            colored_count += 1
        # Poles
        elif bone_name.startswith('pole_'):
            set_bone_color(pose_bone, f'pole_{side}')
            colored_count += 1
        # Mechanism (pivots, look targets, twist)
        elif (bone_name.startswith('pivot_') or
              bone_name == 'look_target' or
              '_twist_' in bone_name):
            set_bone_color(pose_bone, 'mechanism')
            colored_count += 1
        # Deform bones - leave as default theme color (don't apply custom color)

    print(f"  Applied colors to {colored_count} bones")


def apply_bone_shapes(armature, rig_setup, widget_shapes):
    """
    Assign custom shapes to control bones for easy selection.
    Deform bones are explicitly cleared to show as octahedral.

    Shapes:
    - IK targets: sphere
    - Poles: diamond
    - Look targets: pyramid
    - Root: circle
    - All other bones: None (octahedral)
    """
    import bpy

    # Ensure pose mode
    bpy.ops.object.mode_set(mode='POSE')

    shaped_count = 0
    cleared_count = 0

    for pose_bone in armature.pose.bones:
        bone_name = pose_bone.name
        shape = None
        scale = 1.0

        # IK targets get wireframe spheres (smaller scale for clean display)
        if bone_name.startswith('ik_'):
            shape = widget_shapes.get("sphere")
            scale = 0.03
        # Poles get wireframe diamonds
        elif bone_name.startswith('pole_'):
            shape = widget_shapes.get("diamond")
            scale = 0.025
        # Look targets get wireframe pyramids
        elif bone_name == 'look_target':
            shape = widget_shapes.get("pyramid")
            scale = 0.04
        # Root gets flat circle (on XZ ground plane)
        elif bone_name == 'root':
            shape = widget_shapes.get("circle")
            scale = 0.1

        # Apply shape to control bones, clear shape from all others
        if shape:
            pose_bone.custom_shape = shape
            pose_bone.use_custom_shape_bone_size = False
            pose_bone.custom_shape_scale_xyz = (scale, scale, scale)
            shaped_count += 1
        else:
            # Explicitly clear custom shape so deform bones show as octahedral
            if pose_bone.custom_shape is not None:
                pose_bone.custom_shape = None
                cleared_count += 1

    print(f"  Applied custom shapes to {shaped_count} control bones, cleared {cleared_count} (deform bones = octahedral)")


def configure_armature_display(armature, display_type='OCTAHEDRAL'):
    """
    Configure armature viewport display for animation work.

    Settings:
    - display_type: OCTAHEDRAL, STICK, BBONE, ENVELOPE, WIRE
    - show_in_front: Armature always visible through mesh
    - show_names: Hide bone names for cleaner view
    """
    import bpy

    armature.data.display_type = display_type
    armature.show_in_front = True
    armature.data.show_names = False
    armature.data.show_axes = False

    print(f"  Armature display: {display_type}, show_in_front=True")


def setup_animator_rig(armature, rig_setup, animator_config=None):
    """
    Set up animator-friendly rig with collections, colors, shapes.

    Called before save_blend to make .blend files ready for human animation.

    Args:
        armature: Blender armature object
        rig_setup: Rig setup dict from spec
        animator_config: Optional dict to enable/disable features:
            {
                "collections": True,    # Organize into bone collections
                "shapes": True,         # Add custom bone shapes
                "colors": True,         # Color-code bones
                "display": "OCTAHEDRAL" # Armature display type
            }
            Default: All features enabled
    """
    import bpy

    # Default config: everything enabled
    config = {
        "collections": True,
        "shapes": True,
        "colors": True,
        "display": "OCTAHEDRAL"
    }

    # Override with user config if provided
    if animator_config:
        config.update(animator_config)

    print("Setting up animator-friendly rig...")

    # Ensure we're in object mode first
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Select armature
    bpy.context.view_layer.objects.active = armature

    # 1. Create widget shapes (only if shapes enabled)
    widget_shapes = {}
    if config.get("shapes", True):
        widget_shapes = create_widget_shapes()

    # 2. Organize bones into collections
    if config.get("collections", True):
        organize_bone_collections(armature, rig_setup)

    # 3. Apply bone colors
    if config.get("colors", True):
        apply_bone_colors(armature, rig_setup)

    # 4. Apply custom shapes
    if config.get("shapes", True):
        apply_bone_shapes(armature, rig_setup, widget_shapes)

    # 5. Configure armature display
    display_type = config.get("display", "OCTAHEDRAL")
    if display_type:
        configure_armature_display(armature, display_type)

    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    print("Animator rig setup complete")


def bake_rig_to_fk(armature, rig_setup, frame_start, frame_end):
    """
    Bake all IK/constraints to FK keyframes with configurable settings.

    Args:
        armature: Blender armature
        rig_setup: Rig setup dict (may contain 'bake' settings)
        frame_start: First frame to bake
        frame_end: Last frame to bake
    """
    import bpy

    bake_settings = rig_setup.get('bake', {}) if rig_setup else {}

    frame_step = bake_settings.get('frame_step', 1)
    do_clean = bake_settings.get('clean_curves', True)
    remove_ik = bake_settings.get('remove_ik_bones', True)
    remove_constraints = bake_settings.get('remove_constraints', True)
    tolerance = bake_settings.get('tolerance', 0.001)

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')

    # Bake with visual keying (captures IK result as FK rotations)
    bpy.ops.nla.bake(
        frame_start=frame_start,
        frame_end=frame_end,
        step=frame_step,
        only_selected=True,
        visual_keying=True,
        clear_constraints=remove_constraints,
        bake_types={'POSE'}
    )

    # Clean redundant keyframes
    if do_clean:
        clean_fcurves(armature, tolerance)

    # Remove IK control bones
    if remove_ik:
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones
        removed_bones = []
        for bone_name in list(edit_bones.keys()):
            if (bone_name.startswith('ik_') or
                bone_name.startswith('pole_') or
                bone_name.startswith('pivot_') or
                bone_name.startswith('look_')):
                edit_bones.remove(edit_bones[bone_name])
                removed_bones.append(bone_name)
        bpy.ops.object.mode_set(mode='OBJECT')

        if removed_bones:
            print(f"  Removed {len(removed_bones)} control bones")

    print(f"  Baked rig to FK: frames {frame_start}-{frame_end} (step={frame_step})")


# =============================================================================
# IK PRESETS (Expand convenience shortcuts to full chain definitions)
# =============================================================================

def get_chain_between(edit_bones, end_bone_name, start_bone_name):
    """
    Get all bones in the hierarchy from end_bone up to and including start_bone.
    Returns list from start to end (parent to child order).
    """
    chain = []
    current = edit_bones.get(end_bone_name)
    start = edit_bones.get(start_bone_name)

    if not current or not start:
        return []

    # Walk up from end to start
    while current:
        chain.append(current.name)
        if current == start:
            break
        current = current.parent
        # Safety: prevent infinite loop
        if len(chain) > 20:
            break

    if start.name not in chain:
        # start_bone wasn't found in hierarchy
        return []

    # Reverse to get parent-to-child order
    chain.reverse()
    return chain


def calculate_pole_angle(armature, base_bone_name, tip_bone_name, pole_location):
    """
    Calculate the correct pole angle to preserve rest pose.

    The pole angle rotates the IK solution around the chain axis. This function
    calculates the angle needed so that adding the IK constraint doesn't move
    the bones from their rest pose.

    Based on: https://github.com/MystixCode/IKPoleAngles

    Args:
        armature: Blender armature object
        base_bone_name: Name of the first bone in IK chain (e.g., 'leg_upper_L')
        tip_bone_name: Name of the last bone in IK chain (e.g., 'leg_lower_L')
        pole_location: Vector position of the pole target in armature space

    Returns:
        Pole angle in radians
    """
    from mathutils import Vector

    def signed_angle(vector_u, vector_v, normal):
        """Calculate signed angle between two vectors around a normal axis."""
        # Handle zero-length vectors
        if vector_u.length < 0.0001 or vector_v.length < 0.0001:
            return 0.0

        angle = vector_u.angle(vector_v)

        # Determine sign based on cross product alignment with normal
        cross = vector_u.cross(vector_v)
        if cross.length > 0.0001 and cross.angle(normal) < 1.0:
            angle = -angle

        return angle

    # Get bone data (use data.bones for rest pose, not pose.bones)
    base_bone = armature.data.bones[base_bone_name]
    tip_bone = armature.data.bones[tip_bone_name]

    # Chain direction (from base head to tip tail) in local/armature space
    chain_vec = tip_bone.tail_local - base_bone.head_local

    # Pole direction (from base head to pole position)
    pole_vec = pole_location - base_bone.head_local

    # Handle edge case: pole on chain axis
    if chain_vec.cross(pole_vec).length < 0.0001:
        print(f"  Warning: Pole is on chain axis for {base_bone_name}, using 0 angle")
        return 0.0

    # Calculate pole normal (perpendicular to the plane containing chain and pole)
    pole_normal = chain_vec.cross(pole_vec)

    # Project pole direction onto plane perpendicular to chain
    projected_pole_axis = pole_normal.cross(chain_vec)

    # Get signed angle from base bone's X-axis to the projected pole axis
    # This is the rotation needed around the chain axis
    angle = signed_angle(base_bone.x_axis, projected_pole_axis, chain_vec)

    return angle


def expand_ik_presets(presets, armature):
    """
    Expand preset shortcuts to full IK chain definitions.

    Automatically detects intermediate bones (like twist bones) between
    the specified endpoints and includes them in the chain.

    Args:
        presets: Dict like {"humanoid_legs": True, "spider_legs": True}
        armature: Blender armature (to check which bones exist)

    Returns:
        List of expanded ik_chain definitions
    """
    import bpy

    chains = []

    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones
    bone_names = set(edit_bones.keys())

    if presets.get('humanoid_legs'):
        # Standard humanoid leg IK - chain is upper->lower, IK target at ankle
        # IK constraint goes on LAST bone in list, so order: [upper, lower]
        # Foot and toe are FK children (rotate independently for ground contact)
        for side in ['L', 'R']:
            upper = f'leg_upper_{side}'
            lower = f'leg_lower_{side}'
            foot = f'foot_{side}'
            if upper in bone_names and lower in bone_names:
                # IK chain: upper first, lower last (IK constraint goes on lower)
                # Target at 'tip' = lower.tail = ankle position
                chains.append({
                    'name': f'leg_{side}',
                    'bones': [upper, lower],  # IK goes on lower (last), chain_count=2
                    'target': {'name': f'ik_foot_{side}', 'at': 'tip'},  # At ankle (lower.tail)
                    'pole': {
                        'name': f'pole_knee_{side}',
                        'offset': [0, 0.4, 0],  # Forward of knee (+Y)
                        'auto_place': True,
                        'angle': 'auto',  # Calculate dynamically to preserve rest pose
                    },
                })

    if presets.get('humanoid_arms'):
        # Standard humanoid arm IK - chain ends at HAND, not lower arm
        # IK constraint goes on hand_L, chain includes: hand -> arm_lower -> [twist] -> arm_upper
        for side in ['L', 'R']:
            upper = f'arm_upper_{side}'
            lower = f'arm_lower_{side}'
            hand = f'hand_{side}'
            if upper in bone_names and hand in bone_names:
                # Get full chain from hand up to upper arm (includes any twist bones)
                full_chain = get_chain_between(edit_bones, hand, upper)
                if full_chain:
                    chains.append({
                        'name': f'arm_{side}',
                        'bones': full_chain,
                        'target': {'name': f'ik_hand_{side}', 'at': 'tip'},
                        'pole': {
                            'name': f'pole_elbow_{side}',
                            'offset': [0, -0.3, 0],
                            'auto_place': True,
                            'angle': 1.5708,  # +90° in radians - elbows bend backward
                        },
                    })

    if presets.get('spider_legs'):
        # 8 spider legs (expects 2-segment legs: upper + lower)
        leg_positions = ['front', 'mid_front', 'mid_back', 'back']
        for pos in leg_positions:
            for side in ['L', 'R']:
                upper = f'leg_{pos}_upper_{side}'
                lower = f'leg_{pos}_lower_{side}'
                if upper in bone_names and lower in bone_names:
                    # Spider legs spread outward - pole should be outside+above
                    # Use auto_place for correct positioning based on rest pose
                    x_offset = -0.15 if side == 'L' else 0.15  # Outward from body
                    chains.append({
                        'name': f'leg_{pos}_{side}',
                        'bones': [upper, lower],
                        'target': {'name': f'ik_leg_{pos}_{side}', 'at': 'tip'},
                        'pole': {
                            'name': f'pole_{pos}_{side}',
                            'offset': [x_offset, 0, 0.15],  # Outward and up
                            'auto_place': True,
                            'angle': 'auto',
                        },
                    })
                else:
                    # Fallback for single-bone spider legs
                    single = f'leg_{pos}_{side}'
                    if single in bone_names:
                        chains.append({
                            'name': f'leg_{pos}_{side}',
                            'bones': [single],
                            'target': {'name': f'ik_leg_{pos}_{side}', 'at': 'tip'},
                        })

    if presets.get('quadruped_legs'):
        # 4 legs for quadrupeds
        for pos in ['front', 'back']:
            for side in ['L', 'R']:
                upper = f'leg_{pos}_upper_{side}'
                lower = f'leg_{pos}_lower_{side}'
                if upper in bone_names and lower in bone_names:
                    chains.append({
                        'name': f'leg_{pos}_{side}',
                        'bones': [upper, lower],
                        'target': {'name': f'ik_foot_{pos}_{side}', 'at': 'tip'},
                        'pole': {
                            'name': f'pole_{pos}_{side}',
                            'offset': [0, 0.3, 0],
                            'auto_place': True,
                            'angle': 'auto',
                        },
                    })

    if presets.get('basic_spine'):
        # 3-bone spine chain with soft limits
        spine_bones = []
        for name in ['spine_01', 'spine_02', 'spine_03', 'spine', 'spine_1', 'spine_2']:
            if name in bone_names:
                spine_bones.append(name)
        if len(spine_bones) >= 2:
            chains.append({
                'name': 'spine',
                'bones': spine_bones[:3],  # Use up to 3 spine bones
                'target': {'name': 'ik_spine_tip', 'at': 'tip'},
                'rotation_limits': {'pitch': [-30, 30], 'yaw': [-20, 20], 'roll': [-15, 15]},
            })

    bpy.ops.object.mode_set(mode='OBJECT')
    return chains


def expand_foot_presets(presets, armature):
    """
    Expand foot-related presets to foot_systems definitions.

    Args:
        presets: Dict like {"humanoid_legs": True}
        armature: Blender armature

    Returns:
        List of foot_system definitions
    """
    import bpy

    foot_systems = []

    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones
    bone_names = set(edit_bones.keys())
    bpy.ops.object.mode_set(mode='OBJECT')

    if presets.get('humanoid_legs'):
        # Add foot roll for humanoid legs
        for side in ['L', 'R']:
            foot = f'foot_{side}'
            toe = f'toe_{side}'
            if foot in bone_names:
                foot_systems.append({
                    'name': f'foot_{side}',
                    'control': f'ik_foot_{side}',  # Use IK target as control
                    'bones': {
                        'foot': foot,
                        'toe': toe if toe in bone_names else None,
                    },
                    'pivots': {
                        'heel': [0.09 if side == 'R' else -0.09, -0.08, 0],
                        'toe': [0.09 if side == 'R' else -0.09, 0.12, 0],
                        'ball': [0.09 if side == 'R' else -0.09, 0.06, 0],
                    },
                    'attributes': {
                        'roll': {'min': -45, 'max': 90},
                        'bank': {'min': -30, 'max': 30},
                    },
                })

    return foot_systems


def expand_aim_presets(presets, armature):
    """
    Expand aim-related presets to aim_constraints definitions.

    Args:
        presets: Dict like {"head_look": True}
        armature: Blender armature

    Returns:
        List of aim_constraint definitions
    """
    import bpy

    aim_constraints = []

    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones
    bone_names = set(edit_bones.keys())
    bpy.ops.object.mode_set(mode='OBJECT')

    if presets.get('head_look'):
        # Head look-at system
        if 'head' in bone_names:
            aim_constraints.append({
                'name': 'head_look',
                'bone': 'head',
                'target': 'look_target',
                'aim_axis': '+Y',
                'up_axis': '+Z',
                'clamp': {'pitch': [-60, 80], 'yaw': [-90, 90]},
            })

        # Eye look-at (if eyes exist)
        for side in ['L', 'R']:
            eye = f'eye_{side}'
            if eye in bone_names:
                aim_constraints.append({
                    'name': f'eye_{side}_look',
                    'bone': eye,
                    'target': 'look_target',
                    'aim_axis': '+Y',
                    'up_axis': '+Z',
                    'clamp': {'pitch': [-30, 30], 'yaw': [-45, 45]},
                })

    return aim_constraints


def setup_rig_from_spec(armature, rig_setup):
    """
    Set up complete rig from rig_setup specification.

    This is the main entry point for declarative rigging. Handles:
    - IK chains (any length)
    - Presets (expand and set up)
    - Foot roll systems
    - Aim constraints
    - Constraint presets
    - Twist bones

    Args:
        armature: Blender armature
        rig_setup: Dict with rig definition:
            {
                "ik_chains": [...],
                "foot_systems": [...],
                "aim_constraints": [...],
                "constraints": [...],
                "twist_bones": [...],
                "presets": {"humanoid_legs": True, ...},
                "bake": {...},
            }

    Returns:
        Dict with created control bone names and rig_setup reference
    """
    if not rig_setup:
        return {'ik_bones': [], 'uses_ik': False, 'rig_setup': None}

    created = {'ik_bones': [], 'uses_ik': False, 'rig_setup': rig_setup}

    # Get presets
    presets = rig_setup.get('presets', {})

    # --- Expand presets ---
    expanded_chains = expand_ik_presets(presets, armature)
    expanded_foot_systems = expand_foot_presets(presets, armature)
    expanded_aim_constraints = expand_aim_presets(presets, armature)

    # --- Combine explicit definitions with expanded presets ---
    all_chains = list(rig_setup.get('ik_chains', [])) + expanded_chains
    all_foot_systems = list(rig_setup.get('foot_systems', [])) + expanded_foot_systems
    all_aim_constraints = list(rig_setup.get('aim_constraints', [])) + expanded_aim_constraints
    all_twist_bones = list(rig_setup.get('twist_bones', []))

    # --- Set up IK chains ---
    for chain_spec in all_chains:
        result = setup_ik_chain(armature, chain_spec)
        if result:
            created['uses_ik'] = True
            if result.get('target'):
                created['ik_bones'].append(result['target'])
            if result.get('pole'):
                created['ik_bones'].append(result['pole'])

    # --- Set up foot roll systems ---
    for foot_spec in all_foot_systems:
        result = setup_foot_roll(armature, foot_spec)
        if result:
            created['uses_ik'] = True
            for pivot in result.get('pivots', []):
                created['ik_bones'].append(pivot)

    # --- Set up aim constraints ---
    for aim_spec in all_aim_constraints:
        result = setup_aim_constraint(armature, aim_spec)
        if result and result.get('target'):
            created['ik_bones'].append(result['target'])

    # --- Set up twist bones ---
    if all_twist_bones:
        setup_all_twist_bones(armature, all_twist_bones)

    # --- Apply constraints ---
    all_constraints = list(rig_setup.get('constraints', []))
    for constraint_spec in all_constraints:
        apply_constraint_preset(armature, constraint_spec)
    if all_constraints:
        created['constraints'] = all_constraints

    return created


# =============================================================================
# LEGACY IK SUPPORT (for old ik_hints format - will be deprecated)
# =============================================================================

def setup_ik_from_hints(armature, ik_hints):
    """
    Set up IK from legacy ik_hints format.

    DEPRECATED: Use rig_setup instead. This provides backwards compatibility.

    Converts old format to new rig_setup and delegates to setup_rig_from_spec.
    """
    if not ik_hints:
        return False

    # Convert legacy ik_hints to new rig_setup format
    rig_setup = {'ik_chains': [], 'presets': {}}
    mode = ik_hints.get('mode')

    if mode == 'humanoid':
        chains = ik_hints.get('chains', {})
        if chains.get('legs'):
            rig_setup['presets']['humanoid_legs'] = True
        if chains.get('arms'):
            rig_setup['presets']['humanoid_arms'] = True

    elif mode == 'spider':
        # Legacy spider mode - create chains for each specified leg
        legs = ik_hints.get('legs', [])
        for leg_name in legs:
            rig_setup['ik_chains'].append({
                'name': leg_name,
                'bones': [leg_name],  # Single-bone legacy format
                'target': {'name': f'ik_{leg_name}', 'at': 'tip'},
            })

    elif mode == 'quadruped':
        rig_setup['presets']['quadruped_legs'] = True

    result = setup_rig_from_spec(armature, rig_setup)
    return result.get('uses_ik', False)


def keyframe_ik_target(armature, target_name, frame, location):
    """
    Keyframe an IK target at an absolute world-space location.

    Spec files define IK target positions in world space (absolute coordinates).
    Blender's pose bone location is an offset from rest position, so we need
    to convert from absolute to relative.
    """
    import bpy

    bpy.ops.object.mode_set(mode='POSE')
    target = armature.pose.bones.get(target_name)
    if target:
        # Get the bone's rest head position in armature space
        # For root-level bones (no parent), this equals world space
        rest_head = armature.data.bones[target_name].head_local

        # Calculate offset from rest position to desired world position
        offset = (
            location[0] - rest_head.x,
            location[1] - rest_head.y,
            location[2] - rest_head.z
        )

        target.location = offset
        target.keyframe_insert('location', frame=frame)
    else:
        print(f"Warning: IK target '{target_name}' not found for keyframing")


def apply_phase_ik_targets(armature, phase):
    """
    Apply IK target keyframes for a phase.

    Reads ik_targets from phase and keyframes each target's positions.
    Also handles IK/FK blend when specified in keyframes.

    Keyframe format:
        {"frame": 0, "location": [x, y, z]}              # Basic position
        {"frame": 0, "location": [x, y, z], "ikfk": 1.0} # With IK/FK blend (0=FK, 1=IK)
    """
    import bpy

    ik_targets = phase.get('ik_targets')
    if ik_targets:
        for target_name, keyframes in ik_targets.items():
            for kf in keyframes:
                frame = kf['frame']
                location = kf['location']
                keyframe_ik_target(armature, target_name, frame, location)

                # Handle IK/FK blend if specified in keyframe
                if 'ikfk' in kf:
                    # Derive chain name from target name (ik_foot_L -> leg_L)
                    chain_name = _target_to_chain_name(target_name)
                    prop_name = f"IK_{chain_name}"

                    if prop_name in armature:
                        bpy.context.scene.frame_set(frame)
                        armature[prop_name] = kf['ikfk']
                        armature.keyframe_insert(data_path=f'["{prop_name}"]', frame=frame)

    # Also support legacy ikfk_blend format for backwards compatibility
    ikfk_blend = phase.get('ikfk_blend')
    if ikfk_blend:
        for chain_name, keyframes in ikfk_blend.items():
            prop_name = f"IK_{chain_name}"
            if prop_name not in armature:
                print(f"Warning: IK/FK property '{prop_name}' not found on armature")
                continue

            for kf in keyframes:
                frame = kf['frame']
                value = kf['value']
                bpy.context.scene.frame_set(frame)
                armature[prop_name] = value
                armature.keyframe_insert(data_path=f'["{prop_name}"]', frame=frame)


def _target_to_chain_name(target_name):
    """
    Convert IK target name to chain name for IK/FK property lookup.

    Examples:
        ik_foot_L -> leg_L
        ik_foot_R -> leg_R
        ik_hand_L -> arm_L
        ik_hand_R -> arm_R
        ik_tail_tip -> tail
        ik_leg_front_L -> leg_front_L
    """
    # Remove 'ik_' prefix
    if target_name.startswith('ik_'):
        name = target_name[3:]
    else:
        name = target_name

    # Map common foot/hand targets to their chain names
    mappings = {
        'foot_L': 'leg_L',
        'foot_R': 'leg_R',
        'hand_L': 'arm_L',
        'hand_R': 'arm_R',
        'foot_back_L': 'leg_back_L',
        'foot_back_R': 'leg_back_R',
    }

    if name in mappings:
        return mappings[name]

    # For others, strip common suffixes
    if name.endswith('_tip'):
        return name[:-4]  # tail_tip -> tail

    return name


def apply_motion(spec, armature):
    """
    Apply full motion spec to armature, creating action with keyframes.

    Supports both FK poses and IK targets. IK is set up during animation,
    keyframes are applied, then IK is baked to FK before export.

    Args:
        spec: ANIMATION dict from .spec.py file
        armature: Blender armature object

    Returns:
        Created action

    Raises:
        AnimationValidationError: If spec references bones not in armature
    """
    import bpy

    # Validate spec against armature BEFORE any work
    # This catches bone name mismatches early with clear error messages
    validate_against_armature(spec, armature)

    anim = spec['animation']

    # Scene setup
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = anim['duration_frames']
    bpy.context.scene.render.fps = anim.get('fps', 30)

    # Create new action
    action_name = anim['name']
    action = bpy.data.actions.new(action_name)

    # Ensure armature has animation data
    if armature.animation_data is None:
        armature.animation_data_create()
    armature.animation_data.action = action

    # Make armature active
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)

    # Get poses and phases
    poses = anim.get('poses', {})
    phases = anim.get('phases', [])
    is_looping = anim.get('loop', False)
    ground_offset = anim.get('ground_offset', 0.0)

    # Step 1: Set up rig (IK/constraints) before applying any poses
    # New format: rig_setup (preferred)
    # Legacy format: ik_hints (backwards compatible)
    rig_setup = anim.get('rig_setup')
    ik_hints = anim.get('ik_hints', {})

    uses_ik = False
    if rig_setup:
        # New declarative rig format
        result = setup_rig_from_spec(armature, rig_setup)
        uses_ik = result.get('uses_ik', False)
        if uses_ik:
            print(f"Rig setup complete: {len(result.get('ik_bones', []))} control bones")
    elif ik_hints:
        # Legacy format - convert internally
        uses_ik = setup_ik_from_hints(armature, ik_hints)
        if uses_ik:
            print(f"IK setup complete (legacy mode: {ik_hints.get('mode')})")

    # Step 2: Apply each phase (FK poses + IK targets)
    for i, phase in enumerate(phases):
        pose_name = phase.get('pose')

        # Apply FK pose if specified
        if pose_name and pose_name in poses:
            pose_data = poses[pose_name]
            start_frame = phase['frames'][0]

            # First pose establishes base for all bones
            # Subsequent partial poses only keyframe their defined bones
            is_first = (i == 0)
            apply_pose(armature, pose_data, start_frame, ground_offset=ground_offset, is_first_pose=is_first)
        elif pose_name and pose_name not in poses:
            print(f"Warning: Pose '{pose_name}' not found, skipping phase '{phase.get('name')}'")

        # Apply IK targets for this phase
        apply_phase_ik_targets(armature, phase)

    # For looping animations, ensure last frame matches first frame exactly
    if is_looping and phases:
        first_phase = phases[0]
        first_pose_name = first_phase.get('pose')
        if first_pose_name and first_pose_name in poses:
            end_frame = anim['duration_frames']
            # Loop frame should match frame 0 exactly - keyframe ALL bones
            apply_pose(armature, poses[first_pose_name], end_frame, ground_offset=ground_offset, is_first_pose=True)

        # Also ensure IK targets loop correctly
        if 'ik_targets' in first_phase:
            # Keyframe IK targets at end frame with same positions as frame 0
            for target_name, keyframes in first_phase['ik_targets'].items():
                if keyframes:
                    first_kf = keyframes[0]
                    keyframe_ik_target(armature, target_name, end_frame, first_kf['location'])

    # Apply timing curves after all keyframes are set
    for phase in phases:
        timing_curve = phase.get('timing_curve', 'linear')
        start_frame, end_frame = phase['frames']
        apply_timing_curve(action, timing_curve, start_frame, end_frame)

    # Bake procedural layers into keyframes (breathing, sway, noise)
    procedural_layers = anim.get('procedural_layers', [])
    if procedural_layers:
        print(f"Baking {len(procedural_layers)} procedural layers...")
        for layer in procedural_layers:
            bake_procedural_layer(
                action,
                layer,
                anim['duration_frames'],
                anim.get('fps', 30)
            )

    # Step 3: Save .blend BEFORE bake (if requested) so IK rig is visible for debugging
    if anim.get('save_blend', False):
        # Set up animator-friendly rig (collections, colors, shapes)
        # Optional: anim['animator_rig'] can customize which features are enabled
        animator_config = anim.get('animator_rig', None)
        setup_animator_rig(armature, rig_setup, animator_config)

        # Save with IK rig intact for animation work
        blend_path = f"generated/animations/{action_name}.blend"
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print(f"Saved Blender file (animator-ready): {blend_path}")

    # Step 4: Bake IK to FK before export (if IK was used)
    if uses_ik:
        print("Baking IK to FK...")
        bake_rig_to_fk(armature, rig_setup, 0, anim['duration_frames'])

    # Step 5: Calibrate and validate hinge joints (post-bake)
    validation_report = None
    if rig_setup:
        calibration = calibrate_hinge_joints(armature, rig_setup)
        if calibration:
            print(f"Calibrated {len(calibration)} hinge joints")

            # Get strict mode from conventions
            conventions = anim.get('conventions', {})
            strict_mode = conventions.get('strict', False)

            validation_report = validate_motion(
                armature,
                calibration,
                0,
                anim['duration_frames'],
                strict=strict_mode
            )

            # Log summary
            if validation_report['status'] == 'pass':
                print("  Motion validation: PASS")
            elif validation_report['status'] == 'warnings':
                uncalibrated = sum(1 for h in validation_report['hinges'].values() if not h.get('calibrated'))
                print(f"  Motion validation: WARNINGS ({uncalibrated} uncalibrated joints)")
            else:
                violations = validation_report['summary']['total_violations']
                bones = validation_report['summary']['bones_with_violations']
                print(f"  Motion validation: {violations} violations in {bones}")

    print(f"Created action '{action_name}' with {len(phases)} phases")
    return action, validation_report


def export_glb(output_path):
    """Export scene as GLB with animations."""
    import bpy

    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_animations=True,
        export_animation_mode='ACTIONS',
        export_skins=True,
        export_all_influences=False,  # Max 4 bones per vertex (engine-friendly default)
    )
    print(f"Exported to {output_path}")


def generate_animation(spec, output_path, input_glb=None, strict=False):
    """
    Generate animation from spec dict.

    This is the main entry point when called from generate.py.
    For standalone usage, use main() via command line.

    Args:
        spec: ANIMATION dict from .spec.py file
        output_path: Path for output GLB
        input_glb: Optional input armature GLB. If None, uses spec['input_armature']
        strict: If True, fail on validation errors

    Returns:
        validation_report dict or None
    """
    import bpy

    # Get input armature path
    if input_glb is None:
        input_glb = spec.get('animation', spec).get('input_armature')
        if not input_glb:
            raise ValueError("No input_armature specified in spec or arguments")

    # Override strict mode from CLI if specified
    if strict:
        anim = spec.get('animation', spec)
        if 'conventions' not in anim:
            anim['conventions'] = {}
        anim['conventions']['strict'] = True

    # Clear default scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Import the armature
    bpy.ops.import_scene.gltf(filepath=input_glb)

    # Find armature
    armature = find_armature()
    print(f"Found armature: {armature.name}")

    # Apply animation
    action, validation_report = apply_motion(spec, armature)

    # Write validation report if available
    if validation_report:
        report_path = output_path.replace('.glb', '.validation.json')
        write_validation_report(validation_report, report_path)

    # Export GLB
    export_glb(output_path)

    return validation_report


def main():
    """Main entry point for command-line usage."""
    # Parse arguments after '--'
    argv = sys.argv
    if '--' in argv:
        args = argv[argv.index('--') + 1:]
    else:
        print("Usage: blender --background --python animation.py -- "
              "spec.spec.py input.glb output.glb [--strict]")
        sys.exit(1)

    # Parse optional flags
    strict_mode = '--strict' in args
    args = [a for a in args if not a.startswith('--')]

    if len(args) < 3:
        print("Error: Need animation_spec, input_glb, and output_glb paths")
        print("Optional: --strict (fail on validation errors)")
        sys.exit(1)

    spec_path = args[0]
    input_glb = args[1]
    output_glb = args[2]

    print(f"Loading animation spec: {spec_path}")
    print(f"Input armature: {input_glb}")
    print(f"Output: {output_glb}")
    if strict_mode:
        print("Strict mode: ON (will fail on validation errors)")

    # Load spec and generate
    spec = load_spec(spec_path)
    generate_animation(spec, output_glb, input_glb, strict=strict_mode)

    print("Done!")


if __name__ == "__main__":
    main()
