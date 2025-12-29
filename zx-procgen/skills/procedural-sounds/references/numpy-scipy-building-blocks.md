# NumPy/SciPy Building Blocks Reference

Complete reference for audio synthesis functions using numpy, scipy.signal, and soundfile.

## Core Imports

```python
import numpy as np
import soundfile as sf
from scipy import signal
from scipy.ndimage import uniform_filter1d

SAMPLE_RATE = 22050  # ZX standard
```

## Oscillators (Sound Sources)

### Sine Wave
Pure tone oscillator - fundamental building block.

```python
def sine(freq, duration, sample_rate=SAMPLE_RATE):
    """Pure sine wave oscillator."""
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    return np.sin(2 * np.pi * freq * t)

# Usage
audio = sine(440, 1.0)  # 440 Hz for 1 second
```
- Best for: Bass, pure tones, sub layers, FM carriers

### Square Wave
Hollow, woody sound with odd harmonics only.

```python
def square(freq, duration, sample_rate=SAMPLE_RATE):
    """Square wave (odd harmonics only)."""
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    return np.sign(np.sin(2 * np.pi * freq * t))

# Antialiased version using additive synthesis
def square_aa(freq, duration, num_harmonics=20, sample_rate=SAMPLE_RATE):
    """Antialiased square wave via additive synthesis."""
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    audio = np.zeros_like(t)
    for n in range(1, num_harmonics + 1, 2):  # Odd harmonics only
        audio += np.sin(2 * np.pi * freq * n * t) / n
    return audio * (4 / np.pi)
```
- Best for: Retro/8-bit sounds, leads, hollow tones

### Sawtooth Wave
Bright, buzzy sound with all harmonics.

```python
def sawtooth(freq, duration, sample_rate=SAMPLE_RATE):
    """Sawtooth wave (all harmonics)."""
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    return 2 * (freq * t % 1) - 1

# Antialiased version
def sawtooth_aa(freq, duration, num_harmonics=20, sample_rate=SAMPLE_RATE):
    """Antialiased sawtooth via additive synthesis."""
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    audio = np.zeros_like(t)
    for n in range(1, num_harmonics + 1):
        audio += np.sin(2 * np.pi * freq * n * t) / n
    return audio * (2 / np.pi)
```
- Best for: Leads, pads, bass, rich sounds

### Triangle Wave
Soft, flute-like sound.

```python
def triangle(freq, duration, sample_rate=SAMPLE_RATE):
    """Triangle wave."""
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    return 2 * np.abs(2 * (freq * t % 1) - 1) - 1
```
- Best for: Soft leads, sub-bass, mellow sounds

### SuperSaw (Detuned Saws)
Multiple detuned sawtooth waves for rich, full sound.

```python
def supersaw(freq, duration, num_saws=7, detune=0.1, sample_rate=SAMPLE_RATE):
    """Multiple detuned saws for thick sound."""
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    audio = np.zeros_like(t)

    # Spread detune across saws
    detune_spread = np.linspace(-detune, detune, num_saws)

    for d in detune_spread:
        f = freq * (1 + d)
        audio += 2 * (f * t % 1) - 1

    return audio / num_saws
```
- Best for: Trance leads, lasers, big synth sounds

### Noise Sources

```python
def white_noise(duration, sample_rate=SAMPLE_RATE):
    """White noise - all frequencies equal."""
    return np.random.randn(int(sample_rate * duration)).astype(np.float32)

def pink_noise(duration, sample_rate=SAMPLE_RATE):
    """Pink noise - natural 1/f rolloff."""
    num_samples = int(sample_rate * duration)
    white = np.random.randn(num_samples)

    # Apply 1/f spectral shaping via FFT
    fft = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(num_samples)
    freqs[0] = 1  # Avoid division by zero
    fft = fft / np.sqrt(freqs)
    return np.fft.irfft(fft, num_samples).astype(np.float32)

def brown_noise(duration, sample_rate=SAMPLE_RATE):
    """Brown noise - steep 1/f^2 rolloff (Brownian motion)."""
    white = np.random.randn(int(sample_rate * duration))
    brown = np.cumsum(white)
    # Normalize to prevent drift
    brown = brown - np.mean(brown)
    return (brown / np.max(np.abs(brown))).astype(np.float32)
```

