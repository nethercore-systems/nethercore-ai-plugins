# Complete Rust Debug Setup Example

A complete example showing debug system integration in a Rust ZX game.

## Full Working Example

```rust
#![no_std]
#![no_main]

mod ffi;
use ffi::*;

// =============================================================================
// GAME STATE (auto-snapshotted for rollback)
// =============================================================================

// Player state
static mut PLAYER_X: f32 = 480.0;
static mut PLAYER_Y: f32 = 270.0;
static mut PLAYER_VEL_X: f32 = 0.0;
static mut PLAYER_VEL_Y: f32 = 0.0;
static mut PLAYER_HEALTH: f32 = 100.0;
static mut PLAYER_POS: [f32; 3] = [0.0, 0.0, 0.0];

// Tunable physics parameters
static mut MOVE_SPEED: f32 = 200.0;
static mut JUMP_FORCE: f32 = 400.0;
static mut GRAVITY: f32 = 800.0;
static mut FRICTION: f32 = 0.9;
static mut GROUND_Y: f32 = 400.0;

// Debug toggles
static mut GOD_MODE: u8 = 0;
static mut SHOW_HITBOXES: u8 = 0;
static mut SHOW_DEBUG_INFO: u8 = 1;

// Stats (read-only watches)
static mut FRAME_COUNT: u32 = 0;
static mut JUMPS: u32 = 0;
static mut MAX_HEIGHT: f32 = 0.0;

// Colors (with color picker)
static mut PLAYER_COLOR: [u8; 4] = [255, 100, 100, 255];
static mut BG_COLOR: [u8; 4] = [26, 26, 46, 255];

// =============================================================================
// INIT - Register all debug values
// =============================================================================

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        // Configure game
        set_clear_color(0x1a1a2eFF);
        render_mode(0); // Lambert for simple 2D

        // =====================================================================
        // DEBUG REGISTRATION
        // =====================================================================

        // --- Player Group (collapsible) ---
        debug_group_begin(b"Player".as_ptr(), 6);

        // Watch position/velocity (read-only)
        debug_watch_f32(b"X".as_ptr(), 1, &PLAYER_X);
        debug_watch_f32(b"Y".as_ptr(), 1, &PLAYER_Y);
        debug_watch_f32(b"Vel X".as_ptr(), 5, &PLAYER_VEL_X);
        debug_watch_f32(b"Vel Y".as_ptr(), 5, &PLAYER_VEL_Y);

        // Editable health with slider (0-100)
        debug_register_f32_range(
            b"Health".as_ptr(), 6,
            &PLAYER_HEALTH, 0.0, 100.0
        );

        // Player tint color with color picker
        debug_register_color(b"Color".as_ptr(), 5, PLAYER_COLOR.as_ptr());

        debug_group_end();

        // --- Physics Group ---
        debug_group_begin(b"Physics".as_ptr(), 7);

        debug_register_f32_range(
            b"Speed".as_ptr(), 5,
            &MOVE_SPEED, 50.0, 500.0
        );
        debug_register_f32_range(
            b"Jump".as_ptr(), 4,
            &JUMP_FORCE, 100.0, 800.0
        );
        debug_register_f32_range(
            b"Gravity".as_ptr(), 7,
            &GRAVITY, 200.0, 1500.0
        );
        debug_register_f32_range(
            b"Friction".as_ptr(), 8,
            &FRICTION, 0.5, 1.0
        );
        debug_register_f32_range(
            b"Ground".as_ptr(), 6,
            &GROUND_Y, 100.0, 500.0
        );

        debug_group_end();

        // --- Debug Options ---
        debug_group_begin(b"Options".as_ptr(), 7);

        debug_register_bool(b"God Mode".as_ptr(), 8, &GOD_MODE);
        debug_register_bool(b"Hitboxes".as_ptr(), 8, &SHOW_HITBOXES);
        debug_register_bool(b"Info".as_ptr(), 4, &SHOW_DEBUG_INFO);
        debug_register_color(b"BG Color".as_ptr(), 8, BG_COLOR.as_ptr());

        debug_group_end();

        // --- Stats (all read-only) ---
        debug_group_begin(b"Stats".as_ptr(), 5);

        debug_watch_u32(b"Frames".as_ptr(), 6, &FRAME_COUNT);
        debug_watch_u32(b"Jumps".as_ptr(), 5, &JUMPS);
        debug_watch_f32(b"Max Height".as_ptr(), 10, &MAX_HEIGHT);

        debug_group_end();
    }
}

// =============================================================================
// UPDATE - Deterministic game logic
// =============================================================================

#[no_mangle]
pub extern "C" fn update() {
    unsafe {
        // Respect debug pause (F5)
        if debug_is_paused() != 0 {
            return;
        }

        // Get delta time with time scale applied (F7/F8)
        let dt = delta_time() * debug_get_time_scale();

        // Update stats
        FRAME_COUNT = tick_count() as u32;

        // --- Input ---
        let move_x = left_stick_x(0);

        // Apply horizontal movement
        PLAYER_VEL_X = move_x * MOVE_SPEED;

        // Jump (only when grounded)
        if button_pressed(0, button::A) != 0 && PLAYER_Y >= GROUND_Y {
            PLAYER_VEL_Y = -JUMP_FORCE;
            JUMPS += 1;
        }

        // --- Physics ---
        // Apply gravity
        PLAYER_VEL_Y += GRAVITY * dt;

        // Apply friction
        PLAYER_VEL_X *= FRICTION;

        // Update position
        PLAYER_X += PLAYER_VEL_X * dt;
        PLAYER_Y += PLAYER_VEL_Y * dt;

        // Ground collision
        if PLAYER_Y > GROUND_Y {
            PLAYER_Y = GROUND_Y;
            PLAYER_VEL_Y = 0.0;
        }

        // Screen boundaries
        PLAYER_X = PLAYER_X.clamp(20.0, 940.0);

        // Track max height (lowest Y = highest point)
        let height = GROUND_Y - PLAYER_Y;
        if height > MAX_HEIGHT {
            MAX_HEIGHT = height;
        }

        // Update 3D position for vec3 watch
        PLAYER_POS[0] = PLAYER_X;
        PLAYER_POS[1] = PLAYER_Y;
        PLAYER_POS[2] = 0.0;

        // --- Take damage (unless god mode) ---
        if GOD_MODE == 0 {
            // Example: lose health over time
            // PLAYER_HEALTH -= 0.01;
        }
    }
}

// =============================================================================
// RENDER - Drawing only, no state changes!
// =============================================================================

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        // Dynamic background color from debug panel
        let bg = pack_color(&BG_COLOR);
        // Note: can't change clear color after init, but we can draw a rect
        draw_rect(0.0, 0.0, 960.0, 540.0, bg);

        // Draw ground
        draw_rect(0.0, GROUND_Y + 20.0, 960.0, 120.0, 0x333355FF);

        // Draw player
        let color = pack_color(&PLAYER_COLOR);
        draw_rect(PLAYER_X - 20.0, PLAYER_Y - 40.0, 40.0, 40.0, color);

        // Draw hitbox overlay if enabled
        if SHOW_HITBOXES != 0 {
            draw_rect(PLAYER_X - 20.0, PLAYER_Y - 40.0, 40.0, 40.0, 0x00FF0040);
        }

        // Draw debug HUD if enabled
        if SHOW_DEBUG_INFO != 0 {
            let y = 10.0;
            draw_text_str("Press F3 for debug panel", 10.0, y, 16.0, 0xFFFFFFFF);
            draw_text_str("F5=Pause F6=Step F7/F8=Speed", 10.0, y + 20.0, 16.0, 0xAAAAFFFF);

            // Health bar
            draw_rect(10.0, 60.0, 100.0, 8.0, 0x440000FF);
            draw_rect(10.0, 60.0, PLAYER_HEALTH, 8.0, 0xFF0000FF);
        }
    }
}

// =============================================================================
// HELPERS
// =============================================================================

fn pack_color(rgba: &[u8; 4]) -> u32 {
    ((rgba[0] as u32) << 24) |
    ((rgba[1] as u32) << 16) |
    ((rgba[2] as u32) << 8) |
    (rgba[3] as u32)
}

// Panic handler for no_std
#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}
```

## Key Patterns Demonstrated

### 1. Grouping Related Values
```rust
debug_group_begin(b"Player".as_ptr(), 6);
// ... player values ...
debug_group_end();
```

### 2. Watch vs Register
- `debug_watch_*` - Read-only display
- `debug_register_*` - Editable

### 3. Range Sliders
```rust
debug_register_f32_range(b"Speed".as_ptr(), 5, &SPEED, 50.0, 500.0);
```

### 4. Respecting Pause/Time Scale
```rust
if debug_is_paused() != 0 { return; }
let dt = delta_time() * debug_get_time_scale();
```

### 5. Debug Toggles
```rust
static mut SHOW_HITBOXES: u8 = 0;
// In render:
if SHOW_HITBOXES != 0 { /* draw debug overlay */ }
```

## Running Debug Sessions

```bash
# Normal run with debug available
nether run

# Sync test to check determinism
nether run --sync-test

# P2P test for multiplayer debugging
nether run --p2p-test
```

## Workflow Tips

1. **Start with groups** - Organize early, easier to navigate
2. **Watch first** - Use watches until you need editing
3. **Range sliders** - Much easier to tune than typing values
4. **Color pickers** - Great for visual polish
5. **Toggle booleans** - Quick A/B testing
