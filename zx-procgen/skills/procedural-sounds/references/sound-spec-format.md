# Sound Spec Format

Declarative specification format for procedural audio generation. Specs are **data**, not code - the parser handles synthesis deterministically.

## Architecture

```
LLM creates spec (.spec.py)  →  sound_parser.py  →  audio file (WAV/XM/IT)
         ↓
  .studio/sounds/
  .studio/instruments/
  .studio/music/
```

## SFX Spec Format (SOUND)

```python
# .studio/sounds/laser.spec.py
SOUND = {
    "sound": {
        "name": "laser",
        "category": "projectile",  # projectile, impact, ui, ambient, action
        "duration": 0.3,
        "sample_rate": 22050,

        # Layers are mixed together
        "layers": [
            {
                "name": "transient",
                "type": "noise_burst",
                "duration": 0.02,
                "amplitude": 0.3,
                "filter": {"type": "highpass", "cutoff": 4000}
            },
            {
                "name": "body",
                "type": "fm_synth",
                "carrier_freq": 440,
                "mod_ratio": 1.4,
                "mod_index": 5.0,
                "index_decay": 8.0,
                "amplitude": 1.0
            }
        ],

        # Master envelope applied to mixed layers
        "envelope": {
            "attack": 0.005,
            "decay": 0.2,
            "sustain": 0,
            "release": 0.1
        },

        # Optional master filter
        "master_filter": {"type": "lowpass", "cutoff": 6000, "q": 1.5},

        "normalize": True,
        "peak_db": -3.0  # Target peak level
    }
}
```

### Layer Types

| Type | Parameters | Description |
|------|------------|-------------|
| `sine` | `freq`, `freq_end` (sweep) | Pure sine wave |
| `square` | `freq`, `duty` | Square/pulse wave |
| `saw` | `freq`, `antialiased` | Sawtooth wave |
| `triangle` | `freq` | Triangle wave |
| `noise_burst` | `color` (white/pink/brown) | Noise with envelope |
| `fm_synth` | `carrier_freq`, `mod_ratio`, `mod_index`, `index_decay` | FM synthesis |
| `karplus` | `freq`, `damping`, `brightness` | Plucked string |
| `pitched_body` | `start_freq`, `end_freq` | Pitch drop (kicks, toms) |
| `metallic` | `base_freq`, `num_partials`, `inharmonicity` | Cymbals, bells |
| `harmonics` | `freqs`, `amplitudes` | Additive synthesis |

### Layer Parameters (Common)

```python
{
    "name": "layer_name",       # For reference
    "type": "sine",             # Layer type (see table)
    "amplitude": 1.0,           # Mix level (0-1)
    "pan": 0.0,                 # Stereo pan (-1 to 1)
    "delay": 0.0,               # Delay start (seconds)
    "duration": None,           # Override sound duration

    # Per-layer envelope (optional, overrides master)
    "envelope": {
        "attack": 0.01,
        "decay": 0.1,
        "sustain": 0.5,
        "release": 0.1
    },

    # Per-layer filter (optional)
    "filter": {
        "type": "lowpass",      # lowpass, highpass, bandpass
        "cutoff": 2000,
        "cutoff_end": 200,      # For filter sweeps
        "q": 1.0
    }
}
```

### Filter Types

| Type | Parameters | Description |
|------|------------|-------------|
| `lowpass` | `cutoff`, `q` | Removes highs |
| `highpass` | `cutoff`, `q` | Removes lows |
| `bandpass` | `cutoff_low`, `cutoff_high`, `q` | Isolates band |

## Instrument Spec Format (INSTRUMENT)

```python
# .studio/instruments/bass.spec.py
INSTRUMENT = {
    "instrument": {
        "name": "bass",
        "category": "bass",  # bass, lead, pad, keys, drums, sfx
        "base_note": "C3",   # Note for sample (MIDI note name or number)
        "sample_rate": 22050,

        # Synthesis type (pick one)
        "synthesis": {
            "type": "karplus_strong",
            "damping": 0.996,
            "brightness": 0.6
        },

        # OR FM synthesis
        # "synthesis": {
        #     "type": "fm",
        #     "algorithm": "simple",  # simple, dx7_1, dx7_2, ...
        #     "operators": [
        #         {"ratio": 1.0, "level": 1.0, "feedback": 0},
        #         {"ratio": 2.0, "level": 0.5, "mod_target": 0}
        #     ]
        # },

        # OR subtractive synthesis
        # "synthesis": {
        #     "type": "subtractive",
        #     "oscillators": [
        #         {"waveform": "saw", "detune": 0},
        #         {"waveform": "square", "detune": 7}  # cents
        #     ],
        #     "filter": {"type": "lowpass", "cutoff": 2000, "resonance": 0.3}
        # },

        # Amplitude envelope
        "envelope": {
            "attack": 0.01,
            "decay": 0.3,
            "sustain": 0.4,
            "release": 0.2
        },

        # Optional pitch envelope
        "pitch_envelope": {
            "attack": 0.0,
            "amount": 12,      # Semitones
            "decay": 0.05
        },

        # Output settings
        "output": {
            "duration": 1.0,
            "bit_depth": 16,     # 8 or 16
            "loop": True,
            "loop_start": 0.1,   # Seconds from start
            "loop_end": 0.9      # Seconds from start
        }
    }
}
```

### Synthesis Types

