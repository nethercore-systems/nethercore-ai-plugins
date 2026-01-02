---
name: XM Format (FastTracker 2)
description: |
  Use this skill for XM file generation - the simpler of the two tracker formats. Provides Python library for programmatic XM creation.

  **Trigger phrases:** "generate XM", "write XM file", "XM module", "FastTracker", "procedural XM", "XM effects"

  **Load references when:**
  - Effect command details → `references/xm-effects.md`
  - Binary format details → `references/xm-format-spec.md`

  **Use XM when:**
  - Simpler songs with ≤32 channels
  - Smaller file size preferred
  - Don't need NNA polyphony or pitch envelopes

  **Use IT instead when:** Need >32 channels, NNA, pitch envelopes, or resonant filters.

  For composition philosophy, use `tracker-fundamentals`.
  For music theory, use `sound-design:music-composition`.
version: 1.0.0
---

# XM Format (FastTracker 2)

## Overview

XM (Extended Module) is the FastTracker 2 format - simpler and more compact than IT. Ideal for most game music needs.

**Key characteristics:**
- Up to 32 channels
- Note range: C-0 to B-7 (8 octaves)
- Volume and panning envelopes
- Standard effect set (arpeggio, portamento, vibrato, etc.)
- Delta-encoded 16-bit samples (good compression)

## Quick Start

```python
from xm_writer import XmModule, XmPattern, XmNote, XmInstrument, write_xm

# Generate sample data (use procedural-sounds skill!)
kick_sample = generate_kick_sample()  # Returns bytes (16-bit signed PCM)

# Create pattern
pattern = XmPattern.empty(64, num_channels=4)
pattern.set_note(0, 0, XmNote.play("C-4", instrument=1, volume=64))
pattern.set_note(16, 1, XmNote.play("C-4", instrument=2, volume=60))

# Create module with embedded samples
module = XmModule(
    name="My Song",
    num_channels=4,
    default_speed=6,
    default_bpm=125,
    order_table=[0],
    patterns=[pattern],
    instruments=[
        XmInstrument.for_zx("kick", kick_sample),
    ]
)

# Write file
write_xm(module, "output.xm")
```

## Core API

### XmNote

```python
XmNote.play("C-4", instrument=1, volume=64)  # Create note
XmNote.off()                                  # Note off
note_from_name("C#4")                         # Convert name to value
```

**Note values:** 0=none, 1-96=C-0 to B-7, 97=note-off

### XmPattern

```python
pattern = XmPattern.empty(64, num_channels=4)
pattern.set_note(row, channel, note)
```

### XmInstrument

```python
XmInstrument(
    name="kick",              # Becomes ROM sound ID
    sample_data=kick_bytes,   # 16-bit signed PCM
    sample_bits=16,           # 8 or 16
    sample_rate=22050,        # Auto-calculates pitch correction
    sample_loop_type=0,       # 0=one-shot, 1=forward, 2=ping-pong
    sample_loop_start=0,
    sample_loop_length=0,
)

# Convenience constructor for ZX
XmInstrument.for_zx("kick", kick_bytes)
```

### XmModule

```python
XmModule(
    name="Song Name",
    num_channels=4,           # 1-32
    default_speed=6,          # Ticks per row
    default_bpm=125,          # Tempo
    restart_position=0,       # Loop point in order table
    order_table=[0, 1, 0, 2], # Pattern sequence
    patterns=[...],
    instruments=[...],
)
```

## Effects

XM uses hex effect numbers (0-F, plus extended). Common effects:

| Effect | Hex | Usage |
|--------|-----|-------|
| Arpeggio | 0 | `XmNote(effect=0, effect_param=0x37)` |
| Porta Up | 1 | `XmNote(effect=1, effect_param=0x10)` |
| Porta Down | 2 | `XmNote(effect=2, effect_param=0x10)` |
| Tone Porta | 3 | `XmNote(effect=3, effect_param=0x10)` |
| Vibrato | 4 | `XmNote(effect=4, effect_param=0x34)` |
| Vol Slide | 10 | `XmNote(effect=10, effect_param=0x0F)` |
| Set Volume | 12 | `XmNote(effect=12, effect_param=0x40)` |
| Speed/Tempo | 15 | `XmNote(effect=15, effect_param=6)` if <32, else BPM |

See `references/xm-effects.md` for complete list.

## Pitch Correction

XM expects 8363 Hz samples at C-4. For 22050 Hz ZX samples:

```python
# Option 1: Set sample_rate (recommended)
XmInstrument(name="kick", sample_rate=22050, sample_data=data)

# Option 2: Use convenience constructor
XmInstrument.for_zx("kick", data)

# Option 3: Manual (finetune=101, relative_note=16 for 22050 Hz)
XmInstrument(name="kick", sample_finetune=101, sample_relative_note=16, ...)
```

## Nethercore Integration

XM files integrate with nether.toml:

```toml
# Samples are auto-extracted from embedded XM
[[assets.trackers]]
id = "boss_theme"
path = "music/boss_theme.xm"
```

```rust
// In game code
let music = rom_tracker(b"boss_theme", 10);
music_play(music, 0.8, 1);
```

## Volume Column

The volume column (0-64) sets volume directly. Values 65+ are effects:

| Range | Effect |
|-------|--------|
| 0x10-0x50 | Set volume 0-64 |
| 0x60-0x6F | Volume slide down |
| 0x70-0x7F | Volume slide up |
| 0xC0-0xCF | Set panning |
| 0xF0-0xFF | Tone portamento |

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
    pattern = XmPattern.empty(len(notes) * rows_per_note, 4)
    for i, note_name in enumerate(notes):
        if note_name != "---":
            pattern.set_note(i * rows_per_note, 0,
                XmNote.play(note_name, instrument, 64))
    return pattern
```

## Validation

```python
from xm_writer import validate_xm

validate_xm("output.xm")  # Raises ValueError if invalid
```

Also test by:
1. Opening in MilkyTracker
2. Running `nether pack`
3. Playing in Nethercore

## File Size Optimization

- Reuse patterns via order table
- Use fewer channels when possible
- Empty notes compress to 1 byte
- 8-bit samples are half the size of 16-bit

## Project Folder Structure

When generating music, follow this structure:

```
project/
├── generators/                    # Source code (committed)
│   ├── lib/                       # Copy xm_writer.py here
│   │   └── xm_writer.py           # From this skill's scripts/
│   └── tracks/                    # Generator scripts
│       └── song_name.py
└── generated/                     # Output (gitignored)
    └── tracks/
        └── song_name.xm
```

**Canonical location:** `tracker-music/skills/xm-format/scripts/`

Copy both `xm_types.py` and `xm_writer.py` to project's `generators/lib/` when scaffolding.

## Related Skills

- **`it-format`** - IT format (more features, larger files)
- **`tracker-fundamentals`** - When/why to use effects
- **`pattern-design`** - Song structure and efficiency

## Reference Files

- **`scripts/xm_types.py`** - API surface: dataclasses, constants (READ THIS ~250 lines)
- **`scripts/xm_writer.py`** - Binary implementation (just import, don't read)
- **`references/xm-effects.md`** - Effect command reference
- **`references/xm-format-spec.md`** - Binary format specification
- **`examples/basic_xm.py`** - Drum loop example
- **`examples/with_samples.py`** - Embedded samples example
