---
name: Physics & Collision for ZX
description: This skill should be used when the user asks about "collision", "physics", "AABB", "raycast", "gravity", "collision detection", "hit detection", "collider", "bounding box", "intersect", "sphere collision", "capsule collision", or discusses implementing physics or collision systems for Nethercore ZX games.
version: 1.0.0
---

# Physics & Collision for Nethercore ZX

ZX provides rendering only — games must implement their own physics and collision detection in WASM. All physics code MUST be deterministic for rollback netcode compatibility.

## Determinism Requirements

**Critical:** Use only these FFI functions for time and randomness:

| FFI Function | Purpose |
|--------------|---------|
| `delta_time()` | Fixed timestep (1/60 at 60fps) — NOT wall-clock time |
| `random()` | Seeded RNG — deterministic across all clients |
| `random_range(min, max)` | Seeded range RNG |
| `tick_count()` | Current tick number |

**Never use** in `update()`:
- `std::time` or system clock
- `rand()` without seeding
- HashMap iteration (order varies by platform)
- External I/O or floating-point edge cases (NaN, denormals)

## Core Collision Types

### AABB (Axis-Aligned Bounding Box)

The simplest and fastest collision primitive. Use for rectangular objects, level geometry, and broad-phase culling.

```rust
#[derive(Clone, Copy)]
struct AABB {
    min: [f32; 3],  // Bottom-left-back corner
    max: [f32; 3],  // Top-right-front corner
}

impl AABB {
    fn new(center: [f32; 3], half_extents: [f32; 3]) -> Self {
        Self {
            min: [center[0] - half_extents[0], center[1] - half_extents[1], center[2] - half_extents[2]],
            max: [center[0] + half_extents[0], center[1] + half_extents[1], center[2] + half_extents[2]],
        }
    }

    fn intersects(&self, other: &AABB) -> bool {
        self.min[0] <= other.max[0] && self.max[0] >= other.min[0] &&
        self.min[1] <= other.max[1] && self.max[1] >= other.min[1] &&
        self.min[2] <= other.max[2] && self.max[2] >= other.min[2]
    }

    fn contains_point(&self, p: [f32; 3]) -> bool {
        p[0] >= self.min[0] && p[0] <= self.max[0] &&
        p[1] >= self.min[1] && p[1] <= self.max[1] &&
        p[2] >= self.min[2] && p[2] <= self.max[2]
    }
}
```

### Sphere Collision

Ideal for characters, projectiles, and any roughly circular object.

```rust
#[derive(Clone, Copy)]
struct Sphere {
    center: [f32; 3],
    radius: f32,
}

impl Sphere {
    fn intersects(&self, other: &Sphere) -> bool {
        let dx = self.center[0] - other.center[0];
        let dy = self.center[1] - other.center[1];
        let dz = self.center[2] - other.center[2];
        let dist_sq = dx * dx + dy * dy + dz * dz;
        let radii_sum = self.radius + other.radius;
        dist_sq <= radii_sum * radii_sum
    }

    fn intersects_aabb(&self, aabb: &AABB) -> bool {
        // Find closest point on AABB to sphere center
        let closest = [
            self.center[0].clamp(aabb.min[0], aabb.max[0]),
            self.center[1].clamp(aabb.min[1], aabb.max[1]),
            self.center[2].clamp(aabb.min[2], aabb.max[2]),
        ];
        let dx = self.center[0] - closest[0];
        let dy = self.center[1] - closest[1];
        let dz = self.center[2] - closest[2];
        dx * dx + dy * dy + dz * dz <= self.radius * self.radius
    }
}
```

### Raycasting

Essential for shooting, ground detection, line-of-sight, and picking.

