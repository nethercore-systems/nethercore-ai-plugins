# Skeleton Retargeting Reference

Mapping motion capture data from source skeletons (CMU, Mixamo) to custom game skeletons.

## Retargeting Challenges

1. **Different bone counts:** CMU has 31 joints, game may have 20
2. **Different naming:** "LeftUpLeg" vs "L_Thigh" vs "thigh.L"
3. **Different proportions:** Captured actor vs game character
4. **Different T-poses:** Arms at different angles
5. **Different hierarchies:** Extra helper bones

## Bone Mapping System

### Data Structures

```rust
/// Quaternion identity for no correction
pub const IDENTITY: [f32; 4] = [1.0, 0.0, 0.0, 0.0];

/// Maps source skeleton bone to target skeleton bone
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
            rotation_offset: IDENTITY,
            position_scale: 1.0,
        }
    }

    pub fn with_scale(mut self, scale: f32) -> Self {
        self.position_scale = scale;
        self
    }

    pub fn with_rotation(mut self, rot: [f32; 4]) -> Self {
        self.rotation_offset = rot;
        self
    }
}

/// Complete skeleton mapping
pub struct SkeletonMap {
    pub mappings: Vec<BoneMapping>,
    pub source_to_target: std::collections::HashMap<String, usize>,
}
```

### Standard Humanoid Mapping

```rust
impl SkeletonMap {
    /// Standard CMU to game humanoid (20 bones)
    pub fn cmu_to_humanoid() -> Self {
        let mappings = vec![
            // Spine chain
            BoneMapping::new("Hips", 0),
            BoneMapping::new("Spine", 1),
            BoneMapping::new("Spine1", 2),
            BoneMapping::new("Neck", 3),
            BoneMapping::new("Head", 4),

            // Left arm
            BoneMapping::new("LeftShoulder", 5),
            BoneMapping::new("LeftArm", 6),
            BoneMapping::new("LeftForeArm", 7),
            BoneMapping::new("LeftHand", 8),

            // Right arm
            BoneMapping::new("RightShoulder", 9),
            BoneMapping::new("RightArm", 10),
            BoneMapping::new("RightForeArm", 11),
            BoneMapping::new("RightHand", 12),

            // Left leg
            BoneMapping::new("LeftUpLeg", 13),
            BoneMapping::new("LeftLeg", 14),
            BoneMapping::new("LeftFoot", 15),
            BoneMapping::new("LeftToeBase", 16),

            // Right leg
            BoneMapping::new("RightUpLeg", 17),
            BoneMapping::new("RightLeg", 18),
            BoneMapping::new("RightFoot", 19),
            BoneMapping::new("RightToeBase", 20),
        ];

        Self::from_mappings(mappings)
    }

    /// Mixamo to game humanoid
    pub fn mixamo_to_humanoid() -> Self {
        let mappings = vec![
            BoneMapping::new("mixamorig:Hips", 0),
            BoneMapping::new("mixamorig:Spine", 1),
            BoneMapping::new("mixamorig:Spine1", 2),
            BoneMapping::new("mixamorig:Neck", 3),
            BoneMapping::new("mixamorig:Head", 4),
            // ... etc with "mixamorig:" prefix
        ];
        Self::from_mappings(mappings)
    }

    fn from_mappings(mappings: Vec<BoneMapping>) -> Self {
        let mut source_to_target = std::collections::HashMap::new();
        for m in &mappings {
            source_to_target.insert(m.source_name.clone(), m.target_index);
        }
        Self { mappings, source_to_target }
    }
}
```

## Retargeting Algorithm

### Basic Retargeting

