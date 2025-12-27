# Quality Benchmarks Reference

Numerical thresholds and validation code for procedural asset quality.

## Bone Weight Quality

### Thresholds

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Weight sum deviation | <0.001 | 0.001-0.01 | >0.01 |
| Max bone influences | <=4 | 5-6 | >6 |
| Candy wrapper score | >0.9 | 0.7-0.9 | <0.7 |
| Weight bleeding regions | 0 | 1-2 minor | >2 or major |
| Unweighted vertices | 0 | <1% | >1% |

### Validation Code

```rust
pub struct BoneWeightQuality {
    pub overall_score: f32,           // 0-1, higher is better
    pub weight_sum_deviation: f32,    // Max deviation from 1.0
    pub max_influences: u32,          // Highest influence count
    pub candy_wrapper_score: f32,     // 0-1
    pub bleeding_count: u32,          // Number of bleeding regions
    pub unweighted_count: u32,        // Vertices with no weights
}

impl BoneWeightQuality {
    pub fn grade(&self) -> Grade {
        if self.weight_sum_deviation < 0.001
            && self.max_influences <= 4
            && self.candy_wrapper_score > 0.9
            && self.bleeding_count == 0
            && self.unweighted_count == 0
        {
            Grade::Good
        } else if self.weight_sum_deviation < 0.01
            && self.max_influences <= 6
            && self.candy_wrapper_score > 0.7
            && self.bleeding_count <= 2
        {
            Grade::Acceptable
        } else {
            Grade::Poor
        }
    }
}

pub fn validate_bone_weights(
    mesh: &Mesh,
    weights: &BoneWeights,
    skeleton: &Skeleton,
) -> BoneWeightQuality {
    let mut quality = BoneWeightQuality::default();

    // Weight sum validation
    let mut max_deviation = 0.0f32;
    let mut unweighted = 0u32;

    for v in 0..mesh.vertex_count() {
        let w = weights.get_weights(v);
        let sum: f32 = w.iter().sum();

        if sum < 0.001 {
            unweighted += 1;
        }

        let deviation = (sum - 1.0).abs();
        max_deviation = max_deviation.max(deviation);
    }

    quality.weight_sum_deviation = max_deviation;
    quality.unweighted_count = unweighted;

    // Max influences
    quality.max_influences = (0..mesh.vertex_count())
        .map(|v| weights.influence_count(v))
        .max()
        .unwrap_or(0);

    // Candy wrapper detection
    quality.candy_wrapper_score = detect_candy_wrapper(mesh, weights, skeleton);

    // Weight bleeding
    quality.bleeding_count = detect_weight_bleeding(mesh, weights).len() as u32;

    // Overall score
    quality.overall_score = calculate_overall_score(&quality);

    quality
}

fn calculate_overall_score(q: &BoneWeightQuality) -> f32 {
    let mut score = 1.0;

    // Weight sum (critical)
    if q.weight_sum_deviation > 0.01 {
        score *= 0.5;
    } else if q.weight_sum_deviation > 0.001 {
        score *= 0.9;
    }

    // Influences
    if q.max_influences > 6 {
        score *= 0.6;
    } else if q.max_influences > 4 {
        score *= 0.85;
    }

    // Candy wrapper
    score *= q.candy_wrapper_score;

    // Bleeding
    if q.bleeding_count > 2 {
        score *= 0.7;
    } else if q.bleeding_count > 0 {
        score *= 0.9;
    }

    // Unweighted
    let unweighted_ratio = q.unweighted_count as f32 / 100.0;  // Assume 100 vertices
    score *= (1.0 - unweighted_ratio).max(0.5);

    score
}
```

---

## UV Mapping Quality

### Thresholds

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Angle distortion | <5% | 5-15% | >15% |
| Area distortion | <10% | 10-25% | >25% |
| UV utilization | >70% | 50-70% | <50% |
| Texel density variance | <2x | 2-4x | >4x |
| Overlapping UVs | 0% | <1% | >1% |

