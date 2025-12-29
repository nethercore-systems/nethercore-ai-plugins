#!/usr/bin/env python3
"""
Basic XM Generation Example

Generates a simple 4-channel drum loop with kick, snare, and hi-hat.
Demonstrates the core xm_writer API.

Usage:
    python basic_xm.py

Output:
    drum_loop.xm - Valid FastTracker 2 XM file

Integration with Nethercore:
    1. Add samples to nether.toml with matching IDs:
       [[assets.sounds]]
       id = "kick"
       path = "samples/kick.wav"

    2. Add the generated XM:
       [[assets.trackers]]
       id = "drum_loop"
       path = "music/drum_loop.xm"

    3. Play in game:
       music_play(rom_tracker(b"drum_loop", 9), 0.8, 1)
"""

import sys
from pathlib import Path

# Add scripts directory to path for import
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from xm_writer import (
    XmModule, XmPattern, XmNote, XmInstrument,
    write_xm, validate_xm
)


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
    # Define instruments (names MUST match [[assets.sounds]] IDs in nether.toml)
    instruments = [
        XmInstrument(name="kick"),
        XmInstrument(name="snare"),
        XmInstrument(name="hihat"),
    ]

    # Create patterns
    patterns = [
        create_drum_pattern(64),  # Main loop
    ]

    # Build module
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
    write_xm(module, output_path)

    # Validate the output
    try:
        validate_xm(output_path)
        print(f"Created: {output_path}")
        print(f"  Channels: {module.num_channels}")
        print(f"  Patterns: {len(module.patterns)}")
        print(f"  Instruments: {len(module.instruments)}")
        print(f"  Tempo: {module.default_bpm} BPM, speed {module.default_speed}")
        print("\nInstrument names (must match nether.toml [[assets.sounds]] IDs):")
        for i, inst in enumerate(instruments, 1):
            print(f"  {i}: {inst.name}")
    except ValueError as e:
        print(f"Validation failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
