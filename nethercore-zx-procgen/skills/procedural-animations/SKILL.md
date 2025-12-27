---
name: Procedural Animation Generation
description: This skill should be used when the user asks to "generate animation", "create walk cycle", "procedural walk", "idle animation", "attack animation", "procedural motion", "animate mesh", "run cycle", "jump animation", "locomotion", "animation blending", "animation state machine", "tree sway", "vehicle suspension", "robot animation", "rigid body animation", "inverse kinematics", "IK system", "foot placement", "look-at", or mentions motion generation, animation clips, keyframe generation, character locomotion, or procedural movement. Provides comprehensive guidance for generating procedural motion including locomotion, organic motion, mechanical animation, and IK systems.
version: 2.0.0
---

# Procedural Animation Generation

## Overview

Procedural animations enable infinite variation, runtime responsiveness, and reduced asset size. This skill covers **motion generation** - creating animation data that drives rigged characters and objects.

**This skill covers:**
- Locomotion (walk, run, jump cycles)
- Organic motion (tree sway, breathing, tail physics)
- Mechanical animation (vehicles, robots)
- Inverse kinematics (foot placement, look-at)
- Animation state machines and blending

**For skeleton creation and bone weights, see the `skeletal-rigging` skill.**

## ZX Animation System

ZX supports three animation paradigms:

| Type | Use Case | ZX API |
|------|----------|--------|
| **Transform-based** | Simple oscillations, rotations | `push_translate`, `push_rotate_*`, `push_scale` |
| **Skeletal** | Characters, creatures | `set_bones()` with 3x4 matrices |
| **Rigid Body** | Vehicles, robots | Hierarchical transforms |

### Bone Matrix Format

```rust
// Each bone: 3x4 matrix (12 floats, column-major)
// [col0.x, col0.y, col0.z]  // X axis
// [col1.x, col1.y, col1.z]  // Y axis
// [col2.x, col2.y, col2.z]  // Z axis
// [tx,     ty,     tz    ]  // translation
```

### Runtime Animation

```rust
// In render()
skeleton_bind(skeleton_handle);
let bone_transforms = calculate_animation(elapsed_time());
set_bones(bone_transforms.as_ptr(), bone_count);
draw_mesh(skinned_mesh);
```

## Locomotion Generation

### Procedural Walk Cycle

```rust
fn procedural_walk_pose(time: f32, speed: f32) -> BonePose {
    let cycle = (time * speed) % 1.0;
    let phase = cycle * 2.0 * PI;

    BonePose {
        // Vertical bob - two peaks per cycle
        hip_height: 0.02 * (phase * 2.0).sin().abs(),

        // Leg swing - 180° out of phase
        left_thigh: 30.0_f32.to_radians() * phase.sin(),
        right_thigh: 30.0_f32.to_radians() * (phase + PI).sin(),

        // Knee bend - only when leg swinging forward
        left_shin: 45.0_f32.to_radians() * (phase + FRAC_PI_2).sin().max(0.0),
        right_shin: 45.0_f32.to_radians() * (phase + PI + FRAC_PI_2).sin().max(0.0),

        // Counter-rotation
        spine_twist: 5.0_f32.to_radians() * phase.sin(),
        arm_swing: 20.0_f32.to_radians(),
    }
}
```

### Run Cycle (Faster, More Extreme)

```rust
fn procedural_run_pose(time: f32, speed: f32) -> BonePose {
    let cycle = (time * speed * 1.8) % 1.0;  // Faster cycle
    let phase = cycle * 2.0 * PI;

    BonePose {
        hip_height: 0.05 * (phase * 2.0).sin().abs(),  // Higher bob
        left_thigh: 50.0_f32.to_radians() * phase.sin(),
        right_thigh: 50.0_f32.to_radians() * (phase + PI).sin(),
        left_shin: 80.0_f32.to_radians() * (phase + FRAC_PI_2).sin().max(0.0),
        right_shin: 80.0_f32.to_radians() * (phase + PI + FRAC_PI_2).sin().max(0.0),
        spine_twist: 8.0_f32.to_radians() * phase.sin(),
        arm_swing: 40.0_f32.to_radians(),
        forward_lean: 15.0_f32.to_radians(),  // Lean into run
    }
}
```

