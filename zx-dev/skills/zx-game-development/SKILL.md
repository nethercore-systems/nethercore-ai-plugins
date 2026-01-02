---
name: Nethercore ZX Game Development
description: |
  This skill provides ZX game development guidance. Triggers on "create ZX game", "ZX FFI", "nether build", "nether.toml", "ZX graphics/audio", "WASM game".

  **Load references when:**
  - Project setup → `shared/file-organization.md`, `shared/build-workflow.md`
  - Code examples → `examples/hello-world-rust.md`, `examples/game-with-assets.md`
  - Coordinate math → `references/coordinate-conventions.md`
  - Common patterns → `references/quick-patterns.md`
  - FFI details → Read `nethercore/include/zx.rs` directly
version: 2.0.0
---

# Nethercore ZX Game Development

## Overview

Nethercore ZX is a fantasy console targeting 5th-gen aesthetics (PS1/N64/Saturn) with rollback netcode. Games compile to WASM and run in the Nethercore player.

**Specifications:**
- Resolution: 960×540 (fixed, 16:9)
- Tick Rate: 24/30/60/120 fps
- ROM Size: 16MB max
- WASM Memory: 4MB (auto-snapshotted)
- VRAM: 4MB
- Players: 1-4 (local + remote)
- Coordinate System: Y-up, right-handed, -Z forward

## Required Game Exports

Every game exports three functions:

```rust
#[no_mangle] pub extern "C" fn init() { }   // Setup, asset loading
#[no_mangle] pub extern "C" fn update() { } // Deterministic logic
#[no_mangle] pub extern "C" fn render() { } // Drawing only
```

## Project Setup

See `shared/file-organization.md` for project structure and `shared/build-workflow.md` for build commands.

**Key principle:** Keep entry files minimal (~50 lines). FFI bindings in separate module file (`zx.rs`/`zx.h`/`zx.zig`).

## FFI Reference

The FFI provides 250+ functions across these categories:

| Category | Key Functions | Find In zx.rs |
|----------|--------------|---------------|
| System | `delta_time`, `tick_count`, `log` | Lines 1-100 |
| Random | `random`, `random_range`, `random_f32` | Search "random" |
| Input | `button_held`, `button_pressed`, `left_stick_x` | Search "button" |
| Camera | `camera_set`, `camera_fov` | Search "camera" |
| Transforms | `push_translate`, `push_rotate_y`, `push_scale` | Search "push_" |
| Meshes | `load_mesh`, `draw_mesh`, `cube`, `sphere` | Search "mesh" |
| Textures | `load_texture`, `texture_bind` | Search "texture" |
| Audio | `load_sound`, `play_sound`, `music_play` | Search "sound" |
| 2D Drawing | `draw_sprite`, `draw_text`, `draw_rect` | Search "draw_" |
| Environment | `draw_env`, `env_gradient` | Search "env_" |

**Always read `nethercore/include/zx.rs` for accurate signatures.**

## Init-Only Functions

Must call only during `init()`:
- `set_tick_rate(rate)` - 0=24fps, 1=30fps, 2=60fps, 3=120fps
- `set_clear_color(color)` - 0xRRGGBBAA
- `render_mode(mode)` - 0=Lambert, 1=Matcap, 2=PBR, 3=Hybrid
- All `rom_*()`, `load_*()`, procedural mesh functions

## Render Modes

| Mode | Name | Use Case |
|------|------|----------|
| 0 | Lambert | Flat colors, 2D, stylized |
| 1 | Matcap | Sculpted look, toon |
| 2 | PBR | Realistic (default) |
| 3 | Hybrid | PBR + matcap |

## Rollback Safety

See `shared/rollback-rules.md`. Key points:
- All state in static variables
- Use FFI `random()` not external RNG
- Use `tick_count()` not system time
- Never modify state in `render()`

## Documentation

| Resource | Location |
|----------|----------|
| FFI Source | `nethercore/include/zx.rs` (canonical) |
| Cheat Sheet | `nethercore/docs/book/src/cheat-sheet.md` |
| Tutorials | `nethercore/docs/book/src/tutorials/paddle/` |
| Examples | `nethercore/examples/` |
