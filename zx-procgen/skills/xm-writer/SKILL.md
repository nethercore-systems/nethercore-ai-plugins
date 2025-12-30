---
name: Programmatic XM Generation
description: This skill should be used when the user asks to "generate XM programmatically", "write XM from code", "procedural music generation", "create tracker module from Python", "XM writer", "algorithmically generate music", "procedural XM", "output XM file", "create XM without tracker", or needs to create XM files without using a tracker GUI. Provides Python library and guidance for generating valid FastTracker 2 XM files programmatically.
version: 1.0.0
---

# Programmatic XM Generation

## Overview

This skill provides a Python library (`xm_writer.py`) for generating valid FastTracker 2 XM files programmatically. Use this when creating music algorithmically without a tracker GUI.

**This skill provides:** Low-level XM file writing primitives (data structures, binary format, file output).

**For composition theory:** Use the `sound-design` plugin's `music-composition` skill for melody generation, chord progressions, and song structure algorithms.

## When to Use

| Use This Skill | Use procedural-music Skill |
|----------------|---------------------------|
| Generating XM from code/algorithms | Composing in MilkyTracker/OpenMPT |
| Procedural/random music generation | Manual pattern editing |
| Automated asset pipeline | Learning tracker workflow |
| No GUI tracker available | Fine-tuning with visual feedback |

## Quick Start

```python
from xm_writer import XmModule, XmPattern, XmNote, XmInstrument, write_xm

# Create pattern
pattern = XmPattern.empty(64, num_channels=4)
pattern.set_note(0, 0, XmNote.play("C-4", instrument=1, volume=64))
pattern.set_note(16, 1, XmNote.play("C-4", instrument=2, volume=60))

# Create module
module = XmModule(
    name="My Song",
    num_channels=4,
    default_speed=6,
    default_bpm=120,
    order_table=[0],
    patterns=[pattern],
    instruments=[
        XmInstrument(name="kick"),    # Maps to ROM sample
        XmInstrument(name="snare"),
    ]
)

# Write file
write_xm(module, "output.xm")
```

## Core Data Structures

### XmNote

Single note/command in a pattern cell.

```python
@dataclass
class XmNote:
    note: int = 0           # 0=none, 1-96=C-0..B-7, 97=note-off
    instrument: int = 0     # 0=none, 1-128=instrument number
    volume: int = 0         # 0=none, 0x10-0x50=set volume (0-64)
    effect: int = 0         # Effect command (0-35)
    effect_param: int = 0   # Effect parameter (0-255)
```

**Helper methods:**
- `XmNote.play("C-4", instrument=1, volume=64)` - Create note with volume
- `XmNote.off()` - Create note-off
- `note_from_name("C#4")` - Convert name to note value

### XmPattern

Grid of notes (rows x channels).

```python
pattern = XmPattern.empty(64, num_channels=4)  # 64 rows, 4 channels
pattern.set_note(row, channel, note)           # Set note at position
```

### XmInstrument

Instrument metadata. **Name maps to ROM sample ID.**

```python
XmInstrument(
    name="kick",              # MUST match [[assets.sounds]] id
    volume_envelope=None,     # Optional XmEnvelope
    panning_envelope=None,
    vibrato_type=0,           # 0=sine, 1=square, 2=ramp down, 3=ramp up
    volume_fadeout=0,         # 0-4095
    sample_finetune=0,        # -128 to 127
    sample_relative_note=0,   # Semitones from C-4
)
```

### XmModule

Complete XM module containing all data.

```python
XmModule(
    name="Song Name",         # Max 20 chars
    num_channels=4,           # 1-32 channels
    default_speed=6,          # Ticks per row
    default_bpm=125,          # Tempo
    restart_position=0,       # Order to loop to
    linear_frequency_table=True,
    order_table=[0, 1, 0, 2], # Pattern play order
    patterns=[...],           # List of XmPattern
    instruments=[...],        # List of XmInstrument
)
```

## Nethercore Integration

### Approach 1: Embedded Samples (Recommended - Auto-Extraction)

XM files can contain embedded sample data. At pack time, `nether pack` automatically:
- Extracts all samples from the XM file
- Converts them to 22050 Hz mono i16 format
- Creates ROM sound IDs from instrument names (sanitized: `"My Kick!"` → `"my_kick"`)
- Deduplicates identical samples across files (by content hash)
- Makes samples available via `rom_sound("instrument_name")`

**Benefits:**
- No manual sample export from tracker
- No `[[assets.sounds]]` manifest entries needed
- Automatic deduplication across tracks
- Samples stay with the music file

**Example:**

```python
# Generate XM with embedded samples (use real sample data, not zeros!)
module = XmModule(
    name="Boss Theme",
    instruments=[
        XmInstrument(name="Kick_Drum", sample_data=kick_samples),
        XmInstrument(name="Bass_Synth", sample_data=bass_samples),
    ],
    # ...
)
write_xm(module, "boss_theme.xm")
```

