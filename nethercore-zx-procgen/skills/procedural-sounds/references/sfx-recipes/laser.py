#!/usr/bin/env python3
"""
Laser/Zap Sound Effect
======================
Descending frequency sweep with harmonics and slight modulation.

Technique: Subtractive synthesis with SuperSaw + FM modulation
Character: Sci-fi, arcade, retro shooter
Duration: 0.15 - 0.3 seconds
"""

from pyo import *
import time
import os

# =============================================================================
# PARAMETERS - Adjust these to customize the sound
# =============================================================================

# Frequency sweep
START_FREQ = 1200       # Starting frequency (Hz) - higher = more piercing
END_FREQ = 200          # Ending frequency (Hz) - lower = deeper tail
SWEEP_CURVE = "linear"  # "linear" or "exponential"

# Oscillator
DETUNE = 0.5            # SuperSaw detune (0-1) - higher = richer/fatter
BALANCE = 0.7           # SuperSaw balance (0-1) - mix between saws

# Modulation (adds movement/wobble)
MOD_FREQ = 50           # LFO frequency (Hz)
MOD_DEPTH = 200         # Pitch modulation amount (Hz)
USE_MODULATION = True   # Enable/disable modulation

# Filter
FILTER_FREQ = 4000      # Lowpass cutoff (Hz)
FILTER_RES = 0.3        # Resonance (0-1) - higher = more emphasis at cutoff

# Envelope
ATTACK = 0.01           # Attack time (seconds)
DECAY = 0.15            # Decay time (seconds)
RELEASE = 0.05          # Release time (seconds)
DURATION = 0.2          # Total duration (seconds)

# Output
SAMPLE_RATE = 22050     # ZX standard
OUTPUT_FILE = "laser.wav"


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_laser(s):
    """Build the laser synthesis chain."""

    # Envelope - shapes the amplitude over time
    env = Adsr(
        attack=ATTACK,
        decay=DECAY,
        sustain=0,          # No sustain for punchy sound
        release=RELEASE,
        dur=DURATION
    )
    env.play()

    # Frequency sweep
    if SWEEP_CURVE == "exponential":
        freq_sweep = Expseg([(0, START_FREQ), (DURATION, END_FREQ)])
    else:
        freq_sweep = Linseg([(0, START_FREQ), (DURATION, END_FREQ)])
    freq_sweep.play()

    # Optional pitch modulation (adds wobble/character)
    if USE_MODULATION:
        lfo = Sine(freq=MOD_FREQ, mul=MOD_DEPTH)
        pitch = freq_sweep + lfo
    else:
        pitch = freq_sweep

    # Main oscillator - SuperSaw for rich harmonics
    osc = SuperSaw(
        freq=pitch,
        detune=DETUNE,
        bal=BALANCE,
        mul=env
    )

    # Lowpass filter to tame harshness
    filtered = MoogLP(osc, freq=FILTER_FREQ, res=FILTER_RES)

    return filtered


def render():
    """Render the laser sound to WAV file."""
    s = Server(audio="offline")
    s.setSamplingRate(SAMPLE_RATE)
    s.setNchnls(1)
    s.boot()
    s.recordOptions(filename=OUTPUT_FILE, fileformat=0, sampletype=1)

    signal = build_laser(s)
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

def laser_high_energy():
    """More intense, higher pitched laser."""
    global START_FREQ, END_FREQ, MOD_FREQ, MOD_DEPTH, DETUNE
    START_FREQ = 2000
    END_FREQ = 400
    MOD_FREQ = 80
    MOD_DEPTH = 300
    DETUNE = 0.7


def laser_bass():
    """Deep, bassy laser for heavy weapons."""
    global START_FREQ, END_FREQ, FILTER_FREQ, DURATION, DECAY
    START_FREQ = 600
    END_FREQ = 80
    FILTER_FREQ = 2000
    DURATION = 0.35
    DECAY = 0.25


def laser_retro():
    """Classic 8-bit style zap."""
    global START_FREQ, END_FREQ, USE_MODULATION, DETUNE, DURATION
    START_FREQ = 800
    END_FREQ = 100
    USE_MODULATION = False
    DETUNE = 0.0  # Pure saw for retro feel
    DURATION = 0.12


if __name__ == "__main__":
    # Uncomment one variation or use defaults:
    # laser_high_energy()
    # laser_bass()
    # laser_retro()

    render()
