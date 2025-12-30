# Karplus-Strong Synthesis

Physical modeling for plucked string instruments (guitar, bass, harp, etc.).

## How It Works

```
[Noise Burst] → [Delay Line] → [Low-pass Average] → Output
                     ↑__________________|
```

1. Fill delay line with random noise (the "pluck")
2. Each sample: output current, average with next, write back
3. Averaging acts as low-pass filter (high frequencies decay faster)
4. Delay length = sample_rate / frequency

## Implementation

```python
import numpy as np
import soundfile as sf

SAMPLE_RATE = 22050

def karplus_strong(freq: float, duration: float,
                   damping: float = 0.996,
                   brightness: float = 0.5) -> np.ndarray:
    """
    Generate plucked string sound.

    Args:
        freq: Fundamental frequency in Hz
        duration: Note duration in seconds
        damping: Decay rate (0.99-0.999, higher = longer sustain)
        brightness: Initial noise filtering (0-1, higher = brighter)
    """
    num_samples = int(SAMPLE_RATE * duration)
    delay_length = int(SAMPLE_RATE / freq)

    # Initialize delay line with filtered noise
    noise = np.random.randn(delay_length)
    if brightness < 1.0:
        from scipy.signal import butter, filtfilt
        b, a = butter(2, brightness, btype='low')
        noise = filtfilt(b, a, noise)

    delay_line = noise.copy()
    output = np.zeros(num_samples)
    idx = 0

    for i in range(num_samples):
        output[i] = delay_line[idx]

        # Average with next sample (the key filtering step)
        next_idx = (idx + 1) % delay_length
        averaged = 0.5 * (delay_line[idx] + delay_line[next_idx]) * damping
        delay_line[idx] = averaged

        idx = (idx + 1) % delay_length

    return output / np.max(np.abs(output) + 1e-10)
```

## Acoustic Guitar

```python
def generate_guitar_note(freq: float, duration: float = 1.0) -> np.ndarray:
    """Realistic acoustic guitar note."""
    # Core plucked string
    string = karplus_strong(freq, duration, damping=0.996, brightness=0.7)

    # Add subtle body resonance
    t = np.linspace(0, duration, len(string))
    body = np.sin(2 * np.pi * freq * 2 * t) * 0.1 * np.exp(-t * 3)

    output = string + body
    return output / np.max(np.abs(output))

# Generate and save
audio = generate_guitar_note(220.0, 2.0)  # A3
sf.write("guitar_a3.wav", audio, SAMPLE_RATE, subtype='PCM_16')
```

## Parameter Guide

| Parameter | Effect | Good For |
|-----------|--------|----------|
| damping=0.999 | Long sustain | Clean electric, harp |
| damping=0.990 | Quick decay | Muted guitar, pizzicato |
| brightness=0.3 | Soft, warm | Nylon guitar, upright bass |
| brightness=0.9 | Bright, snappy | Steel string, banjo |

## Bass Guitar

Use longer delay line (lower frequency), more damping:

```python
def bass_guitar(freq: float, duration: float = 1.0) -> np.ndarray:
    # Lower frequencies need adjusted parameters
    return karplus_strong(freq, duration, damping=0.998, brightness=0.4)
```

## Electric Guitar

Add distortion after synthesis:

```python
def electric_guitar(freq: float, duration: float, drive: float = 0.5):
    clean = karplus_strong(freq, duration, damping=0.997, brightness=0.8)
    # Soft clipping
    driven = np.tanh(clean * (1 + drive * 5))
    return driven
```
