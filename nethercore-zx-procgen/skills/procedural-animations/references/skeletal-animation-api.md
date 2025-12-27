# ZX Skeletal Animation API Reference

Complete reference for GPU skinning in Nethercore ZX.

## Core Concepts

### Skinned Mesh Pipeline

```
Mesh Vertices → Bone Weights → Bone Matrices → GPU Transform → Final Position
```

Each vertex stores:
- Position (3 floats)
- Normal (3 floats, optional)
- UV (2 floats, optional)
- Bone indices (4 bytes) - which bones influence this vertex
- Bone weights (4 floats) - how much each bone influences

### Coordinate System

- **Y-up, right-handed**
- **Column-major matrices** (compatible with glam/WGSL)
- **Degrees for FFI angles** (convert internally)

## FFI Functions

### load_skeleton

```rust
/// Load inverse bind matrices to GPU.
/// Call once during init() after loading skinned meshes.
///
/// # Arguments
/// * `inverse_bind_ptr` - Pointer to 3x4 matrices (12 floats per bone)
/// * `bone_count` - Number of bones (max 256)
///
/// # Returns
/// Skeleton handle (>0) on success, 0 on error.
pub fn load_skeleton(inverse_bind_ptr: *const f32, bone_count: u32) -> u32;
```

**Usage:**
```rust
// Create inverse bind matrices for a simple 3-bone chain
let inverse_binds: [[f32; 12]; 3] = [
    // Bone 0: root at origin
    [1.0, 0.0, 0.0,  0.0, 1.0, 0.0,  0.0, 0.0, 1.0,  0.0, 0.0, 0.0],
    // Bone 1: offset by 1 unit in Y
    [1.0, 0.0, 0.0,  0.0, 1.0, 0.0,  0.0, 0.0, 1.0,  0.0, -1.0, 0.0],
    // Bone 2: offset by 2 units in Y
    [1.0, 0.0, 0.0,  0.0, 1.0, 0.0,  0.0, 0.0, 1.0,  0.0, -2.0, 0.0],
];

let skeleton = unsafe {
    load_skeleton(inverse_binds.as_ptr() as *const f32, 3)
};
```

### skeleton_bind

```rust
/// Bind a skeleton for subsequent skinned mesh rendering.
///
/// # Arguments
/// * `skeleton` - Handle from load_skeleton(), or 0 to unbind
///
/// # Behavior
/// - skeleton > 0: GPU applies inverse bind matrices automatically
/// - skeleton = 0: Raw mode, set_bones() receives final matrices
pub fn skeleton_bind(skeleton: u32);
```

**Usage:**
```rust
// In init()
let skeleton = load_skeleton(...);

// In render() - bind before drawing skinned meshes
skeleton_bind(skeleton);
set_bones(current_transforms.as_ptr(), bone_count);
draw_mesh(skinned_character);

// Draw non-skinned meshes (unbind skeleton)
skeleton_bind(0);
draw_mesh(static_prop);
```

### set_bones

```rust
/// Set bone transform matrices for the current frame.
///
/// # Arguments
/// * `matrices_ptr` - Pointer to 3x4 matrices (12 floats per bone)
/// * `count` - Number of bones (max 256)
///
/// # Matrix Format (column-major)
/// [col0.x, col0.y, col0.z]  // X axis
/// [col1.x, col1.y, col1.z]  // Y axis
/// [col2.x, col2.y, col2.z]  // Z axis
/// [tx,     ty,     tz    ]  // translation
pub fn set_bones(matrices_ptr: *const f32, count: u32);
```

### rom_skeleton

```rust
/// Load skeleton from ROM data pack.
///
/// # Arguments
/// * `id_ptr` - Pointer to asset ID string
/// * `id_len` - Length of ID string
///
/// # Returns
/// Skeleton handle on success, traps on failure.
pub fn rom_skeleton(id_ptr: u32, id_len: u32) -> u32;

// Helper function
pub fn rom_skeleton_str(id: &str) -> u32 {
    unsafe { rom_skeleton(id.as_ptr() as u32, id.len() as u32) }
}
```

## Mesh Format Flags

```rust
pub mod format {
    pub const SKINNED: u8 = 8;

    // Common skinned combinations
    pub const POS_SKINNED: u8 = SKINNED;                    // 8
    pub const POS_NORMAL_SKINNED: u8 = NORMAL | SKINNED;    // 12
    pub const POS_UV_NORMAL_SKINNED: u8 = UV | NORMAL | SKINNED;  // 13
}
```

## 3x4 Matrix Operations

### Creating Bone Matrices

