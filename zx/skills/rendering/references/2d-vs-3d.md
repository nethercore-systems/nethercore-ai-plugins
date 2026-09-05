# 2D vs 3D Rendering Guide

## Decision Matrix

| Game Type | Recommended Approach |
|-----------|---------------------|
| UI/HUD overlays | Always 2D (`draw_sprite`, `draw_text`) |
| Side-scrollers | 2D drawing OR 3D with orthographic camera |
| Top-down games | Either (2D simpler, 3D allows depth effects) |
| Isometric | 3D with fixed camera angle |
| 3D perspective games | 3D meshes + transforms |
| Hybrid (3D game + 2D UI) | Both - see pattern below |

## Coordinate Systems

| System | Origin | Axes | Used By |
|--------|--------|------|---------|
| **Screen space (2D)** | Top-left (0,0) | X right, Y down | `draw_sprite`, `draw_text`, `draw_rect` |
| **World space (3D)** | World origin | Y up, -Z forward | `push_translate`, `draw_mesh`, `camera_set` |

## 2D Drawing

Screen-space functions ignore camera and transforms.

```rust
fn render() {
    // Always draws at screen coordinates
    texture_bind(tex);
    set_color(0xFFFFFFFF);
    draw_sprite(10.0, 10.0, 64.0, 64.0);
    draw_text_str("SCORE: 100", 20.0, 20.0, 16.0);
    set_color(0xFF0000FF);
    draw_rect(0.0, 0.0, 100.0, 10.0); // Health bar
}
```

**Key functions:**
- `texture_bind(handle)` then `draw_sprite(x, y, w, h)`
- `draw_text(ptr, len, x, y, size)` (or the `draw_text_str` helper)
- `set_color(rgba)` then `draw_rect(x, y, w, h)`
- `set_color(rgba)` then `draw_line(x1, y1, x2, y2, thickness)`
- `set_color(rgba)` then `draw_circle(x, y, radius)`
- `z_index(n)` - Layer ordering (0-255)

## 3D Drawing

World-space functions use camera and transform stack.

```rust
fn render() {
    camera_set(cam_x, cam_y, cam_z, target_x, target_y, target_z);
    camera_fov(60.0);

    push_translate(entity_x, entity_y, entity_z);
    push_rotate_y(angle);
    push_scale_uniform(1.0);
    draw_mesh(MESH_HANDLE);
    push_identity(); // Reset transforms
}
```

**Key functions:**
- `camera_set(x,y,z, tx,ty,tz)` - Position + look-at
- `camera_fov(degrees)` - Field of view
- `push_translate(x, y, z)` - Move
- `push_rotate_y(degrees)` - Rotate (also `_x`, `_z`)
- `push_scale_uniform(s)` - Scale
- `draw_mesh(handle)` - Draw 3D mesh
- `push_identity()` - Reset transform stack

## Hybrid Pattern (3D Game + 2D UI)

```rust
fn render() {
    // 1. Set up camera for 3D world
    camera_set(cam_x, cam_y, cam_z, target_x, target_y, target_z);

    // 2. Draw 3D world
    for entity in entities {
        push_translate(entity.x, entity.y, entity.z);
        draw_mesh(entity.mesh);
        push_identity();
    }

    // 3. Draw 2D UI overlay in screen space
    z_index(255);
    texture_bind(HUD_TEX);
    set_color(0xFFFFFFFF);
    draw_sprite(10.0, 10.0, 200.0, 50.0);
    draw_text_str("HP: 100", 20.0, 25.0, 16.0);
}
```

## Performance Comparison

| Approach | Draw Calls | GPU Load | Best For |
|----------|------------|----------|----------|
| 2D sprites | Many small | Low (2D pipeline) | Simple games, UI |
| 3D meshes | Fewer large | Higher (3D pipeline) | Complex visuals |
| Batched sprites | Few large | Low | Sprite-heavy games |

## Common Patterns

### Pure 2D Game

```rust
fn render() {
    // Background
    texture_bind(BG);
    set_color(0xFFFFFFFF);
    draw_sprite(0.0, 0.0, 960.0, 540.0);

    // Entities (sorted by Y for depth)
    for entity in sorted_by_y(entities) {
        texture_bind(entity.tex);
        draw_sprite(entity.x, entity.y, 64.0, 64.0);
    }

    // UI on top
    z_index(255);
    draw_text_str("SCORE", 10.0, 10.0, 16.0);
}
```

### 2.5D (3D world, fixed camera)

```rust
fn render() {
    // Fixed isometric/top-down camera
    camera_set(0.0, 20.0, 20.0, 0.0, 0.0, 0.0);

    // 3D meshes
    for entity in entities {
        push_translate(entity.x, 0.0, entity.z);
        draw_mesh(entity.mesh);
        push_identity();
    }
}
```

### Full 3D

```rust
fn render() {
    // Player-following camera
    camera_set(
        player_x - 5.0, player_y + 3.0, player_z + 5.0,
        player_x, player_y, player_z
    );

    // Select the EPU environment source (16 u64 configuration values)
    epu_set(ENV_CONFIG.as_ptr());

    // Dynamic entities
    for entity in entities {
        push_translate(entity.x, entity.y, entity.z);
        push_rotate_y(entity.rotation);
        draw_mesh(entity.mesh);
        push_identity();
    }
    draw_epu(); // Environment background is drawn after geometry
}
```

## Z-Ordering

| Context | Method |
|---------|--------|
| 2D sprites | `z_index(0-255)` - Higher draws on top |
| 3D meshes | Depth buffer (automatic) |
| 2D on 3D | Draw after 3D and use `z_index` for layer ordering |
