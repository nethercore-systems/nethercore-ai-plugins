# Blender bpy Post-Processing Reference

Required post-processing steps for all meshes before export. Every mesh MUST have UVs, proper normals, and clean topology.

## Processing Order

Apply in this sequence for best results:

```
1. Apply all modifiers
2. Set correct scale/rotation
3. UV unwrap
4. Clean up geometry
5. Set normals
6. Triangulate
7. Validate
8. Export
```

---

## Step 1: Apply Modifiers

Make all modifiers permanent before export.

```python
def apply_all_modifiers(obj):
    """Apply all modifiers on an object."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    for mod in obj.modifiers:
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except RuntimeError as e:
            print(f"Could not apply {mod.name}: {e}")
```

---

## Step 2: Apply Transforms

Ensure scale is (1,1,1) and rotation is (0,0,0).

```python
def apply_transforms(obj):
    """Apply location, rotation, and scale."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
```

---

## Step 3: UV Unwrapping

Every textured mesh needs UVs. Choose the method based on shape.

### Smart Project (General Purpose)

Best for: Most meshes, complex shapes, organic forms.

```python
def uv_smart_project(obj, angle_limit=66.0, island_margin=0.02):
    """Apply smart UV projection."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(
        angle_limit=angle_limit,    # Higher = fewer islands
        island_margin=island_margin  # Space between islands
    )
    bpy.ops.object.mode_set(mode='OBJECT')
```

### Cube Project

Best for: Box-like objects, architecture, crates.

```python
def uv_cube_project(obj, cube_size=1.0):
    """Apply cube projection UVs."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(
        cube_size=cube_size,
        correct_aspect=True
    )
    bpy.ops.object.mode_set(mode='OBJECT')
```

### Cylinder Project

Best for: Cylindrical objects, pillars, pipes.

```python
def uv_cylinder_project(obj, direction='VIEW_ON_EQUATOR'):
    """Apply cylinder projection UVs."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cylinder_project(
        direction=direction,  # 'VIEW_ON_EQUATOR', 'VIEW_ON_POLES', 'ALIGN_TO_OBJECT'
        correct_aspect=True
    )
    bpy.ops.object.mode_set(mode='OBJECT')
```

### Sphere Project

Best for: Spherical objects, orbs, planets.

```python
def uv_sphere_project(obj):
    """Apply sphere projection UVs."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.sphere_project(correct_aspect=True)
    bpy.ops.object.mode_set(mode='OBJECT')
```

### Manual Unwrap (with seams)

Best for: Characters, complex objects needing precise UV layout.

```python
def uv_unwrap_with_seams(obj, seam_edges=None):
    """Unwrap using angle-based method with marked seams."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    # If seam edges provided, mark them
    if seam_edges:
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_mode(type='EDGE')
        for edge_idx in seam_edges:
            obj.data.edges[edge_idx].select = True
        bpy.ops.mesh.mark_seam(clear=False)

    # Unwrap
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')
```

### Lightmap Pack

