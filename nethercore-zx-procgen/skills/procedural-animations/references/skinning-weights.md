# Skinning & Weight Painting Reference

Complete guide to binding meshes to armatures in Blender.

## Core Concept

Skinning (mesh binding) determines how each vertex moves with the skeleton. Each vertex can be influenced by up to 4 bones (glTF requirement), with weights that sum to 1.0.

## Automatic Weights (Recommended First Approach)

Blender's automatic weights work well for most characters:

```python
import bpy

def bind_mesh_to_armature(mesh_obj, armature_obj):
    """Bind mesh to armature with automatic weights."""
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Select mesh first, then armature (armature must be active)
    mesh_obj.select_set(True)
    armature_obj.select_set(True)
    bpy.context.view_layer.objects.active = armature_obj

    # Parent with automatic weights
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
```

**When auto weights fail:**
- Mesh not watertight (gaps, open edges)
- Bones outside mesh volume
- Very thin or complex geometry

---

## Manual Vertex Groups

Create vertex groups matching bone names:

```python
import bpy

def create_vertex_group(mesh_obj, bone_name, vertex_indices, weight=1.0):
    """Create or update vertex group for bone."""
    # Get or create vertex group
    vg = mesh_obj.vertex_groups.get(bone_name)
    if vg is None:
        vg = mesh_obj.vertex_groups.new(name=bone_name)

    # Assign vertices with weight
    vg.add(vertex_indices, weight, 'REPLACE')
    return vg


# Example usage
mesh = bpy.data.objects["CharacterMesh"]
create_vertex_group(mesh, "spine", [10, 11, 12, 13, 14], 1.0)
create_vertex_group(mesh, "chest", [15, 16, 17, 18], 0.8)
```

### Vertex Group Operations

```python
# Add vertices with weight mode
vg.add([0, 1, 2], 1.0, 'ADD')      # Add to existing weight
vg.add([0, 1, 2], 1.0, 'REPLACE')  # Replace weight
vg.add([0, 1, 2], 0.5, 'SUBTRACT') # Subtract from weight

# Remove vertices from group
vg.remove([0, 1, 2])

# Get weight for specific vertex
weight = vg.weight(vertex_index)
```

---

## Weight Painting Mode

Interactive weight assignment:

```python
import bpy

def enter_weight_paint_mode(mesh_obj, armature_obj):
    """Enter weight paint mode with armature visible."""
    bpy.context.view_layer.objects.active = mesh_obj
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

    # Show armature in front
    armature_obj.show_in_front = True


def exit_weight_paint_mode():
    """Return to object mode."""
    bpy.ops.object.mode_set(mode='OBJECT')
```

### Programmatic Weight Painting

```python
import bpy
import bmesh

def paint_weights_by_distance(mesh_obj, bone_head, bone_tail, bone_name, falloff=1.0):
    """
    Assign weights based on distance to bone axis.

    falloff: Distance at which weight reaches 0
    """
    vg = mesh_obj.vertex_groups.get(bone_name)
    if vg is None:
        vg = mesh_obj.vertex_groups.new(name=bone_name)

    # Calculate weights per vertex
    mesh = mesh_obj.data
    bone_vec = bone_tail - bone_head
    bone_length = bone_vec.length

    for i, vert in enumerate(mesh.vertices):
        # World position of vertex
        world_pos = mesh_obj.matrix_world @ vert.co

        # Project onto bone axis
        to_vert = world_pos - bone_head
        t = to_vert.dot(bone_vec) / (bone_length * bone_length)
        t = max(0, min(1, t))  # Clamp to bone

        # Closest point on bone
        closest = bone_head + bone_vec * t

        # Distance from bone
        distance = (world_pos - closest).length

        # Weight from distance
        weight = max(0, 1 - distance / falloff)

        if weight > 0.001:
            vg.add([i], weight, 'REPLACE')
```

---

## Weight Cleanup (Critical for Export)

glTF requires max 4 bone influences per vertex. Clean weights before export:

```python
import bpy

def cleanup_weights(mesh_obj):
    """Normalize and limit weights for glTF export."""
    bpy.context.view_layer.objects.active = mesh_obj
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

    # Normalize all weights to sum to 1.0
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)

    # Limit to 4 influences per vertex
    bpy.ops.object.vertex_group_limit_total(limit=4)

    bpy.ops.object.mode_set(mode='OBJECT')
```

### Manual Influence Limiting

```python
import bpy

def limit_influences_manual(mesh_obj, max_influences=4):
    """Manually limit bone influences per vertex."""
    mesh = mesh_obj.data

    for vert in mesh.vertices:
        # Get all weights for this vertex
        weights = []
        for vg in mesh_obj.vertex_groups:
            try:
                w = vg.weight(vert.index)
                if w > 0:
                    weights.append((vg.name, w))
            except RuntimeError:
                pass  # Vertex not in group

        if len(weights) > max_influences:
            # Sort by weight descending
            weights.sort(key=lambda x: x[1], reverse=True)

            # Keep top N
            keep = weights[:max_influences]
            remove = weights[max_influences:]

            # Remove from extra groups
            for vg_name, _ in remove:
                vg = mesh_obj.vertex_groups[vg_name]
                vg.remove([vert.index])

            # Renormalize kept weights
            total = sum(w for _, w in keep)
            for vg_name, w in keep:
                vg = mesh_obj.vertex_groups[vg_name]
                vg.add([vert.index], w / total, 'REPLACE')
```

---

## Common Skinning Patterns

### Limb Gradients

Smooth transition between bones:

```python
def create_limb_weights(mesh_obj, upper_bone, lower_bone, upper_verts, lower_verts, blend_verts):
    """Create smooth weight transition at joint."""
    upper_vg = mesh_obj.vertex_groups.new(name=upper_bone)
    lower_vg = mesh_obj.vertex_groups.new(name=lower_bone)

    # Full weight at extremes
    upper_vg.add(upper_verts, 1.0, 'REPLACE')
    lower_vg.add(lower_verts, 1.0, 'REPLACE')

    # Blend at joint
    for i, idx in enumerate(blend_verts):
        t = i / len(blend_verts)  # 0 to 1
        upper_vg.add([idx], 1.0 - t, 'REPLACE')
        lower_vg.add([idx], t, 'REPLACE')
```

### Rigid Binding (No Blending)

For mechanical parts or rigid segments:

```python
def rigid_bind(mesh_obj, bone_name, vertex_indices):
    """Bind vertices 100% to single bone."""
    vg = mesh_obj.vertex_groups.new(name=bone_name)
    vg.add(vertex_indices, 1.0, 'REPLACE')

    # Ensure no other groups affect these vertices
    for other_vg in mesh_obj.vertex_groups:
        if other_vg.name != bone_name:
            other_vg.remove(vertex_indices)
```

### Heat Diffusion Simulation

For complex meshes, simulate heat diffusion from bones:

```python
def heat_weights_simple(mesh_obj, armature_obj, iterations=10, falloff=0.9):
    """Simple heat diffusion weight calculation."""
    mesh = mesh_obj.data

    # Initialize weights from bone positions
    weights = {bone.name: [0.0] * len(mesh.vertices) for bone in armature_obj.data.bones}

    for bone in armature_obj.data.bones:
        # Transform bone to world space
        head_world = armature_obj.matrix_world @ bone.head_local
        tail_world = armature_obj.matrix_world @ bone.tail_local

        for i, vert in enumerate(mesh.vertices):
            vert_world = mesh_obj.matrix_world @ vert.co
            dist = distance_to_line_segment(vert_world, head_world, tail_world)
            weights[bone.name][i] = max(0, 1 - dist * 2)

    # Diffuse weights along edges
    edges = [(e.vertices[0], e.vertices[1]) for e in mesh.edges]

    for _ in range(iterations):
        for bone_name in weights:
            new_weights = weights[bone_name].copy()
            for v0, v1 in edges:
                avg = (weights[bone_name][v0] + weights[bone_name][v1]) / 2
                new_weights[v0] = new_weights[v0] * falloff + avg * (1 - falloff)
                new_weights[v1] = new_weights[v1] * falloff + avg * (1 - falloff)
            weights[bone_name] = new_weights

    # Apply to vertex groups
    for bone_name, vert_weights in weights.items():
        vg = mesh_obj.vertex_groups.new(name=bone_name)
        for i, w in enumerate(vert_weights):
            if w > 0.001:
                vg.add([i], w, 'REPLACE')
```

