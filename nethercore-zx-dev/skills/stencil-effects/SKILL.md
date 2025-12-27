---
name: Stencil Effects
description: This skill should be used when the user asks about "stencil buffer", "stencil_begin", "stencil_end", "portal rendering", "scope effect", "binoculars effect", "mirror reflection", "masked rendering", "window effect", "circular mask", "UI masking", "non-rectangular UI", "vignette effect", "stencil_invert", "stencil_clear", or mentions implementing portal effects, masking systems, scope overlays, or stencil-based rendering for Nethercore ZX games.
version: 1.0.0
---

# Stencil Effects for Nethercore ZX

Implement masked rendering using the ZX stencil buffer. Create portals, scopes, mirrors, and shaped UI elements.

## Stencil FFI Functions

Reference `nethercore/include/zx.rs` lines 419-471 for complete signatures:

| Function | Purpose |
|----------|---------|
| `stencil_begin()` | Start writing to stencil buffer (mask creation) |
| `stencil_end()` | End mask creation, begin stencil testing |
| `stencil_clear()` | Return to normal rendering |
| `stencil_invert()` | Render outside the mask instead of inside |

## Stencil Flow

The stencil buffer works in three phases:

1. **Mask Creation** - Draw shapes that define the visible area
2. **Masked Rendering** - Only pixels inside mask are drawn
3. **Cleanup** - Return to normal rendering

```
stencil_begin()     → Draw mask shape (color buffer ignored)
stencil_end()       → Activate testing (draw only where mask exists)
[draw scene]        → Scene only visible inside mask
stencil_clear()     → Back to normal rendering
```

## Basic Circular Scope

Create a scope/binocular effect:

```rust
static mut CIRCLE_MESH: u32 = 0;

fn init() {
    unsafe {
        // Create circle mesh for mask
        CIRCLE_MESH = sphere(1.0, 32, 16);
    }
}

fn render() {
    unsafe {
        // 1. Draw scope mask
        stencil_begin();

        // Position circle at screen center using ortho projection
        push_identity();
        push_translate(0.0, 0.0, 0.0);  // Center
        push_scale_uniform(0.8);         // Size relative to screen
        draw_mesh(CIRCLE_MESH);

        stencil_end();

        // 2. Draw world (only visible inside circle)
        camera_set(cam_x, cam_y, cam_z, target_x, target_y, target_z);
        draw_env();
        draw_mesh(WORLD_MESH);

        // 3. Clear stencil for HUD
        stencil_clear();

        // Draw scope overlay texture on top
        texture_bind(SCOPE_TEXTURE);
        draw_sprite(0.0, 0.0, 960.0, 540.0, 0xFFFFFFFF);
    }
}
```

## Portal/Window Effect

Render a different scene through a portal:

```rust
fn render_portal() {
    unsafe {
        // 1. Draw portal frame shape to stencil
        stencil_begin();
        push_identity();
        push_translate(portal_x, portal_y, portal_z);
        draw_mesh(PORTAL_FRAME_MESH);  // Flat quad or arch shape
        stencil_end();

        // 2. Render "other side" scene inside portal
        camera_set(
            other_cam_x, other_cam_y, other_cam_z,
            other_target_x, other_target_y, other_target_z
        );
        draw_env();  // Different environment for other world
        draw_mesh(OTHER_WORLD_MESH);

        stencil_clear();

        // 3. Render main scene (portal frame as decoration)
        camera_set(cam_x, cam_y, cam_z, target_x, target_y, target_z);
        draw_env();
        draw_mesh(MAIN_WORLD_MESH);

        // Draw portal frame geometry
        push_translate(portal_x, portal_y, portal_z);
        draw_mesh(PORTAL_BORDER_MESH);
    }
}
```

## Mirror Reflection

Use stencil with flipped camera for mirrors:

