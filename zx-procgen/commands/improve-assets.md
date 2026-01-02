---
description: Guided quality improvement workflow for procedural assets
argument-hint: "[target-tier]"
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash", "Task", "AskUserQuestion"]
---

# Improve Assets

Interactive workflow to upgrade asset quality through the tier system (Placeholder → Temp → Final → Hero).

## Step 1: Asset Discovery

Scan the project for procedural assets:

```bash
# Find all generated asset files
find generated/ -type f \( -name "*.obj" -o -name "*.gltf" -o -name "*.png" -o -name "*.wav" \) 2>/dev/null
```

Also check for generation code:

```bash
# Find generation scripts
find . -name "*gen*.rs" -o -name "*generate*.rs" -o -name "*proc*.rs" 2>/dev/null
```

**If no assets found:**
Report "No assets found. Use /generate-asset or /new-asset-project to create some first."
End the workflow.

## Step 2: Tier Assessment

For each discovered asset, assess its current quality tier:

### Mesh Assessment

Read OBJ/GLTF files and analyze:
```bash
# Count vertices and faces
grep -c "^v " mesh.obj 2>/dev/null
grep -c "^f " mesh.obj 2>/dev/null
grep -c "^vt " mesh.obj 2>/dev/null  # UVs
grep -c "^vn " mesh.obj 2>/dev/null  # Normals
```

**Tier indicators:**
| Indicator | Placeholder | Temp | Final | Hero |
|-----------|-------------|------|-------|------|
| Triangles | < 100 | 100-400 | 400-1000 | 1000+ |
| Has UVs | No | Yes | Yes | Yes |
| Has Normals | No | Yes | Yes | Yes |
| Vertex Colors | No | No | Optional | Yes |

### Texture Assessment

Check PNG files:
```bash
# Get file sizes and dimensions
ls -la generated/textures/*.png 2>/dev/null
file generated/textures/*.png 2>/dev/null
```

**Tier indicators:**
| Indicator | Placeholder | Temp | Final | Hero |
|-----------|-------------|------|-------|------|
| Resolution | 32-64 | 64-128 | 128-256 | 256-512 |
| File Size | < 5KB | 5-20KB | 20-100KB | 100KB+ |
| Channels | 1 (solid) | 2-3 | 4 (full RGBA) | 4 + maps |

### Audio Assessment

Check WAV files:
```bash
# Get audio info
file generated/audio/*.wav 2>/dev/null
ls -la generated/audio/*.wav 2>/dev/null
```

**Tier indicators:**
| Indicator | Placeholder | Temp | Final | Hero |
|-----------|-------------|------|-------|------|
| Duration | < 0.1s | 0.1-0.3s | 0.3-1s | 1s+ layers |
| File Size | < 5KB | 5-20KB | 20-50KB | 50KB+ |

## Step 3: Present Current State

Display a table showing all assets and their assessed tiers:

```markdown
## Asset Quality Assessment

Found [N] assets:

| Asset | Type | Current Tier | Score | Notes |
|-------|------|--------------|-------|-------|
| barrel_01.obj | Mesh | Temp | 58% | Has UVs, needs bevels |
| barrel_01_albedo.png | Texture | Temp | 52% | Low contrast |
| explosion.wav | Audio | Placeholder | 35% | No envelope |
| crate_01.obj | Mesh | Final | 78% | Good quality |

### Tier Distribution
- Placeholder: [N] assets
- Temp: [N] assets
- Final: [N] assets
- Hero: [N] assets
```

## Step 4: Get Target Tier

**If target tier argument ($1) is provided and valid:**
Use that as the target.

**Otherwise, use AskUserQuestion:**

- Question: "What quality tier should we upgrade assets to?"
- Header: "Target"
- Options:
  - **Temp** - Development quality (50-70% score)
  - **Final (Recommended)** - Ship-ready production quality (70-90% score)
  - **Hero** - Maximum quality for key assets (90-100% score)
  - **One tier up** - Upgrade each asset by one level

