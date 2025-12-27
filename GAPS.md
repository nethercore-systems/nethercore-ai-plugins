# Plugin Coverage Gaps

Identified gaps in the nethercore-ai-plugins suite for complete end-to-end ZX game development.

## Minor Improvements:
- Set all to version 1.0
- Set all licenses to MIT & APACHE (similiar to RUST projects)
- Ensure all docs, marketplace, and claude.md files (and others) are ALL up to date

## Gap Summary

| # | Gap | Priority | Plugin | Type | FFI Exists |
|---|-----|----------|--------|------|------------|
| 1 | XM Tracker Music | HIGH | procgen | Skill | N/A |
| 2 | Publishing Workflow | HIGH | NEW | Plugin | N/A |
| 3 | Platform Page Assets | HIGH | publish | Skill | N/A |
| 4 | UI/UX Patterns | MEDIUM | game-design | Skill | Yes |
| 5 | Game Feel / Polish | MEDIUM | game-design | Skill | Yes |
| 6 | Testing & Debug | MEDIUM | zx-dev | Skill | Yes |
| 7 | Level Design | LOW | game-design | Skill | N/A |
| 8 | Environment Processing Unit (EPU) | MEDIUM | zx-dev | Skill | Yes |
| 9 | Split-Screen / Viewport | MEDIUM | game-design | Skill | Yes |
| 10 | Stencil / Masked Rendering | LOW | zx-dev | Skill | Yes |
| 11 | Custom Fonts | LOW | zx-dev | Skill | Yes |
| 12 | Save Data Patterns | MEDIUM | game-design | Skill | Yes |
| 13 | 3D Billboards & Particles | LOW | zx-dev | Skill | Yes |
| 14 | UV-Aware Texturing & Atlasing | MEDIUM | procgen | Skill | N/A |
| 15 | Animated Character Pipeline | HIGH | procgen | Skill + Agent | Yes |
| 16 | Physics & Collision | HIGH | game-design | Skill | N/A (game logic) |
| 17 | Camera Implementation | MEDIUM | zx-dev | Skill | Yes (FFI exists) |
| 18 | Gameplay Mechanics Library | MEDIUM | game-design | Skill | N/A (game logic) |
| 19 | AI & Behavior Patterns | LOW | game-design | Skill | N/A (game logic) |
| 20 | Multiplayer Rendering Patterns | HIGH | game-design | Skill | Yes (FFI exists) |
| 21 | BVH/Motion Capture Integration | HIGH | procgen | Skill | N/A |
| 22 | AI-First Creative Asset Pipeline | HIGH | procgen | Skill + Agents | N/A |
| 23 | Advanced Techniques & Decision Guides | MEDIUM | procgen | Skill | N/A |

### Architectural Refactors

| # | Refactor | Priority | Action |
|---|----------|----------|--------|
| A1 | Orchestrator Plugin | MEDIUM | Move game-orchestrator from game-design → NEW nethercore-zx-orchestrator |
| A2 | Skeletal Rigging Skill | MEDIUM | Split procedural-animations → NEW skeletal-rigging skill in procgen |
| A3 | Mocap Integration Skill | HIGH | NEW mocap-integration skill for BVH parsing, databases, retargeting |
| A4 | Semantic Asset Language Skill | HIGH | NEW semantic-asset-language skill for style tokens, SADL |
| A5 | Creative Agents Suite | HIGH | NEW asset-designer, asset-generator, asset-critic, creative-orchestrator agents |

---

## Gap 1: Procedural Music (XM Tracker)

**Status:** Sound effects covered, music composition NOT covered.

The procgen plugin has skills for textures, meshes, sounds (SFX), and animations - but no guidance for creating XM tracker music. Currently just says "use MilkyTracker" with no procedural/compositional help.

**Missing:**
- XM module structure (patterns, instruments, samples)
- XM effects (arpeggio, vibrato, portamento, volume slides)
- Composition patterns (melodies, bass, percussion, pads)
- Genre templates (action, puzzle, title screen, boss)
- Loop point design for seamless looping
- Integration with procedural-sounds for custom instrument samples

**Prompt for plugin-dev:**
```
Add skill "procedural-music" to nethercore-zx-procgen. Triggers: "create music",
"XM tracker", "compose", "soundtrack", "tracker module", "game music". Cover: XM
structure (patterns, instruments, samples), XM effects (arpeggio, vibrato, portamento,
volume slides, etc), composition patterns (melodies, bass, percussion, pads), genre
templates (action, title, boss, ambient), loop points. Integration: use procedural-
sounds skill to generate custom instrument samples as WAVs. Tools: MilkyTracker/
OpenMPT. Constraints: 22kHz samples, 16MB ROM. Add references/ for effect commands
and composition patterns. ~1500 words.
```

---

## Gap 2: Publishing Workflow

**Status:** Documentation exists in nethercore repo, NO plugin guidance.

Developers can build games but have no AI-assisted path to publish on nethercore.systems.

**Missing:**
- ROM packaging guidance (`cargo xtask cart create-zx`)
- Metadata creation (title, description, tags, version)
- Upload process to nethercore.systems
- Update/versioning workflow

**Prompt for plugin-dev:**
```
Create plugin "nethercore-zx-publish" with skill "publishing-workflow". Triggers:
"publish game", "release game", "upload", "create ROM", "package game", "nether pack".
Cover: ROM creation (cargo xtask cart create-z flags), metadata (id, title, author,
version, description, tags), nether.toml packaging, nethercore.systems upload,
versioning/updates. Add /publish-game command. Source: nethercore/docs/book/src/
guides/publishing.md. ~1500 words.
```

---

## Gap 3: Platform Page Assets

**Status:** NOT covered at all.

Publishing requires visual assets that no plugin helps create.

**Missing:**
- Thumbnail creation (64x64 PNG icon for library)
- Screenshot capture (up to 5 PNGs for platform page)
- Platform description copywriting (compelling game descriptions)
- Tag/category selection guidance

**Prompt for plugin-dev:**
```
Add skill "platform-assets" to nethercore-zx-publish. Triggers: "thumbnail", "icon",
"screenshot", "platform page", "store page", "store listing", "game description", "platform listing". Cover: thumbnail
(64x64 PNG, composition, clarity at small size), screenshots (3-5 gameplay images,
what to capture), platform copy (hook, features, call-to-action), tags/categories.
Add /prepare-platform-assets command. Use references/ for copy templates. ~1200 words.
```

---

## Gap 4: UI/UX Patterns

**Status:** 2D drawing FFI exists in zx-dev, but no design patterns for menus or HUDs.

**Missing:**
- Menu state machines (title → game → pause → gameover)
- HUD layout patterns (health, score, minimap)
- Controller navigation (focus states, selection)
- Text/font rendering patterns

**Prompt for plugin-dev:**
```
Add skill "ui-patterns" to nethercore-zx-game-design. Triggers: "menu", "HUD",
"UI", "pause menu", "title screen", "user interface". Cover: menu state machines,
HUD layouts (health bars, score, minimap), controller navigation (focus, selection),
text rendering with rom_font. Reference 2D drawing FFI from zx-dev. Use references/
for common UI layouts. ~1200 words.
```

---

## Gap 5: Game Feel / Polish

**Status:** Not covered. Critical for quality but no guidance exists.

**Missing:**
- Screen shake implementation
- Hit pause / freeze frames
- Particle effects basics
- Sound-visual synchronization
- Input responsiveness

**Prompt for plugin-dev:**
```
Add skill "game-feel" to nethercore-zx-game-design. Triggers: "game feel", "juice",
"polish", "screen shake", "particles", "impact", "feedback". Cover: screen shake,
hit pause/freeze frames, particle basics, sound-visual sync, anticipation-action-
follow-through, input responsiveness. Tie to ZX FFI (camera, timing, audio). Include
code snippets. ~1000 words.
```

---

## Gap 6: Testing & Debug

**Status:** Debug FFI exists, minimal plugin guidance.

ZX has a debug inspection system (F3 panel, `debug_register_*`) but no skill teaches its use.

**Missing:**
- Debug panel usage (F3, registering values, grouping)
- Sync testing for multiplayer (`--sync-test`, `--p2p-test`)
- Common debugging patterns
- Performance profiling basics

**Prompt for plugin-dev:**
```
Add skill "debugging-guide" to nethercore-zx-dev. Triggers: "debug", "F3",
"debug_register", "sync test", "desync", "profiling". Cover: F3 panel usage,
debug_register_*/debug_watch_* FFI, debug_group organization, frame stepping
(F5/F6/F7/F8), --sync-test and --p2p-test flags. Reference include/zx.rs debug
section. ~1000 words.
```

---

## Gap 7: Level Design Patterns

**Status:** Not covered.

No guidance for spatial content design beyond procedural asset generation.

**Missing:**
- Tile-based level design for 2D games
- 3D level layout principles
- Procedural level generation patterns
- Pacing and difficulty curves

**Prompt for plugin-dev:**
```
Add skill "level-design" to nethercore-zx-game-design. Triggers: "level design",
"tile map", "world layout", "level generation", "map design". Cover: tile-based
design (2D platformer patterns), 3D spatial layout (third-person), procedural
generation basics (rooms, corridors), pacing/difficulty curves. Tie to ZX
constraints (ROM budget for level data). Use references/ for layouts. ~1200 words.
```

---

## Gap 8: Environment Processing Unit (EPU)

**Status:** FFI exists with 8 environment modes, NO plugin documentation.

The ZX console has a powerful EPU for procedural backgrounds and post-effects, but it's completely undocumented in the plugins.

**FFI Functions (from zx.rs):**
- `env_gradient(top_color, bottom_color, dither)` - Vertical gradient background
- `env_scatter(color, density, size, seed)` - Scattered particles/stars
- `env_lines(color, count, direction, speed)` - Animated lines
- `env_silhouette(color, texture, scale)` - Silhouette layer
- `env_rectangles(color, count, seed)` - Random rectangles
- `env_room(floor, ceiling, left, right)` - 3D room projection
- `env_curtains(color, count, speed)` - Animated curtains
- `env_rings(color, count, speed)` - Expanding rings
- `env_blend(mode)` - Blend mode for environment layer

**Missing:**
- EPU mode overview and use cases
- Parameter tuning for each mode
- Combining multiple EPU effects
- Performance characteristics
- Visual examples

**Prompt for plugin-dev:**
```
Add skill "environment-effects" to nethercore-zx-dev. Triggers: "EPU", "environment",
"background effect", "env_gradient", "env_scatter", "procedural background", "sky
effect". Cover: all 8 env modes (gradient, scatter, lines, silhouette, rectangles,
room, curtains, rings), env_blend modes, parameter tuning, combining effects, use
cases (space game stars, racing speed lines, title screen). Source: include/zx.rs
env section. ~1200 words.
```

---

## Gap 9: Split-Screen / Viewport

**Status:** FFI exists, NO multiplayer rendering guidance.

Local multiplayer games need split-screen rendering, but no plugin covers viewport setup.

**FFI Functions (from zx.rs):**
- `viewport(x, y, width, height)` - Set render viewport
- `viewport_clear()` - Reset to full screen

**Missing:**
- Split-screen layout patterns (2-player horizontal, vertical, 4-player grid)
- Per-viewport camera setup
- UI overlay on split-screen
- Performance with multiple viewports

**Prompt for plugin-dev:**
```
Add skill "split-screen-rendering" to nethercore-zx-game-design. Triggers: "split
screen", "local multiplayer", "viewport", "2-player", "4-player local", "couch
co-op". Cover: viewport() FFI, split layouts (2P horizontal/vertical, 3P, 4P grid),
per-viewport camera, shared UI overlay, performance (4 viewports = 4x draw calls).
Tie to multiplayer-design skill. ~800 words.
```

---

## Gap 10: Stencil / Masked Rendering

**Status:** FFI exists for stencil operations, NO usage patterns documented.

Stencil buffer enables portals, scopes, mirrors, and masked effects.

**FFI Functions (from zx.rs):**
- `stencil_begin()` - Start writing to stencil buffer
- `stencil_end()` - Stop writing to stencil buffer
- `stencil_clear()` - Clear stencil buffer
- `stencil_invert()` - Invert stencil mask

**Missing:**
- Portal/window rendering pattern
- Scope/binocular effect
- Mirror reflection technique
- UI masking for non-rectangular elements
- Stencil + depth interaction

**Prompt for plugin-dev:**
```
Add skill "stencil-effects" to nethercore-zx-dev. Triggers: "stencil", "portal",
"scope", "masked rendering", "mirror", "window effect". Cover: stencil buffer
basics, portal/window pattern (draw mask, then scene), scope/binocular effect,
mirror reflections (stencil + flipped camera), UI masking. Include code examples.
Source: include/zx.rs stencil section. ~800 words.
```

---

## Gap 11: Custom Fonts

**Status:** FFI exists for font loading, only default font documented.

Games often need custom bitmap fonts for style, but font creation isn't covered.

**FFI Functions (from zx.rs):**
- `load_font(data_ptr, data_len)` - Load custom font from data
- `load_font_ex(data_ptr, data_len, char_width, char_height)` - Load with explicit sizing
- `font_bind(font_handle)` - Bind font for text rendering
- `rom_font(id_ptr, id_len)` - Load font from ROM

**Missing:**
- Bitmap font creation (grid layout, character mapping)
- Font texture format requirements
- Variable-width font support (if any)
- Font atlas packing
- Integration with procgen for procedural fonts

**Prompt for plugin-dev:**
```
Add skill "custom-fonts" to nethercore-zx-dev. Triggers: "custom font", "bitmap
font", "load_font", "font_bind", "game font", "pixel font". Cover: font texture
format (character grid), load_font vs load_font_ex, character mapping, rom_font
for bundled fonts, creation tools (Hiero, BMFont, hand-drawn). Tie to procedural-
textures for font atlas creation. ~800 words.
```

---

## Gap 12: Save Data Patterns

**Status:** FFI exists for save/load, NO design patterns documented.

Games need save systems, but the plugins don't cover save data architecture.

**FFI Functions (from zx.rs):**
- `save(slot, data_ptr, data_len)` - Save data to slot
- `load(slot, data_ptr, max_len) -> actual_len` - Load data from slot
- `delete(slot)` - Delete save slot
- `save_exists(slot) -> bool` - Check if save exists

