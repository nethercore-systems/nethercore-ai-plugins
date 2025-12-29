---
name: Creative Vision
description: This skill should be used when the user asks about "creative vision", "game vision", "creative direction", "overall feel", "creative pillars", "design intent", "vision alignment", "creative drift", "game identity", "player experience", "emotional design", or discusses establishing the overall creative direction and ensuring implementation matches vision. Provides comprehensive creative direction framework for defining and maintaining holistic project coherence.
version: 1.0.0
---

# Creative Vision

Establish and maintain holistic creative coherence by defining the core vision and ensuring all disciplines (art, sound, code) serve that vision.

## Core Principles

### The Vision Hierarchy

Creative direction flows downward:

```
                 ┌──────────────────┐
                 │ Creative Vision  │  ← What experience do we create?
                 └────────┬─────────┘
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  Art Vision   │ │ Sound Vision  │ │  Tech Vision  │
└───────────────┘ └───────────────┘ └───────────────┘
        │                 │                 │
        ▼                 ▼                 ▼
   [Assets]          [Audio]           [Code]
```

The creative director ensures all three disciplines serve the unified vision.

### Creative Pillars

Define 3-5 non-negotiable experience principles:

**Format:**
```
PILLAR: [Short Name]
STATEMENT: [What this means for the player]
MANIFESTS AS:
- Art: [How art supports this]
- Sound: [How sound supports this]
- Code: [How mechanics support this]
```

**Example pillars:**

```
PILLAR: Atmospheric Dread
STATEMENT: Players should feel isolated and vulnerable
MANIFESTS AS:
- Art: Dark palettes, obscured vision, environmental decay
- Sound: Sparse, ambient, distant threats, silence as tool
- Code: Limited resources, no map, permadeath consequences

PILLAR: Meaningful Choices
STATEMENT: Every decision should have weight and consequence
MANIFESTS AS:
- Art: Clear visual distinction between options
- Sound: Distinct audio feedback for different choice outcomes
- Code: Branching consequences, no "correct" answers

PILLAR: Emergent Discovery
STATEMENT: Players should discover systems through experimentation
MANIFESTS AS:
- Art: Visual hints without explicit tutorials
- Sound: Audio cues that teach through repetition
- Code: Interconnected systems, discoverable interactions
```

### The Experience Promise

Define the core experience in one paragraph:

```
In [GAME NAME], players experience [CORE EMOTION] through
[PRIMARY MECHANIC]. The world evokes [ATMOSPHERE] while
players [CORE VERB: explore/survive/build/fight]. Success
feels like [SUCCESS EMOTION] and failure teaches
[FAILURE LESSON].
```

**Example:**
```
In VOID WALKER, players experience cosmic dread through
careful resource management in procedural stations. The world
evokes isolation and decay while players scavenge for survival.
Success feels like relief and discovery, and failure teaches
respect for the void.
```

## Vision Document Structure

Create a vision document with these sections:

### 1. Experience Promise
The one-paragraph core experience definition.

### 2. Creative Pillars
3-5 pillars with manifestations across disciplines.

### 3. Emotional Journey
Map the intended emotional arc:

```
START: [Initial emotion when player begins]
  │
EARLY GAME: [Emotion during learning/onboarding]
  │
MID GAME: [Emotion during core loop mastery]
  │
LATE GAME: [Emotion during challenge/climax]
  │
END: [Emotion at conclusion/victory]
```

### 4. Target Audience
Define who this game is for:

```
PRIMARY: [Core audience - who this game is made for]
SECONDARY: [Adjacent audience - who might also enjoy]
NOT FOR: [Who this game is explicitly not targeting]
```

### 5. Reference Works
Games, films, books, art that embody the vision:

```
GAME: [Title] - [What aspect we're drawing from]
FILM: [Title] - [What aspect we're drawing from]
BOOK: [Title] - [What aspect we're drawing from]
ART: [Artist/Work] - [What aspect we're drawing from]
```

### 6. Anti-Patterns
What this game explicitly avoids:

```
- [Thing we won't do]: [Why it violates the vision]
- [Another thing]: [Why]
```

## Vision Alignment Check

