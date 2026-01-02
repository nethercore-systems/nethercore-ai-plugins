#!/usr/bin/env python3
"""
UI Click Sound Effect
=====================
Very short sine blip for interface feedback.

Technique: Simple sine with ultra-short envelope
Character: Clean, responsive, non-intrusive
Duration: 0.02 - 0.08 seconds

Dependencies: pip install numpy scipy soundfile
"""

import numpy as np
import soundfile as sf

# =============================================================================
# PARAMETERS
# =============================================================================

# Tone
FREQUENCY = 800             # Click pitch (Hz)
HARMONICS = True            # Add subtle harmonics

# Envelope
ATTACK = 0.001              # Instant attack
DECAY_RATE = 80             # Very quick decay

# Character
CLICK_TYPE = "soft"         # "soft", "crisp", "woody", "digital", "heavy"

# Output
DURATION = 0.04
SAMPLE_RATE = 22050
OUTPUT_FILE = "ui_click.wav"


# =============================================================================
# CLICK TYPE PRESETS
# =============================================================================

CLICK_TYPES = {
    "soft": {
        "frequency": 600,
        "harmonics": False,
        "decay_rate": 60,
        "duration": 0.04
    },
    "crisp": {
        "frequency": 1000,
        "harmonics": True,
        "decay_rate": 100,
        "duration": 0.03
    },
    "woody": {
        "frequency": 400,
        "harmonics": True,
        "decay_rate": 50,
        "duration": 0.05
    },
    "digital": {
        "frequency": 1200,
        "harmonics": False,
        "decay_rate": 150,
        "duration": 0.02
    },
    "heavy": {
        "frequency": 300,
        "harmonics": True,
        "decay_rate": 40,
        "duration": 0.06
    }
}


def apply_click_type(click_name):
    """Apply parameters from click preset."""
    global FREQUENCY, HARMONICS, DECAY_RATE, DURATION

    if click_name in CLICK_TYPES:
        preset = CLICK_TYPES[click_name]
        FREQUENCY = preset["frequency"]
        HARMONICS = preset["harmonics"]
        DECAY_RATE = preset["decay_rate"]
        DURATION = preset["duration"]


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_click():
    """Build the UI click synthesis chain."""
    num_samples = int(SAMPLE_RATE * DURATION)
    t = np.linspace(0, DURATION, num_samples, dtype=np.float32)

    # Envelope with quick attack and decay
    attack_samples = int(ATTACK * SAMPLE_RATE)
    env = np.exp(-t * DECAY_RATE)
    if attack_samples > 0 and attack_samples < num_samples:
        env[:attack_samples] *= np.linspace(0, 1, attack_samples)

    # Main tone
    audio = np.sin(2 * np.pi * FREQUENCY * t) * env

    # Optional harmonics for presence
    if HARMONICS:
        audio += np.sin(2 * np.pi * FREQUENCY * 2 * t) * env * 0.2
        audio += np.sin(2 * np.pi * FREQUENCY * 3 * t) * env * 0.1
        audio /= 1.3  # Normalize

    return audio.astype(np.float32)


def render():
    """Render the click sound to WAV file."""
    if CLICK_TYPE in CLICK_TYPES:
        apply_click_type(CLICK_TYPE)

    audio = build_click()

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.9

    sf.write(OUTPUT_FILE, audio, SAMPLE_RATE, subtype='PCM_16')
    print(f"Generated: {OUTPUT_FILE}")


# =============================================================================
# UI SOUND VARIATIONS
# =============================================================================

def ui_hover():
    """Mouse hover - very subtle."""
    global FREQUENCY, DECAY_RATE, DURATION, HARMONICS
    FREQUENCY = 900
    DECAY_RATE = 120
    DURATION = 0.02
    HARMONICS = False


def ui_confirm():
    """Confirm/accept action - positive feel."""
    global FREQUENCY, DECAY_RATE, DURATION, HARMONICS
    FREQUENCY = 700
    DECAY_RATE = 50
    DURATION = 0.05
    HARMONICS = True


def ui_cancel():
    """Cancel/back action - slightly lower."""
    global FREQUENCY, DECAY_RATE, DURATION
    FREQUENCY = 400
    DECAY_RATE = 60
    DURATION = 0.04


def ui_error():
    """Error/invalid action - dissonant."""
    global FREQUENCY, DECAY_RATE, DURATION, OUTPUT_FILE
    FREQUENCY = 250
    DECAY_RATE = 30
    DURATION = 0.08
    OUTPUT_FILE = "ui_error.wav"


def render_ui_set(output_dir="."):
    """Render a complete UI sound set."""
    global OUTPUT_FILE, CLICK_TYPE

    # Click types
    for click_name in ["soft", "crisp", "digital"]:
        CLICK_TYPE = click_name
        OUTPUT_FILE = f"{output_dir}/ui_click_{click_name}.wav"
        render()

    # Action sounds
    OUTPUT_FILE = f"{output_dir}/ui_hover.wav"
    ui_hover()
    render()

    OUTPUT_FILE = f"{output_dir}/ui_confirm.wav"
    ui_confirm()
    render()

    OUTPUT_FILE = f"{output_dir}/ui_cancel.wav"
    ui_cancel()
    render()

    OUTPUT_FILE = f"{output_dir}/ui_error.wav"
    ui_error()
    render()


if __name__ == "__main__":
    # Set click type:
    # CLICK_TYPE = "crisp"

    # Or use a variation:
    # ui_hover()
    # ui_confirm()
    # ui_cancel()
    # ui_error()

    # Render single click
    render()

    # Or render complete UI set:
    # render_ui_set("generated/audio/ui")
