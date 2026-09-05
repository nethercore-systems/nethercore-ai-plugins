---
name: testing
description: >-
  Testing Nethercore games for determinism and correctness. Covers sync testing,
  replay recording and playback, debug actions, and desync diagnosis. Use when
  running sync tests, setting up replay-based regression tests, or diagnosing
  determinism failures.
license: Apache-2.0
compatibility: Requires nether CLI. Works offline.
metadata:
  author: nethercore-systems
  version: "1.0.1"
---

# Nethercore Testing

Use a focused native rule test, actual player behavior, and a rollback check where simulation changed. Do not turn parser success, a zero exit code or dummy FFI stubs into game acceptance.

## Sync testing

GGRS sync-test mode replays/checks saved state; it is not the same as launching two connected network players.

```bash
nether run --no-build --sync-test --check-distance 2 --players 1 --exit-after-frames 120
```

Build first. Use product-relevant inputs/player counts and longer runs when needed. Verify progress/completion and absence of game/desync errors; enforce an outer timeout. `--exit-after-frames` counts advanced input frames, not every rollback replay. A failure may be a load/runtime/tool error rather than nondeterminism.

## Real-player replay

```bash
nether replay compile smoke.ncrs -o smoke.ncrp
nether run --no-build --replay smoke.ncrs
```

The first command verifies script syntax/encoding. The second runs the cart with scripted input and capture requests. `.ncrs` is TOML; `.ncrp` is binary. The old `nether run --record replay.bin` and `--frames` examples are not supported by this CLI.

Every omitted frame/player is idle. A held input must appear on each intended tick. Inspect actual captured output or measured game state; changed game rules need not reproduce old outcomes unless that is the regression contract. See [replay format](references/replay-format.md).

## Avoid false greens

The audited `nether replay run` implementation is a simplified headless runner that does not load game WASM. Its report is **not** a game regression result. Graphical replay must not be assumed to run assertions/debug actions merely because the parser exposes them; trace current callers before relying on them. See the development skill's known-contradictions reference.

For numerical checks use the game's native simulation tests or an existing real runtime harness. `Runtime::run_scripted_sync_test` is an available core path for scripted rollback without rendering, not a claim that the public replay command uses it.

Debug Inspector actions can set up a local scenario, but export/callback registration and execution must be verified. Do not ship a test whose assertions/actions silently never execute.

## Diagnose

Check simulation RNG, stable iteration/tie-breaking, wall-clock reads, invalid math, rollback-covered state, and render mutations. Do not assume all statics are in linear memory or that every float causes a desync.

See [benchmarking](references/benchmarking.md). Fixed `delta_time()` is not a frame-time profiler.
