# Animation Presets and Templates

Ready-to-use procedural animation patterns for common game scenarios.

## Character Locomotion

### Bipedal Walk Cycle

Classic human/humanoid walk with proper weight shift:

```rust
use core::f32::consts::PI;

struct WalkParams {
    speed: f32,          // Cycles per second
    stride_length: f32,  // Forward movement per cycle
    hip_sway: f32,       // Side-to-side hip motion
    hip_bob: f32,        // Up-down bounce
    arm_swing: f32,      // Arm swing amplitude (degrees)
    spine_twist: f32,    // Counter-rotation (degrees)
}

impl Default for WalkParams {
    fn default() -> Self {
        Self {
            speed: 1.0,
            stride_length: 1.0,
            hip_sway: 0.02,
            hip_bob: 0.03,
            arm_swing: 25.0,
            spine_twist: 8.0,
        }
    }
}

fn bipedal_walk(time: f32, params: &WalkParams) -> CharacterPose {
    let cycle = (time * params.speed) % 1.0;
    let phase = cycle * 2.0 * PI;

    CharacterPose {
        // Root motion
        root_offset: Vec3::new(
            params.hip_sway * phase.sin(),
            params.hip_bob * (phase * 2.0).sin().abs(),
            0.0
        ),

        // Pelvis
        pelvis_tilt: 3.0 * phase.sin(),  // Side tilt during weight shift

        // Legs (opposite phase)
        left_thigh: 30.0 * phase.sin(),
        right_thigh: 30.0 * (phase + PI).sin(),
        left_shin: 45.0 * (phase + PI * 0.5).sin().max(0.0),
        right_shin: 45.0 * (phase + PI * 1.5).sin().max(0.0),
        left_foot: -10.0 * phase.cos(),  // Heel strike / toe push
        right_foot: -10.0 * (phase + PI).cos(),

        // Spine counter-rotation
        spine_twist: params.spine_twist * phase.sin(),
        spine_bend: 2.0,  // Slight forward lean

        // Arms (opposite to legs)
        left_shoulder: -params.arm_swing * phase.sin(),
        right_shoulder: -params.arm_swing * (phase + PI).sin(),
        left_elbow: 20.0 + 15.0 * (phase + PI * 0.5).sin().max(0.0),
        right_elbow: 20.0 + 15.0 * (phase + PI * 1.5).sin().max(0.0),

        // Head stabilization
        head_pitch: -2.0 * (phase * 2.0).sin(),
    }
}
```

### Bipedal Run

Higher energy motion with flight phase:

```rust
fn bipedal_run(time: f32, speed: f32) -> CharacterPose {
    let cycle = (time * speed * 1.5) % 1.0;  // Faster than walk
    let phase = cycle * 2.0 * PI;

    CharacterPose {
        // More pronounced bob (both feet off ground)
        root_offset: Vec3::new(
            0.01 * phase.sin(),
            0.08 * (phase * 2.0).sin().abs(),
            0.0
        ),

        // Greater leg extension
        left_thigh: 50.0 * phase.sin(),
        right_thigh: 50.0 * (phase + PI).sin(),
        left_shin: 80.0 * (phase + PI * 0.5).sin().max(0.0),
        right_shin: 80.0 * (phase + PI * 1.5).sin().max(0.0),

        // Forward lean
        spine_bend: 15.0,

        // Pumping arms
        left_shoulder: -50.0 * phase.sin(),
        right_shoulder: -50.0 * (phase + PI).sin(),
        left_elbow: 90.0,  // Arms bent at 90 degrees
        right_elbow: 90.0,

        ..Default::default()
    }
}
```

### Idle/Breathing

Subtle motion for standing characters:

```rust
fn idle_breathing(time: f32) -> CharacterPose {
    let breath_cycle = time * 0.3;  // Slow breathing
    let weight_shift = time * 0.1;  // Very slow weight shift

    CharacterPose {
        // Subtle chest expansion
        spine_scale: Vec3::new(
            1.0,
            1.0 + 0.02 * breath_cycle.sin(),
            1.0 + 0.015 * breath_cycle.sin()
        ),

        // Shoulders rise slightly with breath
        left_shoulder: 2.0 * breath_cycle.sin(),
        right_shoulder: 2.0 * breath_cycle.sin(),

        // Very subtle weight shift
        root_offset: Vec3::new(
            0.01 * weight_shift.sin(),
            0.0,
            0.0
        ),

        // Head micro-movements
        head_pitch: 1.0 * (time * 0.2).sin(),
        head_yaw: 2.0 * (time * 0.15).sin(),

        ..Default::default()
    }
}
```

