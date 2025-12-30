# SFX Quality Standards and Guidelines

This reference defines quality tiers as concrete code patterns for procedural sound generation. Use these standards to ensure generated SFX meet production requirements.

## Default Quality: Temp Tier (50-70%)

For development placeholder sounds, **always include AT MINIMUM:**

- **✓ 2-3 synthesis layers** (e.g., main oscillator + sub-bass OR harmonics)
- **✓ Proper envelope** with attack transient + exponential decay (NOT linear fade)
- **✓ Filtering** - lowpass sweep OR static resonant filter
- **✓ Harmonics OR detuning** - add 2nd harmonic OR use 2-3 detuned oscillators
- **✓ Normalization** to prevent clipping (scale to 0.9 peak)

These minimum requirements ensure sounds are recognizable, usable for testing, and suitable for development without sounding chiptuney or thin.

## Quality Tier Comparison Table

| Element | Temp (50-70%) | Final (70-90%) | Hero (90-100%) |
|---------|---------------|----------------|----------------|
| **Layers** | 2-3 | 3-4 | 4+ (timbral separation) |
| **Envelope** | Exp decay + attack transient | ADSR or multi-segment | Multi-segment + modulation |
| **Filtering** | Lowpass static OR sweep | Dynamic sweep + resonance | Multi-stage filter chain |
| **Richness** | 2nd harmonic OR 2 detuned oscs | 2nd+3rd harmonics OR 3 oscs | Full harmonic series OR SuperSaw |
| **Effects** | None (optional) | Reverb OR delay OR distortion | Reverb + distortion + compression |
| **Variations** | 1-2 preset functions | 3-4 preset functions | 5+ preset functions |
| **Use Case** | Development, prototyping | Ship-ready production | Marketing, hero assets |

## Anti-Patterns to Avoid

**NEVER generate sounds with only:**

### ❌ Simple sine wave + linear fade (< 30% quality)

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

These produce the exact "8-bit, chiptuney" sounds that users want to avoid.

### ❌ Other common mistakes:

- **No layering** - Single oscillator without harmonics or supporting elements
- **Instant attack** - Sound starts at full volume causing clicks
- **No envelope shaping** - Flat or linearly fading amplitude
- **Missing filter** - Raw oscillator output without frequency shaping
- **No variation functions** - Only one preset, no alternatives
- **Clipping output** - Not normalized, exceeds ±1.0 range

## Pre-Generation Checklist

**Before rendering any SFX, verify your code includes:**

### Required Elements (Temp Tier Minimum)

- [ ] **Layering** - Multiple sound sources combined (not single oscillator)
  - Example: Main + 2nd harmonic, OR main + detuned voices, OR main + sub-bass

- [ ] **Attack transient** - Initial 10-50ms shaped rise (not instant start)
  - Example: `env[:attack_samples] *= np.linspace(0, 1, attack_samples)`

- [ ] **Shaped decay** - Exponential decay (not linear fade)
  - Example: `env = np.exp(-t * decay_rate)` NOT `np.linspace(1, 0, len(t))`

- [ ] **Filtering** - Frequency shaping (static or swept)
  - Example: `signal.butter()` lowpass OR bandpass, applied with `filtfilt()`

- [ ] **Richness** - Harmonics, detuning, OR noise for thickness
  - Example: Add `0.3 * np.sin(2 * phase)` for 2nd harmonic

- [ ] **Normalization** - Scale to 0.9 peak to prevent clipping
  - Example: `audio = audio / np.max(np.abs(audio)) * 0.9`

- [ ] **Variation function** - At least one preset alternative
  - Example: `build_sound_heavy()`, `build_sound_bright()`, etc.

### Additional Elements (Final/Hero Tiers)

- [ ] **ADSR envelope** - Attack, Decay, Sustain, Release segments
- [ ] **Dynamic filtering** - Time-varying cutoff frequency
- [ ] **Effects processing** - Reverb, delay, distortion, chorus
- [ ] **Multiple variations** - 3+ preset functions for different contexts
- [ ] **Professional mixing** - Gain staging, compression if needed

**If any required checklist item is missing, add it before generating.**

