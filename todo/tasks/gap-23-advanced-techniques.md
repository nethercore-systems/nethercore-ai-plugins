# Gap 23: Advanced Techniques & Decision Guides

**Status:** `[ ]` Not Started
**Priority:** MEDIUM
**Plugin:** nethercore-zx-procgen
**Type:** Skill

---

## Problem

PARTIAL coverage. Algorithms exist but lack decision guidance, quality benchmarks, and external library references.

Developers don't know:
1. **Which algorithm to use** for their specific use case
2. **What "good" output looks like** (quality benchmarks)
3. **What external libraries exist** in the Rust/Python/JS ecosystem
4. **Advanced techniques** beyond the basics (domain warping, LSCM, etc.)

## Bone Weight Decision Guide

```
                    What type of mesh?
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
    Primitive          Organic          Mechanical
   (box, sphere)      (character)        (robot)
        │                  │                  │
        ▼                  │                  ▼
    Distance               │              Envelope
     Based                 │            (Volumetric)
   Fast, simple            │             Hard edges
                           │
               ┌───────────┴───────────┐
               ▼                       ▼
           Low-medium               High
             poly?                  poly?
               │                       │
               ▼                       ▼
             Heat                  Geodesic
           Diffusion               Distance
           Good blend            Best quality
```

## Algorithm Characteristics

| Algorithm | Complexity | Quality | Handles Concave | Smooth Transitions |
|-----------|------------|---------|-----------------|-------------------|
| Distance-based | O(n * bones) | 4/10 | No | Yes |
| Envelope | O(n * bones) | 6/10 | Yes | No |
| Heat Diffusion | O(n²) | 8/10 | Yes | Yes |
| Geodesic Distance | O(n² log n) | 10/10 | Yes | Yes |

## Code Examples

### Algorithm Profile Data Structure

```rust
/// Bone weight algorithm comparison
pub struct AlgorithmProfile {
    pub name: &'static str,
    pub complexity: Complexity,       // O(?) per vertex
    pub quality: Quality,             // Subjective 1-10
    pub handles_concave: bool,        // Works with complex geometry
    pub smooth_transitions: bool,     // Gradual weight falloff
    pub respects_topology: bool,      // Follows mesh surface
}

pub const ALGORITHM_PROFILES: &[AlgorithmProfile] = &[
    AlgorithmProfile {
        name: "Distance-based",
        complexity: Complexity::Linear,      // O(n * bones)
        quality: Quality::Basic,             // 4/10
        handles_concave: false,              // Bleeds through thin walls
        smooth_transitions: true,
        respects_topology: false,            // Straight-line distance only
    },
    AlgorithmProfile {
        name: "Envelope (Volumetric)",
        complexity: Complexity::Linear,      // O(n * bones)
        quality: Quality::Good,              // 6/10
        handles_concave: true,               // Respects bone volumes
        smooth_transitions: false,           // Hard cutoffs
        respects_topology: false,
    },
    AlgorithmProfile {
        name: "Heat Diffusion",
        complexity: Complexity::Quadratic,   // O(n²) for heat solve
        quality: Quality::VeryGood,          // 8/10
        handles_concave: true,
        smooth_transitions: true,
        respects_topology: true,             // Follows surface
    },
    AlgorithmProfile {
        name: "Geodesic Distance",
        complexity: Complexity::QuadraticLog, // O(n² log n) Dijkstra
        quality: Quality::Excellent,          // 10/10
        handles_concave: true,
        smooth_transitions: true,
        respects_topology: true,              // True surface distance
    },
];
```

### Bone Weight Quality Validation

