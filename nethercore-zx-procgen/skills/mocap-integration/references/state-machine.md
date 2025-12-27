# Animation State Machine Reference

Managing transitions and blending between motion capture clips and procedural animations.

## State Machine Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Animation Controller                      │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │    Idle     │◄──►│    Walk     │◄──►│    Run      │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │    Jump     │    │   Attack    │    │    Dodge    │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
├──────────────────────────────────────────────────────────────┤
│                        Blend Layer                           │
│  [Base Mocap] + [Procedural Overlay] + [IK Adjustment]       │
└──────────────────────────────────────────────────────────────┘
```

## Core Data Structures

```rust
/// Animation clip reference (mocap or procedural)
#[derive(Clone)]
pub enum AnimSource {
    Mocap(BvhClip),
    Procedural(Box<dyn ProceduralAnim>),
}

/// Single animation state
#[derive(Clone)]
pub struct AnimState {
    pub name: String,
    pub source: AnimSource,
    pub speed: f32,
    pub looping: bool,
    pub time: f32,
}

/// Transition between states
#[derive(Clone)]
pub struct Transition {
    pub from: String,
    pub to: String,
    pub duration: f32,
    pub condition: TransitionCondition,
}

#[derive(Clone)]
pub enum TransitionCondition {
    Immediate,
    OnComplete,
    Parameter(String, f32),  // param name, threshold
    Trigger(String),
}

/// Complete animation controller
pub struct AnimController {
    states: HashMap<String, AnimState>,
    transitions: Vec<Transition>,
    current_state: String,
    blend_state: Option<BlendState>,
    parameters: HashMap<String, f32>,
    triggers: HashSet<String>,
}

struct BlendState {
    from: String,
    to: String,
    progress: f32,
    duration: f32,
}
```

## State Machine Implementation

```rust
impl AnimController {
    pub fn new(initial_state: &str) -> Self {
        Self {
            states: HashMap::new(),
            transitions: Vec::new(),
            current_state: initial_state.to_string(),
            blend_state: None,
            parameters: HashMap::new(),
            triggers: HashSet::new(),
        }
    }

    pub fn add_state(&mut self, state: AnimState) {
        self.states.insert(state.name.clone(), state);
    }

    pub fn add_transition(&mut self, transition: Transition) {
        self.transitions.push(transition);
    }

    pub fn set_parameter(&mut self, name: &str, value: f32) {
        self.parameters.insert(name.to_string(), value);
    }

    pub fn set_trigger(&mut self, name: &str) {
        self.triggers.insert(name.to_string());
    }

    pub fn update(&mut self, dt: f32) -> Vec<[f32; 12]> {
        // Update current state time
        if let Some(state) = self.states.get_mut(&self.current_state) {
            state.time += dt * state.speed;

            if state.looping {
                let duration = state.duration();
                if state.time >= duration {
                    state.time %= duration;
                }
            }
        }

        // Check transitions
        if self.blend_state.is_none() {
            self.check_transitions();
        }

        // Update blend
        if let Some(ref mut blend) = self.blend_state {
            blend.progress += dt / blend.duration;
            if blend.progress >= 1.0 {
                self.current_state = blend.to.clone();
                self.blend_state = None;
            }
        }

        // Clear triggers
        self.triggers.clear();

        // Sample and blend
        self.sample_current()
    }

    fn check_transitions(&mut self) {
        for trans in &self.transitions {
            if trans.from != self.current_state {
                continue;
            }

            let should_transition = match &trans.condition {
                TransitionCondition::Immediate => true,
                TransitionCondition::OnComplete => {
                    let state = &self.states[&self.current_state];
                    !state.looping && state.time >= state.duration()
                }
                TransitionCondition::Parameter(name, threshold) => {
                    self.parameters.get(name).unwrap_or(&0.0) >= threshold
                }
                TransitionCondition::Trigger(name) => {
                    self.triggers.contains(name)
                }
            };

            if should_transition {
                self.blend_state = Some(BlendState {
                    from: trans.from.clone(),
                    to: trans.to.clone(),
                    progress: 0.0,
                    duration: trans.duration,
                });
                break;
            }
        }
    }

    fn sample_current(&self) -> Vec<[f32; 12]> {
        let from_state = &self.states[&self.current_state];
        let from_pose = sample_state(from_state);

        match &self.blend_state {
            Some(blend) => {
                let to_state = &self.states[&blend.to];
                let to_pose = sample_state(to_state);
                blend_poses(&from_pose, &to_pose, blend.progress)
            }
            None => from_pose,
        }
    }
}
```

## Pose Blending

### Linear Interpolation

```rust
/// Blend two pose arrays
pub fn blend_poses(
    from: &[[f32; 12]],
    to: &[[f32; 12]],
    t: f32,
) -> Vec<[f32; 12]> {
    from.iter()
        .zip(to.iter())
        .map(|(a, b)| blend_bone(a, b, t))
        .collect()
}

