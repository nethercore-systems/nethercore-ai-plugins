# Minor Improvements

**Status:** `[ ]` Not Started
**Priority:** LOW
**Type:** Maintenance

---

## Tasks

### 1. Version Standardization
- [ ] Set all plugins to version 1.0
- [ ] Update all plugin.json files

### 2. License Standardization
- [ ] Set license to MIT & Apache 2.0 (similar to Rust projects)
- [ ] Add LICENSE-MIT and LICENSE-APACHE files at repo root (nethercore-ai-plugins/)
- [ ] Update plugin.json license fields in each plugin

### 3. Documentation Consistency
- [ ] Ensure root CLAUDE.md is complete and up to date
- [ ] Ensure all plugins have marketplace descriptions in plugin.json
- [ ] Verify all skill triggers are documented
- [ ] Check all cross-references between skills

## Implementation Checklist

**Root level (nethercore-ai-plugins/):**
```
[ ] LICENSE-MIT file exists
[ ] LICENSE-APACHE file exists
[ ] CLAUDE.md is complete and current
```

**Per plugin:**
```
nethercore-zx-dev/
  [ ] plugin.json version: 1.0
  [ ] plugin.json license: MIT/Apache-2.0
  [ ] plugin.json marketplace description complete
  [ ] All skills documented

nethercore-zx-game-design/
  [ ] plugin.json version: 1.0
  [ ] plugin.json license: MIT/Apache-2.0
  [ ] plugin.json marketplace description complete
  [ ] All skills documented

nethercore-zx-procgen/
  [ ] plugin.json version: 1.0
  [ ] plugin.json license: MIT/Apache-2.0
  [ ] plugin.json marketplace description complete
  [ ] All skills documented
```

## Notes

- License files go at repo root only, not in each plugin folder
- CLAUDE.md is at repo root only, not per-plugin
- Each plugin.json references the license but doesn't need its own license file
- These are low-priority housekeeping tasks that should be done when convenient