```rust
use glam::{Mat4, Vec3, Quat};

/// Convert glam Mat4 to 3x4 bone matrix format
fn mat4_to_3x4(m: Mat4) -> [f32; 12] {
    let cols = m.to_cols_array();
    [
        cols[0], cols[1], cols[2],   // X axis
        cols[4], cols[5], cols[6],   // Y axis
        cols[8], cols[9], cols[10],  // Z axis
        cols[12], cols[13], cols[14] // translation
    ]
}

/// Create bone matrix from transform components
fn create_bone_matrix(translation: Vec3, rotation: Quat, scale: Vec3) -> [f32; 12] {
    let m = Mat4::from_scale_rotation_translation(scale, rotation, translation);
    mat4_to_3x4(m)
}
```

### Bone Hierarchy

```rust
struct Bone {
    parent: Option<usize>,
    local_transform: Mat4,
}

struct Skeleton {
    bones: Vec<Bone>,
    inverse_bind_matrices: Vec<[f32; 12]>,
}

impl Skeleton {
    /// Calculate world-space transforms for all bones
    fn calculate_world_transforms(&self, local_poses: &[Mat4]) -> Vec<[f32; 12]> {
        let mut world_transforms = vec![Mat4::IDENTITY; self.bones.len()];

        for (i, bone) in self.bones.iter().enumerate() {
            let local = local_poses.get(i).unwrap_or(&bone.local_transform);

            world_transforms[i] = match bone.parent {
                Some(parent_idx) => world_transforms[parent_idx] * *local,
                None => *local,
            };
        }

        world_transforms.iter().map(|m| mat4_to_3x4(*m)).collect()
    }
}
```

## Complete Example: Animated Character

```rust
#![no_std]
#![no_main]

mod ffi;
use ffi::*;

static mut SKELETON: u32 = 0;
static mut CHARACTER: u32 = 0;
static mut BONE_MATRICES: [[f32; 12]; 32] = [[0.0; 12]; 32];
const BONE_COUNT: u32 = 20;

#[no_mangle]
pub extern "C" fn init() {
    unsafe {
        render_mode(2);
        set_clear_color(0x1a1a2eFF);

        // Load skeleton and skinned mesh from ROM
        SKELETON = rom_skeleton_str("humanoid_rig");
        CHARACTER = rom_mesh_str("humanoid");

        // Initialize bone matrices to identity
        for i in 0..BONE_COUNT as usize {
            BONE_MATRICES[i] = [
                1.0, 0.0, 0.0,  // X axis
                0.0, 1.0, 0.0,  // Y axis
                0.0, 0.0, 1.0,  // Z axis
                0.0, 0.0, 0.0,  // translation
            ];
        }
    }
}

#[no_mangle]
pub extern "C" fn update() {
    // Animation logic would go here
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        let time = elapsed_time();

        // Update bone transforms procedurally
        update_walk_animation(time, &mut BONE_MATRICES);

        // Setup camera
        camera_set(0.0, 1.5, 4.0, 0.0, 1.0, 0.0);
        draw_env();

        // Render skinned character
        skeleton_bind(SKELETON);
        set_bones(BONE_MATRICES.as_ptr() as *const f32, BONE_COUNT);
        draw_mesh(CHARACTER);
    }
}

fn update_walk_animation(time: f32, bones: &mut [[f32; 12]; 32]) {
    let cycle = (time * 2.0) % 1.0;  // 2 steps per second
    let phase = cycle * 2.0 * core::f32::consts::PI;

    // Bone indices (example humanoid rig)
    const ROOT: usize = 0;
    const SPINE: usize = 1;
    const L_THIGH: usize = 5;
    const R_THIGH: usize = 9;
    const L_SHIN: usize = 6;
    const R_SHIN: usize = 10;

    // Root bob
    let bob = 0.02 * (phase * 2.0).sin().abs();
    bones[ROOT][11] = bob;  // Y translation

    // Spine twist
    let twist = 5.0_f32.to_radians() * phase.sin();
    apply_rotation_y(&mut bones[SPINE], twist);

    // Left leg
    let l_thigh_angle = 30.0_f32.to_radians() * phase.sin();
    apply_rotation_x(&mut bones[L_THIGH], l_thigh_angle);

    let l_shin_angle = 45.0_f32.to_radians() * (phase + 1.57).sin().max(0.0);
    apply_rotation_x(&mut bones[L_SHIN], l_shin_angle);

    // Right leg (180° out of phase)
    let r_thigh_angle = 30.0_f32.to_radians() * (phase + 3.14).sin();
    apply_rotation_x(&mut bones[R_THIGH], r_thigh_angle);

    let r_shin_angle = 45.0_f32.to_radians() * (phase + 4.71).sin().max(0.0);
    apply_rotation_x(&mut bones[R_SHIN], r_shin_angle);
}

fn apply_rotation_x(bone: &mut [f32; 12], angle: f32) {
    let c = angle.cos();
    let s = angle.sin();
    // Apply X rotation to existing matrix
    // Y axis rotates
    bone[3] = c * bone[3] - s * bone[6];
    bone[4] = c * bone[4] - s * bone[7];
    bone[5] = c * bone[5] - s * bone[8];
    // Z axis rotates
    bone[6] = s * bone[3] + c * bone[6];
    bone[7] = s * bone[4] + c * bone[7];
    bone[8] = s * bone[5] + c * bone[8];
}

fn apply_rotation_y(bone: &mut [f32; 12], angle: f32) {
    let c = angle.cos();
    let s = angle.sin();
    // Apply Y rotation
    let x0 = bone[0]; let x1 = bone[1]; let x2 = bone[2];
    let z0 = bone[6]; let z1 = bone[7]; let z2 = bone[8];
    bone[0] = c * x0 + s * z0;
    bone[1] = c * x1 + s * z1;
    bone[2] = c * x2 + s * z2;
    bone[6] = -s * x0 + c * z0;
    bone[7] = -s * x1 + c * z1;
    bone[8] = -s * x2 + c * z2;
}
```

