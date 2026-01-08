# Spider Walk Animation - Professional IK cycle with animation principles
# Duration: 60 frames @ 60fps (1 second)
# Principles: Weight shift, Arc motion, Overlapping action, Natural timing
# Uses alternating tetrapod gait (Set A vs Set B legs)

ANIMATION = {
    "animation": {
        "name": "spider_walk_ik",
        "duration_frames": 60,
        "fps": 60,
        "loop": True,
        "save_blend": True,
        "input_armature": "generated/characters/spider.glb",

        # Validation conventions
        "conventions": {
            "version": "2026-01-08",
            "strict": False,
        },

        # Declarative rig setup - uses spider_legs preset
        "rig_setup": {
            "presets": {
                "spider_legs": True,  # Infers hinge validation for all spider leg joints
            },
            # No explicit constraints needed - spider_legs preset handles it
        },

        # Body poses with enhanced sway for weight shift
        "poses": {
            "body_neutral": {
                "cephalothorax": {"pitch": 2, "yaw": 0, "roll": 0},
                "abdomen": {"pitch": 3, "yaw": 0, "roll": 0},
                "head": {"pitch": -2, "yaw": 0, "roll": 0}
            },
            "body_left_shift": {
                "cephalothorax": {"pitch": 3, "yaw": 0, "roll": -5},  # Increased roll for weight shift
                "abdomen": {"pitch": 5, "yaw": 0, "roll": -3},
                "head": {"pitch": -3, "yaw": 0, "roll": 0}
            },
            "body_right_shift": {
                "cephalothorax": {"pitch": 3, "yaw": 0, "roll": 5},   # Increased roll for weight shift
                "abdomen": {"pitch": 5, "yaw": 0, "roll": 3},
                "head": {"pitch": -3, "yaw": 0, "roll": 0}
            }
        },

        # Leg rest positions (from spider.spec.py)
        # Front legs: [-0.28, 0.25, 0] / [0.28, 0.25, 0]
        # Mid-front legs: [-0.3, 0.08, 0] / [0.3, 0.08, 0]
        # Mid-back legs: [-0.3, -0.08, 0] / [0.3, -0.08, 0]
        # Back legs: [-0.28, -0.22, 0] / [0.28, -0.22, 0]

        # Enhanced stride: Y movement = 0.18 per leg (was 0.10)
        # Enhanced lift: Z = 0.08 at peak (was 0.04)
        # Arc motion: X offset at mid-swing for natural curve

        "phases": [
            # Phase 1: Set A planted, Set B swinging forward with arcs
            {
                "name": "set_a_contact",
                "frames": [0, 15],
                "pose": "body_left_shift",
                "timing_curve": "ease_in_out",
                "description": "Set A legs planted (weight left), Set B swing forward with arcs",
                "ik_targets": {
                    # Set A - planted, sliding backward (ground contact)
                    "ik_leg_front_L": [
                        {"frame": 0, "location": [-0.28, 0.34, 0]},      # Forward plant
                        {"frame": 15, "location": [-0.28, 0.16, 0]}     # Slides back
                    ],
                    "ik_leg_mid_front_R": [
                        {"frame": 0, "location": [0.30, 0.17, 0]},
                        {"frame": 15, "location": [0.30, -0.01, 0]}
                    ],
                    "ik_leg_mid_back_L": [
                        {"frame": 0, "location": [-0.30, 0.01, 0]},
                        {"frame": 15, "location": [-0.30, -0.19, 0]}
                    ],
                    "ik_leg_back_R": [
                        {"frame": 0, "location": [0.28, -0.18, 0]},
                        {"frame": 15, "location": [0.28, -0.24, 0]}
                    ],

                    # Set B - swinging forward with arc motion (lift, arc outward, plant)
                    "ik_leg_front_R": [
                        {"frame": 0, "location": [0.28, 0.16, 0]},       # Back position
                        {"frame": 5, "location": [0.32, 0.22, 0.06]},    # Lifting, arc outward
                        {"frame": 10, "location": [0.34, 0.30, 0.08]},   # Arc peak (outward X, high Z)
                        {"frame": 15, "location": [0.28, 0.34, 0]}       # Plant forward
                    ],
                    "ik_leg_mid_front_L": [
                        {"frame": 0, "location": [-0.30, -0.01, 0]},
                        {"frame": 5, "location": [-0.34, 0.04, 0.06]},
                        {"frame": 10, "location": [-0.36, 0.11, 0.08]},
                        {"frame": 15, "location": [-0.30, 0.17, 0]}
                    ],
                    "ik_leg_mid_back_R": [
                        {"frame": 0, "location": [0.30, -0.19, 0]},
                        {"frame": 5, "location": [0.34, -0.12, 0.06]},
                        {"frame": 10, "location": [0.36, -0.05, 0.08]},
                        {"frame": 15, "location": [0.30, 0.01, 0]}
                    ],
                    "ik_leg_back_L": [
                        {"frame": 0, "location": [-0.28, -0.24, 0]},
                        {"frame": 5, "location": [-0.32, -0.22, 0.06]},
                        {"frame": 10, "location": [-0.34, -0.19, 0.08]},
                        {"frame": 15, "location": [-0.28, -0.18, 0]}
                    ]
                }
            },

            # Phase 2: Set B planted, Set A swinging forward with arcs
            {
                "name": "set_b_contact",
                "frames": [15, 30],
                "pose": "body_right_shift",
                "timing_curve": "ease_in_out",
                "description": "Set B legs planted (weight right), Set A swing forward with arcs",
                "ik_targets": {
                    # Set B - planted, sliding backward
                    "ik_leg_front_R": [
                        {"frame": 15, "location": [0.28, 0.34, 0]},
                        {"frame": 30, "location": [0.28, 0.16, 0]}
                    ],
                    "ik_leg_mid_front_L": [
                        {"frame": 15, "location": [-0.30, 0.17, 0]},
                        {"frame": 30, "location": [-0.30, -0.01, 0]}
                    ],
                    "ik_leg_mid_back_R": [
                        {"frame": 15, "location": [0.30, 0.01, 0]},
                        {"frame": 30, "location": [0.30, -0.19, 0]}
                    ],
                    "ik_leg_back_L": [
                        {"frame": 15, "location": [-0.28, -0.18, 0]},
                        {"frame": 30, "location": [-0.28, -0.24, 0]}
                    ],

                    # Set A - swinging forward with arc motion
                    "ik_leg_front_L": [
                        {"frame": 15, "location": [-0.28, 0.16, 0]},
                        {"frame": 20, "location": [-0.32, 0.22, 0.06]},
                        {"frame": 25, "location": [-0.34, 0.30, 0.08]},
                        {"frame": 30, "location": [-0.28, 0.34, 0]}
                    ],
                    "ik_leg_mid_front_R": [
                        {"frame": 15, "location": [0.30, -0.01, 0]},
                        {"frame": 20, "location": [0.34, 0.04, 0.06]},
                        {"frame": 25, "location": [0.36, 0.11, 0.08]},
                        {"frame": 30, "location": [0.30, 0.17, 0]}
                    ],
                    "ik_leg_mid_back_L": [
                        {"frame": 15, "location": [-0.30, -0.19, 0]},
                        {"frame": 20, "location": [-0.34, -0.12, 0.06]},
                        {"frame": 25, "location": [-0.36, -0.05, 0.08]},
                        {"frame": 30, "location": [-0.30, 0.01, 0]}
                    ],
                    "ik_leg_back_R": [
                        {"frame": 15, "location": [0.28, -0.24, 0]},
                        {"frame": 20, "location": [0.32, -0.22, 0.06]},
                        {"frame": 25, "location": [0.34, -0.19, 0.08]},
                        {"frame": 30, "location": [0.28, -0.18, 0]}
                    ]
                }
            },

            # Phase 3: Repeat Set A contact (second stride)
            {
                "name": "set_a_contact_2",
                "frames": [30, 45],
                "pose": "body_left_shift",
                "timing_curve": "ease_in_out",
                "description": "Set A planted again, Set B swing forward with arcs",
                "ik_targets": {
                    # Set A - planted
                    "ik_leg_front_L": [
                        {"frame": 30, "location": [-0.28, 0.34, 0]},
                        {"frame": 45, "location": [-0.28, 0.16, 0]}
                    ],
                    "ik_leg_mid_front_R": [
                        {"frame": 30, "location": [0.30, 0.17, 0]},
                        {"frame": 45, "location": [0.30, -0.01, 0]}
                    ],
                    "ik_leg_mid_back_L": [
                        {"frame": 30, "location": [-0.30, 0.01, 0]},
                        {"frame": 45, "location": [-0.30, -0.19, 0]}
                    ],
                    "ik_leg_back_R": [
                        {"frame": 30, "location": [0.28, -0.18, 0]},
                        {"frame": 45, "location": [0.28, -0.24, 0]}
                    ],

                    # Set B - swinging with arcs
                    "ik_leg_front_R": [
                        {"frame": 30, "location": [0.28, 0.16, 0]},
                        {"frame": 35, "location": [0.32, 0.22, 0.06]},
                        {"frame": 40, "location": [0.34, 0.30, 0.08]},
                        {"frame": 45, "location": [0.28, 0.34, 0]}
                    ],
                    "ik_leg_mid_front_L": [
                        {"frame": 30, "location": [-0.30, -0.01, 0]},
                        {"frame": 35, "location": [-0.34, 0.04, 0.06]},
                        {"frame": 40, "location": [-0.36, 0.11, 0.08]},
                        {"frame": 45, "location": [-0.30, 0.17, 0]}
                    ],
                    "ik_leg_mid_back_R": [
                        {"frame": 30, "location": [0.30, -0.19, 0]},
                        {"frame": 35, "location": [0.34, -0.12, 0.06]},
                        {"frame": 40, "location": [0.36, -0.05, 0.08]},
                        {"frame": 45, "location": [0.30, 0.01, 0]}
                    ],
                    "ik_leg_back_L": [
                        {"frame": 30, "location": [-0.28, -0.24, 0]},
                        {"frame": 35, "location": [-0.32, -0.22, 0.06]},
                        {"frame": 40, "location": [-0.34, -0.19, 0.08]},
                        {"frame": 45, "location": [-0.28, -0.18, 0]}
                    ]
                }
            },

            # Phase 4: Repeat Set B contact (loop back)
            {
                "name": "set_b_contact_2",
                "frames": [45, 60],
                "pose": "body_right_shift",
                "timing_curve": "ease_in_out",
                "description": "Set B planted, Set A swing to loop point with arcs",
                "ik_targets": {
                    # Set B - planted
                    "ik_leg_front_R": [
                        {"frame": 45, "location": [0.28, 0.34, 0]},
                        {"frame": 60, "location": [0.28, 0.16, 0]}
                    ],
                    "ik_leg_mid_front_L": [
                        {"frame": 45, "location": [-0.30, 0.17, 0]},
                        {"frame": 60, "location": [-0.30, -0.01, 0]}
                    ],
                    "ik_leg_mid_back_R": [
                        {"frame": 45, "location": [0.30, 0.01, 0]},
                        {"frame": 60, "location": [0.30, -0.19, 0]}
                    ],
                    "ik_leg_back_L": [
                        {"frame": 45, "location": [-0.28, -0.18, 0]},
                        {"frame": 60, "location": [-0.28, -0.24, 0]}
                    ],

                    # Set A - swinging to loop position with arcs
                    "ik_leg_front_L": [
                        {"frame": 45, "location": [-0.28, 0.16, 0]},
                        {"frame": 50, "location": [-0.32, 0.22, 0.06]},
                        {"frame": 55, "location": [-0.34, 0.30, 0.08]},
                        {"frame": 60, "location": [-0.28, 0.34, 0]}
                    ],
                    "ik_leg_mid_front_R": [
                        {"frame": 45, "location": [0.30, -0.01, 0]},
                        {"frame": 50, "location": [0.34, 0.04, 0.06]},
                        {"frame": 55, "location": [0.36, 0.11, 0.08]},
                        {"frame": 60, "location": [0.30, 0.17, 0]}
                    ],
                    "ik_leg_mid_back_L": [
                        {"frame": 45, "location": [-0.30, -0.19, 0]},
                        {"frame": 50, "location": [-0.34, -0.12, 0.06]},
                        {"frame": 55, "location": [-0.36, -0.05, 0.08]},
                        {"frame": 60, "location": [-0.30, 0.01, 0]}
                    ],
                    "ik_leg_back_R": [
                        {"frame": 45, "location": [0.28, -0.24, 0]},
                        {"frame": 50, "location": [0.32, -0.22, 0.06]},
                        {"frame": 55, "location": [0.34, -0.19, 0.08]},
                        {"frame": 60, "location": [0.28, -0.18, 0]}
                    ]
                }
            }
        ],

        # Procedural layers for subtle body motion
        "procedural_layers": [
            {
                "type": "bob",
                "target": "cephalothorax",
                "period_frames": 15,
                "amplitude": 0.015,
                "axis": "pitch",
                "description": "Body bob from weight shifts (4x per loop)"
            },
            {
                "type": "breathing",
                "target": "abdomen",
                "period_frames": 60,
                "amplitude": 0.008,
                "axis": "pitch",
                "description": "Subtle breathing motion"
            }
        ]
    }
}
