---
name: Procedural Animation Generation
description: This skill should be used when the user asks to "generate animation", "create walk cycle", "procedural walk", "idle animation", "attack animation", "skeletal animation", "bone weights", "skinning", "rig character", "animate tree", "vehicle suspension", "robot animation", "rigid body animation", "inverse kinematics", "IK system", "animation blending", "procedural motion", "animate mesh", or mentions animation generation, skeletal rigging, bone weight painting, character locomotion, creature animation, or procedural movement for games. Provides comprehensive guidance for generating procedural animations including skeletal, rigid body, and transform-based systems.
version: 2.0.0
---

# Procedural Animation Generation

## Overview

Procedural animations enable infinite variation, runtime responsiveness, and reduced asset size. ZX supports three animation paradigms:

| Type | Use Case | ZX API |
|------|----------|--------|
| **Transform-based** | Simple oscillations, rotations, bounces | `push_translate`, `push_rotate_*`, `push_scale` |
| **Skeletal/Skinned** | Characters, creatures, deformable meshes | `load_skeleton`, `set_bones`, skinned mesh format |
| **Rigid Body** | Vehicles, robots, mechanical objects | Hierarchical transforms, no skinning |

## ZX Skeletal Animation System

ZX uses GPU skinning with 3x4 bone matrices (12 floats per bone, column-major). The pipeline:

1. **Skinned Mesh**: Vertices have bone indices (up to 4) and weights
2. **Skeleton**: Inverse bind matrices loaded once in `init()`
3. **Bone Transforms**: Updated per-frame via `set_bones()`

### Mesh Format

```rust
// Vertex format flag for skinned meshes
const FORMAT_SKINNED: u8 = 8;  // Add bone indices/weights

// Combined with others
const FORMAT_UV_NORMAL_SKINNED: u8 = UV | NORMAL | SKINNED;  // 13
```

### Skeleton Loading

```rust
// In init() - load inverse bind matrices from ROM
let skeleton = rom_skeleton_str("character_rig");
skeleton_bind(skeleton);

// In render() - provide current bone transforms
let bone_matrices: [f32; 256 * 12] = calculate_bone_transforms();
set_bones(bone_matrices.as_ptr(), bone_count);
draw_mesh(skinned_character);
```

### Bone Matrix Format

Each bone uses a 3x4 matrix (implicit `[0, 0, 0, 1]` fourth row):

```
[col0.x, col0.y, col0.z]  // X axis
[col1.x, col1.y, col1.z]  // Y axis
[col2.x, col2.y, col2.z]  // Z axis
[tx,     ty,     tz    ]  // translation
```

## Animation Categories

### Character Locomotion

Generate walk cycles, runs, and idles procedurally:

```rust
fn procedural_walk_pose(time: f32, speed: f32) -> BonePose {
    let cycle = (time * speed) % 1.0;
    let phase = cycle * 2.0 * PI;

    BonePose {
        hip_height: 0.02 * (phase * 2.0).sin().abs(),
        left_thigh: 30.0 * phase.sin(),
        right_thigh: 30.0 * (phase + PI).sin(),
        left_shin: 45.0 * (phase + PI * 0.5).sin().max(0.0),
        right_shin: 45.0 * (phase + PI * 1.5).sin().max(0.0),
        spine_twist: 5.0 * phase.sin(),
        arm_swing: 20.0,
    }
}
```

### Nature/Organic

Trees, plants, and creatures with natural motion:

```rust
fn tree_sway(time: f32, wind_strength: f32) -> f32 {
    let base = (time * 0.5).sin() * wind_strength;
    let detail = (time * 1.7).sin() * wind_strength * 0.3;
    let micro = (time * 4.3).sin() * wind_strength * 0.1;
    base + detail + micro
}
```

### Mechanical/Rigid Body

Vehicles, robots, and machinery without skinning:

```rust
fn vehicle_suspension(wheel_idx: usize, terrain_height: f32, speed: f32) -> Mat4 {
    let spring_k = 50.0;
    let damping = 0.3;
    let compression = (terrain_height - rest_height) * spring_k;
    Mat4::from_translation(Vec3::new(0.0, -compression * damping, 0.0))
}
```

## Procedural Bone Weight Generation

For procedurally generated meshes, calculate bone weights algorithmically:

### Distance-Based Weighting

```rust
fn calculate_bone_weights(
    vertex_pos: Vec3,
    bones: &[Bone],
    max_influences: usize,
) -> (Vec<u8>, Vec<f32>) {
    let mut weights: Vec<(usize, f32)> = bones.iter()
        .enumerate()
        .map(|(i, bone)| {
            let dist = (vertex_pos - bone.position).length();
            let weight = 1.0 / (dist + 0.001);
            (i, weight)
        })
        .collect();

    weights.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    weights.truncate(max_influences);

    // Normalize
    let sum: f32 = weights.iter().map(|(_, w)| w).sum();
    let indices: Vec<u8> = weights.iter().map(|(i, _)| *i as u8).collect();
    let normalized: Vec<f32> = weights.iter().map(|(_, w)| w / sum).collect();

    (indices, normalized)
}
```

