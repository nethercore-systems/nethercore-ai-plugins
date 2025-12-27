# Gap 9: Split-Screen / Viewport

**Status:** `[x]` Completed
**Priority:** MEDIUM
**Plugin:** nethercore-zx-game-design
**Type:** Skill

---

## Problem

FFI exists, NO multiplayer rendering guidance. Local multiplayer games need split-screen rendering, but no plugin covers viewport setup.

## FFI Functions (from zx.rs)

### viewport
```rust
/// Set the viewport for subsequent draw calls.
///
/// All 3D and 2D rendering will be clipped to this region.
/// Camera aspect ratio automatically adjusts to viewport dimensions.
/// 2D coordinates (draw_sprite, draw_text, etc.) become viewport-relative.
///
/// # Arguments
/// * `x` — Left edge in pixels (0-959)
/// * `y` — Top edge in pixels (0-539)
/// * `width` — Width in pixels (1-960)
/// * `height` — Height in pixels (1-540)
pub fn viewport(x: u32, y: u32, width: u32, height: u32);
```

### viewport_clear
```rust
/// Reset viewport to fullscreen (960×540).
///
/// Call this at the end of split-screen rendering to restore full-screen
/// coordinates for HUD elements or between frames.
pub fn viewport_clear();
```

## Example from zx.rs (2-player horizontal split)
```rust
// Player 1: left half
viewport(0, 0, 480, 540);
camera_set(p1_x, p1_y, p1_z, p1_tx, p1_ty, p1_tz);
draw_env();
draw_mesh(scene);

// Player 2: right half
viewport(480, 0, 480, 540);
camera_set(p2_x, p2_y, p2_z, p2_tx, p2_ty, p2_tz);
draw_env();
draw_mesh(scene);

// Reset for HUD (shared across both players)
viewport_clear();
draw_text_str("PAUSED", 400.0, 270.0, 32.0, 0xFFFFFFFF);
```

## Screen Constants
```rust
pub mod screen {
    pub const WIDTH: u32 = 960;
    pub const HEIGHT: u32 = 540;
}
```

## Common Split Layouts

| Players | Layout | Dimensions |
|---------|--------|------------|
| 2P Horizontal | Side by side | 480×540 each |
| 2P Vertical | Top/bottom | 960×270 each |
| 3P | One top, two bottom | 960×270 top, 480×270 each bottom |
| 4P Grid | 2×2 grid | 480×270 each |

## What's Missing

- Split-screen layout patterns with exact pixel values
- Per-viewport camera setup workflow
- UI overlay strategies (viewport_clear for shared HUD)
- Performance considerations (4 viewports = 4× draw calls)
- Border/divider rendering between viewports
- Aspect ratio handling per viewport

## Prompt for Implementation

```
Add skill "split-screen-rendering" to nethercore-zx-game-design. Triggers: "split
screen", "local multiplayer", "viewport", "2-player", "4-player local", "couch
co-op", "viewport_clear".

Cover:
1. viewport(x, y, width, height) and viewport_clear() FFI
2. Screen dimensions: 960×540 (screen::WIDTH, screen::HEIGHT)
3. Split layouts with exact pixel values:
   - 2P horizontal: viewport(0, 0, 480, 540) + viewport(480, 0, 480, 540)
   - 2P vertical: viewport(0, 0, 960, 270) + viewport(0, 270, 960, 270)
   - 4P grid: four 480×270 viewports
4. Per-viewport camera setup (camera_set after each viewport call)
5. Shared UI overlay (viewport_clear() before drawing HUD)
6. Performance: 4 viewports = 4× environment renders, 4× mesh draws
7. Include the example from zx.rs

Source: nethercore/include/zx.rs lines 377-418 (Viewport section)
Tie to multiplayer-design skill. ~800 words.
```

## Dependencies

- None

## Related Gaps

- Gap 17 (Camera) for per-viewport camera code
- Gap 20 (Multiplayer Rendering) for determinism rules
