# Genre Templates

Ready-to-use pattern structures for common game music genres.

## Action/Combat Music

**Characteristics:** High energy, driving rhythm, tension
**Tempo:** 140-170 BPM | **Speed:** 4-6

### Pattern Structure

```
Order: [0, 1, 1, 2, 1, 1, 2, 3]

Pattern 0 - Intro Buildup (64 rows):
Rows 0-15:   Ominous pad, sparse percussion
Rows 16-31:  Add bass drone, building rhythm
Rows 32-47:  Drums enter, intensity rising
Rows 48-63:  Full groove transition

Pattern 1 - Main Combat (64 rows):
Rows 0-15:   Full energy drums + bass
Rows 16-31:  Aggressive lead enters
Rows 32-47:  Lead continues, variation
Rows 48-63:  Prepare for repeat/transition

Pattern 2 - Intensity Peak (64 rows):
Rows 0-15:   Maximum energy, added layers
Rows 16-31:  Chaos elements (arpeggios, fills)
Rows 32-47:  Sustain intensity
Rows 48-63:  Brief release, prepare loop

Pattern 3 - Breakdown (64 rows):
Rows 0-15:   Strip to drums + bass
Rows 16-31:  Tension build (rising elements)
Rows 32-47:  Drum fills, anticipation
Rows 48-63:  Explode back into pattern 1
```

### Channel Layout (8ch)

```
Ch 1: Kick - Hard hits on 1, 3 (rows 0, 8, 16, 24...)
Ch 2: Snare - On 2, 4 (rows 4, 12, 20, 28...)
Ch 3: Hi-hat - Every row or half-row, velocity varied
Ch 4: Bass - Syncopated, follows kick, aggressive tone
Ch 5: Lead - Short staccato phrases, arpeggios
Ch 6: Counter - Power chord stabs, octave doubles
Ch 7: Pad - Sustained tension chords
Ch 8: FX - Impacts, risers, chaos elements
```

---

## Exploration/Ambient

**Characteristics:** Calm, contemplative, non-intrusive
**Tempo:** 80-110 BPM | **Speed:** 6-8

### Pattern Structure

```
Order: [0, 1, 2, 1, 2, 1, 3]

Pattern 0 - Intro (64 rows):
Rows 0-31:   Pad fade in, sparse texture
Rows 32-63:  Gentle rhythm elements enter

Pattern 1 - Main A (64 rows):
Rows 0-15:   Gentle groove established
Rows 16-31:  Melody enters, simple and memorable
Rows 32-47:  Melody continues
Rows 48-63:  Prepare variation

Pattern 2 - Main B (64 rows):
Rows 0-15:   Variation - different chord
Rows 16-31:  Counter-melody or harmony
Rows 32-47:  Return toward main theme
Rows 48-63:  Smooth transition back

Pattern 3 - Bridge (64 rows):
Rows 0-31:   New texture, different register
Rows 32-63:  Gradual return to main
```

### Channel Layout (6ch)

```
Ch 1: Pad - Evolving chord, slow filter movement
Ch 2: Bass - Sustained notes, slow movement
Ch 3: Arpeggio - Gentle rhythmic motion
Ch 4: Melody - Sparse, breathing space
Ch 5: Harmony - Subtle counter-melody
Ch 6: FX - Bells, chimes, ambient texture
```

---

## Boss Battle

**Characteristics:** Intense, oppressive, climactic
**Tempo:** 150-180 BPM | **Speed:** 3-4

### Pattern Structure

```
Order: [0, 1, 2, 1, 2, 3, 3, 1, 2, 3]

Pattern 0 - Ominous Intro (64 rows):
Rows 0-31:   Low drones, tension
Rows 32-47:  Percussion enters, sparse
Rows 48-63:  Build to attack

Pattern 1 - Attack Phase (64 rows):
Rows 0-15:   Aggressive rhythm established
Rows 16-31:  Menacing melody
Rows 32-47:  Full assault
Rows 48-63:  Brief release

Pattern 2 - Intensity Phase (64 rows):
Rows 0-15:   Additional layers, chaos
Rows 16-31:  Chromatic movement, dissonance
Rows 32-47:  Maximum aggression
Rows 48-63:  Prepare transition

Pattern 3 - Desperate Phase (64 rows):
Rows 0-15:   Fastest, most chaotic
Rows 16-31:  Drum fills, urgency
Rows 32-47:  Final push energy
Rows 48-63:  Loop back or victory transition
```

### Channel Layout (8ch)

