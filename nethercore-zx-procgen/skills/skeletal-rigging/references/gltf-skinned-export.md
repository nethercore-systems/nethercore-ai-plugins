# GLTF Skinned Mesh Export

Complete implementation for exporting skinned meshes with skeletons to GLTF format.

## GLTF Structure Overview

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
└── animations (optional)
    └── walk
        ├── channels (per-bone rotation/translation)
        └── samplers (time → value)
```

## Complete Rust Implementation

```rust
use gltf_json as json;
use std::io::Write;

pub struct GltfSkinnedExporter {
    root: json::Root,
    buffer_data: Vec<u8>,
    buffer_views: Vec<json::buffer::View>,
    accessors: Vec<json::Accessor>,
}

impl GltfSkinnedExporter {
    pub fn new() -> Self {
        Self {
            root: json::Root::default(),
            buffer_data: Vec::new(),
            buffer_views: Vec::new(),
            accessors: Vec::new(),
        }
    }

    /// Export complete skinned character to GLTF
    pub fn export(
        mesh: &SkinnedMesh,
        skeleton: &Skeleton,
        path: &str,
    ) -> std::io::Result<()> {
        let mut exporter = Self::new();

        // 1. Export skeleton as node hierarchy
        let joint_indices = exporter.export_skeleton(skeleton);

        // 2. Export skin (inverse bind matrices)
        let skin_index = exporter.export_skin(skeleton, &joint_indices);

        // 3. Export skinned mesh with bone indices/weights
        let mesh_index = exporter.export_skinned_mesh(mesh);

        // 4. Create scene node that references mesh and skin
        exporter.create_skinned_node(mesh_index, skin_index, &joint_indices);

        // 5. Write files
        exporter.write_files(path)
    }

    /// Export skeleton as GLTF node hierarchy
    fn export_skeleton(&mut self, skeleton: &Skeleton) -> Vec<u32> {
        let mut joint_indices = Vec::new();

        for bone in &skeleton.bones {
            let translation = bone.local_position;
            let rotation = bone.local_rotation;

            let node = json::Node {
                name: Some(bone.name.clone()),
                translation: Some([translation.x, translation.y, translation.z]),
                rotation: Some([rotation.x, rotation.y, rotation.z, rotation.w]),
                scale: Some([1.0, 1.0, 1.0]),
                children: None,
                mesh: None,
                skin: None,
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
                let children = parent_node.children.get_or_insert_with(Vec::new);
                children.push(json::Index::new(joint_indices[bone_idx]));
            }
        }

        joint_indices
    }

    /// Export skin with inverse bind matrices
    fn export_skin(&mut self, skeleton: &Skeleton, joints: &[u32]) -> u32 {
        // Calculate inverse bind matrices
        let ibm = skeleton.calculate_inverse_bind_matrices();

        // Convert to flat array
        let ibm_data: Vec<f32> = ibm.iter().flatten().copied().collect();
        let ibm_bytes = bytemuck::cast_slice(&ibm_data);

        // Add buffer view
        let buffer_view_idx = self.add_buffer_view(ibm_bytes, None);

        // Add accessor for inverse bind matrices
        let accessor_idx = self.add_accessor(
            buffer_view_idx,
            json::accessor::Type::Mat4,
            json::accessor::ComponentType::F32,
            skeleton.bones.len(),
            None,
            None,
        );

        // Create skin
        let skin = json::Skin {
            name: Some("character_skin".to_string()),
            inverse_bind_matrices: Some(json::Index::new(accessor_idx as u32)),
            joints: joints.iter().map(|&j| json::Index::new(j)).collect(),
            skeleton: Some(json::Index::new(joints[0])),
            extensions: None,
            extras: Default::default(),
        };

        let skin_idx = self.root.skins.len() as u32;
        self.root.skins.push(skin);
        skin_idx
    }

