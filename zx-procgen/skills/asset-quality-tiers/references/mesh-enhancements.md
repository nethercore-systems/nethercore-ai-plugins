# Mesh Enhancement Techniques

Detailed techniques for upgrading mesh quality through the tier system.

## Placeholder → Temp Upgrades

### Add Proper UV Mapping

Placeholder meshes often lack UVs. Apply appropriate projection:

```python
import bpy
import bmesh

def apply_uv_projection(obj, projection_type='box', scale=1.0, axis='Y'):
    """Apply UV projection to mesh object.

    Args:
        obj: Blender mesh object
        projection_type: 'box', 'cylindrical', or 'spherical'
        scale: UV scale factor
        axis: Axis for cylindrical projection
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    if projection_type == 'box':
        # Box projection for architectural/cubic shapes
        bpy.ops.uv.cube_project(cube_size=scale)
    elif projection_type == 'cylindrical':
        # Cylindrical for rounded objects
        bpy.ops.uv.cylinder_project(scale_to_bounds=True)
    elif projection_type == 'spherical':
        # Spherical for organic shapes
        bpy.ops.uv.sphere_project(scale_to_bounds=True)

    bpy.ops.object.mode_set(mode='OBJECT')
```

### Calculate Normals

Ensure normals are present and correct:

```python
import bpy

def apply_normals(obj, smooth=True, angle_threshold=30.0):
    """Apply normal calculation to mesh.

    Args:
        obj: Blender mesh object
        smooth: True for smooth shading, False for flat
        angle_threshold: Angle for auto-smooth (degrees)
    """
    bpy.context.view_layer.objects.active = obj

    if smooth:
        # Smooth shading with auto-smooth
        bpy.ops.object.shade_smooth()
        obj.data.use_auto_smooth = True
        obj.data.auto_smooth_angle = angle_threshold * (3.14159 / 180)
    else:
        # Flat/faceted shading
        bpy.ops.object.shade_flat()
```

### Clean Geometry

Remove degenerate triangles and fix topology:

```python
import bpy
import bmesh

def clean_geometry(obj, merge_distance=0.001, epsilon=1e-6):
    """Clean mesh geometry by removing degenerates and merging close vertices.

    Args:
        obj: Blender mesh object
        merge_distance: Distance threshold for merging vertices
        epsilon: Threshold for degenerate face detection
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    # Get bmesh
    bm = bmesh.from_edit_mesh(obj.data)

    # Remove zero-area triangles (degenerates)
    bmesh.ops.dissolve_degenerate(bm, dist=epsilon, edges=bm.edges)

    # Merge close vertices
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge_distance)

    # Recalculate normals (fix winding)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
```

### Basic Shape Improvement

Transform primitives into proper game assets:

```python
import bpy
import bmesh
import numpy as np

def add_surface_noise(obj, amplitude=0.02, frequency=4.0):
    """Add noise displacement to mesh vertices.

    Args:
        obj: Blender mesh object
        amplitude: Noise amplitude
        frequency: Noise frequency
    """
    mesh = obj.data
    for vert in mesh.vertices:
        # Simple noise based on position
        noise_val = np.sin(vert.co.x * frequency) * np.sin(vert.co.y * frequency) * np.sin(vert.co.z * frequency)
        offset = noise_val * amplitude
        vert.co += vert.normal * offset

def subdivide_and_relax(obj, subdivisions=1, relax_iterations=2, relax_factor=0.3):
    """Subdivide mesh and relax to smooth sharp corners.

    Args:
        obj: Blender mesh object
        subdivisions: Number of subdivision iterations
        relax_iterations: Number of smooth/relax passes
        relax_factor: Smoothing factor (0-1)
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    # Subdivide
    bpy.ops.mesh.subdivide(number_cuts=subdivisions)

    # Relax/smooth
    for _ in range(relax_iterations):
        bpy.ops.mesh.vertices_smooth(factor=relax_factor)

    bpy.ops.object.mode_set(mode='OBJECT')
```

---

## Temp → Final Upgrades

### Add Bevels

Bevels catch light and improve visual quality significantly:

```python
import bpy
import bmesh

def apply_bevel(obj, width=0.02, segments=1, angle_threshold=30.0):
    """Apply bevel to hard edges.

    Args:
        obj: Blender mesh object
        width: Bevel width
        segments: Number of bevel segments
        angle_threshold: Angle threshold for edge selection (degrees)
    """
    # Add bevel modifier
    bevel_mod = obj.modifiers.new(name='Bevel', type='BEVEL')
    bevel_mod.width = width
    bevel_mod.segments = segments
    bevel_mod.limit_method = 'ANGLE'
    bevel_mod.angle_limit = angle_threshold * (3.14159 / 180)

    # Apply modifier
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier='Bevel')

def bevel_selected_edges(obj, edge_indices, width=0.03, segments=2):
    """Bevel specific edges by index.

    Args:
        obj: Blender mesh object
        edge_indices: List of edge indices to bevel
        width: Bevel width
        segments: Number of segments
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    bm = bmesh.from_edit_mesh(obj.data)
    bm.edges.ensure_lookup_table()

    for idx in edge_indices:
        if idx < len(bm.edges):
            bm.edges[idx].select = True

    bpy.ops.mesh.bevel(offset=width, segments=segments)
    bpy.ops.object.mode_set(mode='OBJECT')
```

### Improve Silhouette

Silhouette clarity is critical for game readability:

```python
import bpy
import bmesh

def extrude_faces(obj, face_indices, distance=0.1, scale=0.9):
    """Extrude selected faces to add distinctive features.

    Args:
        obj: Blender mesh object
        face_indices: List of face indices to extrude
        distance: Extrusion distance
        scale: Scale factor for extruded faces
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()

    for idx in face_indices:
        if idx < len(bm.faces):
            bm.faces[idx].select = True

    bmesh.update_edit_mesh(obj.data)

    # Extrude and scale
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, distance)})
    bpy.ops.transform.resize(value=(scale, scale, scale))

    bpy.ops.object.mode_set(mode='OBJECT')

def inset_and_extrude(obj, face_indices, inset_distance=0.05, extrude_distance=-0.03):
    """Create recesses by insetting then extruding faces.

    Args:
        obj: Blender mesh object
        face_indices: List of face indices
        inset_distance: Inset thickness
        extrude_distance: Extrusion depth (negative for inward)
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()

    for idx in face_indices:
        if idx < len(bm.faces):
            bm.faces[idx].select = True

    bmesh.update_edit_mesh(obj.data)

    # Inset then extrude
    bpy.ops.mesh.inset(thickness=inset_distance, use_boundary=True)
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, extrude_distance)})

    bpy.ops.object.mode_set(mode='OBJECT')
```

### Optimize Topology

Clean up topology while maintaining quality:

```python
import bpy

def decimate_mesh(obj, ratio=0.7, preserve_uvs=True):
    """Reduce polygon count while preserving quality.

    Args:
        obj: Blender mesh object
        ratio: Target ratio (0.7 = reduce to 70%)
        preserve_uvs: Whether to preserve UV seams
    """
    decimate_mod = obj.modifiers.new(name='Decimate', type='DECIMATE')
    decimate_mod.ratio = ratio
    decimate_mod.use_collapse_triangulate = True

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier='Decimate')

def triangulate_mesh(obj, method='BEAUTY'):
    """Triangulate mesh for better performance.

    Args:
        obj: Blender mesh object
        method: Triangulation method ('BEAUTY', 'FIXED', 'FIXED_ALTERNATE', 'SHORTEST_DIAGONAL')
    """
    tri_mod = obj.modifiers.new(name='Triangulate', type='TRIANGULATE')
    tri_mod.quad_method = method

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier='Triangulate')
```

### Enhance UV Layout

Improve texture space utilization:

```python
import bpy

def pack_uvs(obj, margin=0.01, rotate=True):
    """Pack UVs to maximize texture space usage.

    Args:
        obj: Blender mesh object
        margin: Margin between UV islands
        rotate: Allow rotation for better packing
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.uv.pack_islands(margin=margin, rotate=rotate)

    bpy.ops.object.mode_set(mode='OBJECT')

def relax_uvs(obj, iterations=50):
    """Relax UVs to reduce stretch.

    Args:
        obj: Blender mesh object
        iterations: Number of relaxation iterations
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    # Use minimize stretch operation
    bpy.ops.uv.minimize_stretch(iterations=iterations)

    bpy.ops.object.mode_set(mode='OBJECT')
```

