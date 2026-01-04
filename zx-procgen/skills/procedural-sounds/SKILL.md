---
name: Procedural Sound Generation with NumPy/SciPy
description: |
  Use this skill when the user wants to GENERATE or CODE sound effects for ZX games.

  **Spec-Driven Workflow (RECOMMENDED):**
  1. Create `.spec.py` file in `.studio/sounds/`
  2. Run `python sound_parser.py sfx spec.py output.wav`
  3. Spec persists for iteration; parser handles synthesis

  **Load references when:**
  - Creating SFX specs → `references/sound-spec-format.md`
  - Running parser → `references/sound_parser.py`
  - Example specs → `examples/laser.spec.py`, `examples/explosion.spec.py`
  - Manual synthesis (rare) → `references/sfx-recipes/`

  **Before generating:** Check `.studio/sonic-identity.md` for project audio specs.
version: 4.0.0
---

# Procedural Sound Generation with NumPy/SciPy

Generate production-quality game sound effects using a **spec-driven workflow**. Create declarative specs, run the parser, iterate on parameters without regenerating code.

## Spec-Driven Workflow (Primary)

**Architecture:**
```
LLM creates spec (.spec.py)  →  sound_parser.py  →  WAV file
         ↓
  .studio/sounds/
```

**Step 1: Create Spec**
```python
# .studio/sounds/laser.spec.py
SOUND = {
    "sound": {
        "name": "laser",
        "duration": 0.25,
        "layers": [
            {"type": "fm_synth", "carrier_freq": 600, "mod_ratio": 1.5, "mod_index": 6.0},
            {"type": "noise_burst", "duration": 0.02, "amplitude": 0.3}
        ],
        "envelope": {"attack": 0.002, "decay": 0.15, "sustain": 0, "release": 0.08}
    }
}
```

**Step 2: Run Parser**
```bash
python sound_parser.py sfx .studio/sounds/laser.spec.py generated/audio/laser.wav
```

**Step 3: Iterate**
Edit spec parameters, re-run parser. Same spec = same output (deterministic).

**See:** `references/sound-spec-format.md` for complete format, `examples/` for working specs.

## Example Specs

| Sound | Spec File | Description |
|-------|-----------|-------------|
| Laser | `examples/laser.spec.py` | FM + noise transient |
| Explosion | `examples/explosion.spec.py` | 4-layer with rumble |
| Coin | `examples/coin.spec.py` | Ascending harmonics |
| Jump | `examples/jump.spec.py` | Pitch sweep |

## Manual Synthesis (Advanced)

For cases where specs don't cover your needs, use numpy/scipy directly. The rest of this document covers manual synthesis techniques.

## Build Integration

Sound generators are **Python scripts** that run at build time via `nether.toml`:

```toml
[build]
script = "python generation/sfx.py && cargo build -p game --target wasm32-unknown-unknown --release"

[[assets.sounds]]
id = "laser"
path = "generated/audio/laser.wav"
```

See the **Native Asset Pipeline** skill for full architecture details.

## Prerequisites

Install with pip (no native dependencies required):

```bash
pip install numpy scipy soundfile
```

That's it - works on all platforms without portaudio or special setup.

## Core Workflow

Render sounds to WAV files with pure numpy operations:

```python
import numpy as np
import soundfile as sf
from scipy import signal

SAMPLE_RATE = 22050  # ZX standard

def render_sound(filename: str, audio: np.ndarray):
    """Write audio array to 16-bit WAV file."""
    # Normalize to prevent clipping
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio)) * 0.9
    sf.write(filename, audio, SAMPLE_RATE, subtype='PCM_16')

# Example: Simple sine tone
duration = 0.5
t = np.linspace(0, duration, int(SAMPLE_RATE * duration), dtype=np.float32)
audio = np.sin(2 * np.pi * 440 * t)
render_sound("tone.wav", audio)
```