### Quadruped Locomotion

```rust
fn quadruped_walk(time: f32, speed: f32) -> QuadPose {
    let phase = (time * speed) % 1.0 * 2.0 * PI;

    // Diagonal pairs move together
    // Front-left + Back-right, then Front-right + Back-left
    QuadPose {
        front_left: leg_swing(phase),
        back_right: leg_swing(phase),
        front_right: leg_swing(phase + PI),
        back_left: leg_swing(phase + PI),
        spine_flex: 5.0_f32.to_radians() * (phase * 2.0).sin(),
    }
}

fn leg_swing(phase: f32) -> LegPose {
    LegPose {
        thigh: 25.0_f32.to_radians() * phase.sin(),
        shin: 30.0_f32.to_radians() * (phase + FRAC_PI_2).sin().max(0.0),
    }
}
```

## Organic Motion

### Tree/Plant Sway

```rust
fn tree_sway(time: f32, wind_strength: f32, height_factor: f32) -> f32 {
    // Multi-frequency for natural motion
    let base = (time * 0.5).sin() * wind_strength;
    let detail = (time * 1.7).sin() * wind_strength * 0.3;
    let micro = (time * 4.3).sin() * wind_strength * 0.1;

    // More sway at top of tree
    (base + detail + micro) * height_factor
}
```

### Breathing/Idle

```rust
fn idle_breathing(time: f32) -> IdlePose {
    let breath_cycle = (time * 0.4).sin();  // ~2.5 second cycle

    IdlePose {
        chest_scale: 1.0 + breath_cycle * 0.02,
        shoulder_rise: breath_cycle * 0.01,
        subtle_sway: (time * 0.2).sin() * 0.005,
    }
}
```

### Tail/Rope Physics

```rust
fn update_chain_physics(
    nodes: &mut [Vec3],
    target: Vec3,
    segment_length: f32,
    damping: f32,
    velocities: &mut [Vec3],
    dt: f32,
) {
    // Follow the leader with physics
    nodes[0] = target;

    for i in 1..nodes.len() {
        // Spring force toward parent
        let to_parent = nodes[i - 1] - nodes[i];
        let current_dist = to_parent.length();
        let stretch = current_dist - segment_length;

        let spring_force = to_parent.normalize_or_zero() * stretch * 50.0;
        let gravity = Vec3::new(0.0, -9.8, 0.0);

        velocities[i] += (spring_force + gravity) * dt;
        velocities[i] *= damping;
        nodes[i] += velocities[i] * dt;

        // Enforce segment length
        let dir = (nodes[i] - nodes[i - 1]).normalize_or_zero();
        nodes[i] = nodes[i - 1] + dir * segment_length;
    }
}
```

## Mechanical Animation

### Vehicle Suspension

```rust
fn vehicle_suspension(
    wheel_idx: usize,
    terrain_height: f32,
    rest_height: f32,
    spring_k: f32,
    damping: f32,
    velocity: &mut f32,
    dt: f32,
) -> f32 {
    let target = terrain_height;
    let current = rest_height;
    let diff = target - current;

    // Spring-damper system
    let spring_force = diff * spring_k;
    *velocity += spring_force * dt;
    *velocity *= damping;

    rest_height + *velocity * dt
}
```

### Robot Joint Animation

```rust
fn robot_arm_reach(target: Vec3, shoulder: Vec3, arm_length: f32) -> (f32, f32) {
    let to_target = target - shoulder;
    let distance = to_target.length().min(arm_length * 0.95);

    // Simple 2-bone reach
    let shoulder_angle = to_target.y.atan2(to_target.x);
    let elbow_angle = ((distance / arm_length).acos() * 2.0 - PI).max(-PI);

    (shoulder_angle, elbow_angle)
}
```

### Wheel Rotation

