---
name: Nethercore Publishing
description: |
  Publishing Nethercore games. Triggers on "publish game", "release", "upload", "ROM packaging", "nether pack", "CI/CD", "GitHub Actions".

  **Load references when:**
  - ROM packaging details -> `references/rom-packaging.md`
  - CI workflow templates -> `references/ci-workflows.md`
version: 1.0.0
---

# Nethercore Publishing

## Build Commands

| Command | Purpose |
|---------|---------|
| `nether build` | compile + pack (development) |
| `nether build --release` | Optimized release build |
| `nether pack` | Bundle WASM + assets into ROM |

## Upload to nethercore.systems

**Required:**
| File | Format |
|------|--------|
| Game | `.wasm` or `.nczx` |
| Icon | 64x64 PNG |

**Optional:**
- Screenshots (PNG, up to 5)
- Banner (1280x720 PNG)

**Process:**
1. Create account at nethercore.systems
2. Dashboard -> "Upload New Game"
3. Fill metadata, upload files
4. Publish

## Pre-Release Checklist

- [ ] `nether build --release` succeeds
- [ ] `nether run --sync-test` passes
- [ ] ROM under 16MB
- [ ] Icon is 64x64 PNG
- [ ] Description is compelling
- [ ] Version updated in nether.toml

## Versioning

Semantic versioning in `nether.toml`:

```toml
[game]
version = "1.2.3"
```

**Update process:**
1. Bump version in nether.toml
2. Update CHANGELOG.md
3. Commit, tag, push
4. Re-upload to platform

## CI/CD Quick Reference

| Gate | Command | Purpose |
|------|---------|---------|
| Format | `cargo fmt --check` | Code style |
| Lint | `cargo clippy -- -D warnings` | Static analysis |
| Test | `cargo test` | Logic correctness |
| Build | `nether build --release` | WASM compilation |
| Sync | `nether run --sync-test --frames 1000` | Determinism |

See `references/ci-workflows.md` for GitHub Actions templates.
