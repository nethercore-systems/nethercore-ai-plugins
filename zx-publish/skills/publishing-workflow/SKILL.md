---
name: Nethercore ZX Publishing Workflow
description: This skill should be used when the user asks to "publish game", "release game", "upload game", "create ROM", "package game", "nether pack", "nether build", "build ROM", "submit to nethercore", "distribute game", "create nczx file", or mentions ROM packaging, game distribution, nethercore.systems upload, game manifest, nether CLI publishing commands, or versioning/updating published games.
version: 1.0.0
---

# Nethercore ZX Publishing Workflow

## Overview

Publishing a Nethercore ZX game involves building your WASM code, packaging assets into a ROM file, and uploading to nethercore.systems. The nether CLI handles the build pipeline.

## nether CLI Commands

The nether CLI is the primary tool for game developers:

```bash
# Initialize a new project manifest
nether init

# Compile WASM from source (runs build script)
nether compile

# Bundle WASM + assets into .nczx ROM
nether pack

# Build = compile + pack (main command)
nether build

# Build and launch in emulator
nether run
```

### Command Details

**`nether init`** - Creates `nether.toml` manifest interactively:
```bash
nether init --id my-game --title "My Game"
```

**`nether build`** - The primary build command:
```bash
nether build           # Release build
nether build --debug   # Debug build (larger, with symbols)
```

**`nether run`** - Build and test:
```bash
nether run              # Normal run
nether run --debug      # Debug build
nether run --sync-test  # Test rollback determinism
nether run --p2p-test   # Two-instance netplay test
```

## Game Manifest (nether.toml)

Every game requires a `nether.toml` in the project root:

```toml
[game]
id = "my-game"              # Unique identifier (lowercase, hyphens)
title = "My Game"           # Display name
author = "Your Name"        # Creator credit
version = "1.0.0"           # Semantic version
description = "A fun game"  # Short description (optional)
tags = ["arcade", "2d"]     # Searchable tags (optional)

[build]
# Optional: custom build script (defaults to cargo for Rust)
script = "cargo build --target wasm32-unknown-unknown --release"
wasm = "target/wasm32-unknown-unknown/release/my_game.wasm"

# Asset declarations
[[assets.textures]]
id = "player"
path = "assets/player.png"

[[assets.meshes]]
id = "level"
path = "assets/level.obj"

[[assets.sounds]]
id = "jump"
path = "assets/jump.wav"

[[assets.trackers]]
id = "music"
path = "assets/music.xm"
```

### Manifest Fields

**Required [game] fields:**
- `id` - Unique game identifier, lowercase with hyphens (e.g., `space-shooter`)
- `title` - Human-readable display name
- `author` - Developer/studio name
- `version` - Semantic version (major.minor.patch)

**Optional [game] fields:**
- `description` - Short game description
- `tags` - Array of searchable keywords

**Optional [build] fields:**
- `script` - Custom build command (defaults to cargo for Rust projects)
- `wasm` - Path to compiled WASM (auto-detected if omitted)

### Asset Types

| Type | Key | Formats | Notes |
|------|-----|---------|-------|
| Textures | `assets.textures` | PNG, JPG | Converted to GPU format |
| Meshes | `assets.meshes` | OBJ, GLTF, GLB | Converted to nczxmesh |
| Sounds | `assets.sounds` | WAV | 22050Hz, 16-bit mono |
| Music | `assets.trackers` | XM | Tracker modules |
| Skeletons | `assets.skeletons` | GLTF/GLB | Bone hierarchies |
| Animations | `assets.animations` | GLTF/GLB | Keyframe data |
| Raw Data | `assets.data` | Any | Binary blobs |

## ROM File Format

The `.nczx` ROM file bundles everything:
- Compiled WASM game code
- Pre-processed assets (GPU-ready)
- Game metadata from manifest

**Benefits:**
- Single file distribution
- Faster loading (assets pre-converted)
- Content integrity verification
- Size limits enforced (16MB max)

## Upload to nethercore.systems

### Required Files

| File | Format | Description |
|------|--------|-------------|
| Game | `.wasm` or `.nczx` | Compiled game |
| Icon | 64x64 PNG | Library thumbnail |

### Optional Files

| File | Format | Description |
|------|--------|-------------|
| Screenshots | PNG | Gallery images (up to 5) |
| Banner | 1280x720 PNG | Featured games banner |

### Upload Process

1. **Create account** at nethercore.systems/register
2. **Access dashboard** at nethercore.systems/dashboard
3. **Click "Upload New Game"**
4. **Fill in metadata:**
   - Title and description
   - Category selection
   - Tags for discovery
5. **Upload files:**
   - Game file (.wasm or .nczx)
   - Icon (required)
   - Screenshots (optional)
6. **Click "Publish"**

Your game gets a public page: `nethercore.systems/game/your-game-id`

## Versioning and Updates

### Updating a Published Game

1. **Bump version** in nether.toml:
   ```toml
   version = "1.1.0"  # Was 1.0.0
   ```

2. **Build new version:**
   ```bash
   nether build
   ```

3. **Test thoroughly:**
   ```bash
   nether run --sync-test
   ```

4. **Update on platform:**
   - Dashboard > Your Game > Edit
   - Upload new game file
   - Update version number
   - Save changes

Players with old versions see an update prompt.

### Version Guidelines

- **Major (X.0.0)** - Breaking changes, new game modes
- **Minor (0.X.0)** - New features, content additions
- **Patch (0.0.X)** - Bug fixes, balance tweaks

## Pre-Release Checklist

Before publishing, verify:

- [ ] Game builds without errors (`nether build`)
- [ ] All assets load correctly
- [ ] No console errors in browser
- [ ] Multiplayer works (`nether run --p2p-test`)
- [ ] Rollback is deterministic (`nether run --sync-test`)
- [ ] ROM under 16MB limit
- [ ] Icon is 64x64 PNG
- [ ] Description is compelling

## Troubleshooting

### "WASM validation failed"
```bash
cargo clean
cargo build --target wasm32-unknown-unknown --release
```

### "Asset not found"
Check paths in nether.toml are relative to project root:
```bash
ls assets/player.png  # Verify file exists
```

### "ROM too large"
- Compress textures (reduce resolution)
- Lower audio sample rates
- Remove unused assets
- Consider procedural generation

### "Game crashes on load"
Test locally first:
```bash
nether run --debug
```
Check browser console for panic messages.

## Alternative Distribution

Besides nethercore.systems:

- **Direct download** - Share .wasm or .nczx files
- **GitHub Releases** - Host as release artifacts
- **itch.io** - Upload as downloadable with instructions

## Reference Files

See `references/manifest-examples.md` for complete nether.toml examples for different project types (Rust, C, Zig, asset-heavy games).
