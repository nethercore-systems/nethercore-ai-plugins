---
description: Guided publishing workflow for Nethercore ZX games
argument-hint: "[project-path]"
allowed-tools: ["Read", "Bash", "AskUserQuestion", "Write"]
---

# Publish Game Workflow

Guide the user through the complete publishing process for their Nethercore ZX game.

## Step 1: Locate Project

**If project path argument ($1) is provided:**
Check if nether.toml exists at that path.

**If no argument provided:**
Look for nether.toml in the current directory:

```bash
test -f nether.toml && echo "FOUND" || echo "NOT_FOUND"
```

If not found, ask user for the project path using AskUserQuestion.

## Step 2: Validate Manifest

Read and parse the nether.toml file. Check for:

1. **Required fields present:**
   - `[game].id` - Game identifier
   - `[game].title` - Display name
   - `[game].author` - Creator credit
   - `[game].version` - Semantic version

2. **Recommended fields:**
   - `[game].description` - Game description
   - `[game].tags` - Searchable keywords

Report any missing required fields and offer to help add them.

If description is missing, ask if user wants help writing one:
- "Would you like help writing a compelling game description?"
- If yes, ask about: genre, core gameplay, unique features, multiplayer support
- Generate a description following the template from the platform-assets skill

## Step 3: Build Check

Run the build to verify everything compiles:

```bash
nether build
```

Report the result:
- **Success:** Proceed to next step
- **Failure:** Show error and ask user to fix before continuing

## Step 4: Asset Inventory

Check for required and optional assets:

**Required:**
- [ ] Game file (.wasm or .nczx from build)

**Platform assets (check if they exist):**
```bash
# Check for common icon locations
test -f icon.png && echo "icon.png found"
test -f assets/icon.png && echo "assets/icon.png found"

# Check for screenshots
ls -1 screenshot*.png 2>/dev/null
ls -1 assets/screenshot*.png 2>/dev/null
```

Report what was found and what's missing:
- **Icon (64x64 PNG):** Required for upload
- **Screenshots:** Recommended (up to 5)
- **Banner (1280x720):** Optional, for featured games

If icon is missing, suggest:
"Run `/prepare-platform-assets` to create your icon and screenshots."

## Step 5: Pre-Release Verification

Run multiplayer tests if applicable:

Ask user: "Does your game support multiplayer?"

If yes, suggest running:
```bash
nether run --sync-test   # Test rollback determinism
nether run --p2p-test    # Two-instance netplay test
```

## Step 6: Size Check

Check the ROM/WASM size:

```bash
# Find the built file
ls -la *.nczx 2>/dev/null || ls -la target/wasm32-unknown-unknown/release/*.wasm 2>/dev/null
```

Report size and compare to 16MB limit:
- **Under 10MB:** Comfortable margin
- **10-14MB:** Consider optimization
- **14-16MB:** Near limit, may want to reduce
- **Over 16MB:** Must reduce size before upload

## Step 7: Upload Checklist

Present the final checklist:

```
READY TO PUBLISH
================

Game: [title] v[version]
By: [author]

Files Ready:
[x] Game file: [filename] ([size])
[x/] Icon: [status]
[x/] Screenshots: [count] found
[x/] Banner: [status]

Manifest:
[x] ID: [id]
[x] Title: [title]
[x] Author: [author]
[x] Version: [version]
[x/] Description: [present/missing]
[x/] Tags: [count] tags
```

## Step 8: Upload Instructions

Provide upload instructions:

```
UPLOAD STEPS
============

1. Go to: https://nethercore.systems/dashboard

2. Click "Upload New Game"

3. Fill in the form:
   - Title: [title]
   - Description: [paste description if generated]
   - Category: [suggest based on tags/description]
   - Tags: [list from manifest]

4. Upload files:
   - Game: [path to .nczx or .wasm]
   - Icon: [path to icon.png]
   - Screenshots: [list paths]

5. Click "Publish"

Your game page will be at:
https://nethercore.systems/game/[id]
```

## Step 9: Post-Publish

After user confirms upload:

Remind them about:
- Sharing their game page URL
- Collecting feedback
- Version update process (bump version in nether.toml, rebuild, re-upload)

Suggest: "When you're ready to update, bump the version in nether.toml and run `/publish-game` again."
