//! Skeleton retargeting example
//!
//! Demonstrates mapping motion capture data from CMU skeleton to a custom game skeleton
//! with different bone counts and proportions.

use std::collections::HashMap;

// Re-use types from other examples
mod bvh_parser;
use bvh_parser::{BvhClip, BvhJoint, JointTransform};

/// Identity quaternion for no rotation correction
pub const IDENTITY_QUAT: [f32; 4] = [1.0, 0.0, 0.0, 0.0];

/// Mapping from source skeleton bone to target skeleton bone
#[derive(Clone)]
pub struct BoneMapping {
    pub source_name: String,
    pub target_index: usize,
    pub rotation_offset: [f32; 4],  // T-pose correction quaternion
    pub position_scale: f32,         // Limb length ratio
}

impl BoneMapping {
    pub fn new(source: &str, target: usize) -> Self {
        Self {
            source_name: source.to_string(),
            target_index: target,
            rotation_offset: IDENTITY_QUAT,
            position_scale: 1.0,
        }
    }

    pub fn with_scale(mut self, scale: f32) -> Self {
        self.position_scale = scale;
        self
    }

    pub fn with_rotation(mut self, quat: [f32; 4]) -> Self {
        self.rotation_offset = quat;
        self
    }
}

/// Complete skeleton mapping configuration
pub struct SkeletonMap {
    pub mappings: Vec<BoneMapping>,
    source_to_target: HashMap<String, usize>,
}

impl SkeletonMap {
    pub fn from_mappings(mappings: Vec<BoneMapping>) -> Self {
        let source_to_target: HashMap<String, usize> = mappings
            .iter()
            .map(|m| (m.source_name.clone(), m.target_index))
            .collect();
        Self {
            mappings,
            source_to_target,
        }
    }

    /// Standard CMU skeleton to 20-bone humanoid
    pub fn cmu_to_humanoid() -> Self {
        let mappings = vec![
            // Spine chain (5 bones)
            BoneMapping::new("Hips", 0),
            BoneMapping::new("Spine", 1),
            BoneMapping::new("Spine1", 2),
            BoneMapping::new("Neck", 3),
            BoneMapping::new("Head", 4),

            // Left arm (4 bones)
            BoneMapping::new("LeftShoulder", 5),
            BoneMapping::new("LeftArm", 6),
            BoneMapping::new("LeftForeArm", 7),
            BoneMapping::new("LeftHand", 8),

            // Right arm (4 bones)
            BoneMapping::new("RightShoulder", 9),
            BoneMapping::new("RightArm", 10),
            BoneMapping::new("RightForeArm", 11),
            BoneMapping::new("RightHand", 12),

            // Left leg (4 bones)
            BoneMapping::new("LeftUpLeg", 13),
            BoneMapping::new("LeftLeg", 14),
            BoneMapping::new("LeftFoot", 15),
            BoneMapping::new("LeftToeBase", 16),

            // Right leg (4 bones)
            BoneMapping::new("RightUpLeg", 17),
            BoneMapping::new("RightLeg", 18),
            BoneMapping::new("RightFoot", 19),
            BoneMapping::new("RightToeBase", 20),
        ];

        Self::from_mappings(mappings)
    }

    /// Minimal skeleton (12 bones) for low-poly characters
    pub fn cmu_to_minimal() -> Self {
        let mappings = vec![
            BoneMapping::new("Hips", 0),
            BoneMapping::new("Spine1", 1),    // Skip lower spine
            BoneMapping::new("Head", 2),       // Skip neck
            BoneMapping::new("LeftArm", 3),    // Skip shoulder
            BoneMapping::new("LeftForeArm", 4),
            BoneMapping::new("RightArm", 5),
            BoneMapping::new("RightForeArm", 6),
            BoneMapping::new("LeftUpLeg", 7),
            BoneMapping::new("LeftLeg", 8),
            BoneMapping::new("RightUpLeg", 9),
            BoneMapping::new("RightLeg", 10),
            BoneMapping::new("LeftFoot", 11),
            BoneMapping::new("RightFoot", 12),
        ];

        Self::from_mappings(mappings)
    }

