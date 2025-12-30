---
name: Procedural Sound Generation with NumPy/SciPy
description: |
  Use this skill when the user wants to GENERATE or CODE sound effects for ZX games. Trigger phrases: "generate sound", "create SFX", "write audio code", "synthesize WAV", "numpy audio", "scipy sound", "procedural SFX", "make laser sound", "explosion sound code", "footstep generator", "FM synthesis", "Karplus-Strong".

  **Before generating:** Check `.studio/sonic-identity.local.md` for project audio specs (reverb, character, processing). Apply those constraints for consistent audio. If no spec exists, ask about style or suggest `/establish-sonic-identity`.

  This skill provides IMPLEMENTATION CODE using numpy/scipy to produce WAV files at build time for ZX ROM assets.

  For DESIGN PATTERNS (layering, sound categories, what makes a good impact): use sound-design:sfx-design.
version: 3.3.0
---

# Procedural Sound Generation with NumPy/SciPy

Generate production-quality game sound effects using numpy for array operations, scipy.signal for filtering, and soundfile for WAV output. A lean, portable stack with no audio hardware requirements.

## Build Integration

Sound generators are **Python scripts** that run at build time via `nether.toml`:

```toml
[build]
script = "python generator/sfx.py && cargo build -p game --target wasm32-unknown-unknown --release"

[[assets.sounds]]
id = "laser"
path = "assets/audio/laser.wav"
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

## Common SFX Patterns

### Laser/Zap
Descending frequency sweep with harmonics:
```python
def make_laser(duration=0.2, start_freq=1200, end_freq=200):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq_sweep = np.linspace(start_freq, end_freq, len(t))
    phase = np.cumsum(2 * np.pi * freq_sweep / SAMPLE_RATE)
    osc = np.sin(phase) + 0.3 * np.sin(2 * phase)  # Add harmonics
    env = np.exp(-t * 15)  # Quick decay
    return osc * env
```

### Explosion
Noise burst with lowpass sweep:
```python
def make_explosion(duration=0.8):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    noise = np.random.randn(len(t))  # White noise
    env = np.exp(-t * 3)  # Slower decay

    # Sweep filter from high to low
    cutoff_sweep = np.linspace(0.3, 0.02, len(t))
    filtered = np.zeros_like(noise)
    for i, cutoff in enumerate(cutoff_sweep[::100]):
        start, end = i*100, min((i+1)*100, len(t))
        b, a = signal.butter(2, cutoff, btype='low')
        filtered[start:end] = signal.lfilter(b, a, noise[start:end])

    return filtered * env
```

### Coin/Pickup
Ascending arpeggio with quick decay:
```python
def make_coin(duration=0.4):
    freqs = [523, 659, 784, 1047]  # C5, E5, G5, C6
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    audio = np.zeros_like(t)

    for i, freq in enumerate(freqs):
        note_start = i * 0.08
        note_env = np.where(t >= note_start,
                          np.exp(-(t - note_start) * 25), 0)
        audio += np.sin(2 * np.pi * freq * t) * note_env * 0.3

    return audio
```

See `references/sfx-recipes/` for complete production-ready recipes for all common game sounds.

## Output Integration

Generated WAVs go to `assets/audio/` and are referenced in `nether.toml`:

```toml
[[assets.sounds]]
id = "laser"
path = "assets/audio/laser.wav"

[[assets.sounds]]
id = "explosion"
path = "assets/audio/explosion.wav"
```

Play in game code:
```rust
let laser = rom_sound_str("laser");
play_sound(laser);
```

## File Organization

```
generator/
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
