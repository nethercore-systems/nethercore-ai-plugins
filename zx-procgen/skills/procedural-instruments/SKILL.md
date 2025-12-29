---
name: Procedural Instrument Synthesis
description: This skill should be used when the user asks to "generate instrument", "create instrument sample", "synthesize piano", "make guitar sound", "procedural instrument", "instrument sample", "realistic instrument", "high quality synth", "FM electric piano", "Karplus-Strong", "physical modeling instrument", "wavetable pad", "instrument for music", "better sounding instruments", "not chiptuney", "realistic samples", or mentions needing instrument samples for game music that sound better than basic oscillators. Provides production-quality instrument synthesis using advanced techniques.
version: 1.0.0
---

# Procedural Instrument Synthesis

Generate production-quality instrument samples that sound realistic and musical—not chiptuney. This skill covers advanced synthesis techniques implemented in NumPy/SciPy.

## Why Basic Synthesis Sounds Chiptuney

| Chiptuney Approach | Why It Sounds Bad |
|-------------------|-------------------|
| `np.sin(2*pi*f*t)` directly | Static timbre, no evolution |
| Simple ADSR on raw oscillator | Real instruments have complex envelopes per harmonic |
| Instant attack | Real instruments have attack transients with noise |
| Uniform decay | Real instruments have frequency-dependent decay |
| Single oscillator | Real instruments have multiple interacting components |

**Key insight:** Real instruments are physical systems with complex, evolving behavior. The sound changes throughout the note's duration.

## Quick Reference: Which Technique for Which Instrument

| Instrument | Primary Technique | Why |
|------------|------------------|-----|
| Acoustic Guitar | Karplus-Strong | Simulates plucked string physics |
| Electric Guitar | Karplus-Strong + distortion | String physics + amp modeling |
| Bass Guitar | Karplus-Strong (longer delay) | Lower frequencies need longer delay lines |
| Electric Piano | FM Synthesis | DX7 algorithm captures bell-like attack |
| Organ | Additive | Drawbar harmonics are literal additive synthesis |
| Strings/Pads | Wavetable | Evolving timbre from morphing waveforms |
| Brass | Subtractive + attack noise | Filtered saw with breath transient |
| Synth Lead | Subtractive/FM | Filter sweeps, modulation |
| Synth Bass | Subtractive | Heavy filtering, resonance |
| Bells | FM (inharmonic ratios) | Non-integer ratios create bell-like partials |

## Core Building Blocks

### 1. Multi-stage Envelopes

Real instruments don't follow simple ADSR. Use segment-based envelopes:

```python
def multi_envelope(t: np.ndarray, segments: list[tuple[float, float, str]]) -> np.ndarray:
    """
    Create complex envelope from segments.
    segments: [(duration, target_level, curve_type), ...]
    curve_type: 'linear', 'exp', 'log'
    """
    env = np.zeros_like(t)
    current_time = 0.0
    current_level = 0.0

    for duration, target, curve in segments:
        mask = (t >= current_time) & (t < current_time + duration)
        local_t = (t[mask] - current_time) / duration  # 0 to 1

        if curve == 'linear':
            env[mask] = current_level + (target - current_level) * local_t
        elif curve == 'exp':
            env[mask] = current_level + (target - current_level) * (1 - np.exp(-5 * local_t))
        elif curve == 'log':
            env[mask] = current_level + (target - current_level) * np.log1p(local_t * (np.e - 1))

        current_time += duration
        current_level = target

    # Sustain at final level
    env[t >= current_time] = current_level
    return env
```

### 2. Attack Transients

Add noise/inharmonic content at note start for realism:

```python
def attack_transient(t: np.ndarray, attack_duration: float = 0.02,
                     noise_amount: float = 0.3) -> np.ndarray:
    """Add noise burst at attack for realistic transient."""
    noise = np.random.randn(len(t)) * noise_amount
    attack_env = np.exp(-t / attack_duration * 10)
    return noise * attack_env
```

### 3. Vibrato and Expression

Natural pitch variation adds life:

