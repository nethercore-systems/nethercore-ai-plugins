---
name: debugging
description: >-
  Runtime debugging tools for Nethercore games on all consoles. Covers the F4
  Debug Inspector, live value editing, watch variables, frame stepping, and
  time-scale controls. Use when tuning game parameters at runtime, tracking
  state over time, or stepping through frames to find bugs.
license: Apache-2.0
compatibility: Debug Inspector available in all Nethercore consoles. Works offline.
metadata:
  author: nethercore-systems
  version: "1.0.0"
---

# Nethercore Debugging

The debug system is built into the Nethercore player and works with **all consoles**.

## F4 Debug Inspector

Press **F4** during development to open the Debug Inspector. This is your primary debugging tool.

**Features:**
- Live value editing (sliders, toggles, color pickers)
- Read-only watches for monitoring
- Grouped/collapsible organization
- Frame control (pause, step, time scale)
- Zero overhead in release builds

## Quick Reference

| Function | Purpose | Call In |
|----------|---------|---------|
| `debug_register_i32(name, ptr)` | Editable integer | `init()` |
| `debug_register_f32(name, ptr)` | Editable float | `init()` |
| `debug_register_bool(name, ptr)` | Toggle checkbox | `init()` |
| `debug_register_vec3(name, ptr)` | 3D position | `init()` |
| `debug_register_color(name, ptr)` | RGBA picker | `init()` |
| `debug_watch_*(name, ptr)` | Read-only display | `init()` |
| `debug_group_begin/end(name)` | Collapsible sections | `init()` |

## Range-Constrained (Sliders)

```rust
debug_register_f32_range(b"Speed".as_ptr(), 5, &SPEED, 0.0, 20.0);
debug_register_i32_range(b"Lives".as_ptr(), 5, &LIVES, 0, 10);
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **F4** | Toggle Debug Inspector |
| F3 | Toggle Runtime Stats |
| F5 | Pause/Resume |
| F6 | Step one frame (when paused) |
| F7/F8 | Decrease/Increase time scale |

## Frame Control

```rust
fn update() {
    if debug_is_paused() != 0 { return; }
    let dt = delta_time() * debug_get_time_scale();
    // ...
}
```

## Typical Setup

```rust
static mut PLAYER_X: f32 = 0.0;
static mut GRAVITY: f32 = 9.8;
static mut GOD_MODE: u8 = 0;

fn init() {
    unsafe {
        debug_group_begin(b"Player".as_ptr(), 6);
        debug_watch_f32(b"X".as_ptr(), 1, &PLAYER_X);
        debug_register_f32_range(b"Gravity".as_ptr(), 7, &GRAVITY, 1.0, 50.0);
        debug_register_bool(b"God Mode".as_ptr(), 8, &GOD_MODE);
        debug_group_end();
    }
}
```

## When to Use What

| Scenario | Tool |
|----------|------|
| Live parameter tuning | Debug Inspector (F4) |
| Tracking state over time | `log()` in `update()` |
| Regression testing | Replay system |
| Finding exact frame of bug | F5 pause + F6 step |
