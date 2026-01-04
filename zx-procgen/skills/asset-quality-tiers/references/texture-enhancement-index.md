# Texture Enhancement Index

Quick reference for texture quality tier upgrades. Load specific sections as needed.

## Tier Upgrade Paths

| From | To | Focus | Section |
|------|-----|-------|---------|
| Placeholder | Temp | Noise, palette, basic detail | `texture-enhancements.md#placeholder--temp-upgrades` |
| Temp | Final | Layer system, weathering, MRE maps | `texture-enhancements.md#temp--final-upgrades` |
| Final | Hero | PBR detail, hand-painted touches | `texture-enhancements.md#final--hero-upgrades` |

## Technique Reference

| Technique | Use Case | Section |
|-----------|----------|---------|
| Contrast enhancement | Flat, muddy textures | `texture-enhancements.md#contrast-enhancement-techniques` |
| Color richness | Desaturated, boring colors | `texture-enhancements.md#color-richness-techniques` |
| Detail layers | Adding surface detail | `texture-enhancements.md#detail-layer-system` |
| Resolution | Choosing texture size | `texture-enhancements.md#resolution-guidelines` |

## Quick Decision Tree

```
What tier is the current texture?
│
├── PLACEHOLDER (flat color, no detail)
│   └── Add: noise variation + palette + basic shading
│       Target: 50-70% quality (recognizable, usable)
│
├── TEMP (has noise, basic detail)
│   └── Add: multi-layer system + weathering + MRE
│       Target: 70-85% quality (production ready)
│
└── FINAL (multi-layer, weathered)
    └── Add: PBR detail + hand-painted accents
        Target: 85-100% quality (hero asset)
```

## Common Enhancement Patterns

### Placeholder → Temp (Most Common)

1. `add_noise_variation()` - break up flat colors
2. `remap_to_palette()` - establish color coherence
3. `add_grain_layer()` - surface texture
4. `apply_contrast_curve()` - visual depth

### Temp → Final

1. `add_weathering_layer()` - wear and damage
2. `add_edge_highlights()` - definition
3. `generate_mre_map()` - PBR material properties
4. `apply_color_grading()` - mood/atmosphere

## Load Full Reference

For complete code examples and detailed techniques, read:
`texture-enhancements.md`

This file is 1290 lines with full implementations. Only load when you need the actual code.
