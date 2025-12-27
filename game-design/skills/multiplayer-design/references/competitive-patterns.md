# Competitive Design Patterns

---

## Match Structure

### Round-Based
```
Round 1 → Round 2 → Round 3 → Winner
Best of 3/5/7
```

### Time-Limited
```
[Match starts] → [Time runs] → [Highest score wins]
```

### Elimination
```
[All start] → [Players eliminated] → [One remains]
```

---

## Win Condition Types

| Condition | Example | Design Notes |
|-----------|---------|--------------|
| Kill count | First to 10 kills | Pure combat focus |
| Last standing | Battle royale | Tension builds |
| Objective | Hold point | Map control emphasis |
| Score | Trick competition | Skill expression |
| Capture | Flag capture | Team coordination |

---

## Comeback Mechanics

| Mechanic | Effect | Risk |
|----------|--------|------|
| Respawn advantage | Losing player gets boost | Can feel unfair |
| Rubber banding | Catch-up help | Punishes leaders |
| Power plays | Down player gets tools | Exciting but swingy |
| None | Pure skill wins | Can be demoralizing |

**Balance:** Enough hope to keep trying, not enough to invalidate lead.

---

## Starting Positions

| Type | Fairness | Variety |
|------|----------|---------|
| Symmetric | High | Low |
| Random | Medium | High |
| Asymmetric with balance | High | High |

---

## Match Pacing

| Phase | Duration | Design Goal |
|-------|----------|-------------|
| Opening | 20-30% | Positioning, resource gathering |
| Mid-game | 40-50% | Core competition, trades |
| Endgame | 20-30% | Resolution, clutch plays |

---

## Character/Tool Balance

### Balance Philosophy
```
Rock-Paper-Scissors: A beats B, B beats C, C beats A
vs
Skill-based: All equal, execution determines winner
```

### Balance Testing
- [ ] All characters/tools can win
- [ ] No dominant strategy
- [ ] Counters exist but aren't hard
- [ ] Matchup variety
