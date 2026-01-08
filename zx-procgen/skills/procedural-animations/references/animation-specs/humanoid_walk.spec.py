# Humanoid Walk Animation - Professional 4-phase cycle with animation principles
# Duration: 60 frames @ 60fps (1 second, 2 full steps)
# Principles: Weight, Arcs, Follow-through, Overlapping Action, Ease in/out
# Blender coords: +X=right, +Y=forward, +Z=up

ANIMATION = {
    "animation": {
        "name": "humanoid_walk",
        "duration_frames": 60,
        "fps": 60,
        "loop": True,
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

        # 4 key poses with body bounce and spine counter-rotation
        # Contact poses: body LOW (pelvis Z = -0.025), weight settling
        # Passing poses: body HIGH (pelvis Z = +0.025), lifted through swing
        "poses": {
            # Right foot forward, left back - CONTACT (low point, weight settling)
            "contact_right": {
                "pelvis": {"pitch": -3, "yaw": 10, "roll": -3, "location": [0, 0, -0.025]},
                "spine": {"pitch": 4, "yaw": -6, "roll": 0},  # Counter-rotate spine against pelvis
                "neck": {"pitch": 0, "yaw": -4, "roll": 0},
                "head": {"pitch": 3, "yaw": -5, "roll": 0},
                # Left arm forward (counter-swing to right leg)
                "arm_upper_L": {"pitch": 45, "yaw": 8, "roll": -12},
                "arm_lower_L": {"pitch": 30, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                # Right arm back
                "arm_upper_R": {"pitch": -35, "yaw": -8, "roll": 12},
                "arm_lower_R": {"pitch": 18, "yaw": 0, "roll": 0},  # Slight bend
            },

            # Right leg passing through - PASSING (high point, body lifted)
            "passing_right": {
                "pelvis": {"pitch": -4, "yaw": 0, "roll": 4, "location": [0, 0, 0.025]},
                "spine": {"pitch": 2, "yaw": 0, "roll": -2},
                "neck": {"pitch": 0, "yaw": 0, "roll": 0},
                "head": {"pitch": 0, "yaw": 0, "roll": 0},
                # Arms neutral, passing through with slight drag
                "arm_upper_L": {"pitch": 10, "yaw": 5, "roll": -8},
                "arm_lower_L": {"pitch": 15, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "arm_upper_R": {"pitch": -8, "yaw": -5, "roll": 8},
                "arm_lower_R": {"pitch": 14, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
            },

            # Left foot forward, right back - CONTACT (low point, weight settling)
            "contact_left": {
                "pelvis": {"pitch": -3, "yaw": -10, "roll": 3, "location": [0, 0, -0.025]},
                "spine": {"pitch": 4, "yaw": 6, "roll": 0},  # Counter-rotate spine against pelvis
                "neck": {"pitch": 0, "yaw": 4, "roll": 0},
                "head": {"pitch": 3, "yaw": 5, "roll": 0},
                # Right arm forward (counter-swing to left leg)
                "arm_upper_R": {"pitch": 45, "yaw": -8, "roll": 12},
                "arm_lower_R": {"pitch": 30, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                # Left arm back
                "arm_upper_L": {"pitch": -35, "yaw": 8, "roll": -12},
                "arm_lower_L": {"pitch": 18, "yaw": 0, "roll": 0},  # Slight bend
            },

            # Left leg passing through - PASSING (high point, body lifted)
            "passing_left": {
                "pelvis": {"pitch": -4, "yaw": 0, "roll": -4, "location": [0, 0, 0.025]},
                "spine": {"pitch": 2, "yaw": 0, "roll": 2},
                "neck": {"pitch": 0, "yaw": 0, "roll": 0},
                "head": {"pitch": 0, "yaw": 0, "roll": 0},
                # Arms neutral, passing through with slight drag
                "arm_upper_R": {"pitch": 10, "yaw": -5, "roll": 8},
                "arm_lower_R": {"pitch": 15, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
                "arm_upper_L": {"pitch": -8, "yaw": 5, "roll": -8},
                "arm_lower_L": {"pitch": 14, "yaw": 0, "roll": 0},  # Elbow flexion = positive pitch
            },
        },

        # Professional 4-phase walk cycle with arc motion
        # IK targets are ANKLE positions (not toe/ground)
        # Knight ankle rest height: Z = 0.08
        # Stride: Y from -0.45 (back) to +0.45 (front) - EXAGGERATED for cartoon style
        # Lift: Z = 0.08 (planted) to 0.28 (swing peak) - HIGH for snappy animation
        "phases": [
            # Phase 1: Right Contact (frame 0-15)
            # Right foot planted forward (+Y), left pushing off -> swinging
            {
                "name": "right_contact",
                "frames": [0, 15],
                "pose": "contact_right",
                "timing_curve": "ease_out",
                "ik_targets": {
                    "ik_foot_R": [
                        {"frame": 0, "location": [0.08, 0.45, 0.08]},      # Planted forward, ankle height
                        {"frame": 15, "location": [0.08, 0.0, 0.08]},     # Slides back to center
                    ],
                    "ik_foot_L": [
                        {"frame": 0, "location": [-0.08, -0.45, 0.12]},   # Back, toe-off (ankle rises)
                        {"frame": 5, "location": [-0.08, -0.22, 0.22]},   # Push off, lifting HIGH
                        {"frame": 10, "location": [-0.08, 0.0, 0.28]},    # Arc peak at center
                        {"frame": 15, "location": [-0.08, 0.22, 0.18]},   # Forward, descending
                    ]
                }
            },

            # Phase 2: Right Passing (frame 15-30)
            # Left swings forward (+Y) to contact, right slides back
            {
                "name": "passing_right",
                "frames": [15, 30],
                "pose": "passing_right",
                "timing_curve": "ease_in_out",
                "ik_targets": {
                    "ik_foot_R": [
                        {"frame": 15, "location": [0.08, 0.0, 0.08]},     # Center, taking weight
                        {"frame": 30, "location": [0.08, -0.45, 0.12]},   # Back, ready to push
                    ],
                    "ik_foot_L": [
                        {"frame": 15, "location": [-0.08, 0.22, 0.18]},   # Descending
                        {"frame": 22, "location": [-0.08, 0.38, 0.12]},   # Heel strike prep
                        {"frame": 30, "location": [-0.08, 0.45, 0.08]},   # Planted forward
                    ]
                }
            },

            # Phase 3: Left Contact (frame 30-45)
            # Left foot planted forward (+Y), right pushing off -> swinging
            {
                "name": "left_contact",
                "frames": [30, 45],
                "pose": "contact_left",
                "timing_curve": "ease_out",
                "ik_targets": {
                    "ik_foot_L": [
                        {"frame": 30, "location": [-0.08, 0.45, 0.08]},   # Planted forward
                        {"frame": 45, "location": [-0.08, 0.0, 0.08]},    # Slides back to center
                    ],
                    "ik_foot_R": [
                        {"frame": 30, "location": [0.08, -0.45, 0.12]},   # Back, toe-off
                        {"frame": 35, "location": [0.08, -0.22, 0.22]},   # Push off, lifting HIGH
                        {"frame": 40, "location": [0.08, 0.0, 0.28]},     # Arc peak at center
                        {"frame": 45, "location": [0.08, 0.22, 0.18]},    # Forward, descending
                    ]
                }
            },

            # Phase 4: Left Passing (frame 45-60)
            # Right swings forward (+Y) to contact, left slides back
            {
                "name": "passing_left",
                "frames": [45, 60],
                "pose": "passing_left",
                "timing_curve": "ease_in_out",
                "ik_targets": {
                    "ik_foot_L": [
                        {"frame": 45, "location": [-0.08, 0.0, 0.08]},    # Center, taking weight
                        {"frame": 60, "location": [-0.08, -0.45, 0.12]},  # Back, ready to push
                    ],
                    "ik_foot_R": [
                        {"frame": 45, "location": [0.08, 0.22, 0.18]},    # Descending
                        {"frame": 52, "location": [0.08, 0.38, 0.12]},    # Heel strike prep
                        {"frame": 60, "location": [0.08, 0.45, 0.08]},    # Planted (loops to frame 0)
                    ]
                }
            },
        ],

        "procedural_layers": []
    }
}
