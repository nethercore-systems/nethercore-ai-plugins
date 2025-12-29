#!/usr/bin/env python3
"""
Jump Sound Effect
=================
Rising then falling pitch with quick attack.

Technique: Frequency modulation with pitch envelope
Character: Bouncy, playful, responsive
Duration: 0.15 - 0.3 seconds

Dependencies: pip install numpy scipy soundfile
"""

import numpy as np
import soundfile as sf
from scipy import signal

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
DECAY_RATE = 10             # Exponential decay rate

# Filter (optional warmth)
FILTER_ENABLED = True       # Low-pass filter
FILTER_FREQ = 2000          # Cutoff frequency

# Output
DURATION = 0.25
SAMPLE_RATE = 22050
OUTPUT_FILE = "jump.wav"


# =============================================================================
# SYNTHESIS
# =============================================================================

def generate_waveform(phase, waveform):
    """Generate waveform from phase array."""
    if waveform == "square":
        return np.sign(np.sin(phase))
    elif waveform == "triangle":
        # Use sawtooth and fold
        saw = 2 * (phase / (2 * np.pi) % 1) - 1
        return 2 * np.abs(saw) - 1
    else:  # sine
        return np.sin(phase)


def build_jump():
    """Build the jump sound synthesis chain."""
    num_samples = int(SAMPLE_RATE * DURATION)
    t = np.linspace(0, DURATION, num_samples, dtype=np.float32)

    # Pitch envelope: rise then fall
    rise_samples = int(RISE_TIME * SAMPLE_RATE)
    fall_samples = int(FALL_TIME * SAMPLE_RATE)

    freq = np.zeros(num_samples, dtype=np.float32)
    freq[:rise_samples] = np.linspace(START_FREQ, PEAK_FREQ, rise_samples)

    fall_end = rise_samples + fall_samples
    if fall_end <= num_samples:
        freq[rise_samples:fall_end] = np.linspace(PEAK_FREQ, END_FREQ, fall_samples)
        freq[fall_end:] = END_FREQ
    else:
        freq[rise_samples:] = np.linspace(PEAK_FREQ, END_FREQ, num_samples - rise_samples)

    # Integrate frequency to get continuous phase
    phase = np.cumsum(2 * np.pi * freq / SAMPLE_RATE)

    # Generate main oscillator
    audio = generate_waveform(phase, WAVEFORM)

    # Add harmonics for presence
    if ADD_HARMONICS:
        audio += generate_waveform(phase * 2, "sine") * 0.3
        audio += generate_waveform(phase * 3, "sine") * 0.15
        audio /= 1.45

    # Amplitude envelope
    env = np.exp(-t * DECAY_RATE)
    audio *= env

    # Optional lowpass for warmth
    if FILTER_ENABLED:
        nyquist = SAMPLE_RATE / 2
        normalized_cutoff = min(FILTER_FREQ / nyquist, 0.99)
        b, a = signal.butter(2, normalized_cutoff, btype='low')
        audio = signal.filtfilt(b, a, audio)

    return audio.astype(np.float32)


def render():
    """Render the jump sound to WAV file."""
    audio = build_jump()

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.9

    sf.write(OUTPUT_FILE, audio, SAMPLE_RATE, subtype='PCM_16')
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
    global RISE_TIME, FALL_TIME, DURATION, START_FREQ, PEAK_FREQ, END_FREQ, DECAY_RATE
    RISE_TIME = 0.15
    FALL_TIME = 0.25
    DURATION = 0.45
    START_FREQ = 120
    PEAK_FREQ = 280
    END_FREQ = 150
    DECAY_RATE = 5


if __name__ == "__main__":
    # Uncomment one variation or use defaults:
    # jump_high()
    # jump_small()
    # jump_double()
    # jump_retro()
    # jump_floaty()

    render()
