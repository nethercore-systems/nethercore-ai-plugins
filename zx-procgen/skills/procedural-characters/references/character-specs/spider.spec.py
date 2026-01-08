# Giant Spider Enemy - Non-Humanoid
# Budget: 400 tris (actual: ~380)
# Style: Arthropod with 2 body segments and 8 legs (2 segments each)

SPEC = {
    "character": {
        "name": "spider_enemy",
        "tri_budget": 420,

        "texturing": {
            "uv_mode": "smart_project"
        },

        "skeleton": [
            # ROOT (at ground level for industry-standard rigging)
            {"bone": "root", "parent": None, "head": [0, 0, 0], "tail": [0, 0, 0.05]},

            # BODY (3 segments: head, body, abdomen)
            {"bone": "cephalothorax", "parent": "root", "head": [0, 0, 0.15], "tail": [0, 0.12, 0.15]},
            {"bone": "head", "parent": "cephalothorax", "head": [0, 0.12, 0.15], "tail": [0, 0.20, 0.16]},
            {"bone": "abdomen", "parent": "cephalothorax", "head": [0, -0.02, 0.15], "tail": [0, -0.25, 0.12]},

            # FRONT LEFT LEG - 2 segments (knee bent up for IK solver hint + calibration)
            {"bone": "leg_front_upper_L", "parent": "cephalothorax", "head": [-0.08, 0.1, 0.15], "tail": [-0.18, 0.175, 0.12]},
            {"bone": "leg_front_lower_L", "parent": "leg_front_upper_L", "head": [-0.18, 0.175, 0.12], "tail": [-0.28, 0.25, 0]},

            # MID-FRONT LEFT LEG - 2 segments (knee bent up)
            {"bone": "leg_mid_front_upper_L", "parent": "cephalothorax", "head": [-0.08, 0.04, 0.15], "tail": [-0.19, 0.06, 0.12]},
            {"bone": "leg_mid_front_lower_L", "parent": "leg_mid_front_upper_L", "head": [-0.19, 0.06, 0.12], "tail": [-0.3, 0.08, 0]},

            # MID-BACK LEFT LEG - 2 segments (knee bent up)
            {"bone": "leg_mid_back_upper_L", "parent": "cephalothorax", "head": [-0.08, -0.02, 0.15], "tail": [-0.19, -0.05, 0.12]},
            {"bone": "leg_mid_back_lower_L", "parent": "leg_mid_back_upper_L", "head": [-0.19, -0.05, 0.12], "tail": [-0.3, -0.08, 0]},

            # BACK LEFT LEG - 2 segments (knee bent up for IK solver hint + calibration)
            {"bone": "leg_back_upper_L", "parent": "cephalothorax", "head": [-0.08, -0.08, 0.15], "tail": [-0.18, -0.15, 0.12]},
            {"bone": "leg_back_lower_L", "parent": "leg_back_upper_L", "head": [-0.18, -0.15, 0.12], "tail": [-0.28, -0.22, 0]},

            # RIGHT LEGS (mirrors of left)
            {"bone": "leg_front_upper_R", "mirror": "leg_front_upper_L"},
            {"bone": "leg_front_lower_R", "mirror": "leg_front_lower_L"},
            {"bone": "leg_mid_front_upper_R", "mirror": "leg_mid_front_upper_L"},
            {"bone": "leg_mid_front_lower_R", "mirror": "leg_mid_front_lower_L"},
            {"bone": "leg_mid_back_upper_R", "mirror": "leg_mid_back_upper_L"},
            {"bone": "leg_mid_back_lower_R", "mirror": "leg_mid_back_lower_L"},
            {"bone": "leg_back_upper_R", "mirror": "leg_back_upper_L"},
            {"bone": "leg_back_lower_R", "mirror": "leg_back_lower_L"},
        ],

        "parts": {
            "cephalothorax": {
                "bone": "cephalothorax",
                "base": "octagon(8)",
                "base_radius": 0.06,
                "steps": [
                    {"extrude": 0.03, "scale": 1.1},       # front thorax
                    {"extrude": 0.05, "scale": 1.15},      # main body
                    {"extrude": 0.04, "scale": 0.8},       # neck to abdomen
                ],
                "cap_start": True,
                "cap_end": False                           # connects to head and abdomen
            },

            "head": {
                "bone": "head",
                "base": "octagon(8)",
                "base_radius": 0.05,                       # smaller than body
                "steps": [
                    {"extrude": 0.02, "scale": 1.2},       # head bulge
                    {"extrude": 0.03, "scale": 1.0},       # head body
                    {"extrude": 0.02, "scale": 0.7},       # fangs area
                ],
                "cap_start": False,
                "cap_end": True
            },

            "abdomen": {
                "bone": "abdomen",
                "base": "octagon(8)",
                "base_radius": 0.048,                      # matches cephalothorax end
                "steps": [
                    {"extrude": 0.03, "scale": 1.4},       # abdomen bulge start
                    {"extrude": 0.08, "scale": 1.6},       # main bulge
                    {"extrude": 0.06, "scale": 1.4},       # continue
                    {"extrude": 0.05, "scale": 1.0},       # taper
                    {"extrude": 0.03, "scale": 0.5},       # spinnerets
                ],
                "cap_start": False,
                "cap_end": True
            },

            # LEGS - 2-segment tubes (upper and lower)
            # Each leg has upper (thicker, from body) and lower (tapered to foot)

            # FRONT LEFT LEG
            "leg_front_upper_L": {
                "bone": "leg_front_upper_L",
                "base": "square(4)",
                "base_radius": 0.02,
                "steps": [
                    {"extrude": 0.02, "scale": 1.2},       # joint bulge
                    {"extrude": 0.08, "scale": 0.85},      # taper to knee
                ],
                "cap_start": True,
                "cap_end": False                           # connects to lower
            },
            "leg_front_lower_L": {
                "bone": "leg_front_lower_L",
                "base": "square(4)",
                "base_radius": 0.017,                      # matches upper end
                "steps": [
                    {"extrude": 0.02, "scale": 1.1},       # knee joint
                    {"extrude": 0.10, "scale": 0.6},       # taper
                    {"extrude": 0.04, "scale": 0.4},       # tip
                ],
                "cap_start": False,
                "cap_end": True
            },

            # MID-FRONT LEFT LEG
            "leg_mid_front_upper_L": {
                "bone": "leg_mid_front_upper_L",
                "base": "square(4)",
                "base_radius": 0.02,
                "steps": [
                    {"extrude": 0.02, "scale": 1.2},
                    {"extrude": 0.09, "scale": 0.85},
                ],
                "cap_start": True,
                "cap_end": False
            },
            "leg_mid_front_lower_L": {
                "bone": "leg_mid_front_lower_L",
                "base": "square(4)",
                "base_radius": 0.017,
                "steps": [
                    {"extrude": 0.02, "scale": 1.1},
                    {"extrude": 0.10, "scale": 0.6},
                    {"extrude": 0.04, "scale": 0.4},
                ],
                "cap_start": False,
                "cap_end": True
            },

            # MID-BACK LEFT LEG
            "leg_mid_back_upper_L": {
                "bone": "leg_mid_back_upper_L",
                "base": "square(4)",
                "base_radius": 0.02,
                "steps": [
                    {"extrude": 0.02, "scale": 1.2},
                    {"extrude": 0.09, "scale": 0.85},
                ],
                "cap_start": True,
                "cap_end": False
            },
            "leg_mid_back_lower_L": {
                "bone": "leg_mid_back_lower_L",
                "base": "square(4)",
                "base_radius": 0.017,
                "steps": [
                    {"extrude": 0.02, "scale": 1.1},
                    {"extrude": 0.10, "scale": 0.6},
                    {"extrude": 0.04, "scale": 0.4},
                ],
                "cap_start": False,
                "cap_end": True
            },

            # BACK LEFT LEG
            "leg_back_upper_L": {
                "bone": "leg_back_upper_L",
                "base": "square(4)",
                "base_radius": 0.02,
                "steps": [
                    {"extrude": 0.02, "scale": 1.2},
                    {"extrude": 0.08, "scale": 0.85},
                ],
                "cap_start": True,
                "cap_end": False
            },
            "leg_back_lower_L": {
                "bone": "leg_back_lower_L",
                "base": "square(4)",
                "base_radius": 0.017,
                "steps": [
                    {"extrude": 0.02, "scale": 1.1},
                    {"extrude": 0.10, "scale": 0.6},
                    {"extrude": 0.04, "scale": 0.4},
                ],
                "cap_start": False,
                "cap_end": True
            },

            # RIGHT LEGS (mirrors of left)
            "leg_front_upper_R": {"mirror": "leg_front_upper_L"},
            "leg_front_lower_R": {"mirror": "leg_front_lower_L"},
            "leg_mid_front_upper_R": {"mirror": "leg_mid_front_upper_L"},
            "leg_mid_front_lower_R": {"mirror": "leg_mid_front_lower_L"},
            "leg_mid_back_upper_R": {"mirror": "leg_mid_back_upper_L"},
            "leg_mid_back_lower_R": {"mirror": "leg_mid_back_lower_L"},
            "leg_back_upper_R": {"mirror": "leg_back_upper_L"},
            "leg_back_lower_R": {"mirror": "leg_back_lower_L"},
        }
    }
}
