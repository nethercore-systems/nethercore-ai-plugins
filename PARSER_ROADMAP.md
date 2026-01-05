# Spec-Based Parser Roadmap

Ideas for expanding the procedural generation parsers. Each section lists features that could be added to make the spec-based workflow more powerful.

---

## Texture Parser (texture_parser.py)

### Additional Layer Types

| Layer Type | Description | Parameters |
|------------|-------------|------------|
| `clouds` | Fluffy cloud pattern using turbulence | scale, coverage, softness |
| `marble` | Marble veining pattern | vein_scale, turbulence, colors |
| `leather` | Leather grain texture | pore_size, crease_depth |
| `fabric` | Woven fabric pattern | weave_type (plain, twill, satin), thread_colors |
| `rust` | Rust patches with edges | coverage, edge_roughness, colors |
| `moss` | Organic moss/lichen spots | coverage, clump_size, colors |
| `dirt` | Accumulated dirt in crevices | intensity, uses height info |
| `grunge` | General wear/grime overlay | intensity, scale, seed |
| `cracks` | Fracture patterns | density, depth, branching |
| `scales` | Reptile/fish scale pattern | scale_size, overlap, colors |
| `fur` | Directional fur/hair strokes | direction, length, density |
| `water_caustics` | Underwater light pattern | wave_scale, intensity |

### Additional Blend Modes

| Mode | Description |
|------|-------------|
| `subtract` | Darken by subtracting layer |
| `divide` | Lighten by division |
| `color_dodge` | Brightens underlying layer |
| `color_burn` | Darkens underlying layer |
| `hard_light` | Stronger contrast overlay |
| `linear_light` | Linear dodge + burn |
| `pin_light` | Extreme highlights/shadows |
| `difference` | Absolute difference |
| `exclusion` | Softer difference |
| `hue` | Apply layer hue only |
| `saturation` | Apply layer saturation only |
| `color` | Apply layer hue + saturation |
| `luminosity` | Apply layer brightness only |

### Filter Layers

| Filter | Description | Parameters |
|--------|-------------|------------|
| `blur` | Gaussian blur | radius |
| `sharpen` | Unsharp mask | amount, radius |
| `contrast` | Adjust contrast | factor, midpoint |
| `brightness` | Adjust brightness | amount |
| `levels` | Input/output level mapping | black, white, gamma |
| `curves` | Arbitrary curve adjustment | control_points |
| `posterize` | Reduce color levels | levels |
| `threshold` | Binary threshold | value |
| `edge_detect` | Sobel edge detection | strength |
| `emboss` | Emboss/relief effect | direction, depth |
| `pixelate` | Mosaic effect | block_size |
| `dither` | Apply dithering | pattern (ordered, floyd_steinberg) |

### Distortion Layers

| Distortion | Description | Parameters |
|------------|-------------|------------|
| `wave` | Sinusoidal distortion | amplitude, frequency, direction |
| `turbulence` | Fractal distortion | scale, octaves, intensity |
| `swirl` | Spiral distortion | center, angle, radius |
| `pinch` | Pinch/bulge | center, amount |
| `ripple` | Concentric ripples | center, amplitude, frequency |
| `tile` | Make seamlessly tileable | (no params, fixes edges) |

### Advanced Features

- [ ] **Layer masks** - Use grayscale image to control layer visibility
- [ ] **Layer groups** - Group layers with shared blend mode/opacity
- [ ] **UV transforms** - Scale, rotate, offset UVs per layer
- [ ] **Seamless mode** - Automatic edge-wrapping for tileable textures
- [ ] **PBR output** - Generate albedo + MRE from single spec
- [ ] **Palette quantization** - Reduce to indexed palette for retro look
- [ ] **Normal map output** - Height-based layers auto-generate normal map

---

## Normal Parser (normal_parser.py)

### Additional Pattern Types

