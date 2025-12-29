# Synthesis Technique Implementations

Detailed NumPy/SciPy implementations for each synthesis technique.

## Karplus-Strong (Physical Modeling)

The most realistic approach for plucked/struck strings.

### Algorithm

```
1. Create delay line of length: sample_rate / frequency
2. Fill delay line with filtered noise (the "pluck")
3. For each output sample:
   a. Output current delay line value
   b. Average with next value (low-pass filtering)
   c. Apply damping factor
   d. Write back to delay line
   e. Advance index
```

### Key Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| damping | 0.990-0.999 | Decay rate (higher = longer sustain) |
| brightness | 0.0-1.0 | Initial noise filtering (lower = warmer) |
| stretch | 0.5-2.0 | Inharmonicity (for stiff strings) |

### Extended Karplus-Strong

For piano-like inharmonicity:

```python
def extended_ks(freq: float, duration: float,
                stiffness: float = 0.0) -> np.ndarray:
    """
    Extended Karplus-Strong with string stiffness.

    Stiffness causes higher harmonics to be slightly sharp,
    creating the characteristic piano "stretch".
    """
    # Basic implementation + all-pass filter for stiffness
    delay_length = int(SAMPLE_RATE / freq)

    # All-pass filter coefficient based on stiffness
    c = stiffness * 0.5

    # ... (filter each sample through all-pass)
```

### Variations by Instrument

| Instrument | Damping | Brightness | Notes |
|------------|---------|------------|-------|
| Nylon guitar | 0.994 | 0.45 | Warm, quick decay |
| Steel guitar | 0.996 | 0.75 | Bright, medium sustain |
| Electric bass | 0.997 | 0.60 | Long sustain, round |
| Harp | 0.998 | 0.55 | Very long, ethereal |
| Harpsichord | 0.993 | 0.85 | Bright, quick decay |
| Banjo | 0.992 | 0.90 | Very bright, short |

---

## FM Synthesis

Creates complex timbres from simple oscillators through frequency modulation.

### Core Implementation

```python
def fm_2op(freq: float, duration: float,
           ratio: float, index: float,
           index_env: np.ndarray) -> np.ndarray:
    """
    Two-operator FM synthesis.

    Output = sin(carrier_freq * t + index * sin(modulator_freq * t))

    Args:
        ratio: modulator_freq / carrier_freq
        index: modulation depth (affects brightness)
        index_env: envelope for index (creates timbral evolution)
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    mod_freq = freq * ratio
    modulator = np.sin(2 * np.pi * mod_freq * t)
    carrier = np.sin(2 * np.pi * freq * t + index * index_env * modulator)

    return carrier
```

### Multi-Operator Algorithms

DX7-style algorithms with 6 operators:

```
Algorithm 1: Stack
[6] → [5] → [4] → [3] → [2] → [1] → Out

Algorithm 5: Parallel pairs
[6] → [5] ─┐
[4] → [3] ─┼→ Out
[2] → [1] ─┘

Algorithm 32: All parallel (additive)
[6] ─┐
[5] ─┤
[4] ─┤
[3] ─┼→ Out
[2] ─┤
[1] ─┘
```

### Ratio Guidelines

| Ratio | Sound Character | Use For |
|-------|----------------|---------|
| 1:1 | Harmonic, warm | Electric piano, bass |
| 1:2 | Hollow, clarinet-like | Woodwinds |
| 1:3 | Bright, reedy | Brass, leads |
| 1:1.41 | Metallic, inharmonic | Bells, gongs |
| 1:2.76 | Bell-like | Tubular bells |
| 1:3.5 | Harsh metallic | Aggressive sounds |

### Index Guidelines

| Index Range | Character |
|-------------|-----------|
| 0-1 | Subtle modulation, near sine |
| 2-4 | Clear harmonics, musical |
| 5-8 | Bright, metallic |
| 9+ | Harsh, complex |

---

## Wavetable Synthesis

Morph between waveforms for evolving timbres.

### Creating Wavetables

```python
def create_wavetable_pwm() -> np.ndarray:
    """Create pulse width modulation wavetable."""
    frames = 64
    frame_size = 2048
    table = np.zeros((frames, frame_size))

    for f in range(frames):
        duty = 0.1 + 0.8 * (f / (frames - 1))  # 10% to 90%
        t = np.linspace(0, 1, frame_size, endpoint=False)
        table[f] = np.where(t < duty, 1.0, -1.0)

    return table


def create_wavetable_harmonic() -> np.ndarray:
    """Create harmonic addition wavetable (sine to saw)."""
    frames = 64
    frame_size = 2048
    table = np.zeros((frames, frame_size))

    for f in range(frames):
        num_harmonics = 1 + int(f / frames * 20)
        t = np.linspace(0, 1, frame_size, endpoint=False)

        for h in range(1, num_harmonics + 1):
            table[f] += np.sin(2 * np.pi * h * t) / h

    return table
```

### Interpolation

For smooth playback, interpolate:
1. Between frames (timbre morphing)
2. Between samples within frame (pitch accuracy)