## Quality-Focused Code Template

When building custom sounds (no recipe match), use this template as your starting point:

```python
import numpy as np
import soundfile as sf
from scipy import signal

SAMPLE_RATE = 22050

def build_sound():
    """
    Build custom SFX with Temp tier quality (50-70%).
    """
    duration = 0.5
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples, dtype=np.float32)

    # === LAYER 1: Main oscillator ===
    # Your primary sound source (sine, saw, triangle, noise)
    freq = 440  # Frequency in Hz
    phase = 2 * np.pi * freq * t
    layer1 = np.sin(phase)

    # === LAYER 2: Harmonic OR sub-layer ===
    # Adds richness and depth - choose one:
    # Option A: 2nd harmonic for brightness
    layer2 = 0.3 * np.sin(2 * phase)
    # Option B: Sub-bass for weight (uncomment to use)
    # layer2 = 0.4 * np.sin(phase / 2)

    # === LAYER 3 (Optional): Detuned oscillator ===
    # Adds thickness through detuning
    layer3 = 0.2 * np.sin(phase * 1.02)

    # Combine layers with proper mixing
    audio = (layer1 + layer2 + layer3) / 1.5

    # === ENVELOPE: Attack transient + exponential decay ===
    # NOT linear fade - exponential sounds natural
    decay_rate = 10  # Higher = faster decay
    env = np.exp(-t * decay_rate)

    # Attack transient (first 10-50ms) - prevents clicks
    attack_samples = int(SAMPLE_RATE * 0.02)  # 20ms attack
    env[:attack_samples] *= np.linspace(0, 1, attack_samples)

    # Apply envelope
    audio *= env

    # === FILTER: Dynamic sweep OR resonant static ===
    # Shapes frequency content for better timbre

    # Option A: Static lowpass filter
    cutoff_hz = 4000
    nyquist = SAMPLE_RATE / 2
    b, a = signal.butter(2, cutoff_hz / nyquist, btype='low')
    audio = signal.filtfilt(b, a, audio)

    # Option B: Swept lowpass filter (uncomment to use)
    # cutoff_sweep = np.linspace(6000, 2000, len(t))
    # filtered = np.zeros_like(audio)
    # chunk_size = 256
    # for i in range(0, len(audio), chunk_size):
    #     end = min(i + chunk_size, len(audio))
    #     progress = i / len(audio)
    #     cutoff = cutoff_sweep[i]
    #     b, a = signal.butter(2, cutoff / nyquist, btype='low')
    #     filtered[i:end] = signal.lfilter(b, a, audio[i:end])
    # audio = filtered

    # === NORMALIZATION: Prevent clipping ===
    # Scale to 0.9 peak (leave headroom)
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio)) * 0.9

    return audio


def build_sound_heavy():
    """
    Heavier variation with more bass.
    """
    duration = 0.5
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples, dtype=np.float32)

    # Same structure as build_sound(), but with:
    # - Lower base frequency
    # - More sub-bass layer weight
    # - Lower filter cutoff

    freq = 220  # Lower base frequency
    phase = 2 * np.pi * freq * t
    layer1 = np.sin(phase)
    layer2 = 0.6 * np.sin(phase / 2)  # More sub-bass

    audio = (layer1 + layer2) / 1.3

    env = np.exp(-t * 8)  # Slower decay
    attack_samples = int(SAMPLE_RATE * 0.03)
    env[:attack_samples] *= np.linspace(0, 1, attack_samples)
    audio *= env

    # Lower filter cutoff for darker tone
    b, a = signal.butter(2, 2000 / (SAMPLE_RATE/2), btype='low')
    audio = signal.filtfilt(b, a, audio)

    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio)) * 0.9

    return audio


def build_sound_bright():
    """
    Brighter variation with more harmonics.
    """
    duration = 0.5
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples, dtype=np.float32)

    freq = 880  # Higher base frequency
    phase = 2 * np.pi * freq * t

    # More harmonics for brightness
    layer1 = np.sin(phase)
    layer2 = 0.4 * np.sin(2 * phase)  # 2nd harmonic
    layer3 = 0.2 * np.sin(3 * phase)  # 3rd harmonic

    audio = (layer1 + layer2 + layer3) / 1.6

    env = np.exp(-t * 12)  # Faster decay
    attack_samples = int(SAMPLE_RATE * 0.015)
    env[:attack_samples] *= np.linspace(0, 1, attack_samples)
    audio *= env

    # Higher filter cutoff for brighter tone
    b, a = signal.butter(2, 6000 / (SAMPLE_RATE/2), btype='low')
    audio = signal.filtfilt(b, a, audio)

    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio)) * 0.9

    return audio


# === USAGE ===
if __name__ == "__main__":
    # Generate default sound
    audio = build_sound()
    sf.write("sound.wav", audio, SAMPLE_RATE, subtype='PCM_16')

    # Generate variations
    audio_heavy = build_sound_heavy()
    sf.write("sound_heavy.wav", audio_heavy, SAMPLE_RATE, subtype='PCM_16')

    audio_bright = build_sound_bright()
    sf.write("sound_bright.wav", audio_bright, SAMPLE_RATE, subtype='PCM_16')

    print("Generated 3 sound variations")
```

