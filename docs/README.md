# Nethercore AI Plugins Documentation

Cross-plugin workflow guides and integration documentation.

## Cross-Plugin Guides

| Guide | Description |
|-------|-------------|
| [Audio Pipeline](audio-pipeline.md) | End-to-end audio workflow across sound-design, zx-procgen, and tracker-music |

## Plugin-Specific Documentation

Each plugin has its own README.md with detailed usage:

| Plugin | Purpose |
|--------|---------|
| [sound-design](../sound-design/README.md) | Audio design, Sonic Style Language, SFX/music specs |
| [tracker-music](../tracker-music/README.md) | XM/IT music generation, pattern design |
| [zx-procgen](../zx-procgen/README.md) | Procedural asset synthesis (textures, meshes, audio) |

## Quick Reference

### Audio Pipeline
```
sound-design → zx-procgen → tracker-music
   DESIGN       SYNTHESIS    COMPOSITION
```

### Visual Asset Pipeline
```
creative-direction → zx-procgen → zx-dev
     VISION          SYNTHESIS    INTEGRATION
```

### Full Game Pipeline
```
zx-game-design → zx-procgen → zx-dev → zx-test → zx-publish
    DESIGN        ASSETS       CODE     TEST      RELEASE
```
