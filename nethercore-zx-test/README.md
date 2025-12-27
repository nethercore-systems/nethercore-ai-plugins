# nethercore-zx-test

Testing and quality assurance plugin for Nethercore ZX games.

## Overview

This plugin provides testing workflows for Nethercore ZX games, focusing on determinism verification (critical for GGRS rollback netcode) and performance benchmarking.

## Skills

### testing-fundamentals

Core testing concepts for ZX games:
- Sync testing with `nether run --sync-test`
- Replay-based regression testing
- Determinism rules and common desync causes
- Test organization (unit, sync, replay)

**Triggers:** "sync testing", "replay testing", "determinism", "desync", "checksums", "test my game"

### benchmarking

Performance measurement and optimization:
- Key metrics (update time, render time, state size, ROM size)
- Profiling workflow with debug watches
- Frame budget guidance for rollback
- State size analysis for faster rollbacks

**Triggers:** "benchmark", "performance", "profile", "memory", "speed", "slow"

## Agents

### test-runner

Runs sync tests and replay regression tests, reporting pass/fail with actionable messages.

- **Model:** haiku (fast execution)
- **Color:** green
- **Tools:** Bash, Read, Glob

**Triggers:** "run tests", "test my game", "check determinism"

### desync-investigator

Analyzes sync test failures to find non-deterministic code.

- **Model:** sonnet (complex analysis)
- **Color:** red
- **Tools:** Read, Grep, Glob, Bash

**Triggers:** "desync", "checksum mismatch", "sync test failed"

## Installation

Add to your `.claude/settings.local.json`:

```json
{
  "enabledPlugins": {
    "nethercore-zx-test@nethercore-ai-plugins": true
  }
}
```

## Usage Examples

**Run sync tests:**
> "Run tests on my game"

**Investigate desync:**
> "My sync test failed at frame 247, help me find the issue"

**Check performance:**
> "How do I benchmark my game's performance?"

## License

MIT/Apache-2.0
