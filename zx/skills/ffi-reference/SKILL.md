---
name: ffi-reference
description: >-
  ZX fantasy console FFI bindings reference. Documents the current functions
  for rendering, input, audio, camera, transforms, textures, materials, and debug.
  Includes init-only vs render-only call rules and the coordinate system. Use
  when writing or debugging ZX FFI calls in game code.
license: Apache-2.0
compatibility: ZX console only. Requires nethercore/include/zx.rs for full signatures.
metadata:
  author: nethercore-systems
  version: "1.0.1"
---

# ZX FFI Reference

The ZX console provides a broad FFI surface. **Always read `nethercore/include/zx.rs` for accurate signatures.**

## FFI Categories

| Category | Key Functions | Find In zx.rs |
|----------|--------------|---------------|
| System | `delta_time`, `tick_count`, `log` | Lines 1-100 |
| Random | `random`, `random_range`, `random_f32` | Search "random" |
| Input | `button_held`, `button_pressed`, `left_stick_x` | Search "button" |
| Camera | `camera_set`, `camera_fov` | Search "camera" |
| Transforms | `push_translate`, `push_rotate_y`, `push_scale`, `push_identity` | Search "push_" |
| Meshes | `load_mesh`, `draw_mesh`, `cube`, `sphere` | Search "mesh" |
| Textures | `load_texture`, `texture_bind` | Search "texture" |
| Materials | `material_albedo`, `material_mre`, `material_normal` | Search "material" |
| Audio | `load_sound`, `play_sound`, `music_play` | Search "sound" |
| 2D Drawing | `draw_sprite`, `draw_text`, `draw_rect` | Search "draw_" |
| Environment | `epu_set`, `epu_textures`, `epu_asset`, `draw_epu` | Search "epu_" |
| Debug | `debug_register_*`, `debug_watch_*`, `debug_group_*` | Search "debug_" |

## Init-Only Functions

Must call only during `init()`:
- `set_clear_color(color)` - 0xRRGGBBAA
- All `rom_*()`, `load_*()`, procedural mesh functions

## Render-Only Functions

Call only during `render()`:
- All `draw_*` functions
- `camera_set()`, `camera_fov()`
- `push_translate()`, `push_rotate_y()`, `push_scale()`
- `texture_bind()`, `font_bind()`
- `begin_pass()`, `begin_pass_stencil_write()`
- `set_color()`, `z_index()`
- `epu_set()`, `epu_textures()`, `epu_asset()`, `draw_epu()`

## Asset Loading

```rust
// In init()
let tex = rom_texture_str("player");
let mesh = rom_mesh_str("character");
let sfx = rom_sound_str("jump");
let music = rom_tracker_str("theme");
```

## Transform State

There is no generic push/pop transform API. Compose transforms with the
`push_*` calls, then use `push_identity()` (or `transform_set()` with a
column-major 4x4 matrix) when starting an independent object.

```rust
// In render()
push_translate(x, y, z);
push_rotate_y(angle_degrees);
push_scale_uniform(scale);
draw_mesh(MESH);
push_identity();  // Reset before the next independent object
```

## Resource Lifetime

Resource creation/loading is init-only. The FFI exposes no resource unload or
free call; loaded handles live until game shutdown.

## EPU Environment

The current EPU config is 16 `u64` values (128 bytes). Select a source with
`epu_set(config_ptr)`, `epu_textures(px, nx, py, ny, pz, nz)`, or
`epu_asset(id_ptr, id_len)` before the geometry that should use it, then call
`draw_epu()` afterward to draw the environment background. There is no EPU
time-setting API; animate deterministic instruction parameters from game state.

For packed animation clips, keep rigs at 255 bones or fewer: the runtime
skeleton path accepts 256, but the packed keyframe format stores `bone_count`
as `u8`.

## Coordinate System

- Y-up, right-handed, -Z forward
- When yaw=0, camera looks toward -Z
- Angles in degrees for FFI functions
