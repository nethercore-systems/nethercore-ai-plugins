---
name: Procedural Sound Generation
description: This skill should be used when the user asks to "generate sound", "create sound effect", "procedural audio", "synth sound", "synthesize sound", "ADSR envelope", "oscillator", "audio filter", "make SFX", "retro sound effect", or mentions sound synthesis, audio generation, waveform synthesis, or procedural audio for game assets. Provides comprehensive guidance for creating procedural sounds using any language/tool that outputs WAV files compatible with the Nethercore asset pipeline.
version: 1.1.0
---

# Procedural Sound Generation

## Build Integration

Sound generators are **native binaries** (not WASM). They run at build time via `nether.toml`'s `build.script`:

```toml
[build]
script = "cargo run -p generator --release && cargo build -p game --target wasm32-unknown-unknown --release"

[[assets.sounds]]
id = "laser"
path = "../assets/audio/laser.wav"
```

See the **Native Asset Pipeline** skill for full architecture details.

## Overview

Procedural audio is synthesized algorithmically rather than recorded. This enables:
- Infinite variations from parameters
- Tiny file sizes (code generates audio)
- Consistent retro aesthetic
- Perfect control over sound design

**Output Requirements for ZX:**
- Format: WAV (16-bit PCM)
- Sample rate: 22,050 Hz (ZX standard)
- Channels: Mono
- Max duration: A few seconds typically (VRAM budget)

**ZX Audio Capabilities:**
- 16 simultaneous sound channels
- 1 dedicated music channel (looping)
- Stereo panning (-1.0 to +1.0)

## Language/Tool Options

| Tool | Best For | Output |
|------|----------|--------|
| **Rust + proc-gen** | Integration with pipeline | WAV via `write_wav()` |
| **Python + numpy** | Rapid prototyping, complex synthesis | WAV via scipy/wave |
| **Pure Data / Max** | Visual audio programming | WAV export |
| **SuperCollider** | Advanced synthesis | WAV recording |
| **Audacity + Nyquist** | Quick experiments | WAV export |
| **JSFXR / Bfxr** | Retro game sounds | WAV export |

## Using the Rust proc-gen Library

The `nethercore/tools/proc-gen/src/audio/` module provides complete synthesis.

### Source Files (Canonical Reference)

| File | Purpose |
|------|---------|
| `audio/mod.rs` | Module exports, Synth high-level API |
| `audio/oscillators.rs` | Waveform generators |
| `audio/envelope.rs` | ADSR envelopes and presets |
| `audio/filters.rs` | Low-pass, high-pass, biquad |
| `audio/synth.rs` | Synth struct with preset methods |
| `audio/export.rs` | WAV file writing |
| `audio/showcase.rs` | Platform-wide showcase sounds |

### Quick Start (Rust)

```rust
use proc_gen::audio::*;

fn main() {
    let synth = Synth::new(SAMPLE_RATE);

    // Generate a coin pickup sound
    let samples = synth.coin();

    // Convert to 16-bit PCM and export
    let pcm = to_pcm_i16(&samples);
    write_wav(&pcm, SAMPLE_RATE, "assets/audio/coin.wav").unwrap();
}
```

### Cargo.toml Setup

```toml
[package]
name = "my-sound-gen"
version = "0.1.0"
edition = "2021"

[dependencies]
proc-gen = { path = "../nethercore/tools/proc-gen", features = ["wav-export"] }
```

## Waveforms

### Oscillator Types

```rust
pub enum Waveform {
    Sine,       // Pure tone, smooth
    Square,     // Hollow, retro, NES-like
    Saw,        // Bright, buzzy, aggressive
    Triangle,   // Soft, flute-like
    WhiteNoise, // All frequencies, harsh
    PinkNoise,  // Lower frequencies weighted, natural
}
```

### Usage

```rust
// Generate raw waveform samples
let sine_wave = oscillator(Waveform::Sine, frequency, duration, sample_rate);
let noise = oscillator(Waveform::WhiteNoise, 0.0, duration, sample_rate);
```

### Waveform Characteristics

