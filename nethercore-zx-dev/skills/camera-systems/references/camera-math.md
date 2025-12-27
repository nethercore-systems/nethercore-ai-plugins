# Camera Math Reference

Mathematical foundations for camera systems in Nethercore ZX.

## Interpolation Functions

### Linear Interpolation (Lerp)

Smoothly blend between two values:

```rust
/// Linear interpolation between a and b
/// t=0 returns a, t=1 returns b
fn lerp(a: f32, b: f32, t: f32) -> f32 {
    a + (b - a) * t
}

/// Lerp for 3D vectors
fn lerp_vec3(
    a: (f32, f32, f32),
    b: (f32, f32, f32),
    t: f32
) -> (f32, f32, f32) {
    (
        lerp(a.0, b.0, t),
        lerp(a.1, b.1, t),
        lerp(a.2, b.2, t),
    )
}
```

### Smooth Step

Ease-in-out interpolation for more natural movement:

```rust
/// Hermite smooth interpolation (ease-in-out)
fn smoothstep(t: f32) -> f32 {
    let t = t.clamp(0.0, 1.0);
    t * t * (3.0 - 2.0 * t)
}

/// Even smoother (quintic)
fn smootherstep(t: f32) -> f32 {
    let t = t.clamp(0.0, 1.0);
    t * t * t * (t * (t * 6.0 - 15.0) + 10.0)
}
```

### Frame-Rate Independent Smoothing

For smooth camera follow that works at any tick rate:

```rust
/// Exponential smoothing that's frame-rate independent
/// decay: higher = faster (try 5.0-15.0)
fn smooth_damp(current: f32, target: f32, decay: f32, dt: f32) -> f32 {
    let t = 1.0 - (-decay * dt).exp();
    lerp(current, target, t)
}
```

This is better than `lerp(a, b, decay * dt)` because it converges correctly regardless of frame rate.

## Spherical Linear Interpolation (Slerp)

For smooth rotation interpolation:

```rust
/// Slerp between two direction vectors
fn slerp_direction(
    a: (f32, f32, f32),
    b: (f32, f32, f32),
    t: f32
) -> (f32, f32, f32) {
    let dot = a.0*b.0 + a.1*b.1 + a.2*b.2;
    let dot = dot.clamp(-1.0, 1.0);

    let theta = dot.acos();
    if theta.abs() < 0.0001 {
        return lerp_vec3(a, b, t);
    }

    let sin_theta = theta.sin();
    let s0 = ((1.0 - t) * theta).sin() / sin_theta;
    let s1 = (t * theta).sin() / sin_theta;

    (
        a.0 * s0 + b.0 * s1,
        a.1 * s0 + b.1 * s1,
        a.2 * s0 + b.2 * s1,
    )
}
```

## Vector Operations

```rust
fn vec3_add(a: (f32, f32, f32), b: (f32, f32, f32)) -> (f32, f32, f32) {
    (a.0 + b.0, a.1 + b.1, a.2 + b.2)
}

fn vec3_sub(a: (f32, f32, f32), b: (f32, f32, f32)) -> (f32, f32, f32) {
    (a.0 - b.0, a.1 - b.1, a.2 - b.2)
}

fn vec3_scale(v: (f32, f32, f32), s: f32) -> (f32, f32, f32) {
    (v.0 * s, v.1 * s, v.2 * s)
}

fn vec3_length(v: (f32, f32, f32)) -> f32 {
    (v.0*v.0 + v.1*v.1 + v.2*v.2).sqrt()
}

fn vec3_normalize(v: (f32, f32, f32)) -> (f32, f32, f32) {
    let len = vec3_length(v);
    if len > 0.0001 {
        vec3_scale(v, 1.0 / len)
    } else {
        (0.0, 0.0, 1.0) // Default forward
    }
}

fn vec3_dot(a: (f32, f32, f32), b: (f32, f32, f32)) -> f32 {
    a.0*b.0 + a.1*b.1 + a.2*b.2
}

fn vec3_cross(a: (f32, f32, f32), b: (f32, f32, f32)) -> (f32, f32, f32) {
    (
        a.1*b.2 - a.2*b.1,
        a.2*b.0 - a.0*b.2,
        a.0*b.1 - a.1*b.0,
    )
}
```

## Look-At View Matrix

