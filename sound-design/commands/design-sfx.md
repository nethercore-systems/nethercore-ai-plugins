---
name: design-sfx
description: Interactive wizard to design sound effects, producing detailed SFX specifications with layering and synthesis guidance.
argument-hint: "[sound type, e.g., 'sword swing', 'jump', 'explosion']"
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# Design SFX

Guide the user through designing a sound effect, producing a detailed specification with layering and implementation guidance.

## Initial Context

1. Check for existing sonic identity (`.claude/sonic-identity.md`)
   - If exists, reference for style consistency
   - Note SFX character preferences if defined

2. Parse the argument to identify sound category:
   - Movement: jump, footstep, dash, slide
   - Combat: hit, swing, block, shoot
   - Interaction: pickup, button, lever, door
   - UI: click, hover, confirm, error
   - Environment: ambient, weather, machine
   - Creature: growl, attack, death

## Process Overview

1. **Identify Sound** - What exact sound?
2. **Define Context** - Where/when does it play?
3. **Establish Character** - How should it feel?
4. **Design Layers** - Component breakdown
5. **Configure Synthesis** - How to create each layer
6. **Set Variations** - Random variation parameters
7. **Output Specification** - Create SFX doc

## Phase 1: Identify Sound

Clarify exactly what sound is needed:

Ask: "Let me understand the sound you need. You mentioned '[argument]'. Can you describe:"

1. "What action or event triggers this sound?"
2. "What object/character makes this sound?"
3. "Any specific characteristics? (e.g., 'heavy sword', 'small robot')"

Categorize into archetype:
- Impact (collisions, hits)
- Movement (whoosh, footsteps)
- Action (ability, weapon fire)
- Feedback (pickup, damage)
- UI (interface interaction)
- Ambient (environment)
- Creature (vocalization)

## Phase 2: Define Context

Understand where the sound exists:

Ask: "Where does this sound occur in your game?"

**Spatial context:**
- 2D (side-scroller, UI) - Mono or simple stereo
- 3D positioned - Full spatial audio
- Both - Need versions for each

**Frequency context:**
- One-time (story moment)
- Occasional (special abilities)
- Frequent (every attack)
- Constant (ambient loop)

**Priority:**
Based on sonic identity if exists, or ask:
"How critical is this sound for gameplay?"
- Essential feedback (player damage)
- Important action (player abilities)
- Supporting (enemy actions)
- Background (environment)

## Phase 3: Establish Character

Define how the sound should feel.

Based on sonic identity style, or ask:

"How should this sound feel?"

**For weapons/impacts:**
- Light and quick
- Medium and solid
- Heavy and powerful
- Magical and otherworldly
- Mechanical and precise
- Organic and fleshy

**For movement:**
- Airy and swift
- Weighty and grounded
- Floaty and ethereal
- Sharp and precise

**For UI:**
- Clean and modern
- Warm and organic
- Retro and chunky
- Minimal and subtle

"What material quality?" (if applicable)
- Metal, wood, stone, flesh, magic, digital

## Phase 4: Design Layers

Break down into component layers.

Present layer template based on category:

**For Impact sounds:**
```
Layer 1: Transient (attack)
  - Duration: 10-50ms
  - Character: [click/thump/crack]
  - Provides: Timing, definition

Layer 2: Body (material)
  - Duration: 50-200ms
  - Character: [material sound]
  - Provides: Identity, weight

Layer 3: Tail (space)
  - Duration: 200ms+
  - Character: [reverb/ring/debris]
  - Provides: Context, size

Layer 4: Sweetener (optional)
  - Duration: Variable
  - Character: [extra detail]
  - Provides: Polish, uniqueness
```

**For Movement sounds:**
```
Layer 1: Core whoosh
  - Duration: Based on action speed
  - Character: [filtered noise]
  - Provides: Motion sense

Layer 2: Material (if applicable)
  - Duration: Matching
  - Character: [cloth, metal, etc.]
  - Provides: Physical detail

Layer 3: Pitch movement
  - Curve: Rising/falling/arc
  - Provides: Directionality
```

Ask user to confirm or modify layer approach.

## Phase 5: Configure Synthesis

For each layer, define creation method:

**Method options:**
- Synthesis (generate from scratch)
- Sample (recorded source)
- Hybrid (synth + sample)

For synthesis layers, specify:
- Waveform (sine, saw, square, noise)
- Envelope (attack, decay, sustain, release)
- Filter (type, cutoff, resonance)
- Effects (distortion, pitch shift, modulation)

**Example for "sword swing":**

