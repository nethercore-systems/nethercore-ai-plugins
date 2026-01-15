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
| `push_identity()` | Reset to identity |
| `push_matrix(m0..m15)` | Custom 4x4 matrix |

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
| `draw_sprite(x,y, w,h)` | Draw textured quad |
| `draw_rect(x,y, w,h)` | Draw colored rectangle |
| `draw_text_str(text, x,y, size, color)` | Draw text |
| `draw_circle(x, y, radius)` | Draw filled circle |

## Billboards

| Function | Purpose |
|----------|---------|
| `draw_billboard(w, h, mode, color)` | Camera-facing quad |
| `draw_billboard_region(...)` | Billboard with UV region |

Billboard modes:
- 1 = SPHERICAL (faces camera fully)
- 2 = CYLINDRICAL_Y (upright, rotates around Y)
