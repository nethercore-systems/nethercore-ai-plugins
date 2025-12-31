# XM Format Specification (FastTracker 2)

Reference for XM file format version 0x0104. All multi-byte values are little-endian.

## File Structure

```
XM File
├── Header (60 bytes fixed + 276 bytes from header_size)
├── Pattern Data (variable, one per pattern)
└── Instrument Data (variable, one per instrument)
    └── Sample Headers (40 bytes each, sample_length=0 for Nethercore)
```

## Header (Offset 0)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0 | 17 | magic | `"Extended Module: "` (with trailing space) |
| 17 | 20 | name | Module name, null-padded |
| 37 | 1 | marker | Always `0x1A` |
| 38 | 20 | tracker | Tracker name, null-padded |
| 58 | 2 | version | `0x0104` (bytes: `04 01`) |
| 60 | 4 | header_size | Header size from this point (typically 276) |
| 64 | 2 | song_length | Number of entries in order table |
| 66 | 2 | restart_pos | Restart position for looping |
| 68 | 2 | num_channels | Number of channels (1-32) |
| 70 | 2 | num_patterns | Number of patterns |
| 72 | 2 | num_instruments | Number of instruments |
| 74 | 2 | flags | Bit 0: linear frequency table |
| 76 | 2 | default_speed | Default ticks per row |
| 78 | 2 | default_bpm | Default tempo |
| 80 | 256 | order_table | Pattern order (which patterns play in sequence) |

**Total header size:** 336 bytes (60 + 276)

## Pattern Data

Each pattern starts with a header followed by packed note data.

### Pattern Header (9 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0 | 4 | header_length | Header length **including this field** (standard: 9) |
| 4 | 1 | packing_type | Packing type (always 0) |
| 5 | 2 | num_rows | Number of rows (1-256) |
| 7 | 2 | packed_size | Size of packed pattern data |

**Important:** `header_length = 9` per XM spec, which includes the 4-byte length field itself:
`4 (length) + 1 (packing) + 2 (rows) + 2 (packed_size) = 9`

### Note Packing Format

Notes are packed to save space. Each cell can be 1-5 bytes.

**Flag byte format (if first byte >= 0x80):**
```
0x80 | flags
  Bit 0 (0x01): Note follows
  Bit 1 (0x02): Instrument follows
  Bit 2 (0x04): Volume follows
  Bit 3 (0x08): Effect follows
  Bit 4 (0x10): Effect param follows
```

**Examples:**
- `0x80` alone = empty note (1 byte)
- `0x83 31 01` = note C-4 + instrument 1 (3 bytes)
- `0x9F 31 01 40 0F 06` = all fields present (6 bytes)

**Unpacked format (if first byte < 0x80):**
- 5 consecutive bytes: note, instrument, volume, effect, effect_param

### Note Values

| Value | Meaning |
|-------|---------|
| 0 | No note |
| 1-96 | C-0 to B-7 (note = octave*12 + semitone + 1) |
| 97 | Note off |

### Volume Column

| Value | Meaning |
|-------|---------|
| 0 | No volume command |
| 0x10-0x50 | Set volume (0-64) |
| 0x60-0x6F | Volume slide down |
| 0x70-0x7F | Volume slide up |
| 0xC0-0xCF | Set panning |
| 0xF0-0xFF | Tone portamento |

## Instrument Data

### Instrument Header

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0 | 4 | header_size | Instrument header size |
| 4 | 22 | name | Instrument name (maps to ROM sample ID) |
| 26 | 1 | type | Instrument type (always 0) |
| 27 | 2 | num_samples | Number of samples |

If num_samples > 0, additional fields follow:

| Offset | Size | Field |
|--------|------|-------|
| 29 | 4 | sample_header_size | Sample header size (40) |
| 33 | 96 | note_samples | Sample number for each note |
| 129 | 48 | vol_envelope | Volume envelope (12 points * 4 bytes) |
| 177 | 48 | pan_envelope | Panning envelope |
| 225 | 1 | num_vol_points | Number of volume envelope points |
| 226 | 1 | num_pan_points | Number of panning envelope points |
| 227 | 1 | vol_sustain | Volume sustain point |
| 228 | 1 | vol_loop_start | Volume loop start |
| 229 | 1 | vol_loop_end | Volume loop end |
| 230 | 1 | pan_sustain | Panning sustain point |
| 231 | 1 | pan_loop_start | Panning loop start |
| 232 | 1 | pan_loop_end | Panning loop end |
| 233 | 1 | vol_type | Volume flags (bit 0=on, 1=sustain, 2=loop) |
| 234 | 1 | pan_type | Panning flags |
| 235 | 1 | vibrato_type | 0=sine, 1=square, 2=ramp down, 3=ramp up |
| 236 | 1 | vibrato_sweep | Auto-vibrato sweep |
| 237 | 1 | vibrato_depth | Auto-vibrato depth |
| 238 | 1 | vibrato_rate | Auto-vibrato rate |
| 239 | 2 | fadeout | Volume fadeout (0-4095) |
| 241 | 2 | reserved | Reserved |

### Sample Header (40 bytes each)

| Offset | Size | Field | Description |
|--------|------|-------|
| 0 | 4 | length | Sample length in bytes (**0 for Nethercore**) |
| 4 | 4 | loop_start | Loop start position |
| 8 | 4 | loop_length | Loop length |
| 12 | 1 | volume | Default volume (0-64) |
| 13 | 1 | finetune | Finetune (-128 to 127, signed) |
| 14 | 1 | type | Loop type (bits 0-1: 0=none, 1=forward, 2=pingpong) |
| 15 | 1 | panning | Default panning (0-255) |
| 16 | 1 | relative_note | Relative note (semitones from C-4) |
| 17 | 1 | reserved | Reserved |
| 18 | 22 | name | Sample name |

## Nethercore Convention

Nethercore strips sample data during `nether pack`. The XM file contains:
- **sample_length = 0** (no embedded audio)
- **Instrument names** that map to `[[assets.sounds]]` IDs in nether.toml

At runtime, the player resolves instrument names to ROM samples.

## Hex Validation

Valid XM header bytes:
```
00: 45 78 74 65 6E 64 65 64 20 4D 6F 64 75 6C 65 3A 20  "Extended Module: "
11: [20 bytes module name]
25: 1A                                                  Marker
26: [20 bytes tracker name]
3A: 04 01                                              Version 0x0104
3C: 14 01 00 00                                        Header size 276
```
