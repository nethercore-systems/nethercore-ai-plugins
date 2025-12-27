# Character Optimization Guide

Performance optimization and LOD strategies for ZX character assets.

## LOD (Level of Detail) System

### LOD Strategy Overview

```
LOD 0 (Near)    : Full detail, all animations
LOD 1 (Medium)  : Reduced poly, simplified skeleton
LOD 2 (Far)     : Billboard or minimal mesh
LOD 3 (Distant) : Sprite or hidden
```

### Creating LOD Variants

```rust
fn create_character_lods(base: &CharacterConfig) -> Vec<CharacterAsset> {
    vec![
        // LOD 0: Full detail
        create_character(base.clone()),

        // LOD 1: 50% triangles, 60% bones
        create_character(CharacterConfig {
            poly_budget: base.poly_budget / 2,
            skeleton_detail: base.skeleton_detail.reduce(),
            texture_size: base.texture_size.reduce(),
            ..base.clone()
        }),

        // LOD 2: 25% triangles, minimal skeleton
        create_character(CharacterConfig {
            poly_budget: base.poly_budget / 4,
            skeleton_detail: SkeletonDetail::Minimal,
            texture_size: TextureSize::Minimal,
            ..base.clone()
        }),
    ]
}
```

### Runtime LOD Selection

```rust
fn select_lod(distance: f32) -> usize {
    if distance < 5.0 { 0 }       // Full detail
    else if distance < 15.0 { 1 } // Medium
    else if distance < 30.0 { 2 } // Low
    else { 3 }                     // Billboard/hidden
}
```

## Mesh Optimization

### Triangle Reduction Strategies

| Technique | Reduction | Quality Impact |
|-----------|-----------|----------------|
| Remove internal faces | 10-20% | None |
| Merge coplanar faces | 5-15% | Minimal |
| Edge collapse | Variable | Depends on threshold |
| Quadric decimation | Variable | Best quality/poly ratio |

### Edge Loop Preservation

Keep edge loops at joints when reducing:

```rust
fn preserve_deformation_loops(mesh: &mut Mesh, skeleton: &Skeleton) {
    // Mark vertices near joints as protected
    let joint_positions = skeleton.get_joint_positions();
    let protected_radius = 0.1;

    for vertex in mesh.vertices_mut() {
        for joint in &joint_positions {
            if vertex.position.distance(*joint) < protected_radius {
                vertex.protected = true;
            }
        }
    }
}
```

### Optimal Topology

```
Good: Quads with edge loops at joints
      ┌───┬───┬───┐
      │   │   │   │  ← Joint edge loop
      ├───┼───┼───┤
      │   │   │   │
      └───┴───┴───┘

Bad: Random triangulation
      △ △ △ △ △
       △ △ △ △
```

## Skeleton Optimization

### Bone Reduction Table

| Full Skeleton | Reduced | Ultra-Minimal |
|---------------|---------|---------------|
| 50 bones | 25 bones | 10 bones |
| Fingers | No fingers | No hands |
| Face bones | No face | No head joints |
| Twist bones | No twist | Single segments |
| Toes | No toes | No feet |

### Bone Merging

```rust
fn merge_bone_chain(skeleton: &mut Skeleton, bones: &[&str]) {
    // Combine multiple bones into one
    // Useful for: fingers → hand, toes → foot
    let first = skeleton.find_bone(bones[0]);
    let last = skeleton.find_bone(bones.last().unwrap());

    // Create merged bone
    let merged = Bone {
        name: format!("{}_merged", bones[0]),
        parent: first.parent,
        local_position: last.world_position() - first.parent_world_position(),
        ..Default::default()
    };

    // Reassign weights from removed bones to merged
    // ...
}
```

## Texture Optimization

### Size Guidelines

| Character Type | Albedo | MRE | Total VRAM |
|----------------|--------|-----|------------|
| Swarm | 64×64 | None | 16 KB |
| Standard | 128×128 | 64×64 | 80 KB |
| Hero | 256×256 | 128×128 | 320 KB |
| Boss | 512×512 | 256×256 | 1.25 MB |

### Texture Atlas Strategy

Pack multiple characters into shared atlases:

```rust
struct CharacterAtlas {
    texture: TextureBuffer,
    regions: HashMap<String, UvRegion>,
}

fn pack_characters(characters: &[&CharacterAsset]) -> CharacterAtlas {
    let mut packer = AtlasPacker::new(512, 512);

    for character in characters {
        let region = packer.pack(&character.albedo);
        // Remap UVs to atlas region
        character.mesh.remap_uvs(region);
    }

    CharacterAtlas {
        texture: packer.finalize(),
        regions: packer.regions,
    }
}
```

### Compression

