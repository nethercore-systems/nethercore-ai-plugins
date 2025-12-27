# Quality Heuristics Reference

Complete quality assessment heuristics for SADL-generated assets. Use these metrics for self-assessment and iterative refinement.

## Overview

Quality heuristics provide measurable criteria for evaluating generated assets. Each asset type has specific metrics with target ranges and issue detection.

```rust
pub trait QualityAssessment {
    fn passes_minimum(&self) -> bool;
    fn issues(&self) -> Vec<QualityIssue>;
    fn score(&self) -> f32;  // 0.0 - 1.0
    fn suggestions(&self) -> Vec<&'static str>;
}

pub struct QualityIssue {
    pub severity: Severity,
    pub category: &'static str,
    pub message: String,
    pub fix_suggestion: String,
}

pub enum Severity {
    Info,      // Informational, no action needed
    Warning,   // Should be addressed but not blocking
    Error,     // Must be fixed before use
    Critical,  // Asset is unusable
}
```

---

## Texture Quality Heuristics

### Metrics

```rust
pub struct TextureQuality {
    // Visual quality
    pub contrast: f32,           // 0-1, histogram spread
    pub noise_coherence: f32,    // 0-1, pattern consistency
    pub edge_sharpness: f32,     // 0-1, detail clarity
    pub color_variance: f32,     // 0-1, color richness

    // Technical quality
    pub tileability: f32,        // 0-1, edge continuity
    pub unique_colors: u32,      // Number of distinct colors
    pub histogram_balance: f32,  // 0-1, brightness distribution
    pub power_of_two: bool,      // Dimensions are 2^n

    // Content quality
    pub has_alpha: bool,
    pub alpha_coverage: f32,     // % of non-transparent pixels
    pub semantic_match: f32,     // How well it matches intent
}
```

### Thresholds

| Metric | Minimum | Good | Excellent |
|--------|---------|------|-----------|
| contrast | 0.15 | 0.3 | 0.5 |
| noise_coherence | 0.4 | 0.6 | 0.8 |
| edge_sharpness | 0.3 | 0.5 | 0.7 |
| color_variance | 0.1 | 0.25 | 0.4 |
| tileability | 0.8 | 0.9 | 0.98 |
| unique_colors | 50 | 200 | 1000 |
| histogram_balance | 0.3 | 0.5 | 0.7 |

### Implementation

