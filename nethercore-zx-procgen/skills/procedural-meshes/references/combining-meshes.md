# Combining Meshes

Build complex models from simple parts. These techniques are language-agnostic.

## Core Operations

### Merge (Union without Boolean)

Combine multiple meshes into one without modifying geometry. Fast and simple.

**Algorithm (pseudocode):**
```
function merge(meshes):
    result = new_mesh()
    vertex_offset = 0

    for mesh in meshes:
        # Copy vertices
        for vertex in mesh.vertices:
            result.vertices.append(vertex)

        # Copy faces with offset indices
        for face in mesh.faces:
            result.faces.append([
                face[0] + vertex_offset,
                face[1] + vertex_offset,
                face[2] + vertex_offset
            ])

        vertex_offset += len(mesh.vertices)

    return result
```

**Use for:** Assembling parts that don't intersect (character limbs, vehicle parts)

---

### Boolean Operations

Create new geometry by combining shapes mathematically.

| Operation | Result |
|-----------|--------|
| Union | Combined volume of both shapes |
| Difference | First shape minus second |
| Intersection | Only overlapping volume |

**Use for:** Carving holes, creating complex shapes

**Note:** Boolean operations are computationally expensive and may produce degenerate geometry. Clean up with weld/triangulate after.

---

### Weld Vertices

Merge vertices that are within a threshold distance.

**Parameters:**
| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| threshold | Maximum distance to merge | 0.001 |

**Algorithm (pseudocode):**
```
function weld_vertices(mesh, threshold):
    # Build spatial hash for efficiency
    grid = spatial_hash(mesh.vertices, threshold * 2)

    # Find merge candidates
    merge_map = {}
    for i, vertex in enumerate(mesh.vertices):
        nearby = grid.query(vertex, threshold)
        for j in nearby:
            if j < i and distance(vertex, mesh.vertices[j]) < threshold:
                merge_map[i] = j
                break

    # Remap face indices
    for face in mesh.faces:
        for k in range(3):
            if face[k] in merge_map:
                face[k] = merge_map[face[k]]

    # Remove unused vertices
    mesh.compact()
    return mesh
```

**Use for:** Closing seams after merge, fixing imported meshes

---

## Assembly Workflow

### 1. Transform Parts

Position parts before combining.

**Operations:**
| Operation | Description |
|-----------|-------------|
| Translate | Move in 3D space |
| Rotate | Rotate around axis |
| Scale | Resize uniformly or per-axis |

**Best practice:** Apply transforms before merge, not after.

### 2. Merge Parts

Combine all transformed parts.

### 3. Cleanup

- Weld vertices at seams
- Remove duplicate faces
- Recalculate normals

### 4. Finalize

- Triangulate (if needed)
- Snap UVs to pixel grid
- Export

---

## Part Library Pattern

Pre-generate reusable parts for efficient asset creation.

**Concept:**
```
PartLibrary:
    parts: {
        wheel: torus(0.3, 0.1, 16, 8),
        body: cube(1.0, 0.5, 2.0),
        cockpit: sphere(0.4, 12, 6),
        antenna: cylinder(0.02, 0.02, 0.5, 6),
    }

    function assemble_vehicle():
        result = clone(parts.body)

        # Add 4 wheels
        for position in wheel_positions:
            wheel = clone(parts.wheel)
            wheel.translate(position)
            result = merge([result, wheel])

        # Add cockpit
        cockpit = clone(parts.cockpit)
        cockpit.translate(0, 0.4, 0.3)
        result = merge([result, cockpit])

        # Cleanup
        result = weld_vertices(result, 0.001)
        result = recalculate_normals(result)

        return result
```

---

## Symmetry Optimization

Model half, then mirror.

**Algorithm (pseudocode):**
```
function mirror_and_merge(mesh, axis):
    mirrored = clone(mesh)

    # Flip across axis
    for vertex in mirrored.vertices:
        vertex[axis] = -vertex[axis]

    # Flip face winding (important!)
    for face in mirrored.faces:
        face[1], face[2] = face[2], face[1]

    # Merge and weld center seam
    result = merge([mesh, mirrored])
    result = weld_vertices(result, 0.001)

    return result
```

**Use for:** Characters, vehicles, symmetric props

---

## Language Examples

### Rust (proc-gen)

