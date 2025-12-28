# Animation Enhancement Techniques

Detailed techniques for upgrading animation quality through the tier system, based on the 12 Principles of Animation.

## Placeholder → Temp Upgrades

### Add Proper Timing

Transform linear motion into timed motion:

```rust
// Before: Linear interpolation
animation.set_interpolation(Interpolation::Linear);

// After: Add basic easing
animation.set_interpolation(Interpolation::EaseInOut);

// Per-keyframe timing
for keyframe in animation.keyframes_mut() {
    keyframe.set_easing(Easing::QuadInOut);
}
```

### Add Keyframes for Clarity

Placeholder animations often have too few keyframes:

```rust
// Walk cycle minimum keyframes
let walk_keyframes = [
    (0.0, Pose::contact_right()),    // Right foot contact
    (0.25, Pose::passing_right()),   // Right leg passing
    (0.5, Pose::contact_left()),     // Left foot contact
    (0.75, Pose::passing_left()),    // Left leg passing
    (1.0, Pose::contact_right()),    // Loop back
];

for (time, pose) in walk_keyframes {
    animation.add_keyframe(time, pose);
}
```

### Fix Loop Points

Ensure seamless looping:

```rust
// Check loop continuity
let start_pose = animation.pose_at(0.0);
let end_pose = animation.pose_at(1.0);

if !poses_match(&start_pose, &end_pose, threshold: 0.01) {
    // Add transition keyframe
    animation.add_keyframe(0.95, end_pose.blend(&start_pose, 0.5));
    animation.set_keyframe(1.0, start_pose.clone());
}
```

---

## Temp → Final Upgrades

### Add Easing (Slow In/Slow Out)

Natural motion accelerates and decelerates:

```rust
// Configure easing per bone/property
fn apply_easing_profile(animation: &mut Animation, profile: EasingProfile) {
    for track in animation.tracks_mut() {
        match track.bone_type {
            // Root motion: smooth ease
            BoneType::Root => track.set_easing(Easing::CubicInOut),
            // Extremities: snappier
            BoneType::Hand | BoneType::Foot =>
                track.set_easing(Easing::QuadOut),
            // Spine: smooth follow-through
            BoneType::Spine => track.set_easing(Easing::SineInOut),
            _ => track.set_easing(Easing::QuadInOut),
        }
    }
}
```

### Add Secondary Motion

Body parts don't all move at once:

```rust
// Offset secondary elements
fn add_secondary_motion(animation: &mut Animation) {
    let offsets = [
        ("head", 0.02),        // Head follows slightly
        ("hair", 0.04),        // Hair lags more
        ("cape", 0.05),        // Cape lags most
        ("weapon", 0.03),      // Weapon has inertia
    ];

    for (bone_name, delay) in offsets {
        if let Some(track) = animation.get_track_mut(bone_name) {
            track.offset_time(delay);
        }
    }
}
```

### Implement Arc Motion

Natural motion follows arcs, not straight lines:

```rust
// Convert linear motion to arcs
fn arcify_motion(animation: &mut Animation, bone: &str) {
    let track = animation.get_track_mut(bone).unwrap();

    // For each keyframe pair
    for i in 0..track.keyframes.len() - 1 {
        let start = &track.keyframes[i];
        let end = &track.keyframes[i + 1];

        // Calculate arc control point
        let mid_time = (start.time + end.time) / 2.0;
        let arc_height = (end.position - start.position).length() * 0.2;

        // Add arc keyframe
        let arc_pos = (start.position + end.position) / 2.0
            + Vec3::Y * arc_height;

        track.insert_keyframe(mid_time, arc_pos, Easing::SineInOut);
    }
}
```

### Improve Weight and Timing

Different actions have different timing feels:

```rust
// Timing guidelines by action type
fn get_timing_profile(action: ActionType) -> TimingProfile {
    match action {
        ActionType::Walk => TimingProfile {
            total_frames: 16,
            contact_frame: 0,
            passing_frame: 4,
            key_poses: vec![0, 4, 8, 12],
        },
        ActionType::Run => TimingProfile {
            total_frames: 12,
            contact_frame: 0,
            passing_frame: 3,
            key_poses: vec![0, 3, 6, 9],
        },
        ActionType::Jump => TimingProfile {
            total_frames: 24,
            anticipation_frames: 4,
            air_frames: 16,
            landing_frames: 4,
            key_poses: vec![0, 4, 12, 20, 24],
        },
        ActionType::Attack => TimingProfile {
            total_frames: 20,
            anticipation_frames: 6,
            action_frames: 4,
            follow_through_frames: 10,
            key_poses: vec![0, 6, 10, 20],
        },
    }
}
```

---

## Final → Hero Upgrades

### Add Anticipation

Preparation before main action:

