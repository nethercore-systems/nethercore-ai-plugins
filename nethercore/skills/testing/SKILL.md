---
name: Nethercore Testing
description: |
  Testing Nethercore games for determinism and correctness. Triggers on "sync test", "replay test", "determinism test", "desync", "checksums", "test my game".

  **Load references when:**
  - Replay format details -> `references/replay-format.md`
  - Performance benchmarking -> `references/benchmarking.md`
version: 1.0.0
---

# Nethercore Testing

## Sync Testing

Runs two identical instances, compares checksums each frame.

```bash
nether run --sync-test
nether run --sync-test --frames 3000  # Specific duration
```

**Pass criteria:** Identical checksums for 1000+ frames.

## Replay Testing

Record and replay for regression testing:

```bash
nether run --record replay.bin  # Record
nether run --replay replay.bin  # Playback
```

**Workflow:**
1. Record on known-good build
2. Replay on new build
3. Compare outcomes

## Determinism Rules

| Do | Don't |
|---|---|
| `random()` FFI | `rand::thread_rng()` |
| `BTreeMap`, `BTreeSet` | `HashMap`, `HashSet` |
| Frame counter | `Instant::now()` |
| Fixed-point math | Floating-point accumulation |

## Test Organization

| Type | Tool | Purpose |
|------|------|---------|
| Unit | `cargo test` | Pure logic |
| Sync | `nether run --sync-test` | Runtime determinism |
| Replay | `--record`/`--replay` | Cross-build validation |

## Common Desync Causes

1. **Non-deterministic RNG** - Using rand crate instead of FFI
2. **HashMap iteration** - Order varies between runs
3. **System time** - Reading wall clock
4. **Uninitialized memory** - Undefined values
5. **State in render()** - Skipped during rollback

## Debugging Desyncs

1. Run sync test to confirm failure
2. Add `log()` calls around suspicious code
3. Check for forbidden patterns
4. Verify all state is in static variables
