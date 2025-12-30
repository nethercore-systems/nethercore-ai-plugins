---
name: Multiplayer Patterns for ZX
description: |
  Use this skill for ZX-SPECIFIC multiplayer implementation - netcode, determinism, and viewport management. Trigger phrases: "GGRS", "rollback netcode", "determinism rules", "desync", "split screen rendering", "viewport FFI", "player_count()", "local_player_mask()", "sync test".

  This skill provides ZX IMPLEMENTATION - GGRS integration, determinism requirements, viewport rendering, state serialization.

  For GAME DESIGN (co-op patterns, competitive balance, mode ideas): use game-design:multiplayer-design instead.
version: 2.0.1
---

# Multiplayer Patterns for Nethercore ZX

Comprehensive guidance for designing and implementing multiplayer games with GGRS rollback netcode. Covers determinism requirements, state design, viewport management, and rendering strategies.

## ZX Multiplayer Capabilities

| Feature | Value |
|---------|-------|
| Max Players | 4 (any mix of local + remote) |
| Netcode | GGRS deterministic rollback |
| Rollback Window | 8 frames typical |
| Rollback Cost | ~2ms for 8 frames (at 60fps) |
| State Snapshot | ~0.25ms per save (50KB state) |
| Screen Resolution | 960x540 |

---

## Part 1: Netcode Fundamentals

### How GGRS Rollback Works

1. **Input Prediction:** When remote input hasn't arrived, predict it (usually "same as last frame")
2. **State Advance:** Run `update()` with predicted inputs
3. **Correction:** When actual input arrives, if it differs from prediction:
   - Restore previous state snapshot
   - Re-run `update()` with correct inputs
   - Fast-forward to current frame
4. **Smooth Play:** Visual result appears seamless to players

### Why Determinism Matters

For rollback to work, re-running the same inputs **must** produce identical results. Any non-determinism causes **desync** — players see different game states.

**Desync = broken multiplayer.**

### Determinism Requirements

| System | Requirement |
|--------|-------------|
| Physics | Fixed-point math OR identical floating-point behavior |
| AI | Deterministic decision making, seeded random |
| Animations | Frame-based, not time-based |
| Spawning | Seeded random for positions/timing |
| All gameplay logic | Same inputs → same outputs, always |

### What Breaks Determinism

**Forbidden in `update()`:**
- `std::time` / system clock
- `rand()` without seeding
- Hash map iteration (order varies by platform)
- Floating-point edge cases (NaN, denormals)
- External I/O

**Use Instead:**
- `tick_count()` FFI for game time
- `random()` FFI for seeded RNG
- Fixed iteration order (arrays, sorted collections)
- Fixed-point math for critical calculations

---

## Part 2: State Design for Rollback

### Minimize State Size

Smaller state = faster rollback. **Target:** < 100 KB for game state

**Good state design:**
```
Game State (~5 KB):
├── Players: 4 × 500 bytes = 2 KB
│   ├── Position (12 bytes)
│   ├── Velocity (12 bytes)
│   ├── Health/damage (8 bytes)
│   ├── State enum (4 bytes)
│   └── Animation frame (4 bytes)
├── Entities: 20 × 100 bytes = 2 KB
├── World state: 500 bytes
├── RNG state: 64 bytes
└── Input buffer: 500 bytes
```

**Exclude from rollback state:**
- Asset references (immutable, in ROM)
- Cached calculations (can recompute)
- Visual-only data (particles, screen shake)
- Audio state (not gameplay-affecting)

### Separate Rollback vs. Non-Rollback Data

```rust
// MUST be in rollback state
struct GameState {
    players: [PlayerState; 4],
    entities: Vec<Entity>,
    rng_state: u64,
    frame_count: u32,
}

// NOT in rollback state (visual only)
struct VisualState {
    particles: Vec<Particle>,
    screen_shake: f32,
    audio_playing: Vec<SoundId>,
}
```

---

## Part 3: Session FFI Functions

### Critical Rule: update() vs render() Safety

| Function | `update()` | `render()` |
|----------|------------|------------|
| `player_count()` | SAFE | SAFE |
| `local_player_mask()` | NEVER | SAFE |
| `viewport()` | N/A | SAFE |

**Why?**
- `update()` runs on ALL clients with synchronized inputs. It must produce identical results everywhere.
- `render()` runs only on THIS client. Visual differences between clients are fine.

### FFI Functions

