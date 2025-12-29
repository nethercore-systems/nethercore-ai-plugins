#!/usr/bin/env python3
"""
Explosion Sound Effect
======================
Noise burst with lowpass sweep, sub-bass rumble, and reverb.

Technique: Layered subtractive synthesis
Character: Impactful, cinematic, weighty
Duration: 0.5 - 1.5 seconds
"""

from pyo import *
import time

# =============================================================================
# PARAMETERS
# =============================================================================

# Main noise layer
NOISE_TYPE = "pink"         # "white", "pink", or "brown"
NOISE_ATTACK = 0.01         # Quick attack for punch
NOISE_DECAY = 0.5           # Main decay time
NOISE_RELEASE = 0.3         # Tail release

# Filter sweep
FILTER_START = 3000         # Starting cutoff (Hz)
FILTER_END = 200            # Ending cutoff (Hz)
FILTER_SWEEP_TIME = 0.5     # How fast filter closes
FILTER_RES = 0.4            # Resonance (adds punch)

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
REVERB_DAMP = 0.5           # Damping (0-1)
REVERB_MIX = 0.3            # Wet/dry mix

# Distortion (optional grit)
DISTORTION_ENABLED = False  # Enable distortion
DISTORTION_DRIVE = 0.7      # Drive amount (0-1)

# Output
DURATION = 0.9              # Total duration
SAMPLE_RATE = 22050
OUTPUT_FILE = "explosion.wav"


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_explosion(s):
    """Build the explosion synthesis chain."""

    # === MAIN NOISE LAYER ===
    env_noise = Adsr(
        attack=NOISE_ATTACK,
        decay=NOISE_DECAY,
        sustain=0,
        release=NOISE_RELEASE,
        dur=DURATION - 0.1
    )
    env_noise.play()

    # Select noise type
    if NOISE_TYPE == "white":
        noise = Noise(mul=env_noise)
    elif NOISE_TYPE == "brown":
        noise = BrownNoise(mul=env_noise)
    else:  # pink
        noise = PinkNoise(mul=env_noise)

    # Filter sweep - closes down over time
    filter_sweep = Linseg([(0, FILTER_START), (FILTER_SWEEP_TIME, FILTER_END)])
    filter_sweep.play()

    filtered_noise = MoogLP(noise, freq=filter_sweep, res=FILTER_RES)

    # === SUB-BASS RUMBLE LAYER ===
    if SUB_ENABLED:
        env_sub = Adsr(
            attack=0.02,
            decay=0.4,
            sustain=0.2,
            release=0.3,
            dur=DURATION - 0.1
        )
        env_sub.play()

        # Low sine with slight pitch drop
        sub_freq = Linseg([(0, SUB_FREQ), (0.5, SUB_FREQ * 0.7)])
        sub_freq.play()

        sub = Sine(freq=sub_freq, mul=env_sub * SUB_MIX)
    else:
        sub = Sig(0)

    # === SIZZLE LAYER (high-frequency debris) ===
    if SIZZLE_ENABLED:
        env_sizzle = Adsr(
            attack=0.01,
            decay=0.3,
            sustain=0.1,
            release=0.4,
            dur=DURATION - 0.1
        )
        env_sizzle.play()

        sizzle_noise = Noise(mul=env_sizzle * SIZZLE_MIX)
        sizzle = ButHP(sizzle_noise, freq=SIZZLE_FREQ)
    else:
        sizzle = Sig(0)

    # === MIX LAYERS ===
    mixed = Mix([filtered_noise, sub, sizzle], voices=1)

    # === DISTORTION (optional) ===
    if DISTORTION_ENABLED:
        mixed = Disto(mixed, drive=DISTORTION_DRIVE, slope=0.8)

    # === REVERB ===
    reverbed = Freeverb(
        mixed,
        size=REVERB_SIZE,
        damp=REVERB_DAMP,
        bal=REVERB_MIX
    )

    # Soft limiting to prevent clipping
    output = Compress(
        reverbed,
        thresh=-12,
        ratio=4,
        risetime=0.01,
        falltime=0.1,
        mul=0.8
    )

    return output


def render():
    """Render the explosion sound to WAV file."""
    s = Server(audio="offline")
    s.setSamplingRate(SAMPLE_RATE)
    s.setNchnls(1)
    s.boot()
    s.recordOptions(filename=OUTPUT_FILE, fileformat=0, sampletype=1)

    signal = build_explosion(s)
    signal.out()

    s.start()
    s.recstart()
    time.sleep(DURATION + 0.2)
    s.recstop()
    s.stop()
    s.shutdown()

    print(f"Generated: {OUTPUT_FILE}")


# =============================================================================
# VARIATIONS
# =============================================================================

def explosion_small():
    """Small explosion - grenade, barrel."""
    global DURATION, NOISE_DECAY, SUB_ENABLED, REVERB_SIZE
    DURATION = 0.4
    NOISE_DECAY = 0.2
    SUB_ENABLED = False
    REVERB_SIZE = 0.4


def explosion_massive():
    """Large explosion - nuke, boss death."""
    global DURATION, NOISE_DECAY, SUB_MIX, REVERB_SIZE, DISTORTION_ENABLED
    DURATION = 1.5
    NOISE_DECAY = 0.8
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
    global FILTER_START, FILTER_END, REVERB_SIZE, REVERB_DAMP
    FILTER_START = 1500
    FILTER_END = 100
    REVERB_SIZE = 0.95
    REVERB_DAMP = 0.8


if __name__ == "__main__":
    # Uncomment one variation or use defaults:
    # explosion_small()
    # explosion_massive()
    # explosion_retro()
    # explosion_underwater()

    render()
