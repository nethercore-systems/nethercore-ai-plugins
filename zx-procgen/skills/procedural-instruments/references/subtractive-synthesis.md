# Subtractive Synthesis

Start with harmonically rich waveform, filter away frequencies.

## Basic Subtractive

```python
from scipy.signal import butter, lfilter

SAMPLE_RATE = 22050

def subtractive_synth(freq: float, duration: float,
                      waveform: str = 'saw',
                      cutoff_start: float = 4000,
                      cutoff_end: float = 800,
                      resonance: float = 2.0) -> np.ndarray:
    """Subtractive synthesis with filter envelope."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Oscillator
    if waveform == 'saw':
        osc = 2 * (freq * t % 1) - 1
    elif waveform == 'square':
        osc = np.sign(np.sin(2 * np.pi * freq * t))
    elif waveform == 'pulse':
        osc = np.where((freq * t % 1) < 0.25, 1.0, -1.0)
    else:
        osc = np.sin(2 * np.pi * freq * t)

    # Time-varying filter
    output = np.zeros_like(osc)
    chunk_size = SAMPLE_RATE // 50

    for i in range(0, len(osc), chunk_size):
        chunk = osc[i:i + chunk_size]
        progress = i / len(osc)

        cutoff = cutoff_start + (cutoff_end - cutoff_start) * progress
        cutoff_norm = min(cutoff / (SAMPLE_RATE / 2), 0.99)

        b, a = butter(2, cutoff_norm, btype='low')
        output[i:i + len(chunk)] = lfilter(b, a, chunk)

    # Amplitude envelope
    amp = (1 - np.exp(-t * 30)) * np.exp(-t * 1)

    return output * amp
```

## Synth Bass

```python
def synth_bass(freq: float, duration: float = 0.5) -> np.ndarray:
    """Classic subtractive synth bass."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Detuned saws for thickness
    saw1 = 2 * (freq * t % 1) - 1
    saw2 = 2 * (freq * 1.005 * t % 1) - 1
    osc = (saw1 + saw2) * 0.5

    # Sub oscillator
    sub = np.sin(2 * np.pi * freq * 0.5 * t) * 0.5

    # Filter envelope
    cutoff_env = 1500 * np.exp(-t * 8) + 200

    output = np.zeros_like(osc)
    chunk_size = SAMPLE_RATE // 100

    for i in range(0, len(osc), chunk_size):
        chunk = osc[i:i + chunk_size]
        cutoff = cutoff_env[min(i, len(cutoff_env) - 1)]
        cutoff_norm = min(cutoff / (SAMPLE_RATE / 2), 0.99)
        b, a = butter(2, cutoff_norm, btype='low')
        output[i:i + len(chunk)] = lfilter(b, a, chunk)

    output += sub

    # Punchy envelope
    amp = (1 - np.exp(-t * 100)) * np.exp(-t * 3)

    return output * amp / np.max(np.abs(output) + 1e-10)
```

## Brass Lead

```python
def brass_lead(freq: float, duration: float = 1.0) -> np.ndarray:
    """Brassy lead with attack noise."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Saw oscillator
    osc = 2 * (freq * t % 1) - 1

    # Breath noise at attack
    noise = np.random.randn(len(t)) * 0.3
    noise_env = np.exp(-t * 20)
    osc += noise * noise_env

    # Filter opens with note
    cutoff_env = 800 + 3000 * (1 - np.exp(-t * 8))

    output = np.zeros_like(osc)
    chunk_size = SAMPLE_RATE // 100

    for i in range(0, len(osc), chunk_size):
        chunk = osc[i:i + chunk_size]
        cutoff = cutoff_env[min(i, len(cutoff_env) - 1)]
        cutoff_norm = min(cutoff / (SAMPLE_RATE / 2), 0.99)
        b, a = butter(2, cutoff_norm, btype='low')
        output[i:i + len(chunk)] = lfilter(b, a, chunk)

    # Slow attack, medium decay
    amp = (1 - np.exp(-t * 10)) * np.exp(-t * 0.5)

    return output * amp / np.max(np.abs(output) + 1e-10)
```

## Filter Envelope Patterns

| Pattern | Cutoff Start | Cutoff End | Character |
|---------|--------------|------------|-----------|
| Plucky | High | Low | Bright attack, mellow tail |
| Pad | Low | Medium | Slow filter sweep |
| Brass | Low | High | Opens with note |
| Squelch | High | Low (resonant) | Acid bass |
