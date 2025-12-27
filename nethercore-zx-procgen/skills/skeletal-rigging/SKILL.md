---
name: Skeletal Rigging for ZX
description: This skill should be used when the user asks to "rig character", "create skeleton", "bone hierarchy", "add bones", "skeleton setup", "inverse bind matrices", "bind pose", "bone weights", "skinning", "weight painting", "auto-rig", "character rigging", "armature", "joint hierarchy", "deformation bones", or mentions skeleton creation, bone weight calculation, mesh skinning, rigging procedural meshes, or setting up skeletons for animation. Provides comprehensive guidance for creating skeletal rigs and calculating bone weights for procedurally generated meshes compatible with ZX GPU skinning.
version: 1.0.0
---

# Skeletal Rigging for ZX

## Overview

Skeletal rigging prepares meshes for animation by defining bone hierarchies and vertex weights. ZX uses GPU skinning with specific constraints that rigging must respect.

**This skill covers:**
- Skeleton creation and bone hierarchy design
- Inverse bind matrix calculation
- Bone weight algorithms (distance, heat diffusion, geodesic)
- Skinned mesh vertex format
- GLTF skeleton export

**For animation generation (motion, walk cycles, IK), see the `procedural-animations` skill.**

## ZX Skeletal Constraints

| Constraint | Limit | Notes |
|------------|-------|-------|
| **Max bones** | 256 | Per skeleton, enforced by `load_skeleton()` |
| **Bones per vertex** | 4 | Uint8x4 indices + Unorm8x4 weights |
| **Matrix format** | 3x4 | Column-major, 12 floats per bone |
| **Practical limit** | 20-50 bones | Performance sweet spot |

## Bone Hierarchy Design

### Standard Humanoid Skeleton

```
Root (Hips)
├── Spine
│   ├── Chest
│   │   ├── Neck
│   │   │   └── Head
│   │   ├── LeftShoulder
│   │   │   └── LeftUpperArm
│   │   │       └── LeftLowerArm
│   │   │           └── LeftHand
│   │   └── RightShoulder
│   │       └── RightUpperArm
│   │           └── RightLowerArm
│   │               └── RightHand
├── LeftUpperLeg
│   └── LeftLowerLeg
│       └── LeftFoot
└── RightUpperLeg
    └── RightLowerLeg
        └── RightFoot
```

**Minimal humanoid:** 15-20 bones
**Detailed humanoid:** 30-50 bones (fingers, face)

### Quadruped Skeleton

```
Root (Pelvis)
├── Spine
│   ├── Chest
│   │   ├── Neck
│   │   │   └── Head
│   │   ├── LeftFrontLeg
│   │   │   └── LeftFrontLowerLeg
│   │   │       └── LeftFrontPaw
│   │   └── RightFrontLeg
│   │       └── RightFrontLowerLeg
│   │           └── RightFrontPaw
│   └── Tail1 → Tail2 → Tail3
├── LeftBackLeg
│   └── LeftBackLowerLeg
│       └── LeftBackPaw
└── RightBackLeg
    └── RightBackLowerLeg
        └── RightBackPaw
```

## Creating Skeletons Programmatically

### Bone Definition

```rust
use glam::{Vec3, Quat, Mat4};

struct Bone {
    name: String,
    parent: Option<usize>,
    local_position: Vec3,
    local_rotation: Quat,
    local_scale: Vec3,
}

struct Skeleton {
    bones: Vec<Bone>,
}

impl Skeleton {
    fn new() -> Self {
        Self { bones: Vec::new() }
    }

    fn add_bone(&mut self, name: &str, parent: Option<usize>, position: Vec3) -> usize {
        let idx = self.bones.len();
        self.bones.push(Bone {
            name: name.to_string(),
            parent,
            local_position: position,
            local_rotation: Quat::IDENTITY,
            local_scale: Vec3::ONE,
        });
        idx
    }
}
```

### Building a Skeleton