| Type | Character | Best For |
|------|-----------|----------|
| White | Harsh, bright | Hi-hats, impacts, transients |
| Pink | Natural, warm | Explosions, wind, realistic noise |
| Brown | Deep, rumbly | Thunder, bass layers, rumble |

## Envelopes

### ADSR Envelope
Classic attack-decay-sustain-release envelope.

```python
def adsr(duration, attack=0.01, decay=0.1, sustain=0.5, release=0.2,
         sample_rate=SAMPLE_RATE):
    """Generate ADSR envelope."""
    num_samples = int(sample_rate * duration)
    env = np.zeros(num_samples, dtype=np.float32)

    attack_samples = int(attack * sample_rate)
    decay_samples = int(decay * sample_rate)
    release_samples = int(release * sample_rate)
    sustain_samples = num_samples - attack_samples - decay_samples - release_samples

    if sustain_samples < 0:
        sustain_samples = 0

    idx = 0

    # Attack
    if attack_samples > 0:
        env[idx:idx + attack_samples] = np.linspace(0, 1, attack_samples)
        idx += attack_samples

    # Decay
    if decay_samples > 0 and idx < num_samples:
        end_idx = min(idx + decay_samples, num_samples)
        env[idx:end_idx] = np.linspace(1, sustain, end_idx - idx)
        idx = end_idx

    # Sustain
    if sustain_samples > 0 and idx < num_samples:
        end_idx = min(idx + sustain_samples, num_samples)
        env[idx:end_idx] = sustain
        idx = end_idx

    # Release
    if idx < num_samples:
        env[idx:] = np.linspace(sustain, 0, num_samples - idx)

    return env
```

### Exponential Decay
Natural-sounding decay for percussive sounds.

```python
def exp_decay(duration, decay_rate=10, sample_rate=SAMPLE_RATE):
    """Exponential decay envelope."""
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    return np.exp(-t * decay_rate)
```

### Linear Segments
Custom envelope shapes via linear interpolation.

```python
def linseg(points, sample_rate=SAMPLE_RATE):
    """
    Linear segment envelope from control points.

    Args:
        points: List of (time, value) tuples, e.g., [(0, 0), (0.1, 1), (0.5, 0.3), (1, 0)]
    """
    total_duration = points[-1][0]
    num_samples = int(sample_rate * total_duration)
    times = np.array([p[0] for p in points])
    values = np.array([p[1] for p in points])

    t = np.linspace(0, total_duration, num_samples, dtype=np.float32)
    return np.interp(t, times, values).astype(np.float32)

# Usage: frequency sweep from 1000Hz to 200Hz
freq_sweep = linseg([(0, 1000), (0.5, 200)])
```

### Exponential Segments
More natural-sounding curves.

```python
def expseg(points, sample_rate=SAMPLE_RATE):
    """
    Exponential segment envelope from control points.

    Args:
        points: List of (time, value) tuples
    """
    total_duration = points[-1][0]
    num_samples = int(sample_rate * total_duration)
    env = np.zeros(num_samples, dtype=np.float32)

    for i in range(len(points) - 1):
        t0, v0 = points[i]
        t1, v1 = points[i + 1]

        start_idx = int(t0 * sample_rate)
        end_idx = int(t1 * sample_rate)

        if v0 <= 0: v0 = 0.001  # Avoid log(0)
        if v1 <= 0: v1 = 0.001

        t_seg = np.linspace(0, 1, end_idx - start_idx)
        # Exponential interpolation
        env[start_idx:end_idx] = v0 * (v1 / v0) ** t_seg

    return env
```

