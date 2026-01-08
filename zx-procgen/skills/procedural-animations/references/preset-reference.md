# Preset Reference

Rig presets expand to full IK chain definitions. This document lists what each preset requires and creates.

## humanoid_legs

Standard bipedal leg IK with foot targets and knee poles.

**Required bones:**
- `leg_upper_L`, `leg_lower_L`, `foot_L`
- `leg_upper_R`, `leg_lower_R`, `foot_R`

**Optional bones:**
- `toe_L`, `toe_R` (for foot roll)
- `leg_twist_L`, `leg_twist_R` (auto-included in chain)

**Creates:**
- IK targets: `ik_foot_L`, `ik_foot_R`
- Pole vectors: `pole_knee_L`, `pole_knee_R`
- IK/FK properties: `IK_leg_L`, `IK_leg_R`

**Auto-constraints:**
- Knee hinges: X-axis only, 0-160 degrees

**Usage:**
```python
"rig_setup": {
    "presets": {"humanoid_legs": True}
}

"ik_targets": {
    "ik_foot_L": [{"frame": 0, "location": [-0.08, 0.2, 0]}],
    "ik_foot_R": [{"frame": 0, "location": [0.08, -0.1, 0]}],
}
```

---

## humanoid_arms

Standard bipedal arm IK with hand targets and elbow poles.

**Required bones:**
- `arm_upper_L`, `arm_lower_L`
- `arm_upper_R`, `arm_lower_R`

**Optional bones:**
- `hand_L`, `hand_R` (if present, chain ends at hand)
- `arm_twist_L`, `arm_twist_R` (auto-included in chain)

**Creates:**
- IK targets: `ik_hand_L`, `ik_hand_R`
- Pole vectors: `pole_elbow_L`, `pole_elbow_R`
- IK/FK properties: `IK_arm_L`, `IK_arm_R`

**Auto-constraints:**
- Elbow hinges: X-axis only, 0-145 degrees

**Usage:**
```python
"rig_setup": {
    "presets": {"humanoid_arms": True}
}

"ik_targets": {
    "ik_hand_L": [{"frame": 0, "location": [-0.3, 0.5, 1.2]}],
}
```

---

## spider_legs

8-leg IK for arachnid characters with 2-segment legs.

**Required bones (all 16):**
- `leg_front_upper_L`, `leg_front_lower_L`
- `leg_front_upper_R`, `leg_front_lower_R`
- `leg_mid_front_upper_L`, `leg_mid_front_lower_L`
- `leg_mid_front_upper_R`, `leg_mid_front_lower_R`
- `leg_mid_back_upper_L`, `leg_mid_back_lower_L`
- `leg_mid_back_upper_R`, `leg_mid_back_lower_R`
- `leg_back_upper_L`, `leg_back_lower_L`
- `leg_back_upper_R`, `leg_back_lower_R`

**Creates:**
- IK targets: `ik_leg_front_L`, `ik_leg_front_R`, `ik_leg_mid_front_L`, `ik_leg_mid_front_R`, `ik_leg_mid_back_L`, `ik_leg_mid_back_R`, `ik_leg_back_L`, `ik_leg_back_R`
- Pole vectors: `pole_front_L`, `pole_front_R`, etc.

**Usage:**
```python
"rig_setup": {
    "presets": {"spider_legs": True}
}

"ik_targets": {
    "ik_leg_front_L": [{"frame": 0, "location": [-0.28, 0.30, 0]}],
    "ik_leg_front_R": [{"frame": 0, "location": [0.28, 0.30, 0]}],
}
```

---

## quadruped_legs

4-leg IK for quadruped characters (dogs, horses, dragons).

**Required bones (all 8):**
- `leg_front_upper_L`, `leg_front_lower_L`
- `leg_front_upper_R`, `leg_front_lower_R`
- `leg_back_upper_L`, `leg_back_lower_L`
- `leg_back_upper_R`, `leg_back_lower_R`

**Creates:**
- IK targets: `ik_foot_front_L`, `ik_foot_front_R`, `ik_foot_back_L`, `ik_foot_back_R`
- Pole vectors: `pole_front_L`, `pole_front_R`, `pole_back_L`, `pole_back_R`

**Usage:**
```python
"rig_setup": {
    "presets": {"quadruped_legs": True}
}

"ik_targets": {
    "ik_foot_front_L": [{"frame": 0, "location": [-0.15, 0.4, 0]}],
}
```

---

## basic_spine

Flexible spine chain with soft rotation limits.

**Required bones:** None (looks for any spine bones)

**Recognized bone names:**
- `spine_01`, `spine_02`, `spine_03`
- `spine`, `spine_1`, `spine_2`

Uses up to 3 bones found.

**Creates:**
- IK target: `ik_spine_tip`
- Soft constraints on all spine bones (stiffness 0.3)

**Rotation limits:**
- Pitch: -30 to +30 degrees
- Yaw: -20 to +20 degrees
- Roll: -15 to +15 degrees

---

## head_look

Head aiming/look-at system with damped tracking.

**Required bones:**
- `head`

**Optional bones:**
- `eye_L`, `eye_R` (get their own aim constraints)

**Creates:**
- Look target: `look_target`
- DAMPED_TRACK constraint on head
- DAMPED_TRACK on eyes (if present)

**Rotation limits:**
- Head: pitch [-60, 80], yaw [-90, 90]
- Eyes: pitch [-30, 30], yaw [-45, 45]

**Usage:**
```python
"rig_setup": {
    "presets": {"head_look": True}
}

"ik_targets": {
    "look_target": [{"frame": 0, "location": [0, 2, 1.5]}],  # Look forward
    "look_target": [{"frame": 30, "location": [-1, 2, 1.5]}],  # Look left
}
```

---

## Combining Presets

Presets can be combined freely:

```python
"rig_setup": {
    "presets": {
        "humanoid_legs": True,
        "humanoid_arms": True,
        "head_look": True,
    }
}
```

When combining:
- Each preset's chains are independent
- Constraints don't conflict (different bones)
- IK/FK properties created for each chain

---

## Custom Chains

For bones not covered by presets, use explicit `ik_chains`:

```python
"rig_setup": {
    "presets": {"humanoid_legs": True},
    "ik_chains": [
        {
            "name": "tail",
            "bones": ["tail_01", "tail_02", "tail_03", "tail_04", "tail_05"],
            "target": {"name": "ik_tail_tip", "at": "tip"},
            "rotation_limits": {
                "pitch": [-25, 25],
                "yaw": [-40, 40],
                "roll": [-15, 15],
            }
        }
    ]
}
```

Custom chains create:
- IK target: specified name
- IK/FK property: `IK_{chain_name}`
- Optional pole vector (if `pole` specified)
