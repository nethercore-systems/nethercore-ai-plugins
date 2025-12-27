---
name: Core Loop Design
description: This skill should be used when the user asks about "core loop", "gameplay loop", "game loop", "progression system", "game economy", "resource economy", "feedback loop", "reward system", "gameplay cycle", "engagement loop", "compulsion loop", "grind", "pacing", or needs to design the fundamental moment-to-moment and session-to-session gameplay structure.
version: 1.0.0
---

# Core Loop Design

Frameworks for designing the fundamental cycles of gameplay that keep players engaged. The core loop is your game's heartbeat.

## Core Principle: The Loop is the Game

Players don't remember features—they remember how it felt to play. The core loop is what they do over and over, so it must be:
- **Satisfying:** Each cycle feels good
- **Clear:** Players know what to do
- **Variable:** Enough variety to prevent monotony
- **Progressive:** Mastery is visible and rewarding

---

## Understanding Loops

### Loop Anatomy

Every game loop has three phases:

```
     ┌───────────────────────────┐
     │                           │
     ▼                           │
  [ACTION] ───→ [FEEDBACK] ───→ [REWARD]
     │                           │
     │                           │
     └─── Player chooses to ─────┘
          repeat (or not)
```

**Action:** What the player does
**Feedback:** What the game shows in response
**Reward:** What the player gains (intrinsic or extrinsic)

### Loop Hierarchy

Games have nested loops at different time scales:

| Loop Level | Duration | Example |
|------------|----------|---------|
| **Micro** | Seconds | Attack enemy → Hit feedback → Damage dealt |
| **Core** | Minutes | Clear room → XP gain → Level progress |
| **Meta** | Hours | Complete dungeon → New gear → Stronger character |
| **Session** | Play session | Play session → Meaningful progress → Reason to return |
| **Campaign** | Total playtime | Complete game → Final reward → Replay or finish |

---

## Core Loop Worksheet

### Define Your Loops

**Micro Loop (moment-to-moment):**
```
Action: _________________
Feedback: _________________
Reward: _________________
Duration: _____ seconds
```

**Core Loop (main gameplay cycle):**
```
Action: _________________
Feedback: _________________
Reward: _________________
Duration: _____ minutes
```

**Meta Loop (session-level):**
```
Action: _________________
Feedback: _________________
Reward: _________________
Duration: _____ hours
```

### Loop Connection

How do loops connect?

```
Micro loop rewards feed into → Core loop
Core loop rewards feed into → Meta loop
Meta loop rewards create → Reason to start new micro loops
```

---

## Loop Patterns

### The Classic Action Loop

```
[Find challenge] → [Attempt challenge] → [Succeed/Fail]
       ↑                                       │
       └───────── [Learn/Improve] ─────────────┘
```

**Games:** Platformers, action games, skill-based games
**Key:** Failure must teach, success must feel earned

### The Collection Loop

```
[Explore] → [Discover item] → [Add to collection]
     ↑                              │
     └───── [Unlock new areas] ─────┘
```

**Games:** Metroidvanias, adventure games, collectathons
**Key:** Items must be meaningful (useful, rare, interesting)

### The Build Loop

```
[Gather resources] → [Craft/Build] → [Use creation]
        ↑                                  │
        └───── [New opportunities] ────────┘
```

**Games:** Survival, crafting, city builders
**Key:** Building must have purpose and visible impact

### The Combat Loop

```
[Encounter enemy] → [Fight] → [Victory] → [Loot/XP]
        ↑                                     │
        └───── [Get stronger] ────────────────┘
```

**Games:** RPGs, action RPGs, roguelikes
**Key:** Power progression must feel meaningful

### The Story Loop

```
[Receive quest] → [Complete objective] → [Story revelation]
        ↑                                       │
        └───────── [New quest] ─────────────────┘
```

**Games:** Adventure, RPG, narrative games
**Key:** Revelations must be worth the effort

---

## Progression Systems

### Progression Types

| Type | Player Gains | Feels Like |
|------|--------------|------------|
| **Vertical** | More power | Getting stronger |
| **Horizontal** | More options | Getting versatile |
| **Skill** | Player improves | Getting better |
| **Content** | Access to more | Unlocking secrets |
| **Story** | Narrative progress | Discovering truth |

### Progression Curves

**Linear:**
```
Power
  ↑
  │    ╱
  │  ╱
  │╱
  └────→ Time
```
Steady gains, predictable, can feel grindy

**Exponential early:**
```
Power
  ↑
  │╭───
  │
  └────→ Time
```
Fast start, slowing later, good for onboarding

**Exponential late:**
```
Power
  ↑
  │     ╱
  │   ╱
  │──╯
  └────→ Time
```
Slow start, explosive later, requires patience

**Stepped:**
```
Power
  ↑
  │    ┌──
  │  ┌─┘
  │──┘
  └────→ Time
```
Dramatic power spikes, punctuated by plateaus

### Designing Progression

