# Nethercore ZX Development Plugin

A Claude Code plugin providing comprehensive game development guidance for the Nethercore ZX fantasy console.

## Features

- **Complete FFI Reference** - All 250+ FFI functions documented for Rust, C/C++, and Zig
- **Project Templates** - Ready-to-use project structures for all supported languages
- **Asset Pipeline** - Guidance for textures, meshes, sounds, and XM tracker files
- **CLI Tooling** - Full documentation for `nether` CLI and `cargo xtask` commands
- **Working Examples** - Complete hello-world and game-with-assets examples
- **Project Scaffolding** - `zx-dev:new-game` creates complete starter projects
- **Rollback Safety Review** - Agent analyzes code for netcode/determinism issues
- **Replay Debugging** - Generate NCRS scripts to reproduce bugs, run tests, and analyze results

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
        "path": "zx-dev"
      }
    }
  },
  "enabledPlugins": {
    "zx-dev@nethercore-ai-plugins": true
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
        "path": "./nethercore-ai-plugins/zx-dev"
      }
    }
  },
  "enabledPlugins": {
    "zx-dev@nethercore-ai-plugins": true
  }
}
```

## Usage

### Slash Commands

Commands are documented in `plugin:command` form (e.g. `zx-dev:new-game`). Depending on your Claude/Codex client, they may also appear as slash commands (e.g. `/new-game`).

#### `zx-dev:new-game` - Create a New Project

Scaffold a complete ZX game project with working starter code:

```
zx-dev:new-game rust my-game     # Create a Rust project named "my-game"
zx-dev:new-game c platformer     # Create a C project
zx-dev:new-game zig shooter      # Create a Zig project
zx-dev:new-game                  # Interactive mode - asks for language and name
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

### Replay Debugging Commands

Debug games using scriptable replay tests:

#### `zx-dev:replay-test` - Generate Test Script

Create a minimal NCRS script from a bug description:

```
zx-dev:replay-test jump not working     # Generate test for jump issues
zx-dev:replay-test player clips through walls
zx-dev:replay-test                       # Interactive - asks for description
```

#### `zx-dev:replay-analyze` - Analyze Test Report

Parse a replay report to identify root causes:

```
zx-dev:replay-analyze report.json       # Analyze specific report
zx-dev:replay-analyze                   # Find and analyze most recent report
```

#### `zx-dev:replay-template` - Generate Template

Create starter templates for common test scenarios:

```
zx-dev:replay-template jump             # Jump mechanics template
zx-dev:replay-template collision        # Collision detection template
zx-dev:replay-template movement         # Movement template
zx-dev:replay-template physics          # Frame-by-frame physics
zx-dev:replay-template input            # Input handling template
```

### Replay Debugger Agent

Autonomous replay-based debugging. Generates scripts, runs tests, analyzes results, and suggests fixes:

**Triggers on:**
- "Debug why my player clips through platforms"
- "Investigate the double-jump bug"
- "Verify the jump fix is working"

**Workflow:**
1. Understands bug from description
2. Discovers available debug variables
3. Generates minimal test script
4. Runs `nether replay run` headlessly
5. Analyzes report to identify root cause
6. Suggests fix with code references

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
