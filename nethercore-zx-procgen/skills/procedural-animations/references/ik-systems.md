# Inverse Kinematics Systems

Complete IK implementations for procedural animation in Nethercore ZX.

## Overview

Inverse Kinematics (IK) calculates joint angles needed to reach a target position. Essential for:
- Foot placement on uneven terrain
- Hand reaching/grabbing
- Look-at behavior
- Weapon aiming
- Procedural locomotion

## Two-Bone IK (Limbs)

Most common IK for arms and legs.

### Complete Implementation

```rust
use glam::{Vec3, Quat, Mat4};
use core::f32::consts::PI;

/// Solve two-bone IK chain (e.g., shoulder-elbow-hand)
///
/// # Arguments
/// * `root` - Position of first joint (shoulder)
/// * `target` - Desired end effector position (hand)
/// * `bone1_len` - Length of first bone (upper arm)
/// * `bone2_len` - Length of second bone (forearm)
/// * `pole` - Pole vector for elbow direction
/// * `bend_direction` - Preferred bend direction when target is close
///
/// # Returns
/// (bone1_rotation, bone2_rotation) as quaternions
pub fn solve_two_bone_ik(
    root: Vec3,
    target: Vec3,
    bone1_len: f32,
    bone2_len: f32,
    pole: Vec3,
    bend_direction: Vec3,
) -> (Quat, Quat) {
    let chain_len = bone1_len + bone2_len;
    let to_target = target - root;
    let target_dist = to_target.length();

    // Handle edge cases
    if target_dist < 0.001 {
        // Target at root - default pose
        return (Quat::IDENTITY, Quat::from_rotation_x(-PI * 0.5));
    }

    // Clamp to reachable range
    let target_dist = target_dist.clamp(
        (bone1_len - bone2_len).abs() + 0.001,
        chain_len - 0.001
    );

    // Direction to target
    let target_dir = to_target.normalize();

    // Law of cosines for elbow angle
    let cos_elbow = (bone1_len.powi(2) + bone2_len.powi(2) - target_dist.powi(2))
        / (2.0 * bone1_len * bone2_len);
    let elbow_angle = PI - cos_elbow.clamp(-1.0, 1.0).acos();

    // Angle at shoulder (law of cosines)
    let cos_shoulder = (bone1_len.powi(2) + target_dist.powi(2) - bone2_len.powi(2))
        / (2.0 * bone1_len * target_dist);
    let shoulder_offset = cos_shoulder.clamp(-1.0, 1.0).acos();

    // Calculate rotation plane from pole vector
    let plane_normal = to_target.cross(pole - root).normalize();
    let initial_dir = if plane_normal.length_squared() < 0.001 {
        bend_direction.normalize()
    } else {
        plane_normal.cross(target_dir).normalize()
    };

    // Shoulder rotation
    // First rotate to point at target
    let shoulder_to_target = Quat::from_rotation_arc(Vec3::Y, target_dir);

    // Then rotate around target axis to apply shoulder offset
    let shoulder_twist = Quat::from_axis_angle(
        target_dir.cross(initial_dir).normalize(),
        shoulder_offset
    );
    let bone1_rotation = shoulder_to_target * shoulder_twist;

    // Elbow rotation (local to bone1)
    let bone2_rotation = Quat::from_rotation_x(PI - elbow_angle);

    (bone1_rotation, bone2_rotation)
}

/// Apply two-bone IK to bone matrices
pub fn apply_two_bone_ik(
    bones: &mut [[f32; 12]],
    bone1_idx: usize,
    bone2_idx: usize,
    effector_idx: usize,
    target: Vec3,
    pole: Vec3,
    bone1_len: f32,
    bone2_len: f32,
) {
    // Get root position from bone1's parent transform
    let root = Vec3::new(bones[bone1_idx][9], bones[bone1_idx][10], bones[bone1_idx][11]);

    let (rot1, rot2) = solve_two_bone_ik(
        root,
        target,
        bone1_len,
        bone2_len,
        pole,
        Vec3::NEG_Z,  // Default bend backward
    );

    // Apply rotations to bone matrices
    let mat1 = Mat4::from_rotation_translation(rot1, root);
    bones[bone1_idx] = mat4_to_3x4(mat1);

    let bone2_world_pos = root + rot1 * Vec3::new(0.0, bone1_len, 0.0);
    let mat2 = Mat4::from_rotation_translation(rot1 * rot2, bone2_world_pos);
    bones[bone2_idx] = mat4_to_3x4(mat2);

    // Effector follows bone2
    let effector_pos = bone2_world_pos + (rot1 * rot2) * Vec3::new(0.0, bone2_len, 0.0);
    bones[effector_idx] = mat4_to_3x4(Mat4::from_translation(effector_pos));
}
```

