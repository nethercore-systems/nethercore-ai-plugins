# Quality Heuristics Reference

Complete quality assessment heuristics for style-generated assets. Use these metrics for self-assessment and iterative refinement.

## Overview

Quality heuristics provide measurable criteria for evaluating generated assets. Each asset type has specific metrics with target ranges and issue detection.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

class Severity(Enum):
    INFO = "info"          # Informational, no action needed
    WARNING = "warning"    # Should be addressed but not blocking
    ERROR = "error"        # Must be fixed before use
    CRITICAL = "critical"  # Asset is unusable

@dataclass
class QualityIssue:
    severity: Severity
    category: str
    message: str
    fix_suggestion: str

class QualityAssessment(ABC):
    @abstractmethod
    def passes_minimum(self) -> bool:
        pass

    @abstractmethod
    def issues(self) -> list[QualityIssue]:
        pass

    @abstractmethod
    def score(self) -> float:  # 0.0 - 1.0
        pass

    @abstractmethod
    def suggestions(self) -> list[str]:
        pass
```

---

## Texture Quality Heuristics

### Metrics

```python
@dataclass
class TextureQuality:
    # Visual quality
    contrast: float           # 0-1, histogram spread
    noise_coherence: float    # 0-1, pattern consistency
    edge_sharpness: float     # 0-1, detail clarity
    color_variance: float     # 0-1, color richness

    # Technical quality
    tileability: float        # 0-1, edge continuity
    unique_colors: int        # Number of distinct colors
    histogram_balance: float  # 0-1, brightness distribution
    power_of_two: bool        # Dimensions are 2^n

    # Content quality
    has_alpha: bool
    alpha_coverage: float     # % of non-transparent pixels
    semantic_match: float     # How well it matches intent
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

```python
import numpy as np
from PIL import Image

def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0

def analyze_texture(image: Image.Image) -> TextureQuality:
    return TextureQuality(
        contrast=calculate_contrast(image),
        noise_coherence=calculate_coherence(image),
        edge_sharpness=calculate_sharpness(image),
        color_variance=calculate_color_variance(image),
        tileability=calculate_tileability(image),
        unique_colors=count_unique_colors(image),
        histogram_balance=calculate_histogram_balance(image),
        power_of_two=is_power_of_two(image.width) and is_power_of_two(image.height),
        has_alpha=image.mode == 'RGBA',
        alpha_coverage=calculate_alpha_coverage(image),
        semantic_match=0.0,  # Set externally
    )

def passes_minimum(quality: TextureQuality) -> bool:
    return (
        quality.contrast > 0.15 and
        quality.noise_coherence > 0.4 and
        quality.histogram_balance > 0.3 and
        quality.power_of_two
    )

def get_texture_issues(quality: TextureQuality) -> list[QualityIssue]:
    issues = []

    if quality.contrast <= 0.15:
        issues.append(QualityIssue(
            severity=Severity.WARNING,
            category="contrast",
            message=f"Low contrast: {quality.contrast:.2f}",
            fix_suggestion="Add more value variation, increase noise amplitude",
        ))

    if quality.noise_coherence <= 0.4:
        issues.append(QualityIssue(
            severity=Severity.WARNING,
            category="coherence",
            message=f"Incoherent noise: {quality.noise_coherence:.2f}",
            fix_suggestion="Increase noise scale, reduce octaves, use perlin over white noise",
        ))

    if quality.tileability <= 0.8:
        issues.append(QualityIssue(
            severity=Severity.ERROR,
            category="tiling",
            message=f"Visible seams: {quality.tileability:.2f} tileability",
            fix_suggestion="Use tileable noise, blend edges, or generate with periodic functions",
        ))

    if not quality.power_of_two:
        issues.append(QualityIssue(
            severity=Severity.ERROR,
            category="dimensions",
            message="Non-power-of-two dimensions",
            fix_suggestion="Resize to 64, 128, 256, or 512 pixels",
        ))

    if quality.unique_colors < 50:
        issues.append(QualityIssue(
            severity=Severity.INFO,
            category="colors",
            message=f"Few unique colors: {quality.unique_colors}",
            fix_suggestion="Add subtle color variation for more natural appearance",
        ))

    return issues

def calculate_texture_score(quality: TextureQuality) -> float:
    weights = [
        (quality.contrast, 0.2),
        (quality.noise_coherence, 0.15),
        (quality.edge_sharpness, 0.1),
        (quality.histogram_balance, 0.15),
        (quality.tileability, 0.2),
        (min(quality.unique_colors / 1000.0, 1.0), 0.1),
        (1.0 if quality.power_of_two else 0.0, 0.1),
    ]

    return sum(v * w for v, w in weights)

# Measurement functions
def calculate_contrast(image: Image.Image) -> float:
    data = np.array(image.convert('RGB'))
    # Calculate luminance
    lum = 0.299 * data[:,:,0] / 255.0 + 0.587 * data[:,:,1] / 255.0 + 0.114 * data[:,:,2] / 255.0
    return float(lum.max() - lum.min())

def calculate_tileability(image: Image.Image) -> float:
    data = np.array(image.convert('RGB'))
    h, w = data.shape[:2]
    total_diff = 0.0
    samples = 0

    # Compare left edge to right edge
    for y in range(h):
        left = data[y, 0]
        right = data[y, w - 1]
        total_diff += color_distance(left, right)
        samples += 1

    # Compare top edge to bottom edge
    for x in range(w):
        top = data[0, x]
        bottom = data[h - 1, x]
        total_diff += color_distance(top, bottom)
        samples += 1

    avg_diff = total_diff / samples
    return 1.0 - min(avg_diff, 1.0)

def color_distance(c1: np.ndarray, c2: np.ndarray) -> float:
    return float(np.sqrt(np.sum((c1.astype(float) - c2.astype(float)) ** 2)) / 441.67)  # max distance = sqrt(255^2 * 3)
```

