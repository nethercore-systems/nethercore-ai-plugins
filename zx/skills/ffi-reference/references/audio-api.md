# ZX Audio API

## Sound Effects

| Function | Purpose |
|----------|---------|
| `load_sound(data, len)` | Load sound from bytes |
| `rom_sound_str(id)` | Get sound handle from ROM |
| `play_sound(handle)` | Play sound once |
| `play_sound_ex(handle, vol, pan, pitch)` | Play with parameters |
| `stop_sound(handle)` | Stop playing sound |

## Music

| Function | Purpose |
|----------|---------|
| `rom_music_str(id)` | Get music handle from ROM |
| `music_play(handle)` | Start music (loops) |
| `music_stop()` | Stop music |
| `music_pause()` | Pause music |
| `music_resume()` | Resume paused music |
| `music_volume(vol)` | Set music volume (0.0-1.0) |

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
        THEME = rom_music_str("theme");
        music_play(THEME);
    }
}

fn play_jump() {
    unsafe {
        // Play with slight pitch variation
        let pitch = 0.9 + random_f32() * 0.2;
        play_sound_ex(JUMP_SFX, 1.0, 0.0, pitch);
    }
}
```