## FABRIK (Multi-Bone Chains)

Forward And Backward Reaching IK for chains with any number of bones.

```rust
/// FABRIK solver for arbitrary bone chains
pub struct FabrikChain {
    joints: Vec<Vec3>,  // Joint positions
    lengths: Vec<f32>,  // Bone lengths
    tolerance: f32,
    max_iterations: u32,
}

impl FabrikChain {
    pub fn new(joints: Vec<Vec3>) -> Self {
        let mut lengths = Vec::with_capacity(joints.len() - 1);
        for i in 0..joints.len() - 1 {
            lengths.push((joints[i + 1] - joints[i]).length());
        }

        Self {
            joints,
            lengths,
            tolerance: 0.001,
            max_iterations: 10,
        }
    }

    /// Solve IK to reach target
    pub fn solve(&mut self, target: Vec3) -> bool {
        let root = self.joints[0];
        let total_length: f32 = self.lengths.iter().sum();
        let dist_to_target = (target - root).length();

        // Check if target is reachable
        if dist_to_target > total_length {
            // Target unreachable - stretch toward it
            let direction = (target - root).normalize();
            let mut current = root;
            for i in 0..self.joints.len() - 1 {
                self.joints[i] = current;
                current += direction * self.lengths[i];
            }
            self.joints[self.joints.len() - 1] = current;
            return false;
        }

        // FABRIK iterations
        for _ in 0..self.max_iterations {
            // Check if close enough
            let end_effector = self.joints[self.joints.len() - 1];
            if (end_effector - target).length() < self.tolerance {
                return true;
            }

            // Backward pass (end to root)
            self.joints[self.joints.len() - 1] = target;
            for i in (0..self.joints.len() - 1).rev() {
                let direction = (self.joints[i] - self.joints[i + 1]).normalize();
                self.joints[i] = self.joints[i + 1] + direction * self.lengths[i];
            }

            // Forward pass (root to end)
            self.joints[0] = root;
            for i in 0..self.joints.len() - 1 {
                let direction = (self.joints[i + 1] - self.joints[i]).normalize();
                self.joints[i + 1] = self.joints[i] + direction * self.lengths[i];
            }
        }

        true
    }

    /// Get joint rotations after solving
    pub fn get_rotations(&self) -> Vec<Quat> {
        let mut rotations = Vec::with_capacity(self.joints.len() - 1);

        for i in 0..self.joints.len() - 1 {
            let bone_dir = (self.joints[i + 1] - self.joints[i]).normalize();
            let rotation = Quat::from_rotation_arc(Vec3::Y, bone_dir);
            rotations.push(rotation);
        }

        rotations
    }

    /// Apply constraints (e.g., joint limits)
    pub fn apply_constraints(&mut self, constraints: &[JointConstraint]) {
        for (i, constraint) in constraints.iter().enumerate() {
            if i >= self.joints.len() - 1 {
                break;
            }

            // Get current bone direction
            let bone_dir = (self.joints[i + 1] - self.joints[i]).normalize();

            // Get parent direction (or up for root)
            let parent_dir = if i == 0 {
                Vec3::Y
            } else {
                (self.joints[i] - self.joints[i - 1]).normalize()
            };

            // Apply hinge constraint
            if let Some(hinge) = &constraint.hinge {
                let constrained = constrain_to_plane(bone_dir, hinge.axis, parent_dir);
                let angle = parent_dir.dot(constrained).acos();
                let clamped_angle = angle.clamp(hinge.min_angle, hinge.max_angle);

                let axis = parent_dir.cross(constrained).normalize();
                let rotation = Quat::from_axis_angle(axis, clamped_angle);
                let new_dir = rotation * parent_dir;

                self.joints[i + 1] = self.joints[i] + new_dir * self.lengths[i];
            }

            // Apply cone constraint
            if let Some(cone) = &constraint.cone {
                let angle = parent_dir.dot(bone_dir).acos();
                if angle > cone.max_angle {
                    let axis = parent_dir.cross(bone_dir).normalize();
                    let rotation = Quat::from_axis_angle(axis, cone.max_angle);
                    let new_dir = rotation * parent_dir;
                    self.joints[i + 1] = self.joints[i] + new_dir * self.lengths[i];
                }
            }
        }
    }
}

pub struct JointConstraint {
    pub hinge: Option<HingeConstraint>,
    pub cone: Option<ConeConstraint>,
}

pub struct HingeConstraint {
    pub axis: Vec3,
    pub min_angle: f32,
    pub max_angle: f32,
}

pub struct ConeConstraint {
    pub max_angle: f32,
}

fn constrain_to_plane(dir: Vec3, plane_normal: Vec3, parent_dir: Vec3) -> Vec3 {
    let projected = dir - plane_normal * dir.dot(plane_normal);
    if projected.length_squared() < 0.001 {
        parent_dir
    } else {
        projected.normalize()
    }
}
```

