# Bone Orientation

## Limb Bone Roll

Character parser sets roll for `*_upper_*` and `*_lower_*` bones:
```python
bone.align_roll(mathutils.Vector((0, -1, 0)))  # Z toward -Y
```

**Result:** Positive pitch = flexion
- `leg_lower_L: pitch: 90` = knee bent 90 degrees
- `arm_lower_R: pitch: 60` = elbow bent 60 degrees

## IK Bend Hints

Skeletons use Y-offset at joints to guide IK direction:
```python
{"bone": "leg_upper_L", "tail": [-0.08, 0.03, 0.5]},  # Y=0.03 = forward hint
{"bone": "leg_lower_L", "head": [-0.08, 0.03, 0.5]},
```

## Validation

The animation parser now validates joint motion post-bake:

1. **Calibration**: Determines flexion axis/sign from rest geometry
2. **Validation**: Checks each frame for hyperextension/overflexion
3. **Reports**: Produces `.validation.json` alongside exported `.glb`

Use `--strict` to fail on violations:
```bash
blender --background --python animation.py -- spec.spec.py in.glb out.glb --strict
```

## Troubleshooting

**Knee bending backward:**
1. Regenerate character: `python .studio/generate.py --only characters`
2. Check skeleton has Y-offset at knee (0.02-0.05)
3. Add hinge constraints to enforce proper direction:
   ```python
   "constraints": [
       {"bone": "leg_lower_L", "type": "hinge", "axis": "X", "limits": [0, 160]}
   ]
   ```
4. Run with `--strict` to catch violations early