---

## Mesh Quality Heuristics

### Metrics

```python
@dataclass
class MeshQuality:
    # Geometry
    vertex_count: int
    triangle_count: int
    degenerate_tris: int
    non_manifold_edges: int
    watertight: bool

    # UVs
    has_uvs: bool
    uv_coverage: float        # 0-1, how much UV space is used
    uv_overlap: float         # 0-1, overlapping UV regions
    max_stretch: float        # Max UV stretch ratio

    # Normals
    has_normals: bool
    smooth_shading: bool
    normal_consistency: float # 0-1, no flipped normals

    # Bounds
    bounds_size: tuple[float, float, float]
    center_offset: float      # Distance from origin
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

```python
import numpy as np

@dataclass
class Mesh:
    vertices: np.ndarray  # Shape: (N, 3)
    triangles: np.ndarray  # Shape: (M, 3) indices
    uvs: np.ndarray  # Shape: (N, 2)
    normals: np.ndarray  # Shape: (N, 3)

def analyze_mesh(mesh: Mesh) -> MeshQuality:
    return MeshQuality(
        vertex_count=len(mesh.vertices),
        triangle_count=len(mesh.triangles),
        degenerate_tris=count_degenerate_triangles(mesh),
        non_manifold_edges=count_non_manifold_edges(mesh),
        watertight=check_watertight(mesh),
        has_uvs=len(mesh.uvs) > 0,
        uv_coverage=calculate_uv_coverage(mesh),
        uv_overlap=calculate_uv_overlap(mesh),
        max_stretch=calculate_max_stretch(mesh),
        has_normals=len(mesh.normals) > 0,
        smooth_shading=len(mesh.normals) == len(mesh.vertices),
        normal_consistency=check_normal_consistency(mesh),
        bounds_size=calculate_bounds(mesh),
        center_offset=calculate_center_offset(mesh),
    )

def passes_for_budget(quality: MeshQuality, max_tris: int) -> bool:
    return (
        quality.triangle_count <= max_tris and
        quality.degenerate_tris == 0 and
        quality.has_uvs and
        quality.uv_coverage > 0.9 and
        quality.uv_overlap < 0.05 and
        quality.max_stretch < 2.0 and
        quality.has_normals and
        quality.normal_consistency > 0.95
    )

