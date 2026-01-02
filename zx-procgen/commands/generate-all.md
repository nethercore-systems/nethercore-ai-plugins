---
description: Run all procedural generators in a project
argument-hint: "[asset-type] [--parallel] [--dry-run]"
allowed-tools:
  - Read
  - Glob
  - Bash
---

# Generate All Command

Run all procedural asset generators in the project.

## Arguments

The user may provide:
1. **asset-type** (optional): Which generators to run (`meshes`, `textures`, `sprites`, `animations`, `all`)
2. **--parallel** (optional): Run generators in parallel for faster execution
3. **--dry-run** (optional): Show what would be generated without running

## Workflow

1. **Detect Project Structure**
   - Look for `generation/` directory in project root
   - Check for existing `generate_all.py` script
   - Identify which asset types have generators

2. **If generate_all.py Exists**
   - Run it with the specified arguments
   - Report results

3. **If generate_all.py Doesn't Exist**
   - Offer to create it from the template
   - Explain the setup process
   - Point to `generator-patterns` skill for the full template

4. **Run Generators**
   - For meshes/animations: Use `blender --background --python <script>`
   - For textures/sprites: Use `python <script>`
   - Report success/failure for each file

5. **Report Results**
   - Show which assets were generated
   - Report any failures with error messages
   - Show total time taken

## Example Usage

```
/generate-all                    # Generate all asset types
/generate-all meshes             # Generate meshes only
/generate-all textures sprites   # Generate textures and sprites
/generate-all --parallel         # Run in parallel (faster)
/generate-all --dry-run          # Show what would run
```

## Runner Commands

| Asset Type | Command |
|------------|---------|
| meshes | `blender --background --python <file>` |
| textures | `python <file>` |
| sprites | `python <file>` |
| animations | `blender --background --python <file>` |

## Expected Project Structure

The command expects this structure:

```
project/
├── generation/
│   ├── lib/                # Shared utilities
│   │   ├── bpy_utils.py
│   │   ├── texture_buffer.py
│   │   └── sprite_utils.py
│   ├── meshes/             # One .py per mesh
│   │   ├── barrel.py
│   │   └── crate.py
│   ├── textures/           # One .py per texture
│   │   ├── wood_plank.py
│   │   └── metal_brushed.py
│   ├── sprites/            # One .py per sprite
│   │   └── player_idle.py
│   ├── animations/         # One .py per animation
│   │   └── walk_cycle.py
│   └── generate_all.py     # Batch runner (optional)
└── generated/              # Generated output
```

## Prerequisites

Remind the user about requirements:
- **Blender 3.0+** in PATH (for meshes/animations)
- **Python 3.9+** with: `pip install pillow numpy pyfastnoiselite`

## Error Handling

If generators fail:
1. Report which file failed
2. Show the error message
3. Continue running other generators (don't stop on first failure)
4. Summarize all failures at the end

## Template Generation

If the project doesn't have `generate_all.py`, offer to create it:

```python
# Copy from: generator-patterns skill
# Path: skills/generator-patterns/references/generate_all.py
```

Point users to the `generator-patterns` skill for:
- Complete `generate_all.py` template
- Library utility templates (`lib/bpy_utils.py`, etc.)
- File organization best practices
