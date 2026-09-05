# Known implementation contradictions

Source snapshot: Nethercore `b1d589ce4915ec63700be0520970c94be4ffbe34` (2026-09-05). These are findings, **not source fixes**. Re-read current source before acting; runtime/player edits in a local working tree may supersede them. Canonical ZX ABI: `include/zx.rs`; compare modular bindings/host behavior when prose conflicts.

## Raw WAV packing (high)

`tools/nether-cli/src/pack/assets/audio.rs::load_sound` reads RIFF/data bytes as i16 without interpreting sample-rate/channel/bit-depth metadata despite a conversion promise. It can silently misplay common stereo/44100 Hz/float WAV; truncated extents/odd data also need validation.

Workaround: author and verify **22050 Hz mono 16-bit PCM** before raw packing. The existing `tools/nether-export/src/audio.rs::convert_wav` provides a decoder/conversion starting point, not a guarantee of hardened malformed/empty input handling. A separately authorized fix should cover preservation, conversion, malformed/truncated input and both callers with a small regression.

## Resolved: false-positive headless replay

The initial audit found placeholder execution without game WASM. The real ROM-backed runner now executes seeded scripts, registered actions, typed semantic snapshots and assertions, with nonzero failure exits. Build matching `nether-cli` and `nethercore-zx` from the replay implementation; older binaries may retain the defect.

Use the testing skill and `scripts/verify_agent_workflow.py --rebuild-games` for executable cross-game checks and negative controls. Rendered replay is inputs/screenshots-only; semantic snapshots are observations, not restorable checkpoints. Reuse `Runtime::run_scripted_sync_test` for rollback checks instead of adding another runtime.

## Animated rig ceiling (medium)

`tools/nether-export/src/skeleton.rs` and runtime skeleton storage accept 256 bones, but animation export and its u8 count permit at most 255. Author animated rigs to **255**. This can be a format constraint, not necessarily a runtime bug. Do not silently drop a bone or change binary compatibility.

## Legacy/unknown manifest fields (medium)

`tools/nether-cli/src/manifest.rs` uses `[game]`, `[build]`, `[assets]`, `[netplay]`, not `[console]`; unknown fields are not denied and can silently select defaults. Explicitly set correct player/network/render intent. A future parser change needs compatibility-aware warning/rejection behavior, not a silent migration.

## GLB import scope (limitation)

`tools/nether-export/src/mesh/gltf.rs` selects first mesh/primitive, not the whole scene. Prepare and inspect exports. A whole-scene importer is a feature decision, not an automatic documentation maintenance patch.

## Verification boundary

A temporary cartridge with corrected manifest, generated 128x128 PNG and target WAV was built/packed and run in the actual player for a 120-input-frame sync smoke. Fresh framebuffer captures measured **960x540** and showed input-driven movement. That bounded run does not prove every API, multiplayer scenario, backend or headless assertion path. Replay gaps were also traced to idle behavior in the compiler. Keep future verification proportional to the changed path.
