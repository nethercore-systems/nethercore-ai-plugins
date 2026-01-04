---
description: Interactive wizard to establish project creative direction
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
  - Glob
  - Task
argument-hint: "[--art-only|--sound-only|--tech-only|--full]"
---

# Establish Vision Command

Guide the user through establishing creative direction for their project. Create structured direction files in `.studio/` for persistent guidance across sessions.

## Process

### 1. Check Existing Direction

First, check if direction already exists:
- Look for `.studio/creative-direction.md`
- If exists, ask if user wants to update or start fresh

### 2. Determine Scope

Based on arguments or ask user:
- `--full`: Complete direction (all four domains)
- `--art-only`: Just visual direction
- `--sound-only`: Just audio direction
- `--tech-only`: Just technical direction
- No argument: Ask user what to establish

### 3. Creative Vision (if --full or no scope)

Ask user about:
- **Experience Promise**: "In one paragraph, what experience should players have?"
- **Creative Pillars**: "What 3-5 principles are non-negotiable?"
- **Target Audience**: "Who is this game for? Who is it NOT for?"
- **Reference Works**: "What games/films/art inspire this project?"
- **Anti-Patterns**: "What should this game explicitly avoid?"

### 4. Art Direction (if --full or --art-only)

Ask user about:
- **Art Style**: "Describe the visual style (e.g., dark fantasy painterly)"
- **Style Spectrums**: For each spectrum, ask position 1-9:
  - Fidelity: 1=highly stylized → 9=photorealistic
  - Detail: 1=minimal/simple → 9=intricate/complex
  - Saturation: 1=muted/desaturated → 9=vibrant/saturated
  - Contrast: 1=low-key/flat → 9=high-key/dramatic
  - Form: 1=geometric/angular → 9=organic/flowing
  - Line: 1=hard-edge/crisp → 9=soft/blended
- **Color Palette**: "What's the dominant color mood?"
- **Visual Pillars**: "What 3 visual principles must be followed?"

### 5. Sound Direction (if --full or --sound-only)

Ask user about:
- **Sonic Identity**: "Describe the overall sound (e.g., organic ambient)"
- **Music Style**: "What genre/instrumentation for music?"
- **SFX Character**: "How should sound effects feel?"
- **Mix Priority**: "What's most important: gameplay clarity or atmosphere?"
- **Audio Pillars**: "What 3 audio principles must be followed?"

### 6. Tech Direction (if --full or --tech-only)

Ask user about:
- **Architecture Pattern**: "What architecture? (e.g., ECS, component-based)"
- **Determinism**: "Is deterministic execution required? (for rollback netcode)"
- **File Size Limits**: "Max lines per file? (default: 300 soft, 500 hard)"
- **Tech Pillars**: "What 3 technical principles must be followed?"

### 7. Create Direction Files

Based on responses, create **separate direction files** for each domain:

**`.studio/creative-direction.md`** (always created):
```yaml
---
experience_promise: [user input]
creative_pillars:
  - [pillar 1]
  - [pillar 2]
  - [pillar 3]
target_audience: [user input]
avoid_patterns:
  - [anti-pattern 1]
references:
  - [reference work 1]
---

# Creative Vision

[Experience promise paragraph]

## Creative Pillars

1. **[Pillar 1]:** [Description of how it manifests]
2. **[Pillar 2]:** [Description]
3. **[Pillar 3]:** [Description]

## Target Audience

- **Primary:** [Who this is for]
- **Secondary:** [Who else might enjoy]
- **Not For:** [Who should avoid]

## Anti-Patterns

- [What to explicitly avoid]

## Reference Works

- [Game/Film/Art]: [What to draw from it]
```

**`.studio/art-direction.md`** (if --full or --art-only):
```yaml
---
art_style: [user input]
color_palette: [user input]
style_spectrums:
  fidelity: [1-9]
  detail: [1-9]
  saturation: [1-9]
  contrast: [1-9]
  form: [1-9]
  line: [1-9]
visual_pillars:
  - [pillar 1]
  - [pillar 2]
  - [pillar 3]
---

# Art Direction

## Style Description

[Art style description paragraph]

## Style Spectrums

| Spectrum | Value | Description |
|----------|-------|-------------|
| Fidelity | [1-9] | [Stylized ← → Realistic] |
| Detail | [1-9] | [Simple ← → Complex] |
| Saturation | [1-9] | [Muted ← → Vibrant] |
| Contrast | [1-9] | [Low-key ← → High-key] |
| Form | [1-9] | [Geometric ← → Organic] |
| Line | [1-9] | [Hard-edge ← → Soft] |

## Color Palette

- **Dominant:** [Color/mood]
- **Secondary:** [Color/mood]
- **Accent:** [Color/mood]

## Visual Pillars

1. **[Pillar 1]:** [How it manifests visually]
2. **[Pillar 2]:** [How it manifests visually]
3. **[Pillar 3]:** [How it manifests visually]
```

**`.studio/sound-direction.md`** (if --full or --sound-only):
```yaml
---
sonic_identity: [user input]
music_style: [user input]
sfx_character: [user input]
mix_priority: [gameplay-clarity|atmosphere|balanced]
audio_pillars:
  - [pillar 1]
  - [pillar 2]
  - [pillar 3]
---

# Sound Direction

## Sonic Identity

[Overall sound description paragraph]

## Music Style

- **Genre:** [Genre]
- **Instrumentation:** [Key instruments]
- **Mood:** [Emotional character]

## SFX Character

[How effects should feel - punchy, subtle, organic, etc.]

## Mix Priority

1. [Highest priority - e.g., player feedback]
2. [Second priority]
3. [Third priority]

## Audio Pillars

1. **[Pillar 1]:** [How it manifests in audio]
2. **[Pillar 2]:** [How it manifests in audio]
3. **[Pillar 3]:** [How it manifests in audio]
```

**`.studio/tech-direction.md`** (if --full or --tech-only):
```yaml
---
architecture: [user input]
determinism: [required|optional]
file_size_limit: [number]
tech_pillars:
  - [pillar 1]
  - [pillar 2]
  - [pillar 3]
---

# Technical Direction

## Architecture Pattern

[Architecture description - ECS, component-based, etc.]

## Determinism

[Required for rollback netcode / Optional]

## File Size Limits

- **Soft limit:** [X] lines (warning)
- **Hard limit:** [Y] lines (must split)

## Tech Pillars

1. **[Pillar 1]:** [How it manifests in code]
2. **[Pillar 2]:** [How it manifests in code]
3. **[Pillar 3]:** [How it manifests in code]
```

**`.studio/project-status.md`** (always created):
```markdown
# Project Status

Last updated: [date]

## Phase
Current: Setup / Direction Established

## Current Focus
- [ ] Begin implementing core systems

## Notes
Vision established via /establish-vision command.
```

**`.studio/architecture/decisions.md`** (if tech direction):
```markdown
# Architecture Decision Records

| # | Title | Status | Date |
|---|-------|--------|------|
| 1 | Initial Architecture | Accepted | [date] |
```

### 8. Summarize

Display summary of established direction:
- Creative pillars
- Key style choices
- Technical constraints
- Files created

Remind user that directors will now use this direction for coherence checks.

## Tips

- If user is unsure about a question, provide examples
- For style spectrums, explain what each end means
- Reference visual style tokens for ZX projects
- Keep questions conversational, not overwhelming
- Allow "skip" for optional sections
