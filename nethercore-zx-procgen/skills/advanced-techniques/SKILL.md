---
name: Advanced Techniques & Decision Guides
description: This skill should be used when the user asks "which algorithm", "decision guide", "bone weight algorithm", "UV mapping technique", "when to use", "algorithm comparison", "quality benchmark", "noise function selection", "external library", "procgen library", "geodesic distance", "heat diffusion", "LSCM", "ABF++", "which noise", "Perlin vs Simplex", "Worley noise", "algorithm selection", or needs help choosing between procedural generation techniques, algorithms, or external libraries. Provides decision flowcharts, algorithm comparisons, quality benchmarks, and library recommendations for procedural asset generation.
version: 1.0.0
---

# Advanced Techniques & Decision Guides

## Overview

This skill provides decision guidance for choosing between procedural generation algorithms. Use the flowcharts and comparison tables to select the right technique for specific use cases, then consult the detailed references for implementation.

---

## Bone Weight Algorithm Selection

Choose based on mesh type and quality requirements:

```
                    What type of mesh?
                           |
        +------------------+------------------+
        v                  v                  v
    Primitive          Organic          Mechanical
   (box, sphere)      (character)        (robot)
        |                  |                  |
        v                  |                  v
    Distance               |              Envelope
     Based                 |            (Volumetric)
   Fast, simple            |             Hard edges
                           |
               +-----------+-----------+
               v                       v
           Low-medium               High
             poly?                  poly?
               |                       |
               v                       v
             Heat                  Geodesic
           Diffusion               Distance
           Good blend            Best quality
```

### Quick Comparison

| Algorithm | Complexity | Quality | Handles Concave | Smooth Transitions |
|-----------|------------|---------|-----------------|-------------------|
| Distance-based | O(n * bones) | 4/10 | No | Yes |
| Envelope | O(n * bones) | 6/10 | Yes | No |
| Heat Diffusion | O(n^2) | 8/10 | Yes | Yes |
| Geodesic Distance | O(n^2 log n) | 10/10 | Yes | Yes |

**Choose by use case:**
- **Primitives/simple shapes**: Distance-based (fast, adequate)
- **Mechanical/hard-surface**: Envelope (respects volumes, crisp edges)
- **Characters/creatures**: Heat Diffusion (smooth, topology-aware)
- **Hero assets**: Geodesic Distance (highest quality)

See `references/bone-weight-algorithms.md` for implementation details and quality validation.

---

## UV Mapping Technique Selection

Choose based on surface geometry:

```
                    What surface geometry?
                           |
    +-----------+---------++---------+-----------+
    v           v          v          v           v
  Flat      Cylinder    Sphere      Box       Complex
 (wall)      (pipe)     (ball)    (crate)   (organic)
    |           |          |          |           |
    v           v          v          v           v
 Planar    Cylinder   Spherical    Box       LSCM/
Projection Projection Projection Projection  ABF++
```

### Quick Comparison

| Projection | Best For | Distortion Type | Seam Count |
|------------|----------|-----------------|------------|
| Planar | Flat surfaces, decals | Stretching at edges | 0-1 |
| Cylindrical | Tubes, limbs, barrels | Pole pinching at caps | 1 vertical |
| Spherical | Balls, planets, heads | Severe pole pinching | 1 vertical |
| Box/Cubic | Crates, buildings | Hard edges at cube faces | 6 edges |
| LSCM | Organic, any shape | Minimal angle distortion | Auto-detected |
| ABF++ | Hard-surface, CAD | Best angle preservation | Auto-detected |

**Choose by use case:**
- **Walls/floors/decals**: Planar projection
- **Pipes/limbs/barrels**: Cylindrical projection
- **Spheres/heads/planets**: Spherical projection (accept pole distortion)
- **Crates/buildings**: Box projection
- **Organic/complex**: LSCM (most cases) or ABF++ (precision)

See `references/uv-mapping-techniques.md` for algorithm details and seam detection.

---

## Noise Function Selection

Choose based on visual characteristics needed:

```
                    What visual effect?
                           |
    +----------+----------++----------+----------+
    v          v           v           v          v
 Smooth     Faster      Cells      Layered    Domain
 organic   no grid    crystals    complex    warped
    |          |           |           |          |
    v          v           v           v          v
 Perlin    Simplex    Voronoi      FBM      Warped
  Noise     Noise      Noise     (layered)   Noise
```

### Quick Comparison

