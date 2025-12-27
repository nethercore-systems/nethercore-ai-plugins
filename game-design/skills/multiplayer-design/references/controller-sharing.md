# Controller Sharing Patterns

---

## Input Configurations

### Standard (Each Player Has Controller)

```
Player 1: Controller 1 (full)
Player 2: Controller 2 (full)
Player 3: Controller 3 (full)
Player 4: Controller 4 (full)
```

### Shared Controller (Party Game)

```
Player 1: Left side (D-pad, L buttons)
Player 2: Right side (Face buttons, R buttons)
```
- Good for: Cooperative puzzles, party games
- Limit: Simple input requirements

### Pass-and-Play

```
Player 1 plays → [End turn] → Player 2 plays → ...
```
- Good for: Strategy, puzzle games
- Clear boundaries between turns

---

## Visual Feedback per Player

| Element | Purpose |
|---------|---------|
| Player color | Identify who is who |
| Player number | UI reference |
| Controller indicator | Show input device |
| Action highlights | Who did what |

### Color Conventions
```
Player 1: Blue/Red
Player 2: Green/Yellow
Player 3: Pink/Orange
Player 4: Purple/Cyan
```

---

## Screen Real Estate

### Split Screen Division

| Players | Layout |
|---------|--------|
| 2 | Horizontal or vertical split |
| 3 | 2 top, 1 bottom (or L-shape) |
| 4 | Quadrants |

### HUD Placement
- Individual HUDs near each player's screen area
- Shared info in center (timer, score)
- Don't obscure gameplay

---

## Input Latency Considerations

For local play:
- All controllers should feel identical
- No advantage from controller port

For online play:
- Rollback handles latency
- Design for up to 150ms playable

---

## Drop-in/Drop-out

### Joining
- [ ] Can join mid-game?
- [ ] What state do they enter in?
- [ ] How are they introduced?

### Leaving
- [ ] AI takes over?
- [ ] Character disappears?
- [ ] Game pauses?
- [ ] Remaining players continue?
