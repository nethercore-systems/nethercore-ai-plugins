# Spec-Based Parser - Completed Features

This file tracks features that have been implemented in the procedural generation parsers. Sister file to `PARSER_ROADMAP.md` which tracks planned features.

---

## Texture Parser (texture_parser.py)

### Layer Types

| Layer Type | Description | Status |
|------------|-------------|--------|
| `solid` | Solid color fill | Done |
| `noise` | Perlin, Simplex, Voronoi noise | Done |
| `gradient` | Linear (vertical/horizontal/diagonal) and radial | Done |
| `checkerboard` | Checkerboard pattern | Done |
| `stripes` | Vertical/horizontal stripes | Done |
| `wood_grain` | Concentric ring pattern with distortion | Done |
| `brick` | Brick pattern with mortar and per-brick variation | Done |

### Blend Modes

| Mode | Description | Status |
|------|-------------|--------|
| `normal` | Standard alpha compositing | Done |
| `multiply` | Darken by multiplication | Done |
| `add` | Lighten by addition | Done |
| `screen` | Inverse multiply (lighten) | Done |
| `overlay` | Combine multiply and screen | Done |
| `soft_light` | Gentle contrast adjustment | Done |

### Features

| Feature | Status |
|---------|--------|
| Color palette application | Done |
| Color ramp (gradient mapping) | Done |
| Layer opacity control | Done |
| Basic compositing | Done |

---

## Normal Parser (normal_parser.py)

### Pattern Types

| Pattern | Description | Status |
|---------|-------------|--------|
| `bricks` | Brick pattern with mortar | Done |
| `tiles` | Square tiles with gaps | Done |
| `hexagons` | Hexagonal tiles | Done |
| `noise` | Perlin-like height noise | Done |
| `scratches` | Random scratch lines | Done |
| `rivets` | Raised circular bumps | Done |
| `weave` | Woven fabric over/under pattern | Done |

### Features

| Feature | Status |
|---------|--------|
| Height-to-normal conversion (Sobel filter) | Done |
| BC5-compatible RGB normal output | Done |
| Strength control | Done |
| Blur support (scipy) | Done |
| Invert mode | Done |
| Dual mode: pattern OR height image conversion | Done |

---

## Character Parser (character_parser.py)

### Part Types

| Type | Description | Status |
|------|-------------|--------|
| Custom extrude parts | Torso, head, limbs via extrude profiles | Done |
| Mirrored parts | `_L`/`_R` suffix auto-mirroring | Done |
| Sub-parts | Fingers, thumbs, secondary elements | Done |
| Instanced parts | Hair spikes, decorative elements | Done |

### Features

| Feature | Status |
|---------|--------|
| Armature/skeleton creation from specs | Done |
| Extrude+scale mesh generation | Done |
| Bulge and tilt modifiers | Done |
| Smooth skinning with automatic weights | Done |
| Bone influence limiting (4 bones/vertex for ZX) | Done |
| UV mapping (smart project and region-based) | Done |
| Triangle budget validation | Done |
| Seam compatibility checking | Done |
| Vertex welding at joints | Done |

---

## Sound Parser (sound_parser.py)

### Synthesis Types

| Type | Description | Status |
|------|-------------|--------|
| `sine` | Sine wave oscillator | Done |
| `square` | Square wave oscillator | Done |
| `saw` | Sawtooth wave oscillator | Done |
| `triangle` | Triangle wave oscillator | Done |
| `noise_burst` | White, pink, brown noise | Done |
| `fm_synth` | FM synthesis with decaying index | Done |
| `karplus` | Karplus-Strong plucked string | Done |
| `pitched_body` | Frequency sweep for kicks/toms | Done |
| `metallic` | Inharmonic partials | Done |
| `harmonics` | Additive synthesis | Done |

### Features

| Feature | Status |
|---------|--------|
| Multi-layer mixing | Done |
| Per-layer ADSR envelopes | Done |
| Per-layer filters (lowpass, highpass, bandpass) | Done |
| Filter sweep support | Done |
| Frequency sweep | Done |
| Amplitude control | Done |
| Layer delay offset | Done |
| Master envelope and filter | Done |
| Normalization with peak control | Done |

### Instrument Features

| Feature | Status |
|---------|--------|
| Note-to-frequency conversion | Done |
| Base note specification | Done |
| Karplus-Strong synthesis | Done |
| FM synthesis | Done |
| Subtractive synthesis | Done |
| Additive synthesis | Done |
| ADSR envelope | Done |
| Multi-oscillator support | Done |
| Detuning | Done |

---

## Motion Parser (motion_parser.py)

### Core Features

| Feature | Status |
|---------|--------|
| Pose-based keyframe animation | Done |
| Multi-phase animation sequencing | Done |
| Skeleton-agnostic (works with any armature) | Done |
| Blender 4.x and 5.0+ API compatibility | Done |
| GLB export with animations | Done |

### Timing Curves

| Curve | Status |
|-------|--------|
| `linear` | Done |
| `ease_in` | Done |
| `ease_out` | Done |
| `ease_in_out` | Done |
| `exponential_in` | Done |
| `exponential_out` | Done |
| `constant` | Done |

### Procedural Layers

| Layer | Description | Status |
|-------|-------------|--------|
| `breathing` | Rhythmic chest expansion | Done |
| `sway` | Idle body sway | Done |
| `bob` | Vertical bobbing motion | Done |
| `noise` | Random micro-motion | Done |

---

## Summary

| Parser | Core Complete | Advanced Features |
|--------|---------------|-------------------|
| Texture | ~35% | ~0% |
| Normal | ~58% | ~15% |
| Character | ~80% | ~0% |
| Sound | ~45% | ~10% |
| Motion | ~70% | ~0% |

See `PARSER_ROADMAP.md` for planned features and enhancements.
