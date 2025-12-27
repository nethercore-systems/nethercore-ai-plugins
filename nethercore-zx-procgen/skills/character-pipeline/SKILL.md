---
name: Animated Character Pipeline
description: This skill should be used when the user asks to "create character", "animated character", "character workflow", "rigged character", "skinned mesh", "game character", "player character", "NPC", "enemy character", "character creation", "full character pipeline", "character with animations", "walking character", "character asset", or mentions creating complete animated characters, character production workflows, or end-to-end character asset creation. Provides comprehensive guidance for the complete 7-phase character creation pipeline from mesh to in-game animation.
version: 1.0.0
---

# Animated Character Pipeline

## Overview

This skill covers the complete workflow for creating animated characters for ZX games. The pipeline integrates mesh generation, texturing, rigging, and animation into a cohesive workflow.

## The 7-Phase Pipeline

```
PHASE A: MESH GENERATION
    ↓ Deformation-ready topology
PHASE B: TEXTURING
    ↓ UV-aware albedo + material maps
PHASE C: SKELETON CREATION
    ↓ Bone hierarchy + inverse bind matrices
PHASE D: SKINNING
    ↓ Bone weights per vertex
PHASE E: ANIMATION
    ↓ Procedural or keyframed motion
PHASE F: EXPORT
    ↓ GLTF with skin + animations
PHASE G: INTEGRATION
    → nether.toml entries → ROM
```

## Phase A: Mesh Generation

Generate meshes with animation-friendly topology.

### Deformation Topology Requirements

| Feature | Requirement | Why |
|---------|-------------|-----|
| Edge loops at joints | Required | Clean bending at elbows, knees |
| Consistent vertex density | Recommended | Even deformation |
| Minimal triangles | Required | ZX poly budgets |
| Clean UVs | Required | For texturing |

### Character Poly Budgets (ZX)

| Character Type | Triangle Budget |
|----------------|-----------------|
| Swarm enemy | 100-200 |
| Standard character | 300-500 |
| Main player | 500-800 |
| Boss/hero | 800-1500 |

### Generation Example

```rust
fn generate_humanoid_mesh(
    height: f32,
    proportions: &Proportions,
) -> MeshUV {
    let mut mesh = MeshUV::new();

    // Torso - capsule with edge loops
    let torso = generate_capsule_with_loops(
        proportions.torso_width,
        proportions.torso_height,
        8,  // segments around
        4,  // vertical divisions (for spine)
    );

    // Head - sphere
    let head = generate_sphere_uv(
        proportions.head_radius,
        8, 6,
    );
    head.translate(0.0, proportions.neck_height, 0.0);

    // Arms - cylinders with elbow loops
    let arm_template = generate_arm_with_loops(
        proportions.arm_length,
        proportions.arm_radius,
    );

    // Legs - similar with knee loops
    let leg_template = generate_leg_with_loops(
        proportions.leg_length,
        proportions.leg_radius,
    );

    // Combine all parts
    mesh.combine(&torso);
    mesh.combine(&head);
    mesh.combine(&arm_template.mirror_x());  // Both arms
    mesh.combine(&leg_template.mirror_x());  // Both legs

    mesh.apply(SmoothNormals);
    mesh.scale_to_height(height);

    mesh
}
```

### Edge Loops for Joints

```rust
fn generate_capsule_with_loops(
    radius: f32,
    height: f32,
    segments: u32,
    vertical_divisions: u32,
) -> MeshUV {
    let mut mesh = MeshUV::new();

    // Add extra edge loops at key heights
    let loop_heights = [
        0.0,              // Bottom (hip)
        height * 0.3,     // Lower torso
        height * 0.6,     // Upper torso
        height * 0.8,     // Shoulders
        height,           // Top
    ];

    for (i, &h) in loop_heights.iter().enumerate() {
        add_ring(&mut mesh, radius, h, segments, i as u32);
    }

    connect_rings(&mut mesh, segments, loop_heights.len() as u32);
    mesh
}
```