    /// Mixamo skeleton to humanoid
    pub fn mixamo_to_humanoid() -> Self {
        let mappings = vec![
            BoneMapping::new("mixamorig:Hips", 0),
            BoneMapping::new("mixamorig:Spine", 1),
            BoneMapping::new("mixamorig:Spine1", 2),
            BoneMapping::new("mixamorig:Neck", 3),
            BoneMapping::new("mixamorig:Head", 4),
            BoneMapping::new("mixamorig:LeftShoulder", 5),
            BoneMapping::new("mixamorig:LeftArm", 6),
            BoneMapping::new("mixamorig:LeftForeArm", 7),
            BoneMapping::new("mixamorig:LeftHand", 8),
            BoneMapping::new("mixamorig:RightShoulder", 9),
            BoneMapping::new("mixamorig:RightArm", 10),
            BoneMapping::new("mixamorig:RightForeArm", 11),
            BoneMapping::new("mixamorig:RightHand", 12),
            BoneMapping::new("mixamorig:LeftUpLeg", 13),
            BoneMapping::new("mixamorig:LeftLeg", 14),
            BoneMapping::new("mixamorig:LeftFoot", 15),
            BoneMapping::new("mixamorig:LeftToeBase", 16),
            BoneMapping::new("mixamorig:RightUpLeg", 17),
            BoneMapping::new("mixamorig:RightLeg", 18),
            BoneMapping::new("mixamorig:RightFoot", 19),
            BoneMapping::new("mixamorig:RightToeBase", 20),
        ];

        Self::from_mappings(mappings)
    }

    /// Get target index for source bone name
    pub fn get_target(&self, source_name: &str) -> Option<usize> {
        self.source_to_target.get(source_name).copied()
    }
}

/// Retarget a single frame from source to target skeleton
pub fn retarget_frame(
    source_clip: &BvhClip,
    frame: usize,
    skeleton_map: &SkeletonMap,
    target_bone_count: usize,
    position_scale: f32,
) -> Vec<JointTransform> {
    let mut target_poses = vec![JointTransform::default(); target_bone_count];

    for mapping in &skeleton_map.mappings {
        // Find source joint by name
        let source_idx = source_clip
            .joints
            .iter()
            .position(|j| j.name == mapping.source_name);

        if let Some(src_idx) = source_idx {
            let source_pose = source_clip.sample_joint(src_idx, frame);

            // Apply position scaling
            let scaled_pos = [
                source_pose.position[0] * position_scale * mapping.position_scale,
                source_pose.position[1] * position_scale * mapping.position_scale,
                source_pose.position[2] * position_scale * mapping.position_scale,
            ];

            // Apply rotation correction if needed
            let corrected_rot = if mapping.rotation_offset != IDENTITY_QUAT {
                apply_rotation_offset(&source_pose.rotation, &mapping.rotation_offset)
            } else {
                source_pose.rotation
            };

            if mapping.target_index < target_bone_count {
                target_poses[mapping.target_index] = JointTransform {
                    position: scaled_pos,
                    rotation: corrected_rot,
                };
            }
        }
    }

    target_poses
}

/// Apply quaternion rotation offset to Euler angles
fn apply_rotation_offset(euler_deg: &[f32; 3], offset_quat: &[f32; 4]) -> [f32; 3] {
    // Convert euler to quat
    let source_quat = euler_to_quat(euler_deg);

    // Multiply quaternions
    let result_quat = quat_multiply(&source_quat, offset_quat);

    // Convert back to euler
    quat_to_euler(&result_quat)
}

fn euler_to_quat(euler_deg: &[f32; 3]) -> [f32; 4] {
    use std::f32::consts::PI;

    let x = euler_deg[0] * PI / 180.0;
    let y = euler_deg[1] * PI / 180.0;
    let z = euler_deg[2] * PI / 180.0;

    let (sx, cx) = (x * 0.5).sin_cos();
    let (sy, cy) = (y * 0.5).sin_cos();
    let (sz, cz) = (z * 0.5).sin_cos();

    [
        cz * cx * cy + sz * sx * sy,
        cz * sx * cy + sz * cx * sy,
        cz * cx * sy - sz * sx * cy,
        sz * cx * cy - cz * sx * sy,
    ]
}

