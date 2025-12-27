---
description: Prepare marketing assets for nethercore.systems (icon, screenshots, description)
argument-hint: "[project-path]"
allowed-tools: ["Read", "Bash", "AskUserQuestion", "Write"]
---

# Prepare Platform Assets

Guide the user through creating all required marketing assets for their game's platform page.

## Step 1: Locate Project

**If project path argument ($1) is provided:**
Check if nether.toml exists at that path.

**If no argument provided:**
Look for nether.toml in the current directory:

```bash
test -f nether.toml && echo "FOUND" || echo "NOT_FOUND"
```

If not found, ask user for the project path.

## Step 2: Assess Current Assets

Check what assets already exist:

```bash
# Check for icon
echo "=== Icon ==="
test -f icon.png && echo "icon.png exists" && file icon.png
test -f assets/icon.png && echo "assets/icon.png exists" && file assets/icon.png

# Check for screenshots
echo "=== Screenshots ==="
ls -la screenshot*.png 2>/dev/null
ls -la assets/screenshot*.png 2>/dev/null

# Check for banner
echo "=== Banner ==="
test -f banner.png && echo "banner.png exists"
test -f assets/banner.png && echo "assets/banner.png exists"
```

Read nether.toml to check if description exists.

Report status:
- Icon: [found/missing] - Required
- Screenshots: [count] found - Recommended (up to 5)
- Banner: [found/missing] - Optional
- Description: [present/missing] - Recommended

## Step 3: Asset Selection

Use AskUserQuestion to determine which assets to work on:

- Question: "Which assets would you like to prepare?"
- Header: "Assets"
- multiSelect: true
- Options:
  - **Game Icon (64x64)** - Required for platform
  - **Screenshots (up to 5)** - Recommended for game page
  - **Banner (1280x720)** - Optional for featured section
  - **Game Description** - Recommended for discoverability

## Step 4: Icon Creation

If user selected icon:

### Check for existing images

```bash
# Find potential source images
find . -name "*.png" -type f 2>/dev/null | head -20
```

### Ask about source

Use AskUserQuestion:
- Question: "How would you like to create your icon?"
- Header: "Icon Source"
- Options:
  - **From screenshot** - Crop from a game screenshot
  - **From existing image** - Resize an existing asset
  - **Design tips only** - Just give me guidelines

### Provide guidance

**If from screenshot:**
1. Suggest running the game and capturing a screenshot at a good moment
2. Explain how to crop to 64x64 focusing on key element
3. Recommend tools (GIMP, Paint.NET, Photopea)

**If from existing image:**
Ask which image, then provide resize command:
```bash
# Using ImageMagick (if available)
convert [source.png] -resize 64x64 -sharpen 0x1 icon.png
```

**Design tips:**
- Use bold, simple shapes
- High contrast colors (visible on dark #1a1a2e background)
- Center the focal point
- Avoid text (illegible at 64x64)
- Include recognizable game element

## Step 5: Screenshots

If user selected screenshots:

### Capture instructions

Ask about the game's current state:
- Question: "Is your game in a state where you can capture good screenshots?"
- Header: "Capture"
- Options:
  - **Ready now** - Game looks good, ready to capture
  - **Need to prepare** - Need to disable debug UI, reach good point
  - **Just guidance** - Tell me what to capture

### Capture guidance

**What to capture (in order of importance):**
1. **Hero shot** - Most visually impressive moment
2. **Core gameplay** - Typical gameplay in action
3. **Variety** - Different levels, modes, or areas
4. **Features** - Unique mechanics, power-ups
5. **Multiplayer** - If applicable, show multiple players

**Technical notes:**
- Resolution: 960x540 (native) or 1920x1080 (2x)
- Format: PNG (lossless) or high-quality JPG
- Disable debug UI before capturing
- Capture during gameplay, not menus

**Capture methods:**
```bash
# Windows: Win+Shift+S for screen snip
# Or run in windowed mode at exact resolution
nether run
# Then use any screenshot tool
```

## Step 6: Description Writing

If user selected description:

### Gather information

Use AskUserQuestion to collect info:

**Question 1:**
- Question: "What genre best describes your game?"
- Header: "Genre"
- Options:
  - Arcade / Shooter
  - Platformer
  - Puzzle
  - Racing
  - Action / Fighting
  - (User can type custom)

**Question 2:**
- Question: "What makes your game unique or special?"
- Header: "Unique"
- Options: (free text encouraged)

**Question 3:**
- Question: "Does your game support multiplayer?"
- Header: "Multiplayer"
- Options:
  - Local multiplayer (2-4 players)
  - Online multiplayer
  - Both local and online
  - Single player only

### Generate description

Based on answers, generate a description following this structure:

```markdown
[Compelling hook - action + setting + stakes]

## About

[2-3 sentences describing gameplay and what makes it special]

## Features

- [Key feature 1 with specifics]
- [Key feature 2 with specifics]
- [Key feature 3 with specifics]
- [Multiplayer mention if applicable]
```

Present the draft and ask if they want to refine it.

### Update manifest

Offer to add the description to nether.toml:

```toml
[game]
description = """
[The generated description]
"""
```

## Step 7: Banner (Optional)

If user selected banner:

Provide guidance only (banners require more design work):

**Specifications:**
- Size: 1280x720 pixels
- Format: PNG or high-quality JPG
- Safe zone: Keep key elements in center 80%

**Approach:**
1. Start with a compelling screenshot as base
2. Add game title/logo
3. Apply cinematic composition (rule of thirds)
4. Ensure title is readable at thumbnail size

**Tools:**
- GIMP (free)
- Photopea (free, web-based)
- Canva (templates available)

## Step 8: Summary

After completing selected tasks, summarize:

```
ASSET PREPARATION COMPLETE
==========================

[x] Icon: [status and location]
[x] Screenshots: [count] at [locations]
[x] Banner: [status]
[x] Description: [added to manifest / provided]

Next step: Run `/publish-game` to begin the upload process.
```

If any required assets are still missing, note them:

```
Still needed before publishing:
- Icon (required): Create a 64x64 PNG
```
