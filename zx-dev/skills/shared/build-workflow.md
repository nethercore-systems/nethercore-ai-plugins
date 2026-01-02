# ZX Build and Run Workflow

## Critical: ZX Execution Model

**ZX games are WASM libraries, NOT executables.** The game exports `init()`, `update()`, `render()` functions called by the Nethercore player.

## Build Commands

```bash
nether build              # Compile WASM + pack assets into ROM
nether run                # Build and launch in player
nether run --debug        # Debug build with symbols
nether run --sync-test    # Test rollback determinism
nether run --p2p-test     # Two-instance netplay test
```

## NEVER Do This

```bash
cargo run                    # ❌ Games are not native executables
./target/release/my_game     # ❌ Can't run WASM directly
cargo build --release        # ❌ Incomplete - use nether build
```

## Cargo.toml Requirement

```toml
[lib]
crate-type = ["cdylib"]  # Required for WASM library
```

## nether.toml Format

```toml
[game]
id = "my-game"
title = "My Game"
version = "1.0.0"

[build]
# Optional: defaults for Rust projects

[[assets.textures]]
id = "player"
path = "assets/player.png"

[[assets.meshes]]
id = "level"
path = "assets/level.obj"

[[assets.sounds]]
id = "jump"
path = "assets/jump.wav"
```

## Asset Loading

```rust
// From ROM (recommended)
let tex = rom_texture_str("player");
let mesh = rom_mesh_str("level");
let sound = rom_sound_str("jump");
```
