# IK/FK Switching

Control whether limbs follow IK targets (ground contact) or FK poses (airborne/free movement).

## When to Use

| Situation | Mode | `ikfk` Value |
|-----------|------|--------------|
| Feet on ground | IK | 1.0 |
| Airborne (jumping) | FK | 0.0 |
| Hands grabbing object | IK | 1.0 |
| Arms swinging freely | FK | 0.0 |
| Transition (blending) | Blend | 0.0-1.0 |

## Spec Format

IK/FK is controlled inline with IK target keyframes:

```python
"rig_setup": {
    "presets": {"humanoid_legs": True}
},

"phases": [
    {
        "name": "grounded",
        "frames": [0, 20],
        "pose": "crouch",
        "ik_targets": {
            "ik_foot_L": [
                {"frame": 0, "location": [-0.08, 0, 0], "ikfk": 1.0},   # Full IK
                {"frame": 10, "location": [-0.08, 0, 0.05], "ikfk": 0.5}, # Blending
                {"frame": 20, "location": [-0.08, 0, 0.10], "ikfk": 0.0}, # Full FK
            ]
        }
    }
]
```

The `ikfk` key controls the `IK_leg_L` / `IK_leg_R` properties on the armature.

## Stomp Animation Pattern (Recommended Demo)

Simplest demonstration - ONE leg switches IK/FK while the other stays planted:

| Phase | Frames | Right Leg | Left Leg | Description |
|-------|--------|-----------|----------|-------------|
| Lift | 0-15 | 1.0→0.0 | 1.0 | Right lifts off |
| Stomp | 15-30 | 0.0→1.0 | 1.0 | Right slams down |
| Recover | 30-45 | 1.0 | 1.0 | Return to standing |

Why this is clearer than a jump:
- Only ONE leg transitions (right), left stays planted
- Only 3 phases vs 6
- Easy to see IK/FK switch effect in isolation

See `specs/animations/knight_stomp.spec.py` for the complete spec.

## Jump Animation Pattern (Complex)

Full IK/FK sequence for a two-legged jump:

| Phase | Frames | `ikfk` | Description |
|-------|--------|--------|-------------|
| Crouch | 0-15 | 1.0 | Feet planted, IK controls position |
| Launch | 15-25 | 1.0→0.0 | Push off, blend to FK |
| Air | 25-50 | 0.0 | Airborne, FK poses control legs |
| Descend | 50-65 | 0.0→0.5 | Preparing for landing |
| Land | 65-75 | 0.5→1.0 | Contact, IK takes over |
| Recover | 75-90 | 1.0 | Stabilize, full IK |

See `specs/animations/knight_jump.spec.py` for the complete spec.

## Best Practices

1. **Always define FK poses** - Even with IK, define leg rotations in poses for FK fallback
2. **Blend over multiple frames** - Avoid instant 1.0→0.0 switches (causes popping)
3. **IK targets still needed** - Even when `ikfk=0`, define IK target positions for blending
4. **Keep IK targets moving** - During FK phases, animate IK targets to roughly match FK pose
5. **No constraints** - IK direction from skeleton bend hints (Y-offset at knee)

## Property Names

IK/FK properties follow the pattern `IK_{chain_name}`:

| Chain | Property |
|-------|----------|
| Left leg | `IK_leg_L` |
| Right leg | `IK_leg_R` |
| Left arm | `IK_arm_L` |
| Right arm | `IK_arm_R` |

## Viewing in Blender

IK/FK properties appear in **Object Data Properties > Custom Properties** on the armature:

1. Select the armature in Object Mode
2. Go to Properties panel → Object Data (bone icon)
3. Scroll to Custom Properties section
4. Find `IK_leg_L`, `IK_leg_R` sliders (0.0 = FK, 1.0 = IK)

Keyframe these properties to animate the IK/FK blend.