```rust
fn create_humanoid_skeleton() -> Skeleton {
    let mut skel = Skeleton::new();

    // Root
    let root = skel.add_bone("Root", None, Vec3::new(0.0, 1.0, 0.0));

    // Spine chain
    let spine = skel.add_bone("Spine", Some(root), Vec3::new(0.0, 0.2, 0.0));
    let chest = skel.add_bone("Chest", Some(spine), Vec3::new(0.0, 0.3, 0.0));
    let neck = skel.add_bone("Neck", Some(chest), Vec3::new(0.0, 0.2, 0.0));
    let head = skel.add_bone("Head", Some(neck), Vec3::new(0.0, 0.15, 0.0));

    // Left arm
    let l_shoulder = skel.add_bone("L_Shoulder", Some(chest), Vec3::new(-0.15, 0.15, 0.0));
    let l_upper_arm = skel.add_bone("L_UpperArm", Some(l_shoulder), Vec3::new(-0.1, 0.0, 0.0));
    let l_lower_arm = skel.add_bone("L_LowerArm", Some(l_upper_arm), Vec3::new(-0.25, 0.0, 0.0));
    let l_hand = skel.add_bone("L_Hand", Some(l_lower_arm), Vec3::new(-0.2, 0.0, 0.0));

    // Right arm (mirrored)
    let r_shoulder = skel.add_bone("R_Shoulder", Some(chest), Vec3::new(0.15, 0.15, 0.0));
    let r_upper_arm = skel.add_bone("R_UpperArm", Some(r_shoulder), Vec3::new(0.1, 0.0, 0.0));
    let r_lower_arm = skel.add_bone("R_LowerArm", Some(r_upper_arm), Vec3::new(0.25, 0.0, 0.0));
    let r_hand = skel.add_bone("R_Hand", Some(r_lower_arm), Vec3::new(0.2, 0.0, 0.0));

    // Legs
    let l_upper_leg = skel.add_bone("L_UpperLeg", Some(root), Vec3::new(-0.1, -0.05, 0.0));
    let l_lower_leg = skel.add_bone("L_LowerLeg", Some(l_upper_leg), Vec3::new(0.0, -0.4, 0.0));
    let l_foot = skel.add_bone("L_Foot", Some(l_lower_leg), Vec3::new(0.0, -0.4, 0.0));

    let r_upper_leg = skel.add_bone("R_UpperLeg", Some(root), Vec3::new(0.1, -0.05, 0.0));
    let r_lower_leg = skel.add_bone("R_LowerLeg", Some(r_upper_leg), Vec3::new(0.0, -0.4, 0.0));
    let r_foot = skel.add_bone("R_Foot", Some(r_lower_leg), Vec3::new(0.0, -0.4, 0.0));

    skel
}
```

## Inverse Bind Matrices

Inverse bind matrices transform vertices from mesh space to bone space. Calculated once at rig time, uploaded via `load_skeleton()`.

### Calculation

```rust
impl Skeleton {
    /// Calculate world-space bind pose for each bone
    fn calculate_bind_pose(&self) -> Vec<Mat4> {
        let mut world_transforms = vec![Mat4::IDENTITY; self.bones.len()];

        for (i, bone) in self.bones.iter().enumerate() {
            let local = Mat4::from_scale_rotation_translation(
                bone.local_scale,
                bone.local_rotation,
                bone.local_position,
            );

            world_transforms[i] = match bone.parent {
                Some(parent_idx) => world_transforms[parent_idx] * local,
                None => local,
            };
        }

        world_transforms
    }

    /// Calculate inverse bind matrices for GPU upload
    fn calculate_inverse_bind_matrices(&self) -> Vec<[f32; 12]> {
        let bind_pose = self.calculate_bind_pose();

        bind_pose.iter()
            .map(|world| {
                let inverse = world.inverse();
                mat4_to_3x4(inverse)
            })
            .collect()
    }
}

/// Convert 4x4 matrix to ZX 3x4 format (column-major)
fn mat4_to_3x4(m: Mat4) -> [f32; 12] {
    let cols = m.to_cols_array();
    [
        cols[0], cols[1], cols[2],    // X axis
        cols[4], cols[5], cols[6],    // Y axis
        cols[8], cols[9], cols[10],   // Z axis
        cols[12], cols[13], cols[14]  // Translation
    ]
}
```

