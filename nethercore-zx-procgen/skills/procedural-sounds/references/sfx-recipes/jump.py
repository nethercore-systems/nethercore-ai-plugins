#!/usr/bin/env python3
"""
Jump Sound Effect
=================
Rising then falling pitch with quick attack.

Technique: Frequency modulation with pitch envelope
Character: Bouncy, playful, responsive
Duration: 0.15 - 0.3 seconds
"""

from pyo import *
import time

# =============================================================================
# PARAMETERS
# =============================================================================

# Pitch curve
START_FREQ = 150            # Starting frequency (Hz)
PEAK_FREQ = 400             # Peak frequency (Hz)
END_FREQ = 200              # Ending frequency (Hz)
RISE_TIME = 0.08            # Time to reach peak
FALL_TIME = 0.12            # Time to fall from peak

# Waveform
WAVEFORM = "sine"           # "sine", "square", "triangle"
ADD_HARMONICS = True        # Add upper harmonics for presence

# Envelope
ATTACK = 0.01               # Quick attack
DECAY = 0.15                # Main body
RELEASE = 0.05              # Short tail

# Filter (optional warmth)
FILTER_ENABLED = True       # Low-pass filter
FILTER_FREQ = 2000          # Cutoff frequency

# Effects
SUBTLE_CHORUS = False       # Very light chorus for width

# Output
DURATION = 0.25
SAMPLE_RATE = 22050
OUTPUT_FILE = "jump.wav"


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_jump(s):
    """Build the jump sound synthesis chain."""

    # Amplitude envelope
    env = Adsr(
        attack=ATTACK,
        decay=DECAY,
        sustain=0,
        release=RELEASE,
        dur=DURATION
    )
    env.play()

    # Pitch envelope: rise then fall
    # Using Linseg with multiple points
    pitch_env = Linseg([
        (0, START_FREQ),
        (RISE_TIME, PEAK_FREQ),
        (RISE_TIME + FALL_TIME, END_FREQ)
    ])
    pitch_env.play()

    # Main oscillator
    if WAVEFORM == "square":
        osc = LFO(freq=pitch_env, type=2, mul=env)
    elif WAVEFORM == "triangle":
        osc = LFO(freq=pitch_env, type=3, mul=env)
    else:
        osc = Sine(freq=pitch_env, mul=env)

    # Add harmonics for presence
    if ADD_HARMONICS:
        harm1 = Sine(freq=pitch_env * 2, mul=env * 0.3)
        harm2 = Sine(freq=pitch_env * 3, mul=env * 0.15)
        osc = Mix([osc, harm1, harm2], voices=1)

    # Optional lowpass for warmth
    if FILTER_ENABLED:
        osc = ButLP(osc, freq=FILTER_FREQ)

    # Optional subtle chorus
    if SUBTLE_CHORUS:
        osc = Chorus(osc, depth=0.3, feedback=0.1, bal=0.2)

    return osc


def render():
    """Render the jump sound to WAV file."""
    s = Server(audio="offline")
    s.setSamplingRate(SAMPLE_RATE)
    s.setNchnls(1)
    s.boot()
    s.recordOptions(filename=OUTPUT_FILE, fileformat=0, sampletype=1)

    signal = build_jump(s)
    signal.out()

    s.start()
    s.recstart()
    time.sleep(DURATION + 0.1)
    s.recstop()
    s.stop()
    s.shutdown()

    print(f"Generated: {OUTPUT_FILE}")


# =============================================================================
# VARIATIONS
# =============================================================================

def jump_high():
    """High jump - more dramatic arc."""
    global START_FREQ, PEAK_FREQ, END_FREQ, RISE_TIME, FALL_TIME, DURATION
    START_FREQ = 200
    PEAK_FREQ = 600
    END_FREQ = 250
    RISE_TIME = 0.1
    FALL_TIME = 0.15
    DURATION = 0.3


def jump_small():
    """Small hop - quick and subtle."""
    global START_FREQ, PEAK_FREQ, END_FREQ, RISE_TIME, FALL_TIME, DURATION
    START_FREQ = 200
    PEAK_FREQ = 350
    END_FREQ = 220
    RISE_TIME = 0.05
    FALL_TIME = 0.08
    DURATION = 0.15


def jump_double():
    """Double jump - second bounce higher."""
    global START_FREQ, PEAK_FREQ, END_FREQ, RISE_TIME
    START_FREQ = 300
    PEAK_FREQ = 700
    END_FREQ = 350
    RISE_TIME = 0.06


def jump_retro():
    """8-bit style jump."""
    global WAVEFORM, ADD_HARMONICS, FILTER_ENABLED, START_FREQ, PEAK_FREQ
    WAVEFORM = "square"
    ADD_HARMONICS = False
    FILTER_ENABLED = False
    START_FREQ = 180
    PEAK_FREQ = 500


def jump_floaty():
    """Floaty/low gravity jump."""
    global RISE_TIME, FALL_TIME, DURATION, START_FREQ, PEAK_FREQ, END_FREQ
    RISE_TIME = 0.15
    FALL_TIME = 0.25
    DURATION = 0.45
    START_FREQ = 120
    PEAK_FREQ = 280
    END_FREQ = 150


if __name__ == "__main__":
    # Uncomment one variation or use defaults:
    # jump_high()
    # jump_small()
    # jump_double()
    # jump_retro()
    # jump_floaty()

    render()
