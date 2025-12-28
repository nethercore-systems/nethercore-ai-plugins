---
name: Tech Vision
description: This skill should be used when the user asks about "tech direction", "architecture", "code patterns", "technical vision", "code quality", "module structure", "file organization", "code splitting", "architecture decisions", "technical debt", "performance patterns", or discusses establishing or reviewing the technical direction of a game. Provides comprehensive technical architecture framework for maintaining code quality and coherence.
version: 1.0.0
---

# Tech Vision

Establish and maintain technical coherence through systematic architecture decisions, code organization patterns, and quality standards.

## Core Principles

### The Architecture Decision Record (ADR) Approach

Document significant decisions in `.claude/architecture/` as ADRs:

```
.claude/architecture/
├── 001-ecs-over-oop.md
├── 002-rollback-state-separation.md
├── 003-asset-loading-strategy.md
└── decisions.md  (index of all ADRs)
```

Each ADR documents:
- Context: Why this decision was needed
- Decision: What was decided
- Consequences: Trade-offs accepted

### Module Decomposition

Organize code into cohesive modules by responsibility:

```
src/
├── core/           # Engine-level systems
│   ├── input.rs    # Input handling
│   ├── render.rs   # Rendering interface
│   └── audio.rs    # Audio playback
├── game/           # Game-specific logic
│   ├── player.rs   # Player systems
│   ├── enemy.rs    # Enemy AI and behavior
│   └── world.rs    # Level/world state
├── ui/             # User interface
│   ├── hud.rs      # In-game HUD
│   └── menu.rs     # Menu systems
└── shared/         # Cross-cutting concerns
    ├── math.rs     # Math utilities
    └── constants.rs
```

### File Size Limits

**CRITICAL: Prevent token overflow by enforcing file size limits:**

| File Type | Soft Limit | Hard Limit | Action at Hard Limit |
|-----------|------------|------------|----------------------|
| Source code | 300 lines | 500 lines | Split into modules |
| Documentation | 500 lines | 1000 lines | Split into sections |
| Generated assets | 100 lines | 200 lines | External file + loader |

When approaching limits:
1. Identify logical subsections
2. Extract to separate files
3. Create clear interfaces between parts
4. Document the split in architecture notes

### Interface-First Design

Define module boundaries through explicit interfaces:

```rust
// Define the contract
pub trait EnemyBehavior {
    fn update(&mut self, ctx: &GameContext);
    fn take_damage(&mut self, amount: u32);
    fn is_alive(&self) -> bool;
}

// Implementations can be in separate files
mod basic_enemy;      // implements EnemyBehavior
mod flying_enemy;     // implements EnemyBehavior
mod boss_enemy;       // implements EnemyBehavior
```

## Technical Architecture Document

Create a technical architecture document with these sections:

### 1. Technical Pillars

Define 3-5 non-negotiable technical principles:

```
Example pillars:
- "Deterministic execution for rollback netcode"
- "Data-oriented design for cache efficiency"
- "Fail-fast on invalid state"
- "No allocations in hot paths"
```

### 2. Module Map

Document the high-level module structure:

```
┌─────────────┐     ┌─────────────┐
│    Game     │────►│    Core     │
│  (logic)    │     │ (platform)  │
└─────────────┘     └─────────────┘
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│   Shared    │◄───│   Assets    │
│ (utilities) │     │  (data)     │
└─────────────┘     └─────────────┘
```

### 3. Data Flow

Document how data moves through the system:

```
Input → GameState → RenderCommands → Output
          │
          └── AudioCommands → AudioOutput
```

### 4. State Management

Document state organization:

**Persistent State** (saved/loaded):
- Player progress
- Unlocks, achievements
- Settings

**Session State** (per-session):
- Current level
- Active entities
- Score, time

**Frame State** (per-frame):
- Input this frame
- Delta time
- Interpolation alpha

### 5. Memory Layout

