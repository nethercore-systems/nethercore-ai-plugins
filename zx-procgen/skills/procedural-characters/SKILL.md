---
name: Procedural Character Generation
description: |
  Use this skill to GENERATE LOW-POLY CHARACTERS (300-700 tris) for ZX games using the extrude+scale paradigm.

  **Triggers:** "character mesh", "create character", "humanoid mesh", "quadruped mesh", "character spec", "extrude scale", "low-poly character", "PS1 character", "PS2 character", "feminine character", "anatomical mesh"

  **Before generating:** Check `.studio/visual-style.local.md` for project style.

  **Load references when:**
  - Python bpy code → `references/bpy-implementation.md`
  - Skeleton hierarchies → `references/skeleton-presets.md`
  - Body part patterns → `references/body-part-patterns.md`
  - Style guides (mecha, organic, armored) → `references/style-presets.md`
  - Triangle budgets → `references/triangle-budget-guide.md`

  **Load examples when:**
  - Need complete spec templates → `examples/knight.yaml`, `examples/mage.yaml`, `examples/spider.yaml`, `examples/feminine_warrior.yaml`

  For NORMAL MAPS: use `procedural-normal-maps` skill (enable tangent export).
  For TEXTURING: use `mesh-texturing-workflows` skill.
  For ANIMATIONS: use `procedural-animations` skill (reference only).
version: 1.2.0
---

# Procedural Character Generation

Generate low-poly characters (PS1/PS2 era, 300-700 triangles) using a YAML specification format and Blender bpy.

## Core Concept: Extrude+Scale Paradigm

Characters are defined as YAML specs with:
1. **Skeleton** - Bone hierarchy with world positions
2. **Parts** - Body parts that extrude along bone directions
3. **Steps** - Extrude+scale sequences that build each part
4. **Mirroring** - Automatic left/right symmetry

Each body part is a tube that extrudes along its bone's direction, with steps that scale, translate, and rotate the cross-section.

## Target Output

- Single merged mesh with smooth skinning (automatic weights)
- Clean quad topology triangulated for export
- Mitten hands or 3-finger hands
- Simple hair shapes (spikes, bob, ponytail)
- Stylized faces (minimal geometry, texture-driven)

**Limitations:** No individual finger articulation, no facial blend shapes.

---

## Character Spec Format

```yaml
character:
  name: "character_id"
  tri_budget: 400

  # Optional: texturing config (handled by mesh-texturing-workflows)
  texturing:
    uv_mode: "smart_project"  # or "region_based"

  # Skeleton defines bones AND determines part orientations
  skeleton:
    - bone: pelvis
      parent: null
      head: [0, 0, 0.9]       # world position
      tail: [0, 0, 1.0]

    - bone: spine
      parent: pelvis
      head: [0, 0, 1.0]
      tail: [0, 0, 1.3]

    # Right side mirrors left
    - bone: arm_upper_R
      mirror: arm_upper_L

  # Parts reference bones - mesh extrudes along bone direction
  parts:
    torso:
      bone: spine
      base: hexagon(6)        # cross-section shape
      base_radius: 0.12
      steps:
        - extrude: 0.05, scale: 1.15
        - extrude: 0.15, scale: 1.0
        - extrude: 0.08, scale: 0.85
      cap_start: true
      cap_end: false          # open for neck

    # Right side mirrors left
    arm_upper_R:
      mirror: arm_upper_L
```

---

## Skeleton Definition

Each bone requires:
- `bone`: Unique bone name
- `parent`: Parent bone name (null for root)
- `head`: [x, y, z] world position of bone start
- `tail`: [x, y, z] world position of bone end

Or for mirrored bones:
- `bone`: Bone name (use `_R` suffix for right side)
- `mirror`: Source bone name to mirror (X-axis)

**Naming convention:** Use `_L` / `_R` suffixes for left/right bones.

---

## Part Definition

Each part requires:
- `bone`: Which bone this part follows
- `base`: Cross-section shape - `hexagon(6)`, `octagon(8)`, `square(4)`, `triangle(3)`
- `base_radius`: Starting radius in meters
- `steps`: List of extrusion operations
- `cap_start`: Close bottom (true/false)
- `cap_end`: Close top (true/false)

### Step Operations

