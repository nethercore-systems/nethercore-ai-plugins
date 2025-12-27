# Gap 15: Animated Character Pipeline

**Status:** `[ ]` Not Started
**Priority:** HIGH
**Plugin:** nethercore-zx-procgen
**Type:** Skill + Agent

---

## Problem

Individual skills exist but are DISCONNECTED. No unified workflow for creating animated characters.

User asks: *"Generate a humanoid character with walk animation for my ZX game."*

Currently must manually:
1. Use procedural-meshes (no guidance on animation-ready topology)
2. Somehow generate UVs (briefly mentioned)
3. Use procedural-textures (doesn't know the UV layout)
4. Use procedural-animations for skeleton (mixed with animation content)
5. Manually calculate bone weights (buried in animations skill)
6. Generate walk cycle (covered)
7. Export to GLTF with skinning (NOT documented)

## The Complete Pipeline (What Should Exist)

```
PHASE A: MESH GENERATION
  - Generate base mesh with DEFORMATION TOPOLOGY
  - Edge loops at joints (elbow, knee, shoulder)
  - Generate UVs with SEMANTIC REGIONS

PHASE B: TEXTURING
  - Read UV bounds from mesh
  - Generate albedo mapped to UV regions
  - Size to power-of-2, max 256x256 for characters

PHASE C: SKELETON CREATION
  - Define bone hierarchy (root -> spine -> limbs)
  - Position bones at joint locations
  - Calculate inverse bind matrices
  - ZX hard limit: 256 bones max (see `load_skeleton()` in zx.rs)

PHASE D: SKINNING (WEIGHT PAINTING)
  - Calculate bone weights per vertex
  - Normalize weights (sum to 1.0)
  - Limit to 4 bones per vertex (ZX requirement)

PHASE E: ANIMATION
  - Generate procedural keyframes
  - Handle looping (seamless start/end)

PHASE F: EXPORT
  - Export GLTF/GLB with all data
  - Include skeleton as GLTF skin
  - Include animation as GLTF animation

PHASE G: INTEGRATION
  - nether.toml entries for mesh, skeleton, animations, textures
```

## What's Missing Per Phase

| Phase | Current Skill | Gap |
|-------|---------------|-----|
| A: Mesh | procedural-meshes | No deformation topology guidance |
| B: Texture | procedural-textures | No UV-awareness (Gap 14) |
| C: Skeleton | procedural-animations | Mixed with animation (A2 split) |
| D: Skinning | procedural-animations | Buried, no standalone guidance |
| E: Animation | procedural-animations | Covered |
| F: Export | NONE | No GLTF skinned export docs |
| G: Integration | zx-game-development | Partial |

## Prompt for Implementation

```
Add skill "character-pipeline" to nethercore-zx-procgen. Triggers: "create
character", "animated character", "character workflow", "rigged character",
"skinned mesh". Cover the 7-phase pipeline: mesh generation (with deformation
topology), texturing (UV-aware), skeleton creation, skinning (bone weights),
animation, GLTF export, nether.toml integration. Include ZX constraints per
phase. Add quick-start for humanoid and quadruped. ~2000 words.

Add agent "character-generator" to nethercore-zx-procgen. Triggers: "generate
character", "make character", "procedural character". Agent asks questions
(character type, style, needed animations), then orchestrates the full
pipeline, producing mesh + textures + skeleton + animations + nether.toml
entries. Validates ZX compliance. Model: inherit. Tools: Read, Write, Bash,
Glob, AskUserQuestion.
```

## Technical Notes (Verified Against FFI)

**Skeleton FFI (from `nethercore/include/zx.rs` — GPU Skinning section):**
- `load_skeleton(inverse_bind_ptr, bone_count)` — Load inverse bind matrices, **max 256 bones**
- `skeleton_bind(skeleton)` — Bind skeleton for automatic inverse bind application
- `set_bones(matrices_ptr, count)` — Set current bone transforms (3×4 matrices, 12 floats each)

**Vertex Skinning (from zx-spec.md):**
- 4 bones per vertex max (Bone Indices: Uint8x4, Bone Weights: Unorm8x4)
- FORMAT_SKINNED flag (0x08) adds 8 bytes per vertex

**Mesh Formats with Skinning:**
- Format 13 (POS_UV_NORMAL_SKINNED) — Standard animated character (16+8=24 bytes)
- FORMAT_SKINNED can combine with any base format

## Code Examples

### GLTF Skinned Mesh Export

Complete guide for exporting skinned meshes with animations to GLTF:

```rust
/// GLTF Skinned Mesh Export
///
/// GLTF 2.0 stores skinned meshes using:
/// - mesh: geometry with JOINTS_0 and WEIGHTS_0 attributes
/// - skin: bone hierarchy with inverse bind matrices
/// - nodes: skeleton bone transforms (scene graph)
/// - animations: per-bone transforms over time

use gltf_json as json;

/// Complete skinned character export
pub struct GltfSkinnedExporter {
    root: json::Root,
    buffers: Vec<Vec<u8>>,
}

impl GltfSkinnedExporter {
    /// Export complete skinned character to GLTF
    pub fn export(
        mesh: &SkinnedMesh,
        skeleton: &Skeleton,
        animations: &[AnimationClip],
        textures: &[Texture],
    ) -> GltfOutput {
        let mut exporter = Self::new();

        // 1. Export skeleton as node hierarchy
        let joint_indices = exporter.export_skeleton(skeleton);

        // 2. Export skin (inverse bind matrices)
        let skin_index = exporter.export_skin(skeleton, &joint_indices);

        // 3. Export skinned mesh with bone indices/weights
        let mesh_index = exporter.export_skinned_mesh(mesh);

        // 4. Create scene node that references mesh and skin
        exporter.create_skinned_node(mesh_index, skin_index, &joint_indices);

        // 5. Export animations
        for clip in animations {
            exporter.export_animation(clip, &joint_indices);
        }

        // 6. Export textures and materials
        for texture in textures {
            exporter.export_texture(texture);
        }

        exporter.finalize()
    }

    /// Export skeleton as GLTF node hierarchy
    fn export_skeleton(&mut self, skeleton: &Skeleton) -> Vec<u32> {
        let mut joint_indices = vec![];

        for (bone_idx, bone) in skeleton.bones.iter().enumerate() {
            let node = json::Node {
                name: Some(bone.name.clone()),
                translation: Some(bone.local_position.into()),
                rotation: Some(bone.local_rotation.into()),
                scale: Some([1.0, 1.0, 1.0]),
                children: None,  // Set after all nodes created
                ..Default::default()
            };

            let node_index = self.root.nodes.len() as u32;
            self.root.nodes.push(node);
            joint_indices.push(node_index);
        }

        // Set parent-child relationships
        for (bone_idx, bone) in skeleton.bones.iter().enumerate() {
            if let Some(parent_idx) = bone.parent {
                let parent_node = &mut self.root.nodes[joint_indices[parent_idx] as usize];
                let children = parent_node.children.get_or_insert(vec![]);
                children.push(json::Index::new(joint_indices[bone_idx]));
            }
        }

        joint_indices
    }

    /// Export skin with inverse bind matrices
    fn export_skin(&mut self, skeleton: &Skeleton, joints: &[u32]) -> u32 {
        let inverse_binds: Vec<[[f32; 4]; 4]> = skeleton.bones.iter()
            .map(|bone| bone.inverse_bind_matrix)
            .collect();

        let ibm_data = bytemuck::cast_slice(&inverse_binds);
        let buffer_view_idx = self.add_buffer_view(ibm_data, None);
        let accessor_idx = self.add_accessor(
            buffer_view_idx,
            json::accessor::Type::Mat4,
            json::accessor::ComponentType::F32,
            skeleton.bones.len(),
        );

        let skin = json::Skin {
            name: Some("character_skin".to_string()),
            inverse_bind_matrices: Some(json::Index::new(accessor_idx)),
            joints: joints.iter().map(|&j| json::Index::new(j)).collect(),
            skeleton: Some(json::Index::new(joints[0])),
            ..Default::default()
        };

        let skin_idx = self.root.skins.len() as u32;
        self.root.skins.push(skin);
        skin_idx
    }

    /// Export skinned mesh with JOINTS_0 and WEIGHTS_0 attributes
    fn export_skinned_mesh(&mut self, mesh: &SkinnedMesh) -> u32 {
        // JOINTS_0 - bone indices per vertex (4 u8 values)
        let joints_view = self.add_buffer_view(
            bytemuck::cast_slice(&mesh.bone_indices),
            Some(json::buffer::Target::ArrayBuffer),
        );
        let joints_accessor = self.add_accessor(
            joints_view,
            json::accessor::Type::Vec4,
            json::accessor::ComponentType::U8,
            mesh.bone_indices.len(),
        );

        // WEIGHTS_0 - bone weights per vertex (4 f32 values, sum to 1.0)
        let weights_view = self.add_buffer_view(
            bytemuck::cast_slice(&mesh.bone_weights),
            Some(json::buffer::Target::ArrayBuffer),
        );
        let weights_accessor = self.add_accessor(
            weights_view,
            json::accessor::Type::Vec4,
            json::accessor::ComponentType::F32,
            mesh.bone_weights.len(),
        );

        // ... build primitive with POSITION, NORMAL, TEXCOORD_0, JOINTS_0, WEIGHTS_0
    }
}
```

### Skinned Vertex Data Format

```rust
/// Data format for skinned vertices (ZX compatible)
pub struct SkinnedVertex {
    pub position: [f32; 3],
    pub normal: [f32; 3],
    pub uv: [f32; 2],
    pub bone_indices: [u8; 4],   // Up to 4 bones per vertex
    pub bone_weights: [f32; 4],  // Weights sum to 1.0
}

/// Validate skinned mesh before export
pub fn validate_skinned_mesh(mesh: &SkinnedMesh) -> Result<(), Vec<String>> {
    let mut errors = vec![];

    for (idx, (indices, weights)) in mesh.bone_indices.iter()
        .zip(mesh.bone_weights.iter())
        .enumerate()
    {
        // Check weight sum
        let sum: f32 = weights.iter().sum();
        if (sum - 1.0).abs() > 0.001 {
            errors.push(format!("Vertex {}: weights sum to {} (should be 1.0)", idx, sum));
        }

        // Check for invalid bone indices
        for (i, &bone_idx) in indices.iter().enumerate() {
            if weights[i] > 0.0 && bone_idx as usize >= mesh.bone_count {
                errors.push(format!(
                    "Vertex {}: bone index {} out of range (max {})",
                    idx, bone_idx, mesh.bone_count - 1
                ));
            }
        }
    }

    if errors.is_empty() { Ok(()) } else { Err(errors) }
}
```

### GLTF Structure Reference

```
character.gltf
├── scene
│   └── node (mesh + skin reference)
│       ├── mesh: character_mesh
│       │   └── primitive
│       │       ├── POSITION
│       │       ├── NORMAL
│       │       ├── TEXCOORD_0
│       │       ├── JOINTS_0    ← Bone indices (vec4 u8)
│       │       └── WEIGHTS_0   ← Bone weights (vec4 f32)
│       └── skin: character_skin
│           ├── inverseBindMatrices (accessor)
│           ├── joints: [node0, node1, node2...]
│           └── skeleton: node0 (root)
├── nodes (bone hierarchy)
│   ├── 0: root
│   ├── 1: spine (child of 0)
│   ├── 2: head (child of 1)
│   └── ...
└── animations
    └── walk
        ├── channels (per-bone rotation/translation)
        └── samplers (time → value)
```

## Dependencies

- Gap 14 (UV-Aware Texturing) for Phase B
- A2 (Skeletal Rigging refactor) for cleaner Phase C/D

## Related Gaps

- Gap 21 (BVH/Mocap) for alternative animation source
- Gap 22 (Creative Pipeline) for style-driven character generation
