#!/usr/bin/env python3
"""
Explosion Sound Effect
======================
Noise burst with lowpass sweep, sub-bass rumble, and reverb.

Technique: Layered subtractive synthesis
Character: Impactful, cinematic, weighty
Duration: 0.5 - 1.5 seconds

Dependencies: pip install numpy scipy soundfile
"""

import numpy as np
import soundfile as sf
from scipy import signal

# =============================================================================
# PARAMETERS
# =============================================================================

# Main noise layer
NOISE_TYPE = "pink"         # "white", "pink", or "brown"
NOISE_DECAY_RATE = 3        # Exponential decay rate

# Filter sweep
FILTER_START = 3000         # Starting cutoff (Hz)
FILTER_END = 200            # Ending cutoff (Hz)

# Sub-bass rumble layer
SUB_FREQ = 50               # Sub-bass frequency (Hz)
SUB_ENABLED = True          # Enable sub layer
SUB_MIX = 0.4               # Mix level (0-1)

# High sizzle layer (debris/sparkle)
SIZZLE_ENABLED = True       # Enable sizzle layer
SIZZLE_FREQ = 4000          # Highpass cutoff
SIZZLE_MIX = 0.25           # Mix level (0-1)

# Reverb
REVERB_SIZE = 0.8           # Room size (0-1)
REVERB_MIX = 0.3            # Wet/dry mix

# Distortion (optional grit)
DISTORTION_ENABLED = False  # Enable distortion
DISTORTION_DRIVE = 0.7      # Drive amount (0-1)

# Output
DURATION = 0.9              # Total duration
SAMPLE_RATE = 22050
OUTPUT_FILE = "explosion.wav"


# =============================================================================
# UTILITIES
# =============================================================================

def generate_noise(noise_type, num_samples):
    """Generate noise of specified type."""
    if noise_type == "white":
        return np.random.randn(num_samples).astype(np.float32)
    elif noise_type == "brown":
        white = np.random.randn(num_samples)
        brown = np.cumsum(white)
        brown -= np.mean(brown)
        return (brown / np.max(np.abs(brown))).astype(np.float32)
    else:  # pink
        white = np.random.randn(num_samples)
        fft = np.fft.rfft(white)
        freqs = np.fft.rfftfreq(num_samples)
        freqs[0] = 1  # Avoid division by zero
        fft = fft / np.sqrt(freqs)
        return np.fft.irfft(fft, num_samples).astype(np.float32)


def filter_sweep(audio, start_cutoff, end_cutoff, sample_rate):
    """Apply time-varying lowpass filter."""
    num_samples = len(audio)
    output = np.zeros(num_samples, dtype=np.float32)
    chunk_size = 256

    for i in range(0, num_samples, chunk_size):
        end = min(i + chunk_size, num_samples)
        progress = i / num_samples
        cutoff = start_cutoff * (1 - progress) + end_cutoff * progress

        nyquist = sample_rate / 2
        norm_cutoff = max(0.01, min(cutoff / nyquist, 0.99))
        b, a = signal.butter(2, norm_cutoff, btype='low')
        output[i:end] = signal.lfilter(b, a, audio[i:end])

    return output


