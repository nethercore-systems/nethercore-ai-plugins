---
name: Sound Effects Design Patterns
description: |
  Use this skill when DESIGNING sound effects - deciding what sounds to create, how to layer them, and what character they should have. Trigger phrases: "what makes a good impact sound", "how to layer SFX", "UI sound design", "ambient layer recipe", "weapon sound components".

  This skill provides DESIGN PATTERNS - layering approaches, material signatures, frequency allocation, category templates.

  **Pipeline position: DESIGN (1 of 3)**
  - For IMPLEMENTATION CODE (numpy/scipy): use `zx-procgen:procedural-sounds`
  - For quick SFX generation: use `zx-procgen:/generate-sfx`

  See `docs/audio-pipeline.md` for complete workflow.
version: 1.2.0
---

# Sound Effects Design

Game SFX communicate information, provide feedback, and enhance immersion. Every sound must serve a purpose.

> **Note:** Tables below show CONVENTIONAL patterns as starting points, not rules.
> Your project's audio style guide or creative direction ALWAYS overrides these defaults.
> Distinctive sound design often comes from intentionally breaking expectations.

## Design Philosophy

1. **Functional first**: What information does this sound convey?
2. **Appropriate scale**: Match visual importance
3. **Distinctive**: Sounds must be distinguishable
4. **Non-fatiguing**: Will be heard thousands of times
5. **Mix-aware**: Must work with music and other SFX

---

## Sound Anatomy

Every sound has components:

### Temporal Structure

```
[Attack] [Body] [Tail]

Attack: Initial transient (0-50ms)
Body:   Main sound (50-500ms)
Tail:   Decay/reverb (500ms+)
```

### Frequency Structure

```
High:   Air, detail, definition (4kHz+)
Mid:    Presence, character (500Hz-4kHz)
Low:    Weight, power (20-500Hz)
Sub:    Rumble, impact (20-60Hz)
```

---

## Layering Approach

Complex sounds = multiple simple layers:

### Impact Sound Example

```
Layer 1: Transient (defines hit moment)
  - Short click or thump
  - 10-50ms, no tail
  - Provides timing

Layer 2: Body (defines material)
  - Metal clang, wood thud, flesh slap
  - 50-200ms
  - Provides character

Layer 3: Tail (defines space)
  - Reverb, ring-out
  - 200ms-2s
  - Provides context

Layer 4: Sweetener (optional polish)
  - Debris, rattle, echo
  - Adds realism
```

### Layering Guidelines

| Layer | Frequency Focus | Purpose |
|-------|-----------------|---------|
| 1 | High | Definition, timing |
| 2 | Mid | Character, identity |
| 3 | Low | Weight, power |
| 4 | Full | Texture, detail |

---

## Sound Categories

### Impacts

Collisions between objects.

**Design Variables:**
- Material (metal, wood, stone, flesh)
- Mass (heavy = lower, slower; light = higher, faster)
- Velocity (fast = louder, more transient)
- Surface (hard = ringy; soft = thuddy)

**Templates:**

| Impact Type | Attack | Body | Tail | Example |
|-------------|--------|------|------|---------|
| Sword hit | Sharp metallic | Ringing | Short echo | 150ms total |
| Body punch | Thump transient | Fleshy mid | None | 100ms total |
| Explosion | Blast | Low rumble | Long decay | 1-3s total |
| Footstep | Short thud | Material body | Room tail | 200ms total |
| Menu click | Crisp click | Minimal | None | 50ms total |

**Material Signatures (Conventional Defaults):**

These reflect real-world acoustic expectations. Subverting them can define your game's unique sonic identity.

| Material | Typical Frequency | Typical Decay | Conventional Feel | Subversion Ideas |
|----------|-------------------|---------------|-------------------|------------------|
| Metal | High mids, resonant | Long ring | Clangy, bright | Dull thud (rusted), silent (magical) |
| Wood | Low mids | Medium | Thuddy, warm | Hollow ring (drums), sharp crack (dry) |
| Stone | Wide band | Short | Crunchy, solid | Deep boom (caverns), crystalline (magic) |
| Flesh | Low mids | Short | Thuddy, soft | Wet squelch (gore), silent (stylized) |
| Glass | Very high | Medium | Shatter, tinkle | Deep crunch (thick), musical (chimes) |
| Plastic | Upper mids | Short | Clicky, cheap | Solid thunk (heavy), squeaky (toys) |

