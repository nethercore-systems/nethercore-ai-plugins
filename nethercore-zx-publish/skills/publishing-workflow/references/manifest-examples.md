# nether.toml Manifest Examples

## Minimal Rust Project

```toml
[game]
id = "hello-world"
title = "Hello World"
author = "Developer"
version = "1.0.0"
```

Build defaults to `cargo build --target wasm32-unknown-unknown --release`.

## Rust with Assets

```toml
[game]
id = "space-shooter"
title = "Space Shooter"
author = "GameDev Studio"
version = "1.0.0"
description = "Classic arcade action in space"
tags = ["arcade", "shooter", "retro"]

[[assets.textures]]
id = "player"
path = "assets/sprites/player.png"

[[assets.textures]]
id = "enemy"
path = "assets/sprites/enemy.png"

[[assets.textures]]
id = "bullet"
path = "assets/sprites/bullet.png"

[[assets.sounds]]
id = "shoot"
path = "assets/audio/shoot.wav"

[[assets.sounds]]
id = "explosion"
path = "assets/audio/explosion.wav"

[[assets.trackers]]
id = "music"
path = "assets/audio/bgm.xm"
```

## 3D Game with Full Assets

```toml
[game]
id = "platformer-3d"
title = "Platformer 3D"
author = "Studio Name"
version = "0.1.0"
description = "A charming 3D platformer"
tags = ["3d", "platformer", "adventure"]

# Character
[[assets.meshes]]
id = "player"
path = "assets/models/player.glb"

[[assets.skeletons]]
id = "player-skeleton"
path = "assets/models/player.glb"

[[assets.animations]]
id = "player-idle"
path = "assets/animations/idle.glb"

[[assets.animations]]
id = "player-run"
path = "assets/animations/run.glb"

[[assets.animations]]
id = "player-jump"
path = "assets/animations/jump.glb"

# Environment
[[assets.meshes]]
id = "level-01"
path = "assets/levels/level01.glb"

[[assets.textures]]
id = "ground"
path = "assets/textures/ground.png"

[[assets.textures]]
id = "sky"
path = "assets/textures/sky.png"

# Audio
[[assets.sounds]]
id = "jump"
path = "assets/sfx/jump.wav"

[[assets.sounds]]
id = "land"
path = "assets/sfx/land.wav"

[[assets.sounds]]
id = "coin"
path = "assets/sfx/coin.wav"

[[assets.trackers]]
id = "music-level1"
path = "assets/music/level1.xm"
```

## C Project

```toml
[game]
id = "c-game"
title = "C Game"
author = "C Developer"
version = "1.0.0"

[build]
script = "clang --target=wasm32 -nostdlib -O2 -o game.wasm game.c"
wasm = "game.wasm"

[[assets.textures]]
id = "tileset"
path = "assets/tileset.png"
```

## Zig Project

```toml
[game]
id = "zig-game"
title = "Zig Game"
author = "Zig Developer"
version = "1.0.0"

[build]
script = "zig build -Doptimize=ReleaseSmall"
wasm = "zig-out/bin/game.wasm"

[[assets.meshes]]
id = "world"
path = "assets/world.obj"
```

## Minimal with Custom Build

```toml
[game]
id = "custom-build"
title = "Custom Build Game"
author = "Developer"
version = "1.0.0"

[build]
script = "./build.sh"
wasm = "build/game.wasm"
```

## Asset-Heavy Game (Near Size Limit)

```toml
[game]
id = "asset-heavy"
title = "Asset Heavy Game"
author = "Studio"
version = "1.0.0"
description = "Many assets, optimized for size"

# Use compressed/optimized assets
# PNG textures: max 256x256, use indexed color where possible
# Audio: 22050Hz mono, short samples
# Meshes: low-poly, merged where possible

[[assets.textures]]
id = "atlas"
path = "assets/atlas.png"  # Single texture atlas

[[assets.meshes]]
id = "world"
path = "assets/world-merged.obj"  # Merged mesh

[[assets.sounds]]
id = "sfx-bank"
path = "assets/sfx-bank.wav"  # Combined short sounds

[[assets.data]]
id = "level-data"
path = "assets/levels.bin"  # Custom binary format
```

## Debug vs Release

The same manifest works for both:

```bash
# Release (default) - optimized, smaller
nether build

# Debug - symbols, larger, better errors
nether build --debug
```

Debug builds skip `--release` flag and use debug target directory.
