#!/usr/bin/env python3
"""
Hit/Punch Sound Effect
======================
Short noise burst with quick lowpass and body thump.

Technique: Noise + sine transient, heavily filtered
Character: Impactful, physical, weighty
Duration: 0.05 - 0.2 seconds

Dependencies: pip install numpy scipy soundfile
"""

import numpy as np
import soundfile as sf
from scipy import signal

# =============================================================================
# PARAMETERS
# =============================================================================

# Transient (the initial "thwack")
TRANSIENT_FREQ = 100        # Low thump frequency (Hz)
TRANSIENT_DECAY = 30        # Exponential decay rate

# Noise layer (the "texture")
NOISE_TYPE = "white"        # "white" for sharp, "pink" for softer
NOISE_DECAY = 20            # Noise decay rate
NOISE_MIX = 0.6             # Mix level (0-1)

# Filter
FILTER_FREQ = 1500          # Cutoff frequency (Hz)
FILTER_SWEEP = True         # Sweep filter down
FILTER_END = 300            # Ending cutoff if sweeping

# Body (low-end weight)
BODY_ENABLED = True         # Add low-end thump
BODY_FREQ = 80              # Body frequency (Hz)
BODY_MIX = 0.4              # Body mix level

# Compression (for punch)
COMPRESS = True             # Use soft clipping

# Output
DURATION = 0.1
SAMPLE_RATE = 22050
OUTPUT_FILE = "hit.wav"


# =============================================================================
# UTILITIES
# =============================================================================

def generate_noise(noise_type, num_samples):
    """Generate noise of specified type."""
    if noise_type == "pink":
        white = np.random.randn(num_samples)
        fft = np.fft.rfft(white)
        freqs = np.fft.rfftfreq(num_samples)
        freqs[0] = 1
        fft = fft / np.sqrt(freqs)
        return np.fft.irfft(fft, num_samples).astype(np.float32)
    else:  # white
        return np.random.randn(num_samples).astype(np.float32)


def filter_sweep(audio, start_cutoff, end_cutoff, sample_rate):
    """Apply time-varying lowpass filter."""
    num_samples = len(audio)
    output = np.zeros(num_samples, dtype=np.float32)
    chunk_size = 128  # Smaller chunks for short sounds

    for i in range(0, num_samples, chunk_size):
        end = min(i + chunk_size, num_samples)
        progress = i / num_samples
        cutoff = start_cutoff * (1 - progress) + end_cutoff * progress

        nyquist = sample_rate / 2
        norm_cutoff = max(0.01, min(cutoff / nyquist, 0.99))
        b, a = signal.butter(2, norm_cutoff, btype='low')
        output[i:end] = signal.lfilter(b, a, audio[i:end])

    return output


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_hit():
    """Build the hit sound synthesis chain."""
    num_samples = int(SAMPLE_RATE * DURATION)
    t = np.linspace(0, DURATION, num_samples, dtype=np.float32)

    # === TRANSIENT LAYER ===
    trans_env = np.exp(-t * TRANSIENT_DECAY)
    transient = np.sin(2 * np.pi * TRANSIENT_FREQ * t) * trans_env

    # === NOISE LAYER ===
    noise = generate_noise(NOISE_TYPE, num_samples)
    noise_env = np.exp(-t * NOISE_DECAY)

    # Apply filter
    if FILTER_SWEEP:
        filtered_noise = filter_sweep(noise, FILTER_FREQ, FILTER_END, SAMPLE_RATE)
    else:
        nyquist = SAMPLE_RATE / 2
        norm_cutoff = min(FILTER_FREQ / nyquist, 0.99)
        b, a = signal.butter(2, norm_cutoff, btype='low')
        filtered_noise = signal.filtfilt(b, a, noise)

    layer_noise = filtered_noise * noise_env * NOISE_MIX

    # === BODY LAYER ===
    if BODY_ENABLED:
        body_env = np.exp(-t * 25)
        body = np.sin(2 * np.pi * BODY_FREQ * t) * body_env * BODY_MIX
    else:
        body = np.zeros(num_samples, dtype=np.float32)

    # === MIX ===
    mixed = transient + layer_noise + body

    # === COMPRESSION (soft clipping) ===
    if COMPRESS:
        mixed = np.tanh(mixed * 1.5)

    return mixed.astype(np.float32)


def render():
    """Render the hit sound to WAV file."""
    audio = build_hit()

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.9

    sf.write(OUTPUT_FILE, audio, SAMPLE_RATE, subtype='PCM_16')
    print(f"Generated: {OUTPUT_FILE}")


# =============================================================================
# VARIATIONS
# =============================================================================

def hit_punch():
    """Heavy punch - more body, longer tail."""
    global BODY_MIX, BODY_FREQ, NOISE_DECAY, DURATION
    BODY_MIX = 0.6
    BODY_FREQ = 60
    NOISE_DECAY = 15
    DURATION = 0.15


def hit_slap():
    """Sharp slap - more high-end, less body."""
    global BODY_ENABLED, FILTER_FREQ, NOISE_TYPE, NOISE_DECAY
    BODY_ENABLED = False
    FILTER_FREQ = 3000
    NOISE_TYPE = "white"
    NOISE_DECAY = 30


def hit_sword():
    """Sword clash - metallic ring."""
    global TRANSIENT_FREQ, FILTER_FREQ, NOISE_MIX
    TRANSIENT_FREQ = 400
    FILTER_FREQ = 4000
    NOISE_MIX = 0.4


def hit_blunt():
    """Blunt impact - baseball bat, club."""
    global BODY_MIX, BODY_FREQ, TRANSIENT_FREQ, FILTER_FREQ
    BODY_MIX = 0.7
    BODY_FREQ = 50
    TRANSIENT_FREQ = 80
    FILTER_FREQ = 800


def hit_light():
    """Light tap - UI feedback, small damage."""
    global DURATION, NOISE_DECAY, BODY_ENABLED, NOISE_MIX
    DURATION = 0.05
    NOISE_DECAY = 40
    BODY_ENABLED = False
    NOISE_MIX = 0.3


if __name__ == "__main__":
    # Uncomment one variation or use defaults:
    # hit_punch()
    # hit_slap()
    # hit_sword()
    # hit_blunt()
    # hit_light()

    render()
