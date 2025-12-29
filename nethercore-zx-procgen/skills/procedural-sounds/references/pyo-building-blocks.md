# pyo Building Blocks Reference

Complete reference for pyo classes used in game audio synthesis.

## Oscillators (Sound Sources)

### Sine
Pure tone oscillator - fundamental building block.

```python
osc = Sine(freq=440, phase=0, mul=1, add=0)
```
- `freq`: Frequency in Hz (can be signal)
- `phase`: Starting phase (0-1)
- Best for: Bass, pure tones, sub layers

### SuperSaw
Multiple detuned sawtooth waves - rich, full sound.

```python
osc = SuperSaw(freq=440, detune=0.5, bal=0.7, mul=1)
```
- `freq`: Base frequency
- `detune`: Spread of detuned saws (0-1)
- `bal`: Balance between center and spread (0-1)
- Best for: Leads, pads, lasers

### LFO (Low-Frequency Oscillator)
Multi-waveform oscillator for modulation or audio.

```python
lfo = LFO(freq=1, sharp=0.5, type=0, mul=1)
```
- `type`: 0=saw up, 1=saw down, 2=square, 3=triangle, 4=pulse, 5=bipolar pulse, 6=sample-hold, 7=modulated sine
- Best for: Modulation, simple waveforms

### Noise Sources

```python
# White noise - all frequencies equal
noise = Noise(mul=1)

# Pink noise - natural rolloff (1/f)
pink = PinkNoise(mul=1)

# Brown noise - steeper rolloff (1/f^2)
brown = BrownNoise(mul=1)
```

| Type | Character | Best For |
|------|-----------|----------|
| White | Harsh, bright | Hi-hats, impacts |
| Pink | Natural, warm | Explosions, wind |
| Brown | Deep, rumbly | Thunder, bass layers |

## Envelopes

### Adsr
Classic attack-decay-sustain-release envelope.

```python
env = Adsr(
    attack=0.01,    # Time to peak (seconds)
    decay=0.1,      # Time to sustain level
    sustain=0.5,    # Hold level (0-1)
    release=0.2,    # Fade out time
    dur=1.0,        # Total duration
    mul=1
)
env.play()  # Start envelope
```

### Linseg
Linear segment generator - custom envelope shapes.

```python
# Frequency sweep from 1000Hz to 200Hz over 0.5 seconds
sweep = Linseg([(0, 1000), (0.5, 200)])
sweep.play()

# Multi-point envelope
shape = Linseg([(0, 0), (0.1, 1), (0.3, 0.5), (1, 0)])
```

### Expseg
Exponential segment generator - natural curves.

```python
# More natural frequency decay
sweep = Expseg([(0, 1000), (0.5, 200)])
```

### Fader
Simple fade in/out.

```python
fader = Fader(fadein=0.1, fadeout=0.2, dur=1, mul=1)
```

## Filters

### MoogLP
Classic Moog-style resonant lowpass - warm and musical.

```python
filtered = MoogLP(input, freq=1000, res=0.5)
```
- `freq`: Cutoff frequency (Hz, can be signal)
- `res`: Resonance (0-1, self-oscillates near 1)
- Best for: Warm filtering, classic synth sounds

### Butterworth Filters
Clean, precise filtering.

```python
# Lowpass
lp = ButLP(input, freq=1000)

# Highpass
hp = ButHP(input, freq=200)

# Bandpass
bp = ButBP(input, freq=1000, q=5)

# Band reject (notch)
br = ButBR(input, freq=1000, q=5)
```

### Biquad Filters
Versatile digital filters with Q control.

```python
filt = Biquad(input, freq=1000, q=1, type=0)
```
- `type`: 0=lowpass, 1=highpass, 2=bandpass, 3=bandstop, 4=allpass

### Tone / Atone
Simple one-pole filters (gentle rolloff).

```python
# Lowpass (gentle)
warm = Tone(input, freq=2000)

# Highpass (gentle)
thin = Atone(input, freq=200)
```

## FM Synthesis

### FM
Classic two-operator FM synthesis.

```python
fm = FM(
    carrier=440,    # Carrier frequency
    ratio=2,        # Carrier:modulator ratio
    index=5,        # Modulation index (higher = more harmonics)
    mul=1
)
```

