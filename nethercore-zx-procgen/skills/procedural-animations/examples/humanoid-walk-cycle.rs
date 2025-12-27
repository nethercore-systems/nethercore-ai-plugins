//! Procedural Humanoid Walk Cycle
//!
//! Demonstrates pure procedural walk animation without keyframe data.
//! All motion is calculated from sine waves and phase offsets.

#![no_std]
#![no_main]

mod ffi;
use ffi::*;
use core::f32::consts::PI;

// Bone indices for a standard humanoid rig
mod bones {
    pub const ROOT: usize = 0;
    pub const PELVIS: usize = 1;
    pub const SPINE: usize = 2;
    pub const CHEST: usize = 3;
    pub const NECK: usize = 4;
    pub const HEAD: usize = 5;

    pub const L_SHOULDER: usize = 6;
    pub const L_ARM: usize = 7;
    pub const L_FOREARM: usize = 8;
    pub const L_HAND: usize = 9;

    pub const R_SHOULDER: usize = 10;
    pub const R_ARM: usize = 11;
    pub const R_FOREARM: usize = 12;
    pub const R_HAND: usize = 13;

    pub const L_THIGH: usize = 14;
    pub const L_SHIN: usize = 15;
    pub const L_FOOT: usize = 16;

    pub const R_THIGH: usize = 17;
    pub const R_SHIN: usize = 18;
    pub const R_FOOT: usize = 19;
}

const BONE_COUNT: usize = 20;

static mut SKELETON: u32 = 0;
static mut CHARACTER: u32 = 0;
static mut BONE_MATRICES: [[f32; 12]; BONE_COUNT] = [[0.0; 12]; BONE_COUNT];

// Walk parameters
struct WalkParams {
    speed: f32,           // Cycles per second
    stride_amplitude: f32, // Leg swing angle
    hip_bob: f32,         // Vertical bounce
    hip_sway: f32,        // Side-to-side motion
    spine_twist: f32,     // Counter-rotation
    arm_swing: f32,       // Arm swing amplitude
}

const WALK: WalkParams = WalkParams {
    speed: 1.0,
    stride_amplitude: 30.0,
    hip_bob: 0.03,
    hip_sway: 0.02,
    spine_twist: 8.0,
    arm_swing: 25.0,
};

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        render_mode(2);  // PBR
        set_clear_color(0x2a2a3aFF);

        // Load character from ROM
        SKELETON = rom_skeleton_str("humanoid_rig");
        CHARACTER = rom_mesh_str("humanoid");

        // Initialize all bones to identity
        for i in 0..BONE_COUNT {
            BONE_MATRICES[i] = identity_matrix();
        }
    }
}

#[no_mangle]
pub extern "C" fn update() {
    // Animation logic here for rollback-safe games
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        let time = elapsed_time();

        // Calculate walk animation
        calculate_walk_pose(time, &WALK);

        // Setup camera and lighting
        camera_set(0.0, 1.5, 4.0, 0.0, 1.0, 0.0);
        light_set(0, 0.5, -1.0, 0.3);
        light_intensity(0, 1.5);
        draw_env();

        // Draw character
        skeleton_bind(SKELETON);
        set_bones(BONE_MATRICES.as_ptr() as *const f32, BONE_COUNT as u32);
        draw_mesh(CHARACTER);
    }
}

fn calculate_walk_pose(time: f32, params: &WalkParams) {
    let cycle = (time * params.speed) % 1.0;
    let phase = cycle * 2.0 * PI;

    unsafe {
        // Root motion (forward movement would go here)
        BONE_MATRICES[bones::ROOT] = identity_matrix();

        // Pelvis: bob + sway
        let bob = params.hip_bob * (phase * 2.0).sin().abs();
        let sway = params.hip_sway * phase.sin();
        BONE_MATRICES[bones::PELVIS] = translation_matrix(sway, bob, 0.0);

        // Spine: counter-twist
        let twist = params.spine_twist * phase.sin();
        BONE_MATRICES[bones::SPINE] = rotation_y_matrix(twist.to_radians());

        // Chest: slight additional twist
        BONE_MATRICES[bones::CHEST] = rotation_y_matrix((twist * 0.3).to_radians());

        // Head: stabilization (counter the body movement)
        let head_counter = -twist * 0.5;
        BONE_MATRICES[bones::HEAD] = rotation_y_matrix(head_counter.to_radians());

        // Left leg (phase 0)
        let l_thigh_angle = params.stride_amplitude * phase.sin();
        let l_shin_angle = (params.stride_amplitude * 1.5) * (phase + PI * 0.5).sin().max(0.0);
        let l_foot_angle = -10.0 * phase.cos();

        BONE_MATRICES[bones::L_THIGH] = rotation_x_matrix(l_thigh_angle.to_radians());
        BONE_MATRICES[bones::L_SHIN] = rotation_x_matrix(l_shin_angle.to_radians());
        BONE_MATRICES[bones::L_FOOT] = rotation_x_matrix(l_foot_angle.to_radians());

        // Right leg (phase PI - opposite)
        let r_thigh_angle = params.stride_amplitude * (phase + PI).sin();
        let r_shin_angle = (params.stride_amplitude * 1.5) * (phase + PI * 1.5).sin().max(0.0);
        let r_foot_angle = -10.0 * (phase + PI).cos();

        BONE_MATRICES[bones::R_THIGH] = rotation_x_matrix(r_thigh_angle.to_radians());
        BONE_MATRICES[bones::R_SHIN] = rotation_x_matrix(r_shin_angle.to_radians());
        BONE_MATRICES[bones::R_FOOT] = rotation_x_matrix(r_foot_angle.to_radians());

        // Arms swing opposite to legs
        let l_arm_swing = -params.arm_swing * phase.sin();
        let r_arm_swing = -params.arm_swing * (phase + PI).sin();

        BONE_MATRICES[bones::L_ARM] = rotation_x_matrix(l_arm_swing.to_radians());
        BONE_MATRICES[bones::R_ARM] = rotation_x_matrix(r_arm_swing.to_radians());

        // Elbows bend slightly during forward swing
        let l_elbow = 20.0 + 15.0 * (phase + PI * 0.5).sin().max(0.0);
        let r_elbow = 20.0 + 15.0 * (phase + PI * 1.5).sin().max(0.0);

        BONE_MATRICES[bones::L_FOREARM] = rotation_x_matrix(l_elbow.to_radians());
        BONE_MATRICES[bones::R_FOREARM] = rotation_x_matrix(r_elbow.to_radians());
    }
}

// Matrix utilities
fn identity_matrix() -> [f32; 12] {
    [
        1.0, 0.0, 0.0,  // X axis
        0.0, 1.0, 0.0,  // Y axis
        0.0, 0.0, 1.0,  // Z axis
        0.0, 0.0, 0.0,  // Translation
    ]
}

fn translation_matrix(x: f32, y: f32, z: f32) -> [f32; 12] {
    [
        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0,
        x, y, z,
    ]
}

fn rotation_x_matrix(angle: f32) -> [f32; 12] {
    let c = angle.cos();
    let s = angle.sin();
    [
        1.0, 0.0, 0.0,
        0.0, c, s,
        0.0, -s, c,
        0.0, 0.0, 0.0,
    ]
}

fn rotation_y_matrix(angle: f32) -> [f32; 12] {
    let c = angle.cos();
    let s = angle.sin();
    [
        c, 0.0, -s,
        0.0, 1.0, 0.0,
        s, 0.0, c,
        0.0, 0.0, 0.0,
    ]
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
