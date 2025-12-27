---
name: Multiplayer Rendering Patterns
description: This skill should be used when the user asks about "split screen", "local multiplayer", "player_count FFI", "local_player_mask", "multiplayer camera", "same screen multiplayer", "asymmetric multiplayer", "couch co-op", "viewport multiplayer", "2-player split", "4-player screen", or needs implementation patterns for rendering multiplayer games on Nethercore ZX.
version: 0.1.0
---

# Multiplayer Rendering Patterns

Implementation patterns for rendering multiplayer games on Nethercore ZX. This skill covers the critical FFI functions, determinism rules, and rendering strategies for split-screen, same-screen, and asymmetric multiplayer.

## Critical Rule: update() vs render() Safety

The most important rule for multiplayer rendering:

| Function | `update()` | `render()` |
|----------|------------|------------|
| `player_count()` | SAFE | SAFE |
| `local_player_mask()` | NEVER | SAFE |
| `viewport()` | N/A | SAFE |

**Why?**
- `update()` runs on ALL clients with synchronized inputs. It must produce identical results everywhere for rollback to work.
- `render()` runs only on THIS client. Visual differences between clients are fine.

`player_count()` returns the same value on all clients (e.g., 2 for a 2-player game). Safe anywhere.

`local_player_mask()` returns DIFFERENT values per client. Client A might have player 1 local (mask `0b01`), while Client B has player 2 local (mask `0b10`). Using this in `update()` causes desync.

## Session FFI Functions

```rust
/// Returns player count (1-4). SAME on all clients.
fn player_count() -> u32;

/// Returns bitmask of local players. DIFFERENT per client!
fn local_player_mask() -> u32;
```

Check if a specific player is local:

```rust
fn is_local(player_id: u32) -> bool {
    unsafe { (local_player_mask() & (1 << player_id)) != 0 }
}
```

Example session states:

| Setup | Client A | Client B |
|-------|----------|----------|
| 2P Online | `player_count()=2`, `local_player_mask()=0b01` | `player_count()=2`, `local_player_mask()=0b10` |
| 2P Local | `player_count()=2`, `local_player_mask()=0b11` | N/A |
| 4P Mixed | `player_count()=4`, `local_player_mask()=0b0011` | `player_count()=4`, `local_player_mask()=0b1100` |

## Viewport FFI

```rust
/// Set rendering viewport (split-screen regions)
fn viewport(x: u32, y: u32, width: u32, height: u32);

/// Reset to fullscreen (960x540)
fn viewport_clear();
```

The viewport clips all rendering and adjusts camera aspect ratio automatically.

## Pattern 1: Split-Screen (Local Multiplayer)

Each local player gets their own viewport with independent camera.

```rust
#[no_mangle]
pub extern "C" fn render() {
    let count = unsafe { player_count() };
    let local_mask = unsafe { local_player_mask() };

    // Determine layout based on local player count
    let local_count = local_mask.count_ones();

    let mut viewport_idx = 0;
    for player_id in 0..count {
        if (local_mask & (1 << player_id)) != 0 {
            // Set viewport for this local player
            set_player_viewport(viewport_idx, local_count);

            // Set camera to follow this player
            let pos = GAME.players[player_id as usize].position;
            unsafe {
                camera_set(
                    pos.x, pos.y + 5.0, pos.z + 10.0,  // behind and above
                    pos.x, pos.y, pos.z                 // look at player
                );
            }

            // Render scene for this viewport
            unsafe { draw_env(); }
            draw_scene();
            draw_player_hud(player_id);

            viewport_idx += 1;
        }
    }

    // Reset viewport for shared UI (pause menu, etc.)
    unsafe { viewport_clear(); }
    draw_shared_ui();
}

fn set_player_viewport(idx: u32, total: u32) {
    // See references/viewport-layouts.md for all configurations
    match (total, idx) {
        // 2-player horizontal split
        (2, 0) => unsafe { viewport(0, 0, 480, 540) },
        (2, 1) => unsafe { viewport(480, 0, 480, 540) },
        // 4-player quadrants
        (4, 0) => unsafe { viewport(0, 0, 480, 270) },
        (4, 1) => unsafe { viewport(480, 0, 480, 270) },
        (4, 2) => unsafe { viewport(0, 270, 480, 270) },
        (4, 3) => unsafe { viewport(480, 270, 480, 270) },
        // Single player or 3-player layouts
        _ => unsafe { viewport(0, 0, 960, 540) },
    }
}
```

## Pattern 2: Same-Screen (Shared Camera)

All players share one camera. Common for brawlers, sports, co-op adventures.