See `references/numpy-scipy-workflow.md` for complete workflow patterns.

## ZX Audio Requirements

| Spec | Value | Notes |
|------|-------|-------|
| Sample Rate | 22050 Hz | Standard for all ZX audio |
| Bit Depth | 16-bit | Via `subtype='PCM_16'` |
| Channels | Mono | Stereo panning done at playback |
| Max Duration | ~2 seconds | Typical SFX budget |
| Simultaneous | 16 channels | Plus 1 dedicated music channel |

## Quality Standards

**Default: Temp Tier (50-70%)** - Good enough for development, recognizable, usable.

Minimum requirements for ALL generated SFX:
- **2-3 synthesis layers** (main + harmonic/sub/detuned)
- **Proper envelope** (attack transient + exponential decay, NOT linear fade)
- **Filtering** (lowpass sweep OR static resonant)
- **Richness** (harmonics OR detuning for thickness)
- **Normalization** (scale to 0.9 peak)

**Anti-patterns to avoid:**
- ❌ Simple sine wave + linear fade (produces thin, chiptuney sounds)
- ❌ Single oscillator, no harmonics, no filtering
- ❌ Instant attack causing clicks

**See `references/quality-standards.md` for:**
- Quality tier comparison table (Temp/Final/Hero)
- Pre-generation checklist
- Quality-focused code template
- Detailed guidelines and examples

## Technique Selection

| Technique | Best For | Key Functions |
|-----------|----------|---------------|
| **Subtractive** | Bassy, warm, explosive | `np.random` + `signal.butter` |
| **FM** | Metallic, bells, digital | `np.sin` with modulation |
| **Additive** | Organs, complex tones | Multiple `np.sin` summed |
| **Karplus-Strong** | Plucked strings | Delay line averaging |
| **Granular** | Textures, time-stretch | Grain windowing |

### FM Parameter Reference

| Sound | Ratio | Index | Envelope |
|-------|-------|-------|----------|
| Bell | 1:1.4 | 3-8 | Slow decay |
| Electric Piano | 1:1 | 2-4 | Fast decay |
| Bass | 1:1 | 1-3 | Pluck envelope |
| Brass | 1:1 | 4-8 | Slow attack |
| Metallic | 1:1.41 | 5+ | Any |

```python
def fm_synth(freq, duration, ratio=1.0, index=2.0, decay=5.0):
    """FM synthesis: carrier modulated by modulator."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    mod_freq = freq * ratio
    modulator = np.sin(2 * np.pi * mod_freq * t)
    carrier = np.sin(2 * np.pi * freq * t + index * modulator)
    env = np.exp(-t * decay)
    return carrier * env
```

### Karplus-Strong (Plucked Strings)

```python
def karplus_strong(freq, duration, damping=0.996):
    """Physically-modeled plucked string sound."""
    samples = int(SAMPLE_RATE * duration)
    delay_len = int(SAMPLE_RATE / freq)

    # Initialize with noise burst (the "pluck")
    buffer = np.random.rand(delay_len) * 2 - 1
    output = np.zeros(samples)

    for i in range(samples):
        output[i] = buffer[i % delay_len]
        # Average adjacent samples (low-pass = string damping)
        avg = (buffer[i % delay_len] + buffer[(i + 1) % delay_len]) * 0.5
        buffer[i % delay_len] = avg * damping

    return output
```

See `references/numpy-scipy-building-blocks.md` for complete function reference.

## Sound Generation Workflow

When asked to generate a sound effect, **follow these steps:**

### Step 1: Check Recipe Files First

**Before generating custom code**, check if a recipe matches your sound type:

| Sound Type | Recipe File | Quality |
|------------|-------------|---------|
| Laser/Zap/Projectile | `references/sfx-recipes/laser.py` | Temp→Final |
| Explosion/Blast | `references/sfx-recipes/explosion.py` | Final |
| Hit/Impact/Punch | `references/sfx-recipes/hit.py` | Temp |
| Coin/Pickup/Reward | `references/sfx-recipes/coin.py` | Temp |
| Jump/Hop/Bounce | `references/sfx-recipes/jump.py` | Temp |
| Powerup/Buff/Magic | `references/sfx-recipes/powerup.py` | Final |
| Footstep/Walk | `references/sfx-recipes/footstep.py` | Temp |
| UI Click/Button | `references/sfx-recipes/ui-click.py` | Temp |

**If recipe matches:** Read the file, copy `build_*()` function, customize parameters.
**If no match:** Use quality standards and build from scratch (see `references/quality-standards.md` for template).

### Step 2: Apply Quality Tier

Default to **Temp tier (50-70%)**: 2-3 layers, proper envelope, filtering, harmonics/detuning, normalization.

### Step 3: Verify Checklist

Before rendering, ensure: layering ✓, attack transient ✓, exp decay ✓, filtering ✓, richness ✓, normalized ✓.

See `references/quality-standards.md` for complete checklist and quality-focused code template.

## Production-Quality Recipe Library

The `references/sfx-recipes/` directory contains 8 complete, production-ready recipes demonstrating advanced synthesis techniques. **Use these as your primary reference.**

### Combat & Action
- **laser.py** - Multi-osc detuning, harmonics, freq sweep (Temp→Final)
- **explosion.py** - 3-layer (noise + sub-bass + sizzle), reverb (Final)
- **hit.py** - Noise transient, shaped envelope (Temp)

### Gameplay Events
- **coin.py** - Ascending arpeggio, individual note envelopes (Temp)
- **jump.py** - Pitch arc, natural feel (Temp)
- **powerup.py** - FM synthesis, sparkle overlay (Final)

### Character & UI
- **footstep.py** - Surface-specific filtering, batch generation (Temp)
- **ui-click.py** - Quick blip, subtle (Temp)

**Each recipe includes:**
- Clear parameter documentation at top
- Quality features (layering, proper envelopes, filtering)
- Variation functions for different contexts
- Complete working code ready to customize

**How to use:** (1) Identify closest match from table above, (2) Read the recipe file, (3) Copy `build_*()` function, (4) Customize parameters, (5) Use variation functions (e.g., `laser_retro()`, `coin_gem()`).

See `references/sfx-recipes/README.md` for quick reference and quality comparison examples.

## Output Integration

Generated WAVs go to `generated/audio/` and are referenced in `nether.toml`:

```toml
[[assets.sounds]]
id = "laser"
path = "generated/audio/laser.wav"

[[assets.sounds]]
id = "explosion"
path = "generated/audio/explosion.wav"
```

Play in game code:
```rust
let laser = rom_sound_str("laser");
play_sound(laser);
```

## File Organization

```
generation/
├── sfx.py              # Main generator script
├── sounds/
│   ├── combat.py       # Laser, explosion, hit
│   ├── gameplay.py     # Coin, jump, powerup
│   ├── ui.py           # Click, confirm, cancel
│   └── ambient.py      # Wind, water, fire
└── utils/
    ├── synthesis.py    # Common synthesis helpers
    └── export.py       # WAV export utilities
```

## Why NumPy/SciPy?

| Aspect | NumPy/SciPy/Soundfile | pyo |
|--------|----------------------|-----|
| Dependencies | 3 pip packages | pyo + portaudio |
| Installation | `pip install` only | Requires native libs |
| Audio hardware | Not needed | Needs server/offline mode |
| Code style | Array operations | Object graph |
| Learning curve | Standard NumPy | Custom DSP library |
| Portability | All platforms | Platform-specific issues |

## Additional Resources

- `references/numpy-scipy-workflow.md` — Complete rendering patterns
- `references/numpy-scipy-building-blocks.md` — Synthesis function reference
- `references/sfx-recipes/` — Production-ready recipes for all common SFX
