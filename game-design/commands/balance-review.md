---
description: Game balance review framework analyzing difficulty, stats, and economy
argument-hint: "[target]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Balance Review Tool

Systematic analysis of game balance across difficulty, stats, and economy.

## Arguments

- `target` (optional): Path to design document to review
  - Default: `docs/design/game-design.md`
  - Can specify any design document

## Process

1. **Gather information**:
   - Read existing design documents
   - Ask about intended difficulty level
   - Identify core systems to balance

2. **Difficulty curve analysis**:
   - What's the intended curve?
   - Where are the peaks (bosses, challenges)?
   - Where are the rest points?
   - Are difficulty settings planned?

3. **Stat scaling review**:
   - Player power progression
   - Enemy scaling
   - Damage formulas
   - Health pools

4. **Build viability check**:
   - What builds/strategies are intended?
   - Are all builds completable?
   - Are there trap options?
   - Is there a dominant strategy?

5. **Economy analysis**:
   - Resource generation rates
   - Spending requirements
   - Inflation/deflation risks
   - Scarcity levels

6. **Identify red flags**:
   - One-shot potential
   - Required grinding
   - Unused mechanics
   - Obvious imbalances

## Output

Console output with:

```
═══════════════════════════════════════════
BALANCE REVIEW: [Game Name]
═══════════════════════════════════════════

DIFFICULTY CURVE
[Analysis and diagram]

STATUS: [OK / NEEDS ATTENTION / CRITICAL]

STAT SCALING
[Analysis]

STATUS: [OK / NEEDS ATTENTION / CRITICAL]

BUILD VIABILITY
[Analysis of viable builds/strategies]

STATUS: [OK / NEEDS ATTENTION / CRITICAL]

ECONOMY
[Resource flow analysis]

STATUS: [OK / NEEDS ATTENTION / CRITICAL]

RED FLAGS
• [List of concerns]

RECOMMENDATIONS
1. [Priority action items]
2. [Secondary items]
3. [Nice to have]
═══════════════════════════════════════════
```

## Tips

- Balance is iterative—this is a starting point
- Change one variable at a time when fixing
- Playtest data trumps theory
- Fun beats math (if both can't coexist)
