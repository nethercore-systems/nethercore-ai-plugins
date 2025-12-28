---
description: This skill provides verification checklists for different types of game development tasks. Use when completing features, assets, or systems to ensure nothing is missed. Prevents "generated but not integrated" and "coded but not rendered" issues.
---

# Game Development Verification Checklists

Systematic checklists to verify game development tasks are truly complete.

## The Core Question

Before marking anything complete, ask:

**"Would a player notice this in the game?"**

If no - it's not complete.

## Asset Verification Checklists

### Mesh Asset Checklist

```
[ ] File exists in correct location
    → assets/meshes/[name].obj or .gltf

[ ] Correct format
    → Y-up coordinate system
    → Triangulated faces
    → UVs present (for textured meshes)

[ ] Within poly budget
    → Prop: 100-500 tris
    → Character: 1000-2000 tris
    → Environment: varies

[ ] Declared in nether.toml
    → [[assets.meshes]]
    → id = "[name]"
    → path = "assets/meshes/[name].obj"

[ ] Handle exists in src/assets.rs
    → pub const MESH_[NAME]: MeshHandle = asset_handle!("mesh", "[name]");

[ ] Used in game code
    → draw_mesh(MESH_[NAME]) called somewhere
    → Called from render() path

[ ] Texture bound before draw (if textured)
    → texture_bind(TEX_[NAME]) before draw_mesh()
```

### Texture Asset Checklist

```
[ ] File exists in correct location
    → assets/textures/[name].png

[ ] Correct format
    → PNG format
    → Power-of-2 dimensions (64, 128, 256, 512)
    → Max 512x512

[ ] Appropriate channels
    → RGBA for transparency
    → RGB for opaque

[ ] Declared in nether.toml
    → [[assets.textures]]
    → id = "[name]"
    → path = "assets/textures/[name].png"

[ ] Handle exists in src/assets.rs
    → pub const TEX_[NAME]: TextureHandle = asset_handle!("texture", "[name]");

[ ] Used in game code
    → texture_bind(TEX_[NAME]) called
    → Called before relevant draw_mesh()
```

### Sound Asset Checklist

```
[ ] File exists in correct location
    → assets/audio/[name].wav

[ ] Correct format
    → WAV format
    → 22050 Hz sample rate
    → 16-bit depth
    → Mono (not stereo)

[ ] Declared in nether.toml
    → [[assets.sounds]]
    → id = "[name]"
    → path = "assets/audio/[name].wav"

[ ] Handle exists in src/assets.rs
    → pub const SND_[NAME]: SoundHandle = asset_handle!("sound", "[name]");

[ ] Used in game code
    → sound_play(SND_[NAME]) called
    → Called at appropriate game event

[ ] Event actually triggers
    → Gameplay action causes sound_play call
```

## Feature Verification Checklists

### Game Feature Checklist (General)

```
[ ] Module file exists
    → src/[feature].rs

[ ] Module declared in lib.rs
    → mod [feature];

[ ] No incomplete code markers
    → grep -r "TODO|FIXME|unimplemented!|todo!" src/[feature].rs
    → Should find nothing

[ ] All match arms implemented
    → No empty `_ => {}`
    → No placeholder arms

[ ] Build succeeds
    → nether build passes

[ ] State struct defined
    → pub struct [Feature]State or similar

[ ] State initialized in init()
    → GameState includes [feature] field
    → Field is initialized

[ ] Update logic called
    → self.[feature].update() in main update()

[ ] Render logic called (if visual)
    → self.[feature].render() in main render()
```

### Visual Feature Checklist

All of "Game Feature Checklist" PLUS:

```
[ ] Draw function called
    → draw_mesh(), draw_sprite(), draw_text(), etc.
    → Called from render() path, not just defined

[ ] Texture bound if needed
    → texture_bind() before draw_mesh()

[ ] Camera/viewport correct
    → Feature appears in view
    → Not off-screen or behind camera

[ ] Render order correct
    → Not hidden behind other elements
    → UI drawn after 3D, etc.

[ ] Player would see it
    → Actually visible in running game
```

### Interactive Feature Checklist

All of "Game Feature Checklist" PLUS:

```
[ ] Input is read
    → input_*(), button_*(), gamepad_*() called

[ ] Input affects state
    → Reading input changes game state

[ ] State change is visible
    → Player can see/hear result of input

[ ] Feedback is immediate
    → No noticeable delay between input and response
```

### Audio Feature Checklist

All of "Game Feature Checklist" PLUS:

```
[ ] Sound file exists and integrated
    → See "Sound Asset Checklist"

[ ] Trigger event occurs
    → Game event that should play sound happens

[ ] sound_play() is called
    → At the trigger event

[ ] Sound actually plays
    → Can be heard in running game
```

## System Verification Checklists

### Inventory System Checklist

```
[ ] Data structures defined
    → Item struct/enum
    → Inventory struct with slots

[ ] Pickup logic works
    → Items can be collected
    → Items added to inventory

[ ] UI displays inventory
    → Player can see items
    → Slot visualization works

[ ] Item usage works
    → Items can be used/consumed
    → Effects apply correctly

[ ] Persistence (if applicable)
    → Inventory saves/loads
```

### Combat System Checklist

```
[ ] Attack logic works
    → Player can attack
    → Attack has hitbox/detection

[ ] Damage applies
    → Enemies take damage
    → Health decreases

[ ] Death/defeat works
    → Zero health causes death
    → Death animation/effect plays
    → Entity removed/respawned

[ ] Feedback present
    → Hit feedback (visual/audio)
    → Damage numbers (if applicable)
```

### Save System Checklist

```
[ ] Serialization works
    → Game state can be converted to bytes
    → All necessary fields included

[ ] Save function works
    → save_data() called
    → Data persists

[ ] Load function works
    → load_data() retrieves data
    → State restored correctly

[ ] UI present
    → Save/load slots visible
    → Player can initiate save/load
```

## Integration Verification

### After Asset Generation

```
[ ] Files created in correct locations
[ ] Files in correct formats
[ ] Files added to nether.toml
[ ] Handles created in src/assets.rs
[ ] Handles used in game code
[ ] Build still succeeds
[ ] Assets visible/audible in game
```

### After Feature Implementation

```
[ ] Module exists and declared
[ ] No TODO/FIXME markers
[ ] Init/Update/Render hooked up
[ ] Build succeeds
[ ] Feature works in running game
[ ] Player would notice feature
```

### After Bug Fix

```
[ ] Original issue no longer occurs
[ ] No new issues introduced
[ ] Build still succeeds
[ ] Sync test still passes (if multiplayer)
```

## Verification Commands

Quick verification commands to run:

```bash
# Assets exist
ls assets/meshes/*.obj assets/textures/*.png assets/audio/*.wav

# Assets declared
grep "\[\[assets" nether.toml

# Handles exist
grep "asset_handle!" src/assets.rs

# Assets used
grep -r "draw_mesh\|texture_bind\|sound_play" src/

# No incomplete markers
grep -r "TODO\|FIXME\|unimplemented!\|todo!" src/

# Build succeeds
nether build

# Module integrated
grep "mod " src/lib.rs
grep -E "init|update|render" src/lib.rs
```

## Red Flags (Incomplete Work)

If you see any of these, the work is NOT complete:

- `TODO` or `FIXME` comments
- `unimplemented!()` or `todo!()` macros
- Empty match arms: `_ => {}`
- Placeholder functions: `fn foo() { /* TODO */ }`
- Assets in output/ but not assets/
- Assets in assets/ but not in nether.toml
- Handles defined but never used
- Code written but not called from main loop
- Feature works but has no visual/audio feedback