For baked lighting (vertex colors don't need this).

```python
def uv_lightmap_pack(obj, margin=0.02):
    """Pack UVs for lightmapping (no overlaps)."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.lightmap_pack(
        PREF_MARGIN_DIV=margin,
        PREF_NEW_UVLAYER=True  # Create second UV layer
    )
    bpy.ops.object.mode_set(mode='OBJECT')
```

---

## Step 4: Geometry Cleanup

Remove degenerate geometry that causes rendering issues.

```python
def cleanup_geometry(obj):
    """Remove doubles, loose geometry, and degenerate faces."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    # Merge vertices that are too close
    bpy.ops.mesh.remove_doubles(threshold=0.0001)

    # Delete loose vertices and edges (not connected to faces)
    bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=False)

    # Delete degenerate geometry (zero-area faces, zero-length edges)
    bpy.ops.mesh.dissolve_degenerate(threshold=0.0001)

    bpy.ops.object.mode_set(mode='OBJECT')
```

### Additional Cleanup Operations

```python
def fix_non_manifold(obj):
    """Fix non-manifold geometry (holes, internal faces)."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    # Select non-manifold edges
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold(
        extend=False,
        use_wire=True,
        use_boundary=True,
        use_multi_face=True,
        use_non_contiguous=True
    )

    # Fill holes (if any selected)
    try:
        bpy.ops.mesh.fill_holes(sides=32)
    except:
        pass

    bpy.ops.object.mode_set(mode='OBJECT')

def remove_interior_faces(obj):
    """Remove faces inside the mesh (common after booleans)."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_interior_faces()
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.object.mode_set(mode='OBJECT')
```

---

## Step 5: Normals

Ensure normals are consistent and set shading mode.

### Recalculate Normals

Fix inverted or inconsistent normals.

```python
def recalculate_normals(obj, inside=False):
    """Recalculate normals to face outward (or inward)."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=inside)
    bpy.ops.object.mode_set(mode='OBJECT')
```

### Smooth Shading

For organic, curved surfaces.

```python
def apply_smooth_shading(obj, auto_smooth_angle=30):
    """Apply smooth shading with auto-smooth for hard edges."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()

    # Auto-smooth: edges sharper than angle stay hard
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = math.radians(auto_smooth_angle)
```

### Flat Shading

For low-poly, faceted look.

```python
def apply_flat_shading(obj):
    """Apply flat shading (faceted look)."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_flat()
    obj.data.use_auto_smooth = False
```

### Custom Split Normals

For precise control over shading.

```python
def set_custom_normals(obj, normal_direction=(0, 0, 1)):
    """Set custom split normals (all pointing same direction)."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.set_normals_from_faces(keep_sharp=True)
    bpy.ops.object.mode_set(mode='OBJECT')
```

---

## Step 6: Triangulation

Game engines require triangles. Convert all quads/ngons.

```python
def triangulate_mesh(obj, quad_method='BEAUTY', ngon_method='BEAUTY'):
    """Convert all faces to triangles."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris(
        quad_method=quad_method,   # 'BEAUTY', 'FIXED', 'FIXED_ALTERNATE', 'SHORTEST_DIAGONAL', 'LONGEST_DIAGONAL'
        ngon_method=ngon_method    # 'BEAUTY', 'CLIP'
    )
    bpy.ops.object.mode_set(mode='OBJECT')
```

**Quad methods:**
- `'BEAUTY'` — Best looking splits (default)
- `'FIXED'` — Consistent direction
- `'SHORTEST_DIAGONAL'` — Split along shortest diagonal

---

## Step 7: Validation

Check mesh before export.

```python
def validate_mesh(obj, max_tris=2000, require_uvs=True):
    """Validate mesh meets requirements."""
    mesh = obj.data
    issues = []

    # Check triangle count
    tri_count = len([f for f in mesh.polygons])
    if tri_count > max_tris:
        issues.append(f"Triangle count {tri_count} exceeds limit {max_tris}")

    # Check for ngons (should be none after triangulation)
    ngons = [f for f in mesh.polygons if len(f.vertices) > 4]
    if ngons:
        issues.append(f"Found {len(ngons)} ngons (non-triangulated)")

    # Check for UV layer
    if require_uvs and len(mesh.uv_layers) == 0:
        issues.append("No UV layer found")

    # Check for loose vertices
    vertex_face_counts = [0] * len(mesh.vertices)
    for face in mesh.polygons:
        for v_idx in face.vertices:
            vertex_face_counts[v_idx] += 1
    loose = sum(1 for c in vertex_face_counts if c == 0)
    if loose > 0:
        issues.append(f"Found {loose} loose vertices")

    # Report
    if issues:
        print(f"Validation issues for {obj.name}:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"{obj.name} passed validation ({tri_count} tris)")
        return True
```

### Get Mesh Statistics

```python
def get_mesh_stats(obj):
    """Get detailed mesh statistics."""
    mesh = obj.data
    return {
        'vertices': len(mesh.vertices),
        'edges': len(mesh.edges),
        'faces': len(mesh.polygons),
        'triangles': sum(len(f.vertices) - 2 for f in mesh.polygons),
        'uv_layers': len(mesh.uv_layers),
        'vertex_colors': len(mesh.vertex_colors),
        'has_normals': mesh.has_custom_normals,
        'bounds': [list(obj.bound_box[0]), list(obj.bound_box[6])]
    }
```

---

## Step 8: Export

Export to game-ready formats.

### GLB (Recommended)

Binary GLTF — compact, widely supported.

```python
def export_glb(filepath, selected_only=False):
    """Export to GLB format."""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=selected_only,
        export_apply_modifiers=True,
        export_normals=True,
        export_tangents=False,      # Only needed for normal maps
        export_colors=True,         # Include vertex colors
        export_materials='NONE',    # Skip materials for procgen
        export_textures=False,
        export_yup=True             # Y-up for game engines
    )
```

### GLTF (Separate files)

Human-readable JSON + binary.

```python
def export_gltf(filepath, selected_only=False):
    """Export to GLTF format (separate files)."""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLTF_SEPARATE',
        use_selection=selected_only,
        export_apply_modifiers=True,
        export_normals=True,
        export_colors=True
    )
```

### OBJ

Legacy format, widely compatible.

```python
def export_obj(filepath, selected_only=False):
    """Export to OBJ format."""
    bpy.ops.export_scene.obj(
        filepath=filepath,
        use_selection=selected_only,
        use_mesh_modifiers=True,
        use_normals=True,
        use_uvs=True,
        use_materials=False,
        axis_forward='-Z',
        axis_up='Y'
    )
```

### FBX

For engines requiring FBX.

```python
def export_fbx(filepath, selected_only=False):
    """Export to FBX format."""
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=selected_only,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        use_mesh_modifiers=True,
        mesh_smooth_type='FACE',
        axis_forward='-Z',
        axis_up='Y'
    )
```

---

## Complete Post-Processing Pipeline

```python
#!/usr/bin/env python3
"""Complete post-processing pipeline for game meshes."""

import bpy
import math

def post_process_mesh(obj, settings=None):
    """
    Complete post-processing pipeline.

    Args:
        obj: The Blender object to process
        settings: Dict with optional overrides:
            - max_tris: Maximum triangle count (default: 2000)
            - uv_method: 'smart', 'cube', 'cylinder', 'sphere' (default: 'smart')
            - shading: 'smooth', 'flat' (default: 'smooth')
            - auto_smooth_angle: Degrees (default: 30)
    """
    if settings is None:
        settings = {}

    max_tris = settings.get('max_tris', 2000)
    uv_method = settings.get('uv_method', 'smart')
    shading = settings.get('shading', 'smooth')
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
    elif uv_method == 'sphere':
        bpy.ops.uv.sphere_project()

    # 4. Cleanup
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.mesh.delete_loose()
    bpy.ops.mesh.dissolve_degenerate(threshold=0.0001)

    # 5. Triangulate
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY')

    # 6. Normals
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    if shading == 'smooth':
        bpy.ops.object.shade_smooth()
        obj.data.use_auto_smooth = True
        obj.data.auto_smooth_angle = math.radians(auto_smooth_angle)
    else:
        bpy.ops.object.shade_flat()

    # 7. Validate
    tri_count = len(obj.data.polygons)
    if tri_count > max_tris:
        print(f"WARNING: {obj.name} has {tri_count} tris (limit: {max_tris})")
        return False

    print(f"Processed {obj.name}: {tri_count} tris, UVs: {len(obj.data.uv_layers) > 0}")
    return True


def batch_post_process(objects, output_dir, format='GLB'):
    """Process multiple objects and export."""
    import os

    for obj in objects:
        success = post_process_mesh(obj)
        if success:
            filename = f"{obj.name}.{format.lower()}"
            filepath = os.path.join(output_dir, filename)

            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)

            if format == 'GLB':
                bpy.ops.export_scene.gltf(
                    filepath=filepath,
                    export_format='GLB',
                    use_selection=True
                )
            elif format == 'OBJ':
                bpy.ops.export_scene.obj(
                    filepath=filepath,
                    use_selection=True
                )

            print(f"Exported: {filepath}")


# Example usage
if __name__ == "__main__":
    # Process all mesh objects in scene
    mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

    for obj in mesh_objects:
        post_process_mesh(obj, {
            'max_tris': 1000,
            'uv_method': 'smart',
            'shading': 'smooth',
            'auto_smooth_angle': 35
        })

    # Export all
    bpy.ops.export_scene.gltf(
        filepath="output.glb",
        export_format='GLB'
    )
```

---

## Quick Reference

### Minimum Requirements

Every exported mesh needs:
- [x] All modifiers applied
- [x] Scale/rotation applied
- [x] At least one UV layer
- [x] Consistent normals (outward)
- [x] Triangulated (no quads/ngons)
- [x] No loose geometry

### Recommended Settings by Asset Type

| Asset Type | UV Method | Shading | Auto-Smooth |
|------------|-----------|---------|-------------|
| Props (crates, barrels) | Cube | Smooth | 45° |
| Organic (creatures) | Smart | Smooth | 30° |
| Architecture | Smart | Smooth | 60° |
| Low-poly style | Smart | Flat | N/A |
| Vehicles | Smart | Smooth | 40° |
| Characters | Manual | Smooth | 30° |
