# Procedural Variety Reference

---

## Generation Approaches

| Approach | Variety | Quality Control | Cost |
|----------|---------|-----------------|------|
| Pure random | Very high | Very low | Low |
| Template + variation | High | High | Medium |
| Rule-based | Medium | High | High |
| Handcrafted pool | Low | Very high | Very high |

**Recommended:** Template + variation for most indies.

---

## Template + Variation Method

```
1. Create handcrafted room templates (10-30)
2. Add variation points:
   - Enemy spawn points
   - Item placement
   - Obstacle positions
   - Visual variants
3. Combine templates procedurally
4. Apply constraints (difficulty, pacing)
```

---

## Seed-Based Generation

### Implementation Pattern
```
master_seed = player_input OR random
level_seed = hash(master_seed, level_number)
enemy_seed = hash(level_seed, "enemies")
item_seed = hash(level_seed, "items")
```

### Requirements for Nethercore
- All randomness from seed
- Same seed = same generation
- Enables rollback multiplayer
- Enables shared runs

---

## Constraining Randomness

### Rules Examples
- "At least 1 healing item per zone"
- "Boss difficulty ≤ average item power"
- "No more than 3 same enemy type per room"
- "Critical path always exists"

### Validation
```
Generate → Validate → (Pass) Use OR (Fail) Regenerate
```
Set regeneration limit to avoid infinite loops.

---

## Procedural Checklist

- [ ] Seed controls all randomness
- [ ] Templates ensure quality floor
- [ ] Constraints prevent soft-locks
- [ ] Edge cases tested
- [ ] Performance acceptable
- [ ] Variety feels meaningful
