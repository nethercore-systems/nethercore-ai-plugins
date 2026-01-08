---
description: Install the .studio scaffold (generator + parsers) into a project
argument-hint: "[project-dir]"
allowed-tools: ["Bash", "Write", "Glob"]
color: blue
---

# Init Procgen

Install the unified `.studio/` scaffold into a user project by copying from `zx-procgen/scaffold/.studio/`.

> Deprecation notice: Prefer `ai-studio init [project-dir]`. This command remains for backward compatibility.

## Behavior (No Prompts)

- Always overwrites:
  - `.studio/generate.py`
  - `.studio/parsers/**`
- Always preserves:
  - `.studio/specs/**`
  - `.studio/direction/**`
  - `.studio/designs/**`
  - `.studio/analysis/**`

## Install

```bash
TARGET="${1:-.}"

echo "[DEPRECATED] zx-procgen:init-procgen → use: ai-studio init [project-dir]"

if command -v ai-studio >/dev/null 2>&1; then
  ai-studio init "$TARGET"
  exit $?
fi

echo "ai-studio not found; falling back to zx-procgen/scaffold/.studio copy."
SCAFFOLD="zx-procgen/scaffold/.studio"

mkdir -p "$TARGET/.studio"
mkdir -p "$TARGET/.studio/specs" "$TARGET/.studio/direction" "$TARGET/.studio/designs" "$TARGET/.studio/analysis"

# Overwrite generator + parsers
cp -f "$SCAFFOLD/generate.py" "$TARGET/.studio/generate.py"
rm -rf "$TARGET/.studio/parsers"
mkdir -p "$TARGET/.studio/parsers"
cp -R "$SCAFFOLD/parsers/." "$TARGET/.studio/parsers/"

# Ensure spec category folders exist (preserve contents)
mkdir -p "$TARGET/.studio/specs/textures"
mkdir -p "$TARGET/.studio/specs/normals"
mkdir -p "$TARGET/.studio/specs/sounds"
mkdir -p "$TARGET/.studio/specs/instruments"
mkdir -p "$TARGET/.studio/specs/music"
mkdir -p "$TARGET/.studio/specs/meshes"
mkdir -p "$TARGET/.studio/specs/characters"
mkdir -p "$TARGET/.studio/specs/animations"

# Create output dirs
mkdir -p "$TARGET/generated/textures"
mkdir -p "$TARGET/generated/normals"
mkdir -p "$TARGET/generated/meshes"
mkdir -p "$TARGET/generated/characters"
mkdir -p "$TARGET/generated/animations"
mkdir -p "$TARGET/generated/sounds/instruments"
mkdir -p "$TARGET/generated/music"

# Gitignore generated outputs
cat > "$TARGET/generated/.gitignore" << 'EOF'
# Generated assets - regenerate with: python .studio/generate.py
*
!.gitignore
EOF
```

## Next

```bash
ai-studio generate
```