fn quat_to_euler(q: &[f32; 4]) -> [f32; 3] {
    use std::f32::consts::PI;

    let (w, x, y, z) = (q[0], q[1], q[2], q[3]);

    // Roll (X)
    let sinr_cosp = 2.0 * (w * x + y * z);
    let cosr_cosp = 1.0 - 2.0 * (x * x + y * y);
    let roll = sinr_cosp.atan2(cosr_cosp);

    // Pitch (Y)
    let sinp = 2.0 * (w * y - z * x);
    let pitch = if sinp.abs() >= 1.0 {
        (PI / 2.0).copysign(sinp)
    } else {
        sinp.asin()
    };

    // Yaw (Z)
    let siny_cosp = 2.0 * (w * z + x * y);
    let cosy_cosp = 1.0 - 2.0 * (y * y + z * z);
    let yaw = siny_cosp.atan2(cosy_cosp);

    [roll * 180.0 / PI, pitch * 180.0 / PI, yaw * 180.0 / PI]
}

fn quat_multiply(a: &[f32; 4], b: &[f32; 4]) -> [f32; 4] {
    [
        a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3],
        a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2],
        a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1],
        a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0],
    ]
}

// ============================================================================
// Proportional Scaling
// ============================================================================

/// Calculate limb length ratios between source and target skeletons
pub struct LimbProportions {
    pub upper_arm: f32,
    pub forearm: f32,
    pub thigh: f32,
    pub shin: f32,
    pub spine: f32,
}

impl LimbProportions {
    /// Calculate from BVH skeleton and target measurements
    pub fn from_skeletons(
        source_joints: &[BvhJoint],
        target: &TargetSkeleton,
    ) -> Self {
        // Measure source limb lengths from bone offsets
        let src_upper_arm = offset_length_between(source_joints, "LeftArm", "LeftForeArm");
        let src_forearm = offset_length_between(source_joints, "LeftForeArm", "LeftHand");
        let src_thigh = offset_length_between(source_joints, "LeftUpLeg", "LeftLeg");
        let src_shin = offset_length_between(source_joints, "LeftLeg", "LeftFoot");
        let src_spine = measure_spine_length(source_joints);

        Self {
            upper_arm: target.upper_arm_length / src_upper_arm.max(0.001),
            forearm: target.forearm_length / src_forearm.max(0.001),
            thigh: target.thigh_length / src_thigh.max(0.001),
            shin: target.shin_length / src_shin.max(0.001),
            spine: target.spine_length / src_spine.max(0.001),
        }
    }

    /// Apply proportions to bone mapping
    pub fn apply_to_mapping(&self, map: &mut SkeletonMap) {
        for mapping in &mut map.mappings {
            let scale = match mapping.source_name.as_str() {
                name if name.contains("Arm") && !name.contains("Fore") => self.upper_arm,
                name if name.contains("ForeArm") => self.forearm,
                name if name.contains("UpLeg") => self.thigh,
                name if name.contains("Leg") && !name.contains("Up") => self.shin,
                name if name.contains("Spine") => self.spine,
                _ => 1.0,
            };
            mapping.position_scale = scale;
        }
    }
}

/// Target skeleton measurements
pub struct TargetSkeleton {
    pub upper_arm_length: f32,
    pub forearm_length: f32,
    pub thigh_length: f32,
    pub shin_length: f32,
    pub spine_length: f32,
}

impl TargetSkeleton {
    /// Standard human proportions (in meters)
    pub fn standard_human() -> Self {
        Self {
            upper_arm_length: 0.28,
            forearm_length: 0.25,
            thigh_length: 0.42,
            shin_length: 0.40,
            spine_length: 0.45,
        }
    }

    /// Stylized proportions (larger head, shorter limbs)
    pub fn stylized() -> Self {
        Self {
            upper_arm_length: 0.22,
            forearm_length: 0.20,
            thigh_length: 0.35,
            shin_length: 0.32,
            spine_length: 0.35,
        }
    }
}

fn offset_length_between(joints: &[BvhJoint], from: &str, to: &str) -> f32 {
    if let Some(to_joint) = joints.iter().find(|j| j.name == to) {
        let o = to_joint.offset;
        (o[0] * o[0] + o[1] * o[1] + o[2] * o[2]).sqrt()
    } else {
        1.0
    }
}

fn measure_spine_length(joints: &[BvhJoint]) -> f32 {
    let spine_bones = ["Spine", "Spine1", "Neck"];
    let mut total = 0.0;

    for name in spine_bones {
        if let Some(joint) = joints.iter().find(|j| j.name == name) {
            let o = joint.offset;
            total += (o[0] * o[0] + o[1] * o[1] + o[2] * o[2]).sqrt();
        }
    }

    total
}

// ============================================================================
// Auto-mapping with fuzzy name matching
// ============================================================================