```python
def apply_vibrato(phase: np.ndarray, t: np.ndarray,
                  rate: float = 5.0, depth: float = 0.02,
                  delay: float = 0.2) -> np.ndarray:
    """Apply delayed vibrato (musicians don't vibrato on attack)."""
    vibrato_env = np.clip((t - delay) / 0.1, 0, 1)  # Fade in after delay
    vibrato = np.sin(2 * np.pi * rate * t) * depth * vibrato_env
    return phase * (1 + vibrato)
```

## Technique 1: Karplus-Strong (Plucked Strings)

The most realistic way to synthesize plucked string instruments. Simulates a vibrating string using a delay line with filtering.

### How It Works

```
[Noise Burst] → [Delay Line] → [Low-pass Average] → Output
                     ↑__________________|
```

1. Fill delay line with random noise (the "pluck")
2. Each sample: output current, average with next, write back
3. Averaging acts as low-pass filter (high frequencies decay faster)
4. Delay length = sample_rate / frequency

### Implementation

```python
import numpy as np
import soundfile as sf

SAMPLE_RATE = 22050

def karplus_strong(freq: float, duration: float,
                   damping: float = 0.996,
                   brightness: float = 0.5) -> np.ndarray:
    """
    Generate plucked string sound using Karplus-Strong algorithm.

    Args:
        freq: Fundamental frequency in Hz
        duration: Note duration in seconds
        damping: Decay rate (0.99-0.999, higher = longer sustain)
        brightness: Initial noise filtering (0-1, higher = brighter pluck)
    """
    num_samples = int(SAMPLE_RATE * duration)
    delay_length = int(SAMPLE_RATE / freq)

    # Initialize delay line with filtered noise
    noise = np.random.randn(delay_length)
    if brightness < 1.0:
        # Low-pass filter the initial noise for softer attack
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


def generate_guitar_note(freq: float, duration: float = 1.0) -> np.ndarray:
    """Generate a realistic acoustic guitar note."""
    # Core plucked string
    string = karplus_strong(freq, duration, damping=0.996, brightness=0.7)

    # Add subtle body resonance (second harmonic emphasis)
    t = np.linspace(0, duration, len(string))
    body = np.sin(2 * np.pi * freq * 2 * t) * 0.1 * np.exp(-t * 3)

    # Combine
    output = string + body
    return output / np.max(np.abs(output))


# Generate and save
audio = generate_guitar_note(220.0, 2.0)  # A3
sf.write("guitar_a3.wav", audio, SAMPLE_RATE, subtype='PCM_16')
```

### Variations

| Parameter | Effect | Good For |
|-----------|--------|----------|
| damping=0.999 | Long sustain | Clean electric, harp |
| damping=0.990 | Quick decay | Muted guitar, pizzicato |
| brightness=0.3 | Soft, warm | Nylon guitar, upright bass |
| brightness=0.9 | Bright, snappy | Steel string, banjo |

See `examples/acoustic-guitar.py` for full implementation with body resonance.

## Technique 2: FM Synthesis (Keys, Bells)

Frequency Modulation creates complex, evolving timbres from simple sine waves. One oscillator (modulator) modulates another's frequency (carrier).

### Core Formula

```
output = sin(carrier_freq * t + index * sin(modulator_freq * t))
```

- **Carrier:Modulator ratio** determines harmonic content
- **Index** (modulation depth) determines brightness
- **Index envelope** creates timbral evolution

### Implementation

```python
def fm_synth(freq: float, duration: float,
             ratio: float = 1.0,
             index: float = 5.0,
             index_decay: float = 8.0) -> np.ndarray:
    """
    FM synthesis with decaying modulation index.

    Args:
        freq: Carrier frequency
        duration: Note duration
        ratio: Modulator/Carrier frequency ratio
        index: Peak modulation index (brightness)
        index_decay: How fast the brightness decays
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
    amp_env = np.exp(-t * 2) * (1 - np.exp(-t * 50))  # Quick attack, slow decay

    return carrier * amp_env


def electric_piano(freq: float, duration: float = 1.0) -> np.ndarray:
    """DX7-style electric piano (Rhodes-like)."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Two-operator FM: 1:1 ratio is classic EP
    index = 3.5 * np.exp(-t * 6)  # Decaying brightness
    modulator = np.sin(2 * np.pi * freq * t)
    carrier = np.sin(2 * np.pi * freq * t + index * modulator)

    # Add second harmonic for body
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

### Classic FM Recipes

| Sound | Ratio | Index | Index Decay | Character |
|-------|-------|-------|-------------|-----------|
| Electric Piano | 1:1 | 3-5 | Fast (6-10) | Bell-like attack, warm sustain |
| Bell | 1:1.4 or 1:2.76 | 5-10 | Medium (3-5) | Inharmonic, long decay |
| Brass | 1:1 | 6-12 | Slow (1-2) | Bright, brassy |
| Bass | 1:1 | 2-4 | Fast (8-15) | Punchy, defined |

See `examples/electric-piano.py` and `examples/fm-bell.py`.

## Technique 3: Wavetable (Pads, Evolving Sounds)

Cycle through pre-computed waveforms for evolving timbres. The timbre changes smoothly as you move through the table.

### Implementation

```python
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

        # Normalize each frame
        table[f] /= np.max(np.abs(table[f]) + 1e-10)

    return table


