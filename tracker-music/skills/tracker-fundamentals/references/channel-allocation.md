# Channel Allocation Reference

Strategic voice allocation for tracker music.

## Core Principle

Channels are your orchestra sections. Plan them like arranging for a band, not randomly filling slots.

## Standard Layouts

### 4-Channel (Minimal/Chiptune)

| Channel | Role | Notes |
|---------|------|-------|
| 1 | Drums (all) | Kick/snare share, hi-hat interleaved |
| 2 | Bass | Root notes, simple patterns |
| 3 | Lead | Main melody |
| 4 | Harmony | Arpeggios for chords, counter-melody |

**Constraints:** Drums must share one channel - use note priority (kick > snare > hat).

### 8-Channel (Standard)

| Channel | Role | Frequency Range | Notes |
|---------|------|-----------------|-------|
| 1 | Kick | Sub-low (50-100Hz) | Punchy, centered |
| 2 | Snare | Mid (200-2kHz) | Snappy, centered |
| 3 | Hi-hat | High (5k+) | Bright, can pan |
| 4 | Bass | Low (60-250Hz) | Foundation, centered |
| 5 | Lead 1 | Mid-high | Main melody |
| 6 | Lead 2 | Mid | Counter-melody, harmony |
| 7 | Pad/Chord | Full range | Sustained harmony |
| 8 | FX/Fills | Any | Transitions, accents |

### 16-Channel (Full Arrangement)

| Channels | Section | Notes |
|----------|---------|-------|
| 1-4 | Drums | Kick, snare, hats, percussion |
| 5-6 | Bass | Main + variation/octave |
| 7-9 | Lead | Melody + harmonies |
| 10-12 | Pads | Chord layers |
| 13-14 | Strings/Synth | Texture, movement |
| 15-16 | FX/Reserve | Transitions, special moments |

### 32-Channel (Orchestral/Complex)

| Channels | Section | Notes |
|----------|---------|-------|
| 1-6 | Percussion | Full kit + orchestral perc |
| 7-10 | Bass | Multiple bass instruments |
| 11-16 | Strings | Violin, viola, cello, bass sections |
| 17-20 | Brass | Trumpet, horn, trombone, tuba |
| 21-24 | Woodwinds | Flute, clarinet, oboe, bassoon |
| 25-28 | Synths/Keys | Pads, leads, piano |
| 29-32 | FX/Choir | Special textures, vocals |

## Channel Roles Deep Dive

### Rhythm Section (Channels 1-4 typical)

**Kick (Channel 1):**
- Always present in mix
- Centered (no panning)
- Low frequency dominance
- Short notes, clear attacks

**Snare (Channel 2):**
- Defines groove
- Centered or slight variation
- Ghost notes add life
- Volume variation essential

**Hi-hat (Channel 3):**
- Continuous motion
- Can pan slightly
- Velocity variation critical
- Open/closed alternation

**Percussion (Channel 4):**
- Fills gaps
- Toms, cymbals, shakers
- More dynamic freedom
- Pan for width

### Harmonic Foundation

**Bass (Channel 4-5):**
- Root notes of chords
- Locked to kick rhythmically
- Always centered
- Simple patterns work best

**Pads/Chords (Channel 7-8):**
- Harmonic context
- Sustained notes
- Can use full stereo
- Volume should sit below lead

### Melodic Content

**Lead (Channel 5-6):**
- Most prominent voice
- Slightly forward in mix
- Center or slight pan
- Most expression/effects

**Counter-melody (Channel 6):**
- Answers main melody
- Different register
- Pan opposite to lead
- Complementary rhythm

### Texture/FX

**FX Channel (last channels):**
- Risers, impacts, transitions
- Saved for special moments
- Can be any frequency
- Often automated panning

## Panning Strategy

```
Hard Left ←————————————————→ Hard Right
           Hi-hat (slight)
      Rhythm guitar ←→ Rhythm guitar
                 ↓ Kick ↓
                 ↓ Snare ↓
                 ↓ Bass ↓
           Lead (slight)
      Pad layer 1 ←→ Pad layer 2
    Counter-melody ←→ Lead melody
```

### Panning Values

| Position | XM Value | IT Value |
|----------|----------|----------|
| Hard Left | 0x00 | 0x00 |
| Left | 0x20 | 0x20 |
| Center | 0x80 | 0x80 |
| Right | 0xC0 | 0xC0 |
| Hard Right | 0xFF | 0xFF |

**Rule:** Low frequencies (kick, bass) always centered. High frequencies can spread wider.

## Dynamic Channel Assignment

### NNA Polyphony (IT Only)

IT's New Note Actions allow "virtual" extra channels:

```python
piano = ItInstrument(
    name="Piano",
    nna=NNA_FADE,      # Previous notes fade when new ones play
    fadeout=512,       # Fade speed
)

# One channel can now play polyphonic piano!
# Each new note fades the previous, creating up to ~8 virtual voices
```

### Channel Stealing Priority

When channels are limited, prioritize:

1. **Kick/Snare** - Never steal (rhythm foundation)
2. **Bass** - Rarely steal (harmonic foundation)
3. **Lead** - Steal cautiously (melodic importance)
4. **Pads** - Can steal (least noticeable)
5. **FX** - First to steal (decorative)

## Genre-Specific Allocations

### Chiptune (4 channels)

```
1: Pulse lead (melody)
2: Pulse harmony (chords via arpeggio)
3: Triangle bass
4: Noise drums
```

### Electronic/Dance (8 channels)

```
1: Kick (808 style)
2: Snare/Clap
3-4: Hi-hats (closed, open)
5: Bass (synth, sidechained)
6: Lead synth
7: Pad
8: FX/Vocals
```

### Rock (8 channels)

```
1: Kick
2: Snare
3: Hi-hat/Cymbals
4: Bass guitar
5-6: Rhythm guitars (L/R)
7: Lead guitar
8: Vocals/Keys
```

### Orchestral (16+ channels)

```
1-4: Percussion section
5-6: Double bass, cello
7-8: Violas
9-10: Violins
11-12: Brass
13-14: Woodwinds
15-16: Special (harp, choir, etc.)
```

## Troubleshooting

### Muddy Mix

**Problem:** Everything sounds cluttered
**Solution:**
- Reduce pad volume
- High-pass filter bass instruments
- Pan elements apart
- Give lead melodic space (don't compete)

### Thin Mix

**Problem:** Sounds empty
**Solution:**
- Add pad layer
- Double leads an octave apart
- Add subtle reverb/delay via sample tails
- Increase stereo width

### Losing Punch

**Problem:** Drums feel weak
**Solution:**
- Clear space in bass for kick (volume duck)
- Keep drums highest priority
- Shorten competing low elements
- Check relative velocities
