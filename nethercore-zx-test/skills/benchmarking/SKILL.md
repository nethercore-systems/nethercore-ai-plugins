---
name: Benchmarking
description: This skill provides guidance on performance benchmarking for Nethercore ZX games. Use when the user asks about "benchmark", "performance", "profile", "memory", "speed", "slow", "optimize timing", or "measure frame time".
version: 1.0.0
---

# Benchmarking for Nethercore ZX

Measure and optimize game performance for smooth gameplay and efficient rollback.

## Key Metrics

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Update time | <2ms at 60fps | Game logic per tick |
| Render time | <8ms at 60fps | Draw calls per frame |
| State size | <100KB | Bytes snapshotted for rollback |
| ROM size | <16MB | Distribution footprint |

## Profiling Workflow

Build with release mode for accurate timing:
```bash
cargo build --release
nether run --release
```

Expose metrics using debug watch:
```rust
zx::debug_watch_f32("update_ms", update_time_ms);
zx::debug_watch_f32("render_ms", render_time_ms);
zx::debug_watch_i32("entity_count", entities.len() as i32);
```

View metrics with F3 debug panel in-game.

## Frame Budget

At 60fps, each frame has 16.67ms total:
- Update: Target <2ms (rollback may replay 7+ frames)
- Render: Target <8ms
- Headroom: ~6ms for OS/driver overhead

Rollback multiplies update cost:
- 7 rollback frames at 2ms each = 14ms
- Keep update fast to allow deep rollbacks

## State Size Analysis

Smaller state = faster rollback snapshots and restores.

Reduce state size:
- Store indices instead of full objects
- Use compact representations (u8 instead of u32 where possible)
- Avoid sparse allocations and fragmented data
- Separate render-only data from rollback state

Measure state:
```rust
let state_bytes = std::mem::size_of_val(&game_state);
zx::debug_watch_i32("state_bytes", state_bytes as i32);
```

## ROM Size

Check ROM size:
```bash
nether build --release
ls -la target/wasm32-unknown-unknown/release/*.wasm
```

Reduce ROM size:
- Enable LTO: `lto = true` in Cargo.toml
- Strip symbols: `strip = true`
- Use `opt-level = "z"` for size optimization
- Remove unused dependencies
