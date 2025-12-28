---
description: Scaffold a new Nethercore ZX game project with working starter code
argument-hint: "[language] [project-name]"
allowed-tools: ["AskUserQuestion", "Write", "Bash", "Read", "WebFetch"]
---

# New ZX Game Project Scaffolding

Create a complete, working Nethercore ZX game project with proper structure and up-to-date FFI bindings.

## Step 1: Gather Project Configuration

**IMPORTANT**: Ask for language FIRST - this determines everything else.

**If language argument ($1) is not provided or not one of "rust", "c", "zig":**

Use AskUserQuestion to ask:

- Question: "Which programming language for your game?"
- Header: "Language"
- Options:
  - **Rust (Recommended)** - Best tooling, first-class support, and most examples
  - **C** - Lightweight, requires clang with wasm32 target
  - **Zig** - Modern alternative, requires Zig 0.11+

**If project name argument ($2) is not provided:**

Use AskUserQuestion to ask:

- Question: "What should we name your game project?"
- Header: "Name"
- Options:
  - **my-zx-game** - Default starter name
  - **hello-world** - Simple example name

The user can type a custom name.

## Step 2: Validate Project Location

Check if the target directory already exists:

```bash
test -d [project-name] && echo "EXISTS" || echo "OK"
```

If directory exists, inform the user and ask them to choose a different name.

## Step 3: Fetch FFI Bindings

**CRITICAL**: Fetch the complete, up-to-date FFI bindings from GitHub.

The bindings are auto-generated at build time and always current:

| Language | URL |
|----------|-----|
| Rust | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.rs` |
| C | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.h` |
| Zig | `https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.zig` |

Use WebFetch to retrieve the appropriate bindings file for the selected language.

**Prompt for WebFetch**: "Return the complete file contents exactly as-is. This is FFI bindings code."

Save the fetched content to write as a separate module file in Step 4.

## Step 4: Create Project Structure

Based on the language choice, create the appropriate structure:

### For Rust Projects

Create these files:

1. **`[project-name]/Cargo.toml`**:
```toml
[package]
name = "[project-name]"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[profile.release]
opt-level = "z"
lto = true
```

2. **`[project-name]/nether.toml`**:
```toml
[game]
id = "[project-name]"
title = "[Project Title]"
version = "0.1.0"

[build]
target = "wasm32-unknown-unknown"
source = "src/lib.rs"
```

3. **`[project-name]/src/zx.rs`** - Write the COMPLETE fetched bindings file here (NOT inline in lib.rs)

4. **`[project-name]/src/lib.rs`** - Minimal game code that imports zx module:
```rust
#![no_std]

mod zx;
use zx::*;

static mut FRAME: u32 = 0;

#[no_mangle]
pub extern "C" fn init() {
    // Initialization code here
}

#[no_mangle]
pub extern "C" fn update() {
    unsafe {
        FRAME = FRAME.wrapping_add(1);
    }

    // Clear screen
    clear(0x1a1a2e);

    // Draw hello text
    text(10, 10, c"Hello, Nethercore ZX!", 0xffffff);
}
```

**Note**: The lib.rs is intentionally minimal (~20 lines). All FFI bindings are in zx.rs.

### For C Projects

Create these files:

1. **`[project-name]/Makefile`**:
```makefile
CC = clang
CFLAGS = --target=wasm32 -nostdlib -O2

game.wasm: game.c zx.h
	$(CC) $(CFLAGS) -o game.wasm game.c

clean:
	rm -f game.wasm
```

2. **`[project-name]/nether.toml`**:
```toml
[game]
id = "[project-name]"
title = "[Project Title]"
version = "0.1.0"

[build]
target = "wasm32"
source = "game.wasm"
prebuilt = true
```

3. **`[project-name]/zx.h`** - Write the COMPLETE fetched bindings file here

