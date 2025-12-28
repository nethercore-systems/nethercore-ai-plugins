---
name: Procedural Music Composition
description: This skill should be used when the user asks to "create music", "XM tracker", "compose", "soundtrack", "tracker module", "game music", "make a song", "music for my game", "create an XM file", "FastTracker", "MilkyTracker module", or mentions music composition, tracker patterns, XM effects, or game soundtrack creation. Provides comprehensive guidance for creating tracker-based music using XM modules for Nethercore ZX games.
version: 1.0.0
---

# Procedural Music Composition

## Overview

XM (Extended Module) tracker music enables creating complete game soundtracks in a fraction of the ROM space required by raw audio. A full song typically uses 10-50KB for patterns versus 7.9MB for an equivalent 3-minute PCM recording.

**Key advantages:**
- **Compact:** Pattern data only, samples shared with SFX
- **Dynamic:** Jump to sections, change tempo during gameplay
- **Era-authentic:** FastTracker 2 format (1994) matches ZX's 5th-gen aesthetic
- **Rollback-safe:** Deterministic playback from any position

## ZX Audio Constraints

| Constraint | Value |
|------------|-------|
| Sample rate | 22,050 Hz |
| Channels | Up to 32 (in XM module) |
| ROM budget | 16 MB total (shared with all assets) |
| Sample format | 16-bit mono WAV |
| Music channel | 1 dedicated looping channel |

**Typical music budget:**
- Pattern data: 60-150 KB for 3-5 songs
- Shared samples: 200-500 KB
- Total: ~300-650 KB for complete soundtrack

## XM Module Structure

An XM module contains:

```
XM Module
├── Header (metadata, tempo, speed)
├── Order Table (which patterns play in sequence)
├── Patterns (rows × channels of note data)
└── Instruments (envelope + sample mapping)
```

**Terminology:**
- **Pattern:** A grid of notes (typically 64 rows × N channels)
- **Order:** A sequence of pattern indices defining song structure
- **Row:** A horizontal slice across all channels (plays simultaneously)
- **Tick:** Subdivisions within a row (controlled by speed)
- **Speed:** Ticks per row (lower = faster)
- **Tempo/BPM:** Beats per minute

### Pattern Data Format

Each cell in a pattern contains:

| Field | Range | Purpose |
|-------|-------|---------|
| Note | C-0 to B-7, or note-off | Pitch to play |
| Instrument | 1-128 | Which sample/envelope |
| Volume | 0-64 | Volume level |
| Effect | 0-35 | Effect command |
| Effect Param | 00-FF | Effect parameter |

## ⚠️ IMPORTANT: Nethercore XM Format Difference

**Nethercore uses a MODIFIED XM format.** Unlike standard XM files which embed samples directly:

| Standard XM | Nethercore XM |
|-------------|---------------|
| Samples embedded in .xm file | Samples stripped from .xm |
| Large file sizes (MB) | Tiny pattern-only files (KB) |
| Self-contained | References ROM samples by name |

**How it works:**
1. XM instrument **names** map to ROM `[[assets.sounds]]` IDs
2. During `nether pack`, sample data is stripped from the XM
3. At runtime, the player resolves instrument names to ROM samples

This means:
- **Same samples can be shared** between music tracks AND sound effects
- **Much smaller ROM sizes** (no duplicate sample data)
- **Instrument names MUST match** your `[[assets.sounds]]` IDs exactly

## ⚠️ CRITICAL: Standard FastTracker 2 Format Required

**DO NOT create custom XM formats!** Your XM file MUST be 100% compatible with the FastTracker 2 specification (version 0x0104).

### Required Format Compliance

| Component | Requirement | No Custom Formats! |
|-----------|-------------|-------------------|
| Magic header | Exactly `"Extended Module: "` (17 bytes) | ❌ No variations |
| Version | `0x0104` (little-endian `04 01` bytes) | ❌ No custom versions |
| Header structure | Exact FastTracker 2 layout (276 bytes) | ❌ No simplified headers |
| Pattern data | Standard packed/unpacked note format | ❌ No custom encodings |
| Instrument headers | Standard 29+ or 243 byte structure | ❌ No custom sizes |
| Sample headers | Standard 40-byte structure | ❌ No modifications |

