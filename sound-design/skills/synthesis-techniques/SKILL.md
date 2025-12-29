---
name: Synthesis Techniques (Theory)
description: |
  Use this skill when the user asks about synthesis THEORY or wants to UNDERSTAND how synthesis works. Trigger phrases: "how does FM synthesis work", "explain wavetable", "what is granular synthesis", "which synthesis for X sound", "synthesis comparison", "oscillator types", "filter theory", "modulation explained".

  This skill provides CONCEPTUAL UNDERSTANDING of synthesis methods - when to use each, how they work, signal flow diagrams.

  For IMPLEMENTATION CODE (numpy/scipy): use zx-procgen:procedural-sounds instead.
  For INSTRUMENT SAMPLES (realistic instrument synthesis): use zx-procgen:procedural-instruments instead.
version: 1.0.1
---

# Synthesis Techniques

Understanding synthesis techniques enables creating any sound from scratch. Each technique has strengths for different sound types.

## Technique Overview

| Technique | Best For | Complexity | CPU Cost |
|-----------|----------|------------|----------|
| Subtractive | Warm analog sounds | Low | Low |
| FM | Bells, metallic, digital | Medium | Low |
| Wavetable | Evolving textures | Medium | Low |
| Additive | Precise harmonics | High | High |
| Granular | Textures, pads, time-stretch | High | Medium |
| Physical Modeling | Realistic instruments | High | Medium |
| Karplus-Strong | Plucked strings | Low | Low |
| Sample-based | Realistic, complex | Low | Memory |

---

## Subtractive Synthesis

The classic approach: start with harmonically rich waveform, filter away unwanted frequencies.

### Signal Flow

```
Oscillator → Filter → Amplifier → Output
    ↑           ↑          ↑
   LFO        Env 1      Env 2
```

### Core Components

**Oscillators:**
| Waveform | Harmonics | Character |
|----------|-----------|-----------|
| Saw | All harmonics (1/n amplitude) | Bright, buzzy |
| Square | Odd harmonics only | Hollow, woody |
| Triangle | Odd harmonics (1/n² amplitude) | Soft, flute-like |
| Pulse | Variable based on width | Dynamic timbre |

**Filters:**
| Type | Effect | Use For |
|------|--------|---------|
| Low-pass | Remove highs | Warmth, bass |
| High-pass | Remove lows | Thin, airy |
| Band-pass | Isolate band | Vocal, nasal |
| Notch | Remove band | Remove resonance |

**Filter Parameters:**
- **Cutoff:** Where filtering begins (Hz)
- **Resonance:** Boost at cutoff (creates peak)
- **Envelope amount:** How much envelope affects cutoff
- **Key tracking:** Cutoff follows pitch

### Implementation Pattern

```rust
fn subtractive_synth(freq: f32, duration: f32, params: &SubtractiveParams) -> Vec<f32> {
    let sample_rate = 22050;
    let num_samples = (duration * sample_rate as f32) as usize;
    let mut output = Vec::with_capacity(num_samples);

    for i in 0..num_samples {
        let t = i as f32 / sample_rate as f32;

        // Oscillator
        let osc = match params.waveform {
            Saw => 2.0 * (freq * t % 1.0) - 1.0,
            Square => if (freq * t % 1.0) < 0.5 { 1.0 } else { -1.0 },
            // ...
        };

        // Envelope
        let env = adsr_envelope(t, duration, &params.amp_env);
        let filter_env = adsr_envelope(t, duration, &params.filter_env);

        // Filter (simplified)
        let cutoff = params.base_cutoff + filter_env * params.env_amount;
        let filtered = low_pass_filter(osc, cutoff, params.resonance);

        output.push(filtered * env);
    }

    output
}
```

### Best For
- Bass sounds (filtered saw)
- Pads (slow filter sweeps)
- Leads (resonant filter)
- Classic analog sounds

---

## FM Synthesis

Frequency Modulation: one oscillator modulates another's frequency, creating complex harmonics.

### Core Concepts

**Operators:** Each oscillator is an "operator"
- **Carrier:** The oscillator you hear
- **Modulator:** The oscillator that modulates the carrier

**Ratio:** Modulator frequency / Carrier frequency
- Integer ratios = harmonic sounds
- Non-integer = inharmonic/bell-like

**Index:** Modulation depth
- Low = subtle, warm
- High = bright, metallic

### Algorithm Patterns

```
Simple 2-op:
[Mod] → [Carrier] → Output

4-op Stack:
[Op4] → [Op3] → [Op2] → [Op1] → Output

4-op Parallel:
[Op3] → [Op1] ─┬→ Output
[Op4] → [Op2] ─┘
```

### FM Formula

```
output = sin(carrier_freq * t + index * sin(mod_freq * t))
```

### Implementation Pattern

