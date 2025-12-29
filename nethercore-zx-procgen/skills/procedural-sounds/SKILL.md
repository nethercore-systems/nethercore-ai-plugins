---
name: Procedural Sound Generation with pyo
description: This skill should be used when the user asks to "generate sound", "create sound effect", "procedural audio", "synth sound", "synthesize sound", "pyo synthesis", "make SFX", "game audio", "WAV generation", "audio synthesis", "sound design", "FM synthesis", "subtractive synthesis", "additive synthesis", "granular synthesis", or mentions sound effects, audio generation, procedural audio, or sound design for game assets. Provides comprehensive guidance for creating procedural sounds using the pyo Python DSP library.
version: 2.0.0
---

# Procedural Sound Generation with pyo

Generate production-quality game sound effects using pyo, a Python DSP module with 250+ signal processing classes.

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

Install pyo and portaudio:

```bash
# macOS
brew install portaudio
pip install pyo

# Windows
pip install pyo  # Includes portaudio

# Linux
sudo apt-get install libportaudio2 portaudio19-dev
pip install pyo
```

## Offline Rendering (Critical)

Always use `audio="offline"` to render without audio hardware:

```python
from pyo import *
import time

s = Server(audio="offline")
s.boot()
s.recordOptions(filename="output.wav", fileformat=0, sampletype=1)

# Build synthesis chain here...
# signal.out()

s.start()
s.recstart()
time.sleep(duration)
s.recstop()
s.stop()
```

See `references/pyo-offline-workflow.md` for complete workflow patterns.

## ZX Audio Requirements

| Spec | Value | Notes |
|------|-------|-------|
| Sample Rate | 22050 Hz | Set via `s.setSamplingRate(22050)` |
| Bit Depth | 16-bit | `sampletype=1` in recordOptions |
| Channels | Mono | Stereo panning done at playback |
| Max Duration | ~2 seconds | Typical SFX budget |
| Simultaneous | 16 channels | Plus 1 dedicated music channel |

## Technique Selection

| Technique | Best For | Key Classes |
|-----------|----------|-------------|
| **Subtractive** | Bassy, warm, explosive | `Noise` → `MoogLP` |
| **FM** | Metallic, bells, digital | `FM`, `CrossFM` |
| **Additive** | Organs, complex tones | Multiple `Sine` summed |
| **Granular** | Textures, ambience | `Granulator` |

See `references/pyo-building-blocks.md` for complete class reference.

## Common SFX Patterns

### Laser/Zap
Descending frequency sweep with harmonics:
```python
env = Adsr(attack=0.01, decay=0.15, sustain=0, release=0.05, dur=0.2)
lfo = Sine(freq=50, mul=200)
osc = SuperSaw(freq=Sig(1200) + lfo, detune=0.5, bal=0.7, mul=env)
filt = MoogLP(osc, freq=4000, res=0.3)
```

### Explosion
Noise burst with lowpass sweep and reverb:
```python
env = Adsr(attack=0.01, decay=0.6, sustain=0, release=0.3, dur=0.9)
noise = PinkNoise(mul=env)
filt = MoogLP(noise, freq=Linseg([(0, 3000), (0.5, 200)]), res=0.4)
verb = Freeverb(filt, size=0.8, damp=0.5)
```

### Coin/Pickup
Ascending arpeggio with quick decay:
```python
freqs = [523, 659, 784, 1047]  # C5, E5, G5, C6
trigs = [Trig().stop() for _ in freqs]
envs = [Adsr(attack=0.005, decay=0.1, sustain=0, release=0.05, dur=0.12, trig=t) for t in trigs]
oscs = [Sine(freq=f, mul=e) for f, e in zip(freqs, envs)]
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

## Additional Resources

- `references/pyo-offline-workflow.md` — Offline rendering patterns
- `references/pyo-building-blocks.md` — Complete pyo class reference
- `references/sfx-recipes/` — Production-ready recipes for all common SFX