### The ONLY Acceptable Workflow

✅ **CORRECT:** Use MilkyTracker or OpenMPT to create XM files
✅ **CORRECT:** Export as "FastTracker 2 Module (.xm)"
✅ **CORRECT:** XM file opens in MilkyTracker/OpenMPT without errors
✅ **CORRECT:** All headers match the XM specification exactly

❌ **WRONG:** Writing custom binary XM from scratch
❌ **WRONG:** Creating "simplified" or "minimal" XM formats
❌ **WRONG:** Custom header sizes or structures
❌ **WRONG:** Non-standard magic bytes or version numbers

### Format Validation Checklist

Before using an XM file, verify it meets ALL these requirements:

1. **Opens in a tracker**: File must open successfully in MilkyTracker or OpenMPT
2. **Magic bytes**: First 17 bytes are `45 78 74 65 6E 64 65 64 20 4D 6F 64 75 6C 65 3A 20`
3. **Version bytes**: Bytes 58-59 are `04 01` (version 0x0104, little-endian)
4. **Header size**: Bytes 60-63 are typically `14 01 00 00` (276) or `10 01 00 00` (272), little-endian
5. **Parses correctly**: `nether_xm::parse_xm()` returns Ok without errors

### XM File Structure Reference

**Standard FastTracker 2 XM format:**

```
Offset   Size   Description
------   ----   -----------
0        17     Magic: "Extended Module: "
17       20     Module name (null-terminated)
37       1      0x1A marker
38       20     Tracker name
58       2      Version (0x0104 = bytes 04 01)
60       4      Header size (276 = bytes 14 01 00 00)
64       2      Song length (order table length)
66       2      Restart position
68       2      Number of channels (1-32)
70       2      Number of patterns
72       2      Number of instruments
74       2      Flags (bit 0: linear frequency table)
76       2      Default speed
78       2      Default BPM
80       256    Pattern order table
336+     ...    Pattern data (see pattern format below)
...      ...    Instrument headers + sample headers + sample data
```

**Pattern format:**
```
+0      4      Pattern header length (9)
+4      1      Packing type (0)
+5      2      Number of rows (typically 64)
+7      2      Packed pattern data size
+9      ...    Pattern data (packed or unpacked notes)
```

**Note format (unpacked - 5 bytes):**
```
Byte 0: Note (1-96 for C-0 to B-7, 97 for note-off, 0 for no note)
Byte 1: Instrument (1-128, 0 for none)
Byte 2: Volume (0-64, 0 for default)
Byte 3: Effect type (0-35)
Byte 4: Effect parameter (0-255)
```

**Note format (packed):** If first byte >= 0x80, it's packed format with flags indicating which fields follow.

### Official Specification

The canonical XM format specification:
https://github.com/milkytracker/MilkyTracker/blob/master/resources/reference/xm-form.txt

**When in doubt, consult the official spec!**

## Sample Integration with ROM

**Key concept:** XM instrument names map to ROM sample IDs.

In the XM tracker, name instruments to match `[[assets.sounds]]` IDs:
- Instrument named `"kick"` → resolves to `rom_sound("kick")`
- Instrument named `"bass_synth"` → resolves to `rom_sound("bass_synth")`

**Workflow:**

1. Generate samples using procedural-sounds skill (or record/import WAVs)
2. Add samples to ROM in `nether.toml`:
```toml
[[assets.sounds]]
id = "kick"
path = "samples/kick.wav"

[[assets.sounds]]
id = "snare"
path = "samples/snare.wav"

[[assets.sounds]]
id = "bass"
path = "samples/bass.wav"
```

