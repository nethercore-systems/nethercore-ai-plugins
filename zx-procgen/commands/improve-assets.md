---
description: Review generated assets and propose improvements (routes to quality agents)
argument-hint: "[notes]"
allowed-tools: ["Read", "Glob"]
---

# Improve Assets

Use this command when you have generated assets under `generated/**` and want a targeted improvement plan.

## What this does

- Reviews generated outputs against constraints and quality heuristics
- Suggests concrete next improvements (naming, UVs, budgets, consistency)

## Recommended follow-ups

- For a full critique + checklists: use the `zx-procgen:asset-quality-reviewer` agent.
- For implementation of improvements: use the `zx-procgen:quality-enhancer` agent.
- For deterministic checks on 3D outputs (requires Blender): run `ai-studio validate --artifacts --spec <spec>`.