fn blend_bone(from: &[f32; 12], to: &[f32; 12], t: f32) -> [f32; 12] {
    // Extract rotation matrices
    let rot_from = extract_rotation(from);
    let rot_to = extract_rotation(to);

    // Convert to quaternions for smooth interpolation
    let quat_from = mat3_to_quat(&rot_from);
    let quat_to = mat3_to_quat(&rot_to);
    let quat_blend = slerp(&quat_from, &quat_to, t);
    let rot_blend = quat_to_mat3(&quat_blend);

    // Lerp translation
    let tx = from[9] + (to[9] - from[9]) * t;
    let ty = from[10] + (to[10] - from[10]) * t;
    let tz = from[11] + (to[11] - from[11]) * t;

    [
        rot_blend[0][0], rot_blend[0][1], rot_blend[0][2],
        rot_blend[1][0], rot_blend[1][1], rot_blend[1][2],
        rot_blend[2][0], rot_blend[2][1], rot_blend[2][2],
        tx, ty, tz,
    ]
}
```

### Spherical Linear Interpolation (Slerp)

```rust
/// Quaternion slerp for smooth rotation blending
pub fn slerp(from: &[f32; 4], to: &[f32; 4], t: f32) -> [f32; 4] {
    let mut dot = from[0]*to[0] + from[1]*to[1] + from[2]*to[2] + from[3]*to[3];

    // Handle opposite quaternions
    let to = if dot < 0.0 {
        dot = -dot;
        [-to[0], -to[1], -to[2], -to[3]]
    } else {
        *to
    };

    // Use lerp for nearly parallel quaternions
    if dot > 0.9995 {
        return normalize_quat([
            from[0] + (to[0] - from[0]) * t,
            from[1] + (to[1] - from[1]) * t,
            from[2] + (to[2] - from[2]) * t,
            from[3] + (to[3] - from[3]) * t,
        ]);
    }

    let theta = dot.acos();
    let sin_theta = theta.sin();
    let from_weight = ((1.0 - t) * theta).sin() / sin_theta;
    let to_weight = (t * theta).sin() / sin_theta;

    [
        from[0] * from_weight + to[0] * to_weight,
        from[1] * from_weight + to[1] * to_weight,
        from[2] * from_weight + to[2] * to_weight,
        from[3] * from_weight + to[3] * to_weight,
    ]
}
```

## Blend Trees

For smooth locomotion based on speed:

```rust
/// 1D blend tree (e.g., idle -> walk -> run)
pub struct BlendTree1D {
    entries: Vec<BlendEntry>,
    parameter: String,
}

struct BlendEntry {
    clip: AnimSource,
    threshold: f32,
}

impl BlendTree1D {
    pub fn new(parameter: &str) -> Self {
        Self {
            entries: Vec::new(),
            parameter: parameter.to_string(),
        }
    }

    pub fn add(&mut self, clip: AnimSource, threshold: f32) {
        self.entries.push(BlendEntry { clip, threshold });
        self.entries.sort_by(|a, b| a.threshold.partial_cmp(&b.threshold).unwrap());
    }

    pub fn sample(&self, param_value: f32, time: f32) -> Vec<[f32; 12]> {
        // Find surrounding entries
        let mut lower_idx = 0;
        let mut upper_idx = 0;

        for (i, entry) in self.entries.iter().enumerate() {
            if entry.threshold <= param_value {
                lower_idx = i;
            }
            if entry.threshold >= param_value {
                upper_idx = i;
                break;
            }
        }

        if lower_idx == upper_idx {
            return sample_source(&self.entries[lower_idx].clip, time);
        }

        let lower = &self.entries[lower_idx];
        let upper = &self.entries[upper_idx];
        let t = (param_value - lower.threshold) / (upper.threshold - lower.threshold);

        let lower_pose = sample_source(&lower.clip, time);
        let upper_pose = sample_source(&upper.clip, time);
        blend_poses(&lower_pose, &upper_pose, t)
    }
}

// Usage
fn create_locomotion_tree() -> BlendTree1D {
    let mut tree = BlendTree1D::new("speed");
    tree.add(AnimSource::Mocap(load_clip("idle")), 0.0);
    tree.add(AnimSource::Mocap(load_clip("walk")), 1.0);
    tree.add(AnimSource::Mocap(load_clip("run")), 3.0);
    tree
}
```

## Layer System

Combine base animation with overlays:

```rust
/// Animation layer for blending
pub struct AnimLayer {
    pub name: String,
    pub weight: f32,
    pub mask: BoneMask,
    pub source: AnimSource,
}

/// Which bones this layer affects
#[derive(Clone)]
pub enum BoneMask {
    All,
    Only(Vec<usize>),
    Except(Vec<usize>),
}

/// Multi-layer animation system
pub struct LayeredAnimator {
    base_layer: AnimSource,
    overlay_layers: Vec<AnimLayer>,
}