```rust
fn render_mirror() {
    unsafe {
        // 1. Draw mirror surface to stencil
        stencil_begin();
        push_identity();
        push_translate(mirror_x, mirror_y, mirror_z);
        draw_mesh(MIRROR_QUAD);
        stencil_end();

        // 2. Render reflected scene
        // Flip camera Y around mirror plane
        let reflected_y = 2.0 * mirror_y - cam_y;
        camera_set(cam_x, reflected_y, cam_z, target_x, target_y, target_z);

        // Flip culling for reflected geometry
        cull_mode(2);  // Front-face culling
        draw_mesh(SCENE_MESH);
        cull_mode(1);  // Back to normal

        stencil_clear();

        // 3. Render normal scene
        camera_set(cam_x, cam_y, cam_z, target_x, target_y, target_z);
        draw_env();
        draw_mesh(SCENE_MESH);

        // Draw mirror frame
        push_translate(mirror_x, mirror_y, mirror_z);
        set_color(0x888888FF);  // Tint for mirror surface
        uniform_alpha(8);       // Semi-transparent
        draw_mesh(MIRROR_QUAD);
        uniform_alpha(15);
    }
}
```

## Vignette Effect

Use inverted stencil for screen edges:

```rust
fn render_vignette() {
    unsafe {
        // 1. Draw center area to stencil
        stencil_begin();
        // Draw a rounded rectangle or ellipse in center
        draw_mesh(ROUNDED_RECT_MESH);

        // 2. Invert - now we render OUTSIDE the mask
        stencil_invert();

        // 3. Draw dark overlay on edges
        set_color(0x00000080);  // Semi-transparent black
        draw_rect(0.0, 0.0, 960.0, 540.0, 0x000000C0);

        stencil_clear();
    }
}
```

## UI Masking (Non-Rectangular)

Create shaped UI elements:

```rust
fn render_shaped_minimap() {
    unsafe {
        // 1. Draw circular mask for minimap
        stencil_begin();
        // Use 2D circle at minimap location
        push_identity();
        // Position for top-right minimap
        draw_circle(880.0, 80.0, 60.0, 0xFFFFFFFF);
        stencil_end();

        // 2. Draw minimap content (only in circle)
        texture_bind(MINIMAP_TEXTURE);
        draw_sprite(820.0, 20.0, 120.0, 120.0, 0xFFFFFFFF);

        stencil_clear();

        // 3. Draw minimap border
        draw_circle_outline(880.0, 80.0, 60.0, 3.0, 0xFFFFFFFF);
    }
}
```

## Stencil + Depth Interaction

Stencil doesn't affect depth buffer. For correct portal occlusion:

```rust
fn render_portal_with_depth() {
    unsafe {
        // 1. Clear depth in portal area by drawing portal plane
        depth_test(0);  // Disable depth test
        stencil_begin();
        draw_mesh(PORTAL_QUAD);
        stencil_end();

        // 2. Re-enable depth, render portal contents
        depth_test(1);
        // Portal scene starts fresh depth from portal plane
        camera_set(...);
        draw_mesh(PORTAL_WORLD);

        stencil_clear();

        // 3. Main scene renders with portal as hole
        camera_set(...);
        draw_mesh(MAIN_WORLD);
    }
}
```

## Performance Notes

- Stencil buffer cleared automatically each frame
- Stencil operations are GPU-efficient (no extra passes)
- Mask geometry can be low-poly (silhouette matters)
- Nested stencil operations not supported (one level only)

## Rollback Safety

Stencil state is render-only and resets each frame - no rollback concerns. Camera positions and mask transforms should use static variables.

## Additional Resources

- **`examples/stencil-examples.md`** - Complete portal and scope implementations
- **`references/stencil-patterns.md`** - Advanced masking patterns
- **`nethercore/include/zx.rs`** lines 419-471 - Stencil FFI signatures
- **Gap 17 (Camera Systems)** - Camera flip for mirror reflections
- **Gap 9 (Split-Screen)** - Viewport clipping (alternative to stencil)
