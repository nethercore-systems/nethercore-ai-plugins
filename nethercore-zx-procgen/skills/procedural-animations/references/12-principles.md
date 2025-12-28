# The 12 Principles of Animation

*Based on Frank Thomas & Ollie Johnston's "The Illusion of Life: Disney Animation" (1981)*

These principles, developed by Disney animators in the 1930s, remain foundational for creating believable motion. Each section shows how to apply these principles procedurally across different animation types.

---

## 1. Squash and Stretch

### Theory

Objects deform to show weight, flexibility, and force. Rigid objects feel lifeless; squash and stretch conveys material properties and impact energy. The key rule: **maintain volume** - when an object squashes wider, it should get shorter, and vice versa.

### Procedural Applications

#### Locomotion

```rust
fn landing_squash(impact_velocity: f32, mass: f32) -> Vec3 {
    // Higher velocity = more squash
    let squash_amount = (impact_velocity * 0.1).min(0.4);

    Vec3::new(
        1.0 + squash_amount,      // Wider on X
        1.0 - squash_amount,      // Shorter on Y (maintain volume)
        1.0 + squash_amount * 0.5 // Slightly wider on Z
    )
}

fn jump_stretch(upward_velocity: f32) -> Vec3 {
    let stretch = (upward_velocity * 0.05).min(0.3);

    Vec3::new(
        1.0 - stretch * 0.5,  // Narrower
        1.0 + stretch,        // Taller
        1.0 - stretch * 0.5   // Narrower
    )
}
```

#### Combat

```rust
fn weapon_swing_stretch(swing_speed: f32, phase: f32) -> Vec3 {
    // Stretch along swing direction at peak velocity
    let stretch = swing_speed * 0.1 * (phase * PI).sin();

    Vec3::new(1.0, 1.0 + stretch, 1.0 - stretch * 0.3)
}

fn hit_reaction_squash(damage: f32, time_since_hit: f32) -> Vec3 {
    let decay = (-time_since_hit * 8.0).exp();
    let squash = damage * 0.02 * decay;

    Vec3::new(1.0 + squash, 1.0 - squash, 1.0 + squash)
}
```

#### Organic Motion

```rust
fn bouncy_blob(time: f32, bounciness: f32) -> Vec3 {
    let phase = time * 3.0;
    let deform = phase.sin() * bounciness;

    Vec3::new(
        1.0 + deform * 0.2,
        1.0 - deform * 0.2,
        1.0 + deform * 0.1
    )
}
```

#### Mechanical

```rust
fn suspension_compress(load: f32, spring_k: f32) -> f32 {
    // Suspension squashes under load
    let compression = load / spring_k;
    compression.clamp(0.0, 0.3)
}
```

#### UI/Game Feel

```rust
fn button_press_squash(press_progress: f32) -> Vec3 {
    let squash = ease_out_back(press_progress) * 0.2;

    Vec3::new(1.0 + squash, 1.0 - squash * 2.0, 1.0)
}

fn collectible_bounce(time: f32) -> Vec3 {
    let bounce = (time * 8.0).sin().abs() * (-time * 2.0).exp();

    Vec3::new(1.0 + bounce * 0.15, 1.0 - bounce * 0.15, 1.0)
}
```

### Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `squash_factor` | 0.0-0.5 | Maximum deformation (0.3 = 30% wider/shorter) |
| `volume_preservation` | 0.8-1.0 | How strictly volume is maintained |
| `recovery_speed` | 2.0-15.0 | How fast object returns to rest |

### Common Mistakes

- Breaking volume (squashing without stretching the other axis)
- Applying to rigid objects that shouldn't deform (metal, stone)
- Excessive deformation that looks like jelly
- Forgetting to ease back to rest pose

---

## 2. Anticipation

### Theory

Before any major action, there's a preparatory movement in the opposite direction. This "wind-up" telegraphs the action to viewers and makes movement feel powerful. Without anticipation, actions feel sudden and weightless.

### Procedural Applications

#### Locomotion

```rust
fn jump_anticipation(charge_time: f32, max_charge: f32) -> JumpPose {
    let t = (charge_time / max_charge).min(1.0);

    JumpPose {
        crouch_depth: lerp(0.0, 0.3, ease_in_quad(t)),
        arm_raise: lerp(0.0, -30.0_f32.to_radians(), t),
        lean_forward: lerp(0.0, 10.0_f32.to_radians(), t),
    }
}

fn step_anticipation(step_phase: f32) -> f32 {
    // Slight lift before foot plants
    if step_phase < 0.1 {
        ease_out_quad(step_phase / 0.1) * 0.02
    } else {
        0.0
    }
}
```

#### Combat

```rust
fn attack_windup(attack_type: AttackType, charge: f32) -> AttackPose {
    match attack_type {
        AttackType::Slash => AttackPose {
            weapon_angle: lerp(0.0, -120.0_f32.to_radians(), charge),
            shoulder_rotation: lerp(0.0, -45.0_f32.to_radians(), charge),
            hip_twist: lerp(0.0, -20.0_f32.to_radians(), charge),
        },
        AttackType::Thrust => AttackPose {
            weapon_angle: lerp(0.0, 30.0_f32.to_radians(), charge),
            shoulder_rotation: lerp(0.0, -60.0_f32.to_radians(), charge),
            hip_twist: lerp(0.0, -10.0_f32.to_radians(), charge),
        },
        AttackType::Overhead => AttackPose {
            weapon_angle: lerp(0.0, -180.0_f32.to_radians(), charge),
            shoulder_rotation: lerp(0.0, -90.0_f32.to_radians(), charge),
            hip_twist: 0.0,
        },
    }
}
```

#### Organic Motion

```rust
fn snake_strike_coil(charge: f32) -> Vec<Vec3> {
    // Body coils back before strike
    let coil_tightness = ease_in_quad(charge);
    generate_coiled_spine(coil_tightness * 0.5)
}
```

#### Mechanical

```rust
fn piston_retract_before_punch(charge: f32) -> f32 {
    // Hydraulic arm pulls back before extending
    lerp(0.0, -0.3, ease_in_cubic(charge))
}

fn cannon_recoil_anticipation(fire_progress: f32) -> f32 {
    // Slight forward lurch before firing
    if fire_progress < 0.1 {
        ease_out_quad(fire_progress / 0.1) * 0.02
    } else {
        0.0
    }
}
```

#### UI/Game Feel

```rust
fn button_hover_anticipation(hover_time: f32) -> f32 {
    // Slight scale up when hovered, anticipating click
    1.0 + ease_out_quad(hover_time.min(0.2) / 0.2) * 0.05
}

fn screen_transition_anticipation(progress: f32) -> f32 {
    // Pull back slightly before zooming forward
    if progress < 0.15 {
        -ease_out_quad(progress / 0.15) * 0.1
    } else {
        ease_out_back((progress - 0.15) / 0.85)
    }
}
```

### Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `anticipation_duration` | 0.05-0.5s | Time spent in wind-up |
| `anticipation_magnitude` | 0.1-1.0 | How far back the wind-up goes |
| `anticipation_curve` | ease_in_* | Acceleration into anticipation |

### Common Mistakes

- Skipping anticipation entirely (actions feel robotic)
- Anticipation too long (feels sluggish)
- Anticipation in wrong direction
- Same anticipation for light and heavy actions

---

## 3. Staging

### Theory

Present actions clearly so the audience immediately understands what's happening. This involves camera angles, silhouette clarity, timing, and visual hierarchy. In games, this extends to readability during fast-paced gameplay.

### Procedural Applications

#### Locomotion

```rust
fn ensure_clear_silhouette(pose: &mut CharacterPose) {
    // Prevent arms from overlapping body in side view
    if pose.arm_angle.abs() < 15.0_f32.to_radians() {
        pose.arm_angle = 15.0_f32.to_radians() * pose.arm_angle.signum();
    }

    // Keep legs separated
    let min_leg_spread = 10.0_f32.to_radians();
    if (pose.left_leg - pose.right_leg).abs() < min_leg_spread {
        pose.left_leg += min_leg_spread * 0.5;
        pose.right_leg -= min_leg_spread * 0.5;
    }
}
```

#### Combat

```rust
fn telegraph_attack_direction(attack: &Attack) -> VisualCue {
    VisualCue {
        // Flash effect in attack direction
        direction: attack.direction,
        // Longer telegraph for stronger attacks
        duration: attack.damage * 0.01 + 0.1,
        // Color indicates attack type
        color: match attack.element {
            Element::Fire => Color::ORANGE,
            Element::Ice => Color::CYAN,
            Element::Physical => Color::WHITE,
        },
    }
}

fn attack_pose_exaggeration(base_pose: AttackPose, emphasis: f32) -> AttackPose {
    // Push poses further for clarity
    AttackPose {
        weapon_angle: base_pose.weapon_angle * (1.0 + emphasis * 0.3),
        shoulder_rotation: base_pose.shoulder_rotation * (1.0 + emphasis * 0.2),
        hip_twist: base_pose.hip_twist * (1.0 + emphasis * 0.2),
    }
}
```

#### Organic Motion

```rust
fn highlight_main_motion(tree: &mut TreePose, wind_dir: Vec3) {
    // Make primary sway more pronounced than secondary
    tree.trunk_sway *= 1.5;

    // Reduce noise on smaller branches during strong wind
    if tree.wind_strength > 0.5 {
        tree.leaf_flutter *= 0.5;
    }
}
```

#### Mechanical

```rust
fn robot_state_indication(state: RobotState) -> PoseModifier {
    match state {
        RobotState::Idle => PoseModifier::default(),
        RobotState::Alert => PoseModifier {
            head_forward: 0.1,
            shoulder_raise: 0.05,
            stance_widen: 0.1,
        },
        RobotState::Aggressive => PoseModifier {
            head_forward: 0.2,
            shoulder_raise: 0.1,
            stance_widen: 0.2,
            lean_forward: 0.1,
        },
    }
}
```

#### UI/Game Feel

```rust
fn focus_attention(elements: &mut [UIElement], focus_index: usize) {
    for (i, elem) in elements.iter_mut().enumerate() {
        if i == focus_index {
            elem.scale = 1.1;
            elem.brightness = 1.0;
            elem.z_order = 100;
        } else {
            elem.scale = 0.95;
            elem.brightness = 0.6;
            elem.z_order = 0;
        }
    }
}
```

### Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `silhouette_margin` | 5-20 degrees | Minimum angle between limbs |
| `telegraph_duration` | 0.1-0.5s | Warning time for attacks |
| `focus_scale_boost` | 1.05-1.2 | Scale multiplier for focused elements |

### Common Mistakes

- Cluttered poses where limbs overlap
- Important actions hidden by other elements
- No visual hierarchy (everything equally prominent)
- Fast actions with no telegraph

---

## 4. Straight Ahead vs Pose to Pose

### Theory

Two animation methods: **Straight Ahead** animates frame-by-frame for fluid, spontaneous motion. **Pose to Pose** defines key poses first, then fills in between for controlled, planned motion. Procedural animation is inherently straight-ahead, but can incorporate pose-to-pose through blend trees.

### Procedural Applications

#### Locomotion (Hybrid Approach)

```rust
// Pose-to-pose: Define key poses
struct WalkCycleKeyframes {
    contact_left: Pose,   // Left foot touches ground
    passing_left: Pose,   // Right leg passes left
    contact_right: Pose,  // Right foot touches ground
    passing_right: Pose,  // Left leg passes right
}

// Straight-ahead: Procedural interpolation with noise
fn walk_cycle_frame(keyframes: &WalkCycleKeyframes, phase: f32, noise_seed: u32) -> Pose {
    let (from, to, local_t) = get_keyframe_pair(keyframes, phase);

    let mut pose = blend_poses(from, to, ease_in_out_sine(local_t));

    // Add procedural variation (straight-ahead element)
    pose.hip_sway += noise_1d(noise_seed, phase * 10.0) * 0.01;
    pose.shoulder_bob += noise_1d(noise_seed + 1, phase * 20.0) * 0.005;

    pose
}
```

#### Combat (Pose to Pose with Procedural Timing)

```rust
struct AttackAnimation {
    anticipation: Pose,
    swing_start: Pose,
    impact: Pose,
    follow_through: Pose,
    recovery: Pose,
}

fn attack_frame(anim: &AttackAnimation, time: f32, speed_mult: f32) -> Pose {
    // Key poses at fixed points, timing is procedural
    let adjusted_time = time * speed_mult;

    match adjusted_time {
        t if t < 0.2 => blend(anim.anticipation, anim.swing_start, t / 0.2),
        t if t < 0.35 => blend(anim.swing_start, anim.impact, (t - 0.2) / 0.15),
        t if t < 0.6 => blend(anim.impact, anim.follow_through, (t - 0.35) / 0.25),
        t => blend(anim.follow_through, anim.recovery, (t - 0.6) / 0.4),
    }
}
```

#### Organic Motion (Straight Ahead)

