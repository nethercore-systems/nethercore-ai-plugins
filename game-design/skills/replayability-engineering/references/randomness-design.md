# Randomness Design Reference

---

## Input vs Output Randomness

| Type | Example | Player Control | Fairness |
|------|---------|----------------|----------|
| **Input** | Cards dealt | Plan around it | High |
| **Output** | Damage roll | None | Low |

**Prefer input randomness** for important outcomes.

---

## Streak Protection

### Pity Timer
```
After N failures without success:
  - Guarantee success on N+1
  - OR increase odds significantly
```

Example: "Rare item guaranteed after 10 chests without one"

### Pseudo-Random Distribution
```
Base chance: 25%
After miss: +10% cumulative
After hit: Reset to base
```
Prevents long streaks while maintaining expected rate.

---

## Pool Weighting

| Rarity | Base Weight | When Pool Small | When Pool Large |
|--------|-------------|-----------------|-----------------|
| Common | 70% | 80% | 60% |
| Uncommon | 20% | 15% | 25% |
| Rare | 8% | 4% | 12% |
| Legendary | 2% | 1% | 3% |

Adjust weights based on pool size and game state.

---

## Contextual Randomness

| Context | Adjustment |
|---------|------------|
| Low health | Increase healing drops |
| No damage items | Weight damage items |
| Late game | Reduce common drops |
| Struggling player | Subtle assistance |

---

## Randomness Feels

| Feel | Cause | Fix |
|------|-------|-----|
| "Rigged against me" | Actual bad luck | Streak protection |
| "RNG carried me" | Actual good luck | Skill still required |
| "Unfair death" | Output randomness | Use input randomness |
| "Boring" | Too predictable | Add meaningful variance |

---

## Randomness Checklist

- [ ] Critical moments don't use output randomness
- [ ] Streak protection prevents extremes
- [ ] Skill matters more than luck
- [ ] Variance creates stories
- [ ] Same seed = same outcomes (for multiplayer)
