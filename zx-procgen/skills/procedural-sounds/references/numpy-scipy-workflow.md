# NumPy/SciPy Workflow Reference

Complete patterns for rendering audio files using numpy, scipy, and soundfile.

## Core Rendering Pattern

```python
import numpy as np
import soundfile as sf
from scipy import signal

SAMPLE_RATE = 22050  # ZX standard

def render_sound(filename: str, audio: np.ndarray, normalize: bool = True):
    """
    Render audio array to 16-bit WAV file.

    Args:
        filename: Output WAV path
        audio: Audio samples (float32, -1 to 1)
        normalize: Whether to normalize to prevent clipping
    """
    if normalize:
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val * 0.9

    sf.write(filename, audio.astype(np.float32), SAMPLE_RATE, subtype='PCM_16')
    print(f"Generated: {filename}")
```

## File Format Options

```python
# Standard 16-bit WAV (ZX default)
sf.write(filename, audio, SAMPLE_RATE, subtype='PCM_16')

# 24-bit WAV (higher quality)
sf.write(filename, audio, SAMPLE_RATE, subtype='PCM_24')

# 32-bit float WAV (maximum quality)
sf.write(filename, audio, SAMPLE_RATE, subtype='FLOAT')

# FLAC (lossless compression)
sf.write("sound.flac", audio, SAMPLE_RATE)

# OGG Vorbis (lossy compression)
sf.write("sound.ogg", audio, SAMPLE_RATE)
```

## Sample Rate Options

| Value | Use Case |
|-------|----------|
| 22050 | **ZX standard** - good balance |
| 44100 | CD quality |
| 48000 | Video/broadcast standard |
| 11025 | Lo-fi/retro effect |

## Basic Sound Generation

```python
def generate_simple_tone(freq=440, duration=1.0):
    """Generate a simple sine tone with envelope."""
    # Time array
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples, dtype=np.float32)

    # Oscillator
    audio = np.sin(2 * np.pi * freq * t)

    # Envelope (attack + decay)
    attack = int(0.01 * SAMPLE_RATE)
    decay = int(0.2 * SAMPLE_RATE)
    env = np.ones(num_samples)
    env[:attack] = np.linspace(0, 1, attack)
    env[-decay:] = np.linspace(1, 0, decay)

    return audio * env

# Usage
audio = generate_simple_tone(440, 0.5)
render_sound("tone.wav", audio)
```

## Synthesis Function Pattern

Follow this pattern for consistent, reusable sound generators:

```python
def build_laser(
    start_freq=1200,
    end_freq=200,
    duration=0.2,
    detune=0.5,
    filter_freq=4000,
    sample_rate=SAMPLE_RATE
):
    """
    Build a laser/zap sound effect.

    Args:
        start_freq: Starting frequency (Hz)
        end_freq: Ending frequency (Hz)
        duration: Sound length (seconds)
        detune: SuperSaw detune amount (0-1)
        filter_freq: Lowpass cutoff (Hz)

    Returns:
        np.ndarray: Audio samples
    """
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples, dtype=np.float32)

    # Frequency sweep
    freq = np.linspace(start_freq, end_freq, num_samples)
    phase = np.cumsum(2 * np.pi * freq / sample_rate)

    # SuperSaw-like oscillator
    audio = np.sin(phase)
    if detune > 0:
        audio += np.sin(phase * (1 + detune * 0.01)) * 0.5
        audio += np.sin(phase * (1 - detune * 0.01)) * 0.5
        audio /= 2

    # Envelope
    env = np.exp(-t * 15)
    audio *= env

    # Lowpass filter
    nyquist = sample_rate / 2
    normalized_cutoff = min(filter_freq / nyquist, 0.99)
    b, a = signal.butter(2, normalized_cutoff, btype='low')
    audio = signal.filtfilt(b, a, audio)

    return audio.astype(np.float32)
```

## Batch Generation

For efficient multi-sound generation:

```python
def render_batch(sounds: dict, output_dir: str = "generated/sounds"):
    """
    Render multiple sounds to WAV files.

    Args:
        sounds: Dict of {name: (builder_func, kwargs)}
        output_dir: Output directory path
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    for name, (builder, kwargs) in sounds.items():
        audio = builder(**kwargs)
        filepath = os.path.join(output_dir, f"{name}.wav")
        render_sound(filepath, audio)

# Usage
sounds = {
    "laser": (build_laser, {"start_freq": 1200, "duration": 0.2}),
    "laser_heavy": (build_laser, {"start_freq": 600, "end_freq": 80, "duration": 0.35}),
    "laser_retro": (build_laser, {"start_freq": 800, "detune": 0, "duration": 0.12}),
}
render_batch(sounds)
```