### Jump

Three-phase jump animation:

```rust
enum JumpPhase { Anticipation, Airborne, Landing }

fn jump_animation(
    phase: JumpPhase,
    phase_progress: f32,  // 0-1 within phase
) -> CharacterPose {
    match phase {
        JumpPhase::Anticipation => {
            // Crouch down, prepare
            let t = ease_in_out_quad(phase_progress);
            CharacterPose {
                root_offset: Vec3::new(0.0, -0.3 * t, 0.0),
                left_thigh: -30.0 * t,
                right_thigh: -30.0 * t,
                left_shin: 60.0 * t,
                right_shin: 60.0 * t,
                spine_bend: -10.0 * t,
                left_shoulder: -20.0 * t,
                right_shoulder: -20.0 * t,
                ..Default::default()
            }
        }
        JumpPhase::Airborne => {
            // Extend, then tuck for landing
            let extend = if phase_progress < 0.5 {
                phase_progress * 2.0
            } else {
                1.0 - (phase_progress - 0.5) * 2.0
            };

            CharacterPose {
                left_thigh: 20.0 * extend - 20.0 * (1.0 - extend),
                right_thigh: 20.0 * extend - 20.0 * (1.0 - extend),
                left_shin: -10.0 * extend + 40.0 * (1.0 - extend),
                right_shin: -10.0 * extend + 40.0 * (1.0 - extend),
                left_shoulder: -30.0,
                right_shoulder: -30.0,
                left_elbow: 20.0,
                right_elbow: 20.0,
                spine_bend: 10.0 * extend,
                ..Default::default()
            }
        }
        JumpPhase::Landing => {
            // Impact absorption
            let t = ease_out_bounce(phase_progress);
            CharacterPose {
                root_offset: Vec3::new(0.0, -0.2 * (1.0 - t), 0.0),
                left_thigh: -20.0 * (1.0 - t),
                right_thigh: -20.0 * (1.0 - t),
                left_shin: 40.0 * (1.0 - t),
                right_shin: 40.0 * (1.0 - t),
                spine_bend: -5.0 * (1.0 - t),
                ..Default::default()
            }
        }
    }
}
```

### Attack Combo

Multi-hit attack sequence:

```rust
fn attack_combo(attack_index: usize, progress: f32) -> CharacterPose {
    match attack_index {
        0 => {
            // Quick jab
            let wind_up = (progress * 3.0).min(1.0);
            let strike = ((progress - 0.33) * 3.0).clamp(0.0, 1.0);
            let recover = ((progress - 0.66) * 3.0).clamp(0.0, 1.0);

            CharacterPose {
                right_shoulder: -30.0 * wind_up + 80.0 * strike - 50.0 * recover,
                right_elbow: 90.0 * wind_up - 70.0 * strike + 20.0 * recover,
                spine_twist: 20.0 * strike - 10.0 * recover,
                ..Default::default()
            }
        }
        1 => {
            // Wide slash
            let t = ease_in_out_quad(progress);
            CharacterPose {
                right_shoulder: -60.0 + 150.0 * t,
                right_elbow: 30.0,
                spine_twist: -30.0 + 60.0 * t,
                left_thigh: 10.0 * t,
                ..Default::default()
            }
        }
        2 => {
            // Overhead smash
            let wind = (progress * 2.0).min(1.0);
            let smash = ((progress - 0.5) * 2.0).clamp(0.0, 1.0);

            CharacterPose {
                right_shoulder: -120.0 * wind + 40.0 * smash,
                left_shoulder: -100.0 * wind + 30.0 * smash,
                spine_bend: -20.0 * wind + 30.0 * smash,
                left_thigh: -20.0 * smash,
                right_thigh: -20.0 * smash,
                ..Default::default()
            }
        }
        _ => CharacterPose::default(),
    }
}
```

## Quadruped Locomotion

### Four-Legged Walk

Alternating diagonal pairs:

