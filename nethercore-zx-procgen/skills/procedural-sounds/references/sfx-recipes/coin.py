#!/usr/bin/env python3
"""
Coin/Pickup Sound Effect
========================
Ascending arpeggio with bright, cheerful character.

Technique: Additive synthesis with quick envelopes
Character: Rewarding, cheerful, satisfying
Duration: 0.3 - 0.5 seconds

Dependencies: pip install numpy scipy soundfile
"""

import numpy as np
import soundfile as sf
from scipy import signal

# =============================================================================
# PARAMETERS
# =============================================================================

# Notes (frequencies in Hz)
# Default: C5 -> E5 -> G5 -> C6 (major arpeggio)
NOTES = [523, 659, 784, 1047]

# Timing
NOTE_DURATION = 0.08        # Duration per note
GAP_BETWEEN_NOTES = 0.06    # Time between note starts

# Envelope (per note)
DECAY_RATE = 25             # Exponential decay rate

# Tone
WAVEFORM = "sine"           # "sine", "square", or "triangle"
BRIGHTNESS = 0.3            # Add harmonics (0-1)

# Effects
REVERB_MIX = 0.15           # Slight reverb

# Output
SAMPLE_RATE = 22050
OUTPUT_FILE = "coin.wav"


# =============================================================================
# SYNTHESIS
# =============================================================================

def generate_waveform(freq, t, waveform):
    """Generate waveform of specified type."""
    phase = 2 * np.pi * freq * t
    if waveform == "square":
        return np.sign(np.sin(phase))
    elif waveform == "triangle":
        return 2 * np.abs(2 * (freq * t % 1) - 1) - 1
    else:  # sine
        return np.sin(phase)


def simple_reverb(audio, mix, sample_rate):
    """Simple reverb effect."""
    if mix <= 0:
        return audio

    delays = [int(d * sample_rate) for d in [0.025, 0.031]]
    output = np.zeros(len(audio) + max(delays), dtype=np.float32)
    output[:len(audio)] = audio

    for delay in delays:
        for i in range(delay, len(audio)):
            output[i] += output[i - delay] * 0.5

    output = output[:len(audio)]
    return audio * (1 - mix) + output * mix


def build_coin():
    """Build the coin sound synthesis chain."""
    total_duration = len(NOTES) * GAP_BETWEEN_NOTES + NOTE_DURATION + 0.1
    num_samples = int(SAMPLE_RATE * total_duration)
    t = np.linspace(0, total_duration, num_samples, dtype=np.float32)
    audio = np.zeros(num_samples, dtype=np.float32)

    for i, freq in enumerate(NOTES):
        note_start = i * GAP_BETWEEN_NOTES

        # Create note envelope (starts at note_start, decays from there)
        note_mask = t >= note_start
        note_t = t[note_mask] - note_start
        note_env = np.exp(-note_t * DECAY_RATE)

        # Generate waveform
        note_audio = generate_waveform(freq, t[note_mask], WAVEFORM)

        # Add harmonics for brightness
        if BRIGHTNESS > 0:
            note_audio += generate_waveform(freq * 2, t[note_mask], "sine") * BRIGHTNESS * 0.5
            note_audio += generate_waveform(freq * 3, t[note_mask], "sine") * BRIGHTNESS * 0.25
            note_audio /= 1 + BRIGHTNESS * 0.75

        # Apply envelope and add to output
        audio[note_mask] += note_audio * note_env * 0.4

    # Apply reverb
    if REVERB_MIX > 0:
        audio = simple_reverb(audio, REVERB_MIX, SAMPLE_RATE)

    return audio.astype(np.float32)


def render():
    """Render the coin sound to WAV file."""
    audio = build_coin()

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.9

    sf.write(OUTPUT_FILE, audio, SAMPLE_RATE, subtype='PCM_16')
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
    global NOTES, GAP_BETWEEN_NOTES, NOTE_DURATION, BRIGHTNESS, REVERB_MIX
    NOTES = [523, 659, 784, 988, 1047]  # C5 -> E5 -> G5 -> B5 -> C6
    GAP_BETWEEN_NOTES = 0.05
    NOTE_DURATION = 0.1
    BRIGHTNESS = 0.5
    REVERB_MIX = 0.25


def coin_power():
    """Power crystal - deep and resonant."""
    global NOTES, GAP_BETWEEN_NOTES, NOTE_DURATION, REVERB_MIX
    NOTES = [262, 330, 392, 523]  # C4 -> E4 -> G4 -> C5 (octave lower)
    GAP_BETWEEN_NOTES = 0.08
    NOTE_DURATION = 0.15
    REVERB_MIX = 0.3


def coin_retro():
    """8-bit retro coin."""
    global NOTES, WAVEFORM, REVERB_MIX, BRIGHTNESS
    NOTES = [880, 1175]  # A5 -> D6
    WAVEFORM = "square"
    REVERB_MIX = 0.0
    BRIGHTNESS = 0.0


if __name__ == "__main__":
    # Uncomment one variation or use defaults:
    # coin_classic()
    # coin_gem()
    # coin_power()
    # coin_retro()

    render()
