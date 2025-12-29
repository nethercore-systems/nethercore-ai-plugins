#!/usr/bin/env python3
"""
Laser/Zap Sound Effect
======================
Descending frequency sweep with harmonics and slight modulation.

Technique: Subtractive synthesis with detuned oscillators
Character: Sci-fi, arcade, retro shooter
Duration: 0.15 - 0.3 seconds

Dependencies: pip install numpy scipy soundfile
"""

import numpy as np
import soundfile as sf
from scipy import signal

# =============================================================================
# PARAMETERS - Adjust these to customize the sound
# =============================================================================

# Frequency sweep
START_FREQ = 1200       # Starting frequency (Hz) - higher = more piercing
END_FREQ = 200          # Ending frequency (Hz) - lower = deeper tail
SWEEP_CURVE = "linear"  # "linear" or "exponential"

# Oscillator
DETUNE = 0.5            # Detune spread (0-1) - higher = richer/fatter
NUM_OSCS = 3            # Number of oscillators (1-5)

# Modulation (adds movement/wobble)
MOD_FREQ = 50           # LFO frequency (Hz)
MOD_DEPTH = 200         # Pitch modulation amount (Hz)
USE_MODULATION = True   # Enable/disable modulation

# Filter
FILTER_FREQ = 4000      # Lowpass cutoff (Hz)

# Envelope
ATTACK = 0.01           # Attack time (seconds)
DECAY_RATE = 15         # Exponential decay rate (higher = faster)
DURATION = 0.2          # Total duration (seconds)

# Output
SAMPLE_RATE = 22050     # ZX standard
OUTPUT_FILE = "laser.wav"


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_laser():
    """Build the laser synthesis chain."""
    num_samples = int(SAMPLE_RATE * DURATION)
    t = np.linspace(0, DURATION, num_samples, dtype=np.float32)

    # Frequency sweep
    if SWEEP_CURVE == "exponential":
        freq = START_FREQ * (END_FREQ / START_FREQ) ** (t / DURATION)
    else:
        freq = np.linspace(START_FREQ, END_FREQ, num_samples)

    # Optional pitch modulation
    if USE_MODULATION:
        lfo = np.sin(2 * np.pi * MOD_FREQ * t) * MOD_DEPTH
        freq = freq + lfo

    # Integrate frequency to get continuous phase
    phase = np.cumsum(2 * np.pi * freq / SAMPLE_RATE)

    # Multi-oscillator (detuned saws/sines for thickness)
    audio = np.zeros(num_samples, dtype=np.float32)
    if NUM_OSCS > 1 and DETUNE > 0:
        detune_spread = np.linspace(-DETUNE * 0.02, DETUNE * 0.02, NUM_OSCS)
        for d in detune_spread:
            audio += np.sin(phase * (1 + d))
        audio /= NUM_OSCS
    else:
        audio = np.sin(phase)

    # Add harmonics
    audio += 0.3 * np.sin(2 * phase)  # 2nd harmonic
    audio += 0.15 * np.sin(3 * phase)  # 3rd harmonic
    audio /= 1.45  # Normalize

    # Envelope - attack and exponential decay
    env = np.exp(-t * DECAY_RATE)
    attack_samples = int(ATTACK * SAMPLE_RATE)
    if attack_samples > 0:
        env[:attack_samples] *= np.linspace(0, 1, attack_samples)
    audio *= env

    # Lowpass filter
    nyquist = SAMPLE_RATE / 2
    normalized_cutoff = min(FILTER_FREQ / nyquist, 0.99)
    b, a = signal.butter(2, normalized_cutoff, btype='low')
    audio = signal.filtfilt(b, a, audio)

    return audio.astype(np.float32)


def render():
    """Render the laser sound to WAV file."""
    audio = build_laser()

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.9

    sf.write(OUTPUT_FILE, audio, SAMPLE_RATE, subtype='PCM_16')
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
    global START_FREQ, END_FREQ, FILTER_FREQ, DURATION, DECAY_RATE
    START_FREQ = 600
    END_FREQ = 80
    FILTER_FREQ = 2000
    DURATION = 0.35
    DECAY_RATE = 10


def laser_retro():
    """Classic 8-bit style zap."""
    global START_FREQ, END_FREQ, USE_MODULATION, DETUNE, DURATION, NUM_OSCS
    START_FREQ = 800
    END_FREQ = 100
    USE_MODULATION = False
    DETUNE = 0.0
    NUM_OSCS = 1
    DURATION = 0.12


if __name__ == "__main__":
    # Uncomment one variation or use defaults:
    # laser_high_energy()
    # laser_bass()
    # laser_retro()

    render()