```rust
fn flame_flicker(time: f32, base_height: f32) -> FlameShape {
    // Pure straight-ahead: no keyframes, continuous generation
    FlameShape {
        height: base_height * (1.0 + noise_fbm(time * 5.0, 3) * 0.3),
        width: base_height * 0.3 * (1.0 + noise_fbm(time * 7.0 + 100.0, 2) * 0.2),
        lean: noise_fbm(time * 3.0 + 200.0, 2) * 0.2,
        brightness: 0.8 + noise_fbm(time * 10.0, 2) * 0.2,
    }
}
```

#### Mechanical (Pose to Pose)

```rust
fn robot_arm_sequence(target: Vec3, current: &RobotArmState) -> RobotArmState {
    // Strictly pose-to-pose: move through defined configurations
    let waypoints = calculate_arm_waypoints(current.position, target);

    // Interpolate between waypoints with mechanical precision
    interpolate_arm_through_waypoints(&waypoints, current.progress)
}
```

#### UI/Game Feel (Pose to Pose with Easing)

```rust
fn menu_transition(from_state: MenuState, to_state: MenuState, t: f32) -> MenuState {
    // Clear keyframes for predictable UI
    MenuState {
        position: lerp(from_state.position, to_state.position, ease_out_expo(t)),
        scale: lerp(from_state.scale, to_state.scale, ease_out_back(t)),
        opacity: lerp(from_state.opacity, to_state.opacity, ease_out_quad(t)),
    }
}
```

### When to Use Each

| Approach | Best For |
|----------|----------|
| **Straight Ahead** | Fire, smoke, hair, cloth, water, chaotic motion |
| **Pose to Pose** | Precise actions, UI, mechanical systems, choreographed moves |
| **Hybrid** | Character locomotion, combat, expressive movement |

### Common Mistakes

- Using straight-ahead for actions that need precise timing
- Using pose-to-pose for organic effects (looks stiff)
- Not enough keyframes (floaty interpolation)
- Too many keyframes (defeats the purpose)

---

## 5. Follow Through and Overlapping Action

### Theory

When a character stops, different body parts stop at different times. Heavy parts have more momentum (follow through), and parts connect with slight delays (overlapping). This creates organic, connected motion rather than robotic starts/stops.

### Procedural Applications

#### Locomotion

```rust
struct OverlappingMotion {
    hip_delay: f32,      // 0.0 - immediate
    spine_delay: f32,    // Slight delay
    head_delay: f32,     // More delay
    hair_delay: f32,     // Most delay
}

fn apply_overlapping(base_motion: f32, time: f32, delays: &OverlappingMotion) -> BodyPose {
    BodyPose {
        hip_rotation: sample_motion(base_motion, time - delays.hip_delay),
        spine_rotation: sample_motion(base_motion, time - delays.spine_delay) * 0.7,
        head_rotation: sample_motion(base_motion, time - delays.head_delay) * 0.4,
        hair_offset: sample_motion(base_motion, time - delays.hair_delay) * 0.3,
    }
}

fn stop_with_follow_through(
    velocity: Vec3,
    time_since_stop: f32,
    mass: f32,
) -> Vec3 {
    // Heavier = more follow through
    let decay = (-time_since_stop * (10.0 / mass)).exp();
    velocity * decay * 0.3
}
```

#### Combat

```rust
fn weapon_follow_through(swing_end_velocity: Vec3, time: f32) -> WeaponPose {
    let decay = (-time * 5.0).exp();
    let overshoot = swing_end_velocity * decay * 0.4;

    WeaponPose {
        position_offset: overshoot,
        // Weapon continues rotating slightly
        rotation_offset: overshoot.length() * 0.5,
    }
}

fn cape_combat_drag(character_velocity: Vec3, cape_nodes: &mut [Vec3]) {
    // Cape follows character with increasing delay per node
    for (i, node) in cape_nodes.iter_mut().enumerate() {
        let delay_factor = i as f32 * 0.1;
        let target = character_velocity * -0.3 * (1.0 + delay_factor);
        *node = lerp(*node, target, 0.1);
    }
}
```

#### Organic Motion

```rust
fn tree_branch_overlap(
    trunk_sway: f32,
    branch_level: u32,
    time: f32,
) -> f32 {
    // Higher branches have more delay and amplitude
    let delay = branch_level as f32 * 0.15;
    let amplitude = 1.0 + branch_level as f32 * 0.3;

    (time - delay).sin() * trunk_sway * amplitude
}

fn hair_strand_physics(
    head_velocity: Vec3,
    strand_points: &mut [Vec3],
    dt: f32,
) {
    // Each point follows the previous with drag
    let drag = 0.95;
    let stiffness = 5.0;

    for i in 1..strand_points.len() {
        let target = strand_points[i - 1];
        let diff = target - strand_points[i];
        strand_points[i] += diff * stiffness * dt;
        strand_points[i] *= drag;
    }
}
```

#### Mechanical

```rust
fn crane_cable_swing(
    crane_stop_time: f32,
    cable_length: f32,
    initial_velocity: f32,
) -> f32 {
    // Pendulum motion after crane stops
    let period = 2.0 * PI * (cable_length / 9.8).sqrt();
    let decay = (-crane_stop_time * 0.5).exp();

    (crane_stop_time * 2.0 * PI / period).sin() * initial_velocity * decay
}
```

#### UI/Game Feel

```rust
fn notification_follow_through(appear_time: f32) -> NotificationPose {
    // Overshoots target, then settles
    let overshoot = 1.0 + 0.2 * (-appear_time * 3.0).exp() * (appear_time * 15.0).sin();

    NotificationPose {
        scale: overshoot,
        y_offset: (1.0 - overshoot) * 10.0,
    }
}

fn scroll_momentum(scroll_velocity: f32, time_since_release: f32) -> f32 {
    // Scroll continues with friction
    let friction = 0.95_f32.powf(time_since_release * 60.0);
    scroll_velocity * friction
}
```

### Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `delay_per_joint` | 0.02-0.1s | Time offset between connected parts |
| `follow_through_decay` | 2.0-10.0 | How quickly motion dampens |
| `drag_coefficient` | 0.9-0.99 | Resistance for trailing elements |

### Common Mistakes

- Everything stopping at exactly the same time
- No secondary motion on hair, cloth, accessories
- Follow through that never settles (perpetual wobble)
- Delay so large parts feel disconnected

---

## 6. Slow In and Slow Out (Easing)

### Theory

Objects accelerate when starting and decelerate when stopping. Placing more frames at the beginning and end of an action (fewer in the middle) creates natural motion. Linear motion looks mechanical and unnatural.

### Procedural Applications

#### Easing Functions Library

