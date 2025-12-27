# Memory Budget Calculator

Use these templates to plan asset allocation for Nethercore ZX games.

## ROM Budget Template (16 MB Total)

Copy and fill in for your game:

```
=== ROM BUDGET (16 MB = 16,777,216 bytes) ===

WASM Code
├── Game logic: _______ KB
├── Libraries:  _______ KB
└── Subtotal:   _______ KB (~50-200 KB typical)

Meshes
├── Characters: _______ KB × __ count = _______ KB
├── Environments: _____ KB × __ count = _______ KB
├── Props:      _______ KB × __ count = _______ KB
├── Effects:    _______ KB × __ count = _______ KB
└── Subtotal:   _______ MB

Textures (BC7 compressed for modes 1-3, RGBA8 for mode 0)
├── Character diffuse:  _______ KB × __ count = _______ KB
├── Character material: _______ KB × __ count = _______ KB
├── Environment:        _______ KB × __ count = _______ KB
├── UI/HUD:             _______ KB × __ count = _______ KB
├── Effects:            _______ KB × __ count = _______ KB
└── Subtotal:           _______ MB

Audio
├── SFX:   _______ sounds × _______ KB avg = _______ KB
├── Music: _______ tracks × _______ KB avg = _______ KB
└── Subtotal: _______ MB

Animations
├── Character anims: _______ KB × __ characters = _______ KB
├── Object anims:    _______ KB × __ objects = _______ KB
└── Subtotal:        _______ KB

Fonts & UI
├── Fonts:    _______ KB
├── UI atlas: _______ KB
└── Subtotal: _______ KB

==========================================
TOTAL:        _______ MB / 16 MB
REMAINING:    _______ MB
==========================================
```

## Texture Size Reference

BC7 compressed sizes (modes 1-3):
| Resolution | BC7 Size |
|------------|----------|
| 64×64 | 4 KB |
| 128×128 | 16 KB |
| 256×256 | 64 KB |
| 512×512 | 256 KB |
| 1024×1024 | 1 MB |

RGBA8 uncompressed sizes (mode 0):
| Resolution | RGBA8 Size |
|------------|------------|
| 64×64 | 16 KB |
| 128×128 | 64 KB |
| 256×256 | 256 KB |
| 512×512 | 1 MB |

## Audio Size Reference

22,050 Hz, 16-bit mono PCM:
| Duration | Size |
|----------|------|
| 0.5 sec | 22 KB |
| 1 sec | 44 KB |
| 5 sec | 220 KB |
| 30 sec | 1.3 MB |
| 1 min | 2.6 MB |

**Recommendation:** Use nether-qua compression for longer sounds.

## RAM Budget Template (4 MB Total)

Game state should be minimal for fast rollback:

```
=== RAM BUDGET (4 MB = 4,194,304 bytes) ===

Game State (snapshotted for rollback)
├── Player state: _______ bytes × __ players = _______ bytes
├── Entity state: _______ bytes × __ entities = _______ bytes
├── World state:  _______ bytes
├── Input buffer: _______ bytes
└── Subtotal:     _______ KB (target < 100 KB for fast rollback)

Working Memory (not snapshotted)
├── Stack:        _______ KB
├── Heap:         _______ KB
├── Temp buffers: _______ KB
└── Subtotal:     _______ MB

==========================================
TOTAL:        _______ MB / 4 MB
==========================================
```

**Rollback performance targets:**
- 50 KB state: ~0.25ms per snapshot
- 100 KB state: ~0.5ms per snapshot
- 8-frame rollback: multiply by 8

## VRAM Budget Template (4 MB Total)

Active GPU resources:

```
=== VRAM BUDGET (4 MB = 4,194,304 bytes) ===

Loaded Textures
├── Active scene: _______ textures × _______ KB = _______ MB
├── Characters:   _______ textures × _______ KB = _______ MB
├── Effects:      _______ textures × _______ KB = _______ MB
└── Subtotal:     _______ MB

Mesh Buffers
├── Scene geometry:     _______ KB
├── Character meshes:   _______ KB
├── Dynamic geometry:   _______ KB
└── Subtotal:           _______ MB

==========================================
TOTAL:        _______ MB / 4 MB
==========================================
```

## Example Budgets

### Fighting Game (12 MB ROM)

```
WASM Code:        150 KB
Meshes:
├── 8 characters × 200 KB = 1.6 MB
├── 4 stages × 500 KB = 2 MB
├── Effects: 200 KB
└── Subtotal: 3.8 MB

Textures:
├── Character (8 × 512×512 diffuse + 256×256 MRE) = 2.5 MB
├── Stages (4 × 1024×1024): 4 MB
├── UI: 200 KB
└── Subtotal: 6.7 MB

Audio:
├── SFX (50 × 30 KB): 1.5 MB
├── Music (4 × 100 KB loops): 400 KB
└── Subtotal: 1.9 MB

Animations:
├── 8 characters × 100 KB: 800 KB
└── Subtotal: 800 KB

TOTAL: ~12.4 MB (fits with margin)
```

### 3D Platformer (10 MB ROM)

```
WASM Code:        200 KB
Meshes:
├── Player + enemies: 1 MB
├── 20 levels × 100 KB: 2 MB
├── Props: 500 KB
└── Subtotal: 3.5 MB

Textures:
├── Characters: 500 KB
├── Environments: 3 MB
├── UI: 200 KB
└── Subtotal: 3.7 MB

Audio:
├── SFX: 500 KB
├── Music: 1.5 MB
└── Subtotal: 2 MB

Animations: 400 KB

TOTAL: ~9.8 MB (fits well)
```