def get_mesh_issues(quality: MeshQuality) -> list[QualityIssue]:
    issues = []

    if quality.degenerate_tris > 0:
        issues.append(QualityIssue(
            severity=Severity.ERROR,
            category="geometry",
            message=f"{quality.degenerate_tris} degenerate triangles",
            fix_suggestion="Remove zero-area triangles, check for duplicate vertices",
        ))

    if quality.non_manifold_edges > 0:
        issues.append(QualityIssue(
            severity=Severity.WARNING,
            category="topology",
            message=f"{quality.non_manifold_edges} non-manifold edges",
            fix_suggestion="Ensure each edge has exactly 2 adjacent faces",
        ))

    if not quality.has_uvs:
        issues.append(QualityIssue(
            severity=Severity.ERROR,
            category="uvs",
            message="No UV coordinates",
            fix_suggestion="Add UV mapping using box projection, cylindrical, or unwrap",
        ))
    elif quality.uv_coverage < 0.5:
        issues.append(QualityIssue(
            severity=Severity.WARNING,
            category="uvs",
            message=f"Low UV coverage: {quality.uv_coverage * 100.0:.0f}%",
            fix_suggestion="Expand UV islands to use more texture space",
        ))

    if quality.uv_overlap > 0.1:
        issues.append(QualityIssue(
            severity=Severity.WARNING,
            category="uvs",
            message=f"UV overlap: {quality.uv_overlap * 100.0:.0f}%",
            fix_suggestion="Separate overlapping UV islands",
        ))

    if quality.max_stretch > 2.0:
        issues.append(QualityIssue(
            severity=Severity.WARNING,
            category="uvs",
            message=f"High UV stretch: {quality.max_stretch:.1f}x",
            fix_suggestion="Add more UV seams or relax UV islands",
        ))

    if not quality.watertight:
        issues.append(QualityIssue(
            severity=Severity.INFO,
            category="topology",
            message="Mesh is not watertight",
            fix_suggestion="Fill holes if solid appearance needed",
        ))

    return issues

def calculate_mesh_score(quality: MeshQuality) -> float:
    no_errors = quality.degenerate_tris == 0 and quality.has_uvs and quality.has_normals
    if not no_errors:
        return 0.0

    weights = [
        (quality.uv_coverage, 0.25),
        (1.0 - quality.uv_overlap, 0.15),
        (max(2.0 - quality.max_stretch, 0.0) / 2.0, 0.15),
        (quality.normal_consistency, 0.15),
        (1.0 if quality.watertight else 0.7, 0.1),
        (1.0 if quality.non_manifold_edges == 0 else 0.5, 0.1),
        (1.0 - min(quality.center_offset / 10.0, 1.0), 0.1),
    ]

    return sum(v * w for v, w in weights)

def count_degenerate_triangles(mesh: Mesh) -> int:
    count = 0
    for tri in mesh.triangles:
        v0 = mesh.vertices[tri[0]]
        v1 = mesh.vertices[tri[1]]
        v2 = mesh.vertices[tri[2]]

        # Check for zero area
        edge1 = v1 - v0
        edge2 = v2 - v0
        cross = np.cross(edge1, edge2)
        area_sq = np.sum(cross ** 2)

        if area_sq < 1e-10:
            count += 1

    return count
```

---

## Animation Quality Heuristics

Based on the 12 Principles of Animation.

### Metrics

```python
@dataclass
class AnimationQuality:
    # Timing
    total_frames: int
    fps: int
    duration_seconds: float

    # Principles
    has_anticipation: bool
    anticipation_frames: int
    has_follow_through: bool
    follow_through_frames: int
    uses_arcs: bool
    arc_smoothness: float
    has_exaggeration: bool
    exaggeration_amount: float
    timing_variation: float    # 0 = robotic, 1 = organic

    # Technical
    loops_cleanly: bool
    root_motion_distance: float
    bone_count: int
    keyframe_count: int
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

