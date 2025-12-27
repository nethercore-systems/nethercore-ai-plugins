# Viewport Layout Reference

Complete viewport configurations for all player counts on ZX's 960x540 resolution.

## Screen Constants

```rust
const SCREEN_WIDTH: u32 = 960;
const SCREEN_HEIGHT: u32 = 540;
const HALF_WIDTH: u32 = 480;
const HALF_HEIGHT: u32 = 270;
```

## 2-Player Layouts

### Horizontal Split (Side-by-Side)
Best for games with horizontal movement (racing, fighting).

```
┌─────────────┬─────────────┐
│             │             │
│   Player 1  │   Player 2  │
│   480x540   │   480x540   │
│             │             │
└─────────────┴─────────────┘
```

```rust
fn layout_2p_horizontal(idx: u32) {
    match idx {
        0 => viewport(0, 0, 480, 540),
        1 => viewport(480, 0, 480, 540),
        _ => {}
    }
}
```

### Vertical Split (Top/Bottom)
Best for games with vertical movement (top-down, platformers).

```
┌─────────────────────────────┐
│          Player 1           │
│          960x270            │
├─────────────────────────────┤
│          Player 2           │
│          960x270            │
└─────────────────────────────┘
```

```rust
fn layout_2p_vertical(idx: u32) {
    match idx {
        0 => viewport(0, 0, 960, 270),
        1 => viewport(0, 270, 960, 270),
        _ => {}
    }
}
```

## 3-Player Layouts

### One Full + Two Split
Player 1 gets full top, players 2-3 share bottom.

```
┌─────────────────────────────┐
│          Player 1           │
│          960x270            │
├─────────────┬───────────────┤
│   Player 2  │    Player 3   │
│   480x270   │    480x270    │
└─────────────┴───────────────┘
```

```rust
fn layout_3p_one_two(idx: u32) {
    match idx {
        0 => viewport(0, 0, 960, 270),
        1 => viewport(0, 270, 480, 270),
        2 => viewport(480, 270, 480, 270),
        _ => {}
    }
}
```

### Three Column
Equal width columns (narrower aspect ratio).

```
┌─────────┬─────────┬─────────┐
│         │         │         │
│  P1     │   P2    │   P3    │
│ 320x540 │ 320x540 │ 320x540 │
│         │         │         │
└─────────┴─────────┴─────────┘
```

```rust
fn layout_3p_columns(idx: u32) {
    match idx {
        0 => viewport(0, 0, 320, 540),
        1 => viewport(320, 0, 320, 540),
        2 => viewport(640, 0, 320, 540),
        _ => {}
    }
}
```

## 4-Player Layouts

### Standard Quadrants
Most common 4-player layout.

```
┌─────────────┬─────────────┐
│   Player 1  │   Player 2  │
│   480x270   │   480x270   │
├─────────────┼─────────────┤
│   Player 3  │   Player 4  │
│   480x270   │   480x270   │
└─────────────┴─────────────┘
```

```rust
fn layout_4p_quadrants(idx: u32) {
    match idx {
        0 => viewport(0, 0, 480, 270),
        1 => viewport(480, 0, 480, 270),
        2 => viewport(0, 270, 480, 270),
        3 => viewport(480, 270, 480, 270),
        _ => {}
    }
}
```

## Dynamic Layout Function

Complete layout function supporting all configurations:

```rust
/// Set viewport for a local player
/// idx: which local viewport slot (0-3)
/// total: total local players on this client
/// style: layout preference
pub fn set_viewport(idx: u32, total: u32, style: LayoutStyle) {
    match (total, style) {
        (1, _) => viewport(0, 0, 960, 540),

        (2, LayoutStyle::Horizontal) => {
            let x = idx * 480;
            viewport(x, 0, 480, 540);
        }
        (2, LayoutStyle::Vertical) => {
            let y = idx * 270;
            viewport(0, y, 960, 270);
        }

        (3, LayoutStyle::OneTwo) => {
            match idx {
                0 => viewport(0, 0, 960, 270),
                1 => viewport(0, 270, 480, 270),
                2 => viewport(480, 270, 480, 270),
                _ => {}
            }
        }
        (3, LayoutStyle::Columns) => {
            viewport(idx * 320, 0, 320, 540);
        }

        (4, _) => {
            let x = (idx % 2) * 480;
            let y = (idx / 2) * 270;
            viewport(x, y, 480, 270);
        }

        _ => viewport(0, 0, 960, 540),
    }
}

pub enum LayoutStyle {
    Horizontal,  // Side by side
    Vertical,    // Top/bottom
    OneTwo,      // One full + two half
    Columns,     // Equal columns
}
```

## Mixed Local/Remote Examples

When some players are local and some remote:

```rust
fn render() {
    let total_players = player_count();
    let local_mask = local_player_mask();
    let local_count = local_mask.count_ones();

    let mut local_idx = 0;
    for player_id in 0..total_players {
        if (local_mask & (1 << player_id)) != 0 {
            // This player is local, render their viewport
            set_viewport(local_idx, local_count, LayoutStyle::Horizontal);
            render_player_view(player_id);
            local_idx += 1;
        }
        // Remote players: no viewport, their client renders them
    }

    viewport_clear();
    render_shared_ui();
}
```

| Scenario | player_count | local_mask | local_count | Viewports |
|----------|--------------|------------|-------------|-----------|
| 2P local couch | 2 | 0b11 | 2 | 2 side-by-side |
| 2P online | 2 | 0b01 | 1 | 1 fullscreen |
| 4P: 2 local, 2 remote | 4 | 0b0011 | 2 | 2 side-by-side |
| 4P: all local | 4 | 0b1111 | 4 | 4 quadrants |

## Aspect Ratio Considerations

| Layout | Aspect Ratio | Best For |
|--------|--------------|----------|
| Full (960x540) | 16:9 | Single player |
| Half horizontal (480x540) | 8:9 (near square) | Side-by-side racing |
| Half vertical (960x270) | 32:9 (ultra-wide) | Top-down games |
| Quadrant (480x270) | 16:9 | 4-player |
| Third column (320x540) | 9:16 (portrait) | Unusual, avoid |

Camera FOV adjustments may be needed for extreme aspect ratios:

```rust
fn adjusted_fov(base_fov: f32, viewport_width: u32, viewport_height: u32) -> f32 {
    let aspect = viewport_width as f32 / viewport_height as f32;
    if aspect < 1.0 {
        // Portrait/narrow - increase vertical FOV
        base_fov * (1.0 / aspect).sqrt()
    } else {
        base_fov
    }
}
```
