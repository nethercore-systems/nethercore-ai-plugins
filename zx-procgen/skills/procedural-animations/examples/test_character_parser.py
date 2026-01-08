#!/usr/bin/env python3
"""
Blender test script for character parser validation.
Run with: blender --background --python test_character_parser.py
"""

import sys
from pathlib import Path

# Add parsers to path
parsers_path = Path(__file__).parent / ".studio" / "parsers"
sys.path.insert(0, str(parsers_path))

# Import character parser directly to avoid scipy dependency
import character

# Test each character spec
specs = [
    ".studio/specs/characters/knight.spec.py",
    ".studio/specs/characters/mage.spec.py",
    ".studio/specs/characters/spider.spec.py",
    ".studio/specs/characters/feminine_warrior.spec.py",
]

print("=" * 60)
print("  Character Parser Validation Test")
print("=" * 60)
print()

success_count = 0
error_count = 0

for spec_path in specs:
    print(f"Processing: {spec_path}")
    try:
        spec = character.load_spec(spec_path)
        name = Path(spec_path).stem
        output = f"generated/characters/{name}.glb"
        Path(output).parent.mkdir(parents=True, exist_ok=True)

        armature, final_objects = character.generate_character(spec)
        character.export_character(armature, final_objects, output)

        print(f"  [OK] Generated: {output}")
        success_count += 1
    except Exception as e:
        print(f"  [ERROR] {e}")
        import traceback
        traceback.print_exc()
        error_count += 1
    print()

print("=" * 60)
print(f"Results: {success_count} succeeded, {error_count} failed")
print("=" * 60)

if error_count > 0:
    sys.exit(1)
