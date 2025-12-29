---
name: Nethercore ZX Platform Assets
description: This skill should be used when the user asks about "thumbnail", "game icon", "screenshot", "platform page", "store page", "store listing", "game description", "platform listing", "banner image", "marketing assets", "game page assets", or mentions preparing visuals for nethercore.systems, writing game descriptions, choosing tags/categories, creating promotional images, or optimizing game presentation for the platform.
version: 1.0.0
---

# Nethercore ZX Platform Assets

## Overview

Publishing to nethercore.systems requires visual assets and compelling copy. This guide covers creating effective thumbnails, screenshots, descriptions, and metadata for maximum visibility and appeal.

## Required Assets

### Game Icon (Required)

**Specifications:**
- Size: 64x64 pixels
- Format: PNG (RGBA)
- Purpose: Library thumbnail, search results

**Best Practices:**
- Use bold, simple shapes visible at small size
- Include recognizable game element (character, logo, key object)
- High contrast colors for visibility
- Avoid text (too small to read)
- Test at actual size before uploading

**Composition Tips:**
- Center the focal point
- Fill the frame (no wasted space)
- Use 2-3 dominant colors
- Consider the dark library background

### Screenshots (Optional but Recommended)

**Specifications:**
- Resolution: 960x540 (native) or 1920x1080 (2x)
- Format: PNG
- Count: Up to 5 images
- Purpose: Game page gallery

**What to Capture:**
1. **Hero shot** - Best visual moment (action, atmosphere)
2. **Gameplay** - Core mechanics in action
3. **Variety** - Different levels, modes, or areas
4. **Features** - Unique selling points
5. **Multiplayer** - If applicable, show co-op/versus

**Capture Guidelines:**
- Capture during actual gameplay, not menus
- Show the game at its best (good lighting, interesting moment)
- Avoid debug UI or development artifacts
- Consistent quality across all screenshots
- Order matters: first screenshot is most prominent

### Banner (Optional)

**Specifications:**
- Size: 1280x720 pixels
- Format: PNG
- Purpose: Featured games section

**Design Approach:**
- Cinematic composition (rule of thirds)
- Game title/logo prominent but not overwhelming
- Show game world or key characters
- Leave space for platform UI overlays
- High visual impact for scrolling users

## Game Description

The description appears on your game's platform page. Markdown is supported.

### Structure

```markdown
A brief, exciting hook sentence that grabs attention.

## About

2-3 sentences describing the game concept and experience.

## Features

- Key feature 1
- Key feature 2
- Key feature 3

## Controls

Brief control overview (optional but helpful)
```

### Writing Tips

**The Hook (First Sentence):**
- Lead with action or emotion
- Make it intriguing
- Keep it under 20 words

**Good:** "Battle through waves of cosmic horrors in this pulse-pounding arcade shooter."
**Bad:** "This is a game where you shoot enemies in space."

**About Section:**
- Describe the experience, not just mechanics
- Mention genre for discoverability
- Highlight what makes it unique

**Features List:**
- 3-5 bullet points
- Start each with action verb
- Be specific, not generic

**Good:** "Master 8 unique weapons with distinct playstyles"
**Bad:** "Multiple weapons"

## Categories and Tags

### Categories

Select the primary category that best fits:

| Category | Description |
|----------|-------------|
| Arcade | Score-focused, quick sessions |
| Action | Combat, reflexes, intensity |
| Puzzle | Logic, problem-solving |
| Platformer | Jumping, traversal |
| Racing | Speed, vehicles, competition |
| Sports | Athletic simulation |
| Strategy | Planning, resource management |
| Adventure | Exploration, story |
| Shooter | Projectile combat |
| Fighting | Versus combat |

### Tags

Tags improve discoverability. Choose 3-5 relevant tags:

**Gameplay Tags:**
- `multiplayer`, `co-op`, `versus`, `singleplayer`
- `local-multiplayer`, `online`
- `high-score`, `time-attack`, `endless`

**Style Tags:**
- `retro`, `pixel-art`, `low-poly`, `stylized`
- `3d`, `2d`, `isometric`, `top-down`, `side-scroller`

**Theme Tags:**
- `sci-fi`, `fantasy`, `horror`, `comedy`
- `space`, `underwater`, `medieval`, `modern`

**Mood Tags:**
- `relaxing`, `intense`, `challenging`, `casual`

## Asset Creation Workflow

### Using Game Screenshots

1. **Run in windowed mode** at 960x540 or 1920x1080
2. **Disable debug UI** for clean captures
3. **Use screenshot tool:**
   ```bash
   # Windows
   Win+Shift+S

   # Or use nether CLI (if available)
   nether run --screenshot
   ```
4. **Save as PNG** (avoid JPEG compression artifacts)

### Creating Icons

**From Screenshot:**
1. Choose your best screenshot
2. Crop to focus on key element
3. Resize to 64x64
4. Sharpen if needed
5. Test visibility at actual size

**From Scratch:**
1. Start at 256x256 for detail work
2. Design with simple shapes
3. Export at 64x64
4. Verify clarity at final size

**Tools:**
- Image editors: GIMP, Photoshop, Aseprite
- Quick edits: Paint.NET, Photopea (web)

### Banner Creation

1. Start with 1280x720 canvas
2. Use in-game assets or screenshots as base
3. Add title/logo with readable font
4. Apply cinematic crop/composition
5. Test at thumbnail size (platform may show smaller)

## Optimization Checklist

Before uploading, verify:

**Icon (64x64):**
- [ ] Recognizable at small size
- [ ] High contrast on dark background
- [ ] No unreadable text
- [ ] PNG format, under 50KB

**Screenshots:**
- [ ] Native resolution (960x540 or 2x)
- [ ] No debug UI visible
- [ ] Show actual gameplay
- [ ] Best moments captured
- [ ] PNG format

**Description:**
- [ ] Compelling hook sentence
- [ ] Clear genre/gameplay explanation
- [ ] Feature bullets with action verbs
- [ ] No spelling/grammar errors
- [ ] Markdown renders correctly

**Tags:**
- [ ] Primary category selected
- [ ] 3-5 relevant tags
- [ ] Mix of gameplay and style tags

## Reference Files

See additional resources:
- `references/copy-templates.md` - Description templates by genre
- `references/asset-specs.md` - Detailed format specifications