```rust
/// Bone weight quality validation
pub struct WeightQualityReport {
    pub candy_wrapper_score: f32,     // 0 = bad, 1 = good
    pub weight_bleeding: Vec<BleedingRegion>,
    pub unweighted_vertices: Vec<usize>,
    pub over_influenced: Vec<usize>,  // Too many bones affecting vertex
    pub stretching_risk: Vec<StretchZone>,
}

/// Detect "candy wrapper" effect (twisting causes mesh collapse)
pub fn detect_candy_wrapper(mesh: &Mesh, weights: &BoneWeights, skeleton: &Skeleton) -> f32 {
    let mut score = 1.0;

    for bone_idx in 0..skeleton.bones.len() {
        // Find vertices primarily influenced by this bone
        let influenced: Vec<_> = mesh.vertices.iter().enumerate()
            .filter(|(i, _)| weights.primary_bone(*i) == bone_idx)
            .collect();

        if influenced.len() < 3 { continue; }

        // Check if influenced region has good "width" perpendicular to bone axis
        let bone_axis = skeleton.bones[bone_idx].direction();
        let perpendicular_spread = calculate_perpendicular_spread(&influenced, bone_axis);

        // Thin regions around joints are candy wrapper risk
        if perpendicular_spread < CANDY_WRAPPER_THRESHOLD {
            score *= 0.8;  // Penalize
        }
    }

    score
}

/// Detect weight bleeding through thin geometry
pub fn detect_weight_bleeding(mesh: &Mesh, weights: &BoneWeights) -> Vec<BleedingRegion> {
    let mut bleeding = vec![];

    // Find edges where weight changes dramatically
    for edge in mesh.edges() {
        let w0 = weights.get(edge.v0);
        let w1 = weights.get(edge.v1);

        let weight_diff = weight_distance(w0, w1);

        // Check if this edge bridges two geometrically close but topologically distant regions
        let geometric_dist = (mesh.vertices[edge.v0] - mesh.vertices[edge.v1]).length();
        let topological_dist = geodesic_distance(mesh, edge.v0, edge.v1);

        // If geometrically close but topologically far, weights shouldn't match
        if geometric_dist < 0.1 && topological_dist > 1.0 && weight_diff < 0.1 {
            bleeding.push(BleedingRegion {
                vertices: vec![edge.v0, edge.v1],
                severity: 1.0 - weight_diff,
            });
        }
    }

    bleeding
}

/// Visual benchmark examples (what to look for)
pub const WEIGHT_BENCHMARKS: &str = r#"
GOOD WEIGHTS:
✓ Smooth gradient at joints (elbow, knee, shoulder)
✓ Weights sum to 1.0 at every vertex
✓ Maximum 4 bone influences per vertex (GPU limit)
✓ No weights "jump" across geometry gaps
✓ Clean deformation at 90° bend

BAD WEIGHTS:
✗ Candy wrapper: Mesh collapses when twisted
✗ Weight bleeding: Arm moves when leg moves (weights bleed through torso)
✗ Unweighted vertices: Parts don't move with skeleton
✗ Over-influenced: More than 4 bones = GPU artifacts
✗ Hard edges: Visible seams between bone regions
"#;
```

### UV Mapping Decision Guide

```
                    What surface geometry?
                           │
    ┌───────────┬──────────┼──────────┬───────────┐
    ▼           ▼          ▼          ▼           ▼
  Flat      Cylinder    Sphere      Box       Complex
 (wall)      (pipe)     (ball)    (crate)   (organic)
    │           │          │          │           │
    ▼           ▼          ▼          ▼           ▼
 Planar    Cylinder   Spherical    Box       LSCM/
Projection Projection Projection Projection  ABF++
```

### UV Projection Comparison

| Projection | Best For | Distortion Type | Seams |
|------------|----------|-----------------|-------|
| Planar | Flat surfaces, decals | Stretching at edges | None or 1 |
| Cylindrical | Tubes, limbs, barrels | Poles at caps | 1 vertical |
| Spherical | Balls, planets, heads | Severe pole pinching | 1 vertical |
| Box/Cubic | Crates, buildings | Hard edges at cube faces | 6 edges |
| LSCM | Organic, any shape | Minimal angle distortion | Auto-detected |
| ABF++ | Hard-surface, CAD | Angle preservation | Auto-detected |

### LSCM Unwrapping Algorithm

