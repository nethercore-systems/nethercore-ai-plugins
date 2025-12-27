# Advanced Bone Weight Algorithms

Detailed implementations of sophisticated bone weight calculation methods.

## Heat Diffusion Method

Heat diffusion simulates heat spreading from bone positions through mesh connectivity, producing smooth organic weights.

### Algorithm

1. Set bone positions as "heat sources" (value = 1.0)
2. Diffuse heat through mesh edges iteratively
3. Final heat values become weights

### Implementation

```rust
use std::collections::HashMap;
use glam::Vec3;

struct Mesh {
    vertices: Vec<Vec3>,
    edges: Vec<(usize, usize)>,
}

fn heat_diffusion_weights(
    mesh: &Mesh,
    bone_positions: &[Vec3],
    iterations: usize,
    diffusion_rate: f32,
) -> Vec<([u8; 4], [f32; 4])> {
    let vertex_count = mesh.vertices.len();
    let bone_count = bone_positions.len();

    // Initialize heat per bone per vertex
    let mut heat: Vec<Vec<f32>> = vec![vec![0.0; vertex_count]; bone_count];

    // Find nearest vertex to each bone and set initial heat
    for (bone_idx, &bone_pos) in bone_positions.iter().enumerate() {
        let nearest = find_nearest_vertex(&mesh.vertices, bone_pos);
        heat[bone_idx][nearest] = 1.0;
    }

    // Build adjacency list
    let mut neighbors: Vec<Vec<usize>> = vec![Vec::new(); vertex_count];
    for &(a, b) in &mesh.edges {
        neighbors[a].push(b);
        neighbors[b].push(a);
    }

    // Diffuse heat iteratively
    for _ in 0..iterations {
        let mut new_heat = heat.clone();

        for bone_idx in 0..bone_count {
            for v in 0..vertex_count {
                if neighbors[v].is_empty() {
                    continue;
                }

                // Average of neighbor heat values
                let neighbor_avg: f32 = neighbors[v].iter()
                    .map(|&n| heat[bone_idx][n])
                    .sum::<f32>() / neighbors[v].len() as f32;

                // Blend current value with neighbor average
                new_heat[bone_idx][v] =
                    heat[bone_idx][v] * (1.0 - diffusion_rate) +
                    neighbor_avg * diffusion_rate;
            }
        }

        heat = new_heat;
    }

    // Convert heat values to weights
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
            let da = (**a - target).length_squared();
            let db = (**b - target).length_squared();
            da.partial_cmp(&db).unwrap()
        })
        .map(|(i, _)| i)
        .unwrap_or(0)
}
```

### Parameters

| Parameter | Typical Value | Effect |
|-----------|---------------|--------|
| `iterations` | 30-100 | More = smoother but slower |
| `diffusion_rate` | 0.3-0.7 | Higher = faster spread |

## Geodesic Distance Weighting

Uses mesh surface distance rather than Euclidean distance, better for complex topology.

### Implementation

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
        // Reverse for min-heap
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