### Validation Code

```rust
pub struct UvQuality {
    pub overall_score: f32,
    pub angle_distortion: f32,      // 0-1, percentage
    pub area_distortion: f32,       // 0-1, percentage
    pub utilization: f32,           // 0-1, space used
    pub texel_density_cv: f32,      // Coefficient of variation
    pub overlap_percentage: f32,    // 0-1
}

impl UvQuality {
    pub fn grade(&self) -> Grade {
        if self.angle_distortion < 0.05
            && self.area_distortion < 0.10
            && self.utilization > 0.70
            && self.texel_density_cv < 2.0
            && self.overlap_percentage == 0.0
        {
            Grade::Good
        } else if self.angle_distortion < 0.15
            && self.area_distortion < 0.25
            && self.utilization > 0.50
            && self.texel_density_cv < 4.0
            && self.overlap_percentage < 0.01
        {
            Grade::Acceptable
        } else {
            Grade::Poor
        }
    }
}

pub fn validate_uvs(mesh: &Mesh, uvs: &[[f32; 2]]) -> UvQuality {
    UvQuality {
        angle_distortion: measure_angle_distortion(mesh, uvs),
        area_distortion: measure_area_distortion(mesh, uvs),
        utilization: measure_uv_utilization(uvs),
        texel_density_cv: measure_texel_density_variance(mesh, uvs),
        overlap_percentage: detect_uv_overlap(mesh, uvs),
        overall_score: 0.0,  // Calculated after
    }
}

fn measure_angle_distortion(mesh: &Mesh, uvs: &[[f32; 2]]) -> f32 {
    let mut total_distortion = 0.0;
    let mut total_weight = 0.0;

    for tri in mesh.triangles() {
        // 3D angles
        let a3d = triangle_angles_3d(mesh, tri);

        // 2D angles
        let a2d = triangle_angles_2d(uvs, tri);

        let area = triangle_area_3d(mesh, tri);

        for i in 0..3 {
            let distortion = (a3d[i] - a2d[i]).abs() / a3d[i];
            total_distortion += distortion * area;
            total_weight += area;
        }
    }

    total_distortion / total_weight
}

fn measure_area_distortion(mesh: &Mesh, uvs: &[[f32; 2]]) -> f32 {
    let areas_3d: Vec<f32> = mesh.triangles()
        .map(|t| triangle_area_3d(mesh, t))
        .collect();

    let areas_2d: Vec<f32> = mesh.triangles()
        .map(|t| triangle_area_2d(uvs, t))
        .collect();

    let sum_3d: f32 = areas_3d.iter().sum();
    let sum_2d: f32 = areas_2d.iter().sum();

    let mut distortion = 0.0;
    for (a3, a2) in areas_3d.iter().zip(areas_2d.iter()) {
        let ratio_3d = a3 / sum_3d;
        let ratio_2d = a2 / sum_2d;
        distortion += (ratio_3d - ratio_2d).abs();
    }

    distortion / 2.0  // Normalize to 0-1
}

fn measure_uv_utilization(uvs: &[[f32; 2]]) -> f32 {
    // Compute convex hull area / UV space area
    // Or use actual UV island coverage

    let mut min_u = f32::MAX;
    let mut max_u = f32::MIN;
    let mut min_v = f32::MAX;
    let mut max_v = f32::MIN;

    for uv in uvs {
        min_u = min_u.min(uv[0]);
        max_u = max_u.max(uv[0]);
        min_v = min_v.min(uv[1]);
        max_v = max_v.max(uv[1]);
    }

    let used_area = (max_u - min_u) * (max_v - min_v);
    used_area.min(1.0)  // Cap at 1.0
}

fn measure_texel_density_variance(mesh: &Mesh, uvs: &[[f32; 2]]) -> f32 {
    let densities: Vec<f32> = mesh.triangles()
        .map(|t| {
            let area_3d = triangle_area_3d(mesh, t);
            let area_2d = triangle_area_2d(uvs, t);
            area_2d / area_3d.max(0.0001)
        })
        .collect();

    let mean: f32 = densities.iter().sum::<f32>() / densities.len() as f32;
    let variance: f32 = densities.iter()
        .map(|d| (d - mean).powi(2))
        .sum::<f32>() / densities.len() as f32;

    variance.sqrt() / mean  // Coefficient of variation
}

fn detect_uv_overlap(mesh: &Mesh, uvs: &[[f32; 2]]) -> f32 {
    let mut overlap_area = 0.0;
    let mut total_area = 0.0;

    let triangles: Vec<_> = mesh.triangles().collect();

    for i in 0..triangles.len() {
        for j in (i + 1)..triangles.len() {
            let overlap = triangle_overlap_area(uvs, triangles[i], triangles[j]);
            overlap_area += overlap;
        }
        total_area += triangle_area_2d(uvs, triangles[i]);
    }

    overlap_area / total_area
}
```

