---
name: Sonic Style Language (SSL)
description: This skill should be used when the user asks about "sonic style", "audio style", "sound palette", "instrument palette", "mood palette", "audio direction", "sonic identity", "what should my game sound like", "audio aesthetic", "sound design direction", "SSL spec", "sonic tokens", "audio coherence", or wants to translate creative intent ("dark fantasy audio", "retro arcade sounds", "cinematic sci-fi") into structured audio specifications. Provides the Sonic Style Language for bridging creative audio descriptions and implementation.
version: 1.0.0
---

# Sonic Style Language (SSL)

SSL bridges creative audio intent and sound implementation. Instead of guessing synthesis parameters or instrument choices, describe your audio semantically and translate to concrete specifications.

## Core Concepts

SSL has five pillars:

1. **Sonic Styles** - Overall audio aesthetic (Orchestral, Chiptune, Industrial)
2. **Mood Palettes** - Emotional character (Tense, Triumphant, Mysterious)
3. **Instrument Palettes** - Sound source categories (brass.fanfare, synth.pad)
4. **Sound Archetypes** - Functional sound types (impact, stinger, ambience)
5. **Processing Signatures** - Effect character (reverb.cathedral, distortion.warm)

These combine into **Sonic Specifications** - structured bundles that ensure audio coherence.

---

## Sonic Styles

Sonic styles define the overall audio aesthetic. Each style implies instrument families, processing approaches, and compositional tendencies.

### Style Definitions

| Style | Character | Typical Instruments | Processing | Use For |
|-------|-----------|---------------------|------------|---------|
| **Orchestral** | Rich, cinematic, emotional | Strings, brass, woodwinds, percussion | Reverb, natural dynamics | RPGs, adventure, drama |
| **Chiptune** | Retro, limited, nostalgic | Square, triangle, noise, pulse | Minimal, dry | Retro games, pixel art |
| **Electronic** | Modern, synthetic, clean | Synth pads, leads, drums | Compression, sidechaining | Sci-fi, racing, modern |
| **Industrial** | Harsh, mechanical, aggressive | Metal hits, distorted synths, noise | Distortion, compression | Horror, action, dystopia |
| **Ambient** | Atmospheric, sparse, evolving | Pads, drones, textures | Heavy reverb, delay | Exploration, puzzle, calm |
| **Acoustic** | Natural, warm, organic | Guitar, piano, strings, percussion | Light reverb, natural | Indie, folk, cozy |
| **Hybrid** | Blended, layered, modern | Orchestra + electronics | Mixed processing | AAA, epic, blockbuster |
| **Lo-Fi** | Degraded, warm, nostalgic | Filtered samples, vinyl noise | Filtering, saturation | Chill, nostalgic, stylized |
| **Dark Ambient** | Unsettling, sparse, tense | Drones, dissonance, textures | Heavy reverb, modulation | Horror, mystery, tension |
| **Synthwave** | 80s, neon, driving | Analog synths, arpeggios, drums | Chorus, gated reverb | Retro-futurism, action |

### Style Modifiers

Styles can be modified with intensity and era:

```
Style: Orchestral
Intensity: Epic (full orchestra) | Chamber (small ensemble) | Solo (single instrument)
Era: Classical | Romantic | Modern | Contemporary

Style: Electronic
Intensity: Minimal | Standard | Maximal
Era: 80s | 90s | 2000s | Modern

Style: Chiptune
Intensity: Pure (4 channels) | Extended (8+ channels) | Hybrid (with samples)
Era: 8-bit | 16-bit | Modern retro
```

---

## Mood Palettes

Mood palettes define emotional character through musical parameters.

### Mood Definitions

| Mood | Key Tendency | Tempo Range | Dynamics | Harmonic Character |
|------|--------------|-------------|----------|---------------------|
| **Triumphant** | Major | 100-140 BPM | Loud, building | Consonant, resolved |
| **Tense** | Minor/diminished | 80-120 BPM | Building, unstable | Dissonant, unresolved |
| **Mysterious** | Modal (Dorian, Phrygian) | 60-90 BPM | Soft, sparse | Ambiguous, suspended |
| **Melancholic** | Minor | 60-80 BPM | Soft, sustained | Minor 7ths, descending |
| **Aggressive** | Minor/chromatic | 140-180 BPM | Loud, driving | Tritones, power chords |
| **Peaceful** | Major/Lydian | 60-80 BPM | Soft, gentle | Open voicings, diatonic |
| **Playful** | Major | 120-160 BPM | Bouncy, staccato | Major 7ths, chromatic runs |
| **Epic** | Major/minor | 80-120 BPM | Building to loud | Suspended, resolved |
| **Eerie** | Locrian/whole-tone | 40-70 BPM | Sparse, sudden | Clusters, microtones |
| **Heroic** | Major | 100-130 BPM | Bold, marcato | Fanfare, perfect intervals |
| **Nostalgic** | Major/minor mix | 70-100 BPM | Soft, wistful | 7ths, suspensions |
| **Frantic** | Minor/chromatic | 160-200 BPM | Loud, chaotic | Chromatic, unpredictable |