## Variations Pattern

Define preset variations as configuration dicts:

```python
# Base parameters
LASER_BASE = {
    "start_freq": 1200,
    "end_freq": 200,
    "duration": 0.2,
    "detune": 0.5,
    "filter_freq": 4000,
}

# Variations
LASER_HEAVY = {**LASER_BASE, "start_freq": 600, "end_freq": 80, "duration": 0.35}
LASER_RETRO = {**LASER_BASE, "start_freq": 800, "detune": 0, "duration": 0.12}
LASER_HIGH = {**LASER_BASE, "start_freq": 2000, "end_freq": 400}

def render_laser_variants():
    for name, params in [
        ("laser", LASER_BASE),
        ("laser_heavy", LASER_HEAVY),
        ("laser_retro", LASER_RETRO),
        ("laser_high", LASER_HIGH),
    ]:
        audio = build_laser(**params)
        render_sound(f"{name}.wav", audio)
```

## Scheduled Events (Arpeggios, Sequences)

For sounds with multiple events:

```python
def build_coin_arpeggio(
    freqs=[523, 659, 784, 1047],  # C5, E5, G5, C6
    note_duration=0.08,
    gap=0.06,
    sample_rate=SAMPLE_RATE
):
    """Build a coin pickup arpeggio."""
    total_duration = len(freqs) * gap + note_duration
    num_samples = int(sample_rate * total_duration)
    t = np.linspace(0, total_duration, num_samples, dtype=np.float32)
    audio = np.zeros(num_samples, dtype=np.float32)

    for i, freq in enumerate(freqs):
        # Note timing
        note_start = i * gap
        note_mask = (t >= note_start) & (t < note_start + note_duration)

        # Note audio
        note_t = t[note_mask] - note_start
        note_audio = np.sin(2 * np.pi * freq * note_t)

        # Quick decay envelope
        note_env = np.exp(-note_t * 25)

        audio[note_mask] += note_audio * note_env * 0.4

    return audio
```

## Layered Sounds

Combine multiple synthesis layers:

```python
def build_explosion(duration=0.8, sample_rate=SAMPLE_RATE):
    """Build a layered explosion sound."""
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples, dtype=np.float32)

    # === LAYER 1: Main noise burst ===
    noise = np.random.randn(num_samples)
    noise_env = np.exp(-t * 3)

    # Sweep filter from high to low
    filtered_noise = np.zeros(num_samples)
    chunk_size = 256
    for i in range(0, num_samples, chunk_size):
        end = min(i + chunk_size, num_samples)
        progress = i / num_samples
        cutoff = 3000 * (1 - progress) + 200 * progress

        nyquist = sample_rate / 2
        norm_cutoff = max(0.01, min(cutoff / nyquist, 0.99))
        b, a = signal.butter(2, norm_cutoff, btype='low')
        filtered_noise[i:end] = signal.lfilter(b, a, noise[i:end])

    layer1 = filtered_noise * noise_env

    # === LAYER 2: Sub bass rumble ===
    sub_freq = np.linspace(50, 35, num_samples)
    phase = np.cumsum(2 * np.pi * sub_freq / sample_rate)
    sub = np.sin(phase)
    sub_env = np.exp(-t * 2)
    layer2 = sub * sub_env * 0.4

    # === LAYER 3: High sizzle ===
    sizzle = np.random.randn(num_samples)
    sizzle = signal.filtfilt(*signal.butter(2, 0.3, btype='high'), sizzle)
    sizzle_env = np.exp(-t * 5)
    layer3 = sizzle * sizzle_env * 0.25

    # === MIX ===
    mixed = layer1 + layer2 + layer3

    # === REVERB (simple) ===
    reverbed = add_simple_reverb(mixed, room_size=0.8, mix=0.3)

    return reverbed.astype(np.float32)


def add_simple_reverb(audio, room_size=0.8, mix=0.3, sample_rate=SAMPLE_RATE):
    """Add simple reverb using comb filters."""
    delays = [int(d * sample_rate) for d in [0.029, 0.037, 0.041, 0.043]]
    output = np.zeros(len(audio) + max(delays))

    for delay in delays:
        comb = np.zeros(len(output))
        feedback = room_size * 0.8

        for i in range(len(audio)):
            comb[i] = audio[i]
            if i >= delay:
                comb[i] += comb[i - delay] * feedback

        output += comb

    output = output[:len(audio)] / len(delays)
    return audio * (1 - mix) + output * mix
```

## Complete Generator Script Template