---

### Movement Sounds

Whooshes, swipes, and motion.

**Design Variables:**
- Speed (faster = brighter, louder)
- Size (larger = lower, longer)
- Material (air, cloth, blade)
- Direction (pitch can rise/fall)

**Templates:**

| Movement | Duration | Pitch Curve | Character |
|----------|----------|-------------|-----------|
| Fast swing | 100-200ms | Rise or fall | Bright, sharp |
| Slow swing | 300-500ms | Subtle shift | Deeper |
| Arrow fly | 500ms+ | Slight fall | Whistle/hum |
| Cape flutter | Continuous | Rhythmic | Soft, irregular |
| Jump takeoff | 100ms | Rising | Whoosh + effort |
| Landing | 150ms | Falling | Impact + settle |

**Synthesis Approach:**
- Base: Filtered white noise
- Speed mapping: Faster = brighter cutoff (1-4kHz)
- Envelope: Fast attack, medium decay, no sustain
- Optional: Pitch sweep for direction cue

---

### UI/Interface Sounds

Feedback for player actions.

**Design Principles:**
- Instant response (< 50ms latency feel)
- Non-fatiguing (will be heard constantly)
- Appropriate scale (small sounds for small actions)
- Consistent family (all UI sounds related)

**UI Sound Types:**

| Action | Character | Duration | Pitch |
|--------|-----------|----------|-------|
| Hover | Subtle tick | 20-50ms | High |
| Click | Definite thock | 50-100ms | Mid-high |
| Confirm | Positive resolution | 100-200ms | Rising |
| Cancel | Negative/back | 100-150ms | Falling |
| Error | Wrong/blocked | 100-200ms | Dissonant |
| Open menu | Whoosh/reveal | 150-300ms | Rising |
| Close menu | Whoosh/hide | 100-200ms | Falling |
| Notification | Attention grab | 200-500ms | Distinct |
| Slider | Continuous | Ongoing | Tracks value |

**UI Sound Design Tips:**
- Use similar synthesis/instruments across UI
- Click sounds: filtered square wave or recorded click
- Subtle reverb unifies the family
- Avoid pure tones (fatiguing)
- Test at low volume (still audible?)

---

### Ambient/Environmental

Background atmosphere and world sounds.

**Design Principles:**
- Seamless looping
- Non-repetitive (or very long)
- Sets mood without demanding attention
- Layered for depth

**Ambient Categories:**

| Environment | Layers | Key Sounds |
|-------------|--------|------------|
| Forest | 3-4 | Wind, birds, rustling, insects |
| City | 4-5 | Traffic, crowd, sirens, HVAC |
| Cave | 2-3 | Drips, echoes, wind |
| Beach | 3-4 | Waves, wind, gulls, sand |
| Space | 1-2 | Low hum, subtle pings |
| Industrial | 3-4 | Machines, steam, clanks |

**Looping Techniques:**
```
Method 1: Long loop (30-60s)
- Hard to notice repeat
- Larger file size

Method 2: Multiple short layers
- Each layer loops at different length
- Creates variation: 15s + 17s + 21s = ~1 hour before exact repeat

Method 3: Generative
- Random elements triggered
- Never exactly repeats
- Requires runtime processing
```

---

### Creature/Character Sounds

Vocalizations and body sounds.

**Voice Design Variables:**
- Size (larger = lower formants)
- Material (organic, mechanical)
- Emotion (angry, scared, curious)
- Intelligence (speech-like vs. animal)

**Creature Voice Template:**
```
Small creature:
  - High pitch (500Hz+ fundamental)
  - Quick, chattery
  - Squeaks, chirps

Medium creature:
  - Mid pitch (150-300Hz fundamental)
  - Growls, barks, roars
  - Clear emotional reads

Large creature:
  - Low pitch (50-150Hz fundamental)
  - Slow, rumbling
  - Sub-bass elements
  - Long duration
```

