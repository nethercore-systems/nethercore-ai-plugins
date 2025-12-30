# Effect Philosophy Reference

Deep dive into when and why to use specific effects for musical expression.

## Effect Categories

### Movement Effects (Add Life)

| Effect | Creates | Best For | Avoid On |
|--------|---------|----------|----------|
| Vibrato (H/4) | Organic warmth | Leads, pads, sustained notes | Drums, short notes |
| Tremolo (R/7) | Intensity, drama | Strings, tension | Bass, steady groove |
| Panbrello (Y) | Spatial movement | Pads, ambient | Lead melody |
| Arpeggio (0/J) | Harmonic motion | Chords on one channel | When channels available |

### Transition Effects (Connect Notes)

| Effect | Creates | Best For | Avoid On |
|--------|---------|----------|----------|
| Portamento (3/G) | Smooth slides | Melody, bass transitions | Drums, staccato |
| Pitch Slide (1-2/E-F) | Attack character | Kick, synth attacks | Acoustic instruments |
| Tone Porta (3/G) | Deliberate glide | Emphasis, expression | Percussive sounds |

### Dynamic Effects (Shape Loudness)

| Effect | Creates | Best For | Avoid On |
|--------|---------|----------|----------|
| Volume Slide (A/D) | Crescendo/fade | Builds, releases | Steady bass |
| Tremor (I) | Stuttering | Tension, glitch | Melodic content |
| Retrigger (E9x/Q) | Machine-gun | Rolls, builds | Sustained passages |

## Effect Combinations

### Warm Lead

Vibrato + Volume swell creates expressive lead:

```
Row 0:  C-5 01 20 ---   # Start quiet
Row 2:  --- -- -- A40   # Swell up
Row 4:  --- -- -- H24   # Add vibrato at peak
Row 8:  --- -- -- A04   # Gentle fade
```

### Punchy Bass

Pitch drop + tight envelope:

```
Row 0:  C-3 01 40 E20   # Attack with pitch drop
Row 2:  --- -- -- A04   # Quick volume fade
```

### Emotional Melody

Portamento into important notes:

```
Row 0:  G-4 01 40 ---   # Setup note
Row 8:  C-5 01 48 G10   # Slide UP to peak (emphasis)
Row 16: A-4 01 44 G08   # Slide DOWN to resolution
```

### Build-up Sequence

Progressive intensification:

```
Row 48: --- -- -- E94   # Retrigger slow
Row 52: --- -- -- E93   # Faster
Row 56: --- -- -- E92   # Faster still
Row 60: --- -- -- E91   # Maximum before drop
```

## Mood-Effect Mapping

### Triumphant/Heroic

- **Lead:** Strong attacks, deliberate portamento to peaks
- **Brass:** No vibrato (powerful, steady)
- **Dynamics:** Swells into climactic moments
- **Rhythm:** Steady, confident

```
Effects: G (portamento), A (volume swell), minimal H
```

### Mysterious/Tense

- **Lead:** Subtle vibrato, uncertain pitch bends
- **Pads:** Slow filter sweeps (IT), tremolo
- **Dynamics:** Quiet with sudden accents
- **Rhythm:** Irregular, sparse

```
Effects: H (vibrato), R (tremolo), E/F (pitch uncertainty)
```

### Aggressive/Combat

- **Lead:** Fast attacks, pitch drops
- **Drums:** Retrigger rolls, hard accents
- **Bass:** Pitch envelope, distorted character
- **Dynamics:** Constant high energy

```
Effects: E (pitch down), Q/E9x (retrigger), 0 (arpeggio power chords)
```

### Peaceful/Ambient

- **Lead:** Gentle vibrato, slow portamento
- **Pads:** Auto-pan, volume breathing
- **Dynamics:** Gradual, never sudden
- **Rhythm:** Flowing, not grid-locked

```
Effects: H (subtle vibrato), SDx (note delay for swing), A (volume breathing)
```

### Melancholic/Sad

- **Lead:** Slower vibrato, descending portamento
- **Dynamics:** Fades, trailing releases
- **Rhythm:** Sparse, space between notes
- **Harmony:** Minor arpeggios

```
Effects: G (downward slides), A (fades), 0 (minor arpeggios: 037)
```

## Effect Intensity Guidelines

### Vibrato Depth

| Context | Speed | Depth | Code |
|---------|-------|-------|------|
| Subtle warmth | 2 | 2-3 | H22, H23 |
| Expressive | 3-4 | 4-5 | H34, H45 |
| Dramatic | 5-6 | 6-8 | H56, H68 |
| Over-the-top | 7+ | 8+ | H78+ |

### Portamento Speed

| Context | Speed | Code |
|---------|-------|------|
| Instant (almost) | 40+ | G40+ |
| Fast slide | 20-30 | G20, G30 |
| Medium glide | 10-18 | G10, G18 |
| Slow expressive | 04-08 | G04, G08 |
| Very slow | 01-03 | G01, G02 |

### Volume Slide Rate

| Context | Rate | Code |
|---------|------|------|
| Sudden swell | F0 | AF0 |
| Fast fade | 0C-0F | A0C-A0F |
| Medium dynamics | 08-0B | A08-A0B |
| Gentle breathing | 01-04 | A01-A04 |

## Anti-Patterns to Avoid

### Over-Effect

**Bad:** Every note has vibrato, arpeggio, and slide
**Good:** Effects used sparingly for emphasis

### Wrong Effect for Instrument

**Bad:** Vibrato on kick drum, portamento on hi-hat
**Good:** Match effect to instrument character

### Mechanical Application

**Bad:** Same vibrato parameters throughout song
**Good:** Vary parameters based on musical context

### Effect Without Purpose

**Bad:** "This sounds cool" with no musical reason
**Good:** "This creates tension before the chorus"