### Mood Combinations

Moods can layer for complexity:

```
Primary Mood: Tense (drives the core feeling)
Secondary Mood: Mysterious (colors the tension)
Result: Unresolved harmonies + sparse textures + building dynamics
```

---

## Instrument Palettes

Instrument palettes organize sounds into families with variants.

### Palette Structure

```
Category.Family.Variant

Examples:
  orchestral.strings.epic
  synth.pad.warm
  percussion.electronic.punchy
  sfx.impact.heavy
```

### Orchestral Palette

| Family | Variants | Character |
|--------|----------|-----------|
| **strings** | epic, intimate, tremolo, pizzicato, solo | Emotional, sustaining |
| **brass** | fanfare, dark, muted, solo.horn, solo.trumpet | Powerful, heroic |
| **woodwinds** | ensemble, solo.flute, solo.oboe, solo.clarinet | Lyrical, pastoral |
| **percussion** | timpani, snare, cymbals, glockenspiel, marimba | Rhythmic, accents |
| **choir** | ethereal, powerful, whispered, solo | Emotional, human |
| **harp** | glissando, arpeggiated, sustained | Magical, transitional |

### Synthetic Palette

| Family | Variants | Character |
|--------|----------|-----------|
| **pad** | warm, cold, evolving, digital, analog | Sustaining, atmospheric |
| **lead** | saw, square, fm, supersaw, mono | Melodic, cutting |
| **bass** | sub, wobble, reese, 808, fm | Low-end, driving |
| **arp** | plucky, smooth, sequenced, random | Rhythmic, textural |
| **drums** | 808, 909, digital, processed, acoustic | Rhythmic backbone |
| **fx** | riser, sweep, impact, whoosh, glitch | Transitional, accent |

### Acoustic Palette

| Family | Variants | Character |
|--------|----------|-----------|
| **piano** | grand, upright, felt, prepared, electric | Harmonic, melodic |
| **guitar** | acoustic, electric.clean, electric.distorted, nylon | Harmonic, rhythmic |
| **bass** | upright, electric, slap, picked | Low-end foundation |
| **percussion** | kit, hand, world, found | Rhythmic variety |

### Retro Palette

| Family | Variants | Character |
|--------|----------|-----------|
| **square** | 12.5%, 25%, 50%, 75% | Hollow, clear |
| **triangle** | pure, curved | Soft, bass |
| **noise** | white, periodic, metallic | Texture, percussion |
| **pulse** | modulated, fixed | Dynamic, lead |
| **sample** | lo-fi, crunchy, clean | Realistic but limited |

---

## Sound Archetypes

Sound archetypes define functional sound categories with expected characteristics.

### Music Archetypes

| Archetype | Function | Duration | Character |
|-----------|----------|----------|-----------|
| **theme** | Main identity | 60-180s | Memorable, complete |
| **loop** | Background | 30-120s | Seamless, unobtrusive |
| **stinger** | Moment emphasis | 1-5s | Impactful, resolved |
| **transition** | Scene change | 2-10s | Bridging, morphing |
| **ambient** | Atmosphere | 60-300s | Evolving, textural |
| **combat** | Action music | 60-180s | Driving, intense |
| **victory** | Success | 3-15s | Triumphant, resolved |
| **defeat** | Failure | 3-10s | Descending, minor |
| **menu** | UI background | Infinite loop | Non-intrusive, branded |

### SFX Archetypes

| Archetype | Function | Duration | Character |
|-----------|----------|----------|-----------|
| **impact** | Collision/hit | 0.1-0.5s | Punchy, transient |
| **whoosh** | Movement/swipe | 0.2-0.8s | Sweeping, velocity |
| **pickup** | Collection | 0.2-0.5s | Positive, ascending |
| **ui.click** | Button press | 0.05-0.1s | Clean, responsive |
| **ui.hover** | Mouse over | 0.05-0.1s | Subtle, feedback |
| **ui.error** | Invalid action | 0.1-0.3s | Negative, blocked |
| **footstep** | Movement | 0.1-0.3s | Material-dependent |
| **ambient.loop** | Environment | Infinite | Textural, unobtrusive |
| **voice.effort** | Character action | 0.1-0.5s | Human, emotive |
| **explosion** | Destruction | 0.5-2s | Layered, powerful |
| **magic** | Spell/ability | 0.3-1.5s | Synthetic, otherworldly |

---

## Processing Signatures

Processing signatures define the effect character applied to sounds.

### Reverb Signatures

| Signature | Character | Decay | Use For |
|-----------|-----------|-------|---------|
| **reverb.none** | Dry, intimate | 0s | Chiptune, close sounds |
| **reverb.room** | Natural, small | 0.3-0.8s | Acoustic, realistic |
| **reverb.hall** | Spacious, concert | 1.5-3s | Orchestral, epic |
| **reverb.cathedral** | Massive, ethereal | 4-10s | Ambient, sacred |
| **reverb.plate** | Bright, musical | 1-2s | Vocals, snares |
| **reverb.spring** | Metallic, vintage | 0.5-1.5s | Lo-fi, retro |