---

## Debugging Weights

### Visualize Weight Distribution

```python
import bpy

def visualize_weights(mesh_obj, bone_name):
    """Color mesh vertices by weight for debugging."""
    mesh = mesh_obj.data

    # Ensure vertex colors exist
    if not mesh.vertex_colors:
        mesh.vertex_colors.new()

    color_layer = mesh.vertex_colors.active

    vg = mesh_obj.vertex_groups.get(bone_name)
    if not vg:
        return

    for poly in mesh.polygons:
        for loop_index in poly.loop_indices:
            vert_index = mesh.loops[loop_index].vertex_index
            try:
                weight = vg.weight(vert_index)
            except RuntimeError:
                weight = 0

            # Red = high weight, blue = low weight
            color_layer.data[loop_index].color = (weight, 0, 1 - weight, 1)
```

### Weight Statistics

```python
def print_weight_stats(mesh_obj):
    """Print statistics about vertex weights."""
    mesh = mesh_obj.data

    for vert in mesh.vertices:
        influences = []
        for vg in mesh_obj.vertex_groups:
            try:
                w = vg.weight(vert.index)
                if w > 0:
                    influences.append((vg.name, w))
            except RuntimeError:
                pass

        total = sum(w for _, w in influences)
        if abs(total - 1.0) > 0.01:
            print(f"Vertex {vert.index}: total weight = {total:.3f}")
        if len(influences) > 4:
            print(f"Vertex {vert.index}: {len(influences)} influences (max 4)")
```

---

## Armature Modifier

The armature modifier applies bone deformations:

```python
import bpy

def setup_armature_modifier(mesh_obj, armature_obj):
    """Add or configure armature modifier."""
    # Check for existing modifier
    mod = None
    for m in mesh_obj.modifiers:
        if m.type == 'ARMATURE':
            mod = m
            break

    # Create if needed
    if mod is None:
        mod = mesh_obj.modifiers.new('Armature', 'ARMATURE')

    # Configure
    mod.object = armature_obj
    mod.use_vertex_groups = True  # Use vertex groups for weights
    mod.use_bone_envelopes = False  # Don't use bone envelope weights

    return mod
```

### Modifier Order

Armature modifier should typically be first:

```python
def move_armature_modifier_first(mesh_obj):
    """Ensure armature modifier is applied first."""
    for i, mod in enumerate(mesh_obj.modifiers):
        if mod.type == 'ARMATURE':
            while i > 0:
                bpy.ops.object.modifier_move_up(modifier=mod.name)
                i -= 1
            break
```

---

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Mesh explodes | Zero weights or unbound vertices | Check all vertices have weights |
| Vertices stretch infinitely | Weights don't sum to 1.0 | Run normalize_all |
| Candy wrapper twist | Too few influences at joint | Add more bones or blend wider |
| Weight bleeding | Distant bones affecting vertices | Limit influence radius |
| Export fails | More than 4 influences | Run limit_total(limit=4) |
| Mesh doesn't move | No armature modifier | Add modifier and set object |

---

## Pre-Export Checklist

```python
def validate_skinning(mesh_obj, armature_obj):
    """Validate skinning before export."""
    issues = []

    # Check armature modifier exists
    has_modifier = any(m.type == 'ARMATURE' and m.object == armature_obj
                       for m in mesh_obj.modifiers)
    if not has_modifier:
        issues.append("No armature modifier")

    # Check all vertices have weights
    mesh = mesh_obj.data
    for vert in mesh.vertices:
        total_weight = 0
        influence_count = 0
        for vg in mesh_obj.vertex_groups:
            try:
                w = vg.weight(vert.index)
                if w > 0:
                    total_weight += w
                    influence_count += 1
            except RuntimeError:
                pass

        if total_weight < 0.99:
            issues.append(f"Vertex {vert.index}: insufficient weight ({total_weight:.2f})")
        if influence_count > 4:
            issues.append(f"Vertex {vert.index}: too many influences ({influence_count})")

    return issues
```
