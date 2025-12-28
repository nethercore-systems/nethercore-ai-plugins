# Module Organization Patterns

## Core Patterns

### Pattern 1: Feature Modules

Organize by game feature, each containing all related code.

```
src/
├── core/              # Shared engine code
├── features/
│   ├── combat/
│   │   ├── mod.rs
│   │   ├── systems.rs
│   │   ├── components.rs
│   │   └── tests.rs
│   ├── inventory/
│   │   ├── mod.rs
│   │   ├── systems.rs
│   │   ├── components.rs
│   │   └── tests.rs
│   └── dialogue/
│       ├── mod.rs
│       ├── systems.rs
│       └── components.rs
└── main.rs
```

**Pros:**
- Feature changes localized
- Easy to add/remove features
- Clear ownership

**Cons:**
- Cross-feature code duplication
- Shared utilities unclear home

**Best for:** Feature-rich games, plugin systems

### Pattern 2: Layer Modules

Organize by architectural layer.

```
src/
├── domain/            # Game rules, entities
│   ├── player.rs
│   ├── enemy.rs
│   └── world.rs
├── application/       # Game flow, systems
│   ├── game_loop.rs
│   ├── state_machine.rs
│   └── events.rs
├── infrastructure/    # Platform, I/O
│   ├── input.rs
│   ├── render.rs
│   └── audio.rs
└── main.rs
```

**Pros:**
- Clear separation of concerns
- Easy to swap implementations
- Testable layers

**Cons:**
- Features spread across layers
- More files to navigate

**Best for:** Games with multiple backends, highly testable code

### Pattern 3: Type-First Modules

Organize by data type with associated operations.

```
src/
├── types/
│   ├── player.rs      # PlayerState + impl
│   ├── enemy.rs       # EnemyState + impl
│   ├── weapon.rs      # WeaponData + impl
│   └── level.rs       # LevelData + impl
├── systems/
│   ├── physics.rs     # Operates on multiple types
│   ├── collision.rs
│   └── rendering.rs
└── main.rs
```

**Pros:**
- Type and behavior together
- Natural Rust idiom
- Easy to find code

**Cons:**
- Systems span types
- Can grow into god-files

**Best for:** Data-centric designs, smaller games

### Pattern 4: ECS Modules

Standard Entity-Component-System organization.

```
src/
├── components/        # Data only
│   ├── transform.rs
│   ├── sprite.rs
│   ├── physics.rs
│   └── health.rs
├── systems/           # Logic only
│   ├── movement.rs
│   ├── rendering.rs
│   ├── combat.rs
│   └── ai.rs
├── resources/         # Global state
│   ├── time.rs
│   ├── input.rs
│   └── camera.rs
├── entities/          # Entity archetypes
│   ├── player.rs
│   ├── enemy.rs
│   └── projectile.rs
└── main.rs
```

**Pros:**
- Standard ECS pattern
- Highly composable
- Cache-friendly

**Cons:**
- Many small files
- Feature logic distributed

**Best for:** Performance-critical games, many entities

## Module Interface Design

### Public API Surface

Minimize public API:

```rust
// mod.rs - Control what's exposed
mod internal_impl;
mod types;
mod systems;

// Re-export only what external code needs
pub use types::PlayerState;
pub use systems::update_player;

// Keep implementation details private
use internal_impl::*;
```

### Prelude Pattern

For frequently used items:

```rust
// prelude.rs
pub use crate::core::*;
pub use crate::math::*;
pub use crate::types::*;

// Usage in other files
use crate::prelude::*;
```

### Trait-Based Interfaces

Define behavior contracts:

```rust
// traits.rs
pub trait Updateable {
    fn update(&mut self, dt: f32);
}

pub trait Renderable {
    fn render(&self, ctx: &RenderContext);
}

// Implementations can be in separate files
```

## Module Dependencies

### Dependency Direction

Code should flow one way:

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Main   │────►│  Game   │────►│  Core   │
└─────────┘     └─────────┘     └─────────┘
                     │
                     ▼
               ┌─────────┐
               │ Shared  │
               └─────────┘

Arrow = "depends on"
```

**Rules:**
- Core never depends on Game
- Shared never depends on specific modules
- No circular dependencies

### Breaking Cycles

If you find a cycle:

```rust
// BAD: player.rs imports enemy.rs, enemy.rs imports player.rs

// GOOD: Extract shared types
// shared/combat.rs
pub trait Combatant {
    fn take_damage(&mut self, amount: u32);
}

// player.rs
impl Combatant for Player { ... }

// enemy.rs
impl Combatant for Enemy { ... }
```

### Dependency Injection

Pass dependencies instead of importing:

```rust
// BAD: Direct dependency
use crate::audio::play_sound;
impl Player {
    fn attack(&self) {
        play_sound("attack.wav");
    }
}

// GOOD: Injected dependency
impl Player {
    fn attack(&self, audio: &dyn AudioPlayer) {
        audio.play("attack.wav");
    }
}
```

## ZX Game Module Template

Recommended structure for Nethercore ZX games:

```
src/
├── lib.rs             # Entry point, FFI exports
├── game/
│   ├── mod.rs         # GameState, main loop
│   ├── player.rs      # Player logic
│   ├── enemies.rs     # Enemy types and AI
│   ├── world.rs       # Level/world state
│   └── collision.rs   # Collision detection
├── render/
│   ├── mod.rs         # Render orchestration
│   ├── sprites.rs     # Sprite rendering
│   └── effects.rs     # Visual effects
├── audio/
│   ├── mod.rs         # Audio orchestration
│   └── music.rs       # Music state
├── input/
│   └── mod.rs         # Input processing
└── constants.rs       # Game constants
```

### Why This Structure

- **game/**: All deterministic game logic (rollback-safe)
- **render/**: Non-deterministic rendering (can diverge)
- **audio/**: Non-deterministic audio (can diverge)
- **input/**: Platform abstraction

### Module Size Targets

| Module | Target Lines | Max Lines |
|--------|--------------|-----------|
| lib.rs | 50 | 100 |
| game/mod.rs | 100 | 200 |
| game/player.rs | 150 | 300 |
| game/enemies.rs | 200 | 400 |
| render/mod.rs | 100 | 200 |
| constants.rs | 50 | 100 |

## Testing Organization

### Co-located Tests

Keep unit tests with code:

```rust
// player.rs
pub fn calculate_damage(base: u32, multiplier: f32) -> u32 {
    (base as f32 * multiplier) as u32
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_damage_calculation() {
        assert_eq!(calculate_damage(10, 1.5), 15);
    }
}
```

### Integration Tests

Separate directory for cross-module tests:

```
tests/
├── combat_tests.rs      # Combat system integration
├── level_tests.rs       # Level loading/generation
└── save_load_tests.rs   # Serialization roundtrips
```

### Test Utilities

Shared test helpers in dedicated module:

```
src/
└── testing/
    ├── mod.rs
    ├── fixtures.rs      # Test data factories
    ├── mocks.rs         # Mock implementations
    └── assertions.rs    # Custom assertions
```

## Refactoring Modules

### Signs of Needed Refactoring

- Module exceeds size limits
- Frequent merge conflicts
- Unclear responsibility
- High coupling between modules
- Difficulty testing

### Refactoring Steps

1. **Identify boundaries** - What are the distinct responsibilities?
2. **Create new modules** - Empty files with proper structure
3. **Move code** - One function/type at a time
4. **Update imports** - Fix all references
5. **Add re-exports** - Maintain API if needed
6. **Test** - Ensure nothing broke
7. **Document** - Update architecture notes