```python
#!/usr/bin/env python3
"""
SFX Generator for [Game Name]
Generates all game sound effects using numpy/scipy/soundfile.

Usage:
    python sfx.py              # Generate all sounds
    python sfx.py laser        # Generate specific sound
"""

import numpy as np
import soundfile as sf
from scipy import signal
import os
import sys

# =============================================================================
# CONFIGURATION
# =============================================================================

SAMPLE_RATE = 22050
OUTPUT_DIR = "generated/sounds"

# =============================================================================
# CORE UTILITIES
# =============================================================================

def render(name: str, audio: np.ndarray):
    """Render audio to WAV file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{name}.wav")

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.9

    sf.write(filepath, audio.astype(np.float32), SAMPLE_RATE, subtype='PCM_16')
    print(f"Generated: {filepath}")

def lowpass(audio, cutoff):
    """Apply lowpass filter."""
    nyquist = SAMPLE_RATE / 2
    norm = min(cutoff / nyquist, 0.99)
    b, a = signal.butter(2, norm, btype='low')
    return signal.filtfilt(b, a, audio)

def exp_decay(duration, rate=10):
    """Exponential decay envelope."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    return np.exp(-t * rate)

# =============================================================================
# SOUND BUILDERS
# =============================================================================

def build_laser():
    """Laser/zap sound."""
    duration = 0.2
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    freq = np.linspace(1200, 200, len(t))
    phase = np.cumsum(2 * np.pi * freq / SAMPLE_RATE)

    audio = np.sin(phase) + 0.3 * np.sin(2 * phase)
    audio *= exp_decay(duration, 15)
    audio = lowpass(audio, 4000)

    return audio

def build_explosion():
    """Explosion sound."""
    duration = 0.8
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    noise = np.random.randn(len(t))
    noise *= exp_decay(duration, 3)
    audio = lowpass(noise, 1500)

    # Sub bass
    sub = np.sin(np.cumsum(2 * np.pi * np.linspace(50, 30, len(t)) / SAMPLE_RATE))
    sub *= exp_decay(duration, 2) * 0.4

    return audio + sub

def build_coin():
    """Coin pickup sound."""
    duration = 0.4
    freqs = [523, 659, 784, 1047]
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    audio = np.zeros_like(t)

    for i, freq in enumerate(freqs):
        start = i * 0.08
        mask = t >= start
        note_t = t[mask] - start
        audio[mask] += np.sin(2 * np.pi * freq * note_t) * np.exp(-note_t * 25) * 0.3

    return audio

# Add more builders here...

# =============================================================================
# MAIN
# =============================================================================

SOUNDS = {
    "laser": build_laser,
    "explosion": build_explosion,
    "coin": build_coin,
}

def main():
    if len(sys.argv) > 1:
        # Generate specific sound
        name = sys.argv[1]
        if name in SOUNDS:
            render(name, SOUNDS[name]())
        else:
            print(f"Unknown sound: {name}")
            print(f"Available: {', '.join(SOUNDS.keys())}")
    else:
        # Generate all sounds
        for name, builder in SOUNDS.items():
            render(name, builder())
        print("All sounds generated!")

if __name__ == "__main__":
    main()
```

## Common Pitfalls

### 1. Clipping (Values > 1)

```python
# WRONG - may clip
audio = noise + bass + sizzle

# CORRECT - normalize before output
audio = noise + bass + sizzle
audio = audio / np.max(np.abs(audio)) * 0.9
```

### 2. Filter Cutoff Out of Range

```python
# WRONG - will fail if cutoff >= nyquist
b, a = signal.butter(2, cutoff / nyquist, btype='low')

# CORRECT - clamp to valid range
norm_cutoff = min(cutoff / nyquist, 0.99)
b, a = signal.butter(2, norm_cutoff, btype='low')
```

### 3. Wrong Data Type

```python
# WRONG - may cause issues
audio = np.zeros(num_samples)  # float64 by default

# CORRECT - explicit float32
audio = np.zeros(num_samples, dtype=np.float32)
```

### 4. Phase Discontinuities in Frequency Sweeps

```python
# WRONG - direct frequency to phase
audio = np.sin(2 * np.pi * freq_sweep * t)

# CORRECT - integrate frequency to get continuous phase
phase = np.cumsum(2 * np.pi * freq_sweep / sample_rate)
audio = np.sin(phase)
```

## Performance Tips

1. **Use vectorized operations** instead of loops where possible
2. **Pre-allocate arrays** with `np.zeros()` instead of appending
3. **Process in chunks** for time-varying filters
4. **Use `filtfilt`** for zero-phase filtering (cleaner sound)
5. **Cache expensive computations** (e.g., filter coefficients)
