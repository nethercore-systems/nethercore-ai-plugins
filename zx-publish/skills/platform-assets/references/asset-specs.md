# Platform Asset Specifications

## Game Icon

| Property | Requirement |
|----------|-------------|
| Dimensions | 64x64 pixels (exact) |
| Format | PNG |
| Color | RGBA (transparency supported) |
| Max Size | 50KB |
| DPI | 72 (standard web) |

**Technical Notes:**
- Use PNG-8 (indexed) if possible for smaller files
- PNG-24 for complex gradients/transparency
- Avoid interlacing (unnecessary for small images)
- sRGB color profile recommended

**Testing:**
```
Display at 100% zoom on dark (#1a1a2e) background
Icon should be:
- Immediately recognizable
- Clear focal point
- No muddy colors
```

## Screenshots

| Property | Requirement |
|----------|-------------|
| Dimensions | 960x540 (1x) or 1920x1080 (2x) |
| Aspect Ratio | 16:9 (exact) |
| Format | PNG (preferred) or JPG (90+ quality) |
| Max Count | 5 images |
| Max Size | 2MB per image |

**Resolution Options:**
- **960x540** - Native game resolution, pixel-perfect
- **1920x1080** - 2x upscale, sharper on high-DPI displays

**Capture Settings:**
```
Window mode: Borderless or exact resolution
UI: Game UI only (no debug, no OS chrome)
Compression: PNG lossless or JPG 90+
```

**File Naming:**
```
screenshot-01.png  (hero shot)
screenshot-02.png  (gameplay)
screenshot-03.png  (variety)
...
```

## Banner

| Property | Requirement |
|----------|-------------|
| Dimensions | 1280x720 pixels |
| Aspect Ratio | 16:9 |
| Format | PNG or JPG (90+ quality) |
| Max Size | 1MB |

**Safe Zones:**
```
┌────────────────────────────────────┐
│  ┌──────────────────────────────┐  │
│  │                              │  │
│  │     SAFE ZONE FOR TEXT       │  │
│  │     (center 1000x500)        │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│        ↑ Platform UI may overlay   │
└────────────────────────────────────┘
```

Keep important elements (title, characters) in center 80%.

## Game File

| Property | Requirement |
|----------|-------------|
| Formats | `.wasm` or `.nczx` |
| Max Size | 16MB |
| WASM | Valid WebAssembly module |
| Exports | `init`, `update`, `render` |

**Size Breakdown (typical):**
```
WASM code:     100KB - 500KB
Textures:      1MB - 8MB
Meshes:        500KB - 4MB
Audio:         500KB - 2MB
Music (XM):    100KB - 500KB
──────────────────────────────
Total target:  < 10MB (comfortable)
Hard limit:    16MB
```

## Image Optimization

### PNG Optimization

```bash
# Using optipng (lossless)
optipng -o7 screenshot.png

# Using pngquant (lossy, smaller)
pngquant --quality=80-100 screenshot.png
```

### JPG Optimization

```bash
# Using jpegoptim
jpegoptim --max=90 screenshot.jpg

# Using ImageMagick
convert screenshot.png -quality 90 screenshot.jpg
```

### Icon-Specific

```bash
# Resize from larger source
convert source.png -resize 64x64 icon.png

# Sharpen after resize
convert source.png -resize 64x64 -sharpen 0x1 icon.png
```

## Color Profiles

**Recommended:** sRGB IEC61966-2.1

**Converting:**
```bash
# ImageMagick
convert image.png -colorspace sRGB -profile sRGB.icc output.png
```

**Why sRGB:**
- Web standard
- Consistent across browsers
- No color shift on upload

## Validation Checklist

### Icon
- [ ] Exactly 64x64 pixels
- [ ] PNG format
- [ ] Under 50KB
- [ ] Visible on dark background
- [ ] No transparency issues

### Screenshots
- [ ] 960x540 or 1920x1080
- [ ] 16:9 aspect ratio
- [ ] PNG or high-quality JPG
- [ ] Under 2MB each
- [ ] No debug UI visible
- [ ] In logical viewing order

### Banner
- [ ] Exactly 1280x720
- [ ] PNG or JPG
- [ ] Under 1MB
- [ ] Key elements in safe zone
- [ ] Readable at thumbnail size

### Game File
- [ ] Under 16MB
- [ ] Valid WASM or NCZX
- [ ] Exports correct functions
- [ ] Tested with `nether run`
