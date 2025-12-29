---
name: Level Design Principles (Conceptual)
description: |
  Use this skill for CONCEPTUAL level design - how to guide players, create challenge curves, and design memorable spaces. Trigger phrases: "level flow", "pacing", "challenge curve", "player guidance", "teaching through design", "encounter design", "how to design a good level".

  This skill provides UNIVERSAL PRINCIPLES - applicable to any game engine or platform.

  For ZX-SPECIFIC IMPLEMENTATION (tile maps, ROM storage, procedural generation): use zx-game-design:level-design instead.
version: 1.0.1
---

# Level Design Principles

Practical frameworks for designing playable spaces that guide, challenge, and reward players.

## Core Principle: Levels Teach

Every level teaches players something—intentionally or not. Design spaces that:
- Introduce mechanics safely before testing them
- Guide without handholding
- Reward curiosity
- Create memorable moments

---

## Level Flow

### The Flow Triangle

Every level balances three elements:

```
        CHALLENGE
           /\
          /  \
         /    \
        /      \
   GUIDANCE ─── EXPLORATION
```

**High challenge:** Tests player skill
**High guidance:** Keeps player on track
**High exploration:** Rewards curiosity

Adjust the balance based on level purpose.

### Flow Patterns

| Pattern | Description | Use When |
|---------|-------------|----------|
| **Linear** | A→B→C, one path | Tutorial, story moments |
| **Branching** | Multiple paths to same goal | Player choice, replayability |
| **Hub** | Central area with spokes | Open areas, towns |
| **Network** | Interconnected paths | Metroidvania, exploration |
| **Arena** | Contained combat space | Boss fights, encounters |

---

## Player Guidance

### The Breadcrumb Method

Guide players without explicit markers:

| Technique | Example |
|-----------|---------|
| **Light** | Lit path vs dark areas |
| **Color** | Bright object in muted environment |
| **Motion** | Moving element draws attention |
| **Sound** | Audio cues from objective |
| **Geometry** | Lines pointing toward goal |
| **NPCs** | Characters looking/moving toward goal |

### The Gate Method

```
[Safe area with resource]
         │
    [Visible gate]
         │
    [Challenge]
         │
    [New area + reward]
```

Players understand: overcome challenge → access new area.

---

## Challenge Design

### Challenge Curve

```
Difficulty
   │     ╱╲      ╱╲
   │   ╱    ╲  ╱    ╲
   │ ╱        ╲        ╲___
   │╱
   └────────────────────→ Time
     Intro  Peak  Rest  Peak  End
```

**Principles:**
- Introduce → Practice → Test → Rest
- Peaks should not back-to-back
- End slightly below peak (satisfying finish)

### Encounter Design Template

```
ENCOUNTER: [Name]

Purpose: [ ] Teach [ ] Test [ ] Challenge [ ] Rest
Mechanics tested: _______________
Enemy composition: _______________
Environment factors: _______________
Escape/retreat option: [ ] Yes [ ] No
Reward: _______________
```

---

## Spatial Design Checklist

### Before Building

- [ ] Level purpose is clear (what does player learn/do?)
- [ ] Target length defined
- [ ] Key beats identified (intro, challenges, climax)
- [ ] Flow pattern chosen

### During Building

- [ ] Sightlines guide toward objectives
- [ ] Landmarks are visible and memorable
- [ ] Dead ends have rewards or are short
- [ ] Verticality creates interest
- [ ] Cover/positioning matters in combat areas

### After Building

- [ ] Blind playtest: Can new players navigate?
- [ ] Timing test: Does it match target length?
- [ ] Fun test: Are the right moments challenging/rewarding?

---

## Teaching Through Design

### The Teach-Test Pattern

```
1. SAFE INTRO: Show mechanic with no risk
2. GUIDED PRACTICE: Low-risk application
3. REAL TEST: Full-risk application
4. MASTERY: Complex or combined application
```

### Teaching Without Words

| To Teach | Design Method |
|----------|---------------|
| Jump distance | Gap with safe fall, then real gap |
| Enemy pattern | First enemy alone, then in groups |
| Timing | Slow version, then normal speed |
| Combination | Individual mechanics, then combined |

---

## Secrets and Exploration

### Secret Types

| Type | Visibility | Reward |
|------|------------|--------|
| **Hidden** | Not visible, requires search | High value |
| **Obscured** | Partially visible, requires attention | Medium value |
| **Skill-gated** | Visible, requires mastery | Variable |
| **Knowledge-gated** | Requires information from elsewhere | Variable |

### Exploration Rewards

Every detour should reward the player:
- Resources/items
- Lore/world building
- Shortcuts back to main path
- Vantage points/information
- Satisfying completion feeling

---

## Quick Reference Templates

### Level Planning Template

```
LEVEL: [Name]
Purpose: _______________
Target time: _____ minutes
Flow pattern: [ ] Linear [ ] Branching [ ] Hub [ ] Network

BEATS:
1. Intro: _______________
2. Rise: _______________
3. Peak: _______________
4. Rest: _______________
5. Climax: _______________
6. Exit: _______________

KEY LANDMARKS:
• _______________
• _______________
• _______________

SECRETS: _____ total
```

---

## Additional Resources

### Reference Files

- **`references/flow-templates.md`** — Level flow diagrams
- **`references/challenge-curves.md`** — Difficulty pacing patterns
- **`references/spatial-checklist.md`** — Detailed design checklist

### Related Skills

- **`world-building`** — Context for levels
- **`game-balance`** — Encounter balancing
- **`core-loop-design`** — How levels fit the loop
