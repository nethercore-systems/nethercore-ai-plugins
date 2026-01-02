# ZX Project File Organization

## Core Principle

**Keep entry point files minimal (~50 lines max).** All FFI bindings in separate module. Never copy FFI functions inline.

## Project Structures

### Rust
```
src/
├── lib.rs        # MINIMAL: mod declarations + entry points only
├── zx.rs         # FFI bindings (fetch from GitHub, never edit)
├── player.rs     # Game modules (target 200 lines, max 300)
└── enemies.rs
```

### C
```
├── game.c        # MINIMAL: includes + entry points
├── zx.h          # FFI bindings (fetch from GitHub)
├── player.c/h    # Game modules
└── enemies.c/h
```

### Zig
```
src/
├── main.zig      # MINIMAL: imports + entry points
├── zx.zig        # FFI bindings (fetch from GitHub)
├── player.zig    # Game modules
└── enemies.zig
```

## lib.rs Template

```rust
#![no_std]

mod zx;           // FFI module - exists, don't create
mod player;       // Game modules you create
mod enemies;

use zx::*;        // Single zx import here only
use player::*;
use enemies::*;

static mut STATE: Option<GameState> = None;

#[no_mangle]
pub extern "C" fn init() { /* initialize state */ }

#[no_mangle]
pub extern "C" fn update() { /* call state.update() */ }

#[no_mangle]
pub extern "C" fn render() { /* call state.render() */ }
```

## Module Files

```rust
// src/player.rs
use crate::zx::*;  // Access FFI through crate root

pub struct Player { ... }
impl Player { ... }
```

## File Size Rules

| File | Max Lines | Purpose |
|------|-----------|---------|
| lib.rs/game.c/main.zig | 50 | Entry points only |
| System files | 300 | Single responsibility |
| Complex features | Split | Use subdirectory modules |

## FFI Bindings URLs

| Language | URL |
|----------|-----|
| Rust | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.rs` |
| C | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.h` |
| Zig | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.zig` |

Never copy individual FFI functions - always fetch the complete file.
