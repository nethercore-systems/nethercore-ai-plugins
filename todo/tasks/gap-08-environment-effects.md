# Gap 8: Environment Processing Unit (EPU)

**Status:** `[ ]` Not Started
**Priority:** MEDIUM
**Plugin:** nethercore-zx-dev
**Type:** Skill

---

## Problem

FFI exists with 8 environment modes on a dual-layer system, NO plugin documentation. The ZX console has a powerful EPU for procedural backgrounds and post-effects, but it's completely undocumented in the plugins.

## FFI Functions (from zx.rs)

The EPU uses a dual-layer system where each mode can be configured on layer 0 (base) and/or layer 1 (overlay), then blended together.

### Mode 0: Gradient
```rust
/// 4-color gradient background with vertical blending.
env_gradient(
    layer: u32,           // 0 = base, 1 = overlay
    zenith: u32,          // Color directly overhead (0xRRGGBBAA)
    sky_horizon: u32,     // Sky color at horizon
    ground_horizon: u32,  // Ground color at horizon
    nadir: u32,           // Color directly below
    rotation: f32,        // Rotation around Y axis in radians
    shift: f32,           // Horizon vertical shift (-1.0 to 1.0)
);
```

### Mode 1: Scatter (stars, rain, warp)
```rust
/// Procedural particle field.
env_scatter(
    layer: u32,           // 0 = base, 1 = overlay
    variant: u32,         // 0=Stars, 1=Vertical (rain), 2=Horizontal, 3=Warp
    density: u32,         // Particle count (0-255)
    size: u32,            // Particle size (0-255)
    glow: u32,            // Glow/bloom intensity (0-255)
    streak_length: u32,   // Elongation for streaks (0-63, 0=points)
    color_primary: u32,   // Main particle color (0xRRGGBB00)
    color_secondary: u32, // Variation/twinkle color (0xRRGGBB00)
    parallax_rate: u32,   // Layer separation amount (0-255)
    parallax_size: u32,   // Size variation with depth (0-255)
    phase: u32,           // Animation phase (0-65535, wraps)
);
```

### Mode 2: Lines (synthwave grid, racing track)
```rust
/// Infinite procedural grid.
env_lines(
    layer: u32,           // 0 = base, 1 = overlay
    variant: u32,         // 0=Floor, 1=Ceiling, 2=Sphere
    line_type: u32,       // 0=Horizontal, 1=Vertical, 2=Grid
    thickness: u32,       // Line thickness (0-255)
    spacing: f32,         // Distance between lines in world units
    fade_distance: f32,   // Distance where lines start fading
    color_primary: u32,   // Main line color (0xRRGGBBAA)
    color_accent: u32,    // Accent line color (0xRRGGBBAA)
    accent_every: u32,    // Make every Nth line use accent color
    phase: u32,           // Scroll phase (0-65535, wraps)
);
```

### Mode 3: Silhouette (mountains, cityscape)
```rust
/// Layered terrain silhouettes with procedural noise.
env_silhouette(
    layer: u32,           // 0 = base, 1 = overlay
    jaggedness: u32,      // Terrain roughness (0-255, 0=smooth, 255=sharp)
    layer_count: u32,     // Number of depth layers (1-3)
    color_near: u32,      // Nearest silhouette color (0xRRGGBBAA)
    color_far: u32,       // Farthest silhouette color (0xRRGGBBAA)
    sky_zenith: u32,      // Sky color at zenith (0xRRGGBBAA)
    sky_horizon: u32,     // Sky color at horizon (0xRRGGBBAA)
    parallax_rate: u32,   // Layer separation (0-255)
    seed: u32,            // Noise seed for terrain shape
);
```

### Mode 4: Rectangles (city windows, control panels)
```rust
/// Rectangular light sources like windows or screens.
env_rectangles(
    layer: u32,           // 0 = base, 1 = overlay
    variant: u32,         // 0=Scatter, 1=Buildings, 2=Bands, 3=Panels
    density: u32,         // How many rectangles (0-255)
    lit_ratio: u32,       // Percentage lit (0-255, 128=50%)
    size_min: u32,        // Minimum size (0-63)
    size_max: u32,        // Maximum size (0-63)
    aspect: u32,          // Aspect ratio bias (0-3, 0=square, 3=very tall)
    color_primary: u32,   // Main window/panel color (0xRRGGBBAA)
    color_variation: u32, // Color variation (0xRRGGBBAA)
    parallax_rate: u32,   // Layer separation (0-255)
    phase: u32,           // Flicker phase (0-65535, wraps)
);
```

