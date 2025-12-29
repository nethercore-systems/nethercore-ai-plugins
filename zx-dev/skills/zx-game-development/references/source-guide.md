# Source File Guide

This guide explains how to find current FFI specifications in the Nethercore source code.

## Primary Source Files

### Rust FFI (Source of Truth)
**Location:** `nethercore/include/zx.rs`

This is the canonical FFI definition. All other language bindings are generated from this file.

**Structure:**
- Lines 1-50: Module documentation and imports
- Lines 50-150: System functions (timing, logging, RNG)
- Lines 150-300: Input functions (buttons, sticks)
- Lines 300-500: Graphics functions (camera, transforms)
- Lines 500-800: Mesh and texture functions
- Lines 800-1000: 2D drawing functions
- Lines 1000-1300: Environment and materials
- Lines 1300-1500: Audio functions
- Lines 1500-1700: ROM loading, debug, helpers

**Searching:**
```bash
# Find all button-related functions
grep -n "button" nethercore/include/zx.rs

# Find all draw functions
grep -n "fn draw_" nethercore/include/zx.rs

# Find all ROM loading functions
grep -n "rom_" nethercore/include/zx.rs
```

### C Header
**Location:** `nethercore/include/zx.h`

Generated from zx.rs with NCZX_ prefixes for all constants.

**Key patterns:**
- Constants: `NCZX_BUTTON_A`, `NCZX_RENDER_PBR`
- Helper macros: `NCZX_LOG()`, `NCZX_DRAW_TEXT()`
- Inline functions: `nczx_rgba()`, `nczx_clampf()`

### Zig Module
**Location:** `nethercore/include/zx.zig`

Generated from zx.rs with Zig-native slice helpers.

**Key patterns:**
- Namespaced constants: `zx.Button.a`, `zx.Render.pbr`
- Slice helpers: `logStr()`, `drawTextStr()`, `romTexture()`

## Documentation Files

### Cheat Sheet
**Location:** `nethercore/docs/book/src/cheat-sheet.md`

Quick reference with all FFI functions organized by category.

### API Reference
**Location:** `nethercore/docs/book/src/api/`

Detailed documentation by category:
- `system.md` - Timing, logging
- `input.md` - Buttons, sticks
- `graphics.md` - Rendering state
- `camera.md` - 3D camera
- `transforms.md` - Matrix operations
- `meshes.md` - Mesh loading/drawing
- `textures.md` - Texture handling
- `audio.md` - Sound and music
- `drawing-2d.md` - 2D primitives
- `epu.md` - Environment modes
- `materials.md` - PBR/lighting

### Tutorials
**Location:** `nethercore/docs/book/src/tutorials/paddle/`

8-part tutorial building a complete game:
1. Setup and drawing
2. Paddle movement
3. Ball physics
4. AI opponent
5. Multiplayer/rollback
6. Scoring
7. Sound effects
8. Polish and publishing

## Example Projects

### Hello World
**Location:** `nethercore/examples/1-getting-started/`

- `hello-world/` - Rust
- `hello-world-c/` - C
- `hello-world-zig/` - Zig

### Complete Games
**Location:** `nethercore/examples/7-games/`

- `paddle/` - Pong clone (tutorial game)
- `neon-drift/` - Racing game
- `prism-survivors/` - Action game

## Reading Strategy

When implementing a feature:

1. **Start with SKILL.md** - Get the pattern and workflow
2. **Read the source file** - Get exact function signatures from zx.rs/zx.h/zx.zig
3. **Check examples** - See working implementations in examples/
4. **Consult docs** - Read detailed explanations in docs/book/

For FFI functions, always verify signatures against the source files since they are the authoritative reference.
