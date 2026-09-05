---
name: testing
description: >-
  Test Nethercore games with real ROM-backed replay assertions, semantic state
  snapshots, debug actions, and bounded rollback sync tests. Use for regression
  testing, automated game verification, and desync diagnosis.
license: Apache-2.0
compatibility: Requires matching nether and nethercore-zx binaries. Works offline.
metadata:
  author: nethercore-systems
  version: "1.1.0"
---

# Nethercore Testing

## Real replay regression

From a game project with `nether.toml` and an authored `tests/smoke.ncrs`:

```bash
nether build
nether replay validate tests/smoke.ncrs
nether replay run tests/smoke.ncrs --rom game.nczx --headless --report replay-report.json --timeout 30
```

Replace `game.nczx` with the ROM produced from `[game].id`. The matching
`nethercore-zx` executable must be alongside `nether` or discoverable by its
player lookup. Validation checks syntax only; **only ROM-backed execution tests
actual gameplay**. No recording command is provided: author `.ncrs` text scripts.

Require both a zero exit status and a completed `PASSED` report. A timeout,
missing action/variable, trap, failed assertion, or desync is not a pass. Keep
an intentionally false assertion as a negative control when establishing CI.
Use fresh report paths; never interpret an old report after a failed invocation.

## Expose meaningful state

Register `debug_watch_*` or `debug_register_*` pointers in `init()` for stable,
rollback-backed fields: phase, health, position, score, current rule state.
The runner reads these through the existing debug registry. Use group-qualified
names shown in the report, not guessed names or fixed WASM addresses. Keep
pointers valid; for movable game structs use stable shadow statics refreshed
in `update()` and after debug actions. Actions set up scenarios; inputs must
still test the actual rules. Discover available names with a `snap = true`
frame before writing assertions.

See `references/replay-format.md` for a complete discovery script and frame
semantics. Check sound, readability, and game feel through rendered playback
and human review separately; headless success is not an artistic verdict.

## Rollback determinism

```bash
nether run --sync-test --exit-after-frames 1000
```

This uses GGRS to restore/re-simulate and compare checksums; it is not two
independent rendered game instances. The command above requires a display.
A bounded successful run proves only that tested sequence, not every game path
or cross-platform determinism. Test input-rich game scenarios as well as idle.

State belongs in WASM linear memory plus the engine's rollback state. Mutable
WASM globals/tables are not snapshotted; avoid memory growth after init. Use
engine RNG/time/input and keep simulation mutations out of `render()`.

## Executable cross-game check

From this plugin repository, with the sibling engine binaries and game ROMs built:

```bash
python scripts/verify_agent_workflow.py
```

This runs semantic scenarios for Volley Fighter and Scrapheap Saints, repeats
them to compare state snapshots, and checks deliberate failures. Missing game
ROMs fail rather than skip. Pass explicit paths with `--help` for other layouts.
