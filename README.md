# Nethercore AI Plugins

Prompt packs (skills + task agents) for Nethercore fantasy console game development.

## Plugins

| Plugin | Purpose |
|--------|---------|
| `nethercore` | Platform tooling: build, test, optimize, publish |
| `zx` | ZX console: FFI reference, specs, rendering |

## Quick Start

```bash
# Build and run
nether build
nether run

# Test determinism
nether run --sync-test

# Release
nether build --release
```

## Installation

### Claude Code

Add to your settings (example: `.claude/settings.local.json`):

```json
{
  "enabledPlugins": {
    "nethercore@nethercore-ai-plugins": true,
    "zx@nethercore-ai-plugins": true
  }
}
```

### Other AI coding assistants

Open the relevant `SKILL.md` (and optional `references/*.md`) and paste the guidance into your assistant when needed:

- `nethercore/skills/*/SKILL.md`
- `zx/skills/*/SKILL.md`

## Skills Overview

### nethercore (console-agnostic)

- **development** - nether CLI, nether.toml manifest, determinism rules
- **testing** - sync testing, replay testing, benchmarking
- **optimization** - WASM, texture, mesh, audio size reduction
- **publishing** - ROM packaging, platform upload, CI/CD workflows

### zx (ZX console-specific)

- **ffi-reference** - 250+ FFI functions for rendering, input, audio
- **console-specs** - 960x540 resolution, 16MB ROM, 4MB RAM/VRAM
- **rendering** - Cameras, stencil effects, particles, custom fonts

## Asset Generation

For procedural asset generation, use **speccade** (separate repository).

## Architecture

- **nethercore** handles all console-agnostic platform tooling
- **zx** (and future consoles) contain console-specific FFI and specs
- All consoles share the same WASM core, so determinism is universal

## License

Licensed under either of:
- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT license ([LICENSE-MIT](LICENSE-MIT))

at your option.