| Pattern | Description | Parameters |
|---------|-------------|------------|
| `cobblestone` | Irregular rounded stones | stone_size_range, gap_width |
| `pavement` | Irregular paving slabs | slab_size_range, crack_width |
| `bark` | Tree bark ridges | ridge_depth, ridge_spacing |
| `scales_3d` | Overlapping fish/dragon scales | scale_size, overlap, curvature |
| `chain_mail` | Interlocking rings | ring_size, overlap_pattern |
| `diamond_plate` | Industrial floor pattern | diamond_size, raise_height |
| `quilted` | Padded/quilted fabric | stitch_spacing, puff_height |
| `corrugated` | Corrugated metal | wave_width, wave_depth |
| `herringbone` | Herringbone brick/tile | tile_size, angle |
| `basketweave` | Interlocking basket pattern | strip_width, weave_depth |
| `studded` | Regular stud/button pattern | stud_spacing, stud_size, stud_height |
| `knurling` | Machined grip pattern | diamond_size, depth |

### Height Compositing

| Mode | Description |
|------|-------------|
| `add` | Add heights together |
| `multiply` | Multiply heights |
| `max` | Take maximum height at each point |
| `min` | Take minimum height at each point |
| `blend` | Linear blend with mask |

### Advanced Features

- [ ] **Multi-pattern layers** - Combine multiple patterns before conversion
- [ ] **Detail layers** - Add fine noise over base pattern
- [ ] **Edge detection mode** - Generate normals from albedo texture edges
- [ ] **Cavity/AO output** - Generate cavity/ambient occlusion from height
- [ ] **Displacement map** - Output 16-bit height for vertex displacement
- [ ] **BC5 direct output** - Write 2-channel BC5 directly

---

## Character Parser (character_parser.py)

### Additional Part Types

| Type | Description |
|------|-------------|
| `wing` | Feathered/membrane wing with fold |
| `tentacle` | Tapered flexible appendage |
| `tail_segmented` | Segmented tail (scorpion, snake) |
| `wheel` | Cylindrical wheel/roller |
| `propeller` | Rotating blade assembly |
| `cape` | Cloth cape/cloak mesh |
| `ribbon` | Flowing ribbon/scarf |

### Advanced Features

- [ ] **LOD generation** - Auto-generate lower-detail versions
- [ ] **Animation rig presets** - IK chain setups per skeleton type
- [ ] **Cloth simulation hints** - Mark areas for runtime cloth sim
- [ ] **Facial rig markers** - Define blend shape targets in spec
- [ ] **Hitbox generation** - Auto-generate collision primitives
- [ ] **Vertex color painting** - Per-part vertex color specs

---

## Sound Parser (sound_parser.py)

### Additional Synthesis Types

| Type | Description | Parameters |
|------|-------------|------------|
| `wavetable` | Wavetable oscillator | wavetable (array or preset), position |
| `granular` | Granular synthesis | grain_size, density, source |
| `physical_model` | Physical modeling | model (string, bar, membrane), params |
| `formant` | Vocal formant synthesis | vowel, pitch, throat_length |
| `waveshaper` | Waveshaping distortion | curve, drive |
| `ring_mod` | Ring modulation | carrier_freq, depth |
| `vocoder` | Vocoder effect | bands, carrier_source |

### Additional Layer Types

| Layer | Description |
|-------|-------------|
| `impact` | Transient impact with body |
| `whoosh` | Doppler/movement sweep |
| `rumble` | Low frequency rumble |
| `sparkle` | High frequency shimmer |
| `feedback` | Controlled feedback loop |

### Effects

| Effect | Description | Parameters |
|--------|-------------|------------|
| `reverb` | Room reverb | room_size, damping, wet |
| `delay` | Echo delay | time, feedback, wet |
| `chorus` | Chorus/ensemble | depth, rate, voices |
| `flanger` | Flanger effect | depth, rate, feedback |
| `phaser` | Phase modulation | stages, rate, depth |
| `distortion` | Waveshaping distortion | drive, type |
| `bitcrush` | Bit depth reduction | bits, sample_rate |
| `compressor` | Dynamic range compression | threshold, ratio, attack, release |
| `eq` | Parametric EQ | bands (freq, gain, q) |

---

## Animation Parser (animation.py)

### Additional Procedural Layers

