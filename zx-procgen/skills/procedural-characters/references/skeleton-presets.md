# Skeleton Presets

Standard skeleton hierarchies for different creature types. Copy and modify for your character's `.spec.py` file.

---

## Humanoid (20 bones)

Standard bipedal humanoid. Suitable for players, NPCs, humanoid enemies.

```python
"skeleton": [
    # CORE (6 bones)
    {"bone": "pelvis", "parent": None, "head": [0, 0, 0.9], "tail": [0, 0, 1.0]},
    {"bone": "spine", "parent": "pelvis", "head": [0, 0, 1.0], "tail": [0, 0, 1.3]},
    {"bone": "head", "parent": "spine", "head": [0, 0, 1.3], "tail": [0, 0, 1.55]},

    # LEFT ARM (4 bones)
    {"bone": "arm_upper_L", "parent": "spine", "head": [-0.15, 0, 1.25], "tail": [-0.35, 0, 1.15]},
    {"bone": "arm_lower_L", "parent": "arm_upper_L", "head": [-0.35, 0, 1.15], "tail": [-0.55, 0, 1.05]},
    {"bone": "hand_L", "parent": "arm_lower_L", "head": [-0.55, 0, 1.05], "tail": [-0.65, 0, 1.0]},

    # LEFT LEG (4 bones)
    {"bone": "leg_upper_L", "parent": "pelvis", "head": [-0.08, 0, 0.9], "tail": [-0.08, 0, 0.5]},
    {"bone": "leg_lower_L", "parent": "leg_upper_L", "head": [-0.08, 0, 0.5], "tail": [-0.08, 0, 0.1]},
    {"bone": "foot_L", "parent": "leg_lower_L", "head": [-0.08, 0, 0.1], "tail": [-0.08, 0.1, 0.05]},

    # RIGHT SIDE (mirrors)
    {"bone": "arm_upper_R", "mirror": "arm_upper_L"},
    {"bone": "arm_lower_R", "mirror": "arm_lower_L"},
    {"bone": "hand_R", "mirror": "hand_L"},
    {"bone": "leg_upper_R", "mirror": "leg_upper_L"},
    {"bone": "leg_lower_R", "mirror": "leg_lower_L"},
    {"bone": "foot_R", "mirror": "foot_L"},
]
```

### Humanoid Variations

**Chibi (shorter limbs, larger head):**
- Scale head bone tail.z to 1.7 (larger head)
- Reduce arm/leg lengths by 30%
- Widen pelvis (head.x = ±0.12)

**Tall/Lanky:**
- Increase spine length (tail.z = 1.4)
- Extend arm/leg bones by 20%
- Reduce pelvis width

**Stocky/Dwarf:**
- Reduce spine length (tail.z = 1.15)
- Widen pelvis and shoulders
- Shorten legs significantly

**Feminine (V-taper hips):**
- Pelvis points DOWN: head at 1.0, tail at 0.85
- Wider hips: leg attachment at ±0.09
- Narrower shoulders: arm attachment at ±0.16
- Allows hip mesh to extrude toward groin with V-taper

---

## Quadruped (18 bones)

Four-legged creature with horizontal spine. For dogs, wolves, horses, etc.

