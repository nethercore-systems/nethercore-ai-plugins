---
name: Procedural Instrument Synthesis
description: |
  Use this skill to GENERATE instrument samples for ZX game music.

  **Triggers:** "generate instrument", "synthesize piano", "make guitar sound", "instrument sample", "FM synthesis", "Karplus-Strong", "physical modeling", "wavetable"

  **Before generating:** Check `.studio/sonic-identity.local.md` for audio specs.

  **Modular lib/ architecture:** lib/ contains PRIMITIVES only, not pre-made instruments.
  You must COMPOSE your own instruments using these building blocks.

  **Load references when:**
  - Plucked strings (guitar, bass) → `references/karplus-strong.md`
  - Electric piano, bells → `references/fm-synthesis.md`
  - Pads, evolving sounds → `references/wavetable-synthesis.md`
  - Organs → `references/additive-synthesis.md`
  - Synth leads/bass → `references/subtractive-synthesis.md`
  - Example drum implementations → `references/drum-examples.py`

  Production-quality synthesis (not chiptuney) using FM, physical modeling, and wavetable.
version: 4.0.0
---

# Procedural Instrument Synthesis

Generate production-quality instrument samples that sound realistic and musical—not chiptuney.

## CRITICAL: lib/ Contains PRIMITIVES Only

The lib/ directory contains **synthesis primitives**, NOT pre-made instruments.
You must COMPOSE your own instruments using these building blocks.

**DO NOT** expect to find `kick_808()` or `generate_guitar()` in lib/.
Instead, use primitives like `pitched_body()`, `noise_burst()`, `fm_operator()`, `karplus_strong()`.

For example implementations, see `references/drum-examples.py`.

## Project Folder Structure

```
project/
├── generators/                    # Source code (committed to git)
│   ├── lib/                       # Synthesis PRIMITIVES (scaffold once)
│   │   ├── __init__.py
│   │   ├── synthesis.py           # ADSR, FM operators, Karplus-Strong
│   │   ├── waveforms.py           # Oscillators, noise, PCM conversion
│   │   ├── drums.py               # Drum synthesis PRIMITIVES
│   │   ├── effects.py             # Filters, distortion, reverb
│   │   ├── xm_writer.py           # From tracker-music/skills/xm-format/scripts/
│   │   └── it_writer.py           # From tracker-music/skills/it-format/scripts/
│   ├── instruments/               # YOUR instrument definitions
│   │   ├── rhodes.py              # Your FM Rhodes implementation
│   │   └── guitar.py              # Your Karplus-Strong guitar
│   └── tracks/                    # Song generator scripts
│       └── boss_theme.py
│
└── generated/                     # Output (gitignored)
    ├── tracks/
    │   └── boss_theme.it
    └── samples/
        └── rhodes_c4.wav
```

### lib/ Source Locations

When scaffolding lib/, copy from these canonical sources:

| File | Source Location |
|------|-----------------|
| synthesis.py | `zx-procgen/skills/procedural-instruments/lib/synthesis.py` |
| waveforms.py | `zx-procgen/skills/procedural-instruments/lib/waveforms.py` |
| drums.py | `zx-procgen/skills/procedural-instruments/lib/drums.py` |
| effects.py | `zx-procgen/skills/procedural-instruments/lib/effects.py` |
| xm_writer.py | `tracker-music/skills/xm-format/scripts/xm_writer.py` |
| it_writer.py | `tracker-music/skills/it-format/scripts/it_writer.py` |

### Usage Pattern

```python
#!/usr/bin/env python3
"""Custom Instrument Generator - use PRIMITIVES to compose instruments"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

# Import PRIMITIVES - these are building blocks, not complete instruments!
from synthesis import fm_operator, adsr_envelope, karplus_strong, multi_envelope
from waveforms import sine_wave, normalize, to_16bit_pcm
from drums import noise_burst, pitched_body, percussive_envelope
from effects import lowpass_filter, apply_distortion

# Now COMPOSE your own instrument using these primitives
def generate_my_kick():
    """Example: Compose a kick drum from primitives."""
    import numpy as np
    duration = 0.3
    t = np.linspace(0, duration, int(22050 * duration))

    # Body: pitched sine with rapid pitch drop
    body = pitched_body(duration, start_freq=100, end_freq=40)

    # Transient: noise burst
    click = noise_burst(0.01)
    click = np.pad(click, (0, len(body) - len(click)))
    click *= np.exp(-np.linspace(0, 1, len(click)) * 50)

    # Envelope
    env = percussive_envelope(t, attack=0.001, decay=0.12)

    return normalize((body * 0.8 + click * 0.3) * env)
```

### lib/ Contents (PRIMITIVES)

| Module | Primitives | Use For |
|--------|-----------|---------|
| `synthesis` | `adsr_envelope`, `multi_envelope`, `fm_operator`, `karplus_strong`, `attack_transient`, `apply_vibrato` | Core synthesis building blocks |
| `waveforms` | `sine_wave`, `square_wave`, `saw_wave`, `triangle_wave`, `white_noise`, `pink_noise`, `normalize`, `to_8bit_pcm`, `to_16bit_pcm` | Oscillators & conversion |
| `drums` | `noise_burst`, `pitched_body`, `metallic_partials`, `percussive_envelope`, `two_stage_decay`, `drum_lowpass`, `drum_bandpass`, `layer_sounds` | Drum synthesis primitives |
| `effects` | `lowpass_filter`, `highpass_filter`, `bandpass_filter`, `filter_sweep`, `apply_distortion`, `simple_reverb`, `normalize` | Audio processing |

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
| Drums | See `references/drum-examples.py` | `references/drum-examples.py` |

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

## Tracker Integration

Instruments integrate with XM/IT trackers:

```python
from xm_writer import XmModule, XmInstrument, write_xm
from waveforms import to_16bit_pcm

# Generate your instrument
my_piano = generate_my_piano()
piano_bytes = to_16bit_pcm(my_piano)

# Embed in tracker module
module = XmModule(
    name="Song",
    instruments=[XmInstrument.for_zx("piano", piano_bytes)],
    # ...
)
write_xm(module, "generated/tracks/song.xm")
```

Then reference in `nether.toml`:
```toml
[[assets.trackers]]
id = "song"
path = "generated/tracks/song.xm"
# Samples auto-extracted! "piano" becomes rom_sound("piano")
```

## References

- `references/karplus-strong.md` - Plucked strings (guitar, bass, harp)
- `references/fm-synthesis.md` - Electric piano, bells, brass
- `references/wavetable-synthesis.md` - Pads, evolving sounds
- `references/additive-synthesis.md` - Organs, drawbar settings
- `references/subtractive-synthesis.md` - Synth leads, bass, brass
- `references/drum-examples.py` - Example drum implementations (study, don't import!)

## Example Files

- `examples/acoustic-guitar.py` - Karplus-Strong + body resonance
- `examples/electric-piano.py` - FM synthesis
- `examples/synth-bass.py` - Subtractive with filter envelope
- `examples/strings-pad.py` - Wavetable + unison detuning
- `examples/organ.py` - Additive with drawbars

## Related Skills

- `procedural-sounds` - SFX synthesis
- `sound-design/sonic-style-language` - Audio style specs
- `tracker-music/xm-format` - XM writer (canonical source)
- `tracker-music/it-format` - IT writer (canonical source)
