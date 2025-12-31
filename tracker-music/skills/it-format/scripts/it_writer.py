"""
IT (Impulse Tracker) file writer for procedural music generation.

This module provides a pure Python implementation for generating valid IT files
that can be used with Nethercore's tracker engine.

IT format advantages over XM:
- Up to 64 channels (vs XM's 32)
- NNA (New Note Actions) for polyphonic instruments
- Pitch envelopes (in addition to volume/panning)
- Resonant filters
- Multi-sample instruments

Example:
    >>> from it_writer import ItModule, ItPattern, ItNote, ItInstrument, write_it
    >>>
    >>> # Create pattern
    >>> pattern = ItPattern.empty(64, num_channels=4)
    >>> pattern.set_note(0, 0, ItNote.play("C-4", instrument=1, volume=64))
    >>>
    >>> # Create module
    >>> module = ItModule(
    ...     name="My Song",
    ...     num_channels=4,
    ...     default_speed=6,
    ...     default_bpm=125,
    ...     order_table=[0],
    ...     patterns=[pattern],
    ...     instruments=[ItInstrument(name="kick", sample_data=kick_bytes)]
    ... )
    >>>
    >>> # Write file
    >>> write_it(module, "output.it")
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import struct

# =============================================================================
# Constants
# =============================================================================

IT_MAGIC = b"IMPM"
INSTRUMENT_MAGIC = b"IMPI"
SAMPLE_MAGIC = b"IMPS"

NOTE_MIN = 0
NOTE_MAX = 119
NOTE_FADE = 253
NOTE_CUT = 254
NOTE_OFF = 255

ORDER_END = 255
ORDER_SKIP = 254

# IT Flags
FLAG_STEREO = 0x01
FLAG_VOL_0_MIX = 0x02
FLAG_INSTRUMENTS = 0x04
FLAG_LINEAR_SLIDES = 0x08
FLAG_OLD_EFFECTS = 0x10
FLAG_LINK_G_MEMORY = 0x20
FLAG_MIDI_PITCH_CONTROL = 0x40
FLAG_REQUEST_EMBED_MIDI = 0x80

# Sample Flags
SAMPLE_HAS_DATA = 0x01
SAMPLE_16BIT = 0x02
SAMPLE_STEREO = 0x04
SAMPLE_COMPRESSED = 0x08
SAMPLE_LOOP = 0x10
SAMPLE_SUSTAIN_LOOP = 0x20
SAMPLE_LOOP_PINGPONG = 0x40
SAMPLE_SUSTAIN_PINGPONG = 0x80

# Envelope Flags
ENV_ENABLED = 0x01
ENV_LOOP = 0x02
ENV_SUSTAIN_LOOP = 0x04
ENV_CARRY = 0x08
ENV_FILTER = 0x80

# NNA (New Note Action)
NNA_CUT = 0
NNA_CONTINUE = 1
NNA_OFF = 2
NNA_FADE = 3

# DCT (Duplicate Check Type)
DCT_OFF = 0
DCT_NOTE = 1
DCT_SAMPLE = 2
DCT_INSTRUMENT = 3

# DCA (Duplicate Check Action)
DCA_CUT = 0
DCA_OFF = 1
DCA_FADE = 2

# =============================================================================
# Note Conversion
# =============================================================================

def note_from_name(name: str) -> int:
    """
    Convert note name to IT note number.

    Args:
        name: Note name like "C-4", "C#4", "Db4", or "---"

    Returns:
        Note number (0-119) or 0 for empty

    Examples:
        >>> note_from_name("C-4")
        48
        >>> note_from_name("A#5")
        70
        >>> note_from_name("---")
        0
    """
    name = name.strip().replace('-', '')

    if not name or name == "":
        return 0

    semitone_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

    if name[0] not in semitone_map:
        return 0

    semitone = semitone_map[name[0]]
    offset = 1

    # Sharp or flat
    if len(name) > offset:
        if name[offset] == '#':
            semitone += 1
            offset += 1
        elif name[offset] == 'b':
            semitone -= 1
            offset += 1

    # Octave
    try:
        octave = int(name[offset:])
    except ValueError:
        return 0

    if not (0 <= octave <= 9):
        return 0

    note = octave * 12 + semitone
    return max(0, min(119, note))

# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class ItNote:
    """Single note/command in a pattern cell."""
    note: int = 0              # 0=none, 1-119=C-0..B-9, 254=cut, 255=off
    instrument: int = 0        # 0=none, 1-99=instrument
    volume: int = 0            # Volume column
    effect: int = 0            # Effect (A-Z = 1-26)
    effect_param: int = 0      # Effect parameter

    @staticmethod
    def play(note_name: str, instrument: int, volume: int) -> 'ItNote':
        """Create a note with pitch, instrument, and volume."""
        return ItNote(
            note=note_from_name(note_name),
            instrument=instrument,
            volume=min(64, volume),
            effect=0,
            effect_param=0
        )

    @staticmethod
    def play_note(note: int, instrument: int, volume: int) -> 'ItNote':
        """Create a note with MIDI note number."""
        return ItNote(
            note=min(119, note),
            instrument=instrument,
            volume=min(64, volume),
            effect=0,
            effect_param=0
        )

    @staticmethod
    def off() -> 'ItNote':
        """Create a note-off (^^^)."""
        return ItNote(note=NOTE_OFF)

    @staticmethod
    def cut() -> 'ItNote':
        """Create a note-cut (===)."""
        return ItNote(note=NOTE_CUT)

    @staticmethod
    def fade() -> 'ItNote':
        """Create a note-fade."""
        return ItNote(note=NOTE_FADE)

    def with_effect(self, effect: int, effect_param: int) -> 'ItNote':
        """Add effect to note (chainable)."""
        self.effect = effect
        self.effect_param = effect_param
        return self

    def with_volume_column(self, volume: int) -> 'ItNote':
        """Set volume column (chainable)."""
        self.volume = volume
        return self

@dataclass
class ItEnvelope:
    """Envelope for volume, panning, or pitch."""
    points: List[Tuple[int, int]] = field(default_factory=list)  # (tick, value)
    loop_begin: int = 0
    loop_end: int = 0
    sustain_begin: int = 0
    sustain_end: int = 0
    flags: int = 0

@dataclass
class ItInstrument:
    """IT instrument definition."""
    name: str = ""
    filename: str = ""
    nna: int = NNA_CUT
    dct: int = DCT_OFF
    dca: int = DCA_CUT
    fadeout: int = 256
    pitch_pan_separation: int = 0
    pitch_pan_center: int = 60
    global_volume: int = 128
    default_pan: Optional[int] = 32  # 0-64, None = disabled
    random_volume: int = 0
    random_pan: int = 0
    note_sample_table: List[Tuple[int, int]] = field(default_factory=lambda: [(i, 1) for i in range(120)])
    volume_envelope: Optional[ItEnvelope] = None
    panning_envelope: Optional[ItEnvelope] = None
    pitch_envelope: Optional[ItEnvelope] = None
    filter_cutoff: Optional[int] = None  # 0-127
    filter_resonance: Optional[int] = None  # 0-127
    midi_channel: int = 0
    midi_program: int = 0
    midi_bank: int = 0

@dataclass
class ItSample:
    """IT sample definition."""
    name: str = ""
    filename: str = ""
    global_volume: int = 64
    flags: int = 0
    default_volume: int = 64
    default_pan: Optional[int] = None
    length: int = 0
    loop_begin: int = 0
    loop_end: int = 0
    c5_speed: int = 22050
    sustain_loop_begin: int = 0
    sustain_loop_end: int = 0
    vibrato_speed: int = 0
    vibrato_depth: int = 0
    vibrato_rate: int = 0
    vibrato_type: int = 0

@dataclass
class ItPattern:
    """IT pattern containing rows of note data."""
    num_rows: int
    notes: List[List[ItNote]]

    @staticmethod
    def empty(num_rows: int, num_channels: int) -> 'ItPattern':
        """Create an empty pattern."""
        notes = [[ItNote() for _ in range(num_channels)] for _ in range(num_rows)]
        return ItPattern(num_rows=num_rows, notes=notes)

    def set_note(self, row: int, channel: int, note: ItNote):
        """Set a note at the given row and channel."""
        if 0 <= row < len(self.notes) and 0 <= channel < len(self.notes[0]):
            self.notes[row][channel] = note

@dataclass
class ItModule:
    """Complete IT module."""
    name: str = "Untitled"
    num_channels: int = 4
    default_speed: int = 6
    default_bpm: int = 125
    global_volume: int = 128
    mix_volume: int = 48
    panning_separation: int = 128
    pitch_wheel_depth: int = 0
    flags: int = FLAG_STEREO | FLAG_INSTRUMENTS | FLAG_LINEAR_SLIDES
    order_table: List[int] = field(default_factory=list)
    patterns: List[ItPattern] = field(default_factory=list)
    instruments: List[ItInstrument] = field(default_factory=list)
    samples: List[ItSample] = field(default_factory=list)
    sample_data: List[bytes] = field(default_factory=list)
    message: Optional[str] = None

# =============================================================================
# Writer
# =============================================================================

def write_string(data: bytearray, s: str, length: int):
    """Write a fixed-length string, padded with zeros."""
    b = s.encode('latin-1')[:length]
    data.extend(b)
    data.extend(bytes(length - len(b)))

def write_envelope(env: Optional[ItEnvelope]) -> bytes:
    """Write envelope data (82 bytes)."""
    data = bytearray()

    if env is None:
        env = ItEnvelope()

    # Flags
    data.append(env.flags)

    # Num points
    num_points = min(len(env.points), 25)
    data.append(num_points)

    # Loop/sustain points
    data.append(env.loop_begin)
    data.append(env.loop_end)
    data.append(env.sustain_begin)
    data.append(env.sustain_end)

    # Node data (75 bytes = 25 × 3)
    for i in range(25):
        if i < len(env.points):
            tick, value = env.points[i]
            data.append(value & 0xFF)
            data.extend(struct.pack('<H', tick))
        else:
            data.extend(bytes(3))

    # Reserved
    data.append(0)

    return bytes(data)

def pack_pattern(pattern: ItPattern, num_channels: int) -> bytes:
    """Pack pattern data using IT compression."""
    data = bytearray()

    # Previous values for compression
    prev_note = [0] * 64
    prev_instrument = [0] * 64
    prev_volume = [0] * 64
    prev_effect = [0] * 64
    prev_effect_param = [0] * 64

    for row in pattern.notes:
        for channel, note in enumerate(row[:num_channels]):
            # Skip empty notes
            if (note.note == 0 and note.instrument == 0 and
                note.volume == 0 and note.effect == 0 and note.effect_param == 0):
                continue

            # Build mask
            mask = 0

            if note.note != 0 and note.note != prev_note[channel]:
                mask |= 0x01
                prev_note[channel] = note.note
            elif note.note != 0:
                mask |= 0x10

            if note.instrument != 0 and note.instrument != prev_instrument[channel]:
                mask |= 0x02
                prev_instrument[channel] = note.instrument
            elif note.instrument != 0:
                mask |= 0x20

            if note.volume != 0 and note.volume != prev_volume[channel]:
                mask |= 0x04
                prev_volume[channel] = note.volume
            elif note.volume != 0:
                mask |= 0x40

            if ((note.effect != 0 or note.effect_param != 0) and
                (note.effect != prev_effect[channel] or note.effect_param != prev_effect_param[channel])):
                mask |= 0x08
                prev_effect[channel] = note.effect
                prev_effect_param[channel] = note.effect_param
            elif note.effect != 0 or note.effect_param != 0:
                mask |= 0x80

            if mask == 0:
                continue

            # Write channel marker with mask flag
            data.append(channel | 0x80)
            data.append(mask)

            # Write data
            if mask & 0x01:
                data.append(note.note)
            if mask & 0x02:
                data.append(note.instrument)
            if mask & 0x04:
                data.append(note.volume)
            if mask & 0x08:
                data.append(note.effect)
                data.append(note.effect_param)

        # End of row marker
        data.append(0)

    return bytes(data)

def write_it(module: ItModule, filename: str):
    """Write IT module to file."""
    data = bytearray()

    # Calculate offsets
    header_size = 192
    orders_size = len(module.order_table)
    num_instruments = len(module.instruments)
    num_samples = len(module.samples)
    num_patterns = len(module.patterns)

    offset_table_start = header_size + orders_size
    offset_table_size = (num_instruments + num_samples + num_patterns) * 4

    # Message
    message_offset = 0
    message_size = 0
    special = 0
    if module.message:
        message_offset = offset_table_start + offset_table_size
        message_size = len(module.message) + 1
        special = 1

    # Instruments
    instruments_start = offset_table_start + offset_table_size + message_size
    instrument_size = 550
    instrument_offsets = [instruments_start + i * instrument_size for i in range(num_instruments)]

    # Samples
    samples_start = instruments_start + num_instruments * instrument_size
    sample_header_size = 80
    sample_offsets = [samples_start + i * sample_header_size for i in range(num_samples)]

    # Patterns
    patterns_start = samples_start + num_samples * sample_header_size
    packed_patterns = [pack_pattern(p, module.num_channels) for p in module.patterns]
    pattern_offsets = []
    current_offset = patterns_start
    for packed in packed_patterns:
        pattern_offsets.append(current_offset)
        current_offset += 8 + len(packed)

    # Sample data
    sample_data_start = current_offset
    sample_data_offsets = []
    current_offset = sample_data_start
    for sample_bytes in module.sample_data:
        sample_data_offsets.append(current_offset)
        current_offset += len(sample_bytes)

    # ========== Write Header ==========

    data.extend(IT_MAGIC)
    write_string(data, module.name, 26)
    data.extend(bytes([0x04, 0x10]))  # PHilight
    data.extend(struct.pack('<H', len(module.order_table)))
    data.extend(struct.pack('<H', num_instruments))
    data.extend(struct.pack('<H', num_samples))
    data.extend(struct.pack('<H', num_patterns))
    data.extend(struct.pack('<H', 0x0214))  # Cwt
    data.extend(struct.pack('<H', 0x0200))  # Cmwt
    data.extend(struct.pack('<H', module.flags))
    data.extend(struct.pack('<H', special))
    data.append(module.global_volume)
    data.append(module.mix_volume)
    data.append(module.default_speed)
    data.append(module.default_bpm)
    data.append(module.panning_separation)
    data.append(module.pitch_wheel_depth)
    data.extend(struct.pack('<H', len(module.message) if module.message else 0))
    data.extend(struct.pack('<I', message_offset))
    data.extend(bytes(4))  # Reserved

    # Channel pan/vol
    channel_pan = [32] * module.num_channels + [128] * (64 - module.num_channels)
    channel_vol = [64] * module.num_channels + [0] * (64 - module.num_channels)
    data.extend(bytes(channel_pan))
    data.extend(bytes(channel_vol))

    # ========== Write Order Table ==========
    data.extend(bytes(module.order_table))

    # ========== Write Offset Tables ==========
    for offset in instrument_offsets:
        data.extend(struct.pack('<I', offset))
    for offset in sample_offsets:
        data.extend(struct.pack('<I', offset))
    for offset in pattern_offsets:
        data.extend(struct.pack('<I', offset))

    # ========== Write Message ==========
    if module.message:
        data.extend(module.message.encode('latin-1'))
        data.append(0)

    # ========== Write Instruments ==========
    for instr in module.instruments:
        idata = bytearray()
        idata.extend(INSTRUMENT_MAGIC)
        write_string(idata, instr.filename, 12)
        idata.append(0)  # Reserved
        idata.append(instr.nna)
        idata.append(instr.dct)
        idata.append(instr.dca)
        idata.extend(struct.pack('<H', instr.fadeout))
        idata.append(instr.pitch_pan_separation & 0xFF)
        idata.append(instr.pitch_pan_center)
        idata.append(instr.global_volume)
        dfp = (instr.default_pan | 0x80) if instr.default_pan is not None else 32
        idata.append(dfp)
        idata.append(instr.random_volume)
        idata.append(instr.random_pan)
        idata.extend(bytes(4))  # TrkVers/NoS
        write_string(idata, instr.name, 26)
        ifc = (instr.filter_cutoff | 0x80) if instr.filter_cutoff is not None else 0
        ifr = (instr.filter_resonance | 0x80) if instr.filter_resonance is not None else 0
        idata.append(ifc)
        idata.append(ifr)
        idata.append(instr.midi_channel)
        idata.append(instr.midi_program)
        idata.extend(struct.pack('<H', instr.midi_bank))

        # Note-sample table
        for note, sample in instr.note_sample_table:
            idata.append(note)
            idata.append(sample)

        # Envelopes
        idata.extend(write_envelope(instr.volume_envelope))
        idata.extend(write_envelope(instr.panning_envelope))
        idata.extend(write_envelope(instr.pitch_envelope))

        data.extend(idata)

    # ========== Write Sample Headers ==========
    for i, sample in enumerate(module.samples):
        sdata = bytearray()
        sdata.extend(SAMPLE_MAGIC)
        write_string(sdata, sample.filename, 12)
        sdata.append(0)  # Reserved
        sdata.append(sample.global_volume)

        # Always write as 16-bit
        flags = sample.flags | SAMPLE_16BIT | SAMPLE_HAS_DATA
        sdata.append(flags)
        sdata.append(sample.default_volume)
        write_string(sdata, sample.name, 26)
        sdata.append(0x01)  # Cvt - signed samples
        dfp = (sample.default_pan | 0x80) if sample.default_pan is not None else 0
        sdata.append(dfp)
        sdata.extend(struct.pack('<I', len(module.sample_data[i]) // 2))
        sdata.extend(struct.pack('<I', sample.loop_begin))
        sdata.extend(struct.pack('<I', sample.loop_end))
        sdata.extend(struct.pack('<I', sample.c5_speed))
        sdata.extend(struct.pack('<I', sample.sustain_loop_begin))
        sdata.extend(struct.pack('<I', sample.sustain_loop_end))
        sdata.extend(struct.pack('<I', sample_data_offsets[i]))
        sdata.append(sample.vibrato_speed)
        sdata.append(sample.vibrato_depth)
        sdata.append(sample.vibrato_rate)
        sdata.append(sample.vibrato_type)
        data.extend(sdata)

    # ========== Write Patterns ==========
    for i, packed in enumerate(packed_patterns):
        data.extend(struct.pack('<H', len(packed)))
        data.extend(struct.pack('<H', module.patterns[i].num_rows))
        data.extend(bytes(4))  # Reserved
        data.extend(packed)

    # ========== Write Sample Data ==========
    for sample_bytes in module.sample_data:
        data.extend(sample_bytes)

    # Write to file
    with open(filename, 'wb') as f:
        f.write(data)

# =============================================================================
# Validation
# =============================================================================

def validate_it(filename: str):
    """Validate IT file can be parsed."""
    with open(filename, 'rb') as f:
        magic = f.read(4)
        if magic != IT_MAGIC:
            raise ValueError(f"Invalid IT magic: {magic}")
        print(f"{filename} is a valid IT file")