```rust
// Anticipation for jump
fn add_jump_anticipation(animation: &mut Animation) {
    // Before jump: crouch down
    let anticipation_pose = Pose {
        root_y: -0.1,  // Squat down
        spine_rotation: -5.0,  // Lean forward slightly
        knee_bend: 30.0,  // Bend knees
        arm_position: ArmPosition::Back,  // Arms back
    };

    // Insert anticipation before jump
    animation.insert_keyframe(0.0, anticipation_pose);
    animation.insert_keyframe(0.15, anticipation_pose.deeper(1.2));  // Deeper squat
    // Original jump starts at 0.2
}

// Anticipation for punch
fn add_punch_anticipation(animation: &mut Animation) {
    let wind_up = Pose {
        shoulder_rotation: -30.0,  // Pull back
        elbow_bend: 120.0,  // Coil arm
        torso_rotation: -15.0,  // Wind up body
        weight_shift: -0.1,  // Lean back
    };

    animation.insert_keyframe(0.0, wind_up);
    animation.insert_keyframe(0.1, wind_up.exaggerated(1.1));
    // Strike starts at 0.15
}
```

### Add Follow-Through

Motion continues after main action:

```rust
// Follow-through for punch
fn add_punch_follow_through(animation: &mut Animation) {
    // After impact: arm continues, body follows
    let follow_poses = [
        (0.0, "impact"),
        (0.05, Pose {
            arm_extension: 1.1,  // Overextend
            shoulder_forward: 10.0,
            torso_rotation: 20.0,
        }),
        (0.15, Pose {
            arm_extension: 1.05,  // Slight recoil
            shoulder_forward: 5.0,
            torso_rotation: 15.0,
        }),
        (0.3, Pose {
            arm_extension: 0.9,  // Return
            shoulder_forward: 0.0,
            torso_rotation: 5.0,
        }),
    ];

    for (time_offset, pose) in follow_poses {
        animation.add_keyframe(impact_time + time_offset, pose);
    }
}
```

### Overlapping Action

Different body parts move at different times:

```rust
// Overlapping action for character turn
fn add_overlapping_turn(animation: &mut Animation) {
    // Order of movement: hips → spine → shoulders → head → hair
    let overlap_delays = [
        ("hips", 0.0),
        ("spine_lower", 0.02),
        ("spine_upper", 0.04),
        ("shoulders", 0.06),
        ("neck", 0.08),
        ("head", 0.10),
        ("hair_base", 0.12),
        ("hair_tip", 0.15),
    ];

    for (bone, delay) in overlap_delays {
        if let Some(track) = animation.get_track_mut(bone) {
            track.offset_time(delay);
            // Also ease the delayed motion
            track.set_easing(Easing::SineOut);
        }
    }
}
```

### Exaggeration

Push poses beyond realistic for readability:

```rust
// Exaggerate key poses
fn exaggerate_keyframes(animation: &mut Animation, amount: f32) {
    // Find key poses (extremes)
    let key_frames = animation.find_extreme_poses();

    for frame in key_frames {
        let pose = animation.pose_at(frame);
        let neutral = animation.get_neutral_pose();

        // Exaggerate away from neutral
        let exaggerated = Pose::lerp(&neutral, &pose, 1.0 + amount);

        animation.set_keyframe(frame, exaggerated);
    }
}

// Different exaggeration by animation type
fn get_exaggeration_amount(anim_type: AnimationType) -> f32 {
    match anim_type {
        AnimationType::Idle => 0.05,     // Subtle
        AnimationType::Walk => 0.1,      // Noticeable
        AnimationType::Run => 0.15,      // Clear
        AnimationType::Attack => 0.25,   // Dramatic
        AnimationType::Hurt => 0.3,      // Very dramatic
        AnimationType::Death => 0.35,    // Maximum
    }
}
```

### Squash and Stretch

Volume preservation with deformation:

```rust
// Squash on landing
fn add_landing_squash(animation: &mut Animation, impact_frame: usize) {
    let pre_impact = animation.pose_at(impact_frame - 1);
    let impact = animation.pose_at(impact_frame);

    // Calculate squash based on fall velocity
    let velocity = (impact.root_y - pre_impact.root_y).abs();
    let squash_amount = (velocity * 2.0).min(0.3);

    // Apply squash (compress Y, expand XZ)
    let squashed = impact.with_scale(Vec3::new(
        1.0 + squash_amount * 0.5,  // Wider
        1.0 - squash_amount,         // Shorter
        1.0 + squash_amount * 0.5,  // Deeper
    ));

    animation.set_keyframe(impact_frame, squashed);

    // Recovery frames
    animation.insert_keyframe(
        impact_frame + 2,
        impact.with_scale(Vec3::new(0.95, 1.05, 0.95)),  // Slight stretch
    );
    animation.insert_keyframe(
        impact_frame + 4,
        impact,  // Return to normal
    );
}

// Stretch during fast motion
fn add_motion_stretch(animation: &mut Animation) {
    for i in 1..animation.frame_count() - 1 {
        let prev = animation.pose_at(i - 1);
        let curr = animation.pose_at(i);
        let velocity = (curr.root_position - prev.root_position).length();

        if velocity > STRETCH_THRESHOLD {
            let stretch = 1.0 + (velocity - STRETCH_THRESHOLD) * 0.5;
            let direction = (curr.root_position - prev.root_position).normalize();

            // Stretch along motion direction
            let stretched = curr.stretch_along(direction, stretch);
            animation.set_keyframe(i, stretched);
        }
    }
}
```