```rust
// Basic easing functions
fn ease_in_quad(t: f32) -> f32 { t * t }
fn ease_out_quad(t: f32) -> f32 { 1.0 - (1.0 - t) * (1.0 - t) }
fn ease_in_out_quad(t: f32) -> f32 {
    if t < 0.5 { 2.0 * t * t }
    else { 1.0 - (-2.0 * t + 2.0).powi(2) / 2.0 }
}

fn ease_in_cubic(t: f32) -> f32 { t * t * t }
fn ease_out_cubic(t: f32) -> f32 { 1.0 - (1.0 - t).powi(3) }
fn ease_in_out_cubic(t: f32) -> f32 {
    if t < 0.5 { 4.0 * t * t * t }
    else { 1.0 - (-2.0 * t + 2.0).powi(3) / 2.0 }
}

fn ease_out_back(t: f32) -> f32 {
    let c1 = 1.70158;
    let c3 = c1 + 1.0;
    1.0 + c3 * (t - 1.0).powi(3) + c1 * (t - 1.0).powi(2)
}

fn ease_out_elastic(t: f32) -> f32 {
    if t == 0.0 || t == 1.0 { return t; }
    let c4 = (2.0 * PI) / 3.0;
    2.0_f32.powf(-10.0 * t) * ((t * 10.0 - 0.75) * c4).sin() + 1.0
}

fn ease_out_bounce(t: f32) -> f32 {
    let n1 = 7.5625;
    let d1 = 2.75;

    if t < 1.0 / d1 {
        n1 * t * t
    } else if t < 2.0 / d1 {
        let t = t - 1.5 / d1;
        n1 * t * t + 0.75
    } else if t < 2.5 / d1 {
        let t = t - 2.25 / d1;
        n1 * t * t + 0.9375
    } else {
        let t = t - 2.625 / d1;
        n1 * t * t + 0.984375
    }
}
```

#### Locomotion

```rust
fn foot_arc_height(step_phase: f32, max_height: f32) -> f32 {
    // Slow out from ground, slow in to ground
    let t = ease_in_out_sine(step_phase);
    let arc = (t * PI).sin();
    arc * max_height
}

fn turn_rotation(current: f32, target: f32, t: f32) -> f32 {
    // Ease in/out for natural turning
    lerp(current, target, ease_in_out_quad(t))
}
```

#### Combat

```rust
fn attack_swing_speed(phase: f32) -> f32 {
    // Slow anticipation, fast swing, slow follow-through
    match phase {
        p if p < 0.3 => ease_in_cubic(p / 0.3) * 0.3,       // Slow wind-up
        p if p < 0.5 => 0.3 + ease_out_quad((p - 0.3) / 0.2) * 0.5,  // Fast swing
        p => 0.8 + ease_out_cubic((p - 0.5) / 0.5) * 0.2,   // Slow recovery
    }
}
```

#### Organic Motion

```rust
fn breathing_chest_scale(time: f32) -> f32 {
    // Smooth, organic breathing rhythm
    let phase = (time * 0.4 * 2.0 * PI).sin();
    let eased = ease_in_out_sine((phase + 1.0) / 2.0);
    1.0 + eased * 0.03
}
```

#### Mechanical

```rust
fn elevator_motion(progress: f32) -> f32 {
    // Mechanical but with startup/stopping ease
    ease_in_out_quad(progress)
}

fn robot_joint_rotation(current: f32, target: f32, speed: f32, dt: f32) -> f32 {
    // Servo-style motion with acceleration limits
    let diff = target - current;
    let max_step = speed * dt;
    let step = diff.clamp(-max_step, max_step);
    current + step
}
```

#### UI/Game Feel

```rust
fn menu_slide_in(time: f32, duration: f32) -> f32 {
    ease_out_expo((time / duration).min(1.0))
}

fn health_bar_drain(current: f32, target: f32, t: f32) -> f32 {
    // Fast initial drop, slow settle
    lerp(current, target, ease_out_cubic(t))
}

fn popup_scale(time: f32) -> f32 {
    // Bouncy appearance
    ease_out_back((time / 0.3).min(1.0))
}
```

### Easing Selection Guide

| Context | Recommended Easing |
|---------|-------------------|
| UI appearing | `ease_out_back`, `ease_out_elastic` |
| UI disappearing | `ease_in_quad`, `ease_in_cubic` |
| Camera movement | `ease_in_out_quad`, `ease_in_out_cubic` |
| Character starts moving | `ease_in_quad` |
| Character stops | `ease_out_quad` |
| Bouncing | `ease_out_bounce` |
| Impacts | `ease_out_expo` |
| Looping motion | `ease_in_out_sine` |

### Common Mistakes

- Using linear interpolation for organic motion
- Wrong easing direction (ease_in when should be ease_out)
- Over-easing (too slow, feels unresponsive)
- Same easing for everything (monotonous)

---

## 7. Arcs

### Theory

Natural motion follows curved paths, not straight lines. Limbs swing in arcs due to joint rotation, thrown objects follow parabolas, and even eyes track in curves. Perfectly straight motion looks robotic.

### Procedural Applications

#### Locomotion

```rust
fn hand_swing_arc(phase: f32, amplitude: f32) -> Vec3 {
    // Hand swings in figure-8 pattern, not straight line
    let forward = phase.sin() * amplitude;
    let vertical = (phase * 2.0).sin().abs() * amplitude * 0.3;
    let lateral = (phase + FRAC_PI_4).sin() * amplitude * 0.1;

    Vec3::new(lateral, vertical, forward)
}

fn foot_step_arc(phase: f32, step_length: f32, step_height: f32) -> Vec3 {
    // Foot traces arc, not straight lift-and-place
    let x = (phase * PI).sin() * step_height;
    let z = (1.0 - (phase * PI).cos()) * step_length * 0.5;

    Vec3::new(0.0, x, z)
}
```

#### Combat

```rust
fn sword_slash_arc(phase: f32, reach: f32) -> Vec3 {
    // Sword tip traces arc through space
    let angle = lerp(-120.0_f32.to_radians(), 60.0_f32.to_radians(), phase);

    Vec3::new(
        angle.sin() * reach,
        angle.cos() * reach * 0.5,
        0.0
    )
}

fn projectile_arc(start: Vec3, velocity: Vec3, time: f32, gravity: f32) -> Vec3 {
    // Parabolic arc for thrown weapons
    Vec3::new(
        start.x + velocity.x * time,
        start.y + velocity.y * time - 0.5 * gravity * time * time,
        start.z + velocity.z * time,
    )
}
```

#### Organic Motion

```rust
fn tail_wag_arc(segment: usize, time: f32, amplitude: f32) -> f32 {
    // Each segment follows previous in curved wave
    let delay = segment as f32 * 0.1;
    let wave = (time * 3.0 - delay).sin();
    let falloff = 1.0 + segment as f32 * 0.3;  // More motion at tip

    wave * amplitude * falloff
}

fn bird_wing_arc(phase: f32, wing_span: f32) -> Vec3 {
    // Wing tip traces elliptical arc
    let vertical = phase.sin() * wing_span * 0.3;
    let horizontal = wing_span * (1.0 - phase.cos().abs() * 0.1);

    Vec3::new(horizontal, vertical, 0.0)
}
```

