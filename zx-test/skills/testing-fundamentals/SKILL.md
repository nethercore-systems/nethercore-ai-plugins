---
name: Testing Fundamentals
description: This skill provides guidance on testing Nethercore ZX games for determinism and correctness. Use when the user asks about "sync testing", "replay testing", "determinism", "desync", "checksums", "test my game", or "verify determinism".
version: 1.0.0
---

# Testing Fundamentals for Nethercore ZX

Test ZX games for determinism and correctness using sync tests, replay regression, and proper test organization.

## Sync Testing

Sync testing runs two identical game instances and compares checksums each frame to detect non-deterministic behavior.

Run sync tests:
```bash
nether run --sync-test
```

**Pass criteria**: Identical checksums for 1000+ frames of gameplay.

**Common desync causes**:
- Using `rand::thread_rng()` instead of `zx::random()`
- Using `HashMap` (non-deterministic iteration order) instead of `BTreeMap`
- Floating-point accumulation errors in game logic
- Reading system time or wall clock
- Uninitialized memory reads

## Replay Testing

Record inputs for deterministic playback and regression testing across builds.

Record gameplay:
```bash
nether run --record replay.bin
```

Replay recording:
```bash
nether run --replay replay.bin
```

**Regression workflow**:
1. Record reference gameplay on known-good build
2. Replay on new build
3. Compare final game state or outcomes
4. Mismatches indicate breaking changes

## Determinism Rules

ZX uses GGRS rollback netcode requiring 100% deterministic game logic.

| Do | Don't |
|---|---|
| `zx::random()` | `rand::thread_rng()` |
| `BTreeMap`, `BTreeSet` | `HashMap`, `HashSet` |
| Fixed-point or integer math | Floats for game logic |
| Frame counter for timing | System time / `Instant::now()` |
| Explicit initialization | Uninitialized reads |

## Test Organization

Structure tests by scope:

| Test Type | Tool | Purpose |
|-----------|------|---------|
| Unit tests | `cargo test` | Pure logic functions |
| Sync tests | `nether run --sync-test` | Full runtime determinism |
| Replay regression | `--record` / `--replay` | Cross-build validation |

Run unit tests:
```bash
cargo test
```

Run sync test for specific duration:
```bash
nether run --sync-test --frames 3000
```