```rust
impl TextureQuality {
    pub fn analyze(image: &ImageBuffer) -> Self {
        Self {
            contrast: calculate_contrast(image),
            noise_coherence: calculate_coherence(image),
            edge_sharpness: calculate_sharpness(image),
            color_variance: calculate_color_variance(image),
            tileability: calculate_tileability(image),
            unique_colors: count_unique_colors(image),
            histogram_balance: calculate_histogram_balance(image),
            power_of_two: is_power_of_two(image.width()) && is_power_of_two(image.height()),
            has_alpha: image.has_alpha(),
            alpha_coverage: calculate_alpha_coverage(image),
            semantic_match: 0.0,  // Set externally
        }
    }

    pub fn passes_minimum(&self) -> bool {
        self.contrast > 0.15 &&
        self.noise_coherence > 0.4 &&
        self.histogram_balance > 0.3 &&
        self.power_of_two
    }

    pub fn issues(&self) -> Vec<QualityIssue> {
        let mut issues = vec![];

        if self.contrast <= 0.15 {
            issues.push(QualityIssue {
                severity: Severity::Warning,
                category: "contrast",
                message: format!("Low contrast: {:.2}", self.contrast),
                fix_suggestion: "Add more value variation, increase noise amplitude".into(),
            });
        }

        if self.noise_coherence <= 0.4 {
            issues.push(QualityIssue {
                severity: Severity::Warning,
                category: "coherence",
                message: format!("Incoherent noise: {:.2}", self.noise_coherence),
                fix_suggestion: "Increase noise scale, reduce octaves, use perlin over white noise".into(),
            });
        }

        if self.tileability <= 0.8 {
            issues.push(QualityIssue {
                severity: Severity::Error,
                category: "tiling",
                message: format!("Visible seams: {:.2} tileability", self.tileability),
                fix_suggestion: "Use tileable noise, blend edges, or generate with periodic functions".into(),
            });
        }

        if !self.power_of_two {
            issues.push(QualityIssue {
                severity: Severity::Error,
                category: "dimensions",
                message: "Non-power-of-two dimensions".into(),
                fix_suggestion: "Resize to 64, 128, 256, or 512 pixels".into(),
            });
        }

        if self.unique_colors < 50 {
            issues.push(QualityIssue {
                severity: Severity::Info,
                category: "colors",
                message: format!("Few unique colors: {}", self.unique_colors),
                fix_suggestion: "Add subtle color variation for more natural appearance".into(),
            });
        }

        issues
    }

    pub fn score(&self) -> f32 {
        let weights = [
            (self.contrast, 0.2),
            (self.noise_coherence, 0.15),
            (self.edge_sharpness, 0.1),
            (self.histogram_balance, 0.15),
            (self.tileability, 0.2),
            ((self.unique_colors as f32 / 1000.0).min(1.0), 0.1),
            (if self.power_of_two { 1.0 } else { 0.0 }, 0.1),
        ];

        weights.iter().map(|(v, w)| v * w).sum()
    }
}

// Measurement functions
fn calculate_contrast(image: &ImageBuffer) -> f32 {
    let mut min_lum = 1.0f32;
    let mut max_lum = 0.0f32;

    for pixel in image.pixels() {
        let lum = 0.299 * pixel[0] as f32 / 255.0
                + 0.587 * pixel[1] as f32 / 255.0
                + 0.114 * pixel[2] as f32 / 255.0;
        min_lum = min_lum.min(lum);
        max_lum = max_lum.max(lum);
    }

    max_lum - min_lum
}

fn calculate_tileability(image: &ImageBuffer) -> f32 {
    let w = image.width();
    let h = image.height();
    let mut total_diff = 0.0f32;
    let mut samples = 0;

    // Compare left edge to right edge
    for y in 0..h {
        let left = image.get_pixel(0, y);
        let right = image.get_pixel(w - 1, y);
        total_diff += color_distance(left, right);
        samples += 1;
    }

    // Compare top edge to bottom edge
    for x in 0..w {
        let top = image.get_pixel(x, 0);
        let bottom = image.get_pixel(x, h - 1);
        total_diff += color_distance(top, bottom);
        samples += 1;
    }

    let avg_diff = total_diff / samples as f32;
    1.0 - avg_diff.min(1.0)
}
```

---

## Mesh Quality Heuristics

### Metrics

```rust
pub struct MeshQuality {
    // Geometry
    pub vertex_count: u32,
    pub triangle_count: u32,
    pub degenerate_tris: u32,
    pub non_manifold_edges: u32,
    pub watertight: bool,

    // UVs
    pub has_uvs: bool,
    pub uv_coverage: f32,        // 0-1, how much UV space is used
    pub uv_overlap: f32,         // 0-1, overlapping UV regions
    pub max_stretch: f32,        // Max UV stretch ratio

    // Normals
    pub has_normals: bool,
    pub smooth_shading: bool,
    pub normal_consistency: f32, // 0-1, no flipped normals

    // Bounds
    pub bounds_size: [f32; 3],
    pub center_offset: f32,      // Distance from origin
}
```

### Thresholds by Use Case

| Use Case | Max Triangles | Max Vertices | UV Coverage |
|----------|---------------|--------------|-------------|
| Swarm entity | 150 | 100 | 0.5 |
| Standard prop | 300 | 200 | 0.8 |
| Character | 500 | 350 | 0.9 |
| Vehicle | 800 | 500 | 0.85 |
| Hero object | 2000 | 1200 | 0.95 |

### Implementation

