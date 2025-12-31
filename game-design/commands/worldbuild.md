---
description: Interactive world building wizard that guides through designing a game world
argument-hint: "[scope]"
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# World Building Wizard

Guide the user through designing their game world interactively. Create a structured world design document.

## Arguments

- `scope` (optional): "small", "medium", or "large"
  - small: Contained world (single location)
  - medium: Regional world (3-5 connected areas)
  - large: Expansive world (multiple regions)

## Process

1. **Determine scope** (if not provided):
   - Ask about project size, team size, target playtime
   - Recommend appropriate scope based on constraints

2. **Establish identity**:
   - World hook: "A world where [X] means [Y]"
   - Core tension: What conflict defines this world?
   - Tone and atmosphere

3. **Design geography**:
   - Main areas/locations
   - Connections between areas
   - Landmarks for navigation
   - Boundaries of the world

4. **Define inhabitants**:
   - Factions (2-4 recommended)
   - Key NPCs
   - Player's role in the world

5. **Establish rules**:
   - What's possible/impossible
   - Magic/technology level
   - Time systems (if any)

6. **Consistency check**:
   - Review for internal logic
   - Identify potential contradictions
   - Note areas needing detail

## Output

Create `docs/design/world-design.md` with:

```markdown
# World Design: [Game Name]

## World Identity
- Hook: [One sentence]
- Core tension: [Description]
- Tone: [Keywords]

## Geography
[Map/description of areas]

## Factions
[Faction details]

## World Rules
[Consistency rules]

## Open Questions
[Areas needing further design]
```

## Tips

- Start simple, expand as needed
- Focus on what players will interact with
- Every location should serve gameplay purpose
- Factions should create player choices
- Consistency matters more than complexity
