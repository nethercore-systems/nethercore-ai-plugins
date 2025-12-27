---
name: Split-Screen Rendering
description: This skill should be used when the user asks about "split screen", "local multiplayer viewport", "viewport", "viewport_clear", "2-player split", "4-player split", "couch co-op rendering", "local multiplayer screen", "screen divide", "multi-viewport", or needs implementation patterns for split-screen rendering and viewport management on Nethercore ZX.
version: 1.0.0
---

# Split-Screen Rendering

Implement local multiplayer split-screen using the ZX viewport FFI. This skill covers viewport setup, per-viewport camera, and shared UI overlay.

## Viewport FFI

```rust
/// Set the rendering viewport for subsequent draw calls.
/// All 3D/2D rendering clips to this region.
/// Camera aspect ratio automatically adjusts.
/// 2D coordinates become viewport-relative.
fn viewport(x: u32, y: u32, width: u32, height: u32);

/// Reset viewport to fullscreen (960x540).
fn viewport_clear();
```

## Screen Constants

```rust
const SCREEN_WIDTH: u32 = 960;
const SCREEN_HEIGHT: u32 = 540;
```

## Split Layouts

| Players | Layout | Dimensions | Aspect Ratio |
|---------|--------|------------|--------------|
| 2P Horizontal | Side-by-side | 480x540 each | 8:9 |
| 2P Vertical | Top/bottom | 960x270 each | 32:9 |
| 4P Grid | 2x2 quadrants | 480x270 each | 16:9 |

## 2-Player Horizontal Split

Best for racing, fighting, side-scrollers:

```rust
#[no_mangle]
pub extern "C" fn render() {
    // Player 1: left half
    unsafe { viewport(0, 0, 480, 540); }
    camera_set(p1_x, p1_y, p1_z, p1_tx, p1_ty, p1_tz);
    draw_env();
    draw_scene();

    // Player 2: right half
    unsafe { viewport(480, 0, 480, 540); }
    camera_set(p2_x, p2_y, p2_z, p2_tx, p2_ty, p2_tz);
    draw_env();
    draw_scene();

    // Reset for shared HUD
    unsafe { viewport_clear(); }
    draw_text_str("PAUSED", 400.0, 270.0, 32.0, 0xFFFFFFFF);
}
```

## 2-Player Vertical Split

Best for top-down, platformers:

```rust
// Player 1: top half
unsafe { viewport(0, 0, 960, 270); }
// ... camera and draw

// Player 2: bottom half
unsafe { viewport(0, 270, 960, 270); }
// ... camera and draw
```

## 4-Player Grid

Standard quadrant layout:

```rust
fn set_4p_viewport(player_idx: u32) {
    let (x, y) = match player_idx {
        0 => (0, 0),
        1 => (480, 0),
        2 => (0, 270),
        3 => (480, 270),
        _ => (0, 0),
    };
    unsafe { viewport(x, y, 480, 270); }
}
```

## Per-Viewport Camera

Each viewport needs its own camera setup. Call `camera_set` after each `viewport`:

```rust
fn render_player_viewport(player_id: u32) {
    let player = &GAME.players[player_id as usize];

    // Follow camera behind player
    unsafe {
        camera_set(
            player.x, player.y + 5.0, player.z + 10.0,  // Position
            player.x, player.y, player.z                 // Target
        );
    }

    unsafe { draw_env(); }
    draw_world();
    draw_player_hud(player_id);
}
```

## Shared UI Overlay

Reset viewport before drawing elements that span all viewports:

```rust
fn render() {
    render_all_player_viewports();

    // Shared pause menu, notifications, etc.
    unsafe { viewport_clear(); }

    if GAME.paused {
        draw_pause_menu();
    }
    draw_countdown_timer();
}
```

## Complete 2-Player Example

```rust
#[no_mangle]
pub extern "C" fn render() {
    // Player 1 viewport
    unsafe { viewport(0, 0, 480, 540); }
    render_player_view(0);

    // Player 2 viewport
    unsafe { viewport(480, 0, 480, 540); }
    render_player_view(1);

    // Divider line (optional)
    unsafe { viewport_clear(); }
    draw_rect(479.0, 0.0, 2.0, 540.0, 0x000000FF);

    // Shared HUD
    draw_score_display();
}

fn render_player_view(player_id: u32) {
    let p = &GAME.players[player_id as usize];

    unsafe {
        camera_set(p.x, p.y + 8.0, p.z + 12.0, p.x, p.y, p.z);
        draw_env();
    }

    draw_level();
    draw_all_players();
    draw_player_indicator(player_id);
}
```

## Performance Considerations

Each viewport requires separate rendering passes:

| Viewports | draw_env() | draw_mesh() | Impact |
|-----------|------------|-------------|--------|
| 1 | 1x | 1x | Baseline |
| 2 | 2x | 2x | ~2x work |
| 4 | 4x | 4x | ~4x work |

Optimize by:
- Simplifying environment effects for split-screen modes
- Using LOD (level of detail) for distant objects
- Reducing particle counts per viewport

## Dynamic Layout Selection

Choose layout based on local player count:

```rust
fn set_viewport_for_local(idx: u32, local_count: u32) {
    match local_count {
        1 => viewport(0, 0, 960, 540),
        2 => {
            let x = idx * 480;
            viewport(x, 0, 480, 540);
        }
        4 => {
            let x = (idx % 2) * 480;
            let y = (idx / 2) * 270;
            viewport(x, y, 480, 270);
        }
        _ => viewport(0, 0, 960, 540),
    }
}
```

## Integration with Multiplayer

For network multiplayer with local split-screen, see the `multiplayer-rendering` skill which covers:
- `player_count()` and `local_player_mask()` usage
- Determinism rules (viewport code in `render()` only)
- Mixed local/remote player handling

## Additional Resources

- **`nethercore/include/zx.rs`** lines 377-418 - Viewport FFI source
- **`multiplayer-rendering`** skill - Full multiplayer patterns
- **`camera-systems`** skill - Per-viewport camera setup
