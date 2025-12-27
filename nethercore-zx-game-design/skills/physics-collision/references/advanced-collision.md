# Advanced Collision Techniques

Extended collision algorithms for complex game requirements.

## Capsule Collision

Capsules (pill shapes) are ideal for character collision — they handle stairs/slopes smoothly and don't get stuck on corners.

### Capsule Definition

A capsule is defined by two endpoints (the line segment axis) and a radius:

```rust
struct Capsule {
    base: [f32; 3],   // Bottom sphere center
    tip: [f32; 3],    // Top sphere center
    radius: f32,
}

impl Capsule {
    /// Create a vertical capsule from center position
    fn vertical(center: [f32; 3], height: f32, radius: f32) -> Self {
        let half_height = (height - 2.0 * radius).max(0.0) * 0.5;
        Self {
            base: [center[0], center[1] - half_height, center[2]],
            tip: [center[0], center[1] + half_height, center[2]],
            radius,
        }
    }
}
```

### Capsule vs Point

Find the closest point on the capsule's axis to the test point:

```rust
fn closest_point_on_segment(a: [f32; 3], b: [f32; 3], p: [f32; 3]) -> [f32; 3] {
    let ab = [b[0] - a[0], b[1] - a[1], b[2] - a[2]];
    let ap = [p[0] - a[0], p[1] - a[1], p[2] - a[2]];

    let ab_dot_ab = ab[0] * ab[0] + ab[1] * ab[1] + ab[2] * ab[2];
    if ab_dot_ab < 1e-8 { return a; } // Degenerate segment

    let t = (ap[0] * ab[0] + ap[1] * ab[1] + ap[2] * ab[2]) / ab_dot_ab;
    let t = t.clamp(0.0, 1.0);

    [a[0] + t * ab[0], a[1] + t * ab[1], a[2] + t * ab[2]]
}

impl Capsule {
    fn contains_point(&self, p: [f32; 3]) -> bool {
        let closest = closest_point_on_segment(self.base, self.tip, p);
        let dx = p[0] - closest[0];
        let dy = p[1] - closest[1];
        let dz = p[2] - closest[2];
        dx * dx + dy * dy + dz * dz <= self.radius * self.radius
    }
}
```

### Capsule vs Capsule

Find closest points between two line segments, then check sphere overlap:

```rust
fn closest_points_segments(
    a1: [f32; 3], a2: [f32; 3],
    b1: [f32; 3], b2: [f32; 3]
) -> ([f32; 3], [f32; 3]) {
    let d1 = [a2[0] - a1[0], a2[1] - a1[1], a2[2] - a1[2]];
    let d2 = [b2[0] - b1[0], b2[1] - b1[1], b2[2] - b1[2]];
    let r = [a1[0] - b1[0], a1[1] - b1[1], a1[2] - b1[2]];

    let a = d1[0] * d1[0] + d1[1] * d1[1] + d1[2] * d1[2];
    let e = d2[0] * d2[0] + d2[1] * d2[1] + d2[2] * d2[2];
    let f = d2[0] * r[0] + d2[1] * r[1] + d2[2] * r[2];

    let (s, t) = if a < 1e-8 && e < 1e-8 {
        (0.0, 0.0)
    } else if a < 1e-8 {
        (0.0, (f / e).clamp(0.0, 1.0))
    } else {
        let c = d1[0] * r[0] + d1[1] * r[1] + d1[2] * r[2];
        if e < 1e-8 {
            ((-c / a).clamp(0.0, 1.0), 0.0)
        } else {
            let b = d1[0] * d2[0] + d1[1] * d2[1] + d1[2] * d2[2];
            let denom = a * e - b * b;

            let s = if denom.abs() > 1e-8 {
                ((b * f - c * e) / denom).clamp(0.0, 1.0)
            } else {
                0.0
            };

            let t_num = b * s + f;
            let t = if t_num < 0.0 {
                let s = (-c / a).clamp(0.0, 1.0);
                (s, 0.0).0
            } else if t_num > e {
                let s = ((b - c) / a).clamp(0.0, 1.0);
                (s, 1.0).0
            } else {
                t_num / e
            };

            (s, t)
        }
    };

    let p1 = [a1[0] + s * d1[0], a1[1] + s * d1[1], a1[2] + s * d1[2]];
    let p2 = [b1[0] + t * d2[0], b1[1] + t * d2[1], b1[2] + t * d2[2]];
    (p1, p2)
}

impl Capsule {
    fn intersects_capsule(&self, other: &Capsule) -> bool {
        let (p1, p2) = closest_points_segments(self.base, self.tip, other.base, other.tip);
        let dx = p1[0] - p2[0];
        let dy = p1[1] - p2[1];
        let dz = p1[2] - p2[2];
        let dist_sq = dx * dx + dy * dy + dz * dz;
        let radii_sum = self.radius + other.radius;
        dist_sq <= radii_sum * radii_sum
    }
}
```

### Capsule vs AABB

Expand the AABB by capsule radius, then check segment intersection:

