# Audio Enhancement Techniques

Detailed techniques for upgrading audio/SFX quality through the tier system.

## Placeholder → Temp Upgrades

### Add Envelope Shaping

Transform raw tones into shaped sounds:

```python
from dataclasses import dataclass
import numpy as np
import scipy.signal as signal

@dataclass
class Envelope:
    attack: float   # Attack time in seconds
    decay: float    # Decay time in seconds
    sustain: float  # Sustain level (0.0-1.0)
    release: float  # Release time in seconds

# Basic ADSR envelope
envelope = Envelope(
    attack=0.01,   # 10ms attack
    decay=0.1,     # 100ms decay
    sustain=0.6,   # 60% sustain level
    release=0.2,   # 200ms release
)

# Apply to tone
audio = synth.tone('saw', 220.0, duration=0.5, envelope=envelope)
```

### Basic Layering

Add depth with simple layering:

```python
import numpy as np

# Layer 1: Body (main frequency)
body = synth.tone('saw', freq, duration=0.5, envelope=envelope)

# Layer 2: Sub (octave down)
sub = synth.tone('sine', freq / 2.0, duration=0.3, envelope=envelope)

# Mix
audio = body * 0.7 + sub * 0.3
```

### Basic Filtering

Shape frequency content:

```python
from scipy import signal

# Low-pass to remove harshness
audio = apply_lowpass(audio, cutoff=4000.0, resonance=0.3, sample_rate=22050)

# High-pass to remove rumble
audio = apply_highpass(audio, cutoff=80.0, resonance=0.1, sample_rate=22050)

def apply_lowpass(audio: np.ndarray, cutoff: float, resonance: float, sample_rate: int) -> np.ndarray:
    """Apply lowpass filter using scipy."""
    sos = signal.butter(4, cutoff, 'low', fs=sample_rate, output='sos')
    return signal.sosfilt(sos, audio)

def apply_highpass(audio: np.ndarray, cutoff: float, resonance: float, sample_rate: int) -> np.ndarray:
    """Apply highpass filter using scipy."""
    sos = signal.butter(4, cutoff, 'high', fs=sample_rate, output='sos')
    return signal.sosfilt(sos, audio)
```

---

## Temp → Final Upgrades

### Multi-Layer Synthesis

Build rich sounds from multiple components:

```python
from dataclasses import dataclass
import numpy as np
from typing import List, Tuple

@dataclass
class ImpactLayers:
    """Impact sound layers."""
    click: np.ndarray   # Transient click (attack)
    body: np.ndarray    # Body thud (main energy)
    rumble: np.ndarray  # Rumble (low-end weight)
    tail: np.ndarray    # Tail (decay/reverb)

def generate_impact(impact_type: str, sample_rate: int = 22050) -> np.ndarray:
    """Generate multi-layer impact sound."""
    layers = ImpactLayers(
        click=generate_click(duration=0.005, freq=2000.0, sample_rate=sample_rate),
        body=generate_body(impact_type, duration=0.1, sample_rate=sample_rate),
        rumble=generate_rumble(duration=0.3, freq=40.0, sample_rate=sample_rate),
        tail=generate_tail(duration=0.5, sample_rate=sample_rate),
    )

    # Time-aligned mixing
    return mix_timed([
        (layers.click, 0.0, 0.5),     # Immediate
        (layers.body, 0.002, 0.8),    # Slight delay
        (layers.rumble, 0.01, 0.4),   # After attack
        (layers.tail, 0.05, 0.3),     # Decay phase
    ], sample_rate=sample_rate)

def mix_timed(layers: List[Tuple[np.ndarray, float, float]], sample_rate: int) -> np.ndarray:
    """Mix audio layers with time offsets and amplitudes."""
    max_duration = max(delay + len(audio) / sample_rate for audio, delay, _ in layers)
    total_samples = int(max_duration * sample_rate)
    output = np.zeros(total_samples)

    for audio, delay, amplitude in layers:
        start_sample = int(delay * sample_rate)
        end_sample = start_sample + len(audio)
        output[start_sample:end_sample] += audio * amplitude

    return output
```

### Envelope Modulation

Add movement through modulation:

```python
from dataclasses import dataclass

@dataclass
class FilterEnvelope:
    """Filter envelope for modulation."""
    attack: float
    decay: float
    sustain: float
    release: float
    amount: float      # Filter cutoff sweep
    start_freq: float

@dataclass
class PitchEnvelope:
    """Pitch envelope for impact punch."""
    attack: float
    decay: float
    amount: float  # Octave drop

# Filter envelope (separate from amplitude)
filter_envelope = FilterEnvelope(
    attack=0.001,
    decay=0.2,
    sustain=0.3,
    release=0.1,
    amount=4000.0,     # Filter cutoff sweep
    start_freq=200.0,
)

# Pitch envelope (impact "punch")
pitch_envelope = PitchEnvelope(
    attack=0.0,
    decay=0.05,
    amount=2.0,  # Octave drop
)
```