```rust
impl MeshQuality {
    pub fn analyze(mesh: &Mesh) -> Self {
        Self {
            vertex_count: mesh.vertices.len() as u32,
            triangle_count: mesh.triangles.len() as u32 / 3,
            degenerate_tris: count_degenerate_triangles(mesh),
            non_manifold_edges: count_non_manifold_edges(mesh),
            watertight: check_watertight(mesh),
            has_uvs: mesh.uvs.len() > 0,
            uv_coverage: calculate_uv_coverage(mesh),
            uv_overlap: calculate_uv_overlap(mesh),
            max_stretch: calculate_max_stretch(mesh),
            has_normals: mesh.normals.len() > 0,
            smooth_shading: mesh.normals.len() == mesh.vertices.len(),
            normal_consistency: check_normal_consistency(mesh),
            bounds_size: calculate_bounds(mesh),
            center_offset: calculate_center_offset(mesh),
        }
    }

    pub fn passes_for_budget(&self, max_tris: u32) -> bool {
        self.triangle_count <= max_tris &&
        self.degenerate_tris == 0 &&
        self.has_uvs &&
        self.uv_coverage > 0.9 &&
        self.uv_overlap < 0.05 &&
        self.max_stretch < 2.0 &&
        self.has_normals &&
        self.normal_consistency > 0.95
    }

    pub fn issues(&self) -> Vec<QualityIssue> {
        let mut issues = vec![];

        if self.degenerate_tris > 0 {
            issues.push(QualityIssue {
                severity: Severity::Error,
                category: "geometry",
                message: format!("{} degenerate triangles", self.degenerate_tris),
                fix_suggestion: "Remove zero-area triangles, check for duplicate vertices".into(),
            });
        }

        if self.non_manifold_edges > 0 {
            issues.push(QualityIssue {
                severity: Severity::Warning,
                category: "topology",
                message: format!("{} non-manifold edges", self.non_manifold_edges),
                fix_suggestion: "Ensure each edge has exactly 2 adjacent faces".into(),
            });
        }

        if !self.has_uvs {
            issues.push(QualityIssue {
                severity: Severity::Error,
                category: "uvs",
                message: "No UV coordinates".into(),
                fix_suggestion: "Add UV mapping using box projection, cylindrical, or unwrap".into(),
            });
        } else if self.uv_coverage < 0.5 {
            issues.push(QualityIssue {
                severity: Severity::Warning,
                category: "uvs",
                message: format!("Low UV coverage: {:.0}%", self.uv_coverage * 100.0),
                fix_suggestion: "Expand UV islands to use more texture space".into(),
            });
        }

        if self.uv_overlap > 0.1 {
            issues.push(QualityIssue {
                severity: Severity::Warning,
                category: "uvs",
                message: format!("UV overlap: {:.0}%", self.uv_overlap * 100.0),
                fix_suggestion: "Separate overlapping UV islands".into(),
            });
        }

        if self.max_stretch > 2.0 {
            issues.push(QualityIssue {
                severity: Severity::Warning,
                category: "uvs",
                message: format!("High UV stretch: {:.1}x", self.max_stretch),
                fix_suggestion: "Add more UV seams or relax UV islands".into(),
            });
        }

        if !self.watertight {
            issues.push(QualityIssue {
                severity: Severity::Info,
                category: "topology",
                message: "Mesh is not watertight".into(),
                fix_suggestion: "Fill holes if solid appearance needed".into(),
            });
        }

        issues
    }

    pub fn score(&self) -> f32 {
        let no_errors = self.degenerate_tris == 0 && self.has_uvs && self.has_normals;
        if !no_errors { return 0.0; }

        let weights = [
            (self.uv_coverage, 0.25),
            (1.0 - self.uv_overlap, 0.15),
            ((2.0 - self.max_stretch).max(0.0) / 2.0, 0.15),
            (self.normal_consistency, 0.15),
            (if self.watertight { 1.0 } else { 0.7 }, 0.1),
            (if self.non_manifold_edges == 0 { 1.0 } else { 0.5 }, 0.1),
            (1.0 - (self.center_offset / 10.0).min(1.0), 0.1),
        ];

        weights.iter().map(|(v, w)| v * w).sum()
    }
}

fn count_degenerate_triangles(mesh: &Mesh) -> u32 {
    let mut count = 0;
    for tri in mesh.triangles.chunks(3) {
        let v0 = mesh.vertices[tri[0] as usize];
        let v1 = mesh.vertices[tri[1] as usize];
        let v2 = mesh.vertices[tri[2] as usize];

        // Check for zero area
        let edge1 = [v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]];
        let edge2 = [v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]];
        let cross = [
            edge1[1] * edge2[2] - edge1[2] * edge2[1],
            edge1[2] * edge2[0] - edge1[0] * edge2[2],
            edge1[0] * edge2[1] - edge1[1] * edge2[0],
        ];
        let area_sq = cross[0] * cross[0] + cross[1] * cross[1] + cross[2] * cross[2];

        if area_sq < 1e-10 {
            count += 1;
        }
    }
    count
}
```

---

## Animation Quality Heuristics

