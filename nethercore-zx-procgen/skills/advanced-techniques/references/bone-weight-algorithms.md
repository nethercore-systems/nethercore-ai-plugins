# Bone Weight Algorithm Reference

Detailed implementations and quality validation for procedural bone weight generation.

## Algorithm Profiles

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

---

## Distance-Based Weighting

Simplest approach: weight = 1 / distance_to_bone. Fast but bleeds through geometry.

### Implementation

```rust
fn distance_based_weights(
    vertex_pos: Vec3,
    bones: &[Bone],
    max_influences: usize,
) -> (Vec<u8>, Vec<f32>) {
    let mut weights: Vec<(usize, f32)> = bones.iter()
        .enumerate()
        .map(|(i, bone)| {
            // Distance from vertex to bone line segment
            let dist = point_to_segment_distance(vertex_pos, bone.head, bone.tail);
            let weight = 1.0 / (dist + 0.001);  // Avoid division by zero
            (i, weight)
        })
        .collect();

    // Sort by weight descending, take top N
    weights.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    weights.truncate(max_influences);

    // Normalize to sum = 1.0
    let sum: f32 = weights.iter().map(|(_, w)| w).sum();
    let indices: Vec<u8> = weights.iter().map(|(i, _)| *i as u8).collect();
    let normalized: Vec<f32> = weights.iter().map(|(_, w)| w / sum).collect();

    (indices, normalized)
}

fn point_to_segment_distance(p: Vec3, a: Vec3, b: Vec3) -> f32 {
    let ab = b - a;
    let ap = p - a;
    let t = (ap.dot(ab) / ab.dot(ab)).clamp(0.0, 1.0);
    let closest = a + ab * t;
    (p - closest).length()
}
```

### When to Use
- Primitives (boxes, spheres, cylinders)
- Quick prototyping
- When speed matters more than quality

### Limitations
- Weights bleed through thin geometry
- No awareness of mesh topology
- Can produce artifacts on concave meshes

---

## Envelope (Volumetric) Weighting

Uses bone capsules/ellipsoids to define influence regions. Hard edges but respects volumes.

### Implementation

```rust
struct BoneEnvelope {
    bone_idx: usize,
    head: Vec3,
    tail: Vec3,
    head_radius: f32,
    tail_radius: f32,
}

fn envelope_weights(
    vertex_pos: Vec3,
    envelopes: &[BoneEnvelope],
    max_influences: usize,
) -> (Vec<u8>, Vec<f32>) {
    let mut weights: Vec<(usize, f32)> = vec![];

    for env in envelopes {
        // Find closest point on bone axis
        let bone_vec = env.tail - env.head;
        let t = ((vertex_pos - env.head).dot(bone_vec) / bone_vec.dot(bone_vec))
            .clamp(0.0, 1.0);
        let closest = env.head + bone_vec * t;

        // Interpolate radius
        let radius = env.head_radius * (1.0 - t) + env.tail_radius * t;

        // Distance from envelope surface
        let dist_to_axis = (vertex_pos - closest).length();
        let dist_to_surface = dist_to_axis - radius;

        // Weight: 1.0 inside envelope, falloff outside
        let weight = if dist_to_surface <= 0.0 {
            1.0
        } else {
            (1.0 - dist_to_surface / (radius * 0.5)).max(0.0)
        };

        if weight > 0.0 {
            weights.push((env.bone_idx, weight));
        }
    }

    normalize_weights(weights, max_influences)
}
```

### When to Use
- Mechanical/robotic characters
- Hard-surface models
- When sharp transitions are desired

### Tuning
- Adjust envelope radii per bone
- Larger radius = more influence area
- Overlapping envelopes create blending regions

---

## Heat Diffusion Weighting

Simulates heat flow from bones through mesh surface. Topology-aware, smooth results.

### Concept

1. Set heat sources at bone positions (temperature = 1.0)
2. Solve heat equation on mesh surface
3. Weight = normalized heat value per bone

### Implementation

