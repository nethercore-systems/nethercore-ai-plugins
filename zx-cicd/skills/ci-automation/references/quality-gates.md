# Quality Gates Configuration

## Gate Tiers

### Tier 1: Must Have

**Clippy (lint):**
```yaml
- name: Clippy
  run: cargo clippy --target wasm32-unknown-unknown -- -D warnings
```

**Tests:**
```yaml
- name: Test
  run: cargo test
```

**Build:**
```yaml
- name: Build
  run: nether build --release
```

### Tier 2: Should Have

**Format check:**
```yaml
- name: Format
  run: cargo fmt --check
```

**Sync test:**
```yaml
- name: Sync Test
  run: nether run --sync-test --frames 500
```

**Size check:**
```yaml
- name: Check ROM Size
  env:
    MAX_SIZE_MB: 16
  run: |
    MAX_BYTES=$((MAX_SIZE_MB * 1024 * 1024))
    SIZE=$(stat -c%s build/*.nether 2>/dev/null || stat -f%z build/*.nether)
    SIZE_MB=$(echo "scale=2; $SIZE / 1024 / 1024" | bc)
    echo "ROM Size: ${SIZE_MB} MB"
    if [ $SIZE -gt $MAX_BYTES ]; then
      echo "::error::ROM size ${SIZE_MB}MB exceeds ${MAX_SIZE_MB}MB limit!"
      exit 1
    fi
```

### Tier 3: Nice to Have

**Documentation:**
```yaml
- name: Doc
  run: cargo doc --no-deps
```

**Security audit:**
```yaml
- name: Audit
  run: cargo audit
```

## Comprehensive Quality Gate Workflow

```yaml
name: Quality Gates

on:
  pull_request:
    branches: [main]

env:
  CARGO_TERM_COLOR: always
  ROM_SIZE_LIMIT: 16777216

jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt
      - run: cargo fmt --check

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy
          targets: wasm32-unknown-unknown
      - run: cargo clippy --target wasm32-unknown-unknown -- -D warnings

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - run: cargo test

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          targets: wasm32-unknown-unknown
      - run: cargo install nether-cli --locked || true
      - run: nether build --release
      - name: Check ROM Size
        run: |
          SIZE=$(stat -c%s build/*.nether 2>/dev/null || stat -f%z build/*.nether)
          echo "ROM Size: $SIZE bytes"
          if [ $SIZE -gt $ROM_SIZE_LIMIT ]; then
            echo "::error::ROM size exceeds limit!"
            exit 1
          fi

  sync-test:
    runs-on: ubuntu-latest
    needs: [build]
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          targets: wasm32-unknown-unknown
      - run: cargo install nether-cli --locked || true
      - run: nether run --sync-test --frames 500
```

## Branch Protection Setup

After adding quality gates, configure GitHub:

1. Go to Settings → Branches → Add branch protection rule
2. Branch name pattern: `main`
3. Enable:
   - Require a pull request before merging
   - Require status checks to pass before merging
   - Required checks: `lint`, `test`, `build`, `sync-test` (if multiplayer)
