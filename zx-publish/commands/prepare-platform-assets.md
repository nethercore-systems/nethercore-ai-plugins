---
description: Prepare marketing assets for nethercore.systems (icon, screenshots, description)
argument-hint: "[project-path]"
allowed-tools: ["Read", "Bash", "AskUserQuestion", "Write"]
---

# Prepare Platform Assets

Guide the user through creating marketing assets for their game's platform page.

## Steps

### 1. Locate Project
Check for `nether.toml` in current directory or provided path.

### 2. Assess Current Assets
Check for existing:
- Icon (64x64 PNG)
- Screenshots
- Banner (1280x720)
- Description in nether.toml

### 3. Asset Selection
Ask user which assets to prepare (multiSelect):
- Game Icon (required)
- Screenshots (recommended)
- Banner (optional)
- Game Description (recommended)

### 4. Icon Creation
If selected:
- Check for existing images to crop/resize
- Provide guidance: bold shapes, high contrast, no text
- ImageMagick command: `convert source.png -resize 64x64 -sharpen 0x1 icon.png`

### 5. Screenshots
If selected:
- Capture at 960x540 or 1920x1080
- What to capture: hero shot, gameplay, variety, features
- Disable debug UI before capturing

### 6. Description Writing
If selected:
- Ask about genre, unique features, multiplayer
- Generate description using template:

```markdown
[Hook - action + setting]

## About
[2-3 sentences]

## Features
- [Specific feature]
```

Offer to add to nether.toml.

### 7. Summary
Report:
- Assets created/located
- What's still missing
- Next step: `/publish-game`
