# Idle Animation - Generic Humanoid
# Duration: 120 frames @ 60fps (2 seconds)
# Demonstrates: breathing cycle, weight shifts, procedural layers
#
# Character: Generic humanoid, medium build.
# Demeanor: Relaxed but alert stance.
# Goal: Subtle breathing and weight shifts for life-like presence.

MOTION = {
    "animation": {
        "name": "humanoid_idle",
        "duration_frames": 120,
        "fps": 60,
        "loop": True,

        "poses": {
            "idle_base": {
                # Slight forward lean for alertness
                "Hips": {"pitch": -3, "yaw": 0, "roll": 0},
                "Spine": {"pitch": 2, "yaw": 0, "roll": 0},
                "Chest": {"pitch": 1, "yaw": 0, "roll": 0},
                "Neck": {"pitch": 1, "yaw": 0, "roll": 0},
                "Head": {"pitch": -2, "yaw": 0, "roll": 0},

                # Arms relaxed at sides, slightly bent
                "UpperArmL": {"pitch": -10, "yaw": 5, "roll": -8},
                "LowerArmL": {"pitch": 0, "yaw": 0, "roll": -15},
                "HandL": {"pitch": 0, "yaw": 0, "roll": 0},
                "UpperArmR": {"pitch": -10, "yaw": -5, "roll": 8},
                "LowerArmR": {"pitch": 0, "yaw": 0, "roll": 15},
                "HandR": {"pitch": 0, "yaw": 0, "roll": 0},

                # Legs slightly bent, weight centered
                "UpperLegL": {"pitch": 3, "yaw": -2, "roll": 0},
                "LowerLegL": {"pitch": -5, "yaw": 0, "roll": 0},
                "FootL": {"pitch": 0, "yaw": 0, "roll": 0},
                "UpperLegR": {"pitch": 3, "yaw": 2, "roll": 0},
                "LowerLegR": {"pitch": -5, "yaw": 0, "roll": 0},
                "FootR": {"pitch": 0, "yaw": 0, "roll": 0},
            },

            "breath_peak": {
                # Chest expands, slight lift
                "Chest": {"pitch": 3, "yaw": 0, "roll": 0},
                "Hips": {"pitch": -2, "yaw": 0, "roll": 0},
                "Head": {"pitch": -3, "yaw": 0, "roll": 0},
                # Shoulders rise slightly
                "UpperArmL": {"pitch": -12, "yaw": 5, "roll": -10},
                "UpperArmR": {"pitch": -12, "yaw": -5, "roll": 10},
            },

            "weight_shift_left": {
                # Hips tilt as weight goes to left leg
                "Hips": {"pitch": -3, "yaw": 0, "roll": -2},
                "Spine": {"pitch": 2, "yaw": 0, "roll": 1},
                "Chest": {"pitch": 1, "yaw": 0, "roll": 0.5},
                # Left leg takes weight
                "UpperLegL": {"pitch": 5, "yaw": -3, "roll": 0},
                "LowerLegL": {"pitch": -8, "yaw": 0, "roll": 0},
                # Right leg relaxes
                "UpperLegR": {"pitch": 0, "yaw": 3, "roll": 0},
                "LowerLegR": {"pitch": -3, "yaw": 0, "roll": 0},
            },

            "weight_shift_right": {
                # Mirror of left shift
                "Hips": {"pitch": -3, "yaw": 0, "roll": 2},
                "Spine": {"pitch": 2, "yaw": 0, "roll": -1},
                "Chest": {"pitch": 1, "yaw": 0, "roll": -0.5},
                # Right leg takes weight
                "UpperLegR": {"pitch": 5, "yaw": 3, "roll": 0},
                "LowerLegR": {"pitch": -8, "yaw": 0, "roll": 0},
                # Left leg relaxes
                "UpperLegL": {"pitch": 0, "yaw": -3, "roll": 0},
                "LowerLegL": {"pitch": -3, "yaw": 0, "roll": 0},
            },
        },

        "phases": [
            {
                "name": "neutral_hold",
                "frames": [0, 14],
                "pose": "idle_base",
                "timing_curve": "linear",
                "description": "Balanced neutral stance"
            },
            {
                "name": "breath_in",
                "frames": [15, 29],
                "pose": "breath_peak",
                "timing_curve": "ease_out",
                "description": "Inhale - chest expands"
            },
            {
                "name": "breath_out",
                "frames": [30, 44],
                "pose": "idle_base",
                "timing_curve": "ease_in",
                "description": "Exhale - return to neutral"
            },
            {
                "name": "shift_to_left",
                "frames": [45, 59],
                "pose": "weight_shift_left",
                "timing_curve": "ease_in_out",
                "description": "Weight shifts to left leg"
            },
            {
                "name": "hold_left",
                "frames": [60, 74],
                "pose": "weight_shift_left",
                "timing_curve": "linear",
                "description": "Hold on left leg"
            },
            {
                "name": "shift_to_right",
                "frames": [75, 89],
                "pose": "weight_shift_right",
                "timing_curve": "ease_in_out",
                "description": "Weight shifts to right leg"
            },
            {
                "name": "hold_right",
                "frames": [90, 104],
                "pose": "weight_shift_right",
                "timing_curve": "linear",
                "description": "Hold on right leg"
            },
            {
                "name": "return_center",
                "frames": [105, 119],
                "pose": "idle_base",
                "timing_curve": "ease_in_out",
                "description": "Return to center, loop point"
            },
        ],

        "procedural_layers": [
            {
                "type": "breathing",
                "target": "Chest",
                "period_frames": 90,
                "amplitude": 0.015,
                "axis": "pitch",
                "description": "Subtle chest breathing overlay"
            },
            {
                "type": "sway",
                "target": "Spine",
                "period_frames": 180,
                "amplitude": 0.005,
                "axis": "roll",
                "description": "Very subtle side sway"
            },
            {
                "type": "noise",
                "target": "Head",
                "amplitude": 0.002,
                "frequency": 0.3,
                "description": "Micro head movements for life"
            },
            {
                "type": "noise",
                "target": "HandL",
                "amplitude": 0.003,
                "frequency": 0.4,
                "description": "Subtle finger movement hint"
            },
            {
                "type": "noise",
                "target": "HandR",
                "amplitude": 0.003,
                "frequency": 0.35,
                "description": "Subtle finger movement hint"
            },
        ],

        "ik_hints": {
            "feet": None,  # No IK needed for idle
            "hands": None
        },

        "style": {
            "weight": "medium",
            "energy": "calm",
            "intent": "idle"
        }
    }
}
