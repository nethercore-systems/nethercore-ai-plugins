# pyo Offline Workflow Reference

Complete patterns for rendering audio files without audio hardware using pyo's offline mode.

## Core Offline Pattern

```python
from pyo import *
import time

def render_sound(filename: str, duration: float, build_chain):
    """
    Render a sound to WAV file.

    Args:
        filename: Output WAV path
        duration: Length in seconds
        build_chain: Function that builds synthesis chain and returns final signal
    """
    s = Server(audio="offline")
    s.setSamplingRate(22050)  # ZX standard
    s.setNchnls(1)            # Mono
    s.boot()

    s.recordOptions(
        filename=filename,
        fileformat=0,    # WAV
        sampletype=1     # 16-bit
    )

    # Build the synthesis chain
    signal = build_chain(s)
    signal.out()

    s.start()
    s.recstart()
    time.sleep(duration + 0.1)  # Small buffer
    s.recstop()
    s.stop()
    s.shutdown()
```

## Server Configuration Options

```python
s = Server(audio="offline")

# Sample rate (ZX uses 22050)
s.setSamplingRate(22050)

# Channels (1=mono, 2=stereo)
s.setNchnls(1)

# Buffer size (affects precision, 512 is good default)
s.setBufferSize(512)

# Record options
s.recordOptions(
    filename="output.wav",
    fileformat=0,    # 0=WAV, 1=AIFF
    sampletype=1,    # 0=float, 1=16-bit, 2=24-bit, 3=32-bit
    quality=0.4      # For compressed formats
)
```

## fileformat Values

| Value | Format |
|-------|--------|
| 0 | WAV |
| 1 | AIFF |
| 2 | AU |
| 3 | RAW |
| 4 | SD2 |
| 5 | FLAC |
| 6 | CAF |
| 7 | OGG |

## sampletype Values

| Value | Format | Use Case |
|-------|--------|----------|
| 0 | 32-bit float | Maximum quality |
| 1 | 16-bit int | **ZX standard** |
| 2 | 24-bit int | High quality |
| 3 | 32-bit int | Very high quality |

## Triggering Envelopes

For sounds that need triggering (not self-starting):

```python
def render_triggered_sound(filename: str, duration: float):
    s = Server(audio="offline")
    s.setSamplingRate(22050)
    s.setNchnls(1)
    s.boot()
    s.recordOptions(filename=filename, fileformat=0, sampletype=1)

    # Create envelope with trigger
    trig = Trig()
    env = Adsr(attack=0.01, decay=0.2, sustain=0, release=0.1, dur=0.3, trig=trig)
    osc = Sine(freq=440, mul=env)
    osc.out()

    s.start()
    s.recstart()

    # Trigger the envelope
    trig.play()

    time.sleep(duration + 0.1)
    s.recstop()
    s.stop()
    s.shutdown()
```

## Multiple Sounds with Shared Server

For batch generation efficiency:

```python
def render_batch(sounds: dict):
    """
    Render multiple sounds efficiently.

    Args:
        sounds: Dict of {filename: (duration, build_chain)}
    """
    for filename, (duration, build_chain) in sounds.items():
        s = Server(audio="offline")
        s.setSamplingRate(22050)
        s.setNchnls(1)
        s.boot()
        s.recordOptions(filename=filename, fileformat=0, sampletype=1)

        signal = build_chain(s)
        signal.out()

        s.start()
        s.recstart()
        time.sleep(duration + 0.1)
        s.recstop()
        s.stop()
        s.shutdown()

        print(f"Generated: {filename}")
```

## Scheduled Events

For sounds with multiple events (arpeggios, sequences):

```python
def render_arpeggio(filename: str):
    s = Server(audio="offline")
    s.setSamplingRate(22050)
    s.setNchnls(1)
    s.boot()
    s.recordOptions(filename=filename, fileformat=0, sampletype=1)

    freqs = [523, 659, 784, 1047]  # C5, E5, G5, C6
    note_dur = 0.08

    # Create triggers for each note
    trigs = [Trig() for _ in freqs]
    envs = [Adsr(attack=0.005, decay=0.08, sustain=0, release=0.02,
                 dur=note_dur, trig=t) for t in trigs]
    oscs = [Sine(freq=f, mul=e) for f, e in zip(freqs, envs)]

    mix = Mix(oscs, voices=1)
    mix.out()

    s.start()
    s.recstart()

    # Trigger notes with delays
    for i, trig in enumerate(trigs):
        time.sleep(note_dur if i > 0 else 0)
        trig.play()

    time.sleep(note_dur + 0.1)  # Wait for last note
    s.recstop()
    s.stop()
    s.shutdown()
```

