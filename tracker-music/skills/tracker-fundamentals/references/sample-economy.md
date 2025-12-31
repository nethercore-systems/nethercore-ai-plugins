# Sample Economy Reference

Techniques for maximum musical impact with minimum sample data.

## Core Principles

### 1. Loop Points Extend Everything

A 0.1s sample with a good loop point can sustain forever:

```python
# Short attack + looped sustain
sample = ItSample(
    name="pad",
    c5_speed=22050,
    flags=SAMPLE_LOOP,
    loop_begin=2205,      # After 0.1s attack
    loop_end=4410,        # 0.1s loop region
)
# Result: 0.2s of audio sustains infinitely
```

**Best loop regions:**
- Zero crossings (where waveform crosses 0)
- Complete wave cycles
- Avoid transients/attacks

### 2. Pitch-Shift Reuse

One sample, multiple notes:

| Original | Usable Range | Quality |
|----------|--------------|---------|
| C-4 sample | A-3 to E-4 | Excellent |
| C-4 sample | F-3 to A-4 | Good |
| C-4 sample | C-3 to C-5 | Noticeable artifacts |

**Rule of thumb:** ±5 semitones sounds natural, ±7 is acceptable, beyond that record new samples.

### 3. Multi-Sample Zones (IT Only)

Map different samples to different ranges:

```python
# Piano with 3 samples covering full range
instr = ItInstrument(name="Piano")
# Notes 0-39: Low sample (recorded at C-2)
# Notes 40-79: Mid sample (recorded at C-4)
# Notes 80-119: High sample (recorded at C-6)
```

### 4. Shared Samples

Same sample, different instruments:

```python
# One saw wave sample
saw_sample = generate_saw_wave()

# Used as bass (low octave)
bass_instr = ItInstrument(name="bass", sample_relative_note=-24)

# Used as lead (original octave)
lead_instr = ItInstrument(name="lead", sample_relative_note=0)

# Used as pad (with long attack envelope)
pad_instr = ItInstrument(name="pad", sample_relative_note=0,
                         volume_envelope=slow_attack_env)
```

## Sample Length Guidelines

| Instrument Type | Minimum | Recommended | Notes |
|-----------------|---------|-------------|-------|
| Kick | 0.1s | 0.15-0.2s | Short, no loop |
| Snare | 0.15s | 0.2-0.3s | Short, no loop |
| Hi-hat closed | 0.05s | 0.1s | Very short |
| Hi-hat open | 0.2s | 0.3-0.5s | May need loop |
| Bass (synth) | 0.1s | 0.2s looped | Loop after attack |
| Lead | 0.2s | 0.3s looped | Loop after attack |
| Pad | 0.3s | 0.5s looped | Longer for texture |
| Strings | 0.5s | 1s looped | Need bow texture |

## Bit Depth Considerations

| Bit Depth | File Size | Quality | Use For |
|-----------|-----------|---------|---------|
| 8-bit | Half | Lo-fi | Drums, chiptune |
| 16-bit | Full | Clean | Melodic, pads |

```python
# 8-bit for drums (smaller, appropriate lo-fi character)
kick = XmInstrument(name="kick", sample_data=kick_bytes, sample_bits=8)

# 16-bit for melodic content (cleaner)
pad = XmInstrument(name="pad", sample_data=pad_bytes, sample_bits=16)
```

## Sample Rate Optimization

Lower sample rates = smaller files:

| Sample Rate | Quality | Use For |
|-------------|---------|---------|
| 44100 Hz | Studio | Never (overkill for trackers) |
| 22050 Hz | Good | Default for all |
| 11025 Hz | Lo-fi | Drums, retro aesthetic |
| 8000 Hz | Very lo-fi | Intentional degradation |

**Nethercore standard:** 22050 Hz mono

## Space-Saving Techniques

### 1. Noise-Based Drums

Generate drum samples with very short noise bursts + pitch envelope:

```python
def generate_minimal_kick(duration=0.05):
    """50ms kick using noise + pitch envelope = tiny sample"""
    samples = int(22050 * duration)
    t = np.linspace(0, duration, samples)

    # Sine with pitch drop
    freq = 150 * np.exp(-t * 30)  # Fast pitch drop
    wave = np.sin(2 * np.pi * freq * t)

    # Amplitude envelope
    env = np.exp(-t * 40)

    return (wave * env * 32767).astype(np.int16).tobytes()
```

### 2. Waveform Samples

Single-cycle waveforms loop perfectly:

```python
def single_cycle_saw(frequency=261.63):  # C-4
    """One cycle of saw wave - loops perfectly"""
    samples_per_cycle = int(22050 / frequency)
    t = np.linspace(0, 1, samples_per_cycle, endpoint=False)
    wave = 2 * (t - 0.5)  # Sawtooth
    return (wave * 32767).astype(np.int16).tobytes()
# Result: ~84 bytes for a sample that can play any note!
```

### 3. Effect-Based Synthesis

Use tracker effects instead of sample complexity:

```
Instead of: Long sample with built-in vibrato
Use: Short sample + H effect (vibrato)

Instead of: Sample with pitch envelope baked in
Use: Short sample + E effect (pitch slide)

Instead of: Sample with tremolo baked in
Use: Short sample + R effect (tremolo)
```

## Size Budget Guidelines

For a typical game soundtrack:

| Category | Target Size | Notes |
|----------|-------------|-------|
| Drum kit | 50-100 KB | 8-bit OK |
| Bass samples | 20-50 KB | Loop points critical |
| Lead samples | 50-100 KB | May need variety |
| Pad samples | 50-100 KB | Long loops |
| SFX (shared) | 50-100 KB | Overlap with game SFX |
| **Total** | **250-500 KB** | For 3-5 songs |

## Deduplication

Nethercore auto-deduplicates by content hash, so:

```toml
# These will share the same ROM space if identical:
[[assets.trackers]]
id = "song1"
path = "music/song1.xm"  # Contains "kick" sample

[[assets.trackers]]
id = "song2"
path = "music/song2.xm"  # Contains identical "kick" sample
# → Only one copy of kick in ROM
```

**Implication:** Standardize your drum kit across all songs!
