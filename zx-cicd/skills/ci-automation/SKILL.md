---
name: CI Automation
description: This skill provides CI/CD automation templates for Nethercore ZX games. Use when the user asks about "CI", "CD", "GitHub Actions", "automation", "build pipeline", "release workflow", "continuous integration", "quality gates", or "automate my builds".
version: 1.0.0
---

# CI/CD Automation for Nethercore ZX

Automate building, testing, and releasing ZX games with GitHub Actions.

## GitHub Actions Build Workflow

Create `.github/workflows/build.yml`:

```yaml
name: Build & Test
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: dtolnay/rust-action@stable
        with:
          targets: wasm32-unknown-unknown

      - name: Cache
        uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/registry
            ~/.cargo/git
            target
          key: cargo-${{ hashFiles('**/Cargo.lock') }}

      - name: Lint
        run: cargo clippy -- -D warnings

      - name: Test
        run: cargo test

      - name: Build
        run: nether build --release

      - name: Sync Test
        run: nether run --sync-test --frames 1000

      - name: Upload ROM
        uses: actions/upload-artifact@v4
        with:
          name: game-rom
          path: target/game.nczx
```

## Quality Gates

Run these checks in order:

| Gate | Command | Purpose |
|------|---------|---------|
| Format | `cargo fmt --check` | Code style |
| Lint | `cargo clippy -- -D warnings` | Static analysis |
| Unit Test | `cargo test` | Logic correctness |
| Build | `nether build --release` | WASM compilation |
| Sync Test | `nether run --sync-test --frames 1000` | Determinism |

## Release Workflow

Create `.github/workflows/release.yml` for tag-triggered releases:

```yaml
name: Release
on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: dtolnay/rust-action@stable
        with:
          targets: wasm32-unknown-unknown

      - name: Build Release
        run: nether build --release

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: target/game.nczx
```

## Versioning

Use semantic versioning in `nether.toml`:

```toml
[game]
version = "1.2.3"
```

**Tag format**: `v1.2.3`

**Release process**:
1. Update version in `nether.toml`
2. Update `CHANGELOG.md` (Keep a Changelog format)
3. Commit: `git commit -m "Release v1.2.3"`
4. Tag: `git tag v1.2.3`
5. Push: `git push && git push --tags`

## Changelog Format

```markdown
# Changelog

## [1.2.3] - 2024-01-15
### Added
- New enemy type

### Fixed
- Player collision bug
```
