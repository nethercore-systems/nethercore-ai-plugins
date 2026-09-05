# Benchmarking

Measure on the actual target player/configuration and separate cold startup, update, render and rollback catch-up costs. There is no universal snapshot-bytes-to-milliseconds table.

```bash
nether build
```

Inspect actual WASM/ROM sizes and resource usage. `build --verbose` is not supported by `nether`. Use the selected console's specification (`nethercore/shared/src/console.rs`) rather than an invented 2 MiB WASM or 200 KiB snapshot ceiling.

- ZX specifies 16 MiB ROM, 4 MiB linear RAM, 4 MiB VRAM and a 4 ms/tick CPU budget. Specification, enforcement and measurements are different claims.
- A state struct's size is not the whole snapshot: core saves linear memory plus explicit host/input/console state.
- `delta_time()` is a fixed simulation timestep, not elapsed CPU/GPU time. Use host instrumentation/stats for spikes.
- File size, decoded texture/mesh GPU cost and sample memory are separate quantities.
- Record workload, player count, tick rate, debug/release configuration and capture/profiling overhead. Compare the same scenario before/after one optimization.

Accept when the actual workload fits the chosen console budget and retains game behavior/rollback correctness; no performance claims from a parser-only replay.
