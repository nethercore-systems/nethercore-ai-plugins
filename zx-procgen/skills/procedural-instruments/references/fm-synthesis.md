# FM Synthesis

Frequency Modulation for keys, bells, and complex evolving timbres.

## Core Formula

```
output = sin(carrier_freq * t + index * sin(modulator_freq * t))
```

- **Carrier:Modulator ratio** determines harmonic content
- **Index** (modulation depth) determines brightness
- **Index envelope** creates timbral evolution

## Implementation

```python
SAMPLE_RATE = 22050

def fm_synth(freq: float, duration: float,
             ratio: float = 1.0,
             index: float = 5.0,
             index_decay: float = 8.0) -> np.ndarray:
    """
    FM synthesis with decaying modulation index.

    Args:
        freq: Carrier frequency
        ratio: Modulator/Carrier frequency ratio
        index: Peak modulation index (brightness)
        index_decay: How fast brightness decays
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    carrier_freq = freq
    mod_freq = freq * ratio

    # Index envelope: bright attack, mellow sustain
    index_env = index * np.exp(-t * index_decay)

    # Modulator
    modulator = np.sin(2 * np.pi * mod_freq * t)

    # Carrier with FM
    carrier = np.sin(2 * np.pi * carrier_freq * t + index_env * modulator)

    # Amplitude envelope
    amp_env = np.exp(-t * 2) * (1 - np.exp(-t * 50))

    return carrier * amp_env
```

## Electric Piano (DX7-style)

```python
def electric_piano(freq: float, duration: float = 1.0) -> np.ndarray:
    """DX7-style electric piano (Rhodes-like)."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Two-operator FM: 1:1 ratio
    index = 3.5 * np.exp(-t * 6)
    modulator = np.sin(2 * np.pi * freq * t)
    carrier = np.sin(2 * np.pi * freq * t + index * modulator)

    # Second harmonic for body
    harm2 = np.sin(2 * np.pi * freq * 2 * t) * 0.2 * np.exp(-t * 4)

    # Bell-like attack transient
    bell_index = 8 * np.exp(-t * 30)
    bell = np.sin(2 * np.pi * freq * t + bell_index * np.sin(2 * np.pi * freq * 3.5 * t))
    bell *= np.exp(-t * 20) * 0.3

    # Amplitude envelope
    amp = (1 - np.exp(-t * 80)) * np.exp(-t * 1.5)

    output = (carrier + harm2 + bell) * amp
    return output / np.max(np.abs(output))
```

## Bells

Inharmonic ratios create bell-like timbres:

```python
def fm_bell(freq: float, duration: float = 2.0) -> np.ndarray:
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Non-integer ratio for inharmonic spectrum
    ratio = 2.76  # Creates bell-like partials
    index = 8 * np.exp(-t * 3)

    modulator = np.sin(2 * np.pi * freq * ratio * t)
    carrier = np.sin(2 * np.pi * freq * t + index * modulator)

    # Long decay
    amp = np.exp(-t * 1.5)

    return carrier * amp
```

## Classic FM Recipes

| Sound | Ratio | Index | Index Decay | Character |
|-------|-------|-------|-------------|-----------|
| Electric Piano | 1:1 | 3-5 | Fast (6-10) | Bell-like attack, warm sustain |
| Bell | 1:1.4 or 1:2.76 | 5-10 | Medium (3-5) | Inharmonic, long decay |
| Brass | 1:1 | 6-12 | Slow (1-2) | Bright, brassy |
| Bass | 1:1 | 2-4 | Fast (8-15) | Punchy, defined |
| Glockenspiel | 1:3.5 | 4-6 | Medium (4-6) | Metallic, bright |