Based on the 12 Principles of Animation.

### Metrics

```rust
pub struct AnimationQuality {
    // Timing
    pub total_frames: u32,
    pub fps: u32,
    pub duration_seconds: f32,

    // Principles
    pub has_anticipation: bool,
    pub anticipation_frames: u32,
    pub has_follow_through: bool,
    pub follow_through_frames: u32,
    pub uses_arcs: bool,
    pub arc_smoothness: f32,
    pub has_exaggeration: bool,
    pub exaggeration_amount: f32,
    pub timing_variation: f32,    // 0 = robotic, 1 = organic

    // Technical
    pub loops_cleanly: bool,
    pub root_motion_distance: f32,
    pub bone_count: u32,
    pub keyframe_count: u32,
}
```

### Animation Principle Thresholds

| Principle | Minimum | Good | Excellent |
|-----------|---------|------|-----------|
| anticipation_frames | 2 | 4-6 | 6-10 |
| follow_through_frames | 2 | 3-5 | 5-8 |
| arc_smoothness | 0.5 | 0.7 | 0.9 |
| exaggeration_amount | 0.1 | 0.2 | 0.3 |
| timing_variation | 0.1 | 0.3 | 0.5 |

### Implementation

```rust
impl AnimationQuality {
    pub fn analyze(anim: &Animation) -> Self {
        Self {
            total_frames: anim.frames.len() as u32,
            fps: anim.fps,
            duration_seconds: anim.frames.len() as f32 / anim.fps as f32,

            has_anticipation: detect_anticipation(anim),
            anticipation_frames: count_anticipation_frames(anim),
            has_follow_through: detect_follow_through(anim),
            follow_through_frames: count_follow_through_frames(anim),
            uses_arcs: detect_arc_motion(anim),
            arc_smoothness: calculate_arc_smoothness(anim),
            has_exaggeration: detect_exaggeration(anim),
            exaggeration_amount: calculate_exaggeration(anim),
            timing_variation: calculate_timing_variation(anim),

            loops_cleanly: check_loop_continuity(anim),
            root_motion_distance: calculate_root_motion(anim),
            bone_count: anim.bones.len() as u32,
            keyframe_count: count_keyframes(anim),
        }
    }

    pub fn passes_for_type(&self, anim_type: AnimationType) -> bool {
        match anim_type {
            AnimationType::Idle => {
                self.loops_cleanly &&
                self.duration_seconds >= 1.0 &&
                self.timing_variation > 0.1
            }
            AnimationType::Walk => {
                self.loops_cleanly &&
                self.uses_arcs &&
                self.has_follow_through &&
                self.root_motion_distance > 0.5
            }
            AnimationType::Attack => {
                self.has_anticipation &&
                self.has_follow_through &&
                self.has_exaggeration &&
                self.anticipation_frames >= 2
            }
            AnimationType::Jump => {
                self.has_anticipation &&
                self.has_exaggeration &&
                self.uses_arcs
            }
        }
    }

    pub fn issues(&self) -> Vec<QualityIssue> {
        let mut issues = vec![];

        if !self.loops_cleanly {
            issues.push(QualityIssue {
                severity: Severity::Warning,
                category: "looping",
                message: "Animation does not loop cleanly".into(),
                fix_suggestion: "Ensure first and last frames match, or add transition frames".into(),
            });
        }

        if !self.has_anticipation && self.duration_seconds > 0.3 {
            issues.push(QualityIssue {
                severity: Severity::Info,
                category: "principles",
                message: "No anticipation detected".into(),
                fix_suggestion: "Add a wind-up or preparation phase before main action".into(),
            });
        }

        if !self.uses_arcs {
            issues.push(QualityIssue {
                severity: Severity::Info,
                category: "principles",
                message: "Motion appears linear rather than arced".into(),
                fix_suggestion: "Adjust keyframes to create curved motion paths".into(),
            });
        }

        if self.timing_variation < 0.1 {
            issues.push(QualityIssue {
                severity: Severity::Info,
                category: "timing",
                message: "Robotic timing - no ease in/out".into(),
                fix_suggestion: "Add acceleration/deceleration to keyframes".into(),
            });
        }

        if self.arc_smoothness < 0.5 {
            issues.push(QualityIssue {
                severity: Severity::Warning,
                category: "smoothness",
                message: format!("Jerky motion: {:.2} smoothness", self.arc_smoothness),
                fix_suggestion: "Add intermediate keyframes or use spline interpolation".into(),
            });
        }

        issues
    }
}

fn detect_anticipation(anim: &Animation) -> bool {
    // Check if there's a "preparation" phase at the start
    // e.g., crouch before jump, arm pull before punch
    if anim.frames.len() < 5 { return false; }

    // Look for opposite direction movement in first ~20% of frames
    let anticipation_window = (anim.frames.len() as f32 * 0.2) as usize;
    let main_direction = calculate_main_direction(anim);
    let initial_direction = calculate_direction(&anim.frames[0..anticipation_window]);

    // If initial movement is opposite to main movement, that's anticipation
    dot_product(&main_direction, &initial_direction) < -0.3
}

fn calculate_arc_smoothness(anim: &Animation) -> f32 {
    // Measure how smooth the motion curves are
    // 1.0 = perfectly smooth arcs, 0.0 = linear/jerky
    let mut total_smoothness = 0.0;
    let mut samples = 0;

    for bone in &anim.bones {
        let positions: Vec<_> = anim.frames.iter()
            .map(|f| f.bone_positions[bone.id])
            .collect();

        if positions.len() < 3 { continue; }

        // Calculate second derivative (acceleration)
        for i in 1..positions.len() - 1 {
            let accel = [
                positions[i+1][0] - 2.0 * positions[i][0] + positions[i-1][0],
                positions[i+1][1] - 2.0 * positions[i][1] + positions[i-1][1],
                positions[i+1][2] - 2.0 * positions[i][2] + positions[i-1][2],
            ];
            let accel_mag = (accel[0]*accel[0] + accel[1]*accel[1] + accel[2]*accel[2]).sqrt();
            // Smaller acceleration = smoother
            total_smoothness += 1.0 / (1.0 + accel_mag);
            samples += 1;
        }
    }

    if samples == 0 { return 1.0; }
    total_smoothness / samples as f32
}
```

