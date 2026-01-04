# Mesh Enhancement Index

Quick reference for mesh quality tier upgrades. Load specific sections as needed.

## Tier Upgrade Paths

| From | To | Focus | Section |
|------|-----|-------|---------|
| Placeholder | Temp | Topology, UVs, silhouette | `mesh-enhancements.md#placeholder--temp-upgrades` |
| Temp | Final | Edge loops, surface detail | `mesh-enhancements.md#temp--final-upgrades` |
| Final | Hero | Subdivision, LOD, optimization | `mesh-enhancements.md#final--hero-upgrades` |

## Technique Reference

| Technique | Use Case | Section |
|-----------|----------|---------|
| Silhouette improvement | Boring/flat outline | `mesh-enhancements.md#silhouette-improvement-techniques` |
| UV enhancement | Stretching, wasted space | `mesh-enhancements.md#uv-enhancement-techniques` |
| Budget management | Overbudget meshes | `mesh-enhancements.md#budget-management` |

## Quick Decision Tree

```
What tier is the current mesh?
│
├── PLACEHOLDER (primitive shapes, no UVs)
│   └── Add: proper topology + smart UVs + edge bevels
│       Target: Clean, usable base mesh
│
├── TEMP (proper topology, basic UVs)
│   └── Add: edge loops for deformation + surface details
│       Target: Production-ready mesh
│
└── FINAL (good topology, detailed)
    └── Add: subdivision + LOD chain + micro-bevels
        Target: Hero asset quality
```

## Common Enhancement Patterns

### Placeholder → Temp (Most Common)

1. Fix n-gons → quads/tris
2. Add edge loops at joints
3. Apply smart UV project
4. Bevel hard edges (0.02-0.05)

### Temp → Final

1. Add holding edges for subdivision
2. Optimize UV islands
3. Add surface detail loops
4. Create LOD chain if needed

## Budget Quick Reference

| Use Case | Triangle Budget |
|----------|-----------------|
| Swarm entities | 50-150 |
| Props | 50-300 |
| Characters | 200-500 |
| Vehicles | 300-800 |
| Hero/close-up | 500-2000 |

## Load Full Reference

For complete code examples and detailed techniques, read:
`mesh-enhancements.md`

This file is 1142 lines with full implementations. Only load when you need the actual code.