def simple_reverb(audio, room_size, sample_rate):
    """Simple comb filter reverb."""
    delays = [int(d * sample_rate) for d in [0.029, 0.037, 0.041, 0.043]]
    output = np.zeros(len(audio) + max(delays), dtype=np.float32)

    for delay in delays:
        comb = np.zeros(len(output), dtype=np.float32)
        feedback = room_size * 0.8

        comb[:len(audio)] = audio
        for i in range(delay, len(audio)):
            comb[i] += comb[i - delay] * feedback

        output += comb

    return output[:len(audio)] / len(delays)


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_explosion():
    """Build the explosion synthesis chain."""
    num_samples = int(SAMPLE_RATE * DURATION)
    t = np.linspace(0, DURATION, num_samples, dtype=np.float32)

    # === MAIN NOISE LAYER ===
    noise = generate_noise(NOISE_TYPE, num_samples)
    noise_env = np.exp(-t * NOISE_DECAY_RATE)
    filtered_noise = filter_sweep(noise, FILTER_START, FILTER_END, SAMPLE_RATE)
    layer_main = filtered_noise * noise_env

    # === SUB-BASS RUMBLE LAYER ===
    if SUB_ENABLED:
        sub_freq = np.linspace(SUB_FREQ, SUB_FREQ * 0.7, num_samples)
        phase = np.cumsum(2 * np.pi * sub_freq / SAMPLE_RATE)
        sub = np.sin(phase)
        sub_env = np.exp(-t * 2)
        layer_sub = sub * sub_env * SUB_MIX
    else:
        layer_sub = np.zeros(num_samples, dtype=np.float32)

    # === SIZZLE LAYER ===
    if SIZZLE_ENABLED:
        sizzle_noise = np.random.randn(num_samples).astype(np.float32)
        nyquist = SAMPLE_RATE / 2
        norm_cutoff = min(SIZZLE_FREQ / nyquist, 0.99)
        b, a = signal.butter(2, norm_cutoff, btype='high')
        sizzle = signal.filtfilt(b, a, sizzle_noise)
        sizzle_env = np.exp(-t * 5)
        layer_sizzle = sizzle * sizzle_env * SIZZLE_MIX
    else:
        layer_sizzle = np.zeros(num_samples, dtype=np.float32)

    # === MIX LAYERS ===
    mixed = layer_main + layer_sub + layer_sizzle

    # === DISTORTION ===
    if DISTORTION_ENABLED:
        gain = 1 + DISTORTION_DRIVE * 10
        mixed = np.tanh(mixed * gain)

    # === REVERB ===
    if REVERB_MIX > 0:
        reverbed = simple_reverb(mixed, REVERB_SIZE, SAMPLE_RATE)
        mixed = mixed * (1 - REVERB_MIX) + reverbed * REVERB_MIX

    return mixed.astype(np.float32)


def render():
    """Render the explosion sound to WAV file."""
    audio = build_explosion()

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.9

    sf.write(OUTPUT_FILE, audio, SAMPLE_RATE, subtype='PCM_16')
    print(f"Generated: {OUTPUT_FILE}")


# =============================================================================
# VARIATIONS
# =============================================================================

def explosion_small():
    """Small explosion - grenade, barrel."""
    global DURATION, NOISE_DECAY_RATE, SUB_ENABLED, REVERB_SIZE
    DURATION = 0.4
    NOISE_DECAY_RATE = 5
    SUB_ENABLED = False
    REVERB_SIZE = 0.4


def explosion_massive():
    """Large explosion - nuke, boss death."""
    global DURATION, NOISE_DECAY_RATE, SUB_MIX, REVERB_SIZE, DISTORTION_ENABLED
    DURATION = 1.5
    NOISE_DECAY_RATE = 2
    SUB_MIX = 0.6
    REVERB_SIZE = 0.95
    DISTORTION_ENABLED = True


def explosion_retro():
    """8-bit style explosion."""
    global NOISE_TYPE, SUB_ENABLED, SIZZLE_ENABLED, REVERB_MIX, DURATION
    NOISE_TYPE = "white"
    SUB_ENABLED = False
    SIZZLE_ENABLED = False
    REVERB_MIX = 0.1
    DURATION = 0.3


def explosion_underwater():
    """Muffled underwater explosion."""
    global FILTER_START, FILTER_END, REVERB_SIZE
    FILTER_START = 1500
    FILTER_END = 100
    REVERB_SIZE = 0.95


if __name__ == "__main__":
    # Uncomment one variation or use defaults:
    # explosion_small()
    # explosion_massive()
    # explosion_retro()
    # explosion_underwater()

    render()
