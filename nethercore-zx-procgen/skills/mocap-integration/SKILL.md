---
name: Motion Capture Integration
description: This skill should be used when the user asks to "load BVH", "parse BVH file", "motion capture", "mocap animation", "CMU database", "Mixamo animation", "import animation", "retarget animation", "retarget skeleton", "root motion", "animation database", "BVH format", "convert BVH", "skeleton mapping", "bone mapping", "blend mocap", "realistic animation", or mentions motion capture data, BVH files, animation databases, skeleton retargeting, or integrating captured animations with procedural systems for ZX games. Provides comprehensive guidance for parsing BVH files, accessing open-source mocap databases, retargeting to custom skeletons, and converting to ZX 3x4 bone matrices.
version: 1.0.0
---

# Motion Capture Integration

## Overview

Motion capture data provides realistic human animation that pure procedural methods cannot match. This skill covers loading BVH files, accessing open-source databases, retargeting to game skeletons, and integrating with ZX's skeletal animation system.

**Pipeline Summary:**

```
SOURCE DATA (CMU/Mixamo/Truebones)
       ↓
BVH PARSING (hierarchy + motion)
       ↓
RETARGETING (map to game skeleton)
       ↓
ZX CONVERSION (3x4 bone matrices)
       ↓
set_bones() FFI call
```

## BVH File Format

BVH (Biovision Hierarchy) is the standard motion capture format. Structure:

| Section | Content | Purpose |
|---------|---------|---------|
| `HIERARCHY` | Bone tree, offsets, channels | Skeleton definition |
| `MOTION` | Frame count, timing, channel data | Animation frames |

### Channel Order

Root typically has 6 channels (position + rotation), other joints have 3 (rotation only):

```
CHANNELS 6 Xposition Yposition Zposition Xrotation Yrotation Zrotation
CHANNELS 3 Xrotation Yrotation Zrotation
```

**Euler Rotation Order:** CMU uses ZXY (common for mocap). Apply: Z first, then X, then Y.

### Coordinate Systems

| Source | Up | Forward | Position Unit |
|--------|-----|---------|---------------|
| CMU | Y | -Z | Centimeters |
| Mixamo | Y | Z | Centimeters |
| ZX | Y | -Z | Meters |

**Scale Factor:** Divide CMU positions by 100 to convert cm → m.

## Open-Source Animation Databases

### CMU Motion Capture Database

- **URL:** https://mocap.cs.cmu.edu/
- **Motions:** 2,605 clips from 144 subjects
- **Format:** BVH available
- **License:** Free for research; commercial requires attribution

**Recommended Clips for Games:**

| Subject | Motion | Description | Use Case |
|---------|--------|-------------|----------|
| 01 | 01_01 | Basic walk | Locomotion |
| 02 | 02_01 - 02_04 | Running | Sprint cycles |
| 05 | 05_01 - 05_12 | Jumping | Platformer |
| 13 | 13_* | Martial arts | Fighting |
| 14 | 14_* | Boxing | Combat |
| 35 | 35_* | Various actions | General |
| 49 | 49_* | Sports | Athletic games |
| 85 | 85_* | Dancing | Rhythm games |

### Mixamo

- **URL:** https://www.mixamo.com/
- **Motions:** Thousands, game-ready
- **Format:** FBX (export to BVH via Blender)
- **License:** Free with Adobe account

**Blender FBX → BVH:**
```python
# Import FBX, select armature, export BVH
bpy.ops.import_scene.fbx(filepath='animation.fbx')
bpy.ops.export_anim.bvh(filepath='animation.bvh')
```

### Truebones

- **URL:** https://truebones.gumroad.com/
- **Motions:** Various free packs
- **Format:** Native BVH
- **License:** Free packs available

## BVH Parsing

Core data structures for parsing:

```rust
/// BVH channel types
#[derive(Clone, Copy)]
pub enum Channel {
    Xposition, Yposition, Zposition,
    Xrotation, Yrotation, Zrotation,
}

/// Joint in skeleton hierarchy
pub struct BvhJoint {
    pub name: String,
    pub offset: [f32; 3],
    pub channels: Vec<Channel>,
    pub parent: Option<usize>,
}

/// Parsed animation clip
pub struct BvhClip {
    pub joints: Vec<BvhJoint>,
    pub frame_count: usize,
    pub frame_time: f32,
    pub motion_data: Vec<f32>,
}
```

**Parse workflow:**
1. Parse `HIERARCHY` section recursively
2. Build joint list with parent indices
3. Count total channels
4. Parse `MOTION` header (Frames, Frame Time)
5. Read motion data as flat float array

See `references/bvh-format.md` for detailed parsing implementation.
See `examples/bvh-parser.rs` for complete working parser.

## BVH to ZX Conversion

Convert parsed BVH frames to ZX 3x4 bone matrices:

### Euler to Quaternion (ZXY Order)

```rust
pub fn euler_zxy_to_quat(rx: f32, ry: f32, rz: f32) -> [f32; 4] {
    // Convert degrees to radians
    let (sx, cx) = (rx.to_radians() * 0.5).sin_cos();
    let (sy, cy) = (ry.to_radians() * 0.5).sin_cos();
    let (sz, cz) = (rz.to_radians() * 0.5).sin_cos();

    // ZXY composition
    [
        cz*cx*cy + sz*sx*sy,  // w
        cz*sx*cy + sz*cx*sy,  // x
        cz*cx*sy - sz*sx*cy,  // y
        sz*cx*cy - cz*sx*sy,  // z
    ]
}
```

### Build World Transforms

```rust
pub fn bvh_to_zx_matrices(
    clip: &BvhClip,
    frame: usize,
    scale: f32,  // 0.01 for CMU
) -> Vec<[f32; 12]> {
    let mut world: Vec<[[f32; 4]; 3]> = Vec::new();

    for (i, joint) in clip.joints.iter().enumerate() {
        // Get frame data
        let (pos, rot) = sample_joint(clip, frame, i);

        // Build local matrix
        let local = build_local_matrix(
            joint.offset, pos, rot, scale
        );

        // Multiply by parent
        let world_mat = match joint.parent {
            Some(p) => multiply_3x4(&world[p], &local),
            None => local,
        };
        world.push(world_mat);
    }

    // Flatten to ZX format
    world.iter().map(flatten_3x4).collect()
}
```

See `examples/bvh-to-zx-converter.rs` for complete implementation.

## Skeleton Retargeting

Map source skeleton (CMU/Mixamo) to target skeleton (game character):

### Bone Mapping

```rust
pub struct BoneMapping {
    pub source: String,      // CMU bone name
    pub target: usize,       // Game bone index
    pub rotation: [f32; 4],  // T-pose correction
    pub scale: f32,          // Limb length ratio
}

/// Standard CMU to humanoid mapping
pub fn cmu_humanoid_map() -> Vec<BoneMapping> {
    vec![
        BoneMapping::new("Hips", 0, IDENTITY, 1.0),
        BoneMapping::new("Spine", 1, IDENTITY, 1.0),
        BoneMapping::new("Spine1", 2, IDENTITY, 1.0),
        BoneMapping::new("Neck", 3, IDENTITY, 1.0),
        BoneMapping::new("Head", 4, IDENTITY, 1.0),
        BoneMapping::new("LeftShoulder", 5, IDENTITY, 1.0),
        BoneMapping::new("LeftArm", 6, IDENTITY, 1.0),
        // ... etc
    ]
}
```

### Proportional Scaling

Adjust for different body proportions:

```rust
fn retarget_limb(
    source_pose: &JointTransform,
    limb_ratio: f32,  // target_length / source_length
) -> JointTransform {
    JointTransform {
        position: [
            source_pose.position[0] * limb_ratio,
            source_pose.position[1] * limb_ratio,
            source_pose.position[2] * limb_ratio,
        ],
        rotation: source_pose.rotation,
    }
}
```

