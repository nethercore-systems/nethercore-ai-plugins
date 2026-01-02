# Spatial Audio Patterns

Implementation patterns for 3D sound positioning.

## Distance Attenuation

### Attenuation Curves

```rust
fn calculate_volume(distance: f32, config: &AttenuationConfig) -> f32 {
    if distance <= config.min_distance {
        return 1.0;  // Full volume
    }
    if distance >= config.max_distance {
        return 0.0;  // Silent
    }

    let t = (distance - config.min_distance) /
            (config.max_distance - config.min_distance);

    match config.curve {
        Curve::Linear => 1.0 - t,
        Curve::Logarithmic => 1.0 - t.log10().max(0.0),
        Curve::Inverse => config.min_distance / distance,
        Curve::InverseSquare => (config.min_distance / distance).powi(2),
    }
}
```

### Presets

| Type | Min | Max | Curve | Use For |
|------|-----|-----|-------|---------|
| Dialogue | 1m | 15m | Linear | NPC speech |
| Footsteps | 0.5m | 20m | Inverse | Player/enemy steps |
| Gunshots | 5m | 200m | Log | Distant weapons |
| Explosions | 10m | 500m | Log | Big impacts |
| UI | N/A | N/A | None | Interface sounds |
| Ambient point | 2m | 50m | Linear | Environmental |
| Whisper | 0.5m | 5m | Linear | Quiet sounds |

---

## Stereo Panning

### Basic Panning

```rust
fn calculate_pan(
    listener_pos: Vec3,
    listener_forward: Vec3,
    sound_pos: Vec3
) -> f32 {
    let to_sound = (sound_pos - listener_pos).normalize();
    let listener_right = listener_forward.cross(Vec3::UP).normalize();

    // -1 = full left, 0 = center, 1 = full right
    to_sound.dot(listener_right)
}
```

### Distance-Based Pan Narrowing

Far sounds should be more centered:

```rust
fn calculate_pan_with_distance(
    listener_pos: Vec3,
    listener_forward: Vec3,
    sound_pos: Vec3,
    attenuation_config: &AttenuationConfig
) -> f32 {
    let raw_pan = calculate_pan(listener_pos, listener_forward, sound_pos);
    let distance = (sound_pos - listener_pos).length();

    // Calculate distance factor (0 = close, 1 = far)
    let distance_factor = ((distance - attenuation_config.min_distance) /
                          (attenuation_config.max_distance - attenuation_config.min_distance))
                          .clamp(0.0, 1.0);

    // Narrow pan as distance increases
    raw_pan * (1.0 - distance_factor * 0.7)
}
```

---

## Occlusion

### Basic Occlusion

```rust
fn apply_occlusion(sound: &mut Sound, occlusion: f32) {
    // occlusion: 0.0 = clear line of sight, 1.0 = fully blocked

    // Volume reduction
    sound.volume *= 1.0 - (occlusion * 0.5);

    // Low-pass filter (blocked = muffled)
    let cutoff = lerp(20000.0, 500.0, occlusion);
    sound.lowpass_cutoff = cutoff;
}
```

### Raycast-Based Occlusion

```rust
fn calculate_occlusion(
    listener_pos: Vec3,
    sound_pos: Vec3,
    physics: &PhysicsWorld
) -> f32 {
    let direction = sound_pos - listener_pos;
    let distance = direction.length();

    // Cast ray from listener to sound
    if let Some(hit) = physics.raycast(listener_pos, direction.normalize(), distance) {
        // Hit something - calculate occlusion based on material
        match hit.material {
            Material::Solid => 1.0,
            Material::Glass => 0.3,
            Material::Thin => 0.5,
            Material::None => 0.0,
        }
    } else {
        0.0  // Clear path
    }
}
```

### Multi-Ray Occlusion (More Accurate)

```rust
fn calculate_occlusion_multiray(
    listener_pos: Vec3,
    sound_pos: Vec3,
    physics: &PhysicsWorld,
    ray_count: usize
) -> f32 {
    let mut total_occlusion = 0.0;

    // Cast multiple rays in a cone
    for i in 0..ray_count {
        let offset = random_in_sphere() * 0.5;  // Small offset
        let target = sound_pos + offset;

        if physics.raycast(listener_pos, target, ...).is_some() {
            total_occlusion += 1.0;
        }
    }

    total_occlusion / ray_count as f32
}
```

---

## Reverb Zones

### Zone Structure

```rust
struct ReverbZone {
    bounds: BoundingBox,
    reverb_preset: ReverbPreset,
    priority: u32,
    blend_distance: f32,
}

enum ReverbPreset {
    Room { decay: 0.5, early: 0.6, wet: 0.3 },
    Hall { decay: 2.5, early: 0.4, wet: 0.4 },
    Cathedral { decay: 6.0, early: 0.2, wet: 0.5 },
    Outdoor { decay: 0.2, early: 0.1, wet: 0.1 },
    Cave { decay: 4.0, early: 0.8, wet: 0.6 },
}
```

### Zone Blending

```rust
fn get_reverb_for_position(pos: Vec3, zones: &[ReverbZone]) -> ReverbSettings {
    let mut active_zones: Vec<(&ReverbZone, f32)> = vec![];

    for zone in zones {
        if zone.bounds.contains(pos) {
            // Calculate blend weight based on distance to edge
            let dist_to_edge = zone.bounds.distance_to_edge(pos);
            let weight = (dist_to_edge / zone.blend_distance).min(1.0);
            active_zones.push((zone, weight));
        }
    }

    // Blend all active zones
    blend_reverb_settings(&active_zones)
}
```

---

## Doppler Effect

For moving sound sources:

```rust
fn calculate_doppler_pitch(
    listener_pos: Vec3,
    listener_vel: Vec3,
    sound_pos: Vec3,
    sound_vel: Vec3,
    speed_of_sound: f32  // 343 m/s
) -> f32 {
    let direction = (sound_pos - listener_pos).normalize();

    // Relative velocity along the direction
    let listener_approach = listener_vel.dot(direction);
    let source_approach = sound_vel.dot(-direction);

    // Doppler formula
    let pitch = (speed_of_sound + listener_approach) /
                (speed_of_sound + source_approach);

    pitch.clamp(0.5, 2.0)  // Limit extreme values
}
```

---

## HRTF (Head-Related Transfer Function)

For headphone spatialization:

```rust
struct HRTFProcessor {
    left_impulse: Vec<f32>,
    right_impulse: Vec<f32>,
}

fn apply_hrtf(
    input: &[f32],
    azimuth: f32,    // -180 to 180 degrees
    elevation: f32,  // -90 to 90 degrees
    hrtf_database: &HRTFDatabase
) -> (Vec<f32>, Vec<f32>) {
    let (left_ir, right_ir) = hrtf_database.get_impulse_response(azimuth, elevation);

    let left_output = convolve(input, &left_ir);
    let right_output = convolve(input, &right_ir);

    (left_output, right_output)
}
```
