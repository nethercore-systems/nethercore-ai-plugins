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

echo "ERROR: ai-studio not found."
echo
echo "Install the pinned core CLI, then retry:"
echo "  python3 -m pip install -r requirements-core.txt"
exit 2
```

## Next

```bash
ai-studio generate
```
