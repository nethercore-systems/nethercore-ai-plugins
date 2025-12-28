# Vertex Colors

ZX supports per-vertex colors that multiply with material/texture colors.

## When to Use Vertex Colors

| Use Case | Why |
|----------|-----|
| Baked ambient occlusion | Subtle shading in crevices |
| Gradients | Sky-to-ground color variation |
| Region marking | Different materials on one mesh |
| Stylized look | Flat-shaded with color variation |
| Performance | No texture needed |

## Setting Vertex Colors

```rust
// Generate mesh with UV variant (includes color support)
let mut mesh: UnpackedMeshUV = generate_cube_uv(1.0, 1.0, 1.0);

// Set colors per vertex
mesh.colors[0] = [255, 0, 0, 255];    // Red
mesh.colors[1] = [0, 255, 0, 255];    // Green
// ...

// Or apply color modifier
mesh.apply(VertexColorGradient {
    start_color: [64, 64, 64, 255],   // Dark bottom
    end_color: [255, 255, 255, 255],  // White top
    axis: Axis::Y,
});

// Bake ambient occlusion
mesh.apply(BakeAO {
    ray_count: 32,
    max_distance: 0.5,
});
```

## Color Blending in Shader

In the ZX shader, vertex color multiplies with material:
```
final_color = texture_color * vertex_color * set_color_tint
```

## Exporting with Colors

```rust
// OBJ doesn't support vertex colors, use GLTF
write_gltf(&mesh, "assets/meshes/colored.gltf").unwrap();
```

Or write to custom format:
```rust
write_obj_with_colors(&mesh, "assets/meshes/colored.obj", "colored").unwrap();
```
