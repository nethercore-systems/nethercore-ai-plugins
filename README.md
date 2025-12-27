# Nethercore AI Plugins

Official AI-powered development plugins for Nethercore game development. Currently supports Claude Code, with potential for other AI tools in the future.

## Available Plugins

| Plugin | Description | AI Platform |
|--------|-------------|-------------|
| [nethercore-zx-dev](./nethercore-zx-dev/) | ZX fantasy console game development | Claude Code |

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

For nethercore contributors who have cloned the workspace, add to `.claude/settings.local.json`:

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

## Quick Start

Once installed, you can start building ZX games anywhere:

```
/new-game rust my-game    # Create a new Rust game project
cd my-game
nether run                # Build and launch
```

## Plugin Details

### nethercore-zx-dev

**Features:**
- Complete FFI reference (250+ functions)
- Project scaffolding (`/new-game` command)
- Rollback safety code review (automatic agent)
- Templates for Rust, C, and Zig
- Asset pipeline guidance

**Usage:**
- `/new-game [language] [name]` - Create new game project
- Ask "check my game for rollback issues" - Analyze for netcode safety
- Ask about ZX FFI, input handling, graphics, audio, etc.

See [nethercore-zx-dev/README.md](./nethercore-zx-dev/README.md) for full documentation.

## Contributing

Plugins are developed in this repository. Each plugin has its own directory with:
- `plugin.json` - Plugin manifest
- `skills/` - Auto-triggering knowledge skills
- `commands/` - Slash commands
- `agents/` - Specialized sub-agents

## License

Part of the Nethercore project.
