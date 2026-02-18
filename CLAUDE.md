# Nethercore AI Plugins

This repo contains prompt packs for Nethercore game development (skills + task agents).

## Plugins

### nethercore

Platform tooling (console-agnostic):
- **development** - nether CLI, nether.toml, determinism rules, netcode disclaimer
- **testing** - sync testing, replay testing, benchmarking, debug actions
- **optimization** - WASM, texture, mesh, audio optimization
- **publishing** - ROM packaging, platform upload, CI/CD
- **debugging** - F4 Debug Inspector, live value editing, frame control (all consoles)

Agents: `build-analyzer`, `replay-debugger`

### zx

ZX fantasy console specifics:
- **ffi-reference** - ZX FFI bindings (250+ functions)
- **console-specs** - Resolution, memory limits, render modes
- **rendering** - Cameras, stencil effects, particles, fonts, 2D vs 3D guide

## Installation

Add to `.claude/settings.local.json`:

```json
{
  "enabledPlugins": {
    "nethercore@nethercore-ai-plugins": true,
    "zx@nethercore-ai-plugins": true
  }
}
```

## Architecture

- **nethercore** handles all console-agnostic tooling
- **zx** (and future consoles) contain console-specific FFI and specs
- All consoles share the same WASM core, so determinism is universal

## Related

- Asset generation: Use **speccade** (separate repo)
- FFI source: `nethercore/include/zx.rs`

## Standards

Skills follow the [SKILL.md open standard](https://agentskills.io/specification):
- `name` must be lowercase-hyphenated, matching the parent directory name
- `description` must explain WHAT + WHEN, max 1024 chars
- `version` goes under `metadata.version` (not top-level)
- `license` and `metadata.author` recommended for all skills

## Authoring Note

Keep `skills/` and `agents/` content assistant-agnostic (avoid vendor/tool-specific wording). The `.claude-plugin/` folders are just the loader format.
