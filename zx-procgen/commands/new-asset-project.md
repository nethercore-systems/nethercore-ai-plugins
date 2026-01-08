---
description: Create a new asset-only project directory and install the .studio scaffold
argument-hint: "<project-dir>"
allowed-tools:
  - Bash
---

# New Asset Project

Create a new directory and install the unified `.studio/` scaffold into it.

> Prefer `ai-studio init`. This command is a convenience wrapper for quick setup.

```bash
TARGET="${1:?usage: /new-asset-project <project-dir>}"
mkdir -p "$TARGET"

if command -v ai-studio >/dev/null 2>&1; then
  ai-studio init "$TARGET"
else
  echo "ai-studio not found; falling back to /init-procgen scaffold copy."
  # Reuse the init-procgen command’s logic by copying from the repo templates.
  SCAFFOLD="ai_studio_core/templates/project/studio"

  mkdir -p "$TARGET/.studio"
  mkdir -p "$TARGET/.studio/specs" "$TARGET/.studio/direction" "$TARGET/.studio/designs" "$TARGET/.studio/analysis"

  cp -f "$SCAFFOLD/generate.py" "$TARGET/.studio/generate.py"
  rm -rf "$TARGET/.studio/parsers"
  mkdir -p "$TARGET/.studio/parsers"
  cp -R "$SCAFFOLD/parsers/." "$TARGET/.studio/parsers/"

  mkdir -p "$TARGET/generated"

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
fi
```