**Formant Shifting:**
Adjust formant frequency independent of pitch:
- Formants up: smaller/child-like
- Formants down: larger/monstrous
- Extreme: non-human

---

### Weapon Sounds

Attacks, projectiles, and weapon feedback.

**Weapon Sound Components:**

| Phase | Description | Duration |
|-------|-------------|----------|
| Charge/Ready | Anticipation | 0.2-2s |
| Fire/Swing | Main action | 0.1-0.5s |
| Projectile | Travel sound | Duration of flight |
| Impact | Hit feedback | 0.1-0.5s |
| Tail | Aftermath | 0.2-2s |

**Weapon Type Signatures (Common Patterns):**

| Weapon | Conventional Sound | Typical Character | Alternative Approaches |
|--------|-------------------|-------------------|------------------------|
| Sword | Swoosh + ring | Metallic, sharp | Silent (ninja), heavy thunk (cleaver) |
| Bow | Twang + whoosh | Wooden, airy | Mechanical click (crossbow), silent (stealth) |
| Gun | Explosion + crack | Punchy, mechanical | Suppressed thump, sci-fi pew, vintage pop |
| Magic | Synth + sparkle | Synthetic, ethereal | Organic whoosh, silence, reversed sounds |
| Fist | Thud + whoosh | Fleshy, impact | Exaggerated boom (anime), subtle tap (realism) |
| Laser | Zap + beam | Bright, sustained | Low hum (industrial), crackling (unstable) |

**Punch/Power Guidelines:**
- Layer low frequency for weight
- Sharp transient for definition
- Compression for punch
- Saturation for aggression

---

## Frequency Allocation

Avoid sounds masking each other:

### Mix Slot Strategy

```
Slot 1 (Sub: 20-80Hz):     Reserved for music bass, explosions
Slot 2 (Bass: 80-250Hz):   Weapon body, footsteps, UI low
Slot 3 (Low-Mid: 250-500Hz): Voices, instruments, body of sounds
Slot 4 (Mid: 500-2kHz):    Primary information, clarity
Slot 5 (High-Mid: 2-6kHz): Presence, attack, detail
Slot 6 (High: 6kHz+):      Air, sparkle, sibilance
```

### Priority-Based EQ

| Sound Type | Boost | Cut | Reason |
|------------|-------|-----|--------|
| Dialogue | 2-4kHz | 200-400Hz | Clarity |
| Footsteps | 100-300Hz | 4kHz+ | Weight, not piercing |
| Weapons | 2-5kHz | Varies | Presence |
| UI | 1-3kHz | Below 200Hz | Clear, not boomy |
| Ambient | Full range | 2-4kHz | Background, not forward |

---

## Technical Considerations

### File Formats

| Format | Use Case | Quality |
|--------|----------|---------|
| WAV 16-bit | Master/archive | Lossless |
| WAV 22kHz | Retro consoles | Good |
| OGG | Long sounds | Lossy but small |
| ADPCM | Console SFX | 4:1 compression |

### Variation Strategies

Avoid repetition fatigue:

```
Method 1: Multiple variations
- Create 3-5 versions of same sound
- Randomly select at runtime
- Pitch/volume randomization adds more

Method 2: Component randomization
- Store sound components separately
- Combine randomly at runtime
- More variation from less data

Method 3: Real-time parameter variation
- Apply random pitch (±5%)
- Apply random volume (±3dB)
- Apply random filter (±10%)
```

### Memory Budget Planning

```
Sound Category    | Count | Avg Size | Total
------------------|-------|----------|-------
UI                |  20   |   5KB    |  100KB
Footsteps         |  30   |  10KB    |  300KB
Weapons           |  50   |  20KB    | 1000KB
Creatures         |  40   |  30KB    | 1200KB
Ambient (loops)   |  10   | 200KB    | 2000KB
Music (streaming) |   -   |    -     | Stream
```

---

## Additional Resources

- `references/material-library.md` - Material sound signatures
- `references/layering-recipes.md` - Layer combinations
- `references/foley-techniques.md` - Recording real sounds
