---
description: Initialize tracker music infrastructure with zero-token file copying
argument-hint: "[project-dir]"
allowed-tools: ["Bash", "Write", "Glob"]
color: purple
---

# Init Tracker Music Infrastructure

**Token-efficient XM/IT infrastructure setup** - Copies writer files directly using native OS commands (cp/xcopy) instead of reading them into context.

This is the **recommended** command for setting up tracker music projects. It uses native file copying to save 85% tokens.

## Performance Comparison

| Approach | Token Usage | Time | Tool Calls |
|----------|-------------|------|------------|
| This command | ~130 lines | Seconds | ~10 |
| Traditional Read/Write | ~904 lines | Minutes | ~35 |
| **Savings** | **85% reduction** | **10-15x faster** | **80% fewer calls** |

## What Gets Copied

This command copies the complete XM and IT format infrastructure:

| File | Lines | Purpose |
|------|-------|---------|
| `xm_writer.py` | 271 | XM (FastTracker II) format writer |
| `it_writer.py` | 333 | IT (Impulse Tracker) format writer |
| `xm_types.py` | ~150 | XM format types and constants |
| `it_types.py` | ~150 | IT format types and constants |
| **Total** | **~904** | Complete tracker music toolchain |

## Step 1: Determine Project Directory

**If project-dir argument ($1) is provided:**
- Use it as the target directory
- Create it if it doesn't exist: `mkdir -p "$1"`

**If not provided:**
- Use current directory (`.`)
- Validate it looks suitable for a music project

## Step 2: Validate Plugin Root

Check that `CLAUDE_PLUGIN_ROOT` environment variable exists:

```bash
if [ -z "$CLAUDE_PLUGIN_ROOT" ]; then
  echo "❌ Error: CLAUDE_PLUGIN_ROOT not set"
  echo "This command requires the tracker-music plugin to be installed."
  exit 1
fi
```

## Step 3: Create Directory Structure

Create all necessary directories for tracker music projects:

```bash
mkdir -p lib
mkdir -p songs/instruments
mkdir -p songs/patterns
mkdir -p songs/tracks
mkdir -p generated/xm
mkdir -p generated/it
mkdir -p samples
```

**Directory structure:**
```
project/
├── lib/                  # Writer infrastructure (copied from plugin)
│   ├── xm_writer.py
│   ├── it_writer.py
│   ├── xm_types.py
│   └── it_types.py
├── songs/                # Song composition files
│   ├── instruments/      # Instrument definitions
│   ├── patterns/         # Pattern definitions
│   └── tracks/           # Complete song files
├── samples/              # Audio samples for instruments
├── generated/            # Generated tracker files
│   ├── xm/              # FastTracker II modules
│   └── it/              # Impulse Tracker modules
```

## Step 4: Copy Writer Files (Zero Tokens)

Use native OS commands to copy writer files directly from plugin to `lib/`.

**Copy commands (Unix/macOS/Linux):**

```bash
# XM format files
cp "$CLAUDE_PLUGIN_ROOT/tracker-music/skills/xm-format/scripts/xm_writer.py" lib/
cp "$CLAUDE_PLUGIN_ROOT/tracker-music/skills/xm-format/scripts/xm_types.py" lib/

# IT format files
cp "$CLAUDE_PLUGIN_ROOT/tracker-music/skills/it-format/scripts/it_writer.py" lib/
cp "$CLAUDE_PLUGIN_ROOT/tracker-music/skills/it-format/scripts/it_types.py" lib/
```

These commands work on all platforms (Claude Code provides Unix shell on Windows too).

## Step 5: Validate Copies

Count copied files to ensure success:

```bash
COPIED_COUNT=$(ls -1 lib/*.py 2>/dev/null | wc -l)
echo "✅ Successfully copied $COPIED_COUNT writer file(s) to lib/"

if [ "$COPIED_COUNT" -ne 4 ]; then
  echo "❌ Warning: Expected 4 files, got $COPIED_COUNT"
  echo "Some writer files may not have been copied correctly."
fi
```

