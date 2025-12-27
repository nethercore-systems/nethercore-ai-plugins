# External Libraries Reference

Recommended libraries for procedural generation across Rust, Python, and JavaScript ecosystems.

## Rust Libraries

### Core Math

#### glam
Fast, simple math library. Recommended for game development.

```toml
[dependencies]
glam = "0.27"
```

```rust
use glam::{Vec3, Mat4, Quat};

let pos = Vec3::new(1.0, 2.0, 3.0);
let rotation = Quat::from_rotation_y(0.5);
let transform = Mat4::from_rotation_translation(rotation, pos);
```

**Best for:** Transforms, vectors, matrices, quaternions.

#### nalgebra
More comprehensive linear algebra. Use when you need advanced operations.

```toml
[dependencies]
nalgebra = "0.32"
```

```rust
use nalgebra::{Matrix4, Vector3, Rotation3};

// Sparse matrices for heat diffusion
use nalgebra_sparse::CsrMatrix;
```

**Best for:** Sparse matrices, eigenvalues, advanced algebra.

---

### Noise Generation

#### noise
Feature-complete noise library.

```toml
[dependencies]
noise = "0.8"
```

```rust
use noise::{NoiseFn, Perlin, Simplex, Worley, Fbm};

let perlin = Perlin::new(42);
let value = perlin.get([x as f64, y as f64]);

// FBM with Simplex base
let fbm = Fbm::<Simplex>::new(42)
    .set_octaves(6)
    .set_persistence(0.5);
let terrain = fbm.get([x as f64, y as f64]);
```

**Best for:** Perlin, Simplex, Worley, FBM, Ridged noise.

#### fastnoise-lite
Extremely fast, SIMD-optimized. Port of FastNoise Lite.

```toml
[dependencies]
fastnoise-lite = "1.0"
```

```rust
use fastnoise_lite::{FastNoiseLite, NoiseType};

let mut noise = FastNoiseLite::new();
noise.set_noise_type(Some(NoiseType::Simplex));
noise.set_frequency(Some(0.01));
let value = noise.get_noise_2d(x, y);
```

**Best for:** Real-time generation, SIMD performance.

---

### 3D Mesh & File I/O

#### gltf
Read and write GLTF/GLB files.

```toml
[dependencies]
gltf = "1.4"
```

```rust
use gltf::Gltf;

let gltf = Gltf::open("model.gltf")?;
for mesh in gltf.meshes() {
    for primitive in mesh.primitives() {
        let positions = reader.read_positions();
        let normals = reader.read_normals();
    }
}
```

**Best for:** Loading/saving 3D models, skeletons, animations.

#### obj-rs
Simple OBJ file I/O.

```toml
[dependencies]
obj = "0.10"
```

```rust
use obj::{Obj, load_obj};

let obj: Obj = load_obj("mesh.obj")?;
let vertices = obj.vertices;
let indices = obj.indices;
```

**Best for:** Simple mesh export for ZX pipeline.

#### meshopt
Mesh optimization (simplification, cache optimization).

```toml
[dependencies]
meshopt = "0.2"
```

```rust
use meshopt::{simplify, generate_vertex_remap};

// Simplify mesh to target triangle count
let simplified = simplify(&indices, &vertices, target_count, 0.01);
```

**Best for:** LOD generation, mesh optimization.

---

### Image I/O

#### image
Comprehensive image reading/writing.

```toml
[dependencies]
image = "0.25"
```

```rust
use image::{RgbaImage, Rgba};

let mut img = RgbaImage::new(256, 256);
img.put_pixel(x, y, Rgba([r, g, b, 255]));
img.save("texture.png")?;
```

**Best for:** PNG, JPEG, reading/writing textures.

---

### Geometry Processing

#### parry3d
Collision detection and geometric queries.

```toml
[dependencies]
parry3d = "0.13"
```

```rust
use parry3d::shape::TriMesh;
use parry3d::query::PointQuery;

let mesh = TriMesh::new(vertices, indices);
let closest = mesh.project_point(&identity, &point, solid);
```

**Best for:** Distance queries, ray casting, collision.

#### spade
Delaunay triangulation and Voronoi diagrams.

```toml
[dependencies]
spade = "2.0"
```

```rust
use spade::{DelaunayTriangulation, Triangulation};

let mut triangulation = DelaunayTriangulation::new();
triangulation.insert(Point2::new(0.0, 0.0));
```

**Best for:** 2D triangulation, Voronoi cells.

---

## Python Libraries

### Core Scientific

#### numpy
Fundamental array operations.

```bash
pip install numpy
```

```python
import numpy as np

# Create texture buffer
texture = np.zeros((256, 256, 4), dtype=np.uint8)
texture[:, :, 0] = 255  # Red channel
```

**Best for:** Array math, image manipulation, everything.

#### scipy
Scientific computing. Heat equation, geodesics, optimization.

```bash
pip install scipy
```

```python
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
from scipy.spatial.distance import cdist

# Solve heat equation
heat = spsolve(laplacian, sources)

# Geodesic distance via Dijkstra
from scipy.sparse.csgraph import dijkstra
distances = dijkstra(adjacency_matrix, indices=source_vertex)
```

**Best for:** Sparse linear algebra, geodesics, optimization.

---

### Noise

#### noise
Perlin and Simplex noise.

```bash
pip install noise
```

