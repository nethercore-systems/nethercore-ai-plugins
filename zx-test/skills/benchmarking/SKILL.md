---
name: Benchmarking
description: |
  This skill covers performance benchmarking for ZX games. Use when the user asks about "benchmark", "performance", "profile", "memory", "speed", "slow", "frame time", or "optimize timing".
version: 1.0.0
---

# Benchmarking for Nethercore ZX

## Key Metrics

| Metric | Target | Why |
|--------|--------|-----|
| Update time | <2ms | Game logic per tick |
| Render time | <8ms | Draw calls per frame |
| State size | <100KB | Rollback snapshot |
| ROM size | <16MB | Distribution |

## Frame Budget (60fps)

Total: 16.67ms per frame
- Update: <2ms (rollback may replay 7+ frames)
- Render: <8ms
- Headroom: ~6ms

**Rollback impact:** 7 frames × 2ms = 14ms worst case

## Profiling

```rust
zx::debug_watch_f32("update_ms", update_time);
zx::debug_watch_i32("entity_count", entities.len() as i32);
```

View with F3 debug panel in-game.

Build with release mode for accurate timing:
```bash
nether run --release
```

## State Size

Smaller state = faster rollback.

```rust
// Measure state
let bytes = std::mem::size_of_val(&game_state);
zx::debug_watch_i32("state_bytes", bytes as i32);
```

**Reduce state:**
- Store indices, not objects
- Use compact types (u8 vs u32)
- Separate render-only from rollback state

## ROM Size

```bash
nether build --release
```

**Reduce size:**
- LTO + opt-level = "z"
- Strip symbols
- Remove unused deps