```rust
fn fm_synth(carrier_freq: f32, duration: f32, params: &FMParams) -> Vec<f32> {
    let sample_rate = 22050;
    let num_samples = (duration * sample_rate as f32) as usize;
    let mut output = Vec::with_capacity(num_samples);

    let mod_freq = carrier_freq * params.ratio;

    for i in 0..num_samples {
        let t = i as f32 / sample_rate as f32;

        // Modulation index envelope
        let index = params.index * adsr_envelope(t, duration, &params.index_env);

        // Modulator
        let modulator = (2.0 * PI * mod_freq * t).sin();

        // Carrier (modulated)
        let carrier = (2.0 * PI * carrier_freq * t + index * modulator).sin();

        // Amplitude envelope
        let amp = adsr_envelope(t, duration, &params.amp_env);

        output.push(carrier * amp);
    }

    output
}
```

### Classic FM Sounds

| Sound | Ratio | Index | Envelope |
|-------|-------|-------|----------|
| Bell | 1:1.4 | 3-8 | Slow decay |
| Electric Piano | 1:1 | 2-4 | Fast decay |
| Bass | 1:1 | 1-3 | Pluck envelope |
| Brass | 1:1 | 4-8 | Slow attack |
| Metallic | 1:1.41 | 5+ | Any |

### Best For
- Bells and chimes
- Electric piano
- Metallic textures
- Digital/80s sounds
- Complex timbres from simple components

---

## Wavetable Synthesis

Cycle through different waveforms stored in a table for evolving timbres.

### Core Concepts

**Wavetable:** Array of single-cycle waveforms
**Position:** Which waveform(s) to read
**Interpolation:** Blend between adjacent waveforms

### Implementation Pattern

```rust
struct Wavetable {
    frames: Vec<Vec<f32>>,  // Each frame is one cycle
    frame_size: usize,
}

fn wavetable_synth(freq: f32, duration: f32, table: &Wavetable,
                   position_env: &Envelope) -> Vec<f32> {
    let sample_rate = 22050;
    let num_samples = (duration * sample_rate as f32) as usize;
    let mut output = Vec::with_capacity(num_samples);
    let mut phase = 0.0;

    for i in 0..num_samples {
        let t = i as f32 / sample_rate as f32;

        // Get wavetable position (0.0 to 1.0)
        let pos = envelope_value(t, duration, position_env);
        let frame_f = pos * (table.frames.len() - 1) as f32;
        let frame_a = frame_f.floor() as usize;
        let frame_b = (frame_a + 1).min(table.frames.len() - 1);
        let blend = frame_f.fract();

        // Read from both frames
        let idx = (phase * table.frame_size as f32) as usize % table.frame_size;
        let sample_a = table.frames[frame_a][idx];
        let sample_b = table.frames[frame_b][idx];

        // Interpolate
        let sample = sample_a * (1.0 - blend) + sample_b * blend;

        // Advance phase
        phase += freq / sample_rate as f32;
        if phase >= 1.0 { phase -= 1.0; }

        output.push(sample);
    }

    output
}
```

### Creating Wavetables

```rust
fn create_basic_wavetable() -> Wavetable {
    let frame_size = 2048;
    let mut frames = Vec::new();

    // Frame 0: Sine
    frames.push(generate_sine(frame_size));

    // Frame 1: Triangle
    frames.push(generate_triangle(frame_size));

    // Frame 2: Square
    frames.push(generate_square(frame_size));

    // Frame 3: Saw
    frames.push(generate_saw(frame_size));

    Wavetable { frames, frame_size }
}
```

### Best For
- Evolving pads
- Complex textures
- Modern synth sounds
- Morphing timbres

---

## Granular Synthesis

Break audio into tiny grains, reassemble with control over pitch, time, and density.

### Core Concepts

**Grain:** Tiny audio snippet (10-100ms typically)
**Density:** Grains per second
**Spray:** Random position variation
**Pitch:** Independent of playback speed

### Implementation Pattern

```rust
struct GranularParams {
    grain_size: f32,      // seconds
    density: f32,         // grains per second
    spray: f32,           // position randomness
    pitch_shift: f32,     // semitones
    position: f32,        // 0.0 to 1.0 through source
}

fn granular_synth(source: &[f32], duration: f32, params: &GranularParams) -> Vec<f32> {
    let sample_rate = 22050;
    let output_samples = (duration * sample_rate as f32) as usize;
    let mut output = vec![0.0; output_samples];

    let grain_samples = (params.grain_size * sample_rate as f32) as usize;
    let grains_total = (duration * params.density) as usize;

    let mut rng = StdRng::seed_from_u64(42);

    for g in 0..grains_total {
        // When does this grain start in output?
        let output_pos = (g as f32 / params.density * sample_rate as f32) as usize;

        // Where in source to read from?
        let base_pos = params.position * source.len() as f32;
        let spray_offset = (rng.gen::<f32>() - 0.5) * params.spray * source.len() as f32;
        let source_pos = (base_pos + spray_offset) as usize % source.len();

        // Pitch shift ratio
        let pitch_ratio = 2.0_f32.powf(params.pitch_shift / 12.0);

        // Write grain with window
        for i in 0..grain_samples {
            let window = hann_window(i, grain_samples);
            let source_idx = source_pos + (i as f32 * pitch_ratio) as usize;

            if source_idx < source.len() && output_pos + i < output_samples {
                output[output_pos + i] += source[source_idx] * window;
            }
        }
    }

    output
}
```

