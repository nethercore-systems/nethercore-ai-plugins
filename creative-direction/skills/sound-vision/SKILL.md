---
name: Sound Vision
description: This skill should be used when the user asks about "sound direction", "audio style", "sonic identity", "music style", "SFX design", "audio mixing", "soundscape", "audio coherence", "audio design document", or discusses establishing or reviewing the audio direction of a game. Provides comprehensive audio direction framework for defining and maintaining sonic coherence.
version: 1.0.0
---

# Sound Vision

Establish and maintain sonic coherence across all game audio through a systematic sound direction framework.

## Core Principles

### The Three Pillars of Game Audio

1. **Music** - Emotional backbone, pacing, identity
2. **Sound Effects (SFX)** - Feedback, world-building, immersion
3. **Voice/Dialogue** - Narrative, character, instruction

These pillars must work in harmony. When one dominates inappropriately, the soundscape fails.

### Sonic Identity

Every game has a sonic fingerprint defined by:

**Frequency Balance**
- Where does the mix sit? (Bassy, mid-heavy, airy)
- What frequencies define the identity?

**Texture Palette**
- Synthetic vs organic sounds
- Clean vs distorted/processed
- Wet (reverb) vs dry

**Dynamic Range**
- Compressed (consistent loudness) vs dynamic (quiet-to-loud variation)
- How much "loudness room" for impacts?

**Temporal Feel**
- Tight, punchy attacks vs smooth, gradual onsets
- Sustain characteristics

## Audio Design Document Structure

Create an audio design document with these sections:

### 1. Audio Pillars

Define 3-5 sonic principles:

```
Example pillars:
- "Punchy, responsive feedback for all player actions"
- "Organic, living world sounds—nothing synthetic"
- "Music ebbs with exploration, surges with combat"
- "Silence is a design tool, not a mistake"
```

### 2. Reference Audio

Collect audio references that capture target aesthetic:
- Games with similar sonic identity
- Films with relevant soundscapes
- Music genres/artists for tone
- Real-world recordings for texture

### 3. Frequency Allocation

Assign frequency ranges to elements:

```
Sub Bass (20-60Hz):     Impacts, explosions, tension drones
Bass (60-250Hz):        Music bass, footsteps weight
Low Mids (250-500Hz):   Body of sounds, warmth
Mids (500Hz-2kHz):      Dialogue, main melodic content
High Mids (2-6kHz):     Presence, attack, clarity
Highs (6-20kHz):        Air, sparkle, detail
```

### 4. Dynamic Hierarchy

Priority system for mix decisions:

```
PRIORITY 1 (Never duck)
├── Player damage/death feedback
├── Critical gameplay cues
└── Dialogue (when present)

PRIORITY 2 (Light ducking)
├── Player action feedback
├── Immediate threat sounds
└── Important UI feedback

PRIORITY 3 (Duck for Priority 1-2)
├── Ambient world sounds
├── Background music
└── Environmental effects

PRIORITY 4 (Most flexible)
├── Atmospheric layers
├── Distant sounds
└── Non-essential detail
```

### 5. Music Direction

Define music approach:
- **Instrumentation palette**: What instruments define the sound?
- **Genre influences**: What musical styles inform the score?
- **Adaptive music strategy**: How does music respond to gameplay?
- **Silence usage**: When is no music appropriate?

### 6. SFX Design Language

Define sound effect characteristics:
- **Attack style**: Snappy vs gradual
- **Decay behavior**: Quick cutoff vs natural tail
- **Processing aesthetic**: Clean, distorted, filtered, etc.
- **Layering approach**: Minimal vs dense

## Coherence Assessment

When reviewing audio for coherence, check:

### Consistency
- Do all sounds share the same reverb space?
- Is the processing aesthetic consistent?
- Does the texture palette align across categories?

### Mix Balance
- Can player actions be heard clearly?
- Does music support without overwhelming?
- Are frequencies fighting or complementing?

### Emotional Alignment
- Does the audio reinforce intended mood?
- Do transitions feel natural?
- Is the energy level appropriate for gameplay?

### Feedback Clarity
- Are player actions acknowledged instantly?
- Can threats be identified by sound?
- Is UI audio distinct and learnable?

## Mixing Guidelines

### Relative Loudness Targets

```
Reference: Music at comfortable level = 0dB

Player Actions:       +2 to +6dB (always audible)
Enemy Attacks:        +0 to +4dB (threat presence)
Ambient/Environment:  -6 to -12dB (support layer)
UI Feedback:          +0 to +3dB (clear but not harsh)
Dialogue:             +6 to +10dB (intelligibility)
```

### Spatial Audio

Define spatial audio rules:
- What sounds are positional?
- What sounds are non-diegetic (no position)?
- Distance attenuation curve
- Occlusion behavior

### Compression Philosophy

- **Gameplay clarity**: Compress for consistency if needed
- **Dynamic range**: Preserve dynamics for cinematic moments
- **Platform considerations**: Mobile needs more compression

## ZX-Specific Considerations

For Nethercore ZX games:

**Channel Budget**
- 8 SFX channels maximum
- 4 music channels typical
- Plan for channel stealing

**Sample Rate/Quality**
- Balance file size vs quality
- Consistent sample rates
- Appropriate bit depth

**Procedural Audio**
- Consider procedural variation
- Pitch randomization ranges
- Timing variations

## Director Notes Format

When providing sound direction feedback, structure notes as:

```
AUDIO CHECK: [Area/System being reviewed]

ALIGNMENT:
- [What aligns with audio design document]

ISSUES:
- [What deviates from established direction]

RECOMMENDATIONS:
1. [Specific actionable adjustment]
2. [Priority: High/Medium/Low]

MIX NOTES:
- [Frequency conflicts]
- [Level imbalances]
- [Spatial concerns]
```

## Establishing Sound Direction

For new projects, run the vision establishment workflow:

1. **Define emotional targets** - What should players feel?
2. **Collect references** - 5-10 audio examples
3. **Define pillars** - Write 3-5 sonic principles
4. **Set frequency allocation** - Assign ranges to elements
5. **Establish priorities** - Dynamic hierarchy
6. **Create temp mix** - Test with placeholder audio
7. **Document decisions** - Audio design document

Store decisions in `.studio/creative-direction.local.md` for session persistence.

## Additional Resources

### Reference Files

For detailed guidance on specific topics:
- **`references/mixing-techniques.md`** - Technical mixing approaches
- **`references/adaptive-music.md`** - Dynamic music implementation
- **`references/sound-categories.md`** - SFX categorization and design

### ZX Integration

For ZX games, consult the procedural audio skills in `nethercore-zx-procgen`:
- Procedural sound generation
- Audio format specifications
- Channel management
