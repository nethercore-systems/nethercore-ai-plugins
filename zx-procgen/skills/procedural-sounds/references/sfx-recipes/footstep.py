#!/usr/bin/env python3
"""
Footstep Sound Effect
=====================
Filtered noise thump with surface character.

Technique: Noise burst with aggressive filtering
Character: Physical, grounded, varied by surface
Duration: 0.05 - 0.15 seconds

Dependencies: pip install numpy scipy soundfile
"""

import numpy as np
import soundfile as sf
from scipy import signal

# =============================================================================
# PARAMETERS
# =============================================================================

# Surface type presets (choose one or customize)
SURFACE = "concrete"        # "concrete", "grass", "wood", "metal", "gravel", "water", "snow"

# Noise source
NOISE_TYPE = "pink"         # "white", "pink"

# Filter settings
FILTER_FREQ = 600           # Cutoff frequency (Hz)

# Body thump
BODY_ENABLED = True         # Add low-end thump
BODY_FREQ = 60              # Body frequency
BODY_MIX = 0.4              # Body level

# Envelope
DECAY_RATE = 40             # Exponential decay rate

# Output
DURATION = 0.08
SAMPLE_RATE = 22050
OUTPUT_FILE = "footstep.wav"


# =============================================================================
# SURFACE PRESETS
# =============================================================================

SURFACES = {
    "concrete": {
        "noise_type": "pink",
        "filter_freq": 600,
        "body_freq": 60,
        "body_mix": 0.5,
        "decay_rate": 40,
        "duration": 0.07
    },
    "grass": {
        "noise_type": "white",
        "filter_freq": 3000,
        "body_freq": 40,
        "body_mix": 0.2,
        "decay_rate": 30,
        "duration": 0.09
    },
    "wood": {
        "noise_type": "pink",
        "filter_freq": 1200,
        "body_freq": 80,
        "body_mix": 0.6,
        "decay_rate": 35,
        "duration": 0.08
    },
    "metal": {
        "noise_type": "white",
        "filter_freq": 4000,
        "body_freq": 200,
        "body_mix": 0.3,
        "decay_rate": 25,
        "duration": 0.12
    },
    "gravel": {
        "noise_type": "white",
        "filter_freq": 5000,
        "body_freq": 50,
        "body_mix": 0.3,
        "decay_rate": 28,
        "duration": 0.1
    },
    "water": {
        "noise_type": "pink",
        "filter_freq": 2000,
        "body_freq": 100,
        "body_mix": 0.5,
        "decay_rate": 20,
        "duration": 0.15
    },
    "snow": {
        "noise_type": "white",
        "filter_freq": 1500,
        "body_freq": 40,
        "body_mix": 0.1,
        "decay_rate": 45,
        "duration": 0.06
    }
}


def apply_surface_preset(surface_name):
    """Apply parameters from surface preset."""
    global NOISE_TYPE, FILTER_FREQ, BODY_FREQ, BODY_MIX, DECAY_RATE, DURATION

    if surface_name in SURFACES:
        preset = SURFACES[surface_name]
        NOISE_TYPE = preset["noise_type"]
        FILTER_FREQ = preset["filter_freq"]
        BODY_FREQ = preset["body_freq"]
        BODY_MIX = preset["body_mix"]
        DECAY_RATE = preset["decay_rate"]
        DURATION = preset["duration"]


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


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_footstep():
    """Build the footstep sound synthesis chain."""
    num_samples = int(SAMPLE_RATE * DURATION)
    t = np.linspace(0, DURATION, num_samples, dtype=np.float32)

    # Main noise
    noise = generate_noise(NOISE_TYPE, num_samples)
    env = np.exp(-t * DECAY_RATE)

    # Filter
    nyquist = SAMPLE_RATE / 2
    normalized_cutoff = min(FILTER_FREQ / nyquist, 0.99)
    b, a = signal.butter(2, normalized_cutoff, btype='low')
    filtered = signal.filtfilt(b, a, noise)
    layer_main = filtered * env

    # Body thump
    if BODY_ENABLED:
        body_env = np.exp(-t * DECAY_RATE * 0.8)
        body = np.sin(2 * np.pi * BODY_FREQ * t) * body_env * BODY_MIX
    else:
        body = np.zeros(num_samples, dtype=np.float32)

    # Mix
    audio = layer_main + body

    return audio.astype(np.float32)


def render():
    """Render the footstep sound to WAV file."""
    # Apply surface preset if specified
    if SURFACE in SURFACES:
        apply_surface_preset(SURFACE)

    audio = build_footstep()

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.9

    sf.write(OUTPUT_FILE, audio, SAMPLE_RATE, subtype='PCM_16')
    print(f"Generated: {OUTPUT_FILE}")


def render_all_surfaces(output_dir="."):
    """Render footsteps for all surfaces."""
    global OUTPUT_FILE

    for surface_name in SURFACES:
        apply_surface_preset(surface_name)
        OUTPUT_FILE = f"{output_dir}/footstep_{surface_name}.wav"
        render()


# =============================================================================
# VARIATIONS
# =============================================================================

def footstep_heavy():
    """Heavy character - armored, large."""
    global BODY_MIX, BODY_FREQ, DECAY_RATE, DURATION
    BODY_MIX = 0.7
    BODY_FREQ = 40
    DECAY_RATE = 25
    DURATION = 0.12


def footstep_light():
    """Light character - nimble, quiet."""
    global BODY_MIX, DECAY_RATE, DURATION, FILTER_FREQ
    BODY_MIX = 0.2
    DECAY_RATE = 50
    DURATION = 0.05
    FILTER_FREQ = 2000


def footstep_running():
    """Running footstep - quicker, lighter."""
    global DECAY_RATE, DURATION, BODY_MIX
    DECAY_RATE = 60
    DURATION = 0.04
    BODY_MIX = 0.3


if __name__ == "__main__":
    # Set surface type (or call apply_surface_preset directly)
    # SURFACE = "wood"

    # Or uncomment a variation:
    # footstep_heavy()
    # footstep_light()
    # footstep_running()

    # Render single footstep
    render()

    # Or render all surfaces:
    # render_all_surfaces("assets/audio/footsteps")
