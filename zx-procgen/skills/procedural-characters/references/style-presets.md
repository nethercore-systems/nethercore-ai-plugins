# Style Presets

Visual style guides for different character aesthetics.

---

## Mecha / Mechanical

Sharp edges, blocky forms, abrupt transitions.

### Characteristics

- **Bases:** `square(4)` or `octagon(8)` for angular silhouettes
- **Scale transitions:** Abrupt (1.0 → 1.4 → 0.6)
- **Steps:** Fewer, larger extrusions
- **Caps:** All parts capped (`cap_end: true`) for solid look

### Example Scale Patterns

```yaml
# Sharp plate edge
- extrude: 0.01, scale: 1.4    # abrupt flare
- extrude: 0.05, scale: 1.0    # plate body
- extrude: 0.01, scale: 0.6    # abrupt return

# Angular joint
- extrude: 0.08, scale: 1.0    # limb segment
- extrude: 0.02, scale: 0.5    # sharp taper
```

### Visual Result

```
   ┌───────┐
   │       │   Flat surfaces
┌──┘       └──┐
│             │   Sharp corners
└──┐       ┌──┘
   │       │
   └───────┘
```

---

## Organic / Natural

Smooth curves, gradual transitions, muscle-like forms.

### Characteristics

- **Bases:** `hexagon(6)` or `octagon(8)` for rounder cross-sections
- **Scale transitions:** Gradual (1.0 → 1.05 → 1.1 → 1.15)
- **Steps:** More steps, smaller extrusions
- **Bulge:** Use `bulge` for anatomical asymmetry (+ front, - back)

### Example Patterns

```yaml
# Calf muscle (back bulge)
- extrude: 0.08, scale: 1.15, bulge: -0.018
- extrude: 0.08, scale: 0.95, bulge: -0.01
- extrude: 0.08, scale: 0.85, bulge: -0.005

# Chest (front bulge)
- extrude: 0.05, scale: [1.0, 1.1], bulge: 0.015
- extrude: 0.04, scale: [1.1, 1.05], bulge: 0.01

# Smooth torso curve
- extrude: 0.04, scale: [1.1, 1.15], bulge: -0.02   # pelvis
- extrude: 0.05, scale: [0.8, 0.85]                  # waist
- extrude: 0.05, scale: [1.0, 1.1], bulge: 0.015    # chest
```

### Visual Result

```
     ╭───╮
    ╭╯   ╰╮   Smooth curves
   ╭╯     ╰╮
   │       │  Gradual transitions
   ╰╮     ╭╯
    ╰╮   ╭╯
     ╰───╯
```

---

## Armored / Plated

Combination of base form with armor overlays.

### Characteristics

- **Bases:** Mix of `hexagon(6)` for body, `octagon(8)` for plates
- **Flare patterns:** Scale OUT → extrude → scale IN for plate edges
- **Layering:** Larger radius on armor parts than underlying body

### Example Armor Patterns

```yaml
# Pauldron (shoulder armor)
arm_upper_L:
  base: hexagon(6)
  base_radius: 0.045
  steps:
    - extrude: 0.02, scale: 1.5    # FLARE out
    - extrude: 0.04, scale: 1.0    # plate body
    - extrude: 0.015, scale: 0.6   # sharp return
    - extrude: 0.1, scale: 1.0     # arm beneath

# Chest plate
torso:
  base: octagon(8)
  base_radius: 0.12
  steps:
    - extrude: 0.05, scale: 1.0
    - extrude: 0.02, scale: 1.25   # plate edge
    - extrude: 0.08, scale: 1.0    # plate body
    - extrude: 0.02, scale: 0.8    # back to body
    - extrude: 0.1, scale: 0.9     # waist taper

# Gauntlet
arm_lower_L:
  base: hexagon(6)
  base_radius: 0.04
  steps:
    - extrude: 0.1, scale: 1.0
    - extrude: 0.02, scale: 1.3    # cuff flare
    - extrude: 0.03, scale: 1.0    # cuff body
    - extrude: 0.015, scale: 0.7   # wrist return
```

### Visual Result

