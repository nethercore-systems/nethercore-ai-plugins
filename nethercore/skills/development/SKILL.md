---
name: Nethercore Development
description: |
  Core development workflow for Nethercore games. Triggers on "nether build", "nether.toml", "asset handles", "determinism", "rollback rules", "WASM game".

  **Load references when:**
  - Full nether.toml examples -> `references/nether-toml.md`
  - CLI command details -> `references/cli-commands.md`
  - Determinism patterns -> `references/determinism-rules.md`
version: 1.0.0
---

# Nethercore Development

## Overview

Nethercore games compile to WASM and run in the Nethercore player with rollback netcode. All consoles share the same WASM core, ensuring determinism across platforms.

## Required Game Exports

Every game exports three functions:

```rust
#[no_mangle] pub extern "C" fn init() { }   // Setup, asset loading
#[no_mangle] pub extern "C" fn update() { } // Deterministic logic
#[no_mangle] pub extern "C" fn render() { } // Drawing only
```

## nether CLI

| Command | Purpose |
|---------|---------|
| `nether init` | Create nether.toml manifest |
| `nether compile` | Compile WASM from source |
| `nether pack` | Bundle WASM + assets into ROM |
| `nether build` | compile + pack (main command) |
| `nether run` | Build and launch in player |

## Game Manifest (nether.toml)

```toml
[game]
id = "my-game"
title = "My Game"
author = "Your Name"
version = "1.0.0"

[build]
script = "cargo build --target wasm32-unknown-unknown --release"
wasm = "target/wasm32-unknown-unknown/release/my_game.wasm"

[[assets.textures]]
id = "player"
path = "assets/player.png"
```

## Netcode (What You DON'T Do)

The Nethercore player handles **all networking automatically**:
- GGRS rollback synchronization
- State snapshots
- Input transmission
- Desync detection

**Your only responsibility:** Make `update()` deterministic.
**Never write:** Networking code, rollback logic, state sync, or input transmission.

## Determinism (Rollback Safety)

The `update()` function must be deterministic for rollback netcode. Given identical inputs, all clients must produce identical state.

### Rules

1. **All state in WASM memory** - Use static variables (auto-snapshotted)
2. **Use FFI `random()` functions** - Never external randomness
3. **Use `tick_count()` not system time** - Frame-based logic only
4. **render() is display-only** - Never modify game state in render

### Forbidden Patterns

| Pattern | Problem | Correct Alternative |
|---------|---------|---------------------|
| `rand::thread_rng()` | External RNG | FFI `random()`, `random_range()` |
| `SystemTime::now()` | System clock | FFI `tick_count()` |
| `HashMap` iteration | Unordered | Arrays, `BTreeMap` |
| State changes in render() | Skipped during rollback | Move to update() |

### Quick Test

```bash
nether run --sync-test --frames 1000
```

If this fails, you have non-deterministic code.

## Project Structure

```
my-game/
├── nether.toml          # Game manifest
├── src/
│   ├── lib.rs           # Entry point (init/update/render)
│   └── zx.rs            # FFI bindings (console-specific)
├── assets/
│   ├── textures/
│   ├── meshes/
│   └── audio/
└── Cargo.toml
```

**Key principle:** Keep entry files minimal (~50 lines). FFI bindings in separate module.
