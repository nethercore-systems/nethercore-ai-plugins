# Animation Spec Format

Structured format for animation specifications. Animation specs are Python files (`.spec.py`) containing pose data that the unified generator interprets in Blender.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  animation-describer agent                                   │
│  ─────────────────────────                                   │
│  Input: "Create idle animation for PATCH character"         │
│  Output: .studio/specs/animations/patch_idle.spec.py        │
│                                                              │
│  Produces structured poses with bone rotations               │
│  Uses animation principles + character personality           │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  python .studio/generate.py --only animations                │
│  ─────────────────────────────────────                       │
│  Runs parsers/animation.py in Blender headless               │
│  Input: .spec.py spec + armature .glb                        │
│  Output: Animated .glb with keyframes                        │
└─────────────────────────────────────────────────────────────┘
```

**Why this architecture?**

1. **No PyYAML dependency** — Python literals work natively in Blender
2. **No LLM in generation loop** — Parser is deterministic, reusable
3. **Skeleton-agnostic** — Works with any armature if bone names match
4. **Explicit rotations** — No coordinate confusion from natural language

## Animation Spec Format (`.spec.py`)

```python
# [Animation Name] - [CHARACTER] character
# Duration: X frames @ Yfps
#
# Character context (for Claude, not parsed by Blender):
# - [Character personality and physicality notes]
# - [Movement style, weight, energy]

