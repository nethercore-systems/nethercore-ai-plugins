#!/usr/bin/env python3
"""
Hit/Punch Sound Effect
======================
Short noise burst with quick lowpass and body thump.

Technique: Noise + sine transient, heavily filtered
Character: Impactful, physical, weighty
Duration: 0.05 - 0.2 seconds
"""

from pyo import *
import time

# =============================================================================
# PARAMETERS
# =============================================================================

# Transient (the initial "thwack")
TRANSIENT_FREQ = 100        # Low thump frequency (Hz)
TRANSIENT_DECAY = 0.03      # Very quick decay

# Noise layer (the "texture")
NOISE_TYPE = "white"        # "white" for sharp, "pink" for softer
NOISE_DECAY = 0.08          # Noise decay time
NOISE_MIX = 0.6             # Mix level (0-1)

# Filter
FILTER_FREQ = 1500          # Cutoff frequency (Hz)
FILTER_RES = 0.5            # Resonance (adds punch)
FILTER_SWEEP = True         # Sweep filter down
FILTER_END = 300            # Ending cutoff if sweeping

# Body (low-end weight)
BODY_ENABLED = True         # Add low-end thump
BODY_FREQ = 80              # Body frequency (Hz)
BODY_MIX = 0.4              # Body mix level

# Envelope
ATTACK = 0.001              # Instant attack
TOTAL_DURATION = 0.1        # Total length

# Compression (for punch)
COMPRESS = True             # Use compression
COMPRESS_RATIO = 6          # Compression ratio

# Output
SAMPLE_RATE = 22050
OUTPUT_FILE = "hit.wav"


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_hit(s):
    """Build the hit sound synthesis chain."""

    # === TRANSIENT LAYER ===
    trans_env = Adsr(
        attack=ATTACK,
        decay=TRANSIENT_DECAY,
        sustain=0,
        release=0.01,
        dur=TRANSIENT_DECAY + 0.02
    )
    trans_env.play()

    transient = Sine(freq=TRANSIENT_FREQ, mul=trans_env)

    # === NOISE LAYER ===
    noise_env = Adsr(
        attack=ATTACK,
        decay=NOISE_DECAY,
        sustain=0,
        release=0.02,
        dur=NOISE_DECAY + 0.03
    )
    noise_env.play()

    if NOISE_TYPE == "pink":
        noise = PinkNoise(mul=noise_env * NOISE_MIX)
    else:
        noise = Noise(mul=noise_env * NOISE_MIX)

    # Filter the noise
    if FILTER_SWEEP:
        filt_freq = Linseg([(0, FILTER_FREQ), (NOISE_DECAY, FILTER_END)])
        filt_freq.play()
    else:
        filt_freq = FILTER_FREQ

    filtered_noise = MoogLP(noise, freq=filt_freq, res=FILTER_RES)

    # === BODY LAYER ===
    if BODY_ENABLED:
        body_env = Adsr(
            attack=ATTACK,
            decay=0.05,
            sustain=0,
            release=0.02,
            dur=0.08
        )
        body_env.play()

        body = Sine(freq=BODY_FREQ, mul=body_env * BODY_MIX)
    else:
        body = Sig(0)

    # === MIX ===
    mixed = Mix([transient, filtered_noise, body], voices=1)

    # === COMPRESSION ===
    if COMPRESS:
        mixed = Compress(
            mixed,
            thresh=-20,
            ratio=COMPRESS_RATIO,
            risetime=0.001,
            falltime=0.05,
            mul=1.2
        )

    return mixed


def render():
    """Render the hit sound to WAV file."""
    s = Server(audio="offline")
    s.setSamplingRate(SAMPLE_RATE)
    s.setNchnls(1)
    s.boot()
    s.recordOptions(filename=OUTPUT_FILE, fileformat=0, sampletype=1)

    signal = build_hit(s)
    signal.out()

    s.start()
    s.recstart()
    time.sleep(TOTAL_DURATION + 0.05)
    s.recstop()
    s.stop()
    s.shutdown()

    print(f"Generated: {OUTPUT_FILE}")


# =============================================================================
# VARIATIONS
# =============================================================================

def hit_punch():
    """Heavy punch - more body, longer tail."""
    global BODY_MIX, BODY_FREQ, NOISE_DECAY, TOTAL_DURATION
    BODY_MIX = 0.6
    BODY_FREQ = 60
    NOISE_DECAY = 0.12
    TOTAL_DURATION = 0.15


def hit_slap():
    """Sharp slap - more high-end, less body."""
    global BODY_ENABLED, FILTER_FREQ, NOISE_TYPE, NOISE_DECAY
    BODY_ENABLED = False
    FILTER_FREQ = 3000
    NOISE_TYPE = "white"
    NOISE_DECAY = 0.05


def hit_sword():
    """Sword clash - metallic ring."""
    global TRANSIENT_FREQ, FILTER_FREQ, FILTER_RES, NOISE_MIX
    TRANSIENT_FREQ = 400
    FILTER_FREQ = 4000
    FILTER_RES = 0.7
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
    global TOTAL_DURATION, NOISE_DECAY, BODY_ENABLED, NOISE_MIX
    TOTAL_DURATION = 0.05
    NOISE_DECAY = 0.03
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