    /// Export skinned mesh with JOINTS_0 and WEIGHTS_0 attributes
    fn export_skinned_mesh(&mut self, mesh: &SkinnedMesh) -> u32 {
        let vertex_count = mesh.positions.len();

        // POSITION accessor
        let pos_bytes = bytemuck::cast_slice(&mesh.positions);
        let pos_view = self.add_buffer_view(pos_bytes, Some(json::buffer::Target::ArrayBuffer));
        let pos_accessor = self.add_accessor(
            pos_view,
            json::accessor::Type::Vec3,
            json::accessor::ComponentType::F32,
            vertex_count,
            Some(mesh.min_pos),
            Some(mesh.max_pos),
        );

        // NORMAL accessor
        let norm_bytes = bytemuck::cast_slice(&mesh.normals);
        let norm_view = self.add_buffer_view(norm_bytes, Some(json::buffer::Target::ArrayBuffer));
        let norm_accessor = self.add_accessor(
            norm_view,
            json::accessor::Type::Vec3,
            json::accessor::ComponentType::F32,
            vertex_count,
            None,
            None,
        );

        // TEXCOORD_0 accessor
        let uv_bytes = bytemuck::cast_slice(&mesh.uvs);
        let uv_view = self.add_buffer_view(uv_bytes, Some(json::buffer::Target::ArrayBuffer));
        let uv_accessor = self.add_accessor(
            uv_view,
            json::accessor::Type::Vec2,
            json::accessor::ComponentType::F32,
            vertex_count,
            None,
            None,
        );

        // JOINTS_0 accessor - bone indices (4 u8 per vertex)
        let joints_bytes: Vec<u8> = mesh.bone_indices.iter()
            .flat_map(|&[a, b, c, d]| vec![a, b, c, d])
            .collect();
        let joints_view = self.add_buffer_view(&joints_bytes, Some(json::buffer::Target::ArrayBuffer));
        let joints_accessor = self.add_accessor(
            joints_view,
            json::accessor::Type::Vec4,
            json::accessor::ComponentType::U8,
            vertex_count,
            None,
            None,
        );

        // WEIGHTS_0 accessor - bone weights (4 f32 per vertex)
        let weights_bytes = bytemuck::cast_slice(&mesh.bone_weights);
        let weights_view = self.add_buffer_view(weights_bytes, Some(json::buffer::Target::ArrayBuffer));
        let weights_accessor = self.add_accessor(
            weights_view,
            json::accessor::Type::Vec4,
            json::accessor::ComponentType::F32,
            vertex_count,
            None,
            None,
        );

        // INDEX accessor
        let indices_bytes = bytemuck::cast_slice(&mesh.indices);
        let indices_view = self.add_buffer_view(indices_bytes, Some(json::buffer::Target::ElementArrayBuffer));
        let indices_accessor = self.add_accessor(
            indices_view,
            json::accessor::Type::Scalar,
            json::accessor::ComponentType::U16,
            mesh.indices.len(),
            None,
            None,
        );

        // Build primitive attributes
        let mut attributes = std::collections::BTreeMap::new();
        attributes.insert(
            json::validation::Checked::Valid(json::mesh::Semantic::Positions),
            json::Index::new(pos_accessor as u32),
        );
        attributes.insert(
            json::validation::Checked::Valid(json::mesh::Semantic::Normals),
            json::Index::new(norm_accessor as u32),
        );
        attributes.insert(
            json::validation::Checked::Valid(json::mesh::Semantic::TexCoords(0)),
            json::Index::new(uv_accessor as u32),
        );
        attributes.insert(
            json::validation::Checked::Valid(json::mesh::Semantic::Joints(0)),
            json::Index::new(joints_accessor as u32),
        );
        attributes.insert(
            json::validation::Checked::Valid(json::mesh::Semantic::Weights(0)),
            json::Index::new(weights_accessor as u32),
        );

        let primitive = json::mesh::Primitive {
            attributes,
            indices: Some(json::Index::new(indices_accessor as u32)),
            mode: json::validation::Checked::Valid(json::mesh::Mode::Triangles),
            material: None,
            targets: None,
            extensions: None,
            extras: Default::default(),
        };

        let mesh_obj = json::Mesh {
            name: Some("character_mesh".to_string()),
            primitives: vec![primitive],
            weights: None,
            extensions: None,
            extras: Default::default(),
        };

        let mesh_idx = self.root.meshes.len() as u32;
        self.root.meshes.push(mesh_obj);
        mesh_idx
    }

