# Quest Design Patterns

Templates and patterns for designing engaging quests.

---

## Quest Structure Template

Use this template for each quest:

```
═══════════════════════════════════════════════════
QUEST: [Quest Name]
═══════════════════════════════════════════════════

TYPE: [Kill/Fetch/Escort/Investigate/Defend/Deliver/Survive/Race]

SUMMARY:
[One sentence describing the quest]

QUEST GIVER:
[Who gives the quest and why]

OBJECTIVE:
[Clear, specific player goal]

LOCATION:
[Where the quest takes place]

CHALLENGE:
[What makes this quest interesting]

REWARD:
[What player receives - tangible and intangible]

FAILURE STATE:
[What happens if player fails or abandons]

ESTIMATED LENGTH:
[Time to complete]

═══════════════════════════════════════════════════
```

---

## Quest Type Patterns

### Kill/Defeat Quest

**Structure:**
1. Learn about target
2. Find target location
3. Engage and defeat target
4. Confirm completion
5. Return for reward

**Variations:**
- Single target (boss)
- Multiple targets (clear area)
- Conditional defeat (specific method)
- Capture instead of kill

**Design tips:**
- Target should be interesting to fight
- Build up to encounter if significant
- Optional: non-combat solution

**Template:**
```
Target: [Who/what to defeat]
Location: [Where they are]
Challenge: [Why this is hard]
Optional twist: [Alternative approach]
```

---

### Fetch Quest

**Structure:**
1. Learn what's needed
2. Travel to location
3. Obtain item (may involve challenge)
4. Return with item
5. Receive reward

**Variations:**
- Simple retrieval
- Guarded item
- Hidden item (requires investigation)
- Competitive fetch (race against rival)
- Multiple items (collection)

**Design tips:**
- Journey should be interesting
- Item acquisition should feel earned
- Consider: can player keep a copy?

**Template:**
```
Item: [What to fetch]
Location: [Where it is]
Obstacle: [What guards/hides it]
Time pressure: [Yes/No, details]
```

---

### Escort Quest

**Structure:**
1. Meet escortee
2. Begin journey
3. Face threats during travel
4. Reach destination
5. Reward and conclusion

**Variations:**
- Protect from enemies
- Guide through hazards
- Prevent escape (prisoner)
- Multiple escortees
- Two-way escort (bring back)

**Design tips:**
- Escortee AI must be good
- Threats must be manageable
- Give player agency over pacing
- Escortee should be likeable or interesting

**Template:**
```
Escortee: [Who to escort]
Route: [Path taken]
Threats: [What endangers them]
Escortee behavior: [How they help/hinder]
```

---

### Investigation Quest

**Structure:**
1. Discover mystery
2. Gather clues at locations
3. Interview/interrogate
4. Piece together truth
5. Resolution/confrontation

**Variations:**
- Crime solving
- Hidden truth discovery
- Finding missing person
- Uncovering conspiracy
- Ancient secret

**Design tips:**
- Essential clues should be findable
- Red herrings should be fair
- Allow for clever players to deduce early
- Resolution should be satisfying

**Template:**
```
Mystery: [What player is investigating]
Clues: [List of discoverable clues]
Red herrings: [Misleading elements]
Truth: [The actual answer]
Resolution: [How mystery concludes]
```

---

### Defend Quest

**Structure:**
1. Learn threat is coming
2. Prepare defenses
3. Withstand assault
4. Survive until condition
5. Victory or defeat

**Variations:**
- Waves of enemies
- Single overwhelming threat
- Time-limited defense
- Protect specific object/person
- Strategic positioning required

**Design tips:**
- Give preparation time
- Waves should escalate
- Victory should feel earned
- Consider partial success states

**Template:**
```
Defend: [What to protect]
Threat: [What attacks]
Duration: [How long/waves]
Resources: [What player has]
Win condition: [What survival looks like]
```

---

### Deliver Quest

