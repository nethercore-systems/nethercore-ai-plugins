# Replay scripts and verification

Authority: `nethercore/core/src/replay/script/{ast,compiler}.rs` plus actual player and CLI callers. NCRS scripts are TOML; NCRP is the compiled binary format.

```toml
console = "zx"
seed = 12345
players = 1

[[frames]]
f = 0
screenshot = true

[[frames]]
f = 1
p1 = "right"

[[frames]]
f = 2
p1 = "right+a"

[[frames]]
f = 8
screenshot = true
```

Right is held for two ticks, not through frame 8. Missing frames/players are idle; last frame determines script length. Avoid duplicate frame entries; construct the intended frame's full input rather than assuming entries merge.

```bash
nether replay compile smoke.ncrs -o smoke.ncrp
nether run --no-build --replay smoke.ncrs
```

Use the same cart/input/seed for a comparison. Read exact screenshot paths from runtime logs and inspect them; do not assume output goes next to the script. Delete only task-owned captures.

Parser-supported `snap`, `assert`, `action`, `action_params` are not proof of runtime execution. The audited CLI headless path uses a simplified runner without game WASM. Inspect assertion/action call sites before using them as gates; otherwise use native rule assertions and real-player input/rendering probes.

No `nether run --record` or `run --frames` in the audited CLI. Inspect `nether replay --help` and implementation before using recording or binary-playback commands. Do not use graphical player commands on a bare headless CI runner without verified display/GPU support.
