#!/usr/bin/env python3
"""
Unified Asset Generator - Discovers specs and routes to parsers.

Specs live in:
    .studio/specs/<category>/*.spec.py

Usage:
    python .studio/generate.py
    python .studio/generate.py --only textures
    python .studio/generate.py --spec .studio/specs/sounds/laser.spec.py

Blender invocation (for Blender-only categories):
    blender --background --python .studio/generate.py -- --only meshes

Outputs are written under `generated/` (parallel to `.studio/`).
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure parsers module is importable when running from project root.
STUDIO_ROOT = Path(__file__).parent
PROJECT_ROOT = STUDIO_ROOT.parent
sys.path.insert(0, str(STUDIO_ROOT))

SPEC_ROOT = STUDIO_ROOT / "specs"
OUTPUT_ROOT = PROJECT_ROOT / "generated"

HAS_BLENDER = False
try:
    import bpy  # type: ignore

    HAS_BLENDER = True
except Exception:
    HAS_BLENDER = False


# =============================================================================
# CONFIGURATION
# =============================================================================

# Category -> config
# - parser: import path (lazy-imported per category)
# - requires_blender: must run under Blender (bpy available)
# - name_key: wrapper key used by that spec type (spec.get(name_key, spec))
CATEGORY_CONFIG: Dict[str, Dict[str, Any]] = {
    "textures": {"parser": "parsers.texture", "requires_blender": False, "name_key": "texture"},
    "normals": {"parser": "parsers.normal", "requires_blender": False, "name_key": "normal"},
    "sounds": {"parser": "parsers.sound", "requires_blender": False, "name_key": "sound"},
    "instruments": {"parser": "parsers.sound", "requires_blender": False, "name_key": "instrument"},
    "music": {"parser": "parsers.music", "requires_blender": False, "name_key": "song"},
    "meshes": {"parser": "parsers.mesh", "requires_blender": True, "name_key": "mesh"},
    "characters": {"parser": "parsers.character", "requires_blender": True, "name_key": "character"},
    "animations": {"parser": "parsers.animation", "requires_blender": True, "name_key": "animation"},
}


def output_path_for(category: str, spec: Dict[str, Any]) -> Path:
    """Compute the output path for a spec using the spec's internal name."""
    name = extract_internal_name(category, spec)

    if category == "sounds":
        return OUTPUT_ROOT / "sounds" / f"{name}.wav"
    if category == "instruments":
        return OUTPUT_ROOT / "sounds" / "instruments" / f"{name}.wav"
    if category == "music":
        song = spec.get("song", spec)
        fmt = song.get("format", "xm")
        if fmt not in ("xm", "it"):
            raise ValueError(f"Invalid song format '{fmt}' (expected 'xm' or 'it')")
        return OUTPUT_ROOT / "music" / f"{name}.{fmt}"

    # textures, normals, meshes, characters, animations
    ext = {
        "textures": ".png",
        "normals": ".png",
        "meshes": ".glb",
        "characters": ".glb",
        "animations": ".glb",
    }[category]
    return OUTPUT_ROOT / category / f"{name}{ext}"


# =============================================================================
# DISCOVERY + VALIDATION
# =============================================================================


def validate_spec_filename(spec_path: Path) -> None:
    """Enforce canonical spec filename: <id>.spec.py (no extra dot segments)."""
    if spec_path.suffixes != [".spec", ".py"]:
        raise ValueError("spec filename must be '<id>.spec.py'")
    base = spec_path.name[: -len(".spec.py")]
    if not base:
        raise ValueError("spec id is empty")


def validate_spec_location(spec_path: Path) -> str:
    """Validate spec is under .studio/specs/<category>/ and return category."""
    try:
        spec_path.relative_to(SPEC_ROOT)
    except ValueError as e:
        raise ValueError(f"spec must live under {SPEC_ROOT}") from e

    if spec_path.parent == SPEC_ROOT:
        raise ValueError("spec must be in a category folder: .studio/specs/<category>/")

    if spec_path.parent.parent != SPEC_ROOT:
        raise ValueError("spec must be exactly one directory under .studio/specs/")

    category = spec_path.parent.name
    if category not in CATEGORY_CONFIG:
        raise ValueError(f"unknown category '{category}' (expected one of: {', '.join(sorted(CATEGORY_CONFIG))})")

    return category


