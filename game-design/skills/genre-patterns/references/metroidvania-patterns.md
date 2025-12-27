# Metroidvania Design Patterns

---

## World Structure

```
     [Late area] ← requires Ability C
          │
     [Mid area] ← requires Ability B
          │
[Start] ─ [Hub] ─ [Alt path] ← requires Ability A
          │
     [Early area]
```

---

## Ability Gating

| Gate Type | Example | Player Experience |
|-----------|---------|-------------------|
| Hard gate | Need double jump | Clear requirement |
| Soft gate | Can sequence break | Rewards mastery |
| Skill gate | Possible but hard | Optional challenge |

### Core Abilities Template

| Ability | Opens Access To | Acquired |
|---------|-----------------|----------|
| [Mobility 1] | | Early |
| [Mobility 2] | | Mid |
| [Combat upgrade] | | Mid |
| [Traversal] | | Late |

---

## Backtracking Value

Every return trip should offer:
- [ ] New areas accessible
- [ ] Hidden items now reachable
- [ ] Shortcuts unlocked
- [ ] Optional challenges available
- [ ] Faster traversal than before

---

## Map Design

### Map Features Checklist
- [ ] Rooms are distinguishable
- [ ] Landmarks visible on map
- [ ] Unexplored areas marked
- [ ] Current objective shown
- [ ] Fast travel available (late game)

### Room Density
```
Exploration-heavy: 80-150 rooms
Focused: 40-80 rooms
Compact: 20-40 rooms
```

---

## Sequence Breaking

### Levels of Sequence Breaking

| Level | Player Action | Designer Intent |
|-------|---------------|-----------------|
| Intended | Using abilities as designed | Expected |
| Skilled | Advanced technique use | Encouraged |
| Exploit | Engine/physics abuse | Tolerated |
| Bug | Unintended glitch | Often beloved |

---

## Save System

| System | Tension | Accessibility |
|--------|---------|---------------|
| Save rooms only | High | Low |
| Save + quick save | Medium | Medium |
| Save anywhere | Low | High |

For accessibility, consider: save anywhere + hard mode with save rooms.