## Phase B: Texturing

Generate textures that match the mesh's UV layout.

### Character Texture Workflow

```rust
fn generate_character_textures(
    mesh: &MeshUV,
    skin_color: u32,
    clothing_config: &ClothingConfig,
) -> CharacterTextures {
    // 1. Calculate optimal resolution
    let (width, height) = calculate_texture_resolution(mesh, 64.0);

    // 2. Identify UV regions
    let regions = identify_body_regions(mesh);

    // 3. Generate albedo
    let albedo = generate_albedo(
        width, height,
        &regions,
        skin_color,
        clothing_config,
    );

    // 4. Generate MRE (for Mode 2) or SSE (for Mode 3)
    let mre = generate_mre_for_character(&regions, width, height);

    CharacterTextures { albedo, mre, width, height }
}
```

### Body Region Identification

```rust
fn identify_body_regions(mesh: &MeshUV) -> BodyRegions {
    // Based on vertex Y positions and UV islands
    let islands = UvIslandMapper::from_mesh(mesh);

    BodyRegions {
        head: find_region_by_height(&islands, mesh, 0.8, 1.0),
        torso: find_region_by_height(&islands, mesh, 0.4, 0.8),
        arms: find_symmetric_regions(&islands, mesh, 0.5, 0.8),
        legs: find_region_by_height(&islands, mesh, 0.0, 0.4),
    }
}
```

### Texture Size Guidelines

| Character Type | Albedo | MRE/SSE |
|----------------|--------|---------|
| Distant/swarm | 64x64 | 32x32 |
| Standard | 128x128 | 64x64 |
| Player/hero | 256x256 | 128x128 |

## Phase C: Skeleton Creation

Create bone hierarchy matching the mesh structure.

### Standard Humanoid (20 bones)

```rust
fn create_humanoid_skeleton(mesh_height: f32) -> Skeleton {
    let scale = mesh_height / 1.8;  // Normalize to 1.8m reference

    let mut skel = Skeleton::new();

    // Core chain
    let root = skel.add_bone("Root", None, Vec3::ZERO);
    let hips = skel.add_bone("Hips", Some(root), Vec3::new(0.0, 1.0, 0.0) * scale);
    let spine = skel.add_bone("Spine", Some(hips), Vec3::new(0.0, 0.15, 0.0) * scale);
    let chest = skel.add_bone("Chest", Some(spine), Vec3::new(0.0, 0.25, 0.0) * scale);
    let neck = skel.add_bone("Neck", Some(chest), Vec3::new(0.0, 0.2, 0.0) * scale);
    let head = skel.add_bone("Head", Some(neck), Vec3::new(0.0, 0.15, 0.0) * scale);

    // Arms
    let l_shoulder = skel.add_bone("L_Shoulder", Some(chest), Vec3::new(-0.15, 0.15, 0.0) * scale);
    let l_upper = skel.add_bone("L_UpperArm", Some(l_shoulder), Vec3::new(-0.1, 0.0, 0.0) * scale);
    let l_lower = skel.add_bone("L_LowerArm", Some(l_upper), Vec3::new(-0.25, 0.0, 0.0) * scale);
    let l_hand = skel.add_bone("L_Hand", Some(l_lower), Vec3::new(-0.18, 0.0, 0.0) * scale);

    // Mirror for right arm, add legs...
    // (See skeletal-rigging skill for complete skeleton code)

    skel
}
```

### ZX Skeleton Constraints

| Constraint | Limit |
|------------|-------|
| Max bones | 256 |
| Recommended | 20-50 |
| Performance sweet spot | 25-35 |

## Phase D: Skinning

Calculate bone weights for each vertex.

### Weight Calculation

