# nethercore-zx-test (LEAN VERSION)

## Priority: CRITICAL

Minimal viable testing plugin. 2 skills, 2 agents.

---

## Plugin Creation Prompt

```
Create a lean Claude Code plugin called "nethercore-zx-test" for testing Nethercore ZX games.

DESIGN PRINCIPLES:
- Minimal skills (2 max) - reference material only
- Agents do the actual work
- No overlapping content with existing plugins
- Target: <3000 tokens total skill content

CONTEXT:
- ZX uses GGRS rollback netcode requiring 100% determinism
- nether CLI: --sync-test (checksums), --p2p-test (local multiplayer)
- Replay files record input for deterministic playback
- Games run at 24/30/60/120 fps tick rates

SKILLS TO CREATE:

1. "testing-fundamentals" (v1.0.0)
   Core testing concepts in ONE consolidated skill:

   ## Sync Testing
   - `nether run --sync-test` - runs 2 instances, compares checksums
   - Pass criteria: identical checksums for 1000+ frames
   - Common failures: rand, HashMap, floats, system time

   ## Replay Testing
   - Record: `nether run --record replay.bin`
   - Playback: `nether run --replay replay.bin`
   - Regression: compare outcomes across builds

   ## Determinism Rules
   - Use zx::random(), not rand::thread_rng()
   - Use BTreeMap, not HashMap
   - Avoid floats for game logic (or use fixed-point)
   - Never use system time

   ## Test Organization
   - Unit tests: cargo test (pure logic)
   - Integration: sync test (full runtime)
   - Regression: replay comparisons

   Keywords: test, testing, sync, replay, determinism, desync

2. "benchmarking" (v1.0.0)
   Performance measurement in ONE skill:

   ## Key Metrics
   - Update time (game logic per tick)
   - Render time (draw calls per frame)
   - State size (bytes snapshotted for rollback)
   - ROM size (distribution footprint)

   ## Profiling Workflow
   - Build with --release for accurate timing
   - Use debug_watch_f32() to expose metrics
   - Target: update < 2ms, render < 8ms at 60fps

   ## State Size Analysis
   - Smaller state = faster rollback
   - Target: <100KB active game state
   - Avoid sparse allocations

   Keywords: benchmark, performance, profile, memory, speed, slow

AGENTS TO CREATE:

1. "test-runner"
   - Runs sync tests and reports results
   - Executes replay regression tests
   - Summarizes pass/fail with actionable messages
   - Tools: Bash, Read, Glob
   - Trigger: "run tests", "test my game", "check determinism"
   - Model: haiku (fast, simple task), Color: green

2. "desync-investigator"
   - Analyzes sync test failures
   - Binary search to find offending frame
   - Cross-references determinism rules
   - Provides fix suggestions
   - Tools: Read, Grep, Glob, Bash
   - Trigger: "desync", "checksum mismatch", "sync test failed"
   - Model: sonnet (complex analysis), Color: red

COMMANDS: None. Agents handle everything.
```

---

## Size Budget

| Component | Target Tokens | Content |
|-----------|---------------|---------|
| testing-fundamentals | 800 | Core concepts |
| benchmarking | 600 | Metrics + workflow |
| test-runner agent | 200 | Prompt only |
| desync-investigator agent | 300 | Prompt + rules |
| **Total** | **1900** | Under 2K target |

---

## What NOT to Include (Covered Elsewhere)

- Rollback concepts → game-design/multiplayer-design
- F3 debug panel → zx-dev/debugging-guide
- Code patterns for determinism → rollback-reviewer checks these
