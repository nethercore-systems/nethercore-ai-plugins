---
description: Interactive wizard to establish the visual style for a game project.
argument-hint: "[game name or concept]"
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# Establish Visual Style

Guide the user through creating a visual style specification for their game's assets.

## Process Overview

Walk through these phases to establish visual direction:

1. **Understand the Game** - Genre, setting, aesthetic
2. **Define Style** - Primary visual style
3. **Establish Color Palette** - Color direction
4. **Select Material Preferences** - Surface treatments
5. **Configure Quality Parameters** - Detail level and constraints
6. **Output Specification** - Create style document

## Phase 1: Understand the Game

Ask about the game to inform visual decisions.

**Questions to ask:**

1. "What genre is your game?" (Options: RPG, Action, Horror, Puzzle, Platformer, Racing, Simulation, Other)

2. "What's the setting/aesthetic?" (Options: Fantasy, Sci-Fi, Modern, Historical, Abstract, Post-Apocalyptic, Cartoon, Other)

3. "What's the primary visual mood?" (Options: Dark/Gritty, Bright/Cheerful, Mysterious, Clean/Minimal, Chaotic, Nostalgic, Other)

4. "Is there a reference game or media whose visuals you admire?"

If a GDD or creative-direction exists (check `.studio/`), offer to read it for context.

## Phase 2: Define Style Token

Based on game info, recommend a primary style token.

**Mapping Guide:**

| Genre + Setting | Recommended Style | Character |
|-----------------|-------------------|-----------|
| Fantasy Medieval | Rustic | Weathered wood, aged metal, warm |
| Sci-Fi | Geometric | Clean lines, metallic, precise |
| Horror | Gothic | Dark, decayed, organic |
| Cartoon/Casual | Stylized | Bold colors, simple forms |
| Cyberpunk | Cyberpunk | Neon accents, tech surfaces, grime |
| Post-Apocalyptic | Wasteland | Rust, decay, scavenged |
| Historical | Antique | Patina, craftsmanship, period-accurate |
| Nature/Organic | Organic | Flowing forms, natural colors |
| Abstract/Puzzle | Minimal | Clean, geometric, few colors |

Present recommendation with rationale, then ask:

"Based on your [genre] [setting] game, I recommend the **[Style Token]** style. This gives you [character description]. Does this feel right, or would you prefer a different direction?"

## Phase 3: Establish Color Palette

Determine the color direction.

**Palette Options:**

| Palette | Character | Best For |
|---------|-----------|----------|
| WarmEarthy | Browns, oranges, tans | Medieval, rustic, natural |
| CoolMetal | Blues, grays, silvers | Sci-fi, industrial, tech |
| Neon | Bright pinks, cyans, yellows | Cyberpunk, arcade, futuristic |
| Pastel | Soft, light, desaturated | Cute, dreamy, casual |
| Muted | Grays, desaturated colors | Horror, serious, realistic |
| Vibrant | Saturated, bold colors | Cartoon, fantasy, action |
| Monochrome | Single hue variations | Stylized, noir, abstract |
| Nature | Greens, browns, blues | Outdoor, organic, peaceful |

Ask: "Which color palette best fits your vision? (Or describe your preferred colors)"

## Phase 4: Select Material Preferences

Determine surface treatment preferences.

Ask: "What condition should most surfaces be in?"
- Pristine/New (damage: 0.0)
- Slightly Worn (damage: 0.2)
- Well-Used (damage: 0.4)
- Weathered (damage: 0.6)
- Heavily Damaged (damage: 0.8)

Ask: "What's the dominant material family?"
- **Wood** - Crates, furniture, structures
- **Metal** - Armor, machinery, tech
- **Stone** - Buildings, ruins, natural
- **Organic** - Creatures, plants, flesh
- **Tech** - Screens, panels, circuitry
- **Mixed** - Varied based on context

For each selected family, note variant preference (e.g., "metal.rusted" vs "metal.polished").

## Phase 5: Configure Quality Parameters

Set generation constraints.

Ask: "What's your priority balance?"
- **Performance First** - Lower poly, smaller textures (mobile/retro)
- **Balanced** - Standard budgets (default ZX)
- **Quality First** - Higher detail where possible

Map to constraints:
- Performance: poly_budget(50-200), texture_resolution(128)
- Balanced: poly_budget(100-500), texture_resolution(256)
- Quality: poly_budget(200-800), texture_resolution(512)

Ask: "Any specific ZX constraints to note?" (ROM budget concerns, render mode preferences)

## Phase 6: Output Specification

Create the style specification document.

**Output location:** `.studio/visual-style.local.md`

**Template:**

```markdown
# Visual Style Specification

## Game Overview
- **Title:** [Game name]
- **Genre:** [Genre]
- **Setting:** [Setting]
- **Visual Mood:** [1-sentence description]

## Visual Pillars
1. [First pillar - what visuals must achieve]
2. [Second pillar]
3. [Third pillar]

## Style Token
- **Primary:** [Style Token]
- **Damage Level:** [0.0-1.0]
- **Detail Level:** [Low/Medium/High]
- **Edge Hardness:** [0.0-1.0, 0=organic, 1=geometric]

## Color Palette
- **Primary Palette:** [Palette name]
- **Dominant Hues:** [Color descriptions]
- **Accent Colors:** [Accent descriptions]
- **Avoid:** [Colors to avoid]

## Material Preferences

### Primary Materials
| Context | Material | Notes |
|---------|----------|-------|
| [Props] | [material.variant] | [Usage] |
| [Structures] | [material.variant] | [Usage] |
| [Characters] | [material.variant] | [Usage] |

### Surface Treatments
- **Weathering:** [None/Light/Heavy]
- **Wear Patterns:** [Description]
- **Special Effects:** [Glow, transparency, etc.]

## Generation Constraints

### Mesh Budgets
| Asset Type | Poly Range | Notes |
|------------|------------|-------|
| Props | [range] | |
| Characters | [range] | |
| Environment | [range] | |

### Texture Settings
- **Resolution:** [128/256/512]
- **Texel Density:** [pixels per unit]
- **Tiling:** [Requirements]

## Reference Visuals
- [Reference 1]: [What to take from it]
- [Reference 2]: [What to take from it]

## Style Examples

Natural language → style translation for this project:

| Description | Translation |
|-------------|-------------|
| "a barrel" | Style: [token], Material: [mat], Palette: [pal] |
| "a sword" | Style: [token], Material: [mat], Palette: [pal] |
| "a creature" | Style: [token], Material: [mat], Palette: [pal] |

---
*Generated by zx-procgen plugin*
*Last updated: [Date]*
```

After creating the file, summarize:

"I've created your Visual Style specification at `.studio/visual-style.local.md`. This establishes:

- **Style:** [Token]
- **Palette:** [Palette]
- **Materials:** [Key preferences]
- **Constraints:** [Poly/texture budgets]

You can now use this specification with:
- `/generate-asset` - Create assets matching your style
- `asset-designer` agent - Get style-consistent specs
- All procedural generation will reference this file

Would you like to generate some assets using this style?"

## Tips

- If user is unsure, show examples from the style token
- Reference any existing creative-direction for consistency
- For ZX projects, remind about console constraints
- Keep questions conversational
- Allow "skip" for optional sections
