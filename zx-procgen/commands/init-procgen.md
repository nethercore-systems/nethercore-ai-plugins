---
description: Initialize .studio/ with unified asset generator and all parsers
argument-hint: "[project-dir]"
allowed-tools: ["Bash", "Write", "Glob"]
color: blue
---

# Init Procgen

Downloads the complete `.studio/` scaffold from GitHub, including:
- Unified `generate.py` entry point
- All parser modules in `parsers/`
- Directory structure for specs, direction, designs, and analysis

## Step 1: Determine Project Directory

**If project-dir argument ($1) is provided:**
- Use it as the target directory
- Create it if it doesn't exist

**If not provided:**
- Use current directory (`.`)

## Step 2: Check Existing Setup

```bash
TARGET="${1:-.}"

if [ -f "$TARGET/.studio/generate.py" ]; then
  echo ".studio/ already exists"
fi
```

If `.studio/` already exists, present options to the user:

```
Warning: .studio/ already exists

Options:
  1. Overwrite (updates parsers, keeps specs)
  2. Skip (keep existing)
  3. Abort
```

Use AskUserQuestion to let user choose. If overwriting, preserve:
- `specs/` directory contents
- `direction/` directory contents
- `designs/` directory contents
- `analysis/` directory contents
- `status.md`

Only overwrite:
- `generate.py`
- `parsers/` directory

## Step 3: Create Directory Structure

Create all required directories:

```bash
TARGET="${1:-.}"

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
```

## Step 4: Download Scaffold from GitHub

Download all scaffold files using curl:

```bash
TARGET="${1:-.}"
BASE="https://raw.githubusercontent.com/nethercore-systems/nethercore-ai-plugins/main/zx-procgen/scaffold/.studio"

# Core files
curl -sL "$BASE/generate.py" -o "$TARGET/.studio/generate.py"
curl -sL "$BASE/README.md" -o "$TARGET/.studio/README.md"

# Parsers
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

## Step 5: Create generated/ Directory

Create the output directory for procedurally generated assets:

```bash
TARGET="${1:-.}"

mkdir -p "$TARGET/generated/textures"
mkdir -p "$TARGET/generated/sounds"
mkdir -p "$TARGET/generated/meshes"
mkdir -p "$TARGET/generated/characters"
mkdir -p "$TARGET/generated/animations"
mkdir -p "$TARGET/generated/music"
```

## Step 6: Create .gitignore for Generated Assets

Create `.gitignore` in generated/ to exclude generated files (regenerate from specs):

```
# Generated assets - regenerate with: python .studio/generate.py
*
!.gitignore
```

Use the Write tool to create `generated/.gitignore`.

## Step 7: Verify and Report Success

Verify the download succeeded:

```bash
TARGET="${1:-.}"

if [ -f "$TARGET/.studio/generate.py" ] && [ -f "$TARGET/.studio/parsers/texture.py" ]; then
  echo "Download successful"
else
  echo "Error: Download failed. Check your internet connection."
  exit 1
fi
```

Report success:

```
.studio/ initialized successfully!

Structure:
  .studio/
  ├── generate.py           # Run: python .studio/generate.py
  ├── parsers/              # All parser modules
  ├── direction/            # Creative direction (Markdown)
  ├── specs/                # Asset specifications (*.spec.py)
  ├── designs/              # Design documents (Markdown)
  └── analysis/             # Generated reports

  generated/                # Procedural assets (gitignored, regenerable)
  assets/                   # Human-made assets (committed to git)

Quick Start:
  1. Create specs in .studio/specs/<category>/<name>.spec.py
  2. Run: python .studio/generate.py
  3. Generated assets appear in generated/

Commands:
  python .studio/generate.py              # Generate all
  python .studio/generate.py --only textures  # Generate one type
  python .studio/generate.py --dry-run    # Preview
  python .studio/generate.py --list       # List specs
```

## Windows Notes

On Windows, use PowerShell or Git Bash. The curl commands work in both:

```powershell
# PowerShell alternative for mkdir
New-Item -ItemType Directory -Force -Path ".studio\parsers"
```

The scaffold downloads work identically on Windows, macOS, and Linux.
