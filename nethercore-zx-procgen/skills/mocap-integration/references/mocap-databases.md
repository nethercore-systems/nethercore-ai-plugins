# Motion Capture Databases Reference

Comprehensive list of open-source motion capture databases with recommended clips for game development.

## CMU Motion Capture Database

**URL:** https://mocap.cs.cmu.edu/

**Overview:**
- 2,605 motion clips
- 144 subjects
- Multiple formats available (BVH, C3D, AMC/ASF)
- License: Free for research; commercial requires attribution

### Subject Categories

| Subject Range | Category | Best For |
|---------------|----------|----------|
| 01-02 | Walking/Running | Locomotion |
| 05-06 | Jumping | Platformers |
| 07-08 | Walking variations | Character variety |
| 09-12 | Running variations | Athletic games |
| 13-14 | Martial arts/Boxing | Fighting games |
| 15-16 | Exercise | Sports/Fitness |
| 17-19 | Basketball | Sports games |
| 35-36 | General actions | Various |
| 49-50 | Sports | Athletic games |
| 55-56 | Playground | Children animations |
| 85-90 | Dancing | Rhythm games |
| 127-128 | Acrobatics | Action games |
| 141-144 | Everyday actions | Simulation |

### Recommended Clips by Use Case

#### Locomotion

| Subject_Motion | Description | FPS | Duration |
|----------------|-------------|-----|----------|
| 01_01 | Walk cycle | 120 | 5.3s |
| 02_01 | Slow jog | 120 | 4.1s |
| 02_02 | Normal run | 120 | 3.8s |
| 02_03 | Fast run | 120 | 2.9s |
| 07_01 | Walk left turn | 120 | 4.2s |
| 07_02 | Walk right turn | 120 | 4.1s |
| 08_01 | Walk backwards | 120 | 5.0s |
| 09_01 | Run left turn | 120 | 3.2s |

#### Combat

| Subject_Motion | Description | Duration |
|----------------|-------------|----------|
| 13_01 | Martial arts combo | 6.2s |
| 13_05 | Kick sequence | 4.8s |
| 13_17 | Spinning kick | 2.1s |
| 14_01 | Boxing jab | 1.8s |
| 14_06 | Boxing hook | 2.0s |
| 14_14 | Uppercut | 1.9s |
| 14_20 | Dodge/duck | 1.5s |

#### Jumping

| Subject_Motion | Description | Duration |
|----------------|-------------|----------|
| 05_01 | Standing jump | 1.8s |
| 05_02 | Running jump | 2.1s |
| 05_06 | Jump forward | 2.3s |
| 05_10 | Hop on one foot | 1.5s |
| 06_01 | Standing long jump | 2.0s |

#### General Actions

| Subject_Motion | Description | Duration |
|----------------|-------------|----------|
| 35_01 | Pick up object | 2.5s |
| 35_02 | Wave hello | 1.8s |
| 35_08 | Sit down | 3.0s |
| 35_17 | Push object | 2.2s |
| 35_22 | Look around | 3.5s |
| 144_01 | Open door | 2.8s |
| 144_03 | Close door | 2.5s |

#### Dance/Rhythm

| Subject_Motion | Description | Style |
|----------------|-------------|-------|
| 85_01 | Dancing sequence | Modern |
| 85_10 | Hip hop moves | Hip hop |
| 86_01 | Jazz dance | Jazz |
| 86_14 | Breakdance | Street |
| 88_01 | Club dancing | Modern |

### Download Scripts

```bash
# Download single BVH from CMU
wget "http://mocap.cs.cmu.edu/subjects/01/01_01.bvh"

# Batch download locomotion clips
for i in 01_01 02_01 02_02 05_01; do
    wget "http://mocap.cs.cmu.edu/subjects/${i%_*}/${i}.bvh"
done
```

### CMU Skeleton Notes

- Root at Hips (waist level)
- Y-up, -Z forward
- Units: Centimeters (divide by 100 for meters)
- 31 joints typical
- Some subjects use different bone naming

## Mixamo

**URL:** https://www.mixamo.com/

**Overview:**
- Thousands of animations
- Game-ready quality
- Auto-rigging for custom characters
- Free with Adobe account

### Key Advantages

1. **Game-optimized:** Clean loops, consistent timing
2. **Auto-retargeting:** Applies to any humanoid mesh
3. **Categories:** Organized by action type
4. **Search:** Find by name or keywords

### Export Workflow

