# nethercore-zx-cicd

CI/CD automation plugin for Nethercore ZX games.

## Overview

Provides GitHub Actions templates and workflow scaffolding for building, testing, and releasing ZX games.

## Components

### Skills

- **ci-automation** - Complete CI/CD reference with GitHub Actions workflows, quality gates, and release automation

### Agents

- **ci-scaffolder** - Creates `.github/workflows/` with build and release pipelines

## Usage

### Get CI/CD guidance

Ask about CI/CD patterns:
- "How do I set up GitHub Actions for my ZX game?"
- "What quality gates should I use?"
- "How do I automate releases?"

### Scaffold workflows

Let the agent create files for you:
- "Set up CI for my game"
- "Add GitHub Actions"
- "Automate my builds"

## Quality Gates

The generated workflows include:

| Gate | Command | Purpose |
|------|---------|---------|
| Format | `cargo fmt --check` | Code style |
| Lint | `cargo clippy -- -D warnings` | Static analysis |
| Unit Test | `cargo test` | Logic correctness |
| Build | `nether build --release` | WASM compilation |
| Sync Test | `nether run --sync-test` | Determinism verification |

## Installation

Add to `.claude/settings.local.json`:

```json
{
  "enabledPlugins": {
    "nethercore-zx-cicd@nethercore-ai-plugins": true
  }
}
```

## License

MIT/Apache-2.0
