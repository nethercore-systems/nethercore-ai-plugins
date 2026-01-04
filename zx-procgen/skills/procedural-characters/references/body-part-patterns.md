# Body Part Patterns

Reusable patterns for common body parts. Copy and modify for your character.

## Anatomy Quick Ref

| Part | Bulge | Value |
|------|-------|-------|
| Calf | back (-) | -0.015 |
| Glutes | back (-) | -0.02 |
| Chest (F) | front (+) | +0.025 |
| Bicep | front (+) | +0.01 |
| Hamstring | back (-) | -0.008 |

---

## Torso Patterns

### Simple Tube Torso

Basic cylindrical torso. Fast, low tri count.

```yaml
torso:
  bone: spine
  base: hexagon(6)
  base_radius: 0.12
  steps:
    - extrude: 0.05, scale: 1.15    # chest expand
    - extrude: 0.15, scale: 1.0     # chest body
    - extrude: 0.08, scale: 0.85    # waist taper
    - extrude: 0.02, scale: 1.1     # belt flare
  cap_start: true
  cap_end: false
```

### Anatomical Torso

Uses bulge for front/back curvature (replaces translate for anatomy).

```yaml
torso:
  bone: spine
  base: octagon(8)
  base_radius: [0.12, 0.10]
  steps:
    - extrude: 0.04, scale: [1.1, 1.15], bulge: -0.02    # pelvis/glutes
    - extrude: 0.04, scale: [1.0, 1.05], bulge: -0.01    # lower back
    - extrude: 0.05, scale: [0.8, 0.85]                   # waist
    - extrude: 0.04, scale: [0.85, 0.95], bulge: 0.01    # stomach
    - extrude: 0.05, scale: [1.0, 1.1], bulge: 0.015     # chest
    - extrude: 0.04, scale: [1.1, 1.05], bulge: 0.01     # upper chest
    - extrude: 0.04, scale: [1.25, 0.9], bulge: -0.005   # shoulders
  cap_start: true
  cap_end: false
```

### Proportion Notes

**Masculine:** Shoulders 1.3+, hips 0.9, minimal waist taper
**Feminine:** Shoulders 1.1, hips 1.1+, waist 0.7, chest bulge +0.025

---

## Head Patterns

### Helmet Head

Armored character with visor.

```yaml
head:
  bone: head
  base: hexagon(6)
  base_radius: 0.08
  steps:
    - extrude: 0.02, scale: 1.2     # helmet brim
    - extrude: 0.15, scale: 1.0     # helmet body
    - extrude: 0.05, scale: 0.6     # top taper
  cap_start: false                  # open for neck
  cap_end: true
```

### Organic Head

Anatomical head with face structure.

```yaml
head:
  bone: head
  base: octagon(8)
  base_radius: 0.09
  steps:
    # NECK
    - extrude: 0.03, scale: 0.85

    # JAW - push forward for chin
    - extrude: 0.04
      scale: [1.1, 1.15]
      translate: [0, 0.02, 0]

    # FACE - flatten front, rounder back
    - extrude: 0.06
      scale: [1.15, 1.0]
      translate: [0, 0.015, 0]

    # BROW
    - extrude: 0.03
      scale: [1.05, 1.1]
      translate: [0, 0.01, 0]

    # FOREHEAD - recede slightly
    - extrude: 0.04
      scale: [1.0, 0.95]
      translate: [0, -0.01, 0]

    # CROWN - round off
    - extrude: 0.04, scale: 0.85
    - extrude: 0.02, scale: 0.5
  cap_start: false
  cap_end: true
```

### Stylized Head (Chibi)

Large, round head for cute characters.

```yaml
head:
  bone: head
  base: octagon(8)
  base_radius: 0.12
  steps:
    - extrude: 0.02, scale: 0.9     # neck transition
    - extrude: 0.08, scale: 1.3     # expand to ball
    - extrude: 0.1, scale: 1.0      # main sphere
    - extrude: 0.08, scale: 0.8     # taper top
    - extrude: 0.04, scale: 0.4     # close
  cap_start: false
  cap_end: true
```

---

## Limb Patterns

### Upper Arm

