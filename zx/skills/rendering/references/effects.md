# ZX Rendering Effects

## Stencil Constants

**Depth/Stencil Compare:**
| Constant | Value | Use |
|----------|-------|-----|
| `NEVER` | 1 | Never pass |
| `LESS` | 2 | Standard depth |
| `EQUAL` | 3 | Match exactly |
| `ALWAYS` | 8 | Always pass |

**Stencil Operations:**
| Constant | Value | Effect |
|----------|-------|--------|
| `KEEP` | 0 | Keep current |
| `REPLACE` | 2 | Set to ref |

## Scope Effect

```rust
fn render_scoped_view() {
    // Create circular mask
    begin_pass_stencil_write(1, 0);
    draw_circle(SCREEN_CX, SCREEN_CY, 200.0);

    // World only visible inside circle
    begin_pass_stencil_test(1, 0);
    camera_set(cam_x, cam_y, cam_z, tx, ty, tz);
    draw_env();
    draw_mesh(WORLD_MESH);

    // Return to normal, draw scope overlay
    begin_pass(0);
    texture_bind(SCOPE_OVERLAY);
    draw_sprite(0.0, 0.0, 960.0, 540.0);
}
```

## Portal Effect

```rust
fn render_portal() {
    // Draw main world
    camera_set(main_cam...);
    draw_mesh(MAIN_WORLD);

    // Create portal mask
    begin_pass_stencil_write(1, 0);
    push_translate(portal_x, portal_y, portal_z);
    draw_mesh(PORTAL_FRAME);
    push_identity();

    // Other world inside portal (clear_depth=1)
    begin_pass_stencil_test(1, 1);
    camera_set(other_cam...);
    draw_mesh(OTHER_WORLD);

    begin_pass(0);
}
```

## FPS Viewmodel

```rust
fn render_fps() {
    // Draw world
    camera_set(player_x, player_y, player_z, look_x, look_y, look_z);
    draw_env();
    draw_mesh(LEVEL);

    // New pass with depth clear - viewmodel always on top
    begin_pass(1);
    push_translate(0.3, -0.2, 0.5);
    push_rotate_y(sway_angle);
    draw_mesh(GUN);
    push_identity();
}
```

## Particle Effect Recipes

**Smoke:** `vy = 1-2`, `life = 1-3s`, `color = 0x888888FF`
**Fire:** `vy = 2-3`, `life = 0.3-0.7s`, `colors = 0xFFFF88/FF8800`
**Sparks:** `velocity = ±5`, `life = 0.2-0.5s`, `size = 0.1`

## Performance Tips

| Particles | Impact |
|-----------|--------|
| 0-100 | Excellent |
| 100-500 | Good |
| 500-1000 | Moderate |
| 1000+ | Optimize |

Pool particles, use LOD at distance, texture atlas.
