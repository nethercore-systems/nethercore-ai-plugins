# File Organization (Spec-First)

This guide establishes the standard file organization pattern for spec-first procedural asset generation in Nethercore ZX projects.

## Core Principle: One Asset Per Spec

Each procedural asset has exactly one `.spec.py` file under `.studio/specs/<category>/`.

**Canonical filename:** `<id>.spec.py` (no extra dot segments).

## Standard Project Structure

```
my-game/
├── .studio/
│   ├── generate.py
│   ├── parsers/                  # Installed by /init-procgen
│   └── specs/
│       ├── textures/
│       ├── normals/
│       ├── sounds/
│       ├── instruments/
│       ├── music/
│       ├── meshes/
│       ├── characters/
│       └── animations/
└── generated/
    ├── textures/
    ├── normals/
    ├── meshes/
    ├── characters/
    ├── animations/
    ├── audio/
    │   └── instruments/
    └── tracks/
```

## Running the Generator

Generate everything (non-Blender categories):

```bash
python .studio/generate.py
```

Generate a single category:

```bash
python .studio/generate.py --only textures
python .studio/generate.py --only sounds
python .studio/generate.py --only instruments
python .studio/generate.py --only normals
python .studio/generate.py --only music
```

Blender-dependent categories run by invoking Blender on the same entrypoint:

```bash
blender --background --python .studio/generate.py -- --only meshes
blender --background --python .studio/generate.py -- --only characters
blender --background --python .studio/generate.py -- --only animations
```

## Why This Pattern Works

- **Context efficiency:** load one spec file to modify one asset.
- **Determinism:** source of truth is data specs; outputs are reproducible.
- **Safety:** avoids custom per-project generator scripts drifting over time.