```yaml
arm_upper_L:
  bone: arm_upper_L
  base: hexagon(6)
  base_radius: 0.045
  steps:
    - extrude: 0.03, scale: 1.3     # shoulder/pauldron area
    - extrude: 0.02, scale: 0.65    # shoulder taper
    - extrude: 0.12, scale: 1.0     # arm body
    - extrude: 0.03, scale: 0.85    # elbow taper
  cap_start: true
  cap_end: false                    # open for lower arm
```

### Lower Arm

```yaml
arm_lower_L:
  bone: arm_lower_L
  base: hexagon(6)                  # must match arm_upper
  base_radius: 0.038
  steps:
    - extrude: 0.02, scale: 1.1     # elbow area
    - extrude: 0.12, scale: 0.9     # forearm taper
    - extrude: 0.04, scale: 1.15    # wrist cuff
    - extrude: 0.02, scale: 0.7     # wrist
  cap_start: false                  # connects to upper
  cap_end: true                     # closed for hand stub
```

### Upper Leg

```yaml
leg_upper_L:
  bone: leg_upper_L
  base: hexagon(6)
  base_radius: 0.055
  steps:
    - extrude: 0.03, scale: 1.1     # hip area
    - extrude: 0.15, scale: [1.0, 1.1]  # thigh (back bulge)
    - extrude: 0.1, scale: 0.8      # knee taper
  cap_start: true
  cap_end: false
```

### Lower Leg

```yaml
leg_lower_L:
  bone: leg_lower_L
  base: hexagon(6)
  base_radius: 0.045
  steps:
    - extrude: 0.02, scale: 1.1                          # knee
    - extrude: 0.08, scale: 1.15, bulge: -0.018          # calf peak
    - extrude: 0.08, scale: 0.95, bulge: -0.01           # mid calf
    - extrude: 0.08, scale: 0.85, bulge: -0.005          # lower calf
    - extrude: 0.04, scale: 0.9                          # ankle
    - extrude: 0.03, scale: 1.15                         # boot cuff
  cap_start: false
  cap_end: true
```

---

## Hand Patterns

### Stub Hand

Simplest option (~0 extra tris, just close arm_lower).

```yaml
# No separate hand - just set cap_end: true on arm_lower
```

### Mitten Hand (~12 tris)

```yaml
hand_L:
  bone: hand_L
  base: hexagon(6)
  base_radius: 0.025
  steps:
    - extrude: 0.02, scale: [1.3, 0.7]   # flatten into palm
    - extrude: 0.04, scale: 1.0          # palm body
    - extrude: 0.03, scale: [0.9, 1.1]   # taper to fingers
    - extrude: 0.025, scale: 0.6         # fingertip
  cap_start: false
  cap_end: true

  thumb:
    bone: hand_L
    base: square(4)
    base_radius: 0.012
    offset: [-0.02, 0.01, 0.015]
    rotation: [0, 0, -45]
    steps:
      - extrude: 0.02, scale: 0.9
      - extrude: 0.015, scale: 0.6
    cap_start: true
    cap_end: true
```

### 3-Finger Hand (~30 tris)

```yaml
hand_L:
  bone: hand_L
  base: hexagon(6)
  base_radius: 0.025
  steps:
    - extrude: 0.02, scale: [1.2, 0.6]   # flatten palm
    - extrude: 0.035, scale: 1.0         # palm
  cap_start: false
  cap_end: false                         # open for fingers

  fingers:
    - name: index
      base: square(4)
      base_radius: 0.008
      offset: [0.012, 0, 0]
      steps:
        - extrude: 0.025, scale: 0.9
        - extrude: 0.02, scale: 0.7
      cap_start: true
      cap_end: true

    - name: middle
      base: square(4)
      base_radius: 0.009
      offset: [0, 0, 0]
      steps:
        - extrude: 0.03, scale: 0.85
        - extrude: 0.02, scale: 0.65
      cap_start: true
      cap_end: true

    - name: ring
      base: square(4)
      base_radius: 0.008
      offset: [-0.012, 0, 0]
      steps:
        - extrude: 0.025, scale: 0.9
        - extrude: 0.018, scale: 0.7
      cap_start: true
      cap_end: true

  thumb:
    base: square(4)
    base_radius: 0.01
    offset: [0.022, 0.012, -0.01]
    rotation: [0, 0, -60]
    steps:
      - extrude: 0.018, scale: 0.9
      - extrude: 0.015, scale: 0.65
    cap_start: true
    cap_end: true
```

