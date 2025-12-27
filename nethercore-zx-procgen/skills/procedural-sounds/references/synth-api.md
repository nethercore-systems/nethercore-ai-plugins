# Synth API Quick Reference

## Constants

```rust
const SAMPLE_RATE: u32 = 22050;  // ZX standard
```

## Synth Creation

```rust
let synth = Synth::new(SAMPLE_RATE);
```

## Basic Synthesis

```rust
// Single tone
let sound = synth.tone(waveform, frequency, duration, envelope);

// Frequency sweep
let sound = synth.sweep(waveform, start_freq, end_freq, duration, envelope);

// Noise burst
let sound = synth.noise_burst(duration, envelope);

// Mix multiple sounds
let mixed = synth.mix(&[
    (&sound1, volume1),  // volume: 0.0 to 1.0
    (&sound2, volume2),
]);
```

## Waveforms

```rust
Waveform::Sine       // Pure, smooth
Waveform::Square     // Hollow, retro
Waveform::Saw        // Bright, buzzy
Waveform::Triangle   // Soft, flute-like
Waveform::WhiteNoise // Full spectrum
Waveform::PinkNoise  // Natural, warm
```

## Envelopes

```rust
// Structure
Envelope {
    attack: f32,   // seconds to reach peak
    decay: f32,    // seconds to reach sustain
    sustain: f32,  // hold level (0.0-1.0)
    release: f32,  // seconds to silence
}

// Presets
Envelope::pluck()     // Quick attack, fast decay
Envelope::pad()       // Slow attack, long sustain
Envelope::hit()       // Instant attack, no sustain
Envelope::zap()       // Fast in/out
Envelope::explosion() // Medium attack, long decay
Envelope::click()     // Instant, no tail
```

## Preset Sounds

```rust
synth.coin()       // Pickup collection
synth.jump()       // Jump action
synth.laser()      // Shoot/zap
synth.explosion()  // Big boom
synth.hit()        // Impact/damage
synth.click()      // UI interaction
synth.powerup()    // Power-up collect
synth.death()      // Game over
```

## Filters

```rust
// Low-pass (remove highs)
low_pass(&mut samples, cutoff_hz, sample_rate);

// High-pass (remove lows)
high_pass(&mut samples, cutoff_hz, sample_rate);

// Biquad with resonance
biquad_lowpass(&mut samples, cutoff_hz, resonance, sample_rate);
// resonance: 0.7 = flat, 1.0+ = resonant peak
```

## Export

```rust
// Convert to 16-bit PCM
let pcm = to_pcm_i16(&samples);

// Write WAV file
write_wav(&pcm, SAMPLE_RATE, "path/to/output.wav")?;
```

## Frequency Reference

| Note | Frequency |
|------|-----------|
| C4 | 261.63 Hz |
| E4 | 329.63 Hz |
| G4 | 392.00 Hz |
| C5 | 523.25 Hz |
| C6 | 1046.50 Hz |

## Typical Patterns

```rust
// Coin (two ascending notes)
let note1 = synth.tone(Waveform::Square, 988.0, 0.1, Envelope::pluck());
let note2 = synth.tone(Waveform::Square, 1319.0, 0.15, Envelope::pluck());
// Concatenate note1 + note2

// Laser (downward sweep)
synth.sweep(Waveform::Saw, 2000.0, 200.0, 0.15, Envelope::zap());

// Explosion (noise + low sine)
let boom = synth.noise_burst(0.8, Envelope::explosion());
let rumble = synth.tone(Waveform::Sine, 60.0, 1.0, Envelope::explosion());
synth.mix(&[(&boom, 0.8), (&rumble, 0.5)]);
```

## Source Location

`nethercore/tools/proc-gen/src/audio/`
