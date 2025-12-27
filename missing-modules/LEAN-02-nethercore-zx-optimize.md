# nethercore-zx-optimize (LEAN VERSION)

## Priority: CRITICAL

Minimal viable optimization plugin. 2 skills, 2 agents.

---

## Plugin Creation Prompt

```
Create a lean Claude Code plugin called "nethercore-zx-optimize" for optimizing Nethercore ZX games.

DESIGN PRINCIPLES:
- 2 skills max - consolidated reference
- Agents do the analysis work
- Concrete, actionable content only
- Target: <3000 tokens total skill content

CONTEXT:
- ZX limits: 16MB ROM, 4MB RAM, 4MB VRAM
- WASM code: up to 4MB, data pack: up to 12MB
- Textures: BC7 compression available (4:1 ratio)
- Meshes: 16 vertex formats with packing options
- State snapshot performance depends on active memory

SKILLS TO CREATE:

1. "resource-budgets" (v1.0.0)
   Complete resource planning in ONE skill:

   ## Limits
   | Resource | Limit | Typical |
   |----------|-------|---------|
   | ROM | 16 MB | 8-12 MB |
   | WASM | 4 MB | 0.5-2 MB |
   | Data | 12 MB | 4-10 MB |
   | RAM | 4 MB | 1-3 MB |
   | VRAM | 4 MB | 2-4 MB |

   ## Budget by Asset Type
   - Textures: 40-60% of data pack
   - Meshes: 20-30% of data pack
   - Audio: 10-20% of data pack
   - Animations: 5-15% of data pack

   ## Genre Templates
   - Platformer: Light textures, more animations
   - Racing: Heavy meshes, big textures
   - Fighting: Animation-heavy, moderate textures

   ## Warning Thresholds
   - ROM > 12MB: Optimize assets
   - WASM > 2MB: Check dependencies
   - State > 200KB: Rollback will lag

   Keywords: budget, ROM, RAM, VRAM, memory, size, limit

2. "optimization-techniques" (v1.0.0)
   All optimization methods in ONE skill:

   ## WASM Optimization
   ```bash
   # In Cargo.toml
   [profile.release]
   lto = true
   opt-level = "z"
   codegen-units = 1

   # Post-build
   wasm-opt -Oz game.wasm -o game.wasm
   ```
   Typical savings: 20-40%

   ## Texture Optimization
   - Use BC7 compression (4:1 savings)
   - Power-of-2 dimensions required
   - Lower resolution: 256 vs 512 = 4x smaller
   - Atlas sprites to reduce draw calls

   ## Mesh Optimization
   - Choose minimal vertex format
   - POS only (12B) vs full (40B) = 3x smaller
   - Target poly counts: BG 50-200, props 100-500, characters 500-2000
   - Use octahedral normal encoding

   ## Audio Optimization
   - 22050Hz mono only (engine limit)
   - Shorter samples when possible
   - XM modules for music (much smaller than WAV)

   ## State Size Reduction
   - Separate cosmetic from gameplay state
   - Use compact data types (u8 vs u32)
   - Avoid Vec with capacity, use fixed arrays
   - Pool objects instead of dynamic allocation

   Keywords: optimize, compress, reduce, smaller, wasm-opt, BC7

AGENTS TO CREATE:

1. "build-analyzer"
   - Runs nether build, captures output
   - Parses ROM structure breakdown
   - Identifies largest assets
   - Suggests optimization priorities
   - Tools: Bash, Read, Glob
   - Trigger: "analyze build", "what's using space", "ROM breakdown"
   - Model: haiku, Color: blue

2. "optimizer"
   - Applies optimization techniques to project
   - Updates Cargo.toml settings
   - Runs wasm-opt on output
   - Reports size reduction achieved
   - Tools: Read, Write, Bash, Glob
   - Trigger: "optimize", "reduce size", "make smaller"
   - Model: sonnet, Color: green

COMMANDS: None. Agents handle everything.
```

---

## Size Budget

| Component | Target Tokens | Content |
|-----------|---------------|---------|
| resource-budgets | 700 | Tables + templates |
| optimization-techniques | 900 | Concrete techniques |
| build-analyzer agent | 200 | Simple analysis |
| optimizer agent | 300 | Modification task |
| **Total** | **2100** | Under 2.5K |

---

## What NOT to Include

- Asset generation → procgen plugin
- Debug memory inspection → debug plugin (if created)
- Render mode details → zx-dev skills