**Missing:**
- Save data structure design (what to save)
- Serialization patterns (binary format, versioning)
- Multiple save slots UX
- Auto-save timing
- Save corruption prevention
- Rollback-safe save design (don't save during update())

**Prompt for plugin-dev:**
```
Add skill "save-systems" to nethercore-zx-game-design. Triggers: "save game", "save
data", "load game", "save slot", "persistent storage", "game progress". Cover: what
to save (progress, settings, high scores), save data structure design, binary
serialization (bytemuck), version migration, multiple slots UX, auto-save patterns,
rollback safety (save only in render or between frames). ~1000 words.
```

---

## Gap 13: 3D Billboards & Particles

**Status:** FFI exists for billboards, NO particle system patterns.

Billboards are documented in FFI but particle effects using them aren't covered.

**FFI Functions (from zx.rs):**
- `draw_billboard(texture, x, y, z, width, height)` - Camera-facing quad
- `draw_billboard_region(texture, x, y, z, width, height, u, v, uw, vh)` - Billboard with UV region

**Missing:**
- Particle emitter patterns (spawn, update, render)
- Billboard sprite sheets (animation via UV regions)
- Particle pooling for performance
- Common effects (smoke, fire, sparks, dust)
- Soft particles with depth
- Integration with game-feel skill

**Prompt for plugin-dev:**
```
Add skill "billboard-particles" to nethercore-zx-dev. Triggers: "billboard",
"particles", "draw_billboard", "sprite 3D", "smoke effect", "sparks", "particle
system". Cover: billboard basics, particle emitter pattern (spawn/update/render),
sprite sheet animation via UV regions, particle pooling, common effects (smoke,
fire, sparks, dust, rain), performance budgets. Tie to game-feel skill. ~1000 words.
```

---

## Gap 14: UV-Aware Texturing & Atlasing

**Status:** Textures and meshes documented separately, integration workflow MISSING.

The current skills treat texture generation and mesh generation as independent concerns. But real workflows need them connected:
- "I generated a character mesh, how do I procedurally texture it?"
- "How do I create a texture atlas for my 10 props?"
- "How do I place a logo on my vehicle's UV layout?"

**Missing:**

### UV-Aware Texture Generation
- Reading mesh UV bounds to size textures correctly
- Generating textures that match specific UV islands (body, face, clothing)
- Painting texture regions based on UV layout
- Seamless tiling across UV seams

### Texture Atlasing
- Combining multiple textures into single atlas
- UV remapping after atlas packing
- Atlas layout optimization (bin packing)
- Shared atlas for multiple meshes (batching)

### Character Texturing Workflows
- Body region texturing (skin gradients, clothing zones)
- Face detail placement (eyes, mouth regions in UV space)
- Procedural clothing patterns on UV islands
- Variation generation (skin tones, outfit colors)

### Decal/Detail Projection
- Projecting details onto UV space
- Logo/emblem placement on vehicles/armor
- Damage/wear overlay generation
- Baked mesh data (AO, curvature, thickness from geometry)

### Multi-Material Workflows
- Different materials for mesh regions (metal armor + cloth + skin)
- Material ID masks from UV regions
- Coordinated MRE/SSE generation per region

### UV-to-Texture Coordinate Mapping (NEW)

Connecting mesh UVs to texture generation:

```rust
/// Read UV bounds from mesh to size texture correctly
pub fn get_uv_bounds(mesh: &Mesh) -> UvBounds {
    let mut min_u = f32::INFINITY;
    let mut max_u = f32::NEG_INFINITY;
    let mut min_v = f32::INFINITY;
    let mut max_v = f32::NEG_INFINITY;

    for uv in &mesh.uvs {
        min_u = min_u.min(uv[0]);
        max_u = max_u.max(uv[0]);
        min_v = min_v.min(uv[1]);
        max_v = max_v.max(uv[1]);
    }

    UvBounds { min_u, max_u, min_v, max_v }
}

/// Calculate optimal texture resolution based on UV space usage and texel density
pub fn calculate_texture_resolution(
    mesh: &Mesh,
    target_texel_density: f32,  // Texels per world unit
) -> (u32, u32) {
    // Calculate world-space surface area
    let mut total_area = 0.0;
    for tri in mesh.triangles() {
        total_area += triangle_area_3d(
            mesh.vertices[tri.0],
            mesh.vertices[tri.1],
            mesh.vertices[tri.2],
        );
    }

    // Calculate UV-space coverage (0-1 range)
    let bounds = get_uv_bounds(mesh);
    let uv_width = bounds.max_u - bounds.min_u;
    let uv_height = bounds.max_v - bounds.min_v;

    // Desired texture size based on target density
    let desired_texels = (total_area * target_texel_density * target_texel_density).sqrt();

    // Account for UV coverage efficiency
    let coverage = uv_width * uv_height;
    let raw_size = (desired_texels / coverage.sqrt()) as u32;

    // Snap to power of 2
    let size = raw_size.next_power_of_two().min(2048);

    (size, size)
}

/// Map texture coordinates to UV islands
pub struct UvIslandMapper {
    islands: Vec<UvIsland>,
}

impl UvIslandMapper {
    /// Extract UV islands from mesh (connected UV regions)
    pub fn from_mesh(mesh: &Mesh) -> Self {
        let mut visited = vec![false; mesh.triangles().len()];
        let mut islands = vec![];

        for tri_idx in 0..mesh.triangles().len() {
            if visited[tri_idx] { continue; }

            // Flood-fill to find connected island
            let island = flood_fill_island(mesh, tri_idx, &mut visited);
            islands.push(island);
        }

        Self { islands }
    }

    /// Get island containing a UV coordinate
    pub fn island_at(&self, u: f32, v: f32) -> Option<usize> {
        for (idx, island) in self.islands.iter().enumerate() {
            if island.contains(u, v) {
                return Some(idx);
            }
        }
        None
    }

    /// Generate texture with per-island materials
    pub fn generate_textured(
        &self,
        width: u32,
        height: u32,
        island_materials: &[MaterialGenerator],
    ) -> Texture {
        let mut texture = Texture::new(width, height);

        for y in 0..height {
            for x in 0..width {
                let u = x as f32 / width as f32;
                let v = y as f32 / height as f32;

                if let Some(island_idx) = self.island_at(u, v) {
                    let color = island_materials[island_idx].sample(u, v);
                    texture.set_pixel(x, y, color);
                }
            }
        }

        texture
    }
}

/// Texture atlas with UV remapping
pub struct TextureAtlas {
    pub texture: Texture,
    pub uv_transforms: Vec<UvTransform>,  // Per-source-mesh UV remapping
}

pub struct UvTransform {
    pub offset: [f32; 2],
    pub scale: [f32; 2],
}

impl TextureAtlas {
    /// Create atlas from multiple textures, returning UV transforms
    pub fn pack(textures: &[&Texture], padding: u32) -> Self {
        // Bin packing to arrange textures
        let layout = pack_rectangles(
            textures.iter().map(|t| (t.width + padding, t.height + padding)).collect()
        );

        // Calculate atlas size (power of 2)
        let atlas_width = layout.total_width.next_power_of_two();
        let atlas_height = layout.total_height.next_power_of_two();

        let mut atlas = Texture::new(atlas_width, atlas_height);
        let mut uv_transforms = vec![];

        for (idx, placement) in layout.placements.iter().enumerate() {
            // Copy texture to atlas
            atlas.blit(textures[idx], placement.x, placement.y);

            // Calculate UV transform for this texture
            uv_transforms.push(UvTransform {
                offset: [
                    placement.x as f32 / atlas_width as f32,
                    placement.y as f32 / atlas_height as f32,
                ],
                scale: [
                    textures[idx].width as f32 / atlas_width as f32,
                    textures[idx].height as f32 / atlas_height as f32,
                ],
            });
        }

        Self { texture: atlas, uv_transforms }
    }

    /// Remap mesh UVs to atlas coordinates
    pub fn remap_uvs(&self, mesh: &mut Mesh, atlas_index: usize) {
        let transform = &self.uv_transforms[atlas_index];

        for uv in &mut mesh.uvs {
            uv[0] = uv[0] * transform.scale[0] + transform.offset[0];
            uv[1] = uv[1] * transform.scale[1] + transform.offset[1];
        }
    }
}
```

**Prompt for plugin-dev:**
```
Add skill "mesh-texturing-workflows" to nethercore-zx-procgen. Triggers: "texture
character", "UV texture", "texture atlas", "atlas packing", "UV-aware texture",
"procedural character texture", "decal projection", "multi-material mesh", "bake
texture". Cover: UV-aware generation (reading UV bounds, painting UV regions),
atlasing (bin packing, UV remapping), character workflows (body zones, face regions,
clothing), decal projection, baked maps (AO from geometry). Integration: uses
procedural-meshes for UV data, procedural-textures for generation. Include Python
trimesh + PIL examples. ~1500 words.
```

**Example Workflow (Character):**
```
1. Generate character mesh with UVs (procedural-meshes)
   → Body UV island, Head UV island, Clothing UV island

2. Generate UV-aware textures (NEW skill)
   → Skin gradient mapped to body island bounds
   → Face details at head island coordinates
   → Fabric pattern on clothing island

3. Generate material maps (procedural-textures)
   → MRE with skin roughness, cloth roughness, metal armor

4. Export coordinated set
   → character_albedo.png (all regions)
   → character_mre.png (material properties per region)
```

---

## Gap 15: Animated Character Pipeline

**Status:** Individual skills exist but are DISCONNECTED. No unified workflow.

**The Core Problem:**
A user says: *"Generate a humanoid character with walk animation for my ZX game."*

Currently, Claude must:
1. Use procedural-meshes (but no guidance on animation-ready topology)
2. Somehow generate UVs (briefly mentioned)
3. Use procedural-textures (doesn't know the UV layout)
4. Use procedural-animations for skeleton (mixed with animation content)
5. Manually calculate bone weights (buried in animations skill)
6. Generate walk cycle (covered)
7. Export to GLTF with skinning (NOT documented)

**Each step has gaps or disconnects.**

### The Complete Pipeline (What Should Exist)

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANIMATED CHARACTER PIPELINE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PHASE A: MESH GENERATION                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Input: Character description (humanoid, quadruped, etc) │    │
│  │ Process:                                                 │    │
│  │   1. Generate base mesh with DEFORMATION TOPOLOGY        │    │
│  │      - Edge loops at joints (elbow, knee, shoulder)      │    │
│  │      - Sufficient polys in bend areas                    │    │
│  │      - Clean quads (triangulated later)                  │    │
│  │   2. Generate UVs with SEMANTIC REGIONS                  │    │
│  │      - Body island, Head island, Limbs, Clothing         │    │
│  │   3. Respect ZX poly budget (200-500 for characters)     │    │
│  │ Output: Mesh with UVs, ready for skinning                │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  PHASE B: TEXTURING                                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Input: Mesh with UVs + character description             │    │
│  │ Process:                                                 │    │
│  │   1. Read UV bounds from mesh                            │    │
│  │   2. Generate albedo mapped to UV regions                │    │
│  │   3. Generate material maps (MRE/SSE per region)         │    │
│  │   4. Size to power-of-2, max 256x256 for characters      │    │
│  │ Output: Albedo + material textures                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  PHASE C: SKELETON CREATION                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Input: Mesh geometry + character type                    │    │
│  │ Process:                                                 │    │
│  │   1. Define bone hierarchy (root → spine → limbs)        │    │
│  │   2. Position bones at joint locations                   │    │
│  │   3. Calculate inverse bind matrices                     │    │
│  │   4. ZX constraint: reasonable bone count (<50, 256 MAX) │    │
│  │ Output: Skeleton with hierarchy + inverse binds          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  PHASE D: SKINNING (WEIGHT PAINTING)                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Input: Mesh + Skeleton                                   │    │
│  │ Process:                                                 │    │
│  │   1. Calculate bone weights per vertex                   │    │
│  │      - Distance-based (simple)                           │    │
│  │      - Heat diffusion (better quality)                   │    │
│  │   2. Normalize weights (sum to 1.0)                      │    │
│  │   3. Limit to 4 bones per vertex (ZX requirement)        │    │
│  │   4. Assign bone indices                                 │    │
│  │ Output: Mesh with bone indices + weights per vertex      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  PHASE E: ANIMATION                                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Input: Skeleton + animation type (walk, run, idle)       │    │
│  │ Process:                                                 │    │
│  │   1. Generate procedural keyframes OR                    │    │
│  │   2. Define animation clips with bone transforms         │    │
│  │   3. Handle looping (seamless start/end)                 │    │
│  │ Output: Animation data (bone transforms over time)       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  PHASE F: EXPORT                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Input: Mesh + Textures + Skeleton + Skinning + Animation │    │
│  │ Process:                                                 │    │
│  │   1. Export GLTF/GLB with all data                       │    │
│  │   2. Triangulate mesh                                    │    │
│  │   3. Include skeleton as GLTF skin                       │    │
│  │   4. Include animation as GLTF animation                 │    │
│  │   5. Reference textures                                  │    │
│  │ Output: character.gltf + textures (ZX-ready)             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  PHASE G: INTEGRATION                                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ nether.toml entries:                                     │    │
│  │   [[assets.meshes]]                                      │    │
│  │   id = "character"                                       │    │
│  │   path = "assets/character.gltf"                         │    │
│  │                                                          │    │
│  │   [[assets.skeletons]]                                   │    │
│  │   id = "character_rig"                                   │    │
│  │   path = "assets/character.gltf"                         │    │
│  │                                                          │    │
│  │   [[assets.animations]]                                  │    │
│  │   id = "walk"                                            │    │
│  │   path = "assets/character.gltf#walk"                    │    │
│  │                                                          │    │
│  │   [[assets.textures]]                                    │    │
│  │   id = "character_albedo"                                │    │
│  │   path = "assets/character_albedo.png"                   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### ZX-Specific Requirements

| Requirement | Constraint | Current Coverage |
|-------------|------------|------------------|
| Max bones per vertex | 4 | ⚠️ Mentioned but not enforced |
| Bone matrix format | 3x4 column-major | ✅ Documented |
| Skinned vertex format | FORMAT_SKINNED flag | ✅ Documented |
| Skeleton loading | `rom_skeleton`, `skeleton_bind` | ✅ Documented |
| Bone transforms | `set_bones()` | ✅ Documented |
| Poly budget | 200-500 for characters | ⚠️ In constraints, not meshes |
| Texture size | 256x256 typical for characters | ❌ Not in textures skill |

### What's Missing Per Phase

| Phase | Current Skill | Gap |
|-------|---------------|-----|
| A: Mesh | procedural-meshes | No deformation topology guidance |
| B: Texture | procedural-textures | No UV-awareness (Gap 14) |
| C: Skeleton | procedural-animations | Mixed with animation (A2 split) |
| D: Skinning | procedural-animations | Buried, no standalone guidance |
| E: Animation | procedural-animations | ✅ Covered |
| F: Export | NONE | ❌ No GLTF skinned export docs |
| G: Integration | zx-game-development | ⚠️ Partial |

### GLTF Skinned Export Documentation (NEW)

Complete guide for exporting skinned meshes with animations to GLTF:

```rust
/// GLTF Skinned Mesh Export
///
/// GLTF 2.0 stores skinned meshes using:
/// - mesh: geometry with JOINTS_0 and WEIGHTS_0 attributes
/// - skin: bone hierarchy with inverse bind matrices
/// - nodes: skeleton bone transforms (scene graph)
/// - animations: per-bone transforms over time

use gltf_json as json;

/// Complete skinned character export
pub struct GltfSkinnedExporter {
    root: json::Root,
    buffers: Vec<Vec<u8>>,
}

impl GltfSkinnedExporter {
    /// Export complete skinned character to GLTF
    pub fn export(
        mesh: &SkinnedMesh,
        skeleton: &Skeleton,
        animations: &[AnimationClip],
        textures: &[Texture],
    ) -> GltfOutput {
        let mut exporter = Self::new();

        // 1. Export skeleton as node hierarchy
        let joint_indices = exporter.export_skeleton(skeleton);

        // 2. Export skin (inverse bind matrices)
        let skin_index = exporter.export_skin(skeleton, &joint_indices);

        // 3. Export skinned mesh with bone indices/weights
        let mesh_index = exporter.export_skinned_mesh(mesh);

        // 4. Create scene node that references mesh and skin
        exporter.create_skinned_node(mesh_index, skin_index, &joint_indices);

        // 5. Export animations
        for clip in animations {
            exporter.export_animation(clip, &joint_indices);
        }

        // 6. Export textures and materials
        for texture in textures {
            exporter.export_texture(texture);
        }

        exporter.finalize()
    }

    /// Export skeleton as GLTF node hierarchy
    fn export_skeleton(&mut self, skeleton: &Skeleton) -> Vec<u32> {
        let mut joint_indices = vec![];

        for (bone_idx, bone) in skeleton.bones.iter().enumerate() {
            let node = json::Node {
                name: Some(bone.name.clone()),
                translation: Some(bone.local_position.into()),
                rotation: Some(bone.local_rotation.into()),
                scale: Some([1.0, 1.0, 1.0]),
                children: None,  // Set after all nodes created
                ..Default::default()
            };

            let node_index = self.root.nodes.len() as u32;
            self.root.nodes.push(node);
            joint_indices.push(node_index);
        }

        // Set parent-child relationships
        for (bone_idx, bone) in skeleton.bones.iter().enumerate() {
            if let Some(parent_idx) = bone.parent {
                let parent_node = &mut self.root.nodes[joint_indices[parent_idx] as usize];
                let children = parent_node.children.get_or_insert(vec![]);
                children.push(json::Index::new(joint_indices[bone_idx]));
            }
        }

        joint_indices
    }

    /// Export skin with inverse bind matrices
    fn export_skin(&mut self, skeleton: &Skeleton, joints: &[u32]) -> u32 {
        // Calculate inverse bind matrices
        let inverse_binds: Vec<[[f32; 4]; 4]> = skeleton.bones.iter()
            .map(|bone| bone.inverse_bind_matrix)
            .collect();

        // Store in buffer as MAT4 accessor
        let ibm_data = bytemuck::cast_slice(&inverse_binds);
        let buffer_view_idx = self.add_buffer_view(ibm_data, None);
        let accessor_idx = self.add_accessor(
            buffer_view_idx,
            json::accessor::Type::Mat4,
            json::accessor::ComponentType::F32,
            skeleton.bones.len(),
        );

        let skin = json::Skin {
            name: Some("character_skin".to_string()),
            inverse_bind_matrices: Some(json::Index::new(accessor_idx)),
            joints: joints.iter().map(|&j| json::Index::new(j)).collect(),
            skeleton: Some(json::Index::new(joints[0])),  // Root bone
            ..Default::default()
        };

        let skin_idx = self.root.skins.len() as u32;
        self.root.skins.push(skin);
        skin_idx
    }

    /// Export skinned mesh with JOINTS_0 and WEIGHTS_0 attributes
    fn export_skinned_mesh(&mut self, mesh: &SkinnedMesh) -> u32 {
        // Positions
        let pos_view = self.add_buffer_view(
            bytemuck::cast_slice(&mesh.vertices),
            Some(json::buffer::Target::ArrayBuffer),
        );
        let pos_accessor = self.add_accessor(
            pos_view,
            json::accessor::Type::Vec3,
            json::accessor::ComponentType::F32,
            mesh.vertices.len(),
        );

        // Normals
        let norm_view = self.add_buffer_view(
            bytemuck::cast_slice(&mesh.normals),
            Some(json::buffer::Target::ArrayBuffer),
        );
        let norm_accessor = self.add_accessor(
            norm_view,
            json::accessor::Type::Vec3,
            json::accessor::ComponentType::F32,
            mesh.normals.len(),
        );

        // UVs
        let uv_view = self.add_buffer_view(
            bytemuck::cast_slice(&mesh.uvs),
            Some(json::buffer::Target::ArrayBuffer),
        );
        let uv_accessor = self.add_accessor(
            uv_view,
            json::accessor::Type::Vec2,
            json::accessor::ComponentType::F32,
            mesh.uvs.len(),
        );

        // JOINTS_0 - bone indices per vertex (4 u8 values)
        let joints_view = self.add_buffer_view(
            bytemuck::cast_slice(&mesh.bone_indices),
            Some(json::buffer::Target::ArrayBuffer),
        );
        let joints_accessor = self.add_accessor(
            joints_view,
            json::accessor::Type::Vec4,
            json::accessor::ComponentType::U8,
            mesh.bone_indices.len(),
        );

        // WEIGHTS_0 - bone weights per vertex (4 f32 values, sum to 1.0)
        let weights_view = self.add_buffer_view(
            bytemuck::cast_slice(&mesh.bone_weights),
            Some(json::buffer::Target::ArrayBuffer),
        );
        let weights_accessor = self.add_accessor(
            weights_view,
            json::accessor::Type::Vec4,
            json::accessor::ComponentType::F32,
            mesh.bone_weights.len(),
        );

        // Indices
        let idx_view = self.add_buffer_view(
            bytemuck::cast_slice(&mesh.indices),
            Some(json::buffer::Target::ElementArrayBuffer),
        );
        let idx_accessor = self.add_accessor(
            idx_view,
            json::accessor::Type::Scalar,
            json::accessor::ComponentType::U16,
            mesh.indices.len(),
        );

        // Build primitive with all attributes
        let primitive = json::mesh::Primitive {
            attributes: {
                let mut attrs = std::collections::BTreeMap::new();
                attrs.insert(
                    json::validation::Checked::Valid(json::mesh::Semantic::Positions),
                    json::Index::new(pos_accessor),
                );
                attrs.insert(
                    json::validation::Checked::Valid(json::mesh::Semantic::Normals),
                    json::Index::new(norm_accessor),
                );
                attrs.insert(
                    json::validation::Checked::Valid(json::mesh::Semantic::TexCoords(0)),
                    json::Index::new(uv_accessor),
                );
                attrs.insert(
                    json::validation::Checked::Valid(json::mesh::Semantic::Joints(0)),
                    json::Index::new(joints_accessor),
                );
                attrs.insert(
                    json::validation::Checked::Valid(json::mesh::Semantic::Weights(0)),
                    json::Index::new(weights_accessor),
                );
                attrs
            },
            indices: Some(json::Index::new(idx_accessor)),
            mode: json::validation::Checked::Valid(json::mesh::Mode::Triangles),
            ..Default::default()
        };

        let gltf_mesh = json::Mesh {
            name: Some("character_mesh".to_string()),
            primitives: vec![primitive],
            ..Default::default()
        };

        let mesh_idx = self.root.meshes.len() as u32;
        self.root.meshes.push(gltf_mesh);
        mesh_idx
    }

    /// Export animation clip
    fn export_animation(&mut self, clip: &AnimationClip, joints: &[u32]) {
        let mut channels = vec![];
        let mut samplers = vec![];

        // Time values (shared by all channels in this clip)
        let times: Vec<f32> = (0..clip.frame_count)
            .map(|f| f as f32 * clip.frame_time)
            .collect();
        let time_view = self.add_buffer_view(
            bytemuck::cast_slice(&times),
            None,
        );
        let time_accessor = self.add_accessor(
            time_view,
            json::accessor::Type::Scalar,
            json::accessor::ComponentType::F32,
            times.len(),
        );

        // Per-bone animation data
        for (bone_idx, bone_anim) in clip.bone_animations.iter().enumerate() {
            // Rotation channel
            let rot_view = self.add_buffer_view(
                bytemuck::cast_slice(&bone_anim.rotations),
                None,
            );
            let rot_accessor = self.add_accessor(
                rot_view,
                json::accessor::Type::Vec4,
                json::accessor::ComponentType::F32,
                bone_anim.rotations.len(),
            );

            let sampler_idx = samplers.len() as u32;
            samplers.push(json::animation::Sampler {
                input: json::Index::new(time_accessor),
                output: json::Index::new(rot_accessor),
                interpolation: json::validation::Checked::Valid(
                    json::animation::Interpolation::Linear
                ),
                ..Default::default()
            });

            channels.push(json::animation::Channel {
                target: json::animation::Target {
                    node: json::Index::new(joints[bone_idx]),
                    path: json::validation::Checked::Valid(
                        json::animation::Property::Rotation
                    ),
                    ..Default::default()
                },
                sampler: json::Index::new(sampler_idx),
                ..Default::default()
            });

            // Translation channel (if bone has position animation)
            if !bone_anim.translations.is_empty() {
                let trans_view = self.add_buffer_view(
                    bytemuck::cast_slice(&bone_anim.translations),
                    None,
                );
                let trans_accessor = self.add_accessor(
                    trans_view,
                    json::accessor::Type::Vec3,
                    json::accessor::ComponentType::F32,
                    bone_anim.translations.len(),
                );

                let sampler_idx = samplers.len() as u32;
                samplers.push(json::animation::Sampler {
                    input: json::Index::new(time_accessor),
                    output: json::Index::new(trans_accessor),
                    interpolation: json::validation::Checked::Valid(
                        json::animation::Interpolation::Linear
                    ),
                    ..Default::default()
                });

                channels.push(json::animation::Channel {
                    target: json::animation::Target {
                        node: json::Index::new(joints[bone_idx]),
                        path: json::validation::Checked::Valid(
                            json::animation::Property::Translation
                        ),
                        ..Default::default()
                    },
                    sampler: json::Index::new(sampler_idx),
                    ..Default::default()
                });
            }
        }

        let animation = json::Animation {
            name: Some(clip.name.clone()),
            channels,
            samplers,
            ..Default::default()
        };

        self.root.animations.push(animation);
    }
}

/// Data format for skinned vertices (ZX compatible)
pub struct SkinnedVertex {
    pub position: [f32; 3],
    pub normal: [f32; 3],
    pub uv: [f32; 2],
    pub bone_indices: [u8; 4],   // Up to 4 bones per vertex
    pub bone_weights: [f32; 4],  // Weights sum to 1.0
}

/// Validate skinned mesh before export
pub fn validate_skinned_mesh(mesh: &SkinnedMesh) -> Result<(), Vec<String>> {
    let mut errors = vec![];

    for (idx, (indices, weights)) in mesh.bone_indices.iter()
        .zip(mesh.bone_weights.iter())
        .enumerate()
    {
        // Check weight sum
        let sum: f32 = weights.iter().sum();
        if (sum - 1.0).abs() > 0.001 {
            errors.push(format!("Vertex {}: weights sum to {} (should be 1.0)", idx, sum));
        }

        // Check for invalid bone indices
        for (i, &bone_idx) in indices.iter().enumerate() {
            if weights[i] > 0.0 && bone_idx as usize >= mesh.bone_count {
                errors.push(format!(
                    "Vertex {}: bone index {} out of range (max {})",
                    idx, bone_idx, mesh.bone_count - 1
                ));
            }
        }
    }

    if errors.is_empty() {
        Ok(())
    } else {
        Err(errors)
    }
}
```

**GLTF Structure Reference:**
```
character.gltf
├── scene
│   └── node (mesh + skin reference)
│       ├── mesh: character_mesh
│       │   └── primitive
│       │       ├── POSITION
│       │       ├── NORMAL
│       │       ├── TEXCOORD_0
│       │       ├── JOINTS_0    ← Bone indices (vec4 u8)
│       │       └── WEIGHTS_0   ← Bone weights (vec4 f32)
│       └── skin: character_skin
│           ├── inverseBindMatrices (accessor)
│           ├── joints: [node0, node1, node2...]
│           └── skeleton: node0 (root)
├── nodes (bone hierarchy)
│   ├── 0: root
│   ├── 1: spine (child of 0)
│   ├── 2: head (child of 1)
│   └── ...
└── animations
    └── walk
        ├── channels (per-bone rotation/translation)
        └── samplers (time → value)
```

### Proposed Solution

**1. Skill: `character-pipeline`** (orchestration guide)
```
Triggers: "create character", "animated character", "character workflow",
"full character", "mesh to animation", "rigged character"

Content:
- The 7-phase pipeline overview
- Phase handoffs and file formats
- ZX constraints summary
- Quick start templates (humanoid, quadruped)
- Troubleshooting common issues
```

**2. Agent: `character-generator`**
```
Triggers: "generate character", "make me a character", "create animated
humanoid", "procedural character with animations"

Behavior:
- Asks clarifying questions (type, style, animations needed)
- Invokes phases A→G in sequence
- Validates ZX compliance at each step
- Produces complete asset set
```

**3. Updates to Existing Skills**

| Skill | Addition Needed |
|-------|-----------------|
| procedural-meshes | Section: "Topology for Animation" |
| procedural-textures | Section: "Character Texture Sizes" |
| skeletal-rigging (NEW) | Full standalone skill (A2 refactor) |
| procedural-animations | Remove rigging content, focus on motion |

**Prompt for plugin-dev:**
```
Add skill "character-pipeline" to nethercore-zx-procgen. Triggers: "create
character", "animated character", "character workflow", "rigged character",
"skinned mesh". Cover the 7-phase pipeline: mesh generation (with deformation
topology), texturing (UV-aware), skeleton creation, skinning (bone weights),
animation, GLTF export, nether.toml integration. Include ZX constraints per
phase. Add quick-start for humanoid and quadruped. ~2000 words.

Add agent "character-generator" to nethercore-zx-procgen. Triggers: "generate
character", "make character", "procedural character". Agent asks questions
(character type, style, needed animations), then orchestrates the full
pipeline, producing mesh + textures + skeleton + animations + nether.toml
entries. Validates ZX compliance. Model: inherit. Tools: Read, Write, Bash,
Glob, AskUserQuestion.
```

---

## Gap 16: Physics & Collision

**Status:** NOT covered. FFI provides no physics - games must implement their own.

**This is the most critical missing piece.** Every 3D game needs collision detection and physics, but ZX provides rendering only. Games must implement collision in WASM, and no plugin teaches this.

**Missing:**

### Collision Detection
- AABB (Axis-Aligned Bounding Box) intersection
- Sphere-sphere collision
- Capsule collision (for characters)
- Ray casting (for shooting, picking, ground detection)
- Mesh-based collision (simplified)

### Collision Response
- Slide along walls
- Bounce off surfaces
- Push out of overlap
- Trigger vs. solid colliders

### Basic Physics
- Gravity and velocity integration
- Terminal velocity
- Friction (ground, air)
- Deterministic physics for rollback (fixed timestep already provided)

### Spatial Partitioning
- Grid-based broad phase
- Simple octree (for larger worlds)

**Rollback Considerations:**
All physics MUST be deterministic. The FFI provides `delta_time()` as a fixed timestep and `random()` as seeded RNG - physics code must use these, never wall-clock time or external random.

**Prompt for plugin-dev:**
```
Add skill "physics-collision" to nethercore-zx-game-design. Triggers: "collision",
"physics", "AABB", "raycast", "gravity", "collision detection", "hit detection",
"collider". Cover: AABB intersection (2D and 3D), sphere collision, capsule for
characters, raycasting, collision response (slide, bounce), gravity/velocity
integration, friction, determinism for rollback (use delta_time(), random()).
Include Rust code examples. ~2000 words.
```

---

## Gap 17: Camera Implementation

**Status:** FFI functions exist (`camera_set`, `camera_fov`, `push_view_matrix`), but no implementation patterns.

The perspective-patterns skill discusses camera TYPES (side-scroll, third-person, etc.) but provides no CODE for implementing them.

**Missing:**

### Camera Types Implementation
- Follow camera (smooth follow with offset)
- Orbit camera (third-person, mouse/stick controlled)
- First-person camera (head bob, look sensitivity)
- Fixed camera (room-based, cinematic)
- Rail camera (on-rails movement)

### Camera Features
- Smooth interpolation (lerp, slerp)
- Dead zones (don't move until threshold)
- Look-ahead (move camera in movement direction)
- Zoom control

### Camera Collision
- Don't clip through walls
- Pull camera forward when obstructed
- Transparency fade when camera close to character

### Screen Effects (via camera)
- Screen shake implementation
- Camera punch (recoil)
- Smooth zoom transitions

**Prompt for plugin-dev:**
```
Add skill "camera-systems" to nethercore-zx-dev. Triggers: "camera follow",
"orbit camera", "third person camera", "first person camera", "camera collision",
"screen shake", "camera lerp", "camera implementation". Cover: follow camera
(smooth, offset, dead zone), orbit camera (pitch/yaw, distance), first-person
(look sensitivity), camera collision (raycast pull-in), screen shake. Include
Rust code using camera_set() and push_view_matrix(). ~1500 words.
```

---

## Gap 18: Gameplay Mechanics Library

**Status:** NOT covered. Common gameplay patterns must be implemented but aren't taught.

Every game type has common mechanics that every developer reimplements. This skill would provide tested, rollback-safe implementations.

**Missing:**

### Platformer Mechanics
- Variable-height jumping (hold to jump higher)
- Coyote time (grace period after leaving edge)
- Jump buffering (press before landing)
- Wall sliding / wall jumping
- Moving platforms
- One-way platforms

### Combat Mechanics
- Hitbox/hurtbox systems
- Damage calculation
- Knockback/hitstun
- Invincibility frames (i-frames)
- Combo systems

### Movement Mechanics
- 8-directional movement (top-down)
- Tank controls
- Acceleration/deceleration curves
- Dash/dodge mechanics

### Inventory & Items
- Item pickup/drop
- Inventory slots
- Equipment system
- Consumables

### Dialogue & Text
- Text box rendering
- Typewriter effect
- Choice selection
- Branching dialogue state

**Prompt for plugin-dev:**
```
Add skill "gameplay-mechanics" to nethercore-zx-game-design. Triggers: "platformer
physics", "jump", "coyote time", "hitbox", "combat", "inventory", "dialogue",
"movement", "knockback". Cover: platformer (variable jump, coyote, buffer, wall
jump), combat (hitbox/hurtbox, damage, knockback, i-frames), movement (8-dir,
acceleration), items (pickup, inventory). Focus on rollback-safe patterns. Include
Rust code. ~2000 words.
```

---

## Gap 19: AI & Behavior Patterns

**Status:** NOT covered. Enemy AI and NPC behavior must be implemented by games.

**Lower priority** than physics/collision but important for games with enemies or NPCs.

**Missing:**

### State Machines
- Finite state machine pattern
- State transitions
- Entry/exit actions
- Hierarchical state machines

### Movement Behaviors
- Patrol (waypoint following)
- Chase (follow target)
- Flee (run from target)
- Wander (random movement)

### Sensing
- Line-of-sight detection
- Hearing (proximity triggers)
- Memory (last known position)

### Pathfinding (Simple)
- Grid-based A* (for tile games)
- Waypoint graphs (for 3D)
- Steering behaviors (seek, flee, arrive)

### Combat AI
- Attack patterns
- Cooldowns
- Aggression levels
- Target selection

**Prompt for plugin-dev:**
```
Add skill "ai-patterns" to nethercore-zx-game-design. Triggers: "enemy AI",
"state machine", "patrol", "pathfinding", "NPC behavior", "chase", "AI".
Cover: state machines (FSM pattern, transitions), movement (patrol, chase,
flee, wander), sensing (LOS, proximity), simple pathfinding (grid A*,
waypoints), combat AI (attack patterns, cooldowns). Rollback-safe. Include
Rust code. ~1500 words. Lower priority than physics/collision.
```

---

## Gap 20: Multiplayer Rendering Patterns

**Status:** multiplayer-design skill covers THEORY but not IMPLEMENTATION patterns.

**Critical Issue:** The skill never mentions `player_count()` or `local_player_mask()` FFI functions, and doesn't explain how to use them without breaking determinism.

### The Determinism Rule for Multiplayer Rendering

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE GOLDEN RULE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  update() — DETERMINISTIC                                        │
│  ├── Called on ALL clients with SAME synchronized inputs         │
│  ├── Must produce IDENTICAL results everywhere                   │
│  ├── ✅ Use: player_count() — same on all clients                │
│  ├── ✅ Use: button_pressed(player_id, ...) — for ALL players    │
│  └── ❌ NEVER: local_player_mask() — different per client!       │
│                                                                  │
│  render() — LOCAL ONLY                                           │
│  ├── Called only on THIS client                                  │
│  ├── Can differ between clients (that's fine!)                   │
│  ├── ✅ Use: local_player_mask() — to know YOUR players          │
│  └── ✅ Use: viewport() — for split-screen rendering             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### FFI Functions for Multiplayer

```rust
// Session info (safe anywhere)
fn player_count() -> u32;           // 1-4, SAME on all clients
fn local_player_mask() -> u32;      // Bitmask, DIFFERENT per client!

// Example: 2 players, P1 local on Client A, P2 local on Client B
// Client A: player_count() = 2, local_player_mask() = 0b01 (bit 0 = P1)
// Client B: player_count() = 2, local_player_mask() = 0b10 (bit 1 = P2)
```

### Missing: Multiplayer Mode Implementations

**1. Split-Screen (Local Multiplayer)**
```rust
fn render() {
    let local_mask = local_player_mask();
    let local_count = local_mask.count_ones();

    // Determine layout based on local player count
    let layouts = match local_count {
        1 => vec![(0, 0, 960, 540)],                    // Fullscreen
        2 => vec![(0, 0, 480, 540), (480, 0, 480, 540)], // Vertical split
        3 | 4 => vec![                                   // Quad split
            (0, 0, 480, 270), (480, 0, 480, 270),
            (0, 270, 480, 270), (480, 270, 480, 270)
        ],
        _ => vec![],
    };

    let mut viewport_idx = 0;
    for player_id in 0..player_count() {
        if (local_mask & (1 << player_id)) != 0 {
            let (x, y, w, h) = layouts[viewport_idx];
            viewport(x, y, w, h);

            // Render this player's view
            camera_follow_player(player_id);
            draw_scene();

            viewport_idx += 1;
        }
    }

    viewport_clear();
    draw_shared_hud(); // HUD on top of all viewports
}
```

**2. Same-Screen (Shared Camera)**
```rust
fn render() {
    // Camera follows center of all players (or primary local player)
    let center = calculate_player_center(); // Average of all player positions
    camera_set(center.x, center.y + 10.0, center.z - 15.0,
               center.x, center.y, center.z);

    draw_scene();

    // Player indicators (arrows when off-screen)
    for p in 0..player_count() {
        draw_player_indicator(p);
    }
}
```

**3. Asymmetric Multiplayer (Different Roles)**
```rust
fn render() {
    let local_mask = local_player_mask();

    // Find first local player
    let local_id = (0..player_count())
        .find(|p| (local_mask & (1 << p)) != 0)
        .unwrap_or(0);

    let role = game_state.players[local_id].role;

    match role {
        Role::Hunter => {
            // First-person view, limited vision
            camera_first_person(local_id);
            draw_scene_with_fog();
        }
        Role::Prey => {
            // Third-person view, can see more
            camera_third_person(local_id);
            draw_scene();
            draw_hunter_proximity_warning();
        }
        Role::Spectator => {
            // Free camera
            camera_spectator();
            draw_scene();
            draw_all_player_outlines();
        }
    }
}
```

**4. Online with Rollback (Correct Pattern)**
```rust
fn update() {
    // Process ALL players identically on ALL clients
    for p in 0..player_count() {
        let input = get_player_input(p); // Synchronized via GGRS

        // Game logic - MUST be deterministic
        players[p].update(input, delta_time());
    }

    // ❌ WRONG: if local_player_mask() & (1 << p) { ... }
    // This would cause desync!
}

fn render() {
    let local_mask = local_player_mask();

    // Pick camera based on local player(s)
    // This is safe - render doesn't affect game state
    let primary_local = local_mask.trailing_zeros() as usize;
    camera_follow(&players[primary_local]);

    draw_scene();

    // Optional: highlight local player differently
    for p in 0..player_count() {
        let is_local = (local_mask & (1 << p)) != 0;
        draw_player(p, if is_local { 0xFFFFFFFF } else { 0xAAAAAAFF });
    }
}
```

### Missing from Current Skill

| Topic | Status | Impact |
|-------|--------|--------|
| `player_count()` FFI | ❌ Not mentioned | Can't iterate players |
| `local_player_mask()` FFI | ❌ Not mentioned | Can't identify local players |
| update() vs render() safety | ⚠️ Implied but not explicit | Desync risk |
| Split-screen patterns | ❌ Not covered | Local MP broken |
| Same-screen patterns | ❌ Not covered | Shared camera missing |
| Asymmetric patterns | ❌ Not covered | Role-based games broken |
| Viewport FFI integration | ❌ Not linked to Gap 9 | No split-screen code |
| Player indicator UI | ❌ Not covered | Off-screen players invisible |

### Relationship to Other Gaps

- **Gap 9 (Split-Screen/Viewport)** — The viewport FFI usage
- **Gap 17 (Camera Implementation)** — Camera code patterns
- **Gap 20 (This gap)** — HOW to combine them safely for multiplayer

These three should be implemented together or cross-reference heavily.

**Prompt for plugin-dev:**
```
Add skill "multiplayer-rendering" to nethercore-zx-game-design OR expand
multiplayer-design skill. Triggers: "split screen", "local multiplayer",
"player_count", "local_player_mask", "multiplayer camera", "same screen
multiplayer", "asymmetric multiplayer", "couch co-op".

CRITICAL: Emphasize the update() vs render() determinism rule. local_player_mask()
is RENDER ONLY, never in update().

Cover:
1. player_count() and local_player_mask() FFI usage
2. Split-screen rendering (viewport per local player)
3. Same-screen rendering (shared camera, player indicators)
4. Asymmetric rendering (role-based views)
5. The determinism rule with code examples
6. Integration with viewport FFI

Include complete Rust code examples showing correct patterns.
~1500 words.
```

---

## Gap 21: BVH/Motion Capture Integration

**Status:** NOT covered. Animation is purely procedural (math-based synthesis).

**The Core Problem:**
The procedural-animations skill generates motion using sine waves, oscillations, and phase-based locomotion. While this is great for procedural content, it cannot produce realistic human motion. Professional games often use motion capture data for realism, but there is:
- No BVH file format documentation
- No motion capture database references (CMU, Mixamo, Truebones)
- No retargeting (adapting animation to different skeletons)
- No root motion extraction
- No blending between mocap and procedural

### What Should Exist

```
┌─────────────────────────────────────────────────────────────────┐
│                    MOTION CAPTURE PIPELINE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SOURCE DATA                                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ CMU Database: 2,605 free BVH animations                 │    │
│  │ Mixamo: Thousands of game-ready animations (via FBX)    │    │
│  │ Truebones: Free packs with various actions              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  BVH PARSING                                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 1. Parse HIERARCHY section (bone names, offsets)        │    │
│  │ 2. Parse MOTION section (frames, channel data)          │    │
│  │ 3. Build skeleton hierarchy with parent indices         │    │
│  │ 4. Store animation frames (positions + Euler rotations) │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  RETARGETING                                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 1. Map source bones to target bones (name/index)        │    │
│  │ 2. Scale positions for different body proportions       │    │
│  │ 3. Apply IK for endpoint preservation (hands/feet)      │    │
│  │ 4. Extract root motion for character controller         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  ZX CONVERSION                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 1. Convert Euler angles → quaternions → 3x4 matrices    │    │
│  │ 2. Compute world transforms (parent × local)            │    │
│  │ 3. Output column-major 12-float arrays for set_bones()  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  RUNTIME                                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ skeleton_bind(mesh, skeleton)                           │    │
│  │ set_bones(&bone_matrices)                               │    │
│  │ draw_mesh(mesh)                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### BVH File Format Specification

```
HIERARCHY
ROOT Hips
{
    OFFSET 0.0 0.0 0.0
    CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
    JOINT Spine
    {
        OFFSET 0.0 10.0 0.0
        CHANNELS 3 Zrotation Xrotation Yrotation
        JOINT Spine1
        {
            OFFSET 0.0 10.0 0.0
            CHANNELS 3 Zrotation Xrotation Yrotation
            JOINT Neck
            {
                OFFSET 0.0 8.0 0.0
                CHANNELS 3 Zrotation Xrotation Yrotation
                JOINT Head
                {
                    OFFSET 0.0 5.0 0.0
                    CHANNELS 3 Zrotation Xrotation Yrotation
                    End Site
                    {
                        OFFSET 0.0 6.0 0.0
                    }
                }
            }
        }
    }
    JOINT LeftUpLeg
    {
        OFFSET 5.0 0.0 0.0
        CHANNELS 3 Zrotation Xrotation Yrotation
        ...
    }
    JOINT RightUpLeg
    {
        OFFSET -5.0 0.0 0.0
        CHANNELS 3 Zrotation Xrotation Yrotation
        ...
    }
}
MOTION
Frames: 100
Frame Time: 0.0333333
0.0 40.0 0.0 0.0 0.0 0.0 5.0 -2.0 1.0 3.0 -1.0 2.0 ...
0.0 40.1 0.0 0.1 0.0 0.0 5.1 -2.1 1.0 3.1 -1.0 2.0 ...
...
```

**Key Format Details:**

| Section | Content | Notes |
|---------|---------|-------|
| HIERARCHY | Bone tree with offsets | Defines rest pose skeleton |
| OFFSET | Position relative to parent | In parent's local space |
| CHANNELS | Which transforms this joint has | Root: 6 (pos+rot), others: 3 (rot only) |
| Channel Order | Varies by exporter | CMU uses ZXY rotation order |
| MOTION | Frame count + timing | Frame Time in seconds |
| Motion Data | One row per frame | Values in channel order, all joints |
| End Site | Leaf node terminator | Defines bone length for last bone |

**Coordinate System:**

| Source | Up | Forward | Handedness | Position Scale |
|--------|-----|---------|------------|----------------|
| CMU | Y | -Z | Right | Centimeters |
| Mixamo | Y | Z | Right | Centimeters |
| ZX | Y | -Z | Right | Meters |

**Important:** CMU data uses centimeters. Divide positions by 100 for ZX meters.

### Open Source Animation Databases

#### CMU Motion Capture Database
- **URL:** https://mocap.cs.cmu.edu/
- **Content:** 2,605 motions from 144 subjects
- **Format:** BVH available (also ASF/AMC)
- **License:** Free for research; commercial requires attribution
- **Quality:** Professional optical motion capture

**Recommended Clips for Games:**

| CMU Subject | Motion ID | Description | Game Use Case |
|-------------|-----------|-------------|---------------|
| 01 | 01_01 | Basic walk | Character locomotion |
| 01 | 01_02 | Fast walk | Speed variation |
| 02 | 02_01 | Run | Character sprinting |
| 02 | 02_03 | Jog | Medium speed |
| 05 | 05_01 | Jump | Platformer actions |
| 05 | 05_02 | Hop | Small jump |
| 13 | 13_* | Martial arts | Fighting games |
| 14 | 14_* | Punching/kicking | Combat |
| 60 | 60_* | Basketball | Sports games |
| 105 | 105_* | Dance | Rhythm games |
| 08 | 08_* | Walking with props | Carrying objects |

**CMU Standard Skeleton:**
- 31 joints
- Root at Hips
- Standard humanoid hierarchy
- Arms at sides in T-pose

#### Mixamo
- **URL:** https://www.mixamo.com/
- **Content:** Thousands of animations
- **Format:** FBX (convert to BVH via Blender)
- **License:** Free for use with Adobe account; check terms for commercial
- **Quality:** Professional, game-ready

**FBX to BVH Workflow:**
```
1. Download animation from Mixamo as FBX
2. Import FBX into Blender (File → Import → FBX)
3. Select armature
4. Export as BVH (File → Export → Motion Capture (.bvh))
5. Parse BVH using mocap-integration skill
```

#### Truebones Free Packs
- **URL:** https://truebones.gumroad.com/ (free packs available)
- **Content:** Various animation packs (walking, actions, etc.)
- **Format:** BVH
- **License:** Varies by pack; check individual licenses

#### LaFAN1 Dataset (Research)
- **URL:** https://github.com/ubisoft/ubisoft-laforge-animation-dataset
- **Content:** High-quality locomotion transitions
- **Format:** BVH
- **License:** Research use (CC BY-NC 4.0)

### Complete BVH Parser (Rust)

```rust
//! BVH Parser for Nethercore ZX
//!
//! Parses BVH motion capture files into a format suitable for ZX skeletal animation.

use alloc::string::String;
use alloc::vec::Vec;

/// Channel types in BVH files
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Channel {
    Xposition,
    Yposition,
    Zposition,
    Xrotation,
    Yrotation,
    Zrotation,
}

/// A joint in the BVH skeleton hierarchy
#[derive(Debug, Clone)]
pub struct BvhJoint {
    pub name: String,
    pub offset: [f32; 3],         // Position relative to parent (rest pose)
    pub channels: Vec<Channel>,    // Which transforms this joint has
    pub children: Vec<usize>,      // Indices of child joints
    pub parent: Option<usize>,     // Index of parent joint (None for root)
}

/// A parsed BVH animation clip
#[derive(Debug, Clone)]
pub struct BvhClip {
    pub joints: Vec<BvhJoint>,     // Flat array of all joints
    pub frame_count: usize,
    pub frame_time: f32,           // Seconds per frame
    pub motion_data: Vec<f32>,     // Flat: frame_count * total_channels
    pub total_channels: usize,
}

/// Transform data for a single joint at a single frame
#[derive(Debug, Clone)]
pub struct JointTransform {
    pub position: [f32; 3],        // Only meaningful for root
    pub rotation: [f32; 3],        // Euler angles in degrees (order depends on channels)
}

/// All joint transforms for a single frame
#[derive(Debug, Clone)]
pub struct BvhFrame {
    pub joint_transforms: Vec<JointTransform>,
}

impl BvhClip {
    /// Parse BVH from string content
    pub fn parse(content: &str) -> Result<Self, BvhParseError> {
        let mut lines = content.lines().peekable();

        // Skip to HIERARCHY
        while let Some(line) = lines.next() {
            if line.trim() == "HIERARCHY" {
                break;
            }
        }

        // Parse joints recursively
        let mut joints = Vec::new();
        Self::parse_joint(&mut lines, &mut joints, None)?;

        // Count total channels
        let total_channels: usize = joints.iter()
            .map(|j| j.channels.len())
            .sum();

        // Find MOTION section
        while let Some(line) = lines.next() {
            if line.trim() == "MOTION" {
                break;
            }
        }

        // Parse Frames:
        let frame_count = lines.next()
            .and_then(|l| l.trim().strip_prefix("Frames:"))
            .and_then(|s| s.trim().parse::<usize>().ok())
            .ok_or(BvhParseError::MissingFrameCount)?;

        // Parse Frame Time:
        let frame_time = lines.next()
            .and_then(|l| l.trim().strip_prefix("Frame Time:"))
            .and_then(|s| s.trim().parse::<f32>().ok())
            .ok_or(BvhParseError::MissingFrameTime)?;

        // Parse motion data
        let mut motion_data = Vec::with_capacity(frame_count * total_channels);
        for _ in 0..frame_count {
            if let Some(line) = lines.next() {
                for value in line.split_whitespace() {
                    if let Ok(v) = value.parse::<f32>() {
                        motion_data.push(v);
                    }
                }
            }
        }

        Ok(BvhClip {
            joints,
            frame_count,
            frame_time,
            motion_data,
            total_channels,
        })
    }

    fn parse_joint<'a, I>(
        lines: &mut std::iter::Peekable<I>,
        joints: &mut Vec<BvhJoint>,
        parent: Option<usize>,
    ) -> Result<usize, BvhParseError>
    where
        I: Iterator<Item = &'a str>,
    {
        // Read ROOT or JOINT line
        let header = lines.next().ok_or(BvhParseError::UnexpectedEnd)?;
        let header = header.trim();

        let name = if header.starts_with("ROOT ") {
            header.strip_prefix("ROOT ").unwrap().to_string()
        } else if header.starts_with("JOINT ") {
            header.strip_prefix("JOINT ").unwrap().to_string()
        } else {
            return Err(BvhParseError::ExpectedJoint);
        };

        // Expect {
        let brace = lines.next().ok_or(BvhParseError::UnexpectedEnd)?;
        if !brace.trim().starts_with('{') {
            return Err(BvhParseError::ExpectedBrace);
        }

        // Parse OFFSET
        let offset_line = lines.next().ok_or(BvhParseError::UnexpectedEnd)?;
        let offset = Self::parse_offset(offset_line)?;

        // Parse CHANNELS
        let channels_line = lines.next().ok_or(BvhParseError::UnexpectedEnd)?;
        let channels = Self::parse_channels(channels_line)?;

        let joint_idx = joints.len();
        joints.push(BvhJoint {
            name,
            offset,
            channels,
            children: Vec::new(),
            parent,
        });

        // Parse children or End Site
        loop {
            let line = lines.peek().map(|s| s.trim());
            match line {
                Some("}") => {
                    lines.next();
                    break;
                }
                Some(s) if s.starts_with("End Site") => {
                    // Skip End Site block
                    lines.next(); // End Site
                    lines.next(); // {
                    lines.next(); // OFFSET
                    lines.next(); // }
                }
                Some(s) if s.starts_with("JOINT ") || s.starts_with("ROOT ") => {
                    let child_idx = Self::parse_joint(lines, joints, Some(joint_idx))?;
                    joints[joint_idx].children.push(child_idx);
                }
                _ => {
                    lines.next();
                }
            }
        }

        Ok(joint_idx)
    }

    fn parse_offset(line: &str) -> Result<[f32; 3], BvhParseError> {
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() >= 4 && parts[0] == "OFFSET" {
            Ok([
                parts[1].parse().map_err(|_| BvhParseError::InvalidNumber)?,
                parts[2].parse().map_err(|_| BvhParseError::InvalidNumber)?,
                parts[3].parse().map_err(|_| BvhParseError::InvalidNumber)?,
            ])
        } else {
            Err(BvhParseError::InvalidOffset)
        }
    }

    fn parse_channels(line: &str) -> Result<Vec<Channel>, BvhParseError> {
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() < 2 || parts[0] != "CHANNELS" {
            return Err(BvhParseError::InvalidChannels);
        }

        let count: usize = parts[1].parse().map_err(|_| BvhParseError::InvalidNumber)?;
        let mut channels = Vec::with_capacity(count);

        for i in 0..count {
            let ch = match parts.get(2 + i) {
                Some(&"Xposition") => Channel::Xposition,
                Some(&"Yposition") => Channel::Yposition,
                Some(&"Zposition") => Channel::Zposition,
                Some(&"Xrotation") => Channel::Xrotation,
                Some(&"Yrotation") => Channel::Yrotation,
                Some(&"Zrotation") => Channel::Zrotation,
                _ => return Err(BvhParseError::InvalidChannel),
            };
            channels.push(ch);
        }

        Ok(channels)
    }

    /// Sample animation at a specific frame
    pub fn sample_frame(&self, frame: usize) -> BvhFrame {
        let frame = frame.min(self.frame_count.saturating_sub(1));
        let offset = frame * self.total_channels;

        let mut channel_idx = 0;
        let mut joint_transforms = Vec::with_capacity(self.joints.len());

        for joint in &self.joints {
            let mut position = [0.0f32; 3];
            let mut rotation = [0.0f32; 3];

            for channel in &joint.channels {
                let value = self.motion_data.get(offset + channel_idx)
                    .copied()
                    .unwrap_or(0.0);
                channel_idx += 1;

                match channel {
                    Channel::Xposition => position[0] = value,
                    Channel::Yposition => position[1] = value,
                    Channel::Zposition => position[2] = value,
                    Channel::Xrotation => rotation[0] = value,
                    Channel::Yrotation => rotation[1] = value,
                    Channel::Zrotation => rotation[2] = value,
                }
            }

            joint_transforms.push(JointTransform { position, rotation });
        }

        BvhFrame { joint_transforms }
    }

    /// Sample with interpolation between frames
    pub fn sample_time(&self, time: f32) -> BvhFrame {
        let frame_f = time / self.frame_time;
        let frame_a = (frame_f as usize).min(self.frame_count.saturating_sub(1));
        let frame_b = (frame_a + 1).min(self.frame_count.saturating_sub(1));
        let t = frame_f.fract();

        let a = self.sample_frame(frame_a);
        let b = self.sample_frame(frame_b);

        BvhFrame::lerp(&a, &b, t)
    }
}

impl BvhFrame {
    /// Linearly interpolate between two frames
    pub fn lerp(a: &Self, b: &Self, t: f32) -> Self {
        let joint_transforms = a.joint_transforms.iter()
            .zip(b.joint_transforms.iter())
            .map(|(ja, jb)| {
                JointTransform {
                    position: [
                        ja.position[0] + (jb.position[0] - ja.position[0]) * t,
                        ja.position[1] + (jb.position[1] - ja.position[1]) * t,
                        ja.position[2] + (jb.position[2] - ja.position[2]) * t,
                    ],
                    rotation: [
                        lerp_angle(ja.rotation[0], jb.rotation[0], t),
                        lerp_angle(ja.rotation[1], jb.rotation[1], t),
                        lerp_angle(ja.rotation[2], jb.rotation[2], t),
                    ],
                }
            })
            .collect();

        BvhFrame { joint_transforms }
    }
}

/// Interpolate angles handling wrap-around
fn lerp_angle(a: f32, b: f32, t: f32) -> f32 {
    let diff = ((b - a + 180.0) % 360.0) - 180.0;
    a + diff * t
}

#[derive(Debug)]
pub enum BvhParseError {
    UnexpectedEnd,
    ExpectedJoint,
    ExpectedBrace,
    InvalidOffset,
    InvalidChannels,
    InvalidChannel,
    InvalidNumber,
    MissingFrameCount,
    MissingFrameTime,
}
```

### BVH to ZX Bone Matrix Converter

```rust
//! Convert BVH animation data to ZX 3x4 bone matrices

use core::f32::consts::PI;

/// Convert Euler angles (degrees, ZXY order) to quaternion [w, x, y, z]
pub fn euler_zxy_to_quat(z_deg: f32, x_deg: f32, y_deg: f32) -> [f32; 4] {
    let z = z_deg * PI / 180.0;
    let x = x_deg * PI / 180.0;
    let y = y_deg * PI / 180.0;

    let (sz, cz) = (z * 0.5).sin_cos();
    let (sx, cx) = (x * 0.5).sin_cos();
    let (sy, cy) = (y * 0.5).sin_cos();

    // ZXY order composition
    [
        cz * cx * cy + sz * sx * sy,  // w
        cz * sx * cy + sz * cx * sy,  // x
        cz * cx * sy - sz * sx * cy,  // y
        sz * cx * cy - cz * sx * sy,  // z
    ]
}

/// Convert quaternion to 3x3 rotation matrix (row-major)
pub fn quat_to_mat3(q: [f32; 4]) -> [[f32; 3]; 3] {
    let [w, x, y, z] = q;
    [
        [1.0 - 2.0*(y*y + z*z), 2.0*(x*y - w*z),       2.0*(x*z + w*y)      ],
        [2.0*(x*y + w*z),       1.0 - 2.0*(x*x + z*z), 2.0*(y*z - w*x)      ],
        [2.0*(x*z - w*y),       2.0*(y*z + w*x),       1.0 - 2.0*(x*x + y*y)],
    ]
}

/// Convert BVH frame to ZX 3x4 bone matrices (column-major, 12 floats per bone)
pub fn bvh_frame_to_zx(
    clip: &BvhClip,
    frame: &BvhFrame,
    position_scale: f32,  // 0.01 for CMU (cm to m)
) -> Vec<[f32; 12]> {
    let mut world_transforms: Vec<[[f32; 4]; 3]> = Vec::with_capacity(clip.joints.len());

    for (i, joint) in clip.joints.iter().enumerate() {
        let jt = &frame.joint_transforms[i];

        // Build local rotation (ZXY order for CMU data)
        let local_quat = euler_zxy_to_quat(jt.rotation[2], jt.rotation[0], jt.rotation[1]);
        let local_mat3 = quat_to_mat3(local_quat);

        // Local position: rest offset + animation position (if root)
        let local_pos = [
            (joint.offset[0] + jt.position[0]) * position_scale,
            (joint.offset[1] + jt.position[1]) * position_scale,
            (joint.offset[2] + jt.position[2]) * position_scale,
        ];

        // Build 3x4 local transform matrix
        let local_3x4: [[f32; 4]; 3] = [
            [local_mat3[0][0], local_mat3[0][1], local_mat3[0][2], local_pos[0]],
            [local_mat3[1][0], local_mat3[1][1], local_mat3[1][2], local_pos[1]],
            [local_mat3[2][0], local_mat3[2][1], local_mat3[2][2], local_pos[2]],
        ];

        // Multiply with parent to get world transform
        let world_3x4 = match joint.parent {
            Some(parent_idx) => mat3x4_multiply(&world_transforms[parent_idx], &local_3x4),
            None => local_3x4,
        };

        world_transforms.push(world_3x4);
    }

    // Convert to ZX format: column-major flat array
    world_transforms.iter()
        .map(|m| [
            m[0][0], m[1][0], m[2][0],  // X axis column
            m[0][1], m[1][1], m[2][1],  // Y axis column
            m[0][2], m[1][2], m[2][2],  // Z axis column
            m[0][3], m[1][3], m[2][3],  // Translation column
        ])
        .collect()
}

/// Multiply two 3x4 matrices (A * B)
fn mat3x4_multiply(a: &[[f32; 4]; 3], b: &[[f32; 4]; 3]) -> [[f32; 4]; 3] {
    [
        [
            a[0][0]*b[0][0] + a[0][1]*b[1][0] + a[0][2]*b[2][0],
            a[0][0]*b[0][1] + a[0][1]*b[1][1] + a[0][2]*b[2][1],
            a[0][0]*b[0][2] + a[0][1]*b[1][2] + a[0][2]*b[2][2],
            a[0][0]*b[0][3] + a[0][1]*b[1][3] + a[0][2]*b[2][3] + a[0][3],
        ],
        [
            a[1][0]*b[0][0] + a[1][1]*b[1][0] + a[1][2]*b[2][0],
            a[1][0]*b[0][1] + a[1][1]*b[1][1] + a[1][2]*b[2][1],
            a[1][0]*b[0][2] + a[1][1]*b[1][2] + a[1][2]*b[2][2],
            a[1][0]*b[0][3] + a[1][1]*b[1][3] + a[1][2]*b[2][3] + a[1][3],
        ],
        [
            a[2][0]*b[0][0] + a[2][1]*b[1][0] + a[2][2]*b[2][0],
            a[2][0]*b[0][1] + a[2][1]*b[1][1] + a[2][2]*b[2][1],
            a[2][0]*b[0][2] + a[2][1]*b[1][2] + a[2][2]*b[2][2],
            a[2][0]*b[0][3] + a[2][1]*b[1][3] + a[2][2]*b[2][3] + a[2][3],
        ],
    ]
}
```

### Skeleton Retargeting

```rust
//! Retarget animation from source skeleton to target skeleton

/// Mapping from source skeleton bones to target skeleton bones
pub struct SkeletonMap {
    pub mappings: Vec<BoneMapping>,
}

pub struct BoneMapping {
    pub source_name: String,
    pub target_index: usize,
    pub rotation_offset: [f32; 4],  // Quaternion adjustment for T-pose differences
    pub scale: f32,                  // Limb length ratio (target/source)
}

impl SkeletonMap {
    /// Create mapping from CMU skeleton to custom humanoid
    pub fn cmu_to_humanoid() -> Self {
        SkeletonMap {
            mappings: vec![
                BoneMapping { source_name: "Hips".into(), target_index: 0, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "Spine".into(), target_index: 1, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "Spine1".into(), target_index: 2, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "Neck".into(), target_index: 3, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "Head".into(), target_index: 4, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "LeftShoulder".into(), target_index: 5, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "LeftArm".into(), target_index: 6, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "LeftForeArm".into(), target_index: 7, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "LeftHand".into(), target_index: 8, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "RightShoulder".into(), target_index: 9, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "RightArm".into(), target_index: 10, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "RightForeArm".into(), target_index: 11, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "RightHand".into(), target_index: 12, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "LeftUpLeg".into(), target_index: 13, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "LeftLeg".into(), target_index: 14, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "LeftFoot".into(), target_index: 15, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "RightUpLeg".into(), target_index: 16, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "RightLeg".into(), target_index: 17, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
                BoneMapping { source_name: "RightFoot".into(), target_index: 18, rotation_offset: QUAT_IDENTITY, scale: 1.0 },
            ],
        }
    }
}

const QUAT_IDENTITY: [f32; 4] = [1.0, 0.0, 0.0, 0.0];

/// Apply retargeting with optional IK for foot placement
pub fn retarget_frame(
    source_clip: &BvhClip,
    source_frame: &BvhFrame,
    mapping: &SkeletonMap,
    target_bone_count: usize,
) -> Vec<[f32; 12]> {
    let mut target_bones = vec![[
        1.0, 0.0, 0.0,  // Identity X axis
        0.0, 1.0, 0.0,  // Identity Y axis
        0.0, 0.0, 1.0,  // Identity Z axis
        0.0, 0.0, 0.0,  // Zero translation
    ]; target_bone_count];

    // Apply mapped rotations
    for mapping_entry in &mapping.mappings {
        // Find source bone by name
        let source_idx = source_clip.joints.iter()
            .position(|j| j.name == mapping_entry.source_name);

        if let Some(src_idx) = source_idx {
            let src_transform = &source_frame.joint_transforms[src_idx];

            // Convert to quaternion
            let src_quat = euler_zxy_to_quat(
                src_transform.rotation[2],
                src_transform.rotation[0],
                src_transform.rotation[1],
            );

            // Apply rotation offset for T-pose differences
            let adjusted_quat = quat_multiply(src_quat, mapping_entry.rotation_offset);

            // Convert to matrix
            let mat3 = quat_to_mat3(adjusted_quat);

            // Scale position
            let pos = [
                src_transform.position[0] * mapping_entry.scale * 0.01,  // CMU cm to m
                src_transform.position[1] * mapping_entry.scale * 0.01,
                src_transform.position[2] * mapping_entry.scale * 0.01,
            ];

            // Store in target
            target_bones[mapping_entry.target_index] = [
                mat3[0][0], mat3[1][0], mat3[2][0],
                mat3[0][1], mat3[1][1], mat3[2][1],
                mat3[0][2], mat3[1][2], mat3[2][2],
                pos[0], pos[1], pos[2],
            ];
        }
    }

    target_bones
}

fn quat_multiply(a: [f32; 4], b: [f32; 4]) -> [f32; 4] {
    [
        a[0]*b[0] - a[1]*b[1] - a[2]*b[2] - a[3]*b[3],
        a[0]*b[1] + a[1]*b[0] + a[2]*b[3] - a[3]*b[2],
        a[0]*b[2] - a[1]*b[3] + a[2]*b[0] + a[3]*b[1],
        a[0]*b[3] + a[1]*b[2] - a[2]*b[1] + a[3]*b[0],
    ]
}
```

### Root Motion Extraction

```rust
//! Extract root motion for character controller integration

pub struct RootMotion {
    pub position_deltas: Vec<[f32; 3]>,  // Per-frame XZ movement
    pub rotation_deltas: Vec<f32>,        // Per-frame Y rotation (radians)
    pub total_distance: f32,
    pub total_rotation: f32,
}

/// Extract root motion from BVH clip (horizontal movement only)
pub fn extract_root_motion(clip: &BvhClip, position_scale: f32) -> RootMotion {
    let mut position_deltas = Vec::with_capacity(clip.frame_count);
    let mut rotation_deltas = Vec::with_capacity(clip.frame_count);
    let mut total_distance = 0.0f32;
    let mut total_rotation = 0.0f32;

    for i in 1..clip.frame_count {
        let prev = clip.sample_frame(i - 1);
        let curr = clip.sample_frame(i);

        // Root is always joint 0
        let prev_pos = &prev.joint_transforms[0].position;
        let curr_pos = &curr.joint_transforms[0].position;

        // XZ delta (horizontal movement)
        let delta = [
            (curr_pos[0] - prev_pos[0]) * position_scale,
            0.0,  // Ignore vertical for ground movement
            (curr_pos[2] - prev_pos[2]) * position_scale,
        ];

        // Y rotation delta
        let prev_rot = prev.joint_transforms[0].rotation[1];
        let curr_rot = curr.joint_transforms[0].rotation[1];
        let rot_delta = (curr_rot - prev_rot) * PI / 180.0;

        total_distance += (delta[0] * delta[0] + delta[2] * delta[2]).sqrt();
        total_rotation += rot_delta.abs();

        position_deltas.push(delta);
        rotation_deltas.push(rot_delta);
    }

    // First frame has zero delta
    position_deltas.insert(0, [0.0, 0.0, 0.0]);
    rotation_deltas.insert(0, 0.0);

    RootMotion {
        position_deltas,
        rotation_deltas,
        total_distance,
        total_rotation,
    }
}

/// Apply root motion to character in game update
pub fn apply_root_motion(
    character_pos: &mut [f32; 3],
    character_rotation: &mut f32,
    root_motion: &RootMotion,
    frame: usize,
) {
    if frame < root_motion.position_deltas.len() {
        let delta = &root_motion.position_deltas[frame];

        // Rotate delta by character facing direction
        let cos_r = character_rotation.cos();
        let sin_r = character_rotation.sin();

        character_pos[0] += delta[0] * cos_r - delta[2] * sin_r;
        character_pos[2] += delta[0] * sin_r + delta[2] * cos_r;

        *character_rotation += root_motion.rotation_deltas[frame];
    }
}
```

### Animation State Machine

```rust
//! Animation state machine for blending mocap clips

pub struct AnimationStateMachine {
    pub clips: Vec<BvhClip>,
    pub current_state: usize,
    pub next_state: Option<usize>,
    pub blend_progress: f32,
    pub blend_duration: f32,
    pub current_time: f32,
}

impl AnimationStateMachine {
    pub fn new(clips: Vec<BvhClip>) -> Self {
        Self {
            clips,
            current_state: 0,
            next_state: None,
            blend_progress: 0.0,
            blend_duration: 0.2,  // 200ms default blend
            current_time: 0.0,
        }
    }

    /// Transition to a new animation state
    pub fn transition_to(&mut self, state: usize) {
        if state != self.current_state && state < self.clips.len() {
            self.next_state = Some(state);
            self.blend_progress = 0.0;
        }
    }

    /// Update animation time and blending
    pub fn update(&mut self, delta_time: f32) {
        self.current_time += delta_time;

        // Handle blending
        if let Some(next) = self.next_state {
            self.blend_progress += delta_time / self.blend_duration;

            if self.blend_progress >= 1.0 {
                self.current_state = next;
                self.next_state = None;
                self.blend_progress = 0.0;
                self.current_time = 0.0;  // Reset time for new clip
            }
        }

        // Loop current clip
        let clip = &self.clips[self.current_state];
        let clip_duration = clip.frame_count as f32 * clip.frame_time;
        if self.current_time >= clip_duration {
            self.current_time = self.current_time % clip_duration;
        }
    }

    /// Sample current animation state (with blending)
    pub fn sample(&self) -> BvhFrame {
        let current_clip = &self.clips[self.current_state];
        let current_frame = current_clip.sample_time(self.current_time);

        if let Some(next_state) = self.next_state {
            let next_clip = &self.clips[next_state];
            let next_frame = next_clip.sample_time(0.0);  // Start of next clip

            // Blend between current and next
            BvhFrame::lerp(&current_frame, &next_frame, self.blend_progress)
        } else {
            current_frame
        }
    }
}
```

### LLM Semantic Animation Selection

**Movement Verbs → Animation Categories:**

| User Description | Animation Type | CMU Examples |
|------------------|----------------|--------------|
| "walk", "walking", "stroll" | Walk | 01_01, 01_02, 07_01 |
| "run", "sprint", "jog", "running" | Run | 02_01, 02_03, 09_01 |
| "jump", "leap", "hop", "jumping" | Jump | 05_01, 05_02, 16_* |
| "punch", "kick", "fight", "attack" | Combat | 13_*, 14_*, 15_* |
| "wave", "gesture", "greet" | Idle/Social | 10_*, 141_* |
| "sit", "crouch", "kneel" | Posture | 06_*, 111_* |
| "climb", "crawl" | Locomotion | 35_*, 118_* |
| "dance", "spin" | Dance | 05_*, 60_* |

**Adjectives → Animation Variants:**

| Modifier | Effect | Implementation |
|----------|--------|----------------|
| "slow", "careful", "cautious" | Reduce playback speed | `frame_time * 1.5` |
| "fast", "quick", "urgent" | Increase playback speed | `frame_time * 0.7` |
| "tired", "exhausted", "weary" | Pick fatigued variants | Add procedural bob |
| "aggressive", "angry" | Emphasize motion | Increase amplitude 10% |
| "sneaky", "stealthy" | Slower, lower stance | Crouch variants |

### Blending Mocap with Procedural

```rust
/// Blend mocap base with procedural overlays
pub fn enhanced_animation(
    mocap_bones: &[[f32; 12]],
    time: f32,
    look_target: Option<[f32; 3]>,
    foot_ik_targets: Option<([f32; 3], [f32; 3])>,
) -> Vec<[f32; 12]> {
    let mut bones = mocap_bones.to_vec();

    // Add procedural look-at for head
    if let Some(target) = look_target {
        let head_idx = 4;  // Assuming standard humanoid
        apply_look_at(&mut bones[head_idx], target);
    }

    // Apply foot IK for terrain adaptation
    if let Some((left_target, right_target)) = foot_ik_targets {
        let left_foot_idx = 15;
        let right_foot_idx = 18;
        // Apply two-bone IK to legs (see procedural-animations IK systems)
        // ...
    }

    // Add procedural breathing overlay
    let breath = (time * 2.0).sin() * 0.02;
    bones[1][10] += breath;  // Spine Y offset
    bones[2][10] += breath * 0.5;  // Upper spine

    bones
}
```

**Prompt for plugin-dev:**
```
Add skill "mocap-integration" to nethercore-zx-procgen. Triggers: "BVH", "motion
capture", "mocap", "CMU", "Mixamo", "load animation", "parse BVH", "retarget",
"root motion", "animation database", "import animation".

Cover: BVH file format (HIERARCHY + MOTION sections, channel ordering), open source
databases (CMU with recommended clips, Mixamo workflow, Truebones), complete Rust
BVH parser (~400 lines), BVH to ZX 3x4 matrix converter, skeleton retargeting
(bone mapping, proportional scaling), root motion extraction, animation state
machine (blending, transitions), LLM semantic selection (verb → clip mapping).

Integration: Uses procedural-animations for IK, blending overlays. Output format
compatible with set_bones() FFI. Include position scale handling (CMU uses cm).

Examples: bvh-parser.rs, bvh-to-zx-converter.rs, retargeting-example.rs,
animation-state-machine.rs. ~3000 words total.
```

---

## Gap 22: AI-First Creative Asset Pipeline

**Status:** NOT covered. Current agents only review/optimize existing assets. No creative generation workflow.

**The Core Problem:**
LLMs are excellent at understanding creative intent ("make it look more organic", "give it a cyberpunk vibe", "weathered medieval style") but the current plugin has no system for translating these descriptions into procedural parameters. Developers must manually:
1. Interpret creative requirements into specific values
2. Guess at parameter combinations
3. Iterate through trial and error
4. Have no way to describe "good" vs "bad" results programmatically

### What Should Exist

```
┌─────────────────────────────────────────────────────────────────┐
│                 AI-FIRST CREATIVE ASSET PIPELINE                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SEMANTIC ASSET DESCRIPTION LANGUAGE (SADL)                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Style Tokens: rustic, cyberpunk, organic, geometric     │    │
│  │  Color Palettes: warm_earthy, neon, muted, vibrant       │    │
│  │  Materials: metal.polished, wood.weathered, stone.rough  │    │
│  │  Shapes: barrel, crystal, humanoid, mechanical           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  CREATIVE AGENTS (Configurable Mode: Interactive | Autonomous)  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  asset-designer    → Interprets requirements, specs      │    │
│  │  asset-generator   → Produces procedural code            │    │
│  │  asset-critic      → Evaluates quality, suggests fixes   │    │
│  │  creative-orchestrator → Coordinates full pipeline       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  QUALITY HEURISTICS (Self-Assessment)                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Texture: contrast > 0.2, noise coherence, tileability   │    │
│  │  Mesh: poly budget, no degenerates, UV coverage > 95%    │    │
│  │  Animation: arc principle, anticipation, follow-through  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↓                                   │
│  ITERATIVE REFINEMENT WORKFLOW                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Generate → Self-Assess → Present → Feedback → Refine    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Semantic Asset Description Language (SADL)

SADL provides a vocabulary for LLMs to describe and generate assets using semantic terms rather than raw numbers.

#### Style Tokens

Style tokens map artistic concepts to procedural parameter adjustments:

```rust
/// Style token definitions with parameter modifiers
pub enum StyleToken {
    Rustic,      // Aged, worn, natural materials
    Cyberpunk,   // Neon, chrome, high contrast
    Organic,     // Smooth curves, natural patterns
    Geometric,   // Sharp edges, mathematical precision
    Fantasy,     // Magical, ethereal, saturated
    PostApoc,    // Damaged, dirty, improvised
    Minimalist,  // Simple, clean, low detail
    Baroque,     // Ornate, detailed, complex
}

/// Parameter modifiers for each style token
pub struct StyleModifiers {
    pub roughness_offset: f32,      // Added to base roughness
    pub saturation_scale: f32,      // Multiplied with saturation
    pub detail_level: DetailLevel,  // Low, Medium, High
    pub edge_hardness: f32,         // 0.0 = soft, 1.0 = sharp
    pub noise_octaves_offset: i32,  // Added to noise octaves
    pub damage_amount: f32,         // 0.0 = pristine, 1.0 = destroyed
}

impl StyleToken {
    pub fn modifiers(&self) -> StyleModifiers {
        match self {
            StyleToken::Rustic => StyleModifiers {
                roughness_offset: 0.3,
                saturation_scale: 0.7,
                detail_level: DetailLevel::Medium,
                edge_hardness: 0.3,
                noise_octaves_offset: 1,
                damage_amount: 0.4,
            },
            StyleToken::Cyberpunk => StyleModifiers {
                roughness_offset: -0.2,     // More reflective
                saturation_scale: 1.4,      // More vivid
                detail_level: DetailLevel::High,
                edge_hardness: 0.9,         // Sharp edges
                noise_octaves_offset: 0,
                damage_amount: 0.1,
            },
            StyleToken::Organic => StyleModifiers {
                roughness_offset: 0.1,
                saturation_scale: 0.9,
                detail_level: DetailLevel::Medium,
                edge_hardness: 0.1,         // Very soft
                noise_octaves_offset: 2,    // More natural variation
                damage_amount: 0.0,
            },
            StyleToken::Geometric => StyleModifiers {
                roughness_offset: 0.0,
                saturation_scale: 1.0,
                detail_level: DetailLevel::Low,
                edge_hardness: 1.0,         // Maximum sharpness
                noise_octaves_offset: -2,   // Less noise
                damage_amount: 0.0,
            },
            StyleToken::Fantasy => StyleModifiers {
                roughness_offset: -0.1,
                saturation_scale: 1.3,
                detail_level: DetailLevel::High,
                edge_hardness: 0.5,
                noise_octaves_offset: 1,
                damage_amount: 0.0,
            },
            StyleToken::PostApoc => StyleModifiers {
                roughness_offset: 0.5,      // Very rough
                saturation_scale: 0.5,      // Desaturated
                detail_level: DetailLevel::High,
                edge_hardness: 0.6,
                noise_octaves_offset: 2,
                damage_amount: 0.7,         // Heavy damage
            },
            StyleToken::Minimalist => StyleModifiers {
                roughness_offset: 0.0,
                saturation_scale: 0.8,
                detail_level: DetailLevel::Low,
                edge_hardness: 0.7,
                noise_octaves_offset: -3,   // Minimal noise
                damage_amount: 0.0,
            },
            StyleToken::Baroque => StyleModifiers {
                roughness_offset: 0.2,
                saturation_scale: 1.1,
                detail_level: DetailLevel::High,
                edge_hardness: 0.4,
                noise_octaves_offset: 3,    // Maximum detail
                damage_amount: 0.2,
            },
        }
    }
}

/// Apply style token to base material parameters
pub fn apply_style(base: &MaterialParams, style: StyleToken) -> MaterialParams {
    let mods = style.modifiers();
    MaterialParams {
        roughness: (base.roughness + mods.roughness_offset).clamp(0.0, 1.0),
        saturation: base.saturation * mods.saturation_scale,
        detail_level: mods.detail_level,
        // ... apply other modifiers
    }
}
```

#### Color Palette Semantics

Map verbal color descriptions to HSL ranges for procedural generation:

```rust
/// Semantic color palettes with HSL ranges
pub enum ColorPalette {
    WarmEarthy,    // Browns, oranges, tans (wood, leather, earth)
    CoolMetal,     // Silvers, blues, grays (steel, chrome, iron)
    Neon,          // Bright magentas, cyans, greens (cyberpunk, arcade)
    Muted,         // Low saturation, any hue (stone, concrete, fabric)
    Vibrant,       // High saturation, varied hue (fantasy, cartoon)
    Monochrome,    // Single hue, varied lightness (stylized)
    Complementary, // Two opposite hues (high contrast)
    Analogous,     // Adjacent hues (harmonious)
}

pub struct PaletteSpec {
    pub hue_ranges: Vec<(f32, f32)>,      // Allowed hue ranges (0-360)
    pub saturation_range: (f32, f32),     // Min-max saturation (0-1)
    pub lightness_range: (f32, f32),      // Min-max lightness (0-1)
    pub primary_weight: f32,              // Weight for primary vs accent
}

impl ColorPalette {
    pub fn spec(&self) -> PaletteSpec {
        match self {
            ColorPalette::WarmEarthy => PaletteSpec {
                hue_ranges: vec![(15.0, 45.0)],  // Orange-brown range
                saturation_range: (0.3, 0.6),
                lightness_range: (0.2, 0.5),
                primary_weight: 0.8,
            },
            ColorPalette::CoolMetal => PaletteSpec {
                hue_ranges: vec![(200.0, 240.0)],  // Blue-gray range
                saturation_range: (0.0, 0.3),
                lightness_range: (0.4, 0.8),
                primary_weight: 0.9,
            },
            ColorPalette::Neon => PaletteSpec {
                hue_ranges: vec![(280.0, 320.0), (160.0, 200.0)],  // Magenta + Cyan
                saturation_range: (0.8, 1.0),
                lightness_range: (0.5, 0.7),
                primary_weight: 0.5,  // Equal primary/accent
            },
            ColorPalette::Muted => PaletteSpec {
                hue_ranges: vec![(0.0, 360.0)],  // Any hue
                saturation_range: (0.05, 0.25),
                lightness_range: (0.3, 0.6),
                primary_weight: 0.7,
            },
            ColorPalette::Vibrant => PaletteSpec {
                hue_ranges: vec![(0.0, 360.0)],  // Any hue
                saturation_range: (0.7, 1.0),
                lightness_range: (0.4, 0.6),
                primary_weight: 0.6,
            },
            // ... additional palettes
        }
    }

    /// Generate a color from this palette
    pub fn sample(&self, rng: &mut impl Rng) -> [f32; 3] {
        let spec = self.spec();
        let hue_range = &spec.hue_ranges[rng.gen_range(0..spec.hue_ranges.len())];
        let h = rng.gen_range(hue_range.0..hue_range.1);
        let s = rng.gen_range(spec.saturation_range.0..spec.saturation_range.1);
        let l = rng.gen_range(spec.lightness_range.0..spec.lightness_range.1);
        hsl_to_rgb(h, s, l)
    }
}
```

#### Material Semantics

Hierarchical material descriptors with PBR parameters:

```rust
/// Material semantic descriptors (Category.Subcategory)
///
/// Usage: "metal.polished", "wood.weathered", "stone.mossy"
pub struct MaterialSemantic {
    pub category: MaterialCategory,
    pub variant: String,
    pub params: PbrParams,
}

pub enum MaterialCategory {
    Metal,
    Wood,
    Stone,
    Fabric,
    Organic,
    Synthetic,
    Crystal,
}

/// PBR material parameters
pub struct PbrParams {
    pub base_color: [f32; 3],
    pub metallic: f32,
    pub roughness: f32,
    pub normal_strength: f32,
    pub ao_strength: f32,
    pub emission: f32,
}

/// Material database - maps semantic strings to PBR params
pub fn material_from_semantic(descriptor: &str) -> Option<PbrParams> {
    match descriptor {
        // Metals
        "metal.polished" => Some(PbrParams {
            base_color: [0.9, 0.9, 0.9],
            metallic: 1.0,
            roughness: 0.1,
            normal_strength: 0.3,
            ao_strength: 0.5,
            emission: 0.0,
        }),
        "metal.brushed" => Some(PbrParams {
            base_color: [0.85, 0.85, 0.85],
            metallic: 1.0,
            roughness: 0.4,
            normal_strength: 0.8,
            ao_strength: 0.6,
            emission: 0.0,
        }),
        "metal.rusted" => Some(PbrParams {
            base_color: [0.5, 0.3, 0.2],
            metallic: 0.3,      // Rust is less metallic
            roughness: 0.8,
            normal_strength: 1.0,
            ao_strength: 0.9,
            emission: 0.0,
        }),
        "metal.copper" => Some(PbrParams {
            base_color: [0.85, 0.55, 0.40],
            metallic: 1.0,
            roughness: 0.3,
            normal_strength: 0.4,
            ao_strength: 0.5,
            emission: 0.0,
        }),
        "metal.gold" => Some(PbrParams {
            base_color: [1.0, 0.84, 0.0],
            metallic: 1.0,
            roughness: 0.2,
            normal_strength: 0.3,
            ao_strength: 0.4,
            emission: 0.0,
        }),

        // Woods
        "wood.polished" => Some(PbrParams {
            base_color: [0.45, 0.30, 0.15],
            metallic: 0.0,
            roughness: 0.3,
            normal_strength: 0.5,
            ao_strength: 0.7,
            emission: 0.0,
        }),
        "wood.weathered" => Some(PbrParams {
            base_color: [0.35, 0.30, 0.25],
            metallic: 0.0,
            roughness: 0.9,
            normal_strength: 1.0,
            ao_strength: 0.9,
            emission: 0.0,
        }),
        "wood.painted" => Some(PbrParams {
            base_color: [0.6, 0.4, 0.3],  // Varies with paint color
            metallic: 0.0,
            roughness: 0.5,
            normal_strength: 0.3,
            ao_strength: 0.6,
            emission: 0.0,
        }),

        // Stones
        "stone.rough" => Some(PbrParams {
            base_color: [0.5, 0.5, 0.5],
            metallic: 0.0,
            roughness: 0.95,
            normal_strength: 1.0,
            ao_strength: 1.0,
            emission: 0.0,
        }),
        "stone.polished" => Some(PbrParams {
            base_color: [0.4, 0.4, 0.4],
            metallic: 0.0,
            roughness: 0.2,
            normal_strength: 0.4,
            ao_strength: 0.5,
            emission: 0.0,
        }),
        "stone.mossy" => Some(PbrParams {
            base_color: [0.35, 0.45, 0.30],
            metallic: 0.0,
            roughness: 0.85,
            normal_strength: 0.9,
            ao_strength: 1.0,
            emission: 0.0,
        }),

        // Fabrics
        "fabric.cotton" => Some(PbrParams {
            base_color: [0.8, 0.8, 0.75],
            metallic: 0.0,
            roughness: 0.9,
            normal_strength: 0.3,
            ao_strength: 0.8,
            emission: 0.0,
        }),
        "fabric.leather" => Some(PbrParams {
            base_color: [0.35, 0.20, 0.10],
            metallic: 0.0,
            roughness: 0.6,
            normal_strength: 0.7,
            ao_strength: 0.8,
            emission: 0.0,
        }),
        "fabric.silk" => Some(PbrParams {
            base_color: [0.9, 0.85, 0.8],
            metallic: 0.0,
            roughness: 0.2,      // Silky smooth
            normal_strength: 0.2,
            ao_strength: 0.5,
            emission: 0.0,
        }),

        // Organics
        "organic.skin" => Some(PbrParams {
            base_color: [0.8, 0.6, 0.5],
            metallic: 0.0,
            roughness: 0.5,
            normal_strength: 0.6,
            ao_strength: 0.7,
            emission: 0.0,
        }),
        "organic.bark" => Some(PbrParams {
            base_color: [0.3, 0.2, 0.15],
            metallic: 0.0,
            roughness: 1.0,
            normal_strength: 1.0,
            ao_strength: 1.0,
            emission: 0.0,
        }),

        // Synthetics
        "synthetic.plastic" => Some(PbrParams {
            base_color: [0.8, 0.2, 0.2],  // Varies
            metallic: 0.0,
            roughness: 0.4,
            normal_strength: 0.2,
            ao_strength: 0.4,
            emission: 0.0,
        }),
        "synthetic.rubber" => Some(PbrParams {
            base_color: [0.1, 0.1, 0.1],
            metallic: 0.0,
            roughness: 0.8,
            normal_strength: 0.3,
            ao_strength: 0.6,
            emission: 0.0,
        }),

        // Crystals
        "crystal.clear" => Some(PbrParams {
            base_color: [0.95, 0.95, 1.0],
            metallic: 0.0,
            roughness: 0.05,
            normal_strength: 0.2,
            ao_strength: 0.2,
            emission: 0.1,
        }),
        "crystal.amethyst" => Some(PbrParams {
            base_color: [0.6, 0.3, 0.8],
            metallic: 0.0,
            roughness: 0.1,
            normal_strength: 0.3,
            ao_strength: 0.3,
            emission: 0.15,
        }),

        _ => None,
    }
}
```

#### Shape Vocabulary

Map shape descriptions to primitive compositions:

```rust
/// Shape primitives for procedural mesh generation
pub enum ShapePrimitive {
    Box { size: [f32; 3] },
    Sphere { radius: f32, segments: u32 },
    Cylinder { radius: f32, height: f32, segments: u32 },
    Cone { radius: f32, height: f32, segments: u32 },
    Torus { major_radius: f32, minor_radius: f32, segments: u32 },
    Capsule { radius: f32, height: f32, segments: u32 },
}

/// Composite shape descriptions for common objects
pub struct ShapeRecipe {
    pub primitives: Vec<(ShapePrimitive, Transform)>,
    pub operations: Vec<BooleanOp>,
}

pub enum BooleanOp {
    Union(usize, usize),
    Subtract(usize, usize),
    Intersect(usize, usize),
}

/// Shape vocabulary - maps descriptors to recipes
pub fn shape_from_descriptor(descriptor: &str) -> Option<ShapeRecipe> {
    match descriptor {
        "barrel" => Some(ShapeRecipe {
            primitives: vec![
                (ShapePrimitive::Cylinder { radius: 0.5, height: 1.2, segments: 24 },
                 Transform::identity()),
                // Bulge in middle
                (ShapePrimitive::Sphere { radius: 0.55, segments: 16 },
                 Transform::translate(0.0, 0.0, 0.0)),
            ],
            operations: vec![BooleanOp::Union(0, 1)],
        }),

        "crate" => Some(ShapeRecipe {
            primitives: vec![
                (ShapePrimitive::Box { size: [1.0, 1.0, 1.0] },
                 Transform::identity()),
            ],
            operations: vec![],
        }),

        "pillar" => Some(ShapeRecipe {
            primitives: vec![
                (ShapePrimitive::Cylinder { radius: 0.3, height: 3.0, segments: 16 },
                 Transform::identity()),
                // Capital (top)
                (ShapePrimitive::Box { size: [0.5, 0.2, 0.5] },
                 Transform::translate(0.0, 1.5, 0.0)),
                // Base
                (ShapePrimitive::Box { size: [0.5, 0.2, 0.5] },
                 Transform::translate(0.0, -1.5, 0.0)),
            ],
            operations: vec![BooleanOp::Union(0, 1), BooleanOp::Union(0, 2)],
        }),

        "humanoid" => Some(ShapeRecipe {
            // Simplified humanoid base mesh
            primitives: vec![
                // Torso
                (ShapePrimitive::Box { size: [0.4, 0.6, 0.2] },
                 Transform::translate(0.0, 0.0, 0.0)),
                // Head
                (ShapePrimitive::Sphere { radius: 0.12, segments: 16 },
                 Transform::translate(0.0, 0.45, 0.0)),
                // Left arm (upper)
                (ShapePrimitive::Capsule { radius: 0.05, height: 0.3, segments: 8 },
                 Transform::translate(-0.25, 0.15, 0.0)),
                // Right arm (upper)
                (ShapePrimitive::Capsule { radius: 0.05, height: 0.3, segments: 8 },
                 Transform::translate(0.25, 0.15, 0.0)),
                // ... continue with legs
            ],
            operations: vec![],  // All union for humanoid
        }),

        "crystal" => Some(ShapeRecipe {
            primitives: vec![
                // Main crystal body (stretched octahedron)
                (ShapePrimitive::Box { size: [0.3, 1.0, 0.3] },
                 Transform::rotate_z(45.0).then(Transform::rotate_x(45.0))),
            ],
            operations: vec![],
        }),

        "tree" => Some(ShapeRecipe {
            primitives: vec![
                // Trunk
                (ShapePrimitive::Cylinder { radius: 0.15, height: 1.5, segments: 8 },
                 Transform::identity()),
                // Foliage (layered cones)
                (ShapePrimitive::Cone { radius: 0.8, height: 1.0, segments: 8 },
                 Transform::translate(0.0, 1.0, 0.0)),
                (ShapePrimitive::Cone { radius: 0.6, height: 0.8, segments: 8 },
                 Transform::translate(0.0, 1.5, 0.0)),
                (ShapePrimitive::Cone { radius: 0.4, height: 0.6, segments: 8 },
                 Transform::translate(0.0, 1.9, 0.0)),
            ],
            operations: vec![],
        }),

        _ => None,
    }
}
```

### Constrained Generation Recipes

Pre-validated parameter ranges that always produce acceptable results:

```rust
/// A constrained generation recipe with safe parameter ranges
pub struct GenerationRecipe {
    pub name: &'static str,
    pub description: &'static str,
    pub base_style: StyleToken,
    pub palette: ColorPalette,
    pub material: &'static str,
    pub shape_base: &'static str,

    // Constrained ranges (always produce good results)
    pub scale_range: (f32, f32),
    pub noise_amplitude_range: (f32, f32),
    pub detail_poly_budget: (u32, u32),
    pub uv_texel_density: f32,
}

/// Pre-defined recipes for common game asset types
pub const RECIPES: &[GenerationRecipe] = &[
    GenerationRecipe {
        name: "medieval_prop",
        description: "Generic medieval-fantasy props (barrels, crates, furniture)",
        base_style: StyleToken::Rustic,
        palette: ColorPalette::WarmEarthy,
        material: "wood.weathered",
        shape_base: "crate",
        scale_range: (0.5, 2.0),
        noise_amplitude_range: (0.01, 0.05),
        detail_poly_budget: (100, 500),
        uv_texel_density: 256.0,
    },
    GenerationRecipe {
        name: "scifi_panel",
        description: "Sci-fi wall panels, consoles, tech surfaces",
        base_style: StyleToken::Geometric,
        palette: ColorPalette::CoolMetal,
        material: "metal.brushed",
        shape_base: "crate",
        scale_range: (1.0, 4.0),
        noise_amplitude_range: (0.0, 0.01),
        detail_poly_budget: (50, 200),
        uv_texel_density: 512.0,
    },
    GenerationRecipe {
        name: "organic_creature",
        description: "Creatures, monsters, organic characters",
        base_style: StyleToken::Organic,
        palette: ColorPalette::Muted,
        material: "organic.skin",
        shape_base: "humanoid",
        scale_range: (0.8, 3.0),
        noise_amplitude_range: (0.02, 0.1),
        detail_poly_budget: (500, 2000),
        uv_texel_density: 512.0,
    },
    GenerationRecipe {
        name: "cyberpunk_neon",
        description: "Glowing signs, neon decorations, holograms",
        base_style: StyleToken::Cyberpunk,
        palette: ColorPalette::Neon,
        material: "synthetic.plastic",
        shape_base: "crate",
        scale_range: (0.2, 2.0),
        noise_amplitude_range: (0.0, 0.02),
        detail_poly_budget: (20, 100),
        uv_texel_density: 256.0,
    },
    GenerationRecipe {
        name: "natural_rock",
        description: "Rocks, boulders, cliff faces, stone structures",
        base_style: StyleToken::Organic,
        palette: ColorPalette::Muted,
        material: "stone.rough",
        shape_base: "barrel",  // Rounded base
        scale_range: (0.3, 5.0),
        noise_amplitude_range: (0.1, 0.3),
        detail_poly_budget: (200, 1000),
        uv_texel_density: 256.0,
    },
];

/// Generate asset using recipe with random variation
pub fn generate_from_recipe(recipe: &GenerationRecipe, seed: u64) -> GeneratedAsset {
    let mut rng = Rng::seed(seed);

    // All parameters within constrained (safe) ranges
    let scale = rng.gen_range(recipe.scale_range.0..recipe.scale_range.1);
    let noise_amp = rng.gen_range(recipe.noise_amplitude_range.0..recipe.noise_amplitude_range.1);
    let poly_budget = rng.gen_range(recipe.detail_poly_budget.0..recipe.detail_poly_budget.1);

    GeneratedAsset {
        mesh: generate_mesh(recipe.shape_base, scale, noise_amp, poly_budget),
        material: material_from_semantic(recipe.material).unwrap(),
        texture: generate_texture(recipe.palette, recipe.uv_texel_density),
    }
}
```

### Quality Heuristics

Automated assessment of generated assets:

```rust
/// Quality assessment for generated textures
pub struct TextureQuality {
    pub contrast: f32,         // 0-1, should be > 0.2
    pub noise_coherence: f32,  // 0-1, should be > 0.5
    pub tileability: f32,      // 0-1, edge continuity score
    pub unique_colors: u32,    // Should be > 100 for most textures
    pub histogram_balance: f32, // 0-1, avoid over-bright/dark
}

impl TextureQuality {
    pub fn assess(texture: &Texture) -> Self {
        let pixels = texture.pixels();

        // Calculate contrast (RMS of luminance differences)
        let contrast = calculate_rms_contrast(&pixels);

        // Coherence via autocorrelation
        let noise_coherence = calculate_autocorrelation(&pixels);

        // Tileability via edge comparison
        let tileability = calculate_tile_score(&pixels, texture.width, texture.height);

        // Count unique colors
        let unique_colors = pixels.iter()
            .collect::<HashSet<_>>()
            .len() as u32;

        // Histogram balance
        let histogram_balance = calculate_histogram_balance(&pixels);

        Self { contrast, noise_coherence, tileability, unique_colors, histogram_balance }
    }

    pub fn passes_minimum(&self) -> bool {
        self.contrast > 0.15 &&
        self.noise_coherence > 0.4 &&
        self.tileability > 0.8 &&
        self.unique_colors > 50 &&
        self.histogram_balance > 0.3
    }

    pub fn issues(&self) -> Vec<&'static str> {
        let mut issues = vec![];
        if self.contrast <= 0.15 { issues.push("Too flat/uniform - add more variation"); }
        if self.noise_coherence <= 0.4 { issues.push("Noise too random - increase coherence"); }
        if self.tileability <= 0.8 { issues.push("Visible seams when tiled - check edges"); }
        if self.unique_colors <= 50 { issues.push("Too few colors - add subtle variation"); }
        if self.histogram_balance <= 0.3 { issues.push("Too dark or too bright overall"); }
        issues
    }
}

/// Quality assessment for generated meshes
pub struct MeshQuality {
    pub vertex_count: u32,
    pub triangle_count: u32,
    pub degenerate_tris: u32,      // Should be 0
    pub uv_coverage: f32,          // Should be > 0.95
    pub uv_overlap: f32,           // Should be < 0.05
    pub max_stretch: f32,          // UV stretch, should be < 2.0
    pub watertight: bool,          // No holes
}

impl MeshQuality {
    pub fn assess(mesh: &Mesh) -> Self {
        Self {
            vertex_count: mesh.vertices.len() as u32,
            triangle_count: mesh.indices.len() as u32 / 3,
            degenerate_tris: count_degenerate_triangles(mesh),
            uv_coverage: calculate_uv_coverage(mesh),
            uv_overlap: calculate_uv_overlap(mesh),
            max_stretch: calculate_max_uv_stretch(mesh),
            watertight: is_watertight(mesh),
        }
    }

    pub fn passes_for_budget(&self, max_triangles: u32) -> bool {
        self.triangle_count <= max_triangles &&
        self.degenerate_tris == 0 &&
        self.uv_coverage > 0.95 &&
        self.uv_overlap < 0.05 &&
        self.max_stretch < 2.0
    }

    pub fn issues(&self, max_triangles: u32) -> Vec<String> {
        let mut issues = vec![];
        if self.triangle_count > max_triangles {
            issues.push(format!("Over budget: {} > {} tris", self.triangle_count, max_triangles));
        }
        if self.degenerate_tris > 0 {
            issues.push(format!("{} degenerate triangles - remove zero-area faces", self.degenerate_tris));
        }
        if self.uv_coverage <= 0.95 {
            issues.push(format!("UV coverage {:.0}% - some faces missing UVs", self.uv_coverage * 100.0));
        }
        if self.uv_overlap >= 0.05 {
            issues.push(format!("UV overlap {:.0}% - overlapping islands", self.uv_overlap * 100.0));
        }
        if self.max_stretch >= 2.0 {
            issues.push(format!("UV stretch {:.1}x - texture will look distorted", self.max_stretch));
        }
        if !self.watertight {
            issues.push("Mesh has holes - not watertight".to_string());
        }
        issues
    }
}

/// Quality assessment for animations (based on animation principles)
pub struct AnimationQuality {
    pub has_anticipation: bool,   // Windup before action
    pub has_follow_through: bool, // Settling after action
    pub arc_score: f32,           // Natural arcs vs linear motion (0-1)
    pub timing_variance: f32,     // Avoid mechanical uniformity
    pub root_motion_valid: bool,  // Root doesn't drift unexpectedly
}

impl AnimationQuality {
    pub fn assess(clip: &AnimationClip) -> Self {
        Self {
            has_anticipation: detect_anticipation(clip),
            has_follow_through: detect_follow_through(clip),
            arc_score: calculate_arc_score(clip),
            timing_variance: calculate_timing_variance(clip),
            root_motion_valid: validate_root_motion(clip),
        }
    }

    pub fn suggestions(&self) -> Vec<&'static str> {
        let mut suggestions = vec![];
        if !self.has_anticipation {
            suggestions.push("Add anticipation (small opposite motion before main action)");
        }
        if !self.has_follow_through {
            suggestions.push("Add follow-through (overshoot and settle at end)");
        }
        if self.arc_score < 0.6 {
            suggestions.push("Motion too linear - add natural arcs to movement paths");
        }
        if self.timing_variance < 0.2 {
            suggestions.push("Timing too uniform - vary speeds for organic feel");
        }
        if !self.root_motion_valid {
            suggestions.push("Root motion drifts - check loop point alignment");
        }
        suggestions
    }
}
```

### Creative Agent Definitions

Agents with configurable modes (interactive vs autonomous):

#### Agent: asset-designer

```yaml
---
name: asset-designer
description: Interprets creative requirements and produces semantic asset specifications
color: purple
auto_trigger:
  - "design asset"
  - "create asset"
  - "I need a"
  - "make me a"
  - "asset that looks like"
parameters:
  mode:
    type: enum
    values: [interactive, autonomous]
    default: interactive
    description: |
      interactive: Presents interpretation and asks for confirmation before proceeding
      autonomous: Makes reasonable defaults and produces complete spec without pausing
---

You are the **Asset Designer** agent. Your role is to interpret creative requirements
and produce detailed semantic asset specifications using SADL (Semantic Asset Description Language).

## Your Process

### Interactive Mode (default)
1. Parse the user's creative request
2. Present your interpretation:
   - Identified style tokens
   - Proposed color palette
   - Material selection
   - Shape basis
3. Ask for confirmation or adjustments
4. Produce final SADL specification

### Autonomous Mode
1. Parse the user's creative request
2. Make reasonable default choices for any ambiguity
3. Produce complete SADL specification immediately
4. Summarize the creative decisions made

## SADL Specification Format

```
ASSET: [name]
STYLE: [token] (e.g., Rustic, Cyberpunk, Organic)
PALETTE: [palette] (e.g., WarmEarthy, Neon, Muted)
MATERIAL: [category.variant] (e.g., metal.rusted, wood.weathered)
SHAPE: [descriptor] (e.g., barrel, crate, humanoid)
SCALE: [min]-[max] (relative scale range)
DETAIL: [Low|Medium|High]
POLY_BUDGET: [min]-[max]
SPECIAL: [any unique requirements]
```

## Example

User: "I need a treasure chest for my pirate game"

Interactive response:
"I'm interpreting this as a **Rustic** pirate treasure chest. Here's my proposed specification:
- Style: Rustic (aged, worn materials)
- Palette: WarmEarthy (browns, tans, aged wood tones)
- Material: wood.weathered with metal.rusted accents
- Shape: crate base with curved lid
- Detail: Medium

Does this match your vision? Would you like any adjustments?"

Autonomous response:
"Generated SADL specification for pirate treasure chest:
```
ASSET: treasure_chest
STYLE: Rustic
PALETTE: WarmEarthy
MATERIAL: wood.weathered, metal.rusted (accents)
SHAPE: crate + curved_lid
SCALE: 0.8-1.2
DETAIL: Medium
POLY_BUDGET: 300-800
SPECIAL: Iron bands, keyhole, slightly open lid option
```
Creative decisions: Chose weathered wood over polished for authentic pirate aesthetic.
Rusted iron over brass to emphasize age. Medium detail for game-ready asset."
```

#### Agent: asset-generator

```yaml
---
name: asset-generator
description: Produces procedural generation code from SADL specifications
color: green
auto_trigger:
  - "generate from spec"
  - "implement asset"
  - "create mesh for"
---

You are the **Asset Generator** agent. You take SADL specifications and produce
working procedural generation code for the ZX platform.

## Your Process

1. Parse the SADL specification
2. Select appropriate algorithms:
   - Shape: primitive composition or SDF
   - UV: projection method based on shape
   - Texture: noise functions for material
3. Generate Rust code using nethercore-zx-procgen patterns
4. Include quality validation calls

## Code Generation Rules

- Use existing procedural-meshes patterns for geometry
- Use existing procedural-textures patterns for materials
- Apply style modifiers to base parameters
- Include `TextureQuality::assess()` and `MeshQuality::assess()` calls
- Respect poly budget constraints
- Generate seamless textures when tiling is needed

## Output Format

```rust
// Generated from SADL: [asset_name]
// Style: [style], Palette: [palette], Material: [material]

fn generate_[asset_name](seed: u64) -> GeneratedAsset {
    // Shape generation
    // ...

    // UV unwrapping
    // ...

    // Texture generation
    // ...

    // Quality validation
    let mesh_quality = MeshQuality::assess(&mesh);
    let tex_quality = TextureQuality::assess(&texture);

    debug_assert!(mesh_quality.passes_for_budget(POLY_BUDGET));
    debug_assert!(tex_quality.passes_minimum());

    GeneratedAsset { mesh, material, texture }
}
```
```

#### Agent: asset-critic

```yaml
---
name: asset-critic
description: Evaluates generated assets and suggests improvements
color: orange
auto_trigger:
  - "review asset"
  - "evaluate quality"
  - "is this good"
  - "improve this"
parameters:
  strictness:
    type: enum
    values: [lenient, normal, strict]
    default: normal
    description: |
      lenient: Only flag critical issues (broken geometry, missing UVs)
      normal: Flag issues that affect visual quality
      strict: Flag any deviation from best practices
---

You are the **Asset Critic** agent. You evaluate generated assets against
quality heuristics and suggest specific improvements.

## Evaluation Checklist

### Mesh Quality
- [ ] Within poly budget
- [ ] No degenerate triangles
- [ ] Watertight (no holes)
- [ ] Reasonable vertex distribution

### UV Quality
- [ ] Coverage > 95%
- [ ] No overlapping islands
- [ ] Stretch < 2.0x
- [ ] Appropriate texel density

### Texture Quality
- [ ] Sufficient contrast
- [ ] Coherent noise patterns
- [ ] Tileable (if required)
- [ ] Appropriate color variation

### Animation Quality (if applicable)
- [ ] Has anticipation
- [ ] Has follow-through
- [ ] Natural arcs
- [ ] Varied timing

## Strictness Levels

**Lenient**: Only fail on:
- Degenerate geometry
- Missing UVs
- Completely broken output

**Normal**: Also flag:
- Over poly budget by >20%
- UV stretch > 2.5x
- Low contrast textures
- Mechanical animation timing

**Strict**: Also flag:
- Any poly budget overage
- UV stretch > 1.5x
- Non-tileable textures (if tiling expected)
- Missing animation principles
- Suboptimal algorithm choices

## Output Format

```
ASSET REVIEW: [name]
OVERALL: [PASS|NEEDS_WORK|FAIL]

MESH: [score/10]
- [✓|✗] [check item]: [details]

UV: [score/10]
- [✓|✗] [check item]: [details]

TEXTURE: [score/10]
- [✓|✗] [check item]: [details]

SUGGESTIONS:
1. [Specific actionable improvement]
2. [Specific actionable improvement]
```
```

#### Agent: creative-orchestrator

```yaml
---
name: creative-orchestrator
description: Coordinates the full design → generate → critique pipeline
color: magenta
auto_trigger:
  - "create complete asset"
  - "full asset pipeline"
  - "design and generate"
parameters:
  mode:
    type: enum
    values: [interactive, autonomous]
    default: interactive
    description: Inherited by asset-designer
  max_iterations:
    type: number
    default: 3
    description: Maximum critique-refine cycles before presenting result
---

You are the **Creative Orchestrator** agent. You coordinate the full asset
creation pipeline from requirements to validated output.

## Pipeline Steps

1. **Design Phase** (asset-designer)
   - Interpret requirements
   - Produce SADL specification
   - [Interactive: confirm with user]

2. **Generation Phase** (asset-generator)
   - Generate mesh, UVs, texture
   - Apply style modifiers
   - Produce initial asset

3. **Critique Phase** (asset-critic)
   - Evaluate all quality metrics
   - Identify issues
   - Suggest improvements

4. **Refinement Loop** (if needed)
   - Adjust parameters based on critique
   - Regenerate
   - Re-evaluate
   - Repeat up to max_iterations

5. **Delivery**
   - Present final asset
   - Show quality scores
   - Provide generation code

## Mode Behavior

**Interactive Mode:**
- Pause after design phase for approval
- Show critique results and ask if refinement is needed
- Present options when multiple approaches exist

**Autonomous Mode:**
- Run full pipeline without pausing
- Automatically refine based on critique
- Present final result with summary of all decisions

## Output Format

```
═══════════════════════════════════════════════
CREATIVE PIPELINE: [asset_name]
═══════════════════════════════════════════════

DESIGN PHASE
────────────
[SADL specification]

GENERATION PHASE
────────────────
Mesh: [vertex_count] vertices, [tri_count] triangles
Texture: [resolution] [format]
Material: [material_descriptor]

CRITIQUE PHASE (Iteration [n])
──────────────────────────────
[Critique output]

REFINEMENTS APPLIED
───────────────────
- [Change 1]
- [Change 2]

FINAL RESULT
────────────
Quality Scores:
  Mesh: [X]/10
  UV: [X]/10
  Texture: [X]/10

Generation Code: [link or inline code]
═══════════════════════════════════════════════
```
```

### LLM Self-Assessment Prompts

Prompts LLMs can use to evaluate their own generated content:

```markdown
## Texture Self-Assessment Prompt

Before presenting this texture to the user, evaluate:

1. **Contrast Check**: Does the texture have visible detail, or is it a flat color?
   - Look at darkest and brightest areas
   - If difference < 20% brightness, add more variation

2. **Coherence Check**: Does the noise pattern look natural or like TV static?
   - Natural: Smooth gradients, recognizable patterns
   - Static: Random pixels, no structure
   - If static, increase noise scale or add octaves

3. **Tiling Check**: If this texture will tile, are the edges continuous?
   - Compare left edge to right edge
   - Compare top edge to bottom edge
   - If discontinuous, use seamless tiling technique

4. **Style Match**: Does this match the requested style?
   - Rustic → Should look aged, warm colors
   - Cyberpunk → Should have high contrast, neon accents
   - Organic → Should have natural variation, soft edges

## Mesh Self-Assessment Prompt

Before presenting this mesh to the user, evaluate:

1. **Budget Check**: Is triangle count within specified range?
   - Count: [actual] vs Budget: [specified]
   - If over, consider LOD or simplification

2. **Geometry Check**: Any obviously broken geometry?
   - Zero-area triangles (all vertices same position)
   - Inside-out faces (normals pointing wrong way)
   - Disconnected floating vertices

3. **UV Check**: All faces have UV coordinates?
   - Any solid black areas when textured = missing UVs
   - Any severe stretching = UV distortion

4. **Silhouette Check**: Does the outline read correctly?
   - Is the object recognizable from its silhouette?
   - Key features visible from expected view angles?

## Animation Self-Assessment Prompt

Before presenting this animation to the user, evaluate:

1. **Loop Check**: Does it loop seamlessly?
   - Compare first and last frame
   - Any visible pop or snap at loop point?

2. **Principle Check**: Does it follow animation principles?
   - Anticipation: Small opposite motion before main action?
   - Follow-through: Overshoot and settle at end?
   - Arcs: Motion follows curved paths, not straight lines?

3. **Weight Check**: Does it convey appropriate weight?
   - Heavy objects: Slow start, momentum, settling
   - Light objects: Quick response, bouncy
   - Does timing match the object's apparent mass?

4. **Purpose Check**: Does it serve its gameplay purpose?
   - Clear start and end poses?
   - Key poses readable at game speed?
   - Appropriate length for gameplay context?
```

**Prompt for plugin-dev:**
```
Add skill "semantic-asset-language" to nethercore-zx-procgen. Triggers: "SADL",
"semantic asset", "style token", "design asset", "creative asset", "asset
description", "material semantic", "shape vocabulary", "color palette semantic".

Create agents: asset-designer, asset-generator, asset-critic, creative-orchestrator
in nethercore-zx-procgen.

Cover: Full SADL specification (style tokens → parameters, color palettes → HSL,
materials → PBR, shapes → primitives), constrained generation recipes (safe
parameter ranges), quality heuristics (texture contrast/coherence/tileability,
mesh poly/UV/watertight, animation principles), agent definitions with configurable
modes (interactive vs autonomous), iterative refinement workflow, LLM self-assessment
prompts.

Agents should use parameters block for mode configuration. asset-designer and
creative-orchestrator support interactive/autonomous modes. asset-critic supports
lenient/normal/strict strictness.

Include complete Rust code examples for style tokens, color palettes, material
database, shape vocabulary, constrained recipes, quality assessment functions.
~2500 words for skill, ~500 words per agent.
```

---

## Gap 23: Advanced Techniques & Decision Guides

**Status:** PARTIAL. Algorithms exist but lack decision guidance, quality benchmarks, and external library references.

**The Core Problem:**
The procgen skill has good algorithm implementations, but developers don't know:
1. **Which algorithm to use** for their specific use case
2. **What "good" output looks like** (quality benchmarks)
3. **What external libraries exist** in the Rust/Python/JS ecosystem
4. **Advanced techniques** beyond the basics (domain warping, LSCM, etc.)

### Bone Weight Decision Guide

Choosing the right bone weight algorithm based on mesh characteristics:

```
                    ┌─────────────────────────────┐
                    │    What type of mesh?       │
                    └─────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│   Primitive   │       │    Organic    │       │  Mechanical   │
│ (box, sphere) │       │  (character)  │       │   (robot)     │
└───────────────┘       └───────────────┘       └───────────────┘
        │                       │                       │
        ▼                       │                       ▼
┌───────────────┐               │               ┌───────────────┐
│   Distance    │               │               │   Envelope    │
│    Based      │               │               │ (Volumetric)  │
│  Fast, simple │               │               │  Hard edges   │
└───────────────┘               │               └───────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
            ┌───────────────┐       ┌───────────────┐
            │  Low-medium   │       │     High      │
            │    poly?      │       │     poly?     │
            └───────────────┘       └───────────────┘
                    │                       │
                    ▼                       ▼
            ┌───────────────┐       ┌───────────────┐
            │    Heat       │       │   Geodesic    │
            │  Diffusion    │       │   Distance    │
            │  Good blend   │       │  Best quality │
            └───────────────┘       └───────────────┘
```

#### Decision Matrix

| Mesh Type | Best Algorithm | Fallback | Notes |
|-----------|---------------|----------|-------|
| Simple primitives | Distance-based | - | Fastest, good for props |
| Organic character | Heat diffusion | Geodesic | Balance of speed/quality |
| High-poly sculpt | Geodesic | Heat diffusion | Best quality for AAA |
| Mechanical/robot | Envelope | Distance | Hard edges, no blending |
| Cloth/fabric | Geodesic + secondary | Heat diffusion | Needs jiggle bones |
| Quadruped animal | Heat diffusion | Geodesic | Similar to biped |
| Procedural terrain | N/A | - | Usually not rigged |

#### Algorithm Characteristics

```rust
/// Bone weight algorithm comparison
pub struct AlgorithmProfile {
    pub name: &'static str,
    pub complexity: Complexity,       // O(?) per vertex
    pub quality: Quality,             // Subjective 1-10
    pub handles_concave: bool,        // Works with complex geometry
    pub smooth_transitions: bool,     // Gradual weight falloff
    pub respects_topology: bool,      // Follows mesh surface
}

pub const ALGORITHM_PROFILES: &[AlgorithmProfile] = &[
    AlgorithmProfile {
        name: "Distance-based",
        complexity: Complexity::Linear,      // O(n * bones)
        quality: Quality::Basic,             // 4/10
        handles_concave: false,              // Bleeds through thin walls
        smooth_transitions: true,
        respects_topology: false,            // Straight-line distance only
    },
    AlgorithmProfile {
        name: "Envelope (Volumetric)",
        complexity: Complexity::Linear,      // O(n * bones)
        quality: Quality::Good,              // 6/10
        handles_concave: true,               // Respects bone volumes
        smooth_transitions: false,           // Hard cutoffs
        respects_topology: false,
    },
    AlgorithmProfile {
        name: "Heat Diffusion",
        complexity: Complexity::Quadratic,   // O(n²) for heat solve
        quality: Quality::VeryGood,          // 8/10
        handles_concave: true,
        smooth_transitions: true,
        respects_topology: true,             // Follows surface
    },
    AlgorithmProfile {
        name: "Geodesic Distance",
        complexity: Complexity::QuadraticLog, // O(n² log n) Dijkstra
        quality: Quality::Excellent,          // 10/10
        handles_concave: true,
        smooth_transitions: true,
        respects_topology: true,              // True surface distance
    },
];
```

### Bone Weight Quality Benchmarks

Detecting common weight painting problems:

```rust
/// Bone weight quality validation
pub struct WeightQualityReport {
    pub candy_wrapper_score: f32,     // 0 = bad, 1 = good
    pub weight_bleeding: Vec<BleedingRegion>,
    pub unweighted_vertices: Vec<usize>,
    pub over_influenced: Vec<usize>,  // Too many bones affecting vertex
    pub stretching_risk: Vec<StretchZone>,
}

/// Detect "candy wrapper" effect (twisting causes mesh collapse)
pub fn detect_candy_wrapper(mesh: &Mesh, weights: &BoneWeights, skeleton: &Skeleton) -> f32 {
    let mut score = 1.0;

    for bone_idx in 0..skeleton.bones.len() {
        // Find vertices primarily influenced by this bone
        let influenced: Vec<_> = mesh.vertices.iter().enumerate()
            .filter(|(i, _)| weights.primary_bone(*i) == bone_idx)
            .collect();

        if influenced.len() < 3 { continue; }

        // Check if influenced region has good "width" perpendicular to bone axis
        let bone_axis = skeleton.bones[bone_idx].direction();
        let perpendicular_spread = calculate_perpendicular_spread(&influenced, bone_axis);

        // Thin regions around joints are candy wrapper risk
        if perpendicular_spread < CANDY_WRAPPER_THRESHOLD {
            score *= 0.8;  // Penalize
        }
    }

    score
}

/// Detect weight bleeding through thin geometry
pub fn detect_weight_bleeding(mesh: &Mesh, weights: &BoneWeights) -> Vec<BleedingRegion> {
    let mut bleeding = vec![];

    // Find edges where weight changes dramatically
    for edge in mesh.edges() {
        let w0 = weights.get(edge.v0);
        let w1 = weights.get(edge.v1);

        let weight_diff = weight_distance(w0, w1);

        // Check if this edge bridges two geometrically close but topologically distant regions
        let geometric_dist = (mesh.vertices[edge.v0] - mesh.vertices[edge.v1]).length();
        let topological_dist = geodesic_distance(mesh, edge.v0, edge.v1);

        // If geometrically close but topologically far, weights shouldn't match
        if geometric_dist < 0.1 && topological_dist > 1.0 && weight_diff < 0.1 {
            bleeding.push(BleedingRegion {
                vertices: vec![edge.v0, edge.v1],
                severity: 1.0 - weight_diff,
            });
        }
    }

    bleeding
}

/// Visual benchmark examples (what to look for)
pub const WEIGHT_BENCHMARKS: &str = r#"
GOOD WEIGHTS:
✓ Smooth gradient at joints (elbow, knee, shoulder)
✓ Weights sum to 1.0 at every vertex
✓ Maximum 4 bone influences per vertex (GPU limit)
✓ No weights "jump" across geometry gaps
✓ Clean deformation at 90° bend

BAD WEIGHTS:
✗ Candy wrapper: Mesh collapses when twisted
✗ Weight bleeding: Arm moves when leg moves (weights bleed through torso)
✗ Unweighted vertices: Parts don't move with skeleton
✗ Over-influenced: More than 4 bones = GPU artifacts
✗ Hard edges: Visible seams between bone regions
"#;
```

### UV Mapping Decision Guide

Choosing the right UV projection based on surface type:

```
                    ┌─────────────────────────────┐
                    │   What surface geometry?    │
                    └─────────────────────────────┘
                                │
    ┌───────────────┬───────────┼───────────┬───────────────┐
    ▼               ▼           ▼           ▼               ▼
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  Flat   │   │Cylinder │   │ Sphere  │   │  Box    │   │ Complex │
│ (wall)  │   │ (pipe)  │   │ (ball)  │   │ (crate) │   │(organic)│
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
    │               │           │           │               │
    ▼               ▼           ▼           ▼               ▼
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│ Planar  │   │Cylinder │   │Spherical│   │   Box   │   │ LSCM/   │
│Projection│  │Projection│  │Projection│  │Projection│  │ ABF++   │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
```

#### UV Projection Comparison

| Projection | Best For | Distortion Type | Seams |
|------------|----------|-----------------|-------|
| Planar | Flat surfaces, decals | Stretching at edges | None or 1 |
| Cylindrical | Tubes, limbs, barrels | Poles at caps | 1 vertical |
| Spherical | Balls, planets, heads | Severe pole pinching | 1 vertical |
| Box/Cubic | Crates, buildings | Hard edges at cube faces | 6 edges |
| LSCM | Organic, any shape | Minimal angle distortion | Auto-detected |
| ABF++ | Hard-surface, CAD | Angle preservation | Auto-detected |

### Advanced UV Algorithms

Beyond basic projections:

```rust
/// LSCM (Least Squares Conformal Maps)
/// Minimizes angle distortion, good for organic shapes
pub fn lscm_unwrap(mesh: &Mesh, boundary_vertices: &[usize]) -> Vec<[f32; 2]> {
    // 1. Pin two boundary vertices (prevents rotation/scale ambiguity)
    let pin0 = boundary_vertices[0];
    let pin1 = boundary_vertices[boundary_vertices.len() / 2];

    // 2. Build conformal energy matrix (preserves angles)
    let mut matrix = SparseMatrix::new(mesh.vertices.len() * 2, mesh.vertices.len() * 2);

    for tri in mesh.triangles() {
        // Add conformal energy terms for this triangle
        add_conformal_terms(&mut matrix, mesh, tri);
    }

    // 3. Add pin constraints
    matrix.set_row_to_identity(pin0 * 2);      // u0 = 0
    matrix.set_row_to_identity(pin0 * 2 + 1);  // v0 = 0
    matrix.set_row_to_identity(pin1 * 2);      // u1 = 1
    matrix.set_row_to_identity(pin1 * 2 + 1);  // v1 = 0

    // 4. Solve least squares system
    let solution = matrix.solve_least_squares();

    // 5. Extract UV coordinates
    (0..mesh.vertices.len())
        .map(|i| [solution[i * 2], solution[i * 2 + 1]])
        .collect()
}

/// Automatic seam detection for UV unwrapping
pub fn detect_seams(mesh: &Mesh) -> Vec<Edge> {
    let mut seam_edges = vec![];

    // Seam heuristics:
    // 1. High curvature edges (sharp corners)
    // 2. Edges hidden from common view angles
    // 3. Edges that minimize texture distortion when cut

    for edge in mesh.edges() {
        let curvature = edge_curvature(mesh, edge);
        let visibility = edge_visibility_score(mesh, edge);
        let distortion_reduction = distortion_if_cut(mesh, edge);

        let seam_score = curvature * 0.4 + (1.0 - visibility) * 0.3 + distortion_reduction * 0.3;

        if seam_score > SEAM_THRESHOLD {
            seam_edges.push(edge);
        }
    }

    // Ensure seams form connected paths (no dangling cuts)
    connect_seam_paths(seam_edges)
}

/// UV island packing (fit islands efficiently in 0-1 UV space)
pub fn pack_uv_islands(islands: &mut [UvIsland], padding: f32) -> f32 {
    // Sort islands by area (largest first for better packing)
    islands.sort_by(|a, b| b.area().partial_cmp(&a.area()).unwrap());

    // Use guillotine bin packing algorithm
    let mut packer = GuillotinePacker::new(1.0, 1.0);

    for island in islands.iter_mut() {
        let (width, height) = island.bounding_size();

        if let Some((x, y)) = packer.pack(width + padding, height + padding) {
            island.translate(x + padding / 2.0, y + padding / 2.0);
        } else {
            // Doesn't fit, need to scale down
            let scale = 0.9;
            island.scale(scale);
            // Retry...
        }
    }

    // Return UV space utilization (higher = more efficient)
    islands.iter().map(|i| i.area()).sum::<f32>()
}

/// Texel density analysis (consistent texture resolution across mesh)
pub fn analyze_texel_density(mesh: &Mesh, uvs: &[[f32; 2]], texture_size: u32) -> TexelDensityReport {
    let mut densities = vec![];

    for tri in mesh.triangles() {
        // World-space area
        let world_area = triangle_area_3d(
            mesh.vertices[tri.0],
            mesh.vertices[tri.1],
            mesh.vertices[tri.2],
        );

        // UV-space area (scaled to texture pixels)
        let uv_area = triangle_area_2d(
            uvs[tri.0],
            uvs[tri.1],
            uvs[tri.2],
        ) * (texture_size as f32).powi(2);

        // Texels per world unit
        let density = (uv_area / world_area).sqrt();
        densities.push(density);
    }

    TexelDensityReport {
        min: densities.iter().cloned().fold(f32::INFINITY, f32::min),
        max: densities.iter().cloned().fold(0.0, f32::max),
        average: densities.iter().sum::<f32>() / densities.len() as f32,
        variance: calculate_variance(&densities),
    }
}
```

### Noise Decision Guide

Choosing the right noise function for procedural textures:

```
                    ┌─────────────────────────────┐
                    │   What texture type?        │
                    └─────────────────────────────┘
                                │
    ┌───────────┬───────────────┼───────────────┬───────────┐
    ▼           ▼               ▼               ▼           ▼
┌─────────┐ ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│ Organic │ │ Terrain │   │ Cellular│   │  Clouds │   │ Abstract│
│ (wood)  │ │(height) │   │ (cells) │   │ (soft)  │   │(pattern)│
└─────────┘ └─────────┘   └─────────┘   └─────────┘   └─────────┘
    │           │               │               │           │
    ▼           ▼               ▼               ▼           ▼
┌─────────┐ ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  FBM +  │ │   FBM   │   │ Voronoi │   │ Perlin  │   │ Domain  │
│ Warp    │ │ (octaves)│  │(Worley) │   │(Simplex)│   │ Warping │
└─────────┘ └─────────┘   └─────────┘   └─────────┘   └─────────┘
```

#### Noise Function Comparison

| Noise Type | Visual Character | Best For | Performance |
|------------|-----------------|----------|-------------|
| Perlin | Smooth gradients | Clouds, general | Fast |
| Simplex | Smoother, less grid artifacts | Same as Perlin, 3D+ | Faster in higher dims |
| Worley/Voronoi | Cellular, organic cells | Scales, cobblestone, cells | Medium |
| FBM | Layered detail | Terrain, complex surfaces | Slow (multiple samples) |
| Value | Blocky, retro | Pixel art, Minecraft-style | Fastest |

### Advanced Noise Patterns

```rust
/// Domain warping - distort coordinates before sampling noise
pub fn domain_warp(x: f32, y: f32, noise: &impl Noise) -> f32 {
    // Sample noise at original position
    let warp_x = noise.sample(x, y) * WARP_STRENGTH;
    let warp_y = noise.sample(x + 5.2, y + 1.3) * WARP_STRENGTH;

    // Sample again at warped position
    noise.sample(x + warp_x, y + warp_y)
}

/// Multi-level domain warping for complex organic patterns
pub fn multi_domain_warp(x: f32, y: f32, noise: &impl Noise, levels: u32) -> f32 {
    let mut px = x;
    let mut py = y;

    for _ in 0..levels {
        let wx = noise.sample(px, py);
        let wy = noise.sample(px + 5.2, py + 1.3);
        px += wx * WARP_STRENGTH;
        py += wy * WARP_STRENGTH;
    }

    noise.sample(px, py)
}

/// Reaction-diffusion for organic Turing patterns
/// (stripes, spots, labyrinthine patterns)
pub fn reaction_diffusion(grid: &mut [[f32; 2]], iterations: u32, params: RdParams) {
    let (width, height) = (grid.len(), grid[0].len());
    let mut next = grid.clone();

    for _ in 0..iterations {
        for x in 1..width-1 {
            for y in 1..height-1 {
                let [a, b] = grid[x][y];

                // Laplacian (diffusion)
                let lap_a = laplacian_a(grid, x, y);
                let lap_b = laplacian_b(grid, x, y);

                // Gray-Scott reaction
                let reaction = a * b * b;
                let da = params.diffuse_a * lap_a - reaction + params.feed * (1.0 - a);
                let db = params.diffuse_b * lap_b + reaction - (params.kill + params.feed) * b;

                next[x][y] = [
                    (a + da * params.dt).clamp(0.0, 1.0),
                    (b + db * params.dt).clamp(0.0, 1.0),
                ];
            }
        }
        std::mem::swap(grid, &mut next);
    }
}

/// Seamless tiling via 4D noise sampling
pub fn seamless_noise_2d(x: f32, y: f32, width: f32, height: f32, noise4d: &impl Noise4D) -> f32 {
    // Map 2D coordinates to 4D torus
    let s = x / width;
    let t = y / height;

    let nx = (s * TAU).cos();
    let ny = (s * TAU).sin();
    let nz = (t * TAU).cos();
    let nw = (t * TAU).sin();

    noise4d.sample(nx, ny, nz, nw)
}

/// Height map to normal map conversion
pub fn height_to_normal(heightmap: &[[f32]], strength: f32) -> Vec<Vec<[f32; 3]>> {
    let (width, height) = (heightmap.len(), heightmap[0].len());
    let mut normals = vec![vec![[0.0, 0.0, 1.0]; height]; width];

    for x in 1..width-1 {
        for y in 1..height-1 {
            // Sobel filter for gradients
            let dx = (heightmap[x+1][y-1] - heightmap[x-1][y-1])
                   + (heightmap[x+1][y] - heightmap[x-1][y]) * 2.0
                   + (heightmap[x+1][y+1] - heightmap[x-1][y+1]);

            let dy = (heightmap[x-1][y+1] - heightmap[x-1][y-1])
                   + (heightmap[x][y+1] - heightmap[x][y-1]) * 2.0
                   + (heightmap[x+1][y+1] - heightmap[x+1][y-1]);

            let normal = normalize([
                -dx * strength,
                -dy * strength,
                1.0,
            ]);

            normals[x][y] = normal;
        }
    }

    normals
}
```

### External Library Reference

Production-quality libraries for procedural generation:

#### Rust Libraries

| Library | Purpose | Quality | Notes |
|---------|---------|---------|-------|
| `noise` | Perlin, Simplex, Worley, FBM | Excellent | Most complete, well-maintained |
| `bracket-noise` | Game-focused noise | Good | Part of bracket-lib game toolkit |
| `simdnoise` | SIMD-accelerated noise | Excellent | 2-4x faster than scalar |
| `building_blocks` | Voxel/SDF operations | Excellent | Used by Veloren |
| `ncollide3d` | Collision detection | Excellent | Geometric queries, raycasting |
| `nalgebra` | Linear algebra | Excellent | Matrix math, transforms |
| `glam` | Fast game math | Excellent | SIMD vectors, matrices |
| `lyon` | 2D vector graphics | Excellent | Path tessellation |
| `meshopt` | Mesh optimization | Excellent | Bindings to meshoptimizer |

```toml
# Recommended Cargo.toml additions
[dependencies]
noise = "0.8"
simdnoise = "3.1"
glam = "0.24"
nalgebra = "0.32"
```

#### Python Libraries (for tooling/preprocessing)

| Library | Purpose | Notes |
|---------|---------|-------|
| `trimesh` | Mesh I/O, processing | Load any mesh format, boolean ops |
| `opensimplex` | Simplex noise | Simple, no patent issues |
| `noise` | Perlin noise | Multiple noise types |
| `pyvista` | Mesh visualization | Great for debugging |
| `pyglet` | OpenGL bindings | Quick previews |

```python
# Example: Mesh preprocessing in Python, export for ZX
import trimesh
import numpy as np

mesh = trimesh.load('character.obj')
mesh = mesh.simplify_quadric_decimation(1000)  # Reduce to 1000 faces
mesh.export('character_lowpoly.obj')
```

#### JavaScript/WebGL Libraries

| Library | Purpose | Notes |
|---------|---------|-------|
| `simplex-noise` | Fast simplex noise | Browser-compatible |
| `three.js` | 3D rendering | Previewing generated assets |
| `gl-matrix` | Matrix math | WebGL-compatible transforms |

### Quality Benchmarks Summary

| Asset Type | Minimum Quality | Good Quality | Excellent Quality |
|------------|-----------------|--------------|-------------------|
| **Bone Weights** | Sum = 1.0, ≤4 influences | No candy wrapper, no bleeding | Geodesic + secondary weights |
| **UV Coverage** | >90% | >95% | >99% |
| **UV Stretch** | <3.0x | <2.0x | <1.5x |
| **Texture Contrast** | >0.1 | >0.2 | >0.3 |
| **Noise Coherence** | >0.3 | >0.5 | >0.7 |
| **Poly Budget** | Within 150% | Within 110% | Within 100% |
| **Tileability** | >0.7 (visible seams) | >0.9 | >0.98 (seamless) |

**Prompt for plugin-dev:**
```
Add skill "advanced-techniques" to nethercore-zx-procgen. Triggers: "which algorithm",
"decision guide", "best algorithm for", "quality benchmark", "external library",
"domain warping", "LSCM", "seamless tiling", "noise comparison".

Cover: Decision flowcharts for bone weights, UV mapping, and noise functions. Include
ASCII art flowcharts. Quality benchmarks with numeric thresholds. Automated detection
code for candy wrapper, weight bleeding, UV stretch, texture quality. External library
reference tables (Rust: noise, simdnoise, glam, meshopt; Python: trimesh, opensimplex;
JS: simplex-noise). Advanced algorithms: domain warping, reaction-diffusion, LSCM UV
unwrapping, seamless 4D noise tiling, height-to-normal conversion.

Include complete Rust code examples for each technique. Reference existing skills for
basic algorithms, this skill covers "when to use" and advanced techniques.
~2000 words.
```

---

## Implementation Order

### Phase 1: Core Game Development (Must-Have)
1. **Gap 16 (Physics & Collision)** - CRITICAL - Every game needs this
2. **Gap 20 (Multiplayer Rendering)** - CRITICAL - Prevents desync bugs
3. **Gap 17 (Camera Implementation)** - Most games need camera code
4. **Gap 18 (Gameplay Mechanics)** - Common patterns every game uses

### Phase 1.5: Animation & Creative Infrastructure (NEW)
5. **Gap 21 (BVH/Motion Capture)** - Enables realistic animation data from CMU, Mixamo, Truebones
6. **Gap 22 (AI-First Creative Pipeline)** - SADL vocabulary + creative agents for LLM-friendly asset generation
7. **Gap 23 (Advanced Techniques)** - Decision guides for bone weights, UV mapping, noise algorithms
8. **A3 + A4 + A5 (Mocap Skill + SADL Skill + Creative Agents)** - New procgen infrastructure

**Why Phase 1.5?** These gaps transform the plugin from "procedural-only" to "realistic + creative":
- BVH support unlocks thousands of free mocap animations (CMU: 2,605 clips)
- SADL enables LLMs to translate creative intent ("make it rustic") to parameters
- Decision guides prevent developers from choosing wrong algorithms
- Creative agents provide autonomous asset generation workflows

### Phase 2: Asset Pipeline Completion
9. **Gap 1 (Music)** - Completes procgen audio pipeline
10. **Gap 15 + Gap 14 + A2 (Character Pipeline + UV Texturing + Rigging)** - Complete character workflow

### Phase 3: End-to-End Workflow
11. **Gaps 2+3 (Publishing + Platform)** - Ship games to nethercore.systems
12. **Gaps 4+5 (UI + Game Feel)** - Polish and menus

### Phase 4: Developer Experience
13. **Gap 6 (Debug)** - Testing and debugging guide
14. **Gap 12 (Save Data)** - Persistent storage patterns

### Phase 5: Advanced Features
15. **Gaps 8+9 (EPU + Split-Screen)** - Visual polish, local multiplayer
16. **Gap 19 (AI Patterns)** - Enemy behavior
17. **Gap 7 (Level Design)** - Content creation
18. **Gaps 10+11+13 (Stencil + Fonts + Billboards)** - Advanced rendering

### Phase 6: Architectural Cleanup
19. **A1 (Orchestrator)** - Move to dedicated plugin
