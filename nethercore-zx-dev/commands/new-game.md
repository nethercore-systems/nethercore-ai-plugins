---
description: Scaffold a new Nethercore ZX game project with working starter code
argument-hint: "[language] [project-name]"
allowed-tools: ["AskUserQuestion", "Write", "Bash", "Read"]
---

# New ZX Game Project Scaffolding

Create a complete, working Nethercore ZX game project with proper structure.

## Step 1: Gather Project Configuration

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

## Step 3: Create Project Structure

Based on the language choice, create the appropriate structure:

### For Rust Projects

Read the template from @${CLAUDE_PLUGIN_ROOT}/skills/zx-game-development/examples/hello-world-rust.md

Create these files:

1. **`[project-name]/Cargo.toml`** - Use the Cargo.toml from the template
2. **`[project-name]/nether.toml`** - Use the nether.toml from the template, update the game id and title
3. **`[project-name]/src/lib.rs`** - Use the src/lib.rs code from the template

The FFI bindings are included inline in the template's lib.rs via the `mod zx` block.

### For C Projects

Read the template from @${CLAUDE_PLUGIN_ROOT}/skills/zx-game-development/examples/hello-world-c.md

Create these files:

1. **`[project-name]/Makefile`** - Use the Makefile from the template
2. **`[project-name]/nether.toml`** - Use the nether.toml from the template, update the game id and title
3. **`[project-name]/game.c`** - Use the game.c code from the template

The C FFI declarations are included inline at the top of game.c.

### For Zig Projects

Read the template from @${CLAUDE_PLUGIN_ROOT}/skills/zx-game-development/examples/hello-world-zig.md

Create these files:

1. **`[project-name]/build.zig`** - Use the build.zig from the template
2. **`[project-name]/nether.toml`** - Use the nether.toml from the template, update the game id and title
3. **`[project-name]/src/main.zig`** - Use the main.zig code from the template
4. **`[project-name]/src/zx.zig`** - Use the zx.zig module from the template

## Step 4: Create README

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

[List the files created]

## Next Steps

- Modify the game code to add your gameplay
- Add assets to an `assets/` directory
- Update `nether.toml` with asset references
- Check the ZX FFI cheat sheet for available functions

## Resources

- [Nethercore ZX Documentation](https://github.com/user/nethercore/tree/main/docs/book)
- [FFI Cheat Sheet](https://github.com/user/nethercore/tree/main/docs/book/src/cheat-sheet.md)
```

## Step 5: Summary

After creating all files, report to the user:

**Project created successfully!**

Show:
- List of files created
- The directory location

**Next steps:**

```bash
cd [project-name]
nether run
```

Tell them:
- `nether run` builds and launches their game in the player
- They can ask about ZX topics like "ZX input handling" or "ZX 3D graphics" for help
- For multiplayer games, ask "check my game for rollback safety" before testing netplay