Construct a view matrix for `push_view_matrix()`:

```rust
/// Create view matrix (column-major order)
/// eye: camera position
/// target: point to look at
/// up: world up vector (typically 0, 1, 0)
fn look_at(
    eye: (f32, f32, f32),
    target: (f32, f32, f32),
    up: (f32, f32, f32)
) -> [f32; 16] {
    // Forward direction (from eye to target, then negated for view space)
    let f = vec3_normalize(vec3_sub(target, eye));

    // Right direction
    let r = vec3_normalize(vec3_cross(f, up));

    // Recalculate up to ensure orthogonal
    let u = vec3_cross(r, f);

    // Translation in view space
    let tx = -vec3_dot(r, eye);
    let ty = -vec3_dot(u, eye);
    let tz = vec3_dot(f, eye);  // Note: positive because we negate forward

    // Column-major layout
    [
        r.0,  u.0,  -f.0, 0.0,  // Column 0
        r.1,  u.1,  -f.1, 0.0,  // Column 1
        r.2,  u.2,  -f.2, 0.0,  // Column 2
        tx,   ty,   tz,   1.0,  // Column 3
    ]
}
```

Usage:
```rust
let view = look_at(cam_pos, target_pos, (0.0, 1.0, 0.0));
push_view_matrix(
    view[0], view[1], view[2], view[3],
    view[4], view[5], view[6], view[7],
    view[8], view[9], view[10], view[11],
    view[12], view[13], view[14], view[15],
);
```

## Camera Collision Detection

### Sphere-Box Collision

Simple check for camera against axis-aligned bounding boxes:

```rust
struct AABB {
    min: (f32, f32, f32),
    max: (f32, f32, f32),
}

fn sphere_aabb_collision(
    sphere_center: (f32, f32, f32),
    sphere_radius: f32,
    aabb: &AABB
) -> bool {
    // Find closest point on AABB to sphere center
    let closest = (
        sphere_center.0.clamp(aabb.min.0, aabb.max.0),
        sphere_center.1.clamp(aabb.min.1, aabb.max.1),
        sphere_center.2.clamp(aabb.min.2, aabb.max.2),
    );

    // Check if closest point is within sphere
    let dist = vec3_length(vec3_sub(sphere_center, closest));
    dist < sphere_radius
}
```

### Ray-AABB Intersection

For camera collision raycasting:

```rust
/// Returns distance to intersection, or None if no hit
fn ray_aabb_intersection(
    ray_origin: (f32, f32, f32),
    ray_dir: (f32, f32, f32),  // Must be normalized
    aabb: &AABB
) -> Option<f32> {
    let inv_dir = (
        1.0 / ray_dir.0,
        1.0 / ray_dir.1,
        1.0 / ray_dir.2,
    );

    let t1 = (aabb.min.0 - ray_origin.0) * inv_dir.0;
    let t2 = (aabb.max.0 - ray_origin.0) * inv_dir.0;
    let t3 = (aabb.min.1 - ray_origin.1) * inv_dir.1;
    let t4 = (aabb.max.1 - ray_origin.1) * inv_dir.1;
    let t5 = (aabb.min.2 - ray_origin.2) * inv_dir.2;
    let t6 = (aabb.max.2 - ray_origin.2) * inv_dir.2;

    let tmin = t1.min(t2).max(t3.min(t4)).max(t5.min(t6));
    let tmax = t1.max(t2).min(t3.max(t4)).min(t5.max(t6));

    if tmax < 0.0 || tmin > tmax {
        None
    } else if tmin < 0.0 {
        Some(tmax)
    } else {
        Some(tmin)
    }
}
```

### Camera Pull-In

Move camera forward when it would clip through geometry:

```rust
fn apply_camera_collision(
    target: (f32, f32, f32),
    ideal_cam_pos: (f32, f32, f32),
    obstacles: &[AABB],
    cam_radius: f32
) -> (f32, f32, f32) {
    let dir = vec3_sub(ideal_cam_pos, target);
    let dist = vec3_length(dir);
    let ray_dir = vec3_normalize(dir);

    let mut closest_hit = dist;

    for aabb in obstacles {
        if let Some(t) = ray_aabb_intersection(target, ray_dir, aabb) {
            if t < closest_hit {
                closest_hit = t - cam_radius; // Pull back by radius
            }
        }
    }

    // Minimum distance to prevent going inside target
    closest_hit = closest_hit.max(cam_radius * 2.0);

    vec3_add(target, vec3_scale(ray_dir, closest_hit))
}
```

