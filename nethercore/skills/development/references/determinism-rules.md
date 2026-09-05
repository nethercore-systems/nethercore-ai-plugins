# Determinism rules

Given identical initial state and input, simulation must produce identical state. Source anchors: `nethercore/core/src/rollback/state/snapshot.rs`, `core/src/wasm/instance.rs`, and the console FFI implementations.

- Keep mutable simulation state, allocator and RNG state in rollback-covered memory. Core snapshots cover linear memory plus explicit host/input/console rollback state; not arbitrary host resources or every WASM global.
- Host `random`, `random_range`, `random_f32` use deterministic RNG. Alternatively use an explicitly seeded, snapshotted game RNG with stable call ordering.
- `tick_count`, `delta_time`, `elapsed_time` are simulation time, not wall time or profiling clocks.
- Stable array/map iteration and tie-breaking matter. Avoid unordered iteration, OS entropy/time, uninitialized values and non-finite math.
- `render` reads simulation state; never advance gameplay, consume gameplay RNG or store gameplay-affecting render caches. It is skipped on rollback.
- Keep asset loading/creation in the allowed init phase. Guest filesystem APIs are not implied by a native Rust example. Save data/local-player identity must not desynchronize shared rules.
- Fixed-point can help authoritative collision; floats are not universally forbidden. Verify your actual math and do not assume NaN canonicalization.
- Debug pause/time-scale are host development controls; do not multiply game simulation time by local debug controls or early-return from shared simulation based on them.

```bash
nether run --no-build --sync-test --check-distance 2 --players 2 --exit-after-frames 3000
```

Provide representative input and verify real completion/desync logs with an outer timeout. Idle sync, normal replay and native rule assertions prove different things. Native FFI stubs are not emulator evidence.
