---
description: Character design worksheet wizard for creating player characters, NPCs, and antagonists
argument-hint: "[type]"
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# Character Design Wizard

Guide the user through designing a game character with structured worksheets.

## Arguments

- `type` (optional): "player", "npc", "antagonist", "party"
  - player: Main playable character
  - npc: Non-player character (ally, merchant, quest giver, etc.)
  - antagonist: Villain or boss character
  - party: Companion or party member design

## Process by Type

### Player Character
1. Role and function in gameplay
2. Abilities and progression
3. Visual design and silhouette
4. Backstory (if defined character)
5. Player expression opportunities

### NPC
1. Function (merchant, quest giver, ally, etc.)
2. Location and availability
3. Personality (3 traits + contradiction)
4. Key dialogue/interactions
5. Connection to world/factions

### Antagonist
1. Opposition type (rival, tyrant, monster, etc.)
2. Motivation stack (surface, true, hidden)
3. Threat level and presence
4. Encounter design (if boss)
5. Resolution (defeat, redemption, etc.)

### Party/Companion
1. Role in gameplay (tank, support, etc.)
2. Relationship to player
3. Personal arc (if any)
4. Unique abilities
5. Personality contrast with other party members

## Output

Create `docs/design/characters/[name].md` with:

```markdown
# Character: [Name]

## Overview
- Type: [Player/NPC/Antagonist/Companion]
- Function: [Primary gameplay function]
- Hook: "[Adjective] [archetype] who [unique trait]"

## Visual Design
- Silhouette elements:
- Color palette:
- Key features:

## Personality
- Traits: [3 adjectives]
- Contradiction: Seems [X] but is [Y]
- Voice: [Speech pattern]

## Gameplay
[Abilities, interactions, or encounter design]

## Notes
[Additional design considerations]
```

## Tips

- Function first, personality second
- One memorable trait beats ten generic ones
- Silhouette test: recognizable from outline?
- Every character should have a reason to exist