def wavetable_synth(freq: float, duration: float,
                    table: np.ndarray,
                    position_start: float = 0.0,
                    position_end: float = 0.5) -> np.ndarray:
    """
    Play through wavetable with position sweep.

    Args:
        position_start/end: 0.0-1.0, which frames to sweep through
    """
    num_samples = int(SAMPLE_RATE * duration)
    num_frames, frame_size = table.shape

    output = np.zeros(num_samples)
    phase = 0.0
    phase_inc = freq / SAMPLE_RATE

    for i in range(num_samples):
        # Position in wavetable (0 to 1)
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
    env = (1 - np.exp(-t * 5)) * np.exp(-t * 0.5)  # Slow attack, long decay

    return output * env


def strings_pad(freq: float, duration: float = 3.0) -> np.ndarray:
    """Create lush string pad sound."""
    table = create_wavetable()

    # Detuned unison for thickness
    output = np.zeros(int(SAMPLE_RATE * duration))
    detune_cents = [-8, -3, 0, 3, 8]  # Slight detuning

    for cents in detune_cents:
        detune_ratio = 2 ** (cents / 1200)
        voice = wavetable_synth(freq * detune_ratio, duration, table,
                               position_start=0.1, position_end=0.6)
        output[:len(voice)] += voice * 0.2

    return output / np.max(np.abs(output))
```

See `examples/strings-pad.py` for full implementation with chorus and filtering.

## Technique 4: Additive (Organs)

Build sounds by stacking sine waves at harmonic frequencies. Perfect for organs where drawbars literally control harmonic amplitudes.

### Implementation

```python
def additive_synth(freq: float, duration: float,
                   harmonics: dict[int, float]) -> np.ndarray:
    """
    Additive synthesis from harmonic specification.

    Args:
        harmonics: {harmonic_number: amplitude, ...}
                   e.g., {1: 1.0, 2: 0.5, 3: 0.25}
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    output = np.zeros_like(t)

    for harmonic, amp in harmonics.items():
        output += np.sin(2 * np.pi * freq * harmonic * t) * amp

    return output / np.max(np.abs(output) + 1e-10)


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
    # Drawbar harmonic ratios (based on pipe lengths)
    drawbar_harmonics = [0.5, 1.5, 1, 2, 3, 4, 5, 6, 8]

    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    output = np.zeros_like(t)

    for i, char in enumerate(drawbars):
        amp = int(char) / 8.0  # 0-8 maps to 0-1
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

See `examples/organ.py` for full implementation with Leslie speaker simulation.

## Technique 5: Subtractive (Synth Leads/Bass)

Start with harmonically rich waveform, filter away unwanted frequencies. The filter envelope is crucial for expression.

### Implementation

```python
from scipy.signal import butter, lfilter

def subtractive_synth(freq: float, duration: float,
                      waveform: str = 'saw',
                      cutoff_start: float = 4000,
                      cutoff_end: float = 800,
                      resonance: float = 2.0) -> np.ndarray:
    """
    Subtractive synthesis with filter envelope.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Oscillator
    if waveform == 'saw':
        osc = 2 * (freq * t % 1) - 1
    elif waveform == 'square':
        osc = np.sign(np.sin(2 * np.pi * freq * t))
    elif waveform == 'pulse':  # 25% duty cycle
        osc = np.where((freq * t % 1) < 0.25, 1.0, -1.0)
    else:
        osc = np.sin(2 * np.pi * freq * t)

    # Apply time-varying filter
    output = np.zeros_like(osc)
    chunk_size = SAMPLE_RATE // 50  # 20ms chunks

    for i in range(0, len(osc), chunk_size):
        chunk = osc[i:i + chunk_size]
        progress = i / len(osc)

        # Interpolate cutoff
        cutoff = cutoff_start + (cutoff_end - cutoff_start) * progress
        cutoff_norm = min(cutoff / (SAMPLE_RATE / 2), 0.99)

        # Apply filter
        b, a = butter(2, cutoff_norm, btype='low')
        output[i:i + len(chunk)] = lfilter(b, a, chunk)

    # Amplitude envelope
    amp = (1 - np.exp(-t * 30)) * np.exp(-t * 1)

    return output * amp


