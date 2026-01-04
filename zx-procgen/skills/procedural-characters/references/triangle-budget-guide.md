# Triangle Budget Guide

Calculate and manage triangle counts for character models.

---

## Formula

```
tris_per_part = (base_verts × 2 × num_steps) + cap_tris

cap_tris = base_verts - 2  (per cap)
```

### Base Shape Costs

| Shape | Vertices | Tris/Step | Tris/Cap |
|-------|----------|-----------|----------|
| `triangle(3)` | 3 | 6 | 1 |
| `square(4)` | 4 | 8 | 2 |
| `hexagon(6)` | 6 | 12 | 4 |
| `octagon(8)` | 8 | 16 | 6 |

---

## Budget Presets

### 300 Tris (Very Blocky - PS1 Early)

| Part | Base | Steps | Hands | Notes |
|------|------|-------|-------|-------|
| Body | square(4) | 2-3 | stub | Minimal detail |

**Breakdown:**
```
torso (sq, 4 steps):      8 × 4 + 2 + 2  = 36 tris
head (sq, 3 steps):       8 × 3 + 2 + 2  = 28 tris
arm_upper ×2 (sq, 2):     (8 × 2 + 2) × 2 = 36 tris
arm_lower ×2 (sq, 2):     (8 × 2 + 2) × 2 = 36 tris
leg_upper ×2 (sq, 2):     (8 × 2 + 2) × 2 = 36 tris
leg_lower ×2 (sq, 3):     (8 × 3 + 2) × 2 = 52 tris
─────────────────────────────────────────────────
Total:                                     224 tris
Budget remaining:                           76 tris (for details)
```

### 400 Tris (Standard - PS1 Late)

| Part | Base | Steps | Hands | Notes |
|------|------|-------|-------|-------|
| Body | square/hex | 3-4 | mitten | Some detail |

**Breakdown:**
```
torso (hex, 5 steps):     12 × 5 + 4      = 64 tris
head (hex, 4 steps):      12 × 4 + 4 + 4  = 56 tris
arm_upper ×2 (hex, 3):    (12 × 3 + 4) × 2 = 80 tris
arm_lower ×2 (hex, 3):    (12 × 3) × 2    = 72 tris
leg_upper ×2 (hex, 3):    (12 × 3 + 4) × 2 = 80 tris
leg_lower ×2 (hex, 4):    (12 × 4) × 2    = 96 tris
hand_mitten ×2 (sq, 3):   (8 × 3 + 2) × 2 = 52 tris
─────────────────────────────────────────────────
Total:                                     500 tris
```

*Over budget - reduce steps or use square base for limbs*

**Optimized 400:**
```
torso (hex, 4 steps):     12 × 4 + 4      = 52 tris
head (hex, 4 steps):      12 × 4 + 4 + 4  = 56 tris
arm_upper ×2 (sq, 3):     (8 × 3 + 2) × 2 = 52 tris
arm_lower ×2 (sq, 3):     (8 × 3) × 2     = 48 tris
leg_upper ×2 (sq, 3):     (8 × 3 + 2) × 2 = 52 tris
leg_lower ×2 (sq, 4):     (8 × 4 + 2) × 2 = 68 tris
hand_mitten ×2 (sq, 3):   (8 × 3 + 2) × 2 = 52 tris
─────────────────────────────────────────────────
Total:                                     380 tris ✓
```

### 500 Tris (Standard+ - PS2 Early)

| Part | Base | Steps | Hands | Notes |
|------|------|-------|-------|-------|
| Body | hexagon(6) | 4-5 | mitten+thumb | Good detail |

**Breakdown:**
```
torso (hex, 6 steps):     12 × 6 + 4      = 76 tris
head (hex, 5 steps):      12 × 5 + 4 + 4  = 68 tris
arm_upper ×2 (hex, 3):    (12 × 3 + 4) × 2 = 80 tris
arm_lower ×2 (hex, 4):    (12 × 4) × 2    = 96 tris
leg_upper ×2 (hex, 3):    (12 × 3 + 4) × 2 = 80 tris
leg_lower ×2 (hex, 4):    (12 × 4 + 4) × 2 = 104 tris
hand ×2 (hex, 4):         (12 × 4 + 4) × 2 = 104 tris
thumb ×2 (sq, 2):         (8 × 2 + 2) × 2 = 36 tris
─────────────────────────────────────────────────
Total:                                     644 tris
```