```rust
fn wheel_rotation(distance_traveled: f32, wheel_radius: f32) -> f32 {
    let circumference = 2.0 * PI * wheel_radius;
    (distance_traveled / circumference) * 360.0_f32.to_radians()
}
```

## Inverse Kinematics

### Two-Bone IK (Limbs)

```rust
fn solve_two_bone_ik(
    root: Vec3,
    target: Vec3,
    bone1_len: f32,
    bone2_len: f32,
    pole_hint: Vec3,
) -> (Quat, Quat) {
    let chain_len = bone1_len + bone2_len;
    let to_target = target - root;
    let target_dist = to_target.length().min(chain_len * 0.999);

    // Law of cosines for elbow angle
    let cos_elbow = (bone1_len.powi(2) + bone2_len.powi(2) - target_dist.powi(2))
        / (2.0 * bone1_len * bone2_len);
    let elbow_angle = PI - cos_elbow.clamp(-1.0, 1.0).acos();

    // Shoulder angle
    let cos_shoulder = (bone1_len.powi(2) + target_dist.powi(2) - bone2_len.powi(2))
        / (2.0 * bone1_len * target_dist);
    let shoulder_offset = cos_shoulder.clamp(-1.0, 1.0).acos();

    // Calculate rotations using pole hint for twist
    let aim_dir = to_target.normalize();
    let shoulder_rot = Quat::from_rotation_arc(Vec3::Y, aim_dir)
        * Quat::from_axis_angle(aim_dir, shoulder_offset);
    let elbow_rot = Quat::from_axis_angle(Vec3::X, -elbow_angle);

    (shoulder_rot, elbow_rot)
}
```

### Foot Placement IK

```rust
fn foot_ik(
    leg_root: Vec3,
    current_foot: Vec3,
    ground_height: f32,
    leg_length: f32,
) -> Option<Vec3> {
    // Cast ray down from hip to find ground
    let foot_target = Vec3::new(current_foot.x, ground_height, current_foot.z);

    // Check if reachable
    let dist = (foot_target - leg_root).length();
    if dist > leg_length * 0.98 {
        return None;  // Too far, can't reach
    }

    Some(foot_target)
}
```

### Look-At

```rust
fn look_at_rotation(head_pos: Vec3, target: Vec3, up: Vec3) -> Quat {
    let forward = (target - head_pos).normalize();
    let right = up.cross(forward).normalize();
    let corrected_up = forward.cross(right);

    Quat::from_mat3(&Mat3::from_cols(right, corrected_up, forward))
}
```

## Animation State Machines

### Basic State Machine

```rust
#[derive(Clone, Copy, PartialEq)]
enum AnimState { Idle, Walk, Run, Jump, Attack }

struct AnimController {
    current: AnimState,
    target: AnimState,
    blend_time: f32,
    blend_progress: f32,
    state_time: f32,
}

impl AnimController {
    fn update(&mut self, input: &Input, dt: f32) {
        // Determine target state from input
        let new_target = if input.attack_pressed {
            AnimState::Attack
        } else if !input.grounded {
            AnimState::Jump
        } else if input.move_speed > 0.7 {
            AnimState::Run
        } else if input.move_speed > 0.1 {
            AnimState::Walk
        } else {
            AnimState::Idle
        };

        // Start transition if target changed
        if new_target != self.target && self.blend_progress >= 1.0 {
            self.target = new_target;
            self.blend_progress = 0.0;
        }

        // Update blend
        self.blend_progress = (self.blend_progress + dt / self.blend_time).min(1.0);
        self.state_time += dt;

        // Snap to target when blend complete
        if self.blend_progress >= 1.0 && self.current != self.target {
            self.current = self.target;
            self.state_time = 0.0;
        }
    }

    fn sample(&self) -> BonePose {
        let from_pose = self.sample_state(self.current);
        let to_pose = self.sample_state(self.target);

        // Smooth blend using smoothstep
        let t = smoothstep(self.blend_progress);
        blend_poses(&from_pose, &to_pose, t)
    }
}

fn smoothstep(t: f32) -> f32 {
    t * t * (3.0 - 2.0 * t)
}
```

