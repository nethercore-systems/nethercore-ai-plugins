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
2. If not, runs `/init-procgen` to set up the full infrastructure
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

## Step 2: Initialize Full Infrastructure

If `.studio/` doesn't exist or is incomplete, initialize it:

```bash
if [ ! -f "$TARGET/.studio/generate.py" ]; then
  echo "Setting up .studio/ infrastructure..."
  # This would invoke /init-procgen, but since we can't call commands,
  # we copy the scaffold directly
fi
```

## Step 3: Copy Scaffold

Use the unified scaffold from zx-procgen:

```bash
SCAFFOLD="$CLAUDE_PLUGIN_ROOT/zx-procgen/scaffold/.studio"

if [ ! -d "$SCAFFOLD" ]; then
  echo "Error: Scaffold not found at $SCAFFOLD"
  echo "Make sure zx-procgen plugin is installed."
  exit 1
fi

mkdir -p "$TARGET/.studio"
cp -r "$SCAFFOLD"/* "$TARGET/.studio/"
```

## Step 4: Verify Music Support

```bash
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

## Step 6: Report Success

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
