#!/usr/bin/env python3
"""
Coin/Pickup Sound Effect
========================
Ascending arpeggio with bright, cheerful character.

Technique: Additive synthesis with quick envelopes
Character: Rewarding, cheerful, satisfying
Duration: 0.3 - 0.5 seconds
"""

from pyo import *
import time

# =============================================================================
# PARAMETERS
# =============================================================================

# Notes (frequencies in Hz)
# Default: C5 -> E5 -> G5 -> C6 (major arpeggio)
NOTES = [523, 659, 784, 1047]

# Alternatively, define by MIDI notes:
# C5=60, E5=64, G5=67, C6=72
# Use: NOTES = [mtof(n) for n in [60, 64, 67, 72]]

# Timing
NOTE_DURATION = 0.08        # Duration per note
NOTE_OVERLAP = 0.02         # Overlap between notes (polyphony)
GAP_BETWEEN_NOTES = 0.06    # Time between note starts

# Envelope (per note)
ATTACK = 0.005              # Very quick attack
DECAY = 0.08                # Quick decay
SUSTAIN = 0.0               # No sustain (plucky)
RELEASE = 0.03              # Short release

# Tone
WAVEFORM = "sine"           # "sine", "square", or "triangle"
BRIGHTNESS = 0.3            # Add harmonics (0-1)

# Effects
CHORUS_ENABLED = False      # Adds shimmer
REVERB_MIX = 0.15           # Slight reverb

# Output
SAMPLE_RATE = 22050
OUTPUT_FILE = "coin.wav"


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_coin(s):
    """Build the coin sound synthesis chain."""

    total_dur = len(NOTES) * GAP_BETWEEN_NOTES + NOTE_DURATION + 0.1
    oscs = []
    envs = []

    for i, freq in enumerate(NOTES):
        # Trigger for this note (will be played with delay)
        trig = Trig()

        # Envelope for this note
        env = Adsr(
            attack=ATTACK,
            decay=DECAY,
            sustain=SUSTAIN,
            release=RELEASE,
            dur=NOTE_DURATION,
            trig=trig
        )
        envs.append((trig, env, i * GAP_BETWEEN_NOTES))

        # Oscillator
        if WAVEFORM == "square":
            osc = LFO(freq=freq, type=2, mul=env)  # Square wave
        elif WAVEFORM == "triangle":
            osc = LFO(freq=freq, type=3, mul=env)  # Triangle wave
        else:
            osc = Sine(freq=freq, mul=env)

        # Add brightness (harmonics)
        if BRIGHTNESS > 0:
            harmonic = Sine(freq=freq * 2, mul=env * BRIGHTNESS * 0.5)
            harmonic2 = Sine(freq=freq * 3, mul=env * BRIGHTNESS * 0.25)
            osc = Mix([osc, harmonic, harmonic2], voices=1)

        oscs.append(osc)

    # Mix all notes
    mixed = Mix(oscs, voices=1)

    # Optional chorus for shimmer
    if CHORUS_ENABLED:
        mixed = Chorus(mixed, depth=0.5, feedback=0.2, bal=0.3)

    # Light reverb for polish
    if REVERB_MIX > 0:
        mixed = Freeverb(mixed, size=0.3, damp=0.7, bal=REVERB_MIX)

    # Store envelope data for triggering
    mixed._coin_envs = envs

    return mixed


def render():
    """Render the coin sound to WAV file."""
    s = Server(audio="offline")
    s.setSamplingRate(SAMPLE_RATE)
    s.setNchnls(1)
    s.boot()
    s.recordOptions(filename=OUTPUT_FILE, fileformat=0, sampletype=1)

    signal = build_coin(s)
    signal.out()

    s.start()
    s.recstart()

    # Trigger each note with its delay
    for trig, env, delay in signal._coin_envs:
        time.sleep(delay if delay == signal._coin_envs[0][2] else GAP_BETWEEN_NOTES)
        trig.play()

    # Wait for last note to finish
    time.sleep(NOTE_DURATION + 0.15)
    s.recstop()
    s.stop()
    s.shutdown()

    print(f"Generated: {OUTPUT_FILE}")


# =============================================================================
# VARIATIONS
# =============================================================================

def coin_classic():
    """Classic 2-note Mario-style coin."""
    global NOTES, GAP_BETWEEN_NOTES, NOTE_DURATION, WAVEFORM
    NOTES = [988, 1319]  # B5 -> E6
    GAP_BETWEEN_NOTES = 0.08
    NOTE_DURATION = 0.12
    WAVEFORM = "square"


def coin_gem():
    """Sparkly gem pickup - longer, more magical."""
    global NOTES, GAP_BETWEEN_NOTES, NOTE_DURATION, CHORUS_ENABLED, BRIGHTNESS
    NOTES = [523, 659, 784, 988, 1047]  # C5 -> E5 -> G5 -> B5 -> C6
    GAP_BETWEEN_NOTES = 0.05
    NOTE_DURATION = 0.1
    CHORUS_ENABLED = True
    BRIGHTNESS = 0.5


def coin_power():
    """Power crystal - deep and resonant."""
    global NOTES, GAP_BETWEEN_NOTES, NOTE_DURATION, REVERB_MIX
    NOTES = [262, 330, 392, 523]  # C4 -> E4 -> G4 -> C5 (octave lower)
    GAP_BETWEEN_NOTES = 0.08
    NOTE_DURATION = 0.15
    REVERB_MIX = 0.3


def coin_retro():
    """8-bit retro coin."""
    global NOTES, WAVEFORM, CHORUS_ENABLED, REVERB_MIX, BRIGHTNESS
    NOTES = [880, 1175]  # A5 -> D6
    WAVEFORM = "square"
    CHORUS_ENABLED = False
    REVERB_MIX = 0.0
    BRIGHTNESS = 0.0


if __name__ == "__main__":
    # Uncomment one variation or use defaults:
    # coin_classic()
    # coin_gem()
    # coin_power()
    # coin_retro()

    render()