#### Mechanical

```rust
fn piston_motion_with_arc(crank_angle: f32, crank_radius: f32, rod_length: f32) -> f32 {
    // Real piston motion isn't perfectly linear
    let x = crank_angle.cos() * crank_radius;
    let y = crank_angle.sin() * crank_radius;
    let piston_pos = x + (rod_length * rod_length - y * y).sqrt();

    piston_pos
}

fn robot_arm_arc_path(start: Vec3, end: Vec3, t: f32, arc_height: f32) -> Vec3 {
    // Even robots can use arcs for smoother paths
    let linear = lerp(start, end, t);
    let arc_offset = (t * PI).sin() * arc_height;

    linear + Vec3::new(0.0, arc_offset, 0.0)
}
```

#### UI/Game Feel

```rust
fn coin_collect_arc(start: Vec3, target: Vec3, t: f32) -> Vec3 {
    // Coins arc toward UI counter
    let linear = lerp(start, target, ease_out_quad(t));
    let arc = (t * PI).sin() * 50.0;

    linear + Vec3::new(0.0, arc, 0.0)
}

fn eye_tracking_arc(current_look: Vec2, target: Vec2, t: f32) -> Vec2 {
    // Eyes don't track in straight lines
    let direct = lerp(current_look, target, t);
    let perpendicular = Vec2::new(
        -(target.y - current_look.y),
        target.x - current_look.x
    ).normalize_or_zero();

    direct + perpendicular * (t * PI).sin() * 0.1
}
```

### Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `arc_height` | 0.1-0.5 | Peak height of arc relative to distance |
| `arc_eccentricity` | 0.0-1.0 | How elliptical vs circular |
| `arc_tilt` | -45 to 45 deg | Rotation of arc plane |

### Common Mistakes

- Straight-line motion for limb swings
- Linear projectile paths (no gravity arc)
- Identical arc for all actions
- Arcs that intersect the body

---

## 8. Secondary Action

### Theory

Secondary actions support the main action without distracting from it. A character walking (primary) might also swing their arms, blink, or have their coat flutter (secondary). These add life without stealing focus.

### Procedural Applications

#### Locomotion

```rust
fn walk_secondary_actions(walk_phase: f32, speed: f32) -> SecondaryPose {
    SecondaryPose {
        // Arm swing opposite to legs
        arm_swing: (walk_phase * PI).sin() * 20.0_f32.to_radians(),

        // Subtle head bob
        head_bob: (walk_phase * 2.0 * PI).sin().abs() * 0.02,

        // Shoulder rotation counter to hips
        shoulder_counter: (walk_phase * PI).sin() * 5.0_f32.to_radians(),

        // Breathing continues underneath
        chest_breathe: (walk_phase * 0.3).sin() * 0.01,

        // Blink occasionally
        blink: random_blink(walk_phase),
    }
}

fn random_blink(time: f32) -> f32 {
    // Blink every 3-6 seconds with quick close/open
    let blink_time = (time % 4.5);
    if blink_time < 0.15 {
        ease_in_out_quad((blink_time / 0.15).min(1.0) * 2.0 - 1.0).abs()
    } else {
        0.0
    }
}
```

#### Combat

```rust
fn attack_secondary_actions(attack_phase: f32, intensity: f32) -> SecondaryPose {
    SecondaryPose {
        // Facial expression intensifies
        brow_furrow: ease_in_quad(attack_phase) * intensity,

        // Vocal effort (mouth opens)
        mouth_open: if attack_phase > 0.3 && attack_phase < 0.5 {
            (attack_phase - 0.3) / 0.2
        } else {
            0.0
        },

        // Off-hand reacts
        off_hand_brace: attack_phase * 0.5,

        // Armor/cloth reacts to motion
        cape_flutter: intensity * attack_phase,
    }
}
```

#### Organic Motion

```rust
fn tree_secondary_motion(wind: f32, time: f32) -> TreeSecondary {
    TreeSecondary {
        // Leaves flutter faster than branches sway
        leaf_flutter: noise_fbm(time * 10.0, 3) * wind * 0.5,

        // Small branches shake more
        twig_shake: noise_fbm(time * 5.0 + 100.0, 2) * wind * 0.3,

        // Bark texture subtle wobble (if close-up)
        bark_wobble: (time * 2.0).sin() * 0.002,

        // Bird occasionally repositions
        bird_shuffle: if (time % 5.0) < 0.5 {
            (time % 5.0) / 0.5
        } else {
            0.0
        },
    }
}
```

#### Mechanical

```rust
fn robot_secondary_actions(main_action: RobotAction, time: f32) -> RobotSecondary {
    RobotSecondary {
        // Status lights pulse
        light_pulse: (time * 2.0).sin() * 0.5 + 0.5,

        // Cooling vents cycle
        vent_cycle: (time * 0.5).sin().abs(),

        // Antenna sway
        antenna_sway: (time * 1.5).sin() * 0.1,

        // Hydraulic hiss (audio cue timing)
        hydraulic_timing: main_action.requires_hydraulics(),

        // Eye/sensor tracking
        sensor_track: calculate_look_target(time),
    }
}
```

#### UI/Game Feel

```rust
fn idle_menu_secondary(time: f32) -> MenuSecondary {
    MenuSecondary {
        // Subtle background particle drift
        particle_drift: Vec2::new(
            (time * 0.5).sin() * 10.0,
            (time * 0.3).cos() * 5.0
        ),

        // Logo gentle pulse
        logo_pulse: 1.0 + (time * 0.5).sin() * 0.02,

        // Button highlight shimmer
        shimmer_phase: time * 0.3,

        // Background color subtle shift
        bg_hue_shift: (time * 0.1).sin() * 5.0,
    }
}
```

### Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `secondary_amplitude` | 0.1-0.5 | Intensity relative to primary action |
| `secondary_frequency` | 0.5-3.0x | Speed relative to primary |
| `secondary_delay` | 0.0-0.2s | Offset from primary action |

### Common Mistakes

- Secondary actions overwhelming the primary
- No secondary actions (character feels dead)
- Secondary actions that contradict the primary
- Same secondary actions regardless of context

---

## 9. Timing

### Theory

The number of frames for an action defines its speed and feeling. Fewer frames = faster/lighter, more frames = slower/heavier. Timing conveys weight, mood, and personality. The same motion can feel comedic or dramatic based on timing alone.

### Procedural Applications