```
Layer 1: Transient
  Method: Synthesis
  Waveform: Square wave burst
  Envelope: 2ms attack, 10ms decay
  Filter: High-pass at 2kHz
  Purpose: Sharp definition

Layer 2: Whoosh body
  Method: Synthesis
  Waveform: Filtered white noise
  Envelope: 20ms attack, 100ms decay
  Filter: Band-pass 500-3000Hz
  Pitch: Slight downward sweep
  Purpose: Motion sense

Layer 3: Ring
  Method: Synthesis (optional)
  Waveform: Metallic FM
  Envelope: 0ms attack, 200ms decay
  Purpose: Metal character
```

## Phase 6: Set Variations

Define randomization for repeated sounds:

Ask: "This sound may play [frequency]. Should it have variations?"

**Variation types:**

1. **Pre-made variations**
   - Create 3-5 distinct versions
   - Random selection at runtime
   - Most varied, most memory

2. **Pitch randomization**
   - Range: ±[X] semitones (typically ±2)
   - Instant variety, subtle
   - Low memory cost

3. **Volume randomization**
   - Range: ±[X] dB (typically ±2)
   - Natural variation
   - No memory cost

4. **Layerandom ization**
   - Random layer combinations
   - Each play slightly different
   - Medium memory cost

5. **Parameter randomization**
   - Random filter, envelope, etc.
   - Maximum variety
   - Runtime CPU cost

For frequent sounds (footsteps, hits), recommend at least pitch + volume randomization.

## Phase 7: Output Specification

Create the SFX specification.

**Output location:** `.claude/sfx/[sound-name].spec.md`

**Template:**

```markdown
# SFX Specification: [Sound Name]

## Overview
- **Category:** [Impact/Movement/UI/etc.]
- **Trigger:** [What causes this sound]
- **Context:** [Where it plays]
- **Priority:** [1-5]
- **Duration:** [Approximate length]

## Character
- **Feel:** [Description]
- **Weight:** [Light/Medium/Heavy]
- **Material:** [If applicable]
- **Reference:** [Similar sounds in other games]

## Layers

### Layer 1: [Name]
| Property | Value |
|----------|-------|
| Purpose | [What this provides] |
| Method | [Synthesis/Sample/Hybrid] |
| Duration | [Length] |
| Frequency range | [Low/Mid/High] |

**Synthesis details (if applicable):**
- Waveform: [Type]
- Envelope: A:[X]ms D:[X]ms S:[X] R:[X]ms
- Filter: [Type] @ [Frequency], Q=[X]
- Effects: [List]

**Sample details (if applicable):**
- Source: [Description of what to record]
- Processing: [Any processing needed]

### Layer 2: [Name]
[Same structure...]

### Layer 3: [Name]
[Same structure...]

## Mix

### Layering
| Layer | Volume | Pan | Notes |
|-------|--------|-----|-------|
| 1 | [dB] | [C/L/R] | [Notes] |
| 2 | [dB] | [C/L/R] | [Notes] |
| 3 | [dB] | [C/L/R] | [Notes] |

### Master Processing
- Compression: [Settings if any]
- EQ: [Adjustments if any]
- Limiting: [Peak target]

## Variations

### Random Parameters
| Parameter | Range | Notes |
|-----------|-------|-------|
| Pitch | ±[X] semitones | [Notes] |
| Volume | ±[X] dB | [Notes] |
| [Other] | [Range] | [Notes] |

### Pre-made Variations (if applicable)
- Variation A: [Description]
- Variation B: [Description]
- Variation C: [Description]

## Implementation

### Spatial
- **Mode:** [2D/3D/Both]
- **Attenuation:** Min [X]m, Max [X]m
- **Curve:** [Linear/Log/Custom]

### Playback
- **Polyphony:** [Max instances]
- **Priority:** [Steal behavior]
- **Bus:** [Which audio bus]

### Memory
- **Estimated size:** [KB]
- **Load type:** [Resident/Streaming/OnDemand]

## Technical Notes
- [Any special considerations]
- [Integration specifics]
- [Testing notes]

---
*Generated by sound-design plugin*
```

After creating, summarize:

"Created SFX specification at `.claude/sfx/[sound-name].spec.md`

**Summary:**
- [Duration] [Category] sound
- [Layer count] layers: [Brief description]
- Variation: [Type]
- Priority: [Level]

**Next steps:**
1. Create the sound using this spec
2. Use `sfx-architect` agent for synthesis code
3. Test in-game and iterate

Would you like to design another sound effect?"