4. **`[project-name]/game.c`** - Minimal game code that includes zx.h:
```c
#include "zx.h"

static unsigned int frame = 0;

void init(void) {
    // Initialization code here
}

void update(void) {
    frame++;

    // Clear screen
    clear(0x1a1a2e);

    // Draw hello text
    text(10, 10, "Hello, Nethercore ZX!", 0xffffff);
}
```

**Note**: The game.c is intentionally minimal. All FFI declarations are in zx.h.

### For Zig Projects

Create these files:

1. **`[project-name]/build.zig`**:
```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.resolveTargetQuery(.{
        .cpu_arch = .wasm32,
        .os_tag = .freestanding,
    });

    const exe = b.addExecutable(.{
        .name = "game",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = .ReleaseSmall,
    });

    exe.entry = .disabled;
    exe.rdynamic = true;

    b.installArtifact(exe);
}
```

2. **`[project-name]/nether.toml`**:
```toml
[game]
id = "[project-name]"
title = "[Project Title]"
version = "0.1.0"

[build]
target = "wasm32-freestanding"
source = "zig-out/bin/game.wasm"
prebuilt = true
build_command = "zig build"
```

3. **`[project-name]/src/zx.zig`** - Write the COMPLETE fetched bindings file here

4. **`[project-name]/src/main.zig`** - Minimal game code that imports zx module:
```zig
const zx = @import("zx.zig");

var frame: u32 = 0;

export fn init() void {
    // Initialization code here
}

export fn update() void {
    frame +%= 1;

    // Clear screen
    zx.clear(0x1a1a2e);

    // Draw hello text
    zx.text(10, 10, "Hello, Nethercore ZX!", 0xffffff);
}
```

**Note**: The main.zig is intentionally minimal. All FFI bindings are in zx.zig.

## Step 5: Create README

Create `[project-name]/README.md` with:

```markdown
# [Project Title]

A Nethercore ZX game written in [Language].

## Building

```bash
nether build
```

## Running

```bash
nether run
```

## Project Structure

```
[project-name]/
├── [config files]      # Build configuration
├── src/
│   ├── [main file]     # Your game code (keep this small!)
│   └── zx.[ext]        # FFI bindings (auto-generated, don't edit)
└── nether.toml         # Game metadata and build config
```

## FFI Bindings

The `zx.[rs|h|zig]` file contains complete FFI bindings for Nethercore ZX.
These are auto-generated from the console specification.

**Do NOT copy imports into your main file** - just use:
- Rust: `mod zx; use zx::*;`
- C: `#include "zx.h"`
- Zig: `const zx = @import("zx.zig");`

To update bindings to latest version:
```bash
# Rust
curl -o src/zx.rs https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.rs

# C
curl -o zx.h https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.h

# Zig
curl -o src/zx.zig https://raw.githubusercontent.com/nethercore-systems/nethercore/main/include/zx.zig
```

## Next Steps

- Modify the game code to add your gameplay
- Add assets to an `assets/` directory
- Update `nether.toml` with asset references
- Check the ZX FFI cheat sheet for available functions

## Resources

- [Nethercore ZX Documentation](https://github.com/nethercore-systems/nethercore/tree/main/docs/book)
- [FFI Cheat Sheet](https://github.com/nethercore-systems/nethercore/tree/main/docs/book/src/cheat-sheet.md)
```

## Step 6: Summary

After creating all files, report to the user:

**Project created successfully!**

Show:
- List of files created
- The directory location
- **Highlight that FFI bindings are in a separate file** (zx.rs/zx.h/zx.zig)

**Next steps:**

```bash
cd [project-name]
nether run
```

Tell them:
- `nether run` builds and launches their game in the player
- FFI bindings are in a separate module file - **don't copy imports into lib.rs/game.c/main.zig**
- They can ask about ZX topics like "ZX input handling" or "ZX 3D graphics" for help
- For multiplayer games, ask "check my game for rollback safety" before testing netplay
