#!/usr/bin/env python3
"""
Test script for music generation debugging.
Tests both XM and IT generation from specs.
"""

import sys
import os
from pathlib import Path

# Add parsers to path and change working directory
scaffold_dir = Path(__file__).parent
parsers_path = scaffold_dir / ".studio" / "parsers"
sys.path.insert(0, str(parsers_path))
os.chdir(scaffold_dir)

# Import generate.py which has the proper imports set up
sys.path.insert(0, str(scaffold_dir / ".studio"))
from parsers import music

# Test boss theme (XM)
print("=" * 60)
print("  Testing XM Generation (boss_theme.xm)")
print("=" * 60)

spec_path = ".studio/specs/music/boss_theme.spec.py"
output_path = "generated/music/boss_theme.xm"

try:
    spec = music.load_spec(spec_path)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Debug: Check instrument generation
    spec_dir = Path(spec_path).parent
    sample_data, names, rates = music.load_instruments(spec, str(spec_dir))

    print(f"\nInstruments loaded: {len(sample_data)}")
    for i, (name, rate, data_len) in enumerate(zip(names, rates, [len(d) for d in sample_data])):
        print(f"  [{i}] {name}: {rate} Hz, {data_len} bytes ({data_len//2} samples)")

    # Check specs for base notes
    print("\nInstrument specs:")
    song = spec.get('song', spec)
    for i, inst_spec in enumerate(song.get('instruments', [])):
        if isinstance(inst_spec, dict):
            base_note = inst_spec.get('base_note', 'N/A')
            print(f"  [{i}] {inst_spec.get('name', 'unknown')}: base_note={base_note}")

    # Generate
    music.parse_song(spec_path, output_path)
    print(f"\n[OK] Generated: {output_path}")

except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()

print()

# Test menu theme (IT)
print("=" * 60)
print("  Testing IT Generation (menu_theme.it)")
print("=" * 60)

spec_path = ".studio/specs/music/menu_theme.spec.py"
output_path = "generated/music/menu_theme.it"

try:
    spec = music.load_spec(spec_path)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Debug: Check instrument generation
    spec_dir = Path(spec_path).parent
    sample_data, names, rates = music.load_instruments(spec, str(spec_dir))

    print(f"\nInstruments loaded: {len(sample_data)}")
    for i, (name, rate, data_len) in enumerate(zip(names, rates, [len(d) for d in sample_data])):
        print(f"  [{i}] {name}: {rate} Hz, {data_len} bytes ({data_len//2} samples)")

    # Check specs for base notes
    print("\nInstrument specs:")
    song = spec.get('song', spec)
    for i, inst_spec in enumerate(song.get('instruments', [])):
        if isinstance(inst_spec, dict):
            base_note = inst_spec.get('base_note', 'N/A')
            print(f"  [{i}] {inst_spec.get('name', 'unknown')}: base_note={base_note}")

    # Generate
    music.parse_song(spec_path, output_path)
    print(f"\n[OK] Generated: {output_path}")

except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("Done! Check generated/ for output files.")
print("=" * 60)
