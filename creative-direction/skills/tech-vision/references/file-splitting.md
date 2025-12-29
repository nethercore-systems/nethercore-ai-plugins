# File Splitting Guide

## Why Split Files?

### Token Limit Problem

Large files cause problems for AI-assisted development:
- Context window overflow
- Unable to read entire file
- Incomplete understanding leads to bugs
- Regeneration loses important sections

### Code Quality Problem

Large files cause problems for humans:
- Difficult to navigate
- Merge conflicts more likely
- Harder to test in isolation
- Obscures logical structure

### The 300-Line Rule

Target ~300 lines per source file:
- Fits comfortably in AI context
- Single responsibility focus
- Easy mental model
- Quick to read and review

Hard limit: 500 lines. Beyond this, split is mandatory.

## When to Split

### Size-Based Triggers

| Lines | Action |
|-------|--------|
| 0-200 | Healthy, no action needed |
| 200-300 | Watch for growth, plan splits |
| 300-400 | Soft limit exceeded, plan split |
| 400-500 | Split soon, becoming unwieldy |
| 500+ | Split immediately, exceeds hard limit |

### Complexity-Based Triggers

Split when you see:
- Multiple "sections" in one file (separated by comments)
- Multiple unrelated types defined together
- Functions that don't call each other
- Mixed abstraction levels

### Logical Triggers

Split when:
- A concept deserves its own file
- Testing would be easier in isolation
- Different team members work on sections
- Reuse potential exists

## How to Split

### Step 1: Identify Boundaries

Find natural seams in the code:

```
Before (400 lines):
player.rs
├── PlayerState struct (30 lines)
├── Movement functions (120 lines)
├── Combat functions (100 lines)
├── Inventory functions (80 lines)
└── Input handling (70 lines)
```

### Step 2: Extract Modules

Create focused files:

```
After:
player/
├── mod.rs           # Re-exports, PlayerState (50 lines)
├── movement.rs      # Movement logic (130 lines)
├── combat.rs        # Combat logic (110 lines)
├── inventory.rs     # Inventory logic (90 lines)
└── input.rs         # Input handling (80 lines)
```

### Step 3: Define Interfaces

Create clear boundaries between modules:

```rust
// player/mod.rs
mod movement;
mod combat;
mod inventory;
mod input;

pub use movement::*;
pub use combat::*;
pub use inventory::*;

pub struct PlayerState {
    pub position: Vec2,
    pub health: i32,
    pub inventory: Inventory,
}

impl PlayerState {
    pub fn update(&mut self, ctx: &GameContext) {
        movement::update_movement(self, ctx);
        combat::update_combat(self, ctx);
        inventory::update_inventory(self, ctx);
    }
}
```

### Step 4: Update Imports

Replace direct references with module paths:

```rust
// Before
use crate::player::move_player;

// After
use crate::player::movement::move_player;
// Or if re-exported:
use crate::player::move_player;
```

## Splitting Patterns

### Pattern 1: By Responsibility

Split based on what the code does:

```
Original: game.rs (500 lines)

Split by responsibility:
├── state.rs        # Game state struct
├── update.rs       # Update loop logic
├── physics.rs      # Physics calculations
├── collision.rs    # Collision detection
└── spawning.rs     # Entity spawning
```

### Pattern 2: By Entity Type

Split based on what the code operates on:

```
Original: entities.rs (600 lines)

Split by entity:
├── player.rs       # Player entity
├── enemy.rs        # Enemy entities
├── projectile.rs   # Projectiles
├── pickup.rs       # Collectibles
└── effect.rs       # Visual effects
```

### Pattern 3: By Layer

Split based on abstraction level:

```
Original: renderer.rs (450 lines)

Split by layer:
├── types.rs        # Render types and traits
├── commands.rs     # Command building
├── backend.rs      # Platform-specific rendering
└── debug.rs        # Debug visualization
```

