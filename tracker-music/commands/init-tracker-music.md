---
description: Initialize tracker music support (runs /init-procgen if needed)
argument-hint: "[project-dir]"
allowed-tools: ["Bash", "Write", "Glob"]
color: purple
---

# Init Tracker Music

Ensures the unified `.studio/` infrastructure is set up with music support.

Music generation is now part of the unified asset pipeline. This command:
1. Checks if `.studio/` exists
2. If not, downloads the scaffold from GitHub (same as `/init-procgen`)
3. Verifies music parser files are present

## Step 1: Check Existing Setup

```bash
TARGET="${1:-.}"

if [ -f "$TARGET/.studio/generate.py" ] && [ -f "$TARGET/.studio/parsers/music.py" ]; then
  echo "Tracker music already initialized!"
  echo ""
  echo "Music specs go in: .studio/specs/music/"
  echo "Instrument specs go in: .studio/specs/instruments/"
  echo ""
  echo "Generate with: python .studio/generate.py --only music"
  exit 0
fi
```

If music is already set up, report success and exit.

## Step 2: Initialize Infrastructure if Missing

If `.studio/` doesn't exist, create the full directory structure:

```bash
TARGET="${1:-.}"

if [ ! -f "$TARGET/.studio/generate.py" ]; then
  echo "Setting up .studio/ infrastructure..."

  mkdir -p "$TARGET/.studio/parsers"
  mkdir -p "$TARGET/.studio/analysis"
  mkdir -p "$TARGET/.studio/direction"
  mkdir -p "$TARGET/.studio/designs/levels"
  mkdir -p "$TARGET/.studio/designs/mechanics"
  mkdir -p "$TARGET/.studio/designs/systems"
  mkdir -p "$TARGET/.studio/specs/textures"
  mkdir -p "$TARGET/.studio/specs/sounds"
  mkdir -p "$TARGET/.studio/specs/meshes"
  mkdir -p "$TARGET/.studio/specs/characters"
  mkdir -p "$TARGET/.studio/specs/animations"
  mkdir -p "$TARGET/.studio/specs/normals"
  mkdir -p "$TARGET/.studio/specs/instruments"
  mkdir -p "$TARGET/.studio/specs/music"
fi
```

## Step 3: Download Scaffold from GitHub

Download all scaffold files:

```bash
TARGET="${1:-.}"
BASE="https://raw.githubusercontent.com/nethercore-systems/nethercore-ai-plugins/main/zx-procgen/scaffold/.studio"

# Core files
curl -sL "$BASE/generate.py" -o "$TARGET/.studio/generate.py"
curl -sL "$BASE/README.md" -o "$TARGET/.studio/README.md"

# Parsers (all of them for full infrastructure)
curl -sL "$BASE/parsers/__init__.py" -o "$TARGET/.studio/parsers/__init__.py"
curl -sL "$BASE/parsers/texture.py" -o "$TARGET/.studio/parsers/texture.py"
curl -sL "$BASE/parsers/sound.py" -o "$TARGET/.studio/parsers/sound.py"
curl -sL "$BASE/parsers/character.py" -o "$TARGET/.studio/parsers/character.py"
curl -sL "$BASE/parsers/animation.py" -o "$TARGET/.studio/parsers/animation.py"
curl -sL "$BASE/parsers/normal.py" -o "$TARGET/.studio/parsers/normal.py"
curl -sL "$BASE/parsers/music.py" -o "$TARGET/.studio/parsers/music.py"
curl -sL "$BASE/parsers/xm_types.py" -o "$TARGET/.studio/parsers/xm_types.py"
curl -sL "$BASE/parsers/xm_writer.py" -o "$TARGET/.studio/parsers/xm_writer.py"
curl -sL "$BASE/parsers/it_types.py" -o "$TARGET/.studio/parsers/it_types.py"
curl -sL "$BASE/parsers/it_writer.py" -o "$TARGET/.studio/parsers/it_writer.py"
```

## Step 4: Verify Music Support

```bash
TARGET="${1:-.}"

if [ -f "$TARGET/.studio/parsers/music.py" ]; then
  echo "Music parser installed"
else
  echo "Warning: music.py not found in parsers/"
fi

if [ -f "$TARGET/.studio/parsers/xm_writer.py" ]; then
  echo "XM writer installed"
else
  echo "Warning: xm_writer.py not found"
fi

if [ -f "$TARGET/.studio/parsers/it_writer.py" ]; then
  echo "IT writer installed"
else
  echo "Warning: it_writer.py not found"
fi
```

## Step 5: Create Example Spec

Create a minimal song spec example:

```python
# .studio/specs/music/example_song.spec.py
SONG = {
    'song': {
        'name': 'example_song',
        'format': 'xm',  # or 'it'
        'bpm': 120,
        'rows_per_beat': 4,
        'channels': 4,

        'instruments': [
            {'name': 'lead', 'type': 'sine', 'attack': 0.01, 'decay': 0.1},
            {'name': 'bass', 'type': 'saw', 'attack': 0.01, 'decay': 0.2},
        ],

        'patterns': [
            {
                'name': 'intro',
                'rows': 64,
                'channels': {
                    0: [  # Lead melody
                        {'row': 0, 'note': 'C4', 'instrument': 0},
                        {'row': 16, 'note': 'E4', 'instrument': 0},
                    ],
                    1: [  # Bass
                        {'row': 0, 'note': 'C2', 'instrument': 1},
                    ],
                },
            },
        ],

        'order': [0, 0],  # Pattern order
    }
}
```

Use Write tool to create this example if `.studio/specs/music/` is empty.

## Step 6: Create assets/ Directory

```bash
TARGET="${1:-.}"
mkdir -p "$TARGET/assets/music"
```

## Step 7: Report Success

```
Tracker music initialized!

Structure:
  .studio/
  ├── generate.py              # Unified generator
  ├── parsers/
  │   ├── music.py             # Song parser
  │   ├── sound.py             # Instrument synthesis
  │   ├── xm_writer.py         # XM format
  │   ├── xm_types.py
  │   ├── it_writer.py         # IT format
  │   └── it_types.py
  └── specs/
      ├── music/               # Song specs (*.spec.py)
      └── instruments/         # Instrument specs (*.spec.py)

Quick Start:
  1. Create song specs in .studio/specs/music/*.spec.py
  2. Run: python .studio/generate.py --only music
  3. Output appears in assets/music/

Commands:
  /generate-song "dark boss theme"  # Interactive song generation
```

## Notes

The unified `.studio/` infrastructure includes all asset types. Music generation
uses the same workflow as textures, sounds, and other assets:

1. Create spec file in appropriate folder
2. Run `python .studio/generate.py`
3. Find output in `assets/`

For standalone music projects without the full procgen pipeline, the parsers
can still be used directly:

```bash
python .studio/parsers/music.py .studio/specs/music/song.spec.py assets/music/song.xm
```
