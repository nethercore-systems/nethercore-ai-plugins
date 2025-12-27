# Gap 3: Platform Page Assets

**Status:** `[ ]` Not Started
**Priority:** HIGH
**Plugin:** nethercore-zx-publish
**Type:** Skill

---

## Problem

Publishing requires visual assets that no plugin helps create. NOT covered at all.

## What's Missing

- Thumbnail creation (256×256 PNG icon for library)
- Screenshot capture (up to 5 PNGs for platform page)
- Platform description copywriting (compelling game descriptions)
- Tag/category selection guidance

## Prompt for Implementation

```
Add skill "platform-assets" to nethercore-zx-publish. Triggers: "thumbnail", "icon",
"screenshot", "platform page", "store page", "store listing", "game description", "platform listing". Cover: thumbnail
(256×256 PNG, composition, clarity at small size), screenshots (3-5 gameplay images,
what to capture), platform copy (hook, features, call-to-action), tags/categories.
Add /prepare-platform-assets command. Use references/ for copy templates. ~1200 words.
```

## Dependencies

- Gap 2 (Publishing Workflow) - creates the plugin this skill belongs to

## Related Gaps

- Gap 2 (same plugin)