## Look-At IK

Rotate head/eyes to look at target:

```rust
/// Calculate rotation to look at target
pub fn look_at_rotation(
    current_pos: Vec3,
    target: Vec3,
    up: Vec3,
    forward: Vec3,
) -> Quat {
    let to_target = (target - current_pos).normalize();

    // Calculate rotation from default forward to target
    if to_target.dot(forward) > 0.9999 {
        return Quat::IDENTITY;
    }

    if to_target.dot(forward) < -0.9999 {
        return Quat::from_rotation_y(PI);
    }

    Quat::from_rotation_arc(forward, to_target)
}

/// Head look-at with limits
pub struct HeadLookAt {
    pub max_yaw: f32,    // Max horizontal rotation (degrees)
    pub max_pitch: f32,  // Max vertical rotation (degrees)
    pub speed: f32,      // Rotation speed (degrees/second)
}

impl HeadLookAt {
    pub fn update(
        &self,
        current_rotation: &mut Quat,
        head_pos: Vec3,
        target: Vec3,
        head_forward: Vec3,
        dt: f32,
    ) {
        let to_target = (target - head_pos).normalize();

        // Calculate target yaw and pitch
        let local_target = current_rotation.inverse() * to_target;
        let target_yaw = local_target.x.atan2(local_target.z);
        let target_pitch = (-local_target.y).atan2(
            (local_target.x.powi(2) + local_target.z.powi(2)).sqrt()
        );

        // Clamp to limits
        let clamped_yaw = target_yaw.clamp(
            -self.max_yaw.to_radians(),
            self.max_yaw.to_radians()
        );
        let clamped_pitch = target_pitch.clamp(
            -self.max_pitch.to_radians(),
            self.max_pitch.to_radians()
        );

        // Create target rotation
        let target_rot = Quat::from_euler(
            glam::EulerRot::YXZ,
            clamped_yaw,
            clamped_pitch,
            0.0
        );

        // Smooth interpolation
        let max_delta = self.speed.to_radians() * dt;
        *current_rotation = current_rotation.slerp(
            target_rot,
            (max_delta / current_rotation.angle_between(target_rot)).min(1.0)
        );
    }
}

/// Eye look-at with saccades
pub struct EyeLookAt {
    pub left_eye_offset: Vec3,
    pub right_eye_offset: Vec3,
    pub max_angle: f32,
    pub saccade_timer: f32,
    pub saccade_offset: Vec2,
}

impl EyeLookAt {
    pub fn update(&mut self, head_transform: Mat4, target: Vec3, dt: f32) -> (Quat, Quat) {
        // Random saccades (micro-movements)
        self.saccade_timer -= dt;
        if self.saccade_timer <= 0.0 {
            self.saccade_timer = 0.1 + random_f32() * 0.3;
            self.saccade_offset = Vec2::new(
                (random_f32() - 0.5) * 2.0,
                (random_f32() - 0.5) * 1.0
            );
        }

        // Calculate eye rotations
        let left_eye_world = head_transform.transform_point3(self.left_eye_offset);
        let right_eye_world = head_transform.transform_point3(self.right_eye_offset);

        let left_target = target + Vec3::new(self.saccade_offset.x, self.saccade_offset.y, 0.0) * 0.01;
        let right_target = target + Vec3::new(self.saccade_offset.x, self.saccade_offset.y, 0.0) * 0.01;

        let left_rot = self.eye_rotation(left_eye_world, left_target);
        let right_rot = self.eye_rotation(right_eye_world, right_target);

        (left_rot, right_rot)
    }

    fn eye_rotation(&self, eye_pos: Vec3, target: Vec3) -> Quat {
        let to_target = (target - eye_pos).normalize();
        // Eye forward is -Z
        let angle = Vec3::NEG_Z.dot(to_target).acos();

        if angle > self.max_angle.to_radians() {
            // Clamp to maximum
            let axis = Vec3::NEG_Z.cross(to_target).normalize();
            Quat::from_axis_angle(axis, self.max_angle.to_radians())
        } else {
            Quat::from_rotation_arc(Vec3::NEG_Z, to_target)
        }
    }
}
```

