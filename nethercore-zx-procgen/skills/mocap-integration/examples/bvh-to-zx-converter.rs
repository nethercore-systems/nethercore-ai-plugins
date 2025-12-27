//! BVH to ZX bone matrix converter
//!
//! Converts parsed BVH frames to ZX 3x4 bone matrices compatible with set_bones() FFI.
//! Handles Euler to quaternion conversion, coordinate systems, and unit scaling.

use std::f32::consts::PI;

// Re-use types from bvh-parser.rs
mod bvh_parser;
use bvh_parser::{BvhClip, JointTransform};

/// ZX bone matrix: 3x4 column-major (12 floats)
/// Layout: [x_axis(3), y_axis(3), z_axis(3), translation(3)]
pub type BoneMatrix = [f32; 12];

/// Internal 3x4 matrix representation for computation
type Mat3x4 = [[f32; 4]; 3];

/// Quaternion [w, x, y, z]
type Quat = [f32; 4];

/// Convert Euler angles (degrees) to quaternion using ZXY rotation order
/// This is the standard order for CMU motion capture data
pub fn euler_zxy_to_quat(x_deg: f32, y_deg: f32, z_deg: f32) -> Quat {
    let x = x_deg * PI / 180.0;
    let y = y_deg * PI / 180.0;
    let z = z_deg * PI / 180.0;

    let (sx, cx) = (x * 0.5).sin_cos();
    let (sy, cy) = (y * 0.5).sin_cos();
    let (sz, cz) = (z * 0.5).sin_cos();

    // ZXY order: Rz * Rx * Ry
    [
        cz * cx * cy + sz * sx * sy, // w
        cz * sx * cy + sz * cx * sy, // x
        cz * cx * sy - sz * sx * cy, // y
        sz * cx * cy - cz * sx * sy, // z
    ]
}

/// Convert quaternion to 3x3 rotation matrix
fn quat_to_mat3(q: &Quat) -> [[f32; 3]; 3] {
    let (w, x, y, z) = (q[0], q[1], q[2], q[3]);

    let xx = x * x;
    let yy = y * y;
    let zz = z * z;
    let xy = x * y;
    let xz = x * z;
    let yz = y * z;
    let wx = w * x;
    let wy = w * y;
    let wz = w * z;

    [
        [1.0 - 2.0 * (yy + zz), 2.0 * (xy + wz), 2.0 * (xz - wy)],
        [2.0 * (xy - wz), 1.0 - 2.0 * (xx + zz), 2.0 * (yz + wx)],
        [2.0 * (xz + wy), 2.0 * (yz - wx), 1.0 - 2.0 * (xx + yy)],
    ]
}

/// Build a 3x4 matrix from rotation (as quaternion) and translation
fn build_mat3x4(rotation: &Quat, translation: [f32; 3]) -> Mat3x4 {
    let rot = quat_to_mat3(rotation);
    [
        [rot[0][0], rot[0][1], rot[0][2], translation[0]],
        [rot[1][0], rot[1][1], rot[1][2], translation[1]],
        [rot[2][0], rot[2][1], rot[2][2], translation[2]],
    ]
}

/// Multiply two 3x4 matrices (treating as 4x4 with implicit [0,0,0,1] row)
fn multiply_3x4(a: &Mat3x4, b: &Mat3x4) -> Mat3x4 {
    let mut result = [[0.0f32; 4]; 3];

    for i in 0..3 {
        for j in 0..4 {
            result[i][j] = a[i][0] * b[0][j] + a[i][1] * b[1][j] + a[i][2] * b[2][j];
            if j == 3 {
                result[i][j] += a[i][3]; // Add translation
            }
        }
    }

    result
}

/// Identity 3x4 matrix
fn identity_3x4() -> Mat3x4 {
    [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
    ]
}

/// Flatten 3x4 matrix to ZX bone format (column-major 12 floats)
fn flatten_3x4(m: &Mat3x4) -> BoneMatrix {
    [
        m[0][0], m[1][0], m[2][0], // X axis (column 0)
        m[0][1], m[1][1], m[2][1], // Y axis (column 1)
        m[0][2], m[1][2], m[2][2], // Z axis (column 2)
        m[0][3], m[1][3], m[2][3], // Translation (column 3)
    ]
}