    /// Create scene node referencing mesh and skin
    fn create_skinned_node(&mut self, mesh_idx: u32, skin_idx: u32, joints: &[u32]) {
        let node = json::Node {
            name: Some("skinned_character".to_string()),
            mesh: Some(json::Index::new(mesh_idx)),
            skin: Some(json::Index::new(skin_idx)),
            translation: None,
            rotation: None,
            scale: None,
            children: None,
            ..Default::default()
        };

        let node_idx = self.root.nodes.len() as u32;
        self.root.nodes.push(node);

        // Create scene with skinned node and skeleton root
        let scene = json::Scene {
            name: Some("main".to_string()),
            nodes: vec![
                json::Index::new(node_idx),
                json::Index::new(joints[0]),  // Skeleton root
            ],
            extensions: None,
            extras: Default::default(),
        };

        self.root.scenes.push(scene);
        self.root.scene = Some(json::Index::new(0));
    }

    fn add_buffer_view(
        &mut self,
        data: &[u8],
        target: Option<json::buffer::Target>,
    ) -> usize {
        let byte_offset = self.buffer_data.len();
        self.buffer_data.extend_from_slice(data);

        let view = json::buffer::View {
            buffer: json::Index::new(0),
            byte_length: json::validation::USize64(data.len() as u64),
            byte_offset: Some(json::validation::USize64(byte_offset as u64)),
            byte_stride: None,
            target: target.map(json::validation::Checked::Valid),
            name: None,
            extensions: None,
            extras: Default::default(),
        };

        let idx = self.buffer_views.len();
        self.buffer_views.push(view);
        idx
    }

    fn add_accessor(
        &mut self,
        buffer_view: usize,
        type_: json::accessor::Type,
        component_type: json::accessor::ComponentType,
        count: usize,
        min: Option<[f32; 3]>,
        max: Option<[f32; 3]>,
    ) -> usize {
        let accessor = json::Accessor {
            buffer_view: Some(json::Index::new(buffer_view as u32)),
            byte_offset: Some(json::validation::USize64(0)),
            count: json::validation::USize64(count as u64),
            component_type: json::validation::Checked::Valid(
                json::accessor::GenericComponentType(component_type)
            ),
            type_: json::validation::Checked::Valid(type_),
            min: min.map(|m| json::Value::from(vec![m[0], m[1], m[2]])),
            max: max.map(|m| json::Value::from(vec![m[0], m[1], m[2]])),
            normalized: false,
            sparse: None,
            name: None,
            extensions: None,
            extras: Default::default(),
        };

        let idx = self.accessors.len();
        self.accessors.push(accessor);
        idx
    }

    fn write_files(&mut self, path: &str) -> std::io::Result<()> {
        // Finalize buffer
        let buffer = json::Buffer {
            byte_length: json::validation::USize64(self.buffer_data.len() as u64),
            uri: Some(format!("{}.bin", path.trim_end_matches(".gltf"))),
            name: None,
            extensions: None,
            extras: Default::default(),
        };
        self.root.buffers.push(buffer);
        self.root.buffer_views = std::mem::take(&mut self.buffer_views);
        self.root.accessors = std::mem::take(&mut self.accessors);

        // Write binary buffer
        let bin_path = format!("{}.bin", path.trim_end_matches(".gltf"));
        std::fs::write(&bin_path, &self.buffer_data)?;

        // Write GLTF JSON
        let json_string = serde_json::to_string_pretty(&self.root)?;
        std::fs::write(path, json_string)?;

        Ok(())
    }
}
```

## Data Structures

```rust
pub struct SkinnedMesh {
    pub positions: Vec<[f32; 3]>,
    pub normals: Vec<[f32; 3]>,
    pub uvs: Vec<[f32; 2]>,
    pub bone_indices: Vec<[u8; 4]>,
    pub bone_weights: Vec<[f32; 4]>,
    pub indices: Vec<u16>,
    pub min_pos: [f32; 3],
    pub max_pos: [f32; 3],
}