---

## Sound Quality Heuristics

### Metrics

```rust
pub struct SoundQuality {
    // Format
    pub sample_rate: u32,
    pub bit_depth: u16,
    pub channels: u8,
    pub duration_seconds: f32,

    // Audio
    pub peak_amplitude: f32,     // 0-1, highest sample
    pub rms_level: f32,          // 0-1, average loudness
    pub dynamic_range: f32,      // Difference between loud and quiet
    pub has_clipping: bool,      // Peak > 1.0

    // Content
    pub attack_time: f32,        // Time to reach peak (seconds)
    pub decay_time: f32,         // Time from peak to silence
    pub has_silence: bool,       // Excessive silence at start/end
    pub silence_percent: f32,
}
```

### ZX Audio Requirements

| Requirement | Value |
|-------------|-------|
| sample_rate | 22050 Hz |
| bit_depth | 16-bit |
| channels | Mono (1) |
| max_duration | 5 seconds (SFX) |
| peak_amplitude | < 0.95 (avoid clipping) |

### Implementation

```rust
impl SoundQuality {
    pub fn analyze(audio: &AudioBuffer) -> Self {
        let samples = &audio.samples;

        Self {
            sample_rate: audio.sample_rate,
            bit_depth: audio.bit_depth,
            channels: audio.channels,
            duration_seconds: samples.len() as f32 / audio.sample_rate as f32,

            peak_amplitude: calculate_peak(samples),
            rms_level: calculate_rms(samples),
            dynamic_range: calculate_dynamic_range(samples),
            has_clipping: detect_clipping(samples),

            attack_time: calculate_attack_time(samples, audio.sample_rate),
            decay_time: calculate_decay_time(samples, audio.sample_rate),
            has_silence: detect_silence(samples),
            silence_percent: calculate_silence_percent(samples),
        }
    }

    pub fn passes_zx_requirements(&self) -> bool {
        self.sample_rate == 22050 &&
        self.bit_depth == 16 &&
        self.channels == 1 &&
        !self.has_clipping &&
        self.peak_amplitude < 0.95 &&
        self.silence_percent < 0.2
    }

    pub fn issues(&self) -> Vec<QualityIssue> {
        let mut issues = vec![];

        if self.sample_rate != 22050 {
            issues.push(QualityIssue {
                severity: Severity::Error,
                category: "format",
                message: format!("Wrong sample rate: {} Hz", self.sample_rate),
                fix_suggestion: "Resample to 22050 Hz for ZX compatibility".into(),
            });
        }

        if self.channels != 1 {
            issues.push(QualityIssue {
                severity: Severity::Error,
                category: "format",
                message: format!("Stereo audio ({} channels)", self.channels),
                fix_suggestion: "Convert to mono (mix or use left channel)".into(),
            });
        }

        if self.has_clipping {
            issues.push(QualityIssue {
                severity: Severity::Error,
                category: "audio",
                message: "Audio clipping detected".into(),
                fix_suggestion: "Reduce amplitude or apply limiting".into(),
            });
        }

        if self.peak_amplitude < 0.3 {
            issues.push(QualityIssue {
                severity: Severity::Warning,
                category: "audio",
                message: format!("Low amplitude: {:.2}", self.peak_amplitude),
                fix_suggestion: "Normalize audio to increase loudness".into(),
            });
        }

        if self.silence_percent > 0.3 {
            issues.push(QualityIssue {
                severity: Severity::Warning,
                category: "content",
                message: format!("{:.0}% silence", self.silence_percent * 100.0),
                fix_suggestion: "Trim silence from start and end".into(),
            });
        }

        if self.duration_seconds > 5.0 {
            issues.push(QualityIssue {
                severity: Severity::Warning,
                category: "duration",
                message: format!("Long SFX: {:.1}s", self.duration_seconds),
                fix_suggestion: "Consider shorter duration for memory efficiency".into(),
            });
        }

        issues
    }
}

fn calculate_peak(samples: &[f32]) -> f32 {
    samples.iter().map(|s| s.abs()).fold(0.0f32, |a, b| a.max(b))
}

fn calculate_rms(samples: &[f32]) -> f32 {
    let sum_sq: f32 = samples.iter().map(|s| s * s).sum();
    (sum_sq / samples.len() as f32).sqrt()
}

fn detect_clipping(samples: &[f32]) -> bool {
    // Check for consecutive max-value samples (clipping indicator)
    let threshold = 0.99;
    let mut consecutive = 0;

    for sample in samples {
        if sample.abs() > threshold {
            consecutive += 1;
            if consecutive > 3 {
                return true;
            }
        } else {
            consecutive = 0;
        }
    }
    false
}
```

