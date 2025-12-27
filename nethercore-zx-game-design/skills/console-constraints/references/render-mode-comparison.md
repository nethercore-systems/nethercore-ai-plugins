# Render Mode Comparison

Detailed comparison of ZX's four render modes to help select the right one for your game.

## Quick Decision Matrix

| Game Type | Recommended Mode | Reason |
|-----------|------------------|--------|
| 2D platformer | Mode 0 | Sprites, no lighting overhead |
| Puzzle game | Mode 0 | Simple visuals, performance |
| Toon/cartoon 3D | Mode 1 | Stylized matcap shading |
| Character action | Mode 1 or 3 | Stylized or retro aesthetic |
| Racing game | Mode 2 | Realistic car materials |
| Survival horror | Mode 2 or 3 | Atmospheric lighting |
| Fighting game | Mode 3 | 5th-gen arcade aesthetic |
| Retro 3D | Mode 3 | Era-authentic look |

## Mode 0: Lambert (Unlit/Simple)

### Characteristics
- **Lighting:** None (without normals) or simple Lambert (with normals)
- **Texture format:** RGBA8 uncompressed
- **Texture slots:** 1 (albedo)
- **GPU cost:** Lowest

### Shading Formula

Without normals:
```
final_color = texture_sample * vertex_color
```

With normals:
```
n_dot_l = max(0, dot(normal, sun_direction))
direct = albedo * sun_color * n_dot_l
ambient = albedo * sample_sky(normal) * 0.3
final_color = direct + ambient
```

### Best For
- 2D games using sprites/billboards
- UI elements
- Flat-shaded retro graphics
- Performance-critical scenes
- Games prioritizing art style over realism

### Texture Considerations
- Uses RGBA8 (uncompressed) — larger file sizes
- Full alpha channel support
- No material properties needed

---

## Mode 1: Matcap (Stylized)

### Characteristics
- **Lighting:** Baked into matcap texture
- **Texture format:** BC7 compressed
- **Texture slots:** 4 (albedo + 3 matcaps)
- **GPU cost:** Low

### How It Works
Matcap (Material Capture) samples a spherical texture based on view-space normals. The "lighting" is pre-baked into the matcap texture itself.

### Matcap Texture Slots
- Slot 0: Albedo (base color)
- Slot 1-3: Matcap textures with blend modes:
  - Multiply
  - Add
  - HSV modulate

### Best For
- Cartoon/toon aesthetics
- Metallic surfaces without environment maps
- Stylized character games
- Art styles where consistency matters more than dynamic lighting
- Quick prototyping (easy to achieve good looks)

### Creating Matcaps
- Capture from 3D software (Blender, ZBrush)
- Paint manually for artistic control
- Use reference spheres photographed in desired lighting

---

## Mode 2: MR-Blinn-Phong (PBR-Inspired)

### Characteristics
- **Lighting:** Metallic-roughness workflow with energy conservation
- **Texture format:** BC7 compressed
- **Texture slots:** 2 (albedo + MRE)
- **GPU cost:** Medium
- **Dynamic lights:** 4 + procedural sun

### MRE Texture Channels
- **R:** Metallic (0.0 = dielectric, 1.0 = metal)
- **G:** Roughness (0.0 = smooth/shiny, 1.0 = rough/matte)
- **B:** Emissive intensity

### Shading Model
- Normalized Blinn-Phong (Gotanda 2010)
- Energy-conserving specular
- F0 = 0.04 for dielectrics (derived)
- Full metal uses albedo as specular color

### Best For
- Modern/realistic visual style
- Games with varied material types
- Environments with dynamic lighting
- Racing games (car paint, metal, glass)
- When matching contemporary visual standards

### Material Guidelines
- **Metals:** Metallic = 1.0, colored albedo for tint
- **Plastics:** Metallic = 0.0, moderate roughness
- **Wood/fabric:** Metallic = 0.0, high roughness
- **Glass:** Metallic = 0.0, very low roughness

---

## Mode 3: Blinn-Phong (Retro/Artistic)

### Characteristics
- **Lighting:** Classic specular-shininess with rim lighting
- **Texture format:** BC7 compressed
- **Texture slots:** 3 (albedo + SSE + specular)
- **GPU cost:** Medium
- **Dynamic lights:** 4 + procedural sun

### SSE Texture Channels
- **R:** Specular damping (reduces highlight intensity)
- **G:** Shininess (specular tightness, higher = sharper)
- **B:** Emissive intensity

### Specular Texture
Slot 2 provides explicit specular color (RGB), giving artists direct control.

### Rim Lighting
Built-in rim/fresnel effect with adjustable:
- Intensity
- Power (falloff)

### Best For
- 5th-generation era aesthetic
- Fighting games (arcade look)
- Action games with dramatic lighting
- When artists need explicit specular control
- Retro 3D revival games

### Material Guidelines
- Use specular texture for colored highlights
- SSE shininess controls highlight size
- Rim lighting adds depth to characters
- Lower shininess = broader, softer highlights

---

## Comparison Table

| Aspect | Mode 0 | Mode 1 | Mode 2 | Mode 3 |
|--------|--------|--------|--------|--------|
| Lighting | None/Lambert | Matcap baked | Dynamic PBR | Dynamic classic |
| Texture slots | 1 | 4 | 2 | 3 |
| Texture format | RGBA8 | BC7 | BC7 | BC7 |
| Dynamic lights | No | No | 4 + sun | 4 + sun |
| Material workflow | Albedo only | Matcap | Metallic-roughness | Specular-shininess |
| GPU cost | Lowest | Low | Medium | Medium |
| Best era match | 2D/retro | Stylized | Modern | 5th-gen |

---

## Mode Selection Flowchart

```
Is your game 2D or using sprites?
├── Yes → Mode 0 (Lambert)
└── No → Is realistic lighting important?
          ├── Yes → Do you want PBR materials?
          │         ├── Yes → Mode 2 (MR-Blinn-Phong)
          │         └── No → Mode 3 (Blinn-Phong)
          └── No → Is stylized/toon aesthetic desired?
                    ├── Yes → Mode 1 (Matcap)
                    └── No → Do you want 5th-gen retro look?
                              ├── Yes → Mode 3 (Blinn-Phong)
                              └── No → Mode 2 (MR-Blinn-Phong)
```

---

## Lighting System (Modes 2 & 3)

Both lit modes share the same lighting infrastructure:

### Light Types
- **Directional:** 4 slots (sun-like parallel rays)
- **Point:** Same 4 slots (position + range falloff)
- **Sun:** Automatic from procedural sky

### Light Properties
- Position/direction
- Color (RGBA)
- Intensity (0.0-8.0 for HDR)
- Range (point lights only)

### Procedural Sky
- Hemisphere gradient (horizon to zenith)
- Analytical sun disc
- Provides ambient + directional light

---

## Texture Pipeline by Mode

### Mode 0 (Unlit)
```
Source → RGBA8 (no compression)
```
- Larger files but faster to author
- Full alpha support

### Modes 1-3 (Lit)
```
Source → BC7 compression
```
- ~4:1 compression ratio
- Slight quality loss acceptable for materials
- Faster GPU loading

### Texture Size Recommendations
| Purpose | Resolution |
|---------|------------|
| Character diffuse | 512×512 |
| Character material | 256×256 |
| Environment | 512×512 to 1024×1024 |
| Props | 256×256 |
| UI | Power of 2, as needed |
| Matcaps | 256×256 |