### Pattern 4: By Lifecycle

Split based on when code runs:

```
Original: level.rs (550 lines)

Split by lifecycle:
├── loading.rs      # Level loading
├── generation.rs   # Procedural generation
├── runtime.rs      # Runtime updates
├── unloading.rs    # Cleanup
└── types.rs        # Level data types
```

## Splitting Complex Types

### Large Structs

When a struct has many fields:

```rust
// Before: Single large struct
struct GameState {
    // Player fields (10)
    // Enemy fields (8)
    // World fields (12)
    // UI fields (6)
}

// After: Composed smaller structs
struct GameState {
    pub player: PlayerState,
    pub enemies: EnemyState,
    pub world: WorldState,
    pub ui: UiState,
}
```

### Large Impl Blocks

When impl has many methods:

```rust
// Before: One file, 50 methods
impl GameState {
    // 50 methods...
}

// After: Methods in separate files with traits
// game_state/mod.rs
impl GameState {
    // Core methods (10)
}

// game_state/serialization.rs
impl Serialize for GameState { ... }
impl Deserialize for GameState { ... }

// game_state/update.rs
impl GameState {
    pub fn update(&mut self) { ... }
    // Update-related methods
}
```

## Splitting Generated Code

### Asset Generation

When generating assets/code procedurally:

```
BAD: One file with all assets
assets.rs (2000 lines)

GOOD: Asset data in external files
assets/
├── textures.toml    # Texture definitions
├── sounds.toml      # Sound definitions
├── meshes.toml      # Mesh definitions
└── loader.rs        # Loading logic (100 lines)
```

### Generated Implementations

When generating many similar implementations:

```
BAD: All in one file
generated.rs (800 lines of similar patterns)

GOOD: Split by category or generate index
generated/
├── mod.rs           # Re-exports
├── enemies.rs       # Enemy implementations
├── items.rs         # Item implementations
└── effects.rs       # Effect implementations
```

## Documentation for Splits

### Module Documentation

Each new module needs a doc comment:

```rust
//! # Player Movement
//!
//! Handles player movement including:
//! - Basic movement (walk, run)
//! - Advanced movement (jump, dash, wall-cling)
//! - Movement state machine
//!
//! ## Usage
//! ```
//! use player::movement::*;
//! ```

pub fn update_movement(player: &mut PlayerState, ctx: &Context) {
    // ...
}
```

### Architecture Note

Document significant splits in `.studio/architecture/`:

```markdown
# ADR-004: Player Module Split

## Context
player.rs grew to 480 lines with distinct responsibilities.

## Decision
Split into player/mod.rs + 4 submodules.

## Consequences
- Easier to test individual systems
- Clear ownership of functionality
- Slightly more files to navigate
```

## Preventing File Growth

### Code Review Checkpoints

Before merging:
- [ ] No file exceeds 400 lines
- [ ] New functionality in appropriate module
- [ ] Large additions planned for extraction

### Continuous Monitoring

Set up file size warnings:

```bash
# Check for large files
find src -name "*.rs" -exec wc -l {} \; | awk '$1 > 400 {print}'
```

### Design for Splits

When adding features:
- Start with separate file if >100 lines expected
- Use traits for interface flexibility
- Prefer composition over extension

## Quick Reference

### Split Checklist

- [ ] File exceeds 300 lines (soft) or 500 lines (hard)
- [ ] Multiple distinct responsibilities identified
- [ ] Clear boundaries exist between sections
- [ ] Testing would improve with separation
- [ ] No circular dependencies created by split
- [ ] Re-exports maintain API compatibility
- [ ] Documentation updated
- [ ] Architecture note created (if significant)

### File Size Targets

| Category | Target | Max |
|----------|--------|-----|
| Game logic | 200 | 400 |
| System code | 250 | 450 |
| Generated code | 100 | 200 |
| Test files | 300 | 500 |
| Config/data | 100 | 200 |