### Add Secondary Details

Include supporting shapes:

```python
import bpy
import bmesh
import numpy as np
from mathutils import Vector

def generate_bolt(radius=0.02, height=0.01, segments=6):
    """Generate a bolt/rivet mesh.

    Args:
        radius: Bolt head radius
        height: Bolt head height
        segments: Number of sides

    Returns:
        New Blender mesh object
    """
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=height,
        vertices=segments
    )
    return bpy.context.active_object

def add_bolts_at_positions(positions, radius=0.02, height=0.01):
    """Add bolts/rivets at specified positions.

    Args:
        positions: List of (x, y, z) tuples
        radius: Bolt radius
        height: Bolt height
    """
    bolts = []
    for pos in positions:
        bolt = generate_bolt(radius, height)
        bolt.location = Vector(pos)
        bolts.append(bolt)

    # Join all bolts into single object
    bpy.ops.object.select_all(action='DESELECT')
    for bolt in bolts:
        bolt.select_set(True)
    bpy.context.view_layer.objects.active = bolts[0]
    bpy.ops.object.join()

    return bpy.context.active_object
```

---

## Final → Hero Upgrades

### Add Edge Loops

Strategic edge loops for better deformation and detail:

```python
import bpy
import bmesh

def insert_edge_loop(obj, edge_indices, offset=0.1):
    """Insert edge loops near specified edges.

    Args:
        obj: Blender mesh object
        edge_indices: List of edge indices to loop cut near
        offset: Offset from original edge (0-1)
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    bm = bmesh.from_edit_mesh(obj.data)
    bm.edges.ensure_lookup_table()

    for idx in edge_indices:
        if idx < len(bm.edges):
            bm.edges[idx].select = True

    bmesh.update_edit_mesh(obj.data)

    # Loop cut with offset
    bpy.ops.mesh.loop_multi_select(ring=True)
    bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 1}, TRANSFORM_OT_edge_slide={"value": offset})

    bpy.ops.object.mode_set(mode='OBJECT')

def add_support_loops(obj, hard_edge_indices, distance=0.02):
    """Add support loops near hard edges for subdivision.

    Args:
        obj: Blender mesh object
        hard_edge_indices: List of hard edge indices
        distance: Distance of support loop from edge
    """
    bpy.context.view_layer.objects.active = obj

    # Add crease to mark hard edges, then add edge split
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    bm.edges.ensure_lookup_table()

    crease_layer = bm.edges.layers.crease.verify()

    for idx in hard_edge_indices:
        if idx < len(bm.edges):
            bm.edges[idx][crease_layer] = 1.0

    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
```

### Micro-Detail Addition

Fine details visible on close inspection:

```python
import bpy
import bmesh
import numpy as np

def add_surface_imperfections(obj, scale=20.0, amplitude=0.002, octaves=3):
    """Add micro surface noise for imperfections.

    Args:
        obj: Blender mesh object
        scale: Noise frequency scale
        amplitude: Maximum displacement
        octaves: Noise octaves for detail
    """
    mesh = obj.data
    for vert in mesh.vertices:
        total_noise = 0.0
        freq = scale
        amp = amplitude

        for _ in range(octaves):
            noise = (np.sin(vert.co.x * freq) *
                     np.sin(vert.co.y * freq * 1.3) *
                     np.sin(vert.co.z * freq * 0.7))
            total_noise += noise * amp
            freq *= 2
            amp *= 0.5

        vert.co += vert.normal * total_noise

def add_edge_chipping(obj, probability=0.3, depth=0.005, width=0.01):
    """Add edge wear/chipping effect.

    Args:
        obj: Blender mesh object
        probability: Probability of chip at each edge vertex
        depth: Chip depth
        width: Chip width
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()

    # Find edge vertices (vertices with high valence or sharp angles)
    for vert in bm.verts:
        if len(vert.link_edges) >= 3 and np.random.random() < probability:
            # Displace vertex inward
            avg_normal = sum((e.other_vert(vert).normal for e in vert.link_edges), vert.normal)
            avg_normal.normalize()
            vert.co -= avg_normal * depth * np.random.uniform(0.5, 1.0)

    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
```