### Harmonic Content

Add harmonics for richness:

```python
import numpy as np
from typing import List, Tuple

def rich_tone(fundamental: float, duration: float, sample_rate: int = 22050) -> np.ndarray:
    """Generate tone with additive harmonics."""
    harmonics: List[Tuple[float, float]] = [
        (1.0, 1.0),     # Fundamental
        (2.0, 0.5),     # 2nd harmonic
        (3.0, 0.3),     # 3rd harmonic
        (4.0, 0.15),    # 4th harmonic
        (5.0, 0.1),     # 5th harmonic
    ]

    samples = int(duration * sample_rate)
    audio = np.zeros(samples)

    for ratio, amp in harmonics:
        freq = fundamental * ratio
        tone = synth.tone('sine', freq, duration, envelope, sample_rate)
        audio += tone * amp

    return audio
```

### Effects Processing

Add character through effects:

```python
import numpy as np

# Subtle distortion for warmth
audio = apply_saturation(audio, drive=0.2, tone=0.5)

# Short reverb for space
audio = apply_reverb(audio, room_size=0.2, damping=0.5, wet=0.15, sample_rate=22050)

# Compression for punch
audio = apply_compressor(audio, threshold=-12.0, ratio=4.0, attack=0.001, release=0.1, sample_rate=22050)

def apply_saturation(audio: np.ndarray, drive: float, tone: float) -> np.ndarray:
    """Apply soft saturation/distortion."""
    return np.tanh(audio * (1.0 + drive))

def apply_compressor(audio: np.ndarray, threshold: float, ratio: float, attack: float, release: float, sample_rate: int) -> np.ndarray:
    """Apply dynamic range compression."""
    # Simplified compressor implementation
    threshold_linear = 10 ** (threshold / 20.0)
    compressed = audio.copy()
    envelope = 0.0

    attack_samples = int(attack * sample_rate)
    release_samples = int(release * sample_rate)

    for i in range(len(compressed)):
        # Simple envelope follower
        level = abs(compressed[i])
        if level > envelope:
            envelope = level  # Fast attack
        else:
            envelope *= 0.999  # Slow release

        # Apply gain reduction
        if envelope > threshold_linear:
            reduction = (envelope - threshold_linear) / ratio
            compressed[i] *= threshold_linear / (threshold_linear + reduction)

    return compressed
```

---

## Final → Hero Upgrades

### Subtle Variation

No two plays should sound identical:

```python
import numpy as np
from typing import List

def play_with_variation(audio: np.ndarray, rng: np.random.Generator, sample_rate: int = 22050) -> np.ndarray:
    """Apply subtle variations to audio."""
    pitch_shift = 1.0 + (rng.random() - 0.5) * 0.04   # ±2%
    volume_shift = 1.0 + (rng.random() - 0.5) * 0.1   # ±5%
    time_shift = rng.random() * 0.01                  # 0-10ms

    # Apply pitch shift (simplified - use librosa for production)
    varied = apply_pitch_shift(audio, pitch_shift, sample_rate)
    varied = varied * volume_shift
    varied = apply_delay(varied, time_shift, sample_rate)

    return varied

def generate_with_variations(base: np.ndarray, count: int, seed: int = 42, sample_rate: int = 22050) -> List[np.ndarray]:
    """Generate multiple variations of a sound."""
    rng = np.random.default_rng(seed)
    return [play_with_variation(base, rng, sample_rate) for _ in range(count)]

def apply_pitch_shift(audio: np.ndarray, ratio: float, sample_rate: int) -> np.ndarray:
    """Simple pitch shift (use librosa.effects.pitch_shift for production)."""
    # Simplified implementation - resample at different rate
    from scipy import signal
    return signal.resample(audio, int(len(audio) / ratio))

def apply_delay(audio: np.ndarray, delay_seconds: float, sample_rate: int) -> np.ndarray:
    """Apply time delay."""
    delay_samples = int(delay_seconds * sample_rate)
    return np.pad(audio, (delay_samples, 0), mode='constant')[:-delay_samples if delay_samples > 0 else None]
```

### Harmonic Richness

Full harmonic spectrum:

```python
import numpy as np
from typing import List, Tuple

def rich_synth(freq: float, duration: float, sample_rate: int = 22050) -> np.ndarray:
    """Rich synthesis with detuned oscillators."""
    voices: List[Tuple[float, float]] = [
        (freq * 0.995, 0.3),   # Slightly flat
        (freq * 1.0, 0.7),     # Center
        (freq * 1.005, 0.3),   # Slightly sharp
        (freq * 0.5, 0.2),     # Sub octave
        (freq * 2.0, 0.15),    # Upper octave
    ]

    samples = int(duration * sample_rate)
    audio = np.zeros(samples)

    for voice_freq, amp in voices:
        tone = synth.tone('saw', voice_freq, duration, envelope, sample_rate)
        audio += tone * amp

    # Gentle chorus for width
    audio = apply_chorus(audio, rate=0.5, depth=0.002, mix=0.3, sample_rate=sample_rate)

    return audio

def apply_chorus(audio: np.ndarray, rate: float, depth: float, mix: float, sample_rate: int) -> np.ndarray:
    """Apply chorus effect."""
    # Simplified chorus - use LFO-modulated delay
    t = np.arange(len(audio)) / sample_rate
    lfo = np.sin(2 * np.pi * rate * t)
    delay_samples = (depth * sample_rate * lfo).astype(int)

    chorus_signal = audio.copy()
    # Simple delay modulation (production code would use interpolation)
    return audio * (1 - mix) + chorus_signal * mix
```

### Spatial Cues

Add dimensional depth:

```python
import numpy as np

# Stereo width (mix to mono for ZX but process in stereo first)
audio = apply_stereo_width(audio, width=1.2, center_focus=0.8)

# Early reflections for size
audio = apply_early_reflections(audio, room_type='small', distance=2.0, wet=0.1, sample_rate=22050)

# Convert to mono with preserved depth
audio = stereo_to_mono_midside(audio, side_amount=0.2)

def stereo_to_mono_midside(audio: np.ndarray, side_amount: float) -> np.ndarray:
    """Convert stereo to mono using mid-side technique."""
    if audio.ndim == 2:
        mid = (audio[:, 0] + audio[:, 1]) / 2
        side = (audio[:, 0] - audio[:, 1]) / 2
        return mid + side * side_amount
    return audio
```

### Dynamic Layering

Layers that respond to context:

```python
import numpy as np

def impact_with_velocity(velocity: float, base_impact: np.ndarray, body_layer: np.ndarray, crack_layer: np.ndarray, sample_rate: int = 22050) -> np.ndarray:
    """Generate velocity-responsive impact sound."""
    duration = 0.5
    samples = int(duration * sample_rate)
    audio = np.zeros(samples)

    # Always present
    audio += base_impact[:samples] * 0.5

    # Medium velocity adds body
    if velocity > 0.4:
        audio += body_layer[:samples] * (velocity * 0.3)

    # High velocity adds crack
    if velocity > 0.7:
        audio += crack_layer[:samples] * ((velocity - 0.7) * 1.5)

    # Maximum velocity adds distortion
    if velocity > 0.9:
        drive = (velocity - 0.9) * 2.0
        audio = apply_saturation(audio, drive=drive, tone=0.3)

    return audio
```

### Micro-Timing

Precise timing for impact:

```python
import numpy as np
from dataclasses import dataclass

@dataclass
class LayerTiming:
    """Layer timing for punch."""
    transient_offset: float = 0.0     # Transient must be first
    body_offset: float = 0.003        # Body slightly delayed for "thump"
    sub_offset: float = 0.01          # Sub builds slower
    room_offset: float = 0.015        # Room response

@dataclass
class Layers:
    """Audio layers."""
    transient: np.ndarray
    body: np.ndarray
    sub: np.ndarray
    room: np.ndarray

def apply_timing(layers: Layers, timing: LayerTiming, total_duration: float, sample_rate: int = 22050) -> np.ndarray:
    """Apply precise timing to layers."""
    total_samples = int(total_duration * sample_rate)
    audio = np.zeros(total_samples)

    # Insert each layer at its offset
    audio = insert_at_offset(audio, layers.transient, timing.transient_offset, sample_rate)
    audio = insert_at_offset(audio, layers.body, timing.body_offset, sample_rate)
    audio = insert_at_offset(audio, layers.sub, timing.sub_offset, sample_rate)
    audio = insert_at_offset(audio, layers.room, timing.room_offset, sample_rate)

    return audio

def insert_at_offset(output: np.ndarray, layer: np.ndarray, offset: float, sample_rate: int) -> np.ndarray:
    """Insert audio layer at specific time offset."""
    start_sample = int(offset * sample_rate)
    end_sample = min(start_sample + len(layer), len(output))
    layer_end = end_sample - start_sample
    output[start_sample:end_sample] += layer[:layer_end]
    return output
```