---

## Noise Quality

### Thresholds

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Value range | Full [-1,1] or [0,1] | 90%+ | <90% |
| Histogram spread | 60-90% | 40-60% | <40% |
| Tile seam error | <1% | 1-5% | >5% |
| Octave balance | Proper falloff | Slight imbalance | Major imbalance |

### Validation Code

```rust
pub struct NoiseQuality {
    pub value_range_usage: f32,   // 0-1, how much of range is used
    pub histogram_spread: f32,    // 0-1, distribution evenness
    pub tile_seam_error: f32,     // 0-1, edge mismatch
    pub mean_value: f32,          // Should be ~0 or ~0.5
    pub std_deviation: f32,       // Statistical spread
}

impl NoiseQuality {
    pub fn grade(&self) -> Grade {
        if self.value_range_usage > 0.90
            && self.histogram_spread > 0.60
            && self.tile_seam_error < 0.01
        {
            Grade::Good
        } else if self.value_range_usage > 0.80
            && self.histogram_spread > 0.40
            && self.tile_seam_error < 0.05
        {
            Grade::Acceptable
        } else {
            Grade::Poor
        }
    }
}

pub fn validate_noise_texture(pixels: &[f32], width: u32, height: u32) -> NoiseQuality {
    let n = pixels.len();

    // Value range
    let min = pixels.iter().cloned().fold(f32::MAX, f32::min);
    let max = pixels.iter().cloned().fold(f32::MIN, f32::max);
    let value_range_usage = max - min;

    // Mean and std deviation
    let mean: f32 = pixels.iter().sum::<f32>() / n as f32;
    let variance: f32 = pixels.iter().map(|x| (x - mean).powi(2)).sum::<f32>() / n as f32;
    let std_deviation = variance.sqrt();

    // Histogram spread
    let histogram_spread = calculate_histogram_spread(pixels);

    // Tile seam error
    let tile_seam_error = calculate_tile_seam_error(pixels, width, height);

    NoiseQuality {
        value_range_usage,
        histogram_spread,
        tile_seam_error,
        mean_value: mean,
        std_deviation,
    }
}

fn calculate_histogram_spread(values: &[f32]) -> f32 {
    const BINS: usize = 16;
    let mut histogram = [0u32; BINS];

    for &v in values {
        let bin = ((v + 1.0) / 2.0 * BINS as f32).floor() as usize;
        let bin = bin.min(BINS - 1);
        histogram[bin] += 1;
    }

    let total = values.len() as f32;
    let expected = total / BINS as f32;

    // Calculate how evenly distributed
    let chi_squared: f32 = histogram.iter()
        .map(|&count| {
            let diff = count as f32 - expected;
            diff * diff / expected
        })
        .sum();

    // Convert to 0-1 score (lower chi-squared = better distribution)
    1.0 / (1.0 + chi_squared / BINS as f32)
}

fn calculate_tile_seam_error(pixels: &[f32], width: u32, height: u32) -> f32 {
    let mut error = 0.0;
    let mut count = 0;

    // Check horizontal seam (left edge vs right edge)
    for y in 0..height {
        let left = pixels[(y * width) as usize];
        let right = pixels[(y * width + width - 1) as usize];
        error += (left - right).abs();
        count += 1;
    }

    // Check vertical seam (top edge vs bottom edge)
    for x in 0..width {
        let top = pixels[x as usize];
        let bottom = pixels[((height - 1) * width + x) as usize];
        error += (top - bottom).abs();
        count += 1;
    }

    error / count as f32
}
```

