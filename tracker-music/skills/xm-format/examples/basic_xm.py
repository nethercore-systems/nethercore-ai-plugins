#!/usr/bin/env python3
"""
Basic XM Generation Example

Generates a simple 4-channel drum loop with embedded samples.
This is the DEFAULT workflow - always generate samples!

Prerequisites:
    Run /init-procgen or /init-tracker-music to set up .studio/parsers/
    Then copy this example to your project root to run it.

Usage:
    python basic_xm.py

Output:
    drum_loop.xm - Valid FastTracker 2 XM file with embedded samples

Integration with Nethercore:
    Just add the XM file to nether.toml - samples are auto-extracted!

    [[assets.trackers]]
    id = "drum_loop"
    path = "music/drum_loop.xm"

    In game:
    music_play(rom_tracker(b"drum_loop", 9), 0.8, 1)
"""

import sys
import math
from pathlib import Path

# Add .studio/parsers to path (set up via /init-procgen or /init-tracker-music)
parsers_path = Path(".studio/parsers")
if parsers_path.exists():
    sys.path.insert(0, str(parsers_path))

from xm_writer import (
    XmModule, XmPattern, XmNote, XmInstrument,
    write_xm, validate_xm, calculate_pitch_correction, ZX_SAMPLE_RATE
)


# ============================================================================
# Simple Sample Generators
# ============================================================================

import struct

def generate_kick_sample(sample_rate: int = ZX_SAMPLE_RATE) -> bytes:
    """
    Generate a simple kick drum sample (sine sweep).

    Returns 16-bit signed little-endian PCM data.
    """
    duration = int(sample_rate * 0.15)  # 150ms
    samples = []

    for i in range(duration):
        t = i / sample_rate
        # Frequency sweep from 150Hz to 40Hz
        freq = 150 * (1 - t / 0.15) + 40
        # Exponential decay
        amp = math.exp(-t * 15)
        value = math.sin(2 * math.pi * freq * t) * amp
        samples.append(int(value * 32767))

    # Convert to 16-bit little-endian bytes
    return struct.pack(f"<{len(samples)}h", *samples)


def generate_snare_sample(sample_rate: int = ZX_SAMPLE_RATE) -> bytes:
    """
    Generate a simple snare drum sample (noise + tone).

    Returns 16-bit signed little-endian PCM data.
    """
    import random
    duration = int(sample_rate * 0.1)  # 100ms
    samples = []

    for i in range(duration):
        t = i / sample_rate
        # Noise component
        noise = random.uniform(-1, 1)
        # Tone component (200Hz)
        tone = math.sin(2 * math.pi * 200 * t) * 0.3
        # Exponential decay
        amp = math.exp(-t * 25)
        value = (noise * 0.7 + tone * 0.3) * amp
        samples.append(int(value * 32767))

    return struct.pack(f"<{len(samples)}h", *samples)


def generate_hihat_sample(sample_rate: int = ZX_SAMPLE_RATE) -> bytes:
    """
    Generate a simple hi-hat sample (filtered noise).

    Returns 16-bit signed little-endian PCM data.
    """
    import random
    duration = int(sample_rate * 0.05)  # 50ms
    samples = []

    for i in range(duration):
        t = i / sample_rate
        # High-passed noise
        noise = random.uniform(-1, 1)
        # Sharp decay
        amp = math.exp(-t * 50)
        value = noise * amp
        samples.append(int(value * 32767))

    return struct.pack(f"<{len(samples)}h", *samples)


# ============================================================================
# Pattern Creation
# ============================================================================

def create_drum_pattern(num_rows: int = 64) -> XmPattern:
    """
    Create a basic 4/4 drum pattern.

    Channel layout:
      Ch 1: Kick (on beats 1 and 3)
      Ch 2: Snare (on beats 2 and 4)
      Ch 3: Hi-hat (every 2 rows, open on offbeats)
      Ch 4: (empty, for expansion)
    """
    pattern = XmPattern.empty(num_rows, num_channels=4)

    for row in range(num_rows):
        # Kick on beats 1 and 3 (rows 0, 32 in a 64-row pattern at speed 6)
        if row % 32 == 0:
            pattern.set_note(row, 0, XmNote.play("C-4", instrument=1, volume=64))

        # Snare on beats 2 and 4 (rows 16, 48)
        if row % 32 == 16:
            pattern.set_note(row, 1, XmNote.play("C-4", instrument=2, volume=60))

        # Hi-hat every 4 rows, alternating closed/open
        if row % 4 == 0:
            vol = 48 if row % 8 == 0 else 32  # Accent on downbeats
            pattern.set_note(row, 2, XmNote.play("C-4", instrument=3, volume=vol))

    return pattern


def main():
    print("Generating drum samples...")

    # Generate sample data
    kick_sample = generate_kick_sample()
    snare_sample = generate_snare_sample()
    hihat_sample = generate_hihat_sample()

    print(f"  Kick: {len(kick_sample)} bytes")
    print(f"  Snare: {len(snare_sample)} bytes")
    print(f"  Hi-hat: {len(hihat_sample)} bytes")

    # Define instruments WITH embedded samples
    # Using sample_rate=ZX_SAMPLE_RATE auto-calculates finetune and relative_note
    # so samples play at the correct pitch (essential for ZX 22050 Hz samples!)
    instruments = [
        XmInstrument.for_zx(  # Convenience constructor for ZX samples
            name="kick",
            sample_data=kick_sample,
            sample_loop_type=0  # One-shot
        ),
        XmInstrument(  # Explicit sample_rate approach
            name="snare",
            sample_data=snare_sample,
            sample_rate=ZX_SAMPLE_RATE,  # Auto-calculates pitch correction
            sample_bits=16,
            sample_loop_type=0  # One-shot
        ),
        XmInstrument(
            name="hihat",
            sample_data=hihat_sample,
            sample_rate=ZX_SAMPLE_RATE,
            sample_bits=16,
            sample_loop_type=0  # One-shot
        ),
    ]

    # Show pitch correction info
    finetune, relative_note = calculate_pitch_correction(ZX_SAMPLE_RATE)
    print(f"\nPitch correction for {ZX_SAMPLE_RATE} Hz samples:")
    print(f"  finetune={finetune}, relative_note={relative_note}")
    print(f"  (auto-calculated when sample_rate is set)")

    # Create patterns
    patterns = [
        create_drum_pattern(64),  # Main loop
    ]

    # Build module
    print("\nBuilding XM module...")
    module = XmModule(
        name="Drum Loop",
        num_channels=4,
        default_speed=6,      # Ticks per row
        default_bpm=120,      # Beats per minute
        restart_position=0,   # Loop from start
        order_table=[0],      # Just pattern 0, looping
        patterns=patterns,
        instruments=instruments,
    )

    # Write XM file
    output_path = "drum_loop.xm"
    print(f"Writing {output_path}...")
    write_xm(module, output_path)

    # Validate the output
    try:
        validate_xm(output_path)
        print(f"\n[OK] Created: {output_path}")
        print(f"  Channels: {module.num_channels}")
        print(f"  Patterns: {len(module.patterns)}")
        print(f"  Instruments: {len(module.instruments)}")
        print(f"  Tempo: {module.default_bpm} BPM, speed {module.default_speed}")
        print("\nInstruments with embedded samples:")
        for i, inst in enumerate(instruments, 1):
            size = len(inst.sample_data) if inst.sample_data else 0
            print(f"  {i}: {inst.name} ({size} bytes)")
        print("\nSamples are embedded! Just add XM to nether.toml - no separate [[assets.sounds]] needed.")
    except ValueError as e:
        print(f"[ERROR] Validation failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
