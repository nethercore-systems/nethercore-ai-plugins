# Sprite Sheet Organization

Organize sprites into sheets for characters, animations, and palette swaps.

## Character Sprite Layout

Standard layout for character sprite sheets:

```python
from dataclasses import dataclass

@dataclass
class CharacterLayout:
    """Layout metadata for character sprite sheets."""
    sprite_size: tuple[int, int]
    directions: int
    frames_per_dir: int
    # Direction row indices (standard RPG order)
    down: int = 0
    left: int = 1
    right: int = 2
    up: int = 3

def generate_character_sheet_template(
    sprite_width: int,
    sprite_height: int,
    directions: int = 4,        # 4 or 8
    frames_per_dir: int = 4     # typically 4 (idle, walk1, walk2, walk3)
) -> tuple[int, int, CharacterLayout]:
    """
    Generate character sprite sheet layout.

    Rows: directions (down, left, right, up)
    Columns: animation frames

    Returns:
        (sheet_width, sheet_height, layout)
    """
    sheet_width = sprite_width * frames_per_dir
    sheet_height = sprite_height * directions

    layout = CharacterLayout(
        sprite_size=(sprite_width, sprite_height),
        directions=directions,
        frames_per_dir=frames_per_dir,
        down=0, left=1, right=2, up=3
    )

    return sheet_width, sheet_height, layout
```

## Palette Swaps

Generate color variants for enemy types:

```python
import numpy as np
from PIL import Image

def generate_palette_swap(
    source: Image.Image,
    source_palette: list[int],
    target_palette: list[int]
) -> Image.Image:
    """
    Generate palette swap variant of a sprite.

    Args:
        source: Source image
        source_palette: List of source colors (0xRRGGBBAA format)
        target_palette: List of target colors (same length as source_palette)

    Returns:
        New image with swapped colors
    """
    assert len(source_palette) == len(target_palette), "Palettes must have same length"

    result = np.array(source).copy()
    h, w = result.shape[:2]

    # Build color mapping dictionary
    # Convert 0xRRGGBBAA to (R, G, B, A) tuples for comparison
    def color_to_tuple(c: int) -> tuple:
        return ((c >> 24) & 0xFF, (c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF)

    palette_map = {
        color_to_tuple(s): color_to_tuple(t)
        for s, t in zip(source_palette, target_palette)
    }

    # Vectorized approach: create masks for each source color and apply replacements
    for src_color, tgt_color in palette_map.items():
        # Create mask where all channels match source color
        mask = np.all(result == src_color, axis=-1)
        result[mask] = tgt_color

    return Image.fromarray(result)
```

## Example: Enemy Variants

```python
from PIL import Image

base_slime = Image.open("slime_green.png")
green_palette = [0x22AA22FF, 0x118811FF, 0x005500FF]
red_palette = [0xAA2222FF, 0x881111FF, 0x550000FF]
blue_palette = [0x2222AAFF, 0x111188FF, 0x000055FF]

red_slime = generate_palette_swap(base_slime, green_palette, red_palette)
blue_slime = generate_palette_swap(base_slime, green_palette, blue_palette)
```

## Common Sheet Layouts

| Type | Layout | Typical Size |
|------|--------|--------------|
| 4-dir character | 4 cols x 4 rows | 128x128 (32x32 sprites) |
| 8-dir character | 4 cols x 8 rows | 128x256 (32x32 sprites) |
| Attack anim | 6-8 cols x 1 row | 192x32 |
| Death anim | 4-6 cols x 1 row | 128x32 |
| Effect/particle | 4-8 cols x 1 row | Variable |

## Animation Frame Order

Standard RPG Maker convention:

| Row | Direction |
|-----|-----------|
| 0 | Down |
| 1 | Left |
| 2 | Right |
| 3 | Up |

| Column | Frame |
|--------|-------|
| 0 | Idle / Stand |
| 1 | Walk 1 |
| 2 | Walk 2 |
| 3 | Walk 3 |

## ZX Usage

```python
# ZX FFI usage example (pseudo-code for game runtime)
# This would be called from Rust/C game code, shown here for documentation

SPRITE_WIDTH = 32
SPRITE_HEIGHT = 32
CHARACTER_SHEET = 0  # Handle to loaded sprite sheet

def draw_character(x: float, y: float, direction: int, frame: int):
    """
    Draw character sprite from sheet at given position.

    Args:
        x, y: Screen position
        direction: Row index (0=down, 1=left, 2=right, 3=up)
        frame: Column index (animation frame)
    """
    # In actual ZX game code, this would call:
    # draw_sprite_region(
    #     CHARACTER_SHEET,
    #     x, y,
    #     frame * SPRITE_WIDTH,      # src_x
    #     direction * SPRITE_HEIGHT,  # src_y
    #     SPRITE_WIDTH, SPRITE_HEIGHT # width, height
    # )
    pass
```
