# Gap 13: 3D Billboards & Particles

**Status:** `[ ]` Not Started
**Priority:** LOW
**Plugin:** nethercore-zx-dev
**Type:** Skill

---

## Problem

FFI exists for billboards, NO particle system patterns. Billboards are documented in FFI but particle effects using them aren't covered.

## FFI Functions (from zx.rs)

Billboards use the **transform stack** for positioning (not explicit x/y/z params) and **bound texture** (not texture handle param):

```rust
/// Draw a billboard (camera-facing quad) with full texture.
/// Uses currently bound texture and current transform position.
/// - w, h: Billboard size in world units
/// - mode: 1=spherical, 2=cylindrical Y, 3=cylindrical X, 4=cylindrical Z
/// - color: Color tint (0xRRGGBBAA)
pub fn draw_billboard(w: f32, h: f32, mode: u32, color: u32);

/// Draw a billboard with a UV region from the texture.
/// - w, h: Billboard size in world units
/// - src_x, src_y, src_w, src_h: UV region (0.0-1.0 normalized coordinates)
/// - mode: Billboard mode (1-4)
/// - color: Color tint (0xRRGGBBAA)
pub fn draw_billboard_region(
    w: f32, h: f32,
    src_x: f32, src_y: f32, src_w: f32, src_h: f32,
    mode: u32, color: u32,
);
```

### Billboard Modes (from zx.rs constants)
```rust
pub mod billboard {
    pub const SPHERICAL: u32 = 1;      // Fully faces camera
    pub const CYLINDRICAL_Y: u32 = 2;  // Rotates around Y axis only
    pub const CYLINDRICAL_X: u32 = 3;  // Rotates around X axis only
    pub const CYLINDRICAL_Z: u32 = 4;  // Rotates around Z axis only
}
```

### Usage Pattern
```rust
// Bind texture first
texture_bind(particle_texture);

// Position via transform stack
push_translate(x, y, z);

// Draw billboard at current transform
draw_billboard(1.0, 1.0, billboard::SPHERICAL, 0xFFFFFFFF);
```

## What's Missing

- Particle emitter patterns (spawn, update, render)
- Billboard sprite sheets (animation via UV regions with draw_billboard_region)
- Particle pooling for performance
- Common effects (smoke, fire, sparks, dust)
- Billboard mode selection guidance (spherical vs cylindrical)
- Integration with game-feel skill

## Prompt for Implementation

```
Add skill "billboard-particles" to nethercore-zx-dev. Triggers: "billboard",
"particles", "draw_billboard", "sprite 3D", "smoke effect", "sparks", "particle
system". Cover: billboard basics (position via transform stack, texture via
texture_bind), billboard modes (spherical for particles, cylindrical Y for trees/
grass), sprite sheet animation via draw_billboard_region UV regions, particle
emitter pattern (spawn/update/render), particle pooling, common effects (smoke,
fire, sparks, dust, rain), performance budgets. Tie to game-feel skill. ~1000 words.
```

## Dependencies

- None

## Related Gaps

- Gap 5 (Game Feel) for integration with polish effects