ANIMATION = {
    "animation": {
        "name": "animation_id",           # snake_case identifier
        "input_armature": "assets/characters/character.glb",  # Optional
        "duration_frames": 120,           # Total frames
        "fps": 60,                         # Frame rate
        "loop": True,                      # Seamless loop?

        # Named poses with bone rotations (pitch/yaw/roll in DEGREES)
        "poses": {
            "pose_name": {
                "BoneName": {"pitch": 0, "yaw": 0, "roll": 0},
                # ... more bones
            },
            # ... more poses
        },

        # Phases reference poses with frame ranges
        "phases": [
            {
                "name": "phase_name",
                "frames": [start, end],
                "pose": "pose_name",          # Reference to poses dict
                "timing_curve": "linear",     # Interpolation
                "description": "Brief note"   # For debugging/review
            },
            # ... more phases
        ],

        # Procedural layers for organic feel
        "procedural_layers": [
            {
                "type": "breathing",
                "target": "Chest",
                "period_frames": 90,
                "amplitude": 0.02,
                "axis": "pitch"
            },
            # ... more layers
        ],

        "ik_hints": {
            "feet": "ground_contact",  # or None
            "hands": None              # or "target_position"
        },

        "style": {
            "weight": "medium",        # light|medium|heavy
            "energy": "calm",          # smooth|snappy|explosive|calm
            "intent": "idle"           # attack|defend|locomotion|idle|gesture
        }
    }
}
```

## Rotation Convention

All rotations are specified in **degrees** using **pitch/yaw/roll**:

| Term | Axis | Humanoid Example |
|------|------|------------------|
| **pitch** | X-axis | Nodding head, bending elbow |
| **yaw** | Y-axis | Twisting spine, turning head |
| **roll** | Z-axis | Tilting head, side-bending |

The parser converts degrees to radians and applies rotations using Blender's Euler XYZ mode.

### Bone Naming

Bone names must **exactly match** the armature's bone names. Common conventions:

| Bone | Standard Name | Notes |
|------|---------------|-------|
| Root | `Hips` or `pelvis` | Center of mass |
| Spine chain | `Spine`, `Chest`, `Neck`, `Head` | Bottom to top |
| Left arm | `UpperArmL`, `LowerArmL`, `HandL` | or `_L` suffix |
| Right arm | `UpperArmR`, `LowerArmR`, `HandR` | or `_R` suffix |
| Left leg | `UpperLegL`, `LowerLegL`, `FootL` | or `_L` suffix |
| Right leg | `UpperLegR`, `LowerLegR`, `FootR` | or `_R` suffix |

The animation-describer agent should check the target armature's bone names before generating.

## Poses

Poses are snapshots of bone rotations. Only bones that differ from rest pose need to be specified:

```python
"poses": {
    "neutral_stance": {
        # Only specify non-zero rotations
        "Hips": {"pitch": -3, "yaw": 0, "roll": 0},
        "Spine": {"pitch": 2, "yaw": 0, "roll": 0},
        "Head": {"pitch": -2, "yaw": 0, "roll": 0},
        "UpperArmL": {"pitch": -45, "yaw": 15, "roll": -25},
        "LowerArmL": {"pitch": 0, "yaw": 0, "roll": -75},
        "UpperArmR": {"pitch": -45, "yaw": -15, "roll": 25},
        "LowerArmR": {"pitch": 0, "yaw": 0, "roll": 75},
    },

    "breath_peak": {
        # Derive from neutral_stance, only list changes
        "Chest": {"pitch": 3, "yaw": 0, "roll": 0},
        "Hips": {"pitch": -2, "yaw": 0, "roll": 0},
    },
}
```

### Pose Inheritance

For poses that are slight variations, document the base:

```python
"weight_shift_left": {
    # Base: neutral_stance with these modifications
    "Hips": {"pitch": -3, "yaw": 0, "roll": -2},      # Tilted left
    "UpperLegL": {"pitch": 6, "yaw": -2, "roll": 0},  # Weight bearing
    "UpperLegR": {"pitch": -3, "yaw": 2, "roll": 0},  # Relaxed
},
```

## Phases

Phases define keyframe timing by referencing named poses:

```python
"phases": [
    {
        "name": "neutral_hold",
        "frames": [0, 29],
        "pose": "neutral_stance",
        "timing_curve": "linear",
        "description": "Balanced guard position"
    },
    {
        "name": "inhale",
        "frames": [30, 59],
        "pose": "breath_peak",
        "timing_curve": "ease_in_out",
        "description": "Chest expands with breath"
    },
    {
        "name": "exhale",
        "frames": [60, 89],
        "pose": "neutral_stance",
        "timing_curve": "ease_in_out",
        "description": "Return to neutral"
    },
]
```

### Frame Interpretation

- `frames[0]`: Pose is fully applied at this frame
- `frames[1]`: Transition completes to next pose
- For loops, last phase should transition smoothly to first pose

### Timing Curves

| Value | Blender Interpolation | Use Case |
|-------|----------------------|----------|
| `linear` | LINEAR | Mechanical movement |
| `ease_in` | SINE (EASE_IN) | Starts slow, accelerates |
| `ease_out` | SINE (EASE_OUT) | Fast start, gentle stop |
| `ease_in_out` | SINE (AUTO) | Smooth organic motion |
| `exponential_in` | EXPO (EASE_IN) | Heavy wind-up |
| `exponential_out` | EXPO (EASE_OUT) | Explosive release |
| `constant` | CONSTANT | Snap to pose |

## Procedural Layers

Add organic micro-movements without manual keyframing:

```python
"procedural_layers": [
    {
        "type": "breathing",
        "target": "Chest",
        "period_frames": 90,
        "amplitude": 0.02,
        "axis": "pitch",
        "description": "Subtle chest expansion"
    },
    {
        "type": "sway",
        "target": "Spine",
        "period_frames": 150,
        "amplitude": 0.008,
        "axis": "roll",
        "description": "Minimal side-to-side sway"
    },
    {
        "type": "noise",
        "target": "Head",
        "amplitude": 0.005,
        "frequency": 0.5,
        "description": "Micro head movements"
    },
]
```

### Layer Types

| Type | Effect | Parameters |
|------|--------|------------|
| `breathing` | Sine wave on axis | period_frames, amplitude, axis |
| `sway` | Sine wave (often roll) | period_frames, amplitude, axis |
| `noise` | Random micro-motion | amplitude, frequency |
| `bob` | Vertical sine wave | period_frames, amplitude |

The parser applies these as FCurve modifiers.

## IK Hints

Inform the parser about inverse kinematics requirements:

```python
"ik_hints": {
    "feet": "ground_contact",    # Use IK, bake to FK
    "hands": None                 # Pure FK for hands
}
```

| Value | Parser Behavior |
|-------|-----------------|
| `"ground_contact"` | Set up IK targets, bake to FK before export |
| `"target_position"` | IK toward specified positions |
| `None` | Use FK directly |

**Note:** ZX runtime only supports FK, so IK is always baked out.

## Style Metadata

Informs the animation-describer's design choices:

```python
"style": {
    "weight": "medium",    # Affects acceleration/timing
    "energy": "calm",      # Character of motion
    "intent": "idle"       # Animation purpose
}
```

### Weight

| Value | Anticipation | Action | Recovery |
|-------|--------------|--------|----------|
| `light` | Short (20%) | Quick (30%) | Short (50%) |
| `medium` | Normal (30%) | Normal (30%) | Normal (40%) |
| `heavy` | Long (40%) | Slow (20%) | Long (40%) |

### Energy

| Value | Motion Character |
|-------|------------------|
| `calm` | Minimal movement, relaxed |
| `smooth` | Even, flowing motion |
| `snappy` | Quick pose changes, clear keys |
| `explosive` | Fast action, heavy anticipation |

## Complete Example: Idle Animation

```python
# Idle Animation - PATCH character
# Duration: 120 frames @ 60fps (2 seconds)
#
# Character: PATCH - methodical sysadmin archetype, protective, reliable.
# Build: Athletic, balanced stance with slight forward lean.
# Demeanor: Alert but calm, ready but not tense.

