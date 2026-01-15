# Replay Format (NCRS)

## Overview

Nethercore replays use the NCRS format to record input sequences for deterministic playback.

## Recording

```bash
nether run --record my_replay.bin
```

Records:
- Initial random seed
- Frame-by-frame input state
- Player configurations

## Playback

```bash
nether run --replay my_replay.bin
```

Replays inputs exactly, producing identical game state if code is deterministic.

## Regression Testing Workflow

1. **Record golden replay** on known-good build:
   ```bash
   git checkout v1.0.0
   nether run --record golden.bin
   # Play through test scenario
   ```

2. **Test new build** against golden replay:
   ```bash
   git checkout feature-branch
   nether run --replay golden.bin
   # Should produce identical results
   ```

3. **Automate in CI**:
   ```yaml
   - name: Replay regression
     run: nether run --replay tests/golden.bin --frames 1000
   ```

## Debug Replay

For debugging specific issues:

```bash
# Record bug reproduction
nether run --record bug_repro.bin
# Play until bug manifests

# Replay to debug
nether run --replay bug_repro.bin
# Add logging, breakpoints as needed
```
