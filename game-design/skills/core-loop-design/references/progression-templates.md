# Progression System Templates

Ready-to-use progression frameworks for different game types.

---

## Level-Based Progression

Classic numerical leveling system.

### Structure

```
Level 1 ──→ Level 2 ──→ Level 3 ──→ ... ──→ Level Max
   │           │           │                    │
   └─ Stats +  └─ Stats +  └─ Stats +    ... ──┘
   └─ Unlock   └─ Unlock   └─ Unlock
```

### Design Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Max level | | Typical: 20-100 |
| XP curve | Linear/Exponential | |
| Stats per level | | |
| Unlock frequency | Every N levels | |

### XP Curve Templates

**Linear:** Each level requires same XP
```
Level 1: 100 XP
Level 2: 100 XP
Level 3: 100 XP
...
```
Pro: Predictable. Con: May feel too fast or slow.

**Exponential:** Each level requires more XP
```
Level 1: 100 XP
Level 2: 150 XP
Level 3: 225 XP
...
```
Pro: Slows late-game. Con: Can feel grindy.

**Stepped:** Increases at milestones
```
Levels 1-5: 100 XP each
Levels 6-10: 200 XP each
Levels 11-15: 400 XP each
...
```
Pro: Clear phases. Con: Jarring transitions.

---

## Unlock-Based Progression

Gated content and abilities.

### Structure

```
[Starting abilities]
        │
        ▼
[Gate 1: Boss/Item/Location]
        │
        ▼
[Unlock: New ability/area]
        │
        ▼
[Gate 2: Boss/Item/Location]
        │
        ▼
[Unlock: New ability/area]
...
```

### Design Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Total unlocks | | |
| Gate types | Boss/Item/Story/Skill | |
| Unlock visibility | Hidden/Shown | |
| Backtracking value | | Does unlock add to old areas? |

### Unlock Template

```
═══════════════════════════════════════════
UNLOCK: [Name]

Gate type: [ ] Boss [ ] Item [ ] Story [ ] Skill [ ] Location
Location: Where player finds gate
Requirement: What player must do

What it unlocks:
• Ability: _________________
• Access: _________________
• Mechanic: _________________

Backtracking value:
• Opens: _________________
• Reveals: _________________
═══════════════════════════════════════════
```

---

## Skill Tree Progression

Branching ability choices.

### Structure

```
        [Root ability]
           /    \
     [Branch A] [Branch B]
        / \        / \
    [A1] [A2]  [B1] [B2]
```

### Design Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Tree depth | | Levels of choices |
| Branch count | | Specialization options |
| Point source | Levels/Currency/Achievements | |
| Respec option | Yes/No/Limited | |

### Skill Tree Template

```
SKILL TREE: [Name]

Point Source: [ ] Level up [ ] Currency [ ] Boss kills [ ] Other

Branch 1: [Theme]
├─ Tier 1: [Skill] (cost: ___)
│  └─ Description: _______________
├─ Tier 2: [Skill] (cost: ___, requires: ___)
│  └─ Description: _______________
└─ Tier 3: [Skill] (cost: ___, requires: ___)
   └─ Description: _______________

Branch 2: [Theme]
├─ Tier 1: [Skill] (cost: ___)
...
```

### Skill Tree Principles

1. **Immediate value:** First tier should feel impactful
2. **Clear identity:** Branches should feel distinct
3. **Viable builds:** Multiple paths should be viable
4. **Interesting choices:** Points should feel meaningful

---

## Equipment-Based Progression

Power through gear acquisition.

### Structure

```
[Common gear] → [Uncommon] → [Rare] → [Legendary]
      │              │           │          │
   Base stats    +Bonus      +Unique     +Build-defining
```

### Design Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Rarity tiers | | Common to Legendary |
| Equipment slots | | Weapon, armor, accessories |
| Stat ranges | | Per tier |
| Drop rates | | Per tier |
| Upgrade system | Yes/No | Can gear improve? |

### Equipment Template

```
═══════════════════════════════════════════
EQUIPMENT: [Name]

Slot: [ ] Weapon [ ] Armor [ ] Accessory [ ] Other
Rarity: [ ] Common [ ] Uncommon [ ] Rare [ ] Legendary
Source: Where obtained

Stats:
• Primary: _________________
• Secondary: _________________
• Unique effect: _________________

Set bonus (if applicable):
• 2-piece: _________________
• 4-piece: _________________
═══════════════════════════════════════════
```

---

## Mastery Progression

Player skill improvement without power increase.

### Structure

```
[Learn mechanic] → [Practice] → [Master] → [Express mastery]
                      │             │              │
                   Fail/Retry    Consistency    Creativity
```

### Design Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Core mechanics | | What to master |
| Skill ceiling | Low/Med/High | |
| Practice opportunities | | Where player practices |
| Mastery expression | | How experts shine |

### Mastery Framework

```
MECHANIC: [Name]

Skill floor (minimum competence):
• What player can do immediately: _________________
• What player can't do yet: _________________

Skill ceiling (maximum mastery):
• Advanced techniques: _________________
• Expert-only options: _________________

Progression path:
1. Learn basic: _________________
2. Apply reliably: _________________
3. Combine with others: _________________
4. Optimize timing: _________________
5. Express creativity: _________________
```

---

## Hybrid Progression

Combining multiple systems.

### Common Combinations

**Level + Equipment:**
- Levels provide base stats
- Equipment adds customization
- Works well for RPGs

**Unlock + Mastery:**
- Unlocks provide new tools
- Mastery provides depth with each tool
- Works well for action games

**Skill Tree + Equipment:**
- Skills define build direction
- Equipment supports build
- Works well for ARPGs

### Integration Template

```
PRIMARY SYSTEM: _________________
• Main source of power/progress
• How acquired: _________________

SECONDARY SYSTEM: _________________
• Adds depth/customization
• How acquired: _________________

INTEGRATION:
• How they interact: _________________
• Which dominates early: _________________
• Which dominates late: _________________
```

---

## Progression Pacing

### Milestone Planning

| Milestone | Time to Reach | Power Level | Content Unlocked |
|-----------|---------------|-------------|------------------|
| Tutorial complete | | | |
| First boss | | | |
| Mid-game | | | |
| Pre-finale | | | |
| Final | | | |

### Progression Curve Visualization

Plot expected player power over time:

```
Power
100% │                    ╭─
     │                  ╱
 50% │            ╭───╯
     │       ╭───╯
  0% │_____╯
     └────────────────────→ Time
        Early  Mid  Late
```

Mark key unlocks and power spikes on the curve.

---

## Common Progression Problems

### Too Fast

**Symptoms:**
- Player maxes out before content ends
- Later content feels trivial
- No sense of earning power

**Solutions:**
- Extend curve
- Add prestige/new game+
- Horizontal progression after cap

### Too Slow

**Symptoms:**
- Player feels stuck
- Progress invisible
- Grinding feels required

**Solutions:**
- More frequent smaller rewards
- Better progress visualization
- Alternative progression paths

### Too Flat

**Symptoms:**
- Power gains feel meaningless
- No excitement from progression
- Character feels same throughout

**Solutions:**
- Bigger power spikes at milestones
- More impactful unlocks
- Transform playstyle with progression

### Too Steep

**Symptoms:**
- Old content becomes trivial instantly
- Difficulty spikes at new content
- Balance is impossible

**Solutions:**
- Smoother curve
- Level scaling
- Skill matters more than stats
