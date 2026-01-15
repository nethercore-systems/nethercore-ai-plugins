# ZX Plugin

ZX fantasy console FFI reference and specifications. Console-specific knowledge for the ZX platform.

## Skills

### ffi-reference
ZX FFI bindings: rendering, input, audio, transforms. Reference for 250+ functions.

### console-specs
Hardware specifications: resolution, memory limits, render modes, audio system.

### rendering
Rendering techniques: cameras, stencil effects, particles, custom fonts.

## ZX Specifications

| Spec | Value |
|------|-------|
| Resolution | 960x540 |
| ROM | 16 MB |
| RAM | 4 MB |
| VRAM | 4 MB |
| Players | 1-4 |

## Quick Reference

```rust
// Required exports
#[no_mangle] pub extern "C" fn init() { }
#[no_mangle] pub extern "C" fn update() { }
#[no_mangle] pub extern "C" fn render() { }

// Asset loading (in init)
let tex = rom_texture_str("player");
let mesh = rom_mesh_str("character");

// Drawing (in render)
camera_set(0.0, 5.0, 10.0, 0.0, 0.0, 0.0);
push_translate(x, y, z);
draw_mesh(mesh);
push_identity();
```