```python
from noise import snoise2, pnoise2

# Simplex noise
value = snoise2(x * 0.01, y * 0.01, octaves=4)

# Perlin noise
value = pnoise2(x * 0.01, y * 0.01, octaves=4)
```

**Best for:** Quick noise generation.

#### opensimplex
Pure Python simplex noise, works everywhere.

```bash
pip install opensimplex
```

```python
from opensimplex import OpenSimplex

noise = OpenSimplex(seed=42)
value = noise.noise2(x, y)
```

**Best for:** Cross-platform, no C dependencies.

---

### 3D Mesh

#### trimesh
Comprehensive mesh manipulation.

```bash
pip install trimesh
```

```python
import trimesh

mesh = trimesh.load('model.obj')
mesh.vertices  # Nx3 array
mesh.faces     # Mx3 array

# Compute geodesic distance
from trimesh.graph import shortest_path
distances = shortest_path(mesh.edges, source_vertex)

# UV unwrapping
from trimesh.visual.uv import unwrap_faces
uvs = unwrap_faces(mesh)

# Export
mesh.export('output.obj')
mesh.export('output.gltf')
```

**Best for:** Mesh I/O, manipulation, UV unwrapping, analysis.

#### pygltflib
GLTF manipulation.

```bash
pip install pygltflib
```

```python
from pygltflib import GLTF2

gltf = GLTF2.load("model.gltf")
for mesh in gltf.meshes:
    for primitive in mesh.primitives:
        # Access data
        pass
```

**Best for:** GLTF reading/writing, skeleton access.

#### pywavefront
Simple OBJ loading.

```bash
pip install pywavefront
```

```python
import pywavefront

scene = pywavefront.Wavefront('model.obj')
for mesh in scene.mesh_list:
    vertices = mesh.vertices
```

**Best for:** Quick OBJ loading.

---

### Image I/O

#### Pillow
Image reading/writing.

```bash
pip install Pillow
```

```python
from PIL import Image
import numpy as np

# Create from array
img_array = np.zeros((256, 256, 4), dtype=np.uint8)
img = Image.fromarray(img_array, mode='RGBA')
img.save('texture.png')

# Read image
img = Image.open('texture.png')
array = np.array(img)
```

**Best for:** PNG, JPEG, image I/O.

---

## JavaScript/Node Libraries

### Noise

#### simplex-noise
Fast Simplex noise implementation.

```bash
npm install simplex-noise
```

```javascript
import { createNoise2D } from 'simplex-noise';

const noise2D = createNoise2D();
const value = noise2D(x * 0.01, y * 0.01);
```

**Best for:** Browser-based generation, fast 2D/3D noise.

#### noisejs
Perlin and Simplex noise.

```bash
npm install noisejs
```

```javascript
import { Noise } from 'noisejs';

const noise = new Noise(42);
const value = noise.simplex2(x, y);
const perlin = noise.perlin2(x, y);
```

**Best for:** Classic Perlin support.

---

### 3D Graphics

#### three.js
3D graphics library with geometry utilities.

```bash
npm install three
```

```javascript
import * as THREE from 'three';

// Procedural geometry
const geometry = new THREE.BufferGeometry();
geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));

// Built-in primitives
const box = new THREE.BoxGeometry(1, 1, 1);
const sphere = new THREE.SphereGeometry(1, 32, 16);

// Export to GLTF
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter';
```

**Best for:** Geometry generation, GLTF export.

#### gl-matrix
High-performance matrix/vector operations.

```bash
npm install gl-matrix
```

```javascript
import { vec3, mat4, quat } from 'gl-matrix';

const position = vec3.create();
vec3.set(position, 1, 2, 3);

const transform = mat4.create();
mat4.fromRotationTranslation(transform, rotation, position);
```

**Best for:** Math operations, transforms.

---

## Library Selection Guide

### By Task

| Task | Rust | Python | JavaScript |
|------|------|--------|------------|
| Basic math | glam | numpy | gl-matrix |
| Advanced algebra | nalgebra | scipy | - |
| Simplex noise | noise, fastnoise-lite | noise, opensimplex | simplex-noise |
| Worley noise | noise | - (implement) | - (implement) |
| FBM | noise | noise | - (implement) |
| Mesh I/O | gltf, obj-rs | trimesh | three.js |
| Mesh processing | meshopt, parry3d | trimesh, scipy | - |
| Image I/O | image | Pillow | - (Canvas API) |
| Geodesics | - (implement) | scipy, trimesh | - |

### By Performance Priority

**Fastest (real-time):**
- Rust: fastnoise-lite, glam
- Python: numpy with numba JIT

**Most Features:**
- Rust: nalgebra, noise
- Python: trimesh, scipy

**Simplest Setup:**
- Rust: glam, image
- Python: numpy, Pillow

---

## Installation Templates

### Rust Cargo.toml (Full)

```toml
[dependencies]
# Math
glam = "0.27"

# Noise
noise = "0.8"

# 3D I/O
gltf = "1.4"

# Images
image = "0.25"

# Optional: mesh processing
meshopt = "0.2"
```

### Python requirements.txt (Full)

```
numpy
scipy
noise
trimesh
Pillow
pygltflib
```

### Node package.json (Full)

```json
{
  "dependencies": {
    "simplex-noise": "^4.0.0",
    "three": "^0.160.0",
    "gl-matrix": "^3.4.0"
  }
}
```
