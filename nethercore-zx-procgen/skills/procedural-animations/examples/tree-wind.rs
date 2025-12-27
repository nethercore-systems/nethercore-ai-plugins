//! Tree Wind Animation
//!
//! Demonstrates organic procedural animation for trees/plants:
//! - Multi-frequency wind response
//! - Hierarchical bending (trunk → branches → leaves)
//! - Random variation between instances

#![no_std]
#![no_main]

mod ffi;
use ffi::*;
use core::f32::consts::PI;

static mut TRUNK: u32 = 0;
static mut BRANCH: u32 = 0;
static mut LEAVES: u32 = 0;

// Wind parameters
struct WindParams {
    strength: f32,
    direction: f32,  // Radians
    gust_frequency: f32,
    gust_strength: f32,
}

static mut WIND: WindParams = WindParams {
    strength: 0.5,
    direction: 0.0,
    gust_frequency: 0.3,
    gust_strength: 0.3,
};

// Tree configuration
struct TreeConfig {
    trunk_height: f32,
    branch_count: u32,
    branch_layers: u32,
}

const TREE: TreeConfig = TreeConfig {
    trunk_height: 3.0,
    branch_count: 5,
    branch_layers: 3,
};

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        render_mode(2);
        set_clear_color(0x87CEEBFF);

        // Simple procedural meshes
        TRUNK = cylinder(0.2, 0.15, TREE.trunk_height, 8);
        BRANCH = cylinder(0.08, 0.04, 1.5, 6);
        LEAVES = sphere(0.4, 8, 6);
    }
}

#[no_mangle]
pub extern "C" fn update() {
    // Update wind
    let t = unsafe { elapsed_time() };

    unsafe {
        // Slowly rotating wind direction
        WIND.direction = t * 0.1;

        // Varying strength with gusts
        let gust = ((t * WIND.gust_frequency * 2.0 * PI).sin() + 1.0) / 2.0;
        WIND.strength = 0.3 + gust * WIND.gust_strength;
    }
}

#[no_mangle]
pub extern "C" fn render() {
    let t = unsafe { elapsed_time() };

    unsafe {
        camera_set(0.0, 2.0, 8.0, 0.0, 2.0, 0.0);
        light_set(0, 0.5, -1.0, 0.3);
        light_intensity(0, 1.5);
        draw_env();

        // Draw a small grove of trees
        for i in 0..5 {
            let x = (i as f32 - 2.0) * 3.0;
            let z = ((i * 7) % 3) as f32 - 1.0;
            let seed = i as f32 * 1.234;

            push_identity();
            push_translate(x, 0.0, z);
            draw_tree(t, seed);
        }
    }
}

fn draw_tree(time: f32, seed: f32) {
    unsafe {
        // Calculate wind effect at this tree
        let local_wind = calculate_wind(time, seed);

        // Trunk bending (slow, low amplitude)
        let trunk_bend = local_wind.primary * 5.0;  // degrees

        push_translate(0.0, TREE.trunk_height / 2.0, 0.0);
        push_rotate_x(trunk_bend * WIND.direction.cos());
        push_rotate_z(trunk_bend * WIND.direction.sin());

        // Draw trunk
        set_color(0x8B4513FF);  // Brown
        draw_mesh(TRUNK);

        // Branches at different heights
        for layer in 0..TREE.branch_layers {
            let layer_height = 0.3 + (layer as f32 / TREE.branch_layers as f32) * 0.6;
            let layer_y = (layer_height - 0.5) * TREE.trunk_height;

            for b in 0..TREE.branch_count {
                let angle = (b as f32 / TREE.branch_count as f32) * 2.0 * PI;
                let branch_seed = seed + layer as f32 * 0.1 + b as f32 * 0.01;

                push_identity();

                // Position on trunk
                push_translate(0.0, layer_y, 0.0);

                // Inherit trunk rotation
                push_rotate_x(trunk_bend * WIND.direction.cos());
                push_rotate_z(trunk_bend * WIND.direction.sin());

                // Branch base angle
                push_rotate_y(angle.to_degrees());

                // Branch tilt outward
                let tilt = 30.0 + (layer as f32 * 10.0);
                push_rotate_z(tilt);

                // Wind effect on branch (faster response)
                let branch_wind = calculate_wind(time * 1.5, branch_seed);
                let branch_bend = (local_wind.primary + branch_wind.secondary) * 8.0;
                push_rotate_x(branch_bend);

                // Draw branch
                set_color(0x6B4423FF);
                draw_mesh(BRANCH);

                // Leaves at branch tip
                push_translate(0.0, 1.5, 0.0);

                // Leaf flutter (high frequency)
                let flutter = calculate_wind(time * 3.0, branch_seed + 0.5);
                push_rotate_x(flutter.tertiary * 15.0);
                push_rotate_z(flutter.tertiary * 10.0);

                // Seasonal color variation
                let green = 0x228B22FF;
                set_color(green);
                draw_mesh(LEAVES);
            }
        }
    }
}

struct WindEffect {
    primary: f32,    // Slow, whole-tree sway
    secondary: f32,  // Medium, branch movement
    tertiary: f32,   // Fast, leaf flutter
}

fn calculate_wind(time: f32, seed: f32) -> WindEffect {
    unsafe {
        let wind_str = WIND.strength;

        // Primary: slow oscillation
        let primary = (time * 0.5 + seed).sin() * wind_str;

        // Secondary: medium frequency with harmonic
        let secondary = ((time * 1.3 + seed * 2.0).sin() +
                        (time * 2.1 + seed * 3.0).sin() * 0.5) * wind_str * 0.6;

        // Tertiary: fast flutter
        let tertiary = ((time * 4.7 + seed * 5.0).sin() +
                       (time * 7.3 + seed * 7.0).sin() * 0.3 +
                       (time * 11.0 + seed * 11.0).sin() * 0.1) * wind_str * 0.3;

        // Add gusts (irregular)
        let gust = ((time * WIND.gust_frequency + seed).sin() *
                   (time * WIND.gust_frequency * 1.7 + seed * 0.5).cos())
                   * WIND.gust_strength;

        WindEffect {
            primary: primary + gust * 0.5,
            secondary: secondary + gust * 0.3,
            tertiary: tertiary + gust * 0.2,
        }
    }
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
