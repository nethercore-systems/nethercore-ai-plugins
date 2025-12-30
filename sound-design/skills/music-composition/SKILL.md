---
name: Music Composition Reference
description: |
  Use this skill when DESIGNING music content - choosing keys, chord progressions, tempos for specific contexts. Trigger phrases: "chord progression for X mood", "what key for combat music", "tempo for boss fight", "mode for mystery", "how to structure a game theme".

  Contains reference tables: modes by character, keys by genre, tempos by context, chord progressions by emotion.

  NOT for XM creation (use procedural-music) or sound synthesis (use procedural-sounds).
version: 1.1.0
---

# Music Composition for Games

Game music differs from linear music: it must loop seamlessly, respond to gameplay, and support rather than dominate the experience.

## Core Principles

1. **Supportive, not intrusive** - Music enhances, doesn't distract
2. **Loopable** - Most game music must repeat indefinitely
3. **Adaptive** - Music should respond to game state
4. **Memorable** - Themes should be recognizable
5. **Efficient** - Work within platform constraints

---

## Music Theory Reference

> **Note:** All tables below show CONVENTIONAL patterns, not rules.
> Your project's audio style guide or creative direction ALWAYS overrides these defaults.
> Breaking conventions intentionally often creates the most memorable music.

### Scales and Modes

| Mode | Conventional Character | Common Uses | Notable Subversions |
|------|------------------------|-------------|---------------------|
| **Ionian (Major)** | Happy, resolved | Victory, joy, adventure | Major key horror (ironic dread) |
| **Aeolian (Minor)** | Sad, serious | Drama, melancholy | Minor key celebration (bittersweet victory) |
| **Dorian** | Minor but hopeful | Medieval, mysterious | Modern/futuristic (Daft Punk) |
| **Phrygian** | Exotic, dark | Combat, tension, Spanish | Peaceful meditation (Eastern influence) |
| **Lydian** | Dreamy, magical | Wonder, fantasy | Unsettling wrongness (The Simpsons theme) |
| **Mixolydian** | Bluesy, relaxed | Folk, adventure | Aggressive rock (AC/DC) |
| **Locrian** | Unstable, dark | Horror, unease | Avant-garde beauty (jazz)|

### Key Selection by Genre (Conventional Defaults)

| Genre | Common Keys | Why It Works | Breaking the Mold |
|-------|-------------|--------------|-------------------|
| Fantasy/Adventure | D, G, C major; Am, Em | Bright, heroic feel | Dark fantasy in Cm, F#m |
| Horror | Atonal, Cm, F#m | Uncomfortable, dark | Happy keys = psychological horror |
| Sci-Fi | Modal, Dm, Bm | Mysterious, spacey | Major keys = hopeful sci-fi |
| Action | Em, Am, Cm | Driving, intense | Major key = superhero optimism |
| Puzzle | C, G, F major | Calm, clear | Dissonance = mind-bending puzzles |
| Retro | C, G | Hardware simplicity | Any key with chiptune timbres |

### Tempo Guidelines (Starting Points)

These are conventional ranges—your game's identity may demand different choices.

| Context | Typical BPM | Conventional Feel | Subversion Ideas |
|---------|-------------|-------------------|------------------|
| Menu | 80-110 | Inviting, patient | Slow ambient (40-60) or energetic (130+) |
| Exploration | 70-100 | Relaxed, unhurried | Uptempo exploration (120+) for momentum |
| Puzzle | 80-110 | Thoughtful | Slow (60) for contemplation or fast (140) for pressure |
| Action | 120-150 | Energetic | Slow-motion feel (80) with intense harmony |
| Combat | 140-180 | Intense | Slow doom-metal (70) or breakneck (200+) |
| Boss | 150-190 | Climactic | Slow dread (80) or silence with stingers |
| Stealth | 60-90 | Tense, careful | Faster pulse (110) with sparse texture |
| Victory | 100-140 | Triumphant | Slow relief (70) or explosive (160) |
| Defeat | 60-80 | Somber | Silence, or ironic upbeat |

---

## Chord Progressions

