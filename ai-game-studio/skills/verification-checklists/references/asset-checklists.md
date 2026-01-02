# Asset Verification Checklists

## Mesh Asset

- [ ] File exists: `generated/meshes/[name].obj` or `.gltf`
- [ ] Format correct: Y-up, triangulated, UVs present
- [ ] Within poly budget (prop: 100-500, character: 1000-2000)
- [ ] Declared in nether.toml: `[[assets.meshes]]`
- [ ] Handle exists: `pub const MESH_[NAME]: MeshHandle = asset_handle!(...);`
- [ ] Used in code: `draw_mesh(MESH_[NAME])`
- [ ] Texture bound before draw (if textured)

## Texture Asset

- [ ] File exists: `generated/textures/[name].png`
- [ ] Format correct: PNG, power-of-2 (64/128/256/512), max 512x512
- [ ] Appropriate channels (RGBA for transparency, RGB for opaque)
- [ ] Declared in nether.toml: `[[assets.textures]]`
- [ ] Handle exists: `pub const TEX_[NAME]: TextureHandle = asset_handle!(...);`
- [ ] Used in code: `texture_bind(TEX_[NAME])`

## Sound Asset

- [ ] File exists: `generated/audio/[name].wav`
- [ ] Format correct: WAV, 22050 Hz, 16-bit, mono
- [ ] Declared in nether.toml: `[[assets.sounds]]`
- [ ] Handle exists: `pub const SND_[NAME]: SoundHandle = asset_handle!(...);`
- [ ] Used in code: `sound_play(SND_[NAME])`
- [ ] Trigger event actually fires

## After Asset Generation

- [ ] Files in correct locations
- [ ] Correct formats
- [ ] Added to nether.toml
- [ ] Handles in src/assets.rs
- [ ] Handles used in game code
- [ ] Build succeeds
- [ ] Assets visible/audible in game