```python
"skeleton": [
    # CORE (6 bones)
    {"bone": "pelvis", "parent": None, "head": [0, -0.4, 0.5], "tail": [0, -0.3, 0.5]},
    {"bone": "spine", "parent": "pelvis", "head": [0, -0.3, 0.5], "tail": [0, 0.1, 0.55]},
    {"bone": "chest", "parent": "spine", "head": [0, 0.1, 0.55], "tail": [0, 0.4, 0.6]},
    {"bone": "neck", "parent": "chest", "head": [0, 0.4, 0.6], "tail": [0, 0.5, 0.75]},
    {"bone": "head", "parent": "neck", "head": [0, 0.5, 0.75], "tail": [0, 0.7, 0.8]},
    {"bone": "tail", "parent": "pelvis", "head": [0, -0.4, 0.5], "tail": [0, -0.7, 0.4]},

    # FRONT LEGS (4 bones)
    {"bone": "front_leg_upper_L", "parent": "chest", "head": [-0.1, 0.35, 0.55], "tail": [-0.1, 0.35, 0.3]},
    {"bone": "front_leg_lower_L", "parent": "front_leg_upper_L", "head": [-0.1, 0.35, 0.3], "tail": [-0.1, 0.35, 0.05]},
    {"bone": "front_leg_upper_R", "mirror": "front_leg_upper_L"},
    {"bone": "front_leg_lower_R", "mirror": "front_leg_lower_L"},

    # BACK LEGS (4 bones)
    {"bone": "back_leg_upper_L", "parent": "pelvis", "head": [-0.1, -0.35, 0.5], "tail": [-0.1, -0.35, 0.25]},
    {"bone": "back_leg_lower_L", "parent": "back_leg_upper_L", "head": [-0.1, -0.35, 0.25], "tail": [-0.1, -0.35, 0.05]},
    {"bone": "back_leg_upper_R", "mirror": "back_leg_upper_L"},
    {"bone": "back_leg_lower_R", "mirror": "back_leg_lower_L"},
]
```

### Quadruped Variations

**Horse (longer legs, longer neck):**
- Extend leg bones by 40%
- Longer neck (0.3 units)
- Smaller head relative to body

**Dog/Wolf (standard):**
- Use preset as-is
- Adjust tail length for breed

**Cat (shorter, more compact):**
- Reduce all dimensions by 20%
- More curved spine (adjust Y positions)
- Longer tail

---

## Serpent (Variable bones)

Snake-like creature with segmented body. Bone count depends on desired flexibility.

```python
"skeleton": [
    {"bone": "head", "parent": None, "head": [0, 0, 0.1], "tail": [0, 0.15, 0.15]},
    {"bone": "segment_1", "parent": "head", "head": [0, 0, 0.1], "tail": [0, -0.15, 0.1]},
    {"bone": "segment_2", "parent": "segment_1", "head": [0, -0.15, 0.1], "tail": [0, -0.3, 0.1]},
    {"bone": "segment_3", "parent": "segment_2", "head": [0, -0.3, 0.1], "tail": [0, -0.45, 0.1]},
    {"bone": "segment_4", "parent": "segment_3", "head": [0, -0.45, 0.1], "tail": [0, -0.6, 0.1]},
    {"bone": "segment_5", "parent": "segment_4", "head": [0, -0.6, 0.1], "tail": [0, -0.75, 0.08]},
    {"bone": "tail_tip", "parent": "segment_5", "head": [0, -0.75, 0.08], "tail": [0, -0.9, 0.05]},
]
```

### Serpent Notes

- Add more segments for longer snakes (8-12 typical)
- Taper Z position for body curve
- All parts use same base shape for seamless body
- Single tubular mesh, no limbs

---

## Spider (12 bones)

Arthropod with two body segments and 8 legs.

```python
"skeleton": [
    # BODY (2 bones)
    {"bone": "cephalothorax", "parent": None, "head": [0, 0, 0.15], "tail": [0, 0.15, 0.15]},
    {"bone": "abdomen", "parent": "cephalothorax", "head": [0, 0, 0.15], "tail": [0, -0.25, 0.12]},

    # FRONT LEGS (4 bones - left side)
    {"bone": "leg_front_L", "parent": "cephalothorax", "head": [-0.08, 0.08, 0.15], "tail": [-0.25, 0.2, 0.05]},
    {"bone": "leg_mid_front_L", "parent": "cephalothorax", "head": [-0.08, 0.02, 0.15], "tail": [-0.28, 0.05, 0.05]},
    {"bone": "leg_mid_back_L", "parent": "cephalothorax", "head": [-0.08, -0.04, 0.15], "tail": [-0.28, -0.1, 0.05]},
    {"bone": "leg_back_L", "parent": "cephalothorax", "head": [-0.08, -0.1, 0.15], "tail": [-0.25, -0.25, 0.05]},

    # RIGHT LEGS (mirrors)
    {"bone": "leg_front_R", "mirror": "leg_front_L"},
    {"bone": "leg_mid_front_R", "mirror": "leg_mid_front_L"},
    {"bone": "leg_mid_back_R", "mirror": "leg_mid_back_L"},
    {"bone": "leg_back_R", "mirror": "leg_back_L"},
]
```