| Noise Type | Speed | Artifacts | Best For |
|------------|-------|-----------|----------|
| Perlin | Medium | Grid-aligned (visible at angles) | Classic clouds, terrain |
| Simplex | Fast | None (isotropic) | General purpose, modern default |
| Worley/Voronoi | Slow | Cell boundaries | Scales, crystals, cracks, biology |
| FBM | Slow | Depends on base | Complex terrain, realistic surfaces |
| Domain Warping | Very slow | None | Artistic effects, swirls, flames |

**Choose by use case:**
- **Default choice**: Simplex (fast, no artifacts)
- **Classic look**: Perlin (traditional, slight grid bias)
- **Cellular patterns**: Voronoi (scales, stones, cells)
- **Complex terrain**: FBM with Simplex base
- **Artistic effects**: Domain warping

See `references/noise-functions.md` for implementation and parameters.

---

## External Libraries by Ecosystem

### Rust Libraries

| Library | Purpose | Crates.io |
|---------|---------|-----------|
| `noise` | Noise functions (Perlin, Simplex, Worley) | [noise](https://crates.io/crates/noise) |
| `glam` | Math (vectors, matrices, quaternions) | [glam](https://crates.io/crates/glam) |
| `gltf` | GLTF loading/export | [gltf](https://crates.io/crates/gltf) |
| `image` | Image I/O | [image](https://crates.io/crates/image) |
| `meshopt` | Mesh optimization | [meshopt](https://crates.io/crates/meshopt) |
| `nalgebra` | Advanced linear algebra | [nalgebra](https://crates.io/crates/nalgebra) |

### Python Libraries

| Library | Purpose | PyPI |
|---------|---------|------|
| `noise` | Perlin/Simplex noise | [noise](https://pypi.org/project/noise/) |
| `trimesh` | Mesh manipulation, UV, export | [trimesh](https://pypi.org/project/trimesh/) |
| `numpy` | Numeric computation | [numpy](https://pypi.org/project/numpy/) |
| `Pillow` | Image I/O | [Pillow](https://pypi.org/project/Pillow/) |
| `scipy` | Heat equation, geodesics | [scipy](https://pypi.org/project/scipy/) |
| `pygltflib` | GLTF manipulation | [pygltflib](https://pypi.org/project/pygltflib/) |

### JavaScript/Node Libraries

| Library | Purpose | npm |
|---------|---------|-----|
| `simplex-noise` | Fast simplex noise | [simplex-noise](https://www.npmjs.com/package/simplex-noise) |
| `three` | 3D graphics, geometry | [three](https://www.npmjs.com/package/three) |
| `gl-matrix` | Math operations | [gl-matrix](https://www.npmjs.com/package/gl-matrix) |

See `references/external-libraries.md` for usage examples and recommendations.

---

## Quality Benchmarks

### Bone Weights

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Weight sum per vertex | 1.0 exactly | 0.99-1.01 | <0.99 or >1.01 |
| Max influences | <=4 | 5-6 | >6 |
| Candy wrapper score | >0.9 | 0.7-0.9 | <0.7 |
| Weight bleeding regions | 0 | 1-2 minor | >2 or major |

### UV Mapping

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Angle distortion | <5% | 5-15% | >15% |
| Area distortion | <10% | 10-25% | >25% |
| UV utilization | >70% | 50-70% | <50% |
| Texel density variance | <2x | 2-4x | >4x |

### Textures

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Seamless tile error | <1% | 1-5% | >5% |
| Noise octave count | 3-6 | 2 or 7-8 | 1 or >8 |
| Histogram spread | 60-90% range | 40-60% | <40% |

See `references/quality-benchmarks.md` for validation code and detailed thresholds.

---

## Decision Summary

### For Bone Weights:
1. Simple mesh? Use **distance-based**
2. Hard surface/robot? Use **envelope**
3. Character/organic? Use **heat diffusion**
4. Hero asset? Use **geodesic distance**

### For UV Mapping:
1. Know the shape? Use matching **projection** (planar/cylinder/sphere/box)
2. Complex shape? Use **LSCM**
3. Need precision? Use **ABF++**

### For Noise:
1. Default choice? **Simplex**
2. Cellular patterns? **Voronoi**
3. Complex surfaces? **FBM**
4. Artistic effects? **Domain warping**

---

## Additional Resources

### Reference Files

For detailed implementations and advanced techniques:
- **`references/bone-weight-algorithms.md`** - Algorithm implementations, quality validation
- **`references/uv-mapping-techniques.md`** - Projection algorithms, LSCM/ABF++ details
- **`references/noise-functions.md`** - Noise implementations, parameter tuning
- **`references/external-libraries.md`** - Library usage examples, installation
- **`references/quality-benchmarks.md`** - Validation code, numerical thresholds
