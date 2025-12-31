"""Generator library utilities.

This package contains shared utilities for procedural asset generation.
Copy the entire lib/ folder to your project's generator/ directory.
"""
# Note: bpy_utils and animation_utils require Blender
# Only import them when running inside Blender

try:
    from .texture_buffer import TextureBuffer
except ImportError:
    pass

try:
    from .sprite_utils import (
        get_palette, PALETTES,
        find_nearest_color, quantize_image,
        bayer_dither, floyd_steinberg_dither,
        create_sprite_sheet, split_sprite_sheet,
        add_outline, flip_horizontal, flip_vertical,
        save_sprite, load_sprite,
    )
except ImportError:
    pass

# bpy_utils and animation_utils only work inside Blender
# Import them directly in your scripts:
#   from lib.bpy_utils import clear_scene, export_glb
#   from lib.animation_utils import keyframe_location
