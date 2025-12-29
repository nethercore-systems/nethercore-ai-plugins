---
description: Interactive wizard to establish project creative direction
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
  - Glob
argument-hint: "[--art-only|--sound-only|--tech-only|--full]"
---

# Establish Vision Command

Guide the user through establishing creative direction for their project. Create structured direction files in `.studio/` for persistent guidance across sessions.

## Process

### 1. Check Existing Direction

First, check if direction already exists:
- Look for `.studio/creative-direction.local.md`
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
  - Fidelity (stylized ↔ realistic)
  - Detail (simple ↔ complex)
  - Saturation (muted ↔ vibrant)
  - Contrast (low-key ↔ high-key)
  - Form (geometric ↔ organic)
  - Line (hard-edge ↔ soft)
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

Based on responses, create:

**`.studio/creative-direction.local.md`** with YAML frontmatter:
```yaml
---
art_style: [user input]
color_palette: [user input]
style_spectrums:
  fidelity: [1-9]
  saturation: [1-9]
  # ... etc

sonic_identity: [user input]
mix_priority: [user input]

architecture: [user input]
determinism: [required|optional]
file_size_limit: [number]

creative_pillars:
  - [pillar 1]
  - [pillar 2]
  - [pillar 3]

target_audience: [user input]
avoid_patterns:
  - [anti-pattern 1]
---

# Project Vision

[Experience promise paragraph]

# Art Direction Notes

Direction established on [date].
- [Key art decisions noted]

# Sound Direction Notes

Direction established on [date].
- [Key sound decisions noted]

# Tech Direction Notes

Direction established on [date].
- [Key tech decisions noted]
```

**`.studio/project-status.md`**:
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

### 8. Add to .gitignore

Add `.studio/*.local.md` to `.gitignore` if not already present.

### 9. Summarize

Display summary of established direction:
- Creative pillars
- Key style choices
- Technical constraints
- Files created

Remind user that directors will now use this direction for coherence checks.

## Tips

- If user is unsure about a question, provide examples
- For style spectrums, explain what each end means
- Reference SADL style tokens for ZX projects
- Keep questions conversational, not overwhelming
- Allow "skip" for optional sections