| Layer | Description | Parameters |
|-------|-------------|------------|
| `jiggle` | Secondary motion jiggle | stiffness, damping, bones |
| `trail` | Delayed follow motion | delay_frames, bones |
| `spring` | Spring dynamics | spring_constant, damping |
| `look_at` | IK look-at constraint | target, influence |
| `foot_ik` | Ground contact IK | ground_height, smoothing |
| `hand_ik` | Reach/grab IK | target, blend |

### Advanced Features

- [ ] **Animation blending** - Blend multiple specs together
- [ ] **Additive layers** - Layer animations on top of base
- [ ] **Motion matching hints** - Mark transition points for runtime matching
- [ ] **Root motion extraction** - Extract hip movement as root motion
- [ ] **Event markers** - Define sound/particle trigger frames

---

## Sprite Parser (future)

If we add a sprite parser, potential features:

### Layer Types

| Layer | Description |
|-------|-------------|
| `pixel_noise` | Per-pixel random noise |
| `dither_pattern` | Ordered dither patterns |
| `outline` | Add pixel outline |
| `shadow` | Drop shadow offset |
| `highlight` | Specular highlight spots |
| `gradient_ramp` | Apply color gradient |

### Sprite-Specific Features

- [ ] **Frame animation** - Multiple frames in single spec
- [ ] **Palette cycling** - Color cycling animation hints
- [ ] **Tile connectivity** - Auto-tile rules for tilesets
- [ ] **9-slice hints** - Mark stretchable regions

---

## Mesh Parser (future)

If we add a generic mesh parser beyond characters:

### Primitive Operations

| Operation | Description |
|-----------|-------------|
| `cube` | Box with dimensions |
| `sphere` | UV sphere |
| `cylinder` | Cylinder with segments |
| `cone` | Cone shape |
| `torus` | Torus/donut shape |
| `plane` | Flat plane |

### Boolean Operations

| Op | Description |
|----|-------------|
| `union` | Combine meshes |
| `subtract` | Cut one from another |
| `intersect` | Keep only overlap |

### Modifiers

| Modifier | Description |
|----------|-------------|
| `bevel` | Bevel edges |
| `subdivision` | Catmull-Clark subdivision |
| `decimate` | Reduce triangle count |
| `smooth` | Smooth vertices |
| `extrude` | Extrude faces |
| `array` | Duplicate in pattern |
| `mirror` | Mirror across axis |
| `lattice` | Lattice deformation |

---

## Cross-Parser Features

Features that benefit all parsers:

### Shared Systems

- [ ] **Seed propagation** - Master seed controls all randomness
- [ ] **Variable substitution** - `$var` syntax for parameterized specs
- [ ] **Include files** - `#include` to share common definitions
- [ ] **Preset libraries** - Named presets that specs can reference
- [ ] **Validation mode** - Check spec syntax without generating
- [ ] **Preview mode** - Quick low-res preview generation
- [ ] **Batch runner** - Process all specs in directory
- [ ] **Watch mode** - Auto-regenerate when spec changes

### Quality of Life

- [ ] **Verbose output** - Detailed generation logging
- [ ] **Timing stats** - Report generation time
- [ ] **Size estimation** - Predict output file size
- [ ] **Dependency tracking** - Know when to regenerate

---

## Implementation Priority

1. **High Value, Low Effort**
   - Additional texture blend modes
   - Additional normal map patterns (cobblestone, bark)
   - Sound reverb/delay effects
   - Seamless/tileable texture mode

2. **High Value, Medium Effort**
   - Texture layer masks
   - PBR texture output (albedo + MRE from single spec)
   - Normal map multi-pattern compositing
   - Sound distortion/bitcrush effects

3. **High Value, High Effort**
   - Generic mesh parser
   - Sprite parser with animation frames
   - Animation blending system
   - Wavetable/granular synthesis

4. **Nice to Have**
   - Variable substitution
   - Include files
   - Watch mode
   - Preset libraries

---

## Cross-Cutting Pipeline Features

Features that apply to ALL parsers - the difference between a cool generator and a production system.

### Determinism & Reproducibility