## Bone Weight Calculation

Bone weights determine how much each bone influences each vertex. ZX supports up to 4 bones per vertex.

### Algorithm Selection

| Algorithm | Use Case | Complexity |
|-----------|----------|------------|
| **Distance-based** | Simple meshes, fast prototyping | O(V × B) |
| **Envelope-based** | Characters with defined segments | O(V × B) |
| **Heat diffusion** | Organic shapes, smooth falloff | O(iter × V × E) |
| **Geodesic** | Complex topology, most accurate | O(B × V log V) |

### Distance-Based (Simple)

```rust
fn calculate_bone_weights(
    vertex: Vec3,
    bones: &[Bone],
    bone_positions: &[Vec3],
    max_influences: usize,
) -> ([u8; 4], [f32; 4]) {
    let mut weights: Vec<(usize, f32)> = Vec::new();

    for (idx, pos) in bone_positions.iter().enumerate() {
        let dist = (vertex - *pos).length();
        let weight = 1.0 / (dist + 0.001);  // Inverse distance
        weights.push((idx, weight));
    }

    // Sort by weight (highest first), keep top N
    weights.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    weights.truncate(max_influences);

    // Normalize weights to sum to 1.0
    let sum: f32 = weights.iter().map(|(_, w)| w).sum();

    let mut indices = [0u8; 4];
    let mut final_weights = [0.0f32; 4];

    for (i, (idx, w)) in weights.iter().enumerate() {
        indices[i] = *idx as u8;
        final_weights[i] = if sum > 0.0 { w / sum } else { 0.0 };
    }

    (indices, final_weights)
}
```

### Envelope-Based (Better Control)

Use capsule envelopes around bones for more predictable weighting:

```rust
struct BoneEnvelope {
    bone_index: usize,
    head: Vec3,
    tail: Vec3,
    head_radius: f32,
    tail_radius: f32,
    falloff: f32,
}

fn envelope_weight(vertex: Vec3, envelope: &BoneEnvelope) -> f32 {
    let ab = envelope.tail - envelope.head;
    let ap = vertex - envelope.head;
    let t = (ap.dot(ab) / ab.length_squared()).clamp(0.0, 1.0);

    // Interpolate radius along bone
    let radius = envelope.head_radius * (1.0 - t) + envelope.tail_radius * t;

    // Distance to bone axis
    let closest = envelope.head + ab * t;
    let dist = (vertex - closest).length();

    if dist > radius {
        return 0.0;
    }

    // Smooth falloff
    let normalized = dist / radius;
    (1.0 - normalized.powf(1.0 / envelope.falloff)).max(0.0)
}
```

For advanced algorithms (heat diffusion, geodesic), see `references/bone-weight-algorithms.md`.

## Skinned Mesh Vertex Format

### Vertex Structure

```rust
struct SkinnedVertex {
    position: [f32; 3],
    normal: [f32; 3],
    uv: [f32; 2],
    bone_indices: [u8; 4],   // Up to 4 bones
    bone_weights: [f32; 4],  // Must sum to 1.0
}
```

### ZX Format Flag

```rust
const FORMAT_SKINNED: u8 = 0x08;

// Combined formats
const FORMAT_POS_NORMAL_SKINNED: u8 = NORMAL | SKINNED;           // 12
const FORMAT_POS_UV_NORMAL_SKINNED: u8 = UV | NORMAL | SKINNED;   // 13
```

### Validation

