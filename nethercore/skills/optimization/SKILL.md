---
name: optimization
description: >-
  Optimization techniques for Nethercore WASM games. Covers WASM binary size
  reduction (LTO, wasm-opt), texture and mesh compression, audio optimization,
  and state size minimization. Use when a ROM exceeds size limits or when
  reducing build output size.
license: Apache-2.0
compatibility: Works offline; wasm-opt is optional.
metadata:
  author: nethercore-systems
  version: "1.0.1"
---

# Nethercore Optimization

Measure first; use existing build/platform features before adding tooling. Keep simulation and asset correctness while reducing the resource actually over budget.

## WASM

```toml
[profile.release]
lto = true
opt-level = "z"
codegen-units = 1
panic = "abort"
```

Compare size and runtime performance; `"s"` may be better for a particular game. Strip symbols only when debugging requirements permit. `wasm-opt` is optional, not a dependency to install blindly. If used, optimize the actual manifest-selected WASM before `nether pack` and rerun the cart; optimizing a loose file after packing changes nothing in the cart.

## Textures and meshes

ZX RGBA8/BC7 selection is explicit `[game].compress_textures`, not automatically all textures. BC7 uses 16 bytes per 4x4 block, approximately 1 byte/pixel on aligned dimensions, not 0.5. Keep atlas padding/alpha and inspect actual VRAM.

Distinguish float input vertices from packed ROM/GPU vertices. Use `zx-common`'s format/stride functions, not a fixed universal table. Drop attributes only when the render mode/material/normal mapping/skinning permits it. Preserve complete intended geometry through the first-mesh/primitive GLB importer.

## Audio and state

Target PCM is 22050 Hz mono i16; raw WAV currently needs to arrive in that format. XM/IT pattern data plus shared samples can be compact, but there is no guaranteed percentage saving or fixed bytes-per-second for a tracker module.

Use bounded arrays when they fit. A `Vec` is not inherently non-deterministic if allocator/data/RNG state are snapshotted and iteration is stable. Smaller integer fields need explicit range/scale/overflow policy; `i16` alone does not define fixed-point math. Do not reduce numeric accuracy merely to satisfy an arbitrary state-size target.

See [optimization techniques](references/optimization-techniques.md) for the verification sequence.