See `references/retargeting.md` for advanced techniques.

## Root Motion Extraction

Extract character movement from hip bone for controller integration:

```rust
pub struct RootMotion {
    pub position_delta: [f32; 3],
    pub rotation_delta: [f32; 4],
}

pub fn extract_root_motion(
    clip: &BvhClip,
    frame: usize,
    scale: f32,
) -> RootMotion {
    let curr = sample_root(clip, frame);
    let prev = sample_root(clip, frame.saturating_sub(1));

    RootMotion {
        position_delta: [
            (curr.pos[0] - prev.pos[0]) * scale,
            (curr.pos[1] - prev.pos[1]) * scale,
            (curr.pos[2] - prev.pos[2]) * scale,
        ],
        rotation_delta: quat_diff(prev.rot, curr.rot),
    }
}
```

**In-place conversion:** Zero out root XZ position to keep character stationary.

## Animation State Machine

Blend mocap clips with procedural overlays:

```rust
pub struct AnimState {
    pub clip: BvhClip,
    pub time: f32,
    pub speed: f32,
    pub looping: bool,
}

pub struct AnimController {
    current: AnimState,
    blend_target: Option<AnimState>,
    blend_progress: f32,
    blend_duration: f32,
}

impl AnimController {
    pub fn transition(&mut self, clip: BvhClip, duration: f32) {
        self.blend_target = Some(AnimState::new(clip));
        self.blend_duration = duration;
        self.blend_progress = 0.0;
    }

    pub fn update(&mut self, dt: f32) -> Vec<[f32; 12]> {
        self.current.time += dt * self.current.speed;

        let base = sample_clip(&self.current);

        if let Some(ref mut target) = self.blend_target {
            target.time += dt * target.speed;
            let next = sample_clip(target);

            self.blend_progress += dt / self.blend_duration;
            if self.blend_progress >= 1.0 {
                self.current = self.blend_target.take().unwrap();
                return next;
            }

            blend_poses(&base, &next, self.blend_progress)
        } else {
            base
        }
    }
}
```

See `references/state-machine.md` for complete blending logic.

## Semantic Clip Selection

Map natural language to animation clips:

```rust
/// Verb → CMU clip mapping
pub fn semantic_select(action: &str) -> Option<&'static str> {
    match action.to_lowercase().as_str() {
        "walk" | "walking" => Some("01_01"),
        "run" | "running" | "sprint" => Some("02_01"),
        "jump" | "jumping" | "leap" => Some("05_01"),
        "punch" | "punching" | "jab" => Some("14_01"),
        "kick" | "kicking" => Some("14_06"),
        "wave" | "waving" | "greeting" => Some("35_02"),
        "dance" | "dancing" => Some("85_01"),
        _ => None,
    }
}
```

## Integration with Procedural Animations

Combine mocap base with procedural overlays:

```rust
fn final_pose(
    mocap_bones: &[[f32; 12]],
    ik_targets: &IkTargets,
    procedural_overlay: &BonePose,
) -> Vec<[f32; 12]> {
    let mut result = mocap_bones.to_vec();

    // Apply foot IK for terrain adaptation
    apply_foot_ik(&mut result, ik_targets);

    // Add procedural overlay (head look-at, breathing)
    blend_additive(&mut result, procedural_overlay);

    result
}
```

Uses `procedural-animations` skill for IK systems.

## Additional Resources

### Reference Files
- **`references/bvh-format.md`** - Complete BVH format specification
- **`references/mocap-databases.md`** - Database URLs and clip catalogs
- **`references/retargeting.md`** - Advanced skeleton mapping
- **`references/state-machine.md`** - Animation blending system

### Example Files
- **`examples/bvh-parser.rs`** - Complete BVH parser (~400 lines)
- **`examples/bvh-to-zx-converter.rs`** - ZX matrix conversion
- **`examples/retargeting-example.rs`** - CMU to custom skeleton
- **`examples/animation-state-machine.rs`** - Clip blending system