## Step 6: Create Example Instrument

Create a basic instrument definition in `songs/instruments/basic_bass.py`:

```python
# Basic bass instrument using sine wave
# Edit this to create custom instruments

from lib.xm_types import Instrument, Sample

def create_instrument():
    """Create a basic bass instrument."""
    return Instrument(
        name="Basic Bass",
        volume=64,
        samples=[
            Sample(
                name="Sine Bass",
                volume=64,
                panning=128,  # Center
                note_offset=0,
                # Sample data would go here
                # For now, this is a template
            )
        ]
    )
```

Use Write tool to create this small example file.

## Step 7: Create Example Pattern

Create a basic pattern in `songs/patterns/bassline.py`:

```python
# Example bassline pattern
# Edit this to create your own patterns

PATTERN = {
    'name': 'Bassline',
    'rows': 64,
    'channels': 4,
    'notes': [
        # Format: (row, channel, note, instrument, volume, effect, effect_param)
        (0, 0, 'C-3', 1, 64, 0, 0),   # Bass note on beat 1
        (16, 0, 'D#3', 1, 64, 0, 0),  # Bass note on beat 2
        (32, 0, 'F-3', 1, 64, 0, 0),  # Bass note on beat 3
        (48, 0, 'G-3', 1, 64, 0, 0),  # Bass note on beat 4
    ]
}
```

## Step 8: Create Example Song

Create a complete song template in `songs/tracks/demo_song.py`:

```python
# Demo song using XM format
# Edit this to compose your own music

from pathlib import Path
import sys

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'lib'))

from xm_writer import XMModule, XMPattern, XMInstrument, XMSample
from xm_types import NOTE_C3, NOTE_D3, NOTE_E3, NOTE_F3, NOTE_G3

def create_demo_song():
    """Create a simple demo song in XM format."""

    # Create module
    module = XMModule(
        name="Demo Song",
        tracker_name="Nethercore Tracker",
        num_channels=4,
        default_tempo=6,
        default_bpm=125,
    )

    # Create a simple instrument (sine wave bass)
    instrument = XMInstrument(
        name="Bass",
        num_samples=1,
    )

    # Add a sample (placeholder - real sample would have audio data)
    sample = XMSample(
        name="Sine Bass",
        length=8000,
        loop_start=0,
        loop_length=8000,
        volume=64,
        finetune=0,
        loop_type=1,  # Forward loop
        panning=128,  # Center
        relative_note=0,
        sample_data=b'\x00' * 8000,  # Placeholder - replace with real audio
    )
    instrument.samples = [sample]
    module.instruments = [instrument]

    # Create a simple pattern
    pattern = XMPattern(num_rows=64, num_channels=4)

    # Add some notes (C-D-E-F-G sequence)
    pattern.set_note(0, 0, NOTE_C3, 1, 64, 0, 0)   # Row 0, Channel 0
    pattern.set_note(16, 0, NOTE_D3, 1, 64, 0, 0)  # Row 16
    pattern.set_note(32, 0, NOTE_E3, 1, 64, 0, 0)  # Row 32
    pattern.set_note(48, 0, NOTE_F3, 1, 64, 0, 0)  # Row 48

    module.patterns = [pattern]
    module.pattern_order = [0]  # Play pattern 0 once

    return module

def main():
    """Generate the demo song as an XM file."""
    output_path = Path(__file__).parent.parent.parent / 'generated' / 'xm' / 'demo_song.xm'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Generating demo song...")
    module = create_demo_song()

    # Write XM file
    with open(output_path, 'wb') as f:
        module.write(f)

    print(f"✅ Generated: {output_path}")
    print(f"   Size: {output_path.stat().st_size} bytes")
    print("\nNext steps:")
    print("  1. Open the XM file in a tracker (OpenMPT, MilkyTracker, etc.)")
    print("  2. Edit songs/tracks/demo_song.py to compose your own music")
    print("  3. Run this script again to regenerate")

if __name__ == '__main__':
    main()
```

