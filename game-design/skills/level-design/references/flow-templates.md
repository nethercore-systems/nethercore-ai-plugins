# Level Flow Templates

Copy and adapt these flow patterns for your levels.

---

## Linear Flow

```
[Start] → [A] → [B] → [C] → [End]
```

**Best for:** Tutorials, story sequences, controlled pacing
**Risk:** Can feel restrictive

---

## Branching Flow

```
           ┌→ [B1] ─┐
[Start] → [A]       ├→ [C] → [End]
           └→ [B2] ─┘
```

**Best for:** Player choice, difficulty options, replayability
**Risk:** Doubled content cost

---

## Hub Flow

```
           [B]
            │
   [A] ─── [HUB] ─── [C]
            │
           [D]
```

**Best for:** Towns, central areas, player-directed exploration
**Risk:** Can feel directionless

---

## Loop Flow

```
[Start] → [A] → [B]
             ↖   ↓
              [C]
               ↓
            [End]
```

**Best for:** Shortcuts, backtracking rewards, spatial awareness
**Risk:** Can confuse players

---

## Network Flow (Metroidvania)

```
[A] ─── [B] ─── [C]
 │       │       │
[D] ─── [E] ─── [F]
 │       │       │
[G] ─── [H] ─── [I]
```

**Best for:** Exploration-focused games, gated progression
**Risk:** Complex to design and balance

---

## Arena Flow

```
     ┌─────────────┐
     │    [A]      │
     │   ╱   ╲     │
[Entry]        [Exit]
     │   ╲   ╱     │
     │    [B]      │
     └─────────────┘
```

**Best for:** Boss fights, combat encounters, setpieces
**Risk:** Can feel isolated from level

---

## Layered Flow

```
Level 1: [A1] → [B1] → [C1]
              ↓
Level 2: [A2] → [B2] → [C2]
              ↓
Level 3: [A3] → [B3] → [C3]
```

**Best for:** Multi-floor buildings, ascending/descending journeys
**Risk:** Requires clear vertical orientation

---

## Flow Combination Example

```
[Tutorial] → [Hub]
               │
    ┌──────────┼──────────┐
    ↓          ↓          ↓
[Zone A]   [Zone B]   [Zone C]
(linear)   (branching) (network)
    │          │          │
    └──────────┼──────────┘
               ↓
            [Finale]
            (arena)
```

---

## Flow Design Checklist

- [ ] Flow matches level purpose
- [ ] Critical path is clear
- [ ] Optional paths are rewarding
- [ ] Backtracking is minimized or useful
- [ ] Players can orient themselves
- [ ] Pacing varies throughout
