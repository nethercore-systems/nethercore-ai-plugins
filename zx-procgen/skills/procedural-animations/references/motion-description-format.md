# Motion Description Format

Intermediate format between the Motion Agent (semantic) and Code Agent (coordinates). This format describes animation intent without any coordinate values.

## Purpose

LLMs get confused about coordinate spaces when generating FK rotation code directly. This format separates:

1. **Motion Agent** — Uses general knowledge of anatomy/animation to describe motion semantically
2. **Code Agent** — Translates semantic descriptions to Blender bpy with coordinate reasoning

## Format Specification

```yaml
animation:
  name: animation_id          # Unique identifier
  duration_frames: 24         # Total frames
  fps: 30                     # Frames per second
  loop: false                 # Seamless loop?

  style:
    weight: light|medium|heavy           # Affects acceleration curves
    energy: smooth|snappy|explosive      # Timing character
    intent: attack|defend|locomotion|idle|gesture

  phases:
    - name: phase_name
      frames: [start, end]
      description: "Natural language description of body pose and movement"
    # Additional phases...

  timing_curves:
    phase_name: ease_in|ease_out|linear|exponential_in|exponential_out
```

## Style Modifiers

### Weight

| Value | Anticipation | Action | Recovery | Acceleration |
|-------|--------------|--------|----------|--------------|
| light | Short (20%) | Quick (30%) | Short (50%) | Fast, snappy |
| medium | Normal (30%) | Normal (30%) | Normal (40%) | Balanced |
| heavy | Long (40%) | Slow (20%) | Long (40%) | Gradual, momentum |

### Energy

| Value | Key Poses | In-betweens | Easing |
|-------|-----------|-------------|--------|
| smooth | Subtle | Many | BEZIER, gentle curves |
| snappy | Strong, clear | Few | CONSTANT or LINEAR |
| explosive | Exaggerated | Clustered at end | EXPO_IN |

## Phase Descriptions

Write body position descriptions in natural language. Reference:

- **Limb positions**: "arm raised overhead", "leg extended back"
- **Body orientation**: "torso twisted right", "shoulders facing target"
- **Weight distribution**: "weight on back foot", "balanced stance"
- **Relative positions**: "sword behind right shoulder", "hands at chest level"

### Good Examples

```yaml
- name: anticipation
  frames: [0, 8]
  description: "Sword pulled back over right shoulder, elbow bent and high, torso twisted right to coil power, weight shifted to back foot"

- name: strike
  frames: [8, 14]
  description: "Explosive diagonal swing from high-right to low-left, torso unwinds adding rotational power, weight transfers forward onto front foot"
```

### Bad Examples (Avoid These)

```yaml
# BAD: Includes coordinates
description: "Rotate shoulder X by -45 degrees, elbow at 90 degrees"

# BAD: Too vague
description: "Move arm"

# BAD: Technical jargon without anatomical context
description: "Apply quaternion rotation to upper_arm.R bone"
```

## Locomotion Patterns

For walk/run cycles, describe foot contact:

```yaml
phases:
  - name: right_contact
    frames: [0, 6]
    description: "Right foot plants on ground, left leg swings forward, hips dip slightly on contact side"

  - name: right_passing
    frames: [6, 12]
    description: "Left leg passes right leg, weight centered, slight hip rotation as legs cross"

  - name: left_contact
    frames: [12, 18]
    description: "Left foot plants, right leg swings forward, mirror of right_contact"

  - name: left_passing
    frames: [18, 24]
    description: "Right leg passes left, completing the cycle"
```

## Attack Patterns

Three-phase structure for combat animations:

```yaml
phases:
  - name: anticipation
    frames: [0, 8]
    description: "Wind-up pose - weapon pulled back, weight loaded"

  - name: strike
    frames: [8, 14]
    description: "Attack execution - weapon travels arc, power transfers through body"

  - name: recovery
    frames: [14, 24]
    description: "Return to ready - momentum settles, stance re-established"
```

## IK Hints

When animation benefits from IK (ground contact, hand targets), add:

```yaml
ik_hints:
  feet: ground_contact    # Use leg IK for foot placement
  hands: null             # No hand IK needed

# Or for climbing/grabbing:
ik_hints:
  feet: ground_contact
  hands: target_position  # Use arm IK for hand reach
```

The Code Agent will use these hints to decide FK vs IK approach.

## Complete Example: Sword Slash

```yaml
animation:
  name: overhead_sword_slash
  duration_frames: 24
  fps: 30
  loop: false

  style:
    weight: heavy
    energy: explosive
    intent: attack

  phases:
    - name: anticipation
      frames: [0, 8]
      description: "Sword pulled back over right shoulder, elbow high and bent, torso twisted right to coil power, weight shifted onto back foot, slight crouch to load legs"

    - name: strike
      frames: [8, 14]
      description: "Explosive diagonal swing from high-right to low-left, torso unwinds adding rotational power, weight transfers forward, front leg drives extension, sword arm fully extends through arc"

    - name: recovery
      frames: [14, 24]
      description: "Momentum carries sword to rest at left hip level, torso settles back to neutral, weight re-centers to balanced stance, arms relax but stay ready"

  timing_curves:
    anticipation: ease_in
    strike: exponential_in
    recovery: ease_out

  ik_hints:
    feet: ground_contact
    hands: null
```

## Complete Example: Walk Cycle

```yaml
animation:
  name: walk_cycle
  duration_frames: 24
  fps: 30
  loop: true

  style:
    weight: medium
    energy: smooth
    intent: locomotion

  phases:
    - name: right_contact
      frames: [0, 6]
      description: "Right heel strikes ground, leg extended forward, left foot pushes off behind, arms counter-swing (left forward, right back), slight hip drop on right side"

    - name: right_passing
      frames: [6, 12]
      description: "Right foot flat, body passes over right leg, left leg swings through, arms passing center, torso upright with minimal rotation"

    - name: left_contact
      frames: [12, 18]
      description: "Left heel strikes ground, mirroring right_contact, arms reversed (right forward, left back)"

    - name: left_passing
      frames: [18, 24]
      description: "Left foot flat, body passes over left leg, right leg swings through, completing cycle to frame 0 pose"

  timing_curves:
    right_contact: linear
    right_passing: linear
    left_contact: linear
    left_passing: linear

  ik_hints:
    feet: ground_contact
    hands: null
```
