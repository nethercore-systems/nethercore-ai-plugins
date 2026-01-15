# ROM Packaging

## Package Contents

A Nethercore ROM (`.nczx`) contains:
- Compiled WASM binary
- Packed assets (textures, meshes, audio)
- Game manifest metadata

## Build Process

```bash
# Development build
nether build

# Release build (optimized)
nether build --release

# Just pack (skip compile)
nether pack
```

## Release Optimization

For release builds:

1. **Cargo optimization**:
   ```toml
   [profile.release]
   lto = true
   opt-level = "z"
   ```

2. **Post-process WASM**:
   ```bash
   wasm-opt -Oz game.wasm -o game.wasm
   ```

3. **Verify size**:
   ```bash
   nether build --verbose
   # Check total ROM size < 16 MB
   ```

## Platform Assets

For nethercore.systems upload:

| Asset | Size | Format |
|-------|------|--------|
| Icon | 64x64 | PNG |
| Screenshot | 960x540 | PNG |
| Banner | 1280x720 | PNG |

## Manifest Example

```toml
[game]
id = "my-game"
title = "My Game"
author = "Developer Name"
version = "1.0.0"
description = "A brief, compelling description"
tags = ["action", "multiplayer", "arcade"]
```