#### Locomotion

```rust
fn walk_timing_by_character(character: &Character) -> WalkTiming {
    let base_cycle = 1.0; // seconds

    WalkTiming {
        cycle_duration: base_cycle * match character.size {
            Size::Tiny => 0.5,    // Quick, light steps
            Size::Small => 0.7,
            Size::Medium => 1.0,
            Size::Large => 1.3,
            Size::Huge => 1.8,   // Ponderous, heavy steps
        },

        foot_contact_hold: match character.weight {
            Weight::Light => 0.05,
            Weight::Medium => 0.1,
            Weight::Heavy => 0.2,  // Longer ground contact
        },
    }
}

fn run_cycle_timing(urgency: f32) -> f32 {
    // 0.0 = casual jog, 1.0 = sprint
    lerp(0.6, 0.35, urgency)  // seconds per cycle
}
```

#### Combat

```rust
fn attack_timing(weapon: &Weapon, character: &Character) -> AttackTiming {
    let base = weapon.base_speed;

    AttackTiming {
        anticipation: base * 0.3 * character.strength_factor(),
        swing: base * 0.15,          // Fast swing always
        impact_hold: 0.05,           // Brief freeze on hit
        recovery: base * 0.4,        // Slower recovery for heavy weapons

        // Total: heavier weapons take longer overall
        total: base * (0.3 + 0.15 + 0.4),
    }
}

fn hit_stun_duration(damage: f32, target_poise: f32) -> f32 {
    // More damage = longer stun, more poise = shorter
    let base_stun = 0.2;
    let damage_factor = (damage / 50.0).min(1.0);
    let poise_factor = 1.0 / (1.0 + target_poise * 0.1);

    base_stun + damage_factor * 0.5 * poise_factor
}
```

#### Organic Motion

```rust
fn creature_timing_by_metabolism(metabolism: f32) -> CreatureTiming {
    // metabolism: 0.0 = cold-blooded slug, 1.0 = hummingbird
    CreatureTiming {
        blink_speed: lerp(0.5, 0.05, metabolism),
        breath_rate: lerp(0.1, 4.0, metabolism),  // breaths per second
        reaction_delay: lerp(0.5, 0.02, metabolism),
        movement_speed_mult: lerp(0.3, 2.0, metabolism),
    }
}
```

#### Mechanical

```rust
fn machine_timing(power: f32, load: f32) -> MachineTiming {
    // More power = faster, more load = slower
    let efficiency = power / (1.0 + load);

    MachineTiming {
        startup_duration: lerp(2.0, 0.2, efficiency),
        operation_speed: efficiency,
        shutdown_duration: lerp(3.0, 0.5, efficiency),
    }
}
```

#### UI/Game Feel

```rust
fn ui_timing_by_importance(importance: Importance) -> f32 {
    match importance {
        Importance::Critical => 0.1,   // Fast, urgent
        Importance::High => 0.2,
        Importance::Normal => 0.3,
        Importance::Low => 0.5,        // Leisurely
        Importance::Ambient => 1.0,    // Very slow, background
    }
}

fn impact_freeze_frames(damage: f32) -> u32 {
    // Hit stop duration scales with damage
    let base_frames = 2;
    let bonus_frames = (damage / 20.0) as u32;
    (base_frames + bonus_frames).min(8)
}
```

### Timing Reference

| Action | Light/Fast | Medium | Heavy/Slow |
|--------|-----------|--------|------------|
| Jump anticipation | 2-4 frames | 6-10 frames | 12-20 frames |
| Attack swing | 3-6 frames | 8-15 frames | 20-40 frames |
| Landing recovery | 4-8 frames | 10-20 frames | 25-45 frames |
| Turn around | 6-10 frames | 15-25 frames | 30-50 frames |
| Blink | 4-6 frames | 8-12 frames | N/A |

### Common Mistakes

- Everything at the same speed (no weight variation)
- Actions too fast to read
- Actions too slow (unresponsive feel)
- Ignoring character weight in timing

---

## 10. Exaggeration

### Theory

Animation that mimics reality exactly looks dull. Exaggeration pushes poses, timing, and expressions beyond realism for clarity and appeal. The key is knowing how much to push based on style (subtle realism vs cartoony).

### Procedural Applications

#### Locomotion

```rust
fn exaggerate_walk(base_pose: &WalkPose, style: AnimStyle) -> WalkPose {
    let mult = match style {
        AnimStyle::Realistic => 1.0,
        AnimStyle::Stylized => 1.3,
        AnimStyle::Cartoony => 1.8,
        AnimStyle::Anime => 2.5,
    };

    WalkPose {
        hip_sway: base_pose.hip_sway * mult,
        arm_swing: base_pose.arm_swing * mult,
        head_bob: base_pose.head_bob * mult * 0.7,  // Less on head
        lean: base_pose.lean * mult,
    }
}

fn exaggerate_jump_squash(impact_velocity: f32, style: AnimStyle) -> f32 {
    let base_squash = (impact_velocity * 0.1).min(0.3);

    match style {
        AnimStyle::Realistic => base_squash,
        AnimStyle::Stylized => base_squash * 1.5,
        AnimStyle::Cartoony => base_squash * 2.5,
        AnimStyle::Anime => base_squash * 1.8,
    }
}
```

#### Combat

```rust
fn exaggerate_attack_arc(base_arc: f32, weapon_type: WeaponType) -> f32 {
    // Bigger weapons get more exaggerated swings
    let exaggeration = match weapon_type {
        WeaponType::Dagger => 1.1,
        WeaponType::Sword => 1.3,
        WeaponType::Greatsword => 1.6,
        WeaponType::Hammer => 2.0,
    };

    base_arc * exaggeration
}

fn exaggerate_hit_reaction(damage: f32, style: AnimStyle) -> HitReaction {
    let base_knockback = damage * 0.1;
    let base_rotation = damage * 2.0;

    let mult = match style {
        AnimStyle::Realistic => 1.0,
        AnimStyle::Stylized => 1.5,
        AnimStyle::Cartoony => 3.0,
        AnimStyle::Anime => 2.0,
    };

    HitReaction {
        knockback: base_knockback * mult,
        spin: base_rotation * mult,
        hang_time: if style == AnimStyle::Anime { 0.1 } else { 0.0 },
    }
}
```

#### Organic Motion

```rust
fn exaggerate_expression(emotion: Emotion, intensity: f32, style: AnimStyle) -> Face {
    let mult = match style {
        AnimStyle::Realistic => 0.7,
        AnimStyle::Stylized => 1.0,
        AnimStyle::Cartoony => 1.8,
        AnimStyle::Anime => 1.5,
    };

    let base = emotion.base_expression();

    Face {
        brow_height: base.brow_height * intensity * mult,
        eye_size: base.eye_size * (1.0 + (intensity - 0.5) * mult * 0.5),
        mouth_shape: base.mouth_shape.scale(intensity * mult),
    }
}
```