## Skinned Mesh Vertex Layout

When loading skinned meshes, vertex data includes:

```
Position (3 floats)     [x, y, z]
Normal (3 floats)       [nx, ny, nz]      (if FORMAT_NORMAL)
UV (2 floats)           [u, v]            (if FORMAT_UV)
Bone Indices (4 bytes)  [b0, b1, b2, b3]  (if FORMAT_SKINNED)
Bone Weights (4 floats) [w0, w1, w2, w3]  (if FORMAT_SKINNED)
```

### Generating Skinned Mesh Data

```rust
struct SkinnedVertex {
    position: [f32; 3],
    normal: [f32; 3],
    uv: [f32; 2],
    bone_indices: [u8; 4],
    bone_weights: [f32; 4],
}

fn create_skinned_mesh(vertices: &[SkinnedVertex]) -> u32 {
    // Pack vertex data
    let mut data: Vec<f32> = Vec::with_capacity(vertices.len() * 16);

    for v in vertices {
        data.extend_from_slice(&v.position);
        data.extend_from_slice(&v.normal);
        data.extend_from_slice(&v.uv);

        // Pack bone indices as f32 (GPU will interpret)
        data.push(f32::from_bits(
            (v.bone_indices[0] as u32) |
            ((v.bone_indices[1] as u32) << 8) |
            ((v.bone_indices[2] as u32) << 16) |
            ((v.bone_indices[3] as u32) << 24)
        ));

        data.extend_from_slice(&v.bone_weights);
    }

    unsafe {
        load_mesh(
            data.as_ptr(),
            vertices.len() as u32,
            format::POS_UV_NORMAL_SKINNED as u32
        )
    }
}
```

## Performance Considerations

### Bone Count Limits

- **Hardware limit**: 256 bones per skeleton
- **Practical limit**: 30-50 bones for characters
- **Performance sweet spot**: 20-30 bones

### GPU Skinning Benefits

- Vertices transformed on GPU (parallel)
- No CPU vertex processing overhead
- Supports instancing (same skeleton, different poses)

### Optimization Tips

1. **Minimize bone count**: Merge bones with identical transforms
2. **Use LOD**: Fewer bones at distance
3. **Limit influences**: 4 bones per vertex maximum
4. **Batch similar skeletons**: Reduce state changes

## Animation Blending

### Linear Blend (Lerp)

```rust
fn blend_bone_matrices(
    from: &[[f32; 12]],
    to: &[[f32; 12]],
    t: f32,
    out: &mut [[f32; 12]]
) {
    for i in 0..from.len() {
        for j in 0..12 {
            out[i][j] = from[i][j] * (1.0 - t) + to[i][j] * t;
        }
    }
}
```

### Quaternion Slerp (Better for Rotations)

For high-quality rotation blending, decompose matrices to quaternions:

```rust
fn slerp_bone_transforms(
    from: &[BonePose],
    to: &[BonePose],
    t: f32,
) -> Vec<[f32; 12]> {
    from.iter().zip(to.iter())
        .map(|(f, t_pose)| {
            let rotation = f.rotation.slerp(t_pose.rotation, t);
            let translation = f.translation.lerp(t_pose.translation, t);
            let scale = f.scale.lerp(t_pose.scale, t);
            create_bone_matrix(translation, rotation, scale)
        })
        .collect()
}
```

## Common Issues

### Issue: Mesh Explodes

**Cause**: Bone matrices not initialized or incorrect format
**Fix**: Initialize all bone matrices to identity before first render

### Issue: Vertices Not Moving

**Cause**: Skeleton not bound, or bone weights are zero
**Fix**: Call `skeleton_bind()` before `set_bones()` and `draw_mesh()`

### Issue: Twisted/Distorted Mesh

**Cause**: Incorrect bone hierarchy or inverse bind matrices
**Fix**: Verify parent-child relationships match the mesh's bind pose

### Issue: Seams at Joint Boundaries

**Cause**: Hard weight boundaries (0 or 1 only)
**Fix**: Use smooth weight falloff between bones
