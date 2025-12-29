# ZX Console Animation Constraints

Hardware limits and budget guidelines for animation on Nethercore ZX.

## Skeletal Constraints

### Bone Limits

| Constraint | Hard Limit | Recommended | Notes |
|------------|------------|-------------|-------|
| Bones per skeleton | 256 | 20-50 | `load_skeleton()` enforces |
| Bones per vertex | 4 | 4 | glTF requirement |
| Bone matrix size | 3x4 | - | 12 floats per bone |

### Practical Bone Budgets

| Character Type | Bones | Use Case |
|----------------|-------|----------|
| Player character | 15-25 | Full animation set |
| Main NPCs | 15-20 | Dialogue + basic actions |
| Enemies (important) | 12-18 | Combat animations |
| Enemies (basic) | 8-12 | Simple movement |
| Props (animated) | 2-6 | Doors, levers, chests |
| Environmental | 4-10 | Trees, flags, machinery |

### Skeleton Complexity Guide

**Simple (8-12 bones):**
```
root → hips → spine → head
        ├── l_arm → l_hand
        ├── r_arm → r_hand
        ├── l_leg → l_foot
        └── r_leg → r_foot
```

**Standard (15-20 bones):**
```
root → hips → spine → chest → neck → head
        ├── l_shoulder → l_upper_arm → l_lower_arm → l_hand
        ├── r_shoulder → r_upper_arm → r_lower_arm → r_hand
        ├── l_upper_leg → l_lower_leg → l_foot
        └── r_upper_leg → r_lower_leg → r_foot
```

**Complex (25-35 bones):** Add fingers, twist bones, face bones

---

## Animation Frame Budgets

### Target: 30 FPS Playback

| Animation Type | Frames | Duration | Loop |
|----------------|--------|----------|------|
| **Idle/Breathe** | 60 | 2.0 sec | Yes |
| **Walk cycle** | 24-30 | 0.8-1.0 sec | Yes |
| **Run cycle** | 18-24 | 0.6-0.8 sec | Yes |
| **Sprint** | 12-18 | 0.4-0.6 sec | Yes |
| **Jump** | 20-40 | 0.7-1.3 sec | No |
| **Land** | 10-15 | 0.3-0.5 sec | No |
| **Attack (light)** | 12-20 | 0.4-0.7 sec | No |
| **Attack (heavy)** | 25-40 | 0.8-1.3 sec | No |
| **Hit react** | 15-25 | 0.5-0.8 sec | No |
| **Death** | 30-60 | 1.0-2.0 sec | No |
| **Pickup/Use** | 15-30 | 0.5-1.0 sec | No |

### Animation Set Size Guidelines

| Character | Animations | Total Frames |
|-----------|------------|--------------|
| Player | 15-25 | 400-600 |
| Main enemy | 8-12 | 200-350 |
| Minor enemy | 4-8 | 100-200 |
| NPC | 3-6 | 80-150 |

---

## Memory Considerations

### Animation Data Size

Per bone, per keyframe:
- **Rotation (quat):** 4 floats = 16 bytes
- **Position:** 3 floats = 12 bytes (usually only root)
- **Scale:** 3 floats = 12 bytes (rarely used)

**Estimated size per animation:**
```
Size = bones × keyframes × (16 + position_if_used)
```

**Example - Walk cycle:**
- 20 bones
- 24 keyframes
- Rotation only (except root has position)
- Size ≈ 20 × 24 × 16 + 24 × 12 = 7,968 bytes ≈ 8 KB

### Animation Budget Guidelines

| Category | Budget |
|----------|--------|
| Player character | 50-80 KB |
| Main enemies (each) | 20-40 KB |
| Minor enemies (each) | 10-20 KB |
| Props/environmental | 2-10 KB |
| **Total game** | 500 KB - 2 MB |

---

## Performance Optimization

### Keyframe Reduction

Reduce keyframes while preserving motion quality:

```python
def optimize_animation(action, threshold=0.01):
    """Remove redundant keyframes."""
    for fcurve in action.fcurves:
        # Decimate
        remove_indices = []
        points = fcurve.keyframe_points

        for i in range(1, len(points) - 1):
            prev = points[i-1].co[1]
            curr = points[i].co[1]
            next_val = points[i+1].co[1]

            # Linear interpolation check
            t = (points[i].co[0] - points[i-1].co[0]) / (points[i+1].co[0] - points[i-1].co[0])
            expected = prev + (next_val - prev) * t

            if abs(curr - expected) < threshold:
                remove_indices.append(i)

        for i in reversed(remove_indices):
            points.remove(points[i])
```

