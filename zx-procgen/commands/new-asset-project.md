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
  echo "ERROR: ai-studio not found."
  echo
  echo "Install the pinned core CLI, then retry:"
  echo "  python3 -m pip install -r requirements-core.txt"
  exit 2
fi
```