3. Create XM module in tracker (MilkyTracker/OpenMPT)
4. **Name instruments EXACTLY as ROM sample IDs** (case-sensitive!)
5. Add tracker to manifest:
```toml
[[assets.trackers]]
id = "main_theme"
path = "music/main_theme.xm"
```

6. Pack and test: `nether pack && nether run`

**⚠️ Common Mistake:** If music plays but sounds wrong, check that instrument names in the XM match your `[[assets.sounds]]` IDs exactly.

## Essential Effects

XM provides 20+ effect commands. The most commonly used:

| Effect | Hex | Name | Usage |
|--------|-----|------|-------|
| Arpeggio | 0xy | Rapid note switching | Chiptune chords |
| Porta Up | 1xx | Slide pitch up | Rising synths |
| Porta Down | 2xx | Slide pitch down | Drops, dives |
| Tone Porta | 3xx | Glide to note | Smooth melodies |
| Vibrato | 4xy | Pitch wobble | Expression |
| Volume Slide | Axy | Fade in/out | Dynamics |
| Position Jump | Bxx | Jump to order | Song sections |
| Set Volume | Cxx | Immediate volume | Accents |
| Pattern Break | Dxx | Next pattern | Transitions |
| Set Speed/Tempo | Fxx | Speed (<32) or BPM | Tempo changes |

For complete effect reference, see `references/xm-effects.md`.

## Composition Patterns

### Basic Song Structure

```
Order Table: [0, 1, 1, 2, 1, 2, 3, 1]

Pattern 0: Intro (build-up)
Pattern 1: Main (verse/loop)
Pattern 2: Variation (chorus/intensity)
Pattern 3: Breakdown (tension release)
```

Use order table repeats to extend song length without duplicating patterns.

### Channel Roles

| Channel(s) | Role | Typical Instruments |
|------------|------|---------------------|
| 1 | Drums - Kick | Low, punchy |
| 2 | Drums - Snare | Mid, snappy |
| 3 | Drums - Hi-hat | High, short |
| 4 | Bass | Low synth/guitar |
| 5-6 | Lead melody | Main theme |
| 7-8 | Pads/harmony | Sustained chords |

### Loop Point Design

For seamless looping:
1. Ensure first and last patterns have matching elements
2. Use volume slides at loop boundary to prevent clicks
3. Set restart position in XM header to skip intro
4. Test loop transitions extensively

For detailed composition patterns and genre templates, see `references/composition-patterns.md`.

## Tracker Workflow

### Recommended Tools

| Tool | Platform | Best For |
|------|----------|----------|
| MilkyTracker | Cross-platform | Authentic XM editing |
| OpenMPT | Windows | Advanced features, effects |
| Renoise | Cross-platform | Modern workflow, XM export |

### Quick Start

1. **Create samples** using procedural-sounds skill or import WAVs
2. **Open tracker** and create new XM module
3. **Import samples** and name instruments to match ROM IDs
4. **Set tempo** (typically 120-150 BPM for action, 80-100 for ambient)
5. **Compose patterns** for intro, main, variation, breakdown
6. **Arrange order table** to create full song structure
7. **Export XM** (samples will be stripped during pack)

For step-by-step workflow details, see `references/workflow-guide.md`.

## Game Integration

### Loading and Playing

```rust
// In init()
let music = rom_tracker(b"main_theme".as_ptr(), 11);

// Start playback (looping)
music_play(music, 0.8, 1);  // handle, volume, loop
```

### Dynamic Music Control

```rust
// Jump to pattern order (e.g., boss phase)
music_jump(5, 0);  // order 5, row 0

// Check position for sync
let pos = music_position();
let order = (pos >> 16) as u32;
let row = (pos & 0xFFFF) as u32;

// Adjust during gameplay
music_set_tempo(140);  // Speed up for action
music_set_volume(0.5); // Duck for dialogue
```

### Runtime FFI Functions