| Waveform | Character | Best For |
|----------|-----------|----------|
| **Sine** | Pure, smooth | Beeps, pure tones, bass |
| **Square** | Hollow, retro | Chiptune, 8-bit sounds |
| **Saw** | Bright, harsh | Synth leads, lasers |
| **Triangle** | Soft, warm | Flutes, gentle sounds |
| **WhiteNoise** | Harsh, full-spectrum | Explosions, wind, static |
| **PinkNoise** | Natural, warm | Ocean, rain, whoosh |

## ADSR Envelopes

Envelopes shape volume over time:

```
    /\
   /  \____
  /        \
 /          \
A  D  S    R

A = Attack (fade in time)
D = Decay (drop to sustain)
S = Sustain (hold level)
R = Release (fade out)
```

### Envelope Structure

```rust
pub struct Envelope {
    pub attack: f32,   // seconds
    pub decay: f32,    // seconds
    pub sustain: f32,  // 0.0 to 1.0 (level)
    pub release: f32,  // seconds
}
```

### Envelope Presets

```rust
impl Envelope {
    fn pluck() -> Self;     // Quick attack, fast decay (piano, guitar)
    fn pad() -> Self;       // Slow attack, long sustain (strings, synth pads)
    fn hit() -> Self;       // Instant attack, no sustain (drums, impacts)
    fn zap() -> Self;       // Fast in/out (laser, zap)
    fn explosion() -> Self; // Medium attack, long decay
    fn click() -> Self;     // Instant, no tail (UI, ticks)
}
```

### Custom Envelope

```rust
let custom = Envelope {
    attack: 0.01,   // 10ms fade in
    decay: 0.1,     // 100ms decay
    sustain: 0.5,   // 50% sustain level
    release: 0.3,   // 300ms fade out
};
```

## Synth API

High-level sound generation:

### Basic Tone

```rust
let sound = synth.tone(
    Waveform::Square,
    440.0,           // frequency (Hz)
    0.5,             // duration (seconds)
    Envelope::pluck(),
);
```

### Frequency Sweep

```rust
let laser = synth.sweep(
    Waveform::Saw,
    1000.0,  // start frequency
    100.0,   // end frequency
    0.3,     // duration
    Envelope::zap(),
);
```

### Noise Burst

```rust
let explosion = synth.noise_burst(
    0.8,                   // duration
    Envelope::explosion(),
);
```

### Mix Multiple Sounds

```rust
let complex = synth.mix(&[
    (&tone1, 0.7),   // 70% volume
    (&tone2, 0.5),   // 50% volume
    (&noise, 0.3),   // 30% volume
]);
```

## Preset Sounds

Ready-to-use game sounds:

```rust
let coin = synth.coin();       // Pickup/collect
let jump = synth.jump();       // Jump action
let laser = synth.laser();     // Shoot/zap
let explosion = synth.explosion();  // Big boom
let hit = synth.hit();         // Damage/impact
let click = synth.click();     // UI interaction
let powerup = synth.powerup(); // Power-up collect
let death = synth.death();     // Game over/death
```

## Filters

Post-process audio for character:

### Low-Pass Filter

Removes high frequencies (muffles sound):

```rust
low_pass(&mut samples, cutoff_hz, sample_rate);
```

Use for: underwater effects, distance, warmth

### High-Pass Filter

Removes low frequencies (thins sound):

```rust
high_pass(&mut samples, cutoff_hz, sample_rate);
```

Use for: radio effect, tinny sounds, removing rumble

### Biquad Filter with Resonance

More musical filtering with resonance peak:

```rust
biquad_lowpass(&mut samples, cutoff_hz, resonance, sample_rate);
// resonance: 0.7 = flat, 1.0+ = resonant peak
```

## Advanced Techniques

### Layered Sounds

Combine multiple elements:

```rust
fn generate_explosion() -> Vec<f32> {
    let synth = Synth::new(SAMPLE_RATE);

    // Low rumble
    let rumble = synth.tone(
        Waveform::Sine,
        60.0,
        0.8,
        Envelope::explosion(),
    );

    // Mid crunch
    let crunch = synth.noise_burst(0.5, Envelope::hit());
    low_pass(&mut crunch, 2000.0, SAMPLE_RATE);

    // High sizzle
    let sizzle = synth.noise_burst(1.0, Envelope {
        attack: 0.05,
        decay: 0.8,
        sustain: 0.0,
        release: 0.2,
    });
    high_pass(&mut sizzle, 3000.0, SAMPLE_RATE);

    synth.mix(&[
        (&rumble, 0.6),
        (&crunch, 0.8),
        (&sizzle, 0.4),
    ])
}
```