def discover_specs(only: Optional[str] = None) -> List[Path]:
    """Find all .spec.py files, optionally filtered by category."""
    if not SPEC_ROOT.exists():
        return []

    if only is not None:
        if only not in CATEGORY_CONFIG:
            raise ValueError(f"unknown category '{only}'")
        category_dir = SPEC_ROOT / only
        if not category_dir.exists():
            print(f"Warning: Category '{only}' not found at {category_dir}")
            return []
        candidates = sorted(category_dir.glob("*.spec.py"))
    else:
        candidates: List[Path] = []
        for category_dir in SPEC_ROOT.iterdir():
            if category_dir.is_dir():
                candidates.extend(category_dir.glob("*.spec.py"))
        candidates = sorted(candidates)

    errors: List[str] = []
    for spec_path in candidates:
        try:
            validate_spec_filename(spec_path)
            validate_spec_location(spec_path)
        except ValueError as e:
            rel = spec_path.relative_to(SPEC_ROOT) if SPEC_ROOT in spec_path.parents else spec_path
            errors.append(f"{rel}: {e}")

    if errors:
        lines = ["Invalid spec layout:", *[f"  - {e}" for e in errors]]
        raise ValueError("\n".join(lines))

    return candidates


def resolve_spec_path(spec_arg: str) -> Path:
    """Resolve a user-supplied spec path relative to the project root."""
    p = Path(spec_arg)
    if not p.is_absolute():
        p = (PROJECT_ROOT / p).resolve()
    else:
        p = p.resolve()
    return p


def extract_internal_name(category: str, spec: Dict[str, Any]) -> str:
    """Extract the internal 'name' used for output routing."""
    cfg = CATEGORY_CONFIG[category]
    wrapper_key = cfg["name_key"]
    obj = spec.get(wrapper_key, spec)
    if not isinstance(obj, dict):
        raise ValueError(f"spec wrapper '{wrapper_key}' must be a dict")
    name = obj.get("name")
    if not name or not isinstance(name, str):
        raise ValueError("spec is missing required 'name'")
    if "/" in name or "\\" in name:
        raise ValueError("spec name must not contain path separators")
    return name


def load_parser_module(category: str):
    """Lazy-import the parser module for a category."""
    module_name = CATEGORY_CONFIG[category]["parser"]
    return importlib.import_module(module_name)


# =============================================================================
# ANIMATION VALIDATION (EARLY SPEC-LEVEL CHECKS)
# =============================================================================


def validate_animation_against_character_spec(anim_spec: dict, char_spec: dict, anim_path: Path) -> None:
    """
    Validate animation spec bones against character spec skeleton.

    This is an early check BEFORE any Blender work. Catches mismatches
    between animation and character specs at the spec level.
    """
    # Import preset requirements from animation parser (safe: does not require bpy at import time)
    from parsers.animation import PRESET_REQUIREMENTS, collect_referenced_bones

    # Get character skeleton bones
    skeleton = char_spec.get("character", char_spec).get("skeleton", [])
    char_bones = set()
    for bone_def in skeleton:
        bone_name = bone_def.get("bone")
        if bone_name:
            char_bones.add(bone_name)
        mirror = bone_def.get("mirror")
        if mirror and bone_name:
            if bone_name.endswith("_L"):
                char_bones.add(bone_name[:-2] + "_R")
            elif bone_name.endswith("_R"):
                char_bones.add(bone_name[:-2] + "_L")

    if not char_bones:
        print("  [WARN] No skeleton found in character spec")
        return

    referenced = collect_referenced_bones(anim_spec)

    anim = anim_spec.get("animation", anim_spec)
    rig_setup = anim.get("rig_setup", {})
    presets = rig_setup.get("presets", {})

    preset_required: Dict[str, List[str]] = {}
    for preset_name, enabled in presets.items():
        if not enabled:
            continue
        requirements = PRESET_REQUIREMENTS.get(preset_name, {})
        for bone in requirements.get("required", []):
            preset_required.setdefault(bone, []).append(f"preset '{preset_name}'")

    all_missing: Dict[str, List[str]] = {}

    for bone, locations in referenced.items():
        if bone not in char_bones:
            all_missing[bone] = locations

    for bone, sources in preset_required.items():
        if bone not in char_bones:
            all_missing.setdefault(bone, []).extend(sources)

    if all_missing:
        lines = [
            f"Animation spec '{anim_path.name}' references bones not in character skeleton:",
            "",
            "Missing bones:",
        ]

        for bone, locations in sorted(all_missing.items()):
            loc_str = ", ".join(locations[:3])
            if len(locations) > 3:
                loc_str += f", ... ({len(locations)} total)"
            lines.append(f"  - {bone} (referenced in: {loc_str})")

        lines.extend(
            [
                "",
                f"Character skeleton has {len(char_bones)} bones:",
                "  " + ", ".join(sorted(char_bones)),
                "",
                "Fix: Add missing bones to character spec, or remove references from animation spec.",
            ]
        )

        raise ValueError("\n".join(lines))


