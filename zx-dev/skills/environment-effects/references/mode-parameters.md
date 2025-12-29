# EPU Mode Parameters Reference

Complete parameter documentation for all 8 EPU modes. All color parameters use `0xRRGGBBAA` format.

## Mode 0: env_gradient

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| layer | u32 | 0-1 | Target layer (0=base, 1=overlay) |
| zenith | u32 | 0xRRGGBBAA | Color directly overhead |
| sky_horizon | u32 | 0xRRGGBBAA | Sky color at horizon |
| ground_horizon | u32 | 0xRRGGBBAA | Ground color at horizon |
| nadir | u32 | 0xRRGGBBAA | Color directly below |
| rotation | f32 | any | Y-axis rotation in radians |
| shift | f32 | -1.0 to 1.0 | Horizon vertical position (0=equator) |

## Mode 1: env_scatter

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| layer | u32 | 0-1 | Target layer |
| variant | u32 | 0-3 | 0=Stars, 1=Vertical (rain), 2=Horizontal, 3=Warp |
| density | u32 | 0-255 | Particle count |
| size | u32 | 0-255 | Particle size |
| glow | u32 | 0-255 | Bloom/glow intensity |
| streak_length | u32 | 0-63 | Elongation (0=points) |
| color_primary | u32 | 0xRRGGBB00 | Main particle color |
| color_secondary | u32 | 0xRRGGBB00 | Variation/twinkle color |
| parallax_rate | u32 | 0-255 | Layer separation amount |
| parallax_size | u32 | 0-255 | Size variation with depth |
| phase | u32 | 0-65535 | Animation phase (wraps) |

### Scatter Variants

| Variant | Value | Effect |
|---------|-------|--------|
| Stars | 0 | Random scattered points |
| Vertical | 1 | Rain-like vertical streaks |
| Horizontal | 2 | Side-scrolling effect |
| Warp | 3 | Speed lines toward center |

## Mode 2: env_lines

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| layer | u32 | 0-1 | Target layer |
| variant | u32 | 0-2 | 0=Floor, 1=Ceiling, 2=Sphere |
| line_type | u32 | 0-2 | 0=Horizontal, 1=Vertical, 2=Grid |
| thickness | u32 | 0-255 | Line thickness in pixels |
| spacing | f32 | >0 | Distance between lines (world units) |
| fade_distance | f32 | >0 | Distance where lines start fading |
| color_primary | u32 | 0xRRGGBBAA | Main line color |
| color_accent | u32 | 0xRRGGBBAA | Accent line color |
| accent_every | u32 | >=1 | Every Nth line uses accent |
| phase | u32 | 0-65535 | Scroll phase (wraps) |

### Lines Variants

| Variant | Value | Effect |
|---------|-------|--------|
| Floor | 0 | Grid on ground plane |
| Ceiling | 1 | Grid on ceiling plane |
| Sphere | 2 | Grid on sphere (sky dome) |

## Mode 3: env_silhouette

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| layer | u32 | 0-1 | Target layer |
| jaggedness | u32 | 0-255 | Terrain roughness (0=smooth, 255=sharp) |
| layer_count | u32 | 1-3 | Number of depth layers |
| color_near | u32 | 0xRRGGBBAA | Nearest silhouette color |
| color_far | u32 | 0xRRGGBBAA | Farthest silhouette color |
| sky_zenith | u32 | 0xRRGGBBAA | Sky color at zenith |
| sky_horizon | u32 | 0xRRGGBBAA | Sky color at horizon |
| parallax_rate | u32 | 0-255 | Layer separation |
| seed | u32 | any | Noise seed for terrain shape |

## Mode 4: env_rectangles

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| layer | u32 | 0-1 | Target layer |
| variant | u32 | 0-3 | 0=Scatter, 1=Buildings, 2=Bands, 3=Panels |
| density | u32 | 0-255 | Rectangle count |
| lit_ratio | u32 | 0-255 | Lit percentage (128=50%) |
| size_min | u32 | 0-63 | Minimum rectangle size |
| size_max | u32 | 0-63 | Maximum rectangle size |
| aspect | u32 | 0-3 | Aspect bias (0=square, 3=very tall) |
| color_primary | u32 | 0xRRGGBBAA | Main window/panel color |
| color_variation | u32 | 0xRRGGBBAA | Color variation |
| parallax_rate | u32 | 0-255 | Layer separation |
| phase | u32 | 0-65535 | Flicker phase (wraps) |