### By Emotion

**Triumphant/Heroic:**
```
I - IV - V - I       (C - F - G - C)
I - V - vi - IV      (C - G - Am - F)
I - IV - I - V       (C - F - C - G)
```

**Tense/Ominous:**
```
i - VI - III - VII   (Am - F - C - G)
i - iv - VII - III   (Am - Dm - G - C)
i - bII - i          (Am - Bb - Am)
```

**Mysterious:**
```
i - VII - VI - VII   (Am - G - F - G)
Isus4 - I - IVsus2   (Csus4 - C - Fsus2)
Modal vamp on one chord with color tones
```

**Melancholic:**
```
i - iv - i - V       (Am - Dm - Am - E)
i - VI - VII - i     (Am - F - G - Am)
vi - IV - I - V      (Am - F - C - G)
```

**Peaceful:**
```
I - Imaj7 - IV - iv  (C - Cmaj7 - F - Fm)
I - iii - IV - I     (C - Em - F - C)
I - V - vi - iii     (C - G - Am - Em)
```

**Epic/Building:**
```
I - V - vi - IV (repeat with building intensity)
i - III - VII - IV  (Am - C - G - D)
```

---

## Song Structures

### Loop-Based Structure

```
[Intro] → [A] → [A'] → [B] → [A] → [Loop Point]
   4       8      8      8     8     = 36 bars

Loop point connects smoothly back to A section
```

### Layered Structure (Adaptive)

```
Layer 1: Ambient/Pad (always playing)
Layer 2: Rhythm (adds energy)
Layer 3: Melody (adds interest)
Layer 4: Intensity (adds drama)

Gameplay controls which layers are active
```

### Linear Structure (Cutscenes)

```
[Setup] → [Development] → [Climax] → [Resolution]
   8           16             8           8
```

---

## Looping Techniques

### Seamless Loop Checklist

1. **Harmonic continuity**: Last chord leads to first
2. **Rhythmic continuity**: Beat doesn't skip
3. **Melodic continuity**: No jarring jumps
4. **Timbral continuity**: Same instruments active
5. **Dynamic continuity**: Similar volume levels

### Loop Point Strategies

**Crossfade:**
```
End of loop fades out while beginning fades in
Overlap: 0.5-2 seconds
```

**Harmonic Resolution:**
```
End on V chord → Loop to I chord
Natural sense of resolution
```

**Continuous Texture:**
```
Pad/drone sustains across loop point
Melody has natural phrase ending
```

### Testing Loops

1. Listen to loop transition 10+ times
2. Check for clicks, pops, or gaps
3. Verify harmonic sense
4. Test at different entry points
5. Listen while distracted (does it jar you?)

---

## Adaptive Music Systems

### Vertical Layering

Stack musical layers that can be added/removed:

```
Combat Intensity Levels:

Level 0 (Exploration):
  - Ambient pad only

Level 1 (Alert):
  + Add subtle percussion
  + Add bass drone

Level 2 (Combat):
  + Add full drums
  + Add bass line
  + Add tension strings

Level 3 (Boss):
  + Add brass fanfares
  + Add choir
  + Increase tempo (if possible)
```

**Implementation:**
```rust
struct AdaptiveMusic {
    layers: Vec<AudioLayer>,
    current_intensity: f32,  // 0.0 to 1.0
}

impl AdaptiveMusic {
    fn set_intensity(&mut self, intensity: f32) {
        for (i, layer) in self.layers.iter_mut().enumerate() {
            let threshold = i as f32 / self.layers.len() as f32;
            layer.target_volume = if intensity >= threshold { 1.0 } else { 0.0 };
        }
    }

    fn update(&mut self, delta: f32) {
        for layer in &mut self.layers {
            // Smooth crossfade
            layer.volume = lerp(layer.volume, layer.target_volume, delta * 2.0);
        }
    }
}
```

### Horizontal Resequencing

Play different sections based on game state:

```
Section Pool:
  - Intro (play once on area enter)
  - Explore_A, Explore_B, Explore_C (random peaceful)
  - Tension_A, Tension_B (random tense)
  - Combat_A, Combat_B (random combat)
  - Victory (play on win)

Transitions happen at phrase boundaries (every 4/8 bars)
```