### Animation Blending

```rust
fn blend_poses(from: &BonePose, to: &BonePose, t: f32) -> BonePose {
    BonePose {
        hip_height: lerp(from.hip_height, to.hip_height, t),
        left_thigh: lerp(from.left_thigh, to.left_thigh, t),
        right_thigh: lerp(from.right_thigh, to.right_thigh, t),
        // ... blend all bone values
    }
}

fn lerp(a: f32, b: f32, t: f32) -> f32 {
    a + (b - a) * t
}

fn blend_bone_matrices(
    from: &[[f32; 12]],
    to: &[[f32; 12]],
    t: f32,
) -> Vec<[f32; 12]> {
    from.iter().zip(to.iter())
        .map(|(f, to_mat)| {
            let mut result = [0.0; 12];
            for i in 0..12 {
                result[i] = f[i] + (to_mat[i] - f[i]) * t;
            }
            result
        })
        .collect()
}
```

## Common Animation Recipes

### Weapon Bob (First Person)

```rust
fn weapon_bob(time: f32, move_speed: f32) -> (Vec3, Quat) {
    let bob_freq = move_speed * 8.0;
    let bob_amp = move_speed * 0.02;

    let offset = Vec3::new(
        (time * bob_freq).sin() * bob_amp * 0.5,
        (time * bob_freq * 2.0).sin().abs() * bob_amp,
        0.0,
    );

    let tilt = Quat::from_euler(
        EulerRot::XYZ,
        (time * bob_freq * 2.0).sin() * 0.01,
        0.0,
        (time * bob_freq).sin() * 0.02,
    );

    (offset, tilt)
}
```

### Screen Shake

```rust
fn screen_shake(time: f32, intensity: f32, decay: f32) -> Vec3 {
    let t = time * decay;
    let remaining = (-t).exp();

    Vec3::new(
        (t * 50.0).sin() * remaining * intensity,
        (t * 43.0).cos() * remaining * intensity * 0.7,
        0.0,
    )
}
```

### Hover/Float

```rust
fn hover_motion(time: f32, amplitude: f32) -> f32 {
    (time * 2.0).sin() * amplitude
}
```

## Export Formats

| Format | Support | Notes |
|--------|---------|-------|
| **GLTF/GLB** | Full | Animations + skeleton |
| **Custom Binary** | Keyframes | Most efficient for procgen |
| **Runtime** | N/A | Generate in `update()` |

### Binary Keyframe Export

```rust
fn export_animation_binary(
    keyframes: &[Keyframe],
    path: &str,
) -> std::io::Result<()> {
    let mut file = File::create(path)?;

    // Header
    file.write_all(&(keyframes.len() as u32).to_le_bytes())?;

    for kf in keyframes {
        file.write_all(&kf.time.to_le_bytes())?;
        file.write_all(&(kf.bone_index as u16).to_le_bytes())?;
        // Rotation quaternion
        for v in &kf.rotation {
            file.write_all(&v.to_le_bytes())?;
        }
        // Translation
        for v in &kf.translation {
            file.write_all(&v.to_le_bytes())?;
        }
    }

    Ok(())
}
```

## nether.toml Configuration

```toml
[[assets.animations]]
id = "walk"
path = "assets/animations/walk.gltf"

[[assets.animations]]
id = "run"
path = "assets/animations/run.gltf"

[[assets.animations]]
id = "attack"
path = "assets/animations/attack.bin"
```

## Additional Resources

### Reference Files

For detailed implementations:
- **`references/animation-presets.md`** - Common animation parameters
- **`references/ik-systems.md`** - Advanced IK implementations
- **`references/rigid-body-animation.md`** - Vehicle/robot patterns

### Related Skills

- **`skeletal-rigging`** - Skeleton creation, bone weights
- **`character-pipeline`** - Full character workflow
- **`mocap-integration`** - Using motion capture data
