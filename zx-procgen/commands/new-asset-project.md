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
fi
```

