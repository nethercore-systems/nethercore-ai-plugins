# Rollback Safety Rules

## Core Requirement

The `update()` function must be **deterministic** for GGRS rollback netcode. Given identical inputs, all clients must produce identical state.

## Rules

1. **All state in WASM memory** - Use static variables (auto-snapshotted)
2. **Use FFI `random()` functions** - Never external randomness
3. **Use `tick_count()` not system time** - Frame-based logic only
4. **render() is display-only** - Never modify game state in render

## Forbidden Patterns

| Pattern | Problem | Correct Alternative |
|---------|---------|---------------------|
| `rand::thread_rng()` | External RNG | FFI `random()`, `random_range()` |
| `SystemTime::now()` | System clock | FFI `elapsed_time()`, `tick_count()` |
| `HashMap` iteration | Unordered | Arrays, `BTreeMap` |
| State changes in render() | Skipped during rollback | Move to update() |
| File I/O in update() | Non-deterministic | Load in init() |

## Allowed in update()

- FFI `random()`, `random_range()`, `random_f32()`
- FFI `delta_time()`, `elapsed_time()`, `tick_count()`
- FFI `button_pressed()`, `left_stick_x()` (input)
- Static variable mutations
- Array/BTreeMap with consistent iteration

## Allowed in render() Only

- All `draw_*` functions
- `camera_set()`, `camera_fov()`
- `push_translate()`, `push_rotate_y()`, `push_scale()`
- `texture_bind()`, `font_bind()`
- Reading (not writing) game state

## Quick Test

```bash
nether run --sync-test --frames 1000
```

If this fails, you have non-deterministic code.