```python
# Bilinear interpolation for quality
def read_wavetable(table, phase, position):
    num_frames, frame_size = table.shape

    # Frame interpolation
    frame_f = position * (num_frames - 1)
    frame_a, frame_b = int(frame_f), min(int(frame_f) + 1, num_frames - 1)
    frame_blend = frame_f - frame_a

    # Sample interpolation
    idx_f = phase * frame_size
    idx_a, idx_b = int(idx_f) % frame_size, (int(idx_f) + 1) % frame_size
    sample_blend = idx_f - int(idx_f)

    # Bilinear
    v00 = table[frame_a, idx_a]
    v01 = table[frame_a, idx_b]
    v10 = table[frame_b, idx_a]
    v11 = table[frame_b, idx_b]

    top = v00 * (1 - sample_blend) + v01 * sample_blend
    bottom = v10 * (1 - sample_blend) + v11 * sample_blend

    return top * (1 - frame_blend) + bottom * frame_blend
```

---

## Additive Synthesis

Build sounds by summing harmonics.

### Implementation

```python
def additive(freq: float, duration: float,
             partials: list[tuple[float, float, float]]) -> np.ndarray:
    """
    Additive synthesis with per-partial envelopes.

    Args:
        partials: [(ratio, amplitude, decay_rate), ...]
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    output = np.zeros_like(t)

    for ratio, amp, decay in partials:
        partial_freq = freq * ratio
        if partial_freq < SAMPLE_RATE / 2:  # Anti-aliasing
            partial_env = np.exp(-t * decay)
            output += np.sin(2 * np.pi * partial_freq * t) * amp * partial_env

    return output
```

### Instrument Partial Recipes

**Clarinet** (odd harmonics):
```python
partials = [(1, 1.0, 1), (3, 0.75, 1.2), (5, 0.5, 1.5),
            (7, 0.25, 2), (9, 0.1, 2.5)]
```

**Trumpet** (all harmonics, emphasis on 2-4):
```python
partials = [(1, 1.0, 0.8), (2, 0.6, 1), (3, 0.8, 1.2),
            (4, 0.4, 1.5), (5, 0.5, 1.8), (6, 0.3, 2)]
```

**Flute** (mostly fundamental):
```python
partials = [(1, 1.0, 0.5), (2, 0.1, 1), (3, 0.05, 1.5)]
```

---

## Subtractive Synthesis

Filter harmonically rich oscillators.

### Time-Varying Filter

```python
def subtractive_with_env(osc: np.ndarray,
                         cutoff_env: np.ndarray,
                         resonance: float = 1.0) -> np.ndarray:
    """
    Apply time-varying lowpass filter.

    Process in small chunks for smooth cutoff changes.
    """
    chunk_size = SAMPLE_RATE // 100  # 10ms chunks
    output = np.zeros_like(osc)

    for i in range(0, len(osc), chunk_size):
        chunk = osc[i:i + chunk_size]
        cutoff = cutoff_env[min(i + chunk_size // 2, len(cutoff_env) - 1)]
        cutoff_norm = np.clip(cutoff / (SAMPLE_RATE / 2), 0.01, 0.99)

        b, a = butter(2, cutoff_norm, btype='low')
        output[i:i + len(chunk)] = lfilter(b, a, chunk)

    return output
```

### Common Filter Envelopes

```python
# Pluck: fast attack, medium decay
cutoff_env = 3000 * np.exp(-t * 8) + 200

# Pad: slow sweep
cutoff_env = 500 + 2000 * (1 - np.exp(-t * 0.5))

# Acid: slow attack, resonant
cutoff_env = 200 + 2000 * np.sin(2 * np.pi * 0.5 * t) ** 2
```

---

## Common Building Blocks

### ADSR Envelope

```python
def adsr(t: np.ndarray, duration: float,
         attack: float, decay: float,
         sustain: float, release: float) -> np.ndarray:
    """Standard ADSR envelope."""
    env = np.zeros_like(t)

    # Attack
    mask = t < attack
    env[mask] = t[mask] / attack

    # Decay
    mask = (t >= attack) & (t < attack + decay)
    env[mask] = 1 - (1 - sustain) * (t[mask] - attack) / decay

    # Sustain
    release_start = duration - release
    mask = (t >= attack + decay) & (t < release_start)
    env[mask] = sustain

    # Release
    mask = t >= release_start
    env[mask] = sustain * (1 - (t[mask] - release_start) / release)

    return np.clip(env, 0, 1)
```

### Band-Limited Oscillators

```python
def saw_bl(freq: float, t: np.ndarray) -> np.ndarray:
    """Band-limited sawtooth via additive synthesis."""
    output = np.zeros_like(t)
    num_harmonics = int(SAMPLE_RATE / 2 / freq)

    for h in range(1, min(num_harmonics, 30) + 1):
        output += np.sin(2 * np.pi * freq * h * t) / h

    return output * 2 / np.pi


def square_bl(freq: float, t: np.ndarray) -> np.ndarray:
    """Band-limited square via odd harmonics."""
    output = np.zeros_like(t)
    num_harmonics = int(SAMPLE_RATE / 2 / freq)

    for h in range(1, min(num_harmonics, 30) + 1, 2):  # Odd only
        output += np.sin(2 * np.pi * freq * h * t) / h

    return output * 4 / np.pi
```

### Anti-Aliasing

Always check harmonics against Nyquist:

```python
nyquist = SAMPLE_RATE / 2
if freq * harmonic_number < nyquist:
    # Safe to add this harmonic
    output += np.sin(2 * np.pi * freq * harmonic_number * t) * amp
```
