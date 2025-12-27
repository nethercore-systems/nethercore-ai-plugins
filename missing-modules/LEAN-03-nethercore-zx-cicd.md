# nethercore-zx-cicd (LEAN VERSION)

## Priority: HIGH

Minimal viable CI/CD plugin. 1 skill, 1 agent.

---

## Plugin Creation Prompt

```
Create a lean Claude Code plugin called "nethercore-zx-cicd" for CI/CD automation of Nethercore ZX games.

DESIGN PRINCIPLES:
- 1 skill only - complete reference
- 1 agent for scaffolding
- Provide working templates, not theory
- Target: <2000 tokens total

CONTEXT:
- Games are Rust + WASM (wasm32-unknown-unknown)
- Build: nether build --release
- Test: cargo test + nether run --sync-test
- Publish: upload .nczx to nethercore.systems

SKILLS TO CREATE:

1. "ci-automation" (v1.0.0)
   Everything CI/CD in ONE skill:

   ## GitHub Actions Workflow
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
   - cargo fmt --check (formatting)
   - cargo clippy -- -D warnings (lints)
   - cargo test (unit tests)
   - nether build succeeds (builds)
   - --sync-test passes (determinism)

   ## Release Workflow
   ```yaml
   on:
     push:
       tags: ['v*']

   jobs:
     release:
       # ... build steps ...
       - name: Create Release
         uses: softprops/action-gh-release@v1
         with:
           files: target/game.nczx
   ```

   ## Versioning
   ```toml
   # nether.toml
   [game]
   version = "1.2.3"  # semver
   ```
   - Tag format: v1.2.3
   - Changelog: CHANGELOG.md (Keep a Changelog format)

   Keywords: CI, CD, GitHub Actions, automation, build, release, pipeline

AGENTS TO CREATE:

1. "ci-scaffolder"
   - Creates .github/workflows/ directory
   - Generates appropriate workflow file
   - Sets up quality gates
   - Documents required secrets
   - Tools: Read, Write, Glob, Bash
   - Trigger: "set up CI", "add GitHub Actions", "automate builds"
   - Model: sonnet, Color: blue

COMMANDS: None. Agent handles scaffolding.
```

---

## Size Budget

| Component | Target Tokens |
|-----------|---------------|
| ci-automation skill | 1200 |
| ci-scaffolder agent | 300 |
| **Total** | **1500** |

---

## Why So Minimal?

CI/CD is largely **copy-paste templates**. The skill provides the templates, the agent copies and customizes them. No need for 6 separate skills covering every CI provider and scenario.

Users with complex needs can customize the generated files.
