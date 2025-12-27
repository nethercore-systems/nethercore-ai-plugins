//! Animation State Machine for blending mocap clips
//!
//! Manages transitions between animation states with smooth blending.
//! Supports mocap clips, procedural animations, and layered overlays.

use std::collections::{HashMap, HashSet};

// Re-use types from other examples
mod bvh_parser;
mod bvh_to_zx_converter;

use bvh_parser::BvhClip;
use bvh_to_zx_converter::{bvh_time_to_zx, BoneMatrix};

/// Animation source type
pub enum AnimSource {
    Mocap {
        clip: BvhClip,
        position_scale: f32,
    },
    Procedural(Box<dyn ProceduralAnim>),
}

/// Trait for procedural animation sources
pub trait ProceduralAnim: Send + Sync {
    fn sample(&self, time: f32) -> Vec<BoneMatrix>;
    fn duration(&self) -> f32;
    fn is_looping(&self) -> bool;
}

/// Single animation state
pub struct AnimState {
    pub name: String,
    pub source: AnimSource,
    pub speed: f32,
    pub looping: bool,
    pub time: f32,
}

impl AnimState {
    pub fn from_mocap(name: &str, clip: BvhClip) -> Self {
        Self {
            name: name.to_string(),
            source: AnimSource::Mocap {
                clip,
                position_scale: 0.01, // CMU default
            },
            speed: 1.0,
            looping: true,
            time: 0.0,
        }
    }

    pub fn with_scale(mut self, scale: f32) -> Self {
        if let AnimSource::Mocap { ref mut position_scale, .. } = self.source {
            *position_scale = scale;
        }
        self
    }

    pub fn with_speed(mut self, speed: f32) -> Self {
        self.speed = speed;
        self
    }

    pub fn non_looping(mut self) -> Self {
        self.looping = false;
        self
    }

    pub fn duration(&self) -> f32 {
        match &self.source {
            AnimSource::Mocap { clip, .. } => clip.duration(),
            AnimSource::Procedural(anim) => anim.duration(),
        }
    }

    pub fn sample(&self) -> Vec<BoneMatrix> {
        match &self.source {
            AnimSource::Mocap { clip, position_scale } => {
                bvh_time_to_zx(clip, self.time, *position_scale)
            }
            AnimSource::Procedural(anim) => anim.sample(self.time),
        }
    }
}

/// Transition condition
#[derive(Clone)]
pub enum TransitionCondition {
    /// Transition immediately
    Immediate,
    /// Wait for current animation to complete
    OnComplete,
    /// Transition when parameter exceeds threshold
    ParameterGreater(String, f32),
    /// Transition when parameter is below threshold
    ParameterLess(String, f32),
    /// Transition on trigger event
    Trigger(String),
}

/// State transition definition
pub struct Transition {
    pub from: String,
    pub to: String,
    pub duration: f32,
    pub condition: TransitionCondition,
}

impl Transition {
    pub fn new(from: &str, to: &str, duration: f32, condition: TransitionCondition) -> Self {
        Self {
            from: from.to_string(),
            to: to.to_string(),
            duration,
            condition,
        }
    }
}

/// Active blend operation
struct BlendState {
    from: String,
    to: String,
    progress: f32,
    duration: f32,
}

