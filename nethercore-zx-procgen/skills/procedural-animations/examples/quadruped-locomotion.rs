//! Quadruped Locomotion
//!
//! Procedural walk/run cycles for four-legged creatures.
//! Demonstrates diagonal gait (walk) and bound gait (run).

#![no_std]
#![no_main]

mod ffi;
use ffi::*;
use core::f32::consts::PI;

// Bone structure for a quadruped
mod bones {
    pub const ROOT: usize = 0;
    pub const BODY: usize = 1;
    pub const NECK: usize = 2;
    pub const HEAD: usize = 3;
    pub const TAIL_BASE: usize = 4;
    pub const TAIL_MID: usize = 5;
    pub const TAIL_TIP: usize = 6;

    // Front Left leg
    pub const FL_SHOULDER: usize = 7;
    pub const FL_ELBOW: usize = 8;
    pub const FL_WRIST: usize = 9;

    // Front Right leg
    pub const FR_SHOULDER: usize = 10;
    pub const FR_ELBOW: usize = 11;
    pub const FR_WRIST: usize = 12;

    // Back Left leg
    pub const BL_HIP: usize = 13;
    pub const BL_KNEE: usize = 14;
    pub const BL_ANKLE: usize = 15;

    // Back Right leg
    pub const BR_HIP: usize = 16;
    pub const BR_KNEE: usize = 17;
    pub const BR_ANKLE: usize = 18;
}

const BONE_COUNT: usize = 19;

static mut SKELETON: u32 = 0;
static mut MESH: u32 = 0;
static mut BONE_MATRICES: [[f32; 12]; BONE_COUNT] = [[0.0; 12]; BONE_COUNT];

// Animation state
static mut SPEED: f32 = 0.0;
static mut IS_RUNNING: bool = false;

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        render_mode(2);
        set_clear_color(0x87CEEBFF);

        SKELETON = rom_skeleton_str("quadruped_rig");
        MESH = rom_mesh_str("quadruped");

        for i in 0..BONE_COUNT {
            BONE_MATRICES[i] = identity();
        }
    }
}

#[no_mangle]
pub extern "C" fn update() {
    unsafe {
        // Read input
        let forward = left_stick_y(0);
        let run_button = button_held(0, 4);  // A button

        SPEED = forward.abs();
        IS_RUNNING = run_button != 0 && SPEED > 0.5;
    }
}

#[no_mangle]
pub extern "C" fn render() {
    let time = unsafe { elapsed_time() };

    unsafe {
        camera_set(0.0, 2.0, 5.0, 0.0, 0.5, 0.0);
        light_set(0, 0.5, -1.0, 0.3);
        light_intensity(0, 1.5);
        draw_env();

        // Calculate animation
        if SPEED > 0.1 {
            if IS_RUNNING {
                calculate_gallop(time, SPEED);
            } else {
                calculate_walk(time, SPEED);
            }
        } else {
            calculate_idle(time);
        }

        // Draw creature
        skeleton_bind(SKELETON);
        set_bones(BONE_MATRICES.as_ptr() as *const f32, BONE_COUNT as u32);
        draw_mesh(MESH);
    }
}

fn calculate_walk(time: f32, speed: f32) {
    // Diagonal gait: FL+BR, FR+BL move together
    let cycle = (time * speed * 2.0) % 1.0;
    let phase = cycle * 2.0 * PI;

    unsafe {
        // Body pitch/roll
        BONE_MATRICES[bones::BODY] = rotation_x(3.0 * (phase * 2.0).sin());

        // Front Left + Back Right (phase 0)
        let fl_shoulder = 25.0 * phase.sin();
        let fl_elbow = 20.0 * (phase + PI * 0.5).sin().max(0.0);
        let br_hip = 30.0 * phase.sin();
        let br_knee = 35.0 * (phase + PI * 0.5).sin().max(0.0);

        BONE_MATRICES[bones::FL_SHOULDER] = rotation_x(fl_shoulder);
        BONE_MATRICES[bones::FL_ELBOW] = rotation_x(fl_elbow);
        BONE_MATRICES[bones::BR_HIP] = rotation_x(br_hip);
        BONE_MATRICES[bones::BR_KNEE] = rotation_x(br_knee);

        // Front Right + Back Left (phase PI)
        let fr_shoulder = 25.0 * (phase + PI).sin();
        let fr_elbow = 20.0 * (phase + PI * 1.5).sin().max(0.0);
        let bl_hip = 30.0 * (phase + PI).sin();
        let bl_knee = 35.0 * (phase + PI * 1.5).sin().max(0.0);

        BONE_MATRICES[bones::FR_SHOULDER] = rotation_x(fr_shoulder);
        BONE_MATRICES[bones::FR_ELBOW] = rotation_x(fr_elbow);
        BONE_MATRICES[bones::BL_HIP] = rotation_x(bl_hip);
        BONE_MATRICES[bones::BL_KNEE] = rotation_x(bl_knee);

        // Tail follows body
        calculate_tail(time, 0.5);
    }
}