### Secondary Shapes

Add smaller supporting elements:

```python
import bpy
from mathutils import Vector, Matrix
import numpy as np

def generate_cable(start, end, sag=0.1, radius=0.005, segments=16):
    """Generate a sagging cable between two points.

    Args:
        start: Start position (x, y, z)
        end: End position (x, y, z)
        sag: Amount of sag in the middle
        radius: Cable radius
        segments: Number of segments

    Returns:
        Blender curve object
    """
    # Create curve
    curve_data = bpy.data.curves.new('Cable', type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = radius

    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(segments - 1)

    start_v = Vector(start)
    end_v = Vector(end)

    for i, point in enumerate(spline.bezier_points):
        t = i / (segments - 1)
        # Catenary-like curve
        pos = start_v.lerp(end_v, t)
        pos.z -= sag * np.sin(t * np.pi)  # Sag in middle

        point.co = pos
        point.handle_type_left = 'AUTO'
        point.handle_type_right = 'AUTO'

    cable_obj = bpy.data.objects.new('Cable', curve_data)
    bpy.context.collection.objects.link(cable_obj)

    return cable_obj

def generate_handle(style='industrial', length=0.15, grip_radius=0.02):
    """Generate a handle mesh.

    Args:
        style: Handle style ('industrial', 'rounded')
        length: Handle length
        grip_radius: Grip diameter

    Returns:
        Blender mesh object
    """
    bpy.ops.mesh.primitive_cylinder_add(
        radius=grip_radius,
        depth=length,
        vertices=12
    )
    handle = bpy.context.active_object

    if style == 'industrial':
        # Add end caps
        bpy.ops.mesh.primitive_cylinder_add(
            radius=grip_radius * 1.3,
            depth=length * 0.1,
            location=(0, 0, length / 2)
        )
        cap1 = bpy.context.active_object

        bpy.ops.mesh.primitive_cylinder_add(
            radius=grip_radius * 1.3,
            depth=length * 0.1,
            location=(0, 0, -length / 2)
        )
        cap2 = bpy.context.active_object

        # Join
        bpy.ops.object.select_all(action='DESELECT')
        handle.select_set(True)
        cap1.select_set(True)
        cap2.select_set(True)
        bpy.context.view_layer.objects.active = handle
        bpy.ops.object.join()

    return bpy.context.active_object
```

### Perfect Topology

Ensure optimal topology for all use cases:

```python
import bpy
import bmesh

def quadrangulate_mesh(obj, preserve_boundaries=True):
    """Convert triangles to quads for better topology.

    Args:
        obj: Blender mesh object
        preserve_boundaries: Keep boundary edges intact
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.tris_convert_to_quads(
        face_threshold=40.0,
        shape_threshold=40.0
    )

    bpy.ops.object.mode_set(mode='OBJECT')

def optimize_edge_flow(obj, iterations=20):
    """Optimize mesh edge flow for better deformation.

    Args:
        obj: Blender mesh object
        iterations: Number of optimization passes
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    # Use smooth with preserve volume
    for _ in range(iterations):
        bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=1)

    bpy.ops.object.mode_set(mode='OBJECT')
```

### Vertex Color Enhancement

Add vertex colors for variation:

```python
import bpy
import bmesh
import numpy as np

def bake_ambient_occlusion(obj, samples=64, distance=0.5):
    """Bake ambient occlusion to vertex colors.

    Args:
        obj: Blender mesh object
        samples: Number of AO samples
        distance: AO ray distance
    """
    # Ensure vertex color layer exists
    if not obj.data.vertex_colors:
        obj.data.vertex_colors.new(name='AO')

    color_layer = obj.data.vertex_colors['AO']

    # Simple approximation - darken based on local concavity
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()

    for face in bm.faces:
        for loop in face.loops:
            vert = loop.vert
            # Estimate concavity from neighboring normals
            avg_normal = sum((v.normal for v in vert.link_verts), vert.normal)
            avg_normal.normalize()
            concavity = 1.0 - max(0, vert.normal.dot(avg_normal))
            ao_value = 1.0 - concavity * 0.5

            loop_idx = loop.index
            color_layer.data[loop_idx].color = (ao_value, ao_value, ao_value, 1.0)

    bm.free()

def add_vertex_color_variation(obj, hue_range=0.05, sat_range=0.1, val_range=0.15, scale=2.0):
    """Add color variation to vertex colors.

    Args:
        obj: Blender mesh object
        hue_range: Hue variation range
        sat_range: Saturation variation range
        val_range: Value variation range
        scale: Noise scale
    """
    if not obj.data.vertex_colors:
        obj.data.vertex_colors.new(name='Variation')

    color_layer = obj.data.vertex_colors.active

    mesh = obj.data
    for poly in mesh.polygons:
        for loop_idx in poly.loop_indices:
            vert_idx = mesh.loops[loop_idx].vertex_index
            vert = mesh.vertices[vert_idx]

            # Generate noise-based variation
            noise = np.sin(vert.co.x * scale) * np.sin(vert.co.y * scale * 1.3)

            base_color = color_layer.data[loop_idx].color
            r = base_color[0] + noise * val_range
            g = base_color[1] + noise * val_range * 0.9
            b = base_color[2] + noise * val_range * 0.8

            color_layer.data[loop_idx].color = (
                max(0, min(1, r)),
                max(0, min(1, g)),
                max(0, min(1, b)),
                1.0
            )
```

---

## Silhouette Improvement Techniques

### Principle: Readability at Distance

Game assets must be recognizable from afar:

1. **Strong primary shape** - Main form clearly reads
2. **Distinctive features** - Unique elements break up shape
3. **Negative space** - Gaps and holes create interest
4. **Asymmetry** - Avoid perfectly symmetric shapes

### Common Silhouette Problems

| Problem | Solution |
|---------|----------|
| Blobby/unclear | Add extrusions, insets, distinctive shapes |
| Too symmetric | Break symmetry with details on one side |
| No negative space | Add holes, gaps, overlapping elements |
| Lost at distance | Exaggerate key features |

### Silhouette Enhancement Code

```python
import bpy
import bmesh
import numpy as np

def scale_protrusions(obj, scale=1.2):
    """Exaggerate protruding features for better silhouette.

    Args:
        obj: Blender mesh object
        scale: Scale factor for protrusions
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()

    # Find vertices that protrude (positive distance from center)
    center = sum((v.co for v in bm.verts), bm.verts[0].co.copy()) / len(bm.verts)

    for vert in bm.verts:
        direction = vert.co - center
        dist = direction.length
        if dist > 0:
            # Scale outward
            vert.co = center + direction * scale

    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

def add_silhouette_breakers(obj, count=3, size_range=(0.1, 0.2)):
    """Add distinctive elements to break up silhouette.

    Args:
        obj: Blender mesh object
        count: Number of elements to add
        size_range: Min/max size of elements
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(obj.data)
    bm.edges.ensure_lookup_table()

    # Find boundary edges for placement
    boundary_edges = [e for e in bm.edges if e.is_boundary]

    if boundary_edges:
        # Select random edges
        selected = np.random.choice(boundary_edges, min(count, len(boundary_edges)), replace=False)
        for edge in selected:
            edge.select = True

        bmesh.update_edit_mesh(obj.data)

        # Extrude for visual interest
        size = np.random.uniform(size_range[0], size_range[1])
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, size)})

    bpy.ops.object.mode_set(mode='OBJECT')
```

---

## UV Enhancement Techniques

### Coverage Optimization

Target 90%+ UV space usage for Final/Hero:

```python
import bpy
import bmesh

def analyze_uv_coverage(obj) -> float:
    """Calculate UV space coverage percentage.

    Args:
        obj: Blender mesh object

    Returns:
        Coverage as fraction (0-1)
    """
    mesh = obj.data
    if not mesh.uv_layers:
        return 0.0

    uv_layer = mesh.uv_layers.active

    # Calculate total UV area
    total_area = 0.0
    for poly in mesh.polygons:
        # Get UV coordinates for this face
        uvs = [uv_layer.data[loop_idx].uv for loop_idx in poly.loop_indices]
        if len(uvs) >= 3:
            # Triangulate and sum area
            for i in range(1, len(uvs) - 1):
                a = uvs[0]
                b = uvs[i]
                c = uvs[i + 1]
                # 2D cross product for triangle area
                area = abs((b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)) / 2
                total_area += area

    print(f"UV Coverage: {total_area * 100:.1f}%")
    return total_area

def pack_uvs_optimized(obj, margin=0.005, rotate=True):
    """Pack UVs efficiently to maximize coverage.

    Args:
        obj: Blender mesh object
        margin: Margin between islands
        rotate: Allow rotation for better packing
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    # Average islands scale for consistency
    bpy.ops.uv.average_islands_scale()

    # Pack with settings
    bpy.ops.uv.pack_islands(margin=margin, rotate=rotate)

    bpy.ops.object.mode_set(mode='OBJECT')
```

### Seam Placement

Hide seams in less visible areas:

```python
import bpy
import bmesh

def mark_uv_seams(obj, edge_indices):
    """Mark edges as UV seams.

    Args:
        obj: Blender mesh object
        edge_indices: List of edge indices to mark as seams
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(obj.data)
    bm.edges.ensure_lookup_table()

    for idx in edge_indices:
        if idx < len(bm.edges):
            bm.edges[idx].seam = True

    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

def smart_unwrap(obj, angle_limit=66.0, island_margin=0.01):
    """Smart UV unwrap with angle-based projection.

    Args:
        obj: Blender mesh object
        angle_limit: Angle limit for projection (degrees)
        island_margin: Margin between UV islands
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.uv.smart_project(
        angle_limit=angle_limit * (3.14159 / 180),
        island_margin=island_margin
    )

    bpy.ops.object.mode_set(mode='OBJECT')
```

### Stretch Reduction

Minimize texture distortion:

```python
import bpy
import bmesh

def identify_high_stretch_faces(obj, threshold=1.5):
    """Find faces with high UV stretch.

    Args:
        obj: Blender mesh object
        threshold: Stretch threshold

    Returns:
        List of face indices with high stretch
    """
    mesh = obj.data
    if not mesh.uv_layers:
        return []

    problem_faces = []
    uv_layer = mesh.uv_layers.active

    for poly in mesh.polygons:
        # Calculate 3D area
        verts = [mesh.vertices[v].co for v in poly.vertices]
        if len(verts) >= 3:
            edge1 = verts[1] - verts[0]
            edge2 = verts[2] - verts[0]
            area_3d = edge1.cross(edge2).length / 2

            # Calculate UV area
            uvs = [uv_layer.data[loop_idx].uv for loop_idx in poly.loop_indices]
            if len(uvs) >= 3:
                uv_area = abs((uvs[1].x - uvs[0].x) * (uvs[2].y - uvs[0].y) -
                             (uvs[2].x - uvs[0].x) * (uvs[1].y - uvs[0].y)) / 2

                if uv_area > 0:
                    stretch = area_3d / uv_area
                    if stretch > threshold:
                        problem_faces.append(poly.index)

    return problem_faces

def relax_uvs_minimize_stretch(obj, iterations=100):
    """Relax UVs to minimize stretch.

    Args:
        obj: Blender mesh object
        iterations: Number of relaxation iterations
    """
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    # Minimize stretch
    bpy.ops.uv.minimize_stretch(iterations=iterations)

    bpy.ops.object.mode_set(mode='OBJECT')
```

---

## Budget Management

### Poly Count by Tier and Asset Type

| Asset Type | Placeholder | Temp | Final | Hero |
|------------|-------------|------|-------|------|
| Swarm entity | 10-30 | 30-80 | 80-150 | 150-300 |
| Small prop | 20-50 | 50-150 | 150-300 | 300-500 |
| Medium prop | 50-100 | 100-300 | 300-500 | 500-800 |
| Large prop | 100-200 | 200-500 | 500-1000 | 1000-1500 |
| Character | 100-200 | 200-400 | 400-800 | 800-2000 |
| Vehicle | 100-300 | 300-600 | 600-1000 | 1000-2000 |