```rust
fn quadruped_walk(time: f32, speed: f32) -> QuadrupedPose {
    let cycle = (time * speed) % 1.0;
    let phase = cycle * 2.0 * PI;

    // Diagonal pairs: FL+BR, FR+BL
    QuadrupedPose {
        // Body motion
        body_pitch: 3.0 * (phase * 2.0).sin(),
        body_roll: 2.0 * phase.sin(),

        // Front left + Back right
        front_left_shoulder: 25.0 * phase.sin(),
        front_left_elbow: 20.0 * (phase + PI * 0.5).sin().max(0.0),
        back_right_hip: 25.0 * phase.sin(),
        back_right_knee: 30.0 * (phase + PI * 0.5).sin().max(0.0),

        // Front right + Back left (opposite phase)
        front_right_shoulder: 25.0 * (phase + PI).sin(),
        front_right_elbow: 20.0 * (phase + PI * 1.5).sin().max(0.0),
        back_left_hip: 25.0 * (phase + PI).sin(),
        back_left_knee: 30.0 * (phase + PI * 1.5).sin().max(0.0),

        // Tail follows body
        tail_base: 10.0 * (phase + PI * 0.25).sin(),
        tail_mid: 15.0 * (phase + PI * 0.5).sin(),
        tail_tip: 20.0 * (phase + PI * 0.75).sin(),
    }
}
```

### Four-Legged Gallop

Full extension and contraction:

```rust
fn quadruped_gallop(time: f32, speed: f32) -> QuadrupedPose {
    let cycle = (time * speed * 2.0) % 1.0;
    let phase = cycle * 2.0 * PI;

    // Gallop: front legs together, back legs together
    let front_phase = phase;
    let back_phase = phase + PI * 0.5;  // Slight offset

    QuadrupedPose {
        // Spine flexion (bunny hop style)
        body_pitch: 15.0 * phase.sin(),

        // Front legs together
        front_left_shoulder: 40.0 * front_phase.sin(),
        front_right_shoulder: 40.0 * front_phase.sin(),
        front_left_elbow: 30.0 * (front_phase + PI * 0.3).sin().max(0.0),
        front_right_elbow: 30.0 * (front_phase + PI * 0.3).sin().max(0.0),

        // Back legs together (offset)
        back_left_hip: 50.0 * back_phase.sin(),
        back_right_hip: 50.0 * back_phase.sin(),
        back_left_knee: 40.0 * (back_phase + PI * 0.3).sin().max(0.0),
        back_right_knee: 40.0 * (back_phase + PI * 0.3).sin().max(0.0),

        ..Default::default()
    }
}
```

## Nature and Environment

### Tree Swaying

Multi-layer wind response:

```rust
fn tree_sway(time: f32, wind: WindParams) -> TreePose {
    // Base frequency varies with wind strength
    let base_freq = 0.3 + wind.strength * 0.2;

    // Primary sway (whole tree)
    let primary = (time * base_freq).sin() * wind.strength * 15.0;

    // Secondary (branches respond faster)
    let secondary = (time * base_freq * 2.3).sin() * wind.strength * 8.0;

    // Tertiary (leaves/twigs, high frequency)
    let tertiary = (time * base_freq * 5.7).sin() * wind.strength * 3.0;

    // Wind gusts (irregular)
    let gust = ((time * 0.7).sin() * (time * 1.3).cos()) * wind.gust_strength * 10.0;

    TreePose {
        trunk_bend: primary + gust * 0.3,
        branch_bend: primary * 0.7 + secondary + gust * 0.5,
        twig_bend: primary * 0.5 + secondary * 0.8 + tertiary + gust,
        leaf_flutter: tertiary * 2.0 + (time * 15.0).sin() * 5.0,

        // Direction follows wind
        bend_direction: wind.direction,
    }
}
```

### Water Surface

Procedural waves:

```rust
fn water_vertex_offset(
    position: Vec2,
    time: f32,
    wave_params: &[WaveParams],
) -> f32 {
    let mut height = 0.0;

    for wave in wave_params {
        let dot = position.x * wave.direction.x + position.y * wave.direction.y;
        height += wave.amplitude *
            (dot * wave.frequency + time * wave.speed).sin();
    }

    height
}

// Preset wave configurations
fn calm_water() -> Vec<WaveParams> {
    vec![
        WaveParams { amplitude: 0.02, frequency: 2.0, speed: 0.5, direction: Vec2::new(1.0, 0.0) },
        WaveParams { amplitude: 0.01, frequency: 4.0, speed: 0.8, direction: Vec2::new(0.7, 0.7) },
    ]
}

fn stormy_water() -> Vec<WaveParams> {
    vec![
        WaveParams { amplitude: 0.3, frequency: 1.0, speed: 2.0, direction: Vec2::new(1.0, 0.0) },
        WaveParams { amplitude: 0.15, frequency: 2.0, speed: 2.5, direction: Vec2::new(0.8, 0.6) },
        WaveParams { amplitude: 0.1, frequency: 4.0, speed: 3.0, direction: Vec2::new(0.5, 0.866) },
        WaveParams { amplitude: 0.05, frequency: 8.0, speed: 4.0, direction: Vec2::new(-0.3, 0.95) },
    ]
}
```