```rust
fn validate_skinned_mesh(vertices: &[SkinnedVertex], bone_count: usize) -> Result<(), String> {
    for (i, v) in vertices.iter().enumerate() {
        // Check weight sum
        let sum: f32 = v.bone_weights.iter().sum();
        if (sum - 1.0).abs() > 0.001 {
            return Err(format!("Vertex {}: weights sum to {} (should be 1.0)", i, sum));
        }

        // Check bone indices
        for (j, &idx) in v.bone_indices.iter().enumerate() {
            if v.bone_weights[j] > 0.0 && idx as usize >= bone_count {
                return Err(format!("Vertex {}: bone index {} out of range", i, idx));
            }
        }
    }
    Ok(())
}
```

## GLTF Export

Export skeleton and skinned mesh to GLTF for `nether pack`:

```rust
use gltf_json as json;

fn export_skinned_gltf(
    mesh: &SkinnedMesh,
    skeleton: &Skeleton,
    path: &str,
) -> std::io::Result<()> {
    // 1. Create node for each bone
    let joint_indices: Vec<u32> = skeleton.bones.iter()
        .enumerate()
        .map(|(i, bone)| {
            // Create node with local transform
            // Store node index as joint index
            i as u32
        })
        .collect();

    // 2. Create skin with inverse bind matrices
    let ibm = skeleton.calculate_inverse_bind_matrices();
    // Add as accessor

    // 3. Export mesh with JOINTS_0 and WEIGHTS_0 attributes
    // See references/gltf-skinned-export.md for complete code

    Ok(())
}
```

See `references/gltf-skinned-export.md` for complete GLTF export implementation.

## Python Alternative

```python
import numpy as np

def calculate_bone_weights_batch(
    vertices: np.ndarray,      # (N, 3)
    bone_positions: np.ndarray, # (B, 3)
    bone_radii: np.ndarray,     # (B,)
    max_influences: int = 4
) -> tuple[np.ndarray, np.ndarray]:
    """Calculate bone weights for all vertices."""
    n_vertices = len(vertices)

    # Distance to all bones: (N, B)
    dists = np.linalg.norm(
        vertices[:, np.newaxis, :] - bone_positions[np.newaxis, :, :],
        axis=2
    )

    # Inverse distance weights with radius falloff
    raw_weights = np.maximum(0, 1 - dists / bone_radii[np.newaxis, :])

    # Get top-k per vertex
    indices = np.zeros((n_vertices, max_influences), dtype=np.uint8)
    weights = np.zeros((n_vertices, max_influences), dtype=np.float32)

    for v in range(n_vertices):
        sorted_idx = np.argsort(-raw_weights[v])[:max_influences]
        sorted_w = raw_weights[v, sorted_idx]

        # Normalize
        if sorted_w.sum() > 0:
            sorted_w /= sorted_w.sum()

        indices[v] = sorted_idx
        weights[v] = sorted_w

    return indices, weights
```

## nether.toml Configuration

```toml
[[assets.skeletons]]
id = "humanoid_rig"
path = "assets/skeletons/humanoid.gltf"

[[assets.meshes]]
id = "character"
path = "assets/meshes/character.gltf"  # Skinned mesh
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Mesh explodes | Uninitialized bone matrices | Initialize to identity before first render |
| Vertices stuck | Weights are zero or skeleton not bound | Check `skeleton_bind()` called, weights sum to 1.0 |
| Candy wrapper twist | Too few bones at joints | Add intermediate twist bones |
| Weight bleeding | Distant bones affecting vertices | Use envelope weighting with radius limits |
| GLTF import fails | Invalid inverse bind matrices | Verify matrices are invertible |

## Additional Resources

### Reference Files

For detailed implementations:
- **`references/bone-weight-algorithms.md`** - Heat diffusion, geodesic weighting
- **`references/gltf-skinned-export.md`** - Complete GLTF export code
- **`references/skeleton-presets.md`** - Common skeleton configurations

### Related Skills

- **`procedural-animations`** - Motion generation, walk cycles, IK
- **`procedural-meshes`** - Generating animation-ready mesh topology
- **`character-pipeline`** - Full character creation workflow
