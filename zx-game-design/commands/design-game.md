---
description: Interactive GDD builder wizard for Nethercore ZX games
argument-hint: "[perspective]"
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
  - Glob
  - Task
---

# Game Design Document Wizard

Create a Game Design Document for a Nethercore ZX game. Guide the user through a structured design process and output a complete GDD to `docs/design/`.

## Process

### Step 1: Understand the Vision

If no perspective argument provided ($1), ask the user to choose:
- Side-Scroller (2D platformer, fighter, puzzle)
- Top-Down (racing, twin-stick shooter, strategy)
- Third-Person (action-adventure, 3D platformer)
- First-Person (shooter, exploration)

If perspective provided: $1

Gather the core concept:
1. Ask for a one-sentence game pitch
2. Ask for the target player experience (what emotions/feelings?)
3. Ask for 1-2 reference games for inspiration

### Step 2: Validate Against ZX Constraints

Based on the concept, analyze feasibility:
- Recommend render mode (0-3) with rationale
- Suggest tick rate (24/30/60/120 fps)
- Estimate if the scope fits in 16 MB ROM
- Flag any potential constraint issues

Present findings and ask user to confirm or adjust.

### Step 3: Choose GDD Depth

Ask user which template depth:
- **Quick** (1 page): Core concept, constraints, asset list. Good for game jams.
- **Standard** (3-5 pages): Full mechanics, levels, memory budget. Good for indie projects.
- **Comprehensive** (full doc): All sections including narrative, milestones. Good for production.

### Step 4: Gather Design Details

Based on chosen depth, collect information for each section:

**For all depths:**
- Core mechanic description
- Control scheme overview
- Initial asset list estimate

**For Standard and Comprehensive:**
- Detailed mechanics breakdown
- Level/world structure
- Memory budget allocation
- Audio design notes
- Multiplayer configuration (if applicable)

**For Comprehensive only:**
- Narrative overview
- Character specifications
- Art direction notes
- Development milestones
- Risk assessment

Use AskUserQuestion to gather preferences efficiently. Don't overwhelm with too many questions at once.

### Step 5: Generate the GDD

Create the directory if needed:
```
docs/design/
```

Write the GDD to `docs/design/game-design.md` using the appropriate template:
- Quick: Use `${CLAUDE_PLUGIN_ROOT}/skills/game-design-documents/references/gdd-template-quick.md`
- Standard: Use `${CLAUDE_PLUGIN_ROOT}/skills/game-design-documents/references/gdd-template-standard.md`
- Comprehensive: Use `${CLAUDE_PLUGIN_ROOT}/skills/game-design-documents/references/gdd-template-comprehensive.md`

Fill in all gathered information, making reasonable estimates where the user didn't specify.

### Step 6: Review and Iterate

Present a summary of the generated GDD:
- Title and high concept
- Key technical decisions (render mode, tick rate, multiplayer)
- Estimated memory budget
- Next steps

Ask if the user wants to refine any section.

## Output Location

All GDDs saved to: `docs/design/game-design.md`

If file already exists, ask user if they want to:
- Overwrite
- Create new file with timestamp
- Append/update existing

## Integration Notes

After GDD is complete, suggest next steps:
- Use `/validate-design` to check constraint compliance
- Use `/plan-assets` to generate asset specs for procgen
- Use `zx-dev` `/new-game` to scaffold the project

When the game is ready for release:
- Use `zx-publish` `/prepare-platform-assets` to create marketing assets
- Use `zx-publish` `/publish-game` to package ROM and upload

For full workflow orchestration from design through publishing, the user can enable the `zx-orchestrator` plugin.
