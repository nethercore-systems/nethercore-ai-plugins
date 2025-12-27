# Gap 16: Physics & Collision

**Status:** `[x]` Completed
**Priority:** HIGH (CRITICAL)
**Plugin:** nethercore-zx-game-design
**Type:** Skill

---

## Problem

NOT covered. FFI provides no physics - games must implement their own.

**This is the most critical missing piece.** Every 3D game needs collision detection and physics, but ZX provides rendering only. Games must implement collision in WASM, and no plugin teaches this.

## What's Missing

### Collision Detection
- AABB (Axis-Aligned Bounding Box) intersection
- Sphere-sphere collision
- Capsule collision (for characters)
- Ray casting (for shooting, picking, ground detection)
- Mesh-based collision (simplified)

### Collision Response
- Slide along walls
- Bounce off surfaces
- Push out of overlap
- Trigger vs. solid colliders

### Basic Physics
- Gravity and velocity integration
- Terminal velocity
- Friction (ground, air)
- Deterministic physics for rollback (fixed timestep already provided)

### Spatial Partitioning
- Grid-based broad phase
- Simple octree (for larger worlds)

## Rollback Considerations

All physics MUST be deterministic. The FFI provides `delta_time()` as a fixed timestep and `random()` as seeded RNG - physics code must use these, never wall-clock time or external random.

## Prompt for Implementation

```
Add skill "physics-collision" to nethercore-zx-game-design. Triggers: "collision",
"physics", "AABB", "raycast", "gravity", "collision detection", "hit detection",
"collider". Cover: AABB intersection (2D and 3D), sphere collision, capsule for
characters, raycasting, collision response (slide, bounce), gravity/velocity
integration, friction, determinism for rollback (use delta_time(), random()).
Include Rust code examples. ~2000 words.
```

## Dependencies

- None

## Related Gaps

- Gap 18 (Gameplay Mechanics) uses collision for platforming, combat
- Gap 17 (Camera) for camera collision