| Feature | Description |
|---------|-------------|
| Global seed propagation | Hierarchical seeds (`asset_seed → layer_seed → sublayer_seed`) |
| Deterministic random streams | Avoid order-dependent randomness |
| Spec hashing | Hash spec → cache outputs → detect changes |

### Versioning & Compatibility

| Feature | Description |
|---------|-------------|
| Spec versioning | `spec_version: 1.2` field for format evolution |
| Migration hooks | Auto-upgrade old specs to current format |
| Deprecation warnings | Non-breaking evolution of features |

### Variants & Parameter Sweeps

| Feature | Description |
|---------|-------------|
| Variant generation | Ranges in specs (`roughness: [0.3, 0.6]`) |
| Combinatorial variants | Generate N permutations automatically |
| Constraint-based variation | "Different but within bounds" |

### Validation & Debugging

| Feature | Description |
|---------|-------------|
| Schema validation | JSON Schema / custom DSL validation |
| Visualization hooks | Render intermediate layers for debugging |
| Error localization | "Layer X invalid parameter Y" with line numbers |

---

## Texture Parser - Additional Gaps

Beyond patterns and blend modes, control & data flow features.

### Data-Driven Mask Layers

| Mask Type | Description |
|-----------|-------------|
| `curvature_mask` | Mask from mesh curvature data |
| `ao_mask` | Mask from ambient occlusion |
| `slope_mask` | Terrain-style slope-based masking |
| `id_mask` | Material zone masks from ID map |

### Procedural Mask Generators

| Generator | Description |
|-----------|-------------|
| `noise_mask` | Thresholded noise patterns |
| `edge_mask` | Derived from normal or height data |
| `distance_mask` | Distance field from shapes |
| `directional_mask` | Wind/wear direction masks |

### Color Intelligence

| Feature | Description |
|---------|-------------|
| Gradient maps | Map grayscale → color ramps |
| Physically plausible colors | Energy-conserving albedo ranges |
| Weathering models | Dirt accumulates after rust, etc. |

### Output Targets

| Feature | Description |
|---------|-------------|
| Engine-specific exports | Unity HDRP, Unreal Material Instance formats |
| Packed texture control | Custom channel packing layouts (ORM, MRE, etc.) |

---

## Normal/Height Parser - Additional Gaps

Signal processing and analysis beyond patterns.

### Height Signal Operations

| Operation | Description |
|-----------|-------------|
| Erosion | Hydraulic / thermal erosion simulation |
| Edge-preserving blur | Blur while keeping sharp features |
| Height remapping | Curves / bias / gain adjustment |
| Frequency splitting | Separate macro vs micro detail layers |

### Normal-Specific Controls

| Feature | Description |
|---------|-------------|
| Per-layer strength | Independent intensity per pattern |
| Reoriented Normal Mapping (RNM) | Correct detail normal blending |
| Detail normal blending | Overlay/blend methods |
| Tangent space selection | MikkTSpace vs custom |

### Analysis Outputs

| Output | Description |
|--------|-------------|
| Slope map | Surface angle for terrain texturing |
| Curvature map | Convex/concave for wear patterns |
| Thickness map | For SSS approximation |
| Bent normal | For improved ambient lighting |

---

## Character Parser - Additional Gaps

Beyond parts, structural and metadata features.

### Topology & Structure

| Feature | Description |
|---------|-------------|
| Symmetry rules | Mirror, radial, broken symmetry |
| Parametric skeleton generation | Generate bones from proportions |
| Constraint-driven proportions | "Long legs, short torso" params |
| Boolean mesh ops | Union / subtract / bevel for details |

### Surface & Deformation

| Feature | Description |
|---------|-------------|
| Muscle / fat volumes | Anatomical volume hints |
| Pose-aware deformation | Corrective shapes per pose |
| Weight painting rules | Automatic weight distribution rules |

### Metadata Outputs

| Output | Description |
|--------|-------------|
| Attachment sockets | Named points for weapons/items |
| Gameplay tags | Per-part tags (head, weakpoint, armor) |
| Material zones | Per-region material IDs |
| Damage regions | Hurtbox/hitbox zone definitions |

---

## Sound Parser - Additional Gaps

Structure and context beyond synthesis.

### Time & Structure

