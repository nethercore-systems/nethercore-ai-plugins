# Procedural Bone Weight Generation

Algorithms for automatically calculating bone weights for procedurally generated meshes.

## Overview

Bone weights determine how much each bone influences each vertex during skeletal deformation. For procedural meshes, calculate weights algorithmically rather than painting manually.

## Weight Constraints

1. **Sum to 1.0**: All weights for a vertex must sum to 1.0
2. **Max 4 influences**: ZX supports up to 4 bones per vertex
3. **Non-negative**: All weights must be >= 0

## Distance-Based Weighting

Simplest approach: weight inversely proportional to distance from bone.

### Basic Implementation

```rust
use glam::Vec3;

struct Bone {
    position: Vec3,      // World-space position
    head: Vec3,          // Joint start
    tail: Vec3,          // Joint end
    radius: f32,         // Influence radius
}

fn calculate_bone_weights(
    vertex: Vec3,
    bones: &[Bone],
    max_influences: usize,
) -> ([u8; 4], [f32; 4]) {
    let mut influences: Vec<(usize, f32)> = Vec::new();

    for (idx, bone) in bones.iter().enumerate() {
        // Distance to bone segment
        let dist = point_to_segment_distance(vertex, bone.head, bone.tail);

        if dist < bone.radius {
            // Inverse distance with falloff
            let weight = 1.0 - (dist / bone.radius);
            influences.push((idx, weight));
        }
    }

    // Sort by weight (highest first)
    influences.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    influences.truncate(max_influences);

    // Normalize weights
    let sum: f32 = influences.iter().map(|(_, w)| w).sum();

    let mut indices = [0u8; 4];
    let mut weights = [0.0f32; 4];

    for (i, (idx, w)) in influences.iter().enumerate() {
        indices[i] = *idx as u8;
        weights[i] = if sum > 0.0 { w / sum } else { 0.0 };
    }

    (indices, weights)
}

fn point_to_segment_distance(p: Vec3, a: Vec3, b: Vec3) -> f32 {
    let ab = b - a;
    let ap = p - a;
    let t = (ap.dot(ab) / ab.length_squared()).clamp(0.0, 1.0);
    let closest = a + ab * t;
    (p - closest).length()
}
```

### Envelope-Based Weighting

Use capsule envelopes around bones for more control:

```rust
struct BoneEnvelope {
    head_radius: f32,
    tail_radius: f32,
    falloff: f32,  // 0-1, how quickly weight falls off
}

fn envelope_weight(
    vertex: Vec3,
    bone: &Bone,
    envelope: &BoneEnvelope,
) -> f32 {
    let ab = bone.tail - bone.head;
    let ap = vertex - bone.head;
    let t = (ap.dot(ab) / ab.length_squared()).clamp(0.0, 1.0);

    // Interpolate radius along bone
    let radius = envelope.head_radius * (1.0 - t) + envelope.tail_radius * t;

    // Distance to bone axis
    let closest = bone.head + ab * t;
    let dist = (vertex - closest).length();

    if dist > radius {
        return 0.0;
    }

    // Smooth falloff
    let normalized = dist / radius;
    let weight = 1.0 - normalized.powf(1.0 / envelope.falloff);
    weight.max(0.0)
}
```

## Heat Diffusion Method

More sophisticated approach using mesh connectivity for organic shapes.

### Algorithm

1. Set bone positions as "heat sources" (value = 1.0)
2. Diffuse heat through mesh edges
3. Final heat values become weights

