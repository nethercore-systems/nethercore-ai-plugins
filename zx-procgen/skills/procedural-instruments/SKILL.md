---
name: Procedural Instrument Synthesis
description: |
  Generate instrument samples for ZX game music.

  **Spec-Driven Workflow (RECOMMENDED):**
  1. Create `.spec.py` in `.studio/instruments/`
  2. Run `python sound_parser.py instrument spec.py output.wav`

  **Load references when:**
  - Instrument specs → `procedural-sounds/references/sound-spec-format.md`
  - Parser → `procedural-sounds/references/sound_parser.py`
  - Example specs → `examples/bass.spec.py`, `examples/lead.spec.py`
  - Karplus-Strong → `references/karplus-strong.md`
  - FM synthesis → `references/fm-synthesis.md`
  - Drum examples → `references/drum-examples.py`

  **Before generating:** Check `.studio/sonic-identity.md` for audio specs.
version: 5.1.0
---

# Procedural Instrument Synthesis

Generate production-quality instrument samples using a **spec-driven workflow**.

## Spec-Driven Workflow

**Step 1: Create Spec**
```python
# .studio/instruments/bass.spec.py
INSTRUMENT = {
    "instrument": {
        "name": "bass",
        "base_note": "C2",
        "synthesis": {
            "type": "karplus_strong",
            "damping": 0.994,
            "brightness": 0.5
        },
        "envelope": {"attack": 0.01, "decay": 0.4, "sustain": 0.3, "release": 0.3},
        "output": {"duration": 1.5, "bit_depth": 16, "loop": True}
    }
}
```

**Step 2: Run Parser**
```bash
python sound_parser.py instrument .studio/instruments/bass.spec.py generated/samples/bass.wav
```

See `procedural-sounds/references/sound-spec-format.md` for complete format.

## Technique Selection

| Instrument | Technique | Reference |
|------------|-----------|-----------|
| Acoustic Guitar | Karplus-Strong | `karplus-strong.md` |
| Electric Piano | FM Synthesis | `fm-synthesis.md` |
| Bells | FM (inharmonic) | `fm-synthesis.md` |
| Organ | Additive | `additive-synthesis.md` |
| Strings/Pads | Wavetable | `wavetable-synthesis.md` |
| Synth Lead/Bass | Subtractive | `subtractive-synthesis.md` |
| Drums | See examples | `drum-examples.py` |

## Why Basic Synthesis Sounds Chiptuney

| Problem | Why It Sounds Bad |
|---------|-------------------|
| Raw `np.sin()` | Static timbre, no evolution |
| Simple ADSR | Real instruments have complex envelopes |
| Instant attack | Real instruments have transients |
| Single oscillator | Real instruments have multiple components |

## lib/ Architecture (Manual Synthesis)

**lib/ contains PRIMITIVES only** - compose your own instruments:

| Module | Primitives |
|--------|-----------|
| `synthesis` | `adsr_envelope`, `fm_operator`, `karplus_strong` |
| `waveforms` | `sine_wave`, `saw_wave`, `noise`, `to_16bit_pcm` |
| `drums` | `noise_burst`, `pitched_body`, `percussive_envelope` |
| `effects` | `lowpass_filter`, `distortion`, `reverb` |

## Usage Pattern

```python
from synthesis import fm_operator, adsr_envelope
from waveforms import normalize, to_16bit_pcm
from effects import lowpass_filter

def generate_my_piano():
    # Compose using primitives
    carrier = fm_operator(...)
    env = adsr_envelope(...)
    return normalize(carrier * env)
```

## Quality Checklist

- No clicks (attack/release ramps)
- Pitch correct (verify frequency)
- Timbre evolves (envelope on filter/index)
- Attack has character (transient noise)
- Sounds musical (test in context)

## Tracker Integration

```python
from xm_writer import XmModule, XmInstrument
from waveforms import to_16bit_pcm

my_piano = generate_my_piano()
module = XmModule(
    instruments=[XmInstrument.for_zx("piano", to_16bit_pcm(my_piano))]
)
```

```toml
[[assets.trackers]]
id = "song"
path = "generated/tracks/song.xm"
# Samples auto-extracted: rom_sound("piano")
```

## Related Skills

- `procedural-sounds` - SFX synthesis
- `sound-design/sonic-style-language` - Audio style specs
- `tracker-music/xm-format` - XM writer