## Step 5: Select Assets to Enhance

**If many assets exist, use AskUserQuestion:**

- Question: "Which assets should we enhance?"
- Header: "Selection"
- multiSelect: true
- Options:
  - **All below target** - Upgrade everything below target tier
  - **Meshes only** - Focus on 3D geometry
  - **Textures only** - Focus on images
  - **Audio only** - Focus on sounds
  - **Specific assets** - I'll specify which ones

## Step 6: Execute Enhancements

For each selected asset, apply tier-appropriate enhancements:

### Enhancement Flow

1. **Read generation code** (if it exists)
2. **Identify enhancement opportunities**
3. **Modify generation parameters**
4. **Regenerate asset** (or modify directly)
5. **Validate improvement**

### Use quality-enhancer Agent

For complex enhancements, invoke the quality-enhancer agent:

```
Task tool call:
  subagent_type: "zx-procgen:quality-enhancer"
  description: "Enhance [asset] to [tier]"
  prompt: "Upgrade [asset_path] from [current_tier] to [target_tier]. Apply appropriate enhancement techniques for [asset_type]."
```

### Enhancement Techniques Summary

**Mesh: → Temp**
- Add UV mapping
- Calculate normals
- Clean geometry

**Mesh: → Final**
- Add bevels (0.02 width)
- Improve silhouette
- Optimize UV coverage

**Mesh: → Hero**
- Add edge loops
- Add secondary shapes
- Add vertex color AO

**Texture: → Temp**
- Add noise layer
- Establish palette

**Texture: → Final**
- Boost contrast
- Add detail layers
- Generate MRE channel

**Texture: → Hero**
- Add wear/damage
- Add all material maps
- Add micro-variation

**Audio: → Temp**
- Add ADSR envelope
- Basic filtering

**Audio: → Final**
- Add layering
- Add effects (compression, reverb)

**Audio: → Hero**
- Add variation
- Add harmonic richness
- Perfect the mix

## Step 7: Report Results

After enhancements complete, present:

```markdown
## Enhancement Complete

### Summary
- **Assets Enhanced:** [N]
- **Time Taken:** [duration]
- **Average Quality Change:** [before]% → [after]%

### Results

| Asset | Before | After | Change | Status |
|-------|--------|-------|--------|--------|
| barrel_01.obj | Temp (58%) | Final (84%) | +26% | Success |
| barrel_01_albedo.png | Temp (52%) | Final (79%) | +27% | Success |
| explosion.wav | Placeholder (35%) | Temp (62%) | +27% | Success |

### Files Modified
1. `generation/barrel.py` - Added bevel pass
2. `generation/barrel_tex.py` - Added contrast boost, detail layers
3. `generation/sfx.py` - Added envelope shaping

### Next Steps
- Run `/improve-assets hero` to upgrade key assets to Hero quality
- Use `quality-analyzer` agent to get detailed quality report
- Review visual results in game viewer
```

## Quick Modes

### Fast Assessment Only

If user says "just assess" or "show me what we have":
- Run steps 1-3 only
- Show current state without making changes

### Specific Asset

If user specifies an asset name:
- Only assess and enhance that asset
- Skip selection step

### Batch Mode

If user says "improve everything" or "upgrade all":
- Skip selection step
- Enhance all assets below target tier

## Error Handling

**No generation code found:**
"I found assets but no generation code. I can:
1. Create generation code from asset analysis
2. Modify assets directly (less flexible)
3. Skip this asset"

**Asset already at target tier:**
"[Asset] is already at [tier] tier. Skip or upgrade to Hero?"

**Enhancement fails:**
"Enhancement of [asset] encountered an issue: [error]
Keeping original asset. Would you like to try a different approach?"

## Tips

- Start with Final tier for shipping games
- Reserve Hero for player characters and key props
- Meshes usually benefit most from bevel addition
- Textures improve significantly with contrast boost
- Audio needs envelope shaping at minimum
