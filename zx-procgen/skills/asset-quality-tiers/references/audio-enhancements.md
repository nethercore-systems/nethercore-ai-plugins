# Audio Enhancement Techniques

Detailed techniques for upgrading audio/SFX quality through the tier system.

## Placeholder → Temp Upgrades

### Add Envelope Shaping

Transform raw tones into shaped sounds:

```rust
// Basic ADSR envelope
synth.set_envelope(Envelope {
    attack: 0.01,   // 10ms attack
    decay: 0.1,    // 100ms decay
    sustain: 0.6,  // 60% sustain level
    release: 0.2,  // 200ms release
});

// Apply to tone
synth.tone(Waveform::Saw, 220.0, 0.5, envelope);
```

### Basic Layering

Add depth with simple layering:

```rust
// Layer 1: Body (main frequency)
let body = synth.tone(Waveform::Saw, freq, 0.5, envelope);

// Layer 2: Sub (octave down)
let sub = synth.tone(Waveform::Sine, freq / 2.0, 0.3, envelope);

// Mix
audio.mix(&[
    (&body, 0.7),
    (&sub, 0.3),
]);
```

### Basic Filtering

Shape frequency content:

```rust
// Low-pass to remove harshness
audio.filter(Filter::LowPass {
    cutoff: 4000.0,
    resonance: 0.3,
});

// High-pass to remove rumble
audio.filter(Filter::HighPass {
    cutoff: 80.0,
    resonance: 0.1,
});
```

---

## Temp → Final Upgrades

### Multi-Layer Synthesis

Build rich sounds from multiple components:

```rust
// Impact sound layers
struct ImpactLayers {
    // Transient click (attack)
    click: AudioBuffer,
    // Body thud (main energy)
    body: AudioBuffer,
    // Rumble (low-end weight)
    rumble: AudioBuffer,
    // Tail (decay/reverb)
    tail: AudioBuffer,
}

fn generate_impact(impact_type: ImpactType) -> AudioBuffer {
    let layers = ImpactLayers {
        click: generate_click(0.005, 2000.0),
        body: generate_body(impact_type, 0.1),
        rumble: generate_rumble(0.3, 40.0),
        tail: generate_tail(0.5),
    };

    // Time-aligned mixing
    audio.mix_timed(&[
        (&layers.click, 0.0, 0.5),    // Immediate
        (&layers.body, 0.002, 0.8),   // Slight delay
        (&layers.rumble, 0.01, 0.4),  // After attack
        (&layers.tail, 0.05, 0.3),    // Decay phase
    ])
}
```

### Envelope Modulation

Add movement through modulation:

```rust
// Filter envelope (separate from amplitude)
synth.set_filter_envelope(FilterEnvelope {
    attack: 0.001,
    decay: 0.2,
    sustain: 0.3,
    release: 0.1,
    amount: 4000.0,  // Filter cutoff sweep
    start_freq: 200.0,
});

// Pitch envelope (impact "punch")
synth.set_pitch_envelope(PitchEnvelope {
    attack: 0.0,
    decay: 0.05,
    amount: 2.0,  // Octave drop
});
```

### Harmonic Content

Add harmonics for richness:

```rust
// Additive harmonics
fn rich_tone(fundamental: f32, duration: f32) -> AudioBuffer {
    let harmonics = [
        (1.0, 1.0),     // Fundamental
        (2.0, 0.5),     // 2nd harmonic
        (3.0, 0.3),     // 3rd harmonic
        (4.0, 0.15),    // 4th harmonic
        (5.0, 0.1),     // 5th harmonic
    ];

    let mut audio = AudioBuffer::silence(duration);
    for (ratio, amp) in harmonics {
        audio.add(&synth.tone(
            Waveform::Sine,
            fundamental * ratio,
            duration,
            envelope,
        ), amp);
    }
    audio
}
```

### Effects Processing

Add character through effects:

```rust
// Subtle distortion for warmth
audio.effect(Effect::Saturation {
    drive: 0.2,
    tone: 0.5,
});

// Short reverb for space
audio.effect(Effect::Reverb {
    room_size: 0.2,
    damping: 0.5,
    wet: 0.15,
});

// Compression for punch
audio.effect(Effect::Compressor {
    threshold: -12.0,
    ratio: 4.0,
    attack: 0.001,
    release: 0.1,
});
```

---

## Final → Hero Upgrades

### Subtle Variation

No two plays should sound identical:

```rust
// Pitch variation
fn play_with_variation(audio: &AudioBuffer, rng: &mut Rng) -> AudioBuffer {
    let pitch_shift = 1.0 + (rng.next_f32() - 0.5) * 0.04;  // ±2%
    let volume_shift = 1.0 + (rng.next_f32() - 0.5) * 0.1;  // ±5%
    let time_shift = rng.next_f32() * 0.01;  // 0-10ms

    audio
        .pitch_shift(pitch_shift)
        .amplify(volume_shift)
        .delay(time_shift)
}

// Multiple variations stored
fn generate_with_variations(base: &AudioBuffer, count: usize) -> Vec<AudioBuffer> {
    let mut rng = Rng::new(seed);
    (0..count)
        .map(|_| play_with_variation(base, &mut rng))
        .collect()
}
```

### Harmonic Richness

Full harmonic spectrum:

```rust
// Rich synthesis with detuned oscillators
fn rich_synth(freq: f32, duration: f32) -> AudioBuffer {
    let voices = [
        (freq * 0.995, 0.3),   // Slightly flat
        (freq * 1.0, 0.7),     // Center
        (freq * 1.005, 0.3),   // Slightly sharp
        (freq * 0.5, 0.2),     // Sub octave
        (freq * 2.0, 0.15),    // Upper octave
    ];

    let mut audio = AudioBuffer::silence(duration);
    for (voice_freq, amp) in voices {
        audio.add(&synth.tone(
            Waveform::Saw,
            voice_freq,
            duration,
            envelope,
        ), amp);
    }

    // Gentle chorus for width
    audio.effect(Effect::Chorus {
        rate: 0.5,
        depth: 0.002,
        mix: 0.3,
    });

    audio
}
```

### Spatial Cues

Add dimensional depth:

```rust
// Stereo width (mix to mono for ZX but process in stereo first)
audio.effect(Effect::StereoWidth {
    width: 1.2,
    center_focus: 0.8,
});

// Early reflections for size
audio.effect(Effect::EarlyReflections {
    room_type: RoomType::Small,
    distance: 2.0,
    wet: 0.1,
});

// Convert to mono with preserved depth
audio.stereo_to_mono(MonoMode::MidSide { side_amount: 0.2 });
```

### Dynamic Layering

Layers that respond to context:

```rust
// Velocity-responsive layers
fn impact_with_velocity(velocity: f32) -> AudioBuffer {
    let mut audio = AudioBuffer::silence(0.5);

    // Always present
    audio.add(&base_impact, 0.5);

    // Medium velocity adds body
    if velocity > 0.4 {
        audio.add(&body_layer, velocity * 0.3);
    }

    // High velocity adds crack
    if velocity > 0.7 {
        audio.add(&crack_layer, (velocity - 0.7) * 1.5);
    }

    // Maximum velocity adds distortion
    if velocity > 0.9 {
        audio.effect(Effect::Saturation {
            drive: (velocity - 0.9) * 2.0,
            tone: 0.3,
        });
    }

    audio
}
```

### Micro-Timing

Precise timing for impact:

```rust
// Layer timing for punch
struct LayerTiming {
    // Transient must be first
    transient_offset: 0.0,
    // Body slightly delayed for "thump"
    body_offset: 0.003,
    // Sub builds slower
    sub_offset: 0.01,
    // Room response
    room_offset: 0.015,
}

fn apply_timing(layers: &Layers, timing: &LayerTiming) -> AudioBuffer {
    let mut audio = AudioBuffer::silence(total_duration);

    audio.insert(&layers.transient, timing.transient_offset);
    audio.insert(&layers.body, timing.body_offset);
    audio.insert(&layers.sub, timing.sub_offset);
    audio.insert(&layers.room, timing.room_offset);

    audio
}
```

---

## SFX Category Enhancements

### Impact Sounds

| Tier | Characteristics |
|------|-----------------|
| Placeholder | Single tone with basic envelope |
| Temp | Body + transient, basic filtering |
| Final | Multi-layer, filtered, compressed |
| Hero | Variable layers, spatial, variations |

### UI Sounds

| Tier | Characteristics |
|------|-----------------|
| Placeholder | Simple beep |
| Temp | Shaped tone with filter sweep |
| Final | Layered, harmonic, pleasant |
| Hero | Subtle variation, perfect timing |

### Ambient Sounds

| Tier | Characteristics |
|------|-----------------|
| Placeholder | Looped noise |
| Temp | Filtered noise with movement |
| Final | Multi-layer, evolving |
| Hero | Rich texture, seamless loop |

### Weapon Sounds

| Tier | Characteristics |
|------|-----------------|
| Placeholder | Noise burst |
| Temp | Attack + decay, basic layers |
| Final | Mechanical + explosion layers |
| Hero | Full chain, variations, tail |

---

## Mixing Guidelines by Tier

### Placeholder

```rust
// Simple normalization
audio.normalize(-6.0);  // Leave headroom
```

### Temp

```rust
// Basic leveling
audio.normalize(-6.0);
audio.filter(Filter::HighPass { cutoff: 60.0, resonance: 0.1 });
audio.filter(Filter::LowPass { cutoff: 12000.0, resonance: 0.1 });
```

### Final

```rust
// Proper mix prep
audio.effect(Effect::Compressor {
    threshold: -12.0,
    ratio: 3.0,
    attack: 0.01,
    release: 0.1,
});
audio.normalize(-6.0);

// EQ for clarity
audio.effect(Effect::EQ {
    low_cut: 60.0,
    low_shelf: (200.0, -2.0),
    mid: (1000.0, 1.0, 1.0),
    high_shelf: (6000.0, 2.0),
    high_cut: 15000.0,
});
```

### Hero

```rust
// Full mastering chain
audio.effect(Effect::EQ { /* detailed EQ */ });
audio.effect(Effect::Multiband {
    bands: 3,
    crossovers: [200.0, 2000.0],
    ratios: [3.0, 2.0, 2.5],
    thresholds: [-18.0, -15.0, -12.0],
});
audio.effect(Effect::Saturation { drive: 0.1, tone: 0.6 });
audio.effect(Effect::Limiter { ceiling: -1.0 });
audio.normalize(-3.0);

// Final check
assert!(audio.peak() < 0.95, "Clipping detected");
assert!(audio.rms() > -20.0, "Too quiet");
```

---

## ZX-Specific Considerations

### Sample Rate

All tiers must output 22050 Hz:

```rust
// Ensure correct sample rate
if audio.sample_rate() != 22050 {
    audio.resample(22050, ResampleQuality::High);
}
```

### Mono Output

ZX requires mono:

```rust
// Convert stereo processing to mono
audio.to_mono(MonoMode::Mix);
```

### Duration Budgets

| SFX Type | Placeholder | Temp | Final | Hero |
|----------|-------------|------|-------|------|
| UI click | 0.05s | 0.1s | 0.15s | 0.2s |
| Impact | 0.1s | 0.2s | 0.3s | 0.5s |
| Weapon | 0.2s | 0.3s | 0.5s | 0.8s |
| Ambient loop | 1.0s | 2.0s | 4.0s | 8.0s |
