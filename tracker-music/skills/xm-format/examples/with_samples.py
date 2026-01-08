#!/usr/bin/env python3
"""
XM Generation with Embedded Samples

Demonstrates the recommended workflow: generating XM files with embedded sample data.
Includes simple waveform generators (sine, square, sawtooth) for demonstration.

For complex synthesis (FM, Karplus-Strong, subtractive), use the procedural-sounds skill!

Prerequisites:
    Run /init-procgen to set up .studio/parsers/
    Then copy this example to your project root to run it.

Usage:
    python with_samples.py

Output:
    synth_loop.xm - Valid FastTracker 2 XM file with embedded 8-bit and 16-bit samples

Integration with Nethercore:
    No separate [[assets.sounds]] entries needed! Just add the XM file:

    [[assets.trackers]]
    id = "synth_loop"
    path = "music/synth_loop.xm"

    At pack time, nether-cli automatically extracts samples from the XM file,
    converts them to ROM format, and makes them available via rom_sound().
"""

import sys
import math
from pathlib import Path

# Add .studio/parsers to path (set up via /init-procgen)
parsers_path = Path(".studio/parsers")
if parsers_path.exists():
    sys.path.insert(0, str(parsers_path))

from xm_writer import (
    XmModule, XmPattern, XmNote, XmInstrument,
    write_xm, validate_xm
)


# ============================================================================
# Simple Waveform Generators
# For production use, consider the procedural-sounds skill for complex synthesis!
# ============================================================================

def generate_sine_wave_8bit(frequency: float, duration_samples: int, sample_rate: int = 22050) -> bytes:
    """
    Generate an 8-bit signed sine wave.

    Args:
        frequency: Frequency in Hz
        duration_samples: Length in samples
        sample_rate: Sample rate (default 22050 Hz)

    Returns:
        8-bit signed PCM data (int8, -128 to 127)
    """
    samples = []
    for i in range(duration_samples):
        t = i / sample_rate
        value = math.sin(2 * math.pi * frequency * t)
        # Scale to 8-bit signed range
        sample = int(value * 127)
        samples.append(sample & 0xFF)  # Convert to unsigned byte representation

    return bytes(samples)


def generate_square_wave_8bit(frequency: float, duration_samples: int, sample_rate: int = 22050) -> bytes:
    """Generate an 8-bit signed square wave."""
    samples = []
    period_samples = sample_rate / frequency

    for i in range(duration_samples):
        phase = (i % period_samples) / period_samples
        value = 127 if phase < 0.5 else -128
        samples.append(value & 0xFF)

    return bytes(samples)


def generate_sawtooth_wave_8bit(frequency: float, duration_samples: int, sample_rate: int = 22050) -> bytes:
    """Generate an 8-bit signed sawtooth wave."""
    samples = []
    period_samples = sample_rate / frequency

    for i in range(duration_samples):
        phase = (i % period_samples) / period_samples
        # Ramp from -128 to 127
        value = int((phase * 2 - 1) * 127)
        samples.append(value & 0xFF)

    return bytes(samples)


def generate_sine_wave_16bit(frequency: float, duration_samples: int, sample_rate: int = 22050) -> bytes:
    """
    Generate a 16-bit signed sine wave (little-endian).

    Returns:
        16-bit signed PCM data (int16, -32768 to 32767, little-endian)
    """
    import struct
    samples = []
    for i in range(duration_samples):
        t = i / sample_rate
        value = math.sin(2 * math.pi * frequency * t)
        # Scale to 16-bit signed range
        sample = int(value * 32767)
        samples.append(sample)

    return struct.pack(f"<{len(samples)}h", *samples)


# ============================================================================
# Pattern Creation
# ============================================================================

