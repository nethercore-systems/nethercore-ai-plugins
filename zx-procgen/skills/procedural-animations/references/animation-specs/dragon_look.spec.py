# Dragon Look Animation - Head look and aim constraint test
# Duration: 180 frames @ 60fps (3 seconds)
# Demonstrates: head_look preset, aim constraints with clamping, eye tracking
# Tests untested features: aim constraints, head_look preset, look target animation

ANIMATION = {
    "animation": {
        "name": "dragon_look",
        "duration_frames": 180,
        "fps": 60,
        "loop": True,
        "save_blend": True,  # Save .blend for debugging
        "input_armature": "generated/characters/dragon.glb",

        # Validation conventions
        "conventions": {
            "version": "2026-01-08",
            "strict": False,
        },

        # Declarative rig setup for look-at testing
        "rig_setup": {
            "presets": {
                "head_look": True,    # Auto-creates aim for head toward look_target
                "basic_spine": True   # Spine follows subtly
            },

            # Explicit aim constraints for fine control
            "aim_constraints": [
                {
                    "bone": "head",
                    "target": "look_target",
                    "aim_axis": "+Y",  # Dragon head points +Y (forward)
                    "up_axis": "+Z",
                    "clamp": {
                        "pitch": [-60, 80],   # Can look down more than up
                        "yaw": [-90, 90]      # Full side-to-side range
                    },
                    "influence": 1.0
                },
                {
                    "bone": "neck",
                    "target": "look_target",
                    "aim_axis": "+Y",
                    "up_axis": "+Z",
                    "clamp": {
                        "pitch": [-30, 40],   # Neck has less range than head
                        "yaw": [-60, 60]
                    },
                    "influence": 0.6  # Partial influence - head leads
                },
                {
                    "bone": "eye_L",
                    "target": "look_target",
                    "aim_axis": "+Y",
                    "up_axis": "+Z",
                    "clamp": {
                        "pitch": [-40, 40],
                        "yaw": [-50, 30]      # Left eye asymmetric for stereo
                    },
                    "influence": 0.8
                },
                {
                    "bone": "eye_R",
                    "target": "look_target",
                    "aim_axis": "+Y",
                    "up_axis": "+Z",
                    "clamp": {
                        "pitch": [-40, 40],
                        "yaw": [-30, 50]      # Right eye mirrors left
                    },
                    "influence": 0.8
                }
            ],

            # Bake with curve cleaning
            "bake": {
                "clean_curves": True,
                "tolerance": 0.001
            }
        },

        # FK poses for body (head/neck controlled by aim constraints)
        "poses": {
            "relaxed": {
                "pelvis": {"pitch": 0, "yaw": 0, "roll": 0},
                "spine_01": {"pitch": 0, "yaw": 0, "roll": 0},
                "spine_02": {"pitch": 0, "yaw": 0, "roll": 0},
                "spine_03": {"pitch": 0, "yaw": 0, "roll": 0},
                "chest": {"pitch": 0, "yaw": 0, "roll": 0}
                # head, neck, eyes controlled by aim constraints
            },

            "alert_left": {
                "pelvis": {"pitch": 0, "yaw": 5, "roll": 0},
                "spine_01": {"pitch": 0, "yaw": 3, "roll": 0},
                "spine_02": {"pitch": 0, "yaw": 2, "roll": 0},
                "spine_03": {"pitch": 0, "yaw": 1, "roll": 0},
                "chest": {"pitch": 2, "yaw": 3, "roll": 0}
            },

            "alert_right": {
                "pelvis": {"pitch": 0, "yaw": -5, "roll": 0},
                "spine_01": {"pitch": 0, "yaw": -3, "roll": 0},
                "spine_02": {"pitch": 0, "yaw": -2, "roll": 0},
                "spine_03": {"pitch": 0, "yaw": -1, "roll": 0},
                "chest": {"pitch": 2, "yaw": -3, "roll": 0}
            },

            "look_up": {
                "pelvis": {"pitch": -3, "yaw": 0, "roll": 0},
                "spine_01": {"pitch": -2, "yaw": 0, "roll": 0},
                "spine_02": {"pitch": -2, "yaw": 0, "roll": 0},
                "spine_03": {"pitch": -1, "yaw": 0, "roll": 0},
                "chest": {"pitch": -3, "yaw": 0, "roll": 0}
            }
        },

        # Look target moves around to test aim constraint following
        # Dragon head is at approximately [0, 0.7, 0.6]
        # Look target starts 1 unit in front, then moves around

        "phases": [
            # Phase 1: Look straight ahead (baseline)
            {
                "name": "look_forward",
                "frames": [0, 30],
                "pose": "relaxed",
                "timing_curve": "ease_out",
                "description": "Looking forward - establishes baseline",
                "look_targets": {
                    "look_target": [
                        {"frame": 0, "location": [0, 1.7, 0.6]},
                        {"frame": 30, "location": [0, 1.7, 0.6]}
                    ]
                }
            },

            # Phase 2: Track target moving left
            {
                "name": "track_left",
                "frames": [30, 60],
                "pose": "alert_left",
                "timing_curve": "ease_in_out",
                "description": "Target moves left - tests yaw tracking",
                "look_targets": {
                    "look_target": [
                        {"frame": 30, "location": [0, 1.7, 0.6]},
                        {"frame": 45, "location": [-0.5, 1.5, 0.6]},
                        {"frame": 60, "location": [-1.0, 1.2, 0.6]}
                    ]
                }
            },

            # Phase 3: Target moves up (tests pitch clamping)
            {
                "name": "track_up",
                "frames": [60, 90],
                "pose": "look_up",
                "timing_curve": "ease_in_out",
                "description": "Target moves up - tests pitch limits",
                "look_targets": {
                    "look_target": [
                        {"frame": 60, "location": [-1.0, 1.2, 0.6]},
                        {"frame": 75, "location": [-0.5, 1.4, 1.2]},
                        {"frame": 90, "location": [0, 1.5, 1.8]}  # High above - should clamp
                    ]
                }
            },

            # Phase 4: Track target moving right
            {
                "name": "track_right",
                "frames": [90, 120],
                "pose": "alert_right",
                "timing_curve": "ease_in_out",
                "description": "Target sweeps right - tests full yaw range",
                "look_targets": {
                    "look_target": [
                        {"frame": 90, "location": [0, 1.5, 1.8]},
                        {"frame": 105, "location": [0.5, 1.4, 1.0]},
                        {"frame": 120, "location": [1.0, 1.2, 0.6]}
                    ]
                }
            },

            # Phase 5: Target moves down and close (tests near focus)
            {
                "name": "track_close",
                "frames": [120, 150],
                "pose": "relaxed",
                "timing_curve": "ease_in_out",
                "description": "Target comes close and low - tests convergence",
                "look_targets": {
                    "look_target": [
                        {"frame": 120, "location": [1.0, 1.2, 0.6]},
                        {"frame": 135, "location": [0.3, 1.0, 0.3]},
                        {"frame": 150, "location": [0, 0.9, 0.2]}  # Close and low
                    ]
                }
            },

            # Phase 6: Return to forward for loop
            {
                "name": "return_forward",
                "frames": [150, 180],
                "pose": "relaxed",
                "timing_curve": "ease_out",
                "description": "Return to forward for seamless loop",
                "look_targets": {
                    "look_target": [
                        {"frame": 150, "location": [0, 0.9, 0.2]},
                        {"frame": 165, "location": [0, 1.3, 0.4]},
                        {"frame": 180, "location": [0, 1.7, 0.6]}
                    ]
                }
            }
        ],

        # No procedural layers - focus on aim constraint testing
        "procedural_layers": []
    }
}
