# Minor Improvements

**Status:** `[x]` Complete
**Priority:** LOW
**Type:** Maintenance

---

## Tasks

### 1. Version Standardization
- [x] Set all plugins to version 1.0
- [x] Update all plugin.json files

### 2. License Standardization
- [x] Set license to MIT & Apache 2.0 (similar to Rust projects)
- [x] Add LICENSE-MIT and LICENSE-APACHE files at repo root (nethercore-ai-plugins/)
- [x] Update plugin.json license fields in each plugin

### 3. Documentation Consistency
- [x] Ensure root CLAUDE.md is complete and up to date
- [x] Ensure all plugins have marketplace descriptions in plugin.json
- [x] Verify all skill triggers are documented
- [x] Check all cross-references between skills

## Implementation Checklist

**Root level (nethercore-ai-plugins/):**
```
[x] LICENSE-MIT file exists
[x] LICENSE-APACHE file exists
[x] CLAUDE.md is complete and current
```

**Per plugin:**
```
nethercore-zx-dev/
  [x] plugin.json version: 1.0
  [x] plugin.json license: MIT/Apache-2.0
  [x] plugin.json marketplace description complete
  [x] All skills documented

nethercore-zx-game-design/
  [x] plugin.json version: 1.0
  [x] plugin.json license: MIT/Apache-2.0
  [x] plugin.json marketplace description complete
  [x] All skills documented

nethercore-zx-procgen/
  [x] plugin.json version: 1.0
  [x] plugin.json license: MIT/Apache-2.0
  [x] plugin.json marketplace description complete
  [x] All skills documented

nethercore-zx-publish/
  [x] plugin.json version: 1.0
  [x] plugin.json license: MIT/Apache-2.0
  [x] plugin.json marketplace description complete
  [x] All skills documented

nethercore-zx-orchestrator/
  [x] plugin.json version: 1.0
  [x] plugin.json license: MIT/Apache-2.0
  [x] plugin.json marketplace description complete
  [x] All skills documented
```

## Notes

- License files go at repo root only, not in each plugin folder
- CLAUDE.md is at repo root only, not per-plugin
- Each plugin.json references the license but doesn't need its own license file
- These are low-priority housekeeping tasks that should be done when convenient
