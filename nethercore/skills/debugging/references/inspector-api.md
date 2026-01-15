# Debug Inspector API

The debug inspector is a Nethercore player feature available to **all consoles**.

## Overview

Two debugging systems work together:

| System | Purpose | Best For |
|--------|---------|----------|
| **F4 Debug Inspector** | Live editing & monitoring | Human tweaking during play |
| **log() + Replay assertions** | Programmatic debugging | Agentic test loops, CI |

## F4 Debug Inspector

Press **F4** during development. Zero overhead in release builds.

### Registration Functions (call in init())

| Function | Control Type | Example |
|----------|--------------|---------|
| `debug_register_i32(name, ptr)` | Numeric input | Enemy count |
| `debug_register_f32(name, ptr)` | Numeric input | Gravity |
| `debug_register_bool(name, ptr)` | Checkbox | God mode |
| `debug_register_vec2(name, ptr)` | 2D input | Position |
| `debug_register_vec3(name, ptr)` | 3D input | Camera target |
| `debug_register_color(name, ptr)` | Color picker | Tint |
| `debug_register_rect(name, ptr)` | 4-value input | Bounds |

### Range-Constrained (Sliders)

| Function | Example |
|----------|---------|
| `debug_register_i32_range(name, ptr, min, max)` | Lives 0-10 |
| `debug_register_f32_range(name, ptr, min, max)` | Speed 0.0-20.0 |
| `debug_register_u8_range(name, ptr, min, max)` | Level 1-255 |

### Watch Functions (Read-Only)

Same types as registration, but `debug_watch_*` instead of `debug_register_*`.
Use for values you want to monitor but not edit (e.g., velocity, frame count).

### Grouping

```rust
debug_group_begin(b"Player".as_ptr(), 6);
debug_watch_f32(b"X".as_ptr(), 1, &PLAYER_X);
debug_register_f32(b"Health".as_ptr(), 6, &HEALTH);
debug_group_end();
```

### Frame Control

```rust
fn update() {
    // Respect debug pause
    if debug_is_paused() != 0 { return; }

    // Respect time scale
    let dt = delta_time() * debug_get_time_scale();
}
```

### Fixed-Point Types

For deterministic math:
- `debug_register_fixed_i16_q8`
- `debug_register_fixed_i32_q8`
- `debug_register_fixed_i32_q16`
- `debug_register_fixed_i32_q24`

---

## Programmatic Debugging (Agentic Loop)

For AI-assisted debugging and CI, use `log()` + replay assertions:

### log() Function

```rust
fn update() {
    let msg = format!("frame {} pos: {},{}", tick_count(), x, y);
    log(msg.as_ptr(), msg.len() as u32);
}
```

Output captured when running `nether run` or `nether run --replay`.

### Replay Assertions

```toml
[[frames]]
f = 300
assert = "$player_x > 100"
snap = true
```

### Debug Actions (Skip to Scenario)

Games can register callable actions:

```rust
// In init()
debug_action_begin(b"Load Level".as_ptr(), 10, b"debug_load_level".as_ptr(), 16);
debug_action_param_i32(b"level".as_ptr(), 5, 1);
debug_action_end();
```

Then use in replay scripts:

```toml
[[frames]]
f = 0
action = "Load Level"
action_params = { level = 3 }

[[frames]]
f = 1
snap = true
```

---

## Full Agentic Test Loop

1. **Create test**: Write `.ncrs` script with debug actions to set up scenario
2. **Run**: `nether run --replay test.ncrs`
3. **Observe**: Check log output and assertion results
4. **Fix**: Modify code
5. **Validate**: Re-run replay

### Example Script (Bug Reproduction)

```toml
seed = 12345
players = 1

# Skip to problematic state
[[frames]]
f = 0
action = "Load Level"
action_params = { level = 2 }

[[frames]]
f = 0
action = "Set Player Health"
action_params = { health = 1 }

# Start test
[[frames]]
f = 1
snap = true

# Trigger the bug
[[frames]]
f = 60
p1 = "right+a"

# Verify fix
[[frames]]
f = 120
assert = "$player_alive == 1"
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| F3 | Toggle Runtime Stats Panel |
| F4 | Toggle Debug Inspector |
| F5 | Pause/unpause |
| F6 | Step one frame (while paused) |
| F7 | Decrease time scale |
| F8 | Increase time scale |
