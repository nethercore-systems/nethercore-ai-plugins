# ZX Render API

## Camera

| Function | Purpose |
|----------|---------|
| `camera_set(x,y,z, tx,ty,tz)` | Position + look-at |
| `camera_fov(degrees)` | Field of view (default 60) |
| `push_view_matrix(m0..m15)` | Custom 4x4 view matrix |

## Transform Stack

| Function | Purpose |
|----------|---------|
| `push_translate(x, y, z)` | Translate |
| `push_rotate_x(deg)` | Rotate around X |
| `push_rotate_y(deg)` | Rotate around Y |
| `push_rotate_z(deg)` | Rotate around Z |
| `push_scale(x, y, z)` | Non-uniform scale |
| `push_scale_uniform(s)` | Uniform scale |
| `push_identity()` | Reset current model matrix |

## Mesh Drawing

| Function | Purpose |
|----------|---------|
| `draw_mesh(handle)` | Draw loaded mesh |
| `cube(size)` | Procedural cube |
| `sphere(radius, segments)` | Procedural sphere |
| `plane(width, height)` | Procedural plane |

## Material Binding

| Function | Slot | Purpose |
|----------|------|---------|
| `material_albedo(tex)` | 0 | Color/diffuse |
| `material_mre(tex)` | 1 | Metallic/Roughness/Emissive |
| `material_normal(tex)` | 3 | Normal map |
| `set_color(rgba)` | - | Vertex color tint |

`material_normal()` uses material slot 3; do not substitute a generic texture
slot. Normal-mapped meshes also need UVs and tangents.

## Render Passes

| Function | Purpose |
|----------|---------|
| `begin_pass(clear_depth)` | New render pass |
| `begin_pass_stencil_write(ref, clear_depth)` | Create stencil mask |
| `begin_pass_stencil_test(ref, clear_depth)` | Render inside mask |
| `z_index(n)` | 2D ordering (0-255) |

## 2D Drawing

| Function | Purpose |
|----------|---------|
| `draw_sprite(x,y, w,h)` | Draw the currently bound texture |
| `draw_rect(x,y, w,h)` | Draw a rectangle in the current color |
| `draw_text(ptr,len,x,y,size)` | Draw UTF-8 bytes in the current color |
| `draw_circle(x, y, radius)` | Draw a filled circle in the current color |

## Billboards

| Function | Purpose |
|----------|---------|
| `draw_billboard(w, h, mode)` | Camera-facing quad in current color |
| `draw_billboard_region(...)` | Billboard with UV region |

Billboard modes:
- 1 = SPHERICAL (faces camera fully)
- 2 = CYLINDRICAL_Y (upright, rotates around Y)

Bind the texture with `texture_bind(handle)` and set tint with
`set_color(rgba)` before drawing.

## EPU Environment

`epu_set()` reads a 128-byte configuration containing 16 `u64` values.
Choose the source with `epu_set(config_ptr)`, `epu_textures(px, nx, py, ny,
pz, nz)`, or `epu_asset(id_ptr, id_len)` before geometry draws. Call
`draw_epu()` afterward to draw the environment background. There is no time
setter; drive animated parameters from deterministic game state.