```rust
struct Ray {
    origin: [f32; 3],
    direction: [f32; 3],  // Must be normalized
}

struct RayHit {
    t: f32,              // Distance along ray
    point: [f32; 3],     // Hit position
    normal: [f32; 3],    // Surface normal at hit
}

impl Ray {
    /// Raycast against AABB. Returns Some(t) if hit, where hit_point = origin + direction * t
    fn intersect_aabb(&self, aabb: &AABB) -> Option<f32> {
        let mut t_min = 0.0f32;
        let mut t_max = f32::MAX;

        for i in 0..3 {
            if self.direction[i].abs() < 1e-8 {
                // Ray parallel to slab
                if self.origin[i] < aabb.min[i] || self.origin[i] > aabb.max[i] {
                    return None;
                }
            } else {
                let inv_d = 1.0 / self.direction[i];
                let mut t1 = (aabb.min[i] - self.origin[i]) * inv_d;
                let mut t2 = (aabb.max[i] - self.origin[i]) * inv_d;
                if t1 > t2 { core::mem::swap(&mut t1, &mut t2); }
                t_min = t_min.max(t1);
                t_max = t_max.min(t2);
                if t_min > t_max { return None; }
            }
        }
        if t_min >= 0.0 { Some(t_min) } else { None }
    }

    /// Raycast against sphere
    fn intersect_sphere(&self, sphere: &Sphere) -> Option<f32> {
        let oc = [
            self.origin[0] - sphere.center[0],
            self.origin[1] - sphere.center[1],
            self.origin[2] - sphere.center[2],
        ];
        let a = self.direction[0] * self.direction[0]
              + self.direction[1] * self.direction[1]
              + self.direction[2] * self.direction[2];
        let b = 2.0 * (oc[0] * self.direction[0] + oc[1] * self.direction[1] + oc[2] * self.direction[2]);
        let c = oc[0] * oc[0] + oc[1] * oc[1] + oc[2] * oc[2] - sphere.radius * sphere.radius;
        let discriminant = b * b - 4.0 * a * c;

        if discriminant < 0.0 { return None; }
        let t = (-b - discriminant.sqrt()) / (2.0 * a);
        if t >= 0.0 { Some(t) } else { None }
    }
}
```

## Collision Response

### Penetration Resolution (Push Out)

When objects overlap, push them apart along the minimum translation vector:

```rust
fn resolve_aabb_penetration(a: &AABB, b: &AABB) -> Option<[f32; 3]> {
    // Calculate overlap on each axis
    let overlap_x = (a.max[0].min(b.max[0]) - a.min[0].max(b.min[0])).max(0.0);
    let overlap_y = (a.max[1].min(b.max[1]) - a.min[1].max(b.min[1])).max(0.0);
    let overlap_z = (a.max[2].min(b.max[2]) - a.min[2].max(b.min[2])).max(0.0);

    if overlap_x <= 0.0 || overlap_y <= 0.0 || overlap_z <= 0.0 {
        return None; // No collision
    }

    // Push out along axis with minimum overlap
    let center_a = [(a.min[0] + a.max[0]) * 0.5, (a.min[1] + a.max[1]) * 0.5, (a.min[2] + a.max[2]) * 0.5];
    let center_b = [(b.min[0] + b.max[0]) * 0.5, (b.min[1] + b.max[1]) * 0.5, (b.min[2] + b.max[2]) * 0.5];

    if overlap_x <= overlap_y && overlap_x <= overlap_z {
        let sign = if center_a[0] > center_b[0] { 1.0 } else { -1.0 };
        Some([overlap_x * sign, 0.0, 0.0])
    } else if overlap_y <= overlap_z {
        let sign = if center_a[1] > center_b[1] { 1.0 } else { -1.0 };
        Some([0.0, overlap_y * sign, 0.0])
    } else {
        let sign = if center_a[2] > center_b[2] { 1.0 } else { -1.0 };
        Some([0.0, 0.0, overlap_z * sign])
    }
}
```

### Slide Response

For character controllers sliding along walls:

```rust
fn slide_velocity(velocity: [f32; 3], normal: [f32; 3]) -> [f32; 3] {
    // Remove velocity component along normal
    let dot = velocity[0] * normal[0] + velocity[1] * normal[1] + velocity[2] * normal[2];
    if dot >= 0.0 { return velocity; } // Moving away from surface

    [
        velocity[0] - dot * normal[0],
        velocity[1] - dot * normal[1],
        velocity[2] - dot * normal[2],
    ]
}
```

### Bounce Response

For projectiles and physics objects:

```rust
fn bounce_velocity(velocity: [f32; 3], normal: [f32; 3], restitution: f32) -> [f32; 3] {
    let dot = velocity[0] * normal[0] + velocity[1] * normal[1] + velocity[2] * normal[2];
    if dot >= 0.0 { return velocity; }

    let reflect = 1.0 + restitution;
    [
        velocity[0] - reflect * dot * normal[0],
        velocity[1] - reflect * dot * normal[1],
        velocity[2] - reflect * dot * normal[2],
    ]
}
```

## Basic Physics

### Velocity Integration

Use the fixed timestep from `delta_time()` for deterministic physics:

```rust
struct PhysicsBody {
    position: [f32; 3],
    velocity: [f32; 3],
    acceleration: [f32; 3],
}

impl PhysicsBody {
    fn integrate(&mut self, dt: f32) {
        // Semi-implicit Euler (stable for games)
        self.velocity[0] += self.acceleration[0] * dt;
        self.velocity[1] += self.acceleration[1] * dt;
        self.velocity[2] += self.acceleration[2] * dt;

        self.position[0] += self.velocity[0] * dt;
        self.position[1] += self.velocity[1] * dt;
        self.position[2] += self.velocity[2] * dt;
    }
}
```

### Gravity with Terminal Velocity

```rust
const GRAVITY: f32 = -20.0;      // Units per second squared
const TERMINAL_VELOCITY: f32 = -30.0;

fn apply_gravity(velocity: &mut [f32; 3], dt: f32) {
    velocity[1] += GRAVITY * dt;
    velocity[1] = velocity[1].max(TERMINAL_VELOCITY);
}
```

### Friction

```rust
fn apply_friction(velocity: &mut [f32; 3], friction: f32, dt: f32) {
    let factor = (1.0 - friction * dt).max(0.0);
    velocity[0] *= factor;
    velocity[2] *= factor;
}

// Different friction for ground vs air
const GROUND_FRICTION: f32 = 8.0;
const AIR_FRICTION: f32 = 0.5;
```

## Trigger vs. Solid Colliders

Distinguish between colliders that block movement and those that only detect overlap:

```rust
#[derive(Clone, Copy, PartialEq)]
enum ColliderType {
    Solid,    // Blocks movement, resolves penetration
    Trigger,  // Detects overlap only, doesn't block
}

struct Collider {
    bounds: AABB,
    collider_type: ColliderType,
    layer: u32,  // For collision filtering
}

fn process_collisions(player: &mut PhysicsBody, colliders: &[Collider]) {
    let player_aabb = AABB::new(player.position, [0.5, 1.0, 0.5]);

    for collider in colliders {
        if player_aabb.intersects(&collider.bounds) {
            match collider.collider_type {
                ColliderType::Solid => {
                    if let Some(push) = resolve_aabb_penetration(&player_aabb, &collider.bounds) {
                        player.position[0] += push[0];
                        player.position[1] += push[1];
                        player.position[2] += push[2];
                    }
                }
                ColliderType::Trigger => {
                    // Fire event, collect item, etc.
                }
            }
        }
    }
}
```

## Complete Physics Update Pattern

```rust
fn physics_update(game: &mut Game) {
    let dt = unsafe { delta_time() };

    for entity in &mut game.entities {
        // Apply forces
        apply_gravity(&mut entity.velocity, dt);

        // Integrate
        entity.position[0] += entity.velocity[0] * dt;
        entity.position[1] += entity.velocity[1] * dt;
        entity.position[2] += entity.velocity[2] * dt;

        // Collision detection and response
        let entity_aabb = AABB::new(entity.position, entity.half_extents);

        for wall in &game.walls {
            if entity_aabb.intersects(wall) {
                if let Some(push) = resolve_aabb_penetration(&entity_aabb, wall) {
                    entity.position[0] += push[0];
                    entity.position[1] += push[1];
                    entity.position[2] += push[2];

                    // Zero velocity on collision axis
                    if push[0].abs() > 0.001 { entity.velocity[0] = 0.0; }
                    if push[1].abs() > 0.001 { entity.velocity[1] = 0.0; }
                    if push[2].abs() > 0.001 { entity.velocity[2] = 0.0; }
                }
            }
        }

        // Apply friction if grounded
        if entity.grounded {
            apply_friction(&mut entity.velocity, GROUND_FRICTION, dt);
        } else {
            apply_friction(&mut entity.velocity, AIR_FRICTION, dt);
        }
    }
}
```

## Ground Detection

Use a short raycast to detect ground:

```rust
fn check_grounded(position: [f32; 3], feet_offset: f32, world: &[AABB]) -> bool {
    let ray = Ray {
        origin: position,
        direction: [0.0, -1.0, 0.0],
    };

    let ground_check_dist = feet_offset + 0.05; // Small margin

    for aabb in world {
        if let Some(t) = ray.intersect_aabb(aabb) {
            if t <= ground_check_dist {
                return true;
            }
        }
    }
    false
}
```

## Additional Resources

### Reference Files

For advanced collision techniques:
- **`references/advanced-collision.md`** — Capsule collision, swept tests, spatial partitioning

### Related Skills

- **multiplayer-design** — Determinism requirements, state serialization
- **perspective-patterns** — Camera collision for third-person games
