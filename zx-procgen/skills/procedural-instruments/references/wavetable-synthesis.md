# Wavetable Synthesis

Cycle through pre-computed waveforms for evolving timbres.

## Creating a Wavetable

```python
SAMPLE_RATE = 22050

def create_wavetable(num_frames: int = 64, frame_size: int = 2048) -> np.ndarray:
    """Create wavetable morphing from sine to saw."""
    table = np.zeros((num_frames, frame_size))

    for f in range(num_frames):
        t = np.linspace(0, 1, frame_size, endpoint=False)
        # Morph: add more harmonics as frame increases
        num_harmonics = 1 + int(f / num_frames * 15)
        for h in range(1, num_harmonics + 1):
            amp = 1.0 / h  # Saw-like harmonic structure
            table[f] += np.sin(2 * np.pi * h * t) * amp

        table[f] /= np.max(np.abs(table[f]) + 1e-10)

    return table
```

## Playing the Wavetable

```python
def wavetable_synth(freq: float, duration: float,
                    table: np.ndarray,
                    position_start: float = 0.0,
                    position_end: float = 0.5) -> np.ndarray:
    """
    Play through wavetable with position sweep.

    Args:
        position_start/end: 0.0-1.0, frames to sweep through
    """
    num_samples = int(SAMPLE_RATE * duration)
    num_frames, frame_size = table.shape

    output = np.zeros(num_samples)
    phase = 0.0
    phase_inc = freq / SAMPLE_RATE

    for i in range(num_samples):
        pos = position_start + (position_end - position_start) * (i / num_samples)

        # Interpolate between frames
        frame_f = pos * (num_frames - 1)
        frame_a = int(frame_f)
        frame_b = min(frame_a + 1, num_frames - 1)
        blend = frame_f - frame_a

        # Read from wavetable
        idx = int(phase * frame_size) % frame_size
        sample_a = table[frame_a, idx]
        sample_b = table[frame_b, idx]

        output[i] = sample_a * (1 - blend) + sample_b * blend

        phase += phase_inc
        if phase >= 1.0:
            phase -= 1.0

    # Apply envelope
    t = np.linspace(0, duration, num_samples)
    env = (1 - np.exp(-t * 5)) * np.exp(-t * 0.5)

    return output * env
```

## String Pad

Lush strings using wavetable + detuned unison:

```python
def strings_pad(freq: float, duration: float = 3.0) -> np.ndarray:
    """Create lush string pad sound."""
    table = create_wavetable()

    # Detuned unison for thickness
    output = np.zeros(int(SAMPLE_RATE * duration))
    detune_cents = [-8, -3, 0, 3, 8]

    for cents in detune_cents:
        detune_ratio = 2 ** (cents / 1200)
        voice = wavetable_synth(freq * detune_ratio, duration, table,
                               position_start=0.1, position_end=0.6)
        output[:len(voice)] += voice * 0.2

    return output / np.max(np.abs(output))
```

## Wavetable Variations

| Position Sweep | Character |
|----------------|-----------|
| 0.0 → 0.2 | Subtle evolution, mostly sine |
| 0.0 → 0.5 | Moderate evolution, sine to partial saw |
| 0.0 → 1.0 | Full sweep, dramatic brightening |
| 0.5 → 0.5 | Static, no evolution |
| 0.8 → 0.3 | Reverse sweep, starts bright |
