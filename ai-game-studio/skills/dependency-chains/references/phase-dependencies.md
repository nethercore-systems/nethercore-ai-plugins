# Phase Dependencies

## Phase 0: Creative Foundation

**Produces:** Creative pillars, art style guide, audio style guide

**Required for:** Consistent asset generation, design alignment, quality reviews

**Can skip if:** Small/jam project

## Phase 1: Game Design

**Requires:** Creative vision (optional)

**Produces:** GDD, asset specs, mechanic definitions

**Required for:** Feature implementation, asset generation

**Cannot skip:** GDD defines the game

## Phase 2: Asset Generation

**Requires:** Asset specs from GDD, style guides

**Produces:** Meshes, textures, audio files, animations

**Required for:** Asset integration, visual/audio features

## Phase 3: Asset Integration

**Requires:** Generated asset files

**Produces:** nether.toml declarations, asset handles, usage examples

**Required for:** Using assets in game code

**Critical:** Generated assets are USELESS until integrated

## Phase 4: Implementation

**Requires:** Integrated assets, GDD

**Produces:** Game modules, logic, rendering code

**Required for:** Playable game, testing

## Phase 5: Testing

**Requires:** Building code, runnable game

**Produces:** Test results, bug reports, metrics

**Required for:** Quality assurance, release

## Phase 6: Publishing

**Requires:** Passing tests, complete features, marketing assets

**Produces:** ROM package, platform listing

## Feature-Level Dependencies

### Visual Feature
```
Feature renders correctly requires:
├── Mesh exists (assets/meshes/)
├── Texture exists (assets/textures/)
├── nether.toml declares assets
├── Asset handles exist (src/assets.rs)
├── Code uses handles
└── Code called from render()
```

### Audio Feature
```
Sound plays correctly requires:
├── Audio file exists (assets/audio/, WAV 22050Hz mono 16-bit)
├── nether.toml declares sound
├── Sound handle exists
├── Code calls sound_play()
└── Trigger actually fires
```

### Game Mechanic
```
Mechanic works requires:
├── State struct exists
├── State initialized in init()
├── Update logic in update()
├── Render logic in render() (if visual)
└── Input handling (if interactive)
```