---

## Foot Patterns

### Boot Foot

```yaml
foot_L:
  bone: foot_L
  base: hexagon(6)
  base_radius: 0.035
  steps:
    # Ankle
    - extrude: 0.02, scale: 1.1

    # Heel - push backward
    - extrude: 0.025
      scale: [1.0, 1.3]
      translate: [0, -0.02, 0]

    # Sole - flatten and extend forward
    - extrude: 0.015
      scale: [1.1, 0.8]
      translate: [0, 0.04, 0]

    # Toe box
    - extrude: 0.04
      scale: [0.9, 0.9]
      translate: [0, 0.02, 0]

    # Toe tip
    - extrude: 0.02, scale: 0.6
  cap_start: false
  cap_end: true
```

### Stub Foot

For simpler characters, just close the leg_lower.

```yaml
# Set leg_lower cap_end: true, no separate foot part
```

---

## Hair Patterns

### Spiky Hair

Multiple triangular spikes parented to head.

```yaml
hair_spiky:
  bone: head
  base: triangle(3)
  base_radius: 0.02
  instances:
    - position: [0, -0.05, 0.18], rotation: [-20, 0, 0]     # back spike
    - position: [0.04, -0.03, 0.17], rotation: [-15, 20, 0]
    - position: [-0.04, -0.03, 0.17], rotation: [-15, -20, 0]
    - position: [0, 0, 0.19], rotation: [10, 0, 0]          # top spike
  steps:
    - extrude: 0.08, scale: 0.7
    - extrude: 0.06, scale: 0.3
  cap_start: true
  cap_end: true
```

### Bob Hair

Helmet-like hair surrounding head.

```yaml
hair_bob:
  bone: head
  base: octagon(8)
  base_radius: 0.11                # larger than head
  offset: [0, 0, 0.08]             # positioned around upper head
  steps:
    - extrude: 0.02, scale: 1.05
    - extrude: 0.08, scale: 1.1
    - extrude: 0.06, scale: 0.95
    - extrude: 0.04, scale: 0.7
  cap_start: true
  cap_end: true
```

### Ponytail

Single flowing shape from back of head.

```yaml
hair_ponytail:
  bone: head                       # or dedicated ponytail bone
  base: hexagon(6)
  base_radius: 0.03
  offset: [0, -0.08, 0.12]         # back of head
  steps:
    - extrude: 0.05, scale: 1.1
    - extrude: 0.12, scale: 0.9
    - extrude: 0.08, scale: 0.7
    - extrude: 0.05, scale: 0.4
  cap_start: true
  cap_end: true
```

---

## Clothing Patterns

Use scale OUT then IN to create edges/flares:

```
    │    │     bare arm
    │    │
   ┌┘    └┐    scale: 1.25 (sleeve edge)
  ┌┘      └┐
  │        │   extrude (sleeve body)
  └┐      ┌┘
   └┐    ┌┘    scale: 0.7 (back to arm)
    │    │
```

### Sleeve

```yaml
arm_with_sleeve:
  bone: arm_upper_L
  base: hexagon(6)
  base_radius: 0.045
  steps:
    - extrude: 0.08, scale: 0.9       # shoulder
    - extrude: 0.02, scale: 1.25      # sleeve FLARE
    - extrude: 0.06, scale: 1.0       # sleeve body
    - extrude: 0.02, scale: 0.7       # back to arm width
    - extrude: 0.10, scale: 1.0       # exposed arm
  cap_start: true
  cap_end: false
```

### Armor Plate

Sharp scale transitions for hard edges:

```yaml
pauldron:
  bone: arm_upper_L
  base: octagon(8)
  base_radius: 0.06
  steps:
    - extrude: 0.01, scale: 1.4       # sharp flare
    - extrude: 0.03, scale: 1.0       # plate body
    - extrude: 0.01, scale: 0.5       # sharp return
  cap_start: true
  cap_end: false
```

### Robe/Skirt

Extended torso that covers legs:

```yaml
torso_robed:
  bone: spine
  base: octagon(8)
  base_radius: 0.12
  steps:
    # ... normal torso steps ...
    # Then extend past hip level:
    - extrude: 0.1, scale: 1.3        # skirt flare
    - extrude: 0.2, scale: 1.1        # skirt body
    - extrude: 0.15, scale: 1.05      # continue down
    - extrude: 0.1, scale: 0.95       # taper at hem
  cap_start: true
  cap_end: true                       # closed at bottom
```

---

## Non-Humanoid Parts

### Spider Leg (single segment)

```yaml
leg_front_L:
  bone: leg_front_L
  base: square(4)
  base_radius: 0.015
  steps:
    - extrude: 0.02, scale: 1.2       # joint bulge
    - extrude: 0.08, scale: 0.8       # taper
    - extrude: 0.05, scale: 0.6       # tip
  cap_start: true
  cap_end: true
```

### Serpent Segment

```yaml
segment_1:
  bone: segment_1
  base: octagon(8)
  base_radius: 0.08
  steps:
    - extrude: 0.05, scale: 1.02      # slight bulge
    - extrude: 0.08, scale: 1.0       # body
    - extrude: 0.02, scale: 0.98      # slight taper
  cap_start: false                    # connects to previous
  cap_end: false                      # connects to next
```

### Wing (flat membrane)

```yaml
wing_L:
  bone: wing_upper_L
  base: square(4)
  base_radius: 0.02
  steps:
    - extrude: 0.01, scale: [3.0, 0.3]    # flatten wide
    - extrude: 0.15, scale: [1.2, 1.0]    # extend outward
    - extrude: 0.1, scale: [0.7, 1.0]     # taper tip
  cap_start: true
  cap_end: true
```

### Tail

```yaml
tail:
  bone: tail
  base: hexagon(6)
  base_radius: 0.04
  steps:
    - extrude: 0.05, scale: 1.1       # base bulge
    - extrude: 0.1, scale: 0.9        # taper
    - extrude: 0.08, scale: 0.7
    - extrude: 0.06, scale: 0.5
    - extrude: 0.04, scale: 0.3       # tip
  cap_start: false                    # connects to pelvis
  cap_end: true
```

---

## Feminine Patterns

### Feminine Torso

Narrower shoulders, wider hips, chest/glute bulges.

```yaml
torso_feminine:
  bone: spine
  base: octagon(8)
  base_radius: [0.11, 0.09]
  steps:
    - extrude: 0.04, scale: [1.15, 1.1], bulge: -0.025   # glutes
    - extrude: 0.03, scale: [1.05, 1.0], bulge: -0.015
    - extrude: 0.05, scale: [0.7, 0.8]                    # waist
    - extrude: 0.03, scale: [0.75, 0.9], bulge: 0.005    # stomach
    - extrude: 0.03, scale: [0.85, 1.0], bulge: 0.015    # under bust
    - extrude: 0.04, scale: [0.95, 1.15], bulge: 0.03    # bust
    - extrude: 0.03, scale: [1.0, 1.0], bulge: 0.015     # upper chest
    - extrude: 0.04, scale: [1.1, 0.9]                    # shoulders
  cap_start: true
  cap_end: false
```

### Feminine Hips

Pelvis bone points DOWN (head at top, tail at bottom). Creates V-taper toward groin.

```yaml
hips_feminine:
  bone: pelvis        # tail below head
  base: hexagon(6)
  base_radius: [0.18, 0.13]
  steps:
    - extrude: 0.25, scale: [1.0, 1.0], bulge: -0.025    # glute peak
    - extrude: 0.35, scale: [0.75, 0.85], bulge: -0.015  # narrowing
    - extrude: 0.5, scale: [0.35, 0.5]                    # groin V-taper
  cap_start: true
  cap_end: true
```

### Upper Leg with Glute Attachment

```yaml
leg_upper_feminine_L:
  bone: leg_upper_L
  base: hexagon(6)
  base_radius: 0.085
  steps:
    - extrude: 0.15, scale: 1.0, bulge: -0.015           # glute attachment
    - extrude: 0.25, scale: 0.92, bulge: -0.008          # upper thigh
    - extrude: 0.35, scale: 0.85                          # mid thigh
    - extrude: 0.3, scale: 0.75                           # knee
  cap_start: true
  cap_end: false
```