| Feature | Description |
|---------|-------------|
| Multi-stage envelopes | Beyond ADSR (attack→body→tail sections) |
| Macro timing | Distinct attack / sustain / decay phases |
| Loop-aware generation | Seamless loop points |

### Spatial & Runtime Awareness

| Feature | Description |
|---------|-------------|
| Distance curves | Attenuation/filtering by distance |
| Occlusion hints | Muffling parameters |
| Surface interaction | Same impact, different material response |

### Asset Families

| Feature | Description |
|---------|-------------|
| Sound sets | Variants with shared identity |
| State-based layers | Idle / effort / extreme versions |

---

## Animation Parser - Additional Gaps

Motion intent and runtime integration.

### Motion Semantics

| Feature | Description |
|---------|-------------|
| Gait definitions | Walk / run / sneak parameters |
| Phase-aware cycles | Footfall timing, contact frames |
| Balance constraints | Center-of-mass tracking |

### Authoring Helpers

| Feature | Description |
|---------|-------------|
| Pose libraries | Reusable named poses |
| Constraint stacks | IK chains, aim constraints |
| Procedural posing | Reach, brace, lean generators |

### Runtime Integration

| Feature | Description |
|---------|-------------|
| State machine hints | Transition conditions metadata |
| Blend tree metadata | Weight/parameter mappings |
| Sync markers | Footfall, impact event frames |

---

## Spec Language & Tooling

Making "assets as code" actually usable.

### Spec Language Features

| Feature | Description |
|---------|-------------|
| Expressions | `roughness = base * wear_factor` |
| Conditionals | If/else based on parameters |
| Inheritance | Base spec → override specs |
| Includes / references | `#include` for reusable blocks |

### Authoring Experience

| Feature | Description |
|---------|-------------|
| Live preview | Real-time generation feedback |
| Hot reload | Auto-regenerate on save |
| Graph view | Visualize layer stacks / dependencies |
| CLI tooling | Batch generation, CI integration |

---

## Code Generator Parsers (future)

These parsers output **code** (Rust/C/Zig) rather than data files. More complex but enables runtime systems.

### UI Parser

Outputs: Rust/C/Zig code for UI layouts

| Feature | Description |
|---------|-------------|
| Layout specs | Widget tree definitions |
| Style specs | Colors, fonts, spacing |
| State bindings | Data binding hints |
| Focus navigation | Controller/keyboard nav order |

**Output example:** `ui_main_menu.rs` with widget creation code

### VFX Parser

Outputs: Rust/C/Zig code for particle systems

| Feature | Description |
|---------|-------------|
| Emitter definitions | Spawn rate, lifetime, velocity |
| Particle properties | Size, color, rotation curves |
| Force fields | Gravity, wind, turbulence |
| Collision response | Bounce, stick, die |

**Output example:** `vfx_explosion.rs` with particle system setup

### Cutscene Parser

Outputs: Rust/C/Zig code for scripted sequences

| Feature | Description |
|---------|-------------|
| Camera paths | Keyframed positions/rotations |
| Entity actions | Move, animate, spawn, despawn |
| Timing | Delays, triggers, conditions |
| Dialogue integration | Text display triggers |

**Output example:** `cutscene_intro.rs` with sequenced actions

**Note:** These are higher effort than asset parsers due to language binding complexity. Consider starting with a single target language (Rust) and adding C/Zig later.

---

## Tilemap Parser (future)

Procedural level generation - outputs data files (JSON/binary), not runtime code.

### Generation Algorithms

| Algorithm | Description |
|-----------|-------------|
| BSP dungeons | Binary space partition rooms |
| Cellular automata | Cave and organic terrain |
| Wave Function Collapse | Pattern-based generation |
| Noise-based terrain | Heightmap with biomes |

### Tilemap Features

| Feature | Description |
|---------|-------------|
| Autotile | 4-bit, 8-bit, 47-tile blob systems |
| RLE compression | Efficient storage |
| Collision layer output | Walkable/blocked data |
| Entity placement | Spawn point / pickup markers |

---

## Tracking

See `PARSER_ROADMAP_DONE.md` for completed features.
