# ZX Render Modes Reference

Render mode is configured in `nether.toml` as a build-time setting. Each mode requires different texture maps.

```toml
# nether.toml
[render]
mode = 2  # 0=Lambert, 1=Matcap, 2=MR, 3=SS
```

## Mode 0: Lambert/Unlit (1 map)

The simplest mode - texture multiplied by vertex color.

| Slot | Texture | Purpose |
|------|---------|---------|
| 0 | Albedo | RGB base color |

**Shading:**
- Without normals: `final = texture * vertex_color`
- With normals: Lambert with sun direction and sky ambient

**Use:** UI, sprites, flat-shaded retro graphics, performance-critical scenes

---

## Mode 1: Matcap (up to 4 maps)

View-space normal sampling from matcap textures. Lighting is "baked" into the matcap.

| Slot | Texture | Sampled By |
|------|---------|------------|
| 0 | Albedo | UV coordinates |
| 1 | Matcap 1 | View-space normal |
| 2 | Matcap 2 | View-space normal |
| 3 | Matcap 3 | View-space normal |

### Blend Modes

| Mode | Value | Effect | Use Case |
|------|-------|--------|----------|
| Multiply | 0 | Darkens | Shadows, AO, toon bands |
| Add | 1 | Brightens | Highlights, rim, glow |
| HSV Modulate | 2 | Hue shift | Iridescence, rainbow |

### How Matcaps Work

```
view_normal = transform_to_view_space(surface_normal)
matcap_uv = view_normal.xy * 0.5 + 0.5
final = albedo * vertex_color * matcap1 * matcap2 * matcap3
```

See `matcap-generation.md` for the complete matcap library (20+ types).

---

## Mode 2: Metallic-Roughness (2 maps)

PBR-inspired normalized Blinn-Phong with energy conservation.

| Slot | Texture | Channels |
|------|---------|----------|
| 0 | Albedo | RGB: Diffuse color |
| 1 | MRE | R: Metallic, G: Roughness, B: Emissive |

### MRE Channel Values

| Channel | 0.0 | 1.0 |
|---------|-----|-----|
| Metallic (R) | Dielectric (plastic) | Full metal |
| Roughness (G) | Mirror smooth | Fully diffuse |
| Emissive (B) | No glow | Max self-illumination |

### Common Material Presets

| Material | Metallic | Roughness |
|----------|----------|-----------|
| Polished metal | 0.9 | 0.2 |
| Brushed metal | 0.9 | 0.4 |
| Plastic | 0.0 | 0.5 |
| Rubber | 0.0 | 0.9 |
| Glass | 0.0 | 0.1 |

---

## Mode 3: Specular-Shininess (3 maps)

Classic Blinn-Phong with explicit specular control. Era-authentic PS1/N64/Saturn aesthetic.

| Slot | Texture | Channels |
|------|---------|----------|
| 0 | Albedo | RGB: Diffuse color |
| 1 | SSE | R: Specular Damping, G: Shininess, B: Emissive |
| 2 | Specular | RGB: Specular highlight tint |

### SSE Channel Values

| Channel | 0.0 | 1.0 |
|---------|-----|-----|
| Specular Damping (R) | Full specular | No specular |
| Shininess (G) | Diffuse (exp=1) | Mirror (exp=256) |
| Emissive (B) | No glow | Max glow |

**Note:** Specular Damping (R) should usually be 0. Only increase for worn/dirty areas.

---

## Mode Selection Guide

| Goal | Mode | Why |
|------|------|-----|
| Best performance | 0 | Single texture |
| Stylized toon | 1 | Matcap lighting |
| Modern PBR look | 2 | Metallic-roughness |
| Retro PS1/N64 | 3 | Classic Blinn-Phong |
| Emissive effects | 2 or 3 | B channel = emissive |

See `mre-sse-generation.md` for texture generation examples.