/// Animation state machine controller
pub struct AnimController {
    states: HashMap<String, AnimState>,
    transitions: Vec<Transition>,
    current_state: String,
    blend_state: Option<BlendState>,
    parameters: HashMap<String, f32>,
    triggers: HashSet<String>,
}

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

    /// Add an animation state
    pub fn add_state(&mut self, state: AnimState) {
        self.states.insert(state.name.clone(), state);
    }

    /// Add a transition rule
    pub fn add_transition(&mut self, transition: Transition) {
        self.transitions.push(transition);
    }

    /// Set a float parameter
    pub fn set_parameter(&mut self, name: &str, value: f32) {
        self.parameters.insert(name.to_string(), value);
    }

    /// Get a parameter value
    pub fn get_parameter(&self, name: &str) -> f32 {
        self.parameters.get(name).copied().unwrap_or(0.0)
    }

    /// Fire a trigger (consumed after one check)
    pub fn set_trigger(&mut self, name: &str) {
        self.triggers.insert(name.to_string());
    }

    /// Get current state name
    pub fn current_state(&self) -> &str {
        &self.current_state
    }

    /// Force immediate state change (no blend)
    pub fn force_state(&mut self, state_name: &str) {
        if self.states.contains_key(state_name) {
            self.current_state = state_name.to_string();
            self.blend_state = None;
            if let Some(state) = self.states.get_mut(state_name) {
                state.time = 0.0;
            }
        }
    }

    /// Update controller and return bone matrices
    pub fn update(&mut self, dt: f32) -> Vec<BoneMatrix> {
        // Update current state time
        if let Some(state) = self.states.get_mut(&self.current_state) {
            state.time += dt * state.speed;

            let duration = state.duration();
            if state.looping && state.time >= duration {
                state.time %= duration;
            }
        }

        // Update blend target time if blending
        if let Some(ref blend) = self.blend_state {
            if let Some(state) = self.states.get_mut(&blend.to) {
                state.time += dt * state.speed;
            }
        }

        // Check for new transitions (only if not currently blending)
        if self.blend_state.is_none() {
            self.check_transitions();
        }

        // Update blend progress
        if let Some(ref mut blend) = self.blend_state {
            blend.progress += dt / blend.duration;
            if blend.progress >= 1.0 {
                // Blend complete
                self.current_state = blend.to.clone();
                self.blend_state = None;
            }
        }

        // Clear triggers (they're one-shot)
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
                    if let Some(state) = self.states.get(&self.current_state) {
                        !state.looping && state.time >= state.duration()
                    } else {
                        false
                    }
                }
                TransitionCondition::ParameterGreater(name, threshold) => {
                    self.get_parameter(name) > *threshold
                }
                TransitionCondition::ParameterLess(name, threshold) => {
                    self.get_parameter(name) < *threshold
                }
                TransitionCondition::Trigger(name) => {
                    self.triggers.contains(name)
                }
            };

            if should_transition {
                // Reset target state time
                if let Some(state) = self.states.get_mut(&trans.to) {
                    state.time = 0.0;
                }

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

    fn sample_current(&self) -> Vec<BoneMatrix> {
        let from_pose = self.states.get(&self.current_state)
            .map(|s| s.sample())
            .unwrap_or_default();

        match &self.blend_state {
            Some(blend) => {
                let to_pose = self.states.get(&blend.to)
                    .map(|s| s.sample())
                    .unwrap_or_default();

                let t = ease_in_out(blend.progress);
                blend_poses(&from_pose, &to_pose, t)
            }
            None => from_pose,
        }
    }
}

/// Smooth easing function for blends
fn ease_in_out(t: f32) -> f32 {
    if t < 0.5 {
        2.0 * t * t
    } else {
        1.0 - (-2.0 * t + 2.0).powi(2) / 2.0
    }
}

/// Blend two pose arrays
pub fn blend_poses(from: &[BoneMatrix], to: &[BoneMatrix], t: f32) -> Vec<BoneMatrix> {
    if from.is_empty() {
        return to.to_vec();
    }
    if to.is_empty() {
        return from.to_vec();
    }

    from.iter()
        .zip(to.iter())
        .map(|(a, b)| blend_bone(a, b, t))
        .collect()
}

fn blend_bone(from: &BoneMatrix, to: &BoneMatrix, t: f32) -> BoneMatrix {
    // For simplicity, use linear interpolation
    // In production, extract rotation as quaternion and use slerp
    let mut result = [0.0f32; 12];
    for i in 0..12 {
        result[i] = from[i] + (to[i] - from[i]) * t;
    }

    // Renormalize rotation columns (first 9 elements form 3x3 rotation)
    normalize_rotation_matrix(&mut result);

    result
}