**Structure:**
1. Receive package/message
2. Travel to destination
3. Overcome obstacles
4. Deliver to recipient
5. Receive reward/next step

**Variations:**
- Fragile delivery (no combat)
- Time-sensitive
- Secret delivery (stealth)
- Delivery transforms during travel
- Recipient is not who expected

**Design tips:**
- Journey should be the challenge
- Package should create constraints
- Recipient interaction matters

**Template:**
```
Package: [What to deliver]
Constraint: [How package affects travel]
Destination: [Where to go]
Recipient: [Who receives it]
Complication: [What goes wrong]
```

---

## Quest Chain Patterns

### Linear Chain

```
Quest A → Quest B → Quest C → Quest D
```

Each quest unlocks the next. Good for main storylines.

**Design notes:**
- Each quest should be satisfying alone
- Callbacks to previous quests
- Escalating stakes and complexity

### Branching Chain

```
Quest A ──→ Quest B1 ──→ Quest C1
       └──→ Quest B2 ──→ Quest C2
```

Player choice determines path. Good for moral choices.

**Design notes:**
- Choices should be meaningful
- Branches should be meaningfully different
- Consider convergence points

### Prerequisite Web

```
Quest A ──┐
          ├──→ Quest D
Quest B ──┤
          ├──→ Quest E
Quest C ──┘
```

Multiple quests unlock later quests. Good for open worlds.

**Design notes:**
- Clear communication of prerequisites
- Quests should be completeable in any order
- Consider minimum/all completion paths

### Recursive Chain

```
Quest A → Result affects world → New Quest A variant
```

Quest repeats with variations. Good for roguelikes or procedural games.

**Design notes:**
- Variations should feel fresh
- Player progression should be evident
- Meta-progression across attempts

---

## Quest Motivation Patterns

### External Motivation

Player is given reason to complete quest:

| Motivator | Example |
|-----------|---------|
| **Reward** | "I'll pay you 100 gold" |
| **Authority** | "The king commands it" |
| **Threat** | "If you don't, the village burns" |
| **Need** | "You need this key to proceed" |

### Internal Motivation

Player wants to complete quest:

| Motivator | Example |
|-----------|---------|
| **Curiosity** | "What's in that sealed tomb?" |
| **Completion** | "I need all the artifacts" |
| **Connection** | "This NPC is my friend" |
| **Justice** | "That villain must be stopped" |

### Hybrid Motivation

Combine external and internal:
- External: "Find the lost child"
- Internal: Player cares about child after meeting their parent

---

## Quest Complication Patterns

### Twist Patterns

| Pattern | Example |
|---------|---------|
| **Not what it seems** | The "monster" is protecting its young |
| **Third party** | Someone else claims the item |
| **Changed circumstances** | The village moved while you were gone |
| **Betrayal** | Quest giver was using you |
| **Moral complexity** | Target has sympathetic motivation |

### Obstacle Patterns

| Pattern | Example |
|---------|---------|
| **Gatekeeper** | Need permission or key |
| **Puzzle** | Mechanism blocks progress |
| **Combat** | Enemies guard objective |
| **Skill check** | Requires specific ability |
| **Resource cost** | Requires spending supplies |

---

## Side Quest Purpose

Every side quest should serve at least one purpose:

| Purpose | Example |
|---------|---------|
| **World building** | Quest reveals lore |
| **Character development** | Companion quest deepens relationship |
| **Resource provision** | Provides needed items |
| **Skill testing** | Uses specific mechanic |
| **Pacing** | Break from main intensity |
| **Optional challenge** | Hard content for skilled players |
| **Exploration reward** | Found in optional area |

---

## Quest Design Checklist

Before finalizing a quest:

- [ ] Objective is clear
- [ ] Player understands why they should do it
- [ ] Challenge is appropriate for game stage
- [ ] Reward matches effort
- [ ] Quest fits world and tone
- [ ] Player has agency in completion
- [ ] Failure state exists and is fair
- [ ] Quest doesn't break pacing
- [ ] Quest has satisfying conclusion
