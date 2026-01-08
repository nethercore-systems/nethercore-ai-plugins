---
description: Install/update the unified .studio spec workflow into the current project
argument-hint: "[project-dir]"
allowed-tools: ["Bash"]
---

# Setup Spec Workflow

This is a compatibility alias for installing the `.studio/` scaffold.

Preferred:

```bash
ai-studio init "${1:-.}"
```

If `ai-studio` is not available, use:

```bash
/init-procgen "${1:-.}"
```