```rust
use std::collections::HashMap;

struct Mesh {
    vertices: Vec<Vec3>,
    edges: Vec<(usize, usize)>,
}

fn heat_diffusion_weights(
    mesh: &Mesh,
    bones: &[Bone],
    iterations: usize,
) -> Vec<([u8; 4], [f32; 4])> {
    let vertex_count = mesh.vertices.len();
    let bone_count = bones.len();

    // Initialize heat per bone per vertex
    let mut heat: Vec<Vec<f32>> = vec![vec![0.0; vertex_count]; bone_count];

    // Set initial heat at bone positions
    for (bone_idx, bone) in bones.iter().enumerate() {
        // Find nearest vertex to bone
        let nearest = find_nearest_vertex(&mesh.vertices, bone.position);
        heat[bone_idx][nearest] = 1.0;
    }

    // Build adjacency for diffusion
    let mut neighbors: Vec<Vec<usize>> = vec![Vec::new(); vertex_count];
    for &(a, b) in &mesh.edges {
        neighbors[a].push(b);
        neighbors[b].push(a);
    }

    // Diffuse heat
    for _ in 0..iterations {
        let mut new_heat = heat.clone();

        for bone_idx in 0..bone_count {
            for v in 0..vertex_count {
                if neighbors[v].is_empty() {
                    continue;
                }

                let neighbor_avg: f32 = neighbors[v].iter()
                    .map(|&n| heat[bone_idx][n])
                    .sum::<f32>() / neighbors[v].len() as f32;

                // Blend current with neighbor average
                new_heat[bone_idx][v] = heat[bone_idx][v] * 0.5 + neighbor_avg * 0.5;
            }
        }

        heat = new_heat;
    }

    // Convert heat to weights
    let mut result = Vec::with_capacity(vertex_count);

    for v in 0..vertex_count {
        let mut bone_heats: Vec<(usize, f32)> = (0..bone_count)
            .map(|b| (b, heat[b][v]))
            .filter(|(_, h)| *h > 0.001)
            .collect();

        bone_heats.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        bone_heats.truncate(4);

        let sum: f32 = bone_heats.iter().map(|(_, h)| h).sum();

        let mut indices = [0u8; 4];
        let mut weights = [0.0f32; 4];

        for (i, (idx, h)) in bone_heats.iter().enumerate() {
            indices[i] = *idx as u8;
            weights[i] = if sum > 0.0 { h / sum } else { 0.0 };
        }

        result.push((indices, weights));
    }

    result
}

fn find_nearest_vertex(vertices: &[Vec3], target: Vec3) -> usize {
    vertices.iter()
        .enumerate()
        .min_by(|(_, a), (_, b)| {
            let da = (*a - target).length_squared();
            let db = (*b - target).length_squared();
            da.partial_cmp(&db).unwrap()
        })
        .map(|(i, _)| i)
        .unwrap_or(0)
}
```

## Geodesic Distance Weighting

Use mesh surface distance rather than straight-line distance:

```rust
use std::collections::BinaryHeap;
use std::cmp::Ordering;

#[derive(Clone)]
struct DistEntry {
    vertex: usize,
    distance: f32,
}

impl Ord for DistEntry {
    fn cmp(&self, other: &Self) -> Ordering {
        other.distance.partial_cmp(&self.distance).unwrap_or(Ordering::Equal)
    }
}

impl PartialOrd for DistEntry {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl PartialEq for DistEntry {
    fn eq(&self, other: &Self) -> bool {
        self.distance == other.distance
    }
}

impl Eq for DistEntry {}

fn geodesic_distances(
    mesh: &Mesh,
    start_vertex: usize,
) -> Vec<f32> {
    let n = mesh.vertices.len();
    let mut distances = vec![f32::INFINITY; n];
    distances[start_vertex] = 0.0;

    let mut heap = BinaryHeap::new();
    heap.push(DistEntry { vertex: start_vertex, distance: 0.0 });

    // Build adjacency with edge lengths
    let mut adj: Vec<Vec<(usize, f32)>> = vec![Vec::new(); n];
    for &(a, b) in &mesh.edges {
        let len = (mesh.vertices[a] - mesh.vertices[b]).length();
        adj[a].push((b, len));
        adj[b].push((a, len));
    }

    // Dijkstra's algorithm
    while let Some(DistEntry { vertex, distance }) = heap.pop() {
        if distance > distances[vertex] {
            continue;
        }

        for &(neighbor, edge_len) in &adj[vertex] {
            let new_dist = distance + edge_len;
            if new_dist < distances[neighbor] {
                distances[neighbor] = new_dist;
                heap.push(DistEntry { vertex: neighbor, distance: new_dist });
            }
        }
    }

    distances
}

fn geodesic_bone_weights(
    mesh: &Mesh,
    bones: &[Bone],
) -> Vec<([u8; 4], [f32; 4])> {
    // Find nearest vertex to each bone
    let bone_vertices: Vec<usize> = bones.iter()
        .map(|b| find_nearest_vertex(&mesh.vertices, b.position))
        .collect();

    // Calculate geodesic distances from each bone
    let all_distances: Vec<Vec<f32>> = bone_vertices.iter()
        .map(|&start| geodesic_distances(mesh, start))
        .collect();

    // Convert to weights
    let mut result = Vec::with_capacity(mesh.vertices.len());

    for v in 0..mesh.vertices.len() {
        let mut bone_weights: Vec<(usize, f32)> = all_distances.iter()
            .enumerate()
            .map(|(b, distances)| {
                let d = distances[v];
                let w = if d < 0.001 { 1000.0 } else { 1.0 / d };
                (b, w)
            })
            .collect();

        bone_weights.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        bone_weights.truncate(4);

        let sum: f32 = bone_weights.iter().map(|(_, w)| w).sum();

        let mut indices = [0u8; 4];
        let mut weights = [0.0f32; 4];

        for (i, (idx, w)) in bone_weights.iter().enumerate() {
            indices[i] = *idx as u8;
            weights[i] = w / sum;
        }

        result.push((indices, weights));
    }

    result
}
```

## Volumetric Weighting

For characters with clear body segments:

```rust
struct BodySegment {
    bone_index: usize,
    min_y: f32,
    max_y: f32,
    falloff_zones: (f32, f32),  // (bottom blend, top blend)
}

fn volumetric_weights(
    vertex: Vec3,
    segments: &[BodySegment],
) -> ([u8; 4], [f32; 4]) {
    let y = vertex.y;

    let mut weights: Vec<(usize, f32)> = segments.iter()
        .filter_map(|seg| {
            if y < seg.min_y - seg.falloff_zones.0 ||
               y > seg.max_y + seg.falloff_zones.1 {
                return None;
            }

            let weight = if y < seg.min_y {
                // Bottom falloff zone
                1.0 - (seg.min_y - y) / seg.falloff_zones.0
            } else if y > seg.max_y {
                // Top falloff zone
                1.0 - (y - seg.max_y) / seg.falloff_zones.1
            } else {
                // Full influence
                1.0
            };

            Some((seg.bone_index, weight.max(0.0)))
        })
        .collect();

    normalize_to_4(&mut weights)
}

fn normalize_to_4(weights: &mut Vec<(usize, f32)>) -> ([u8; 4], [f32; 4]) {
    weights.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    weights.truncate(4);

    let sum: f32 = weights.iter().map(|(_, w)| w).sum();

    let mut indices = [0u8; 4];
    let mut out_weights = [0.0f32; 4];

    for (i, (idx, w)) in weights.iter().enumerate() {
        indices[i] = *idx as u8;
        out_weights[i] = if sum > 0.0 { w / sum } else { 0.0 };
    }

    (indices, out_weights)
}
```

## Python Implementation

Using numpy for efficient batch processing:

```python
import numpy as np
from scipy.spatial import cKDTree

def calculate_bone_weights_batch(
    vertices: np.ndarray,  # (N, 3)
    bone_positions: np.ndarray,  # (B, 3)
    bone_radii: np.ndarray,  # (B,)
    max_influences: int = 4
) -> tuple[np.ndarray, np.ndarray]:
    """
    Calculate bone weights for all vertices at once.

    Returns:
        indices: (N, 4) uint8 - bone indices
        weights: (N, 4) float32 - bone weights
    """
    n_vertices = len(vertices)
    n_bones = len(bone_positions)

    # Calculate all pairwise distances
    # Shape: (N, B)
    dists = np.linalg.norm(
        vertices[:, np.newaxis, :] - bone_positions[np.newaxis, :, :],
        axis=2
    )

    # Calculate raw weights (inverse distance with radius falloff)
    raw_weights = np.maximum(0, 1 - dists / bone_radii[np.newaxis, :])

    # Get top-k influences per vertex
    indices = np.zeros((n_vertices, max_influences), dtype=np.uint8)
    weights = np.zeros((n_vertices, max_influences), dtype=np.float32)

    for v in range(n_vertices):
        # Sort by weight descending
        sorted_idx = np.argsort(-raw_weights[v])[:max_influences]
        sorted_weights = raw_weights[v, sorted_idx]

        # Normalize
        weight_sum = sorted_weights.sum()
        if weight_sum > 0:
            sorted_weights /= weight_sum

        indices[v] = sorted_idx
        weights[v] = sorted_weights

    return indices, weights


def heat_diffusion_weights_numpy(
    vertices: np.ndarray,
    edges: list[tuple[int, int]],
    bone_vertices: list[int],
    iterations: int = 50,
    diffusion_rate: float = 0.5
) -> tuple[np.ndarray, np.ndarray]:
    """
    Heat diffusion method using numpy.
    """
    n_vertices = len(vertices)
    n_bones = len(bone_vertices)

    # Build sparse adjacency
    adj = [[] for _ in range(n_vertices)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    # Initialize heat (one channel per bone)
    heat = np.zeros((n_bones, n_vertices), dtype=np.float32)
    for bone_idx, v in enumerate(bone_vertices):
        heat[bone_idx, v] = 1.0

    # Diffuse
    for _ in range(iterations):
        new_heat = heat.copy()
        for v in range(n_vertices):
            if not adj[v]:
                continue
            neighbor_avg = heat[:, adj[v]].mean(axis=1)
            new_heat[:, v] = heat[:, v] * (1 - diffusion_rate) + neighbor_avg * diffusion_rate
        heat = new_heat

    # Convert to weights
    heat = heat.T  # (N, B)

    # Top 4 per vertex
    indices = np.zeros((n_vertices, 4), dtype=np.uint8)
    weights = np.zeros((n_vertices, 4), dtype=np.float32)

    for v in range(n_vertices):
        sorted_idx = np.argsort(-heat[v])[:4]
        sorted_weights = heat[v, sorted_idx]
        weight_sum = sorted_weights.sum()
        if weight_sum > 0:
            sorted_weights /= weight_sum
        indices[v] = sorted_idx
        weights[v] = sorted_weights

    return indices, weights
```

## Best Practices

### Choosing an Algorithm

| Method | Best For | Complexity |
|--------|----------|------------|
| **Distance** | Simple meshes, fast prototyping | O(V * B) |
| **Envelope** | Characters with defined segments | O(V * B) |
| **Heat Diffusion** | Organic shapes, smooth falloff | O(iterations * V * E) |
| **Geodesic** | Complex topology, accurate | O(B * V log V) |

### Quality Checks

1. **Verify normalization**: All weights sum to 1.0
2. **Check coverage**: No vertices with zero total weight
3. **Test deformation**: Animate and look for artifacts
4. **Smooth transitions**: No sharp weight boundaries at joints

### Common Issues

**Candy wrapper effect**: Twist artifacts at joints
- Solution: Add intermediate bones or increase blend zone

**Stretching at extremities**: Fingers/toes stretch unnaturally
- Solution: Increase bone influence radius at tips

**Weight bleeding**: Unrelated body parts move together
- Solution: Use volumetric constraints or geodesic distances