When reviewing work for vision alignment:

### Pillar Mapping

For each piece of work, map to pillars:

```
WORK: [Asset/Feature/System being reviewed]

PILLAR 1 [Name]:
- Supports: [How it supports this pillar]
- OR Neutral: [Doesn't affect this pillar]
- OR Conflicts: [How it works against this pillar]

PILLAR 2 [Name]:
...
```

If work conflicts with pillars without justification, it's drifting.

### Experience Fit

Ask:
- Does this reinforce the experience promise?
- Does this evoke the intended emotions?
- Would the target audience appreciate this?
- Does this feel like the reference works?

### Cross-Discipline Coherence

Verify disciplines align:
- Does the art match the sound?
- Does the sound match the mechanics?
- Does the code support the intended experience?

## Detecting Creative Drift

### Warning Signs

**Art Drift:**
- Style inconsistency with established work
- Emotional tone mismatch
- Visual complexity creep or simplification

**Sound Drift:**
- Audio identity inconsistency
- Mix priority violations
- Emotional tone mismatch

**Tech Drift:**
- Features that don't serve pillars
- Complexity that undermines experience
- Performance issues affecting feel

**Vision Drift:**
- Scope changes without pillar review
- Feature additions that dilute focus
- Audience expansion that compromises core

### Drift Response

When drift is detected:

1. **Acknowledge**: Name the drift clearly
2. **Trace**: When did it start?
3. **Evaluate**: Is it good drift (evolution) or bad drift (loss)?
4. **Decide**: Correct course or update vision deliberately
5. **Document**: Record the decision

## Director Coordination

### When to Involve Which Director

| Situation | Primary Director | Supporting |
|-----------|-----------------|------------|
| New feature proposal | Creative | All |
| Asset review | Art/Sound | Creative |
| Performance issue | Tech | Creative |
| Player feedback | Creative | Relevant |
| Milestone review | Creative | All |
| Scope change | Creative | All |

### Review Cadence

**Per-Asset**: Art or Sound director (continuous via hooks)
**Per-Feature**: Tech director (code reviews)
**Per-Milestone**: Creative director (holistic review)
**Per-Major-Decision**: All directors (architectural)

### Conflict Resolution

When directors disagree:

1. Return to pillars: What do they say?
2. Return to experience promise: What does it require?
3. Consider target audience: What do they need?
4. Prototype if unclear: Test both approaches
5. Document decision: ADR with reasoning

## Establishing Creative Vision

For new projects, run the vision establishment workflow:

1. **Define experience promise** - One paragraph core experience
2. **Identify pillars** - 3-5 non-negotiable principles
3. **Map emotional journey** - Start to end player arc
4. **Define audience** - Who is this for?
5. **Collect references** - Games/films/art that inspire
6. **List anti-patterns** - What we're avoiding
7. **Cross-discipline mapping** - How pillars manifest
8. **Document** - Create vision document

Store vision in `.studio/creative-direction.local.md` for persistence.

## Director Notes Format

When providing creative direction feedback, structure notes as:

```
VISION CHECK: [Work/Feature being reviewed]

PILLAR ALIGNMENT:
- Pillar 1: [Supports/Neutral/Conflicts] - [Details]
- Pillar 2: [Supports/Neutral/Conflicts] - [Details]
- ...

EXPERIENCE FIT:
- [How it serves or undermines the experience promise]

DISCIPLINE COHERENCE:
- Art-Sound alignment: [Assessment]
- Sound-Code alignment: [Assessment]
- Art-Code alignment: [Assessment]

DRIFT STATUS:
- [No drift detected] OR
- [Drift detected]: [Description and recommended response]

RECOMMENDATIONS:
1. [Specific actionable guidance]
2. [Priority: High/Medium/Low]
```

## Additional Resources

### Reference Files

For detailed guidance on specific topics:
- **`references/pillar-design.md`** - How to craft effective pillars
- **`references/emotional-design.md`** - Designing emotional experiences
- **`references/vision-templates.md`** - Full vision document templates

### Related Skills

- **art-vision** - Visual direction framework
- **sound-vision** - Audio direction framework
- **tech-vision** - Technical direction framework