Common ratios:
- `1:1` - Warm, slightly metallic
- `2:1` - Octave harmonics
- `3:1` - Hollow, clarinet-like
- `1.414:1` - Bell-like, inharmonic

### CrossFM
Two oscillators modulating each other.

```python
cfm = CrossFM(
    carrier=440,
    ratio=2,
    ind1=2,     # Index osc1 → osc2
    ind2=2      # Index osc2 → osc1
)
```

## Effects

### Freeverb
Classic Schroeder reverb.

```python
verb = Freeverb(
    input,
    size=0.8,   # Room size (0-1)
    damp=0.5,   # High-frequency damping (0-1)
    bal=0.3     # Dry/wet mix (0=dry, 1=wet)
)
```

### Delay
Simple delay line.

```python
delay = Delay(
    input,
    delay=0.25,     # Delay time (seconds)
    feedback=0.5,   # Feedback amount (0-1)
    maxdelay=1      # Maximum delay buffer
)
```

### Disto
Waveshaping distortion.

```python
dist = Disto(
    input,
    drive=0.75,     # Distortion amount (0-1)
    slope=0.5,      # Curve shape
    mul=1
)
```

### Chorus
Stereo chorus effect.

```python
chorus = Chorus(
    input,
    depth=1,        # Modulation depth
    feedback=0.25,  # Feedback amount
    bal=0.5         # Dry/wet mix
)
```

### Compress
Dynamics compressor.

```python
comp = Compress(
    input,
    thresh=-20,     # Threshold (dB)
    ratio=4,        # Compression ratio
    risetime=0.01,  # Attack time
    falltime=0.1,   # Release time
    mul=1
)
```

### Clip
Hard clipping / limiting.

```python
limited = Clip(input, min=-0.9, max=0.9)
```

## Utilities

### Mix
Combine multiple signals.

```python
mixed = Mix([osc1, osc2, noise], voices=1)
```
- `voices`: Number of output channels (1=mono)

### Sig
Constant signal value (useful for modulation targets).

```python
base_freq = Sig(440)
modulated = base_freq + lfo * 100
osc = Sine(freq=modulated)
```

### Trig
Trigger generator for envelopes.

```python
trig = Trig()
env = Adsr(trig=trig, ...)
# Later:
trig.play()  # Triggers the envelope
```

### CallAfter
Schedule function call after delay.

```python
def trigger_note():
    trig.play()

CallAfter(trigger_note, 0.5)  # Trigger after 0.5 seconds
```

## Signal Math

Pyo objects support arithmetic:

```python
# Add signals
combined = osc1 + osc2

# Scale signal
quieter = osc * 0.5

# Frequency modulation
vibrato = Sine(freq=5, mul=10)
osc = Sine(freq=440 + vibrato)

# Filter modulation
sweep = Linseg([(0, 2000), (1, 200)])
filt = MoogLP(noise, freq=sweep)
```

## Common Patterns

### Subtractive Synthesis
Noise/rich-waveform through filter.

```python
env = Adsr(attack=0.01, decay=0.3, sustain=0, release=0.1, dur=0.4)
noise = PinkNoise(mul=env)
filt = MoogLP(noise, freq=Linseg([(0, 3000), (0.3, 200)]), res=0.4)
```

### FM Bell
Inharmonic FM ratios for bell sounds.

```python
env = Adsr(attack=0.001, decay=0.5, sustain=0, release=0.3, dur=0.8)
bell = FM(carrier=440, ratio=1.414, index=8, mul=env)
```

### Layered Sound
Multiple elements mixed together.

```python
# Body layer
body_env = Adsr(...)
body = Sine(freq=80, mul=body_env)

# Texture layer
tex_env = Adsr(...)
texture = PinkNoise(mul=tex_env)
texture = MoogLP(texture, freq=1000)

# Mix
mixed = Mix([body, texture], voices=1)
```

### Pitch Sweep
Frequency changing over time.

```python
pitch = Linseg([(0, 1000), (0.3, 200)])  # Descending
# or
pitch = Expseg([(0, 200), (0.3, 1000)])  # Ascending (exponential)

osc = Sine(freq=pitch, mul=env)
```