---

## Texture Quality

### Thresholds

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| MRE value validity | 100% in [0,1] | 99%+ | <99% |
| Alpha coherence | Smooth gradients | Some noise | Random noise |
| Resolution | Power of 2 | Other | Non-standard |
| Mipmap chain | Complete | Partial | Missing |

### Validation Code

```rust
pub struct TextureQuality {
    pub resolution_valid: bool,       // Power of 2
    pub value_range_valid: bool,      // All values in [0,255]
    pub alpha_coherence: f32,         // 0-1, gradient smoothness
    pub channel_correlation: f32,     // For packed textures
}

pub fn validate_texture(image: &RgbaImage) -> TextureQuality {
    let (width, height) = image.dimensions();

    // Power of 2 check
    let resolution_valid = width.is_power_of_two() && height.is_power_of_two();

    // Value range always valid for u8
    let value_range_valid = true;

    // Alpha coherence
    let alpha_coherence = measure_alpha_coherence(image);

    TextureQuality {
        resolution_valid,
        value_range_valid,
        alpha_coherence,
        channel_correlation: 0.0,
    }
}

fn measure_alpha_coherence(image: &RgbaImage) -> f32 {
    let (width, height) = image.dimensions();
    let mut total_diff = 0.0;
    let mut count = 0;

    for y in 0..(height - 1) {
        for x in 0..(width - 1) {
            let a = image.get_pixel(x, y)[3] as f32;
            let a_right = image.get_pixel(x + 1, y)[3] as f32;
            let a_down = image.get_pixel(x, y + 1)[3] as f32;

            total_diff += (a - a_right).abs();
            total_diff += (a - a_down).abs();
            count += 2;
        }
    }

    let avg_diff = total_diff / count as f32;

    // Lower average difference = smoother gradients = higher coherence
    1.0 - (avg_diff / 255.0)
}

pub fn validate_mre_texture(image: &RgbaImage) -> MreQuality {
    let mut metallic_range = (f32::MAX, f32::MIN);
    let mut roughness_range = (f32::MAX, f32::MIN);
    let mut emissive_range = (f32::MAX, f32::MIN);

    for pixel in image.pixels() {
        let m = pixel[0] as f32 / 255.0;
        let r = pixel[1] as f32 / 255.0;
        let e = pixel[2] as f32 / 255.0;

        metallic_range.0 = metallic_range.0.min(m);
        metallic_range.1 = metallic_range.1.max(m);
        roughness_range.0 = roughness_range.0.min(r);
        roughness_range.1 = roughness_range.1.max(r);
        emissive_range.0 = emissive_range.0.min(e);
        emissive_range.1 = emissive_range.1.max(e);
    }

    MreQuality {
        metallic_range,
        roughness_range,
        emissive_range,
        valid: true,  // All values inherently in [0,1] for u8
    }
}
```

---

## Animation Quality

### Thresholds

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Quaternion normalization | <0.0001 error | <0.001 | >0.001 |
| Keyframe spacing | Uniform or adaptive | Slightly irregular | Random |
| Root motion smoothness | Continuous | Minor pops | Visible pops |
| Bone scale uniformity | 1.0 +/- 0.01 | +/- 0.05 | >0.05 |