## Using CallAfter for Precise Timing

```python
def render_with_callbacks(filename: str, duration: float):
    s = Server(audio="offline")
    s.setSamplingRate(22050)
    s.setNchnls(1)
    s.boot()
    s.recordOptions(filename=filename, fileformat=0, sampletype=1)

    trig = Trig()
    env = Adsr(attack=0.01, decay=0.2, sustain=0.5, release=0.1, dur=0.5, trig=trig)
    osc = Sine(freq=440, mul=env)
    osc.out()

    # Schedule trigger after 0.1 seconds
    def trigger_note():
        trig.play()

    s.start()
    s.recstart()

    # Use CallAfter for precise server-time scheduling
    CallAfter(trigger_note, 0.1)

    time.sleep(duration + 0.2)
    s.recstop()
    s.stop()
    s.shutdown()
```

## Common Pitfalls

### 1. Forgetting to call .out()

```python
# WRONG - sound won't be recorded
osc = Sine(freq=440, mul=env)

# CORRECT
osc = Sine(freq=440, mul=env)
osc.out()
```

### 2. Not waiting long enough

```python
# WRONG - may cut off sound
time.sleep(duration)

# CORRECT - add buffer for release tails
time.sleep(duration + 0.1)
```

### 3. Not shutting down server

```python
# WRONG - may cause issues with subsequent renders
s.stop()

# CORRECT
s.stop()
s.shutdown()
```

### 4. Reusing Server without shutdown

```python
# WRONG - server state persists
for sound in sounds:
    s.recstart()
    # ...
    s.recstop()

# CORRECT - fresh server each time
for sound in sounds:
    s = Server(audio="offline")
    s.boot()
    # ...
    s.shutdown()
```

## Complete Generator Script Template

```python
#!/usr/bin/env python3
"""
SFX Generator for [Game Name]
Generates all game sound effects using pyo offline rendering.
"""

from pyo import *
import time
import os

OUTPUT_DIR = "assets/audio"
SAMPLE_RATE = 22050

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def render(name: str, duration: float, build_chain):
    """Render a sound effect to WAV."""
    filepath = os.path.join(OUTPUT_DIR, f"{name}.wav")

    s = Server(audio="offline")
    s.setSamplingRate(SAMPLE_RATE)
    s.setNchnls(1)
    s.boot()
    s.recordOptions(filename=filepath, fileformat=0, sampletype=1)

    signal = build_chain(s)
    if signal:
        signal.out()

    s.start()
    s.recstart()
    time.sleep(duration + 0.1)
    s.recstop()
    s.stop()
    s.shutdown()

    print(f"Generated: {filepath}")

# Sound definitions
def build_laser(s):
    env = Adsr(attack=0.01, decay=0.15, sustain=0, release=0.05, dur=0.2)
    env.play()
    osc = SuperSaw(freq=Linseg([(0, 1200), (0.2, 200)]), detune=0.5, mul=env)
    return MoogLP(osc, freq=4000, res=0.3)

def build_explosion(s):
    env = Adsr(attack=0.01, decay=0.5, sustain=0, release=0.3, dur=0.8)
    env.play()
    noise = PinkNoise(mul=env)
    filt = MoogLP(noise, freq=Linseg([(0, 3000), (0.5, 200)]), res=0.4)
    return Freeverb(filt, size=0.8, damp=0.5, mul=0.8)

def build_coin(s):
    # See sfx-recipes/coin.py for complete implementation
    pass

if __name__ == "__main__":
    ensure_output_dir()

    render("laser", 0.25, build_laser)
    render("explosion", 1.0, build_explosion)
    # render("coin", 0.5, build_coin)

    print("All sounds generated!")
```
