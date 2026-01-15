# CI Workflow Templates

## Basic Build Workflow

`.github/workflows/build.yml`:

```yaml
name: Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Rust
        uses: dtolnay/rust-action@stable
        with:
          targets: wasm32-unknown-unknown

      - name: Install nether CLI
        run: cargo install nether-cli

      - name: Format check
        run: cargo fmt --check

      - name: Lint
        run: cargo clippy -- -D warnings

      - name: Test
        run: cargo test

      - name: Build
        run: nether build --release

      - name: Sync test
        run: nether run --sync-test --frames 1000
```

## Release Workflow

`.github/workflows/release.yml`:

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

      - name: Install Rust
        uses: dtolnay/rust-action@stable
        with:
          targets: wasm32-unknown-unknown

      - name: Install tools
        run: |
          cargo install nether-cli
          cargo install wasm-opt

      - name: Build release
        run: |
          nether build --release
          wasm-opt -Oz game.wasm -o game.wasm

      - name: Create release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            game.nczx
            CHANGELOG.md
```

## Quality Gates

Run in order for best results:

1. `cargo fmt --check` - Fast, catches style issues
2. `cargo clippy -- -D warnings` - Catches common bugs
3. `cargo test` - Unit tests
4. `nether build --release` - Full build
5. `nether run --sync-test` - Determinism verification