### Bone Influence Optimization

Ensure max 4 influences per vertex:

```python
def limit_bone_influences(mesh_obj, max_influences=4):
    """Limit and renormalize bone influences."""
    bpy.context.view_layer.objects.active = mesh_obj
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
    bpy.ops.object.vertex_group_limit_total(limit=max_influences)
    bpy.ops.object.vertex_group_normalize_all()
    bpy.ops.object.mode_set(mode='OBJECT')
```

### Animation Sharing

Reuse animations across similar characters:

```python
def share_animation(source_rig, target_rig, action_name):
    """Apply animation from one rig to another (must have matching bone names)."""
    action = bpy.data.actions.get(action_name)
    if not action:
        return

    if not target_rig.animation_data:
        target_rig.animation_data_create()

    # Link action (doesn't duplicate data)
    target_rig.animation_data.action = action
```

---

## Style Guidelines (N64/PS1/PS2 Era)

### Motion Characteristics

| Era | Characteristics |
|-----|-----------------|
| N64 | Snappy, limited interpolation, clear poses |
| PS1 | Similar to N64, slightly more frames |
| PS2 | Smoother, more in-betweens, still stylized |

### Animation Style Tips

1. **Strong Key Poses:** Each keyframe should be a clear, readable pose
2. **Limited In-Betweens:** Use fewer frames, let interpolation do work
3. **Exaggeration:** Push poses slightly beyond realistic
4. **Snappy Timing:** Quick transitions, hold on key poses
5. **Simple Loops:** Clean loop points, no complex blending

### Example: N64-Style Walk

```python
def n64_style_walk(rig, duration_frames=20):
    """Fewer frames, sharper poses."""
    action = bpy.data.actions.new("Walk_N64")
    rig.animation_data.action = action

    # Just 4 key poses instead of per-frame sampling
    key_frames = [1, 5, 10, 15, 20]
    poses = [
        {"l_leg": 0.4, "r_leg": -0.4},  # Contact L
        {"l_leg": 0.0, "r_leg": 0.0},   # Pass
        {"l_leg": -0.4, "r_leg": 0.4},  # Contact R
        {"l_leg": 0.0, "r_leg": 0.0},   # Pass
        {"l_leg": 0.4, "r_leg": -0.4},  # Loop
    ]

    bpy.ops.object.mode_set(mode='POSE')

    for frame, pose in zip(key_frames, poses):
        bpy.context.scene.frame_set(frame)

        rig.pose.bones["l_upper_leg"].rotation_euler.x = pose["l_leg"]
        rig.pose.bones["r_upper_leg"].rotation_euler.x = pose["r_leg"]

        rig.pose.bones["l_upper_leg"].keyframe_insert(data_path="rotation_euler", frame=frame)
        rig.pose.bones["r_upper_leg"].keyframe_insert(data_path="rotation_euler", frame=frame)

    bpy.ops.object.mode_set(mode='OBJECT')
```

---

## Validation Checklist

Before exporting for ZX:

```python
def validate_for_zx(armature):
    """Check animation against ZX constraints."""
    issues = []
    warnings = []

    # Bone count
    bone_count = len(armature.data.bones)
    if bone_count > 256:
        issues.append(f"Too many bones: {bone_count} (max 256)")
    elif bone_count > 50:
        warnings.append(f"High bone count: {bone_count} (recommended <50)")

    # Animation frame counts
    for action in bpy.data.actions:
        frame_count = action.frame_range[1] - action.frame_range[0]
        if frame_count > 300:
            warnings.append(f"Long animation '{action.name}': {frame_count} frames")

    # Mesh influences
    for child in armature.children:
        if child.type != 'MESH':
            continue
        for vert in child.data.vertices:
            count = sum(1 for vg in child.vertex_groups
                       if vg.weight(vert.index) > 0.001)
            if count > 4:
                issues.append(f"Vertex {vert.index} has {count} influences (max 4)")

    return {"issues": issues, "warnings": warnings}
```

---

## Quick Reference

### Bone Budget

| Type | Bones | Notes |
|------|-------|-------|
| Player | 20-25 | Full rig |
| Enemy | 10-18 | Depends on importance |
| NPC | 12-18 | Can share with enemies |
| Prop | 2-6 | Minimal |

### Frame Budget (per animation)

| Type | Frames |
|------|--------|
| Loop | 18-60 |
| Action | 12-40 |
| Transition | 8-15 |

### Memory Budget

| Total animations | Approx. size |
|------------------|--------------|
| Player set | 50-80 KB |
| Per enemy type | 20-40 KB |
| Whole game | 500 KB - 2 MB |
