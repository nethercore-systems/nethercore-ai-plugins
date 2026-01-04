# Wood Plank Texture
# A stylized wood grain pattern with warm brown tones
# Size: 256x256 RGB PNG

TEXTURE = {
    "texture": {
        "name": "wood_plank",
        "size": [256, 256],

        "layers": [
            # Base wood color via gradient
            {
                "type": "solid",
                "color": 0.5
            },
            # Wood grain rings
            {
                "type": "wood_grain",
                "ring_count": 12,
                "distortion": 0.4,
                "seed": 42,
                "blend": "multiply",
                "opacity": 0.6
            },
            # Subtle noise for texture
            {
                "type": "noise",
                "noise_type": "perlin",
                "scale": 0.15,
                "octaves": 3,
                "seed": 123,
                "blend": "soft_light",
                "opacity": 0.3
            },
            # Fine grain detail
            {
                "type": "noise",
                "noise_type": "perlin",
                "scale": 0.4,
                "octaves": 2,
                "seed": 456,
                "blend": "overlay",
                "opacity": 0.15
            }
        ],

        # Warm brown color ramp
        "color_ramp": [
            "#4A3728",  # Dark brown (shadows)
            "#6B4423",  # Medium brown
            "#8B4513",  # Saddle brown
            "#A0522D",  # Sienna
            "#B8732D"   # Light brown (highlights)
        ],

        "output": {
            "format": "png",
            "channels": "rgb",
            "size": [256, 256]
        }
    }
}
