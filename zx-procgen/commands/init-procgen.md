---
description: Initialize .studio/ with unified asset generator and all parsers
argument-hint: "[project-dir]"
allowed-tools: ["Bash", "Write", "Glob"]
color: blue
---

# Init Procgen

Copies the complete `.studio/` scaffold to the project, including:
- Unified `generate.py` entry point
- All parser modules in `parsers/`
- Directory structure for specs, direction, designs, and analysis

## Step 1: Determine Project Directory

**If project-dir argument ($1) is provided:**
- Use it as the target directory
- Create it if it doesn't exist

**If not provided:**
- Use current directory (`.`)

## Step 2: Validate Plugin Root

Check that `CLAUDE_PLUGIN_ROOT` environment variable exists:

```bash
if [ -z "$CLAUDE_PLUGIN_ROOT" ]; then
  echo "Error: CLAUDE_PLUGIN_ROOT not set"
  echo "This command requires the zx-procgen plugin to be installed."
  exit 1
fi
```

## Step 3: Copy Scaffold (Zero Tokens)

Copy the entire scaffold directory using native OS commands:

```bash
# Set source and target
SCAFFOLD="$CLAUDE_PLUGIN_ROOT/zx-procgen/scaffold/.studio"
TARGET="${1:-.}/.studio"

# Create target if it doesn't exist
mkdir -p "$TARGET"

# Copy entire scaffold (use cp -r for recursive)
cp -r "$SCAFFOLD"/* "$TARGET/"

# Verify copy
if [ -f "$TARGET/generate.py" ]; then
  echo "Copied .studio/ scaffold successfully"
else
  echo "Error: Failed to copy scaffold"
  exit 1
fi
```

## Step 4: Create assets/ Directory

Create the output directory for generated assets:

```bash
mkdir -p "${1:-.}/assets/textures"
mkdir -p "${1:-.}/assets/sounds"
mkdir -p "${1:-.}/assets/meshes"
mkdir -p "${1:-.}/assets/characters"
mkdir -p "${1:-.}/assets/animations"
mkdir -p "${1:-.}/assets/music"
```

## Step 5: Create .gitignore for Assets

Create `.gitignore` in assets/ to exclude generated files (regenerate from specs):

```
# Generated assets - regenerate with: python .studio/generate.py
*
!.gitignore
```

Use the Write tool to create `assets/.gitignore`.

## Step 6: Report Success

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

  assets/                   # Generated output (gitignored)

Quick Start:
  1. Create specs in .studio/specs/<category>/<name>.spec.py
  2. Run: python .studio/generate.py
  3. Generated assets appear in assets/

Commands:
  python .studio/generate.py              # Generate all
  python .studio/generate.py --only textures  # Generate one type
  python .studio/generate.py --dry-run    # Preview
  python .studio/generate.py --list       # List specs
```

## Edge Cases

### Already Initialized
If `.studio/` already exists:
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
