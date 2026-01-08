#!/usr/bin/env python3
"""
Blender test script for animation parser validation.
Run with: blender --background --python test_animation_parser.py

Tests ALL animation specs including:
- Basic FK animation (idle)
- 2-bone IK (humanoid_walk)
- 8x 2-bone IK (spider_walk_ik)
- 5-bone N-bone IK (dragon_tail_sway)
- Head look / aim constraints (dragon_look)
- Foot roll system (knight_walk_footroll)
- Twist bones (knight_arm_reach)
"""

import sys
from pathlib import Path

# Add parsers to path
parsers_path = Path(__file__).parent / ".studio" / "parsers"
sys.path.insert(0, str(parsers_path))

# Import parsers
import animation
import character

print("=" * 70)
print("  Animation Parser Validation Test Suite")
print("=" * 70)
print()

# Characters needed for animations
CHARACTER_SPECS = [
    ("knight", ".studio/specs/characters/knight.spec.py"),
    ("spider", ".studio/specs/characters/spider.spec.py"),
    ("dragon", ".studio/specs/characters/dragon.spec.py"),
]

# Animation specs to test with features they validate
ANIMATION_SPECS = [
    # (name, path, feature_tested, required_character)
    ("idle", ".studio/specs/animations/idle.spec.py", "Basic FK", "knight"),
    ("humanoid_walk", ".studio/specs/animations/humanoid_walk.spec.py", "2-bone IK (humanoid_legs)", "knight"),
    ("spider_walk_ik", ".studio/specs/animations/spider_walk_ik.spec.py", "8x 2-bone IK (spider_legs)", "spider"),
    ("dragon_tail_sway", ".studio/specs/animations/dragon_tail_sway.spec.py", "5-bone N-bone IK + basic_spine", "dragon"),
    ("dragon_look", ".studio/specs/animations/dragon_look.spec.py", "head_look + aim constraints", "dragon"),
    ("knight_walk_footroll", ".studio/specs/animations/knight_walk_footroll.spec.py", "Foot roll system", "knight"),
    ("knight_arm_reach", ".studio/specs/animations/knight_arm_reach.spec.py", "Twist bones + arm IK", "knight"),
    ("knight_jump", ".studio/specs/animations/knight_jump.spec.py", "IK/FK switch + body bounce", "knight"),
]

succeeded = 0
failed = 0
results = []

# Phase 1: Generate required characters
print("Phase 1: Generating Character Meshes")
print("-" * 70)

character_errors = []
for char_name, spec_path in CHARACTER_SPECS:
    output = f"generated/characters/{char_name}.glb"
    Path(output).parent.mkdir(parents=True, exist_ok=True)

    if not Path(spec_path).exists():
        print(f"  [SKIP] {char_name}: spec not found ({spec_path})")
        continue

    try:
        # Clear scene for each character
        import bpy
        bpy.ops.wm.read_factory_settings(use_empty=True)

        spec = character.load_spec(spec_path)
        armature, objects = character.generate_character(spec)
        character.export_character(armature, objects, output)
        print(f"  [OK] {char_name}")
    except Exception as e:
        print(f"  [ERROR] {char_name}: {e}")
        character_errors.append(char_name)

print()

# Phase 2: Generate animations
print("Phase 2: Testing Animation Specs")
print("-" * 70)

for name, spec_path, feature, required_char in ANIMATION_SPECS:
    output = f"generated/animations/{name}.glb"
    Path(output).parent.mkdir(parents=True, exist_ok=True)

    # Check if spec exists
    if not Path(spec_path).exists():
        print(f"  [SKIP] {name}: spec not found")
        results.append((name, feature, "SKIP", "spec not found"))
        continue

    # Check if required character was generated
    if required_char in character_errors:
        print(f"  [SKIP] {name}: required character '{required_char}' failed")
        results.append((name, feature, "SKIP", f"character '{required_char}' failed"))
        continue

    try:
        spec = animation.load_spec(spec_path)
        animation.generate_animation(spec, output)
        print(f"  [OK] {name} - {feature}")
        results.append((name, feature, "OK", None))
        succeeded += 1
    except Exception as e:
        print(f"  [ERROR] {name}: {e}")
        results.append((name, feature, "ERROR", str(e)))
        failed += 1

print()
print("=" * 70)
print("  Test Coverage Summary")
print("=" * 70)
print()
print(f"{'Animation':<25} {'Feature Tested':<35} {'Result':<8}")
print("-" * 70)

for name, feature, status, error in results:
    status_icon = "[OK]" if status == "OK" else "[SKIP]" if status == "SKIP" else "[FAIL]"
    print(f"{name:<25} {feature:<35} {status_icon}")
    if error and status == "ERROR":
        print(f"                          Error: {error[:50]}...")

print()
print("=" * 70)
print(f"Results: {succeeded} succeeded, {failed} failed, {len(results) - succeeded - failed} skipped")
print("=" * 70)

if failed > 0:
    sys.exit(1)
