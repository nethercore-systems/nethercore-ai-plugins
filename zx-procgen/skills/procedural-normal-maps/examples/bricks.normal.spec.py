# Brick Wall Normal Map
# Generates height-based brick pattern and converts to tangent-space normals
# Size: 256x256 RGB PNG

NORMAL = {
    "normal": {
        "name": "brick_wall",
        "size": [256, 256],
        "method": "from_pattern",

        "pattern": {
            "type": "bricks",
            "brick_size": [64, 32],      # [width, height] in pixels
            "mortar_width": 4,           # Gap between bricks
            "mortar_depth": 0.35,        # How deep the mortar appears (0-1)
            "brick_variation": 0.08,     # Height variation per brick
            "seed": 42
        },

        "processing": {
            "blur": 0.5,       # Slight blur for smoother normals
            "strength": 1.2    # Normal intensity (>1 = more pronounced)
        },

        "output": {
            "format": "png",
            "channels": "rgb"  # Standard tangent-space RGB normals
        }
    }
}
