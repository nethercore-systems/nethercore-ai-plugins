# UV Mapping Technique Reference

Detailed implementations for UV unwrapping algorithms.

## Projection Methods

### Planar Projection

Projects vertices onto a plane. Best for flat surfaces.

```rust
fn planar_projection(mesh: &Mesh, axis: ProjectionAxis) -> Vec<[f32; 2]> {
    mesh.vertices.iter().map(|v| {
        match axis {
            ProjectionAxis::XY => [v.x, v.y],
            ProjectionAxis::XZ => [v.x, v.z],
            ProjectionAxis::YZ => [v.y, v.z],
        }
    }).collect()
}

// With automatic axis selection based on normal
fn auto_planar_projection(mesh: &Mesh, face_indices: &[usize]) -> Vec<[f32; 2]> {
    // Calculate average face normal
    let avg_normal = calculate_average_normal(mesh, face_indices);

    // Choose projection axis perpendicular to dominant normal component
    let axis = if avg_normal.y.abs() > avg_normal.x.abs() && avg_normal.y.abs() > avg_normal.z.abs() {
        ProjectionAxis::XZ  // Looking down Y
    } else if avg_normal.x.abs() > avg_normal.z.abs() {
        ProjectionAxis::YZ  // Looking down X
    } else {
        ProjectionAxis::XY  // Looking down Z
    };

    planar_projection(mesh, axis)
}
```

### Cylindrical Projection

Wraps UVs around a cylinder. Best for tubes, limbs, barrels.

```rust
fn cylindrical_projection(mesh: &Mesh, axis: Vec3, center: Vec3) -> Vec<[f32; 2]> {
    mesh.vertices.iter().map(|v| {
        let local = *v - center;

        // Project onto plane perpendicular to axis
        let on_axis = axis * local.dot(axis);
        let radial = local - on_axis;

        // Angle around axis -> U coordinate
        let angle = radial.z.atan2(radial.x);
        let u = (angle / (2.0 * PI) + 0.5).fract();

        // Height along axis -> V coordinate
        let v = local.dot(axis) * 0.5 + 0.5;

        [u, v]
    }).collect()
}
```

**Handling the seam:**
```rust
fn fix_cylindrical_seam(uvs: &mut Vec<[f32; 2]>, mesh: &Mesh) {
    // Find edges that cross the U=0/1 boundary
    for edge in mesh.edges() {
        let u0 = uvs[edge.v0][0];
        let u1 = uvs[edge.v1][0];

        // If UVs are far apart, one needs adjustment
        if (u0 - u1).abs() > 0.5 {
            if u0 < 0.5 {
                uvs[edge.v0][0] += 1.0;
            } else {
                uvs[edge.v1][0] += 1.0;
            }
        }
    }
}
```

### Spherical Projection

Maps to a sphere. Best for balls, planets, heads.

```rust
fn spherical_projection(mesh: &Mesh, center: Vec3) -> Vec<[f32; 2]> {
    mesh.vertices.iter().map(|v| {
        let dir = (*v - center).normalize();

        // Longitude -> U (0 to 1)
        let u = (dir.z.atan2(dir.x) / (2.0 * PI) + 0.5).fract();

        // Latitude -> V (0 at south pole, 1 at north)
        let v = dir.y.asin() / PI + 0.5;

        [u, v]
    }).collect()
}
```

**Note:** Spherical projection has severe distortion at poles. For heads, consider using LSCM instead.

### Box (Cubic) Projection

Projects onto 6 cube faces. Best for crates, buildings.

```rust
fn box_projection(mesh: &Mesh) -> Vec<[f32; 2]> {
    mesh.vertices.iter().zip(mesh.normals.iter()).map(|(v, n)| {
        // Determine dominant face based on normal
        let abs_n = n.abs();
        let face = if abs_n.x >= abs_n.y && abs_n.x >= abs_n.z {
            if n.x > 0.0 { Face::PosX } else { Face::NegX }
        } else if abs_n.y >= abs_n.z {
            if n.y > 0.0 { Face::PosY } else { Face::NegY }
        } else {
            if n.z > 0.0 { Face::PosZ } else { Face::NegZ }
        };

        // Project onto face plane
        match face {
            Face::PosX | Face::NegX => [v.z, v.y],
            Face::PosY | Face::NegY => [v.x, v.z],
            Face::PosZ | Face::NegZ => [v.x, v.y],
        }
    }).collect()
}
```

---

## LSCM (Least Squares Conformal Maps)

Minimizes angle distortion. Best for organic shapes.

### Algorithm Overview

1. Pin two boundary vertices (fixes rotation/scale ambiguity)
2. Build conformal energy matrix
3. Solve least-squares system
4. Extract UV coordinates

### Implementation

