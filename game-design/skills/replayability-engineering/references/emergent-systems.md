# Emergent Systems Design

---

## System Interaction Matrix

Map how systems interact:

```
        Fire  Ice   Elec  Poison
Fire     -    Evap  Explode Cure
Ice     Evap   -    Shatter Freeze
Elec   Explode Shatter -    Spread
Poison  Cure  Freeze Spread  -
```

---

## Designing for Emergence

### Simple Rules, Complex Outcomes

| Rule | Emergent Behavior |
|------|-------------------|
| Fire spreads to oil | Chain reactions |
| Water conducts electricity | Area denial |
| Enemies flee from fire | Herding tactics |
| Poison stacks | Damage over time builds |

### Interaction Categories

| Category | Examples |
|----------|----------|
| Element × Element | Fire + ice = steam |
| Item × Item | Lifesteal + AoE = survival |
| Ability × Environment | Dash + pit = skip |
| Enemy × Enemy | Shield + ranged = combo |

---

## Synergy Design Template

```
SYNERGY: [Name]

Component A: _____________
Component B: _____________
Result: _____________

Discovery: □ Obvious □ Tutorial □ Experimentation □ Hidden
Power level: □ Minor □ Moderate □ Major □ Build-defining
Availability: □ Common □ Uncommon □ Rare
```

---

## Avoiding Broken Combos

| Issue | Detection | Fix |
|-------|-----------|-----|
| Infinite loops | Playtest extremes | Add cooldowns |
| One-shot everything | Damage caps | Diminishing returns |
| Invincibility | Edge cases | Time limits |
| Trivializes content | Win rate data | Nerf synergy |

---

## Emergence Checklist

- [ ] Systems interact in expected ways
- [ ] Unexpected interactions are fun (not broken)
- [ ] Discovery feels rewarding
- [ ] Multiple valid strategies exist
- [ ] Skill still matters with combos
