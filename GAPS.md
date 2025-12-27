# Plugin Coverage Gaps

Identified gaps in the nethercore-ai-plugins suite for complete end-to-end ZX game development.

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

### Architectural Refactors

| # | Refactor | Priority | Action |
|---|----------|----------|--------|
| A1 | Orchestrator Plugin | MEDIUM | Move game-orchestrator from game-design → NEW nethercore-zx-orchestrator |
| A2 | Skeletal Rigging Skill | MEDIUM | Split procedural-animations → NEW skeletal-rigging skill in procgen |

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
│  │   4. ZX constraint: reasonable bone count (<50)          │    │
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

## Implementation Order

### Phase 1: Core Game Development (Must-Have)
1. **Gap 16 (Physics & Collision)** - CRITICAL - Every game needs this
2. **Gap 20 (Multiplayer Rendering)** - CRITICAL - Prevents desync bugs
3. **Gap 17 (Camera Implementation)** - Most games need camera code
4. **Gap 18 (Gameplay Mechanics)** - Common patterns every game uses

### Phase 2: Asset Pipeline Completion
5. **Gap 1 (Music)** - Completes procgen audio pipeline
6. **Gap 15 + Gap 14 + A2 (Character Pipeline + UV Texturing + Rigging)** - Complete character workflow

### Phase 3: End-to-End Workflow
7. **Gaps 2+3 (Publishing + Platform)** - Ship games to nethercore.systems
8. **Gaps 4+5 (UI + Game Feel)** - Polish and menus

### Phase 4: Developer Experience
9. **Gap 6 (Debug)** - Testing and debugging guide
10. **Gap 12 (Save Data)** - Persistent storage patterns

### Phase 5: Advanced Features
11. **Gaps 8+9 (EPU + Split-Screen)** - Visual polish, local multiplayer
12. **Gap 19 (AI Patterns)** - Enemy behavior
13. **Gap 7 (Level Design)** - Content creation
14. **Gaps 10+11+13 (Stencil + Fonts + Billboards)** - Advanced rendering

### Phase 6: Architectural Cleanup
15. **A1 (Orchestrator)** - Move to dedicated plugin

---

## Architectural Consideration: Orchestrator Placement

**Current State:** `game-orchestrator` agent lives in `nethercore-zx-game-design`.

**Problem:** The orchestrator coordinates *across* all three plugins (game-design → procgen → zx-dev). Having it inside game-design creates:
1. Circular conceptual dependency (game-design "owns" coordination of itself)
2. Unclear responsibility (design vs. workflow management)
3. Plugin that grows beyond its name

**Recommended Solution:** Create `nethercore-zx-orchestrator` as a dedicated coordination plugin.

| Component | Current Location | Recommended Location |
|-----------|-----------------|---------------------|
| game-orchestrator | game-design | **NEW: orchestrator** |
| Project state tracking | (implicit) | **NEW: orchestrator** |
| Cross-plugin handoffs | (undocumented) | **NEW: orchestrator** |

**New Plugin Structure:**
```
nethercore-zx-orchestrator/
├── plugin.json
├── agents/
│   └── game-orchestrator.md    # Moved from game-design
├── skills/
│   └── workflow-guide/         # NEW: explains the 3-phase pipeline
│       └── SKILL.md
└── commands/
    └── project-status.md       # NEW: /project-status command
```

**Benefits:**
- Clear separation of concerns
- Orchestrator can evolve independently
- Plugin names match responsibilities
- Natural place for future workflow features (templates, CI/CD, etc.)

**Prompt for plugin-dev:**
```
Create plugin "nethercore-zx-orchestrator" to coordinate the ZX game development
pipeline. Move game-orchestrator agent from game-design. Add skill "workflow-guide"
(triggers: "development workflow", "game pipeline", "phases", "what's next") that
explains Design → Assets → Implementation flow. Add /project-status command to
assess current project state. The orchestrator invokes other plugins but doesn't
duplicate their content.
```

---

## Architectural Consideration: Rigging vs. Animation Split

**Current State:** `procedural-animations` skill covers BOTH:
1. Skeletal rigging (bone weights, skeleton export, bind pose)
2. Animation generation (walk cycles, IK, state machines)

**Problem:** These are different concerns:
- **Rigging** = One-time mesh preparation (asset pipeline)
- **Animation** = Runtime/asset motion generation

Someone might want to skin a procedural mesh without procedural animation (using hand-authored clips). The combined skill is already 300+ lines.

**Recommended Solution:** Split into two skills.

| Topic | Current | Recommended |
|-------|---------|-------------|
| Bone weight generation | procedural-animations | **skeletal-rigging** |
| Skeleton hierarchy | procedural-animations | **skeletal-rigging** |
| Bind pose / inverse bind | procedural-animations | **skeletal-rigging** |
| GLTF skinned export | procedural-animations | **skeletal-rigging** |
| Walk cycles | procedural-animations | procedural-animations |
| IK systems | procedural-animations | procedural-animations |
| State machines | procedural-animations | procedural-animations |
| Blending | procedural-animations | procedural-animations |

**New Skill:**
```
nethercore-zx-procgen/skills/skeletal-rigging/
├── SKILL.md
├── references/
│   ├── bone-weight-algorithms.md
│   └── skeleton-formats.md
└── examples/
    ├── auto-rig-humanoid.rs
    └── blender-export.md
```

**Triggers for skeletal-rigging:**
"rig character", "bone weights", "skinning", "auto-rig", "skeleton hierarchy", "bind pose", "inverse bind matrix", "weight painting"

**Triggers for procedural-animations (refined):**
"walk cycle", "run animation", "idle animation", "IK", "inverse kinematics", "animation blending", "state machine", "procedural locomotion"

**Prompt for plugin-dev:**
```
Split procedural-animations skill. Create "skeletal-rigging" skill for mesh
preparation: bone weight generation (distance-based, heat diffusion), skeleton
hierarchy design, bind pose, inverse bind matrices, GLTF export with skinning.
Keep procedural-animations for runtime motion: walk/run cycles, IK, state machines,
blending, rigid body animation. Update triggers appropriately.
```

---

## Prompt Best Practices

All prompts include:
- Explicit trigger phrases for skill activation
- Word count targets (~1000-1500 words)
- references/ folder for supplementary content
- Source file references where applicable
- Integration with existing skills/FFI