```
   ╱────────╲
  ╱          ╲   Plate flare
 │            │
 │    body    │  Plate body
 │            │
  ╲          ╱   Sharp return
   ──────────
```

---

## Robed / Flowing

Extended torso that covers lower body.

### Characteristics

- **Extended torso:** Continues past hip bone
- **Scale expansion:** Gradual increase for flowing fabric
- **No separate legs:** Or legs hidden beneath robe
- **Triangle savings:** Fewer leg parts needed

### Example Robe Patterns

```yaml
torso_robed:
  bone: spine
  base: octagon(8)
  base_radius: 0.11
  steps:
    # Normal upper torso
    - extrude: 0.05, scale: 1.1
    - extrude: 0.08, scale: 1.0
    - extrude: 0.05, scale: 0.85   # waist

    # Robe extends down
    - extrude: 0.03, scale: 1.2    # hip flare
    - extrude: 0.1, scale: 1.3     # robe body
    - extrude: 0.12, scale: 1.35   # continue expanding
    - extrude: 0.1, scale: 1.4     # wide hem
    - extrude: 0.02, scale: 1.0    # hem edge
  cap_start: true
  cap_end: true                    # closed at bottom

# Optional visible feet
foot_L:
  bone: foot_L
  # ... normal foot pattern
  # Positioned to peek out from robe
```

### Visual Result

```
     ┌─┐
     │ │      Head/shoulders
   ┌─┘ └─┐
  ╱       ╲   Waist
 ╱         ╲
│           │ Expanding robe
│           │
╰───────────╯ Wide hem
```

---

## Chibi / Super-Deformed

Exaggerated proportions for cute characters.

### Characteristics

- **Large head:** 1.5-2x normal head size
- **Short limbs:** 50-70% normal length
- **Wide body:** Rounder, softer shapes
- **Stubby hands/feet:** Minimal detail

### Proportion Adjustments

```yaml
# Head: larger radius, more spherical
head:
  base: octagon(8)
  base_radius: 0.12     # 50% larger than normal
  steps:
    - extrude: 0.02, scale: 0.9
    - extrude: 0.08, scale: 1.4    # expand to sphere
    - extrude: 0.1, scale: 1.0     # maintain size
    - extrude: 0.06, scale: 0.7    # round top
    - extrude: 0.03, scale: 0.4

# Arms: shorter, stubbier
arm_upper_L:
  base: hexagon(6)
  base_radius: 0.04
  steps:
    - extrude: 0.06, scale: 1.0    # short segment
    - extrude: 0.02, scale: 0.85

arm_lower_L:
  base: hexagon(6)
  base_radius: 0.034
  steps:
    - extrude: 0.05, scale: 1.0    # very short
    - extrude: 0.02, scale: 0.8

# Torso: wider, rounder
torso:
  base: octagon(8)
  base_radius: 0.13
  steps:
    - extrude: 0.04, scale: 1.1
    - extrude: 0.06, scale: 1.0
    - extrude: 0.03, scale: 0.95
```

---

## Style Mixing

Combine elements for unique looks:

### Mecha + Organic (Cyborg)

```yaml
# Organic torso with mechanical arm
torso:
  base: hexagon(6)         # organic
  # ... smooth curves

arm_upper_L:
  base: square(4)          # mechanical
  # ... sharp angles
```

### Armored + Robed (Battle Mage)

```yaml
torso:
  # Upper: armor plates
  # Lower: flowing robe extension
  steps:
    - extrude: 0.02, scale: 1.3    # chest plate
    - extrude: 0.05, scale: 1.0
    - extrude: 0.02, scale: 0.7
    # ... then robe expansion
```

---

## Quick Reference

| Style | Base Shape | Scale Transitions | Steps | Special |
|-------|------------|-------------------|-------|---------|
| Mecha | square/octagon | Abrupt (1.0→1.4→0.6) | Fewer | All caps closed |
| Organic | hexagon/octagon | Gradual (1.0→1.05→1.1) | More | [X,Y] asymmetry |
| Armored | hexagon | OUT→flat→IN | Medium | Flare patterns |
| Robed | octagon | Expanding | Medium | Extended torso |
| Chibi | octagon | Exaggerated | Medium | 1.5x head, 0.6x limbs |
