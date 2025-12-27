# Composition Patterns for Game Music

Genre-specific templates and techniques for creating effective game soundtracks.

## Genre Templates

### Action/Combat Music

**Characteristics:** High energy, driving rhythm, tension
**Tempo:** 140-170 BPM
**Speed:** 4-6 ticks/row

```
Order Structure: [0, 1, 1, 2, 1, 1, 2, 3]
Pattern 0: Intro buildup (drums only → full)
Pattern 1: Main loop (full energy)
Pattern 2: Intensity peak (added melody, faster hi-hats)
Pattern 3: Breakdown (sparse, builds tension)

Channel Layout:
Ch 1: Kick - on 1 and 3 (rows 0, 8, 16, 24)
Ch 2: Snare - on 2 and 4 (rows 4, 12, 20, 28)
Ch 3: Hi-hat - every row or half-row
Ch 4: Bass - syncopated, follows kick
Ch 5: Lead - short staccato phrases
Ch 6: Pad - sustained power chords
```

### Puzzle/Ambient

**Characteristics:** Calm, contemplative, non-intrusive
**Tempo:** 80-110 BPM
**Speed:** 6-8 ticks/row

```
Order Structure: [0, 1, 2, 1, 2, 1, 3]
Pattern 0: Intro (sparse, atmospheric)
Pattern 1: Main A (gentle melody)
Pattern 2: Main B (variation)
Pattern 3: Bridge (new texture)

Channel Layout:
Ch 1: Bass - sustained notes, slow movement
Ch 2: Pad 1 - evolving chord
Ch 3: Pad 2 - counterpoint harmony
Ch 4: Arpeggio - gentle rhythmic motion
Ch 5: Melody - sparse, breathing space
Ch 6: FX - subtle texture (filtered noise, bells)
```

### Title Screen

**Characteristics:** Memorable, represents game identity
**Tempo:** 100-130 BPM
**Speed:** 6 ticks/row

```
Order Structure: [0, 1, 1, 2, 1, 1, 2, 3, 0]
Pattern 0: Intro fanfare (attention-grabbing)
Pattern 1: Main theme (memorable melody)
Pattern 2: Variation (builds on theme)
Pattern 3: Breakdown/loop prep

Tips:
- Start with a distinctive hook
- Build to a satisfying peak
- Ensure clean loop back to intro
- Consider 30-60 second total length
```

### Boss Battle

**Characteristics:** Intense, oppressive, climactic
**Tempo:** 150-180 BPM
**Speed:** 3-4 ticks/row

```
Order Structure: [0, 1, 2, 1, 2, 3, 3, 1, 2, 3]
Pattern 0: Ominous intro (low drones, tension)
Pattern 1: Attack phase (aggressive rhythm)
Pattern 2: Intensity (added layers, chaos)
Pattern 3: Desperate (highest energy, fastest)

Techniques:
- Use chromatic bass movement for tension
- Arpeggio effects for chaotic feel
- Pattern loops (E6x) for relentless sections
- Occasional tempo spikes (Fxx) for hits
```

### Victory/Fanfare

**Characteristics:** Triumphant, celebratory, short
**Tempo:** 120-140 BPM
**Length:** 4-8 bars (one-shot or short loop)

```
Pattern 0: Full fanfare
- Rising arpeggio opening
- Triumphant brass-like lead
- Cymbal crash accent
- Resolving chord progression
```

### Game Over/Defeat

**Characteristics:** Somber, reflective
**Tempo:** 60-80 BPM
**Length:** 4-8 bars

```
Pattern 0: Defeat jingle
- Descending melody
- Minor key resolution
- Fade to silence or held chord
```

## Pattern Structure Techniques

### Verse-Chorus Form

```
Order: [intro, verse, verse, chorus, verse, chorus, bridge, chorus, outro]
       [  0  ,   1  ,   1  ,   2   ,   1  ,   2   ,   3   ,   2   ,  4  ]

Pattern 0 (Intro): Build anticipation
Pattern 1 (Verse): Establish groove, lower energy
Pattern 2 (Chorus): Main hook, higher energy
Pattern 3 (Bridge): Contrast, different progression
Pattern 4 (Outro): Wind down, prepare for loop
```

### Call and Response

```
Rows 0-7:  Lead plays phrase A
Rows 8-15: Harmony responds with phrase B
Rows 16-23: Lead plays phrase A (variation)
Rows 24-31: Full ensemble answers
```

### Build and Drop

```
Rows 0-15:  Minimal elements, building
Rows 16-23: Add layers progressively
Rows 24-27: Peak tension (fills, risers)
Rows 28-31: Drop - full elements or breakdown
```

## Melody Patterns

### Pentatonic Scale (safe, always sounds good)
Notes: C, D, E, G, A (major) or A, C, D, E, G (minor)

### Common Melodic Motifs

**Rising Energy:**
```
C-4, D-4, E-4, G-4  (ascending)
```

**Falling Resolution:**
```
G-4, E-4, D-4, C-4  (descending)
```

**Tension-Release:**
```
E-4, F-4, E-4, D-4, C-4  (chromatic approach)
```

**Arpeggio Chord Tones:**
```
C-4, E-4, G-4, C-5  (broken chord)
```

## Bass Patterns

### Steady Root
```
Row 0: C-2 (root)
Row 4: C-2
Row 8: C-2
Row 12: C-2
```

### Octave Jump
```
Row 0: C-2
Row 4: C-3
Row 8: C-2
Row 12: C-3
```

### Walking Bass
```
Row 0: C-2
Row 4: D-2
Row 8: E-2
Row 12: G-2
```

### Syncopated
```
Row 0: C-2
Row 3: --- (rest)
Row 6: C-2
Row 10: D-2
Row 14: C-2
```

## Percussion Patterns

### Basic 4/4 Beat
```
Row:    0   4   8  12  16  20  24  28
Kick:   X   -   X   -   X   -   X   -
Snare:  -   X   -   X   -   X   -   X
HiHat:  X   X   X   X   X   X   X   X
```

### Double-Time Feel
```
Kick on every 2 rows, hi-hat on every row
Add snare ghost notes on odd rows (lower volume)
```

### Breakbeat
```
Row:    0   2   4   6   8  10  12  14
Kick:   X   -   -   X   -   -   X   -
Snare:  -   -   X   -   -   X   -   X
```

## Loop Point Design

### Clean Loop Transition

1. **Match first and last row textures**
   - If intro has sparse drums, outro should too
   - Pad/chord should be same or complementary

2. **Use volume fades at boundary**
   ```
   Row 62: --- -- -- A08  ; Start fade
   Row 63: --- -- -- A08  ; Continue fade
   Row 0:  C-4 01 40 ---  ; Fresh start at full volume
   ```

3. **Set restart position to skip intro**
   - In XM header, set restart position to skip pattern 0
   - Intro plays once, then loops from pattern 1

4. **Avoid hanging notes at loop point**
   - Ensure all channels have note-off or new note at loop start
   - Use EC (note cut) on final row if needed

### Testing Loops

1. Play song to loop point
2. Listen carefully at transition
3. Check for clicks, pops, or jarring changes
4. Adjust volumes, add/remove notes as needed
