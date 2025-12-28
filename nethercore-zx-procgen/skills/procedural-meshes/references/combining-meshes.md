# Combining Meshes

Build complex models from simple parts.

## Merge Multiple Meshes

```rust
use proc_gen::mesh::combine;

let head: UnpackedMesh = generate_sphere(0.5, 16, 8);
let body: UnpackedMesh = generate_capsule(0.3, 1.0, 12, 6);
let arm: UnpackedMesh = generate_capsule(0.1, 0.6, 8, 4);

// Position parts
head.apply(Transform::translate(0.0, 1.5, 0.0));
body.apply(Transform::translate(0.0, 0.5, 0.0));
let mut arm_l = arm.clone();
let mut arm_r = arm.clone();
arm_l.apply(Transform::translate(-0.4, 1.0, 0.0));
arm_r.apply(Transform::translate(0.4, 1.0, 0.0));

// Combine all parts
let mut character = combine::merge(vec![head, body, arm_l, arm_r]);

// Clean up
character.apply(WeldVertices { threshold: 0.001 });
character.apply(RecalculateNormals);

write_obj(&character, "assets/meshes/character.obj", "character").unwrap();
```

## Boolean Operations (Python/trimesh)

```python
import trimesh

a = trimesh.primitives.Sphere(radius=1.0)
b = trimesh.primitives.Box(extents=[1.5, 1.5, 1.5])

# Boolean operations
union = a.union(b)
difference = a.difference(b)
intersection = a.intersection(b)

difference.export("assets/meshes/carved.obj")
```

## Part Library Pattern

```rust
struct PartLibrary {
    wheel: UnpackedMesh,
    body: UnpackedMesh,
    cockpit: UnpackedMesh,
}

impl PartLibrary {
    fn new() -> Self {
        Self {
            wheel: generate_torus(0.3, 0.1, 16, 8),
            body: generate_cube(1.0, 0.5, 2.0),
            cockpit: generate_sphere(0.4, 12, 6),
        }
    }

    fn assemble_vehicle(&self) -> UnpackedMesh {
        let mut result = self.body.clone();

        // Add wheels
        for (x, z) in [(-0.6, -0.6), (0.6, -0.6), (-0.6, 0.6), (0.6, 0.6)] {
            let mut wheel = self.wheel.clone();
            wheel.apply(Transform::translate(x, -0.2, z));
            result = combine::merge(vec![result, wheel]);
        }

        // Add cockpit
        let mut cockpit = self.cockpit.clone();
        cockpit.apply(Transform::translate(0.0, 0.4, 0.3));
        result = combine::merge(vec![result, cockpit]);

        result
    }
}
```
