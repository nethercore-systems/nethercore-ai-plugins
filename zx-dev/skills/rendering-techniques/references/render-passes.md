# Advanced Render Pass Patterns

Complete patterns from the stencil-demo example. For basic patterns, see the main SKILL.md.

## API Quick Reference

```rust
begin_pass(clear_depth)                        // Standard depth pass
begin_pass_stencil_write(ref_value, clear_depth)  // Mask creation
begin_pass_stencil_test(ref_value, clear_depth)   // Render inside mask
begin_pass_full(                                // Full control
    depth_compare,      // compare::LESS, etc.
    depth_write,        // 0 or 1
    clear_depth,        // 0 or 1
    stencil_compare,    // compare::EQUAL, etc.
    stencil_ref,        // Reference value
    stencil_pass_op,    // stencil_op::KEEP, etc.
    stencil_fail_op,
    stencil_depth_fail_op,
)
z_index(n)                                     // 2D ordering (0-255)
```

---

## Demo 0: Circle Mask (Basic)

Simple circular mask - content only visible inside circle.

```rust
fn render_circle_mask() {
    // Create circular mask
    begin_pass_stencil_write(1, 0);
    draw_circle(SCREEN_CX, SCREEN_CY, 200.0);

    // Render scene inside mask
    begin_pass_stencil_test(1, 0);
    draw_scene();

    // Return to normal
    begin_pass(0);
}
```

**Key points:**
- `begin_pass_stencil_write` draws geometry to stencil only (no color output)
- `begin_pass_stencil_test` only renders where stencil matches ref value

---

## Demo 1: Inverted Mask / Vignette

Render OUTSIDE the mask using `NOT_EQUAL` comparison.

```rust
fn render_vignette() {
    // Draw scene first (unmasked)
    draw_scene();

    // Create circle mask
    begin_pass_stencil_write(1, 0);
    draw_circle(SCREEN_CX, SCREEN_CY, 250.0);

    // Render OUTSIDE mask (NOT_EQUAL)
    begin_pass_full(
        compare::LESS,        // Standard depth compare
        1,                    // Write to depth buffer
        0,                    // Don't clear depth
        compare::NOT_EQUAL,   // Inverted stencil test!
        1,                    // Reference value to compare against
        stencil_op::KEEP,     // Keep stencil on pass
        stencil_op::KEEP,     // Keep stencil on fail
        stencil_op::KEEP,     // Keep stencil on depth fail
    );
    set_color(0x000000AA);  // Semi-transparent black
    draw_rect(0.0, 0.0, SCREEN_WIDTH, SCREEN_HEIGHT);  // Dark vignette

    begin_pass(0);
}
```

**Key insight:** `compare::NOT_EQUAL` renders where stencil != ref, creating inverted masks.

---

## Demo 2: Diagonal Split with Different Tints

Split screen diagonally with different color treatments on each side.

```rust
fn render_diagonal_split() {
    // Create diagonal mask using screen-space triangle
    begin_pass_stencil_write(1, 0);

    // Screen-space orthographic for 2D mask geometry
    push_projection_matrix(
        2.0/SCREEN_WIDTH, 0.0, 0.0, 0.0,
        0.0, -2.0/SCREEN_HEIGHT, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        -1.0, 1.0, 0.0, 1.0,
    );
    push_view_matrix(
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    );

    // Triangle covering top-right half
    let verts: [f32; 9] = [
        0.0, 0.0, 0.0,                    // Bottom-left
        SCREEN_WIDTH, 0.0, 0.0,           // Bottom-right
        SCREEN_WIDTH, SCREEN_HEIGHT, 0.0, // Top-right
    ];
    draw_triangles(verts.as_ptr(), 3, format::POS);
    push_identity();

    // Top-right side: warm tint (inside mask)
    begin_pass_stencil_test(1, 0);
    set_color(0xFFCCAA80);  // Warm overlay
    draw_scene();

    // Bottom-left side: cool tint (outside mask via NOT_EQUAL)
    begin_pass_full(
        compare::LESS, 1, 0,
        compare::NOT_EQUAL, 1,
        stencil_op::KEEP, stencil_op::KEEP, stencil_op::KEEP,
    );
    set_color(0xAABBFF80);  // Cool overlay
    draw_scene();

    begin_pass(0);
}
```

**Use cases:** Day/night split, memory flashback effects, dimension shifts.

---

## Demo 3: Animated Portal

Full portal effect with decorative ring and separate interior view.

