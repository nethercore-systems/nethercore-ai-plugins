# GitHub Actions Workflow Templates

## Build Workflow (.github/workflows/build.yml)

```yaml
name: Build & Test
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          targets: wasm32-unknown-unknown
          components: clippy

      - name: Cache
        uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/registry
            ~/.cargo/git
            target
          key: cargo-${{ hashFiles('**/Cargo.lock') }}

      - name: Lint
        run: cargo clippy --target wasm32-unknown-unknown -- -D warnings

      - name: Test
        run: cargo test

      - name: Build
        run: |
          cargo install nether-cli --locked || true
          nether build --release

      - name: Sync Test
        run: nether run --sync-test --frames 1000

      - name: Upload ROM
        uses: actions/upload-artifact@v4
        with:
          name: game-rom
          path: build/*.nether
          retention-days: 14
```

## Release Workflow (.github/workflows/release.yml)

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
        uses: dtolnay/rust-toolchain@stable
        with:
          targets: wasm32-unknown-unknown

      - name: Build Release
        run: |
          cargo install nether-cli --locked || true
          nether build --release

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: build/*.nether
```

## Optimized Parallel Workflow

For faster CI with parallel jobs:

```yaml
name: Build

on:
  push:
    branches: [main]
    paths: ['src/**', 'assets/**', 'Cargo.toml', 'Cargo.lock', 'nether.toml']
  pull_request:
    branches: [main]

env:
  CARGO_TERM_COLOR: always

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy
          targets: wasm32-unknown-unknown
      - uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/registry
            ~/.cargo/git
            target
          key: ${{ runner.os }}-cargo-lint-${{ hashFiles('**/Cargo.lock') }}
      - run: cargo clippy --target wasm32-unknown-unknown -- -D warnings

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/registry
            ~/.cargo/git
            target
          key: ${{ runner.os }}-cargo-test-${{ hashFiles('**/Cargo.lock') }}
      - run: cargo test

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          targets: wasm32-unknown-unknown
      - uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/registry
            ~/.cargo/git
            target
          key: ${{ runner.os }}-cargo-build-${{ hashFiles('**/Cargo.lock') }}
      - run: cargo install nether-cli --locked || true
      - run: nether build --release
      - uses: actions/upload-artifact@v4
        with:
          name: game-rom
          path: build/*.nether
          retention-days: 14
```

## Changelog Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.0.0] - YYYY-MM-DD
### Added
- Initial release

[Unreleased]: https://github.com/user/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```
