---
name: development
description: >-
  Core development workflow for Nethercore WASM games. Covers the nether CLI
  (build, run, pack), nether.toml manifest authoring, required WASM exports,
  and determinism rules for rollback netcode. Use when building, configuring,
  or structuring a Nethercore game project.
license: Apache-2.0
compatibility: Requires nether CLI. Works offline.
metadata:
  author: nethercore-systems
  version: "1.0.1"
---

# Nethercore Development

Build guest games against the actual console contract; this is not permission to change the emulator. During skill maintenance, inspect source read-only and report implementation contradictions separately.

## Establish the target

Inspect the game's manifest, build scripts, bindings and existing tests first. Use the selected console's canonical bindings and host implementation; for ZX, `nethercore/include/zx.rs` is the designated ABI source. Resolve the actual CLI/player and check `--help`; old documentation and binary versions can disagree.

## Required exports (Rust 2021)

```rust
#[no_mangle] pub extern "C" fn init() { }   // Configure and load resources once
#[no_mangle] pub extern "C" fn update() { } // Deterministic simulation
#[no_mangle] pub extern "C" fn render() { } // Presentation; skipped during rollback
```

Use a WASM `cdylib`, `wasm32-unknown-unknown`, and the game's existing native-test layout. Rust 2024 uses unsafe export attributes; do not mix edition scaffolds. Prefer `no_std` when practical, not an unnecessary engine/allocator.

## Build and manifest

```bash
nether build                       # compile + pack; release by default
nether run --no-build               # inspect the exact packed cart
nether run --no-build --sync-test --check-distance 2 --players 1 --exit-after-frames 120
```

`nether init` creates a manifest; `compile` builds WASM only; `pack` uses existing WASM and assets. `--debug` selects a debug build. There are no `build --release`, `build --verbose` or `run --frames` options in the audited CLI. See [CLI commands](references/cli-commands.md).

Example ZX manifest:

```toml
[game]
id = "my-game"
title = "My Game"
author = "Your Name"
version = "1.0.0"
render_mode = 0
tick_rate = 60
max_players = 1
compress_textures = false

[netplay]
enabled = false

[build]
script = "cargo build --target wasm32-unknown-unknown --release"
wasm = "target/wasm32-unknown-unknown/release/my_game.wasm"

[[assets.textures]]
id = "player"
path = "assets/player.png"
```

Set multiplayer intent explicitly; defaults enable netplay and four players. Settings belong under `[game]`, not `[console]`. Specify exact WASM output to avoid renamed-crate artifacts. Generate assets before packing; the manifest does not discover external authoring projects. See [manifest reference](references/nether-toml.md).

## Rollback responsibilities

The host owns transport, input transmission, snapshots and GGRS scheduling. The game still owns deterministic rules, input handling for all players, stable iteration and rollback-safe resource/effect use. Do not add guest networking to duplicate the host.

- Keep simulation/RNG/allocator state in rollback-covered memory. Static variables are not automatically proof of linear-memory placement; arbitrary WASM globals/host objects are not guaranteed snapshots.
- Use host simulation time (`tick_count`, `delta_time`, `elapsed_time`) and host RNG or an explicitly snapshotted deterministic RNG, never OS time/entropy.
- `render` must not advance gameplay or consume its RNG. Resource creation and ROM loading belong in `init` where guarded.
- Local identity, debugging controls and persistent saves must not silently alter shared simulation.
- Measure/check the actual required player and input scenarios. A startup/tool failure is not automatically a desync, and an idle smoke is not full determinism certification.

See [determinism rules](references/determinism-rules.md). Run the smallest native rule regression plus the real player; native FFI stubs cannot prove asset/render correctness. See [known contradictions](references/known-contradictions.md) before relying on replay reports or raw WAV conversion.
