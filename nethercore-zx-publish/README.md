# Nethercore ZX Publishing Plugin

A Claude Code plugin providing guidance for publishing Nethercore ZX games to nethercore.systems.

## Features

- **Publishing Workflow** - Complete guide for ROM packaging and platform upload
- **nether CLI** - Documentation for `nether build`, `nether pack`, and related commands
- **Manifest Guide** - nether.toml configuration with examples for all project types
- **Platform Assets** - Thumbnail, screenshot, and banner creation guidance
- **Description Writing** - Templates and tips for compelling game descriptions
- **Versioning** - Update workflow for published games

## Installation

### Global Installation (Recommended)

Add to your global Claude settings (`~/.claude/settings.json` on macOS/Linux, `%USERPROFILE%\.claude\settings.json` on Windows):

```json
{
  "extraKnownMarketplaces": {
    "nethercore-ai-plugins": {
      "source": {
        "source": "github",
        "repo": "nethercore-systems/nethercore-ai-plugins",
        "path": "nethercore-zx-publish"
      }
    }
  },
  "enabledPlugins": {
    "nethercore-zx-publish@nethercore-ai-plugins": true
  }
}
```

### Workspace Installation

For nethercore contributors, add to `.claude/settings.local.json`:

```json
{
  "extraKnownMarketplaces": {
    "nethercore-ai-plugins": {
      "source": {
        "source": "directory",
        "path": "./nethercore-ai-plugins/nethercore-zx-publish"
      }
    }
  },
  "enabledPlugins": {
    "nethercore-zx-publish@nethercore-ai-plugins": true
  }
}
```

## Usage

### Slash Commands

#### `/publish-game` - Guided Publishing Workflow

Walk through the complete publishing process:

```
/publish-game              # Use current directory
/publish-game ./my-game    # Specify project path
```

This command:
1. Validates your nether.toml manifest
2. Builds your game (`nether build`)
3. Checks for required assets (icon, screenshots)
4. Runs pre-release verification
5. Provides upload instructions for nethercore.systems

#### `/prepare-platform-assets` - Create Marketing Assets

Prepare visual assets for your game's platform page:

```
/prepare-platform-assets           # Use current directory
/prepare-platform-assets ./my-game # Specify project path
```

This command helps you create:
- **Icon (64x64 PNG)** - Required for library thumbnail
- **Screenshots (up to 5)** - Recommended for game page
- **Banner (1280x720)** - Optional for featured section
- **Game Description** - Markdown copy for platform

### Auto-Triggering Skills

The skills automatically activate when you:

- Ask about publishing or releasing games
- Mention ROM packaging or .nczx files
- Work with nether CLI publishing commands
- Need help with platform assets or descriptions
- Ask about uploading to nethercore.systems

### Example Queries

**Publishing:**
- "How do I publish my game to nethercore.systems?"
- "Create a nether.toml for my project"
- "Package my game into a ROM file"
- "How do I update a published game?"

**Platform Assets:**
- "What size should my game icon be?"
- "Help me write a game description"
- "What screenshots should I capture?"
- "How do I prepare my game for the platform?"

## Publishing Requirements

### Required Files

| File | Format | Description |
|------|--------|-------------|
| Game | `.wasm` or `.nczx` | Compiled game (16MB max) |
| Icon | 64x64 PNG | Library thumbnail |

### Optional Files

| File | Format | Description |
|------|--------|-------------|
| Screenshots | PNG | Gallery images (up to 5) |
| Banner | 1280x720 PNG | Featured games section |

### Manifest (nether.toml)

```toml
[game]
id = "my-game"
title = "My Game"
author = "Developer"
version = "1.0.0"
description = "A brief description"
tags = ["arcade", "action"]

[[assets.textures]]
id = "player"
path = "assets/player.png"
```

## nether CLI Commands

| Command | Purpose |
|---------|---------|
| `nether init` | Create new nether.toml |
| `nether build` | Compile + pack ROM |
| `nether pack` | Pack assets only |
| `nether run` | Build and launch |

## License

Part of the Nethercore project.