fn normalize_rotation_matrix(m: &mut BoneMatrix) {
    // Normalize X axis
    let len_x = (m[0] * m[0] + m[1] * m[1] + m[2] * m[2]).sqrt();
    if len_x > 0.0001 {
        m[0] /= len_x;
        m[1] /= len_x;
        m[2] /= len_x;
    }

    // Orthogonalize Y axis
    let dot = m[0] * m[3] + m[1] * m[4] + m[2] * m[5];
    m[3] -= dot * m[0];
    m[4] -= dot * m[1];
    m[5] -= dot * m[2];

    // Normalize Y axis
    let len_y = (m[3] * m[3] + m[4] * m[4] + m[5] * m[5]).sqrt();
    if len_y > 0.0001 {
        m[3] /= len_y;
        m[4] /= len_y;
        m[5] /= len_y;
    }

    // Z axis = X cross Y
    m[6] = m[1] * m[5] - m[2] * m[4];
    m[7] = m[2] * m[3] - m[0] * m[5];
    m[8] = m[0] * m[4] - m[1] * m[3];
}

// ============================================================================
// 1D Blend Tree
// ============================================================================

/// 1D blend tree for locomotion (idle -> walk -> run)
pub struct BlendTree1D {
    entries: Vec<(AnimSource, f32)>, // (source, threshold)
    parameter: String,
}

impl BlendTree1D {
    pub fn new(parameter: &str) -> Self {
        Self {
            entries: Vec::new(),
            parameter: parameter.to_string(),
        }
    }

    pub fn add_mocap(&mut self, clip: BvhClip, threshold: f32, position_scale: f32) {
        self.entries.push((
            AnimSource::Mocap { clip, position_scale },
            threshold,
        ));
        self.entries.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap());
    }

    pub fn sample(&self, param_value: f32, time: f32) -> Vec<BoneMatrix> {
        if self.entries.is_empty() {
            return Vec::new();
        }

        // Find surrounding entries
        let mut lower_idx = 0;
        let mut upper_idx = 0;

        for (i, (_, threshold)) in self.entries.iter().enumerate() {
            if *threshold <= param_value {
                lower_idx = i;
            }
            if *threshold >= param_value && upper_idx == 0 {
                upper_idx = i;
            }
        }
        upper_idx = upper_idx.max(lower_idx);

        // Sample sources
        let sample_source = |source: &AnimSource, time: f32| -> Vec<BoneMatrix> {
            match source {
                AnimSource::Mocap { clip, position_scale } => {
                    bvh_time_to_zx(clip, time, *position_scale)
                }
                AnimSource::Procedural(anim) => anim.sample(time),
            }
        };

        if lower_idx == upper_idx {
            return sample_source(&self.entries[lower_idx].0, time);
        }

        let lower_threshold = self.entries[lower_idx].1;
        let upper_threshold = self.entries[upper_idx].1;
        let t = (param_value - lower_threshold) / (upper_threshold - lower_threshold);

        let lower_pose = sample_source(&self.entries[lower_idx].0, time);
        let upper_pose = sample_source(&self.entries[upper_idx].0, time);

        blend_poses(&lower_pose, &upper_pose, t)
    }
}

// ============================================================================
// Layer System
// ============================================================================

/// Bone mask for layer blending
#[derive(Clone)]
pub enum BoneMask {
    All,
    Only(Vec<usize>),
    Except(Vec<usize>),
}

impl BoneMask {
    fn affects(&self, bone_idx: usize) -> bool {
        match self {
            BoneMask::All => true,
            BoneMask::Only(indices) => indices.contains(&bone_idx),
            BoneMask::Except(indices) => !indices.contains(&bone_idx),
        }
    }

    /// Upper body only (for aiming while walking)
    pub fn upper_body() -> Self {
        BoneMask::Only(vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    }

    /// Lower body only
    pub fn lower_body() -> Self {
        BoneMask::Only(vec![0, 13, 14, 15, 16, 17, 18, 19, 20])
    }
}

/// Animation layer for blending
pub struct AnimLayer {
    pub name: String,
    pub weight: f32,
    pub mask: BoneMask,
    pub state: AnimState,
}

/// Multi-layer animation system
pub struct LayeredAnimator {
    base_controller: AnimController,
    overlay_layers: Vec<AnimLayer>,
}

impl LayeredAnimator {
    pub fn new(base: AnimController) -> Self {
        Self {
            base_controller: base,
            overlay_layers: Vec::new(),
        }
    }