```rust
#[no_mangle]
pub extern "C" fn render() {
    // Calculate camera center from all player positions
    let center = calculate_player_center();
    let zoom = calculate_zoom_for_players();

    unsafe {
        camera_set(
            center.x, center.y + zoom * 0.5, center.z + zoom,
            center.x, center.y, center.z
        );
        draw_env();
    }

    draw_scene();

    // Draw indicators for players at screen edges
    draw_offscreen_indicators();

    // Draw HUD elements for all players
    draw_all_player_huds();
}

fn calculate_player_center() -> Vec3 {
    let count = unsafe { player_count() } as usize;
    let mut sum = Vec3::ZERO;
    for i in 0..count {
        sum += GAME.players[i].position;
    }
    sum / count as f32
}

fn calculate_zoom_for_players() -> f32 {
    // Find bounding box of all players
    let count = unsafe { player_count() } as usize;
    let mut min = GAME.players[0].position;
    let mut max = min;

    for i in 1..count {
        let p = GAME.players[i].position;
        min = min.min(p);
        max = max.max(p);
    }

    let spread = (max - min).length();
    // Minimum zoom + spread-based zoom
    10.0 + spread * 0.5
}
```

## Pattern 3: Asymmetric (Role-Based Views)

Different players see different views based on their role.

```rust
#[no_mangle]
pub extern "C" fn render() {
    let local_mask = unsafe { local_player_mask() };

    // Check which role this client controls
    if (local_mask & 1) != 0 {
        // Player 0: First-person hunter view
        render_hunter_view();
    } else if (local_mask & 2) != 0 {
        // Player 1: Top-down commander view
        render_commander_view();
    }
}

fn render_hunter_view() {
    let player = &GAME.players[0];
    unsafe {
        // First-person camera
        camera_set(
            player.position.x, player.position.y + 1.7, player.position.z,
            player.position.x + player.facing.x,
            player.position.y + 1.7,
            player.position.z + player.facing.z
        );
        camera_fov(90.0);
        draw_env();
    }
    draw_scene();
    draw_hunter_hud();
}

fn render_commander_view() {
    unsafe {
        // Top-down orthographic-style view
        camera_set(
            GAME.map_center.x, 50.0, GAME.map_center.z,
            GAME.map_center.x, 0.0, GAME.map_center.z
        );
        camera_fov(30.0);
        draw_env();
    }
    draw_scene();
    draw_unit_markers();
    draw_commander_hud();
}
```

## Correct Input Handling in update()

Reading input for ALL players in update() is safe because inputs are synchronized:

```rust
#[no_mangle]
pub extern "C" fn update() {
    let count = unsafe { player_count() };

    // Process input for ALL players (deterministic)
    for player_id in 0..count {
        process_player_input(player_id);
    }

    // Update game state (deterministic)
    update_physics();
    update_ai();
    check_collisions();
}

fn process_player_input(player_id: u32) {
    // These functions read synchronized input - SAFE in update()
    let move_x = unsafe { left_stick_x(player_id) };
    let move_y = unsafe { left_stick_y(player_id) };
    let jump = unsafe { button_pressed(player_id, button::A) };

    // Apply to game state
    GAME.players[player_id as usize].velocity.x = move_x * MOVE_SPEED;
    if jump != 0 && GAME.players[player_id as usize].grounded {
        GAME.players[player_id as usize].velocity.y = JUMP_FORCE;
    }
}
```

## Common Mistakes

**WRONG - Using local_player_mask in update():**
```rust
fn update() {
    let mask = local_player_mask();  // DESYNC! Different per client
    if (mask & 1) != 0 {
        // Only runs on some clients - breaks determinism
    }
}
```

**WRONG - Skipping remote player input:**
```rust
fn update() {
    let mask = local_player_mask();
    for i in 0..player_count() {
        if (mask & (1 << i)) != 0 {  // DESYNC!
            process_input(i);  // Remote players never updated
        }
    }
}
```

**CORRECT - Process all players, render local:**
```rust
fn update() {
    for i in 0..player_count() {
        process_input(i);  // All players, deterministic
    }
}

fn render() {
    let mask = local_player_mask();  // OK in render
    // Use mask for viewport/camera decisions
}
```

## Integration with multiplayer-design

This skill covers **implementation patterns**. For **theoretical foundations**, see the `multiplayer-design` skill which covers:
- Rollback netcode fundamentals
- Determinism requirements
- State serialization
- Testing strategies

## Additional Resources

- **`references/viewport-layouts.md`** - All viewport configurations for 1-4 players
