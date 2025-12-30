---
name: Procedural Instrument Synthesis
description: |
  Use this skill to GENERATE instrument samples for ZX game music.

  **Triggers:** "generate instrument", "synthesize piano", "make guitar sound", "instrument sample", "FM synthesis", "Karplus-Strong", "physical modeling", "wavetable"

  **Before generating:** Check `.studio/sonic-identity.local.md` for audio specs.

  **Load references when:**
  - Plucked strings (guitar, bass) → `references/karplus-strong.md`
  - Electric piano, bells → `references/fm-synthesis.md`
  - Pads, evolving sounds → `references/wavetable-synthesis.md`
  - Organs → `references/additive-synthesis.md`
  - Synth leads/bass → `references/subtractive-synthesis.md`

  Production-quality synthesis (not chiptuney) using FM, physical modeling, and wavetable.
version: 2.0.0
---

# Procedural Instrument Synthesis

Generate production-quality instrument samples that sound realistic and musical—not chiptuney.

## Why Basic Synthesis Sounds Chiptuney

| Chiptuney Approach | Why It Sounds Bad |
|-------------------|-------------------|
| `np.sin(2*pi*f*t)` directly | Static timbre, no evolution |
| Simple ADSR on raw oscillator | Real instruments have complex envelopes |
| Instant attack | Real instruments have attack transients |
| Uniform decay | Real instruments have frequency-dependent decay |
| Single oscillator | Real instruments have multiple components |

**Key insight:** Real instruments are physical systems with complex, evolving behavior.

## Quick Reference: Which Technique for Which Instrument

| Instrument | Technique | Reference |
|------------|-----------|-----------|
| Acoustic Guitar | Karplus-Strong | `references/karplus-strong.md` |
| Electric Guitar | Karplus-Strong + distortion | `references/karplus-strong.md` |
| Bass Guitar | Karplus-Strong (longer delay) | `references/karplus-strong.md` |
| Electric Piano | FM Synthesis | `references/fm-synthesis.md` |
| Bells | FM (inharmonic ratios) | `references/fm-synthesis.md` |
| Organ | Additive | `references/additive-synthesis.md` |
| Strings/Pads | Wavetable | `references/wavetable-synthesis.md` |
| Synth Lead | Subtractive/FM | `references/subtractive-synthesis.md` |
| Synth Bass | Subtractive | `references/subtractive-synthesis.md` |
| Brass | Subtractive + noise | `references/subtractive-synthesis.md` |

## Core Building Blocks

### Multi-stage Envelopes

Real instruments don't follow simple ADSR:

```python
def multi_envelope(t, segments):
    """segments: [(duration, target_level, curve_type), ...]"""
    env = np.zeros_like(t)
    current_time, current_level = 0.0, 0.0

    for duration, target, curve in segments:
        mask = (t >= current_time) & (t < current_time + duration)
        local_t = (t[mask] - current_time) / duration

        if curve == 'exp':
            env[mask] = current_level + (target - current_level) * (1 - np.exp(-5 * local_t))
        # ... other curves

        current_time += duration
        current_level = target

    return env
```

### Attack Transients

Add noise at note start for realism:

```python
def attack_transient(t, attack_duration=0.02, noise_amount=0.3):
    noise = np.random.randn(len(t)) * noise_amount
    attack_env = np.exp(-t / attack_duration * 10)
    return noise * attack_env
```

### Vibrato

Natural pitch variation:

```python
def apply_vibrato(phase, t, rate=5.0, depth=0.02, delay=0.2):
    vibrato_env = np.clip((t - delay) / 0.1, 0, 1)  # Fade in after delay
    vibrato = np.sin(2 * np.pi * rate * t) * depth * vibrato_env
    return phase * (1 + vibrato)
```

## Quality Checklist

| Check | How to Test | Fix |
|-------|-------------|-----|
| No clicks | Listen to start/end | Add attack/release ramp |
| Pitch correct | Tune against reference | Check frequency calc |
| Timbre evolves | Changes over duration | Add envelope to filter/index |
| Attack has character | First 50ms distinct | Add transient noise |
| Sounds musical | Play in context | Adjust envelopes |

## XM Tracker Integration

1. Generate instrument samples
2. Save as WAV to `assets/audio/`
3. Reference in `nether.toml`:
   ```toml
   [[assets.sounds]]
   id = "epiano"
   path = "assets/audio/epiano_c4.wav"
   ```
4. In XM tracker, name instrument "epiano" to match

## References

- `references/karplus-strong.md` - Plucked strings (guitar, bass, harp)
- `references/fm-synthesis.md` - Electric piano, bells, brass
- `references/wavetable-synthesis.md` - Pads, evolving sounds
- `references/additive-synthesis.md` - Organs, drawbar settings
- `references/subtractive-synthesis.md` - Synth leads, bass, brass

## Example Files

- `examples/acoustic-guitar.py` - Karplus-Strong + body resonance
- `examples/electric-piano.py` - FM synthesis
- `examples/synth-bass.py` - Subtractive with filter envelope
- `examples/strings-pad.py` - Wavetable + unison detuning
- `examples/organ.py` - Additive with drawbars

## Related Skills

- `procedural-sounds` - SFX synthesis
- `sound-design/sonic-style-language` - Audio style specs
