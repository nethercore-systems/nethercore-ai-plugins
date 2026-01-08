---
description: Interactive wizard to design sound effects, producing SFX specifications in conversation context for immediate synthesis.
argument-hint: "[sound type, e.g., 'sword swing', 'jump', 'explosion']"
allowed-tools:
  - Read
  - Glob
  - AskUserQuestion
  - Task
---

# Design SFX

Guide the user through designing a sound effect, producing a detailed specification with layering and implementation guidance.

## Initial Context

1. Check for existing sonic identity (`.studio/sonic-identity.md`)
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

**Consult** `sfx-design:references/layering-recipes.md` for category-specific layer templates (impacts, movement, UI, weapons, creatures, ambient).

Present layer template based on sound category. Standard approach uses 3-4 layers:
- **Transient**: Timing, definition (10-50ms)
- **Body**: Character, identity (50-200ms)
- **Tail**: Space, context (200ms+)
- **Sweetener**: Polish (optional)

Ask user to confirm or modify layer approach.

## Phase 5: Configure Synthesis

For each layer, define creation method:

**Method options:**
- Synthesis (generate from scratch)
- Sample (recorded source)
- Hybrid (synth + sample)

**Consult** `sfx-design:references/material-signatures.md` for material-specific frequency/envelope parameters.

For synthesis layers, specify: Waveform, Envelope (ADSR), Filter (type/cutoff/Q), Effects.

## Phase 6: Set Variations

Define randomization for repeated sounds:

Ask: "This sound may play [frequency]. Should it have variations?"

**Consult** `sfx-design:references/variation-strategies.md` for variation types (pre-made, pitch, volume, layer, parameter) with implementation patterns.

For frequent sounds (footsteps, hits), recommend at least pitch + volume randomization (±2 semitones, ±2 dB).

## Phase 7: Output Specification

Present the SFX specification in the conversation. Do NOT write to a file - the specification stays in context for immediate use by sfx-architect.

**Present this specification:**

```
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
| 1 | 0 dB | C | Primary transient |
| 2 | -3 dB | C | Body layer |
| 3 | -6 dB | C | Tail/ambience |

(Fill in actual values based on the designed layers)

### Master Processing
- Compression: [Settings if any]
- EQ: [Adjustments if any]
- Limiting: [Peak target]

## Variations

### Random Parameters
| Parameter | Range | Notes |
|-----------|-------|-------|
| Pitch | ±2 semitones | Natural variation |
| Volume | ±1 dB | Subtle dynamics |

(Adjust ranges based on user preferences from Phase 6)

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

After presenting, summarize and offer next steps:

"**SFX Design Complete!**

**Summary:**
- [Duration] [Category] sound
- [Layer count] layers: [Brief description]
- Variation: [Type]
- Priority: [Level]

**Ready to synthesize?**
The `sfx-architect` agent can create a `.spec.py` file with synthesis code from this design.

Would you like me to:
- Generate the synthesis code now? (spawns sfx-architect with this spec)
- Design another sound effect first?
- Refine this specification?"

**If user wants synthesis code:**
Use Task tool with subagent_type: "sound-design:sfx-architect"
Pass the full specification from this conversation as context.
