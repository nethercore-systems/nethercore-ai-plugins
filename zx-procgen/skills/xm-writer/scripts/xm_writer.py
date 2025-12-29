#!/usr/bin/env python3
"""
XM Writer - Generate valid FastTracker 2 XM files programmatically.

This module provides low-level primitives for creating XM tracker modules.
For composition theory (melody, chords, song structure), use the sound-design
plugin's music-composition skill.

Nethercore-specific: Generated XM files have sample_length=0. Instrument names
map to ROM samples at runtime via [[assets.sounds]] IDs in nether.toml.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import struct


# ============================================================================
# Constants
# ============================================================================

XM_MAGIC = b"Extended Module: "
XM_VERSION = 0x0104  # FastTracker 2 format
XM_HEADER_SIZE = 276  # Standard header size (after version field)

# Note values
NOTE_NONE = 0
NOTE_OFF = 97
NOTE_MIN = 1   # C-0
NOTE_MAX = 96  # B-7

# Limits
MAX_CHANNELS = 32
MAX_PATTERNS = 256
MAX_PATTERN_ROWS = 256
MAX_INSTRUMENTS = 128


# ============================================================================
# Note Helpers
# ============================================================================

def note_from_name(name: str) -> int:
    """
    Convert note name to XM note value.

    Examples:
        note_from_name("C-4") -> 49
        note_from_name("A#3") -> 46
        note_from_name("---") -> 0 (no note)
        note_from_name("===") -> 97 (note off)
    """
    if name in ("---", "...", ""):
        return NOTE_NONE
    if name in ("===", "OFF"):
        return NOTE_OFF

    # Parse note name: C-4, C#4, Db4, etc.
    name = name.upper().replace("-", "")

    note_map = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

    note_char = name[0]
    if note_char not in note_map:
        raise ValueError(f"Invalid note: {name}")

    semitone = note_map[note_char]

    # Check for sharp/flat
    idx = 1
    if len(name) > 1 and name[1] == "#":
        semitone += 1
        idx = 2
    elif len(name) > 1 and name[1] == "B":
        semitone -= 1
        idx = 2

    # Parse octave
    octave = int(name[idx:])

    # XM note value: 1 = C-0, 13 = C-1, 49 = C-4, etc.
    return octave * 12 + semitone + 1


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class XmNote:
    """Single note/command in a pattern cell."""
    note: int = 0           # 0=none, 1-96=C-0..B-7, 97=note-off
    instrument: int = 0     # 0=none, 1-128=instrument
    volume: int = 0         # 0=none, 0x10-0x50=set volume (0-64)
    effect: int = 0         # Effect command (0-35)
    effect_param: int = 0   # Effect parameter (0-255)

    def is_empty(self) -> bool:
        """Check if note cell is completely empty."""
        return (self.note == 0 and self.instrument == 0 and
                self.volume == 0 and self.effect == 0 and self.effect_param == 0)

    @staticmethod
    def off() -> "XmNote":
        """Create a note-off."""
        return XmNote(note=NOTE_OFF)

    @staticmethod
    def play(note_name: str, instrument: int, volume: int = 64) -> "XmNote":
        """Create a note with instrument and volume."""
        return XmNote(
            note=note_from_name(note_name),
            instrument=instrument,
            volume=0x10 + min(64, max(0, volume))  # Volume column format
        )


@dataclass
class XmPattern:
    """Pattern containing rows of note data."""
    num_rows: int = 64
    notes: List[List[XmNote]] = field(default_factory=list)  # [row][channel]

    @staticmethod
    def empty(num_rows: int, num_channels: int) -> "XmPattern":
        """Create an empty pattern with given dimensions."""
        notes = [[XmNote() for _ in range(num_channels)] for _ in range(num_rows)]
        return XmPattern(num_rows=num_rows, notes=notes)

    def set_note(self, row: int, channel: int, note: XmNote) -> None:
        """Set a note at the given position."""
        if row < len(self.notes) and channel < len(self.notes[row]):
            self.notes[row][channel] = note


@dataclass
class XmEnvelope:
    """Volume or panning envelope."""
    points: List[Tuple[int, int]] = field(default_factory=list)  # [(tick, value)]
    sustain_point: int = 0
    loop_start: int = 0
    loop_end: int = 0
    enabled: bool = False
    sustain_enabled: bool = False
    loop_enabled: bool = False


@dataclass
class XmInstrument:
    """Instrument metadata (name maps to ROM sample ID)."""
    name: str = ""                                  # Maps to [[assets.sounds]] id
    volume_envelope: Optional[XmEnvelope] = None
    panning_envelope: Optional[XmEnvelope] = None
    vibrato_type: int = 0      # 0=sine, 1=square, 2=ramp down, 3=ramp up
    vibrato_sweep: int = 0
    vibrato_depth: int = 0
    vibrato_rate: int = 0
    volume_fadeout: int = 0    # 0-4095
    sample_finetune: int = 0   # -128 to 127
    sample_relative_note: int = 0  # Semitones from C-4
    sample_loop_start: int = 0
    sample_loop_length: int = 0
    sample_loop_type: int = 0  # 0=none, 1=forward, 2=ping-pong


@dataclass
class XmModule:
    """Complete XM module."""
    name: str = "Untitled"
    num_channels: int = 4
    default_speed: int = 6     # Ticks per row
    default_bpm: int = 125     # Beats per minute
    restart_position: int = 0  # Order position for looping
    linear_frequency_table: bool = True
    order_table: List[int] = field(default_factory=list)  # Pattern order
    patterns: List[XmPattern] = field(default_factory=list)
    instruments: List[XmInstrument] = field(default_factory=list)


# ============================================================================
# Pattern Packing
# ============================================================================

def pack_pattern_data(pattern: XmPattern, num_channels: int) -> bytes:
    """
    Pack pattern data using XM compressed format.

    Format:
    - If first byte >= 0x80: packed format with flags indicating which fields follow
    - Otherwise: unpacked 5-byte format

    Flag byte (0x80 | flags):
    - Bit 0 (0x01): Note present
    - Bit 1 (0x02): Instrument present
    - Bit 2 (0x04): Volume present
    - Bit 3 (0x08): Effect present
    - Bit 4 (0x10): Effect param present
    """
    output = bytearray()

    for row in pattern.notes:
        for ch_idx, note in enumerate(row):
            if ch_idx >= num_channels:
                break

            # Empty note: just the packed marker
            if note.is_empty():
                output.append(0x80)
                continue

            # Build flag byte
            flags = 0x80
            if note.note != 0:
                flags |= 0x01
            if note.instrument != 0:
                flags |= 0x02
            if note.volume != 0:
                flags |= 0x04
            if note.effect != 0:
                flags |= 0x08
            if note.effect_param != 0:
                flags |= 0x10

            output.append(flags)

            # Write only present fields
            if note.note != 0:
                output.append(note.note)
            if note.instrument != 0:
                output.append(note.instrument)
            if note.volume != 0:
                output.append(note.volume)
            if note.effect != 0:
                output.append(note.effect)
            if note.effect_param != 0:
                output.append(note.effect_param)

    return bytes(output)


# ============================================================================
# XM File Writer
# ============================================================================

def write_xm(module: XmModule, output_path: str) -> None:
    """
    Write XM module to file.

    Creates a valid FastTracker 2 XM file with sample_length=0 for all
    instruments. Instrument names are used to map to ROM samples at runtime.
    """
    output = bytearray()

    # Derive counts
    num_patterns = len(module.patterns)
    num_instruments = len(module.instruments)
    song_length = len(module.order_table) if module.order_table else 1

    # Validate
    if num_patterns > MAX_PATTERNS:
        raise ValueError(f"Too many patterns: {num_patterns} > {MAX_PATTERNS}")
    if num_instruments > MAX_INSTRUMENTS:
        raise ValueError(f"Too many instruments: {num_instruments} > {MAX_INSTRUMENTS}")
    if module.num_channels > MAX_CHANNELS:
        raise ValueError(f"Too many channels: {module.num_channels} > {MAX_CHANNELS}")

    # ========== XM Header ==========

    # Magic (17 bytes)
    output.extend(XM_MAGIC)

    # Module name (20 bytes, null-padded)
    name_bytes = module.name.encode("ascii", errors="replace")[:20]
    output.extend(name_bytes.ljust(20, b"\x00"))

    # 0x1A marker
    output.append(0x1A)

    # Tracker name (20 bytes)
    tracker_name = b"Nethercore XM Writer"
    output.extend(tracker_name.ljust(20, b"\x00"))

    # Version (2 bytes, little-endian)
    output.extend(struct.pack("<H", XM_VERSION))

    # Header size (4 bytes) - size of header after this field
    output.extend(struct.pack("<I", 276))

    # Song length (2 bytes)
    output.extend(struct.pack("<H", song_length))

    # Restart position (2 bytes)
    output.extend(struct.pack("<H", module.restart_position))

    # Number of channels (2 bytes)
    output.extend(struct.pack("<H", module.num_channels))

    # Number of patterns (2 bytes)
    output.extend(struct.pack("<H", num_patterns))

    # Number of instruments (2 bytes)
    output.extend(struct.pack("<H", num_instruments))

    # Flags (2 bytes) - bit 0: linear frequency table
    flags = 1 if module.linear_frequency_table else 0
    output.extend(struct.pack("<H", flags))

    # Default speed (2 bytes)
    output.extend(struct.pack("<H", module.default_speed))

    # Default BPM (2 bytes)
    output.extend(struct.pack("<H", module.default_bpm))

    # Pattern order table (256 bytes)
    for i in range(256):
        if i < len(module.order_table):
            output.append(module.order_table[i])
        else:
            output.append(0)

    # ========== Pattern Data ==========

    for pattern in module.patterns:
        packed_data = pack_pattern_data(pattern, module.num_channels)

        # Pattern header length (4 bytes) - per XM spec, includes the length field itself
        # Standard value: 9 = 4 (length) + 1 (packing) + 2 (rows) + 2 (packed_size)
        output.extend(struct.pack("<I", 9))

        # Packing type (1 byte) - always 0
        output.append(0)

        # Number of rows (2 bytes)
        output.extend(struct.pack("<H", pattern.num_rows))

        # Packed pattern data size (2 bytes)
        output.extend(struct.pack("<H", len(packed_data)))

        # Pattern data
        output.extend(packed_data)

    # ========== Instruments ==========

    for instrument in module.instruments:
        _write_instrument(output, instrument)

    # Write to file
    with open(output_path, "wb") as f:
        f.write(output)


def _write_instrument(output: bytearray, instrument: XmInstrument) -> None:
    """Write a single instrument to the output buffer."""

    # We always write one sample per instrument (for ROM mapping)
    num_samples = 1
    header_size = 263  # 243 + 20 extra for sample header base

    # Instrument header size (4 bytes)
    output.extend(struct.pack("<I", header_size))

    # Instrument name (22 bytes)
    name_bytes = instrument.name.encode("ascii", errors="replace")[:22]
    output.extend(name_bytes.ljust(22, b"\x00"))

    # Instrument type (1 byte) - always 0
    output.append(0)

    # Number of samples (2 bytes)
    output.extend(struct.pack("<H", num_samples))

    # Sample header size (4 bytes)
    output.extend(struct.pack("<I", 40))

    # Sample number for all notes (96 bytes) - all use sample 0
    output.extend(bytes(96))

    # Volume envelope points (48 bytes = 12 points * 4 bytes)
    vol_env = instrument.volume_envelope
    for i in range(12):
        if vol_env and i < len(vol_env.points):
            output.extend(struct.pack("<HH", vol_env.points[i][0], vol_env.points[i][1]))
        else:
            output.extend(struct.pack("<HH", 0, 0))

    # Panning envelope points (48 bytes)
    pan_env = instrument.panning_envelope
    for i in range(12):
        if pan_env and i < len(pan_env.points):
            output.extend(struct.pack("<HH", pan_env.points[i][0], pan_env.points[i][1]))
        else:
            output.extend(struct.pack("<HH", 0, 0))

    # Number of volume envelope points (1 byte)
    output.append(len(vol_env.points) if vol_env else 0)

    # Number of panning envelope points (1 byte)
    output.append(len(pan_env.points) if pan_env else 0)

    # Volume sustain/loop points (3 bytes)
    output.append(vol_env.sustain_point if vol_env else 0)
    output.append(vol_env.loop_start if vol_env else 0)
    output.append(vol_env.loop_end if vol_env else 0)

    # Panning sustain/loop points (3 bytes)
    output.append(pan_env.sustain_point if pan_env else 0)
    output.append(pan_env.loop_start if pan_env else 0)
    output.append(pan_env.loop_end if pan_env else 0)

    # Volume type flags (1 byte)
    vol_flags = 0
    if vol_env:
        if vol_env.enabled:
            vol_flags |= 1
        if vol_env.sustain_enabled:
            vol_flags |= 2
        if vol_env.loop_enabled:
            vol_flags |= 4
    output.append(vol_flags)

    # Panning type flags (1 byte)
    pan_flags = 0
    if pan_env:
        if pan_env.enabled:
            pan_flags |= 1
        if pan_env.sustain_enabled:
            pan_flags |= 2
        if pan_env.loop_enabled:
            pan_flags |= 4
    output.append(pan_flags)

    # Vibrato settings (4 bytes)
    output.append(instrument.vibrato_type)
    output.append(instrument.vibrato_sweep)
    output.append(instrument.vibrato_depth)
    output.append(instrument.vibrato_rate)

    # Volume fadeout (2 bytes)
    output.extend(struct.pack("<H", instrument.volume_fadeout))

    # Reserved (22 bytes to reach header_size)
    output.extend(bytes(22))

    # ========== Sample Header (40 bytes) ==========

    # Sample length (4 bytes) - SET TO 0 (Nethercore strips samples)
    output.extend(struct.pack("<I", 0))

    # Sample loop start (4 bytes)
    output.extend(struct.pack("<I", instrument.sample_loop_start))

    # Sample loop length (4 bytes)
    output.extend(struct.pack("<I", instrument.sample_loop_length))

    # Volume (1 byte)
    output.append(64)

    # Finetune (1 byte, signed)
    output.append(instrument.sample_finetune & 0xFF)

    # Type (1 byte) - loop type in lower 2 bits
    output.append(instrument.sample_loop_type & 0x03)

    # Panning (1 byte) - center
    output.append(128)

    # Relative note (1 byte, signed)
    output.append(instrument.sample_relative_note & 0xFF)

    # Reserved (1 byte)
    output.append(0)

    # Sample name (22 bytes) - use instrument name
    output.extend(name_bytes.ljust(22, b"\x00"))

    # NO SAMPLE DATA (sample_length = 0)


# ============================================================================
# Validation
# ============================================================================

def validate_xm(path: str) -> bool:
    """
    Validate that an XM file has correct magic and version.

    Returns True if valid, raises ValueError with details if not.
    """
    with open(path, "rb") as f:
        data = f.read(64)

    if len(data) < 60:
        raise ValueError(f"File too small: {len(data)} bytes")

    if data[:17] != XM_MAGIC:
        raise ValueError(f"Invalid magic: {data[:17]!r}")

    version = struct.unpack("<H", data[58:60])[0]
    if version != XM_VERSION:
        raise ValueError(f"Unsupported version: 0x{version:04X}")

    return True