```rust
/// Retarget a single frame from source to target skeleton
pub fn retarget_frame(
    source_clip: &BvhClip,
    frame: usize,
    skeleton_map: &SkeletonMap,
    target_bone_count: usize,
    position_scale: f32,  // 0.01 for CMU cm to m
) -> Vec<JointTransform> {
    let mut target_poses = vec![JointTransform::default(); target_bone_count];

    for mapping in &skeleton_map.mappings {
        // Find source joint by name
        let source_idx = source_clip.joints.iter()
            .position(|j| j.name == mapping.source_name);

        if let Some(src_idx) = source_idx {
            let source_pose = source_clip.sample_joint(src_idx, frame);

            // Apply position scaling
            let scaled_pos = [
                source_pose.position[0] * position_scale * mapping.position_scale,
                source_pose.position[1] * position_scale * mapping.position_scale,
                source_pose.position[2] * position_scale * mapping.position_scale,
            ];

            // Apply rotation correction
            let corrected_rot = if mapping.rotation_offset != IDENTITY {
                quat_multiply(
                    euler_to_quat(&source_pose.rotation),
                    mapping.rotation_offset
                )
            } else {
                euler_to_quat(&source_pose.rotation)
            };

            target_poses[mapping.target_index] = JointTransform {
                position: scaled_pos,
                rotation: quat_to_euler(&corrected_rot),
            };
        }
    }

    target_poses
}
```

### Proportional Scaling

For characters with different limb proportions:

```rust
/// Calculate limb ratios between source and target
pub struct LimbProportions {
    pub upper_arm: f32,
    pub forearm: f32,
    pub thigh: f32,
    pub shin: f32,
    pub spine: f32,
}

impl LimbProportions {
    pub fn from_skeletons(source: &[BvhJoint], target: &TargetSkeleton) -> Self {
        // Measure source limb lengths from offsets
        let src_upper_arm = offset_length(&source, "LeftArm", "LeftForeArm");
        let src_forearm = offset_length(&source, "LeftForeArm", "LeftHand");
        let src_thigh = offset_length(&source, "LeftUpLeg", "LeftLeg");
        let src_shin = offset_length(&source, "LeftLeg", "LeftFoot");

        Self {
            upper_arm: target.upper_arm_length / src_upper_arm,
            forearm: target.forearm_length / src_forearm,
            thigh: target.thigh_length / src_thigh,
            shin: target.shin_length / src_shin,
            spine: target.spine_length / measure_spine(source),
        }
    }
}

fn offset_length(joints: &[BvhJoint], from: &str, to: &str) -> f32 {
    let to_joint = joints.iter().find(|j| j.name == to).unwrap();
    let offset = to_joint.offset;
    (offset[0].powi(2) + offset[1].powi(2) + offset[2].powi(2)).sqrt()
}
```

### T-Pose Correction

When source and target have different rest poses:

```rust
/// Calculate rotation offset for T-pose differences
pub fn calculate_tpose_offset(
    source_tpose_dir: [f32; 3],  // Direction bone points in source T-pose
    target_tpose_dir: [f32; 3],  // Direction bone points in target T-pose
) -> [f32; 4] {
    let source_norm = normalize(source_tpose_dir);
    let target_norm = normalize(target_tpose_dir);

    // Quaternion that rotates source direction to target direction
    quat_from_rotation_arc(source_norm, target_norm)
}

fn quat_from_rotation_arc(from: [f32; 3], to: [f32; 3]) -> [f32; 4] {
    let dot = from[0] * to[0] + from[1] * to[1] + from[2] * to[2];

    if dot > 0.9999 {
        return IDENTITY;
    }

    if dot < -0.9999 {
        // 180 degree rotation around any perpendicular axis
        let perp = if from[0].abs() < 0.9 {
            cross(from, [1.0, 0.0, 0.0])
        } else {
            cross(from, [0.0, 1.0, 0.0])
        };
        let axis = normalize(perp);
        return [0.0, axis[0], axis[1], axis[2]];
    }

    let c = cross(from, to);
    let s = ((1.0 + dot) * 2.0).sqrt();
    let inv_s = 1.0 / s;

    [s * 0.5, c[0] * inv_s, c[1] * inv_s, c[2] * inv_s]
}
```

## Advanced Techniques

### Endpoint Preservation with IK

Preserve hand/foot positions when skeleton proportions differ:

```rust
/// Retarget with IK for endpoint accuracy
pub fn retarget_with_ik(
    source_clip: &BvhClip,
    frame: usize,
    skeleton_map: &SkeletonMap,
    target_skeleton: &TargetSkeleton,
) -> Vec<[f32; 12]> {
    // First pass: basic retarget
    let mut poses = retarget_frame(source_clip, frame, skeleton_map, ...);

    // Calculate source hand/foot world positions
    let source_left_hand = source_clip.world_position(frame, "LeftHand");
    let source_right_hand = source_clip.world_position(frame, "RightHand");
    let source_left_foot = source_clip.world_position(frame, "LeftFoot");
    let source_right_foot = source_clip.world_position(frame, "RightFoot");

    // Apply two-bone IK to match endpoints
    let (l_shoulder, l_elbow) = solve_two_bone_ik(
        target_skeleton.left_shoulder_pos(&poses),
        source_left_hand,
        target_skeleton.upper_arm_length,
        target_skeleton.forearm_length,
        poses[6].rotation,  // Hint from retarget
    );
    poses[6].rotation = l_shoulder;
    poses[7].rotation = l_elbow;

    // Repeat for other limbs...

    poses
}
```

### Hierarchical Name Matching

Handle different naming conventions:

```rust
/// Fuzzy match bone names across naming conventions
pub fn fuzzy_bone_match(source_name: &str, target_name: &str) -> bool {
    let source = normalize_bone_name(source_name);
    let target = normalize_bone_name(target_name);
    source == target
}

fn normalize_bone_name(name: &str) -> String {
    let name = name.to_lowercase();
    let name = name.replace("mixamorig:", "");
    let name = name.replace(":", "");
    let name = name.replace("_", "");
    let name = name.replace(".", "");
    let name = name.replace("left", "l");
    let name = name.replace("right", "r");

    // Handle common variations
    let name = name.replace("upleg", "thigh");
    let name = name.replace("forearm", "lowerarm");
    let name = name.replace("leg", "shin");

    name
}
```

### Automatic Mapping

Auto-generate mapping by analyzing skeletons:

```rust
/// Generate skeleton map by matching bone names
pub fn auto_generate_map(
    source: &[BvhJoint],
    target: &[TargetBone],
) -> SkeletonMap {
    let mut mappings = Vec::new();

    for (target_idx, target_bone) in target.iter().enumerate() {
        // Find best matching source bone
        let best_match = source.iter()
            .enumerate()
            .filter(|(_, j)| fuzzy_bone_match(&j.name, &target_bone.name))
            .map(|(i, j)| (i, j.name.clone()))
            .next();

        if let Some((_, source_name)) = best_match {
            mappings.push(BoneMapping::new(&source_name, target_idx));
        }
    }

    SkeletonMap::from_mappings(mappings)
}
```

## Common Skeleton Mappings

### CMU Subject Variations

Some CMU subjects use different bone names:

| Standard | Alt 1 | Alt 2 |
|----------|-------|-------|
| LeftUpLeg | LHipJoint | leftupleg |
| RightUpLeg | RHipJoint | rightupleg |
| Spine | LowerBack | spine |
| Spine1 | Spine | spine1 |
| Head | Head | head |

### Minimal Humanoid (12 bones)

For low-poly characters:

```rust
pub fn cmu_to_minimal() -> SkeletonMap {
    let mappings = vec![
        BoneMapping::new("Hips", 0),
        BoneMapping::new("Spine1", 1),   // Skip lower spine
        BoneMapping::new("Head", 2),
        BoneMapping::new("LeftArm", 3),  // Skip shoulder
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
    SkeletonMap::from_mappings(mappings)
}
```

## Debugging Retargeting

```rust
/// Visualize skeleton mapping issues
pub fn debug_retarget(
    source: &[BvhJoint],
    target: &[TargetBone],
    map: &SkeletonMap,
) {
    println!("=== Retarget Debug ===");

    // Check unmapped source bones
    for joint in source {
        if !map.source_to_target.contains_key(&joint.name) {
            println!("UNMAPPED SOURCE: {}", joint.name);
        }
    }

    // Check unmapped target bones
    let mapped_targets: std::collections::HashSet<_> =
        map.mappings.iter().map(|m| m.target_index).collect();
    for (i, bone) in target.iter().enumerate() {
        if !mapped_targets.contains(&i) {
            println!("UNMAPPED TARGET: {} (index {})", bone.name, i);
        }
    }

    // Show mapping
    for m in &map.mappings {
        println!("{} -> target[{}]", m.source_name, m.target_index);
    }
}
```