## Foot IK (Ground Adaptation)

Place feet on uneven terrain:

```rust
pub struct FootIK {
    pub hip_height: f32,
    pub thigh_length: f32,
    pub shin_length: f32,
    pub foot_offset: f32,  // Ankle to ground
}

impl FootIK {
    /// Solve foot placement on terrain
    pub fn solve(
        &self,
        hip_pos: Vec3,
        foot_target: Vec3,
        ground_normal: Vec3,
        pole: Vec3,
    ) -> (Quat, Quat, Quat) {
        // Adjust target for foot offset
        let ankle_target = foot_target + Vec3::Y * self.foot_offset;

        // Solve leg IK
        let (thigh_rot, shin_rot) = solve_two_bone_ik(
            hip_pos,
            ankle_target,
            self.thigh_length,
            self.shin_length,
            pole,
            Vec3::NEG_Z,
        );

        // Foot rotation to match ground
        // Forward is -Z in world space
        let foot_forward = (thigh_rot * shin_rot * Vec3::NEG_Z).normalize();
        let foot_up = ground_normal;
        let foot_right = foot_forward.cross(foot_up).normalize();
        let adjusted_forward = foot_up.cross(foot_right).normalize();

        let foot_rot = Quat::from_mat3(&glam::Mat3::from_cols(
            foot_right,
            foot_up,
            adjusted_forward,
        ));

        (thigh_rot, shin_rot, foot_rot)
    }
}

/// Full character foot IK system
pub struct CharacterFootIK {
    left_foot: FootIK,
    right_foot: FootIK,
    pelvis_height: f32,
}

impl CharacterFootIK {
    pub fn update(
        &mut self,
        pelvis_pos: Vec3,
        left_hip_offset: Vec3,
        right_hip_offset: Vec3,
        terrain: &dyn Fn(Vec2) -> (f32, Vec3),  // Returns (height, normal)
        dt: f32,
    ) -> CharacterLegPose {
        // Ray cast for foot targets
        let left_hip = pelvis_pos + left_hip_offset;
        let right_hip = pelvis_pos + right_hip_offset;

        // Simple vertical ray for foot placement
        let left_foot_xz = Vec2::new(left_hip.x, left_hip.z);
        let right_foot_xz = Vec2::new(right_hip.x, right_hip.z);

        let (left_ground, left_normal) = terrain(left_foot_xz);
        let (right_ground, right_normal) = terrain(right_foot_xz);

        // Calculate IK targets
        let left_target = Vec3::new(left_hip.x, left_ground, left_hip.z);
        let right_target = Vec3::new(right_hip.x, right_ground, right_hip.z);

        // Adjust pelvis height based on leg reach
        let left_reach = (left_hip - left_target).length();
        let right_reach = (right_hip - right_target).length();
        let max_reach = self.left_foot.thigh_length + self.left_foot.shin_length - 0.05;

        let pelvis_adjustment = if left_reach > max_reach || right_reach > max_reach {
            let needed = (left_reach.max(right_reach) - max_reach).max(0.0);
            -needed
        } else {
            0.0
        };

        // Solve IK for both legs
        let adjusted_pelvis = pelvis_pos + Vec3::Y * pelvis_adjustment;
        let left_hip = adjusted_pelvis + left_hip_offset;
        let right_hip = adjusted_pelvis + right_hip_offset;

        let (l_thigh, l_shin, l_foot) = self.left_foot.solve(
            left_hip,
            left_target,
            left_normal,
            left_hip + Vec3::NEG_Z * 0.5,
        );

        let (r_thigh, r_shin, r_foot) = self.right_foot.solve(
            right_hip,
            right_target,
            right_normal,
            right_hip + Vec3::NEG_Z * 0.5,
        );

        CharacterLegPose {
            pelvis_offset: pelvis_adjustment,
            left_thigh: l_thigh,
            left_shin: l_shin,
            left_foot: l_foot,
            right_thigh: r_thigh,
            right_shin: r_shin,
            right_foot: r_foot,
        }
    }
}

pub struct CharacterLegPose {
    pub pelvis_offset: f32,
    pub left_thigh: Quat,
    pub left_shin: Quat,
    pub left_foot: Quat,
    pub right_thigh: Quat,
    pub right_shin: Quat,
    pub right_foot: Quat,
}
```

