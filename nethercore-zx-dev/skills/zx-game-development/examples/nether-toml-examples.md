# nether.toml Examples

Manifest examples for various project types.

## Minimal (Rust, No Assets)

```toml
[game]
id = "my-game"
title = "My Game"
author = "Developer"
version = "1.0.0"
```

Rust projects auto-detect cargo build settings.

## Minimal (C/Zig, Custom Build)

```toml
[game]
id = "my-game"
title = "My Game"
author = "Developer"
version = "1.0.0"

[build]
script = "make"
wasm = "build/game.wasm"
```

## Zig Project

```toml
[game]
id = "my-game"
title = "My Game"
author = "Developer"
version = "1.0.0"

[build]
script = "zig build -Doptimize=ReleaseFast"
wasm = "zig-out/bin/game.wasm"
```

## Full Metadata

```toml
[game]
id = "awesome-game"
title = "Awesome Game"
author = "Studio Name"
version = "1.2.3"
description = "An awesome game for Nethercore ZX"
tags = ["action", "arcade", "multiplayer"]
```

## With Textures

```toml
[game]
id = "textured-game"
title = "Textured Game"
author = "Developer"
version = "1.0.0"

[[assets.textures]]
id = "player"
path = "assets/player.png"

[[assets.textures]]
id = "enemies"
path = "assets/enemies.png"

[[assets.textures]]
id = "tileset"
path = "assets/tileset.png"

[[assets.textures]]
id = "ui"
path = "assets/ui.png"
```

## With 3D Meshes

```toml
[game]
id = "3d-game"
title = "3D Game"
author = "Developer"
version = "1.0.0"

[[assets.meshes]]
id = "player"
path = "assets/player.obj"

[[assets.meshes]]
id = "level"
path = "assets/level.gltf"

[[assets.meshes]]
id = "props"
path = "assets/props.glb"

# Pre-converted Nethercore format
[[assets.meshes]]
id = "optimized"
path = "assets/optimized.nczxmesh"
```

## With Audio

```toml
[game]
id = "audio-game"
title = "Audio Game"
author = "Developer"
version = "1.0.0"

# Sound effects (WAV, 22050Hz, 16-bit mono)
[[assets.sounds]]
id = "jump"
path = "assets/sfx/jump.wav"

[[assets.sounds]]
id = "shoot"
path = "assets/sfx/shoot.wav"

[[assets.sounds]]
id = "explosion"
path = "assets/sfx/explosion.wav"

[[assets.sounds]]
id = "coin"
path = "assets/sfx/coin.wav"

# Music (XM tracker)
[[assets.trackers]]
id = "title-music"
path = "assets/music/title.xm"

[[assets.trackers]]
id = "gameplay-music"
path = "assets/music/gameplay.xm"

[[assets.trackers]]
id = "boss-music"
path = "assets/music/boss.xm"
```

## With Skeletal Animation

```toml
[game]
id = "animated-game"
title = "Animated Game"
author = "Developer"
version = "1.0.0"

[[assets.meshes]]
id = "character"
path = "assets/character.nczxmesh"

[[assets.skeletons]]
id = "character-skeleton"
path = "assets/character.nczxskel"

[[assets.keyframes]]
id = "walk"
path = "assets/animations/walk.nczxanim"

[[assets.keyframes]]
id = "run"
path = "assets/animations/run.nczxanim"

[[assets.keyframes]]
id = "jump"
path = "assets/animations/jump.nczxanim"

# Alternative: use animations (alias for keyframes)
[[assets.animations]]
id = "attack"
path = "assets/animations/attack.nczxanim"
```

## With Raw Data Files

```toml
[game]
id = "data-game"
title = "Data Game"
author = "Developer"
version = "1.0.0"

# Binary data files (levels, configs, etc.)
[[assets.data]]
id = "levels"
path = "assets/levels.bin"

[[assets.data]]
id = "dialog"
path = "assets/dialog.bin"

[[assets.data]]
id = "enemy-patterns"
path = "assets/enemies.dat"
```

## Complete Game Example

```toml
[game]
id = "complete-game"
title = "Complete Game"
author = "Game Studio"
version = "1.0.0"
description = "A complete example with all asset types"
tags = ["example", "complete", "demo"]

# Textures
[[assets.textures]]
id = "player"
path = "assets/textures/player.png"

[[assets.textures]]
id = "enemies"
path = "assets/textures/enemies.png"

[[assets.textures]]
id = "environment"
path = "assets/textures/environment.png"

[[assets.textures]]
id = "ui"
path = "assets/textures/ui.png"

# Meshes
[[assets.meshes]]
id = "player-model"
path = "assets/meshes/player.gltf"

[[assets.meshes]]
id = "level-1"
path = "assets/meshes/level1.obj"

[[assets.meshes]]
id = "props"
path = "assets/meshes/props.glb"

# Skeletons and Animations
[[assets.skeletons]]
id = "player-skeleton"
path = "assets/animations/player.nczxskel"

[[assets.animations]]
id = "idle"
path = "assets/animations/idle.nczxanim"

[[assets.animations]]
id = "walk"
path = "assets/animations/walk.nczxanim"

[[assets.animations]]
id = "run"
path = "assets/animations/run.nczxanim"

# Sound Effects
[[assets.sounds]]
id = "jump"
path = "assets/audio/jump.wav"

[[assets.sounds]]
id = "shoot"
path = "assets/audio/shoot.wav"

[[assets.sounds]]
id = "hit"
path = "assets/audio/hit.wav"

[[assets.sounds]]
id = "coin"
path = "assets/audio/coin.wav"

[[assets.sounds]]
id = "menu-select"
path = "assets/audio/menu-select.wav"

# Music
[[assets.trackers]]
id = "title-theme"
path = "assets/music/title.xm"

[[assets.trackers]]
id = "level-theme"
path = "assets/music/level.xm"

[[assets.trackers]]
id = "boss-theme"
path = "assets/music/boss.xm"

[[assets.trackers]]
id = "victory"
path = "assets/music/victory.xm"

# Data
[[assets.data]]
id = "levels"
path = "assets/data/levels.bin"

[[assets.data]]
id = "localization"
path = "assets/data/strings.bin"
```

## Asset ID Naming Conventions

- Use lowercase with hyphens: `player-sprite`, `level-1-mesh`
- Be descriptive: `jump-sound` not `sfx1`
- Group by type in the ID: `ui-button`, `ui-panel`
- Keep IDs short but clear

## Loading Assets in Code

```rust
// Textures
let player_tex = rom_texture_str("player");

// Meshes
let level = rom_mesh_str("level-1");

// Sounds
let jump = rom_sound_str("jump");

// Music (trackers)
let bgm = rom_tracker_str("title-theme");

// Raw data
let level_data_len = rom_data_len_str("levels");
let mut buffer = vec![0u8; level_data_len as usize];
rom_data_str("levels", buffer.as_mut_ptr(), level_data_len);
```