For performance-critical code, document memory patterns:

```
Entity Storage:
├── SoA (Structure of Arrays) for iteration
├── Arena allocation for level-scoped objects
└── Pool allocation for frequently spawned entities
```

## Code Quality Standards

### Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Types | PascalCase | `PlayerState`, `EnemyConfig` |
| Functions | snake_case | `update_player`, `spawn_enemy` |
| Constants | SCREAMING_SNAKE | `MAX_ENEMIES`, `TILE_SIZE` |
| Modules | snake_case | `player_movement`, `enemy_ai` |

### Documentation Standards

**Public API**: Every public function needs:
```rust
/// Brief one-line description.
///
/// More details if needed.
///
/// # Examples (for non-obvious usage)
/// ```
/// let result = function_name(arg);
/// ```
pub fn function_name(arg: Type) -> Result { }
```

**Private implementation**: Explain "why" not "what":
```rust
// Using i32 instead of f32 for deterministic rollback
let position: i32 = ...
```

### Error Handling

Establish consistent error handling:

```rust
// For recoverable errors: Result
fn load_asset(path: &str) -> Result<Asset, LoadError>

// For programming errors: panic
fn get_entity(id: EntityId) -> &Entity {
    self.entities.get(id).expect("Entity must exist")
}

// For validation: early return with logging
if !is_valid(input) {
    warn!("Invalid input: {:?}", input);
    return;
}
```

## Coherence Assessment

When reviewing code for coherence, check:

### Structural Consistency
- Do modules follow the established organization?
- Are file sizes within limits?
- Is the module map accurate?

### Pattern Adherence
- Are the technical pillars respected?
- Is error handling consistent?
- Do naming conventions match?

### Performance Alignment
- Are hot paths allocation-free (if required)?
- Is state management following the documented pattern?
- Are determinism requirements maintained?

### Documentation Currency
- Do ADRs reflect current decisions?
- Is the module map up to date?
- Are interfaces documented?

## ZX-Specific Technical Direction

For Nethercore ZX games:

### Rollback Compatibility

All game state must be:
- Deterministic (no floats, no random without seed)
- Serializable (for save/load state)
- Separable (rollback state vs render state)

### Memory Budgets

```
Game State:      Max 256KB
Render State:    Max 64KB
Audio State:     Max 32KB
Asset Cache:     Remaining RAM
```

### FFI Boundaries

Keep FFI calls minimal and batched:
- Collect draw calls, submit once per frame
- Batch audio triggers
- Minimize state queries across boundary

## Director Notes Format

When providing technical direction feedback, structure notes as:

```
TECH REVIEW: [Module/System being reviewed]

ALIGNMENT:
- [What aligns with technical architecture]

VIOLATIONS:
- [What deviates from established patterns]
- [File size concerns]
- [Architecture drift]

RECOMMENDATIONS:
1. [Specific actionable adjustment]
2. [Priority: High/Medium/Low]

REFACTORING:
- [Suggested file splits]
- [Module reorganization]
- [Interface clarifications]
```

## Establishing Technical Direction

For new projects, run the vision establishment workflow:

1. **Define pillars** - Write 3-5 technical principles
2. **Create module map** - Plan high-level organization
3. **Document data flow** - How data moves through system
4. **Set limits** - File size, complexity budgets
5. **Create ADR template** - For future decisions
6. **Initial ADRs** - Document founding decisions

Store decisions in `.claude/architecture/` and summary in `.claude/creative-direction.local.md`.

## Additional Resources

### Reference Files

For detailed guidance on specific topics:
- **`references/module-patterns.md`** - Module organization patterns
- **`references/file-splitting.md`** - When and how to split files
- **`references/architecture-docs.md`** - Documentation templates

### ZX Integration

For ZX games, consult:
- `nethercore-zx-dev` for FFI patterns
- `nethercore-zx-dev/rollback-reviewer` for determinism