#### Mechanical

```rust
fn exaggerate_mechanical_motion(base_speed: f32, style: AnimStyle) -> f32 {
    // Even machines can be exaggerated for style
    match style {
        AnimStyle::Realistic => base_speed,
        AnimStyle::Stylized => base_speed * 1.2,  // Snappier
        AnimStyle::Cartoony => base_speed * 1.5,  // More dynamic
        AnimStyle::Anime => base_speed * 1.3,
    }
}
```

#### UI/Game Feel

```rust
fn exaggerate_ui_feedback(base_scale: f32, importance: f32) -> f32 {
    // More important = more exaggerated feedback
    let exaggeration = 1.0 + importance * 0.5;
    base_scale * exaggeration
}

fn exaggerate_screen_shake(base_intensity: f32, style: AnimStyle) -> f32 {
    match style {
        AnimStyle::Realistic => base_intensity * 0.5,
        AnimStyle::Stylized => base_intensity,
        AnimStyle::Cartoony => base_intensity * 2.0,
        AnimStyle::Anime => base_intensity * 1.5,
    }
}
```

### Exaggeration by Style

| Element | Realistic | Stylized | Cartoony |
|---------|-----------|----------|----------|
| Pose extremes | 1.0x | 1.3x | 2.0x |
| Squash/stretch | 0-10% | 10-30% | 30-60% |
| Anticipation | Subtle | Visible | Obvious |
| Follow through | Brief | Moderate | Extended |
| Speed contrast | Low | Medium | High |

### Common Mistakes

- No exaggeration (boring, stiff animation)
- Over-exaggeration for the style (breaks believability)
- Inconsistent exaggeration levels
- Exaggerating the wrong elements

---

## 11. Solid Drawing

### Theory

Characters should feel like they have volume, weight, and exist in 3D space. Avoid "twins" (perfectly symmetrical poses), maintain consistent proportions, and respect anatomy. In 3D/procedural animation, this means proper bone hierarchies and avoiding impossible poses.

### Procedural Applications

#### Locomotion

```rust
fn break_symmetry(pose: &mut CharacterPose, asymmetry: f32) {
    // Avoid perfect mirror poses
    pose.left_arm_swing *= 1.0 + asymmetry * 0.1;
    pose.right_arm_swing *= 1.0 - asymmetry * 0.05;

    pose.left_shoulder_height += asymmetry * 0.02;
    pose.right_shoulder_height -= asymmetry * 0.01;

    // Slight head tilt
    pose.head_tilt = asymmetry * 3.0_f32.to_radians();
}

fn maintain_ground_contact(pose: &mut CharacterPose, ground_height: f32) {
    // Ensure feet actually touch ground (no floating)
    let lowest_foot = pose.left_foot_y.min(pose.right_foot_y);
    let adjustment = ground_height - lowest_foot;

    pose.root_y += adjustment;
}
```

#### Combat

```rust
fn validate_pose_physically(pose: &AttackPose) -> AttackPose {
    let mut valid = pose.clone();

    // Clamp to anatomical limits
    valid.shoulder_rotation = valid.shoulder_rotation.clamp(
        -90.0_f32.to_radians(),
        180.0_f32.to_radians()
    );

    valid.elbow_bend = valid.elbow_bend.clamp(
        0.0,  // Can't bend backwards
        150.0_f32.to_radians()
    );

    valid.wrist_twist = valid.wrist_twist.clamp(
        -90.0_f32.to_radians(),
        90.0_f32.to_radians()
    );

    valid
}

fn add_weight_to_weapon(pose: &mut AttackPose, weapon_weight: f32) {
    // Heavy weapons pull the body
    pose.lean_forward += weapon_weight * 0.01;
    pose.shoulder_drop = weapon_weight * 0.02;
    pose.wrist_strain = (weapon_weight * 0.005).min(0.1);
}
```

#### Organic Motion

```rust
fn maintain_skeleton_integrity(bones: &mut [BoneTransform]) {
    // Ensure bones stay connected
    for i in 1..bones.len() {
        let parent = &bones[bones[i].parent_index];
        let expected_origin = parent.transform_point(bones[i].local_offset);

        // Snap to parent endpoint
        bones[i].world_position = expected_origin;
    }
}

fn preserve_volume_during_deform(mesh: &mut Mesh, deformation: &Deformation) {
    let original_volume = mesh.calculate_volume();

    mesh.apply_deformation(deformation);

    let new_volume = mesh.calculate_volume();
    let scale_factor = (original_volume / new_volume).powf(1.0 / 3.0);

    // Restore volume by scaling
    mesh.uniform_scale(scale_factor);
}
```

#### Mechanical

```rust
fn enforce_joint_constraints(robot: &mut RobotPose) {
    // Each joint has specific limits
    for joint in &mut robot.joints {
        joint.angle = joint.angle.clamp(joint.min_angle, joint.max_angle);

        // Ensure parts don't intersect
        if check_self_collision(robot, joint) {
            joint.angle = find_safe_angle(robot, joint);
        }
    }
}
```

#### UI/Game Feel

```rust
fn consistent_ui_proportions(element: &mut UIElement, base_size: f32) {
    // Maintain aspect ratio during scaling
    let aspect = element.original_width / element.original_height;

    if element.width / element.height != aspect {
        element.height = element.width / aspect;
    }

    // Ensure minimum readable size
    element.width = element.width.max(base_size * 0.5);
    element.height = element.height.max(base_size * 0.5);
}
```

### Pose Validation Checklist

```rust
fn validate_character_pose(pose: &CharacterPose) -> Vec<PoseIssue> {
    let mut issues = Vec::new();

    // Check for twins
    if (pose.left_arm - pose.right_arm).abs() < 0.01 {
        issues.push(PoseIssue::Twins("Arms are mirrored"));
    }

    // Check joint limits
    if pose.elbow_bend < 0.0 {
        issues.push(PoseIssue::ImpossibleBend("Elbow bending wrong way"));
    }

    // Check ground contact
    if pose.lowest_foot_height > 0.01 && pose.is_grounded {
        issues.push(PoseIssue::Floating("Character floating above ground"));
    }

    // Check proportions
    if pose.head_scale > 1.5 || pose.head_scale < 0.7 {
        issues.push(PoseIssue::ProportionError("Head size inconsistent"));
    }

    issues
}
```

### Common Mistakes

- Perfectly symmetrical "twins" poses
- Limbs bending the wrong direction
- Characters floating above ground
- Proportions changing during animation
- Bones disconnecting from parents

