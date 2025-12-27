# Gap 21: BVH/Motion Capture Integration

**Status:** `[x]` Completed
**Priority:** HIGH
**Plugin:** nethercore-zx-procgen
**Type:** Skill

---

## Problem

NOT covered. Animation is purely procedural (math-based synthesis). While procedural animation is great for content, it cannot produce realistic human motion.

Professional games often use motion capture data for realism, but there is:
- No BVH file format documentation
- No motion capture database references (CMU, Mixamo, Truebones)
- No retargeting (adapting animation to different skeletons)
- No root motion extraction
- No blending between mocap and procedural

## The Motion Capture Pipeline

```
SOURCE DATA
  CMU Database: 2,605 free BVH animations
  Mixamo: Thousands of game-ready animations (via FBX)
  Truebones: Free packs with various actions
       ↓
BVH PARSING
  1. Parse HIERARCHY section (bone names, offsets)
  2. Parse MOTION section (frames, channel data)
  3. Build skeleton hierarchy with parent indices
  4. Store animation frames (positions + Euler rotations)
       ↓
RETARGETING
  1. Map source bones to target bones (name/index)
  2. Scale positions for different body proportions
  3. Apply IK for endpoint preservation (hands/feet)
  4. Extract root motion for character controller
       ↓
ZX CONVERSION
  1. Convert Euler angles → quaternions → 3x4 matrices
  2. Compute world transforms (parent × local)
  3. Output column-major 12-float arrays for set_bones()
```

## Open Source Animation Databases

### CMU Motion Capture Database
- **URL:** https://mocap.cs.cmu.edu/
- **Content:** 2,605 motions from 144 subjects
- **Format:** BVH available
- **License:** Free for research; commercial requires attribution

### Mixamo
- **URL:** https://www.mixamo.com/
- **Content:** Thousands of animations
- **Format:** FBX (convert to BVH via Blender)

### Truebones
- **URL:** https://truebones.gumroad.com/
- **Content:** Various animation packs
- **Format:** BVH

### Recommended CMU Clips for Games

| CMU Subject | Motion ID | Description | Game Use Case |
|-------------|-----------|-------------|---------------|
| 01 | 01_01 | Basic walk | Character locomotion |
| 02 | 02_01 | Run | Character sprinting |
| 05 | 05_01 | Jump | Platformer actions |
| 13 | 13_* | Martial arts | Fighting games |
| 14 | 14_* | Punching/kicking | Combat |

## BVH File Format Reference

| Section | Purpose | Notes |
|---------|---------|-------|
| HIERARCHY | Bone tree structure | Parent-child relationships |
| OFFSET | Position relative to parent | In parent's local space |
| CHANNELS | Which transforms this joint has | Root: 6 (pos+rot), others: 3 (rot only) |
| MOTION | Frame count + timing | Frame Time in seconds |

**Coordinate System:**

| Source | Up | Forward | Position Scale |
|--------|-----|---------|----------------|
| CMU | Y | -Z | Centimeters |
| ZX | Y | -Z | Meters |

**Important:** CMU data uses centimeters. Divide positions by 100 for ZX meters.

## Code Examples

### BVH Parser Core Structures

```rust
/// Channel types in BVH files
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Channel {
    Xposition, Yposition, Zposition,
    Xrotation, Yrotation, Zrotation,
}

/// A joint in the BVH skeleton hierarchy
#[derive(Debug, Clone)]
pub struct BvhJoint {
    pub name: String,
    pub offset: [f32; 3],         // Position relative to parent (rest pose)
    pub channels: Vec<Channel>,    // Which transforms this joint has
    pub children: Vec<usize>,      // Indices of child joints
    pub parent: Option<usize>,     // Index of parent joint (None for root)
}

/// A parsed BVH animation clip
#[derive(Debug, Clone)]
pub struct BvhClip {
    pub joints: Vec<BvhJoint>,
    pub frame_count: usize,
    pub frame_time: f32,           // Seconds per frame
    pub motion_data: Vec<f32>,     // Flat: frame_count * total_channels
    pub total_channels: usize,
}

/// Transform data for a single joint at a single frame
#[derive(Debug, Clone)]
pub struct JointTransform {
    pub position: [f32; 3],        // Only meaningful for root
    pub rotation: [f32; 3],        // Euler angles in degrees
}
```

### BVH Parser Implementation

```rust
impl BvhClip {
    /// Parse BVH from string content
    pub fn parse(content: &str) -> Result<Self, BvhParseError> {
        let mut lines = content.lines().peekable();

        // Skip to HIERARCHY
        while let Some(line) = lines.next() {
            if line.trim() == "HIERARCHY" { break; }
        }

        // Parse joints recursively
        let mut joints = Vec::new();
        Self::parse_joint(&mut lines, &mut joints, None)?;

        // Count total channels
        let total_channels: usize = joints.iter().map(|j| j.channels.len()).sum();

        // Find MOTION section, parse Frames: and Frame Time:
        // ... parse motion_data rows ...

        Ok(BvhClip { joints, frame_count, frame_time, motion_data, total_channels })
    }

    /// Sample animation at a specific frame
    pub fn sample_frame(&self, frame: usize) -> BvhFrame {
        let offset = frame * self.total_channels;
        let mut channel_idx = 0;
        let mut joint_transforms = Vec::with_capacity(self.joints.len());

        for joint in &self.joints {
            let mut position = [0.0f32; 3];
            let mut rotation = [0.0f32; 3];

            for channel in &joint.channels {
                let value = self.motion_data[offset + channel_idx];
                channel_idx += 1;
                match channel {
                    Channel::Xposition => position[0] = value,
                    Channel::Yposition => position[1] = value,
                    Channel::Zposition => position[2] = value,
                    Channel::Xrotation => rotation[0] = value,
                    Channel::Yrotation => rotation[1] = value,
                    Channel::Zrotation => rotation[2] = value,
                }
            }
            joint_transforms.push(JointTransform { position, rotation });
        }
        BvhFrame { joint_transforms }
    }
}
```