```rust
fn render_portal(time: f32) {
    // Draw main world
    camera_set(main_cam_x, main_cam_y, main_cam_z,
               main_look_x, main_look_y, main_look_z);
    draw_env();
    draw_mesh(MAIN_WORLD);

    // Portal ring decoration (no depth write - decorative only)
    begin_pass_full(
        compare::ALWAYS,      // Always pass depth test
        0,                    // depth_write = FALSE (critical!)
        0,                    // Don't clear depth
        compare::ALWAYS,      // Always pass stencil
        0,                    // No ref value needed
        stencil_op::KEEP, stencil_op::KEEP, stencil_op::KEEP,
    );
    push_translate(portal_x, portal_y, portal_z);
    push_rotate_z(time * 30.0);  // Spinning ring animation
    texture_bind(PORTAL_RING_TEX);
    draw_mesh(PORTAL_RING);
    push_identity();

    // Create portal mask (inner circle)
    begin_pass_stencil_write(1, 0);
    push_translate(portal_x, portal_y, portal_z);
    draw_circle(0.0, 0.0, PORTAL_RADIUS);
    push_identity();

    // Portal interior with clear_depth=1 for separate 3D view
    begin_pass_stencil_test(1, 1);  // clear_depth = 1!
    camera_set(other_cam_x, other_cam_y, other_cam_z,
               other_look_x, other_look_y, other_look_z);
    draw_env();
    draw_mesh(OTHER_WORLD);

    // Return to normal
    begin_pass(0);
}
```

**Critical insights:**
- **Ring decoration:** Uses `depth_write=0` so it doesn't block the interior
- **Portal interior:** Uses `clear_depth=1` to reset depth buffer for separate 3D scene
- **Execution order:** Ring must render BEFORE mask creation to appear behind portal edge

---

## FPS Viewmodel Pattern

Render weapon on top of everything using depth clear.

```rust
fn render_fps_view() {
    // Draw world
    camera_set(player_x, player_y, player_z, look_x, look_y, look_z);
    draw_env();
    draw_mesh(LEVEL);
    draw_enemies();

    // New pass with depth clear - viewmodel always renders on top
    begin_pass(1);  // clear_depth = 1

    // Viewmodel uses separate camera/transform
    push_translate(0.3, -0.2, 0.5);   // Offset from view
    push_rotate_y(sway_angle);         // Weapon sway
    push_rotate_x(bob_angle);          // View bob
    draw_mesh(GUN);
    push_identity();
}
```

**Why it works:** `begin_pass(1)` clears the depth buffer, so the viewmodel's depth starts fresh and renders on top of everything from the previous pass.

---

## Z-Index for 2D Ordering

Control 2D draw order within a single render pass.

```rust
fn render_2d_layers() {
    // Background (layer 0 - furthest back)
    z_index(0);
    draw_sprite(0.0, 0.0, 960.0, 540.0);  // Fullscreen BG

    // Game objects (layer 1)
    z_index(1);
    for enemy in enemies.iter() {
        draw_sprite(enemy.x, enemy.y, 32.0, 32.0);
    }
    draw_sprite(player_x, player_y, 32.0, 32.0);

    // Particles (layer 2)
    z_index(2);
    for particle in particles.iter() {
        draw_sprite(particle.x, particle.y, 8.0, 8.0);
    }

    // UI (layer 3 - closest)
    z_index(3);
    draw_text_str("SCORE: 1000", 10.0, 10.0, 24.0);
    draw_sprite(health_bar_x, health_bar_y, health_bar_w, 16.0);
}
```

**Important notes:**
- `z_index` only affects ordering within the **same render pass**
- Range: 0-255 (higher = closer/on top)
- Resets to 0 each frame
- Does NOT affect 3D depth testing (use transforms for 3D ordering)

---

## begin_pass_full Parameter Reference

```rust
begin_pass_full(
    depth_compare: u32,       // When depth test passes
    depth_write: u32,         // Write to depth buffer (0=no, 1=yes)
    clear_depth: u32,         // Clear depth buffer (0=no, 1=yes)
    stencil_compare: u32,     // When stencil test passes
    stencil_ref: u32,         // Reference value for stencil ops
    stencil_pass_op: u32,     // What to do when stencil passes
    stencil_fail_op: u32,     // What to do when stencil fails
    stencil_depth_fail_op: u32, // Stencil pass but depth fails
)
```

### Common Configurations

**Standard rendering (default):**
```rust
begin_pass_full(compare::LESS, 1, 0, compare::ALWAYS, 0,
    stencil_op::KEEP, stencil_op::KEEP, stencil_op::KEEP);
```

**Decorative overlay (no depth write):**
```rust
begin_pass_full(compare::ALWAYS, 0, 0, compare::ALWAYS, 0,
    stencil_op::KEEP, stencil_op::KEEP, stencil_op::KEEP);
```

**Inverted stencil mask:**
```rust
begin_pass_full(compare::LESS, 1, 0, compare::NOT_EQUAL, 1,
    stencil_op::KEEP, stencil_op::KEEP, stencil_op::KEEP);
```

**Multiple stencil layers (increment ref):**
```rust
// Pass 1: Write ref=1 for inner area
begin_pass_stencil_write(1, 0);
draw_circle(x, y, small_radius);

// Pass 2: Increment to ref=2 for middle area
begin_pass_full(compare::ALWAYS, 0, 0, compare::EQUAL, 1,
    stencil_op::INCREMENT_CLAMP, stencil_op::KEEP, stencil_op::KEEP);
draw_circle(x, y, medium_radius);

// Now can test against ref=1 or ref=2 for different effects
```