### Best For
- Time stretching without pitch change
- Pitch shifting without time change
- Atmospheric textures
- Glitchy/experimental sounds
- Transforming recordings

---

## Physical Modeling

Simulate the physics of real instruments mathematically.

### Karplus-Strong (Plucked Strings)

Simple algorithm for realistic plucked string sounds:

```rust
fn karplus_strong(freq: f32, duration: f32, damping: f32) -> Vec<f32> {
    let sample_rate = 22050;
    let num_samples = (duration * sample_rate as f32) as usize;

    // Delay line length determines pitch
    let delay_length = (sample_rate as f32 / freq) as usize;
    let mut delay_line = vec![0.0; delay_length];

    // Initialize with noise burst (pluck)
    let mut rng = StdRng::seed_from_u64(42);
    for i in 0..delay_length {
        delay_line[i] = rng.gen::<f32>() * 2.0 - 1.0;
    }

    let mut output = Vec::with_capacity(num_samples);
    let mut idx = 0;

    for _ in 0..num_samples {
        // Output current sample
        let out = delay_line[idx];
        output.push(out);

        // Average with next sample (low-pass = damping)
        let next_idx = (idx + 1) % delay_length;
        let averaged = (delay_line[idx] + delay_line[next_idx]) * 0.5 * damping;

        delay_line[idx] = averaged;
        idx = (idx + 1) % delay_length;
    }

    output
}
```

### Waveguide Synthesis

Model traveling waves in tubes/strings:

```
Excitation → [Delay] → [Reflection] → [Delay] → Output
                  ↑_____________________|
```

### Best For
- Plucked strings (guitar, harp)
- Struck instruments (piano, marimba)
- Wind instruments
- Realistic acoustic sounds

---

## Additive Synthesis

Build sounds by adding sine waves at harmonic frequencies.

### Core Concept

Any sound = sum of sinusoids at different frequencies and amplitudes.

```rust
fn additive_synth(freq: f32, duration: f32, harmonics: &[(f32, f32)]) -> Vec<f32> {
    // harmonics: [(relative_freq, amplitude), ...]
    let sample_rate = 22050;
    let num_samples = (duration * sample_rate as f32) as usize;
    let mut output = vec![0.0; num_samples];

    for (harmonic_ratio, amplitude) in harmonics {
        let harmonic_freq = freq * harmonic_ratio;

        for i in 0..num_samples {
            let t = i as f32 / sample_rate as f32;
            output[i] += (2.0 * PI * harmonic_freq * t).sin() * amplitude;
        }
    }

    // Normalize
    let max = output.iter().map(|x| x.abs()).fold(0.0_f32, f32::max);
    if max > 0.0 {
        for s in &mut output {
            *s /= max;
        }
    }

    output
}

// Example: Organ-like sound
let organ_harmonics = [
    (1.0, 1.0),    // Fundamental
    (2.0, 0.5),    // 2nd harmonic
    (3.0, 0.25),   // 3rd harmonic
    (4.0, 0.125),  // 4th harmonic
];
```

### Best For
- Precise timbre control
- Organ sounds
- Analysis/resynthesis
- Educational purposes

---

## Ring Modulation

Multiply two signals together for metallic, robotic sounds.

```rust
fn ring_modulate(signal: &[f32], mod_freq: f32, sample_rate: u32) -> Vec<f32> {
    signal.iter().enumerate().map(|(i, &s)| {
        let t = i as f32 / sample_rate as f32;
        let modulator = (2.0 * PI * mod_freq * t).sin();
        s * modulator
    }).collect()
}
```

### Best For
- Robot voices
- Metallic textures
- Dissonant effects
- Sci-fi sounds

---

## Technique Selection Guide

| Want to Create | Use Technique |
|----------------|---------------|
| Warm bass | Subtractive (saw + LP filter) |
| Electric piano | FM (1:1 ratio) |
| Bells | FM (non-integer ratio) |
| Plucked strings | Karplus-Strong |
| Evolving pad | Wavetable |
| Stretched audio | Granular |
| Organ | Additive |
| Robot voice | Ring modulation |
| Realistic flute | Physical modeling |
| Glitchy texture | Granular |
| 80s digital | FM |
| Analog synth | Subtractive |

---

## Additional Resources

- `references/fm-algorithms.md` - FM operator configurations
- `references/filter-types.md` - Filter implementations
- `references/envelope-shapes.md` - Envelope design patterns