### Rectangles Variants

| Variant | Value | Effect |
|---------|-------|--------|
| Scatter | 0 | Random positions |
| Buildings | 1 | Stacked like windows on buildings |
| Bands | 2 | Horizontal bands |
| Panels | 3 | Control panel arrangement |

## Mode 5: env_room

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| layer | u32 | 0-1 | Target layer |
| color_ceiling | u32 | 0xRRGGBB00 | Ceiling color |
| color_floor | u32 | 0xRRGGBB00 | Floor color |
| color_walls | u32 | 0xRRGGBB00 | Wall color |
| panel_size | f32 | >0 | Wall panel pattern size (world units) |
| panel_gap | u32 | 0-255 | Gap between panels |
| light_dir_x | f32 | any | Light direction X |
| light_dir_y | f32 | any | Light direction Y |
| light_dir_z | f32 | any | Light direction Z |
| light_intensity | u32 | 0-255 | Light strength |
| corner_darken | u32 | 0-255 | Corner/edge darkening |
| room_scale | f32 | >0 | Room size multiplier |
| viewer_x | i32 | -128 to 127 | Viewer X (-1.0 to 1.0 normalized) |
| viewer_y | i32 | -128 to 127 | Viewer Y |
| viewer_z | i32 | -128 to 127 | Viewer Z |

## Mode 6: env_curtains

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| layer | u32 | 0-1 | Target layer |
| layer_count | u32 | 1-3 | Depth layers |
| density | u32 | 0-255 | Structures per cell |
| height_min | u32 | 0-63 | Minimum height |
| height_max | u32 | 0-63 | Maximum height |
| width | u32 | 0-31 | Structure width |
| spacing | u32 | 0-31 | Gap between structures |
| waviness | u32 | 0-255 | Organic wobble (0=straight) |
| color_near | u32 | 0xRRGGBBAA | Nearest color |
| color_far | u32 | 0xRRGGBBAA | Farthest color |
| glow | u32 | 0-255 | Neon/magical glow |
| parallax_rate | u32 | 0-255 | Layer separation |
| phase | u32 | 0-65535 | Scroll phase (wraps) |

## Mode 7: env_rings

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| layer | u32 | 0-1 | Target layer |
| ring_count | u32 | 1-255 | Number of rings |
| thickness | u32 | 0-255 | Ring thickness |
| color_a | u32 | 0xRRGGBBAA | First alternating color |
| color_b | u32 | 0xRRGGBBAA | Second alternating color |
| center_color | u32 | 0xRRGGBBAA | Bright center color |
| center_falloff | u32 | 0-255 | Center glow falloff |
| spiral_twist | f32 | any | Spiral rotation in degrees (0=concentric) |
| axis_x | f32 | -1 to 1 | Ring axis X (normalized) |
| axis_y | f32 | -1 to 1 | Ring axis Y |
| axis_z | f32 | -1 to 1 | Ring axis Z |
| phase | u32 | 0-65535 | Rotation phase (wraps) |

## env_blend

| Mode | Value | Formula | Use Case |
|------|-------|---------|----------|
| Alpha | 0 | `overlay * alpha + base * (1-alpha)` | Transparent overlays |
| Add | 1 | `base + overlay` | Glowing effects, stars |
| Multiply | 2 | `base * overlay` | Shadows, darkening |
| Screen | 3 | `1 - (1-base) * (1-overlay)` | Lighting, fog |

## Color Format Notes

- **0xRRGGBBAA**: Red, Green, Blue, Alpha (8 bits each)
- **0xRRGGBB00**: Alpha ignored (used by `env_scatter` and `env_room`)
- Alpha: 0x00 = transparent, 0xFF = opaque
