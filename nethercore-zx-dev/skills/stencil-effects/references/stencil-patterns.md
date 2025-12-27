# Advanced Stencil Patterns

Reference guide for complex stencil techniques in Nethercore ZX.

## Stencil State Machine

```
NORMAL → stencil_begin() → WRITING
WRITING → stencil_end() → TESTING_INSIDE
TESTING_INSIDE → stencil_invert() → TESTING_OUTSIDE
WRITING → stencil_invert() → TESTING_OUTSIDE (skip inside testing)
TESTING_* → stencil_clear() → NORMAL
```

## Mask Shape Options

| Shape | Method | Notes |
|-------|--------|-------|
| Circle | `draw_circle()` or `sphere()` | 2D for UI, 3D sphere viewed head-on |
| Rectangle | `draw_rect()` or `plane()` | Simplest mask |
| Arbitrary | `draw_mesh()` | Custom silhouette mesh |
| Text | `draw_text()` | Text-shaped masks |
| Combined | Multiple draws | Union of all shapes |

## Multiple Masked Regions

Stencil accumulates during WRITING phase:

```rust
stencil_begin();
draw_circle(100.0, 100.0, 50.0, 0xFFFFFFFF);  // Region 1
draw_circle(200.0, 150.0, 50.0, 0xFFFFFFFF);  // Region 2
draw_rect(300.0, 100.0, 80.0, 60.0, 0xFFFFFFFF);  // Region 3
stencil_end();

// Scene visible in ALL three regions
draw_mesh(SCENE);
```

## Stencil vs Viewport

| Feature | Stencil | Viewport |
|---------|---------|----------|
| Arbitrary shapes | Yes | Rectangle only |
| Multiple regions | Yes | One at a time |
| Camera aspect | Unchanged | Auto-adjusted |
| Performance | GPU mask | Scissor test |
| Use case | Effects | Split-screen |

Combine both for shaped split-screen:

```rust
// Player 1: left half, circular mask
viewport(0, 0, 480, 540);
stencil_begin();
draw_circle(240.0, 270.0, 200.0, 0xFFFFFFFF);
stencil_end();
// ... render P1 view ...
stencil_clear();
viewport_clear();
```

## Transition Effects

### Iris Wipe

```rust
static mut IRIS_SIZE: f32 = 540.0;  // Full screen to 0

fn update_iris_out() {
    unsafe {
        IRIS_SIZE -= delta_time() * 300.0;
        if IRIS_SIZE < 0.0 { IRIS_SIZE = 0.0; }
    }
}

fn render_with_iris() {
    unsafe {
        stencil_begin();
        draw_circle(480.0, 270.0, IRIS_SIZE, 0xFFFFFFFF);
        stencil_end();

        // Scene only visible in shrinking circle
        draw_env();
        draw_mesh(SCENE);

        stencil_clear();
    }
}
```

### Star Wipe

Use star-shaped mesh for stencil mask, animate scale:

```rust
stencil_begin();
push_identity();
push_translate(480.0, 270.0, 0.0);
push_scale_uniform(wipe_scale);
push_rotate_z(wipe_rotation);
draw_mesh(STAR_MESH);
stencil_end();
```

## Depth Buffer Considerations

### Portal Depth Problem

Without depth handling, portal contents may Z-fight:

```
Main scene depth: 0.1 - 100.0
Portal contents: also 0.1 - 100.0  ← Conflict!
```

### Solution: Clear Depth in Portal Area

```rust
// 1. Render main scene first (fills depth buffer)
camera_set(...main camera...);
draw_mesh(MAIN_WORLD);

// 2. Clear depth where portal is
depth_test(0);  // Disable test, but still write
stencil_begin();
// Draw portal quad - this writes to stencil AND depth
// (depth becomes "far" value, clearing that region)
draw_mesh(PORTAL_QUAD);
stencil_end();

// 3. Portal contents now render correctly
depth_test(1);
camera_set(...portal camera...);
draw_mesh(PORTAL_WORLD);

stencil_clear();
```

## Performance Guidelines

| Operation | Cost |
|-----------|------|
| stencil_begin/end | ~0 (state change) |
| Mask geometry | Minimal (fill rate) |
| Stencil test | Free (HW) |
| Multiple regions | Additive fill |

**Tips:**
- Keep mask geometry simple (silhouette only matters)
- Avoid very small stencil regions (overdraw waste)
- One stencil layer only (no nesting)
- Clear stencil when done to avoid artifacts

## Common Issues

### Nothing Renders After stencil_end()

- **Cause:** Mask geometry didn't cover intended area
- **Fix:** Check mask position, ensure it's visible to camera during write

### Inverted Mask Wrong

- **Cause:** Called `stencil_invert()` after `stencil_clear()`
- **Fix:** Call `stencil_invert()` before `stencil_clear()`, after `stencil_begin()`

### Stencil Persists Between Frames

- **Cause:** Missing `stencil_clear()` call
- **Fix:** Always call `stencil_clear()` when done

### Mask Visible as Geometry

- **Cause:** Mask mesh has color/texture
- **Fix:** Mask geometry doesn't need valid appearance - only shape matters. Color buffer is ignored during stencil write.

## Debugging Stencil

No direct stencil visualization in ZX. Workarounds:

```rust
// Temporarily render mask as visible to debug shape
set_color(0xFF0000FF);  // Red
draw_mesh(MASK_MESH);
set_color(0xFFFFFFFF);

// Comment out stencil calls to verify scene renders correctly
// stencil_begin();
draw_mesh(MASK_MESH);
// stencil_end();
```