### Distortion Signatures

| Signature | Character | Use For |
|-----------|-----------|---------|
| **distortion.none** | Clean | Most sounds |
| **distortion.warm** | Subtle saturation | Warmth, presence |
| **distortion.crunch** | Moderate overdrive | Rock, aggression |
| **distortion.heavy** | Aggressive clipping | Metal, industrial |
| **distortion.bitcrush** | Digital degradation | Retro, glitch |
| **distortion.tape** | Analog warmth | Lo-fi, vintage |

### Filter Signatures

| Signature | Character | Use For |
|-----------|-----------|---------|
| **filter.lowpass.warm** | Remove highs, warm | Distance, muffled |
| **filter.lowpass.telephone** | Narrow band | Radio, phone |
| **filter.highpass.thin** | Remove lows | Tinny, small |
| **filter.bandpass.nasal** | Mid-focused | Voice effect |
| **filter.notch** | Remove specific freq | Problem solving |

---

## Sonic Specification Format

Combine all elements into a complete Sonic Specification:

```yaml
# Sonic Specification
game: "Dark Fantasy RPG"
version: 1.0

identity:
  tagline: "Ancient evil awakens in a dying world"
  audio_pillars:
    - "Orchestral grandeur with dark undertones"
    - "Environmental storytelling through ambience"
    - "Combat that feels weighty and consequential"

style:
  primary: Orchestral
  secondary: Dark Ambient
  intensity: Epic
  era: Modern

mood:
  exploration: Mysterious + Melancholic
  combat: Aggressive + Epic
  story: Tense + Triumphant (resolution)
  menu: Mysterious

instruments:
  primary:
    - orchestral.strings.epic
    - orchestral.brass.dark
    - orchestral.choir.ethereal
  accent:
    - orchestral.percussion.timpani
    - orchestral.harp.glissando
  texture:
    - synth.pad.evolving
    - sfx.ambient.wind

music_params:
  tempo_ranges:
    exploration: [60, 80]
    combat: [120, 150]
    boss: [140, 170]
  key_tendencies:
    exploration: ["Dm", "Am", "Em"]
    combat: ["Cm", "Gm", "Fm"]
    victory: ["C", "G", "D"]
  time_signatures:
    primary: "4/4"
    boss: "7/8"  # Unsettling

sfx_character:
  impacts:
    style: "weighty, metallic"
    layers: ["low_thud", "metal_ring", "debris"]
  magic:
    style: "dark, resonant"
    processing: reverb.cathedral
  ui:
    style: "stone, ancient"
    pitch_range: [200, 800]

processing:
  master:
    reverb: reverb.hall
    compression: moderate
  music:
    reverb: reverb.hall
    stereo_width: wide
  sfx:
    reverb: reverb.room
    ducking: true
  ambient:
    reverb: reverb.cathedral
    volume: -12dB

mix_priorities:
  1: player_feedback  # Always audible
  2: dialogue
  3: combat_sfx
  4: music
  5: ambient

adaptive_music:
  layers: ["percussion", "strings", "brass", "full"]
  transitions: crossfade
  combat_intensity: velocity_based
```

---

## Quick Reference Tables

### Genre → Style Mapping

| Game Genre | Primary Style | Secondary Style | Mood Tendency |
|------------|---------------|-----------------|---------------|
| Fantasy RPG | Orchestral | Ambient | Epic, Mysterious |
| Sci-Fi Shooter | Electronic | Hybrid | Aggressive, Tense |
| Horror | Dark Ambient | Industrial | Eerie, Tense |
| Platformer | Chiptune | Acoustic | Playful, Triumphant |
| Racing | Electronic | Synthwave | Aggressive, Frantic |
| Puzzle | Ambient | Lo-Fi | Peaceful, Mysterious |
| Fighting | Hybrid | Industrial | Aggressive, Epic |
| Survival | Dark Ambient | Acoustic | Tense, Melancholic |
| Cozy/Life Sim | Acoustic | Lo-Fi | Peaceful, Nostalgic |
| Roguelike | Synthwave | Chiptune | Tense, Playful |

### Mood → Musical Parameters

| Mood | Key | Tempo | Dynamics | Rhythm |
|------|-----|-------|----------|--------|
| Triumphant | Major | Fast | fff | Marcato |
| Tense | Minor | Medium | mp→ff | Ostinato |
| Mysterious | Modal | Slow | pp-mp | Rubato |
| Aggressive | Minor | Fast | ff | Driving |
| Peaceful | Major | Slow | pp | Legato |
| Epic | Major/Minor | Medium | p→fff | Building |

---

## Additional Resources

- `references/sonic-styles.md` - Detailed style specifications
- `references/instrument-palettes.md` - Complete instrument database
- `references/mood-parameters.md` - Musical parameter mappings
- `references/processing-chains.md` - Effect signal chains
