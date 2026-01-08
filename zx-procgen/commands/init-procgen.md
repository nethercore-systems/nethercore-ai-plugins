---
description: Install the .studio scaffold (generator + parsers) into a project
argument-hint: "[project-dir]"
allowed-tools: ["Bash", "Write", "Glob"]
color: blue
---

# Init Procgen

Install the unified `.studio/` scaffold into a user project.

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

echo "ai-studio not found; falling back to copying the scaffold from this repo."
SCAFFOLD="ai_studio_core/templates/project/studio"

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
# Generated assets - regenerate with: ai-studio generate
*
!.gitignore
EOF

# Pin core version/config (best-effort; ai-studio init does this automatically)
if [ ! -f "$TARGET/ai_studio.toml" ]; then
  CORE_VERSION="0.1.0"
  if command -v python3 >/dev/null 2>&1; then
    CORE_VERSION="$(python3 - << 'PY'
import re
from pathlib import Path

text = Path("ai_studio_core/__init__.py").read_text(encoding="utf-8")
m = re.search(r'__version__\\s*=\\s*\"([^\"]+)\"', text)
print(m.group(1) if m else "0.1.0")
PY
)"
  fi

  cat > "$TARGET/ai_studio.toml" << EOF
# ai-studio project configuration
core_version = "$CORE_VERSION"

[engine]
default_targets = ["godot"]

[export]
model_3d = "glb"
texture_2d = "png"
audio_sfx = "wav"
music = "xm"

[conventions]
units = "meters"
up_axis = "Y"
forward_axis = "-Z"
scale = 1.0

[paths]
output_root = "generated"
studio_root = ".studio"
EOF
fi
```

## Next

```bash
ai-studio generate
```
