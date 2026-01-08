# Knight Enemy - Armored Humanoid
# Budget: 600 tris
# Style: Armored with pauldrons and helmet

SPEC = {
    "character": {
        "name": "knight_enemy",
        "tri_budget": 600,

        "texturing": {
            "uv_mode": "smart_project"
        },

        "skeleton": [
            # ROOT (at ground level for industry-standard rigging)
            {"bone": "root", "parent": None, "head": [0, 0, 0], "tail": [0, 0, 0.05]},

            # CORE
            {"bone": "pelvis", "parent": "root", "head": [0, 0, 0.9], "tail": [0, 0, 1.0]},
            {"bone": "spine", "parent": "pelvis", "head": [0, 0, 1.0], "tail": [0, 0, 1.3]},
            {"bone": "neck", "parent": "spine", "head": [0, 0, 1.3], "tail": [0, 0, 1.42]},
            {"bone": "head", "parent": "neck", "head": [0, 0, 1.42], "tail": [0, 0, 1.55]},

            # LEFT ARM
            {"bone": "arm_upper_L", "parent": "spine", "head": [-0.15, 0, 1.25], "tail": [-0.35, 0, 1.15]},
            {"bone": "arm_lower_L", "parent": "arm_upper_L", "head": [-0.35, 0, 1.15], "tail": [-0.55, 0, 1.05]},

            # LEFT LEG
            # Blender: +X=right, +Y=forward, +Z=up
            # Forward knee bend (Y=0.08 at knee) gives IK preferred direction AND enables calibration
            # Calibration requires ~12° bend (dot < 0.98), Y=0.08 provides ~11-12°
            {"bone": "leg_upper_L", "parent": "pelvis", "head": [-0.08, 0, 0.9], "tail": [-0.08, 0.08, 0.5]},
            {"bone": "leg_lower_L", "parent": "leg_upper_L", "head": [-0.08, 0.08, 0.5], "tail": [-0.08, 0, 0.08]},
            {"bone": "foot_L", "parent": "leg_lower_L", "head": [-0.08, 0, 0.08], "tail": [-0.08, 0.12, 0.02]},
            {"bone": "toe_L", "parent": "foot_L", "head": [-0.08, 0.12, 0.02], "tail": [-0.08, 0.18, 0]},

            # RIGHT SIDE (mirrors)
            {"bone": "arm_upper_R", "mirror": "arm_upper_L"},
            {"bone": "arm_lower_R", "mirror": "arm_lower_L"},
            {"bone": "leg_upper_R", "mirror": "leg_upper_L"},
            {"bone": "leg_lower_R", "mirror": "leg_lower_L"},
            {"bone": "foot_R", "mirror": "foot_L"},
            {"bone": "toe_R", "mirror": "toe_L"},
        ],

        "parts": {
            "pelvis": {
                "bone": "pelvis",
                "base": "hexagon(6)",
                "base_radius": 0.11,
                "steps": [
                    {"extrude": 0.05, "scale": 0.95},     # hip guard
                    {"extrude": 0.05, "scale": 1.0},      # belt area
                ],
                "cap_start": True,
                "cap_end": False
            },

            "torso": {
                "bone": "spine",
                "base": "hexagon(6)",
                "base_radius": 0.11,
                "steps": [
                    {"extrude": 0.02, "scale": 1.2},      # chest plate edge
                    {"extrude": 0.15, "scale": 1.15},     # chest plate body
                    {"extrude": 0.08, "scale": 1.0},      # mid torso
                    {"extrude": 0.05, "scale": 0.85},     # upper chest
                ],
                "cap_start": False,
                "cap_end": False
            },

            "neck": {
                "bone": "neck",
                "base": "hexagon(6)",
                "base_radius": 0.07,
                "steps": [
                    {"extrude": 0.04, "scale": 1.1},      # gorget
                    {"extrude": 0.08, "scale": 0.95},     # neck guard
                ],
                "cap_start": False,
                "cap_end": False
            },

            "head": {
                "bone": "head",
                "base": "hexagon(6)",
                "base_radius": 0.075,
                "steps": [
                    {"extrude": 0.02, "scale": 1.2},      # helmet brim
                    {"extrude": 0.09, "scale": 1.0},      # helmet body
                    {"extrude": 0.03, "scale": 0.7},      # helmet taper
                    {"extrude": 0.01, "scale": 0.4},      # helmet peak
                ],
                "cap_start": False,
                "cap_end": True
            },

            "arm_upper_L": {
                "bone": "arm_upper_L",
                "base": "hexagon(6)",
                "base_radius": 0.045,
                "steps": [
                    {"extrude": 0.03, "scale": 1.4},      # pauldron flare
                    {"extrude": 0.04, "scale": 1.0},      # pauldron body
                    {"extrude": 0.02, "scale": 0.6},      # shoulder taper
                    {"extrude": 0.13, "scale": 1.0},      # arm body
                ],
                "cap_start": True,
                "cap_end": False
            },

            "arm_lower_L": {
                "bone": "arm_lower_L",
                "base": "hexagon(6)",
                "base_radius": 0.038,
                "steps": [
                    {"extrude": 0.03, "scale": 1.15},     # elbow guard
                    {"extrude": 0.12, "scale": 0.9},      # forearm
                    {"extrude": 0.04, "scale": 1.2},      # gauntlet cuff
                    {"extrude": 0.03, "scale": 0.65},     # wrist
                ],
                "cap_start": False,
                "cap_end": True
            },

            "leg_upper_L": {
                "bone": "leg_upper_L",
                "base": "hexagon(6)",
                "base_radius": 0.055,
                "steps": [
                    {"extrude": 0.03, "scale": 1.15},     # hip armor
                    {"extrude": 0.24, "scale": 1.0},      # thigh plate
                    {"extrude": 0.11, "scale": 0.75},     # knee taper
                ],
                "cap_start": True,
                "cap_end": False
            },

            "leg_lower_L": {
                "bone": "leg_lower_L",
                "base": "hexagon(6)",
                "base_radius": 0.041,
                "steps": [
                    {"extrude": 0.03, "scale": 1.2},      # knee guard
                    {"extrude": 0.20, "scale": 0.85},     # shin
                    {"extrude": 0.15, "scale": 0.75},     # lower shin
                ],
                "cap_start": False,
                "cap_end": False
            },

            "foot_L": {
                "bone": "foot_L",
                "base": "hexagon(6)",
                "base_radius": 0.038,
                "steps": [
                    {"extrude": 0.03, "scale": 1.2},       # ankle boot cuff
                    {"extrude": 0.06, "scale": 1.0},       # boot body (follows bone forward-down)
                ],
                "cap_start": False,
                "cap_end": False  # connects to toe
            },

            "toe_L": {
                "bone": "toe_L",
                "base": "hexagon(6)",
                "base_radius": 0.038,
                "steps": [
                    {"extrude": 0.04, "scale": 0.85},      # toe box
                    {"extrude": 0.02, "scale": 0.5},       # toe tip rounded
                ],
                "cap_start": False,
                "cap_end": True
            },

            # RIGHT SIDE (mirrors)
            "arm_upper_R": {"mirror": "arm_upper_L"},
            "arm_lower_R": {"mirror": "arm_lower_L"},
            "leg_upper_R": {"mirror": "leg_upper_L"},
            "leg_lower_R": {"mirror": "leg_lower_L"},
            "foot_R": {"mirror": "foot_L"},
            "toe_R": {"mirror": "toe_L"},
        }
    }
}