---

## Strictness Levels

Quality checks can operate at different strictness levels:

```rust
pub enum Strictness {
    Lenient,   // Only critical errors
    Normal,    // Errors and warnings
    Strict,    // All issues including info
}

impl Strictness {
    pub fn filter_issues(&self, issues: Vec<QualityIssue>) -> Vec<QualityIssue> {
        match self {
            Strictness::Lenient => issues.into_iter()
                .filter(|i| matches!(i.severity, Severity::Error | Severity::Critical))
                .collect(),
            Strictness::Normal => issues.into_iter()
                .filter(|i| !matches!(i.severity, Severity::Info))
                .collect(),
            Strictness::Strict => issues,
        }
    }

    pub fn passes(&self, issues: &[QualityIssue]) -> bool {
        match self {
            Strictness::Lenient => !issues.iter().any(|i|
                matches!(i.severity, Severity::Critical)),
            Strictness::Normal => !issues.iter().any(|i|
                matches!(i.severity, Severity::Error | Severity::Critical)),
            Strictness::Strict => issues.is_empty(),
        }
    }
}
```

---

## Quality Report Format

Standard output format for quality assessments:

```markdown
## Quality Assessment Report

### Asset: player_character.obj
**Type:** Mesh
**Score:** 0.85 / 1.0

#### Metrics
| Metric | Value | Status |
|--------|-------|--------|
| Triangles | 420 | OK (budget: 500) |
| UV Coverage | 94% | OK |
| UV Overlap | 2% | OK |
| Degenerate Tris | 0 | OK |
| Watertight | Yes | OK |

#### Issues
| Severity | Category | Message |
|----------|----------|---------|
| Warning | uvs | High UV stretch: 1.8x |
| Info | topology | 3 non-manifold edges |

#### Suggestions
1. Consider relaxing UVs around the character's arms to reduce stretch
2. Non-manifold edges are at seam locations - acceptable for this use case

### Summary
- **Meshes:** 1 analyzed, 0 errors, 1 warning
- **Overall:** PASS (Normal strictness)
```