## Step 9: Create Generator Script

Create `generate_music.py` wrapper for all music generation:

```python
#!/usr/bin/env python3
"""Generate tracker music files from song definitions.

This script discovers all song definition files and generates
XM/IT modules using the writers from lib/.

Token-efficient approach: This file is small (~150 lines) vs reading
writers into context (~904 lines).
"""

import os
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

def generate_xm_songs():
    """Generate XM files from songs/tracks/*.xm.py"""
    songs_dir = Path('songs/tracks')
    output_dir = Path('generated/xm')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all XM song scripts
    song_files = list(songs_dir.glob('*.xm.py'))
    if not song_files:
        print("ℹ️ No XM songs found in songs/tracks/")
        return

    print(f"\n=== Generating {len(song_files)} XM song(s) ===")
    for song_file in song_files:
        print(f"  {song_file.stem}...", end=' ')
        try:
            # Execute the song script
            # It should generate its own output
            import subprocess
            result = subprocess.run(
                [sys.executable, str(song_file)],
                capture_output=True,
                text=True,
                cwd=song_file.parent
            )
            if result.returncode == 0:
                print(f"✅")
            else:
                print(f"❌ Error: {result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")

def generate_it_songs():
    """Generate IT files from songs/tracks/*.it.py"""
    songs_dir = Path('songs/tracks')
    output_dir = Path('generated/it')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all IT song scripts
    song_files = list(songs_dir.glob('*.it.py'))
    if not song_files:
        print("ℹ️ No IT songs found in songs/tracks/")
        return

    print(f"\n=== Generating {len(song_files)} IT song(s) ===")
    for song_file in song_files:
        print(f"  {song_file.stem}...", end=' ')
        try:
            # Execute the song script
            import subprocess
            result = subprocess.run(
                [sys.executable, str(song_file)],
                capture_output=True,
                text=True,
                cwd=song_file.parent
            )
            if result.returncode == 0:
                print(f"✅")
            else:
                print(f"❌ Error: {result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("╔════════════════════════════════════════════╗")
    print("║   Nethercore Tracker Music Generator      ║")
    print("║           XM/IT Format Support            ║")
    print("╚════════════════════════════════════════════╝")

    generate_xm_songs()
    generate_it_songs()

    print("\n✨ Generation complete!")
    print("\nNext steps:")
    print("  1. Review generated modules in generated/ directory")
    print("  2. Open in your favorite tracker (OpenMPT, MilkyTracker, etc.)")
    print("  3. Edit song definitions in songs/tracks/ to compose")
    print("  4. Run this script again to regenerate")
```

Use Write tool to create `generate_music.py`.

## Step 10: Create README

Create `README.md` explaining the workflow:

```markdown
# Tracker Music Project

This project uses the Nethercore tracker music infrastructure to compose music in XM (FastTracker II) and IT (Impulse Tracker) formats.

## Directory Structure

- `lib/` - XM/IT format writers (do not edit, regenerated from plugin)
- `songs/tracks/` - Song composition files (edit these)
- `songs/instruments/` - Instrument definitions
- `songs/patterns/` - Pattern definitions (reusable)
- `samples/` - Audio samples for instruments
- `generated/` - Generated XM/IT modules

## Quick Start

1. Edit `songs/tracks/demo_song.py` to compose your music
2. Run `python generate_music.py` to generate modules
3. Open generated XM/IT files in your tracker of choice

## Supported Trackers

- **OpenMPT** (Windows/Wine) - Full XM/IT support
- **MilkyTracker** (Cross-platform) - XM support
- **Schism Tracker** (Cross-platform) - IT support

## Integration with Nethercore ZX

Generated tracker modules can be used in Nethercore ZX games:

1. Convert XM/IT to Nethercore audio format
2. Use `/init-procgen-infrastructure sounds` to set up sound generation
3. Generate instrument samples using `sound_parser.py`
4. Compose music using tracker patterns

## Resources

- XM Format Spec: See `lib/xm_types.py` for constants and structure
- IT Format Spec: See `lib/it_types.py` for constants and structure
- Example Songs: See `songs/tracks/demo_song.py`

## Token Efficiency

This infrastructure setup used **85% fewer tokens** than traditional approaches:
- Traditional: ~904 lines (reading writer files into context)
- This setup: ~130 lines (only examples and wrapper)
- **Savings: 774 lines (85% reduction)**
```