```python
from enum import Enum

class AnimationType(Enum):
    IDLE = "idle"
    WALK = "walk"
    ATTACK = "attack"
    JUMP = "jump"

@dataclass
class Animation:
    frames: list
    fps: int
    bones: list

def analyze_animation(anim: Animation) -> AnimationQuality:
    return AnimationQuality(
        total_frames=len(anim.frames),
        fps=anim.fps,
        duration_seconds=len(anim.frames) / anim.fps,

        has_anticipation=detect_anticipation(anim),
        anticipation_frames=count_anticipation_frames(anim),
        has_follow_through=detect_follow_through(anim),
        follow_through_frames=count_follow_through_frames(anim),
        uses_arcs=detect_arc_motion(anim),
        arc_smoothness=calculate_arc_smoothness(anim),
        has_exaggeration=detect_exaggeration(anim),
        exaggeration_amount=calculate_exaggeration(anim),
        timing_variation=calculate_timing_variation(anim),

        loops_cleanly=check_loop_continuity(anim),
        root_motion_distance=calculate_root_motion(anim),
        bone_count=len(anim.bones),
        keyframe_count=count_keyframes(anim),
    )

def passes_for_type(quality: AnimationQuality, anim_type: AnimationType) -> bool:
    checks = {
        AnimationType.IDLE: (
            quality.loops_cleanly and
            quality.duration_seconds >= 1.0 and
            quality.timing_variation > 0.1
        ),
        AnimationType.WALK: (
            quality.loops_cleanly and
            quality.uses_arcs and
            quality.has_follow_through and
            quality.root_motion_distance > 0.5
        ),
        AnimationType.ATTACK: (
            quality.has_anticipation and
            quality.has_follow_through and
            quality.has_exaggeration and
            quality.anticipation_frames >= 2
        ),
        AnimationType.JUMP: (
            quality.has_anticipation and
            quality.has_exaggeration and
            quality.uses_arcs
        ),
    }
    return checks.get(anim_type, False)

def get_animation_issues(quality: AnimationQuality) -> list[QualityIssue]:
    issues = []

    if not quality.loops_cleanly:
        issues.append(QualityIssue(
            severity=Severity.WARNING,
            category="looping",
            message="Animation does not loop cleanly",
            fix_suggestion="Ensure first and last frames match, or add transition frames",
        ))

    if not quality.has_anticipation and quality.duration_seconds > 0.3:
        issues.append(QualityIssue(
            severity=Severity.INFO,
            category="principles",
            message="No anticipation detected",
            fix_suggestion="Add a wind-up or preparation phase before main action",
        ))

    if not quality.uses_arcs:
        issues.append(QualityIssue(
            severity=Severity.INFO,
            category="principles",
            message="Motion appears linear rather than arced",
            fix_suggestion="Adjust keyframes to create curved motion paths",
        ))

    if quality.timing_variation < 0.1:
        issues.append(QualityIssue(
            severity=Severity.INFO,
            category="timing",
            message="Robotic timing - no ease in/out",
            fix_suggestion="Add acceleration/deceleration to keyframes",
        ))

    if quality.arc_smoothness < 0.5:
        issues.append(QualityIssue(
            severity=Severity.WARNING,
            category="smoothness",
            message=f"Jerky motion: {quality.arc_smoothness:.2f} smoothness",
            fix_suggestion="Add intermediate keyframes or use spline interpolation",
        ))

    return issues

def detect_anticipation(anim: Animation) -> bool:
    # Check if there's a "preparation" phase at the start
    # e.g., crouch before jump, arm pull before punch
    if len(anim.frames) < 5:
        return False

    # Look for opposite direction movement in first ~20% of frames
    anticipation_window = int(len(anim.frames) * 0.2)
    main_direction = calculate_main_direction(anim)
    initial_direction = calculate_direction(anim.frames[0:anticipation_window])

    # If initial movement is opposite to main movement, that's anticipation
    return dot_product(main_direction, initial_direction) < -0.3

def calculate_arc_smoothness(anim: Animation) -> float:
    # Measure how smooth the motion curves are
    # 1.0 = perfectly smooth arcs, 0.0 = linear/jerky
    total_smoothness = 0.0
    samples = 0

    for bone in anim.bones:
        positions = [f.bone_positions[bone.id] for f in anim.frames]

        if len(positions) < 3:
            continue

        # Calculate second derivative (acceleration)
        for i in range(1, len(positions) - 1):
            accel = np.array([
                positions[i+1][0] - 2.0 * positions[i][0] + positions[i-1][0],
                positions[i+1][1] - 2.0 * positions[i][1] + positions[i-1][1],
                positions[i+1][2] - 2.0 * positions[i][2] + positions[i-1][2],
            ])
            accel_mag = np.sqrt(np.sum(accel ** 2))
            # Smaller acceleration = smoother
            total_smoothness += 1.0 / (1.0 + accel_mag)
            samples += 1

    if samples == 0:
        return 1.0
    return total_smoothness / samples

def dot_product(a: list, b: list) -> float:
    return sum(x * y for x, y in zip(a, b))
```

---

## Sound Quality Heuristics

### Metrics

```python
@dataclass
class SoundQuality:
    # Format
    sample_rate: int
    bit_depth: int
    channels: int
    duration_seconds: float

    # Audio
    peak_amplitude: float     # 0-1, highest sample
    rms_level: float          # 0-1, average loudness
    dynamic_range: float      # Difference between loud and quiet
    has_clipping: bool        # Peak > 1.0

    # Content
    attack_time: float        # Time to reach peak (seconds)
    decay_time: float         # Time from peak to silence
    has_silence: bool         # Excessive silence at start/end
    silence_percent: float
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

```python
@dataclass
class AudioBuffer:
    samples: np.ndarray
    sample_rate: int
    bit_depth: int
    channels: int

