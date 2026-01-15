# ZX Input API

## Determinism Note

All input functions return **deterministic values** synchronized by the netcode. Call them in `update()` - the values are identical across all clients for the same frame. Never cache input state across frames.

## Button Functions

| Function | Returns | Purpose |
|----------|---------|---------|
| `button_held(player, btn)` | bool | Button currently down |
| `button_pressed(player, btn)` | bool | Button just pressed this frame |
| `button_released(player, btn)` | bool | Button just released this frame |

## Button Constants

| Button | Value | Physical |
|--------|-------|----------|
| `BTN_A` | 0 | A / Cross |
| `BTN_B` | 1 | B / Circle |
| `BTN_X` | 2 | X / Square |
| `BTN_Y` | 3 | Y / Triangle |
| `BTN_L1` | 4 | Left bumper |
| `BTN_R1` | 5 | Right bumper |
| `BTN_L3` | 6 | Left stick click |
| `BTN_R3` | 7 | Right stick click |
| `BTN_START` | 8 | Start/Menu |
| `BTN_SELECT` | 9 | Select/Back |
| `BTN_UP` | 10 | D-pad up |
| `BTN_DOWN` | 11 | D-pad down |
| `BTN_LEFT` | 12 | D-pad left |
| `BTN_RIGHT` | 13 | D-pad right |

## Analog Functions

| Function | Range | Purpose |
|----------|-------|---------|
| `left_stick_x(player)` | -1.0 to 1.0 | Left stick horizontal |
| `left_stick_y(player)` | -1.0 to 1.0 | Left stick vertical |
| `right_stick_x(player)` | -1.0 to 1.0 | Right stick horizontal |
| `right_stick_y(player)` | -1.0 to 1.0 | Right stick vertical |
| `left_trigger(player)` | 0.0 to 1.0 | L2 trigger |
| `right_trigger(player)` | 0.0 to 1.0 | R2 trigger |

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
    if button_pressed(p, BTN_A) {
        jump();
    }

    // Analog input
    let move_x = left_stick_x(p);
    let move_y = left_stick_y(p);

    // Trigger
    let accel = right_trigger(p);
}
```
