#!/usr/bin/env python3
"""
Footstep Sound Effect
=====================
Filtered noise thump with surface character.

Technique: Noise burst with aggressive filtering
Character: Physical, grounded, varied by surface
Duration: 0.05 - 0.15 seconds
"""

from pyo import *
import time

# =============================================================================
# PARAMETERS
# =============================================================================

# Surface type presets (choose one or customize)
SURFACE = "concrete"        # "concrete", "grass", "wood", "metal", "gravel"

# Noise source
NOISE_TYPE = "pink"         # "white", "pink", "brown"

# Filter settings
FILTER_FREQ = 600           # Cutoff frequency (Hz)
FILTER_RES = 0.3            # Resonance

# Body thump
BODY_ENABLED = True         # Add low-end thump
BODY_FREQ = 60              # Body frequency
BODY_MIX = 0.4              # Body level

# Envelope
ATTACK = 0.001              # Instant
DECAY = 0.04                # Quick decay
RELEASE = 0.02              # Short release

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
        "filter_res": 0.3,
        "body_freq": 60,
        "body_mix": 0.5,
        "decay": 0.04,
        "duration": 0.07
    },
    "grass": {
        "noise_type": "white",
        "filter_freq": 3000,
        "filter_res": 0.1,
        "body_freq": 40,
        "body_mix": 0.2,
        "decay": 0.06,
        "duration": 0.09
    },
    "wood": {
        "noise_type": "pink",
        "filter_freq": 1200,
        "filter_res": 0.5,
        "body_freq": 80,
        "body_mix": 0.6,
        "decay": 0.05,
        "duration": 0.08
    },
    "metal": {
        "noise_type": "white",
        "filter_freq": 4000,
        "filter_res": 0.6,
        "body_freq": 200,
        "body_mix": 0.3,
        "decay": 0.08,
        "duration": 0.12
    },
    "gravel": {
        "noise_type": "white",
        "filter_freq": 5000,
        "filter_res": 0.2,
        "body_freq": 50,
        "body_mix": 0.3,
        "decay": 0.07,
        "duration": 0.1
    },
    "water": {
        "noise_type": "pink",
        "filter_freq": 2000,
        "filter_res": 0.4,
        "body_freq": 100,
        "body_mix": 0.5,
        "decay": 0.1,
        "duration": 0.15
    },
    "snow": {
        "noise_type": "white",
        "filter_freq": 1500,
        "filter_res": 0.1,
        "body_freq": 40,
        "body_mix": 0.1,
        "decay": 0.05,
        "duration": 0.06
    }
}


def apply_surface_preset(surface_name):
    """Apply parameters from surface preset."""
    global NOISE_TYPE, FILTER_FREQ, FILTER_RES, BODY_FREQ, BODY_MIX, DECAY, DURATION

    if surface_name in SURFACES:
        preset = SURFACES[surface_name]
        NOISE_TYPE = preset["noise_type"]
        FILTER_FREQ = preset["filter_freq"]
        FILTER_RES = preset["filter_res"]
        BODY_FREQ = preset["body_freq"]
        BODY_MIX = preset["body_mix"]
        DECAY = preset["decay"]
        DURATION = preset["duration"]


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_footstep(s):
    """Build the footstep sound synthesis chain."""

    # Main noise envelope
    env = Adsr(
        attack=ATTACK,
        decay=DECAY,
        sustain=0,
        release=RELEASE,
        dur=DURATION
    )
    env.play()

    # Noise source
    if NOISE_TYPE == "white":
        noise = Noise(mul=env)
    elif NOISE_TYPE == "brown":
        noise = BrownNoise(mul=env)
    else:
        noise = PinkNoise(mul=env)

    # Filter
    filtered = MoogLP(noise, freq=FILTER_FREQ, res=FILTER_RES)

    # Body thump
    if BODY_ENABLED:
        body_env = Adsr(
            attack=ATTACK,
            decay=DECAY * 0.8,
            sustain=0,
            release=RELEASE,
            dur=DURATION * 0.8
        )
        body_env.play()

        body = Sine(freq=BODY_FREQ, mul=body_env * BODY_MIX)
    else:
        body = Sig(0)

    # Mix
    mixed = Mix([filtered, body], voices=1)

    return mixed


def render():
    """Render the footstep sound to WAV file."""
    # Apply surface preset if specified
    if SURFACE in SURFACES:
        apply_surface_preset(SURFACE)

    s = Server(audio="offline")
    s.setSamplingRate(SAMPLE_RATE)
    s.setNchnls(1)
    s.boot()
    s.recordOptions(filename=OUTPUT_FILE, fileformat=0, sampletype=1)

    signal = build_footstep(s)
    signal.out()

    s.start()
    s.recstart()
    time.sleep(DURATION + 0.05)
    s.recstop()
    s.stop()
    s.shutdown()

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
    global BODY_MIX, BODY_FREQ, DECAY, DURATION
    BODY_MIX = 0.7
    BODY_FREQ = 40
    DECAY = 0.08
    DURATION = 0.12


def footstep_light():
    """Light character - nimble, quiet."""
    global BODY_MIX, DECAY, DURATION, FILTER_FREQ
    BODY_MIX = 0.2
    DECAY = 0.03
    DURATION = 0.05
    FILTER_FREQ = 2000


def footstep_running():
    """Running footstep - quicker, lighter."""
    global DECAY, DURATION, BODY_MIX
    DECAY = 0.025
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