    pub fn add_layer(&mut self, layer: AnimLayer) {
        self.overlay_layers.push(layer);
    }

    pub fn set_layer_weight(&mut self, name: &str, weight: f32) {
        if let Some(layer) = self.overlay_layers.iter_mut().find(|l| l.name == name) {
            layer.weight = weight.clamp(0.0, 1.0);
        }
    }

    pub fn update(&mut self, dt: f32) -> Vec<BoneMatrix> {
        // Update base controller
        let mut result = self.base_controller.update(dt);

        // Apply overlay layers
        for layer in &mut self.overlay_layers {
            if layer.weight <= 0.0 {
                continue;
            }

            // Update layer time
            layer.state.time += dt * layer.state.speed;
            if layer.state.looping {
                layer.state.time %= layer.state.duration();
            }

            // Sample layer
            let layer_pose = layer.state.sample();

            // Blend masked bones
            for (i, bone) in result.iter_mut().enumerate() {
                if layer.mask.affects(i) && i < layer_pose.len() {
                    *bone = blend_bone(bone, &layer_pose[i], layer.weight);
                }
            }
        }

        result
    }

    pub fn base(&mut self) -> &mut AnimController {
        &mut self.base_controller
    }
}

// ============================================================================
// Usage Example
// ============================================================================

fn main() {
    // Load some BVH clips
    let idle_clip = BvhClip::parse(&std::fs::read_to_string("idle.bvh").unwrap()).unwrap();
    let walk_clip = BvhClip::parse(&std::fs::read_to_string("walk.bvh").unwrap()).unwrap();
    let run_clip = BvhClip::parse(&std::fs::read_to_string("run.bvh").unwrap()).unwrap();
    let attack_clip = BvhClip::parse(&std::fs::read_to_string("attack.bvh").unwrap()).unwrap();

    // Create animation controller
    let mut controller = AnimController::new("idle");

    // Add states
    controller.add_state(AnimState::from_mocap("idle", idle_clip));
    controller.add_state(AnimState::from_mocap("walk", walk_clip));
    controller.add_state(AnimState::from_mocap("run", run_clip));
    controller.add_state(
        AnimState::from_mocap("attack", attack_clip)
            .with_speed(1.5)
            .non_looping()
    );

    // Add transitions
    controller.add_transition(Transition::new(
        "idle", "walk", 0.2,
        TransitionCondition::ParameterGreater("speed".into(), 0.5),
    ));

    controller.add_transition(Transition::new(
        "walk", "idle", 0.2,
        TransitionCondition::ParameterLess("speed".into(), 0.3),
    ));

    controller.add_transition(Transition::new(
        "walk", "run", 0.15,
        TransitionCondition::ParameterGreater("speed".into(), 2.0),
    ));

    controller.add_transition(Transition::new(
        "run", "walk", 0.15,
        TransitionCondition::ParameterLess("speed".into(), 1.5),
    ));

    // Attack can interrupt any locomotion state
    for state in ["idle", "walk", "run"] {
        controller.add_transition(Transition::new(
            state, "attack", 0.1,
            TransitionCondition::Trigger("attack".into()),
        ));
    }

    controller.add_transition(Transition::new(
        "attack", "idle", 0.3,
        TransitionCondition::OnComplete,
    ));

    // Game loop simulation
    let dt = 1.0 / 60.0;
    let mut time = 0.0;

    for frame in 0..300 {
        // Simulate input
        let speed = if frame < 60 {
            0.0  // Idle
        } else if frame < 120 {
            1.0  // Walking
        } else if frame < 180 {
            3.0  // Running
        } else {
            1.0  // Back to walking
        };

        controller.set_parameter("speed", speed);

        // Trigger attack at frame 100
        if frame == 100 {
            controller.set_trigger("attack");
        }

        // Update and get bone matrices
        let bones = controller.update(dt);

        // In a real game: set_bones(bones.as_ptr(), bones.len());

        if frame % 30 == 0 {
            println!(
                "Frame {}: state={}, speed={:.1}, bones={}",
                frame,
                controller.current_state(),
                speed,
                bones.len()
            );
        }

        time += dt;
    }
}
