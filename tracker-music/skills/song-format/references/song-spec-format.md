# Song Spec Format Reference

Complete specification for song `.spec.py` files used by the unified generator.

## File Format

Song specs are Python files containing a single `SONG` dict. All spec files use the `.spec.py` extension - the folder and dict name identify the type:

```python
# .studio/specs/music/example.spec.py
SONG = {
    "song": {
        # ... specification fields
    }
}
```

The parser loads this via `exec()` and extracts the `SONG` dict.

## Top-Level Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | str | `"Untitled"` | Internal identifier |
| `title` | str | (uses `name`) | Display name embedded in module |
| `format` | str | `"xm"` | Output format: `"xm"` or `"it"` |
| `bpm` | int | `125` | Beats per minute |
| `speed` | int | `6` | Ticks per row |
| `rows_per_beat` | int | `4` | Rows per beat (for calculation) |
| `rows_per_pattern` | int | `64` | Default pattern length |
| `channels` | int | `8` | Number of channels |
| `instruments` | list | `[]` | Instrument definitions |
| `patterns` | dict | `{}` | Named pattern definitions |
| `arrangement` | list | `[]` | Pattern playback order |
| `restart_position` | int | `0` | Loop point (order index) |
| `automation` | list | `[]` | Procedural effects |
| `channel_names` | dict | `{}` | Optional channel labels |
| `it_options` | dict | `{}` | IT-specific settings |

## Instruments

Instruments can be defined in three ways:

### 1. External Reference

Reference an instrument spec file:

```python
{"ref": "../instruments/kick.spec.py"}
```

Path is relative to the song spec file's directory.

### 2. Inline Synthesis

Full synthesis specification inline:

```python
{
    "name": "bass",
    "synthesis": {
        "type": "karplus_strong",
        "damping": 0.994,
        "brightness": 0.5
    },
    "envelope": {
        "attack": 0.01,
        "decay": 0.4,
        "sustain": 0.3,
        "release": 0.3
    },
    "base_note": "C2",
    "sample_rate": 22050,
    "output": {
        "duration": 1.5,
        "loop": true
    }
}
```

See `sound-spec-format.md` for full INSTRUMENT spec.

### 3. WAV File

Load pre-recorded sample:

```python
{"wav": "samples/piano_c4.wav", "name": "piano"}
```

WAV must be 16-bit PCM, mono or stereo.

## Patterns

Patterns are named collections of rows containing notes:

```python
"patterns": {
    "intro": {
        "rows": 64,
        "notes": {
            0: [...],  # Channel 0 notes
            1: [...],  # Channel 1 notes
        }
    },
    "verse": {...},
    "chorus": {...}
}
```

### Pattern Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `rows` | int | `64` | Number of rows in pattern |
| `notes` | dict | `{}` | Channel -> note list mapping |

### Note Specification

Each note in the `notes` arrays:

```python
{
    "row": 0,           # Required: Row position (0-based)
    "note": "C-4",      # Note name or MIDI number
    "inst": 0,          # Instrument index (0-based)
    "vol": 64,          # Volume (0-64)
    "effect": 0x0,      # Effect command (hex)
    "param": 0x00       # Effect parameter (hex)
}
```

### Note Values

| Format | Examples | Description |
|--------|----------|-------------|
| Standard | `"C-4"`, `"F#3"`, `"Bb5"` | Note with octave |
| No separator | `"C4"`, `"F#3"` | Also valid |
| MIDI number | `60` | Middle C |
| No note | `"---"`, `""`, `None` | Row without note |
| Note off | `"==="`, `"OFF"` | Stop playing |
| Note cut | `"^^^"`, `"CUT"` | IT only: immediate cut |
| Note fade | `"~~~"`, `"FADE"` | IT only: fade out |

### Effects

Effects can be specified numerically or by name:

**Numeric (raw hex):**
```python
{"row": 0, "note": "C-4", "effect": 0x4, "param": 0x34}  # Vibrato
```

**Named effect:**
```python
{"row": 0, "note": "C-4", "effect_name": "vibrato", "effect_xy": [3, 4]}
```

### XM Effect Names

| Name | Hex | Description |
|------|-----|-------------|
| `arpeggio` | 0x0 | Arpeggio |
| `porta_up` | 0x1 | Portamento up |
| `porta_down` | 0x2 | Portamento down |
| `tone_porta` | 0x3 | Tone portamento |
| `vibrato` | 0x4 | Vibrato |
| `vol_slide` | 0xA | Volume slide |
| `position_jump` | 0xB | Position jump |
| `set_volume` | 0xC | Set volume |
| `pattern_break` | 0xD | Pattern break |
| `speed_tempo` | 0xF | Set speed/tempo |

### IT Effect Names

| Name | Letter | Description |
|------|--------|-------------|
| `set_speed` | A | Set speed |
| `position_jump` | B | Position jump |
| `pattern_break` | C | Pattern break |
| `vol_slide` | D | Volume slide |
| `porta_down` | E | Portamento down |
| `porta_up` | F | Portamento up |
| `tone_porta` | G | Tone portamento |
| `vibrato` | H | Vibrato |
| `arpeggio` | J | Arpeggio |
| `tempo` | T | Set tempo |

## Arrangement

Specifies the order patterns are played:

```python
"arrangement": [
    {"pattern": "intro"},
    {"pattern": "verse", "repeat": 2},
    {"pattern": "chorus"},
    {"pattern": "verse", "repeat": 2},
    {"pattern": "chorus"},
    {"pattern": "outro"}
]
```

### Arrangement Entry Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `pattern` | str | required | Pattern name |
| `repeat` | int | `1` | Times to repeat |

### Loop Point

`restart_position` specifies where the song loops back to:

```python
"restart_position": 1  # Skip intro (index 0) on loop
```

## Automation

Procedural effects applied during generation:

### Volume Fade

Gradual volume change over rows:

```python
{
    "type": "volume_fade",
    "pattern": "intro",
    "channel": 0,
    "start_row": 0,
    "end_row": 32,
    "start_vol": 0,
    "end_vol": 64
}
```

### Tempo Change

Change BPM at a specific point:

```python
{
    "type": "tempo_change",
    "pattern": "chorus",
    "row": 0,
    "bpm": 150
}
```

## IT-Specific Options

```python
"it_options": {
    "stereo": true,           # Stereo output
    "global_volume": 128,     # Global volume (0-128)
    "mix_volume": 48          # Mixing volume
}
```

## Channel Names

Optional labels for documentation:

```python
"channel_names": {
    0: "kick",
    1: "snare",
    2: "hihat",
    3: "bass",
    4: "lead",
    5: "pad"
}
```

## Complete Example

```python
SONG = {
    "song": {
        "name": "boss_battle",
        "title": "Dark Lord Battle",
        "format": "xm",
        "bpm": 155,
        "speed": 4,
        "channels": 8,

        "channel_names": {
            0: "kick",
            1: "snare",
            2: "hihat",
            3: "bass",
            4: "lead",
            5: "counter",
            6: "pad",
            7: "fx"
        },

        "instruments": [
            {"ref": "instruments/kick.spec.py"},
            {"ref": "instruments/snare.spec.py"},
            {"ref": "instruments/hihat.spec.py"},
            {"ref": "instruments/bass.spec.py"},
            {"ref": "instruments/lead.spec.py"},
            {"ref": "instruments/counter.spec.py"},
            {"ref": "instruments/pad.spec.py"},
            {"ref": "instruments/fx.spec.py"}
        ],

        "patterns": {
            "intro": {
                "rows": 64,
                "notes": {
                    0: [
                        {"row": 0, "note": "C-3", "inst": 0, "vol": 40},
                        {"row": 32, "note": "C-3", "inst": 0, "vol": 56}
                    ],
                    6: [
                        {"row": 0, "note": "D-2", "inst": 6, "vol": 20}
                    ]
                }
            },
            "main": {
                "rows": 64,
                "notes": {
                    0: [
                        {"row": 0, "note": "C-3", "inst": 0, "vol": 64},
                        {"row": 16, "note": "C-3", "inst": 0, "vol": 64},
                        {"row": 32, "note": "C-3", "inst": 0, "vol": 64},
                        {"row": 48, "note": "C-3", "inst": 0, "vol": 64}
                    ],
                    1: [
                        {"row": 8, "note": "D-3", "inst": 1, "vol": 64},
                        {"row": 24, "note": "D-3", "inst": 1, "vol": 56},
                        {"row": 40, "note": "D-3", "inst": 1, "vol": 64},
                        {"row": 56, "note": "D-3", "inst": 1, "vol": 56}
                    ],
                    3: [
                        {"row": 0, "note": "D-1", "inst": 3, "vol": 64},
                        {"row": 16, "note": "D#1", "inst": 3, "vol": 64},
                        {"row": 32, "note": "E-1", "inst": 3, "vol": 64},
                        {"row": 48, "note": "D-1", "inst": 3, "vol": 64}
                    ],
                    4: [
                        {"row": 0, "note": "D-4", "inst": 4, "vol": 56},
                        {"row": 16, "note": "F-4", "inst": 4, "vol": 56},
                        {"row": 32, "note": "A-4", "inst": 4, "vol": 64}
                    ]
                }
            },
            "breakdown": {
                "rows": 64,
                "notes": {
                    0: [
                        {"row": 0, "note": "C-3", "inst": 0, "vol": 64},
                        {"row": 48, "note": "C-3", "inst": 0, "vol": 48}
                    ],
                    6: [
                        {"row": 0, "note": "D-2", "inst": 6, "vol": 48}
                    ]
                }
            }
        },

        "arrangement": [
            {"pattern": "intro"},
            {"pattern": "main", "repeat": 2},
            {"pattern": "breakdown"},
            {"pattern": "main", "repeat": 2}
        ],

        "restart_position": 1,

        "automation": [
            {
                "type": "volume_fade",
                "pattern": "intro",
                "channel": 6,
                "start_row": 0,
                "end_row": 48,
                "start_vol": 0,
                "end_vol": 48
            }
        ]
    }
}
```

## Generator CLI

```bash
python .studio/generate.py --only music
```

## Integration with Build System

In `nether.toml`:

```toml
[build]
script = "python .studio/generate.py && cargo build -p game --target wasm32-unknown-unknown --release"

[[assets.sounds]]
id = "boss_theme"
path = "../generated/music/boss_theme.xm"
```

## Validation

The parser validates:

- All patterns referenced in arrangement exist
- Instrument indices are within bounds
- Row numbers are within pattern rows
- Note formats are valid
- Paths to referenced instruments exist

Errors are reported with file and context information.