/// Convert an entire BVH frame to ZX bone matrices
///
/// # Arguments
/// * `clip` - Parsed BVH clip
/// * `frame` - Frame index to sample
/// * `position_scale` - Scale factor for positions (0.01 for CMU cm → m)
///
/// # Returns
/// Vector of 3x4 matrices in ZX format, one per joint
pub fn bvh_frame_to_zx(clip: &BvhClip, frame: usize, position_scale: f32) -> Vec<BoneMatrix> {
    let mut world_transforms: Vec<Mat3x4> = Vec::with_capacity(clip.joints.len());

    for (i, joint) in clip.joints.iter().enumerate() {
        let jt = clip.sample_joint(i, frame);

        // Build local rotation from Euler angles (ZXY order for CMU)
        let local_quat = euler_zxy_to_quat(jt.rotation[0], jt.rotation[1], jt.rotation[2]);

        // Local position: rest offset + animated position
        let local_pos = [
            (joint.offset[0] + jt.position[0]) * position_scale,
            (joint.offset[1] + jt.position[1]) * position_scale,
            (joint.offset[2] + jt.position[2]) * position_scale,
        ];

        // Build local 3x4 transform
        let local_mat = build_mat3x4(&local_quat, local_pos);

        // Compute world transform by multiplying with parent
        let world_mat = match joint.parent {
            Some(parent_idx) => multiply_3x4(&world_transforms[parent_idx], &local_mat),
            None => local_mat,
        };

        world_transforms.push(world_mat);
    }

    // Convert to ZX format
    world_transforms.iter().map(flatten_3x4).collect()
}

/// Convert BVH frame with time interpolation
pub fn bvh_time_to_zx(clip: &BvhClip, time: f32, position_scale: f32) -> Vec<BoneMatrix> {
    let frame_f = time / clip.frame_time;
    let frame_a = (frame_f as usize).min(clip.frame_count.saturating_sub(1));
    let frame_b = (frame_a + 1).min(clip.frame_count.saturating_sub(1));
    let t = frame_f.fract();

    if frame_a == frame_b || t < 0.001 {
        return bvh_frame_to_zx(clip, frame_a, position_scale);
    }

    // Get matrices for both frames
    let matrices_a = bvh_frame_to_zx(clip, frame_a, position_scale);
    let matrices_b = bvh_frame_to_zx(clip, frame_b, position_scale);

    // Blend
    matrices_a
        .iter()
        .zip(matrices_b.iter())
        .map(|(a, b)| blend_bone_matrix(a, b, t))
        .collect()
}

/// Blend two bone matrices
fn blend_bone_matrix(a: &BoneMatrix, b: &BoneMatrix, t: f32) -> BoneMatrix {
    // Extract rotation parts and convert to quaternions for slerp
    let rot_a = mat3_to_quat(&[
        [a[0], a[1], a[2]],
        [a[3], a[4], a[5]],
        [a[6], a[7], a[8]],
    ]);
    let rot_b = mat3_to_quat(&[
        [b[0], b[1], b[2]],
        [b[3], b[4], b[5]],
        [b[6], b[7], b[8]],
    ]);

    let rot_blend = slerp(&rot_a, &rot_b, t);
    let rot_mat = quat_to_mat3(&rot_blend);

    // Lerp translation
    let tx = a[9] + (b[9] - a[9]) * t;
    let ty = a[10] + (b[10] - a[10]) * t;
    let tz = a[11] + (b[11] - a[11]) * t;

    [
        rot_mat[0][0],
        rot_mat[1][0],
        rot_mat[2][0],
        rot_mat[0][1],
        rot_mat[1][1],
        rot_mat[2][1],
        rot_mat[0][2],
        rot_mat[1][2],
        rot_mat[2][2],
        tx,
        ty,
        tz,
    ]
}

/// Convert 3x3 rotation matrix to quaternion
fn mat3_to_quat(m: &[[f32; 3]; 3]) -> Quat {
    let trace = m[0][0] + m[1][1] + m[2][2];

    if trace > 0.0 {
        let s = (trace + 1.0).sqrt() * 2.0;
        [
            0.25 * s,
            (m[2][1] - m[1][2]) / s,
            (m[0][2] - m[2][0]) / s,
            (m[1][0] - m[0][1]) / s,
        ]
    } else if m[0][0] > m[1][1] && m[0][0] > m[2][2] {
        let s = (1.0 + m[0][0] - m[1][1] - m[2][2]).sqrt() * 2.0;
        [
            (m[2][1] - m[1][2]) / s,
            0.25 * s,
            (m[0][1] + m[1][0]) / s,
            (m[0][2] + m[2][0]) / s,
        ]
    } else if m[1][1] > m[2][2] {
        let s = (1.0 + m[1][1] - m[0][0] - m[2][2]).sqrt() * 2.0;
        [
            (m[0][2] - m[2][0]) / s,
            (m[0][1] + m[1][0]) / s,
            0.25 * s,
            (m[1][2] + m[2][1]) / s,
        ]
    } else {
        let s = (1.0 + m[2][2] - m[0][0] - m[1][1]).sqrt() * 2.0;
        [
            (m[1][0] - m[0][1]) / s,
            (m[0][2] + m[2][0]) / s,
            (m[1][2] + m[2][1]) / s,
            0.25 * s,
        ]
    }
}

