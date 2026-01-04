# Blender Tangent Export for Normal Maps

Complete guide to exporting meshes with tangent vertex data for normal mapping.

## When You Need Tangents

Tangent data is required when:
- Mesh will use a normal map texture
- Material uses tangent-space lighting (Modes 0, 1, 2, 3 with normal maps)

Tangent data is **not** needed when:
- Using vertex normals only (no normal map)
- Flat-shaded low-poly aesthetic
- Memory-constrained (tangents add 4 bytes/vertex)

---

## Prerequisites

Before calculating tangents, the mesh must have:

1. **UV coordinates** - Tangents are calculated per UV layer
2. **Normals** - Tangents are perpendicular to normals
3. **Triangulated faces** - Recommended for consistent results

---

## Tangent Calculation

### Basic Calculation

```python
import bpy

def calculate_tangents(obj):
    """Calculate tangent vectors for the active mesh.

    Must be called after:
    - UV unwrapping
    - Normal calculation
    - Triangulation (recommended)
    """
    mesh = obj.data

    # Verify prerequisites
    if not mesh.uv_layers:
        raise ValueError(f"{obj.name} has no UV layer - cannot calculate tangents")

    if not mesh.polygons:
        raise ValueError(f"{obj.name} has no faces")

    # Calculate tangents
    mesh.calc_tangents()

    print(f"Tangents calculated for {obj.name}")
    return True
```

### With Error Handling

```python
def safe_calculate_tangents(obj):
    """Calculate tangents with validation and error handling."""
    mesh = obj.data

    # Check for UV layer
    if not mesh.uv_layers:
        print(f"WARNING: {obj.name} has no UVs, adding automatic UVs")
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0)
        bpy.ops.object.mode_set(mode='OBJECT')

    # Ensure normals are correct
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Calculate tangents
    try:
        mesh.calc_tangents()
        return True
    except RuntimeError as e:
        print(f"ERROR calculating tangents for {obj.name}: {e}")
        return False
```

---

## Complete Export Pipeline

### Post-Processing with Tangents

```python
import bpy
import math

def post_process_for_normal_maps(obj, settings=None):
    """Complete post-processing pipeline with tangent support.

    Args:
        obj: Blender mesh object
        settings: Optional dict with:
            - uv_method: 'smart', 'cube', 'cylinder' (default: 'smart')
            - auto_smooth_angle: degrees (default: 30)
            - max_tris: triangle limit (default: 2000)
    """
    if settings is None:
        settings = {}

    uv_method = settings.get('uv_method', 'smart')
    auto_smooth_angle = settings.get('auto_smooth_angle', 30)

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # 1. Apply modifiers
    for mod in obj.modifiers[:]:
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except RuntimeError:
            pass

    # 2. Apply transforms
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    # 3. UV unwrap
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    if uv_method == 'smart':
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    elif uv_method == 'cube':
        bpy.ops.uv.cube_project(cube_size=1.0)
    elif uv_method == 'cylinder':
        bpy.ops.uv.cylinder_project()

    # 4. Cleanup
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.mesh.delete_loose()

    # 5. Triangulate
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY')

    # 6. Normals
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = math.radians(auto_smooth_angle)

    # 7. Calculate tangents (CRITICAL for normal maps)
    obj.data.calc_tangents()

    print(f"Processed {obj.name} with tangents")
    return obj
```

### Export with Tangents

```python
def export_glb_with_tangents(filepath, obj=None):
    """Export mesh to GLB with tangent data for normal mapping.

    Args:
        filepath: Output file path (.glb)
        obj: Optional specific object to export (exports all if None)
    """
    export_settings = {
        'filepath': filepath,
        'export_format': 'GLB',
        'export_apply_modifiers': True,
        'export_normals': True,
        'export_tangents': True,      # CRITICAL: Enable tangent export
        'export_colors': 'ACTIVE',
        'export_materials': 'NONE',
        'export_yup': True,
    }

    if obj:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        export_settings['use_selection'] = True

    bpy.ops.export_scene.gltf(**export_settings)
    print(f"Exported with tangents: {filepath}")
```

---

## Complete Example Script

