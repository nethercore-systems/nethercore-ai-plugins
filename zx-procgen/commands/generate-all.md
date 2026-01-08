---
description: Run the unified .studio/generate.py pipeline
argument-hint: ""
allowed-tools:
  - Read
  - Glob
  - Bash
---

# Generate All

Generate assets from `.studio/specs/**` using the unified generator.

## Prerequisite

If `.studio/generate.py` is missing, run `/init-procgen` first.

## Generate (Python)

From the project root:

```bash
python .studio/generate.py
```

## Generate (Blender-Dependent Categories)

Meshes, characters, and animations run by invoking Blender on the same entrypoint:

```bash
blender --background --python .studio/generate.py -- --only meshes
blender --background --python .studio/generate.py -- --only characters
blender --background --python .studio/generate.py -- --only animations
```
