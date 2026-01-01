---
name: IT Format (Impulse Tracker)
description: |
  Use this skill for IT file generation - the more powerful of the two tracker formats. Provides Python library for programmatic IT creation with advanced features.

  **Trigger phrases:** "generate IT", "write IT file", "Impulse Tracker", "procedural IT", "NNA", "pitch envelope", "IT effects"

  **Load references when:**
  - Effect command details → `references/it-effects.md`
  - Workflow examples → `references/workflow-guide.md`
  - Binary format details → `references/it-format-spec.md`

  **Use IT when:**
  - Need >32 channels (IT: 64)
  - Need NNA polyphony (notes fade/continue)
  - Need pitch envelopes
  - Need resonant filters

  **Use XM instead when:** Simpler songs, smaller file size, features sufficient.

  For composition philosophy, use `tracker-fundamentals`.
  For music theory, use `sound-design:music-composition`.
version: 1.0.0
---

# IT Format (Impulse Tracker)

## Overview

IT (Impulse Tracker) is the more advanced tracker format with features beyond XM.

**Key advantages over XM:**
- Up to 64 channels (vs 32)
- Note range: C-0 to B-9 (10 octaves vs 8)
- NNA (New Note Actions) for polyphonic instruments
- Pitch envelopes (modulate pitch over time)
- Resonant filters (cutoff + resonance)
- Multi-sample instruments (different samples per note range)

## Quick Start

```python
from it_writer import ItModule, ItPattern, ItNote, ItInstrument, ItSample, write_it

# Generate sample data
kick_sample = generate_kick_sample()  # 16-bit signed PCM bytes

# Create pattern
pattern = ItPattern.empty(64, num_channels=4)
pattern.set_note(0, 0, ItNote.play("C-4", instrument=1, volume=64))
pattern.set_note(16, 1, ItNote.play("C-4", instrument=2, volume=60))

# Create module
module = ItModule(
    name="My Song",
    num_channels=4,
    default_speed=6,
    default_bpm=125,
    order_table=[0],
    patterns=[pattern],
    instruments=[ItInstrument(name="kick")],
    samples=[ItSample(name="kick", c5_speed=22050, default_volume=64)],
    sample_data=[kick_sample]
)

# Write file
write_it(module, "output.it")
```

## Core API

### ItNote

```python
ItNote.play("C-4", instrument=1, volume=64)   # Basic note
ItNote.play_note(60, 1, 64)                    # MIDI note number
ItNote.off()                                    # Note-off (^^^)
ItNote.cut()                                    # Note-cut (===)
ItNote.fade()                                   # Note-fade

# Chainable builders
note = ItNote.play("C-4", 1, 64)
    .with_effect(7, 0x10)        # Tone portamento G10
    .with_volume_column(85)       # Volume slide up
```

**Note values:** 0-119 (C-0 to B-9), 253=fade, 254=cut, 255=off

### ItPattern

```python
pattern = ItPattern.empty(64, num_channels=8)
pattern.set_note(row, channel, note)
```

### ItInstrument

```python
ItInstrument(
    name="Piano",
    nna=NNA_FADE,            # Cut, Continue, Off, Fade
    dct=DCT_NOTE,            # Duplicate check: Off, Note, Sample, Instrument
    dca=DCA_CUT,             # Duplicate action: Cut, Off, Fade
    fadeout=256,             # Fade speed (0-1024)
    global_volume=128,       # 0-128
    default_pan=32,          # 0-64 (32=center), None=disabled
    volume_envelope=vol_env, # Optional ItEnvelope
    pitch_envelope=pitch_env,# IT-only! ±2 octaves
    filter_cutoff=127,       # IT-only! 0-127
    filter_resonance=0,      # IT-only! 0-127
)
```

### ItSample

```python
ItSample(
    name="kick",
    c5_speed=22050,      # Sample rate
    default_volume=64,   # 0-64
    flags=SAMPLE_LOOP,   # Loop flags
    loop_begin=0,
    loop_end=1000,
)
```

### ItModule

```python
ItModule(
    name="Song Name",
    num_channels=4,          # 1-64
    default_speed=6,
    default_bpm=125,
    global_volume=128,       # 0-128
    order_table=[0, 1, 0],
    patterns=[...],
    instruments=[...],
    samples=[...],
    sample_data=[...],       # List of bytes for each sample
)
```

## Effects (A-Z)

IT uses letter-based effects (A=1, B=2, ..., Z=26):

| Effect | Letter | Code | Usage |
|--------|--------|------|-------|
| Set Speed | A | 1 | `.with_effect(1, 6)` |
| Position Jump | B | 2 | `.with_effect(2, 0)` |
| Pattern Break | C | 3 | `.with_effect(3, 0)` |
| Volume Slide | D | 4 | `.with_effect(4, 0x0F)` |
| Porta Down | E | 5 | `.with_effect(5, 0x10)` |
| Porta Up | F | 6 | `.with_effect(6, 0x10)` |
| Tone Porta | G | 7 | `.with_effect(7, 0x10)` |
| Vibrato | H | 8 | `.with_effect(8, 0x34)` |
| Tremor | I | 9 | `.with_effect(9, 0x34)` |
| Arpeggio | J | 10 | `.with_effect(10, 0x37)` |
| Set Tempo | T | 20 | `.with_effect(20, 125)` |
| Set Panning | X | 24 | `.with_effect(24, 0x80)` |

