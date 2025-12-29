---
name: Generate SFX
description: Quick single sound effect generation using pyo synthesis
argument-hint: "<type> [output-path]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
---

# Generate SFX Command

Generate a Python script for a game sound effect using pyo synthesis.

## Arguments

The user may provide:
1. **type** (required): The type of sound effect (laser, explosion, coin, jump, hit, powerup, footstep, click)
2. **output-path** (optional): Where to save the script (defaults to `generator/sfx/<type>.py`)

## Workflow

1. **Parse Arguments**
   - Extract the sound type from arguments
   - Determine output path (use default if not specified)

2. **Load Recipe Reference**
   - Read the corresponding recipe from the procedural-sounds skill's references
   - Recipe location: `skills/procedural-sounds/references/sfx-recipes/<type>.py`

3. **Customize for Project**
   - Check if project has existing sound generator structure
   - Look for `generator/` directory or similar
   - Adapt output path and imports if needed

4. **Generate Script**
   - Copy the recipe as the base
   - Update the OUTPUT_FILE path to match project structure
   - Add project-specific header comments

5. **Provide Instructions**
   - Show how to run the script
   - Explain customization options
   - Note any prerequisites (pyo installation)

## Sound Types

| Type | Description | Technique |
|------|-------------|-----------|
| `laser` | Sci-fi zap/shoot | SuperSaw sweep |
| `explosion` | Impact/boom | Layered noise |
| `coin` | Pickup/collect | Arpeggio |
| `jump` | Player jump | Pitch arc |
| `hit` | Damage/punch | Noise transient |
| `powerup` | Power-up collect | FM + chorus |
| `footstep` | Walking sounds | Filtered noise |
| `click` | UI interaction | Sine blip |

## Example Usage

```
/generate-sfx laser
/generate-sfx explosion assets/audio/big_boom.py
/generate-sfx footstep generator/sounds/footstep_grass.py
```

## Output Structure

The generated script will be self-contained with:
- Documented parameters for customization
- Preset variations for different flavors
- Render function for WAV output
- ZX-compatible settings (22050Hz, 16-bit, mono)

## Prerequisites Note

Remind the user that they need:
1. Python 3.x
2. pyo library (`pip install pyo`)
3. portaudio (usually bundled on Windows, may need install on Linux/macOS)

## If Type Not Recognized

If the user requests a sound type not in the recipe list:
1. Explain available types
2. Offer to create a custom recipe using the pyo building blocks
3. Reference the procedural-sounds skill for synthesis guidance
