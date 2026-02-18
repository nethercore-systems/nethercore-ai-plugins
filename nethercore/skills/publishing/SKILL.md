---
name: publishing
description: >-
  Publishing Nethercore games to nethercore.systems. Covers ROM packaging with
  nether pack, release builds, platform upload requirements, versioning, and
  CI/CD pipeline setup with GitHub Actions. Use when preparing a game for
  release or setting up automated builds.
license: Apache-2.0
compatibility: Requires nether CLI. Needs network for upload.
metadata:
  author: nethercore-systems
  version: "1.0.0"
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