```rust
impl Capsule {
    fn intersects_aabb(&self, aabb: &AABB) -> bool {
        // Expand AABB by capsule radius
        let expanded = AABB {
            min: [
                aabb.min[0] - self.radius,
                aabb.min[1] - self.radius,
                aabb.min[2] - self.radius,
            ],
            max: [
                aabb.max[0] + self.radius,
                aabb.max[1] + self.radius,
                aabb.max[2] + self.radius,
            ],
        };

        // Check if segment intersects expanded AABB
        // (simplified: check endpoints and midpoint)
        let mid = [
            (self.base[0] + self.tip[0]) * 0.5,
            (self.base[1] + self.tip[1]) * 0.5,
            (self.base[2] + self.tip[2]) * 0.5,
        ];

        expanded.contains_point(self.base) ||
        expanded.contains_point(self.tip) ||
        expanded.contains_point(mid)
    }
}
```

## Swept Collision (Continuous Detection)

Prevents fast-moving objects from tunneling through thin walls.

### Swept AABB vs AABB

```rust
struct SweptResult {
    t: f32,           // Time of collision (0.0 to 1.0)
    normal: [f32; 3], // Collision normal
}

fn swept_aabb(
    moving: &AABB,
    velocity: [f32; 3],
    static_box: &AABB
) -> Option<SweptResult> {
    let mut t_entry = [f32::NEG_INFINITY; 3];
    let mut t_exit = [f32::INFINITY; 3];

    for i in 0..3 {
        if velocity[i].abs() < 1e-8 {
            // Not moving on this axis
            if moving.max[i] < static_box.min[i] || moving.min[i] > static_box.max[i] {
                return None; // No overlap and not moving toward it
            }
        } else {
            let inv_v = 1.0 / velocity[i];
            let mut t1 = (static_box.min[i] - moving.max[i]) * inv_v;
            let mut t2 = (static_box.max[i] - moving.min[i]) * inv_v;
            if t1 > t2 { core::mem::swap(&mut t1, &mut t2); }
            t_entry[i] = t1;
            t_exit[i] = t2;
        }
    }

    let entry_time = t_entry[0].max(t_entry[1]).max(t_entry[2]);
    let exit_time = t_exit[0].min(t_exit[1]).min(t_exit[2]);

    // No collision if entry is after exit, or collision is behind us, or too far ahead
    if entry_time > exit_time || entry_time < 0.0 || entry_time > 1.0 {
        return None;
    }

    // Determine collision normal (axis with latest entry time)
    let normal = if t_entry[0] >= t_entry[1] && t_entry[0] >= t_entry[2] {
        if velocity[0] > 0.0 { [-1.0, 0.0, 0.0] } else { [1.0, 0.0, 0.0] }
    } else if t_entry[1] >= t_entry[2] {
        if velocity[1] > 0.0 { [0.0, -1.0, 0.0] } else { [0.0, 1.0, 0.0] }
    } else {
        if velocity[2] > 0.0 { [0.0, 0.0, -1.0] } else { [0.0, 0.0, 1.0] }
    };

    Some(SweptResult { t: entry_time, normal })
}
```

### Using Swept Collision

```rust
fn move_with_sweep(
    entity: &mut Entity,
    velocity: [f32; 3],
    walls: &[AABB],
    dt: f32
) {
    let entity_aabb = AABB::new(entity.position, entity.half_extents);
    let frame_velocity = [velocity[0] * dt, velocity[1] * dt, velocity[2] * dt];

    let mut remaining_time = 1.0;
    let mut current_velocity = frame_velocity;

    for _ in 0..3 { // Max 3 iterations (corner case)
        let mut earliest_hit: Option<SweptResult> = None;

        for wall in walls {
            if let Some(hit) = swept_aabb(&entity_aabb, current_velocity, wall) {
                if earliest_hit.is_none() || hit.t < earliest_hit.as_ref().unwrap().t {
                    earliest_hit = Some(hit);
                }
            }
        }

        match earliest_hit {
            Some(hit) => {
                // Move to collision point (minus small epsilon)
                let move_t = (hit.t - 0.001).max(0.0);
                entity.position[0] += current_velocity[0] * move_t;
                entity.position[1] += current_velocity[1] * move_t;
                entity.position[2] += current_velocity[2] * move_t;

                // Slide remaining velocity
                remaining_time -= hit.t;
                if remaining_time <= 0.0 { break; }

                current_velocity = slide_velocity(
                    [
                        current_velocity[0] * remaining_time,
                        current_velocity[1] * remaining_time,
                        current_velocity[2] * remaining_time,
                    ],
                    hit.normal
                );
            }
            None => {
                // No collision, apply remaining velocity
                entity.position[0] += current_velocity[0];
                entity.position[1] += current_velocity[1];
                entity.position[2] += current_velocity[2];
                break;
            }
        }
    }
}
```

## Spatial Partitioning

For games with many colliders, use spatial partitioning to reduce checks.

### Grid-Based Broad Phase

Simple and effective for 2D or flat 3D games:

```rust
const CELL_SIZE: f32 = 4.0;
const GRID_WIDTH: usize = 64;
const GRID_HEIGHT: usize = 64;

struct SpatialGrid {
    cells: Vec<Vec<usize>>,  // Entity indices per cell
}

impl SpatialGrid {
    fn new() -> Self {
        Self {
            cells: vec![Vec::new(); GRID_WIDTH * GRID_HEIGHT],
        }
    }

    fn clear(&mut self) {
        for cell in &mut self.cells {
            cell.clear();
        }
    }

    fn cell_index(x: f32, z: f32) -> Option<usize> {
        let cx = ((x / CELL_SIZE) as isize + (GRID_WIDTH / 2) as isize) as usize;
        let cz = ((z / CELL_SIZE) as isize + (GRID_HEIGHT / 2) as isize) as usize;
        if cx < GRID_WIDTH && cz < GRID_HEIGHT {
            Some(cz * GRID_WIDTH + cx)
        } else {
            None
        }
    }

    fn insert(&mut self, entity_idx: usize, aabb: &AABB) {
        // Insert into all overlapping cells
        let min_cx = ((aabb.min[0] / CELL_SIZE).floor() as isize + (GRID_WIDTH / 2) as isize).max(0) as usize;
        let max_cx = ((aabb.max[0] / CELL_SIZE).floor() as isize + (GRID_WIDTH / 2) as isize).min(GRID_WIDTH as isize - 1) as usize;
        let min_cz = ((aabb.min[2] / CELL_SIZE).floor() as isize + (GRID_HEIGHT / 2) as isize).max(0) as usize;
        let max_cz = ((aabb.max[2] / CELL_SIZE).floor() as isize + (GRID_HEIGHT / 2) as isize).min(GRID_HEIGHT as isize - 1) as usize;

        for cz in min_cz..=max_cz {
            for cx in min_cx..=max_cx {
                self.cells[cz * GRID_WIDTH + cx].push(entity_idx);
            }
        }
    }

    fn query(&self, aabb: &AABB) -> impl Iterator<Item = usize> + '_ {
        let min_cx = ((aabb.min[0] / CELL_SIZE).floor() as isize + (GRID_WIDTH / 2) as isize).max(0) as usize;
        let max_cx = ((aabb.max[0] / CELL_SIZE).floor() as isize + (GRID_WIDTH / 2) as isize).min(GRID_WIDTH as isize - 1) as usize;
        let min_cz = ((aabb.min[2] / CELL_SIZE).floor() as isize + (GRID_HEIGHT / 2) as isize).max(0) as usize;
        let max_cz = ((aabb.max[2] / CELL_SIZE).floor() as isize + (GRID_HEIGHT / 2) as isize).min(GRID_HEIGHT as isize - 1) as usize;

        (min_cz..=max_cz)
            .flat_map(move |cz| (min_cx..=max_cx).map(move |cx| cz * GRID_WIDTH + cx))
            .flat_map(|idx| self.cells[idx].iter().copied())
    }
}
```

### Usage Pattern

```rust
fn physics_update_with_grid(game: &mut Game) {
    // Rebuild grid each frame (for dynamic objects)
    game.grid.clear();
    for (i, entity) in game.entities.iter().enumerate() {
        let aabb = AABB::new(entity.position, entity.half_extents);
        game.grid.insert(i, &aabb);
    }

    // Collision detection with spatial queries
    for i in 0..game.entities.len() {
        let entity_aabb = AABB::new(game.entities[i].position, game.entities[i].half_extents);

        for j in game.grid.query(&entity_aabb) {
            if i >= j { continue; } // Avoid duplicate pairs and self

            let other_aabb = AABB::new(game.entities[j].position, game.entities[j].half_extents);
            if entity_aabb.intersects(&other_aabb) {
                // Handle collision between i and j
            }
        }
    }
}
```

## Collision Layers and Masks

Filter which objects can collide with each other:

```rust
#[derive(Clone, Copy)]
struct CollisionFilter {
    layer: u32,    // This object belongs to these layers
    mask: u32,     // This object collides with these layers
}

impl CollisionFilter {
    const PLAYER: u32 = 1 << 0;
    const ENEMY: u32 = 1 << 1;
    const PROJECTILE: u32 = 1 << 2;
    const WORLD: u32 = 1 << 3;
    const TRIGGER: u32 = 1 << 4;

    fn can_collide(&self, other: &CollisionFilter) -> bool {
        (self.mask & other.layer) != 0 && (other.mask & self.layer) != 0
    }
}

// Example configurations:
// Player collides with world, enemies, triggers
// filter: { layer: PLAYER, mask: WORLD | ENEMY | TRIGGER }

// Enemy projectile collides with player and world only
// filter: { layer: PROJECTILE, mask: PLAYER | WORLD }
```

## Performance Tips

1. **Broad phase first**: Always use spatial partitioning or AABB tests before expensive checks
2. **Exit early**: Check bounding spheres before detailed collision
3. **Cache bounds**: Precompute AABBs when positions change, not every query
4. **Fixed-point math**: Consider fixed-point for critical physics if float determinism is a concern
5. **Limit iterations**: Cap physics substeps and collision resolution loops
