---
description: Interactive wizard to design music tracks for a game, producing detailed composition specifications.
argument-hint: "[track name or context, e.g., 'main theme' or 'boss battle']"
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
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

Ask: "Here are suggested parameters based on [Mood]. Adjust as needed:"

**Tempo:**
"I suggest [X-Y] BPM for [mood]. What feels right?"
- Present slider or specific value

**Key:**
"For [mood], I suggest [key options]. Preference?"
- Major keys for positive
- Minor keys for negative/tense
- Modal for mysterious/exotic

**Time Signature:**
"Standard 4/4, or something different?"
- 4/4 - Standard, comfortable
- 3/4 - Waltz, elegant
- 6/8 - Flowing, compound
- 5/4 or 7/8 - Unsettling, complex

**Duration:**
"How long should the loop be?"
- Short: 30-60 seconds
- Medium: 60-120 seconds
- Long: 120-180 seconds
- Linear: Full length (for cutscenes)

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

**For Looping Gameplay:**
```
[Intro (optional)] → [A] → [B] → [A'] → [Loop]
4 bars             8 bars  8 bars  8 bars
```

**For Menu/Title:**
```
[Fanfare/Intro] → [Main Theme] → [Development] → [Theme Return] → [Loop]
4 bars            16 bars         8 bars          8 bars
```

**For Combat:**
```
[Tension Build] → [Main] → [Intensity] → [Main] → [Loop]
4 bars           8 bars    8 bars        8 bars
```

**For Boss:**
```
[Ominous Intro] → [Phase 1] → [Build] → [Phase 2] → [Desperation] → [Loop]
4 bars           16 bars      4 bars    16 bars      8 bars
```

Ask: "Does this structure work, or would you like to modify it?"

## Phase 6: Configure Adaptivity (Optional)

Ask: "Should this track respond to gameplay?"

If yes, configure:

**Vertical Layering:**
"What layers should be controllable?"
- Percussion layer (add/remove)
- Intensity layer (add for action)
- Melodic layer (add for calm)
- Tension layer (add for danger)

**Horizontal Resequencing:**
"Should the track switch between sections based on game state?"
- Define section pool
- Define transition rules

**Parameters:**
"What gameplay values should affect the music?"
- Health → filter, intensity
- Combat → layers
- Speed → tempo (if flexible)

## Phase 7: Output Specification

Create the composition specification.

**Output location:** `.studio/music/[track-name].spec.md`

**Template:**

```markdown
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
| [Chord] | [Chord] | [Chord] | [Chord] |
```

### Section B (Variation)
```
| [Chord] | [Chord] | [Chord] | [Chord] |
```

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

After creating, summarize and offer next steps:

"Created specification at `.studio/music/[track-name].spec.md`

**Summary:**
- [Tempo] BPM in [Key]
- [Duration] with loop at [point]
- Instruments: [List]
- Mood: [Mood description]

**Next steps:**
1. Use this spec to compose in your DAW/tracker
2. Run `music-architect` agent for deeper composition help
3. After creation, `audio-coherence-reviewer` can validate against sonic identity

Would you like to design another track, or proceed to SFX?"
