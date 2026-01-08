---
description: Establish a visual style guide for procedural assets
argument-hint: "[style goals]"
allowed-tools: ["Read"]
---

# Establish Visual Style

Create a compact visual style guide that downstream specs can reference (palette, materials, shape language).

## Recommended workflow

1. Use `creative-direction:establish-vision` to define the overall art direction.
2. Use `zx-procgen:asset-designer` to translate that direction into generation-ready style tokens and constraints.
3. Generate a small set of test assets with `zx-procgen:generate-asset` and iterate.