fn calculate_gallop(time: f32, speed: f32) {
    // Bound gait: front legs together, back legs together
    let cycle = (time * speed * 3.0) % 1.0;
    let phase = cycle * 2.0 * PI;

    unsafe {
        // Strong spine flexion (bunny hop)
        let spine_flex = 15.0 * phase.sin();
        BONE_MATRICES[bones::BODY] = rotation_x(spine_flex);

        // Front legs together
        let front_shoulder = 40.0 * phase.sin();
        let front_elbow = 35.0 * (phase + PI * 0.3).sin().max(0.0);

        BONE_MATRICES[bones::FL_SHOULDER] = rotation_x(front_shoulder);
        BONE_MATRICES[bones::FL_ELBOW] = rotation_x(front_elbow);
        BONE_MATRICES[bones::FR_SHOULDER] = rotation_x(front_shoulder);
        BONE_MATRICES[bones::FR_ELBOW] = rotation_x(front_elbow);

        // Back legs together (offset phase)
        let back_phase = phase + PI * 0.5;
        let back_hip = 50.0 * back_phase.sin();
        let back_knee = 45.0 * (back_phase + PI * 0.3).sin().max(0.0);

        BONE_MATRICES[bones::BL_HIP] = rotation_x(back_hip);
        BONE_MATRICES[bones::BL_KNEE] = rotation_x(back_knee);
        BONE_MATRICES[bones::BR_HIP] = rotation_x(back_hip);
        BONE_MATRICES[bones::BR_KNEE] = rotation_x(back_knee);

        // Tail streams behind during run
        calculate_tail(time, 1.0);
    }
}

fn calculate_idle(time: f32) {
    // Subtle breathing and head movement
    let breath = (time * 0.5).sin();

    unsafe {
        BONE_MATRICES[bones::BODY] = rotation_x(breath * 2.0);

        // Slight head movement
        BONE_MATRICES[bones::HEAD] = combine(
            rotation_x((time * 0.3).sin() * 3.0),
            rotation_y((time * 0.2).sin() * 5.0)
        );

        // Reset legs to neutral
        BONE_MATRICES[bones::FL_SHOULDER] = identity();
        BONE_MATRICES[bones::FL_ELBOW] = rotation_x(10.0);
        BONE_MATRICES[bones::FR_SHOULDER] = identity();
        BONE_MATRICES[bones::FR_ELBOW] = rotation_x(10.0);
        BONE_MATRICES[bones::BL_HIP] = identity();
        BONE_MATRICES[bones::BL_KNEE] = rotation_x(15.0);
        BONE_MATRICES[bones::BR_HIP] = identity();
        BONE_MATRICES[bones::BR_KNEE] = rotation_x(15.0);

        calculate_tail(time, 0.2);
    }
}

fn calculate_tail(time: f32, intensity: f32) {
    // Cascading wave through tail
    let wave = time * 3.0;

    unsafe {
        BONE_MATRICES[bones::TAIL_BASE] = combine(
            rotation_x(intensity * 10.0 * wave.sin()),
            rotation_y(intensity * 15.0 * (wave * 0.7).sin())
        );

        BONE_MATRICES[bones::TAIL_MID] = combine(
            rotation_x(intensity * 15.0 * (wave + 0.3).sin()),
            rotation_y(intensity * 20.0 * (wave * 0.7 + 0.3).sin())
        );

        BONE_MATRICES[bones::TAIL_TIP] = combine(
            rotation_x(intensity * 20.0 * (wave + 0.6).sin()),
            rotation_y(intensity * 25.0 * (wave * 0.7 + 0.6).sin())
        );
    }
}

// Matrix utilities
fn identity() -> [f32; 12] {
    [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
}

fn rotation_x(deg: f32) -> [f32; 12] {
    let r = deg * PI / 180.0;
    let c = r.cos();
    let s = r.sin();
    [1.0, 0.0, 0.0, 0.0, c, s, 0.0, -s, c, 0.0, 0.0, 0.0]
}

fn rotation_y(deg: f32) -> [f32; 12] {
    let r = deg * PI / 180.0;
    let c = r.cos();
    let s = r.sin();
    [c, 0.0, -s, 0.0, 1.0, 0.0, s, 0.0, c, 0.0, 0.0, 0.0]
}

fn combine(a: [f32; 12], b: [f32; 12]) -> [f32; 12] {
    // Simplified matrix multiply for rotations only
    [
        a[0]*b[0] + a[3]*b[1] + a[6]*b[2],
        a[1]*b[0] + a[4]*b[1] + a[7]*b[2],
        a[2]*b[0] + a[5]*b[1] + a[8]*b[2],
        a[0]*b[3] + a[3]*b[4] + a[6]*b[5],
        a[1]*b[3] + a[4]*b[4] + a[7]*b[5],
        a[2]*b[3] + a[5]*b[4] + a[8]*b[5],
        a[0]*b[6] + a[3]*b[7] + a[6]*b[8],
        a[1]*b[6] + a[4]*b[7] + a[7]*b[8],
        a[2]*b[6] + a[5]*b[7] + a[8]*b[8],
        0.0, 0.0, 0.0,
    ]
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
