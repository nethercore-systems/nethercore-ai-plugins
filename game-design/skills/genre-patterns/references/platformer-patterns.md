# Platformer Design Patterns

---

## Movement Feel Spectrum

```
Floaty ←────────────────────→ Tight
(Kirby)                      (Celeste)
   │                            │
   ├── Forgiving               ├── Precise
   ├── Accessible              ├── Demanding
   └── Relaxed                 └── Technical
```

---

## Jump Parameters

| Parameter | Low Value | High Value |
|-----------|-----------|------------|
| Jump height | Gentle platforming | Vertical levels |
| Air control | Committed jumps | Aerial precision |
| Gravity | Floaty feel | Snappy feel |
| Coyote time | Punishing | Forgiving |

### Recommended Starting Values
- Coyote time: 4-8 frames (67-133ms)
- Jump buffer: 6-10 frames (100-167ms)
- Variable jump: Release cuts velocity 50%

---

## Level Design Patterns

### Teaching Jump Distance
```
[Safe] → [Tutorial gap, safe fall] → [Real gap, consequence]
```

### Escalation Pattern
```
[Single obstacle]
    ↓
[Obstacle + timing]
    ↓
[Multiple obstacles]
    ↓
[Combination test]
```

---

## Hazard Checklist

- [ ] Visible before dangerous
- [ ] Consistent damage/death rules
- [ ] Fair tells (spikes look sharp, lava glows)
- [ ] Recovery period after hit (i-frames)
- [ ] Respawn is quick

---

## Common Platformer Features

| Feature | Purpose | Complexity |
|---------|---------|------------|
| Double jump | Accessibility, air correction | Low |
| Wall jump | Verticality, recovery | Medium |
| Dash | Speed, precision | Medium |
| Grapple | Mobility, spectacle | High |
| Transform | Variety, puzzles | High |
