---
description: Scaffold a new Nethercore ZX game project with working starter code
argument-hint: "[language] [project-name]"
allowed-tools: ["AskUserQuestion", "Write", "Bash", "Read", "WebFetch"]
---

# New ZX Game Project

Create a complete ZX game project with proper structure and FFI bindings.

## Step 1: Gather Configuration

**If language not provided**, ask:
- Question: "Which programming language?"
- Options: **Rust (Recommended)**, **C**, **Zig**

**If project name not provided**, ask:
- Question: "Project name?"
- Options: **my-zx-game**, **hello-world**

## Step 2: Validate Location

```bash
test -d [project-name] && echo "EXISTS" || echo "OK"
```

## Step 3: Fetch FFI Bindings

Use WebFetch to get bindings from:

| Language | URL |
|----------|-----|
| Rust | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.rs` |
| C | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.h` |
| Zig | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.zig` |

Prompt: "Return complete file contents as-is."

## Step 4: Create Project

See `shared/file-organization.md` for structure patterns.

### Rust
- `Cargo.toml` with `crate-type = ["cdylib"]`
- `nether.toml` with game metadata
- `src/zx.rs` - Complete fetched bindings
- `src/lib.rs` - Minimal (~30 lines)

### C
- `Makefile` with wasm32 target
- `nether.toml`
- `zx.h` - Complete fetched bindings
- `game.c` - Minimal

### Zig
- `build.zig` for wasm32-freestanding
- `nether.toml`
- `src/zx.zig` - Complete fetched bindings
- `src/main.zig` - Minimal

### Minimal Entry Point (Rust)
```rust
#![no_std]
mod zx;
use zx::*;

static mut FRAME: u32 = 0;

#[no_mangle]
pub extern "C" fn init() { }

#[no_mangle]
pub extern "C" fn update() {
    unsafe { FRAME = FRAME.wrapping_add(1); }
    clear(0x1a1a2e);
    text(10, 10, c"Hello, Nethercore ZX!", 0xffffff);
}
```

## Step 5: Summary

Report:
- Files created
- FFI bindings in separate module
- Next steps: `cd [project-name] && nether run`
