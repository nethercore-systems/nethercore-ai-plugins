---
description: Interactive wizard to establish the overall audio direction for a game project. Creates a audio style guide specification.
argument-hint: "[game name or concept]"
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
  - Task
---

# Establish Sonic Identity

Guide the user through creating a comprehensive audio style guide specification for their game.

## Process Overview

Walk through these phases to establish audio direction:

1. **Understand the Game** - Genre, setting, mood
2. **Define Sonic Style** - Primary and secondary styles
3. **Establish Mood Palette** - Emotional range
4. **Select Instrument Palettes** - Sound sources
5. **Configure Processing** - Reverb, effects character
6. **Set Mix Priorities** - What's most important
7. **Output Specification** - Create audio style document

## Phase 1: Understand the Game

Ask about the game to inform audio decisions.

**Questions to ask:**

1. "What genre is your game?" (Options: RPG, Action, Horror, Puzzle, Platformer, Racing, Simulation, Other)

2. "What's the setting/aesthetic?" (Options: Fantasy, Sci-Fi, Modern, Historical, Abstract, Post-Apocalyptic, Other)

3. "What's the primary mood you want players to feel?" (Options: Excited, Tense, Peaceful, Mysterious, Heroic, Scared, Playful, Other)

4. "Is there a reference game or media whose audio you admire?"

If a GDD exists (check for `*.gdd.md` or `design/*.md`), offer to read it for context.

## Phase 2: Define Sonic Style

Based on game info, recommend a primary and secondary sonic style.

**Consult** `sonic-style-language:references/sonic-styles.md` for genre→style mappings.

Present recommendation with rationale, then ask:

"Based on your [genre] [setting] game, I recommend **[Primary Style]** with **[Secondary Style]** influences. This will give you [character description]. Does this feel right, or would you prefer a different direction?"

## Phase 3: Establish Mood Palette

Determine the emotional range needed.

Ask: "What moods will your game need to express?"

**Consult** `sonic-style-language:references/mood-parameters.md` for mood options with tempo/key/dynamics mappings.

Present mood checklist from reference. For each selected mood, note the primary game context (e.g., "Tense - during stealth sections").

## Phase 4: Select Instrument Palettes

Based on sonic style, recommend instrument families.

Ask: "Let me suggest instrument families for your [Style] approach. Please confirm or adjust:"

**Consult** `sonic-style-language:references/instrument-palettes.md` for style-specific instrument recommendations.

Present Primary/Accent/Texture instruments based on selected style. Allow user to modify selections.

## Phase 5: Configure Processing

Establish the effect character.

**Consult** `sonic-style-language:references/processing-signatures.md` for reverb types and character options.

Ask about space/environment and overall audio character. Map answers to processing signatures from the reference.

## Phase 6: Set Mix Priorities

Determine what sounds are most critical.

Ask: "Rank these in order of audio importance for your game (1 = most important):"

- Player feedback (damage, actions)
- Dialogue/Voice
- Music
- Combat/Action SFX
- Environmental ambient
- UI sounds

Create priority order from 1 (highest) to 6 (lowest).

## Phase 7: Output Specification

Create the audio style specification document.

**Output location:** `.studio/sonic-identity.md`

**Template:**

```markdown
# Sonic Identity Specification

## Game Overview
- **Title:** [Game name]
- **Genre:** [Genre]
- **Setting:** [Setting]
- **Core Experience:** [1-sentence description]

## Audio Pillars
1. [First pillar - what the audio must achieve]
2. [Second pillar]
3. [Third pillar]

## Sonic Style
- **Primary:** [Style]
- **Secondary:** [Style]
- **Intensity:** [Low/Medium/High]
- **Character:** [Description]

## Mood Palette

| Context | Primary Mood | Secondary Mood |
|---------|--------------|----------------|
| [Context 1] | [Mood] | [Mood] |
| [Context 2] | [Mood] | [Mood] |
...

## Instrument Palette

### Primary Instruments
- [instrument.family.variant]: [Usage]
...

### Accent Instruments
- [instrument.family.variant]: [Usage]
...

### Texture Instruments
- [instrument.family.variant]: [Usage]
...

## Processing Signature

| Element | Setting | Notes |
|---------|---------|-------|
| Reverb Type | [Type] | [Context] |
| Reverb Decay | [Time] | |
| Overall Character | [Description] | |
| Filtering Tendency | [Description] | |

## Mix Priorities

1. **[Priority 1]** - Always audible
2. **[Priority 2]** - Clear and present
3. **[Priority 3]** - Supporting
4. **[Priority 4]** - Background
5. **[Priority 5]** - Atmospheric
6. **[Priority 6]** - Optional

## Music Direction

### Tempo Ranges
| Context | BPM Range |
|---------|-----------|
| Exploration | [Range] |
| Combat | [Range] |
| Menu | [Range] |

### Key Tendencies
| Context | Keys |
|---------|------|
| Positive | [Keys] |
| Negative | [Keys] |
| Neutral | [Keys] |

## SFX Direction

### Impact Character
- Style: [Description]
- Weight: [Light/Medium/Heavy]
- Processing: [Dry/Wet/etc.]

### UI Character
- Style: [Description]
- Family: [Description]

## Reference Audio
- [Reference 1]: [What to take from it]
- [Reference 2]: [What to take from it]

---
*Generated by sound-design plugin*
*Last updated: [Date]*
```

After creating the file, summarize:

"I've created your Sonic Identity specification at `.studio/sonic-identity.md`. This establishes:

- **Style:** [Primary] + [Secondary]
- **Moods:** [List]
- **Instruments:** [Key families]
- **Processing:** [Character]

You can now use this specification with:
- `/design-soundtrack` - Create music specs
- `/design-sfx` - Create sound effect specs
- `sonic-designer` agent - Get asset-specific recommendations

Would you like to proceed with designing specific audio assets?"