## Filters

### Butterworth Filters
Clean, precise filtering using scipy.signal.

```python
def lowpass(audio, cutoff, order=2, sample_rate=SAMPLE_RATE):
    """Butterworth lowpass filter."""
    nyquist = sample_rate / 2
    normalized_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normalized_cutoff, btype='low')
    return signal.filtfilt(b, a, audio).astype(np.float32)

def highpass(audio, cutoff, order=2, sample_rate=SAMPLE_RATE):
    """Butterworth highpass filter."""
    nyquist = sample_rate / 2
    normalized_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normalized_cutoff, btype='high')
    return signal.filtfilt(b, a, audio).astype(np.float32)

def bandpass(audio, low_cutoff, high_cutoff, order=2, sample_rate=SAMPLE_RATE):
    """Butterworth bandpass filter."""
    nyquist = sample_rate / 2
    low = low_cutoff / nyquist
    high = high_cutoff / nyquist
    b, a = signal.butter(order, [low, high], btype='band')
    return signal.filtfilt(b, a, audio).astype(np.float32)
```

### Resonant Filter (Moog-style approximation)
For classic synth filtering with resonance.

```python
def resonant_lowpass(audio, cutoff, resonance=0.5, sample_rate=SAMPLE_RATE):
    """
    Resonant lowpass filter approximation.

    Args:
        cutoff: Cutoff frequency in Hz
        resonance: Resonance amount 0-1 (self-oscillates near 1)
    """
    nyquist = sample_rate / 2
    normalized_cutoff = min(cutoff / nyquist, 0.99)

    # Use higher order for resonance approximation
    q = 0.707 + resonance * 10  # Q factor from resonance
    sos = signal.butter(4, normalized_cutoff, btype='low', output='sos')

    # Apply filter
    filtered = signal.sosfilt(sos, audio)

    # Add resonance peak via bandpass boost
    if resonance > 0:
        bp_low = max(0.01, normalized_cutoff * 0.9)
        bp_high = min(0.99, normalized_cutoff * 1.1)
        sos_bp = signal.butter(2, [bp_low, bp_high], btype='band', output='sos')
        peak = signal.sosfilt(sos_bp, audio)
        filtered = filtered + peak * resonance * 2

    return filtered.astype(np.float32)
```

### Time-Varying Filter
For filter sweeps (common in SFX).

```python
def filter_sweep(audio, start_cutoff, end_cutoff, sample_rate=SAMPLE_RATE):
    """
    Apply time-varying lowpass filter (cutoff sweep).
    """
    num_samples = len(audio)
    output = np.zeros_like(audio)

    # Process in chunks with varying cutoff
    chunk_size = 512
    cutoffs = np.linspace(start_cutoff, end_cutoff, num_samples // chunk_size + 1)

    for i, cutoff in enumerate(cutoffs):
        start = i * chunk_size
        end = min(start + chunk_size, num_samples)
        if start >= num_samples:
            break

        nyquist = sample_rate / 2
        norm_cutoff = max(0.01, min(cutoff / nyquist, 0.99))
        b, a = signal.butter(2, norm_cutoff, btype='low')
        output[start:end] = signal.lfilter(b, a, audio[start:end])

    return output.astype(np.float32)
```

## FM Synthesis

### Basic FM
Classic two-operator FM synthesis.

```python
def fm_synth(carrier_freq, duration, ratio=2.0, index=5.0, sample_rate=SAMPLE_RATE):
    """
    FM synthesis.

    Args:
        carrier_freq: Carrier frequency in Hz
        ratio: Modulator/carrier frequency ratio
        index: Modulation index (higher = more harmonics)
    """
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    mod_freq = carrier_freq * ratio

    # Modulator
    modulator = np.sin(2 * np.pi * mod_freq * t)

    # Carrier (frequency modulated)
    carrier = np.sin(2 * np.pi * carrier_freq * t + index * modulator)

    return carrier
```

