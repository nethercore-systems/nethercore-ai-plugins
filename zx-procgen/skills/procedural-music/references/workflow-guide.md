# Tracker Workflow Guide

Step-by-step workflow for creating XM music for Nethercore ZX games.

## Tool Setup

### MilkyTracker (Recommended for Authenticity)

1. Download from [milkytracker.org](https://milkytracker.org/)
2. Launch and create new XM module (Ctrl+N)
3. Set channels: Config → Number of channels (typically 4-8)
4. Set default tempo: 125 BPM, Speed 6

### OpenMPT (Recommended for Windows)

1. Download from [openmpt.org](https://openmpt.org/)
2. Create new XM module (File → New → FastTracker 2 Module)
3. Configure channels in Pattern Editor
4. Set tempo in General tab

## Sample Preparation

### Using Procedural Sounds

Generate samples with the proc-gen audio library:

```rust
use proc_gen::audio::*;

fn generate_music_samples() {
    let synth = Synth::new(22050);

    // Kick drum
    let kick = synth.sweep(Waveform::Sine, 150.0, 40.0, 0.2, Envelope::hit());
    write_wav(&to_pcm_i16(&kick), 22050, "samples/kick.wav").unwrap();

    // Snare
    let mut snare = synth.noise_burst(0.15, Envelope::hit());
    high_pass(&mut snare, 200.0, 22050);
    write_wav(&to_pcm_i16(&snare), 22050, "samples/snare.wav").unwrap();

    // Hi-hat
    let mut hihat = synth.noise_burst(0.05, Envelope::click());
    high_pass(&mut hihat, 6000.0, 22050);
    write_wav(&to_pcm_i16(&hihat), 22050, "samples/hihat.wav").unwrap();

    // Bass
    let bass = synth.tone(Waveform::Saw, 110.0, 0.3, Envelope::pluck());
    low_pass(&mut bass, 800.0, 22050);
    write_wav(&to_pcm_i16(&bass), 22050, "samples/bass.wav").unwrap();

    // Lead synth
    let lead = synth.tone(Waveform::Square, 440.0, 0.4, Envelope::pad());
    write_wav(&to_pcm_i16(&lead), 22050, "samples/lead.wav").unwrap();
}
```

### Sample Requirements

- **Format:** 16-bit mono WAV
- **Sample rate:** 22,050 Hz (ZX standard)
- **Duration:** As short as practical (save ROM space)
- **Naming:** Match ROM asset IDs exactly

## Tracker Workflow

### 1. Import Samples

**MilkyTracker:**
1. Press Ins to go to Instrument Editor
2. Click "Load" and select WAV files
3. Name each instrument to match ROM ID (e.g., "kick", "snare")

**OpenMPT:**
1. Go to Samples tab
2. Right-click → Load Sample
3. Name samples to match ROM IDs

### 2. Configure Instruments

For each instrument:
- Set volume envelope (or disable for SFX-style)
- Set default volume (40-64)
- Set base note (C-4 typically)
- Set loop points if sample should sustain

### 3. Create Patterns

**Pattern structure:**
```
64 rows × N channels (typical)

Row 0:  Beat 1
Row 16: Beat 2
Row 32: Beat 3
Row 48: Beat 4
```

**Navigation:**
- Arrow keys: Move cursor
- Tab: Next channel
- Space: Play from cursor
- Enter: Play pattern

**Entering notes:**
- QWERTY keyboard maps to piano
- Z = C-4, X = D-4, C = E-4, etc.
- Q = C-5, W = D-5, E = E-5, etc.

### 4. Arrange Order Table

**MilkyTracker:**
- Use Ord (Order List) section
- Add patterns in desired sequence
- Set song length and restart position

**OpenMPT:**
- Use General tab → Order List
- Drag patterns to reorder
- Set restart position for loops

### 5. Add Effects

Common effect usage:
```
C-4 01 40 ---  ; Note, instrument, volume, no effect
C-4 01 -- 1FF  ; Portamento up (slide pitch)
--- -- -- A04  ; Volume slide up (no new note)
--- -- -- F80  ; Set tempo to 128 BPM
```

### 6. Export XM

**MilkyTracker:**
- File → Save Module (Ctrl+S)
- Ensure .xm extension

**OpenMPT:**
- File → Save As → FastTracker 2 Module (.xm)

## Nethercore Integration

### nether.toml Configuration

```toml
[game]
id = "my-game"
title = "My Game"

# Declare samples (shared between SFX and music)
[[assets.sounds]]
id = "kick"
path = "samples/kick.wav"

[[assets.sounds]]
id = "snare"
path = "samples/snare.wav"

[[assets.sounds]]
id = "hihat"
path = "samples/hihat.wav"

[[assets.sounds]]
id = "bass"
path = "samples/bass.wav"

[[assets.sounds]]
id = "lead"
path = "samples/lead.wav"

# Declare tracker modules
[[assets.trackers]]
id = "main_theme"
path = "music/main_theme.xm"

[[assets.trackers]]
id = "boss_battle"
path = "music/boss.xm"
```

### Build and Test

```bash
# Pack assets and build
nether build

# Run and test
nether run
```

### In-Game Usage

```rust
#[no_mangle]
pub extern "C" fn init() {
    // Load sounds (required for tracker sample mapping)
    rom_sound(b"kick".as_ptr(), 4);
    rom_sound(b"snare".as_ptr(), 5);
    rom_sound(b"hihat".as_ptr(), 5);
    rom_sound(b"bass".as_ptr(), 4);
    rom_sound(b"lead".as_ptr(), 4);

    // Load and play tracker
    let music = rom_tracker(b"main_theme".as_ptr(), 10);
    music_play(music, 0.8, 1);  // 80% volume, looping
}
```

## Troubleshooting

### No Sound Playing
1. Check samples are loaded before tracker
2. Verify instrument names match ROM sound IDs exactly
3. Check music volume is non-zero

### Clicks/Pops at Loop Point
1. Add volume fades at pattern end
2. Ensure notes don't cut abruptly
3. Check for hanging notes across loop

### Wrong Pitch
1. Verify sample base note setting
2. Check finetune values
3. Ensure sample rate is 22,050 Hz

### ROM Size Too Large
1. Reduce sample lengths
2. Share samples between tracks
3. Use shorter loop regions in samples
4. Consider fewer channels

## XM Format Validation

**CRITICAL:** Always verify your XM files are standard FastTracker 2 format before using them.

### Validation Command (Unix/macOS/Git Bash)

```bash
# View first 80 bytes of XM file in hex
xxd -l 80 your_song.xm | head -5
```

**Expected output (first line MUST show):**
```
00000000: 4578 7465 6e64 6564 204d 6f64 756c 653a  Extended Module:
```

### Validation Command (Windows PowerShell)

```powershell
# View first 80 bytes in hex
Format-Hex your_song.xm -Count 80 | Select-Object -First 10
```

### Manual Hex Validation

**First 80 bytes of a valid XM file:**

```
Offset(h) 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F

00000000  45 78 74 65 6E 64 65 64 20 4D 6F 64 75 6C 65 3A  Extended Module:
00000010  20 4D 79 20 53 6F 6E 67 00 00 00 00 00 00 00 00   My Song........
00000020  00 00 00 00 00 1A 4D 69 6C 6B 79 54 72 61 63 6B  ......MilkyTrack
00000030  65 72 20 31 2E 30 34 00 00 00 00 00 00 00 04 01  er 1.04.........
00000040  14 01 00 00 05 00 00 00 02 00 08 00 01 00 00 00  ................
```

**Key validation points:**

1. **Bytes 0-16:** `45 78 74 65 6E 64 65 64 20 4D 6F 64 75 6C 65 3A 20`
   - ASCII: `"Extended Module: "`
   - If this doesn't match, the file is NOT a valid XM

2. **Bytes 17-36:** Module name (20 bytes, null-padded)
   - Example: `" My Song\0\0\0..."`

3. **Byte 37:** `1A` (hex marker)

4. **Bytes 38-57:** Tracker name (20 bytes)
   - Example: `"MilkyTracker 1.04\0\0..."`

5. **Bytes 58-59:** Version `04 01` (0x0104 little-endian)
   - If this is anything else, the file won't parse

6. **Bytes 60-63:** Header size (typically `14 01 00 00` = 276 or `10 01 00 00` = 272 bytes, little-endian)

### Tracker Validation

**The definitive validation:**

1. Open the XM file in MilkyTracker or OpenMPT
2. If it opens and plays correctly → Valid FastTracker 2 format ✅
3. If it fails to open or shows errors → Invalid format ❌

**Download MilkyTracker:** https://milkytracker.org/

### Common Invalid Formats

❌ **Custom magic bytes**
```
00000000: 4E 43 5A 58 4D 75 73 69 63 00 00 00 00 00 00 00  NCZXMusic.......
```
This is NOT a valid XM file!

❌ **Wrong version**
```
00000000: ... (correct magic) ...
0000003A: 01 00  # Version 0x0001 instead of 0x0104
```
This will be rejected by the parser!

❌ **Custom header size**
```
00000000: ... (correct magic) ...
0000003C: 20 00 00 00  # Header size 32 instead of 276
```
This will cause parsing errors!

### Validation Checklist

Before using an XM file in your game, verify:

- [ ] Opens in MilkyTracker or OpenMPT without errors
- [ ] First 17 bytes are `Extended Module: ` (use hex viewer)
- [ ] Bytes 58-59 are `04 01` (version 0x0104)
- [ ] Bytes 60-63 are `14 01 00 00` (header size 276)
- [ ] Instrument names match your `[[assets.sounds]]` IDs exactly
- [ ] File extension is `.xm`

**If ANY of these fail, the XM file is invalid and must be recreated!**