```yaml
step:
  extrude: 0.1              # distance (required)
  scale: 1.2 | [X, Y]       # uniform or asymmetric
  bulge: -0.02 | [side, fb] # radial push: + front, - back
  tilt: 5 | [x, y]          # perpendicular rotation (degrees)
  translate: [x, y, z]      # offset (prefer bulge for anatomy)
  rotate: 15                # around bone axis
```

| Param | Effect |
|-------|--------|
| `scale [X,Y]` | Ellipse sizing (X=side, Y=depth) |
| `bulge` | Teardrop shape (asymmetric radial push) |
| `tilt` | Slant cross-section plane |

---

## Joint Seam Rules

**Critical:** Connected parts MUST share the same base vertex count.

```yaml
# CORRECT - both use hexagon(6)
torso:
  base: hexagon(6)
  cap_end: false

head:
  base: hexagon(6)    # matches torso
  cap_start: false

# INCORRECT - vertex mismatch = gaps
torso:
  base: octagon(8)    # 8 vertices
head:
  base: hexagon(6)    # 6 vertices - WON'T WELD
```

Parts are welded with 2mm tolerance. Ensure:
1. Same `base:` for connected parts
2. Matching end radius (final step scale)
3. Bone head/tail alignment at connection points

---

## Quick Reference

### Base Shapes

| Shape | Vertices | Tris/Step | Best For |
|-------|----------|-----------|----------|
| `triangle(3)` | 3 | 6 | Hair spikes, minimal |
| `square(4)` | 4 | 8 | Blocky/mecha, low budget |
| `hexagon(6)` | 6 | 12 | Standard characters |
| `octagon(8)` | 8 | 16 | Smooth organic |

### Triangle Formula

```
tris_per_part = base_verts × 2 × num_steps + cap_tris
cap_tris = base_verts - 2
```

### Budget Guidelines

| Budget | Bases | Steps/Part | Hands |
|--------|-------|------------|-------|
| 300 | square(4) | 2-3 | stub |
| 400 | square/hex | 3-4 | mitten |
| 500 | hexagon(6) | 4-5 | mitten+thumb |
| 700 | hex/oct | 5-7 | 3-finger |

---

## Workflow

### 1. Design Phase (character-designer agent)

1. Determine character type (humanoid, quadruped, creature)
2. Choose style preset (mecha, organic, armored, robed)
3. Set triangle budget
4. Generate character-spec.yaml

### 2. Generation Phase (character-generator agent)

1. Load character-spec.yaml
2. Create armature from skeleton
3. Build each part via extrude+scale
4. Merge and skin with automatic weights
5. Apply UVs
6. Export GLB

---

## Non-Humanoid Characters

The extrude+scale paradigm works for any creature. See `references/skeleton-presets.md` for:

| Creature | Key Difference |
|----------|----------------|
| Quadruped | Horizontal spine, 4 legs, tail |
| Serpent | Chain of segments, tubular body |
| Spider | 2 body segments, 8 legs |
| Bird | Wings use arm bone pattern |

---

## ZX Constraints

| Constraint | Limit |
|------------|-------|
| Max bones per game | 256 |
| Bones per vertex | 4 |
| Texture resolution | 512×512 max |
| Typical character tris | 300-500 |

---

## Normal Map Support (Optional)

Characters can use normal maps for surface detail (skin pores, cloth weave, armor scratches) at any triangle budget.

### When to Use Normal Maps

| Budget | Recommendation |
|--------|----------------|
| 300 | Skip - geometry too low for visible benefit |
| 400-500 | Optional - adds detail for hero characters |
| 700+ | Recommended - surface detail enhances quality |

### Enabling Normal Maps

Add to character spec:

```yaml
character:
  name: "hero_knight"
  tri_budget: 500
  use_normal_maps: true  # Enables tangent export
```

This triggers:
1. `mesh.calc_tangents()` before export
2. `export_tangents=True` in GLB export
3. Memory overhead: +4 bytes/vertex

### Normal Map Textures

Use the `procedural-normal-maps` skill to generate:
- Skin detail (subtle noise)
- Cloth weave patterns
- Armor scratches and dents
- Hair texture

Export as `{character}_normal.png` for auto-BC5 compression.

---

## Related

- **character-designer agent** - Generates character-spec.yaml from description
- **character-generator agent** - Builds mesh from spec
- **mesh-texturing-workflows skill** - Texture generation
- **procedural-animations skill** - Animation (separate workflow)