---

## 12. Appeal

### Theory

Characters should be interesting to watch - this is "appeal." It doesn't mean cute; villains and monsters can have appeal too. Appeal comes from clear design, readable poses, interesting asymmetry, and personality in movement.

### Procedural Applications

#### Locomotion

```rust
fn add_personality_to_walk(
    base_walk: WalkCycle,
    personality: Personality,
) -> WalkCycle {
    match personality {
        Personality::Confident => WalkCycle {
            stride_length: base_walk.stride_length * 1.2,
            hip_sway: base_walk.hip_sway * 1.3,
            head_height: base_walk.head_height + 0.05,
            arm_swing: base_walk.arm_swing * 0.8,  // Less arm swing
            ..base_walk
        },

        Personality::Nervous => WalkCycle {
            stride_length: base_walk.stride_length * 0.7,
            speed: base_walk.speed * 1.3,  // Quick short steps
            shoulder_hunch: 0.1,
            head_dart: 0.05,  // Looking around
            ..base_walk
        },

        Personality::Tired => WalkCycle {
            stride_length: base_walk.stride_length * 0.8,
            speed: base_walk.speed * 0.7,
            foot_drag: 0.02,
            head_droop: 0.1,
            shoulder_slump: 0.15,
            ..base_walk
        },

        Personality::Aggressive => WalkCycle {
            stride_length: base_walk.stride_length * 1.1,
            lean_forward: 0.1,
            fist_clench: true,
            brow_furrow: 0.5,
            heavy_footfall: true,
            ..base_walk
        },
    }
}
```

#### Combat

```rust
fn fighting_style_appeal(
    attack: &mut AttackAnimation,
    style: FightingStyle,
) {
    match style {
        FightingStyle::Elegant => {
            attack.add_flourish(0.0, 0.2);  // Opening flourish
            attack.smooth_transitions = true;
            attack.arc_exaggeration = 1.2;
        },

        FightingStyle::Brutal => {
            attack.impact_emphasis = 1.5;
            attack.recovery_stagger = true;
            attack.add_grunt_timing(0.4);
        },

        FightingStyle::Technical => {
            attack.precision_movements = true;
            attack.minimal_wind_up = true;
            attack.efficient_recovery = true;
        },

        FightingStyle::Wild => {
            attack.random_variation = 0.2;
            attack.overswing = true;
            attack.off_balance_recovery = true;
        },
    }
}
```

#### Organic Motion

```rust
fn creature_appeal_traits(creature: &mut CreatureAnimation) {
    // Add signature movements that define the creature
    creature.idle_quirks = vec![
        IdleQuirk::HeadTilt { frequency: 0.3, angle: 15.0 },
        IdleQuirk::EarFlick { frequency: 0.5 },
        IdleQuirk::TailSwish { pattern: SwishPattern::Curious },
    ];

    // Distinctive locomotion
    creature.gait_personality = GaitPersonality {
        bounce: 0.3,         // Springy movement
        sway: 0.2,           // Side-to-side personality
        head_lead: true,     // Head moves first
    };
}
```

#### Mechanical

```rust
fn robot_personality_appeal(robot: &mut RobotAnimation, personality: RobotPersonality) {
    match personality {
        RobotPersonality::Helpful => {
            robot.posture = Posture::Attentive;
            robot.movement_eagerness = 1.2;
            robot.head_tracking_responsiveness = 0.9;
        },

        RobotPersonality::Menacing => {
            robot.posture = Posture::Looming;
            robot.movement_deliberate = true;
            robot.red_eye_glow = true;
            robot.hydraulic_hiss_emphasis = 1.5;
        },

        RobotPersonality::Quirky => {
            robot.head_tilts = true;
            robot.occasional_malfunction = 0.1;
            robot.beep_personality = BeepStyle::Musical;
        },
    }
}
```

#### UI/Game Feel

```rust
fn ui_personality(theme: UITheme) -> UIPersonality {
    match theme {
        UITheme::Playful => UIPersonality {
            bounce_factor: 1.3,
            color_vibrancy: 1.2,
            rounded_corners: true,
            hover_wiggle: true,
            sound_style: SoundStyle::Cheerful,
        },

        UITheme::Sleek => UIPersonality {
            transition_style: TransitionStyle::Smooth,
            color_vibrancy: 0.8,
            sharp_corners: true,
            subtle_glow: true,
            sound_style: SoundStyle::Minimal,
        },

        UITheme::Retro => UIPersonality {
            pixel_snap: true,
            limited_palette: true,
            scan_lines: true,
            chunky_animations: true,
            sound_style: SoundStyle::Chiptune,
        },
    }
}
```

### Appeal Checklist

| Element | Questions to Ask |
|---------|------------------|
| **Silhouette** | Is the pose readable as a silhouette? |
| **Asymmetry** | Are left/right sides slightly different? |
| **Line of action** | Is there a clear dynamic line through the pose? |
| **Personality** | Does movement reflect character personality? |
| **Contrast** | Is there variety in timing and poses? |
| **Details** | Are there small touches that add life? |

### Common Mistakes

- Generic, personality-less movement
- Overly symmetric poses
- Forgetting signature quirks
- Same movement for all characters
- No contrast between characters' styles

---

## Quick Reference Card

| Principle | Key Question | Procedural Solution |
|-----------|--------------|---------------------|
| **Squash & Stretch** | Does it feel like it has weight? | Scale transforms on impact/velocity |
| **Anticipation** | Can I predict what's coming? | Add wind-up phase before actions |
| **Staging** | Is the action clear? | Ensure silhouette clarity, telegraph |
| **Straight/Pose** | Is the motion controlled or wild? | Keyframes vs continuous generation |
| **Follow Through** | Do parts settle naturally? | Add delayed secondary motion |
| **Slow In/Out** | Does it accelerate naturally? | Use easing functions, not linear |
| **Arcs** | Does it move in curves? | Calculate arc paths for all motion |
| **Secondary Action** | Is it alive when idle? | Add breathing, blinking, micro-motion |
| **Timing** | Does timing match weight? | Adjust durations by mass/importance |
| **Exaggeration** | Is it interesting? | Push poses beyond realistic limits |
| **Solid Drawing** | Does it feel 3D? | Validate anatomy, avoid twins |
| **Appeal** | Is it engaging? | Add personality quirks, asymmetry |

---

## Further Reading

- Thomas, Frank & Johnston, Ollie. *The Illusion of Life: Disney Animation* (1981)
- Williams, Richard. *The Animator's Survival Kit* (2001)
- Lasseter, John. "Principles of Traditional Animation Applied to 3D Computer Animation" (1987)
