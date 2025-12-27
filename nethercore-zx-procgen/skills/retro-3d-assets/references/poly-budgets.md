# Poly Budget Reference for Retro 3D Assets

Detailed triangle budget guidelines for authentic 32-bit era aesthetics.

## Character Budgets

### Minimal (80-150 tris)
Extremely blocky, relies heavily on texture for detail.

| Part | Triangles | Notes |
|------|-----------|-------|
| Head | 12-20 | Beveled box (8) or low sphere (12-20) |
| Torso | 16-30 | Simple box or tapered cylinder |
| Arms (each) | 8-16 | 4-sided tapered cylinder |
| Legs (each) | 8-16 | 4-sided tapered cylinder |
| Hands | 4-8 | Box or omit entirely |
| Feet | 4-8 | Box or wedge |

**Example:** Crowd NPCs, distant enemies, swarm units

### Standard (150-300 tris)
Typical retro protagonist level. Readable silhouette.

| Part | Triangles | Notes |
|------|-----------|-------|
| Head | 20-40 | 6-sided sphere, separate jaw optional |
| Torso | 30-50 | Beveled box, chest definition |
| Arms (each) | 15-25 | 6-sided cylinder, elbow bend |
| Legs (each) | 15-25 | 6-sided cylinder, knee bend |
| Hands | 8-15 | Mitten with thumb separation |
| Feet | 8-12 | Boot shape with toe |

**Example:** Player character, major NPCs, bosses

### Detailed (300-500 tris)
Maximum detail for hero moments, close-ups.

| Part | Triangles | Notes |
|------|-----------|-------|
| Head | 40-80 | 8-sided sphere, facial features modeled |
| Torso | 50-80 | Muscle definition, armor plates |
| Arms (each) | 25-40 | 8-sided, bicep/forearm separation |
| Legs (each) | 25-40 | 8-sided, thigh/calf separation |
| Hands | 15-30 | Individual fingers possible |
| Feet | 12-20 | Detailed boot/shoe |

**Example:** Title screen hero, cutscene characters

---

## Prop Budgets

### Pickups & Collectibles (10-40 tris)
Simple shapes, readable at distance.

| Item | Triangles | Shape |
|------|-----------|-------|
| Coin | 8-12 | 6-8 sided cylinder |
| Health pack | 12-20 | Cross or box |
| Ammo box | 8 | Cube |
| Key | 10-16 | Simple key silhouette |
| Gem | 12-24 | Double-ended crystal |

### Interactive Props (40-100 tris)

| Item | Triangles | Notes |
|------|-----------|-------|
| Crate | 8-24 | Cube, optional edge bevels |
| Barrel | 12-24 | 6-8 sided cylinder |
| Door | 8-16 | Flat panel with frame |
| Lever | 10-20 | Base + handle |
| Chest | 16-40 | Box with lid geometry |

### Decorative Props (60-200 tris)

| Item | Triangles | Notes |
|------|-----------|-------|
| Chair | 30-60 | Visible from multiple angles |
| Table | 20-40 | Tabletop + legs |
| Lamp | 20-50 | Base + shade |
| Statue | 80-200 | Hero prop, central focus |
| Tree | 40-100 | Trunk + 3-6 billboard leaves |

---

## Vehicle Budgets

| Type | Triangles | Notes |
|------|-----------|-------|
| Simple car | 80-150 | Box body, wheel circles |
| Detailed car | 150-300 | Fenders, hood detail |
| Spaceship | 100-250 | Modular sections |
| Tank | 150-350 | Turret separate from body |
| Motorcycle | 80-150 | Wheels, frame, handlebars |

---

## Environment Budgets

### Modular Pieces

| Piece | Triangles | Notes |
|-------|-----------|-------|
| Wall segment | 2-8 | Single or double-sided |
| Floor tile | 2 | Single quad |
| Corner (inner) | 4-8 | 90-degree turn |
| Corner (outer) | 4-8 | 90-degree turn |
| Pillar | 8-16 | 4-8 sided cylinder |
| Archway | 12-24 | Curved top optional |
| Stairs (per step) | 2 | Stack quads for staircase |
| Ramp | 2-4 | Single sloped quad |
| Platform | 4-16 | Flat with edge detail |

### Large Structures

| Structure | Triangles | Notes |
|-----------|-----------|-------|
| Building (exterior) | 100-400 | Multiple modular sections |
| Room (interior) | 50-200 | Walls, floor, ceiling |
| Bridge | 30-100 | Span + supports |
| Tower | 50-150 | Cylindrical or square |

---

## Poly Budget Strategies

### Where to Spend Polygons

1. **Silhouette edges** - Curves visible against background
2. **Character faces** - Most expressive area
3. **Hands** - Interact with objects, often visible
4. **Hero props** - Central focus items
5. **Moving parts** - Joints need geometry to bend

### Where to Save Polygons

1. **Hidden surfaces** - Remove unseen faces
2. **Flat areas** - Single quad suffices
3. **Distant objects** - Use fewer sides
4. **Texture detail** - Let texture do the work
5. **Symmetry** - Mirror modifier to save authoring time

---

## Poly Count Verification

### Rust

```rust
fn count_triangles(mesh: &UnpackedMesh) -> usize {
    mesh.triangles.len() / 3
}

fn verify_budget(mesh: &UnpackedMesh, max_tris: usize, name: &str) {
    let count = count_triangles(mesh);
    if count > max_tris {
        eprintln!("WARNING: {} has {} tris (budget: {})", name, count, max_tris);
    }
}
```

### Python

```python
def verify_poly_budget(mesh, max_tris, name):
    tri_count = len(mesh.faces)
    if tri_count > max_tris:
        print(f"WARNING: {name} has {tri_count} tris (budget: {max_tris})")
    return tri_count <= max_tris
```

---

## Era Reference

Actual poly counts from 32-bit era games:

| Game | Characters | Environment |
|------|------------|-------------|
| Crash Bandicoot | ~500 tris | ~3000 per scene |
| Tomb Raider | ~500 tris | Modular rooms |
| Metal Gear Solid | ~300-800 tris | ~5000 per area |
| Final Fantasy VII | ~250-500 tris | Pre-rendered BGs |
| Spyro | ~300-600 tris | Large open areas |

ZX targets the lower end of this range for maximum on-screen objects with modern performance overhead.