| Type | Key Parameters | Best For |
|------|----------------|----------|
| `karplus_strong` | `damping`, `brightness` | Plucked strings, bass |
| `fm` | `algorithm`, `operators` | Electric pianos, bells, basses |
| `subtractive` | `oscillators`, `filter` | Synth leads, pads |
| `additive` | `partials` | Organs, tonal sounds |
| `wavetable` | `wavetable`, `position` | Complex evolving tones |
| `sample` | `source_path` | Sample-based (import existing) |

## Track Spec Format (TRACK)

```python
# .studio/music/boss_theme.spec.py
TRACK = {
    "track": {
        "name": "boss_theme",
        "format": "xm",           # "xm" or "it"
        "bpm": 140,
        "rows_per_beat": 4,       # Usually 4 (16 rows = 1 bar in 4/4)
        "channels": 8,
        "title": "Boss Battle",   # Embedded in file

        # Instrument references (paths relative to .studio/)
        "instruments": [
            "instruments/kick.spec.py",
            "instruments/snare.spec.py",
            "instruments/bass.spec.py",
            "instruments/lead.spec.py"
        ],

        # Pattern definitions
        "patterns": [
            {
                "name": "intro",
                "rows": 64,
                "data": {
                    # Channel 0: Kick
                    0: [
                        {"row": 0, "note": "C3", "inst": 0, "vol": 64},
                        {"row": 8, "note": "C3", "inst": 0, "vol": 48},
                        {"row": 16, "note": "C3", "inst": 0},
                        {"row": 24, "note": "C3", "inst": 0, "vol": 48}
                    ],
                    # Channel 1: Snare
                    1: [
                        {"row": 8, "note": "D3", "inst": 1},
                        {"row": 24, "note": "D3", "inst": 1}
                    ],
                    # Channel 2: Bass
                    2: [
                        {"row": 0, "note": "C2", "inst": 2},
                        {"row": 12, "note": "C2", "inst": 2},
                        {"row": 16, "note": "D#2", "inst": 2},
                        {"row": 28, "note": "D2", "inst": 2}
                    ]
                }
            },
            {
                "name": "verse",
                "rows": 64,
                "data": { ... }
            }
        ],

        # Pattern order (song arrangement)
        "sequence": [
            {"pattern": "intro", "repeat": 2},
            {"pattern": "verse"},
            {"pattern": "chorus"},
            {"pattern": "verse"},
            {"pattern": "chorus"},
            {"pattern": "outro"}
        ],

        # Global effects
        "master_volume": 64,
        "initial_speed": 6,       # Ticks per row
        "restart_position": 2     # Loop point (pattern index)
    }
}
```

### Note Format

Notes can be specified as:
- MIDI note names: `"C4"`, `"F#3"`, `"Bb5"`
- MIDI numbers: `60`, `48`, `72`
- Special: `"---"` (note off), `"^^^"` (note cut), `"==="` (note fade)

### Effect Commands

```python
# Effects are optional per-note
{"row": 0, "note": "C4", "inst": 0, "effect": "1", "effect_param": "0F"}
```

| Effect | XM | IT | Description |
|--------|----|----|-------------|
| `"0"` | Arpeggio | Arpeggio | xy = semitones |
| `"1"` | Porta Up | Porta Up | xx = speed |
| `"2"` | Porta Down | Porta Down | xx = speed |
| `"3"` | Tone Porta | Tone Porta | xx = speed |
| `"4"` | Vibrato | Vibrato | xy = speed, depth |
| `"A"` | Vol Slide | Vol Slide | xy = up/down |
| `"C"` | Set Volume | Set Volume | xx = 0-64 |
| `"F"` | Set Speed/BPM | Set Speed/BPM | xx < 32 = speed, else BPM |

## Parser Usage

```bash
# Generate SFX
python sound_parser.py sfx .studio/sounds/laser.spec.py generated/audio/laser.wav

# Generate instrument sample
python sound_parser.py instrument .studio/instruments/bass.spec.py generated/samples/bass.wav

# Generate tracker module (generates instrument samples + XM/IT)
python sound_parser.py track .studio/music/boss_theme.spec.py generated/tracks/boss_theme.xm
```

## Directory Structure

```
project/
├── .studio/
│   ├── sounds/           # SFX specs
│   │   ├── laser.spec.py
│   │   ├── explosion.spec.py
│   │   └── coin.spec.py
│   ├── instruments/      # Instrument specs
│   │   ├── kick.spec.py
│   │   ├── bass.spec.py
│   │   └── lead.spec.py
│   └── music/            # Track specs
│       ├── menu.spec.py
│       └── boss_theme.spec.py
└── generated/
    ├── audio/            # Generated WAV files
    ├── samples/          # Generated instrument samples
    └── tracks/           # Generated XM/IT files
```

## Design Guidelines

### SFX Categories

| Category | Typical Duration | Layers | Example |
|----------|------------------|--------|---------|
| `ui` | 0.05-0.2s | 1-2 | Button click, menu select |
| `action` | 0.1-0.5s | 2-4 | Jump, attack, collect |
| `projectile` | 0.2-0.5s | 2-3 | Laser, bullet, arrow |
| `impact` | 0.1-0.4s | 2-4 | Hit, explosion, collision |
| `ambient` | 1-5s | 1-3 | Wind, water, machinery |

### Instrument Categories

| Category | Synthesis | Loop | Example |
|----------|-----------|------|---------|
| `bass` | Karplus/FM | Yes | Bass guitar, synth bass |
| `lead` | FM/Subtractive | Yes | Lead synth, melody |
| `pad` | Additive/Subtractive | Yes | Ambient, atmosphere |
| `keys` | FM | Yes | Piano, organ, EP |
| `drums` | Noise + pitched | No | Kick, snare, hi-hat |
