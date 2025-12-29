# glTF Export Reference

Export settings and validation for animated .glb files in Blender.

## Basic Export

```python
import bpy

def export_animated_glb(filepath, armature=None):
    """Export scene with animations to GLB."""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',           # Binary format
        export_animations=True,        # Include animations
        export_animation_mode='ACTIONS',  # Each Action = clip
        export_skins=True,             # Include skeletal skinning
        export_all_influences=False,   # Limit to 4 bones/vertex
    )
```

---

## Export Settings Reference

### Animation Settings

| Setting | Value | Purpose |
|---------|-------|---------|
| `export_animations` | `True` | Include animation data |
| `export_animation_mode` | `'ACTIONS'` | Export each Action as separate clip |
| `export_animation_mode` | `'ACTIVE_ACTIONS'` | Export only active Actions |
| `export_animation_mode` | `'NLA_TRACKS'` | Use NLA strips |
| `export_frame_range` | `True` | Use scene frame range |
| `export_frame_step` | `1` | Sample every N frames |
| `export_force_sampling` | `True` | Force keyframe sampling |
| `export_optimize_animation_size` | `True` | Remove redundant keyframes |

### Skinning Settings

| Setting | Value | Purpose |
|---------|-------|---------|
| `export_skins` | `True` | Include mesh skinning |
| `export_all_influences` | `False` | Limit to 4 bones per vertex |
| `export_def_bones` | `True` | Export only deformation bones |

### Mesh Settings (relevant for animated meshes)

| Setting | Value | Purpose |
|---------|-------|---------|
| `export_apply_modifiers` | `True` | Apply non-armature modifiers |
| `export_tangents` | `False` | Usually not needed |
| `export_normals` | `True` | Include vertex normals |
| `export_colors` | `True` | Include vertex colors |
| `export_attributes` | `True` | Include custom attributes |

---

## Complete Export Function

```python
import bpy
import os

def export_game_asset(
    filepath,
    export_animations=True,
    apply_modifiers=True,
    optimize=True,
):
    """Export game-ready GLB with all common settings."""

    # Ensure GLB extension
    if not filepath.lower().endswith('.glb'):
        filepath += '.glb'

    # Deselect all first
    bpy.ops.object.select_all(action='DESELECT')

    bpy.ops.export_scene.gltf(
        filepath=filepath,

        # Format
        export_format='GLB',

        # Selection (export all or selected only)
        use_selection=False,
        use_visible=True,

        # Mesh
        export_apply_modifiers=apply_modifiers,
        export_normals=True,
        export_colors=True,
        export_tangents=False,

        # Skinning
        export_skins=True,
        export_all_influences=False,
        export_def_bones=True,

        # Animation
        export_animations=export_animations,
        export_animation_mode='ACTIONS',
        export_frame_range=True,
        export_force_sampling=True,
        export_optimize_animation_size=optimize,

        # Materials (optional)
        export_materials='EXPORT',
        export_image_format='AUTO',

        # Compression
        export_draco_mesh_compression_enable=False,
    )

    print(f"Exported: {filepath}")
    return filepath
```

---

## Animation Mode Options

### ACTIONS Mode (Recommended)

Each Blender Action becomes a separate animation clip:

```python
# Create multiple actions
idle_action = bpy.data.actions.new("Idle")
walk_action = bpy.data.actions.new("Walk")
run_action = bpy.data.actions.new("Run")

# Assign to armature
armature.animation_data.action = walk_action
# ... keyframe ...

# Export with ACTIONS mode
bpy.ops.export_scene.gltf(
    filepath="character.glb",
    export_animation_mode='ACTIONS',
)
# Result: character.glb contains "Idle", "Walk", "Run" clips
```

### ACTIVE_ACTIONS Mode

Only exports currently assigned Actions:

```python
bpy.ops.export_scene.gltf(
    filepath="character.glb",
    export_animation_mode='ACTIVE_ACTIONS',
)
```

### NLA_TRACKS Mode

Uses NLA strips for complex animation sequences:

```python
# Setup NLA track
track = armature.animation_data.nla_tracks.new()
strip = track.strips.new("Walk_Loop", 1, walk_action)
strip.repeat = 2

bpy.ops.export_scene.gltf(
    filepath="character.glb",
    export_animation_mode='NLA_TRACKS',
)
```

---

## Pre-Export Validation

```python
def validate_for_export(armature):
    """Check common issues before export."""
    issues = []

    # Check for animation data
    if not armature.animation_data:
        issues.append("No animation data on armature")
        return issues

    if not armature.animation_data.action and not bpy.data.actions:
        issues.append("No actions to export")

    # Check bone influences
    for child in armature.children:
        if child.type != 'MESH':
            continue

        for vert in child.data.vertices:
            influence_count = 0
            total_weight = 0

            for vg in child.vertex_groups:
                try:
                    weight = vg.weight(vert.index)
                    if weight > 0:
                        influence_count += 1
                        total_weight += weight
                except RuntimeError:
                    pass

            if influence_count > 4:
                issues.append(f"Mesh {child.name}: vertex {vert.index} has {influence_count} influences (max 4)")

            if influence_count > 0 and abs(total_weight - 1.0) > 0.01:
                issues.append(f"Mesh {child.name}: vertex {vert.index} weights sum to {total_weight:.2f}")

    # Check action frame ranges
    for action in bpy.data.actions:
        if action.frame_range[1] - action.frame_range[0] > 10000:
            issues.append(f"Action '{action.name}' is very long ({action.frame_range[1]} frames)")

    return issues


def run_validation(armature):
    """Run and print validation results."""
    issues = validate_for_export(armature)

    if issues:
        print("Export validation issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("Validation passed!")
        return True
```

