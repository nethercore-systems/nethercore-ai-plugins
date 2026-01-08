# Knight Stomp Animation - Simple IK/FK Switch Demo
# Duration: 45 frames @ 60fps (0.75 seconds)
#
# Purpose: Minimal demonstration of IK/FK switching on ONE leg.
# - Left leg stays planted (IK=1.0) throughout
# - Right leg lifts (IK→FK) then stomps (FK→IK)
#
# IK/FK values: 0.0 = FK (direct bone rotation), 1.0 = IK (foot follows target)

ANIMATION = {
    "animation": {
        "name": "knight_stomp",
        "duration_frames": 45,
        "fps": 60,
        "loop": False,
        "save_blend": True,
        "input_armature": "generated/characters/knight.glb",

        # Validation conventions
        "conventions": {
            "version": "2026-01-08",
            "strict": False,
        },

        "rig_setup": {
            "presets": {
                "humanoid_legs": True,
            },
        },

        "poses": {
            # Neutral standing pose
            "stand": {
                "pelvis": {"pitch": 0, "yaw": 0, "roll": 0, "location": [0, 0, 0]},
                "spine": {"pitch": 0, "yaw": 0, "roll": 0},
                "neck": {"pitch": 0, "yaw": 0, "roll": 0},
                "head": {"pitch": 0, "yaw": 0, "roll": 0},
                "arm_upper_L": {"pitch": 10, "yaw": 5, "roll": -8},
                "arm_lower_L": {"pitch": 15, "yaw": 0, "roll": 0},
                "arm_upper_R": {"pitch": 10, "yaw": -5, "roll": 8},
                "arm_lower_R": {"pitch": 15, "yaw": 0, "roll": 0},
                # Leg FK poses (used when ikfk < 1.0)
                "leg_upper_L": {"pitch": 3, "yaw": -2, "roll": 0},
                "leg_lower_L": {"pitch": 5, "yaw": 0, "roll": 0},
                "foot_L": {"pitch": 0, "yaw": 0, "roll": 0},
                "leg_upper_R": {"pitch": 3, "yaw": 2, "roll": 0},
                "leg_lower_R": {"pitch": 5, "yaw": 0, "roll": 0},
                "foot_R": {"pitch": 0, "yaw": 0, "roll": 0},
            },

            # Right leg raised STRAIGHT UP (not kicking forward)
            "lift": {
                "pelvis": {"pitch": 0, "yaw": 0, "roll": -2, "location": [0.01, 0, 0]},
                "spine": {"pitch": 0, "yaw": 0, "roll": 1},
                "neck": {"pitch": 0, "yaw": 0, "roll": 0},
                "head": {"pitch": 0, "yaw": 0, "roll": 0},
                # Arms: minimal movement for stomp
                "arm_upper_L": {"pitch": 10, "yaw": 5, "roll": -8},
                "arm_lower_L": {"pitch": 15, "yaw": 0, "roll": 0},
                "arm_upper_R": {"pitch": 10, "yaw": -5, "roll": 8},
                "arm_lower_R": {"pitch": 15, "yaw": 0, "roll": 0},
                # Left leg (stays planted - IK controlled)
                "leg_upper_L": {"pitch": 5, "yaw": -2, "roll": 0},
                "leg_lower_L": {"pitch": 8, "yaw": 0, "roll": 0},
                "foot_L": {"pitch": 0, "yaw": 0, "roll": 0},
                # Right leg lifted high (positive pitch = knee flexion)
                "leg_upper_R": {"pitch": 60, "yaw": 0, "roll": 0},
                "leg_lower_R": {"pitch": 90, "yaw": 0, "roll": 0},
                "foot_R": {"pitch": 30, "yaw": 0, "roll": 0},
            },

            # Impact pose - right foot slams down
            "stomp": {
                "pelvis": {"pitch": 8, "yaw": 0, "roll": 0, "location": [0, 0, -0.04]},
                "spine": {"pitch": -5, "yaw": 0, "roll": 0},
                "neck": {"pitch": 3, "yaw": 0, "roll": 0},
                "head": {"pitch": 5, "yaw": 0, "roll": 0},
                # Arms react to impact
                "arm_upper_L": {"pitch": 20, "yaw": 10, "roll": -15},
                "arm_lower_L": {"pitch": 30, "yaw": 0, "roll": 0},
                "arm_upper_R": {"pitch": 20, "yaw": -10, "roll": 15},
                "arm_lower_R": {"pitch": 30, "yaw": 0, "roll": 0},
                # Both legs absorbing impact (positive pitch = knee flexion)
                "leg_upper_L": {"pitch": 25, "yaw": -3, "roll": 0},
                "leg_lower_L": {"pitch": 35, "yaw": 0, "roll": 0},
                "foot_L": {"pitch": 10, "yaw": 0, "roll": 0},
                "leg_upper_R": {"pitch": 25, "yaw": 3, "roll": 0},
                "leg_lower_R": {"pitch": 35, "yaw": 0, "roll": 0},
                "foot_R": {"pitch": 10, "yaw": 0, "roll": 0},
            },

            # Return to standing
            "recover": {
                "pelvis": {"pitch": 0, "yaw": 0, "roll": 0, "location": [0, 0, 0]},
                "spine": {"pitch": 0, "yaw": 0, "roll": 0},
                "neck": {"pitch": 0, "yaw": 0, "roll": 0},
                "head": {"pitch": 0, "yaw": 0, "roll": 0},
                "arm_upper_L": {"pitch": 10, "yaw": 5, "roll": -8},
                "arm_lower_L": {"pitch": 15, "yaw": 0, "roll": 0},
                "arm_upper_R": {"pitch": 10, "yaw": -5, "roll": 8},
                "arm_lower_R": {"pitch": 15, "yaw": 0, "roll": 0},
                "leg_upper_L": {"pitch": 3, "yaw": -2, "roll": 0},
                "leg_lower_L": {"pitch": 5, "yaw": 0, "roll": 0},
                "foot_L": {"pitch": 0, "yaw": 0, "roll": 0},
                "leg_upper_R": {"pitch": 3, "yaw": 2, "roll": 0},
                "leg_lower_R": {"pitch": 5, "yaw": 0, "roll": 0},
                "foot_R": {"pitch": 0, "yaw": 0, "roll": 0},
            },
        },

        "phases": [
            # Phase 1: Lift - Right leg lifts STRAIGHT UP (IK → FK)
            {
                "name": "lift",
                "frames": [0, 15],
                "pose": "lift",
                "timing_curve": "ease_in_out",
                "ik_targets": {
                    # LEFT leg: stays planted throughout (IK=1.0 always)
                    "ik_foot_L": [
                        {"frame": 0, "location": [-0.09, 0, 0], "ikfk": 1.0},
                        {"frame": 15, "location": [-0.09, 0, 0], "ikfk": 1.0},
                    ],
                    # RIGHT leg: lifts straight UP (Y=0 throughout, only Z changes)
                    "ik_foot_R": [
                        {"frame": 0, "location": [0.09, 0, 0], "ikfk": 1.0},      # Planted
                        {"frame": 5, "location": [0.09, 0, 0.02], "ikfk": 0.5},   # Lifting
                        {"frame": 15, "location": [0.09, 0, 0.12], "ikfk": 0.0},  # Up (FK)
                    ],
                },
            },

            # Phase 2: Stomp - Right foot slams STRAIGHT DOWN (FK → IK)
            {
                "name": "stomp",
                "frames": [15, 30],
                "pose": "stomp",
                "timing_curve": "exponential_out",
                "ik_targets": {
                    # LEFT leg: still planted
                    "ik_foot_L": [
                        {"frame": 15, "location": [-0.09, 0, 0], "ikfk": 1.0},
                        {"frame": 30, "location": [-0.09, 0, 0], "ikfk": 1.0},
                    ],
                    # RIGHT leg: comes straight DOWN (Y=0 throughout)
                    "ik_foot_R": [
                        {"frame": 15, "location": [0.09, 0, 0.12], "ikfk": 0.0},  # Up
                        {"frame": 22, "location": [0.09, 0, 0.04], "ikfk": 0.5},  # Descending
                        {"frame": 25, "location": [0.09, 0, 0], "ikfk": 1.0},     # Contact!
                        {"frame": 30, "location": [0.09, 0, 0], "ikfk": 1.0},     # Planted
                    ],
                },
            },

            # Phase 3: Recover - Return to standing (both IK)
            {
                "name": "recover",
                "frames": [30, 45],
                "pose": "recover",
                "timing_curve": "ease_out",
                "ik_targets": {
                    "ik_foot_L": [
                        {"frame": 30, "location": [-0.09, 0, 0], "ikfk": 1.0},
                        {"frame": 45, "location": [-0.09, 0, 0], "ikfk": 1.0},
                    ],
                    "ik_foot_R": [
                        {"frame": 30, "location": [0.09, 0, 0], "ikfk": 1.0},
                        {"frame": 45, "location": [0.09, 0, 0], "ikfk": 1.0},
                    ],
                },
            },
        ],

        "procedural_layers": [],
    }
}
