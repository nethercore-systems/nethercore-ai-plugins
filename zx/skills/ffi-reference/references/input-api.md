# ZX Input API

## Determinism Note

Input FFI reads the host-mapped native controller state. In netplay, the
sampled values are synchronized for the same simulation frame. Call these
queries in `update()` and do not cache input state across frames.

## Button Functions

| Function | Returns (`u32`) | Purpose |
|----------|---------|---------|
| `button_held(player, btn)` | `1`/`0` | Button currently down |
| `button_pressed(player, btn)` | `1`/`0` | Button just pressed this frame |
| `button_released(player, btn)` | `1`/`0` | Button just released this frame |

## Button Constants

| Button | Value | Physical |
|--------|-------|----------|
| `button::UP` | 0 | D-pad up |
| `button::DOWN` | 1 | D-pad down |
| `button::LEFT` | 2 | D-pad left |
| `button::RIGHT` | 3 | D-pad right |
| `button::A` | 4 | A / Cross |
| `button::B` | 5 | B / Circle |
| `button::X` | 6 | X / Square |
| `button::Y` | 7 | Y / Triangle |
| `button::L1` | 8 | Left bumper |
| `button::R1` | 9 | Right bumper |
| `button::L3` | 10 | Left stick click |
| `button::R3` | 11 | Right stick click |
| `button::START` | 12 | Start/Menu |
| `button::SELECT` | 13 | Select/Back |

## Analog Functions

| Function | Range | Purpose |
|----------|-------|---------|
| `left_stick_x(player)` | -1.0 to 1.0 | Left stick horizontal |
| `left_stick_y(player)` | -1.0 to 1.0 | Left stick vertical |
| `right_stick_x(player)` | -1.0 to 1.0 | Right stick horizontal |
| `right_stick_y(player)` | -1.0 to 1.0 | Right stick vertical |
| `trigger_left(player)` | 0.0 to 1.0 | L2 trigger |
| `trigger_right(player)` | 0.0 to 1.0 | R2 trigger |

## Player Info

| Function | Purpose |
|----------|---------|
| `player_count()` | Number of active players (1-4) |
| `local_player_mask()` | Bitmask of local players |

## Example Usage

```rust
fn update() {
    let p = 0; // Player 0

    // Digital input
    if button_pressed(p, button::A) != 0 {
        jump();
    }

    // Analog input
    let move_x = left_stick_x(p);
    let move_y = left_stick_y(p);

    // Trigger
    let accel = trigger_right(p);
}
```
