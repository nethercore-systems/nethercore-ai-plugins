# Mesh Enhancement Techniques

Detailed techniques for upgrading mesh quality through the tier system.

## Placeholder → Temp Upgrades

### Add Proper UV Mapping

Placeholder meshes often lack UVs. Apply appropriate projection:

```rust
// Box projection for architectural/cubic shapes
mesh.apply(UVProject::Box { scale: 1.0 });

// Cylindrical for rounded objects
mesh.apply(UVProject::Cylindrical { axis: Axis::Y });

// Spherical for organic shapes
mesh.apply(UVProject::Spherical { center: Vec3::ZERO });
```

### Calculate Normals

Ensure normals are present and correct:

```rust
// For faceted/low-poly look
mesh.apply(FlatNormals);

// For smooth appearance
mesh.apply(SmoothNormals { angle_threshold: 30.0 });
```

### Clean Geometry

Remove degenerate triangles and fix topology:

```rust
// Remove zero-area triangles
mesh.apply(RemoveDegenerates { epsilon: 1e-6 });

// Merge close vertices
mesh.apply(MergeClose { distance: 0.001 });

// Ensure consistent winding
mesh.apply(FixWinding);
```

### Basic Shape Improvement

Transform primitives into proper game assets:

```rust
// Add some variation to flat surfaces
mesh.apply(Noise {
    amplitude: 0.02,
    frequency: 4.0,
    axis: None,  // All axes
});

// Round sharp corners slightly
mesh.apply(Subdivide { iterations: 1 });
mesh.apply(Relax { iterations: 2, factor: 0.3 });
```

---

## Temp → Final Upgrades

### Add Bevels

Bevels catch light and improve visual quality significantly:

```rust
// Bevel all hard edges
mesh.apply(Bevel {
    width: 0.02,
    segments: 1,
    angle_threshold: 30.0,
});

// Selective beveling for important edges
mesh.apply(BevelEdges {
    edges: &important_edge_indices,
    width: 0.03,
    segments: 2,
});
```

### Improve Silhouette

Silhouette clarity is critical for game readability:

```rust
// Add distinctive features
mesh.apply(Extrude {
    faces: &top_faces,
    distance: 0.1,
    scale: 0.9,
});

// Create recesses for visual interest
mesh.apply(Inset {
    faces: &side_faces,
    distance: 0.05,
});
mesh.apply(Extrude {
    faces: &inset_faces,
    distance: -0.03,
    scale: 1.0,
});
```

### Optimize Topology

Clean up topology while maintaining quality:

```rust
// Remove unnecessary subdivision on flat areas
mesh.apply(Decimate {
    target_ratio: 0.7,
    preserve_boundaries: true,
    preserve_uv_seams: true,
});

// Retriangulate for better performance
mesh.apply(Triangulate { method: TriMethod::Beauty });
```

### Enhance UV Layout

Improve texture space utilization:

```rust
// Maximize UV coverage
mesh.apply(PackUVs {
    margin: 0.01,
    rotate: true,
});

// Reduce stretch
mesh.apply(RelaxUVs {
    iterations: 50,
    method: RelaxMethod::Angle,
});
```

### Add Secondary Details

Include supporting shapes:

```rust
// Add bolts/rivets to metal objects
for position in bolt_positions {
    let bolt = generate_bolt(0.02, 0.01);
    mesh.merge(&bolt.translated(position));
}

// Add edge wear/damage
mesh.apply(EdgeWear {
    amount: 0.3,
    noise_scale: 2.0,
});
```

---

## Final → Hero Upgrades

### Add Edge Loops

Strategic edge loops for better deformation and detail:

```rust
// Add edge loop near important features
mesh.apply(InsertEdgeLoop {
    edge_ring: &feature_edges,
    offset: 0.1,
});

// Support loops for subdivision
mesh.apply(AddSupportLoops {
    edges: &hard_edges,
    distance: 0.02,
});
```

### Micro-Detail Addition

Fine details visible on close inspection:

```rust
// Surface imperfections
mesh.apply(SurfaceNoise {
    scale: 20.0,
    amplitude: 0.002,
    octaves: 3,
});

// Wear patterns on edges
mesh.apply(EdgeChipping {
    probability: 0.3,
    depth: 0.005,
    width: 0.01,
});

// Panel lines for mechanical objects
mesh.apply(PanelLines {
    width: 0.001,
    depth: 0.002,
    pattern: PanelPattern::Grid { size: 0.2 },
});
```

### Secondary Shapes

Add smaller supporting elements:

```rust
// Screws, bolts, rivets
mesh.merge(&generate_hardware(HardwareType::Bolt, positions));

// Cables, wires
mesh.merge(&generate_cable(start, end, sag: 0.1, radius: 0.005));

// Handles, grips
mesh.merge(&generate_handle(HandleStyle::Industrial, transform));
```

### Perfect Topology

Ensure optimal topology for all use cases:

```rust
// Quadrangulate for subdivision/animation
mesh.apply(Quadrangulate {
    preserve_boundaries: true,
    max_valence: 6,
});

// Ensure good edge flow
mesh.apply(OptimizeEdgeFlow {
    iterations: 20,
    target_valence: 4,
});
```

### Vertex Color Enhancement

Add vertex colors for variation:

```rust
// Ambient occlusion bake
mesh.apply(BakeAO {
    samples: 64,
    distance: 0.5,
});

// Color variation
mesh.apply(VertexColorVariation {
    hue_range: 0.05,
    saturation_range: 0.1,
    value_range: 0.15,
    scale: 2.0,
});

// Wear/dirt accumulation
mesh.apply(VertexColorWear {
    cavity_darkening: 0.2,
    edge_lightening: 0.1,
});
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

```rust
// Exaggerate key features
mesh.apply(ScaleFeatures {
    feature_type: FeatureType::Protrusions,
    scale: 1.2,
});

// Add distinctive elements
mesh.apply(AddSilhouetteBreakers {
    frequency: 3,
    size_range: (0.1, 0.2),
    placement: Placement::Edges,
});
```

---

## UV Enhancement Techniques

### Coverage Optimization

Target 90%+ UV space usage for Final/Hero:

```rust
// Analyze current coverage
let coverage = mesh.uv_coverage();
println!("UV Coverage: {:.1}%", coverage * 100.0);

// Pack efficiently
mesh.apply(PackUVs {
    margin: 0.005,
    rotate: true,
    scale_to_fit: true,
});
```

### Seam Placement

Hide seams in less visible areas:

```rust
// Mark preferred seam locations
mesh.apply(MarkUVSeams {
    edges: find_hidden_edges(&mesh),
    priority: SeamPriority::High,
});

// Unwrap with seam preferences
mesh.apply(SmartUnwrap {
    angle_limit: 66.0,
    island_margin: 0.01,
    respect_seams: true,
});
```

### Stretch Reduction

Minimize texture distortion:

```rust
// Identify high-stretch areas
let stretch_map = mesh.calculate_stretch();
let problem_faces = stretch_map.iter()
    .filter(|(_, stretch)| *stretch > 1.5)
    .map(|(face, _)| *face)
    .collect();

// Add seams to reduce stretch
mesh.apply(AddSeamsForStretch {
    max_stretch: 1.3,
    max_seams: 5,
});

// Relax UVs
mesh.apply(RelaxUVs {
    iterations: 100,
    method: RelaxMethod::ABF,
});
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

```rust
// Check budget before operations
let current_tris = mesh.triangle_count();
let budget = get_budget_for_tier(asset_type, target_tier);

if current_tris > budget {
    // Decimate to budget
    mesh.apply(Decimate {
        target_count: budget,
        preserve_boundaries: true,
        preserve_uv_seams: true,
    });
}
```

### Strategic Detail Placement

Focus detail where it matters:

```rust
// Identify visible faces (facing camera in typical gameplay)
let visible_faces = mesh.faces_facing(typical_camera_direction, 60.0);

// Add detail only to visible areas
mesh.apply(SubdivideSelective {
    faces: &visible_faces,
    iterations: 1,
});
```
