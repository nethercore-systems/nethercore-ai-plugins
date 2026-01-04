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

## Animation Parser (motion_parser.py)

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
