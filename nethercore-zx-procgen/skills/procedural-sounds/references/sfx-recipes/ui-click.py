#!/usr/bin/env python3
"""
UI Click Sound Effect
=====================
Very short sine blip for interface feedback.

Technique: Simple sine with ultra-short envelope
Character: Clean, responsive, non-intrusive
Duration: 0.02 - 0.08 seconds
"""

from pyo import *
import time

# =============================================================================
# PARAMETERS
# =============================================================================

# Tone
FREQUENCY = 800             # Click pitch (Hz)
HARMONICS = True            # Add subtle harmonics

# Envelope
ATTACK = 0.001              # Instant
DECAY = 0.02                # Very quick
RELEASE = 0.01              # Minimal tail

# Character
CLICK_TYPE = "soft"         # "soft", "crisp", "woody", "digital"

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
        "attack": 0.002,
        "decay": 0.025,
        "duration": 0.04
    },
    "crisp": {
        "frequency": 1000,
        "harmonics": True,
        "attack": 0.001,
        "decay": 0.015,
        "duration": 0.03
    },
    "woody": {
        "frequency": 400,
        "harmonics": True,
        "attack": 0.001,
        "decay": 0.035,
        "duration": 0.05
    },
    "digital": {
        "frequency": 1200,
        "harmonics": False,
        "attack": 0.0005,
        "decay": 0.01,
        "duration": 0.02
    },
    "heavy": {
        "frequency": 300,
        "harmonics": True,
        "attack": 0.002,
        "decay": 0.04,
        "duration": 0.06
    }
}


def apply_click_type(click_name):
    """Apply parameters from click preset."""
    global FREQUENCY, HARMONICS, ATTACK, DECAY, DURATION

    if click_name in CLICK_TYPES:
        preset = CLICK_TYPES[click_name]
        FREQUENCY = preset["frequency"]
        HARMONICS = preset["harmonics"]
        ATTACK = preset["attack"]
        DECAY = preset["decay"]
        DURATION = preset["duration"]


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_click(s):
    """Build the UI click synthesis chain."""

    env = Adsr(
        attack=ATTACK,
        decay=DECAY,
        sustain=0,
        release=RELEASE,
        dur=DURATION
    )
    env.play()

    # Main tone
    osc = Sine(freq=FREQUENCY, mul=env)

    # Optional harmonics for presence
    if HARMONICS:
        harm1 = Sine(freq=FREQUENCY * 2, mul=env * 0.2)
        harm2 = Sine(freq=FREQUENCY * 3, mul=env * 0.1)
        osc = Mix([osc, harm1, harm2], voices=1)

    return osc


def render():
    """Render the click sound to WAV file."""
    if CLICK_TYPE in CLICK_TYPES:
        apply_click_type(CLICK_TYPE)

    s = Server(audio="offline")
    s.setSamplingRate(SAMPLE_RATE)
    s.setNchnls(1)
    s.boot()
    s.recordOptions(filename=OUTPUT_FILE, fileformat=0, sampletype=1)

    signal = build_click(s)
    signal.out()

    s.start()
    s.recstart()
    time.sleep(DURATION + 0.02)
    s.recstop()
    s.stop()
    s.shutdown()

    print(f"Generated: {OUTPUT_FILE}")


# =============================================================================
# UI SOUND VARIATIONS
# =============================================================================

def ui_hover():
    """Mouse hover - very subtle."""
    global FREQUENCY, DECAY, DURATION, HARMONICS
    FREQUENCY = 900
    DECAY = 0.01
    DURATION = 0.02
    HARMONICS = False


def ui_confirm():
    """Confirm/accept action - positive feel."""
    global FREQUENCY, DECAY, DURATION, HARMONICS
    FREQUENCY = 700
    DECAY = 0.03
    DURATION = 0.05
    HARMONICS = True


def ui_cancel():
    """Cancel/back action - slightly lower."""
    global FREQUENCY, DECAY, DURATION
    FREQUENCY = 400
    DECAY = 0.025
    DURATION = 0.04


def ui_error():
    """Error/invalid action - dissonant."""
    global FREQUENCY, DECAY, DURATION, OUTPUT_FILE
    FREQUENCY = 250
    DECAY = 0.06
    DURATION = 0.08
    OUTPUT_FILE = "ui_error.wav"


def ui_toggle_on():
    """Toggle switch on - rising pitch."""
    # This needs custom synthesis for pitch change
    pass


def ui_toggle_off():
    """Toggle switch off - falling pitch."""
    pass


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
    # render_ui_set("assets/audio/ui")
