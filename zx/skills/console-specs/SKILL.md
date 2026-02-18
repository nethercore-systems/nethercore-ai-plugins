---
name: console-specs
description: >-
  ZX fantasy console hardware specifications and resource budgets. Covers
  resolution (960x540), memory limits (4 MB RAM/VRAM, 16 MB ROM), render
  modes, audio system (22 kHz, 16 channels), and input layout. Use when
  planning resource budgets or checking console capabilities.
license: Apache-2.0
compatibility: ZX console only.
metadata:
  author: nethercore-systems
  version: "1.0.0"
---

# ZX Console Specifications

## Core Specs

| Spec | Value |
|------|-------|
| Resolution | 960x540 fixed (16:9) |
| Color depth | 32-bit RGBA8 |
| ROM | 16 MB max |
| RAM | 4 MB |
| VRAM | 4 MB |
| Tick rate | 24/30/60/120 fps |
| Max players | 4 |
| Alpha | 2-bit Bayer 4x4 |

## Render Modes

Choose ONE in `init()` - cannot change at runtime.

| Mode | Name | Best For |
|------|------|----------|
| 0 | Lambert | 2D, flat stylized |
| 1 | Matcap | Stylized 3D, toon |
| 2 | MR-Blinn-Phong | PBR, realistic |
| 3 | Blinn-Phong | Retro 5th-gen |

## Audio System

| Spec | Value |
|------|-------|
| Sample rate | 22,050 Hz |
| Format | 16-bit signed PCM, mono |
| Sound channels | 16 simultaneous |
| Music channel | 1 dedicated |

## Input (6th-gen Controller)

| Input | Type |
|-------|------|
| D-Pad | 4-way digital |
| Face buttons | A, B, X, Y |
| Bumpers | L1, R1 (digital) |
| Triggers | L2, R2 (analog 0-1) |
| Sticks | Left + Right (analog -1 to 1) |
| Menu | Start, Select |

## What ZX Excels At

- 3D platformers and action games
- Fighting games (4-player, rollback)
- Racing games
- Third-person adventures
- Split-screen local multiplayer
- Online competitive games

## What Requires Planning

- Large open worlds (16 MB ROM)
- Orchestral soundtracks (16 channels)
- Massive texture counts (4 MB VRAM)
