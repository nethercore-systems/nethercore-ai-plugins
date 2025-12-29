# zx-optimize

Optimization plugin for Nethercore ZX games. Provides resource budgeting guidance, optimization techniques, and automated analysis for ROM size, WASM, RAM, VRAM, and asset optimization.

## Features

- **Resource budget planning** for ZX console limits
- **Optimization techniques** for WASM, textures, meshes, audio, and state
- **Automated build analysis** to identify largest assets
- **Automated optimization** applying best practices

## Skills

### resource-budgets
Complete resource planning for ZX games including:
- Console limits (16MB ROM, 4MB WASM, 4MB RAM, 4MB VRAM)
- Budget allocation by asset type
- Genre-specific templates (platformer, racing, fighting, RPG)
- State snapshot sizing for rollback netcode

**Triggers:** "budget", "ROM size", "RAM limit", "VRAM budget", "memory", "size limits"

### optimization-techniques
All optimization methods in one place:
- WASM optimization (LTO, opt-level, wasm-opt)
- Texture optimization (BC7, resolution, atlasing)
- Mesh optimization (vertex formats, poly counts)
- Audio optimization (XM modules, sample rates)
- State size reduction (compact types, fixed arrays)

**Triggers:** "optimize", "compress", "reduce size", "wasm-opt", "BC7"

## Agents

### build-analyzer
Runs `nether build` and analyzes output to:
- Parse ROM structure breakdown
- Identify largest assets
- Compare against resource budgets
- Suggest optimization priorities

**Triggers:** "analyze build", "what's using space", "ROM breakdown"
**Model:** haiku | **Color:** blue

### optimizer
Applies optimization techniques to the project:
- Updates Cargo.toml settings
- Runs wasm-opt on output
- Reports size reduction achieved

**Triggers:** "optimize", "reduce size", "make smaller"
**Model:** sonnet | **Color:** green

## Usage

### Check resource budgets
```
"What are the ZX memory limits?"
"How should I budget my data pack?"
"What's a good state size for rollback?"
```

### Learn optimization techniques
```
"How do I optimize my WASM binary?"
"What texture compression should I use?"
"How can I reduce my state size?"
```

### Analyze your build
```
"What's taking up space in my build?"
"Analyze my ROM for optimization"
"My ROM is 14MB, what should I cut?"
```

### Apply optimizations
```
"Optimize my game build"
"Apply WASM optimizations"
"Reduce my ROM size"
```

## Installation

Add to your `.claude/settings.local.json`:

```json
{
  "enabledPlugins": {
    "zx-optimize@nethercore-ai-plugins": true
  }
}
```

## License

MIT/Apache-2.0
