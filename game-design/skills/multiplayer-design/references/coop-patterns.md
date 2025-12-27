# Co-op Design Patterns

---

## Co-op Role Structures

### Symmetric Co-op
All players identical.
- **Pros:** Fair, no role drama, easy balance
- **Cons:** Less strategic depth, potential redundancy

### Class-Based Co-op
Distinct roles with equal importance.
```
Tank ←── Team ──→ Healer
           │
          DPS
```

### Asymmetric Co-op
Completely different gameplay.
- Player 1: Action gameplay
- Player 2: Strategy/management

---

## Engagement Patterns

### Always-Active
Both players constantly engaged.
- Best for: Action games
- Challenge: Balancing simultaneous demands

### Turn-Based Roles
Players alternate activity peaks.
- Best for: Puzzle co-op, strategy
- Challenge: Keeping inactive player engaged

### Support + Lead
One player primary, others assist.
- Best for: Story games with helpers
- Challenge: Support feeling meaningful

---

## Skill Disparity Handling

| Problem | Solution |
|---------|----------|
| Experienced + new player | Scalable difficulty, mentoring mechanics |
| Skill ceiling difference | Multiple valid contributions |
| One player carrying | Tasks requiring both players |
| Dead weight | Catch-up mechanics, support roles |

---

## Revive Systems

| System | Tension | Friendliness |
|--------|---------|--------------|
| No revive | Very high | Low |
| Timed revive | High | Medium |
| Instant revive | Low | High |
| Lives shared | Medium | Medium |
| Checkpoint revive | Medium | High |

---

## Co-op Checklist

- [ ] Both players needed to progress
- [ ] Both players always have something to do
- [ ] Communication is useful but not mandatory
- [ ] Different skill levels can enjoy together
- [ ] Victory feels shared
- [ ] Failure doesn't blame one player