pub struct Skeleton {
    pub bones: Vec<Bone>,
}

pub struct Bone {
    pub name: String,
    pub parent: Option<usize>,
    pub local_position: Vec3,
    pub local_rotation: Quat,
    pub local_scale: Vec3,
}
```

## Python Alternative

```python
import json
import struct
import numpy as np

def export_skinned_gltf(mesh, skeleton, output_path):
    """Export skinned mesh to GLTF."""
    buffer_data = bytearray()
    buffer_views = []
    accessors = []

    def add_buffer_view(data, target=None):
        offset = len(buffer_data)
        buffer_data.extend(data)
        view = {
            "buffer": 0,
            "byteLength": len(data),
            "byteOffset": offset,
        }
        if target:
            view["target"] = target
        buffer_views.append(view)
        return len(buffer_views) - 1

    def add_accessor(view_idx, type_, component_type, count, min_val=None, max_val=None):
        acc = {
            "bufferView": view_idx,
            "byteOffset": 0,
            "componentType": component_type,
            "count": count,
            "type": type_,
        }
        if min_val is not None:
            acc["min"] = min_val
        if max_val is not None:
            acc["max"] = max_val
        accessors.append(acc)
        return len(accessors) - 1

    # Export positions
    pos_data = mesh.positions.astype(np.float32).tobytes()
    pos_view = add_buffer_view(pos_data, 34962)  # ARRAY_BUFFER
    pos_acc = add_accessor(pos_view, "VEC3", 5126, len(mesh.positions),
                          mesh.positions.min(axis=0).tolist(),
                          mesh.positions.max(axis=0).tolist())

    # Export normals
    norm_data = mesh.normals.astype(np.float32).tobytes()
    norm_view = add_buffer_view(norm_data, 34962)
    norm_acc = add_accessor(norm_view, "VEC3", 5126, len(mesh.normals))

    # Export UVs
    uv_data = mesh.uvs.astype(np.float32).tobytes()
    uv_view = add_buffer_view(uv_data, 34962)
    uv_acc = add_accessor(uv_view, "VEC2", 5126, len(mesh.uvs))

    # Export bone indices (JOINTS_0)
    joints_data = mesh.bone_indices.astype(np.uint8).tobytes()
    joints_view = add_buffer_view(joints_data, 34962)
    joints_acc = add_accessor(joints_view, "VEC4", 5121, len(mesh.bone_indices))  # UNSIGNED_BYTE

    # Export bone weights (WEIGHTS_0)
    weights_data = mesh.bone_weights.astype(np.float32).tobytes()
    weights_view = add_buffer_view(weights_data, 34962)
    weights_acc = add_accessor(weights_view, "VEC4", 5126, len(mesh.bone_weights))

    # Export indices
    indices_data = mesh.indices.astype(np.uint16).tobytes()
    indices_view = add_buffer_view(indices_data, 34963)  # ELEMENT_ARRAY_BUFFER
    indices_acc = add_accessor(indices_view, "SCALAR", 5123, len(mesh.indices))  # UNSIGNED_SHORT

    # Create nodes for skeleton
    nodes = []
    joint_indices = []

    for i, bone in enumerate(skeleton.bones):
        node = {"name": bone.name}
        if bone.translation is not None:
            node["translation"] = bone.translation.tolist()
        if bone.rotation is not None:
            node["rotation"] = bone.rotation.tolist()  # [x, y, z, w]
        nodes.append(node)
        joint_indices.append(i)

    # Set parent-child relationships
    for i, bone in enumerate(skeleton.bones):
        if bone.parent is not None:
            if "children" not in nodes[bone.parent]:
                nodes[bone.parent]["children"] = []
            nodes[bone.parent]["children"].append(i)

    # Export inverse bind matrices
    ibm = skeleton.calculate_inverse_bind_matrices()
    ibm_data = ibm.astype(np.float32).tobytes()
    ibm_view = add_buffer_view(ibm_data)
    ibm_acc = add_accessor(ibm_view, "MAT4", 5126, len(skeleton.bones))

    # Create skin
    skin = {
        "inverseBindMatrices": ibm_acc,
        "joints": joint_indices,
        "skeleton": 0,
    }

    # Create mesh
    mesh_node_idx = len(nodes)
    nodes.append({
        "name": "skinned_mesh",
        "mesh": 0,
        "skin": 0,
    })

    gltf = {
        "asset": {"version": "2.0"},
        "scene": 0,
        "scenes": [{"nodes": [mesh_node_idx, 0]}],  # mesh node + skeleton root
        "nodes": nodes,
        "meshes": [{
            "primitives": [{
                "attributes": {
                    "POSITION": pos_acc,
                    "NORMAL": norm_acc,
                    "TEXCOORD_0": uv_acc,
                    "JOINTS_0": joints_acc,
                    "WEIGHTS_0": weights_acc,
                },
                "indices": indices_acc,
            }]
        }],
        "skins": [skin],
        "buffers": [{"byteLength": len(buffer_data), "uri": output_path.replace('.gltf', '.bin')}],
        "bufferViews": buffer_views,
        "accessors": accessors,
    }

    # Write files
    with open(output_path, 'w') as f:
        json.dump(gltf, f, indent=2)

    with open(output_path.replace('.gltf', '.bin'), 'wb') as f:
        f.write(buffer_data)