## Key Template Features

The template demonstrates all Temp tier quality requirements:

1. **Multiple layers** (3) - Main + harmonic + detuned
2. **Proper attack transient** - 20ms shaped rise
3. **Exponential decay** - Natural-sounding envelope
4. **Filtering** - Lowpass with both static and swept options
5. **Normalization** - Prevents clipping
6. **Variation functions** - Heavy and bright presets

## Usage Guidelines

### When to use this template:

- No existing recipe matches your sound type
- You need a custom synthesis approach
- Building a unique sound effect

### When to use recipe files instead:

- Sound matches a recipe (laser, explosion, coin, etc.)
- Recipe provides 80% of what you need
- You want production-proven patterns

**Recipe files (`references/sfx-recipes/`) are always the preferred starting point.** Use this template only when recipes don't match your needs.

## Upgrading Quality Tiers

### From Temp (50-70%) to Final (70-90%):

1. Add 1-2 more synthesis layers
2. Implement full ADSR envelope (not just exp decay)
3. Add dynamic filter sweep (time-varying cutoff)
4. Include effects (reverb OR delay OR distortion)
5. Create 3-4 variation functions

### From Final (70-90%) to Hero (90-100%):

1. Ensure 4+ synthesis layers with clear timbral roles
2. Add modulation envelopes (time-varying FM index, filter resonance)
3. Implement full effects chain (reverb + distortion, or chorus + delay)
4. Professional mixing with compression/limiting
5. Create 5+ variation functions for different contexts
6. Add parameter animation (sweeps, LFOs, envelopes on multiple parameters)

## Quality Verification

Before finalizing any SFX generation:

1. **Listen test** - Does it sound thin/chiptuney? If yes, add layers/harmonics
2. **Visual inspection** - Check waveform for clicks at start/end (fix envelope)
3. **Checklist verification** - All required elements present?
4. **Variation test** - At least 2 presets available?
5. **Peak level check** - Normalized to ±0.9 range?

If any verification fails, iterate on the synthesis before rendering final WAV.

## Common Synthesis Patterns by Sound Type

Quick reference for which techniques work best:

| Sound Type | Best Technique | Key Features |
|------------|----------------|--------------|
| **Laser/Zap** | Subtractive + sweep | Freq sweep, harmonics, quick decay |
| **Explosion** | Layered subtractive | Noise + sub-bass + sizzle, filter sweep |
| **Hit/Impact** | Noise transient | Short attack, fast decay, pitch drop optional |
| **Coin/Pickup** | Additive | Arpeggio, individual note envelopes |
| **Jump** | Pitch arc | Quick rise, gradual fall, shaped envelope |
| **Powerup** | FM synthesis | Bell-like tone, sparkle overlay |
| **Ambient/Drone** | Additive or granular | Slow evolution, long sustain, effects |
| **UI Click** | Simple sine | Very short (20-80ms), minimal layers |

For each sound type, check `references/sfx-recipes/` first for complete production examples.
