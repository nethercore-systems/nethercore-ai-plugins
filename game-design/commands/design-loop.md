---
description: Core loop analysis and design tool for mapping gameplay cycles
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
---

# Core Loop Design Tool

Analyze and design the fundamental gameplay loops that drive engagement.

## Process

1. **Identify current loop** (or design new):
   - What does the player DO most often?
   - What FEEDBACK do they receive?
   - What REWARD do they get?

2. **Map loop hierarchy**:
   - Micro loop (seconds): moment-to-moment actions
   - Core loop (minutes): main gameplay cycle
   - Meta loop (hours): session-level progression

3. **Analyze connections**:
   - How do micro rewards feed core loop?
   - How do core rewards feed meta loop?
   - What motivates continuing?

4. **Identify progression**:
   - What progression type? (vertical, horizontal, skill, content)
   - How visible is progression?
   - What's the progression curve?

5. **Economy check**:
   - What resources exist?
   - Where do they come from (sources)?
   - Where do they go (sinks)?
   - Is economy balanced?

6. **Engagement analysis**:
   - Where might players get bored?
   - Where might players get frustrated?
   - What creates "one more turn" feeling?

## Output

Create `docs/design/core-loop.md` with:

```markdown
# Core Loop Design

## Loop Summary
Micro (Xs): [action] → [feedback] → [reward]
Core (Xm): [cycle description]
Meta (Xh): [session/campaign structure]

## Loop Diagram
[ASCII diagram of loop flow]

## Progression
- Type: [vertical/horizontal/skill/content]
- Curve: [description]
- Visibility: [how player sees progress]

## Economy
| Resource | Sources | Sinks |
|----------|---------|-------|
| [name] | [list] | [list] |

## Engagement Risks
[Identified problems and solutions]

## Action Items
[Changes to implement]
```

## Tips

- The loop IS the game—get this right
- Test micro loop first (does it feel good?)
- Every loop level should reward somehow
- Economy should slightly favor progression feeling