See `references/it-effects.md` for complete list.

## NNA (New Note Actions)

NNA controls polyphonic behavior:

```python
from it_writer import NNA_CUT, NNA_CONTINUE, NNA_OFF, NNA_FADE

# Polyphonic piano - previous notes fade when new ones play
piano = ItInstrument(
    name="Piano",
    nna=NNA_FADE,         # Fade previous note
    dct=DCT_NOTE,         # Check for duplicate notes
    dca=DCA_FADE,         # Fade duplicates
    fadeout=512,          # Fade speed
)

# One channel can now play chords!
pattern.set_note(0, 0, ItNote.play("C-4", 1, 64))
pattern.set_note(0, 1, ItNote.play("E-4", 1, 64))
pattern.set_note(0, 2, ItNote.play("G-4", 1, 64))
```

## Envelopes

### Volume Envelope (ADSR)

```python
from it_writer import ItEnvelope, ENV_ENABLED, ENV_LOOP, ENV_SUSTAIN_LOOP

vol_env = ItEnvelope()
vol_env.points = [
    (0, 0),      # Start silent
    (10, 64),    # Attack to peak
    (30, 48),    # Decay to sustain
    (100, 48),   # Hold sustain
    (130, 0),    # Release to silence
]
vol_env.sustain_begin = 2
vol_env.sustain_end = 3
vol_env.flags = ENV_ENABLED | ENV_SUSTAIN_LOOP

instr = ItInstrument(name="Pad", volume_envelope=vol_env)
```

### Pitch Envelope (IT-only)

```python
# Kick drum with pitch drop
pitch_env = ItEnvelope()
pitch_env.points = [
    (0, 24),     # Start high (+24 semitones)
    (15, 0),     # Drop to normal pitch
]
pitch_env.flags = ENV_ENABLED

kick = ItInstrument(name="Kick", pitch_envelope=pitch_env)
```

### Filter Envelope (IT-only)

```python
# Bass with filter sweep
filter_env = ItEnvelope()
filter_env.points = [
    (0, 64),     # Start bright
    (50, 16),    # Sweep to dark
]
filter_env.flags = ENV_ENABLED | ENV_FILTER

bass = ItInstrument(
    name="Bass",
    filter_cutoff=127,
    filter_resonance=32,
    filter_envelope=filter_env
)
```

## Multi-Sample Instruments

Map different samples to note ranges:

```python
piano = ItInstrument(name="Piano")

# Map notes to samples
for note in range(0, 40):      # Low notes
    piano.note_sample_table[note] = (note, 1)
for note in range(40, 80):     # Mid notes
    piano.note_sample_table[note] = (note, 2)
for note in range(80, 120):    # High notes
    piano.note_sample_table[note] = (note, 3)
```

## Nethercore Integration

```toml
[[assets.trackers]]
id = "boss_theme"
path = "music/boss_theme.it"
```

```rust
let music = rom_tracker(b"boss_theme", 10);
music_play(music, 0.8, 1);
```

## Validation

```python
from it_writer import validate_it

validate_it("output.it")  # Prints validation message
```

Test by:
1. Opening in OpenMPT or SchismTracker
2. Running `nether pack`
3. Playing in Nethercore

## XM vs IT Decision

| Feature | XM | IT |
|---------|----|----|
| Channels | 32 | 64 |
| Note range | 8 octaves | 10 octaves |
| Polyphony | Note-off only | NNA (fade, continue) |
| Pitch envelope | No | Yes |
| Resonant filter | No | Yes |
| File size | Smaller | Larger |

**Choose IT when:** Polyphonic instruments, pitch effects, filters, or >32 channels needed.

## Project Folder Structure

When generating music, follow this structure:

```
project/
├── generators/                    # Source code (committed)
│   ├── lib/                       # Copy it_writer.py here
│   │   └── it_writer.py           # From this skill's scripts/
│   └── tracks/                    # Generator scripts
│       └── song_name.py
└── generated/                     # Output (gitignored)
    └── tracks/
        └── song_name.it
```

**Canonical writer location:** `tracker-music/skills/it-format/scripts/it_writer.py`

Copy to project's `generators/lib/` when scaffolding.

## Related Skills

- **`xm-format`** - XM format (simpler, smaller)
- **`tracker-fundamentals`** - When/why to use effects
- **`pattern-design`** - Song structure and efficiency

## Reference Files

- **`scripts/it_writer.py`** - Python library (CANONICAL SOURCE)
- **`references/it-effects.md`** - Complete effect reference
- **`references/workflow-guide.md`** - Envelopes, NNA examples
- **`references/it-format-spec.md`** - Binary format specification