### BVH to ZX Bone Matrix Converter

```rust
/// Convert Euler angles (degrees, ZXY order) to quaternion [w, x, y, z]
pub fn euler_zxy_to_quat(z_deg: f32, x_deg: f32, y_deg: f32) -> [f32; 4] {
    let z = z_deg * PI / 180.0;
    let x = x_deg * PI / 180.0;
    let y = y_deg * PI / 180.0;

    let (sz, cz) = (z * 0.5).sin_cos();
    let (sx, cx) = (x * 0.5).sin_cos();
    let (sy, cy) = (y * 0.5).sin_cos();

    // ZXY order composition
    [
        cz * cx * cy + sz * sx * sy,  // w
        cz * sx * cy + sz * cx * sy,  // x
        cz * cx * sy - sz * sx * cy,  // y
        sz * cx * cy - cz * sx * sy,  // z
    ]
}

/// Convert BVH frame to ZX 3x4 bone matrices (column-major, 12 floats per bone)
pub fn bvh_frame_to_zx(
    clip: &BvhClip,
    frame: &BvhFrame,
    position_scale: f32,  // 0.01 for CMU (cm to m)
) -> Vec<[f32; 12]> {
    let mut world_transforms: Vec<[[f32; 4]; 3]> = Vec::with_capacity(clip.joints.len());

    for (i, joint) in clip.joints.iter().enumerate() {
        let jt = &frame.joint_transforms[i];

        // Build local rotation (ZXY order for CMU data)
        let local_quat = euler_zxy_to_quat(jt.rotation[2], jt.rotation[0], jt.rotation[1]);
        let local_mat3 = quat_to_mat3(local_quat);

        // Local position: rest offset + animation position
        let local_pos = [
            (joint.offset[0] + jt.position[0]) * position_scale,
            (joint.offset[1] + jt.position[1]) * position_scale,
            (joint.offset[2] + jt.position[2]) * position_scale,
        ];

        // Build 3x4 local transform, multiply with parent for world
        let world_3x4 = match joint.parent {
            Some(parent_idx) => mat3x4_multiply(&world_transforms[parent_idx], &local_3x4),
            None => local_3x4,
        };
        world_transforms.push(world_3x4);
    }

    // Convert to ZX format: column-major flat array
    world_transforms.iter()
        .map(|m| [
            m[0][0], m[1][0], m[2][0],  // X axis
            m[0][1], m[1][1], m[2][1],  // Y axis
            m[0][2], m[1][2], m[2][2],  // Z axis
            m[0][3], m[1][3], m[2][3],  // Translation
        ])
        .collect()
}
```

### Skeleton Retargeting

```rust
/// Mapping from source skeleton bones to target skeleton bones
pub struct SkeletonMap {
    pub mappings: Vec<BoneMapping>,
}

pub struct BoneMapping {
    pub source_name: String,
    pub target_index: usize,
    pub rotation_offset: [f32; 4],  // Quaternion for T-pose differences
    pub scale: f32,                  // Limb length ratio
}

impl SkeletonMap {
    /// Create mapping from CMU skeleton to custom humanoid
    pub fn cmu_to_humanoid() -> Self {
        SkeletonMap {
            mappings: vec![
                BoneMapping { source_name: "Hips".into(), target_index: 0, .. },
                BoneMapping { source_name: "Spine".into(), target_index: 1, .. },
                BoneMapping { source_name: "Head".into(), target_index: 4, .. },
                BoneMapping { source_name: "LeftArm".into(), target_index: 6, .. },
                BoneMapping { source_name: "RightArm".into(), target_index: 10, .. },
                // ... etc for all bones
            ],
        }
    }
}
```

## Prompt for Implementation

```
Add skill "mocap-integration" to nethercore-zx-procgen. Triggers: "BVH", "motion
capture", "mocap", "CMU", "Mixamo", "load animation", "parse BVH", "retarget",
"root motion", "animation database", "import animation".

Cover: BVH file format (HIERARCHY + MOTION sections, channel ordering), open source
databases (CMU with recommended clips, Mixamo workflow, Truebones), complete Rust
BVH parser (~400 lines), BVH to ZX 3x4 matrix converter, skeleton retargeting
(bone mapping, proportional scaling), root motion extraction, animation state
machine (blending, transitions), LLM semantic selection (verb → clip mapping).

Integration: Uses procedural-animations for IK, blending overlays. Output format
compatible with set_bones() FFI. Include position scale handling (CMU uses cm).

Examples: bvh-parser.rs, bvh-to-zx-converter.rs, retargeting-example.rs,
animation-state-machine.rs. ~3000 words total.
```

## Dependencies

- None

## Related Gaps

- Gap 15 (Character Pipeline) for Phase E animation integration
- A3 (Mocap Skill Refactor) related to this gap
