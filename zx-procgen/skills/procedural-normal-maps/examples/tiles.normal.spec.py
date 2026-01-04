# Tile Floor Normal Map
# Square tiles with grout lines
# Size: 256x256 RGB PNG

NORMAL = {
    "normal": {
        "name": "tile_floor",
        "size": [256, 256],
        "method": "from_pattern",

        "pattern": {
            "type": "tiles",
            "tile_size": 64,        # Square tiles
            "gap_width": 4,         # Grout line width
            "gap_depth": 0.25,      # How recessed the grout appears
            "seed": 123
        },

        "processing": {
            "blur": 0.3,       # Minimal blur
            "strength": 1.0,   # Standard strength
            "invert": False
        },

        "output": {
            "format": "png",
            "channels": "rgb"
        }
    }
}
