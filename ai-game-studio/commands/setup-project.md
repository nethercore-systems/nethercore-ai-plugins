---
name: setup-project
description: Complete project setup wizard - GDD, creative vision, and sonic identity in one flow
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
  - Glob
  - Skill
argument-hint: "[--skip-gdd|--skip-vision|--skip-audio|--quick]"
---

# Setup Project Command

Guide the user through complete project foundation setup. Orchestrates all "establish" workflows in the recommended order to create a fully-documented project baseline.

## Overview

This command coordinates:
1. **Game Design Document** (via `/design-game`)
2. **Creative Direction** (via `/establish-vision`)
3. **Sonic Identity** (via `/establish-sonic-identity`)

Each step builds on the previous, creating a coherent project foundation.

## Process

### 1. Check Existing Setup

First, scan for existing project documentation:

```
.studio/
├── creative-direction.local.md   # Creative direction
├── sonic-identity.local.md       # Audio direction (SSL)
├── project-status.md             # Project status tracking
└── architecture/
    └── decisions.md              # ADRs
docs/
└── gdd.md                        # Game Design Document
```

If any exist, ask user:
- "Found existing [X]. Update it, skip it, or start fresh?"

### 2. Determine Scope

Based on arguments:
- `--skip-gdd`: Skip Game Design Document
- `--skip-vision`: Skip creative direction
- `--skip-audio`: Skip sonic identity
- `--quick`: Abbreviated versions of each (fewer questions)
- No arguments: Full setup with all steps

Ask user to confirm the scope before proceeding.

### 3. Game Design Document (First)

**Why first:** Everything else derives from the game concept.

If not skipping GDD:
- Explain: "Let's start by defining what your game IS. This informs all other decisions."
- Invoke the `/design-game` skill/command flow
- Key outputs needed:
  - Game concept and pillars
  - Core mechanics
  - Target platform constraints
  - Multiplayer requirements (affects determinism)
  - Asset requirements (informs procgen)

If `--quick`: Focus on concept, pillars, and constraints only.

### 4. Creative Direction (Second)

**Why second:** Visual and technical direction depends on game concept.

If not skipping vision:
- Explain: "Now let's establish the creative direction - how should the game look, sound, and be built?"
- Invoke the `/establish-vision` command flow
- Reference GDD decisions when asking questions:
  - "Your GDD mentions [genre]. What visual style fits that?"
  - "Your game is [multiplayer]. Determinism is required for rollback."
- Key outputs:
  - Art style and color palette
  - Technical architecture
  - Creative pillars

If `--quick`: Focus on style keywords and key constraints only.

### 5. Sonic Identity (Third)

**Why third:** Audio direction should complement visual direction.

If not skipping audio:
- Explain: "Finally, let's define the sonic identity - how should your game SOUND?"
- Invoke the `/establish-sonic-identity` command flow
- Reference previous decisions:
  - "Your art style is [dark fantasy]. What audio mood matches?"
  - "Your creative pillars include [tension]. How should audio reinforce that?"
- Key outputs:
  - SSL specification
  - Music direction
  - SFX character

If `--quick`: Focus on overall sonic mood and key instruments only.

### 6. Create Project Status

After all steps, create/update `.studio/project-status.md`:

```markdown
# Project Status

Last updated: [date]

## Setup Completed
- [x] Game Design Document
- [x] Creative Direction
- [x] Sonic Identity

## Phase
Current: Foundation Complete - Ready for Implementation

## Next Steps
Based on your GDD, recommended next actions:
1. [ ] Scaffold project with `/new-game [language]`
2. [ ] Generate placeholder assets with `/generate-asset`
3. [ ] Implement core loop prototype

## Quick Reference
- **Concept:** [one-liner from GDD]
- **Art Style:** [from creative direction]
- **Sonic Mood:** [from SSL]
- **Architecture:** [from tech direction]
```

### 7. Summary

Display a comprehensive summary:

```
Project Setup Complete!

GAME: [Title]
[One-line concept]

CREATIVE DIRECTION:
- Art: [style keywords]
- Sound: [mood keywords]
- Tech: [architecture]

PILLARS:
1. [Pillar 1]
2. [Pillar 2]
3. [Pillar 3]

FILES CREATED:
- docs/gdd.md
- .studio/creative-direction.local.md
- .studio/sonic-identity.local.md
- .studio/project-status.md

NEXT: Run `/new-game rust` to scaffold your project.
```

## Tips

- If user seems overwhelmed, offer `--quick` mode
- Reference previous answers to maintain coherence
- For ZX projects, remind about console constraints
- Allow going back to revise earlier sections
- Save progress after each major section (user can resume)

## Error Handling

- If a sub-command fails, save progress and allow retry
- If user wants to stop mid-way, save partial progress
- Mark incomplete sections in project-status.md