## Angle Conversion

```rust
fn degrees_to_radians(deg: f32) -> f32 {
    deg * core::f32::consts::PI / 180.0
}

fn radians_to_degrees(rad: f32) -> f32 {
    rad * 180.0 / core::f32::consts::PI
}
```

## Spherical Coordinates

Convert between spherical (yaw/pitch/distance) and Cartesian:

```rust
/// Convert spherical to Cartesian position
/// yaw: horizontal angle in degrees (0 = +Z, 90 = +X)
/// pitch: vertical angle in degrees (0 = horizontal, 90 = up)
/// distance: radius from center
fn spherical_to_cartesian(
    yaw_deg: f32,
    pitch_deg: f32,
    distance: f32
) -> (f32, f32, f32) {
    let yaw = degrees_to_radians(yaw_deg);
    let pitch = degrees_to_radians(pitch_deg);

    let x = distance * yaw.sin() * pitch.cos();
    let y = distance * pitch.sin();
    let z = distance * yaw.cos() * pitch.cos();

    (x, y, z)
}

/// Convert Cartesian to spherical (yaw, pitch, distance)
fn cartesian_to_spherical(pos: (f32, f32, f32)) -> (f32, f32, f32) {
    let dist = vec3_length(pos);
    if dist < 0.0001 {
        return (0.0, 0.0, 0.0);
    }

    let pitch = (pos.1 / dist).asin();
    let yaw = pos.0.atan2(pos.2);

    (
        radians_to_degrees(yaw),
        radians_to_degrees(pitch),
        dist,
    )
}
```

## Quaternion Basics

For smooth 3D rotations (optional, more complex):

```rust
type Quat = (f32, f32, f32, f32); // (x, y, z, w)

fn quat_identity() -> Quat {
    (0.0, 0.0, 0.0, 1.0)
}

fn quat_from_axis_angle(axis: (f32, f32, f32), angle_deg: f32) -> Quat {
    let half = degrees_to_radians(angle_deg) * 0.5;
    let s = half.sin();
    (axis.0 * s, axis.1 * s, axis.2 * s, half.cos())
}

fn quat_slerp(a: Quat, b: Quat, t: f32) -> Quat {
    let dot = a.0*b.0 + a.1*b.1 + a.2*b.2 + a.3*b.3;

    // If dot < 0, negate one quaternion to take shorter path
    let (b, dot) = if dot < 0.0 {
        ((-b.0, -b.1, -b.2, -b.3), -dot)
    } else {
        (b, dot)
    };

    if dot > 0.9995 {
        // Linear interpolation for nearly identical quaternions
        let result = (
            lerp(a.0, b.0, t),
            lerp(a.1, b.1, t),
            lerp(a.2, b.2, t),
            lerp(a.3, b.3, t),
        );
        return quat_normalize(result);
    }

    let theta = dot.acos();
    let sin_theta = theta.sin();
    let s0 = ((1.0 - t) * theta).sin() / sin_theta;
    let s1 = (t * theta).sin() / sin_theta;

    (
        a.0 * s0 + b.0 * s1,
        a.1 * s0 + b.1 * s1,
        a.2 * s0 + b.2 * s1,
        a.3 * s0 + b.3 * s1,
    )
}

fn quat_normalize(q: Quat) -> Quat {
    let len = (q.0*q.0 + q.1*q.1 + q.2*q.2 + q.3*q.3).sqrt();
    (q.0/len, q.1/len, q.2/len, q.3/len)
}
```

## Constants

```rust
mod constants {
    pub const PI: f32 = 3.14159265359;
    pub const TAU: f32 = 6.28318530718;
    pub const DEG_TO_RAD: f32 = PI / 180.0;
    pub const RAD_TO_DEG: f32 = 180.0 / PI;
}
```

## Notes

- All matrices use **column-major** order for `push_view_matrix()` and `push_projection_matrix()`
- Nethercore uses **Y-up, right-handed** coordinate system
- Angles in FFI functions use **degrees** (convert to radians for trig)
- Use `random_f32()` for shake effects to maintain rollback safety