---

## SFX Category Enhancements

### Impact Sounds

| Tier | Characteristics |
|------|-----------------|
| Placeholder | Single tone with basic envelope |
| Temp | Body + transient, basic filtering |
| Final | Multi-layer, filtered, compressed |
| Hero | Variable layers, spatial, variations |

### UI Sounds

| Tier | Characteristics |
|------|-----------------|
| Placeholder | Simple beep |
| Temp | Shaped tone with filter sweep |
| Final | Layered, harmonic, pleasant |
| Hero | Subtle variation, perfect timing |

### Ambient Sounds

| Tier | Characteristics |
|------|-----------------|
| Placeholder | Looped noise |
| Temp | Filtered noise with movement |
| Final | Multi-layer, evolving |
| Hero | Rich texture, seamless loop |

### Weapon Sounds

| Tier | Characteristics |
|------|-----------------|
| Placeholder | Noise burst |
| Temp | Attack + decay, basic layers |
| Final | Mechanical + explosion layers |
| Hero | Full chain, variations, tail |

---

## Mixing Guidelines by Tier

### Placeholder

```python
import numpy as np

# Simple normalization
audio = normalize(audio, target_db=-6.0)  # Leave headroom

def normalize(audio: np.ndarray, target_db: float) -> np.ndarray:
    """Normalize audio to target dB level."""
    peak = np.max(np.abs(audio))
    target_linear = 10 ** (target_db / 20.0)
    return audio * (target_linear / peak) if peak > 0 else audio
```

### Temp

```python
from scipy import signal

# Basic leveling
audio = normalize(audio, target_db=-6.0)
audio = apply_highpass(audio, cutoff=60.0, resonance=0.1, sample_rate=22050)
audio = apply_lowpass(audio, cutoff=12000.0, resonance=0.1, sample_rate=22050)
```

### Final

```python
import numpy as np

# Proper mix prep
audio = apply_compressor(audio, threshold=-12.0, ratio=3.0, attack=0.01, release=0.1, sample_rate=22050)
audio = normalize(audio, target_db=-6.0)

# EQ for clarity (simplified - use scipy or pydub for production)
audio = apply_eq(audio,
    low_cut=60.0,
    low_shelf=(200.0, -2.0),
    mid=(1000.0, 1.0, 1.0),
    high_shelf=(6000.0, 2.0),
    high_cut=15000.0,
    sample_rate=22050
)
```

### Hero

```python
import numpy as np

# Full mastering chain
audio = apply_eq(audio, sample_rate=22050)  # Detailed EQ
audio = apply_multiband_compression(audio,
    bands=3,
    crossovers=[200.0, 2000.0],
    ratios=[3.0, 2.0, 2.5],
    thresholds=[-18.0, -15.0, -12.0],
    sample_rate=22050
)
audio = apply_saturation(audio, drive=0.1, tone=0.6)
audio = apply_limiter(audio, ceiling=-1.0)
audio = normalize(audio, target_db=-3.0)

# Final check
assert np.max(np.abs(audio)) < 0.95, "Clipping detected"
assert 20 * np.log10(np.sqrt(np.mean(audio**2))) > -20.0, "Too quiet"
```

---

## ZX-Specific Considerations

### Sample Rate

All tiers must output 22050 Hz:

```python
from scipy import signal

# Ensure correct sample rate
def ensure_sample_rate(audio: np.ndarray, current_rate: int, target_rate: int = 22050) -> np.ndarray:
    """Resample audio to target sample rate if needed."""
    if current_rate != target_rate:
        num_samples = int(len(audio) * target_rate / current_rate)
        audio = signal.resample(audio, num_samples)
    return audio
```

### Mono Output

ZX requires mono:

```python
import numpy as np

# Convert stereo processing to mono
def to_mono(audio: np.ndarray) -> np.ndarray:
    """Convert stereo to mono by mixing channels."""
    if audio.ndim == 2:
        return np.mean(audio, axis=1)
    return audio
```

### Duration Budgets

| SFX Type | Placeholder | Temp | Final | Hero |
|----------|-------------|------|-------|------|
| UI click | 0.05s | 0.1s | 0.15s | 0.2s |
| Impact | 0.1s | 0.2s | 0.3s | 0.5s |
| Weapon | 0.2s | 0.3s | 0.5s | 0.8s |
| Ambient loop | 1.0s | 2.0s | 4.0s | 8.0s |