/// Spherical linear interpolation for quaternions
fn slerp(a: &Quat, b: &Quat, t: f32) -> Quat {
    let mut dot = a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3];

    // Handle opposite quaternions
    let b = if dot < 0.0 {
        dot = -dot;
        [-b[0], -b[1], -b[2], -b[3]]
    } else {
        *b
    };

    // Use lerp for nearly parallel quaternions
    if dot > 0.9995 {
        return normalize_quat([
            a[0] + (b[0] - a[0]) * t,
            a[1] + (b[1] - a[1]) * t,
            a[2] + (b[2] - a[2]) * t,
            a[3] + (b[3] - a[3]) * t,
        ]);
    }

    let theta = dot.acos();
    let sin_theta = theta.sin();
    let a_weight = ((1.0 - t) * theta).sin() / sin_theta;
    let b_weight = (t * theta).sin() / sin_theta;

    [
        a[0] * a_weight + b[0] * b_weight,
        a[1] * a_weight + b[1] * b_weight,
        a[2] * a_weight + b[2] * b_weight,
        a[3] * a_weight + b[3] * b_weight,
    ]
}

fn normalize_quat(q: Quat) -> Quat {
    let len = (q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3]).sqrt();
    if len > 0.0001 {
        [q[0] / len, q[1] / len, q[2] / len, q[3] / len]
    } else {
        [1.0, 0.0, 0.0, 0.0]
    }
}

// ============================================================================
// ZX FFI Integration
// ============================================================================

#[cfg(feature = "zx")]
mod zx_integration {
    use super::*;

    extern "C" {
        fn set_bones(bones: *const f32, count: u32);
    }

    /// Apply BVH animation to ZX skeletal mesh
    pub fn apply_bvh_animation(clip: &BvhClip, time: f32, position_scale: f32) {
        let matrices = bvh_time_to_zx(clip, time, position_scale);

        unsafe {
            set_bones(matrices.as_ptr() as *const f32, matrices.len() as u32);
        }
    }

    /// Animation player for ZX games
    pub struct BvhPlayer {
        clip: BvhClip,
        time: f32,
        speed: f32,
        looping: bool,
        position_scale: f32,
    }

    impl BvhPlayer {
        pub fn new(clip: BvhClip) -> Self {
            Self {
                clip,
                time: 0.0,
                speed: 1.0,
                looping: true,
                position_scale: 0.01, // CMU default
            }
        }

        pub fn with_scale(mut self, scale: f32) -> Self {
            self.position_scale = scale;
            self
        }

        pub fn set_speed(&mut self, speed: f32) {
            self.speed = speed;
        }

        pub fn set_looping(&mut self, looping: bool) {
            self.looping = looping;
        }

        pub fn update(&mut self, dt: f32) {
            self.time += dt * self.speed;

            let duration = self.clip.duration();
            if self.looping {
                while self.time >= duration {
                    self.time -= duration;
                }
            } else {
                self.time = self.time.min(duration);
            }
        }

        pub fn apply(&self) {
            apply_bvh_animation(&self.clip, self.time, self.position_scale);
        }

        pub fn is_finished(&self) -> bool {
            !self.looping && self.time >= self.clip.duration()
        }
    }
}

// ============================================================================
// Usage Example
// ============================================================================

fn main() {
    // Example: Convert BVH to ZX bone matrices
    let bvh_content = std::fs::read_to_string("walk.bvh").expect("Failed to read BVH");
    let clip = BvhClip::parse(&bvh_content).expect("Failed to parse BVH");

    println!("Converting BVH to ZX bone matrices...");
    println!("  Joints: {}", clip.joints.len());
    println!("  Frames: {}", clip.frame_count);

    // Convert first frame with CMU scaling (cm to m)
    let matrices = bvh_frame_to_zx(&clip, 0, 0.01);

    println!("\nFrame 0 bone matrices:");
    for (i, mat) in matrices.iter().enumerate() {
        let joint_name = &clip.joints[i].name;
        println!("  {}: translation = ({:.3}, {:.3}, {:.3})", joint_name, mat[9], mat[10], mat[11]);
    }

    // Example: Interpolated sampling
    let time = 0.5; // 0.5 seconds into animation
    let matrices_interp = bvh_time_to_zx(&clip, time, 0.01);
    println!("\nAt t={:.2}s: {} bone matrices generated", time, matrices_interp.len());
}
