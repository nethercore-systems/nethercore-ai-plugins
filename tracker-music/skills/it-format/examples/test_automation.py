#!/usr/bin/env python3
"""Test that automation survives packing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / ".studio"))

from parsers import music
from parsers.it_writer import _pack_pattern

# Load menu theme spec
spec = music.load_song_spec(".studio/specs/music/menu_theme.spec.py")
song = spec['song']

# Build patterns
patterns, pattern_map = music.build_it_patterns(spec, song['channels'])

print("BEFORE AUTOMATION:")
print(f"Pattern 0 (ambient), channel 1, first 5 rows:")
for row in range(5):
    print(f"  Row {row}: vol={patterns[0].notes[row][1].volume}")

# Apply automation
automation = song.get('automation', [])
music.apply_automation_it(patterns, automation, pattern_map)

print("\nAFTER AUTOMATION:")
print(f"Pattern 0 (ambient), channel 1, first 35 rows:")
for row in range(0, 35, 4):
    print(f"  Row {row}: vol={patterns[0].notes[row][1].volume}")

# Pack pattern
packed = _pack_pattern(patterns[0], song['channels'])

print(f"\nPACKED SIZE: {len(packed)} bytes")
print("\nFirst 100 bytes (hex):")
for i in range(0, min(100, len(packed)), 16):
    hex_str = ' '.join(f'{b:02X}' for b in packed[i:i+16])
    print(f"  {i:04X}: {hex_str}")

# Decode and verify
pos, row, last_mask = 0, 0, [0] * 64
found_vols = []

while pos < len(packed) and row <= 35:
    if packed[pos] == 0:
        row += 1
        pos += 1
        continue
    ch_var = packed[pos]
    pos += 1
    ch = (ch_var - 1) & 63
    mask = packed[pos] if (ch_var & 0x80) else last_mask[ch]
    if ch_var & 0x80:
        pos += 1
        last_mask[ch] = mask
    if mask & 0x01: pos += 1
    if mask & 0x02: pos += 1
    if mask & 0x04:
        if ch == 1:
            found_vols.append((row, packed[pos]))
        pos += 1
    if mask & 0x08: pos += 2

print(f"\nFOUND IN PACKED DATA:")
print(f"Channel 1 (pad) - {len(found_vols)} volume entries:")
for r, v in found_vols[:20]:
    exp = int(0 + (40 - 0) * (r / 32))
    print(f"  Row {r:2d}: vol={v:2d} (expected {exp})")

if len(found_vols) < 10:
    print("\nERROR: Automation was applied but not packed!")
else:
    print("\nSUCCESS: Automation survived packing")
