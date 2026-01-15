# nether.toml Reference

## Full Example

```toml
[game]
id = "space-fighter"
title = "Space Fighter"
author = "Your Name"
version = "1.0.0"
description = "A space combat game"
tags = ["arcade", "shooter", "multiplayer"]

[build]
script = "cargo build --target wasm32-unknown-unknown --release"
wasm = "target/wasm32-unknown-unknown/release/space_fighter.wasm"

# Textures - auto-compressed to BC7
[[assets.textures]]
id = "player_ship"
path = "assets/textures/player.png"

[[assets.textures]]
id = "enemy_ship"
path = "assets/textures/enemy.png"

[[assets.textures]]
id = "bullet"
path = "assets/textures/bullet.png"

# Meshes - GLB/GLTF format
[[assets.meshes]]
id = "ship_model"
path = "assets/meshes/ship.glb"

# Audio - 22050Hz mono WAV
[[assets.sounds]]
id = "laser"
path = "assets/audio/laser.wav"

[[assets.sounds]]
id = "explosion"
path = "assets/audio/explosion.wav"

# Music - XM/IT tracker format
[[assets.music]]
id = "battle_theme"
path = "assets/music/battle.xm"
```

## Asset Handle Usage

In code, use `rom_*_str()` to get handles:

```rust
let tex = rom_texture_str("player_ship");
let mesh = rom_mesh_str("ship_model");
let sfx = rom_sound_str("laser");
let music = rom_music_str("battle_theme");
```

## Asset Path Conventions

- Textures: PNG (auto-compressed to BC7)
- Meshes: GLB or GLTF
- Audio: WAV (22050Hz mono)
- Music: XM or IT tracker format