```
Ch 1: Kick - Double-time, aggressive
Ch 2: Snare - Hard hits, blast beats optional
Ch 3: Hi-hat/Cymbal - Constant motion
Ch 4: Percussion - Toms, impacts
Ch 5: Bass - Chromatic movement, dissonant
Ch 6: Lead - Menacing theme
Ch 7: Stabs - Orchestral hits, brass stabs
Ch 8: FX - Risers, impacts, chaos
```

---

## Victory Fanfare

**Characteristics:** Triumphant, celebratory, short
**Tempo:** 120-140 BPM | **Length:** 4-8 bars (one-shot)

### Pattern Structure

```
Order: [0]  ← Single pattern, no loop

Pattern 0 - Victory (32-64 rows):
Rows 0-7:    Rising arpeggio/fanfare opening
Rows 8-15:   Triumphant brass-like melody
Rows 16-23:  Peak moment, cymbal crash
Rows 24-31:  Resolution, held chord, fade
```

### Channel Layout (4ch)

```
Ch 1: Drums - Cymbal crash, simple rhythm
Ch 2: Bass - Strong root notes
Ch 3: Lead - Triumphant fanfare melody
Ch 4: Harmony - Chord support
```

---

## Puzzle/Thinking

**Characteristics:** Thoughtful, unobtrusive, looping
**Tempo:** 90-110 BPM | **Speed:** 6-8

### Pattern Structure

```
Order: [0, 1, 1, 2, 1, 1, 2, 1]

Pattern 0 - Intro (32 rows):
Rows 0-31:   Minimal, sets mood

Pattern 1 - Main Loop (64 rows):
Rows 0-15:   Simple groove
Rows 16-31:  Subtle melodic element
Rows 32-47:  Variation
Rows 48-63:  Return to start feel

Pattern 2 - Variation (64 rows):
Rows 0-31:   Different chord or texture
Rows 32-63:  Transition back smoothly
```

### Channel Layout (4ch)

```
Ch 1: Light percussion or none
Ch 2: Bass - Simple, supportive
Ch 3: Arpeggio/Sequence - Rhythmic interest
Ch 4: Pad - Harmonic bed
```

---

## Stealth/Tension

**Characteristics:** Suspenseful, minimal, anxious
**Tempo:** 70-90 BPM | **Speed:** 8

### Pattern Structure

```
Order: [0, 1, 1, 2, 1, 1, 2, 3]

Pattern 0 - Setup (64 rows):
Rows 0-63:   Drone, heartbeat pulse

Pattern 1 - Stealth Main (64 rows):
Rows 0-15:   Sparse hits, tension
Rows 16-31:  Subtle melodic fragment
Rows 32-47:  Return to sparse
Rows 48-63:  Slight build

Pattern 2 - Alert Variation (64 rows):
Rows 0-31:   More active, danger hint
Rows 32-63:  Return to stealth feel

Pattern 3 - Danger Near (64 rows):
Rows 0-31:   Highest tension, still restrained
Rows 32-63:  Ready to explode into combat
```

### Channel Layout (4ch)

```
Ch 1: Heartbeat/Pulse - Sub bass, slow rhythm
Ch 2: Texture - Filtered noise, subtle
Ch 3: Sparse Hits - Occasional impacts
Ch 4: Melody - Fragments, unresolved
```

---

## Menu/Title Screen

**Characteristics:** Memorable, represents game, inviting
**Tempo:** 100-130 BPM | **Speed:** 6

### Pattern Structure

```
Order: [0, 1, 1, 2, 1, 1, 2, 3]

Pattern 0 - Opening (64 rows):
Rows 0-15:   Iconic hook/fanfare
Rows 16-31:  Establish groove
Rows 32-47:  Main theme preview
Rows 48-63:  Lead into main loop

Pattern 1 - Main Theme (64 rows):
Rows 0-15:   Full theme statement
Rows 16-31:  Theme continues
Rows 32-47:  Variation/development
Rows 48-63:  Prepare repeat

Pattern 2 - Chorus/Hook (64 rows):
Rows 0-15:   Most memorable section
Rows 16-31:  Hook continues
Rows 32-47:  Build or sustain
Rows 48-63:  Transition

Pattern 3 - Bridge (64 rows):
Rows 0-31:   Different section, ear refresh
Rows 32-63:  Return to main theme
```

### Channel Layout (8ch)

```
Ch 1: Kick
Ch 2: Snare
Ch 3: Hi-hat
Ch 4: Bass
Ch 5: Lead - Main theme
Ch 6: Counter - Harmonies
Ch 7: Pad - Chord support
Ch 8: FX - Accents, transitions
```
