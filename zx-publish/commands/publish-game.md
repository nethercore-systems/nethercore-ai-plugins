---
description: Guided publishing workflow for Nethercore ZX games
argument-hint: "[project-path]"
allowed-tools: ["Read", "Bash", "AskUserQuestion", "Write"]
---

# Publish Game Workflow

Guide the user through publishing their ZX game to nethercore.systems.

## Steps

### 1. Locate Project
Check for `nether.toml` in current directory or provided path.

### 2. Validate Manifest
Required fields: `[game].id`, `title`, `author`, `version`

If description missing, offer to help write one using platform-assets skill templates.

### 3. Build Check
```bash
nether build
```

### 4. Asset Inventory
Check for:
- Icon (64x64 PNG) - required
- Screenshots - recommended
- Banner (1280x720) - optional

If icon missing, suggest `/prepare-platform-assets`.

### 5. Pre-Release Tests
If multiplayer:
```bash
nether run --sync-test
```

### 6. Size Check
Compare ROM to 16MB limit.

### 7. Upload Checklist
Present summary:
- Game file path
- Asset status
- Manifest completeness

### 8. Upload Instructions
Direct user to:
1. nethercore.systems/dashboard
2. "Upload New Game"
3. Fill metadata, upload files
4. Publish

Game page: `nethercore.systems/game/[id]`

### 9. Post-Publish
Remind about:
- Sharing game page URL
- Version updates (bump version, rebuild, re-upload)