```toml
# nether.toml - Just add the XM file, samples auto-extracted!
[[assets.trackers]]
id = "boss_theme"
path = "music/boss_theme.xm"
# Instruments automatically become: rom_sound("kick_drum"), rom_sound("bass_synth")
```

```rust
// In game code - samples are available!
let kick = rom_sound(b"kick_drum", 10);
let bass = rom_sound(b"bass_synth", 10);
let music = rom_tracker(b"boss_theme", 10);
music_play(music, 0.8, 1);
```

### Approach 2: ROM-Only References (Legacy - Sample-less XM)

XM files can have `sample_length=0`, with instrument names mapping to separately
loaded `[[assets.sounds]]` IDs in nether.toml.

**Use when:**
- Sharing samples across many XM files without embedding
- Samples loaded from other sources (procedural generation, WAV files)

**Example:**

```toml
# nether.toml
[[assets.sounds]]
id = "kick"          # Must match XmInstrument(name="kick") exactly
path = "samples/kick.wav"

[[assets.trackers]]
id = "my_song"
path = "music/my_song.xm"
```

**Note:** You can mix both approaches - auto-extracted samples supplement (not replace) manual entries.

## Common Patterns

### Basic Drum Loop

```python
def create_drum_pattern(rows=64):
    pattern = XmPattern.empty(rows, 4)
    for row in range(rows):
        if row % 32 == 0:      # Kick on 1, 3
            pattern.set_note(row, 0, XmNote.play("C-4", 1, 64))
        if row % 32 == 16:     # Snare on 2, 4
            pattern.set_note(row, 1, XmNote.play("C-4", 2, 60))
        if row % 4 == 0:       # Hi-hat 16ths
            pattern.set_note(row, 2, XmNote.play("C-4", 3, 48))
    return pattern
```

### Melody from Note List

```python
def melody_to_pattern(notes, instrument, rows_per_note=8):
    """Convert note names to pattern."""
    pattern = XmPattern.empty(len(notes) * rows_per_note, 4)
    for i, note_name in enumerate(notes):
        if note_name != "---":
            pattern.set_note(i * rows_per_note, 0,
                XmNote.play(note_name, instrument, 64))
    return pattern

# Example: C major scale
melody = ["C-4", "D-4", "E-4", "F-4", "G-4", "A-4", "B-4", "C-5"]
pattern = melody_to_pattern(melody, instrument=4)
```

### Song Structure with Order Table

```python
# Create patterns for different sections
intro = create_intro_pattern()      # Pattern 0
verse = create_verse_pattern()      # Pattern 1
chorus = create_chorus_pattern()    # Pattern 2
outro = create_outro_pattern()      # Pattern 3

module = XmModule(
    # ... other fields ...
    patterns=[intro, verse, chorus, outro],
    order_table=[0, 1, 1, 2, 1, 1, 2, 2, 3],  # Intro, V, V, C, V, V, C, C, Outro
    restart_position=1,  # Loop back to first verse
)
```

## Effect Commands

Common effects (see `references/xm-effects.md` in procedural-music skill for complete list):

| Effect | Hex | Usage |
|--------|-----|-------|
| Arpeggio | 0 | `XmNote(effect=0, effect_param=0x37)` for major chord |
| Porta Up | 1 | `XmNote(effect=1, effect_param=0x10)` |
| Porta Down | 2 | `XmNote(effect=2, effect_param=0x10)` |
| Volume Slide | 10 | `XmNote(effect=10, effect_param=0x0F)` slide down |
| Set Volume | 12 | `XmNote(effect=12, effect_param=0x40)` full volume |
| Set Speed | 15 | `XmNote(effect=15, effect_param=6)` if < 32 |
| Set BPM | 15 | `XmNote(effect=15, effect_param=120)` if >= 32 |

## Validation

```python
from xm_writer import validate_xm

try:
    validate_xm("output.xm")
    print("Valid XM file")
except ValueError as e:
    print(f"Invalid: {e}")
```

Also test by:
1. Opening in MilkyTracker - should load without errors
2. Running `nether pack` - should process without errors
3. Playing in Nethercore player - should produce audio

## File Size Optimization

XM pattern data uses compression (packed format). Tips for smaller files:
- Use fewer channels when possible
- Reuse patterns via order table instead of duplicating
- Keep pattern count low (combine similar sections)
- Empty notes compress to 1 byte each

## Related Skills

- **`procedural-music`** - Manual tracker composition, XM format overview
- **`sound-design/music-composition`** - Music theory, melody generation, chord progressions
- **`procedural-sounds`** - Generate WAV samples for instruments

## Reference Files

- **`references/xm-format-spec.md`** - Byte-level XM format specification
- **`examples/basic_xm.py`** - Working drum loop example
