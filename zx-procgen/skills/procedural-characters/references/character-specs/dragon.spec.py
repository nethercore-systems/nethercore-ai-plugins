# Dragon Quadruped - Tests N-bone IK, basic_spine, head_look, quadruped_legs
# Budget: 500 tris
# Style: Western dragon quadruped with long tail

SPEC = {
    "character": {
        "name": "dragon",
        "tri_budget": 500,

        "texturing": {
            "uv_mode": "smart_project"
        },

        "skeleton": [
            # ROOT (at ground level)
            {"bone": "root", "parent": None, "head": [0, 0, 0], "tail": [0, 0, 0.05]},

            # PELVIS - quadruped hip center
            {"bone": "pelvis", "parent": "root", "head": [0, 0, 0.4], "tail": [0, 0.1, 0.4]},

            # SPINE - 4 bones for basic_spine preset testing
            {"bone": "spine_01", "parent": "pelvis", "head": [0, 0.1, 0.4], "tail": [0, 0.22, 0.42]},
            {"bone": "spine_02", "parent": "spine_01", "head": [0, 0.22, 0.42], "tail": [0, 0.34, 0.45]},
            {"bone": "spine_03", "parent": "spine_02", "head": [0, 0.34, 0.45], "tail": [0, 0.46, 0.48]},
            {"bone": "chest", "parent": "spine_03", "head": [0, 0.46, 0.48], "tail": [0, 0.55, 0.5]},

            # NECK + HEAD - for head_look preset
            {"bone": "neck", "parent": "chest", "head": [0, 0.55, 0.5], "tail": [0, 0.7, 0.6]},
            {"bone": "head", "parent": "neck", "head": [0, 0.7, 0.6], "tail": [0, 0.9, 0.58]},

            # EYES - for aim constraint testing
            {"bone": "eye_L", "parent": "head", "head": [-0.04, 0.82, 0.62], "tail": [-0.04, 0.87, 0.62]},
            {"bone": "eye_R", "parent": "head", "head": [0.04, 0.82, 0.62], "tail": [0.04, 0.87, 0.62]},

            # FRONT LEGS (2-bone each for quadruped_legs preset, knee bent forward for IK hint)
            {"bone": "leg_front_upper_L", "parent": "chest", "head": [-0.1, 0.5, 0.45], "tail": [-0.12, 0.55, 0.22]},
            {"bone": "leg_front_lower_L", "parent": "leg_front_upper_L", "head": [-0.12, 0.55, 0.22], "tail": [-0.12, 0.52, 0.05]},
            {"bone": "foot_front_L", "parent": "leg_front_lower_L", "head": [-0.12, 0.52, 0.05], "tail": [-0.12, 0.6, 0]},

            {"bone": "leg_front_upper_R", "mirror": "leg_front_upper_L"},
            {"bone": "leg_front_lower_R", "mirror": "leg_front_lower_L"},
            {"bone": "foot_front_R", "mirror": "foot_front_L"},

            # BACK LEGS (2-bone each, knee bent forward for IK hint)
            {"bone": "leg_back_upper_L", "parent": "pelvis", "head": [-0.1, -0.05, 0.38], "tail": [-0.12, 0.0, 0.2]},
            {"bone": "leg_back_lower_L", "parent": "leg_back_upper_L", "head": [-0.12, 0.0, 0.2], "tail": [-0.12, -0.03, 0.05]},
            {"bone": "foot_back_L", "parent": "leg_back_lower_L", "head": [-0.12, -0.03, 0.05], "tail": [-0.12, 0.05, 0]},

            {"bone": "leg_back_upper_R", "mirror": "leg_back_upper_L"},
            {"bone": "leg_back_lower_R", "mirror": "leg_back_lower_L"},
            {"bone": "foot_back_R", "mirror": "foot_back_L"},

            # TAIL - 5 bones for N-bone IK testing
            {"bone": "tail_01", "parent": "pelvis", "head": [0, -0.05, 0.38], "tail": [0, -0.2, 0.35]},
            {"bone": "tail_02", "parent": "tail_01", "head": [0, -0.2, 0.35], "tail": [0, -0.35, 0.3]},
            {"bone": "tail_03", "parent": "tail_02", "head": [0, -0.35, 0.3], "tail": [0, -0.5, 0.25]},
            {"bone": "tail_04", "parent": "tail_03", "head": [0, -0.5, 0.25], "tail": [0, -0.65, 0.2]},
            {"bone": "tail_05", "parent": "tail_04", "head": [0, -0.65, 0.2], "tail": [0, -0.8, 0.15]},
        ],

        "parts": {
            "pelvis": {
                "bone": "pelvis",
                "base": "octagon(8)",
                "base_radius": 0.1,
                "steps": [
                    {"extrude": 0.08, "scale": 1.1},      # hip bulge
                    {"extrude": 0.07, "scale": 1.0},      # hip body
                ],
                "cap_start": True,
                "cap_end": False
            },

            "spine_01": {
                "bone": "spine_01",
                "base": "octagon(8)",
                "base_radius": 0.09,
                "steps": [
                    {"extrude": 0.12, "scale": 1.05},
                ],
                "cap_start": False,
                "cap_end": False
            },

            "spine_02": {
                "bone": "spine_02",
                "base": "octagon(8)",
                "base_radius": 0.095,
                "steps": [
                    {"extrude": 0.12, "scale": 1.0},
                ],
                "cap_start": False,
                "cap_end": False
            },

            "spine_03": {
                "bone": "spine_03",
                "base": "octagon(8)",
                "base_radius": 0.095,
                "steps": [
                    {"extrude": 0.12, "scale": 1.05},
                ],
                "cap_start": False,
                "cap_end": False
            },

            "chest": {
                "bone": "chest",
                "base": "octagon(8)",
                "base_radius": 0.1,
                "steps": [
                    {"extrude": 0.09, "scale": 1.1},      # chest bulge
                ],
                "cap_start": False,
                "cap_end": False
            },

            "neck": {
                "bone": "neck",
                "base": "octagon(8)",
                "base_radius": 0.07,
                "steps": [
                    {"extrude": 0.08, "scale": 1.1},      # neck base
                    {"extrude": 0.1, "scale": 0.85},      # neck taper
                ],
                "cap_start": False,
                "cap_end": False
            },

            "head": {
                "bone": "head",
                "base": "octagon(8)",
                "base_radius": 0.06,
                "steps": [
                    {"extrude": 0.04, "scale": 1.3},      # skull bulge
                    {"extrude": 0.1, "scale": 1.0},       # skull body
                    {"extrude": 0.06, "scale": 0.7},      # snout
                ],
                "cap_start": False,
                "cap_end": True
            },

            # FRONT LEGS
            "leg_front_upper_L": {
                "bone": "leg_front_upper_L",
                "base": "hexagon(6)",
                "base_radius": 0.04,
                "steps": [
                    {"extrude": 0.03, "scale": 1.2},      # shoulder
                    {"extrude": 0.17, "scale": 0.85},     # upper leg
                ],
                "cap_start": True,
                "cap_end": False
            },

            "leg_front_lower_L": {
                "bone": "leg_front_lower_L",
                "base": "hexagon(6)",
                "base_radius": 0.034,
                "steps": [
                    {"extrude": 0.02, "scale": 1.1},      # knee
                    {"extrude": 0.13, "scale": 0.8},      # lower leg
                ],
                "cap_start": False,
                "cap_end": False
            },

            "foot_front_L": {
                "bone": "foot_front_L",
                "base": "square(4)",
                "base_radius": 0.03,
                "steps": [
                    {"extrude": 0.04, "scale": 1.3},      # ankle
                    {"extrude": 0.04, "scale": 0.6},      # foot
                ],
                "cap_start": False,
                "cap_end": True
            },

            "leg_front_upper_R": {"mirror": "leg_front_upper_L"},
            "leg_front_lower_R": {"mirror": "leg_front_lower_L"},
            "foot_front_R": {"mirror": "foot_front_L"},

            # BACK LEGS
            "leg_back_upper_L": {
                "bone": "leg_back_upper_L",
                "base": "hexagon(6)",
                "base_radius": 0.045,
                "steps": [
                    {"extrude": 0.03, "scale": 1.15},     # hip
                    {"extrude": 0.12, "scale": 0.85},     # thigh
                ],
                "cap_start": True,
                "cap_end": False
            },

            "leg_back_lower_L": {
                "bone": "leg_back_lower_L",
                "base": "hexagon(6)",
                "base_radius": 0.038,
                "steps": [
                    {"extrude": 0.02, "scale": 1.1},      # knee
                    {"extrude": 0.11, "scale": 0.8},      # shin
                ],
                "cap_start": False,
                "cap_end": False
            },

            "foot_back_L": {
                "bone": "foot_back_L",
                "base": "square(4)",
                "base_radius": 0.032,
                "steps": [
                    {"extrude": 0.04, "scale": 1.3},      # ankle
                    {"extrude": 0.04, "scale": 0.6},      # foot
                ],
                "cap_start": False,
                "cap_end": True
            },

            "leg_back_upper_R": {"mirror": "leg_back_upper_L"},
            "leg_back_lower_R": {"mirror": "leg_back_lower_L"},
            "foot_back_R": {"mirror": "foot_back_L"},

            # TAIL - 5 segments tapering to tip
            "tail_01": {
                "bone": "tail_01",
                "base": "hexagon(6)",
                "base_radius": 0.06,
                "steps": [
                    {"extrude": 0.15, "scale": 0.85},
                ],
                "cap_start": True,
                "cap_end": False
            },

            "tail_02": {
                "bone": "tail_02",
                "base": "hexagon(6)",
                "base_radius": 0.051,
                "steps": [
                    {"extrude": 0.15, "scale": 0.85},
                ],
                "cap_start": False,
                "cap_end": False
            },

            "tail_03": {
                "bone": "tail_03",
                "base": "hexagon(6)",
                "base_radius": 0.043,
                "steps": [
                    {"extrude": 0.15, "scale": 0.85},
                ],
                "cap_start": False,
                "cap_end": False
            },

            "tail_04": {
                "bone": "tail_04",
                "base": "hexagon(6)",
                "base_radius": 0.037,
                "steps": [
                    {"extrude": 0.15, "scale": 0.8},
                ],
                "cap_start": False,
                "cap_end": False
            },

            "tail_05": {
                "bone": "tail_05",
                "base": "square(4)",
                "base_radius": 0.03,
                "steps": [
                    {"extrude": 0.1, "scale": 0.6},
                    {"extrude": 0.05, "scale": 0.3},      # tail tip
                ],
                "cap_start": False,
                "cap_end": True
            },
        }
    }
}
