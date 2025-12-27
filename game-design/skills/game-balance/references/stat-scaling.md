# Stat Scaling Reference

---

## Power Multiplier Table

| Game Progress | Player Power | Enemy Power | Gap |
|--------------|--------------|-------------|-----|
| 0% (start) | 1.0x | 1.0x | 0% |
| 25% | 1.5x | 1.4x | +7% player |
| 50% | 2.0x | 1.9x | +5% player |
| 75% | 2.7x | 2.6x | +4% player |
| 100% | 3.5x | 3.3x | +6% player |

**Note:** Slight player advantage makes progression feel good.

---

## Common Stat Ranges

### Health

| Entity | Start | End |
|--------|-------|-----|
| Player | 100 | 300-500 |
| Fodder enemy | 20-40 | 60-100 |
| Soldier enemy | 50-80 | 150-250 |
| Boss | 500-1000 | 2000-5000 |

### Damage

| Source | Start | End |
|--------|-------|-----|
| Player attack | 10-15 | 30-50 |
| Player special | 25-40 | 80-150 |
| Fodder attack | 5-10 | 15-25 |
| Boss attack | 20-30 | 50-100 |

---

## Time-to-Kill Targets

| Enemy Type | Target TTK | Feeling |
|------------|------------|---------|
| Fodder | 1-3 seconds | Quick, satisfying |
| Soldier | 5-10 seconds | Moderate engagement |
| Elite | 15-30 seconds | Significant fight |
| Boss | 2-5 minutes | Epic encounter |

---

## Formula Templates

### Linear Scaling
```
Stat = Base + (Level × Growth)
Example: HP = 100 + (Level × 20)
```

### Percentage Scaling
```
Stat = Base × (1 + Level × 0.1)
Example: Damage = 10 × (1 + Level × 0.1)
```

### Diminishing Returns
```
Stat = Base × (1 - 0.99^Level)
Example: Defense = 100 × (1 - 0.99^Level)
```

---

## Balance Red Flags

- [ ] One-shots at appropriate gear level
- [ ] Fights lasting >1 minute for regular enemies
- [ ] Required grinding to progress
- [ ] Stats feel meaningless (tiny differences)
- [ ] Dramatic power cliff between areas
