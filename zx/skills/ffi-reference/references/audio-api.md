# ZX Audio API

## Sound Effects

| Function | Purpose |
|----------|---------|
| `load_sound(data, len)` | Load sound from bytes |
| `rom_sound_str(id)` | Get sound handle from ROM |
| `play_sound(handle, volume, pan)` | Play sound once |
| `channel_play(channel, handle, volume, pan, looping)` | Play on a channel |
| `channel_set(channel, volume, pan)` | Update a channel |
| `channel_stop(channel)` | Stop a channel |

## Music

| Function | Purpose |
|----------|---------|
| `rom_tracker_str(id)` | Get tracker music handle from ROM |
| `music_play(handle, volume, looping)` | Start music |
| `music_stop()` | Stop music |
| `music_pause(paused)` | Pause (`1`) or resume (`0`) music |
| `music_set_volume(vol)` | Set music volume (0.0-1.0) |

## Parameters

| Parameter | Range | Default |
|-----------|-------|---------|
| Volume | 0.0 - 1.0 | 1.0 |
| Pan | -1.0 (left) to 1.0 (right) | 0.0 (center) |
| Pitch | 0.5 - 2.0 | 1.0 |

## Audio Specs

- Sample rate: 22,050 Hz
- Format: 16-bit signed PCM, mono
- Sound channels: 16 simultaneous
- Music channel: 1 dedicated

## Example Usage

```rust
static mut JUMP_SFX: u32 = 0;
static mut THEME: u32 = 0;

fn init() {
    unsafe {
        JUMP_SFX = rom_sound_str("jump");
        THEME = rom_tracker_str("theme");
        music_play(THEME, 1.0, 1); // volume, looping
    }
}

fn play_jump() {
    unsafe {
        // Play with the current volume and pan
        play_sound(JUMP_SFX, 1.0, 0.0);
    }
}
```