def get_character_spec_for_animation(anim_spec: dict) -> Optional[dict]:
    """Find and load the character spec referenced by an animation spec."""
    anim = anim_spec.get("animation", anim_spec)

    char_name = anim.get("character")
    input_armature = anim.get("input_armature", "")

    if not char_name and input_armature:
        armature_path = Path(input_armature)
        char_name = armature_path.stem

    if not char_name:
        return None

    char_spec_path = SPEC_ROOT / "characters" / f"{char_name}.spec.py"
    if not char_spec_path.exists():
        print(f"  [WARN] Character spec not found: {char_spec_path}")
        return None

    from parsers import character

    return character.load_spec(str(char_spec_path))


# =============================================================================
# GENERATION
# =============================================================================


def generate_spec(spec_path: Path, dry_run: bool = False) -> bool:
    """Generate asset from a single spec file."""
    try:
        validate_spec_filename(spec_path)
        category = validate_spec_location(spec_path)
    except ValueError as e:
        print(f"  [ERR] {spec_path}: {e}")
        return False

    cfg = CATEGORY_CONFIG[category]
    if cfg["requires_blender"] and not HAS_BLENDER:
        print(
            f"  [SKIP] {spec_path.name}: Requires Blender "
            f"(run via: blender --background --python .studio/generate.py -- --only {category})"
        )
        return False

    try:
        parser_module = load_parser_module(category)
    except Exception:
        print(f"  [SKIP] Parser not implemented: {category}")
        return False

    try:
        spec = parser_module.load_spec(str(spec_path))
        output_path = output_path_for(category, spec)
    except Exception as e:
        print(f"  [ERR] {spec_path.name}: {e}")
        return False

    if dry_run:
        rel_out = output_path.relative_to(PROJECT_ROOT) if PROJECT_ROOT in output_path.parents else output_path
        print(f"  [DRY] {spec_path.name} -> {rel_out}")
        return True

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if category == "textures":
            result = parser_module.generate_texture(spec)
            parser_module.write_png(str(output_path), result)

        elif category == "normals":
            result = parser_module.generate_normal(spec)
            parser_module.write_png(str(output_path), result)

        elif category == "sounds":
            result = parser_module.generate_sfx(spec)
            sound_spec = spec.get("sound", spec)
            sample_rate = sound_spec.get("sample_rate", 22050)
            parser_module.write_wav(str(output_path), result, sample_rate)

        elif category == "instruments":
            result = parser_module.generate_instrument(spec)
            inst_spec = spec.get("instrument", spec)
            sample_rate = inst_spec.get("sample_rate", 22050)
            parser_module.write_wav(str(output_path), result, sample_rate)

        elif category == "music":
            parser_module.generate_song(spec, str(output_path))

        elif category == "characters":
            armature, merged = parser_module.generate_character(spec)
            parser_module.export_character(armature, merged, str(output_path))

        elif category == "animations":
            char_spec = get_character_spec_for_animation(spec)
            if char_spec:
                validate_animation_against_character_spec(spec, char_spec, spec_path)
            parser_module.generate_animation(spec, str(output_path))

        elif category == "meshes":
            parser_module.generate_mesh(spec, str(output_path))

        rel_out = output_path.relative_to(PROJECT_ROOT) if PROJECT_ROOT in output_path.parents else output_path
        print(f"  [OK] {spec_path.name} -> {rel_out}")
        return True

    except Exception as e:
        print(f"  [ERR] {spec_path.name}: {e}")
        return False


