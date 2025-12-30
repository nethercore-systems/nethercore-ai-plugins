# UI Sprite Generation

Generate UI elements: panels, buttons, health bars, and other interface components.

## 9-Slice Panel Generation

Generate UI panels that scale without stretching corners.

**Note:** ZX has no runtime 9-slice support; generate pre-scaled variants or implement slicing in game code.

```rust
fn generate_9slice_panel(
    width: u32, height: u32,
    corner_size: u32,
    border_color: u32,
    fill_color: u32,
    shadow_color: u32,
) -> TextureBuffer {
    let mut tex = TextureBuffer::new(width, height);
    tex.solid(fill_color);

    // Draw border (1px)
    for x in 0..width {
        tex.set(x, 0, border_color);              // Top
        tex.set(x, height - 1, shadow_color);     // Bottom (shadow)
    }
    for y in 0..height {
        tex.set(0, y, border_color);              // Left
        tex.set(width - 1, y, shadow_color);      // Right (shadow)
    }

    // Inner highlight (optional)
    for x in 1..(width - 1) {
        tex.set(x, 1, lighten(fill_color, 0.2));
    }

    tex
}

/// 9-slice regions for game code slicing
pub struct NineSlice {
    pub left: u32, pub right: u32, pub top: u32, pub bottom: u32,
}

impl NineSlice {
    pub fn uniform(border: u32) -> Self {
        Self { left: border, right: border, top: border, bottom: border }
    }
}
```

## Health Bar Generation

```rust
fn generate_health_bar(
    width: u32, height: u32,
    segments: u32,
    fill_color: u32,
    empty_color: u32,
    border_color: u32,
) -> TextureBuffer {
    let mut tex = TextureBuffer::new(width, height);
    tex.solid(border_color);

    let inner_width = width - 2;
    let segment_width = inner_width / segments;

    for seg in 0..segments {
        let x = 1 + seg * segment_width;
        // First half filled, second half empty (for demonstration)
        let color = if seg < segments / 2 { fill_color } else { empty_color };

        for sy in 1..(height - 1) {
            for sx in x..(x + segment_width - 1) {
                tex.set(sx, sy, color);
            }
        }
    }

    tex
}
```

## Button State Sheet

Generate sprite sheet with 4 states (normal, hover, pressed, disabled):

```rust
fn generate_button_sheet(
    button_width: u32, button_height: u32,
    base_color: u32,
    text_area: bool,
) -> TextureBuffer {
    // 4 states arranged horizontally
    let sheet_width = button_width * 4;
    let mut tex = TextureBuffer::new(sheet_width, button_height);

    let states = [
        (base_color, 0.0, 0.2),      // Normal: base, no darken, slight highlight
        (base_color, 0.0, 0.3),      // Hover: brighter highlight
        (darken(base_color, 0.15), 0.0, 0.0),  // Pressed: darker, no highlight
        (desaturate(base_color, 0.5), 0.2, 0.0), // Disabled: desaturated
    ];

    for (i, (color, shadow, highlight)) in states.iter().enumerate() {
        let x_offset = i as u32 * button_width;
        draw_button_state(&mut tex, x_offset, button_width, button_height,
                         *color, *shadow, *highlight);
    }

    tex
}
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

```rust
// In game code, select button state based on interaction
fn draw_button(x: f32, y: f32, state: ButtonState) {
    let state_offset = match state {
        ButtonState::Normal => 0,
        ButtonState::Hover => 1,
        ButtonState::Pressed => 2,
        ButtonState::Disabled => 3,
    };

    draw_sprite_region(
        BUTTON_SHEET,
        x, y,
        state_offset * BUTTON_WIDTH, 0,
        BUTTON_WIDTH, BUTTON_HEIGHT,
    );
}
```
