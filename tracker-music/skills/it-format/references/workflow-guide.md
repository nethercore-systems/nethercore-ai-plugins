# IT Writer Workflow Guide

Practical examples for common IT generation patterns.

## Table of Contents

1. [Basic Drum Pattern](#basic-drum-pattern)
2. [Envelopes](#envelopes)
3. [NNA (New Note Actions)](#nna-new-note-actions)
4. [Multi-Sample Instruments](#multi-sample-instruments)
5. [Filters](#filters)
6. [Song Structure](#song-structure)

## Basic Drum Pattern

```python
from it_writer import *

# Generate samples (use procedural-sounds skill!)
kick_audio = generate_kick()    # Returns bytes (16-bit signed PCM)
snare_audio = generate_snare()
hihat_audio = generate_hihat()

# Create module
module = ItModule(
    name="Drum Loop",
    num_channels=4,
    default_speed=6,
    default_bpm=140
)

# Add instruments and samples
kick_sample = ItSample(name="kick", c5_speed=22050, default_volume=64)
module.samples.append(kick_sample)
module.sample_data.append(kick_audio)
module.instruments.append(ItInstrument(name="kick"))

snare_sample = ItSample(name="snare", c5_speed=22050, default_volume=60)
module.samples.append(snare_sample)
module.sample_data.append(snare_audio)
module.instruments.append(ItInstrument(name="snare"))

hihat_sample = ItSample(name="hihat", c5_speed=22050, default_volume=48)
module.samples.append(hihat_sample)
module.sample_data.append(hihat_audio)
module.instruments.append(ItInstrument(name="hihat"))

# Create pattern (64 rows, 4 channels)
pattern = ItPattern.empty(64, 4)

# Kick on 1, 3 (rows 0, 32)
for row in [0, 32]:
    pattern.set_note(row, 0, ItNote.play("C-4", 1, 64))

# Snare on 2, 4 (rows 16, 48)
for row in [16, 48]:
    pattern.set_note(row, 1, ItNote.play("C-4", 2, 60))

# Hi-hat 16ths
for row in range(0, 64, 4):
    vol = 48 if row % 8 == 0 else 32  # Accent every 8th row
    pattern.set_note(row, 2, ItNote.play("C-4", 3, vol))

module.patterns.append(pattern)
module.order_table = [0]

# Write
write_it(module, "drums.it")
```

## Envelopes

### Volume Envelope (ADSR)

```python
def create_adsr_envelope(attack=10, decay=20, sustain_level=48, release=30):
    """Create classic ADSR envelope."""
    env = ItEnvelope()

    env.points = [
        (0, 0),                     # Start at 0
        (attack, 64),               # Attack to peak
        (attack + decay, sustain_level),  # Decay to sustain
        (100, sustain_level),       # Hold sustain (will loop here)
        (100 + release, 0),         # Release to 0
    ]

    # Loop during sustain
    env.loop_begin = 2
    env.loop_end = 3

    # Sustain point (holds until note-off)
    env.sustain_begin = 3
    env.sustain_end = 3

    env.flags = ENV_ENABLED | ENV_LOOP | ENV_SUSTAIN_LOOP

    return env

# Use in instrument
instr = ItInstrument(
    name="Pad",
    volume_envelope=create_adsr_envelope(attack=20, decay=30, sustain_level=52, release=50)
)
```

### Panning Envelope (Auto-Pan)

```python
def create_autopan_envelope(speed=10, width=32):
    """Create auto-panning envelope."""
    env = ItEnvelope()

    # Oscillate between left and right
    # Values: 0=left, 32=center, 64=right
    center = 32
    left = max(0, center - width)
    right = min(64, center + width)

    env.points = [
        (0, center),
        (speed, right),
        (speed * 2, center),
        (speed * 3, left),
        (speed * 4, center),
    ]

    # Loop the whole pattern
    env.loop_begin = 0
    env.loop_end = 4

    env.flags = ENV_ENABLED | ENV_LOOP

    return env

instr = ItInstrument(
    name="Pan Synth",
    panning_envelope=create_autopan_envelope(speed=12, width=28)
)
```

### Pitch Envelope (Pitch Bend)

IT-only feature! Modulates pitch ±32 semitones.

```python
def create_pitch_bend_envelope(bend_amount=12, bend_time=20):
    """Create pitch bend down effect."""
    env = ItEnvelope()

    # Start high, slide down to normal pitch
    # Values: -32 to +32 semitones
    env.points = [
        (0, bend_amount),   # Start bent up
        (bend_time, 0),     # Slide to normal pitch
    ]

    env.flags = ENV_ENABLED

    return env

# Kick drum with pitch bend
kick_instr = ItInstrument(
    name="Kick",
    pitch_envelope=create_pitch_bend_envelope(bend_amount=24, bend_time=15)
)
```

### Filter Envelope (Sweep)

IT-only feature! Modulates filter cutoff over time.

```python
def create_filter_sweep(start=127, end=32, sweep_time=40):
    """Create filter cutoff sweep."""
    env = ItEnvelope()

    # Sweep from bright to dark
    # Values: 0-64 (maps to IT's 0-127 internally)
    env.points = [
        (0, start // 2),      # Start bright
        (sweep_time, end // 2),  # Sweep to dark
    ]

    env.flags = ENV_ENABLED | ENV_FILTER

    return env

# Synth bass with filter sweep
bass_instr = ItInstrument(
    name="Bass",
    filter_cutoff=127,      # Initial cutoff
    filter_resonance=32,    # Resonance amount
    filter_envelope=create_filter_sweep(127, 24, 50)
)
```

## NNA (New Note Actions)

NNA controls what happens when a new note is played while the previous note is still sounding.

### NNA_CUT (Default)

Previous note is immediately cut when new note plays.

```python
instr = ItInstrument(
    name="Lead",
    nna=NNA_CUT,     # Cut previous note
    dct=DCT_OFF,     # Don't check for duplicates
    dca=DCA_CUT      # How to handle duplicates (unused here)
)
```

**Use for:** Monophonic leads, bass, most instruments

### NNA_FADE (Polyphonic)

Previous note fades out in background when new note plays. Creates polyphonic effect.

```python
def create_polyphonic_piano():
    instr = ItInstrument(
        name="Piano",
        nna=NNA_FADE,         # Fade previous note
        dct=DCT_NOTE,         # Check for duplicate notes
        dca=DCA_FADE,         # Fade duplicate notes
        fadeout=512,          # Fade speed (0-1024, higher = faster)
        volume_envelope=create_adsr_envelope(attack=5, decay=20, sustain_level=48, release=40)
    )
    return instr

# Play chords
pattern = ItPattern.empty(64, 4)
piano = 1

# C major chord - all notes sustain together!
pattern.set_note(0, 0, ItNote.play("C-4", piano, 64))
pattern.set_note(0, 1, ItNote.play("E-4", piano, 64))
pattern.set_note(0, 2, ItNote.play("G-4", piano, 64))

# Notes released at different times
pattern.set_note(32, 0, ItNote.off())   # Release C
pattern.set_note(48, 1, ItNote.off())   # Release E
pattern.set_note(64, 2, ItNote.off())   # Release G
```

**Use for:** Piano, pads, strings, any polyphonic instrument

### NNA_CONTINUE (Sustain Background)

Previous note continues playing at full volume in background.

```python
instr = ItInstrument(
    name="Drone",
    nna=NNA_CONTINUE,    # Continue previous note
    dct=DCT_OFF,         # No duplicate checking
    fadeout=0            # No fadeout
)
```

**Use for:** Drones, ambient textures

## Multi-Sample Instruments

Map different samples to different note ranges.

```python
def create_multisampled_piano():
    # Generate samples for different ranges
    low_audio = generate_piano_sample(note='C-2')   # Low sample
    mid_audio = generate_piano_sample(note='C-4')   # Mid sample
    high_audio = generate_piano_sample(note='C-6')  # High sample

    # Create samples
    low_sample = ItSample(name="piano_low", c5_speed=8363)
    mid_sample = ItSample(name="piano_mid", c5_speed=16726)
    high_sample = ItSample(name="piano_high", c5_speed=33452)

    # Create instrument with note mapping
    instr = ItInstrument(name="Piano")

    # Map notes to samples
    # Notes 0-39: Sample 1 (low)
    for note in range(0, 40):
        instr.note_sample_table[note] = (note, 1)

    # Notes 40-79: Sample 2 (mid)
    for note in range(40, 80):
        instr.note_sample_table[note] = (note, 2)

    # Notes 80-119: Sample 3 (high)
    for note in range(80, 120):
        instr.note_sample_table[note] = (note, 3)

    return instr, [low_sample, mid_sample, high_sample], [low_audio, mid_audio, high_audio]

# Usage
piano_instr, piano_samples, piano_audio = create_multisampled_piano()
module.instruments.append(piano_instr)
module.samples.extend(piano_samples)
module.sample_data.extend(piano_audio)
```

## Filters

IT supports resonant low-pass filters.

### Static Filter

```python
instr = ItInstrument(
    name="Filtered Bass",
    filter_cutoff=64,      # 0-127 (64 = ~1kHz)
    filter_resonance=32    # 0-127 (higher = more resonance)
)
```

### Dynamic Filter with Envelope

```python
# Create filter envelope (sweep from bright to dark)
filter_env = ItEnvelope()
filter_env.points = [
    (0, 64),    # Start at full cutoff
    (20, 32),   # Sweep to half
    (50, 16),   # Continue to dark
]
filter_env.flags = ENV_ENABLED | ENV_FILTER

instr = ItInstrument(
    name="Sweep Bass",
    filter_cutoff=127,
    filter_resonance=48,
    filter_envelope=filter_env
)
```

### Filter with Effect Command

```python
# Use Z effect to modulate filter in real-time
note = ItNote.play("C-3", bass_instr, 64)
    .with_effect(26, 0x80)  # Z80 - set filter cutoff
```

## Song Structure

### Intro - Verse - Chorus Pattern

```python
# Create sections
intro = create_intro_pattern()      # Pattern 0
verse = create_verse_pattern()      # Pattern 1
chorus = create_chorus_pattern()    # Pattern 2
bridge = create_bridge_pattern()    # Pattern 3
outro = create_outro_pattern()      # Pattern 4

module.patterns = [intro, verse, chorus, bridge, outro]

# Song structure via order table
module.order_table = [
    0,      # Intro
    1,      # Verse 1
    1,      # Verse 2
    2,      # Chorus 1
    1,      # Verse 3
    1,      # Verse 4
    2,      # Chorus 2
    2,      # Chorus 3 (repeat)
    3,      # Bridge
    2,      # Final chorus
    4,      # Outro
]
```

### Pattern Loops (Repeat Sections)

```python
# Use SBx effect for pattern loops
def create_looping_verse():
    pattern = ItPattern.empty(64, 4)

    # Set loop start
    pattern.set_note(0, 0, ItNote().with_effect(19, 0xB0))  # SB0

    # ... fill pattern with notes ...

    # Loop 4 times
    pattern.set_note(63, 0, ItNote().with_effect(19, 0xB4))  # SB4

    return pattern
```

### Smooth Transitions with Portamento

```python
def create_transition_pattern(from_note, to_note, speed=0x20):
    """Create smooth pitch transition between sections."""
    pattern = ItPattern.empty(64, 1)

    # Start note
    pattern.set_note(0, 0, ItNote.play(from_note, 1, 64))

    # Halfway through, slide to new note
    pattern.set_note(32, 0, ItNote.play(to_note, 1, 64)
        .with_effect(7, speed))  # G (tone portamento)

    return pattern

transition = create_transition_pattern("C-3", "F-3", speed=0x10)
```

## Complete Example: Synth Lead

```python
from it_writer import *

# Create volume envelope (punchy ADSR)
vol_env = ItEnvelope()
vol_env.points = [(0, 64), (5, 64), (25, 40), (50, 40), (80, 0)]
vol_env.loop_begin = 2
vol_env.loop_end = 3
vol_env.sustain_begin = 3
vol_env.sustain_end = 3
vol_env.flags = ENV_ENABLED | ENV_LOOP | ENV_SUSTAIN_LOOP

# Create vibrato panning
pan_env = ItEnvelope()
pan_env.points = [(0, 32), (8, 44), (16, 32), (24, 20), (32, 32)]
pan_env.loop_begin = 0
pan_env.loop_end = 4
pan_env.flags = ENV_ENABLED | ENV_LOOP

# Create synth lead instrument
lead_instr = ItInstrument(
    name="Synth Lead",
    nna=NNA_CUT,
    global_volume=128,
    default_pan=32,
    volume_envelope=vol_env,
    panning_envelope=pan_env
)

# Generate saw wave sample
lead_audio = generate_saw_wave(frequency=440, duration=1.0, sample_rate=22050)

lead_sample = ItSample(
    name="saw_lead",
    c5_speed=22050,
    default_volume=64,
    flags=SAMPLE_LOOP,
    loop_begin=0,
    loop_end=len(lead_audio) // 2
)

# Create module
module = ItModule(
    name="Synth Demo",
    num_channels=4,
    default_speed=6,
    default_bpm=140
)

module.instruments.append(lead_instr)
module.samples.append(lead_sample)
module.sample_data.append(lead_audio)

# Create melody pattern
pattern = ItPattern.empty(64, 4)
melody = ["C-5", "D-5", "E-5", "G-5", "E-5", "D-5", "C-5", "---"]

for i, note_name in enumerate(melody):
    if note_name != "---":
        row = i * 8
        note = ItNote.play(note_name, 1, 64)
        if i > 0:  # Add portamento after first note
            note = note.with_effect(7, 0x10)
        pattern.set_note(row, 0, note)

module.patterns.append(pattern)
module.order_table = [0]

write_it(module, "synth_lead.it")
```

## Tips

1. **Start simple:** Begin with basic patterns, add envelopes/NNA later
2. **Test incrementally:** Write file after each major change, test in tracker
3. **Use NNA_FADE for polyphony:** Essential for chords and overlapping notes
4. **Envelope sustain points:** Use sustain loops to hold notes until note-off
5. **Filter sweeps:** Create dynamic sounds with filter envelopes
6. **Volume column:** Use for fast volume fades without using effect column
7. **Pattern reuse:** Use order table to reuse patterns (saves space)

## Reference

- **ITTECH.TXT:** https://github.com/schismtracker/schismtracker/wiki/ITTECH.TXT
- **IT Effects:** See `it-effects.md`
- **IT Format:** See `it-format-spec.md`