### Mode 5: Room (interior spaces)
```rust
/// Interior of a 3D box with directional lighting.
env_room(
    layer: u32,           // 0 = base, 1 = overlay
    color_ceiling: u32,   // Ceiling color (0xRRGGBB00)
    color_floor: u32,     // Floor color (0xRRGGBB00)
    color_walls: u32,     // Wall color (0xRRGGBB00)
    panel_size: f32,      // Wall panel pattern size in world units
    panel_gap: u32,       // Gap between panels (0-255)
    light_dir_x: f32,     // Light direction X
    light_dir_y: f32,     // Light direction Y
    light_dir_z: f32,     // Light direction Z
    light_intensity: u32, // Directional light strength (0-255)
    corner_darken: u32,   // Corner/edge darkening (0-255)
    room_scale: f32,      // Room size multiplier
    viewer_x: i32,        // Viewer X position (-128 to 127)
    viewer_y: i32,        // Viewer Y position (-128 to 127)
    viewer_z: i32,        // Viewer Z position (-128 to 127)
);
```

### Mode 6: Curtains (pillars, trees, vertical structures)
```rust
/// Vertical structures arranged around the viewer.
env_curtains(
    layer: u32,           // 0 = base, 1 = overlay
    layer_count: u32,     // Depth layers (1-3)
    density: u32,         // Structures per cell (0-255)
    height_min: u32,      // Minimum height (0-63)
    height_max: u32,      // Maximum height (0-63)
    width: u32,           // Structure width (0-31)
    spacing: u32,         // Gap between structures (0-31)
    waviness: u32,        // Organic wobble (0-255, 0=straight)
    color_near: u32,      // Nearest structure color (0xRRGGBBAA)
    color_far: u32,       // Farthest structure color (0xRRGGBBAA)
    glow: u32,            // Neon/magical glow (0-255)
    parallax_rate: u32,   // Layer separation (0-255)
    phase: u32,           // Horizontal scroll phase (0-65535, wraps)
);
```

### Mode 7: Rings (portals, tunnels, vortex)
```rust
/// Concentric rings for portals or vortex effects.
env_rings(
    layer: u32,           // 0 = base, 1 = overlay
    ring_count: u32,      // Number of rings (1-255)
    thickness: u32,       // Ring thickness (0-255)
    color_a: u32,         // First alternating color (0xRRGGBBAA)
    color_b: u32,         // Second alternating color (0xRRGGBBAA)
    center_color: u32,    // Bright center color (0xRRGGBBAA)
    center_falloff: u32,  // Center glow falloff (0-255)
    spiral_twist: f32,    // Spiral rotation in degrees (0=concentric)
    axis_x: f32,          // Ring axis X (normalized)
    axis_y: f32,          // Ring axis Y (normalized)
    axis_z: f32,          // Ring axis Z (normalized)
    phase: u32,           // Rotation phase (0-65535, wraps)
);
```

### Layer Blending
```rust
/// Set blend mode for combining base and overlay layers.
/// mode: 0=Alpha, 1=Add, 2=Multiply, 3=Screen
env_blend(mode: u32);
```

### Rendering
```rust
/// Render the configured environment. Call first in render().
draw_env();
```

## What's Missing

- EPU mode overview with visual examples
- Parameter tuning guide for each mode
- Combining dual-layer effects (base + overlay)
- Blend mode explanations and use cases
- Animation techniques using `phase` parameter
- Performance characteristics
- Use case examples (space game, racing, platformer, etc.)

## Prompt for Implementation

```
Add skill "environment-effects" to nethercore-zx-dev. Triggers: "EPU", "environment",
"background effect", "env_gradient", "env_scatter", "env_lines", "env_silhouette",
"env_rectangles", "env_room", "env_curtains", "env_rings", "procedural background",
"sky effect", "draw_env".

Cover the dual-layer EPU system:
1. Overview of 8 modes (gradient, scatter, lines, silhouette, rectangles, room, curtains, rings)
2. Layer system (layer 0 = base, layer 1 = overlay)
3. env_blend modes (Alpha, Add, Multiply, Screen)
4. Full parameter documentation for each mode (use zx.rs as source of truth)
5. Animation via phase parameter (0-65535 wrapping)
6. Practical use cases:
   - Space game: scatter(Stars) on base + gradient overlay
   - Racing: lines(Floor) + gradient sky
   - Platformer: silhouette mountains + gradient
   - Title screen: rings for portal effect
   - Interior scene: room mode

Source: nethercore/include/zx.rs lines 800-970 (EPU section)
Reference actual function signatures, not simplified versions.
~1500 words.
```

## Dependencies

- None

## Related Gaps

- None (standalone FFI documentation)