/// Generate skeleton mapping by fuzzy name matching
pub fn auto_generate_mapping(
    source_joints: &[BvhJoint],
    target_bone_names: &[&str],
) -> SkeletonMap {
    let mut mappings = Vec::new();

    for (target_idx, target_name) in target_bone_names.iter().enumerate() {
        // Find best matching source bone
        if let Some((_, source_name)) = source_joints
            .iter()
            .filter(|j| fuzzy_bone_match(&j.name, target_name))
            .map(|j| (0, j.name.clone()))
            .next()
        {
            mappings.push(BoneMapping::new(&source_name, target_idx));
        }
    }

    SkeletonMap::from_mappings(mappings)
}

/// Fuzzy match bone names across naming conventions
fn fuzzy_bone_match(source: &str, target: &str) -> bool {
    let source = normalize_bone_name(source);
    let target = normalize_bone_name(target);
    source == target
}

fn normalize_bone_name(name: &str) -> String {
    let name = name.to_lowercase();

    // Remove common prefixes
    let name = name
        .replace("mixamorig:", "")
        .replace(":", "")
        .replace("_", "")
        .replace(".", "")
        .replace("-", "");

    // Normalize left/right
    let name = name
        .replace("left", "l")
        .replace("right", "r");

    // Normalize common variations
    let name = name
        .replace("upleg", "thigh")
        .replace("forearm", "lowerarm")
        .replace("upperarm", "arm");

    name
}

// ============================================================================
// Debug utilities
// ============================================================================

/// Print mapping debug information
pub fn debug_mapping(
    source_joints: &[BvhJoint],
    target_bone_count: usize,
    map: &SkeletonMap,
) {
    println!("=== Retarget Mapping Debug ===");
    println!("Source joints: {}", source_joints.len());
    println!("Target bones: {}", target_bone_count);
    println!("Mappings: {}", map.mappings.len());
    println!();

    // Check unmapped source bones
    let mapped_sources: std::collections::HashSet<_> =
        map.mappings.iter().map(|m| m.source_name.as_str()).collect();

    println!("Unmapped source bones:");
    for joint in source_joints {
        if !mapped_sources.contains(joint.name.as_str()) {
            println!("  - {}", joint.name);
        }
    }
    println!();

    // Check unmapped target indices
    let mapped_targets: std::collections::HashSet<_> =
        map.mappings.iter().map(|m| m.target_index).collect();

    println!("Unmapped target indices:");
    for i in 0..target_bone_count {
        if !mapped_targets.contains(&i) {
            println!("  - index {}", i);
        }
    }
    println!();

    // Show complete mapping
    println!("Bone mappings:");
    for m in &map.mappings {
        println!(
            "  {} -> target[{}] (scale: {:.2})",
            m.source_name, m.target_index, m.position_scale
        );
    }
}

// ============================================================================
// Usage Example
// ============================================================================

fn main() {
    // Parse a BVH file
    let bvh_content = std::fs::read_to_string("walk.bvh").expect("Failed to read BVH");
    let clip = BvhClip::parse(&bvh_content).expect("Failed to parse BVH");

    println!("Source skeleton: {} joints", clip.joints.len());
    for (i, joint) in clip.joints.iter().enumerate() {
        println!("  [{}] {}", i, joint.name);
    }
    println!();

    // Create skeleton mapping
    let mut skeleton_map = SkeletonMap::cmu_to_humanoid();

    // Optional: Apply proportional scaling for different body types
    let target = TargetSkeleton::standard_human();
    let proportions = LimbProportions::from_skeletons(&clip.joints, &target);
    proportions.apply_to_mapping(&mut skeleton_map);

    // Debug the mapping
    debug_mapping(&clip.joints, 21, &skeleton_map);

    // Retarget a frame
    let target_bone_count = 21;
    let position_scale = 0.01; // CMU uses cm
    let retargeted = retarget_frame(&clip, 0, &skeleton_map, target_bone_count, position_scale);

    println!("\nRetargeted frame 0:");
    for (i, pose) in retargeted.iter().enumerate() {
        println!(
            "  target[{}]: pos=({:.3}, {:.3}, {:.3}), rot=({:.1}, {:.1}, {:.1})",
            i,
            pose.position[0], pose.position[1], pose.position[2],
            pose.rotation[0], pose.rotation[1], pose.rotation[2]
        );
    }
}