```rust
fn lscm_unwrap(mesh: &Mesh, boundary_vertices: &[usize]) -> Vec<[f32; 2]> {
    let n = mesh.vertices.len();

    // 1. Pin two boundary vertices
    let pin0 = boundary_vertices[0];
    let pin1 = boundary_vertices[boundary_vertices.len() / 2];

    // 2. Build conformal energy matrix
    // Each triangle contributes terms to minimize angle distortion
    let mut matrix = SparseMatrix::new(n * 2, n * 2);
    let mut rhs = vec![0.0; n * 2];

    for tri in mesh.triangles() {
        add_conformal_terms(&mut matrix, mesh, tri);
    }

    // 3. Add pin constraints
    // pin0 -> (0, 0)
    matrix.set_row_to_identity(pin0 * 2);
    matrix.set_row_to_identity(pin0 * 2 + 1);
    rhs[pin0 * 2] = 0.0;
    rhs[pin0 * 2 + 1] = 0.0;

    // pin1 -> (1, 0)
    matrix.set_row_to_identity(pin1 * 2);
    matrix.set_row_to_identity(pin1 * 2 + 1);
    rhs[pin1 * 2] = 1.0;
    rhs[pin1 * 2 + 1] = 0.0;

    // 4. Solve least squares
    let solution = matrix.solve_least_squares(&rhs);

    // 5. Extract UVs
    (0..n)
        .map(|i| [solution[i * 2], solution[i * 2 + 1]])
        .collect()
}

fn add_conformal_terms(matrix: &mut SparseMatrix, mesh: &Mesh, tri: Triangle) {
    let p0 = mesh.vertices[tri.v0];
    let p1 = mesh.vertices[tri.v1];
    let p2 = mesh.vertices[tri.v2];

    // Local 2D coordinates in triangle plane
    let e1 = p1 - p0;
    let e2 = p2 - p0;
    let normal = e1.cross(e2).normalize();

    // Build local coordinate system
    let x_axis = e1.normalize();
    let y_axis = normal.cross(x_axis);

    // Project to 2D
    let local = [
        [0.0, 0.0],
        [e1.dot(x_axis), e1.dot(y_axis)],
        [e2.dot(x_axis), e2.dot(y_axis)],
    ];

    // Conformal energy: minimize (du/dx - dv/dy)^2 + (du/dy + dv/dx)^2
    // This leads to Cauchy-Riemann equations
    add_cauchy_riemann_terms(matrix, tri, &local);
}
```

### When to Use LSCM
- Organic shapes (characters, creatures, plants)
- Complex topology
- When angle preservation matters more than area

---

## ABF++ (Angle-Based Flattening)

Optimizes interior angles to minimize distortion. Best for hard-surface models.

### Algorithm Overview

1. Compute target angles (preserve triangle shape)
2. Iteratively adjust angles to satisfy constraints
3. Reconstruct UVs from angles

```rust
fn abf_unwrap(mesh: &Mesh) -> Vec<[f32; 2]> {
    // 1. Compute target angles from 3D triangles
    let target_angles = compute_target_angles(mesh);

    // 2. Initialize with target angles
    let mut angles = target_angles.clone();

    // 3. Iterative optimization
    for _ in 0..MAX_ITERATIONS {
        // Constraint: angles in each triangle sum to PI
        enforce_triangle_sum(&mut angles, mesh);

        // Constraint: angles around each vertex sum to 2*PI (interior) or less (boundary)
        enforce_vertex_sum(&mut angles, mesh);

        // Minimize deviation from target
        minimize_angle_deviation(&mut angles, &target_angles);
    }

    // 4. Reconstruct UVs from angles
    reconstruct_uvs_from_angles(mesh, &angles)
}
```

### When to Use ABF++
- CAD models
- Hard-surface (vehicles, weapons, architecture)
- When precise angle preservation is critical

---

## Automatic Seam Detection

Find optimal places to cut the mesh for unwrapping.

```rust
fn detect_seams(mesh: &Mesh) -> Vec<Edge> {
    let mut seam_candidates: Vec<(Edge, f32)> = vec![];

    for edge in mesh.edges() {
        let score = seam_score(mesh, edge);
        seam_candidates.push((edge, score));
    }

    // Higher score = better seam candidate
    seam_candidates.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());

    // Build connected seam paths
    connect_seam_paths(seam_candidates)
}

fn seam_score(mesh: &Mesh, edge: Edge) -> f32 {
    // Factor 1: High curvature (sharp corners) = good seam location
    let curvature = edge_curvature(mesh, edge);

    // Factor 2: Low visibility (hidden edges) = good seam location
    let visibility = edge_visibility_score(mesh, edge);

    // Factor 3: Distortion reduction if cut here
    let distortion_reduction = estimate_distortion_reduction(mesh, edge);

    // Combine factors
    curvature * 0.4 + (1.0 - visibility) * 0.3 + distortion_reduction * 0.3
}

fn edge_curvature(mesh: &Mesh, edge: Edge) -> f32 {
    // Get adjacent face normals
    let faces = mesh.edge_faces(edge);
    if faces.len() != 2 {
        return 1.0;  // Boundary edge
    }

    let n0 = mesh.face_normal(faces[0]);
    let n1 = mesh.face_normal(faces[1]);

    // Curvature = 1 - dot product (0 = flat, 1 = 90 deg, 2 = 180 deg)
    1.0 - n0.dot(n1)
}
```