### Grass Field

Wind-responsive grass:

```rust
fn grass_blade_bend(
    blade_base: Vec3,
    time: f32,
    wind_strength: f32,
    wind_direction: Vec2,
) -> f32 {
    // Spatial variation (different blades move differently)
    let spatial_offset = blade_base.x * 0.3 + blade_base.z * 0.5;

    // Primary wave
    let primary = (time * 2.0 + spatial_offset).sin();

    // Secondary ripple
    let secondary = (time * 4.5 + spatial_offset * 2.0).sin() * 0.3;

    // Random flutter
    let flutter = (time * 12.0 + spatial_offset * 5.0).sin() * 0.1;

    (primary + secondary + flutter) * wind_strength * 30.0
}
```

## Mechanical Objects

### Vehicle Suspension

Spring-damper system:

```rust
struct WheelState {
    compression: f32,
    velocity: f32,
}

fn update_suspension(
    wheel: &mut WheelState,
    ground_height: f32,
    vehicle_height: f32,
    dt: f32,
    params: &SuspensionParams,
) -> f32 {
    let rest_length = params.rest_length;
    let current_length = vehicle_height - ground_height;

    // Target compression
    let target_compression = (rest_length - current_length).max(0.0);

    // Spring force
    let spring_force = (target_compression - wheel.compression) * params.spring_k;

    // Damping force
    let damping_force = -wheel.velocity * params.damping;

    // Update velocity and position
    let acceleration = (spring_force + damping_force) / params.wheel_mass;
    wheel.velocity += acceleration * dt;
    wheel.compression += wheel.velocity * dt;
    wheel.compression = wheel.compression.clamp(0.0, params.max_compression);

    // Return suspension offset for rendering
    wheel.compression
}

fn vehicle_body_pose(wheels: &[WheelState; 4]) -> VehiclePose {
    // Calculate body pitch and roll from wheel compressions
    let front_avg = (wheels[0].compression + wheels[1].compression) / 2.0;
    let back_avg = (wheels[2].compression + wheels[3].compression) / 2.0;
    let left_avg = (wheels[0].compression + wheels[2].compression) / 2.0;
    let right_avg = (wheels[1].compression + wheels[3].compression) / 2.0;

    VehiclePose {
        pitch: (back_avg - front_avg) * 10.0,  // Degrees
        roll: (right_avg - left_avg) * 8.0,
        height_offset: -(front_avg + back_avg + left_avg + right_avg) / 4.0,
    }
}
```

### Robot Arm

Multi-joint robotic arm:

```rust
fn robot_arm_ik(
    target: Vec3,
    arm_config: &RobotArmConfig,
) -> RobotArmPose {
    // 6-DOF arm with base rotation, shoulder, elbow, wrist
    let target_2d = Vec2::new(
        (target.x.powi(2) + target.z.powi(2)).sqrt(),
        target.y - arm_config.base_height
    );

    // Base rotation (yaw)
    let base_yaw = target.x.atan2(target.z).to_degrees();

    // Solve 2-bone IK for shoulder + elbow
    let l1 = arm_config.upper_arm_length;
    let l2 = arm_config.forearm_length;
    let dist = target_2d.length().min(l1 + l2 - 0.01);

    // Elbow angle (law of cosines)
    let cos_elbow = (l1.powi(2) + l2.powi(2) - dist.powi(2)) / (2.0 * l1 * l2);
    let elbow_angle = 180.0 - cos_elbow.acos().to_degrees();

    // Shoulder angle
    let shoulder_angle = target_2d.y.atan2(target_2d.x).to_degrees()
        + (l2 * elbow_angle.to_radians().sin()).atan2(
            l1 + l2 * elbow_angle.to_radians().cos()
        ).to_degrees();

    RobotArmPose {
        base_yaw,
        shoulder_pitch: shoulder_angle,
        elbow_pitch: elbow_angle,
        wrist_pitch: -shoulder_angle - elbow_angle,  // Keep end effector level
        wrist_roll: 0.0,
    }
}
```

