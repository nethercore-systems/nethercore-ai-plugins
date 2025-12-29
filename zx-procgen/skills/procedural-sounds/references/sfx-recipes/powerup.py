#!/usr/bin/env python3
"""
Powerup Sound Effect
====================
Rising pitch with FM shimmer and optional arpeggio for magical feel.

Technique: FM synthesis + arpeggio overlay
Character: Magical, empowering, exciting
Duration: 0.4 - 0.8 seconds

Dependencies: pip install numpy scipy soundfile
"""

import numpy as np
import soundfile as sf
from scipy import signal

# =============================================================================
# PARAMETERS
# =============================================================================

# Main sweep
START_FREQ = 200            # Starting frequency (Hz)
END_FREQ = 800              # Ending frequency (Hz)
SWEEP_TIME = 0.5            # Sweep duration

# FM synthesis (shimmer/sparkle)
FM_ENABLED = True           # Enable FM shimmer
FM_RATIO = 3.0              # Carrier:modulator ratio
FM_INDEX = 4.0              # Modulation index (higher = more harmonics)

# Arpeggio overlay (optional sparkle notes)
ARPEGGIO_ENABLED = True     # Add sparkle notes
ARPEGGIO_NOTES = [523, 784, 1047, 1319]  # C5, G5, C6, E6
ARPEGGIO_INTERVAL = 0.08    # Time between notes
ARPEGGIO_MIX = 0.3          # Mix level

# Effects
REVERB_MIX = 0.25           # Reverb mix

# Envelope
ATTACK = 0.05               # Gradual attack
DECAY_RATE = 3              # Exponential decay rate

# Output
DURATION = 0.6
SAMPLE_RATE = 22050
OUTPUT_FILE = "powerup.wav"


# =============================================================================
# UTILITIES
# =============================================================================

def simple_reverb(audio, mix, sample_rate):
    """Simple reverb effect."""
    if mix <= 0:
        return audio

    delays = [int(d * sample_rate) for d in [0.03, 0.037, 0.045]]
    output = np.zeros(len(audio) + max(delays), dtype=np.float32)
    output[:len(audio)] = audio

    for delay in delays:
        for i in range(delay, len(output) - 1):
            output[i] += output[i - delay] * 0.4

    output = output[:len(audio)]
    return audio * (1 - mix) + output * mix


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_powerup():
    """Build the powerup sound synthesis chain."""
    num_samples = int(SAMPLE_RATE * DURATION)
    t = np.linspace(0, DURATION, num_samples, dtype=np.float32)

    # === MAIN SWEEP ===
    # Frequency sweep
    sweep_samples = int(SWEEP_TIME * SAMPLE_RATE)
    freq = np.zeros(num_samples, dtype=np.float32)
    freq[:sweep_samples] = np.linspace(START_FREQ, END_FREQ, sweep_samples)
    freq[sweep_samples:] = END_FREQ

    # Integrate frequency to get phase
    phase = np.cumsum(2 * np.pi * freq / SAMPLE_RATE)

    # Envelope
    env = 1 - np.exp(-t / ATTACK)  # Attack
    env *= np.exp(-(t - DURATION * 0.3).clip(0) * DECAY_RATE)  # Decay after peak

    # Main oscillator (FM or simple)
    if FM_ENABLED:
        # FM synthesis
        mod_freq = freq * FM_RATIO
        mod_phase = np.cumsum(2 * np.pi * mod_freq / SAMPLE_RATE)
        modulator = np.sin(mod_phase)

        # Index envelope (decays over time)
        index_env = FM_INDEX * np.exp(-t * 2)
        main_audio = np.sin(phase + index_env * modulator) * env
    else:
        main_audio = np.sin(phase) * env

    # === ARPEGGIO SPARKLE ===
    if ARPEGGIO_ENABLED:
        arp_audio = np.zeros(num_samples, dtype=np.float32)

        for i, note_freq in enumerate(ARPEGGIO_NOTES):
            note_start = i * ARPEGGIO_INTERVAL
            note_mask = t >= note_start
            note_t = t[note_mask] - note_start

            # Note with quick decay
            note_env = np.exp(-note_t * 15)
            note = np.sin(2 * np.pi * note_freq * note_t) * note_env

            arp_audio[note_mask] += note * ARPEGGIO_MIX

        main_audio = main_audio + arp_audio

    # === REVERB ===
    if REVERB_MIX > 0:
        main_audio = simple_reverb(main_audio, REVERB_MIX, SAMPLE_RATE)

    return main_audio.astype(np.float32)


def render():
    """Render the powerup sound to WAV file."""
    audio = build_powerup()

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.9

    sf.write(OUTPUT_FILE, audio, SAMPLE_RATE, subtype='PCM_16')
    print(f"Generated: {OUTPUT_FILE}")


# =============================================================================
# VARIATIONS
# =============================================================================

def powerup_health():
    """Health restore - gentle, warm."""
    global START_FREQ, END_FREQ, FM_ENABLED, REVERB_MIX
    START_FREQ = 300
    END_FREQ = 500
    FM_ENABLED = False
    REVERB_MIX = 0.35


def powerup_speed():
    """Speed boost - quick, energetic."""
    global SWEEP_TIME, DURATION, START_FREQ, END_FREQ, ARPEGGIO_INTERVAL
    SWEEP_TIME = 0.25
    DURATION = 0.35
    START_FREQ = 300
    END_FREQ = 1200
    ARPEGGIO_INTERVAL = 0.04


def powerup_ultimate():
    """Ultimate ability - dramatic, powerful."""
    global DURATION, SWEEP_TIME, END_FREQ, FM_INDEX, REVERB_MIX, ARPEGGIO_NOTES
    DURATION = 0.8
    SWEEP_TIME = 0.6
    END_FREQ = 1000
    FM_INDEX = 6.0
    REVERB_MIX = 0.4
    ARPEGGIO_NOTES = [262, 392, 523, 659, 784, 1047]


def powerup_subtle():
    """Small buff - subtle, quick."""
    global DURATION, SWEEP_TIME, ARPEGGIO_ENABLED, FM_ENABLED
    DURATION = 0.3
    SWEEP_TIME = 0.2
    ARPEGGIO_ENABLED = False
    FM_ENABLED = False


def powerup_dark():
    """Dark/corrupted powerup - ominous."""
    global START_FREQ, END_FREQ, FM_RATIO, FM_INDEX
    START_FREQ = 100
    END_FREQ = 300
    FM_RATIO = 1.5
    FM_INDEX = 8.0


if __name__ == "__main__":
    # Uncomment one variation or use defaults:
    # powerup_health()
    # powerup_speed()
    # powerup_ultimate()
    # powerup_subtle()
    # powerup_dark()

    render()