def create_synth_pattern(num_rows: int = 64) -> XmPattern:
    """
    Create a simple synth pattern.

    Channel layout:
      Ch 1: Bassline (sine wave, low notes)
      Ch 2: Lead (square wave, melody)
      Ch 3: Pad (sawtooth wave, chords)
      Ch 4: Hi-res bass (16-bit sine, sub-bass)
    """
    pattern = XmPattern.empty(num_rows, num_channels=4)

    # Bassline: simple walking bass
    bass_notes = ["C-2", "C-2", "G-2", "G-2", "A-2", "A-2", "F-2", "F-2"]
    for i, note in enumerate(bass_notes):
        row = i * 8
        pattern.set_note(row, 0, XmNote.play(note, instrument=1, volume=64))

    # Lead: simple melody
    lead_notes = ["C-4", "E-4", "G-4", "E-4"]
    for i, note in enumerate(lead_notes):
        row = i * 16
        pattern.set_note(row, 1, XmNote.play(note, instrument=2, volume=56))

    # Pad: long chord notes
    pattern.set_note(0, 2, XmNote.play("C-3", instrument=3, volume=40))
    pattern.set_note(32, 2, XmNote.play("A-3", instrument=3, volume=40))

    # Sub-bass: 16-bit sine for extra depth
    pattern.set_note(0, 3, XmNote.play("C-1", instrument=4, volume=64))
    pattern.set_note(32, 3, XmNote.play("A-1", instrument=4, volume=64))

    return pattern


# ============================================================================
# Main
# ============================================================================

def main():
    print("Generating waveform samples...")

    # Generate 8-bit samples (looping)
    # Note: For looping samples, generate enough for smooth loop
    sample_rate = 22050
    loop_duration = int(sample_rate * 0.5)  # 0.5 second loops

    bass_sample = generate_sine_wave_8bit(110, loop_duration, sample_rate)  # A2 sine
    lead_sample = generate_square_wave_8bit(440, loop_duration, sample_rate)  # A4 square
    pad_sample = generate_sawtooth_wave_8bit(220, loop_duration, sample_rate)  # A3 sawtooth

    # Generate 16-bit sample for sub-bass
    sub_bass_sample = generate_sine_wave_16bit(55, loop_duration, sample_rate)  # A1 sine

    print(f"  Bass: {len(bass_sample)} bytes (8-bit)")
    print(f"  Lead: {len(lead_sample)} bytes (8-bit)")
    print(f"  Pad: {len(pad_sample)} bytes (8-bit)")
    print(f"  Sub-bass: {len(sub_bass_sample)} bytes (16-bit)")

    # Define instruments with embedded samples
    instruments = [
        XmInstrument(
            name="bass_sine",
            sample_data=bass_sample,
            sample_bits=8,
            sample_loop_type=1,  # Forward loop
            sample_loop_start=0,
            sample_loop_length=len(bass_sample)
        ),
        XmInstrument(
            name="lead_square",
            sample_data=lead_sample,
            sample_bits=8,
            sample_loop_type=1,
            sample_loop_start=0,
            sample_loop_length=len(lead_sample)
        ),
        XmInstrument(
            name="pad_saw",
            sample_data=pad_sample,
            sample_bits=8,
            sample_loop_type=1,
            sample_loop_start=0,
            sample_loop_length=len(pad_sample)
        ),
        XmInstrument(
            name="sub_bass_16",
            sample_data=sub_bass_sample,
            sample_bits=16,  # 16-bit sample!
            sample_loop_type=1,
            sample_loop_start=0,
            sample_loop_length=len(sub_bass_sample) // 2  # Loop length in samples, not bytes
        ),
    ]

    print("\nCreating pattern...")
    patterns = [
        create_synth_pattern(64),
    ]

    print("Building XM module...")
    module = XmModule(
        name="Synth Loop",
        num_channels=4,
        default_speed=6,
        default_bpm=125,
        restart_position=0,
        order_table=[0],  # Loop pattern 0
        patterns=patterns,
        instruments=instruments,
    )

    # Write XM file
    output_path = "synth_loop.xm"
    print(f"\nWriting {output_path}...")
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
            bits = inst.sample_bits
            size = len(inst.sample_data) if inst.sample_data else 0
            loop = "looping" if inst.sample_loop_type else "one-shot"
            print(f"  {i}: {inst.name} ({bits}-bit, {size} bytes, {loop})")

        print("\nNext steps:")
        print("  1. Open in MilkyTracker to verify playback")
        print("  2. Add to nether.toml:")
        print("     [[assets.trackers]]")
        print("     id = \"synth_loop\"")
        print("     path = \"music/synth_loop.xm\"")
        print("  3. Use in game:")
        print("     music_play(rom_tracker(b\"synth_loop\", 9), 0.8, 1)")

    except ValueError as e:
        print(f"[ERROR] Validation failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
