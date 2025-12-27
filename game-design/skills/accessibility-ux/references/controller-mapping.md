# Controller Mapping Reference

---

## Standard Layouts by Genre

### Platformer
```
L1: ______          R1: Item/Dash
L2: ______          R2: ______

D-Pad: Movement     Y: ______
(alt movement)      B: Special
                    A: Jump
                    X: Attack

Left Stick: Move    Right Stick: ______
```

### Action RPG
```
L1: Lock-on         R1: Light attack
L2: Block           R2: Heavy attack

D-Pad: Items        Y: Item use
                    B: Dodge
                    A: Interact
                    X: Special

Left Stick: Move    Right Stick: Camera
```

### Twin-Stick Shooter
```
L1: ______          R1: Fire
L2: Special 1       R2: Special 2

D-Pad: Weapon swap  Y: Reload
                    B: Dash
                    A: ______
                    X: Interact

Left Stick: Move    Right Stick: Aim
```

---

## Alternative Layouts

### Lefty
Swap left/right stick functions
Swap L/R buttons

### One-Handed (Right)
```
D-Pad: Movement (via right stick)
Face buttons: Primary actions
R1/R2: Modifiers
```

### Simplified
Fewer required inputs:
- Combine similar functions
- Auto-aim enabled
- No simultaneous button presses

---

## Button Priority

| Priority | Button | Usage |
|----------|--------|-------|
| 1 | A/X | Primary action (jump, confirm) |
| 2 | X/Square | Secondary action (attack) |
| 3 | B/Circle | Tertiary/cancel |
| 4 | Y/Triangle | Context/special |
| 5 | R1/RB | Primary modifier |
| 6 | L1/LB | Secondary modifier |
| 7 | R2/RT | Trigger action |
| 8 | L2/LT | Trigger action |

---

## Remapping Checklist

- [ ] Every action mappable to every button
- [ ] Conflicts detected and warned
- [ ] Preview mapping before save
- [ ] Multiple profiles supported
- [ ] Reset to default option