### Turret Tracking

Smooth turret following target:

```rust
fn turret_track(
    current: &mut TurretPose,
    target_world: Vec3,
    turret_position: Vec3,
    dt: f32,
    params: &TurretParams,
) {
    let to_target = target_world - turret_position;

    // Target angles
    let target_yaw = to_target.x.atan2(to_target.z).to_degrees();
    let horizontal_dist = (to_target.x.powi(2) + to_target.z.powi(2)).sqrt();
    let target_pitch = (-to_target.y.atan2(horizontal_dist)).to_degrees()
        .clamp(params.min_pitch, params.max_pitch);

    // Smooth interpolation
    let yaw_diff = angle_difference(current.yaw, target_yaw);
    let pitch_diff = target_pitch - current.pitch;

    let max_yaw_speed = params.rotation_speed * dt;
    let max_pitch_speed = params.rotation_speed * 0.5 * dt;

    current.yaw += yaw_diff.clamp(-max_yaw_speed, max_yaw_speed);
    current.pitch += pitch_diff.clamp(-max_pitch_speed, max_pitch_speed);

    // Normalize yaw
    current.yaw = normalize_angle(current.yaw);
}

fn angle_difference(from: f32, to: f32) -> f32 {
    let diff = (to - from) % 360.0;
    if diff > 180.0 { diff - 360.0 }
    else if diff < -180.0 { diff + 360.0 }
    else { diff }
}
```

## Easing Functions Library

```rust
fn ease_in_quad(t: f32) -> f32 { t * t }
fn ease_out_quad(t: f32) -> f32 { 1.0 - (1.0 - t).powi(2) }
fn ease_in_out_quad(t: f32) -> f32 {
    if t < 0.5 { 2.0 * t * t }
    else { 1.0 - (-2.0 * t + 2.0).powi(2) / 2.0 }
}

fn ease_in_cubic(t: f32) -> f32 { t.powi(3) }
fn ease_out_cubic(t: f32) -> f32 { 1.0 - (1.0 - t).powi(3) }

fn ease_in_elastic(t: f32) -> f32 {
    let c = 2.0 * PI / 3.0;
    if t == 0.0 { 0.0 }
    else if t == 1.0 { 1.0 }
    else { -2.0_f32.powf(10.0 * t - 10.0) * ((t * 10.0 - 10.75) * c).sin() }
}

fn ease_out_elastic(t: f32) -> f32 {
    let c = 2.0 * PI / 3.0;
    if t == 0.0 { 0.0 }
    else if t == 1.0 { 1.0 }
    else { 2.0_f32.powf(-10.0 * t) * ((t * 10.0 - 0.75) * c).sin() + 1.0 }
}

fn ease_out_bounce(t: f32) -> f32 {
    let n1 = 7.5625;
    let d1 = 2.75;
    if t < 1.0 / d1 { n1 * t * t }
    else if t < 2.0 / d1 { let t = t - 1.5 / d1; n1 * t * t + 0.75 }
    else if t < 2.5 / d1 { let t = t - 2.25 / d1; n1 * t * t + 0.9375 }
    else { let t = t - 2.625 / d1; n1 * t * t + 0.984375 }
}

fn ease_in_out_back(t: f32) -> f32 {
    let c1 = 1.70158;
    let c2 = c1 * 1.525;
    if t < 0.5 {
        (2.0 * t).powi(2) * ((c2 + 1.0) * 2.0 * t - c2) / 2.0
    } else {
        ((2.0 * t - 2.0).powi(2) * ((c2 + 1.0) * (t * 2.0 - 2.0) + c2) + 2.0) / 2.0
    }
}
```

## Blend and Transition

```rust
fn blend_poses(from: &CharacterPose, to: &CharacterPose, t: f32) -> CharacterPose {
    let t = t.clamp(0.0, 1.0);
    CharacterPose {
        left_thigh: lerp(from.left_thigh, to.left_thigh, t),
        right_thigh: lerp(from.right_thigh, to.right_thigh, t),
        // ... blend all fields
    }
}

fn lerp(a: f32, b: f32, t: f32) -> f32 {
    a + (b - a) * t
}

fn slerp_angle(a: f32, b: f32, t: f32) -> f32 {
    let diff = angle_difference(a, b);
    a + diff * t
}
```
