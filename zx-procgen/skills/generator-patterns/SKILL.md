---
name: Generator Patterns
description: |
  Use this skill when setting up procedural asset generation projects.

  **Triggers:** "project structure", "file organization", "generator setup", "multiple assets", "batch generation", "lib utilities".

  **Load references when:**
  - Setting up project structure → `references/file-organization.md`
  - Mesh generation utilities → `references/lib/bpy_utils.py`
  - Texture generation utilities → `references/lib/texture_buffer.py`
  - Sprite generation utilities → `references/lib/sprite_utils.py`
  - Animation utilities → `references/lib/animation_utils.py`
  - Batch runner → `references/generate_all.py`
version: 1.0.0
---

# Generator Patterns

Shared patterns for organizing procedural asset generation code. Optimized for maintainability and LLM context efficiency.

## Core Principle: One Asset Per File

Every procedural asset (mesh, texture, sprite, animation) should have its own dedicated Python file. This pattern provides:

1. **LLM Context Efficiency** - Load only lib + single asset file (~150 lines vs 500+)
2. **Maintainability** - Changes to one asset don't affect others
3. **Discoverability** - File name = asset name
4. **Parallel Development** - Multiple agents can work on different assets without conflicts
5. **Testing** - Run single file to test single asset
6. **Batch Generation** - Simple `generate_all.py` script runs everything

## Standard Project Structure

```
generator/
├── lib/                          # Shared utilities (copy from references/)
│   ├── bpy_utils.py              # Mesh generation helpers
│   ├── texture_buffer.py         # Texture buffer class
│   ├── sprite_utils.py           # Sprite/palette helpers
│   └── animation_utils.py        # Animation keyframe helpers
├── meshes/
│   ├── barrel.py                 # One file per mesh
│   ├── crate.py
│   └── chair.py
├── textures/
│   ├── wood_plank.py             # One file per texture
│   ├── metal_brushed.py
│   └── stone_cobble.py
├── sprites/
│   ├── player_idle.py            # One file per sprite/sheet
│   ├── enemy_walk.py
│   └── ui_buttons.py
├── animations/
│   ├── walk_cycle.py             # One file per animation
│   └── attack_slash.py
└── generate_all.py               # Batch runner
```

## Asset File Template

Each asset file follows this pattern:

```python
#!/usr/bin/env python3
"""Generate [asset name]."""
from lib.[relevant_lib] import [helpers]

# Asset-specific configuration
OUTPUT_PATH = "../assets/meshes/barrel.glb"

def generate():
    """Generate the asset."""
    # Implementation here
    pass

if __name__ == "__main__":
    generate()
```

## File Size Limits

| Limit | Lines | Action |
|-------|-------|--------|
| Target | ≤150 | Ideal for single asset |
| Soft | 200 | Consider extracting helpers to lib/ |
| Hard | 300 | MUST split or refactor |

If an asset file exceeds 200 lines, extract reusable functions to the appropriate lib/ module.

## References

- `references/file-organization.md` - Detailed organization guide
- `references/lib/bpy_utils.py` - Mesh generation utilities template
- `references/lib/texture_buffer.py` - Texture buffer class template
- `references/lib/sprite_utils.py` - Sprite generation utilities template
- `references/lib/animation_utils.py` - Animation utilities template
- `references/generate_all.py` - Batch runner template

## Related Skills

- `procedural-meshes` - Mesh-specific generation techniques
- `procedural-textures` - Texture-specific generation techniques
- `procedural-sprites` - Sprite-specific generation techniques
- `procedural-animations` - Animation-specific generation techniques
