# nether CLI commands

Authority: `nethercore/tools/nether-cli/src/main.rs` and the selected executable's `--help`. These commands describe the audited CLI, not hypothetical future console tooling.

| Command | Purpose |
|---|---|
| `nether init` | Create `nether.toml` |
| `nether compile` | Run build script, locate WASM |
| `nether pack` | Pack existing WASM and manifest assets |
| `nether build` | Compile + pack, release by default |
| `nether build --debug` | Debug build |
| `nether run --no-build` | Launch existing cart |
| `nether run --watch` | Watch/rebuild/relaunch |
| `nether run --no-build --sync-test --check-distance 2 --players 1 --exit-after-frames 120` | Bounded sync smoke |
| `nether run --no-build --replay smoke.ncrs` | Real-player scripted input/captures |
| `nether preview` | Asset inspection; inspect its help for arguments |
| `nether replay compile smoke.ncrs -o smoke.ncrp` | Script-to-binary compilation, not game execution |

Use `-p <game-dir>` when outside the project. Keep an outer timeout and inspect runtime errors and actual completion. The frame limit counts advanced input frames, not all rollback re-simulation ticks.

Do not use old `build --release`, `build --verbose`, `run --frames`, `run --record`, or `nether test`. Do not treat `.bin` as interchangeable with `.ncrs` scripts or `.ncrp` binary replays. Discover recording/binary playback support through `nether replay --help` and actual implementation before promising it.

For semantic regression, use matching `nether` and `nethercore-zx` builds:

```bash
nether replay validate tests/smoke.ncrs
nether replay run tests/smoke.ncrs --rom game.nczx --headless --report replay-report.json --timeout 30
```

Replace `game.nczx` with the actual packed cart. Require zero exit, completed `PASSED` report, meaningful snapshots/assertions, and a deliberate failing control. Older binaries used a false-green placeholder. Rendered replay accepts inputs/screenshots only and rejects actions/assertions/semantic snapshots; headless rejects screenshots. See the testing skill for frame and state semantics.