def analyze_sound(audio: AudioBuffer) -> SoundQuality:
    samples = audio.samples

    return SoundQuality(
        sample_rate=audio.sample_rate,
        bit_depth=audio.bit_depth,
        channels=audio.channels,
        duration_seconds=len(samples) / audio.sample_rate,

        peak_amplitude=calculate_peak(samples),
        rms_level=calculate_rms(samples),
        dynamic_range=calculate_dynamic_range(samples),
        has_clipping=detect_clipping(samples),

        attack_time=calculate_attack_time(samples, audio.sample_rate),
        decay_time=calculate_decay_time(samples, audio.sample_rate),
        has_silence=detect_silence(samples),
        silence_percent=calculate_silence_percent(samples),
    )

def passes_zx_requirements(quality: SoundQuality) -> bool:
    return (
        quality.sample_rate == 22050 and
        quality.bit_depth == 16 and
        quality.channels == 1 and
        not quality.has_clipping and
        quality.peak_amplitude < 0.95 and
        quality.silence_percent < 0.2
    )

def get_sound_issues(quality: SoundQuality) -> list[QualityIssue]:
    issues = []

    if quality.sample_rate != 22050:
        issues.append(QualityIssue(
            severity=Severity.ERROR,
            category="format",
            message=f"Wrong sample rate: {quality.sample_rate} Hz",
            fix_suggestion="Resample to 22050 Hz for ZX compatibility",
        ))

    if quality.channels != 1:
        issues.append(QualityIssue(
            severity=Severity.ERROR,
            category="format",
            message=f"Stereo audio ({quality.channels} channels)",
            fix_suggestion="Convert to mono (mix or use left channel)",
        ))

    if quality.has_clipping:
        issues.append(QualityIssue(
            severity=Severity.ERROR,
            category="audio",
            message="Audio clipping detected",
            fix_suggestion="Reduce amplitude or apply limiting",
        ))

    if quality.peak_amplitude < 0.3:
        issues.append(QualityIssue(
            severity=Severity.WARNING,
            category="audio",
            message=f"Low amplitude: {quality.peak_amplitude:.2f}",
            fix_suggestion="Normalize audio to increase loudness",
        ))

    if quality.silence_percent > 0.3:
        issues.append(QualityIssue(
            severity=Severity.WARNING,
            category="content",
            message=f"{quality.silence_percent * 100.0:.0f}% silence",
            fix_suggestion="Trim silence from start and end",
        ))

    if quality.duration_seconds > 5.0:
        issues.append(QualityIssue(
            severity=Severity.WARNING,
            category="duration",
            message=f"Long SFX: {quality.duration_seconds:.1f}s",
            fix_suggestion="Consider shorter duration for memory efficiency",
        ))

    return issues

def calculate_peak(samples: np.ndarray) -> float:
    return float(np.max(np.abs(samples)))

def calculate_rms(samples: np.ndarray) -> float:
    return float(np.sqrt(np.mean(samples ** 2)))

def detect_clipping(samples: np.ndarray) -> bool:
    # Check for consecutive max-value samples (clipping indicator)
    threshold = 0.99
    consecutive = 0

    for sample in samples:
        if abs(sample) > threshold:
            consecutive += 1
            if consecutive > 3:
                return True
        else:
            consecutive = 0
    return False
```

---

## Strictness Levels

Quality checks can operate at different strictness levels:

```python
class Strictness(Enum):
    LENIENT = "lenient"   # Only critical errors
    NORMAL = "normal"     # Errors and warnings
    STRICT = "strict"     # All issues including info

def filter_issues(strictness: Strictness, issues: list[QualityIssue]) -> list[QualityIssue]:
    filters = {
        Strictness.LENIENT: lambda i: i.severity in (Severity.ERROR, Severity.CRITICAL),
        Strictness.NORMAL: lambda i: i.severity != Severity.INFO,
        Strictness.STRICT: lambda i: True,
    }
    return [i for i in issues if filters[strictness](i)]

def passes(strictness: Strictness, issues: list[QualityIssue]) -> bool:
    checks = {
        Strictness.LENIENT: lambda: not any(i.severity == Severity.CRITICAL for i in issues),
        Strictness.NORMAL: lambda: not any(i.severity in (Severity.ERROR, Severity.CRITICAL) for i in issues),
        Strictness.STRICT: lambda: len(issues) == 0,
    }
    return checks[strictness]()
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
