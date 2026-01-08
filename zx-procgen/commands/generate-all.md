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

## Generate (Preferred)

From the project root:

```bash
ai-studio generate
```

## Generate (Blender-Dependent Categories)

Meshes, characters, and animations run by invoking Blender on the same entrypoint:

```bash
ai-studio generate --only meshes
ai-studio generate --only characters
ai-studio generate --only animations
```
