# RPG Design Patterns

---

## RPG Subgenres

| Type | Combat | Focus |
|------|--------|-------|
| Turn-based | Menu/tactical | Strategy, party |
| Action RPG | Real-time | Reflexes, builds |
| Tactical | Grid/position | Planning, resources |

---

## Core Systems

### Character Growth
- [ ] Level-based (XP → level → stats)
- [ ] Skill-based (use it → improve it)
- [ ] Equipment-based (gear defines power)
- [ ] Hybrid

### Class/Build System
- [ ] Fixed classes
- [ ] Flexible skill trees
- [ ] Classless (free point distribution)
- [ ] Job/class switching

### Stat Design

| Stat | Affects | Common Range |
|------|---------|--------------|
| Strength | Physical damage | 1-100 |
| Defense | Damage reduction | 1-100 |
| Speed | Turn order, evasion | 1-100 |
| Magic | Spell power | 1-100 |
| HP | Survivability | 50-9999 |
| MP | Resource pool | 20-999 |

---

## Party Design

### Party Size
- 1 (solo): Deep single-character build
- 3-4: Classic party, role balance
- 5-6: Tactical complexity
- Large (6+): Management focus

### Role Balance
```
Tank (absorbs damage)
  │
  ├── DPS (deals damage)
  │
  └── Support (heals/buffs)
```

---

## Loot/Equipment Checklist

- [ ] Visible stat improvements
- [ ] Clear rarity tiers
- [ ] Meaningful choices (not just "bigger numbers")
- [ ] Equipment affects appearance (optional but engaging)
- [ ] Trade-offs exist (not all upgrades)

---

## Quest Checklist

- [ ] Main quest is always clear
- [ ] Side quests are truly optional
- [ ] Rewards match effort
- [ ] Quest log is manageable
- [ ] Completion is trackable