### Staying Within Budget

```python
import bpy
from enum import Enum
from typing import Dict, Tuple

class AssetType(Enum):
    SWARM = 'swarm'
    SMALL_PROP = 'small_prop'
    MEDIUM_PROP = 'medium_prop'
    LARGE_PROP = 'large_prop'
    CHARACTER = 'character'
    VEHICLE = 'vehicle'

class Tier(Enum):
    PLACEHOLDER = 'placeholder'
    TEMP = 'temp'
    FINAL = 'final'
    HERO = 'hero'

# Budget ranges: (min, max) triangles
BUDGETS: Dict[AssetType, Dict[Tier, Tuple[int, int]]] = {
    AssetType.SWARM: {Tier.PLACEHOLDER: (10, 30), Tier.TEMP: (30, 80), Tier.FINAL: (80, 150), Tier.HERO: (150, 300)},
    AssetType.SMALL_PROP: {Tier.PLACEHOLDER: (20, 50), Tier.TEMP: (50, 150), Tier.FINAL: (150, 300), Tier.HERO: (300, 500)},
    AssetType.CHARACTER: {Tier.PLACEHOLDER: (100, 200), Tier.TEMP: (200, 400), Tier.FINAL: (400, 800), Tier.HERO: (800, 2000)},
}

def get_triangle_count(obj) -> int:
    """Get triangle count for mesh object."""
    mesh = obj.data
    return sum(len(poly.vertices) - 2 for poly in mesh.polygons)

def get_budget_for_tier(asset_type: AssetType, tier: Tier) -> int:
    """Get max triangle budget for asset type and tier."""
    return BUDGETS.get(asset_type, {}).get(tier, (0, 1000))[1]

def enforce_budget(obj, asset_type: AssetType, tier: Tier):
    """Decimate mesh if over budget.

    Args:
        obj: Blender mesh object
        asset_type: Type of asset
        tier: Quality tier
    """
    current_tris = get_triangle_count(obj)
    budget = get_budget_for_tier(asset_type, tier)

    if current_tris > budget:
        ratio = budget / current_tris

        # Add decimate modifier
        decimate_mod = obj.modifiers.new(name='BudgetDecimate', type='DECIMATE')
        decimate_mod.ratio = ratio
        decimate_mod.use_collapse_triangulate = True

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier='BudgetDecimate')

        print(f"Decimated from {current_tris} to {get_triangle_count(obj)} triangles")
```

### Strategic Detail Placement

Focus detail where it matters:

```python
import bpy
import bmesh
from mathutils import Vector

def get_visible_faces(obj, camera_direction, angle_threshold=60.0):
    """Find faces visible from typical camera direction.

    Args:
        obj: Blender mesh object
        camera_direction: 3D vector for camera direction
        angle_threshold: Maximum angle from camera to consider visible (degrees)

    Returns:
        List of face indices facing the camera
    """
    mesh = obj.data
    visible = []
    threshold_rad = angle_threshold * (3.14159 / 180)
    cam_dir = Vector(camera_direction).normalized()

    for poly in mesh.polygons:
        # Check if face normal faces camera
        angle = poly.normal.angle(cam_dir)
        if angle < threshold_rad:
            visible.append(poly.index)

    return visible

def subdivide_visible_faces(obj, camera_direction, angle_threshold=60.0, iterations=1):
    """Add detail only to camera-visible faces.

    Args:
        obj: Blender mesh object
        camera_direction: Typical camera direction
        angle_threshold: Visibility angle threshold
        iterations: Subdivision iterations
    """
    visible_faces = get_visible_faces(obj, camera_direction, angle_threshold)

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()

    for idx in visible_faces:
        if idx < len(bm.faces):
            bm.faces[idx].select = True

    bmesh.update_edit_mesh(obj.data)

    # Subdivide selected faces
    bpy.ops.mesh.subdivide(number_cuts=iterations)

    bpy.ops.object.mode_set(mode='OBJECT')
```