Use Write tool to create `README.md`.

## Step 11: Create .gitignore

Create `.gitignore` for the project:

```
# Generated tracker modules
generated/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Virtual environments
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Temporary audio files
*.tmp
*.bak
```

## Step 12: Report Success

After all steps complete, report to the user:

```
✅ Tracker music infrastructure initialized successfully!

📦 Copied writer files to lib/:
  - xm_writer.py (271 lines)
  - it_writer.py (333 lines)
  - xm_types.py (~150 lines)
  - it_types.py (~150 lines)

📝 Created example files:
  - songs/tracks/demo_song.py - Complete XM song example
  - songs/instruments/basic_bass.py - Instrument template
  - songs/patterns/bassline.py - Pattern template

🔧 Created generator script: generate_music.py

📖 Created README.md with usage instructions

📊 Token efficiency:
  - Traditional approach: ~904 lines read via Read/Write
  - This approach: ~130 lines (examples + wrapper)
  - Savings: 85% (774 lines saved)

Next steps:
  1. Edit songs/tracks/demo_song.py to compose your music
  2. Run: python generate_music.py
  3. Open generated XM/IT files in your tracker
  4. Integrate with Nethercore ZX using audio pipeline

Integration with Nethercore ZX:
  1. Use /init-procgen-infrastructure sounds for SFX generation
  2. Generate instrument samples with sound_parser.py
  3. Compose tracker music with these writers
  4. Convert XM/IT to Nethercore audio format

Need help?
  - /generate-song - AI-assisted song composition
  - See README.md for detailed workflow
```

## Edge Cases

### Plugin Not Installed
If `CLAUDE_PLUGIN_ROOT` is not set:
```
❌ Error: tracker-music plugin not found

The CLAUDE_PLUGIN_ROOT environment variable is not set. This means
the tracker-music plugin is not installed or not loaded.

To install:
  1. Add nethercore-ai-plugins to your Claude Code settings
  2. Enable the tracker-music plugin
  3. Restart Claude Code

See: https://github.com/nethercore-systems/nethercore-ai-plugins
```

### Writer Files Missing
If source writer files don't exist:
```
❌ Error: Writer file not found

Expected: $CLAUDE_PLUGIN_ROOT/tracker-music/skills/xm-format/scripts/xm_writer.py
Found: (file does not exist)

This may indicate:
  - Plugin is outdated (update to latest version)
  - Plugin installation is corrupted (reinstall)
  - Wrong CLAUDE_PLUGIN_ROOT path
```

### Existing Files
If `lib/` already contains writer files:
```
⚠️ Warning: lib/ directory already contains writer files

Found:
  - lib/xm_writer.py
  - lib/it_writer.py

These will be overwritten. Continue? [y/N]
```

Use AskUserQuestion if you detect existing files.

## Notes

- This command saves **85% tokens** vs traditional Read/Write
- Uses native cp commands for instant file copying
- Only reads small example files into context (not writers)
- Ideal for new music composition projects
- Works seamlessly with `/init-procgen-infrastructure` for complete audio pipeline
- XM/IT formats are widely supported by tracker software
- Generated modules can be opened in OpenMPT, MilkyTracker, Schism Tracker, etc.