### Heat Diffusion (Advanced)

For organic meshes, use heat diffusion from bones through mesh connectivity. See `references/bone-weight-generation.md`.

## Animation State Machines

Manage transitions between animation states:

```rust
enum AnimState { Idle, Walk, Run, Jump, Attack }

struct AnimController {
    current: AnimState,
    blend_time: f32,
    blend_progress: f32,
}

impl AnimController {
    fn update(&mut self, input: Input, dt: f32) -> BonePose {
        let target = self.determine_target_state(input);
        if target != self.current {
            self.start_transition(target);
        }

        let from_pose = self.sample_state(self.current);
        let to_pose = self.sample_state(target);
        blend_poses(&from_pose, &to_pose, self.blend_progress)
    }
}
```

## Inverse Kinematics

Procedural IK for foot placement, look-at, and reaching:

### Two-Bone IK (Limbs)

```rust
fn solve_two_bone_ik(
    root: Vec3,
    target: Vec3,
    bone1_len: f32,
    bone2_len: f32,
    pole: Vec3,
) -> (Quat, Quat) {
    let chain_len = bone1_len + bone2_len;
    let target_dist = (target - root).length().min(chain_len * 0.999);

    // Law of cosines for elbow angle
    let cos_angle = (bone1_len.powi(2) + bone2_len.powi(2) - target_dist.powi(2))
        / (2.0 * bone1_len * bone2_len);
    let elbow_angle = cos_angle.acos();

    // Calculate rotations (simplified)
    // See references/ik-systems.md for complete implementation
    (shoulder_rotation, elbow_rotation)
}
```

## Asset Pipeline Integration

### Generate Animation Data

```python
# Python: Generate keyframe data for nether pack
import struct

def export_animation(keyframes, path):
    with open(path, 'wb') as f:
        f.write(struct.pack('I', len(keyframes)))
        for kf in keyframes:
            f.write(struct.pack('f', kf['time']))
            f.write(struct.pack('H', kf['bone_index']))
            f.write(struct.pack('4f', *kf['rotation']))  # quaternion
            f.write(struct.pack('3f', *kf['translation']))

# Procedurally generate walk cycle
keyframes = generate_walk_cycle(bone_count=20, duration=1.0, fps=24)
export_animation(keyframes, 'assets/animations/walk.bin')
```

### nether.toml Configuration

```toml
[[assets.skeletons]]
id = "character_rig"
path = "assets/skeletons/character.gltf"

[[assets.meshes]]
id = "character"
path = "assets/meshes/character.gltf"  # Skinned mesh

[[assets.animations]]
id = "walk"
path = "assets/animations/walk.bin"
```

## Common Animation Recipes

### Breathing/Idle

```rust
let breath = 1.0 + (time * 2.0).sin() * 0.02;
push_scale(1.0, breath, 1.0);
```

### Head Look-At

```rust
fn look_at_rotation(head_pos: Vec3, target: Vec3) -> Quat {
    let dir = (target - head_pos).normalize();
    Quat::from_rotation_arc(Vec3::Z, dir)
}
```

### Tail/Rope Physics

```rust
fn update_chain(nodes: &mut [Vec3], target: Vec3, dt: f32) {
    nodes[0] = target;
    for i in 1..nodes.len() {
        let dir = (nodes[i] - nodes[i-1]).normalize();
        nodes[i] = nodes[i-1] + dir * segment_length;
    }
}
```

### Wheel Rotation

```rust
let wheel_angle = (distance_traveled / wheel_circumference) * 360.0;
push_rotate_x(wheel_angle);
```

## Export Formats

| Format | Skeleton | Animation | Notes |
|--------|----------|-----------|-------|
| **GLTF/GLB** | Yes | Yes | Recommended, full support |
| **FBX** | Yes | Yes | Good Blender support |
| **Custom Binary** | Yes | Yes | Most efficient for procgen |

## Additional Resources

### Reference Files

For detailed implementations and advanced techniques:
- **`references/skeletal-animation-api.md`** - Complete ZX skinning API reference
- **`references/bone-weight-generation.md`** - Automatic weight calculation algorithms
- **`references/animation-presets.md`** - Character and object animation templates
- **`references/rigid-body-animation.md`** - Vehicle, robot, and mechanical animation
- **`references/ik-systems.md`** - Inverse kinematics implementations

### Example Files

Working examples in `examples/`:
- **`humanoid-walk-cycle.rs`** - Procedural bipedal locomotion
- **`quadruped-locomotion.rs`** - Four-legged creature walk/run
- **`vehicle-physics.rs`** - Suspension and wheel animation
- **`tree-wind.rs`** - Organic swaying motion

### Blender Integration

Use Blender for complex rigs, export to GLTF:
```python
bpy.ops.export_scene.gltf(filepath='character.gltf', export_skins=True)
```
