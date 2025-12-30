# Additive Synthesis

Build sounds by stacking sine waves at harmonic frequencies.

## Basic Additive

```python
SAMPLE_RATE = 22050

def additive_synth(freq: float, duration: float,
                   harmonics: dict[int, float]) -> np.ndarray:
    """
    Additive synthesis from harmonic specification.

    Args:
        harmonics: {harmonic_number: amplitude, ...}
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    output = np.zeros_like(t)

    for harmonic, amp in harmonics.items():
        output += np.sin(2 * np.pi * freq * harmonic * t) * amp

    return output / np.max(np.abs(output) + 1e-10)
```

## Hammond Organ with Drawbars

```python
def drawbar_organ(freq: float, duration: float = 1.0,
                  drawbars: str = "888000000") -> np.ndarray:
    """
    Hammond-style organ with drawbar settings.

    Drawbars: 9 digits (0-8) for:
    16', 5-1/3', 8', 4', 2-2/3', 2', 1-3/5', 1-1/3', 1'

    Common settings:
    - "888000000" - Full bass
    - "888888888" - Full organ
    - "800000888" - Jazz
    - "888800000" - Gospel
    """
    drawbar_harmonics = [0.5, 1.5, 1, 2, 3, 4, 5, 6, 8]

    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    output = np.zeros_like(t)

    for i, char in enumerate(drawbars):
        amp = int(char) / 8.0
        if amp > 0:
            harm_freq = freq * drawbar_harmonics[i]
            output += np.sin(2 * np.pi * harm_freq * t) * amp

    # Key click (characteristic Hammond sound)
    click = np.random.randn(int(SAMPLE_RATE * 0.01)) * 0.3
    click *= np.linspace(1, 0, len(click))
    output[:len(click)] += click

    # Simple envelope
    env = (1 - np.exp(-t * 50)) * np.exp(-t * 0.1)
    output *= env

    return output / np.max(np.abs(output))
```

## Common Drawbar Settings

| Setting | Name | Character |
|---------|------|-----------|
| 888000000 | Full bass | Rich low end |
| 888888888 | Full organ | All harmonics |
| 800000888 | Jazz | Mellow with highs |
| 888800000 | Gospel | Classic church |
| 806000000 | Blues | Hollow, vocal |
| 008800000 | Flute | Pure, simple |
| 000006000 | Clarinet | Odd harmonics only |

## Drawbar Harmonic Ratios

| Drawbar | Pipe | Harmonic | Note Interval |
|---------|------|----------|---------------|
| 1 | 16' | 0.5 | Sub-octave |
| 2 | 5-1/3' | 1.5 | Fifth above sub |
| 3 | 8' | 1 | Fundamental |
| 4 | 4' | 2 | Octave |
| 5 | 2-2/3' | 3 | Twelfth |
| 6 | 2' | 4 | Double octave |
| 7 | 1-3/5' | 5 | 17th |
| 8 | 1-1/3' | 6 | 19th |
| 9 | 1' | 8 | Triple octave |
