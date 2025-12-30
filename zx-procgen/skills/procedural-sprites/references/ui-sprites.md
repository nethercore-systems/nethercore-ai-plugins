# UI Sprite Generation

Generate UI elements: panels, buttons, health bars, and other interface components.

## 9-Slice Panel Generation

Generate UI panels that scale without stretching corners.

**Note:** ZX has no runtime 9-slice support; generate pre-scaled variants or implement slicing in game code.

```python
import numpy as np
from PIL import Image
from dataclasses import dataclass

@dataclass
class NineSlice:
    """9-slice regions for game code slicing."""
    left: int
    right: int
    top: int
    bottom: int

    @classmethod
    def uniform(cls, border: int) -> "NineSlice":
        return cls(left=border, right=border, top=border, bottom=border)

def generate_9slice_panel(
    width: int,
    height: int,
    corner_size: int,
    border_color: int,
    fill_color: int,
    shadow_color: int
) -> Image.Image:
    """Generate a 9-slice UI panel."""
    # Convert colors from 0xRRGGBBAA to RGBA tuples
    def to_rgba(c: int) -> tuple:
        return ((c >> 24) & 0xFF, (c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF)

    fill_rgba = to_rgba(fill_color)
    border_rgba = to_rgba(border_color)
    shadow_rgba = to_rgba(shadow_color)

    # Create filled texture
    tex = np.full((height, width, 4), fill_rgba, dtype=np.uint8)

    # Draw border (1px) - vectorized
    tex[0, :] = border_rgba           # Top
    tex[height - 1, :] = shadow_rgba  # Bottom (shadow)
    tex[:, 0] = border_rgba           # Left
    tex[:, width - 1] = shadow_rgba   # Right (shadow)

    # Inner highlight (optional)
    highlight_rgba = tuple(min(255, int(c * 1.2)) for c in fill_rgba[:3]) + (fill_rgba[3],)
    tex[1, 1:width - 1] = highlight_rgba

    return Image.fromarray(tex)
```

## Health Bar Generation

```python
import numpy as np
from PIL import Image

def generate_health_bar(
    width: int,
    height: int,
    segments: int,
    fill_color: int,
    empty_color: int,
    border_color: int
) -> Image.Image:
    """Generate a segmented health bar sprite."""
    # Convert colors from 0xRRGGBBAA to RGBA tuples
    def to_rgba(c: int) -> tuple:
        return ((c >> 24) & 0xFF, (c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF)

    fill_rgba = to_rgba(fill_color)
    empty_rgba = to_rgba(empty_color)
    border_rgba = to_rgba(border_color)

    # Create border-filled texture
    tex = np.full((height, width, 4), border_rgba, dtype=np.uint8)

    inner_width = width - 2
    segment_width = inner_width // segments

    for seg in range(segments):
        x = 1 + seg * segment_width
        # First half filled, second half empty (for demonstration)
        color = fill_rgba if seg < segments // 2 else empty_rgba

        # Fill segment (vectorized)
        tex[1:height - 1, x:x + segment_width - 1] = color

    return Image.fromarray(tex)
```

## Button State Sheet

Generate sprite sheet with 4 states (normal, hover, pressed, disabled):

```python
import numpy as np
from PIL import Image

def generate_button_sheet(
    button_width: int,
    button_height: int,
    base_color: int,
    text_area: bool = False
) -> Image.Image:
    """Generate button sprite sheet with 4 states (normal, hover, pressed, disabled)."""
    # 4 states arranged horizontally
    sheet_width = button_width * 4
    tex = np.zeros((button_height, sheet_width, 4), dtype=np.uint8)

    def to_rgba(c: int) -> np.ndarray:
        return np.array([
            (c >> 24) & 0xFF, (c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF
        ], dtype=np.float32)

    def darken(rgba: np.ndarray, amount: float) -> np.ndarray:
        result = rgba.copy()
        result[:3] = np.clip(result[:3] * (1 - amount), 0, 255)
        return result

    def desaturate(rgba: np.ndarray, amount: float) -> np.ndarray:
        result = rgba.copy()
        gray = np.mean(result[:3])
        result[:3] = result[:3] * (1 - amount) + gray * amount
        return result

    base_rgba = to_rgba(base_color)

    # State definitions: (color_modifier, shadow_amount, highlight_amount)
    states = [
        (base_rgba, 0.0, 0.2),                      # Normal
        (base_rgba, 0.0, 0.3),                      # Hover
        (darken(base_rgba, 0.15), 0.0, 0.0),       # Pressed
        (desaturate(base_rgba, 0.5), 0.2, 0.0),    # Disabled
    ]

    for i, (color, shadow, highlight) in enumerate(states):
        x_offset = i * button_width
        draw_button_state(tex, x_offset, button_width, button_height,
                         color, shadow, highlight)

    return Image.fromarray(tex)

def draw_button_state(tex, x_offset, width, height, color, shadow, highlight):
    """Draw a single button state into the texture atlas."""
    # Fill base color
    tex[:, x_offset:x_offset + width] = color.astype(np.uint8)

    # Add highlight to top edge
    if highlight > 0:
        highlight_color = np.clip(color[:3] * (1 + highlight), 0, 255)
        tex[0, x_offset:x_offset + width, :3] = highlight_color.astype(np.uint8)
```

## Common UI Element Sizes

| Element | Typical Size | Notes |
|---------|--------------|-------|
| Icon | 16x16, 24x24, 32x32 | Power of 2 preferred |
| Button | 64x24, 96x32 | Wide for text |
| Health bar | 64x8, 128x12 | Wide and thin |
| Panel border | 4-8px | For 9-slice corners |
| Cursor | 16x16, 24x24 | With hotspot offset |

## Button Drawing in Game

```python
from enum import IntEnum

class ButtonState(IntEnum):
    NORMAL = 0
    HOVER = 1
    PRESSED = 2
    DISABLED = 3

BUTTON_WIDTH = 64
BUTTON_HEIGHT = 24
BUTTON_SHEET = 0  # Handle to loaded sprite sheet

def draw_button(x: float, y: float, state: ButtonState):
    """
    Draw button sprite from sheet at given position.

    In game code, select button state based on interaction.
    """
    state_offset = int(state)

    # In actual ZX game code, this would call:
    # draw_sprite_region(
    #     BUTTON_SHEET,
    #     x, y,
    #     state_offset * BUTTON_WIDTH, 0,  # src_x, src_y
    #     BUTTON_WIDTH, BUTTON_HEIGHT       # width, height
    # )
    pass
```
