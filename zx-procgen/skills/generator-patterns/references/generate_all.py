#!/usr/bin/env python3
"""Run all procedural generators.

Copy this file to your project's generator/ folder.

Usage:
    python generate_all.py              # Generate all asset types
    python generate_all.py meshes       # Generate meshes only
    python generate_all.py textures     # Generate textures only
    python generate_all.py sprites      # Generate sprites only
    python generate_all.py animations   # Generate animations only
    python generate_all.py --dry-run    # Show what would be generated
    python generate_all.py --parallel   # Run generators in parallel (faster)

Requirements:
    - Python 3.9+
    - Blender 3.0+ (in PATH) for meshes/animations
    - pip install pillow numpy pyfastnoiselite (for textures/sprites)
"""
import argparse
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Tuple


# Map folder to runner command
# Meshes and animations use Blender in headless mode
# Textures and sprites use Python directly
RUNNERS: Dict[str, List[str]] = {
    "meshes": ["blender", "--background", "--python"],
    "textures": ["python"],
    "sprites": ["python"],
    "animations": ["blender", "--background", "--python"],
}


def get_generator_files(folder: str) -> List[Path]:
    """Get all generator files in a folder."""
    folder_path = Path(__file__).parent / folder
    if not folder_path.exists():
        return []

    files = []
    for file in sorted(folder_path.glob("*.py")):
        # Skip private files and __init__.py
        if file.name.startswith("_"):
            continue
        files.append(file)

    return files


def run_generator(file: Path, runner: List[str], dry_run: bool = False) -> Tuple[Path, bool, str]:
    """Run a single generator file.

    Returns:
        Tuple of (file, success, message)
    """
    if dry_run:
        return (file, True, f"Would run: {' '.join(runner)} {file}")

    cmd = runner + [str(file)]
    start_time = time.time()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )
        elapsed = time.time() - start_time

        if result.returncode == 0:
            return (file, True, f"OK ({elapsed:.1f}s)")
        else:
            error = result.stderr.strip() if result.stderr else result.stdout.strip()
            # Truncate long errors
            if len(error) > 200:
                error = error[:200] + "..."
            return (file, False, f"FAILED: {error}")

    except subprocess.TimeoutExpired:
        return (file, False, "TIMEOUT (>300s)")
    except FileNotFoundError as e:
        return (file, False, f"RUNNER NOT FOUND: {e}")
    except Exception as e:
        return (file, False, f"ERROR: {e}")


def run_generators(folders: List[str], dry_run: bool = False,
                   parallel: bool = False, max_workers: int = 4):
    """Run all generators in specified folders."""
    results = {"success": [], "failed": []}

    for folder in folders:
        if folder not in RUNNERS:
            print(f"Unknown folder: {folder}")
            continue

        runner = RUNNERS[folder]
        files = get_generator_files(folder)

        if not files:
            print(f"\n[{folder}] No generators found")
            continue

        print(f"\n{'='*60}")
        print(f"[{folder}] {len(files)} generator(s)")
        print('='*60)

        if parallel and not dry_run:
            # Parallel execution
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(run_generator, f, runner, dry_run): f
                    for f in files
                }

                for future in as_completed(futures):
                    file, success, message = future.result()
                    status = "✓" if success else "✗"
                    print(f"  {status} {file.name}: {message}")

                    if success:
                        results["success"].append(file)
                    else:
                        results["failed"].append(file)
        else:
            # Sequential execution
            for file in files:
                file, success, message = run_generator(file, runner, dry_run)
                status = "✓" if success else "✗"
                print(f"  {status} {file.name}: {message}")

                if success:
                    results["success"].append(file)
                else:
                    results["failed"].append(file)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Run procedural asset generators"
    )
    parser.add_argument(
        "folders",
        nargs="*",
        default=list(RUNNERS.keys()),
        help="Folders to process (default: all)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without running"
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run generators in parallel (faster but uses more resources)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)"
    )

    args = parser.parse_args()

    print("Procedural Asset Generator")
    print("="*60)

    if args.dry_run:
        print("DRY RUN - no files will be generated")

    start_time = time.time()
    results = run_generators(
        args.folders,
        dry_run=args.dry_run,
        parallel=args.parallel,
        max_workers=args.workers
    )
    elapsed = time.time() - start_time

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  Success: {len(results['success'])}")
    print(f"  Failed:  {len(results['failed'])}")
    print(f"  Time:    {elapsed:.1f}s")

    if results["failed"]:
        print("\nFailed generators:")
        for file in results["failed"]:
            print(f"  - {file}")
        sys.exit(1)
    else:
        print("\nAll generators completed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
