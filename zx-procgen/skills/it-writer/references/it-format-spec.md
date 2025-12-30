# IT Format Specification (Summary)

Concise reference for the Impulse Tracker IT file format. Full specification: [ITTECH.TXT](https://github.com/schismtracker/schismtracker/wiki/ITTECH.TXT)

## File Structure

```
IT File Format:
┌─────────────────────────────┐
│ Header (192 bytes)          │  Magic, name, counts, flags
├─────────────────────────────┤
│ Order Table (variable)      │  Pattern play order
├─────────────────────────────┤
│ Instrument Offset Table     │  4 bytes × num_instruments
├─────────────────────────────┤
│ Sample Offset Table         │  4 bytes × num_samples
├─────────────────────────────┤
│ Pattern Offset Table        │  4 bytes × num_patterns
├─────────────────────────────┤
│ Instruments (variable)      │  ~550 bytes each
├─────────────────────────────┤
│ Sample Headers (variable)   │  80 bytes each
├─────────────────────────────┤
│ Patterns (variable)         │  Compressed pattern data
├─────────────────────────────┤
│ Sample Data (variable)      │  Raw PCM audio
└─────────────────────────────┘
```

## Header Format (192 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0 | 4 | Magic | "IMPM" (0x4D504D49) |
| 4 | 26 | Name | Song name (null-padded) |
| 30 | 2 | PHilight | Pattern highlighting (default: 0x0410) |
| 32 | 2 | OrdNum | Number of orders |
| 34 | 2 | InsNum | Number of instruments |
| 36 | 2 | SmpNum | Number of samples |
| 38 | 2 | PatNum | Number of patterns |
| 40 | 2 | Cwt | Created with tracker version |
| 42 | 2 | Cmwt | Compatible with version |
| 44 | 2 | Flags | Module flags |
| 46 | 2 | Special | Special flags |
| 48 | 1 | GV | Global volume (0-128) |
| 49 | 1 | MV | Mix volume (0-128) |
| 50 | 1 | IS | Initial speed (ticks/row) |
| 51 | 1 | IT | Initial tempo (BPM) |
| 52 | 1 | Sep | Panning separation (0-128) |
| 53 | 1 | PWD | Pitch wheel depth |
| 54 | 2 | MsgLgth | Message length |
| 56 | 4 | MsgOff | Message offset |
| 60 | 4 | Reserved | Reserved |
| 64 | 64 | ChnlPan | Channel pan (64 bytes) |
| 128 | 64 | ChnlVol | Channel volume (64 bytes) |

## Module Flags (Offset 44)

| Bit | Flag | Description |
|-----|------|-------------|
| 0 | STEREO | Stereo playback |
| 1 | VOL_0_MIX | Vol0 optimizations |
| 2 | INSTRUMENTS | Use instruments (vs samples-only) |
| 3 | LINEAR_SLIDES | Linear frequency slides |
| 4 | OLD_EFFECTS | Old IT effects (vs S3M) |
| 5 | LINK_G_MEMORY | Link G memory with E/F |
| 6 | MIDI_PITCH | MIDI pitch controller |
| 7 | EMBED_MIDI | Request embedded MIDI |

## Instrument Format (550 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0 | 4 | Magic | "IMPI" (0x49504D49) |
| 4 | 12 | Filename | DOS filename |
| 16 | 1 | Reserved | 0x00 |
| 17 | 1 | NNA | New note action (0-3) |
| 18 | 1 | DCT | Duplicate check type (0-3) |
| 19 | 1 | DCA | Duplicate check action (0-2) |
| 20 | 2 | Fadeout | Fadeout speed (0-1024) |
| 22 | 1 | PPS | Pitch-pan separation |
| 23 | 1 | PPC | Pitch-pan center |
| 24 | 1 | GbV | Global volume (0-128) |
| 25 | 1 | DfP | Default pan (0-64, +128 if enabled) |
| 26 | 1 | RV | Random volume variation |
| 27 | 1 | RP | Random panning variation |
| 28 | 4 | TrkVers | Tracker version/NoS |
| 32 | 26 | Name | Instrument name |
| 58 | 1 | IFC | Filter cutoff (+128 if enabled) |
| 59 | 1 | IFR | Filter resonance (+128 if enabled) |
| 60 | 1 | MCh | MIDI channel |
| 61 | 1 | MPr | MIDI program |
| 62 | 2 | MIDIBnk | MIDI bank |
| 64 | 240 | NoteTab | Note-sample table (120 × 2 bytes) |
| 304 | 82 | VolEnv | Volume envelope |
| 386 | 82 | PanEnv | Panning envelope |
| 468 | 82 | PitEnv | Pitch envelope |

### NNA (New Note Action)

- 0: Cut previous note
- 1: Continue previous note
- 2: Note off previous note
- 3: Fade out previous note

### DCT (Duplicate Check Type)

- 0: Off (no duplicate checking)
- 1: Note (check for same note)
- 2: Sample (check for same sample)
- 3: Instrument (check for same instrument)

### DCA (Duplicate Check Action)

- 0: Cut duplicate note
- 1: Note off duplicate
- 2: Fade out duplicate

## Envelope Format (82 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0 | 1 | Flags | Envelope flags |
| 1 | 1 | Num | Number of node points (0-25) |
| 2 | 1 | LpB | Loop begin point |
| 3 | 1 | LpE | Loop end point |
| 4 | 1 | SLB | Sustain loop begin |
| 5 | 1 | SLE | Sustain loop end |
| 6 | 75 | Nodes | 25 nodes × 3 bytes (Y, tick_lo, tick_hi) |
| 81 | 1 | Reserved | 0x00 |

### Envelope Flags

| Bit | Flag | Description |
|-----|------|-------------|
| 0 | ENABLED | Envelope is enabled |
| 1 | LOOP | Loop is enabled |
| 2 | SUSTAIN_LOOP | Sustain loop enabled |
| 3 | CARRY | Carry (unused) |
| 7 | FILTER | Filter envelope (not volume/pan) |

**Node Format:** Each node is 3 bytes:
- Byte 0: Y value (signed -32 to +32 for pitch, 0-64 for vol/pan)
- Bytes 1-2: Tick position (uint16, little-endian)

## Sample Format (80 bytes header)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0 | 4 | Magic | "IMPS" (0x53504D49) |
| 4 | 12 | Filename | DOS filename |
| 16 | 1 | Reserved | 0x00 |
| 17 | 1 | GvL | Global volume (0-64) |
| 18 | 1 | Flg | Sample flags |
| 19 | 1 | Vol | Default volume (0-64) |
| 20 | 26 | Name | Sample name |
| 46 | 1 | Cvt | Convert flags (0x01 = signed) |
| 47 | 1 | DfP | Default pan (0-64, +128 if enabled) |
| 48 | 4 | Length | Length in samples |
| 52 | 4 | LoopBeg | Loop begin in samples |
| 56 | 4 | LoopEnd | Loop end in samples |
| 60 | 4 | C5Speed | Sample rate for C-5 |
| 64 | 4 | SusLBeg | Sustain loop begin |
| 68 | 4 | SusLEnd | Sustain loop end |
| 72 | 4 | SmpPoint | Offset to sample data |
| 76 | 1 | ViS | Vibrato speed |
| 77 | 1 | ViD | Vibrato depth |
| 78 | 1 | ViR | Vibrato rate |
| 79 | 1 | ViT | Vibrato type (0-3) |

### Sample Flags

| Bit | Flag | Description |
|-----|------|-------------|
| 0 | HAS_DATA | Sample has associated data |
| 1 | 16BIT | 16-bit sample (vs 8-bit) |
| 2 | STEREO | Stereo sample |
| 3 | COMPRESSED | IT215 compressed |
| 4 | LOOP | Loop enabled |
| 5 | SUSTAIN_LOOP | Sustain loop enabled |
| 6 | LOOP_PINGPONG | Ping-pong loop |
| 7 | SUSTAIN_PINGPONG | Sustain ping-pong |

## Pattern Format (Compressed)

Patterns use channel-based compression:

```
Pattern Header (8 bytes):
  +0: Length (uint16) - packed data size
  +2: Rows (uint16) - number of rows
  +4: Reserved (4 bytes)

Pattern Data (variable):
  For each row:
    For each channel with data:
      Channel marker (1 byte):
        Bits 0-5: Channel number (0-63)
        Bit 7: Mask variable follows

      If mask variable:
        Mask byte (1 byte):
          Bit 0: Note present
          Bit 1: Instrument present
          Bit 2: Volume present
          Bit 3: Effect present
          Bit 4: Use previous note
          Bit 5: Use previous instrument
          Bit 6: Use previous volume
          Bit 7: Use previous effect

      Data bytes (if mask bits 0-3 set):
        Note (1 byte if bit 0)
        Instrument (1 byte if bit 1)
        Volume (1 byte if bit 2)
        Effect + Param (2 bytes if bit 3)

    Row end marker (1 byte = 0x00)
```

### Note Values

- 0: No note
- 1-119: C-0 to B-9 (120 notes)
- 253: Note fade
- 254: Note cut (===)
- 255: Note off (^^^)

## Sample Data

Samples are stored as raw PCM:
- **8-bit:** Signed int8 (-128 to 127)
- **16-bit:** Signed int16 little-endian (-32768 to 32767)
- **Stereo:** Interleaved L/R channels

If compressed (IT215), see ITTECH.TXT for decompression algorithm.

## Effect Values (A-Z)

Effects are encoded as 1-26 (A=1, B=2, ..., Z=26) with 8-bit parameter.

See `it-effects.md` for complete effect reference.

## Python Implementation Notes

The `it_writer.py` library handles all these details automatically:

```python
from it_writer import ItModule, ItPattern, ItNote, write_it

# High-level API - format details abstracted
module = ItModule(name="Song", num_channels=4, default_speed=6, default_bpm=125)
pattern = ItPattern.empty(64, 4)
pattern.set_note(0, 0, ItNote.play("C-4", 1, 64))
module.patterns.append(pattern)
module.order_table = [0]

write_it(module, "output.it")  # Handles all binary formatting
```

## Reference

**Full Specification:** https://github.com/schismtracker/schismtracker/wiki/ITTECH.TXT

**Key Differences from XM:**
- 64 channels (vs 32)
- Note range: 120 notes (vs 96)
- NNA support (polyphony)
- Pitch envelopes (XM lacks these)
- Resonant filters
- More complex volume column encoding
- Channel-based pattern compression (vs XM's row-based)
