# Brick Wall Texture
# Red brick wall with mortar joints
# Size: 256x256 RGB PNG

TEXTURE = {
    "texture": {
        "name": "brick_wall",
        "size": [256, 256],

        "layers": [
            # Base brick pattern
            {
                "type": "brick",
                "brick_width": 64,
                "brick_height": 32,
                "mortar_width": 4,
                "mortar_color": 0.4,
                "brick_color": 0.6,
                "variation": 0.15,
                "seed": 42
            },
            # Weathering noise (darker spots)
            {
                "type": "noise",
                "noise_type": "perlin",
                "scale": 0.08,
                "octaves": 3,
                "seed": 789,
                "blend": "multiply",
                "opacity": 0.25
            },
            # Surface texture
            {
                "type": "noise",
                "noise_type": "perlin",
                "scale": 0.3,
                "octaves": 2,
                "seed": 101,
                "blend": "overlay",
                "opacity": 0.2
            },
            # Slight color variation
            {
                "type": "noise",
                "noise_type": "voronoi",
                "scale": 0.02,
                "jitter": 0.8,
                "seed": 202,
                "blend": "soft_light",
                "opacity": 0.15
            }
        ],

        # Red brick color ramp
        "color_ramp": [
            "#3D2A2A",  # Dark mortar/shadows
            "#6B4444",  # Dark brick
            "#8B4444",  # Medium brick
            "#A05050",  # Standard brick red
            "#B86060",  # Light brick
            "#C87070"   # Highlight
        ],

        "output": {
            "format": "png",
            "channels": "rgb",
            "size": [256, 256]
        }
    }
}