```rust
fn heat_diffusion_weights(
    mesh: &Mesh,
    bones: &[Bone],
    iterations: usize,
) -> Vec<Vec<f32>> {
    let n = mesh.vertices.len();
    let bone_count = bones.len();

    // Initialize: heat[bone][vertex]
    let mut heat: Vec<Vec<f32>> = vec![vec![0.0; n]; bone_count];

    // Set heat sources
    for (bone_idx, bone) in bones.iter().enumerate() {
        for (v_idx, pos) in mesh.vertices.iter().enumerate() {
            let dist = point_to_segment_distance(*pos, bone.head, bone.tail);
            if dist < 0.1 {  // Close to bone
                heat[bone_idx][v_idx] = 1.0;
            }
        }
    }

    // Build adjacency and Laplacian
    let adj = mesh.build_adjacency();
    let laplacian = build_cotangent_laplacian(mesh);

    // Iterative heat diffusion
    for _ in 0..iterations {
        for bone_idx in 0..bone_count {
            let mut new_heat = vec![0.0; n];

            for v in 0..n {
                // Heat diffuses to neighbors
                let mut sum = 0.0;
                let mut weight_sum = 0.0;

                for &neighbor in &adj[v] {
                    let edge_weight = laplacian[(v, neighbor)];
                    sum += heat[bone_idx][neighbor] * edge_weight;
                    weight_sum += edge_weight;
                }

                new_heat[v] = heat[bone_idx][v] * 0.5 + (sum / weight_sum) * 0.5;
            }

            // Keep heat sources hot
            for (v_idx, pos) in mesh.vertices.iter().enumerate() {
                let dist = point_to_segment_distance(*pos, bones[bone_idx].head, bones[bone_idx].tail);
                if dist < 0.1 {
                    new_heat[v_idx] = 1.0;
                }
            }

            heat[bone_idx] = new_heat;
        }
    }

    // Normalize per vertex
    for v in 0..n {
        let sum: f32 = (0..bone_count).map(|b| heat[b][v]).sum();
        if sum > 0.0 {
            for b in 0..bone_count {
                heat[b][v] /= sum;
            }
        }
    }

    heat
}
```

### When to Use
- Organic characters
- Creatures
- Any mesh where smooth blending matters

### Parameters
- `iterations`: More = smoother (50-200 typical)
- Heat source size: Larger = more spread

---

## Geodesic Distance Weighting

Computes true surface distance using Dijkstra's algorithm. Highest quality, most expensive.

### Implementation

```rust
fn geodesic_weights(
    mesh: &Mesh,
    bones: &[Bone],
    max_influences: usize,
) -> Vec<(Vec<u8>, Vec<f32>)> {
    let n = mesh.vertices.len();
    let bone_count = bones.len();

    // Compute geodesic distance from each bone to all vertices
    let mut geo_dist: Vec<Vec<f32>> = vec![vec![f32::MAX; n]; bone_count];

    for (bone_idx, bone) in bones.iter().enumerate() {
        // Find vertices on bone
        let mut sources = vec![];
        for (v_idx, pos) in mesh.vertices.iter().enumerate() {
            let dist = point_to_segment_distance(*pos, bone.head, bone.tail);
            if dist < 0.1 {
                sources.push(v_idx);
            }
        }

        // Dijkstra from sources
        geo_dist[bone_idx] = dijkstra_multi_source(mesh, &sources);
    }

    // Convert distances to weights
    let mut result = vec![];
    for v in 0..n {
        let mut weights: Vec<(usize, f32)> = (0..bone_count)
            .filter(|&b| geo_dist[b][v] < f32::MAX)
            .map(|b| (b, 1.0 / (geo_dist[b][v] + 0.001)))
            .collect();

        weights.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        weights.truncate(max_influences);

        let sum: f32 = weights.iter().map(|(_, w)| w).sum();
        let indices: Vec<u8> = weights.iter().map(|(i, _)| *i as u8).collect();
        let normalized: Vec<f32> = weights.iter().map(|(_, w)| w / sum).collect();

        result.push((indices, normalized));
    }

    result
}

fn dijkstra_multi_source(mesh: &Mesh, sources: &[usize]) -> Vec<f32> {
    let n = mesh.vertices.len();
    let mut dist = vec![f32::MAX; n];
    let mut heap = BinaryHeap::new();

    for &s in sources {
        dist[s] = 0.0;
        heap.push(Reverse((OrderedFloat(0.0), s)));
    }

    let adj = mesh.build_edge_adjacency();

    while let Some(Reverse((OrderedFloat(d), u))) = heap.pop() {
        if d > dist[u] {
            continue;
        }

        for &(v, edge_len) in &adj[u] {
            let new_dist = d + edge_len;
            if new_dist < dist[v] {
                dist[v] = new_dist;
                heap.push(Reverse((OrderedFloat(new_dist), v)));
            }
        }
    }

    dist
}
```