def synth_bass(freq: float, duration: float = 0.5) -> np.ndarray:
    """Classic subtractive synth bass."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Detuned saws for thickness
    saw1 = 2 * (freq * t % 1) - 1
    saw2 = 2 * (freq * 1.005 * t % 1) - 1  # Slight detune
    osc = (saw1 + saw2) * 0.5

    # Sub oscillator
    sub = np.sin(2 * np.pi * freq * 0.5 * t) * 0.5

    # Filter envelope: quick attack, medium decay
    cutoff_env = 1500 * np.exp(-t * 8) + 200

    output = np.zeros_like(osc)
    chunk_size = SAMPLE_RATE // 100

    for i in range(0, len(osc), chunk_size):
        chunk = osc[i:i + chunk_size]
        cutoff = cutoff_env[min(i, len(cutoff_env) - 1)]
        cutoff_norm = min(cutoff / (SAMPLE_RATE / 2), 0.99)
        b, a = butter(2, cutoff_norm, btype='low')
        output[i:i + len(chunk)] = lfilter(b, a, chunk)

    # Combine with sub
    output += sub

    # Punchy amplitude envelope
    amp = (1 - np.exp(-t * 100)) * np.exp(-t * 3)

    return output * amp / np.max(np.abs(output) + 1e-10)
```

See `examples/synth-bass.py` and `examples/brass-lead.py`.

## Quality Checklist

Before using a generated instrument, verify:

| Check | How to Test | Fix If Failing |
|-------|-------------|----------------|
| No clicks at start/end | Listen carefully | Add attack/release ramp |
| Pitch is correct | Tune against reference | Check frequency calculation |
| Timbre evolves | Should change over duration | Add envelope to filter/index |
| Attack has character | First 50ms should be distinct | Add transient noise |
| Sounds musical | Play in context with other sounds | Adjust envelopes, filtering |
| No aliasing | No harsh high frequencies | Add anti-aliasing filter |

## Integration with XM Tracker

Generated instruments become samples in your XM module:

1. Generate instrument samples at various pitches (or generate root pitch only)
2. Save as WAV to `assets/audio/`
3. Reference in `nether.toml`:
   ```toml
   [[assets.sounds]]
   id = "epiano"
   path = "assets/audio/epiano_c4.wav"
   ```
4. In XM tracker, name instrument "epiano" to match

For multi-sample instruments (like piano with samples at different octaves), generate samples at C2, C3, C4, C5 and use XM's sample mapping.

## Complete Recipes

See the `examples/` directory for full, production-ready implementations:

| File | Instrument | Technique |
|------|------------|-----------|
| `acoustic-guitar.py` | Acoustic guitar | Karplus-Strong + body resonance |
| `electric-piano.py` | Rhodes-style EP | FM synthesis |
| `fm-bell.py` | Tubular bell | FM with inharmonic ratio |
| `synth-bass.py` | Analog-style bass | Subtractive with filter env |
| `strings-pad.py` | String ensemble | Wavetable + unison detuning |
| `organ.py` | Hammond organ | Additive with drawbars |
| `brass-lead.py` | Brass section | Subtractive + breath noise |
| `pluck-synth.py` | Synth pluck | Karplus-Strong + filtering |

## Additional Resources

- `references/synthesis-implementations.md` — Detailed technique explanations
- `references/instrument-physics.md` — What makes each instrument unique
- `sound-design/skills/synthesis-techniques` — Conceptual overview
- `sound-design/skills/instrument-palettes` — Instrument categories
