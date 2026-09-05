# Executable replay scripts (.ncrs)

Scripts are TOML. First discover the actual game's registered semantic state.
Save this as `tests/inspect.ncrs` inside a game project:

```toml
console = "zx"
seed = 12345
players = 1

[[frames]]
f = 0
snap = true

[[frames]]
f = 1
p1 = "a"
snap = true

[[frames]]
f = 2
p1 = "idle"
snap = true
```

Run after building (replace the ROM filename with the actual build output):

```bash
nether replay validate tests/inspect.ncrs
nether replay run tests/inspect.ncrs --rom game.nczx --headless --report inspect.json --timeout 30
```

Unspecified frames and players are idle; inputs do not persist. Repeat an input
on every frame it must be held. Frame indices start at zero. `p1` addresses
player index 0. An action runs before that frame's update; snapshots show
pre/post-update values, and assertions evaluate post-update state. The script
seed/player count configure the game before initialization. Replay does not load
or write persistent saves. `$prev_name` means the preceding tick, not the last
captured snapshot. Floating comparisons use registered f32 precision, not an
arbitrary epsilon; integer comparisons stay exact.

Use names emitted by the report. For example, **if the game registers** a
`match/score_p1` value and a `Force Point` action accepting `scorer`:

```toml
[[frames]]
f = 3
action = "Force Point"
action_params = { scorer = 0 }
snap = true
assert = "$match_score_p1 == 1"
```

The parameter key is `action_params`, not `params`. Use exact registered action
labels and declared parameter types. Compare snapshots on two identical runs
for repeatability. Retain scenario assertions to detect incorrect yet perfectly
deterministic gameplay. An empty state map is not semantic coverage: register
relevant watches in the game first.

For rendered playback, create `tests/visual.ncrs` containing only inputs and
`screenshot = true`, then use `nether run --replay tests/visual.ncrs`. Actions,
assertions and `snap` are rejected in rendered mode; screenshots are rejected
in headless mode. Semantic snapshots are not restorable save states. Binary
checkpoint/seek helpers are not a complete time-travel debugger and do not
replace replaying from a correctly initialized game.

The checked-in `tests/replay/` scenarios in this plugin repository are exercised
by `python scripts/verify_agent_workflow.py --rebuild-games`; they target actual sibling games,
not invented example names.