### Spider Variations

**Larger spider (more leg segments):**
Add `leg_*_lower` bones for 2-segment legs (24 bones total)

**Scorpion:**
- Add pincers (2 bones at front)
- Add tail segments (5-6 bones curving up)

---

## Bird (20 bones)

Bipedal with wings. For birds, dragons, winged creatures.

```python
"skeleton": [
    # CORE (5 bones)
    {"bone": "pelvis", "parent": None, "head": [0, 0, 0.3], "tail": [0, 0.05, 0.35]},
    {"bone": "spine", "parent": "pelvis", "head": [0, 0.05, 0.35], "tail": [0, 0.15, 0.4]},
    {"bone": "neck", "parent": "spine", "head": [0, 0.15, 0.4], "tail": [0, 0.25, 0.55]},
    {"bone": "head", "parent": "neck", "head": [0, 0.25, 0.55], "tail": [0, 0.35, 0.55]},
    {"bone": "tail_feathers", "parent": "pelvis", "head": [0, 0, 0.3], "tail": [0, -0.2, 0.25]},

    # WINGS (4 bones)
    {"bone": "wing_upper_L", "parent": "spine", "head": [-0.1, 0.1, 0.38], "tail": [-0.3, 0.05, 0.35]},
    {"bone": "wing_lower_L", "parent": "wing_upper_L", "head": [-0.3, 0.05, 0.35], "tail": [-0.55, 0, 0.3]},
    {"bone": "wing_upper_R", "mirror": "wing_upper_L"},
    {"bone": "wing_lower_R", "mirror": "wing_lower_L"},

    # LEGS (6 bones)
    {"bone": "leg_upper_L", "parent": "pelvis", "head": [-0.05, -0.02, 0.3], "tail": [-0.05, -0.05, 0.15]},
    {"bone": "leg_lower_L", "parent": "leg_upper_L", "head": [-0.05, -0.05, 0.15], "tail": [-0.05, 0, 0.05]},
    {"bone": "foot_L", "parent": "leg_lower_L", "head": [-0.05, 0, 0.05], "tail": [-0.05, 0.08, 0.02]},
    {"bone": "leg_upper_R", "mirror": "leg_upper_L"},
    {"bone": "leg_lower_R", "mirror": "leg_lower_L"},
    {"bone": "foot_R", "mirror": "foot_L"},
]
```

### Bird Variations

**Dragon (larger, more robust):**
- Scale all dimensions 3-5x
- Add longer neck segments
- Thicker wing bones

**Penguin (no flight):**
- Short stubby wings
- Upright posture (vertical spine)
- Thick body

---

## Bone Naming Conventions

| Suffix | Meaning |
|--------|---------|
| `_L` | Left side |
| `_R` | Right side |
| `_upper` | Proximal segment (closer to body) |
| `_lower` | Distal segment (further from body) |
| `_front` | Anterior |
| `_back` | Posterior |
| `_mid` | Middle |

---

## Animation Presets

Reference `procedural-animations` skill for animation patterns matching these skeletons:

| Skeleton | Animation Presets |
|----------|-------------------|
| Humanoid | walk, run, idle, attack, jump, death |
| Quadruped | walk, run, idle, attack, sit |
| Serpent | slither, strike, coil |
| Spider | walk, attack, idle |
| Bird | walk, fly, idle, peck |