```rust
fn skin_character(
    mesh: &MeshUV,
    skeleton: &Skeleton,
) -> SkinnedMesh {
    let bone_positions = skeleton.calculate_bone_world_positions();

    // For each vertex, calculate bone influences
    let weights: Vec<([u8; 4], [f32; 4])> = mesh.positions.iter()
        .map(|pos| {
            calculate_bone_weights(
                Vec3::from(*pos),
                &bone_positions,
                4,  // Max influences
            )
        })
        .collect();

    SkinnedMesh::from_mesh_and_weights(mesh, weights)
}
```

### Validation

```rust
fn validate_skinning(skinned: &SkinnedMesh) -> Result<(), Vec<String>> {
    let mut errors = Vec::new();

    for (i, weights) in skinned.bone_weights.iter().enumerate() {
        let sum: f32 = weights.iter().sum();
        if (sum - 1.0).abs() > 0.01 {
            errors.push(format!("Vertex {}: weights sum to {}", i, sum));
        }
    }

    if errors.is_empty() { Ok(()) } else { Err(errors) }
}
```

## Phase E: Animation

Generate or apply animations to the skeleton.

### Procedural Walk Cycle

```rust
fn generate_walk_animation(
    skeleton: &Skeleton,
    duration: f32,
    fps: u32,
) -> Animation {
    let frame_count = (duration * fps as f32) as usize;
    let mut keyframes = Vec::new();

    for frame in 0..frame_count {
        let time = frame as f32 / fps as f32;
        let pose = procedural_walk_pose(time, 1.0);

        // Convert pose to bone transforms
        let transforms = apply_pose_to_skeleton(skeleton, &pose);
        keyframes.push(AnimationFrame { time, transforms });
    }

    Animation { keyframes, duration, loops: true }
}
```

### Animation Asset Creation

```rust
fn bake_procedural_animation(
    skeleton: &Skeleton,
    animation_fn: fn(f32) -> Pose,
    duration: f32,
    name: &str,
) -> AnimationAsset {
    let fps = 24;
    let frames = (duration * fps as f32) as usize;

    let keyframes: Vec<_> = (0..frames)
        .map(|f| {
            let t = f as f32 / fps as f32;
            let pose = animation_fn(t);
            (t, pose_to_bone_matrices(skeleton, &pose))
        })
        .collect();

    AnimationAsset {
        name: name.to_string(),
        keyframes,
        duration,
    }
}
```

## Phase F: Export

Export complete character to GLTF format.

### Complete Export

```rust
fn export_character(
    skinned_mesh: &SkinnedMesh,
    skeleton: &Skeleton,
    textures: &CharacterTextures,
    animations: &[Animation],
    output_path: &str,
) -> std::io::Result<()> {
    let mut exporter = GltfSkinnedExporter::new();

    // 1. Export skeleton nodes
    let joint_indices = exporter.export_skeleton(skeleton);

    // 2. Export skin with inverse bind matrices
    let skin_idx = exporter.export_skin(skeleton, &joint_indices);

    // 3. Export skinned mesh
    let mesh_idx = exporter.export_skinned_mesh(skinned_mesh);

    // 4. Create skinned node
    exporter.create_skinned_node(mesh_idx, skin_idx, &joint_indices);

    // 5. Export animations
    for anim in animations {
        exporter.export_animation(anim, &joint_indices);
    }

    // 6. Export textures
    exporter.export_texture(&textures.albedo, "albedo");
    exporter.export_texture(&textures.mre, "mre");

    // 7. Write files
    exporter.write_gltf(output_path)?;
    textures.albedo.write_png(&format!("{}_albedo.png", output_path))?;
    textures.mre.write_png(&format!("{}_mre.png", output_path))?;

    Ok(())
}
```

## Phase G: Integration

Configure nether.toml for the game.

### nether.toml Configuration

