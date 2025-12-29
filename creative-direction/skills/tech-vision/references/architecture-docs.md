# Architecture Documentation Templates

## Architecture Decision Record (ADR)

### Template

```markdown
# ADR-[NUMBER]: [Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Date

YYYY-MM-DD

## Context

[What is the issue that we're seeing that is motivating this decision?]

## Decision

[What is the change that we're proposing and/or doing?]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Tradeoff 2]

### Neutral
- [Side effect 1]

## Alternatives Considered

### [Alternative 1]
- Description: [What this option was]
- Rejected because: [Why we didn't choose it]

### [Alternative 2]
- Description: [What this option was]
- Rejected because: [Why we didn't choose it]
```

### Example ADR

```markdown
# ADR-001: Use Fixed-Point Math for Game Logic

## Status
Accepted

## Date
2024-01-15

## Context
Nethercore ZX requires deterministic execution for rollback netcode.
Floating-point operations can produce different results across
platforms due to compiler optimizations and CPU differences.

## Decision
Use 16.16 fixed-point integers for all game logic calculations.
Floats are only allowed for rendering-only calculations that
don't affect game state.

## Consequences

### Positive
- Guaranteed determinism across all platforms
- Simpler serialization (just integers)
- No denormalized number issues

### Negative
- Reduced precision compared to f32
- More complex math (division especially)
- Learning curve for team

### Neutral
- Need fixed-point math library
- Some algorithms need adaptation

## Alternatives Considered

### Use Rust's strict float mode
- Description: Compiler flags for stricter float behavior
- Rejected because: Still not guaranteed across platforms

### Use integer-only without fixed point
- Description: Work in pixel coordinates only
- Rejected because: Too limiting for physics and smooth movement
```

## Technical Design Document

### Template

```markdown
# [System/Feature] Technical Design

## Overview

[Brief description of what this system does and why it exists]

## Goals

1. [Primary goal]
2. [Secondary goal]
3. [Constraint or requirement]

## Non-Goals

- [What this system explicitly doesn't do]
- [Scope boundaries]

## Architecture

### Components

```
[ASCII diagram of components and relationships]
```

### Data Structures

```rust
// Primary data structures with field documentation
```

### Interfaces

```rust
// Key traits and public functions
```

## Behavior

### [Behavior 1]

[Description of how the system behaves in this scenario]

### [Behavior 2]

[Description of how the system behaves in this scenario]

## Integration

### Dependencies

- [Module/System this depends on]: [Why]

### Dependents

- [Module/System that depends on this]: [How]

## Testing Strategy

- Unit tests for: [What]
- Integration tests for: [What]
- Manual testing for: [What]

## Open Questions

- [ ] [Unresolved question 1]
- [ ] [Unresolved question 2]

## References

- [Link to related documents]
- [Link to external resources]
```

## Module README

### Template

For each significant module, create a `README.md`:

```markdown
# [Module Name]

[One paragraph describing what this module does]

## Responsibilities

- [Primary responsibility]
- [Secondary responsibility]

## Structure

```
module/
├── mod.rs          # [What this contains]
├── types.rs        # [What this contains]
├── systems.rs      # [What this contains]
└── tests.rs        # [What this contains]
```

## Usage

```rust
use crate::module::prelude::*;

// Example usage
```

## Key Types

### [TypeName]

[Brief description of the type and its purpose]

### [TypeName2]

[Brief description of the type and its purpose]

## Key Functions

### `function_name(args) -> Return`

[What this function does and when to use it]

## Dependencies

- `core`: [Why this module depends on core]
- `math`: [Why this module depends on math]

## Design Decisions

See:
- ADR-XXX: [Decision that affects this module]
- ADR-YYY: [Another relevant decision]

## Common Patterns

### [Pattern Name]

```rust
// How to do a common thing with this module
```

## Gotchas

- [Non-obvious behavior 1]
- [Common mistake to avoid]
```

## Project Structure Document

### Template

```markdown
# Project Structure

## Directory Layout

```
project/
├── src/                   # Source code
│   ├── lib.rs             # Library entry point
│   ├── [module]/          # [Module description]
│   └── ...
├── tests/                 # Integration tests
├── docs/                  # Documentation
│   └── architecture/      # ADRs and design docs
├── assets/                # Game assets
└── tools/                 # Development tools
```

## Module Map

```
┌─────────────────────────────────────────┐
│                  Main                   │
│           (entry, FFI exports)          │
└─────────────────────────────────────────┘
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
┌───────────┐ ┌───────────┐ ┌───────────┐
│   Game    │ │  Render   │ │   Audio   │
│  (logic)  │ │ (display) │ │  (sound)  │
└───────────┘ └───────────┘ └───────────┘
       │
       ▼
┌───────────┐
│   Core    │
│ (shared)  │
└───────────┘
```

## Key Files

| File | Purpose | Size Target |
|------|---------|-------------|
| src/lib.rs | FFI exports, initialization | 50 lines |
| src/game/mod.rs | Game state, main loop | 150 lines |
| ... | ... | ... |

## Build Outputs

| Output | Description |
|--------|-------------|
| target/wasm32.../game.wasm | Game WASM module |
| assets.bin | Packed asset bundle |
| game.nether | Final ROM file |

## Dependencies

### Runtime
- [dependency]: [What it's used for]

### Development
- [dev-dependency]: [What it's used for]

## Configuration

### Build Configuration
- Location: `nether.toml`
- Key settings: [list important settings]

### Runtime Configuration
- Location: `.studio/creative-direction.local.md`
- Purpose: Per-project creative direction settings
```

## Data Flow Document

### Template

```markdown
# Data Flow: [System/Feature]

## Overview

[What data this system processes and why]

## Flow Diagram

```
┌─────────┐    ┌─────────┐    ┌─────────┐
│  Input  │───►│ Process │───►│ Output  │
└─────────┘    └─────────┘    └─────────┘
     │              │              │
     ▼              ▼              ▼
[describe]    [describe]    [describe]
```

## Input Data

### [Input Type 1]
- Source: [Where this comes from]
- Format: [Data structure]
- Frequency: [How often received]

## Processing Steps

### Step 1: [Name]
- Input: [What it receives]
- Output: [What it produces]
- Side effects: [Any state changes]

### Step 2: [Name]
...

## Output Data

### [Output Type 1]
- Destination: [Where this goes]
- Format: [Data structure]
- Frequency: [How often produced]

## State Changes

| State | Modified By | When |
|-------|-------------|------|
| GameState.x | Step 2 | [Condition] |

## Error Handling

| Error | Cause | Response |
|-------|-------|----------|
| [Error type] | [What causes it] | [How it's handled] |
```

## Persistent Direction Files

### creative-direction.local.md

Store project-level creative direction:

```markdown
---
# Art Direction
art_style: dark-fantasy-painterly
color_palette: desaturated-warm
style_spectrums:
  fidelity: 4
  saturation: 3
  contrast: 4

# Sound Direction
sonic_identity: organic-ambient
mix_priority: gameplay-first

# Tech Direction
architecture: ecs-with-rollback
determinism: required
file_size_limit: 300

# Creative Vision
pillars:
  - atmospheric-dread
  - meaningful-choices
  - emergent-narrative
---

# Project Direction Notes

## Art Notes
[Accumulated art direction decisions]

## Sound Notes
[Accumulated sound direction decisions]

## Tech Notes
[Accumulated technical decisions]

## Creative Notes
[Accumulated creative vision notes]
```

This file is:
- Ignored by git (add to .gitignore)
- Read by director agents for context
- Updated as decisions are made
- Persists across Claude sessions
