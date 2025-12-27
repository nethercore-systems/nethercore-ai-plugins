//! Vehicle Physics Animation
//!
//! Demonstrates rigid body animation for a car with:
//! - Wheel rotation based on speed
//! - Front wheel steering
//! - Suspension compression
//! - Body pitch/roll from weight transfer

#![no_std]
#![no_main]

mod ffi;
use ffi::*;
use core::f32::consts::PI;

// Vehicle meshes
static mut BODY: u32 = 0;
static mut WHEEL: u32 = 0;

// Vehicle state
static mut SPEED: f32 = 0.0;
static mut STEERING: f32 = 0.0;
static mut WHEEL_ROTATIONS: [f32; 4] = [0.0; 4];
static mut SUSPENSIONS: [f32; 4] = [0.0; 4];
static mut SUSPENSION_VELOCITIES: [f32; 4] = [0.0; 4];

// Vehicle parameters
const WHEEL_RADIUS: f32 = 0.35;
const WHEEL_BASE: f32 = 2.5;      // Front to rear axle
const TRACK_WIDTH: f32 = 1.5;     // Left to right wheels
const MAX_STEER: f32 = 35.0;      // Max steering angle
const SPRING_K: f32 = 50.0;       // Suspension spring constant
const DAMPING: f32 = 5.0;         // Suspension damping
const SUSPENSION_TRAVEL: f32 = 0.15;

// Wheel positions (relative to body center)
const WHEEL_POSITIONS: [(f32, f32, f32); 4] = [
    (WHEEL_BASE / 2.0, 0.0, TRACK_WIDTH / 2.0),   // Front Right
    (WHEEL_BASE / 2.0, 0.0, -TRACK_WIDTH / 2.0),  // Front Left
    (-WHEEL_BASE / 2.0, 0.0, TRACK_WIDTH / 2.0),  // Rear Right
    (-WHEEL_BASE / 2.0, 0.0, -TRACK_WIDTH / 2.0), // Rear Left
];

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        render_mode(2);
        set_clear_color(0x87CEEBFF);

        BODY = rom_mesh_str("car_body");
        WHEEL = rom_mesh_str("car_wheel");
    }
}

#[no_mangle]
pub extern "C" fn update() {
    let dt = unsafe { delta_time() };

    unsafe {
        // Read input
        let throttle = trigger_right(0) - trigger_left(0);
        let steer_input = -left_stick_x(0);

        // Update speed
        SPEED += throttle * 10.0 * dt;
        SPEED *= 0.98;  // Friction

        // Update steering
        STEERING = steer_input * MAX_STEER;

        // Update wheel rotations based on speed
        let wheel_angular_velocity = SPEED / WHEEL_RADIUS;
        for i in 0..4 {
            WHEEL_ROTATIONS[i] += wheel_angular_velocity * dt * 57.2958; // rad/s to deg
        }

        // Simulate suspension
        for i in 0..4 {
            // Simple ground simulation (flat + bumps)
            let (x, _, z) = WHEEL_POSITIONS[i];
            let ground_height = simulate_ground(x, z);

            // Spring-damper physics
            let target = ground_height.clamp(0.0, SUSPENSION_TRAVEL);
            let spring_force = (target - SUSPENSIONS[i]) * SPRING_K;
            let damp_force = -SUSPENSION_VELOCITIES[i] * DAMPING;

            SUSPENSION_VELOCITIES[i] += (spring_force + damp_force) * dt;
            SUSPENSIONS[i] += SUSPENSION_VELOCITIES[i] * dt;
            SUSPENSIONS[i] = SUSPENSIONS[i].clamp(0.0, SUSPENSION_TRAVEL);
        }
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        // Camera follows vehicle (simplified - would track position in real game)
        camera_set(0.0, 5.0, 10.0, 0.0, 0.5, 0.0);

        light_set(0, 0.3, -0.8, 0.5);
        light_intensity(0, 1.5);
        draw_env();

        // Calculate body pitch and roll from suspension
        let front_avg = (SUSPENSIONS[0] + SUSPENSIONS[1]) / 2.0;
        let rear_avg = (SUSPENSIONS[2] + SUSPENSIONS[3]) / 2.0;
        let left_avg = (SUSPENSIONS[1] + SUSPENSIONS[3]) / 2.0;
        let right_avg = (SUSPENSIONS[0] + SUSPENSIONS[2]) / 2.0;

        let body_pitch = (rear_avg - front_avg) * 100.0;  // Degrees
        let body_roll = (right_avg - left_avg) * 80.0;
        let body_height = 0.5 - (SUSPENSIONS[0] + SUSPENSIONS[1] + SUSPENSIONS[2] + SUSPENSIONS[3]) / 4.0;

        // Draw body with pitch/roll
        push_identity();
        push_translate(0.0, body_height, 0.0);
        push_rotate_x(body_pitch);
        push_rotate_z(body_roll);
        draw_mesh(BODY);

        // Draw wheels
        for i in 0..4 {
            let (x, _, z) = WHEEL_POSITIONS[i];
            let is_front = i < 2;

            push_identity();

            // Position at wheel mount
            push_translate(x, body_height - SUSPENSIONS[i], z);

            // Apply body rotation to wheel position
            push_rotate_x(body_pitch);
            push_rotate_z(body_roll);

            // Steering (front wheels only)
            if is_front {
                push_rotate_y(STEERING);
            }

            // Wheel spin
            push_rotate_z(WHEEL_ROTATIONS[i]);

            draw_mesh(WHEEL);
        }
    }
}

fn simulate_ground(x: f32, _z: f32) -> f32 {
    // Simple procedural bumps
    let t = unsafe { elapsed_time() };
    let bump = ((x + t * unsafe { SPEED } * 0.5) * 2.0).sin() * 0.02;
    bump.max(0.0)
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
