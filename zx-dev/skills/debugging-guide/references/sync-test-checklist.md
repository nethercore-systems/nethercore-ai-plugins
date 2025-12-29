# Sync Test Debugging Checklist

Use this checklist when `--sync-test` reports a desync.

## Quick Checks

- [ ] All random values use `random()`, `random_range()`, `random_f32()`, or `random_f32_range()`
- [ ] No calls to external time (wall clock, system time)
- [ ] All game state in static variables (not heap-allocated)
- [ ] `render()` function only draws, never modifies state
- [ ] No uninitialized memory reads

## State Location

**Must be static:**
```rust
// CORRECT - static variables are auto-snapshotted
static mut PLAYER_X: f32 = 0.0;
static mut GAME_STATE: GameState = GameState::new();
```

**Avoid heap allocation:**
```rust
// PROBLEMATIC - Vec uses heap, may not snapshot correctly
// Use fixed-size arrays instead
static mut ENEMIES: [Enemy; 64] = [Enemy::new(); 64];
static mut ENEMY_COUNT: usize = 0;
```

## Random Number Usage

**Correct - deterministic RNG:**
```rust
let damage = random_range(5, 15);
let spawn_x = random_f32_range(0.0, 960.0);
let should_crit = random() % 100 < crit_chance;
```

**Incorrect - external randomness:**
```rust
// NEVER do this
use std::time::SystemTime;
let seed = SystemTime::now();  // Desync!

// Or this
let damage = rand::random::<i32>();  // Desync!
```

## Time Usage

**Correct - deterministic time:**
```rust
let dt = delta_time();           // Fixed timestep
let total = elapsed_time();      // Accumulated timesteps
let frame = tick_count();        // Frame counter
```

**Incorrect - wall clock:**
```rust
// NEVER do this
use std::time::Instant;
let start = Instant::now();  // Desync!
```

## Render vs Update

**Update (deterministic):**
```rust
fn update() {
    // All state changes here
    PLAYER_X += velocity * delta_time();
    check_collisions();
    update_enemies();
}
```

**Render (display only):**
```rust
fn render() {
    // ONLY drawing, no state changes
    draw_sprite(texture, PLAYER_X, PLAYER_Y, ...);

    // WRONG - don't do this:
    // PLAYER_X += 1.0;  // This would desync!
}
```

## Floating Point Concerns

**Prefer integer math for positions:**
```rust
// More deterministic
static mut PLAYER_X_FP: i32 = 0;  // Q16.16 fixed point
```

**If using float, ensure consistent operations:**
```rust
// Avoid order-dependent operations
let sum = a + b + c;  // Same order every time
```

## Conditional Logic

**Check that conditionals are deterministic:**
```rust
// Correct - uses deterministic state
if tick_count() % 60 == 0 {
    spawn_enemy();
}

// Correct - uses random()
if random() % 100 < spawn_chance {
    spawn_enemy();
}

// WRONG - uses non-deterministic input
if keyboard_pressed() {  // If reading raw OS input, desync!
    jump();
}
```

## Debug Process

1. **Add watches** to suspicious variables
2. **Run sync test** - note which variable diverges first
3. **Trace backwards** - what modifies that variable?
4. **Check operations** - random, time, conditionals?
5. **Isolate** - comment out code sections until desync disappears
6. **Fix** - ensure all operations are deterministic

## Common Patterns That Desync

| Pattern | Problem | Fix |
|---------|---------|-----|
| `rand::random()` | External RNG | Use `random()` |
| `SystemTime::now()` | Wall clock | Use `tick_count()` |
| `HashMap` iteration | Order varies | Use `BTreeMap` or array |
| Pointer comparison | Address varies | Compare values |
| Float to string | Precision varies | Avoid in logic |
| Uninitialized arrays | Random contents | Initialize all memory |

## Testing Tips

- Run `--sync-test` early and often during development
- Add sync tests to your CI pipeline
- Test with varying input patterns
- Use `--p2p-test` to test actual rollback behavior
