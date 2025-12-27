# Gap 2: Publishing Workflow

**Status:** `[x]` Completed
**Priority:** HIGH
**Plugin:** NEW (nethercore-zx-publish)
**Type:** Plugin + Skill

---

## Problem

Documentation exists in nethercore repo, but NO plugin guidance for publishing games to nethercore.systems.

## What's Missing

- ROM packaging guidance using nether CLI (`nether build`, `nether pack`)
- nether.toml manifest creation (id, title, author, version, description)
- Asset bundling into .nczx ROM files
- Upload process to nethercore.systems
- Update/versioning workflow

## Correct Commands (for game developers)

The nether CLI is the recommended tool for game developers:

```bash
# Create a new manifest
nether init

# Compile WASM + pack into ROM (main command)
nether build

# Pack only (use existing WASM)
nether pack

# Build and run in emulator
nether run
```

**Note:** `cargo xtask cart create-zx` exists but is an internal platform development tool,
NOT intended for game developers. Game developers should use the nether CLI instead.

## Prompt for Implementation

```
Create plugin "nethercore-zx-publish" with skill "publishing-workflow". Triggers:
"publish game", "release game", "upload", "create ROM", "package game", "nether pack",
"nether build". Cover: nether CLI commands (nether init, nether build, nether pack,
nether run), nether.toml manifest format (id, title, author, version, description,
build script, wasm path, asset declarations), ROM packaging into .nczx files,
nethercore.systems upload process, versioning/updates workflow. Add /publish-game
command. Source: nethercore/docs/book/src/guides/publishing.md,
nethercore/tools/nether-cli/src/main.rs. ~1500 words.
```

## Dependencies

- None (creates new plugin)

## Related Gaps

- Gap 3 (Platform Page Assets) should be added to this plugin