fn geodesic_distances(mesh: &Mesh, start_vertex: usize) -> Vec<f32> {
    let n = mesh.vertices.len();
    let mut distances = vec![f32::INFINITY; n];
    distances[start_vertex] = 0.0;

    // Build adjacency with edge lengths
    let mut adj: Vec<Vec<(usize, f32)>> = vec![Vec::new(); n];
    for &(a, b) in &mesh.edges {
        let len = (mesh.vertices[a] - mesh.vertices[b]).length();
        adj[a].push((b, len));
        adj[b].push((a, len));
    }

    // Dijkstra's algorithm
    let mut heap = BinaryHeap::new();
    heap.push(DistEntry { vertex: start_vertex, distance: 0.0 });

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
    bone_positions: &[Vec3],
) -> Vec<([u8; 4], [f32; 4])> {
    // Find nearest vertex to each bone
    let bone_vertices: Vec<usize> = bone_positions.iter()
        .map(|&pos| find_nearest_vertex(&mesh.vertices, pos))
        .collect();

    // Calculate geodesic distances from each bone
    let all_distances: Vec<Vec<f32>> = bone_vertices.iter()
        .map(|&start| geodesic_distances(mesh, start))
        .collect();

    // Convert to weights (inverse distance)
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

For characters with clear body segments, assign weights based on spatial regions.

```rust
struct BodySegment {
    bone_index: usize,
    min_y: f32,
    max_y: f32,
    falloff_bottom: f32,
    falloff_top: f32,
}

fn volumetric_weights(
    vertex: Vec3,
    segments: &[BodySegment],
) -> ([u8; 4], [f32; 4]) {
    let y = vertex.y;

    let mut weights: Vec<(usize, f32)> = segments.iter()
        .filter_map(|seg| {
            if y < seg.min_y - seg.falloff_bottom ||
               y > seg.max_y + seg.falloff_top {
                return None;
            }

            let weight = if y < seg.min_y {
                // Bottom falloff zone
                1.0 - (seg.min_y - y) / seg.falloff_bottom
            } else if y > seg.max_y {
                // Top falloff zone
                1.0 - (y - seg.max_y) / seg.falloff_top
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

## Python Implementations

### NumPy Heat Diffusion

```python
import numpy as np

def heat_diffusion_weights_numpy(
    vertices: np.ndarray,
    edges: list[tuple[int, int]],
    bone_vertices: list[int],
    iterations: int = 50,
    diffusion_rate: float = 0.5
) -> tuple[np.ndarray, np.ndarray]:
    """Heat diffusion using numpy for speed."""
    n_vertices = len(vertices)
    n_bones = len(bone_vertices)

    # Build adjacency
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

    # Transpose to (N, B)
    heat = heat.T

    # Get top 4 per vertex
    indices = np.zeros((n_vertices, 4), dtype=np.uint8)
    weights = np.zeros((n_vertices, 4), dtype=np.float32)

    for v in range(n_vertices):
        sorted_idx = np.argsort(-heat[v])[:4]
        sorted_weights = heat[v, sorted_idx]
        if sorted_weights.sum() > 0:
            sorted_weights /= sorted_weights.sum()
        indices[v] = sorted_idx
        weights[v] = sorted_weights

    return indices, weights
```

### SciPy Geodesic

```python
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

def geodesic_weights_scipy(
    vertices: np.ndarray,
    edges: list[tuple[int, int]],
    bone_positions: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Fast geodesic weighting using scipy sparse graphs."""
    n = len(vertices)

    # Build sparse adjacency matrix
    row, col, data = [], [], []
    for a, b in edges:
        dist = np.linalg.norm(vertices[a] - vertices[b])
        row.extend([a, b])
        col.extend([b, a])
        data.extend([dist, dist])

    graph = csr_matrix((data, (row, col)), shape=(n, n))

    # Find nearest vertex to each bone
    bone_vertices = []
    for bp in bone_positions:
        dists = np.linalg.norm(vertices - bp, axis=1)
        bone_vertices.append(np.argmin(dists))

    # Calculate geodesic distances from each bone
    all_dists = []
    for bv in bone_vertices:
        dists = dijkstra(graph, indices=bv)
        all_dists.append(dists)

    all_dists = np.array(all_dists).T  # (N, B)

    # Convert to weights
    raw_weights = 1.0 / (all_dists + 0.001)

    indices = np.zeros((n, 4), dtype=np.uint8)
    weights = np.zeros((n, 4), dtype=np.float32)

    for v in range(n):
        sorted_idx = np.argsort(-raw_weights[v])[:4]
        sorted_w = raw_weights[v, sorted_idx]
        if sorted_w.sum() > 0:
            sorted_w /= sorted_w.sum()
        indices[v] = sorted_idx
        weights[v] = sorted_w

    return indices, weights
```

## Quality Metrics

### Weight Smoothness

```rust
fn weight_smoothness(mesh: &Mesh, weights: &[([u8; 4], [f32; 4])]) -> f32 {
    let mut total_diff = 0.0;
    let mut count = 0;

    for &(a, b) in &mesh.edges {
        for i in 0..4 {
            let w_a = weights[a].1[i];
            let w_b = weights[b].1[i];
            total_diff += (w_a - w_b).abs();
        }
        count += 1;
    }

    if count > 0 { total_diff / count as f32 } else { 0.0 }
}
```

### Coverage Check

```rust
fn check_coverage(weights: &[([u8; 4], [f32; 4])]) -> Vec<usize> {
    weights.iter()
        .enumerate()
        .filter(|(_, (_, w))| w.iter().sum::<f32>() < 0.99)
        .map(|(i, _)| i)
        .collect()
}
```

## Best Practices

### Algorithm Selection

| Mesh Type | Recommended Algorithm |
|-----------|----------------------|
| Simple props | Distance-based |
| Humanoid characters | Envelope or Heat diffusion |
| Organic creatures | Heat diffusion |
| Complex topology | Geodesic |
| Performance-critical | Distance-based with envelopes |

### Iteration Tuning

For heat diffusion:
- Start with 30 iterations, increase if weights too sharp
- Use diffusion_rate 0.5 for balanced spread
- Higher iterations smooth weights but slow computation

### Common Fixes

| Problem | Solution |
|---------|----------|
| Sharp weight boundaries | Increase diffusion iterations |
| Weight bleeding | Add envelope radius limits |
| Zero weights on extremities | Ensure bones cover entire mesh |
| Performance issues | Use distance-based for preview, geodesic for final |
