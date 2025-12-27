# Gap 17: Camera Implementation

**Status:** `[x]` Completed
**Priority:** MEDIUM
**Plugin:** nethercore-zx-dev
**Type:** Skill

---

## Problem

FFI functions exist (`camera_set`, `camera_fov`, `push_view_matrix`, `push_projection_matrix`), but no implementation patterns. The perspective-patterns skill discusses camera TYPES (side-scroll, third-person, etc.) but provides no CODE for implementing them.

**Verified FFI functions (from `nethercore/include/zx.rs` — Camera Functions section):**
- `camera_set(x, y, z, target_x, target_y, target_z)` — Position camera and look-at
- `camera_fov(fov_degrees)` — Set field of view (typically 45-90, default 60)
- `push_view_matrix(m0..m15)` — Custom view matrix (16 floats, column-major)
- `push_projection_matrix(m0..m15)` — Custom projection matrix (16 floats, column-major)

## What's Missing

### Camera Types Implementation
- Follow camera (smooth follow with offset)
- Orbit camera (third-person, mouse/stick controlled)
- First-person camera (head bob, look sensitivity)
- Fixed camera (room-based, cinematic)
- Rail camera (on-rails movement)

### Camera Features
- Smooth interpolation (lerp, slerp)
- Dead zones (don't move until threshold)
- Look-ahead (move camera in movement direction)
- Zoom control

### Camera Collision
- Don't clip through walls
- Pull camera forward when obstructed
- Transparency fade when camera close to character

### Screen Effects (via camera)
- Screen shake implementation
- Camera punch (recoil)
- Smooth zoom transitions

## Prompt for Implementation

```
Add skill "camera-systems" to nethercore-zx-dev. Triggers: "camera follow",
"orbit camera", "third person camera", "first person camera", "camera collision",
"screen shake", "camera lerp", "camera implementation". Cover: follow camera
(smooth, offset, dead zone), orbit camera (pitch/yaw, distance), first-person
(look sensitivity), camera collision (raycast pull-in), screen shake. Include
Rust code using camera_set(), camera_fov(), push_view_matrix(), and
push_projection_matrix(). Reference Camera Functions section in
nethercore/include/zx.rs. ~1500 words.
```

## Dependencies

- None

## Related Gaps

- Gap 5 (Game Feel) for screen shake patterns
- Gap 9 (Split-Screen) for per-viewport cameras
- Gap 10 (Stencil) for mirror camera flip
- Gap 16 (Physics) for camera collision raycasting