---

## Common Export Issues

### Issue: Animation Not Exported

**Cause:** No actions assigned or action not in use
**Solution:**
```python
# Ensure action is assigned
if not armature.animation_data:
    armature.animation_data_create()
armature.animation_data.action = my_action

# Or push to NLA track to preserve
track = armature.animation_data.nla_tracks.new()
track.strips.new("clip", 1, my_action)
```

### Issue: Mesh Explodes in Game

**Cause:** Invalid bone weights or missing armature modifier
**Solution:**
```python
# Normalize weights
bpy.context.view_layer.objects.active = mesh
bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
bpy.ops.object.vertex_group_normalize_all()
bpy.ops.object.mode_set(mode='OBJECT')

# Check armature modifier
for mod in mesh.modifiers:
    if mod.type == 'ARMATURE':
        print(f"Armature: {mod.object}")
```

### Issue: Wrong Animation Speed

**Cause:** Frame rate mismatch
**Solution:**
```python
# Set scene FPS to match target
bpy.context.scene.render.fps = 30

# Or scale animation during export
# Export will adjust to scene FPS
```

### Issue: Object Animation Not Included

**Cause:** Object transform animation not enabled
**Solution:**
```python
bpy.ops.export_scene.gltf(
    filepath="object.glb",
    export_animations=True,
    export_animation_mode='ACTIONS',
    # Ensure object has animation_data
)

# Check object has animation data
if not obj.animation_data:
    print("Object has no animation data!")
```

---

## Export for Specific Targets

### ZX Console (N64/PS1 Era)

```python
def export_for_zx(filepath, armature):
    """Optimized export for ZX console."""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',

        # Animation
        export_animations=True,
        export_animation_mode='ACTIONS',
        export_frame_step=1,
        export_optimize_animation_size=True,

        # Skinning - strict 4 influences
        export_skins=True,
        export_all_influences=False,

        # No extras
        export_tangents=False,
        export_morph=False,

        # Compression off (ZX handles its own)
        export_draco_mesh_compression_enable=False,
    )
```

### Web/Three.js

```python
def export_for_web(filepath):
    """Export optimized for web viewing."""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',

        # Enable Draco compression
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,

        # Optimize animations
        export_optimize_animation_size=True,

        # Include materials
        export_materials='EXPORT',
        export_image_format='WEBP',
    )
```

---

## Batch Export

```python
import bpy
import os

def batch_export_actions(armature, output_dir):
    """Export each action as separate GLB file."""
    os.makedirs(output_dir, exist_ok=True)

    for action in bpy.data.actions:
        # Assign action
        armature.animation_data.action = action

        # Export
        filepath = os.path.join(output_dir, f"{action.name}.glb")
        bpy.ops.export_scene.gltf(
            filepath=filepath,
            export_format='GLB',
            export_animations=True,
            export_animation_mode='ACTIVE_ACTIONS',
            export_skins=True,
        )
        print(f"Exported: {filepath}")


def export_with_all_actions(filepath, armature):
    """Export single GLB containing all actions."""
    # Push all actions to NLA tracks to ensure export
    if not armature.animation_data:
        armature.animation_data_create()

    for action in bpy.data.actions:
        if action.name.startswith(armature.name) or True:  # Filter as needed
            track = armature.animation_data.nla_tracks.new()
            track.name = action.name
            strip = track.strips.new(action.name, 1, action)

    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        export_animations=True,
        export_animation_mode='ACTIONS',
        export_skins=True,
    )
```

---

## Post-Export Verification

```python
import json
import struct

def verify_glb(filepath):
    """Basic GLB structure verification."""
    with open(filepath, 'rb') as f:
        # Check magic number
        magic = f.read(4)
        if magic != b'glTF':
            print("ERROR: Not a valid GLB file")
            return False

        version = struct.unpack('<I', f.read(4))[0]
        length = struct.unpack('<I', f.read(4))[0]

        print(f"glTF version: {version}")
        print(f"File size: {length} bytes")

        # Read JSON chunk
        chunk_length = struct.unpack('<I', f.read(4))[0]
        chunk_type = f.read(4)

        if chunk_type == b'JSON':
            json_data = json.loads(f.read(chunk_length))

            if 'animations' in json_data:
                print(f"Animations: {len(json_data['animations'])}")
                for anim in json_data['animations']:
                    print(f"  - {anim.get('name', 'unnamed')}")

            if 'skins' in json_data:
                print(f"Skins: {len(json_data['skins'])}")

        return True

# Usage
verify_glb("character.glb")
```