```toml
# nether.toml - enable texture compression
[[assets.textures]]
id = "characters_atlas"
path = "assets/textures/characters_atlas.png"
compression = "bc1"  # DXT1 for albedo
```

## Animation Optimization

### Keyframe Reduction

```rust
fn reduce_keyframes(animation: &mut Animation, threshold: f32) {
    // Remove keyframes that can be interpolated
    let mut i = 1;
    while i < animation.keyframes.len() - 1 {
        let prev = &animation.keyframes[i - 1];
        let curr = &animation.keyframes[i];
        let next = &animation.keyframes[i + 1];

        // Interpolate between prev and next
        let t = (curr.time - prev.time) / (next.time - prev.time);
        let interpolated = lerp_pose(&prev.pose, &next.pose, t);

        // Compare with actual keyframe
        if pose_distance(&interpolated, &curr.pose) < threshold {
            animation.keyframes.remove(i);
        } else {
            i += 1;
        }
    }
}
```

### Animation Sharing

```rust
// Share animation data between similar characters
struct AnimationLibrary {
    walk: Animation,     // Shared walk cycle
    run: Animation,      // Shared run cycle
    // Character-specific animations stored separately
}

fn apply_shared_animation(
    skeleton: &Skeleton,
    library_anim: &Animation,
    bone_mapping: &BoneMapping,
) -> Animation {
    // Retarget animation to character's skeleton
    retarget_animation(library_anim, bone_mapping)
}
```

### Baked vs. Procedural

| Type | Size | CPU Cost | Use For |
|------|------|----------|---------|
| Baked | Large | None | Complex motions |
| Procedural | None | Medium | Locomotion, idle |
| Hybrid | Small | Low | Best of both |

## Memory Budget Calculator

```rust
fn calculate_character_memory(config: &CharacterConfig) -> MemoryBudget {
    let mesh_size = config.poly_budget * 3 * 32;  // 32 bytes per vertex
    let skeleton_size = config.bone_count * 64;    // 64 bytes per bone
    let texture_size = config.texture_size.area() * 4;  // RGBA

    let anim_size: usize = config.animations.iter()
        .map(|a| a.keyframes * config.bone_count * 28)  // 28 bytes per bone per frame
        .sum();

    MemoryBudget {
        mesh: mesh_size,
        skeleton: skeleton_size,
        textures: texture_size,
        animations: anim_size,
        total: mesh_size + skeleton_size + texture_size + anim_size,
    }
}
```

## Performance Profiling

### Skinning Performance

```rust
// Measure skinning cost per character
fn profile_skinning(character: &Character) -> ProfileResult {
    let start = elapsed_time();

    for _ in 0..100 {
        calculate_bone_matrices(&character.skeleton, &character.pose);
    }

    ProfileResult {
        bone_count: character.skeleton.bones.len(),
        avg_time_ms: (elapsed_time() - start) / 100.0,
    }
}
```

### Budget Recommendations

| Screen Characters | Max Total Bones | Max Triangles |
|-------------------|-----------------|---------------|
| 1-2 | 100 | 3,000 |
| 5-10 | 200 | 5,000 |
| 20+ | 400 | 8,000 |
| 50+ (swarm) | 500 | 10,000 |

## Common Optimizations

### Instancing for Crowds

```rust
// Use same mesh/skeleton for multiple instances
fn render_crowd(template: &Character, instances: &[Transform]) {
    let mesh = template.mesh_handle;
    let skeleton = template.skeleton_handle;

    skeleton_bind(skeleton);

    for (i, transform) in instances.iter().enumerate() {
        // Each instance has unique pose but shares mesh
        let pose = calculate_crowd_pose(i, elapsed_time());
        set_bones(pose.as_ptr(), template.bone_count);

        push_translate(transform.position);
        push_rotate_y(transform.rotation);
        draw_mesh(mesh);
        pop();
    }
}
```

### Animation LOD

```rust
fn animation_update_rate(distance: f32) -> u32 {
    if distance < 10.0 { 1 }       // Every frame
    else if distance < 20.0 { 2 }  // Every 2 frames
    else if distance < 40.0 { 4 }  // Every 4 frames
    else { 8 }                      // Every 8 frames
}
```

### Bone Culling

```rust
fn cull_invisible_bones(skeleton: &mut Skeleton, camera: &Camera) {
    // Don't update bones that are behind camera or occluded
    for bone in skeleton.bones.iter_mut() {
        if !camera.frustum_contains(bone.world_position) {
            bone.skip_update = true;
        }
    }
}
```

## Quick Reference

### Optimization Checklist

- [ ] Mesh LODs created (3 levels minimum)
- [ ] Edge loops preserved at joints
- [ ] Texture atlased where possible
- [ ] Animations share keyframes
- [ ] Procedural used for locomotion
- [ ] Bone count under budget
- [ ] Memory profiled and verified
