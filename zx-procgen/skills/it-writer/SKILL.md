---
name: Programmatic IT Generation
description: This skill should be used when the user asks to "generate IT programmatically", "write IT from code", "procedural Impulse Tracker", "create IT module from Python", "IT writer", "algorithmically generate IT music", "procedural IT", "output IT file", or needs to create IT (Impulse Tracker) files without using a tracker GUI. Provides Python library for generating valid IT files with embedded samples.
version: 1.0.0
---

# Programmatic IT Generation

## Overview

Generate valid Impulse Tracker IT files programmatically using Python. IT format provides advanced features beyond XM: 64 channels (vs 32), NNA (New Note Actions), pitch envelopes, resonant filters, and multi-sample instruments.

**This skill provides:** Low-level IT file writing primitives (Python library, data structures, binary format).

**For composition theory:** Use `sound-design:music-composition` for melody generation, chord progressions, and song structure.

## When to Use IT vs XM

| Use IT | Use XM |
|--------|--------|
| Need >32 channels (IT: 64) | ≤32 channels sufficient |
| Need NNA (polyphonic fade) | Simple note cut/off OK |
| Need pitch envelopes | Volume/panning only |
| Need resonant filters | No filtering needed |
| Multi-sample instruments | Single sample/instrument |

Both formats work identically with Nethercore's tracker engine and sample loading system.

## Quick Start

```python
from it_writer import ItModule, ItPattern, ItNote, ItInstrument, write_it

# Generate sample data (use procedural-sounds skill!)
kick_sample = generate_kick_sample()  # Returns bytes (16-bit signed PCM)

# Create pattern
pattern = ItPattern.empty(64, num_channels=4)
pattern.set_note(0, 0, ItNote.play("C-4", instrument=1, volume=64))
pattern.set_note(16, 1, ItNote.play("C-4", instrument=2, volume=60))

# Create module WITH embedded samples (DEFAULT workflow)
module = ItModule(
    name="My Song",
    num_channels=4,
    default_speed=6,
    default_bpm=125,
    order_table=[0],
    patterns=[pattern],
    instruments=[ItInstrument(name="kick")],
    samples=[ItSample(name="kick", c5_speed=22050, default_volume=64)],
    sample_data=[kick_sample]  # Raw 16-bit PCM bytes
)

# Write file
write_it(module, "output.it")
```

## Core API

### ItNote Helper Methods

```python
ItNote.play("C-4", instrument=1, volume=64)    # Pitch + instrument + volume
ItNote.play_note(60, 1, 64)                    # MIDI note number (60 = C-4)
ItNote.off()                                    # Note-off (^^^)
ItNote.cut()                                    # Note-cut (===)
ItNote.fade()                                   # Note-fade

# Chainable builders
note = ItNote.play("C-4", 1, 64)
    .with_effect(7, 0x10)        # Tone portamento G10
    .with_volume_column(85)       # Volume slide up
```

**Note range:** C-0 (0) to B-9 (119) - 10 octaves vs XM's 8

### ItPattern

```python
pattern = ItPattern.empty(64, num_channels=8)
pattern.set_note(row, channel, note)
```

### ItInstrument (Advanced)

IT instruments map different notes to different samples and control polyphonic behavior with NNA.

```python
instr = ItInstrument(
    name="Piano",
    global_volume=128,           # 0-128
    default_pan=32,              # 0-64 (32=center), None=disabled
    nna=NNA_FADE,                # Cut, Continue, Off, Fade
    dct=DCT_NOTE,                # Duplicate check: Off, Note, Sample, Instrument
    dca=DCA_CUT,                 # Duplicate action: Cut, Off, Fade
    fadeout=256,                 # 0-1024 (higher = faster fade)
    volume_envelope=vol_env,     # Optional ItEnvelope
    pitch_envelope=pitch_env,    # IT-only! Modulates pitch ±2 octaves
    filter_cutoff=127,           # IT-only! 0-127
    filter_resonance=0,          # IT-only! 0-127
)

# Multi-sample mapping (advanced)
instr.note_sample_table = [(note, sample_id) for note in range(120)]
```

See `references/workflow-guide.md` for envelope creation and NNA examples.

## Nethercore Integration

IT files work identically to XM:

```toml
# nether.toml - Just add IT file, samples auto-extracted!
[[assets.trackers]]
id = "boss_theme"
path = "music/boss_theme.it"
# Instruments become: rom_sound("kick"), rom_sound("snare"), etc.
```

```rust
// In game code
let kick = rom_sound(b"kick", 10);
let music = rom_tracker(b"boss_theme", 10);
music_play(music, 0.8, 1);
```

## IT Effects

IT uses A-Z effect commands (1-26 in Python):

| Effect | Letter | Value | Usage |
|--------|--------|-------|-------|
| Set Speed | A | 1 | `with_effect(1, 6)` |
| Position Jump | B | 2 | `with_effect(2, 0)` |
| Pattern Break | C | 3 | `with_effect(3, 0)` |
| Volume Slide | D | 4 | `with_effect(4, 0x0F)` |
| Porta Down | E | 5 | `with_effect(5, 0x10)` |
| Porta Up | F | 6 | `with_effect(6, 0x10)` |
| Tone Portamento | G | 7 | `with_effect(7, 0x10)` |
| Vibrato | H | 8 | `with_effect(8, 0x34)` |
| Set Tempo | T | 20 | `with_effect(20, 125)` |
| Set Panning | X | 24 | `with_effect(24, 0x80)` |

See `references/it-effects.md` for complete list with examples.

## Volume Column

IT volume column has complex encoding:

- **0-64**: Set volume
- **65-74**: Fine volume up (a-j)
- **75-84**: Fine volume down (k-t)
- **85-94**: Volume slide up
- **95-104**: Volume slide down
- **128-192**: Set panning (0-64)

```python
note.with_volume_column(64)   # Max volume
note.with_volume_column(85)   # Fine volume slide up
note.with_volume_column(160)  # Set panning center (128 + 32)
```

## Testing

```python
# Validate file format
from it_writer import validate_it
validate_it("output.it")

# Also test:
# 1. Open in OpenMPT or SchismTracker
# 2. Run `nether pack` to verify parsing
# 3. Play in Nethercore player
```

## Related Skills

- **`xm-writer`** - XM format generation (simpler alternative)
- **`procedural-music`** - Manual tracker composition, music theory
- **`procedural-sounds`** - Generate sample audio data (synthesis)
- **`sound-design:music-composition`** - Melody, chords, song structure

## Reference Files

- **`it_writer.py`** - Python library (import this in your scripts)
- **`references/workflow-guide.md`** - Envelopes, NNA examples, patterns
- **`references/it-effects.md`** - Complete effect command reference
- **`references/it-format-spec.md`** - Byte-level IT format (ITTECH.TXT summary)