```rust
/// Returns player count (1-4). SAME on all clients.
fn player_count() -> u32;

/// Returns bitmask of local players. DIFFERENT per client!
fn local_player_mask() -> u32;

/// Set rendering viewport (split-screen regions)
fn viewport(x: u32, y: u32, width: u32, height: u32);

/// Reset to fullscreen (960x540)
fn viewport_clear();
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

---

## Part 4: Viewport Management

### Split Layouts

| Players | Layout | Dimensions | Aspect Ratio |
|---------|--------|------------|--------------|
| 2P Horizontal | Side-by-side | 480x540 each | 8:9 |
| 2P Vertical | Top/bottom | 960x270 each | 32:9 |
| 4P Grid | 2x2 quadrants | 480x270 each | 16:9 |

### 2-Player Horizontal Split

```rust
#[no_mangle]
pub extern "C" fn render() {
    // Player 1: left half
    unsafe { viewport(0, 0, 480, 540); }
    render_player_view(0);

    // Player 2: right half
    unsafe { viewport(480, 0, 480, 540); }
    render_player_view(1);

    // Reset for shared HUD
    unsafe { viewport_clear(); }
    draw_shared_ui();
}
```

### 4-Player Quadrants

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

### Dynamic Layout Selection

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

---

## Part 5: Rendering Patterns

### Pattern 1: Split-Screen (Local Multiplayer)

Each local player gets their own viewport with independent camera:

```rust
#[no_mangle]
pub extern "C" fn render() {
    let count = unsafe { player_count() };
    let local_mask = unsafe { local_player_mask() };
    let local_count = local_mask.count_ones();

    let mut viewport_idx = 0;
    for player_id in 0..count {
        if (local_mask & (1 << player_id)) != 0 {
            set_player_viewport(viewport_idx, local_count);

            let pos = GAME.players[player_id as usize].position;
            unsafe {
                camera_set(
                    pos.x, pos.y + 5.0, pos.z + 10.0,
                    pos.x, pos.y, pos.z
                );
                draw_env();
            }
            draw_scene();
            draw_player_hud(player_id);

            viewport_idx += 1;
        }
    }

    unsafe { viewport_clear(); }
    draw_shared_ui();
}
```

### Pattern 2: Same-Screen (Shared Camera)

All players share one camera. Common for brawlers, sports, co-op:

```rust
#[no_mangle]
pub extern "C" fn render() {
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
    draw_offscreen_indicators();
    draw_all_player_huds();
}
```

### Pattern 3: Asymmetric (Role-Based Views)

Different players see different views based on their role:

```rust
#[no_mangle]
pub extern "C" fn render() {
    let local_mask = unsafe { local_player_mask() };

    if (local_mask & 1) != 0 {
        render_hunter_view();  // First-person
    } else if (local_mask & 2) != 0 {
        render_commander_view();  // Top-down
    }
}
```

---

## Part 6: Input Handling

### Correct Input Handling in update()

Reading input for ALL players in `update()` is safe because inputs are synchronized:

```rust
#[no_mangle]
pub extern "C" fn update() {
    let count = unsafe { player_count() };

    // Process input for ALL players (deterministic)
    for player_id in 0..count {
        process_player_input(player_id);
    }

    update_physics();
    update_ai();
    check_collisions();
}

fn process_player_input(player_id: u32) {
    let move_x = unsafe { left_stick_x(player_id) };
    let move_y = unsafe { left_stick_y(player_id) };
    let jump = unsafe { button_pressed(player_id, button::A) };

    GAME.players[player_id as usize].velocity.x = move_x * MOVE_SPEED;
    if jump != 0 && GAME.players[player_id as usize].grounded {
        GAME.players[player_id as usize].velocity.y = JUMP_FORCE;
    }
}
```

### Input Delay

Intentional input delay improves online experience:
- **3 frames:** Minimal perceivable delay
- **4-5 frames:** Good balance for most games
- **6+ frames:** Noticeable but still playable

**Why add delay?** More time for inputs to arrive reduces rollbacks.

---

## Part 7: Common Mistakes

### WRONG - Using local_player_mask in update()

```rust
fn update() {
    let mask = local_player_mask();  // DESYNC! Different per client
    if (mask & 1) != 0 {
        // Only runs on some clients - breaks determinism
    }
}
```

### WRONG - Skipping remote player input

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

### CORRECT - Process all players, render local

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

---

## Part 8: Testing Multiplayer

### Testing Progression

1. **Local Single-Player** - Verify basic gameplay
2. **Local Multi-Player** - 2-4 controllers on same machine
3. **Synthetic Desync Test** - Run two instances, feed identical inputs, compare state hashes
4. **Local Network Test** - Two machines on same LAN
5. **Simulated Latency** - Add artificial delay (50-200ms)
6. **Real Online Test** - Different networks/regions

### Desync Debugging

When state differs between clients:

1. **Add state hashing:** Hash game state each frame
2. **Log divergence frame:** Find first frame where hashes differ
3. **Compare state dumps:** What changed?
4. **Check suspects:** Random calls, floating-point precision, hash map iteration, uninitialized memory

---

## Part 9: Performance Considerations

Each viewport requires separate rendering passes:

| Viewports | draw_env() | draw_mesh() | Impact |
|-----------|------------|-------------|--------|
| 1 | 1x | 1x | Baseline |
| 2 | 2x | 2x | ~2x work |
| 4 | 4x | 4x | ~4x work |

**Optimize by:**
- Simplifying environment effects for split-screen modes
- Using LOD for distant objects
- Reducing particle counts per viewport

---

## Additional Resources

### Reference Files
- **`references/determinism-checklist.md`** — Verification checklist
- **`references/netplay-patterns.md`** — Common multiplayer patterns
- **`references/viewport-layouts.md`** — All viewport configurations

### Integration with zx-dev
The zx-dev plugin provides:
- **Rollback Safety Reviewer agent** — Detects non-deterministic code
- FFI documentation for `random()`, `tick_count()`
- Camera systems for per-viewport setup
