---
description: Interactive wizard to design music tracks for a game, producing composition specifications in conversation context.
argument-hint: "[track name or context, e.g., 'main theme' or 'boss battle']"
allowed-tools:
  - Read
  - Glob
  - AskUserQuestion
  - Task
---

# Design Soundtrack

Guide the user through designing a music track, producing a detailed composition specification.

## Initial Context

1. Check for existing sonic identity (`.studio/sonic-identity.md`)
   - If exists, load and reference it
   - If not, suggest running `/establish-sonic-identity` first, or proceed with questions

2. Parse the argument for track context:
   - "main theme" → Title/menu music
   - "boss battle" → Intense combat
   - "exploration" → Background ambience
   - etc.

## Process Overview

1. **Define Purpose** - What is this track for?
2. **Set Mood** - What should players feel?
3. **Establish Parameters** - Tempo, key, structure
4. **Select Instruments** - What sounds to use
5. **Design Structure** - Song form and sections
6. **Configure Adaptivity** - If interactive music
7. **Output Specification** - Create composition doc

## Phase 1: Define Purpose

Ask: "What is this music for?"

Options:
- Main menu / Title screen
- Gameplay - Exploration
- Gameplay - Combat
- Gameplay - Stealth
- Boss encounter
- Cutscene / Story
- Victory / Achievement
- Defeat / Game over
- Credits
- Other: [describe]

Based on selection, note:
- **Loop requirement** (menu/gameplay = looping, cutscene = linear)
- **Typical duration** (menu: 60-180s loop, gameplay: 30-120s loop)
- **Energy level** (low/medium/high)

## Phase 2: Set Mood

If sonic identity exists, present relevant moods from palette.

Ask: "What primary mood should this track convey?"

Then: "Any secondary mood to layer in?"

For each mood, load the mood-parameters from audio style skill reference.

## Phase 3: Establish Parameters

Based on mood, suggest parameters:

**Consult** `sonic-style-language:references/mood-parameters.md` for mood→tempo/key/dynamics mappings.

Ask: "Here are suggested parameters based on [Mood]. Adjust as needed:"
- **Tempo**: Suggest BPM range from mood reference
- **Key**: Major (positive), Minor (tense), Modal (mysterious)
- **Time Signature**: 4/4, 3/4, 6/8, 5/4, 7/8
- **Duration**: Short (30-60s), Medium (60-120s), Long (120-180s), Linear (cutscenes)

## Phase 4: Select Instruments

Reference sonic identity if available.

Ask: "Based on your [Style] direction, here are instrument suggestions:"

Present categorized options:

**Melodic (lead):**
- [List relevant instruments from palette]
- "Which should carry the melody?"

**Harmonic (chords/pads):**
- [List options]
- "Which for harmonic foundation?"

**Rhythmic (percussion):**
- [List options]
- "What drives the rhythm?"

**Textural (atmosphere):**
- [List options]
- "Any atmospheric elements?"

Allow multiple selections per category.

## Phase 5: Design Structure

Based on track purpose, suggest structure:

**Consult** `music-composition:references/genre-templates.md` for purpose-specific structures (gameplay, menu, combat, boss).

Present appropriate template with section names and bar counts. Ask: "Does this structure work, or would you like to modify it?"

## Phase 6: Configure Adaptivity (Optional)

Ask: "Should this track respond to gameplay?"

If yes, **consult** `music-composition:references/adaptive-patterns.md` for:
- **Vertical layering**: Controllable layer configurations
- **Horizontal resequencing**: Section pool and transition rules
- **Parameter mapping**: Gameplay values → music parameters

## Phase 7: Output Specification

Present the composition specification in the conversation. Do NOT write to a file - the specification stays in context for immediate use by song-generator.

**Present this specification:**

```
# Music Specification: [Track Name]

## Overview
- **Purpose:** [What this track is for]
- **Duration:** [Length, loop point if applicable]
- **Mood:** [Primary] + [Secondary]
- **Reference:** [Any reference tracks/games]

## Musical Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Tempo | [BPM] | [Fixed or range] |
| Key | [Key] | [May modulate to...] |
| Time Signature | [Time sig] | |
| Mode | [Mode] | [Character] |

## Chord Progression

### Section A (Main)
```
| Am | F | C | G |
```
(Fill in actual chords based on the key and mood selected)

### Section B (Variation)
```
| Dm | Am | E | Am |
```
(Variation typically introduces new harmonic movement)

## Instrumentation

### Lead/Melody
- [Instrument]: [Role]

### Harmony
- [Instrument]: [Role]

### Rhythm
- [Instrument]: [Role]

### Texture
- [Instrument]: [Role]

## Structure

```
[Section diagram]

Section:  | Intro | A    | B    | A'   |
Bars:     | 4     | 8    | 8    | 8    |
Intensity:| Low   | Med  | High | Med  |
```

### Section Details

**Intro:**
- [Description of intro]
- Instruments: [List]
- Purpose: [Build anticipation, set mood, etc.]

**Section A:**
- [Description]
- Instruments: [List]
- Melodic content: [Describe]

**Section B:**
- [Description]
- What changes: [List]

## Loop Design

- **Loop point:** After bar [X]
- **Returns to:** Bar [Y] (Section [Z])
- **Transition notes:**
  - Last chord should lead to first
  - [Any special considerations]

## Adaptivity (if applicable)

### Layers
| Layer | Content | Trigger |
|-------|---------|---------|
| Base | [Content] | Always |
| [Layer 2] | [Content] | [Condition] |

### Parameters
| Gameplay Value | Controls | Range |
|----------------|----------|-------|
| [Value] | [What it affects] | [Range] |

## Mix Notes

- [Any special mixing considerations]
- [Priority relative to other sounds]
- [Reverb/processing notes]

## Implementation Notes

- [File format requirements]
- [Integration specifics]
- [Testing considerations]

---
*Generated by sound-design plugin*
```

After presenting, summarize and offer next steps:

"**Music Design Complete!**

**Summary:**
- [Tempo] BPM in [Key]
- [Duration] with loop at [point]
- Instruments: [List]
- Mood: [Mood description]

**Ready to generate?**
The `song-generator` agent can create a playable tracker file (.xm/.it) from this design.

Would you like me to:
- Generate the track now? (spawns song-generator with this spec)
- Design another track first?
- Design sound effects instead?"

**If user wants to generate:**
Use Task tool with subagent_type: "tracker-music:song-generator"
Pass the full specification from this conversation as context.
