# Hello World - Rust

Complete hello world example in Rust.

## Project Structure

```
hello-world/
├── Cargo.toml
├── nether.toml
└── src/
    └── lib.rs
```

## Cargo.toml

```toml
[package]
name = "hello-world"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[profile.release]
opt-level = "z"
lto = true
```

## nether.toml

```toml
[game]
id = "hello-world"
title = "Hello World"
author = "Developer"
version = "1.0.0"
```

## src/lib.rs

```rust
#![no_std]
#![no_main]

// Copy zx.rs from nethercore/include/ and include it
mod zx;
use zx::*;

#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}

static mut FRAME: u64 = 0;

#[no_mangle]
pub extern "C" fn init() {
    set_clear_color(0x1a1a2eFF);  // Dark blue background
    render_mode(0);               // Lambert mode for 2D
}

#[no_mangle]
pub extern "C" fn update() {
    unsafe {
        FRAME = tick_count();
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        // Animated color
        let t = elapsed_time();
        let r = ((t.sin() * 0.5 + 0.5) * 255.0) as u8;
        let g = (((t * 1.3).sin() * 0.5 + 0.5) * 255.0) as u8;
        let b = (((t * 1.7).sin() * 0.5 + 0.5) * 255.0) as u8;
        let color = rgba(r, g, b, 255);

        // Draw centered text
        draw_text_str("Hello, Nethercore ZX!", 280.0, 250.0, 32.0, color);

        // Frame counter
        let frame_text = format_frame(FRAME);
        draw_text_str(&frame_text, 10.0, 10.0, 16.0, 0xFFFFFF80);
    }
}

fn format_frame(frame: u64) -> &'static str {
    // In no_std, use a static buffer or just display fixed text
    "Press START to continue"
}
```

## Alternative: With std (Simpler)

If you don't need minimal binary size:

```rust
// No #![no_std] needed
mod zx;
use zx::*;

static mut PLAYER_X: f32 = 480.0;
static mut PLAYER_Y: f32 = 270.0;

#[no_mangle]
pub extern "C" fn init() {
    set_clear_color(0x1a1a2eFF);
    render_mode(0);
    log_str("Hello World initialized!");
}

#[no_mangle]
pub extern "C" fn update() {
    unsafe {
        let speed = 200.0 * delta_time();
        PLAYER_X += left_stick_x(0) * speed;
        PLAYER_Y += left_stick_y(0) * speed;

        // Clamp to screen
        PLAYER_X = PLAYER_X.clamp(16.0, 944.0);
        PLAYER_Y = PLAYER_Y.clamp(16.0, 524.0);
    }
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        // Background
        draw_rect(0.0, 0.0, 960.0, 540.0, 0x1a1a2eFF);

        // Player
        draw_rect(PLAYER_X - 16.0, PLAYER_Y - 16.0, 32.0, 32.0, 0xFF6B6BFF);

        // Instructions
        draw_text_str("Use left stick to move", 340.0, 500.0, 16.0, 0xFFFFFF80);
    }
}
```

## Build and Run

```bash
# Build
nether build

# Run
nether run

# Or in one step
nether run
```

## Reference

For the complete zx.rs file, copy from:
```
nethercore/include/zx.rs
```

Or reference existing examples:
```
nethercore/examples/1-getting-started/hello-world/
```
