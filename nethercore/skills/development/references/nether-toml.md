# nether.toml reference

Source: `nethercore/tools/nether-cli/src/manifest.rs`. IDs are explicit authored keys; asset paths are relative to the manifest. Unknown/deprecated fields can be silently ignored, so spelling and table placement matter.

```toml
[game]
id = "space-fighter"
title = "Space Fighter"
author = "Your Name"
version = "1.0.0"
description = "A space combat game"
tags = ["arcade", "multiplayer"]
render_mode = 0
tick_rate = 60
max_players = 2
compress_textures = true

[netplay]
enabled = true

[build]
script = "cargo build --target wasm32-unknown-unknown --release"
wasm = "target/wasm32-unknown-unknown/release/space_fighter.wasm"

[[assets.textures]]
id = "ship"
path = "assets/ship.png"

[[assets.meshes]]
id = "ship_mesh"
path = "assets/ship.glb"

[[assets.sounds]]
id = "laser"
path = "assets/laser.wav"

[[assets.trackers]]
id = "battle_theme"
path = "assets/battle.xm"
```

- `compress_textures` explicitly chooses RGBA8 vs BC7; choosing a lit render mode does not automatically enable compression.
- Raw WAV packing currently assumes mono 16-bit PCM at 22050 Hz; it does not implement the resample/downmix promised by its comment. Validate source audio before packing.
- Music uses `assets.trackers`, not `assets.music`. XM/IT embedded samples are extracted; names must resolve without collisions. `patterns = false` deliberately imports only a sample library.
- GLB/glTF mesh import selects first mesh/primitive, not the whole scene. Skinned exports need corresponding `assets.skeletons` and `assets.keyframes` (`animations` alias) entries. Use `skin_name`/`animation_name` selectors when required; wildcard clips need collision-safe `id_prefix`.
- Runtime skeleton capacity is 256 bones, but packed animation export accepts at most 255. Use the tighter limit for animated content.
- EPU face entries are `[[assets.epu_environments]]` with `id, px, nx, py, ny, pz, nz`.

Load exact IDs in `init` with the console bindings; do not invent `_str` helpers:

```rust
unsafe {
    let id = b"ship";
    let texture = rom_texture(id.as_ptr(), id.len() as u32);
    // Store the handle in game state for later drawing.
}
```

ZX tracker loading is `rom_tracker`, not `rom_music`. Check the canonical bindings for signatures and init guards. A successful pack does not prove correct downstream playback or budgets.
