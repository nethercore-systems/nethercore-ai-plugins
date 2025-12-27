---
description: Validate game design against Nethercore ZX constraints
argument-hint: [gdd-path]
allowed-tools: Read, Grep, Glob
---

# Design Validation

Analyze a Game Design Document and validate it against Nethercore ZX console constraints.

## Input

GDD file path: $ARGUMENTS

If no path provided, default to: `docs/design/game-design.md`

## Validation Process

### Step 1: Load the GDD

Read the specified GDD file. If file doesn't exist, inform user and suggest using `/design-game` to create one.

### Step 2: Extract Key Specifications

Parse the GDD for:
- Render mode selection
- Tick rate
- Player count and multiplayer mode
- Memory budget estimates (ROM, RAM, VRAM)
- Asset counts (characters, levels, sounds, textures)
- Game state size estimate

### Step 3: Validate Against Constraints

Check each specification against ZX limits:

**ROM Budget (16 MB max)**
- Sum all asset size estimates
- Flag if total exceeds 16 MB
- Warn if total exceeds 14 MB (low margin)
- Suggest areas to optimize if over budget

**RAM State (target < 100 KB for rollback)**
- Estimate game state size from entity counts
- Flag if state likely exceeds 100 KB
- Explain rollback performance implications

**VRAM Budget (4 MB max)**
- Estimate active texture memory
- Flag if textures loaded simultaneously exceed limit
- Suggest texture resolution adjustments

**Render Mode Compatibility**
- Check if chosen render mode matches described art style
- Verify texture workflow matches mode (MRE for mode 2, SSE for mode 3)
- Suggest alternatives if mismatch detected

**Tick Rate Appropriateness**
- Check if tick rate matches game type
- Warn if fighting/action game uses < 60 fps
- Suggest 120 fps for first-person if not specified

**Multiplayer Determinism**
- If multiplayer is specified, check for determinism red flags
- Flag any mentioned random systems without seeding
- Flag time-based mechanics
- Suggest determinism review

**Audio Channel Budget (16 channels)**
- Count estimated simultaneous sound sources
- Flag if likely to exceed 16 channels
- Suggest audio priority system if needed

### Step 4: Generate Report

Output a validation report with:

```
# Design Validation Report

## Summary
- GDD: [filename]
- Status: [PASS / WARNINGS / CRITICAL ISSUES]

## Constraint Checks

### ROM Budget
- Estimated: X MB / 16 MB
- Status: ✓ OK / ⚠ Tight / ✗ Over budget
- [Details if issues]

### RAM State
- Estimated: X KB
- Rollback performance: [Good / Acceptable / Concerning]
- [Details if issues]

### VRAM Budget
- Estimated: X MB / 4 MB
- Status: ✓ OK / ⚠ Tight / ✗ Over budget
- [Details if issues]

### Render Mode
- Selected: Mode X
- Compatibility: ✓ Good fit / ⚠ Potential mismatch
- [Details if issues]

### Tick Rate
- Selected: X fps
- For game type: ✓ Appropriate / ⚠ Consider change
- [Details if issues]

### Multiplayer
- Configuration: [X players, mode]
- Determinism: ✓ No issues found / ⚠ Review needed
- [Details if issues]

### Audio
- Estimated channels: X / 16
- Status: ✓ OK / ⚠ Tight / ✗ Over budget
- [Details if issues]

## Recommendations

1. [High priority recommendation]
2. [Medium priority recommendation]
3. [Low priority recommendation]

## Next Steps

- Address any critical issues before implementation
- Use /plan-assets to generate detailed asset specifications
- Use nethercore-zx-dev /new-game to scaffold project
```

### Step 5: Offer Assistance

After presenting the report, offer to:
- Help fix any critical issues
- Adjust the GDD with updated specifications
- Explain any constraint in more detail
- Proceed to asset planning if validation passed