def generate_all(
    only: Optional[str] = None,
    spec_file: Optional[str] = None,
    dry_run: bool = False,
) -> tuple[int, int]:
    """Generate all specs, returning (success_count, error_count)."""
    try:
        if spec_file:
            spec_path = resolve_spec_path(spec_file)
            if not spec_path.exists():
                print(f"Error: Spec file not found: {spec_path}")
                return 0, 1
            specs = [spec_path]
        else:
            specs = discover_specs(only)
    except Exception as e:
        print(f"Error: {e}")
        return 0, 1

    if not specs:
        print("No specs found.")
        return 0, 0

    by_category: Dict[str, List[Path]] = {}
    for spec in specs:
        category = spec.parent.name
        by_category.setdefault(category, []).append(spec)

    success = 0
    errors = 0

    for category, category_specs in sorted(by_category.items()):
        print(f"\n=== {category.upper()} ({len(category_specs)} specs) ===")
        for spec_path in category_specs:
            if generate_spec(spec_path, dry_run):
                success += 1
            else:
                errors += 1

    return success, errors


def clean_generated(only: Optional[str] = None) -> None:
    """Remove generated assets."""
    import shutil

    if only is None:
        if OUTPUT_ROOT.exists():
            shutil.rmtree(OUTPUT_ROOT)
            print(f"Cleaned: {OUTPUT_ROOT}")
        return

    if only not in CATEGORY_CONFIG:
        raise ValueError(f"unknown category '{only}'")

    if only == "sounds":
        sounds_dir = OUTPUT_ROOT / "sounds"
        if sounds_dir.exists():
            for wav in sounds_dir.glob("*.wav"):
                wav.unlink()
            print(f"Cleaned: {sounds_dir}/*.wav")
        return

    target_dir = {
        "instruments": OUTPUT_ROOT / "sounds" / "instruments",
        "music": OUTPUT_ROOT / "music",
    }.get(only, OUTPUT_ROOT / only)

    if target_dir.exists():
        shutil.rmtree(target_dir)
        print(f"Cleaned: {target_dir}")


def _argv_for_argparse() -> List[str]:
    """Blender runs scripts with many args; parse only args after `--`."""
    if HAS_BLENDER:
        if "--" in sys.argv:
            return sys.argv[sys.argv.index("--") + 1 :]
        return []
    return sys.argv[1:]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Unified asset generator for Nethercore ZX",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python .studio/generate.py
  python .studio/generate.py --only textures
  python .studio/generate.py --only sounds
  python .studio/generate.py --spec .studio/specs/sounds/laser.spec.py
  python .studio/generate.py --dry-run
  python .studio/generate.py --clean
        """,
    )

    parser.add_argument(
        "--only",
        choices=sorted(CATEGORY_CONFIG.keys()),
        help="Only generate assets of this type",
    )
    parser.add_argument(
        "--spec",
        help="Generate a specific spec file (path relative to project root)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without actually generating",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove generated assets",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_specs",
        help="List all discovered specs",
    )

    args = parser.parse_args(_argv_for_argparse())

    print("=" * 50)
    print("  Nethercore ZX - Unified Asset Generator")
    print("=" * 50)
    print(f"Specs:  {SPEC_ROOT}")
    print(f"Output: {OUTPUT_ROOT}")

    if args.clean:
        clean_generated(args.only)
        return

    if args.list_specs:
        specs = discover_specs(args.only)
        print(f"\nDiscovered {len(specs)} spec(s):")
        for spec in specs:
            print(f"  {spec.relative_to(SPEC_ROOT)}")
        return

    success, errors = generate_all(
        only=args.only,
        spec_file=args.spec,
        dry_run=args.dry_run,
    )

    print("\n" + "=" * 50)
    if args.dry_run:
        print(f"Dry run complete: {success} would generate, {errors} would skip/fail")
    else:
        print(f"Generation complete: {success} succeeded, {errors} failed")

    if errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
