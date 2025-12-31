---
name: Tracker Music Fundamentals
description: |
  Use this skill when generating tracker music to understand WHY to use specific techniques. This is the philosophy layer that separates amateur from polished output.

  **Pipeline position: COMPOSITION (3 of 3)**
  - For music theory (modes, progressions): use `sound-design:music-composition`
  - For instrument synthesis: use `zx-procgen:procedural-instruments`

  See `docs/audio-pipeline.md` for complete workflow.

  **Trigger phrases:** "why use vibrato", "when to use effects", "make it sound professional", "tracker polish", "humanize the music", "sound less mechanical"

  **Load references when:**
  - Effect usage philosophy → `references/effect-philosophy.md`
  - Sample economy → `references/sample-economy.md`
  - Channel voice allocation → `references/channel-allocation.md`

  For format-specific implementation, use `xm-format` or `it-format` skills.
version: 1.1.0
---

# Tracker Music Fundamentals

## Core Philosophy

Tracker music is **constraint-driven art**. Limited channels, limited polyphony, limited effects - but these constraints create a distinctive aesthetic. The goal isn't to simulate an orchestra; it's to create music that sounds *intentional* within tracker limitations.

**Three Pillars:**
1. **Economy** - Maximum musical impact with minimum resources
2. **Expression** - Effects as musical expression, not decoration
3. **Flow** - Seamless playback with intentional dynamics

## The Polish Layer

What separates amateur tracker music from professional:

| Amateur | Polished |
|---------|----------|
| Flat velocity throughout | Velocity variation on repeating notes |
| Effects used randomly | Effects serve musical purpose |
| Copy-paste patterns | Pattern variations with small changes |
| Abrupt note endings | Volume fades and release tails |
| Mechanical timing | Slight groove variations |
| All notes same length | Articulation variety (staccato/legato) |

## Effect Philosophy

Effects aren't decoration - they're **musical expression encoded as data**.

### Vibrato (H/4) - Warmth and Life

**WHY:** Sustained notes feel lifeless without movement. Vibrato adds organic warmth.

**WHEN to use:**
- Held melody notes (especially 8+ rows)
- Lead instruments
- String/pad sustains
- NOT on percussive sounds or bass

**HOW to apply:**
```python
# Subtle vibrato for warmth
.with_effect(4, 0x24)  # Speed 2, depth 4 (gentle)

# Expressive vibrato for emphasis
.with_effect(4, 0x46)  # Speed 4, depth 6 (noticeable)

# Delayed vibrato (more natural)
row 0:  C-4 01 -- ---   # Attack clean
row 4:  --- -- -- H24   # Vibrato enters after attack
```

### Portamento/Glide (3/G) - Smoothness and Emphasis

**WHY:** Instant pitch jumps are mechanical. Slides create connection and emphasis.

**WHEN to use:**
- Melodic phrases (slide INTO important notes)
- Bass transitions (smooth root movement)
- Synth leads (characteristic of electronic music)
- NOT on drums or percussive attacks

**HOW to apply:**
```python
# Slide into chorus note for emphasis
row 0:  C-4 01 40 ---   # Verse note
row 8:  E-4 01 40 G10   # Slide UP to chorus (emphasizes arrival)

# Bass slides between roots
row 0:  C-2 02 40 ---   # Root
row 16: G-2 02 40 G08   # Slide to fifth (smooth transition)
```

### Arpeggio (0/J) - Chords Without Polyphony

**WHY:** With limited channels, can't always spare 3 for a chord. Arpeggio creates chord impression on one channel.

**WHEN to use:**
- Harmony parts when channels are tight
- Chiptune aesthetic (intentional lo-fi)
- Rhythmic harmonic motion
- NOT when you have spare channels (real chords sound better)

**HOW to apply:**
```python
# Major chord feel
.with_effect(0, 0x47)  # Root + 4 + 7 semitones (C-E-G)

# Minor chord feel
.with_effect(0, 0x37)  # Root + 3 + 7 semitones (C-Eb-G)

# Power chord (for leads)
.with_effect(0, 0x07)  # Root + 0 + 7 semitones (C-C-G)
```

### Volume Slides (A/D) - Dynamics and Expression

**WHY:** Static volume is robotic. Real instruments crescendo and diminuendo.

**WHEN to use:**
- Build tension before drops
- Fade tails on sustained notes
- Swell into important sections
- Create breathing room

**HOW to apply:**
```python
# Fade out at phrase end
row 56: --- -- -- A08   # Start fade
row 60: --- -- -- A08   # Continue fade
row 63: --- -- -- A08   # Nearly silent for clean loop

# Swell into chorus
row 0:  C-4 01 10 ---   # Start quiet
row 4:  --- -- -- A80   # Swell up
row 8:  --- -- -- A80   # Continue swell
row 12: --- -- -- A80   # Arrive at full volume
```

