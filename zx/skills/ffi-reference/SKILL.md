---
name: ZX FFI Reference
description: |
  ZX console FFI bindings reference. Triggers on "ZX FFI", "zx.rs", "ZX API", "ZX functions", "ZX rendering", "ZX input", "ZX audio".

  **Load references when:**
  - Render API details -> `references/render-api.md`
  - Input API details -> `references/input-api.md`
  - Audio API details -> `references/audio-api.md`
  - Full FFI -> Read `nethercore/include/zx.rs` directly
version: 1.0.0
---

# ZX FFI Reference

The ZX console provides 250+ FFI functions. **Always read `nethercore/include/zx.rs` for accurate signatures.**

## FFI Categories

| Category | Key Functions | Find In zx.rs |
|----------|--------------|---------------|
| System | `delta_time`, `tick_count`, `log` | Lines 1-100 |
| Random | `random`, `random_range`, `random_f32` | Search "random" |
| Input | `button_held`, `button_pressed`, `left_stick_x` | Search "button" |
| Camera | `camera_set`, `camera_fov` | Search "camera" |
| Transforms | `push_translate`, `push_rotate_y`, `push_scale` | Search "push_" |
| Meshes | `load_mesh`, `draw_mesh`, `cube`, `sphere` | Search "mesh" |
| Textures | `load_texture`, `texture_bind` | Search "texture" |
| Materials | `material_albedo`, `material_mre`, `material_normal` | Search "material" |
| Audio | `load_sound`, `play_sound`, `music_play` | Search "sound" |
| 2D Drawing | `draw_sprite`, `draw_text`, `draw_rect` | Search "draw_" |
| Environment | `draw_env`, `env_gradient` | Search "env_" |
| Debug | `debug_register_*`, `debug_watch_*`, `debug_group_*` | Search "debug_" |

## Init-Only Functions

Must call only during `init()`:
- `set_tick_rate(rate)` - 0=24fps, 1=30fps, 2=60fps, 3=120fps
- `set_clear_color(color)` - 0xRRGGBBAA
- `render_mode(mode)` - 0=Lambert, 1=Matcap, 2=PBR, 3=Hybrid
- All `rom_*()`, `load_*()`, procedural mesh functions

## Render-Only Functions

Call only during `render()`:
- All `draw_*` functions
- `camera_set()`, `camera_fov()`
- `push_translate()`, `push_rotate_y()`, `push_scale()`
- `texture_bind()`, `font_bind()`
- `begin_pass()`, `begin_pass_stencil_write()`

## Asset Loading

```rust
// In init()
let tex = rom_texture_str("player");
let mesh = rom_mesh_str("character");
let sfx = rom_sound_str("jump");
let music = rom_music_str("theme");
```

## Transform Stack

```rust
// In render()
push_translate(x, y, z);
push_rotate_y(angle_degrees);
push_scale_uniform(scale);
draw_mesh(MESH);
push_identity();  // Reset
```

## Coordinate System

- Y-up, right-handed, -Z forward
- When yaw=0, camera looks toward -Z
- Angles in degrees for FFI functions
