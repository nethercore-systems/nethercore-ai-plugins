---
description: This skill documents dependency chains in game development - what must be completed before other tasks can begin. Use when planning task order, identifying blockers, or ensuring proper sequencing of game development work.
---

# Game Development Dependency Chains

Understanding what depends on what ensures tasks are completed in the correct order and nothing is blocked.

## Core Development Pipeline

```
Creative Vision → Game Design → Asset Specs → Assets → Integration → Implementation → Testing → Publishing
```

Each phase depends on the previous. Skipping phases causes problems.

## Phase Dependencies

### Phase 0: Creative Foundation

**Produces:**
- Creative pillars (docs/design/creative-vision.md)
- Art style guide (docs/design/art-style.md)
- Sonic Style Language (docs/design/ssl.md)

**Required for:**
- Consistent asset generation
- Design decisions alignment
- Quality reviews

**Can skip if:** Small/jam project, willing to iterate on style

### Phase 1: Game Design

**Requires:**
- Creative vision (optional but recommended)

**Produces:**
- Game Design Document (docs/design/game-design.md)
- Asset specifications (docs/design/asset-specs.md)
- Mechanic definitions

**Required for:**
- Feature implementation (what to build)
- Asset generation (what to create)
- Scope decisions

**Cannot skip:** GDD defines what game you're making

### Phase 2: Asset Generation

**Requires:**
- Asset specifications (from GDD)
- Style guides (for consistency)

**Produces:**
- Mesh files (assets/meshes/*.obj)
- Texture files (assets/textures/*.png)
- Audio files (assets/audio/*.wav)
- Animation files (assets/animations/*.anim)

**Required for:**
- Asset integration
- Feature implementation (visual/audio features)
- Rendering

### Phase 3: Asset Integration

**Requires:**
- Generated asset files

**Produces:**
- nether.toml declarations
- Asset handles (src/assets.rs)
- Usage examples

**Required for:**
- Using assets in game code
- Rendering assets
- Playing sounds

**Critical insight:** Generated assets are USELESS until integrated

### Phase 4: Implementation

**Requires:**
- Integrated assets (for visual/audio features)
- GDD (for feature specs)

**Produces:**
- Game modules (src/*.rs)
- Game logic
- Rendering code

**Required for:**
- Playable game
- Testing

### Phase 5: Testing

**Requires:**
- Building code (nether build succeeds)
- Runnable game

**Produces:**
- Test results
- Bug reports
- Performance metrics

**Required for:**
- Quality assurance
- Release confidence

### Phase 6: Publishing

**Requires:**
- Passing tests
- Complete features
- Marketing assets

**Produces:**
- ROM package
- Platform listing
- Live game

## Feature-Level Dependencies

### Visual Feature Dependencies

```
Feature renders correctly requires:
├── Mesh exists (assets/meshes/X.obj)
│   └── Generated or created
├── Texture exists (assets/textures/X.png)
│   └── Generated or created
├── nether.toml declares assets
│   └── [[assets.meshes]], [[assets.textures]]
├── Asset handles exist (src/assets.rs)
│   └── pub const MESH_X, pub const TEX_X
├── Code uses handles
│   └── texture_bind(TEX_X); draw_mesh(MESH_X);
└── Code is called from render()
    └── Integration in main render loop
```

**If any link breaks, feature won't render.**

### Audio Feature Dependencies

```
Sound plays correctly requires:
├── Audio file exists (assets/audio/X.wav)
│   └── Correct format: WAV, 22050Hz, mono, 16-bit
├── nether.toml declares sound
│   └── [[assets.sounds]]
├── Sound handle exists (src/assets.rs)
│   └── pub const SND_X
├── Code calls sound_play(SND_X)
│   └── At appropriate trigger
└── Trigger actually fires
    └── Gameplay event occurs
```

### Game Mechanic Dependencies

```
Mechanic works correctly requires:
├── State struct exists
│   └── Data to track mechanic state
├── State initialized in init()
│   └── Default values set
├── Update logic in update()
│   └── State changes each frame
├── Render logic in render() (if visual)
│   └── State is displayed
└── Input handling (if interactive)
    └── Player can affect state
```

## Common Dependency Chains

### "Player Character" Chain

```
1. Character design (GDD) → defines what player looks like/does
2. Character mesh generation → 3D model
3. Character texture generation → skin/colors
4. Character animation generation → walk, run, attack
5. Asset integration → handles and nether.toml
6. Player module → state, input, movement
7. Player rendering → draw with animations
8. Player update → movement, physics
9. Integration → init/update/render hooks
```

### "Enemy" Chain

```
1. Enemy design (GDD) → behavior, stats
2. Enemy mesh/texture → visual
3. Enemy animations → idle, walk, attack, death
4. Asset integration → handles
5. Enemy AI module → state machine, behavior
6. Spawn system → when/where enemies appear
7. Combat integration → damage, death
8. Integration → init/update/render hooks
```

### "Power-Up" Chain

```
1. Power-up design (GDD) → types, effects, duration
2. Power-up mesh/texture → visual pickup
3. Power-up sound → pickup, activation sounds
4. Asset integration → handles
5. Power-up module → types, effects, timers
6. Spawn system → where power-ups appear
7. Collection logic → player picks up
8. Effect application → modify player stats
9. UI feedback → show active power-ups
10. Integration → init/update/render hooks
```

### "Track/Level" Chain

```
1. Level design (GDD) → layout, obstacles, goals
2. Track/level mesh → 3D geometry
3. Track texture → surface appearance
4. Asset integration → handles
5. Level module → geometry data, spawn points
6. Collision setup → track boundaries
7. Rendering → draw track
8. Camera setup → view the track
9. Player placement → spawn on track
```

## Blocking Dependencies

These MUST be resolved before continuing:

| Blocker | Blocked Tasks | Resolution |
|---------|---------------|------------|
| No GDD | All implementation | Create GDD with /design-game |
| No assets | Visual features | Generate with asset-generator |
| Assets not integrated | Rendering | Run integration-assistant |
| No handles | Asset usage in code | Create src/assets.rs |
| Build fails | All testing | Fix compilation errors |
| Module not in lib.rs | Feature doesn't run | Add mod declaration |
| Not in update() | Feature doesn't update | Add update call |
| Not in render() | Feature doesn't display | Add render call |

## Parallelizable Tasks

These CAN run simultaneously (no dependencies between them):

- Different asset types (textures, meshes, sounds)
- Different enemy types
- Different UI elements
- Different systems (if not sharing state)
- Analysis tasks (reviewing code, assets, design)
- Direction reviews (art, sound, tech directors)

## Sequential Requirements

These MUST run in order:

1. Design → Implementation (can't implement undefined features)
2. Generation → Integration (can't integrate non-existent assets)
3. Integration → Usage (can't use non-integrated assets)
4. Code → Test (can't test non-existent code)
5. Pass tests → Release (shouldn't release failing game)

## Dependency Verification

Before starting a task, verify its dependencies:

```bash
# Before implementing feature that uses assets:
ls assets/meshes/feature*.obj  # Asset exists?
grep "feature" nether.toml     # Declared?
grep "FEATURE" src/assets.rs   # Handle exists?

# Before testing:
nether build                   # Builds?

# Before rendering feature:
grep "mod feature" src/lib.rs  # Module declared?
grep "feature" src/lib.rs      # Used in init/update/render?
```