## CCD (Cyclic Coordinate Descent)

Alternative multi-bone solver, good for tails and tentacles:

```rust
pub struct CCDSolver {
    joints: Vec<Vec3>,
    lengths: Vec<f32>,
    max_iterations: u32,
    tolerance: f32,
}

impl CCDSolver {
    pub fn solve(&mut self, target: Vec3) -> bool {
        for _ in 0..self.max_iterations {
            // Check if close enough
            let end = self.joints[self.joints.len() - 1];
            if (end - target).length() < self.tolerance {
                return true;
            }

            // Iterate from end to root
            for i in (0..self.joints.len() - 1).rev() {
                let joint = self.joints[i];
                let end = self.joints[self.joints.len() - 1];

                // Vector from this joint to end effector
                let to_end = (end - joint).normalize();
                // Vector from this joint to target
                let to_target = (target - joint).normalize();

                // Rotation to align end with target
                if to_end.dot(to_target) < 0.9999 {
                    let rotation = Quat::from_rotation_arc(to_end, to_target);

                    // Rotate all joints after this one
                    for j in (i + 1)..self.joints.len() {
                        let relative = self.joints[j] - joint;
                        self.joints[j] = joint + rotation * relative;
                    }
                }
            }
        }

        false
    }
}
```

## Utility Functions

```rust
fn mat4_to_3x4(m: Mat4) -> [f32; 12] {
    let cols = m.to_cols_array();
    [
        cols[0], cols[1], cols[2],
        cols[4], cols[5], cols[6],
        cols[8], cols[9], cols[10],
        cols[12], cols[13], cols[14],
    ]
}

fn random_f32() -> f32 {
    unsafe { ffi::random_f32() }
}
```

## Best Practices

### Performance

1. **Solve priority**: Important IK first (feet, hands), optional last (eyes)
2. **Reduce iterations**: Most problems solve in 3-5 FABRIK iterations
3. **Skip when static**: Don't solve IK if target hasn't moved
4. **LOD for IK**: Simpler IK at distance

### Quality

1. **Use pole vectors**: Prevents elbow/knee flipping
2. **Apply constraints**: Joint limits prevent unnatural poses
3. **Blend with animation**: Smooth transitions in/out of IK
4. **Handle unreachable**: Graceful degradation when target is too far