Common ratios:
- `1:1` — Warm, slightly metallic
- `2:1` — Octave harmonics
- `3:1` — Hollow, clarinet-like
- `1.414:1` — Bell-like, inharmonic

### FM with Envelope on Index
For dynamic timbre changes.

```python
def fm_synth_env(carrier_freq, duration, ratio=2.0, index=5.0,
                 index_env=None, sample_rate=SAMPLE_RATE):
    """FM synthesis with time-varying modulation index."""
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    mod_freq = carrier_freq * ratio

    if index_env is None:
        index_env = exp_decay(duration, decay_rate=5, sample_rate=sample_rate)

    modulator = np.sin(2 * np.pi * mod_freq * t)
    carrier = np.sin(2 * np.pi * carrier_freq * t + index * index_env * modulator)

    return carrier
```

## Effects

### Simple Delay
Single delay with feedback.

```python
def delay(audio, delay_time=0.25, feedback=0.5, mix=0.3, sample_rate=SAMPLE_RATE):
    """Simple delay effect."""
    delay_samples = int(delay_time * sample_rate)
    output = np.copy(audio)

    for i in range(delay_samples, len(audio)):
        output[i] += audio[i - delay_samples] * feedback

    return (audio * (1 - mix) + output * mix).astype(np.float32)
```

### Simple Reverb (Schroeder)
Basic algorithmic reverb using comb and allpass filters.

```python
def reverb(audio, room_size=0.8, damping=0.5, mix=0.3, sample_rate=SAMPLE_RATE):
    """
    Simple Schroeder reverb approximation.
    """
    # Comb filter delays (in samples)
    comb_delays = [int(d * sample_rate) for d in [0.0297, 0.0371, 0.0411, 0.0437]]

    # Allpass delays
    ap_delays = [int(d * sample_rate) for d in [0.09, 0.011]]

    output = np.zeros(len(audio) + max(comb_delays) + max(ap_delays))

    # Parallel comb filters
    for delay in comb_delays:
        comb_out = np.zeros_like(output)
        feedback = room_size * 0.9

        for i in range(delay, len(audio)):
            comb_out[i] = audio[i] + comb_out[i - delay] * feedback * (1 - damping)

        output += comb_out

    output /= len(comb_delays)

    # Series allpass filters
    for delay in ap_delays:
        allpass_out = np.zeros_like(output)
        g = 0.7

        for i in range(delay, len(output)):
            allpass_out[i] = -g * output[i] + output[i - delay] + g * allpass_out[i - delay]

        output = allpass_out

    # Trim to original length and mix
    output = output[:len(audio)]
    return (audio * (1 - mix) + output * mix).astype(np.float32)
```

### Distortion
Waveshaping distortion.

```python
def distortion(audio, drive=0.7):
    """
    Soft-clipping distortion.

    Args:
        drive: Distortion amount 0-1
    """
    gain = 1 + drive * 10
    return np.tanh(audio * gain).astype(np.float32)

def hard_clip(audio, threshold=0.9):
    """Hard clipping/limiting."""
    return np.clip(audio, -threshold, threshold).astype(np.float32)
```

### Compression
Dynamic range compression.

```python
def compress(audio, threshold=-20, ratio=4, attack=0.01, release=0.1,
             sample_rate=SAMPLE_RATE):
    """
    Simple dynamic range compressor.
    """
    threshold_linear = 10 ** (threshold / 20)

    # Envelope follower
    envelope = np.abs(audio)
    attack_samples = int(attack * sample_rate)
    release_samples = int(release * sample_rate)

    smoothed = np.zeros_like(envelope)
    smoothed[0] = envelope[0]

    for i in range(1, len(envelope)):
        if envelope[i] > smoothed[i-1]:
            coef = 1 - np.exp(-1 / attack_samples)
        else:
            coef = 1 - np.exp(-1 / release_samples)
        smoothed[i] = smoothed[i-1] + coef * (envelope[i] - smoothed[i-1])

    # Gain reduction
    gain = np.ones_like(smoothed)
    above_threshold = smoothed > threshold_linear
    gain[above_threshold] = (threshold_linear +
                             (smoothed[above_threshold] - threshold_linear) / ratio) / smoothed[above_threshold]

    return (audio * gain).astype(np.float32)
```