```python
#!/usr/bin/env python3
"""Generate mesh with tangent data for normal mapping."""

import bpy
import math

OUTPUT_DIR = "../generated/meshes"

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_wall_panel():
    """Create a wall panel mesh for normal mapping demo."""
    # Create subdivided plane
    bpy.ops.mesh.primitive_plane_add(size=2)
    obj = bpy.context.active_object
    obj.name = "wall_panel"

    # Subdivide for smooth normal interpolation
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=4)
    bpy.ops.object.mode_set(mode='OBJECT')

    return obj

def post_process_with_tangents(obj):
    """Full post-processing with tangent calculation."""
    bpy.context.view_layer.objects.active = obj

    # UV unwrap
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)

    # Cleanup
    bpy.ops.mesh.remove_doubles(threshold=0.0001)

    # Triangulate
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY')

    # Normals
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = math.radians(30)

    # Calculate tangents
    obj.data.calc_tangents()

def export_with_tangents(obj, filepath):
    """Export single object with tangent data."""
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)

    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=True,
        export_apply_modifiers=True,
        export_normals=True,
        export_tangents=True,  # Enable for normal maps
        export_colors='ACTIVE',
        export_materials='NONE',
        export_yup=True
    )

def main():
    clear_scene()

    # Create mesh
    obj = create_wall_panel()

    # Post-process with tangents
    post_process_with_tangents(obj)

    # Export
    export_with_tangents(obj, f"{OUTPUT_DIR}/wall_panel.glb")

    # Stats
    mesh = obj.data
    print(f"Exported: wall_panel.glb")
    print(f"  Triangles: {len(mesh.polygons)}")
    print(f"  Vertices: {len(mesh.vertices)}")
    print(f"  Has UVs: {len(mesh.uv_layers) > 0}")
    print(f"  Tangents: Enabled")

if __name__ == "__main__":
    main()
```

---

## Memory Considerations

Tangent data adds 4 bytes per vertex:

| Vertices | Tangent Cost |
|----------|--------------|
| 100 | 400 bytes |
| 500 | 2 KB |
| 1000 | 4 KB |
| 5000 | 20 KB |

**Vertex format with tangents:**
- Position: 12 bytes (3 × f32)
- UV: 8 bytes (2 × f32)
- Normal: 4 bytes (packed)
- **Tangent: 4 bytes (packed)**
- Color: 4 bytes (RGBA u8)

Total: 32 bytes/vertex with tangents vs 28 bytes without.

---

## Validation

```python
def validate_tangent_mesh(obj):
    """Validate mesh is ready for normal mapping."""
    mesh = obj.data
    issues = []

    # Check UVs
    if not mesh.uv_layers:
        issues.append("No UV layer - tangents cannot be calculated")

    # Check polygon count (should be triangulated)
    quads = [f for f in mesh.polygons if len(f.vertices) == 4]
    if quads:
        issues.append(f"{len(quads)} quads found - should be triangulated")

    # Check for proper tangent calculation
    try:
        mesh.calc_tangents()
    except RuntimeError as e:
        issues.append(f"Tangent calculation failed: {e}")

    if issues:
        print(f"Validation issues for {obj.name}:")
        for issue in issues:
            print(f"  - {issue}")
        return False

    print(f"{obj.name} is valid for normal mapping")
    return True
```

---

## Troubleshooting

### "Tangent calculation failed"

**Cause:** Missing UV layer or degenerate geometry.
**Solution:** Ensure mesh has UVs and no zero-area faces.

### Lighting looks wrong with normal map

**Cause:** Tangent space mismatch.
**Solution:** Ensure mesh uses consistent tangent convention (Y-up, right-handed).

### Visible seams at UV island boundaries

**Cause:** Tangent discontinuity at UV seams.
**Solution:**
1. Minimize UV seams
2. Use larger UV islands
3. Mark sharp edges at UV seams

---

## Quick Reference

### Required for normal maps:
- [x] UV layer present
- [x] Normals calculated and consistent
- [x] `mesh.calc_tangents()` called
- [x] `export_tangents=True` in export

### Export settings:
```python
bpy.ops.export_scene.gltf(
    filepath="mesh.glb",
    export_format='GLB',
    export_normals=True,
    export_tangents=True,  # REQUIRED for normal maps
    # ... other settings
)
```