```rust
/// LSCM (Least Squares Conformal Maps)
/// Minimizes angle distortion, good for organic shapes
pub fn lscm_unwrap(mesh: &Mesh, boundary_vertices: &[usize]) -> Vec<[f32; 2]> {
    // 1. Pin two boundary vertices (prevents rotation/scale ambiguity)
    let pin0 = boundary_vertices[0];
    let pin1 = boundary_vertices[boundary_vertices.len() / 2];

    // 2. Build conformal energy matrix (preserves angles)
    let mut matrix = SparseMatrix::new(mesh.vertices.len() * 2, mesh.vertices.len() * 2);

    for tri in mesh.triangles() {
        // Add conformal energy terms for this triangle
        add_conformal_terms(&mut matrix, mesh, tri);
    }

    // 3. Add pin constraints
    matrix.set_row_to_identity(pin0 * 2);      // u0 = 0
    matrix.set_row_to_identity(pin0 * 2 + 1);  // v0 = 0
    matrix.set_row_to_identity(pin1 * 2);      // u1 = 1
    matrix.set_row_to_identity(pin1 * 2 + 1);  // v1 = 0

    // 4. Solve least squares system
    let solution = matrix.solve_least_squares();

    // 5. Extract UV coordinates
    (0..mesh.vertices.len())
        .map(|i| [solution[i * 2], solution[i * 2 + 1]])
        .collect()
}

/// Automatic seam detection for UV unwrapping
pub fn detect_seams(mesh: &Mesh) -> Vec<Edge> {
    let mut seam_edges = vec![];

    // Seam heuristics:
    // 1. High curvature edges (sharp corners)
    // 2. Edges hidden from common view angles
    // 3. Edges that minimize texture distortion when cut

    for edge in mesh.edges() {
        let curvature = edge_curvature(mesh, edge);
        let visibility = edge_visibility_score(mesh, edge);
        let distortion_reduction = distortion_if_cut(mesh, edge);

        let seam_score = curvature * 0.4 + (1.0 - visibility) * 0.3 + distortion_reduction * 0.3;

        if seam_score > SEAM_THRESHOLD {
            seam_edges.push(edge);
        }
    }

    // Ensure seams form connected paths (no dangling cuts)
    connect_seam_paths(seam_edges)
}

/// UV island packing (fit islands efficiently in 0-1 UV space)
pub fn pack_uv_islands(islands: &mut [UvIsland], padding: f32) -> f32 {
    // Sort islands by area (largest first for better packing)
    islands.sort_by(|a, b| b.area().partial_cmp(&a.area()).unwrap());

    // Use guillotine bin packing algorithm
    let mut packer = GuillotinePacker::new(1.0, 1.0);

    for island in islands.iter_mut() {
        let (width, height) = island.bounding_size();

        if let Some((x, y)) = packer.pack(width + padding, height + padding) {
            island.translate(x + padding / 2.0, y + padding / 2.0);
        }
    }

    packer.utilization()  // Returns 0.0-1.0 efficiency
}
```

## What's Missing

- Bone weight algorithm decision matrix
- UV mapping technique comparison (box, cylinder, sphere, LSCM)
- Noise function selection guide
- External library references per algorithm
- Quality benchmarks with numerical thresholds

## Prompt for Implementation

```
Add skill "advanced-techniques" to nethercore-zx-procgen OR expand existing skills.
Triggers: "which algorithm", "decision guide", "bone weight algorithm", "UV mapping
technique", "when to use", "algorithm comparison", "quality benchmark".

Cover:
1. Bone weight algorithms: decision flowchart, algorithm comparison table, quality
   benchmarks (max error, weight sum validation)
2. UV mapping: box vs cylinder vs sphere vs LSCM, decision criteria
3. Noise functions: when to use Perlin vs Simplex vs Worley vs FBM
4. External libraries: Rust (gltf, mint, glam), Python (trimesh, numpy), etc.
5. Quality benchmarks: numerical thresholds for "good" output

Include decision flowcharts as ASCII diagrams. ~1500 words.
```

## Dependencies

- None

## Related Gaps

- Enhances all procgen skills with decision guidance
