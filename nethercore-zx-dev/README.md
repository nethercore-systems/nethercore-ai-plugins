# Nethercore ZX Development Plugin

A Claude Code plugin providing comprehensive game development guidance for the Nethercore ZX fantasy console.

## Features

- **Complete FFI Reference** - All 250+ FFI functions documented for Rust, C/C++, and Zig
- **Project Templates** - Ready-to-use project structures for all supported languages
- **Asset Pipeline** - Guidance for textures, meshes, sounds, and XM tracker files
- **CLI Tooling** - Full documentation for `nether` CLI and `cargo xtask` commands
- **Working Examples** - Complete hello-world and game-with-assets examples
- **Project Scaffolding** - `/new-game` command creates complete starter projects
- **Rollback Safety Review** - Agent analyzes code for netcode/determinism issues

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
        "path": "nethercore-zx-dev"
      }
    }
  },
  "enabledPlugins": {
    "nethercore-zx-dev@nethercore-ai-plugins": true
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
        "path": "./nethercore-ai-plugins/nethercore-zx-dev"
      }
    }
  },
  "enabledPlugins": {
    "nethercore-zx-dev@nethercore-ai-plugins": true
  }
}
```

## Usage

### Slash Commands

#### `/new-game` - Create a New Project

Scaffold a complete ZX game project with working starter code:

```
/new-game rust my-game     # Create a Rust project named "my-game"
/new-game c platformer     # Create a C project
/new-game zig shooter      # Create a Zig project
/new-game                  # Interactive mode - asks for language and name
```

Creates a ready-to-build project with:
- Proper directory structure
- Working hello-world code
- Build configuration (Cargo.toml, Makefile, or build.zig)
- Game manifest (nether.toml)
- FFI bindings included

### Rollback Safety Reviewer

The plugin includes an agent that analyzes your game code for determinism issues that would break multiplayer netcode:

**Triggers automatically when you ask:**
- "Check my game for rollback issues"
- "Is this code rollback-safe?"
- "My multiplayer game keeps desyncing"
- "Review netcode compatibility"

**Detects:**
- Unsafe random sources (must use FFI `random()` instead of `rand::random()`)
- System time access (must use FFI `delta_time()` instead of `Instant::now()`)
- HashMap iteration order issues
- State mutations in `render()` instead of `update()`
- Floating point precision hazards
- Uninitialized memory

### Auto-Triggering Skill

The skill automatically activates when you:

- Ask to create a Nethercore ZX game or example
- Mention ZX FFI functions, zx.rs, zx.h, or zx.zig
- Work with nether.toml or the nether CLI
- Develop WASM games for Nethercore

### Example Queries

- "Create a new Nethercore ZX game in Rust"
- "How do I load textures in ZX?"
- "Show me the input handling FFI functions"
- "Create a nether.toml for my game with textures and sounds"
- "Build a hello world example in C"
- "Check my game for rollback safety issues"

## Console Specifications

| Spec | Value |
|------|-------|
| Resolution | 960x540 (fixed) |
| Color Depth | RGBA8 |
| Tick Rate | 24/30/60/120 fps |
| ROM Size | 16MB max |
| WASM Memory | 4MB |
| VRAM | 4MB |
| Max Players | 4 (local + remote) |
| Netcode | GGRS rollback |

## License

Part of the Nethercore project.