```rust
use proc_gen::mesh::*;

// Create parts
let head = generate_sphere(0.5, 16, 8);
let body = generate_capsule(0.3, 1.0, 12, 6);
let arm = generate_capsule(0.1, 0.6, 8, 4);

// Position parts
let mut parts = vec![];

let mut head_t = head.clone();
head_t.apply(Transform::translate(0.0, 1.5, 0.0));
parts.push(head_t);

let mut body_t = body.clone();
body_t.apply(Transform::translate(0.0, 0.5, 0.0));
parts.push(body_t);

let mut arm_l = arm.clone();
arm_l.apply(Transform::translate(-0.4, 1.0, 0.0));
parts.push(arm_l);

let mut arm_r = arm.clone();
arm_r.apply(Transform::translate(0.4, 1.0, 0.0));
parts.push(arm_r);

// Combine all parts
let mut character = combine::merge(parts);

// Cleanup
character.apply(WeldVertices { threshold: 0.001 });
character.apply(RecalculateNormals);

write_obj(&character, "character.obj", "character").unwrap();
```

### Python (trimesh)

```python
import trimesh
import numpy as np

# Create parts
head = trimesh.primitives.Sphere(radius=0.5)
body = trimesh.primitives.Capsule(radius=0.3, height=1.0)
arm = trimesh.primitives.Capsule(radius=0.1, height=0.6)

# Position parts
head.apply_translation([0, 1.5, 0])
body.apply_translation([0, 0.5, 0])

arm_l = arm.copy()
arm_l.apply_translation([-0.4, 1.0, 0])

arm_r = arm.copy()
arm_r.apply_translation([0.4, 1.0, 0])

# Combine
character = trimesh.util.concatenate([head, body, arm_l, arm_r])

# Cleanup
character.merge_vertices(merge_tex=True, merge_norm=True)
character.fix_normals()

character.export("character.obj")
```

### JavaScript (Three.js)

```javascript
import * as THREE from 'three';
import { mergeBufferGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';

// Create parts
const head = new THREE.SphereGeometry(0.5, 16, 8);
const body = new THREE.CapsuleGeometry(0.3, 1.0, 6, 12);
const arm = new THREE.CapsuleGeometry(0.1, 0.6, 4, 8);

// Position parts
head.translate(0, 1.5, 0);
body.translate(0, 0.5, 0);

const armL = arm.clone();
armL.translate(-0.4, 1.0, 0);

const armR = arm.clone();
armR.translate(0.4, 1.0, 0);

// Combine
const character = mergeBufferGeometries([head, body, armL, armR]);
character.computeVertexNormals();
```

### Conceptual (any language)

```
# Create parts
head = generate_sphere(radius=0.5, segments=16, rings=8)
body = generate_capsule(radius=0.3, height=1.0)
arm = generate_capsule(radius=0.1, height=0.6)

# Position parts
head = translate(head, 0, 1.5, 0)
body = translate(body, 0, 0.5, 0)
arm_l = translate(clone(arm), -0.4, 1.0, 0)
arm_r = translate(clone(arm), 0.4, 1.0, 0)

# Combine
character = merge([head, body, arm_l, arm_r])

# Cleanup
character = weld_vertices(character, threshold=0.001)
character = recalculate_normals(character)

# Export
export_obj(character, "character.obj")
```

---

## Boolean Operations (Advanced)

For carving and complex CSG operations.

### Python (trimesh)

```python
import trimesh

a = trimesh.primitives.Sphere(radius=1.0)
b = trimesh.primitives.Box(extents=[1.5, 1.5, 1.5])

# Boolean operations
union = a.union(b)
difference = a.difference(b)
intersection = a.intersection(b)

difference.export("carved.obj")
```

### JavaScript (THREE-CSGMesh)

```javascript
import { CSG } from 'three-csg-ts';

const sphereMesh = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 16));
const boxMesh = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.5, 1.5));

const result = CSG.subtract(sphereMesh, boxMesh);
```

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forgetting to clone | Original mesh modified | Always clone before transform |
| Not welding after merge | Visible seams, doubled vertices | Weld with small threshold |
| Wrong face winding after mirror | Inverted normals on mirrored half | Flip face order when mirroring |
| Boolean on non-watertight mesh | Failed operation or holes | Ensure meshes are closed |
| Too many boolean operations | Performance degradation | Simplify design or use merge |