---

## Animation Type Guidelines

### Walk Cycle (Final → Hero)

| Aspect | Final | Hero Addition |
|--------|-------|---------------|
| Keyframes | 8-12 | 16-24 |
| Secondary motion | Arm swing | + shoulder, spine twist |
| Overlap | Basic | Full body chain |
| Weight | Implied | Clear weight shift |
| Personality | Neutral | Character-specific |

### Run Cycle (Final → Hero)

| Aspect | Final | Hero Addition |
|--------|-------|---------------|
| Keyframes | 8-10 | 12-16 |
| Air time | Present | Exaggerated float |
| Impact | Simple | Squash on contact |
| Arms | Basic pump | Full wind-up, overlap |
| Lean | Static | Dynamic based on speed |

### Attack Animation (Final → Hero)

| Aspect | Final | Hero Addition |
|--------|-------|---------------|
| Anticipation | 2-3 frames | 4-6 frames with wind-up |
| Strike | Clear | Smear frames, stretch |
| Follow-through | Present | Overlapping settle |
| Recovery | Simple | Weight-based return |
| Exaggeration | 15% | 25-30% |

### Jump Animation (Final → Hero)

| Aspect | Final | Hero Addition |
|--------|-------|---------------|
| Anticipation | Crouch | Deep squat, arm swing |
| Launch | Simple | Stretch, anticipation |
| Air | Static pose | Slight movement, arc arms |
| Landing | Contact | Squash, recovery bounce |
| Timing | Linear | Variable (hang time) |

---

## Frame Budget by Tier

### Standard Frame Counts

| Animation | Placeholder | Temp | Final | Hero |
|-----------|-------------|------|-------|------|
| Idle | 1 | 4-6 | 8-16 | 24-48 |
| Walk | 4 | 8 | 12-16 | 16-24 |
| Run | 4 | 6-8 | 10-12 | 12-16 |
| Jump | 3 | 6-8 | 12-16 | 20-30 |
| Attack | 4 | 8-10 | 14-18 | 20-30 |
| Hurt | 2 | 4-6 | 8-12 | 12-20 |
| Death | 4 | 8-12 | 16-24 | 30-48 |

### FPS Guidelines

| Tier | Target FPS | Notes |
|------|------------|-------|
| Placeholder | 10 | Just readable |
| Temp | 15 | Smooth enough |
| Final | 20-24 | Production quality |
| Hero | 24-30 | Maximum smoothness |

---

## Quality Checks

### Loop Continuity Check

```rust
fn check_loop_quality(animation: &Animation) -> LoopQuality {
    let start = animation.pose_at(0.0);
    let end = animation.pose_at(animation.duration());

    LoopQuality {
        position_error: (end.root_position - start.root_position).length(),
        rotation_error: (end.root_rotation - start.root_rotation).angle(),
        velocity_match: check_velocity_continuity(animation),
        acceleration_match: check_acceleration_continuity(animation),
    }
}
```

### Motion Arc Check

```rust
fn check_arc_quality(animation: &Animation, bone: &str) -> f32 {
    let track = animation.get_track(bone).unwrap();
    let mut total_deviation = 0.0;
    let mut samples = 0;

    // Sample motion path
    for t in (0..100).map(|i| i as f32 / 100.0) {
        let prev = track.position_at(t - 0.01);
        let curr = track.position_at(t);
        let next = track.position_at(t + 0.01);

        // Check if path curves smoothly
        let expected_next = curr + (curr - prev);
        let deviation = (next - expected_next).length();
        total_deviation += deviation;
        samples += 1;
    }

    1.0 - (total_deviation / samples as f32).min(1.0)
}
```

### Timing Variation Check

```rust
fn check_timing_quality(animation: &Animation) -> f32 {
    let velocities: Vec<f32> = (0..animation.frame_count() - 1)
        .map(|i| {
            let p0 = animation.root_position_at(i);
            let p1 = animation.root_position_at(i + 1);
            (p1 - p0).length()
        })
        .collect();

    // Check for variation (not constant velocity)
    let mean = velocities.iter().sum::<f32>() / velocities.len() as f32;
    let variance = velocities.iter()
        .map(|v| (v - mean).powi(2))
        .sum::<f32>() / velocities.len() as f32;

    // Higher variance = better timing
    (variance / mean.max(0.001)).min(1.0)
}
```
