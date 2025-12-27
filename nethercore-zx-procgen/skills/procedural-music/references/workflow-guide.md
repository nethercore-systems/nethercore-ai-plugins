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