---

## UV Island Packing

Efficiently pack UV islands into 0-1 UV space.

```rust
fn pack_uv_islands(islands: &mut [UvIsland], padding: f32) -> f32 {
    // Sort by area (largest first = better packing)
    islands.sort_by(|a, b| b.area().partial_cmp(&a.area()).unwrap());

    // Guillotine bin packing
    let mut packer = GuillotinePacker::new(1.0, 1.0);

    for island in islands.iter_mut() {
        // Try both orientations
        let (width, height) = island.bounding_size();

        let placed = packer.pack(width + padding, height + padding)
            .or_else(|| {
                // Try rotated 90 degrees
                island.rotate_90();
                packer.pack(height + padding, width + padding)
            });

        if let Some((x, y)) = placed {
            island.translate(x + padding / 2.0, y + padding / 2.0);
        } else {
            // Island doesn't fit - need to scale down all islands
            // or use multiple UV tiles
        }
    }

    packer.utilization()  // 0.0-1.0 efficiency
}

struct GuillotinePacker {
    free_rects: Vec<Rect>,
}

impl GuillotinePacker {
    fn new(width: f32, height: f32) -> Self {
        Self {
            free_rects: vec![Rect { x: 0.0, y: 0.0, w: width, h: height }],
        }
    }

    fn pack(&mut self, width: f32, height: f32) -> Option<(f32, f32)> {
        // Find best-fit free rectangle
        let best_idx = self.free_rects.iter()
            .enumerate()
            .filter(|(_, r)| r.w >= width && r.h >= height)
            .min_by(|(_, a), (_, b)| {
                let a_waste = a.w * a.h - width * height;
                let b_waste = b.w * b.h - width * height;
                a_waste.partial_cmp(&b_waste).unwrap()
            })
            .map(|(i, _)| i)?;

        let rect = self.free_rects.remove(best_idx);
        let pos = (rect.x, rect.y);

        // Split remaining space (guillotine cut)
        if rect.w - width > 0.01 {
            self.free_rects.push(Rect {
                x: rect.x + width,
                y: rect.y,
                w: rect.w - width,
                h: height,
            });
        }
        if rect.h - height > 0.01 {
            self.free_rects.push(Rect {
                x: rect.x,
                y: rect.y + height,
                w: rect.w,
                h: rect.h - height,
            });
        }

        Some(pos)
    }
}
```

---

## Quality Metrics

### Angle Distortion

```rust
fn measure_angle_distortion(mesh: &Mesh, uvs: &[[f32; 2]]) -> f32 {
    let mut total_distortion = 0.0;
    let mut total_area = 0.0;

    for tri in mesh.triangles() {
        // 3D angles
        let angles_3d = triangle_angles_3d(mesh, tri);

        // 2D angles
        let angles_2d = triangle_angles_2d(uvs, tri);

        // Distortion per angle
        for i in 0..3 {
            let distortion = (angles_3d[i] - angles_2d[i]).abs() / angles_3d[i];
            total_distortion += distortion * triangle_area_3d(mesh, tri);
        }

        total_area += triangle_area_3d(mesh, tri);
    }

    total_distortion / total_area
}
```

### Area Distortion

```rust
fn measure_area_distortion(mesh: &Mesh, uvs: &[[f32; 2]]) -> f32 {
    let areas_3d: Vec<f32> = mesh.triangles().map(|t| triangle_area_3d(mesh, t)).collect();
    let areas_2d: Vec<f32> = mesh.triangles().map(|t| triangle_area_2d(uvs, t)).collect();

    // Normalize both
    let total_3d: f32 = areas_3d.iter().sum();
    let total_2d: f32 = areas_2d.iter().sum();

    let mut distortion = 0.0;
    for (a3d, a2d) in areas_3d.iter().zip(areas_2d.iter()) {
        let ratio_3d = a3d / total_3d;
        let ratio_2d = a2d / total_2d;
        distortion += (ratio_3d - ratio_2d).abs();
    }

    distortion
}
```

### Texel Density Uniformity

```rust
fn measure_texel_density_variance(mesh: &Mesh, uvs: &[[f32; 2]], texture_size: u32) -> f32 {
    let densities: Vec<f32> = mesh.triangles().map(|t| {
        let area_3d = triangle_area_3d(mesh, t);
        let area_uv = triangle_area_2d(uvs, t);
        let texels = area_uv * (texture_size * texture_size) as f32;
        texels / area_3d  // texels per world unit
    }).collect();

    let mean: f32 = densities.iter().sum::<f32>() / densities.len() as f32;
    let variance: f32 = densities.iter().map(|d| (d - mean).powi(2)).sum::<f32>() / densities.len() as f32;

    variance.sqrt() / mean  // Coefficient of variation
}
```