**Questions to answer:**
- What gates progression? (time, skill, exploration)
- How visible is progression? (numbers, visual changes)
- Can progression be lost? (permadeath, resource drain)
- Is progression shared or per-character?

---

## Economy Design

### Resource Types

| Resource | Accumulation | Spending | Purpose |
|----------|--------------|----------|---------|
| **Currency** | Steady | Flexible | General purchasing |
| **Consumables** | Variable | Immediate | Tactical decisions |
| **Materials** | Exploration | Crafting | Progression gating |
| **Time** | Constant | Action cost | Pacing control |
| **Health/Lives** | Limited | Risk cost | Tension creation |

### Economy Principles

**Sources and Sinks:**
- Sources: Where resources come from
- Sinks: Where resources go

```
[Sources] ──→ [Player's inventory] ──→ [Sinks]
Enemies drop         ↕              Shop purchases
Exploration      Save/Load          Consumable use
Crafting                           Upgrade costs
```

**Balance rule:** Sinks must match or exceed sources long-term, or economy inflates.

### Scarcity Design

Scarcity creates value. Control through:
- **Limited sources:** Finite enemy spawns
- **Time gating:** Resources regenerate slowly
- **Location gating:** Resources in specific areas
- **Skill gating:** Resources from challenges

**Warning:** Too much scarcity creates frustration. Too little creates meaninglessness.

---

## Feedback Systems

### Feedback Types

| Type | Speed | Purpose | Example |
|------|-------|---------|---------|
| **Immediate** | Instant | Confirm action | Hit spark, sound effect |
| **Short-term** | Seconds | Show impact | Enemy health bar, XP popup |
| **Medium-term** | Minutes | Show progress | Level up, quest complete |
| **Long-term** | Hours | Show achievement | Unlocks, story progress |

### Feedback Intensity

Match feedback intensity to action significance:

```
Basic attack → Small hit sound/visual
Critical hit → Big hit sound/visual, camera shake
Level up → Sound, visual fanfare, UI celebration
Boss defeat → Extended celebration, narrative moment
```

### The Feedback Checklist

For each player action:
- [ ] Visual feedback exists
- [ ] Audio feedback exists
- [ ] Feedback is immediate (or delay is intentional)
- [ ] Feedback intensity matches action significance
- [ ] Negative outcomes are clear but not punishing

---

## Engagement and Flow

### Flow State Design

Players enter flow when challenge matches skill:

```
Anxiety zone
(too hard)  │       ╱
            │     ╱
Challenge   │   ╱ ← FLOW CHANNEL
            │ ╱
Boredom zone╱
(too easy)  └─────────────→
                 Skill
```

### Creating Flow

**Dynamic difficulty:**
- Adjust based on player performance
- Invisible to player
- Maintains challenge without frustration

**Player-controlled difficulty:**
- Difficulty settings
- Optional challenges
- Self-imposed restrictions

**Designed difficulty curve:**
- Careful content ordering
- Teaching before testing
- Recovery periods after spikes

### Preventing Negative Loops

Watch for loops that push players away:

**Death spiral:**
```
[Fail] → [Lose resources] → [Harder next attempt] → [Fail again]
```
**Solution:** Failure shouldn't compound difficulty

**Grinding trap:**
```
[Stuck] → [Grind for power] → [Trivialize content] → [Boredom]
```
**Solution:** Skill should matter more than grinding

---

## Session Structure

### Session Pacing

Structure sessions with variety:

```
[Hook] → [Rising action] → [Peak] → [Cool down] → [Cliffhanger]
   5%         30%             40%        20%           5%
```

### Natural Break Points

Design stopping points:
- After completing objectives
- In safe zones
- After narrative beats
- Before major challenges

**Save systems should support session length:**
- Short sessions: Frequent auto-saves
- Medium sessions: Checkpoint saves
- Long sessions: Manual save anywhere

### Session Length Design

**Target session length:** _____ minutes

Design content for this length:
- [ ] Complete loop cycles fit session
- [ ] Progress feels meaningful each session
- [ ] Natural stopping points exist
- [ ] Returning players can resume smoothly

---

## Loop Testing

### Test Questions

1. **First minute:** Does player know what to do?
2. **First ten minutes:** Is player engaged?
3. **First hour:** Does player feel progress?
4. **Multiple sessions:** Does player want to return?

### Warning Signs

**Loop is too short:**
- Player finishes content too quickly
- No long-term goals remain
- Replay feels identical

**Loop is too long:**
- Player loses focus
- Progress feels invisible
- Session length doesn't fit

**Loop is unbalanced:**
- One phase takes too long
- Rewards don't match effort
- Feedback is missing or delayed

---

## Additional Resources

### Reference Files

- **`references/loop-worksheet.md`** — Detailed loop design template
- **`references/progression-templates.md`** — Progression system patterns
- **`references/economy-design.md`** — Resource economy frameworks

### Related Skills

- **`game-balance`** — Balancing loop rewards
- **`player-psychology`** — Understanding player engagement
- **`replayability-engineering`** — Loops for replayable games