## Utilities

### Mix Multiple Signals
```python
def mix(signals, gains=None):
    """Mix multiple audio signals."""
    if gains is None:
        gains = [1.0] * len(signals)

    max_len = max(len(s) for s in signals)
    output = np.zeros(max_len, dtype=np.float32)

    for sig, gain in zip(signals, gains):
        output[:len(sig)] += sig * gain

    return output
```

### Normalize
```python
def normalize(audio, peak=0.9):
    """Normalize audio to peak level."""
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        return (audio / max_val * peak).astype(np.float32)
    return audio
```

### Frequency Sweep
```python
def freq_sweep(start_freq, end_freq, duration, sample_rate=SAMPLE_RATE):
    """
    Generate oscillator with frequency sweep.
    Returns audio with frequency changing from start to end.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    freq = np.linspace(start_freq, end_freq, len(t))

    # Integrate frequency to get phase
    phase = np.cumsum(2 * np.pi * freq / sample_rate)
    return np.sin(phase).astype(np.float32)
```

### Karplus-Strong (Plucked String)
```python
def karplus_strong(freq, duration, damping=0.99, sample_rate=SAMPLE_RATE):
    """
    Karplus-Strong plucked string synthesis.
    """
    delay_length = int(sample_rate / freq)
    num_samples = int(sample_rate * duration)

    # Initialize delay line with noise
    delay_line = np.random.randn(delay_length).astype(np.float32)
    output = np.zeros(num_samples, dtype=np.float32)

    for i in range(num_samples):
        output[i] = delay_line[i % delay_length]
        # Average adjacent samples (lowpass = damping)
        next_idx = (i + 1) % delay_length
        delay_line[i % delay_length] = (delay_line[i % delay_length] +
                                        delay_line[next_idx]) * 0.5 * damping

    return output
```

## Signal Math Examples

```python
# Combine signals (additive)
combined = osc1 + osc2

# Scale amplitude
quieter = audio * 0.5

# Apply envelope
shaped = audio * envelope

# Frequency modulation
vibrato_lfo = sine(5, duration) * 10  # 5 Hz vibrato, 10 Hz depth
modulated_freq = 440 + vibrato_lfo
# Then use modulated_freq in freq_sweep or similar

# Ring modulation
ring_mod = audio * sine(200, len(audio) / SAMPLE_RATE)
```

## Common Patterns

### Subtractive Synthesis
```python
def subtractive_bass(freq, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    osc = sawtooth_aa(freq, duration)
    env = adsr(duration, attack=0.01, decay=0.2, sustain=0.3, release=0.1)
    filtered = resonant_lowpass(osc, 800, resonance=0.4)
    return filtered * env
```

### FM Bell
```python
def fm_bell(freq, duration):
    audio = fm_synth_env(freq, duration, ratio=1.414, index=8)
    env = adsr(duration, attack=0.001, decay=0.5, sustain=0, release=0.3)
    return audio * env
```

### Layered Sound
```python
def layered_explosion(duration):
    # Body layer (low rumble)
    body = brown_noise(duration)
    body = lowpass(body, 200)
    body_env = exp_decay(duration, decay_rate=2)

    # Texture layer (crackle)
    texture = pink_noise(duration)
    texture = bandpass(texture, 500, 2000)
    texture_env = exp_decay(duration, decay_rate=5)

    # High sizzle
    sizzle = white_noise(duration)
    sizzle = highpass(sizzle, 3000)
    sizzle_env = exp_decay(duration, decay_rate=8)

    return mix([body * body_env, texture * texture_env * 0.5, sizzle * sizzle_env * 0.3])
```