1. Select animation on Mixamo
2. Download as FBX
3. Import to Blender:
   ```python
   import bpy
   bpy.ops.import_scene.fbx(filepath='mixamo_anim.fbx')
   ```
4. Export as BVH:
   ```python
   bpy.ops.export_anim.bvh(filepath='animation.bvh')
   ```

### Recommended Mixamo Animations

| Animation | Use Case | Loop? |
|-----------|----------|-------|
| Walking | Basic locomotion | Yes |
| Running | Sprint | Yes |
| Jump | Platformer | No |
| Idle | Standing | Yes |
| Sword Slash | Melee combat | No |
| Punch | Unarmed combat | No |
| Die | Death sequence | No |
| Victory | Win state | No |
| Crouch Idle | Stealth | Yes |
| Roll | Evasion | No |

### Mixamo vs CMU

| Aspect | Mixamo | CMU |
|--------|--------|-----|
| Quality | Game-ready | Raw capture |
| Variety | Stylized actions | Natural motion |
| Loops | Pre-looped | Manual loop |
| Format | FBX (convert) | Native BVH |
| License | Adobe ToS | Attribution |
| Custom chars | Yes | No |

## Truebones

**URL:** https://truebones.gumroad.com/

**Overview:**
- Various free and paid packs
- Native BVH format
- Game-focused animations
- No account required for free packs

### Free Packs

| Pack | Contents | Size |
|------|----------|------|
| Free Motion Capture | 20+ basic actions | 50MB |
| Zombie Pack | Walk, attack, idle | 30MB |
| Dance Pack Sample | 10 dance moves | 25MB |

### Using Truebones

```rust
// Truebones uses standard BVH format
let clip = BvhClip::parse(&fs::read_to_string("truebones_walk.bvh")?)?;
// May need skeleton remapping for custom characters
```

## Bandai Namco Research Motion Dataset

**URL:** https://github.com/BandaiNamcoResearchInc/Bandai-Namco-Research-Motiondataset

**Overview:**
- High-quality game animations
- BVH format
- CC BY-NC 4.0 license

### Notable Content

- Stylized combat animations
- Expressive character actions
- Game-quality timing

## Lafan1 Dataset

**URL:** https://github.com/ubisoft/ubisoft-laforge-animation-dataset

**Overview:**
- Ubisoft motion capture
- High quality for ML research
- BVH format
- Academic license

## Integration Example

```rust
/// Load animation from database with fallback
pub fn load_database_animation(name: &str) -> Result<BvhClip, String> {
    // Try local cache first
    let cache_path = format!("assets/mocap/{}.bvh", name);
    if let Ok(content) = fs::read_to_string(&cache_path) {
        return BvhClip::parse(&content);
    }

    // Map semantic name to CMU clip
    let cmu_id = match name {
        "walk" => "01_01",
        "run" => "02_01",
        "jump" => "05_01",
        _ => return Err(format!("Unknown animation: {}", name)),
    };

    // Would download from CMU in production
    Err(format!("Animation not cached: {}", cmu_id))
}
```

## License Summary

| Database | Commercial Use | Requirements |
|----------|----------------|--------------|
| CMU | Yes | Attribution |
| Mixamo | Yes | Adobe ToS |
| Truebones Free | Check pack | Varies |
| Bandai Namco | No | Non-commercial |
| Lafan1 | No | Academic |

## Preprocessing Tips

### Loop Extraction

```rust
/// Find loop point where start ≈ end
pub fn find_loop_frame(clip: &BvhClip, threshold: f32) -> Option<usize> {
    let start = clip.sample_joint(0, 0);

    for frame in (clip.frame_count / 2)..clip.frame_count {
        let end = clip.sample_joint(0, frame);
        let diff = position_distance(&start.position, &end.position);
        if diff < threshold {
            return Some(frame);
        }
    }
    None
}
```

### Root Motion Removal

```rust
/// Make animation play in place
pub fn remove_root_motion(clip: &mut BvhClip) {
    let root_idx = 0;
    let x_offset = clip.joints[root_idx].channel_offset;
    let z_offset = x_offset + 2;  // Assuming XYZ order

    let x_start = clip.motion_data[x_offset];
    let z_start = clip.motion_data[z_offset];

    for frame in 0..clip.frame_count {
        let base = frame * clip.total_channels;
        clip.motion_data[base + x_offset] = x_start;
        clip.motion_data[base + z_offset] = z_start;
    }
}
```
