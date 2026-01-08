# Knight Jump Animation - IK/FK Switch Demo
# Duration: 90 frames @ 60fps (1.5 seconds)
# Demonstrates: IK for ground contact, FK for airborne, smooth transitions
#
# IK/FK values: 0.0 = FK (direct bone rotation), 1.0 = IK (foot follows target)
#
# Phases:
#   1. Crouch (IK=1.0) - feet planted, preparing to jump
#   2. Launch (IK→FK) - push off, blend to airborne
#   3. Air (IK=0.0) - fully airborne, legs controlled by FK poses
#   4. Descend (FK) - preparing for landing
#   5. Land (FK→IK) - feet contact ground, IK takes over
#   6. Recover (IK=1.0) - return to standing

ANIMATION = {
    "animation": {
        "name": "knight_jump",
        "duration_frames": 90,
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
            # Crouch - compressed, ready to spring
            "crouch": {
                "pelvis": {"pitch": 15, "yaw": 0, "roll": 0, "location": [0, 0, -0.08]},
                "spine": {"pitch": -10, "yaw": 0, "roll": 0},
                "neck": {"pitch": 5, "yaw": 0, "roll": 0},
                "head": {"pitch": 10, "yaw": 0, "roll": 0},
                "arm_upper_L": {"pitch": 40, "yaw": 10, "roll": -15},
                "arm_lower_L": {"pitch": 30, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "arm_upper_R": {"pitch": 40, "yaw": -10, "roll": 15},
                "arm_lower_R": {"pitch": 30, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                # FK leg poses (used when ikfk < 1.0)
                "leg_upper_L": {"pitch": 60, "yaw": -5, "roll": 0},
                "leg_lower_L": {"pitch": 90, "yaw": 0, "roll": 0},
                "foot_L": {"pitch": 30, "yaw": 0, "roll": 0},
                "leg_upper_R": {"pitch": 60, "yaw": 5, "roll": 0},
                "leg_lower_R": {"pitch": 90, "yaw": 0, "roll": 0},
                "foot_R": {"pitch": 30, "yaw": 0, "roll": 0},
            },

            # Launch - extending upward, arms swing up for momentum
            "launch": {
                "pelvis": {"pitch": 5, "yaw": 0, "roll": 0, "location": [0, 0, 0.05]},
                "spine": {"pitch": -5, "yaw": 0, "roll": 0},
                "neck": {"pitch": -5, "yaw": 0, "roll": 0},
                "head": {"pitch": 0, "yaw": 0, "roll": 0},
                "arm_upper_L": {"pitch": 70, "yaw": 10, "roll": -15},   # Arms swing UP/forward
                "arm_lower_L": {"pitch": 30, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "arm_upper_R": {"pitch": 70, "yaw": -10, "roll": 15},
                "arm_lower_R": {"pitch": 30, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "leg_upper_L": {"pitch": 10, "yaw": -5, "roll": 0},
                "leg_lower_L": {"pitch": 20, "yaw": 0, "roll": 0},
                "foot_L": {"pitch": 40, "yaw": 0, "roll": 0},
                "leg_upper_R": {"pitch": 10, "yaw": 5, "roll": 0},
                "leg_lower_R": {"pitch": 20, "yaw": 0, "roll": 0},
                "foot_R": {"pitch": 40, "yaw": 0, "roll": 0},
            },

            # Air - peak of jump, arms out for balance
            "air_peak": {
                "pelvis": {"pitch": 0, "yaw": 0, "roll": 0, "location": [0, 0, 0.15]},
                "spine": {"pitch": 0, "yaw": 0, "roll": 0},
                "neck": {"pitch": 0, "yaw": 0, "roll": 0},
                "head": {"pitch": -5, "yaw": 0, "roll": 0},
                "arm_upper_L": {"pitch": 45, "yaw": 40, "roll": -20},   # Arms out to sides, slightly forward
                "arm_lower_L": {"pitch": 20, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "arm_upper_R": {"pitch": 45, "yaw": -40, "roll": 20},
                "arm_lower_R": {"pitch": 20, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "leg_upper_L": {"pitch": 25, "yaw": -8, "roll": 0},
                "leg_lower_L": {"pitch": 40, "yaw": 0, "roll": 0},
                "foot_L": {"pitch": 30, "yaw": 0, "roll": 0},
                "leg_upper_R": {"pitch": 25, "yaw": 8, "roll": 0},
                "leg_lower_R": {"pitch": 40, "yaw": 0, "roll": 0},
                "foot_R": {"pitch": 30, "yaw": 0, "roll": 0},
            },

            # Descend - preparing for landing, arms forward for balance
            "descend": {
                "pelvis": {"pitch": 10, "yaw": 0, "roll": 0, "location": [0, 0, 0.08]},
                "spine": {"pitch": 5, "yaw": 0, "roll": 0},
                "neck": {"pitch": 5, "yaw": 0, "roll": 0},
                "head": {"pitch": 10, "yaw": 0, "roll": 0},
                "arm_upper_L": {"pitch": 30, "yaw": 25, "roll": -15},   # Arms forward for balance
                "arm_lower_L": {"pitch": 25, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "arm_upper_R": {"pitch": 30, "yaw": -25, "roll": 15},
                "arm_lower_R": {"pitch": 25, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "leg_upper_L": {"pitch": 15, "yaw": -5, "roll": 0},
                "leg_lower_L": {"pitch": 25, "yaw": 0, "roll": 0},
                "foot_L": {"pitch": -10, "yaw": 0, "roll": 0},
                "leg_upper_R": {"pitch": 15, "yaw": 5, "roll": 0},
                "leg_lower_R": {"pitch": 25, "yaw": 0, "roll": 0},
                "foot_R": {"pitch": -10, "yaw": 0, "roll": 0},
            },

            # Land - absorbing impact
            "land": {
                "pelvis": {"pitch": 12, "yaw": 0, "roll": 0, "location": [0, 0, -0.05]},
                "spine": {"pitch": -5, "yaw": 0, "roll": 0},
                "neck": {"pitch": 5, "yaw": 0, "roll": 0},
                "head": {"pitch": 8, "yaw": 0, "roll": 0},
                "arm_upper_L": {"pitch": 10, "yaw": 15, "roll": -15},
                "arm_lower_L": {"pitch": 35, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "arm_upper_R": {"pitch": 10, "yaw": -15, "roll": 15},
                "arm_lower_R": {"pitch": 35, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "leg_upper_L": {"pitch": 50, "yaw": -5, "roll": 0},
                "leg_lower_L": {"pitch": 70, "yaw": 0, "roll": 0},
                "foot_L": {"pitch": 20, "yaw": 0, "roll": 0},
                "leg_upper_R": {"pitch": 50, "yaw": 5, "roll": 0},
                "leg_lower_R": {"pitch": 70, "yaw": 0, "roll": 0},
                "foot_R": {"pitch": 20, "yaw": 0, "roll": 0},
            },

            # Recover - returning to stand, neutral pose
            "recover": {
                "pelvis": {"pitch": 0, "yaw": 0, "roll": 0, "location": [0, 0, 0]},
                "spine": {"pitch": 0, "yaw": 0, "roll": 0},
                "neck": {"pitch": 0, "yaw": 0, "roll": 0},
                "head": {"pitch": 0, "yaw": 0, "roll": 0},
                "arm_upper_L": {"pitch": 10, "yaw": 5, "roll": -8},   # Arms slightly forward
                "arm_lower_L": {"pitch": 15, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "arm_upper_R": {"pitch": 10, "yaw": -5, "roll": 8},
                "arm_lower_R": {"pitch": 15, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "leg_upper_L": {"pitch": 3, "yaw": -2, "roll": 0},
                "leg_lower_L": {"pitch": 5, "yaw": 0, "roll": 0},
                "foot_L": {"pitch": 0, "yaw": 0, "roll": 0},
                "leg_upper_R": {"pitch": 3, "yaw": 2, "roll": 0},
                "leg_lower_R": {"pitch": 5, "yaw": 0, "roll": 0},
                "foot_R": {"pitch": 0, "yaw": 0, "roll": 0},
            },
        },

        # IK/FK is now inline with keyframes: "ikfk": 1.0 = full IK, 0.0 = full FK
        "phases": [
            # Phase 1: Crouch (full IK - feet planted)
            {
                "name": "crouch",
                "frames": [0, 15],
                "pose": "crouch",
                "timing_curve": "ease_in",
                "ik_targets": {
                    "ik_foot_L": [
                        {"frame": 0, "location": [-0.09, 0, 0], "ikfk": 1.0},
                        {"frame": 15, "location": [-0.12, -0.05, 0], "ikfk": 1.0},
                    ],
                    "ik_foot_R": [
                        {"frame": 0, "location": [0.09, 0, 0], "ikfk": 1.0},
                        {"frame": 15, "location": [0.12, -0.05, 0], "ikfk": 1.0},
                    ]
                },
            },

            # Phase 2: Launch (IK → FK as feet leave ground)
            {
                "name": "launch",
                "frames": [15, 25],
                "pose": "launch",
                "timing_curve": "exponential_out",
                "ik_targets": {
                    "ik_foot_L": [
                        {"frame": 15, "location": [-0.12, -0.05, 0], "ikfk": 1.0},
                        {"frame": 20, "location": [-0.10, 0, 0.05], "ikfk": 0.5},  # Blending out
                        {"frame": 25, "location": [-0.08, 0.05, 0.10], "ikfk": 0.0}, # Full FK
                    ],
                    "ik_foot_R": [
                        {"frame": 15, "location": [0.12, -0.05, 0], "ikfk": 1.0},
                        {"frame": 20, "location": [0.10, 0, 0.05], "ikfk": 0.5},
                        {"frame": 25, "location": [0.08, 0.05, 0.10], "ikfk": 0.0},
                    ]
                },
            },

            # Phase 3: Air (full FK - legs follow pose, not IK targets)
            {
                "name": "air",
                "frames": [25, 50],
                "pose": "air_peak",
                "timing_curve": "ease_in_out",
                "ik_targets": {
                    # IK targets still defined but ikfk=0 means FK controls legs
                    "ik_foot_L": [
                        {"frame": 25, "location": [-0.08, 0.05, 0.10], "ikfk": 0.0},
                        {"frame": 50, "location": [-0.08, 0.02, 0.12], "ikfk": 0.0},
                    ],
                    "ik_foot_R": [
                        {"frame": 25, "location": [0.08, 0.05, 0.10], "ikfk": 0.0},
                        {"frame": 50, "location": [0.08, 0.02, 0.12], "ikfk": 0.0},
                    ]
                },
            },

            # Phase 4: Descend (still FK, preparing for landing)
            {
                "name": "descend",
                "frames": [50, 65],
                "pose": "descend",
                "timing_curve": "ease_in",
                "ik_targets": {
                    "ik_foot_L": [
                        {"frame": 50, "location": [-0.08, 0.02, 0.12], "ikfk": 0.0},
                        {"frame": 60, "location": [-0.09, 0, 0.05], "ikfk": 0.3},  # Starting to blend in
                        {"frame": 65, "location": [-0.10, 0, 0.02], "ikfk": 0.5},
                    ],
                    "ik_foot_R": [
                        {"frame": 50, "location": [0.08, 0.02, 0.12], "ikfk": 0.0},
                        {"frame": 60, "location": [0.09, 0, 0.05], "ikfk": 0.3},
                        {"frame": 65, "location": [0.10, 0, 0.02], "ikfk": 0.5},
                    ]
                },
            },

            # Phase 5: Land (FK → IK, ground contact)
            {
                "name": "land",
                "frames": [65, 75],
                "pose": "land",
                "timing_curve": "ease_out",
                "ik_targets": {
                    "ik_foot_L": [
                        {"frame": 65, "location": [-0.10, 0, 0.02], "ikfk": 0.5},
                        {"frame": 68, "location": [-0.11, 0, 0], "ikfk": 1.0},     # Contact! Full IK
                        {"frame": 75, "location": [-0.12, -0.03, 0], "ikfk": 1.0},
                    ],
                    "ik_foot_R": [
                        {"frame": 65, "location": [0.10, 0, 0.02], "ikfk": 0.5},
                        {"frame": 68, "location": [0.11, 0, 0], "ikfk": 1.0},
                        {"frame": 75, "location": [0.12, -0.03, 0], "ikfk": 1.0},
                    ]
                },
            },

            # Phase 6: Recover (full IK - return to standing)
            {
                "name": "recover",
                "frames": [75, 90],
                "pose": "recover",
                "timing_curve": "ease_out",
                "ik_targets": {
                    "ik_foot_L": [
                        {"frame": 75, "location": [-0.12, -0.03, 0], "ikfk": 1.0},
                        {"frame": 90, "location": [-0.09, 0, 0], "ikfk": 1.0},
                    ],
                    "ik_foot_R": [
                        {"frame": 75, "location": [0.12, -0.03, 0], "ikfk": 1.0},
                        {"frame": 90, "location": [0.09, 0, 0], "ikfk": 1.0},
                    ]
                },
            },
        ],

        "procedural_layers": []
    }
}