### Pitch Variation

Add randomness for variety:

```rust
fn generate_hit_variation(seed: u32) -> Vec<f32> {
    let synth = Synth::new(SAMPLE_RATE);

    // Vary pitch based on seed
    let base_freq = 200.0;
    let variation = ((seed % 100) as f32 / 100.0 - 0.5) * 100.0;
    let freq = base_freq + variation;

    synth.tone(Waveform::Square, freq, 0.1, Envelope::hit())
}
```

### Arpeggio

Rising or falling notes:

```rust
fn generate_powerup() -> Vec<f32> {
    let synth = Synth::new(SAMPLE_RATE);
    let note_duration = 0.08;

    let notes = [262.0, 330.0, 392.0, 523.0]; // C E G C
    let mut result = Vec::new();

    for freq in notes {
        let note = synth.tone(
            Waveform::Square,
            freq,
            note_duration,
            Envelope::pluck(),
        );
        result.extend(note);
    }

    result
}
```

## Python Alternative

Using numpy for synthesis:

```python
import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 22050

def oscillator(waveform: str, freq: float, duration: float) -> np.ndarray:
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)

    if waveform == "sine":
        return np.sin(2 * np.pi * freq * t)
    elif waveform == "square":
        return np.sign(np.sin(2 * np.pi * freq * t))
    elif waveform == "saw":
        return 2 * (t * freq % 1) - 1
    elif waveform == "noise":
        return np.random.uniform(-1, 1, len(t))

def apply_envelope(samples: np.ndarray, adsr: tuple) -> np.ndarray:
    attack, decay, sustain, release = adsr
    total = len(samples) / SAMPLE_RATE

    envelope = np.ones(len(samples))
    # ... envelope shaping
    return samples * envelope

def generate_coin():
    tone1 = oscillator("square", 987.77, 0.1)  # B5
    tone2 = oscillator("square", 1318.5, 0.15) # E6
    return np.concatenate([tone1, tone2])

# Generate and save
coin = generate_coin()
coin_16bit = (coin * 32767).astype(np.int16)
wavfile.write("assets/audio/coin.wav", SAMPLE_RATE, coin_16bit)
```

## Integration with Nethercore

### Asset Pipeline

1. Generate WAV files to `assets/audio/`
2. Reference in `nether.toml`:
```toml
[[assets.sounds]]
id = "coin"
path = "assets/audio/coin.wav"
```
3. Run `nether pack` to bundle into ROM
4. Play in game:
```rust
let coin = rom_sound_str("coin");
play_sound(coin);
```

### Best Practices

1. **22,050 Hz sample rate**: ZX standard, saves memory
2. **Mono audio**: Stereo doubles size, panning done in playback
3. **Short durations**: 0.1-2 seconds typical for SFX
4. **Normalize**: Keep peaks at ~0.9 to avoid clipping
5. **Test in game**: Sounds differ in context

## Sound Design Reference

### Common Game Sounds

| Sound | Waveform | Technique |
|-------|----------|-----------|
| Coin | Square | Two ascending notes |
| Jump | Sine | Quick upward sweep |
| Laser | Saw | Downward sweep |
| Explosion | Noise + Sine | Layered, filtered |
| Hit | Square + Noise | Short burst |
| Menu Click | Square | Single short beep |
| Power-up | Square | Ascending arpeggio |
| Death | Square | Descending notes |

### Frequency Ranges

| Range | Frequency | Use |
|-------|-----------|-----|
| Sub-bass | 20-60 Hz | Rumble, impact |
| Bass | 60-250 Hz | Body, weight |
| Low-mid | 250-500 Hz | Warmth |
| Mid | 500-2000 Hz | Presence, clarity |
| High-mid | 2000-4000 Hz | Edge, bite |
| High | 4000+ Hz | Air, sparkle |

## Additional Resources

- `references/synth-api.md` - Complete API reference
- `references/presets.md` - Envelope and sound presets
- `examples/` - Game-specific sound generation
