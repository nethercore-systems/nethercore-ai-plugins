#!/usr/bin/env python3
"""
Powerup Sound Effect
====================
Rising pitch with FM shimmer and chorus for magical feel.

Technique: FM synthesis + chorus + rising sweep
Character: Magical, empowering, exciting
Duration: 0.4 - 0.8 seconds
"""

from pyo import *
import time

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
CHORUS_ENABLED = True       # Chorus for width/shimmer
CHORUS_DEPTH = 0.7          # Depth (0-1)
REVERB_MIX = 0.25           # Reverb mix

# Envelope
ATTACK = 0.05               # Gradual attack
DECAY = 0.4                 # Long decay
RELEASE = 0.15              # Smooth release

# Output
DURATION = 0.6
SAMPLE_RATE = 22050
OUTPUT_FILE = "powerup.wav"


# =============================================================================
# SYNTHESIS
# =============================================================================

def build_powerup(s):
    """Build the powerup sound synthesis chain."""

    # === MAIN SWEEP ===
    env_main = Adsr(
        attack=ATTACK,
        decay=DECAY,
        sustain=0.3,
        release=RELEASE,
        dur=DURATION
    )
    env_main.play()

    # Rising frequency
    freq_sweep = Linseg([(0, START_FREQ), (SWEEP_TIME, END_FREQ)])
    freq_sweep.play()

    # Main oscillator (FM or simple)
    if FM_ENABLED:
        # FM synthesis for shimmer
        main_osc = FM(
            carrier=freq_sweep,
            ratio=FM_RATIO,
            index=FM_INDEX,
            mul=env_main
        )
    else:
        main_osc = Sine(freq=freq_sweep, mul=env_main)

    layers = [main_osc]

    # === ARPEGGIO SPARKLE ===
    if ARPEGGIO_ENABLED:
        arp_oscs = []
        arp_data = []

        for i, freq in enumerate(ARPEGGIO_NOTES):
            trig = Trig()
            env = Adsr(
                attack=0.005,
                decay=0.1,
                sustain=0,
                release=0.05,
                dur=0.12,
                trig=trig
            )
            osc = Sine(freq=freq, mul=env * ARPEGGIO_MIX)
            arp_oscs.append(osc)
            arp_data.append((trig, i * ARPEGGIO_INTERVAL))

        arp_mix = Mix(arp_oscs, voices=1)
        layers.append(arp_mix)

        # Store for triggering
        main_osc._arp_data = arp_data
    else:
        main_osc._arp_data = []

    # === MIX LAYERS ===
    mixed = Mix(layers, voices=1)

    # === EFFECTS ===
    if CHORUS_ENABLED:
        mixed = Chorus(
            mixed,
            depth=CHORUS_DEPTH,
            feedback=0.3,
            bal=0.4
        )

    if REVERB_MIX > 0:
        mixed = Freeverb(
            mixed,
            size=0.5,
            damp=0.6,
            bal=REVERB_MIX
        )

    mixed._arp_data = main_osc._arp_data
    return mixed


def render():
    """Render the powerup sound to WAV file."""
    s = Server(audio="offline")
    s.setSamplingRate(SAMPLE_RATE)
    s.setNchnls(1)
    s.boot()
    s.recordOptions(filename=OUTPUT_FILE, fileformat=0, sampletype=1)

    signal = build_powerup(s)
    signal.out()

    s.start()
    s.recstart()

    # Trigger arpeggio notes
    current_time = 0
    for trig, delay in signal._arp_data:
        wait_time = delay - current_time
        if wait_time > 0:
            time.sleep(wait_time)
            current_time = delay
        trig.play()

    time.sleep(DURATION - current_time + 0.2)
    s.recstop()
    s.stop()
    s.shutdown()

    print(f"Generated: {OUTPUT_FILE}")


# =============================================================================
# VARIATIONS
# =============================================================================

def powerup_health():
    """Health restore - gentle, warm."""
    global START_FREQ, END_FREQ, FM_ENABLED, CHORUS_DEPTH, REVERB_MIX
    START_FREQ = 300
    END_FREQ = 500
    FM_ENABLED = False
    CHORUS_DEPTH = 0.4
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
    ARPEGGIO_NOTES = [262, 392, 523, 659, 784, 1047]  # More notes


def powerup_subtle():
    """Small buff - subtle, quick."""
    global DURATION, SWEEP_TIME, ARPEGGIO_ENABLED, CHORUS_ENABLED, FM_ENABLED
    DURATION = 0.3
    SWEEP_TIME = 0.2
    ARPEGGIO_ENABLED = False
    CHORUS_ENABLED = False
    FM_ENABLED = False


def powerup_dark():
    """Dark/corrupted powerup - ominous."""
    global START_FREQ, END_FREQ, FM_RATIO, FM_INDEX
    START_FREQ = 100
    END_FREQ = 300
    FM_RATIO = 1.5
    FM_INDEX = 8.0  # More dissonant


if __name__ == "__main__":
    # Uncomment one variation or use defaults:
    # powerup_health()
    # powerup_speed()
    # powerup_ultimate()
    # powerup_subtle()
    # powerup_dark()

    render()