impl LayeredAnimator {
    pub fn sample(&self, time: f32) -> Vec<[f32; 12]> {
        let mut result = sample_source(&self.base_layer, time);

        for layer in &self.overlay_layers {
            if layer.weight <= 0.0 { continue; }

            let layer_pose = sample_source(&layer.source, time);

            for (i, bone) in result.iter_mut().enumerate() {
                if layer.mask.affects(i) {
                    *bone = blend_bone(bone, &layer_pose[i], layer.weight);
                }
            }
        }

        result
    }
}

impl BoneMask {
    fn affects(&self, bone_idx: usize) -> bool {
        match self {
            BoneMask::All => true,
            BoneMask::Only(indices) => indices.contains(&bone_idx),
            BoneMask::Except(indices) => !indices.contains(&bone_idx),
        }
    }
}
```

## Procedural Overlays

Add procedural motion on top of mocap:

```rust
/// Apply procedural overlay to mocap base
pub fn apply_overlay(
    base: &[[f32; 12]],
    overlay: &ProceduralOverlay,
    time: f32,
) -> Vec<[f32; 12]> {
    let mut result = base.to_vec();

    // Head look-at
    if let Some(look_target) = overlay.look_at {
        let head_idx = overlay.head_bone;
        let look_rot = calculate_look_rotation(
            extract_position(&result[head_idx]),
            look_target
        );
        result[head_idx] = apply_additive_rotation(&result[head_idx], look_rot);
    }

    // Breathing
    if overlay.breathing > 0.0 {
        let breath = 1.0 + (time * 2.0).sin() * 0.02 * overlay.breathing;
        let chest_idx = overlay.chest_bone;
        result[chest_idx] = apply_scale(&result[chest_idx], [1.0, breath, 1.0]);
    }

    // Arm swing modifier
    if overlay.arm_swing != 1.0 {
        for &idx in &overlay.arm_bones {
            // Amplify or dampen arm rotation
            result[idx] = scale_rotation(&result[idx], overlay.arm_swing);
        }
    }

    result
}

pub struct ProceduralOverlay {
    pub look_at: Option<[f32; 3]>,
    pub breathing: f32,
    pub arm_swing: f32,
    pub head_bone: usize,
    pub chest_bone: usize,
    pub arm_bones: Vec<usize>,
}
```

## Transition Curves

Smoother blending with easing:

```rust
/// Easing functions for transitions
pub fn ease_in_out(t: f32) -> f32 {
    if t < 0.5 {
        2.0 * t * t
    } else {
        1.0 - (-2.0 * t + 2.0).powi(2) / 2.0
    }
}

pub fn ease_out_cubic(t: f32) -> f32 {
    1.0 - (1.0 - t).powi(3)
}

pub fn ease_in_cubic(t: f32) -> f32 {
    t.powi(3)
}

// Use in blending
fn sample_with_easing(&self) -> Vec<[f32; 12]> {
    if let Some(blend) = &self.blend_state {
        let eased_t = ease_in_out(blend.progress);
        let from = sample_state(&self.states[&blend.from]);
        let to = sample_state(&self.states[&blend.to]);
        blend_poses(&from, &to, eased_t)
    } else {
        sample_state(&self.states[&self.current_state])
    }
}
```

## Complete Usage Example

```rust
fn setup_character_animator() -> AnimController {
    let mut controller = AnimController::new("idle");

    // Add states
    controller.add_state(AnimState {
        name: "idle".into(),
        source: AnimSource::Mocap(load_clip("35_01")),
        speed: 1.0,
        looping: true,
        time: 0.0,
    });

    controller.add_state(AnimState {
        name: "walk".into(),
        source: AnimSource::Mocap(load_clip("01_01")),
        speed: 1.0,
        looping: true,
        time: 0.0,
    });

    controller.add_state(AnimState {
        name: "attack".into(),
        source: AnimSource::Mocap(load_clip("14_01")),
        speed: 1.5,
        looping: false,
        time: 0.0,
    });

    // Add transitions
    controller.add_transition(Transition {
        from: "idle".into(),
        to: "walk".into(),
        duration: 0.2,
        condition: TransitionCondition::Parameter("speed".into(), 0.5),
    });

    controller.add_transition(Transition {
        from: "walk".into(),
        to: "idle".into(),
        duration: 0.2,
        condition: TransitionCondition::Parameter("speed".into(), 0.0),
    });

    controller.add_transition(Transition {
        from: "idle".into(),
        to: "attack".into(),
        duration: 0.1,
        condition: TransitionCondition::Trigger("attack".into()),
    });

    controller.add_transition(Transition {
        from: "attack".into(),
        to: "idle".into(),
        duration: 0.3,
        condition: TransitionCondition::OnComplete,
    });

    controller
}

// In game loop
fn update(controller: &mut AnimController, input: &Input, dt: f32) {
    controller.set_parameter("speed", input.movement_speed);

    if input.attack_pressed {
        controller.set_trigger("attack");
    }

    let bones = controller.update(dt);
    set_bones(bones.as_ptr(), bones.len());
}
```