ANIMATION = {
    "animation": {
        "name": "patch_idle",
        "input_armature": "assets/characters/patch.glb",
        "duration_frames": 120,
        "fps": 60,
        "loop": True,

        "poses": {
            "idle_base": {
                "Hips": {"pitch": -3, "yaw": 0, "roll": 0},
                "Spine": {"pitch": 2, "yaw": 0, "roll": 0},
                "Chest": {"pitch": 1, "yaw": 0, "roll": 0},
                "Head": {"pitch": -2, "yaw": 0, "roll": 0},
                "UpperArmL": {"pitch": -45, "yaw": 15, "roll": -25},
                "LowerArmL": {"pitch": 0, "yaw": 0, "roll": -75},
                "UpperArmR": {"pitch": -45, "yaw": -15, "roll": 25},
                "LowerArmR": {"pitch": 0, "yaw": 0, "roll": 75},
                "UpperLegL": {"pitch": 5, "yaw": -3, "roll": 0},
                "LowerLegL": {"pitch": -8, "yaw": 0, "roll": 0},
                "UpperLegR": {"pitch": 5, "yaw": 3, "roll": 0},
                "LowerLegR": {"pitch": -8, "yaw": 0, "roll": 0},
            },

            "breath_peak": {
                "Chest": {"pitch": 3, "yaw": 0, "roll": 0},
                "Hips": {"pitch": -2, "yaw": 0, "roll": 0},
                "Head": {"pitch": -3, "yaw": 0, "roll": 0},
            },

            "weight_shift_left": {
                "Hips": {"pitch": -3, "yaw": 0, "roll": -1.5},
                "Spine": {"pitch": 2, "yaw": 0, "roll": 0.5},
                "UpperLegL": {"pitch": 6, "yaw": -2, "roll": 0},
                "UpperLegR": {"pitch": 3, "yaw": 4, "roll": 0},
                "LowerLegR": {"pitch": -5, "yaw": 0, "roll": 0},
            },
        },

        "phases": [
            {
                "name": "neutral_stance",
                "frames": [0, 29],
                "pose": "idle_base",
                "timing_curve": "linear",
                "description": "Balanced guard position"
            },
            {
                "name": "breath_in",
                "frames": [30, 44],
                "pose": "breath_peak",
                "timing_curve": "ease_out",
                "description": "Chest expands"
            },
            {
                "name": "breath_out",
                "frames": [45, 59],
                "pose": "idle_base",
                "timing_curve": "ease_in",
                "description": "Return to neutral"
            },
            {
                "name": "weight_shift",
                "frames": [60, 89],
                "pose": "weight_shift_left",
                "timing_curve": "ease_in_out",
                "description": "Subtle weight redistribution"
            },
            {
                "name": "return_center",
                "frames": [90, 119],
                "pose": "idle_base",
                "timing_curve": "ease_in_out",
                "description": "Back to balanced stance, loops"
            },
        ],

        "procedural_layers": [
            {
                "type": "breathing",
                "target": "Chest",
                "period_frames": 90,
                "amplitude": 0.02,
                "axis": "pitch",
                "description": "Smooth sine wave breathing"
            },
            {
                "type": "sway",
                "target": "Spine",
                "period_frames": 150,
                "amplitude": 0.008,
                "axis": "roll",
                "description": "Minimal side-to-side sway"
            },
            {
                "type": "noise",
                "target": "Head",
                "amplitude": 0.003,
                "frequency": 0.3,
                "description": "Micro head adjustments"
            },
        ],

        "ik_hints": {
            "feet": None,
            "hands": None
        },

        "style": {
            "weight": "medium",
            "energy": "calm",
            "intent": "idle"
        }
    }
}
```

## File Organization

```
.studio/
├── generate.py                    # Unified generator
├── parsers/
│   └── animation.py               # Animation parser
└── specs/
    └── animations/
        ├── patch_idle.spec.py
        ├── patch_walk.spec.py
        └── patch_attack.spec.py

assets/
└── animations/
    ├── patch_idle.glb             # Output from generator
    ├── patch_walk.glb
    └── patch_attack.glb
```

## Execution

Via unified generator (recommended):
```bash
python .studio/generate.py --only animations
```

Standalone (for debugging):
```bash
blender --background --python .studio/parsers/animation.py -- \
    .studio/specs/animations/patch_idle.spec.py \
    assets/characters/patch.glb \
    assets/animations/patch_idle.glb
```

## Related

- Animation parser: `.studio/parsers/animation.py`
- IK utilities (for `ground_contact`): `references/ik-utilities.md`
- Character rigs: `procedural-characters` skill
- ZX constraints: `references/zx-constraints.md`