*Over budget - reduce to 5 steps on limbs*

### 700 Tris (Hero - PS2 Mid)

| Part | Base | Steps | Hands | Notes |
|------|------|-------|-------|-------|
| Body | hex/oct | 5-7 | 3-finger | High detail |

**Breakdown:**
```
torso (oct, 8 steps):     16 × 8 + 6      = 134 tris
head (oct, 7 steps):      16 × 7 + 6 + 6  = 124 tris
arm_upper ×2 (hex, 4):    (12 × 4 + 4) × 2 = 104 tris
arm_lower ×2 (hex, 4):    (12 × 4) × 2    = 96 tris
leg_upper ×2 (hex, 4):    (12 × 4 + 4) × 2 = 104 tris
leg_lower ×2 (hex, 5):    (12 × 5 + 4) × 2 = 128 tris
3-finger hand ×2:                           ~60 tris
─────────────────────────────────────────────────
Total:                                     ~750 tris
```

---

## Quick Estimation Table

| Budget | Max Parts | Base | Avg Steps | Hands |
|--------|-----------|------|-----------|-------|
| 200 | 6-8 | sq(4) | 2 | stub |
| 300 | 8-10 | sq(4) | 2-3 | stub |
| 400 | 10-12 | sq/hex | 3-4 | mitten |
| 500 | 12-14 | hex(6) | 4-5 | mitten+thumb |
| 700 | 14-16 | hex/oct | 5-7 | 3-finger |

---

## Optimization Strategies

### Reduce Steps

Most impactful change. Each step costs `base_verts × 2` tris.

```yaml
# Before: 5 steps = 60 tris (hex)
- extrude: 0.02, scale: 1.1
- extrude: 0.03, scale: 1.0
- extrude: 0.05, scale: 0.95
- extrude: 0.03, scale: 0.9
- extrude: 0.02, scale: 0.85

# After: 3 steps = 36 tris (hex)
- extrude: 0.05, scale: 1.1
- extrude: 0.08, scale: 0.95
- extrude: 0.02, scale: 0.85
```

### Use Simpler Bases

Switch from octagon to hexagon to square for limbs.

```yaml
# hex arm: 12 × 4 = 48 tris/arm
# sq arm:  8 × 4 = 32 tris/arm
# Savings: 16 tris/arm, 32 tris for both arms
```

### Share Caps

Remove caps between connected parts (they'll weld anyway).

```yaml
arm_upper:
  cap_end: false    # save 4 tris (hex)

arm_lower:
  cap_start: false  # save 4 tris (hex)
```

### Skip Thumbs

Mitten hands without thumbs save ~36 tris.

### Use Stub Hands/Feet

Close arm_lower/leg_lower directly instead of separate parts.

---

## Mirroring Costs

Mirrored parts double the tri count of their source:

```yaml
arm_upper_R:
  mirror: arm_upper_L    # same tri count as source
```

When counting, include both sides.

---

## Instance Multiplication

Hair spikes and similar instanced parts multiply:

```yaml
hair_spiky:
  instances:             # 4 spikes
    - position: ...
    - position: ...
    - position: ...
    - position: ...
  steps:
    - extrude: 0.08, scale: 0.7
    - extrude: 0.06, scale: 0.3

# triangle(3), 2 steps, 1 cap = 6 × 2 + 1 = 13 tris/spike
# 4 spikes = 52 tris total
```

---

## Validation

Use `estimate_tris()` before generating:

```python
estimated = estimate_tris(spec)
budget = spec['character']['tri_budget']

if estimated > budget:
    print(f"WARNING: ~{estimated} tris exceeds budget of {budget}")
```

The generator will warn but still proceed.