| Function | Purpose |
|----------|---------|
| `rom_tracker(id, len)` | Load from ROM |
| `music_play(h, vol, loop)` | Start playback |
| `music_stop()` | Stop playback |
| `music_pause(paused)` | Pause/resume |
| `music_set_volume(vol)` | Adjust volume |
| `music_jump(order, row)` | Seek position |
| `music_position()` | Get current position |
| `music_set_tempo(bpm)` | Change tempo |
| `music_set_speed(ticks)` | Change speed |

## Sample Creation Integration

Use the procedural-sounds skill to generate instrument samples:

```rust
use proc_gen::audio::*;

// Generate bass sample
let bass = synth.tone(Waveform::Saw, 110.0, 0.5, Envelope::pluck());
low_pass(&mut bass, 800.0, SAMPLE_RATE);
write_wav(&to_pcm_i16(&bass), SAMPLE_RATE, "samples/bass.wav");

// Generate kick
let kick = synth.coin();  // Or custom design
write_wav(&to_pcm_i16(&kick), SAMPLE_RATE, "samples/kick.wav");
```

The procedural-sounds skill provides complete synthesis guidance.

## Music Theory

For deep music theory knowledge, consult the **`sound-design`** plugin's music composition skill:

**`sound-design/skills/music-composition/SKILL.md`** covers:

- **Scales and Modes** - Lydian (dreamy), Dorian (mysterious), Phrygian (combat), and when to use each
- **Chord Progressions** - By emotion (triumphant, tense, mysterious, melancholic, peaceful)
- **Tempo Guidelines** - BPM ranges for menu, exploration, combat, boss, stealth
- **Song Structures** - Loop-based, layered (adaptive), and linear (cutscenes)
- **Looping Techniques** - Seamless loops, crossfades, harmonic resolution
- **Adaptive Music** - Vertical layering, horizontal resequencing, stinger systems
- **Leitmotifs** - Creating memorable themes for characters and places
- **Genre Patterns** - Orchestral, electronic, chiptune, ambient

This skill (procedural-music) focuses on **XM tracker format and ZX integration**. For composition theory, use the sound-design plugin.

---

## CRITICAL: Code Organization & File Size Limits

**When generating sample synthesis code (not XM files themselves), follow these limits:**

| Limit | Lines | Action |
|-------|-------|--------|
| Target | ≤300 | Ideal file size |
| Soft limit | 400 | Consider splitting |
| Hard limit | 500 | MUST split immediately |
| Unacceptable | >500 | Never generate |

### Module Structure for Sample Generation

```
generator/src/
├── main.rs              # Entry point only (~50 lines)
├── lib.rs               # Module exports (~30 lines)
├── samples/
│   ├── mod.rs           # Re-exports (~20 lines)
│   ├── drums.rs         # Kick, snare, hats (~150 lines)
│   ├── bass.rs          # Bass instruments (~100 lines)
│   ├── leads.rs         # Lead/melody (~100 lines)
│   └── pads.rs          # Pads/ambient (~80 lines)
└── constants.rs         # Note frequencies, patterns (~50 lines)
```

### XM Files Are Already Compact

XM pattern data is inherently small (patterns are ~64 rows × channels). The concern is **sample generation code**, not the XM files themselves. Keep sample generators modular and each instrument generator under 100 lines.

---

## Additional Resources

### Reference Files

For detailed information, consult:
- **`references/xm-effects.md`** - Complete effect command reference
- **`references/composition-patterns.md`** - Genre templates and song structures
- **`references/workflow-guide.md`** - Step-by-step tracker workflow

### Related Skills

- **`sound-design/skills/music-composition`** - Music theory, chord progressions, adaptive music
- **`sound-design/skills/synthesis-techniques`** - FM, wavetable, granular synthesis
- **`procedural-sounds`** - Generating instrument samples procedurally

### External Resources

- [MilkyTracker](https://milkytracker.org/) - Cross-platform XM tracker
- [OpenMPT](https://openmpt.org/) - Windows tracker with XM export
- [XM Format Spec](https://github.com/milkytracker/MilkyTracker/wiki/XM-file-format) - Technical reference