**Transition Matrix:**
```
         To:
From:    Explore  Tension  Combat  Victory
Explore    ✓         ✓        ✓       -
Tension    ✓         ✓        ✓       -
Combat     -         ✓        ✓       ✓
Victory    ✓         -        -       -
```

### Stinger System

Short musical phrases for events:

| Event | Stinger Type | Length |
|-------|--------------|--------|
| Item pickup | Rising arpeggio | 0.5-1s |
| Secret found | Mysterious phrase | 1-2s |
| Enemy alert | Tense hit | 0.5s |
| Boss appear | Dramatic fanfare | 2-4s |
| Death | Descending phrase | 1-2s |
| Level complete | Victory fanfare | 3-5s |

**Design Rule:** Stingers should:
- Work over any current music
- Not have strong harmonic content
- Be recognizable but short

---

## Leitmotifs

Recurring musical themes associated with characters, places, or concepts.

### Creating Effective Leitmotifs

1. **Short**: 4-8 notes maximum
2. **Distinctive**: Unique interval pattern
3. **Flexible**: Works in different keys/styles
4. **Memorable**: Singable

### Leitmotif Techniques

**Melodic Transformation:**
```
Hero Theme (Major, confident):
C - E - G - A - G

Hero Theme (Minor, struggling):
C - Eb - G - Ab - G

Hero Theme (Triumphant):
C - E - G - A - C (higher octave)
```

**Rhythmic Transformation:**
```
Normal: ♩ ♩ ♩ ♩
Tense:  ♪♪ ♪♪ ♩ ♩
Epic:   𝅝 𝅝 ♩ ♩
```

**Instrumental Transformation:**
```
Village: Folk instruments
Battle: Brass and percussion
Tragic: Solo violin
Victory: Full orchestra
```

---

## Genre-Specific Patterns

### Orchestral (RPG, Adventure)

```
Structure: Theme and Variations
- Establish main theme (16 bars)
- Variation 1: Different instrumentation
- Variation 2: Different key
- Development: Combine themes
- Return to main theme

Layering:
- Strings: Foundation, emotion
- Brass: Power, heroics
- Woodwinds: Color, melody
- Percussion: Drama, rhythm
```

### Electronic (Action, Racing, Sci-Fi)

```
Structure: Build and Drop
- Intro (ambient, building)
- Build (add elements, risers)
- Drop (full energy)
- Breakdown (reduce elements)
- Repeat

Key Elements:
- Sidechain compression (pumping)
- Filter sweeps (transitions)
- Risers and impacts (transitions)
- Layered drums (power)
```

### Chiptune (Retro, Indie)

```
Structure: Simple loops
- A section (8-16 bars)
- B section (8-16 bars)
- Repeat

Constraints:
- Limited polyphony (3-4 voices)
- Arpeggio for chords
- Noise channel for drums
- Duty cycle for expression
```

### Ambient (Puzzle, Exploration, Horror)

```
Structure: Evolving texture
- No clear sections
- Slow evolution over time
- Generative elements possible

Techniques:
- Long reverb tails
- Slow filter movements
- Overlapping drones
- Sparse melodic fragments
```

---

## Practical Workflow

### 1. Understand Context
- What game genre/mood?
- What's happening on screen?
- How long will players hear this?
- What are technical constraints?

### 2. Establish Framework
- Choose key and tempo
- Define structure (loop length)
- Plan layers (if adaptive)
- Sketch chord progression

### 3. Create Foundation
- Lay down chords/pad
- Add bass line
- Establish rhythm

### 4. Add Identity
- Write main melody/theme
- Add counter-melodies
- Include signature sounds

### 5. Polish
- Verify loop point
- Balance mix
- Test in context
- Iterate

---

## Additional Resources

- `references/chord-progressions.md` - Extended progression database
- `references/adaptive-patterns.md` - Adaptive music implementation
- `references/genre-templates.md` - Genre-specific starting points
