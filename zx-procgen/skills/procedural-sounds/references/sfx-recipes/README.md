# SFX Recipes

Production-ready NumPy/SciPy recipes for common game sound effects.

## Quick Reference

| Recipe | File | Duration | Technique |
|--------|------|----------|-----------|
| Laser/Zap | `laser.py` | 0.15-0.3s | Frequency sweep |
| Explosion | `explosion.py` | 0.5-1.5s | Layered noise |
| Coin/Pickup | `coin.py` | 0.3-0.5s | Arpeggio |
| Jump | `jump.py` | 0.15-0.3s | Pitch arc |
| Hit/Punch | `hit.py` | 0.05-0.2s | Noise transient |
| Powerup | `powerup.py` | 0.4-0.8s | FM + arpeggio |
| Footstep | `footstep.py` | 0.05-0.15s | Filtered noise |
| UI Click | `ui-click.py` | 0.02-0.08s | Sine blip |

## What Makes These Recipes High-Quality?

These recipes demonstrate production-quality techniques that produce professional-sounding SFX, not thin chiptuney sounds. Here's what separates high-quality SFX from low-quality placeholder sounds:

### ❌ Bad Example (< 30% quality)

Simple sine wave + linear fade:

```python
# DON'T DO THIS - Produces thin, chiptuney sound
t = np.linspace(0, 0.3, int(22050 * 0.3))
audio = np.sin(2 * np.pi * 440 * t)
audio *= np.linspace(1, 0, len(t))  # Linear fade
```

**Problems:**
- Single oscillator (no richness)
- No harmonics or detuning (thin sound)
- Linear fade (unnatural decay)
- No filtering (harsh, static timbre)
- No attack transient (clicks/pops)
- No normalization (may clip)

**Result:** Thin, 8-bit, chiptuney sound unsuitable even for prototyping.

### ✓ Good Example (Temp tier, 50-70% quality)

From `laser.py` recipe:

```python
# Production-quality approach
freq = np.linspace(800, 200, len(t))  # Frequency sweep
phase = np.cumsum(2 * np.pi * freq / 22050)

# LAYER 1: Main oscillator
layer1 = np.sin(phase)

# LAYER 2: 2nd harmonic for richness
layer2 = 0.3 * np.sin(2 * phase)

# LAYER 3: Detuned oscillator for thickness
layer3 = 0.2 * np.sin(phase * 1.02)

audio = (layer1 + layer2 + layer3) / 1.5

# Proper envelope: attack + exponential decay
env = np.exp(-t * 15)  # Exponential (NOT linear)
env[:220] *= np.linspace(0, 1, 220)  # 10ms attack transient

audio *= env

# Filtering for tone shaping
b, a = signal.butter(2, 4000/11025, btype='low')
audio = signal.filtfilt(b, a, audio)

# Normalization
audio = audio / np.max(np.abs(audio)) * 0.9
```

**Quality features:**
- ✓ 3 synthesis layers (depth)
- ✓ Harmonics + detuning (richness)
- ✓ Exponential decay (natural)
- ✓ Attack transient (clean start, no clicks)
- ✓ Lowpass filter (tone shaping)
- ✓ Normalization (no clipping)

**Result:** Rich, professional, recognizable laser sound suitable for production.

### Quality Checklist

Every recipe in this directory includes:

1. **Multiple layers** - Harmonics, detuning, or complementary synthesis
2. **Proper envelopes** - Attack transient + exponential decay curves
3. **Filtering** - Static or swept for timbral evolution
4. **Effects** (where appropriate) - Reverb, distortion, modulation
5. **Variation functions** - Different presets for different contexts
6. **Clear parameters** - Documented at top for easy customization
7. **Normalization** - Clean output without clipping

**Use these patterns as your templates.** When generating custom SFX, apply the same quality standards you see in these recipes.

### Quality Tier Examples

**Temp Tier (50-70%)** - Good for development:
- `laser.py` - 3 layers, harmonics, filtering
- `coin.py` - Arpeggio with individual note envelopes
- `hit.py` - Noise transient with shaped envelope

**Final Tier (70-90%)** - Ship-ready production:
- `explosion.py` - 4 layers (main + sub + sizzle + reverb), dynamic filtering
- `powerup.py` - FM synthesis + arpeggio overlay, multiple variations

## Prerequisites

```bash
pip install numpy scipy soundfile
```

## Usage

Each recipe is a standalone Python script:

```bash
# Generate with default settings
python laser.py

# Generates: laser.wav
```

## Customization

Each script has clearly documented parameter sections:

```python
# =============================================================================
# PARAMETERS - Adjust these to customize the sound
# =============================================================================

START_FREQ = 1200       # Starting frequency (Hz)
END_FREQ = 200          # Ending frequency (Hz)
# ...
```

## Variations

Each recipe includes preset variations as functions:

```python
# In laser.py
def laser_high_energy():
    """More intense, higher pitched laser."""
    # ...

def laser_retro():
    """Classic 8-bit style zap."""
    # ...

if __name__ == "__main__":
    # laser_retro()  # Uncomment to use variation
    render()
```

## Batch Generation

For generating complete sound sets:

```python
# In footstep.py
def render_all_surfaces(output_dir="."):
    """Render footsteps for all surfaces."""
    # Generates: footstep_concrete.wav, footstep_wood.wav, etc.

# In ui-click.py
def render_ui_set(output_dir="."):
    """Render a complete UI sound set."""
    # Generates: ui_click.wav, ui_hover.wav, ui_confirm.wav, etc.
```

## Integration

Output WAVs to your assets directory and reference in `nether.toml`:

```toml
[[assets.sounds]]
id = "laser"
path = "generated/sounds/laser.wav"
```

## Adding New Recipes

Follow the template structure:

1. Parameter section at top with documented settings
2. Build function returning np.ndarray audio
3. Render function with sf.write() output
4. Variation functions for common presets
5. Main block with render call

Example template:

```python
#!/usr/bin/env python3
"""
Sound Effect Name
=================
Description of the sound.

Dependencies: pip install numpy scipy soundfile
"""

import numpy as np
import soundfile as sf
from scipy import signal

# =============================================================================
# PARAMETERS
# =============================================================================

DURATION = 0.3
SAMPLE_RATE = 22050
OUTPUT_FILE = "sound.wav"

# =============================================================================
# SYNTHESIS
# =============================================================================

def build_sound():
    """Build the sound synthesis chain."""
    num_samples = int(SAMPLE_RATE * DURATION)
    t = np.linspace(0, DURATION, num_samples, dtype=np.float32)

    # Your synthesis code here
    audio = np.sin(2 * np.pi * 440 * t)

    return audio.astype(np.float32)


def render():
    """Render the sound to WAV file."""
    audio = build_sound()

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.9

    sf.write(OUTPUT_FILE, audio, SAMPLE_RATE, subtype='PCM_16')
    print(f"Generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    render()
```
