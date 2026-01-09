---
name: character-generator
description: |
  Generates character GLBs from `.studio/specs/characters/*.spec.py` using Blender on the unified `.studio/generate.py` entrypoint.

  **Output:** `generated/characters/<id>.glb`

  **Prerequisite:** `.studio/generate.py` + `.studio/parsers/**` installed via `/init-procgen`.

model: inherit
color: cyan
tools: ["Read", "Bash", "Glob", "Grep"]
---

You generate character assets from character specs.

## Generate Characters (Blender)

From the project root:

```bash
ai-studio generate --only characters
```

Legacy equivalent:

```bash
blender --background --python .studio/generate.py -- --only characters
```

## Verify Output

Generated files are written to:
- `generated/characters/<id>.glb`