```toml
# Complete character asset set
[[assets.meshes]]
id = "player"
path = "assets/characters/player.gltf"

[[assets.skeletons]]
id = "player_rig"
path = "assets/characters/player.gltf"

[[assets.textures]]
id = "player_albedo"
path = "assets/characters/player_albedo.png"

[[assets.textures]]
id = "player_mre"
path = "assets/characters/player_mre.png"

[[assets.animations]]
id = "player_walk"
path = "assets/characters/player.gltf#walk"

[[assets.animations]]
id = "player_idle"
path = "assets/characters/player.gltf#idle"

[[assets.animations]]
id = "player_attack"
path = "assets/characters/player.gltf#attack"
```

### Runtime Usage

```rust
static mut PLAYER_MESH: u32 = 0;
static mut PLAYER_SKELETON: u32 = 0;
static mut PLAYER_TEXTURE: u32 = 0;

fn init() {
    unsafe {
        render_mode(2);

        PLAYER_MESH = rom_mesh_str("player");
        PLAYER_SKELETON = rom_skeleton_str("player_rig");
        PLAYER_TEXTURE = rom_texture_str("player_albedo");
    }
}

fn render() {
    unsafe {
        // Bind texture
        texture_bind(PLAYER_TEXTURE);

        // Bind skeleton and set bone transforms
        skeleton_bind(PLAYER_SKELETON);
        set_bones(current_pose.as_ptr(), BONE_COUNT);

        // Draw skinned mesh
        draw_mesh(PLAYER_MESH);
    }
}
```

## Quick Start Templates

### Humanoid Character

```rust
fn create_humanoid_character(config: HumanoidConfig) -> CharacterAsset {
    // A: Mesh
    let mesh = generate_humanoid_mesh(config.height, &config.proportions);

    // B: Textures
    let textures = generate_character_textures(
        &mesh,
        config.skin_color,
        &config.clothing,
    );

    // C: Skeleton
    let skeleton = create_humanoid_skeleton(config.height);

    // D: Skinning
    let skinned = skin_character(&mesh, &skeleton);

    // E: Animations
    let walk = generate_walk_animation(&skeleton, 1.0, 24);
    let idle = generate_idle_animation(&skeleton, 2.0, 12);

    // F: Export
    export_character(
        &skinned,
        &skeleton,
        &textures,
        &[walk, idle],
        "assets/characters/humanoid",
    ).unwrap();

    CharacterAsset {
        mesh: skinned,
        skeleton,
        textures,
        animations: vec![walk, idle],
    }
}
```

### Quadruped Character

```rust
fn create_quadruped_character(config: QuadrupedConfig) -> CharacterAsset {
    // A: Mesh - four-legged body
    let mesh = generate_quadruped_mesh(&config);

    // B: Textures
    let textures = generate_creature_textures(&mesh, &config.colors);

    // C: Skeleton - quadruped rig
    let skeleton = create_quadruped_skeleton(&config);

    // D: Skinning
    let skinned = skin_character(&mesh, &skeleton);

    // E: Animations - quadruped gaits
    let walk = generate_quadruped_walk(&skeleton, 1.0, 24);
    let run = generate_quadruped_run(&skeleton, 0.6, 24);

    // F: Export
    export_character(
        &skinned,
        &skeleton,
        &textures,
        &[walk, run],
        "assets/characters/quadruped",
    ).unwrap();

    CharacterAsset {
        mesh: skinned,
        skeleton,
        textures,
        animations: vec![walk, run],
    }
}
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Mesh explodes | Bone matrices uninitialized | Initialize to identity |
| Poor deformation | Missing edge loops | Add loops at joints |
| Texture seams | UV island gaps | Extend texture past UV edges |
| Weight popping | Hard weight boundaries | Use smooth falloff |
| Animation jerky | Low keyframe rate | Increase to 24+ fps |

## Additional Resources

### Reference Files

- **`references/character-presets.md`** - Pre-built character configurations
- **`references/optimization-guide.md`** - LOD and performance tips

### Related Skills

- **`procedural-meshes`** - Detailed mesh generation
- **`skeletal-rigging`** - Skeleton and weight calculation
- **`procedural-animations`** - Animation generation
- **`mesh-texturing-workflows`** - UV-aware texturing