### Validation Code

```rust
pub struct AnimationQuality {
    pub quaternion_error: f32,      // Max normalization error
    pub keyframe_regularity: f32,   // 0-1, timing consistency
    pub motion_smoothness: f32,     // 0-1, derivative continuity
    pub scale_deviation: f32,       // Max deviation from 1.0
}

pub fn validate_animation(keyframes: &[Keyframe]) -> AnimationQuality {
    let mut max_quat_error = 0.0f32;
    let mut max_scale_deviation = 0.0f32;

    for kf in keyframes {
        // Quaternion normalization
        let q = &kf.rotation;
        let len = (q.x * q.x + q.y * q.y + q.z * q.z + q.w * q.w).sqrt();
        max_quat_error = max_quat_error.max((len - 1.0).abs());

        // Scale deviation
        let s = &kf.scale;
        let scale_error = ((s.x - 1.0).abs())
            .max((s.y - 1.0).abs())
            .max((s.z - 1.0).abs());
        max_scale_deviation = max_scale_deviation.max(scale_error);
    }

    AnimationQuality {
        quaternion_error: max_quat_error,
        keyframe_regularity: measure_keyframe_regularity(keyframes),
        motion_smoothness: measure_motion_smoothness(keyframes),
        scale_deviation: max_scale_deviation,
    }
}

fn measure_keyframe_regularity(keyframes: &[Keyframe]) -> f32 {
    if keyframes.len() < 2 {
        return 1.0;
    }

    let intervals: Vec<f32> = keyframes.windows(2)
        .map(|w| w[1].time - w[0].time)
        .collect();

    let mean: f32 = intervals.iter().sum::<f32>() / intervals.len() as f32;
    let variance: f32 = intervals.iter()
        .map(|i| (i - mean).powi(2))
        .sum::<f32>() / intervals.len() as f32;

    let cv = variance.sqrt() / mean;

    1.0 / (1.0 + cv)  // Lower variance = higher regularity
}

fn measure_motion_smoothness(keyframes: &[Keyframe]) -> f32 {
    if keyframes.len() < 3 {
        return 1.0;
    }

    // Check for velocity discontinuities
    let mut max_acceleration = 0.0f32;

    for i in 1..(keyframes.len() - 1) {
        let dt1 = keyframes[i].time - keyframes[i - 1].time;
        let dt2 = keyframes[i + 1].time - keyframes[i].time;

        let v1 = (keyframes[i].position - keyframes[i - 1].position) / dt1;
        let v2 = (keyframes[i + 1].position - keyframes[i].position) / dt2;

        let accel = (v2 - v1).length() / ((dt1 + dt2) / 2.0);
        max_acceleration = max_acceleration.max(accel);
    }

    // Normalize (lower acceleration = smoother)
    1.0 / (1.0 + max_acceleration * 0.1)
}
```

---

## Aggregate Quality Report

```rust
pub struct AssetQualityReport {
    pub bone_weights: Option<BoneWeightQuality>,
    pub uvs: Option<UvQuality>,
    pub textures: Vec<TextureQuality>,
    pub animations: Vec<AnimationQuality>,
    pub overall_grade: Grade,
    pub issues: Vec<QualityIssue>,
}

#[derive(Debug)]
pub struct QualityIssue {
    pub severity: Severity,
    pub category: Category,
    pub description: String,
    pub suggestion: String,
}

impl AssetQualityReport {
    pub fn print_summary(&self) {
        println!("Asset Quality Report");
        println!("====================");
        println!("Overall Grade: {:?}", self.overall_grade);
        println!();

        if !self.issues.is_empty() {
            println!("Issues Found:");
            for issue in &self.issues {
                println!("  [{:?}] {}: {}", issue.severity, issue.category, issue.description);
                println!("         Suggestion: {}", issue.suggestion);
            }
        }
    }
}
```