```

## Validation

Before export, validate the skinned mesh:

```rust
fn validate_for_gltf(mesh: &SkinnedMesh, skeleton: &Skeleton) -> Result<(), Vec<String>> {
    let mut errors = Vec::new();

    // Check vertex count consistency
    let n = mesh.positions.len();
    if mesh.normals.len() != n || mesh.uvs.len() != n ||
       mesh.bone_indices.len() != n || mesh.bone_weights.len() != n {
        errors.push("Inconsistent vertex attribute counts".to_string());
    }

    // Validate bone weights
    for (i, weights) in mesh.bone_weights.iter().enumerate() {
        let sum: f32 = weights.iter().sum();
        if (sum - 1.0).abs() > 0.01 {
            errors.push(format!("Vertex {}: weights sum to {}", i, sum));
        }
    }

    // Validate bone indices
    let bone_count = skeleton.bones.len();
    for (i, indices) in mesh.bone_indices.iter().enumerate() {
        for (j, &idx) in indices.iter().enumerate() {
            if mesh.bone_weights[i][j] > 0.0 && idx as usize >= bone_count {
                errors.push(format!("Vertex {}: bone index {} >= {}", i, idx, bone_count));
            }
        }
    }

    if errors.is_empty() { Ok(()) } else { Err(errors) }
}
```

## Usage Example

```rust
fn main() {
    // Create skeleton
    let skeleton = create_humanoid_skeleton();

    // Create mesh with weights
    let mesh = generate_character_mesh();
    let weights = calculate_bone_weights(&mesh, &skeleton);
    let skinned_mesh = SkinnedMesh::from_mesh_and_weights(mesh, weights);

    // Export
    GltfSkinnedExporter::export(&skinned_mesh, &skeleton, "character.gltf")
        .expect("Failed to export");

    println!("Exported to character.gltf + character.bin");
}
```