### Pitch Slides (1-2/E-F) - Attack Character

**WHY:** Kick drums need pitch drop for punch. Synth leads use pitch for character.

**WHEN to use:**
- Kick drums (pitch down from high)
- 808-style bass (pitch envelope)
- Laser/sci-fi effects
- Synth lead attacks

**HOW to apply:**
```python
# Punchy kick with pitch drop
row 0: C-5 01 40 E40   # Start high, slide down fast

# Synth lead with character
row 0: E-4 03 40 E08   # Slight pitch drop on attack (adds weight)
```

### Retrigger (E9x/Q) - Rhythmic Intensity

**WHY:** Rapid retriggering creates machine-gun effect for energy.

**WHEN to use:**
- Snare rolls before drops
- Hi-hat intensification
- Build-up sections
- NOT throughout (fatiguing)

**HOW to apply:**
```python
# Snare roll build-up
row 28: C-4 02 40 E93   # Retrigger every 3 ticks
row 30: C-4 02 40 E92   # Faster (every 2 ticks)
row 31: C-4 02 40 E91   # Fastest (every tick) into drop
```

## Human Feel Techniques

### Velocity Variation

Never use the same velocity for repeating notes:

```python
# Bad: Mechanical
for row in range(0, 64, 4):
    pattern.set_note(row, 2, ItNote.play("C-4", 3, 48))

# Good: Human feel
velocities = [48, 40, 44, 36, 48, 38, 46, 40]  # Varied pattern
for i, row in enumerate(range(0, 64, 4)):
    vol = velocities[i % len(velocities)]
    pattern.set_note(row, 2, ItNote.play("C-4", 3, vol))
```

### Groove Offset

Slight timing variations create groove:

```python
# Swing feel (delay every other hi-hat)
for row in range(0, 64, 4):
    if (row // 4) % 2 == 1:
        # Delay odd hits with SDx (note delay)
        note = ItNote.play("C-4", 3, 48).with_effect(19, 0xD2)  # SD2
    else:
        note = ItNote.play("C-4", 3, 48)
    pattern.set_note(row, 2, note)
```

### Ghost Notes

Quiet notes between main hits add life:

```python
# Main hi-hat hits + ghost notes
for row in range(0, 64, 2):
    if row % 4 == 0:
        pattern.set_note(row, 2, ItNote.play("C-4", 3, 48))  # Main hit
    else:
        pattern.set_note(row, 2, ItNote.play("C-4", 3, 24))  # Ghost (quiet)
```

## Pattern Variation Principles

### The 4-Bar Rule

Never loop the same 4 bars more than twice without variation:

```python
# Order table with variations
order_table = [
    0,  # Intro
    1,  # Verse (pattern 1)
    2,  # Verse variation (pattern 2 - small changes)
    1,  # Verse again
    2,  # Verse variation again
    3,  # Chorus (contrast)
]
```

### Variation Techniques

1. **Add/remove a note** - Same pattern, one element different
2. **Velocity change** - Same notes, different emphasis
3. **Fill on 4th bar** - Drum fill every 4th repetition
4. **Effect variation** - Add vibrato/slide on repeat
5. **Octave shift** - Same melody, different register

## Sample Economy

See `references/sample-economy.md` for details.

**Key principles:**
- Use loop points to extend short samples
- Pitch-shift one sample for multiple notes (within reason)
- Share samples across instruments where possible
- Shorter samples = smaller file size

## Channel Allocation

See `references/channel-allocation.md` for details.

**Typical 8-channel layout:**
| Channel | Role | Notes |
|---------|------|-------|
| 1 | Kick | Low, punchy |
| 2 | Snare | Mid, snappy |
| 3 | Hi-hat | High, short |
| 4 | Bass | Low synth/guitar |
| 5 | Lead 1 | Main melody |
| 6 | Lead 2 | Counter-melody |
| 7 | Pad/Chord | Harmony |
| 8 | FX/Transition | Risers, impacts |

## Quality Checklist

Before finalizing any generated track:

- [ ] No two adjacent notes have identical velocity (unless intentional)
- [ ] Sustained notes have vibrato or movement
- [ ] Melodic transitions use portamento where appropriate
- [ ] Volume fades at loop boundaries
- [ ] At least one variation per 4-bar phrase
- [ ] Effects serve musical purpose (not decoration)
- [ ] Channel roles are clearly defined
- [ ] Loop point is seamless