### When to Use
- Hero characters
- Close-up deformations
- When quality is paramount

### Optimization
- Precompute for static skeletons
- Use spatial acceleration (octree) for large meshes
- Consider hybrid: geodesic for key vertices, interpolate rest

---

## Quality Validation

### Weight Quality Report

```rust
pub struct WeightQualityReport {
    pub sum_deviation: f32,           // Max deviation from 1.0
    pub candy_wrapper_score: f32,     // 0 = bad, 1 = good
    pub weight_bleeding: Vec<BleedingRegion>,
    pub unweighted_vertices: Vec<usize>,
    pub over_influenced: Vec<usize>,  // >4 bones per vertex
}
```

### Sum Validation

```rust
fn validate_weight_sums(weights: &BoneWeights) -> (f32, Vec<usize>) {
    let mut max_deviation = 0.0;
    let mut bad_vertices = vec![];

    for v in 0..weights.vertex_count() {
        let sum: f32 = weights.get_weights(v).iter().sum();
        let deviation = (sum - 1.0).abs();

        max_deviation = max_deviation.max(deviation);

        if deviation > 0.01 {
            bad_vertices.push(v);
        }
    }

    (max_deviation, bad_vertices)
}
```

### Candy Wrapper Detection

Detects mesh collapse when twisted (thin regions at joints).

```rust
fn detect_candy_wrapper(mesh: &Mesh, weights: &BoneWeights, skeleton: &Skeleton) -> f32 {
    let mut score = 1.0;

    for bone_idx in 0..skeleton.bones.len() {
        // Find vertices primarily influenced by this bone
        let influenced: Vec<_> = mesh.vertices.iter().enumerate()
            .filter(|(i, _)| weights.primary_bone(*i) == bone_idx)
            .collect();

        if influenced.len() < 3 {
            continue;
        }

        // Check perpendicular spread around bone axis
        let bone_axis = skeleton.bones[bone_idx].direction();
        let perpendicular_spread = calculate_perpendicular_spread(&influenced, bone_axis);

        // Thin regions at joints = candy wrapper risk
        const CANDY_WRAPPER_THRESHOLD: f32 = 0.1;
        if perpendicular_spread < CANDY_WRAPPER_THRESHOLD {
            score *= 0.8;  // Penalize
        }
    }

    score
}
```

### Weight Bleeding Detection

Detects weights that cross geometry gaps.

```rust
fn detect_weight_bleeding(mesh: &Mesh, weights: &BoneWeights) -> Vec<BleedingRegion> {
    let mut bleeding = vec![];

    for edge in mesh.edges() {
        let w0 = weights.get(edge.v0);
        let w1 = weights.get(edge.v1);

        let weight_diff = weight_distance(w0, w1);
        let geometric_dist = (mesh.vertices[edge.v0] - mesh.vertices[edge.v1]).length();
        let topological_dist = geodesic_distance(mesh, edge.v0, edge.v1);

        // Geometrically close but topologically far = potential bleed
        if geometric_dist < 0.1 && topological_dist > 1.0 && weight_diff < 0.1 {
            bleeding.push(BleedingRegion {
                vertices: vec![edge.v0, edge.v1],
                severity: 1.0 - weight_diff,
            });
        }
    }

    bleeding
}
```

---

## Visual Quality Checklist

```
GOOD WEIGHTS:
+ Smooth gradient at joints (elbow, knee, shoulder)
+ Weights sum to 1.0 at every vertex
+ Maximum 4 bone influences per vertex (GPU limit)
+ No weights "jump" across geometry gaps
+ Clean deformation at 90 deg bend

BAD WEIGHTS:
- Candy wrapper: Mesh collapses when twisted
- Weight bleeding: Arm moves when leg moves
- Unweighted vertices: Parts don't move with skeleton
- Over-influenced: More than 4 bones = GPU artifacts
- Hard edges: Visible seams between bone regions
```
