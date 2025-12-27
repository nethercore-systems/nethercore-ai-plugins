# Character Presets

Pre-built character configurations for common ZX game archetypes.

## Humanoid Presets

### Player Hero (Standard)

```rust
let config = HumanoidConfig {
    height: 1.8,
    proportions: Proportions::Stylized {
        head_scale: 1.2,     // Slightly larger head
        torso_scale: 1.0,
        limb_scale: 0.95,
    },
    poly_budget: 600,
    skeleton_detail: SkeletonDetail::Standard,  // 22 bones
    texture_size: TextureSize::Hero,            // 256x256
    animations: vec![
        AnimPreset::Walk,
        AnimPreset::Run,
        AnimPreset::Idle,
        AnimPreset::Jump,
        AnimPreset::Attack,
        AnimPreset::Hit,
        AnimPreset::Death,
    ],
};
```

**Stats:**
- Triangles: 500-600
- Bones: 22
- Texture: 256x256 albedo, 128x128 MRE
- Animations: 7 clips

### NPC Villager (Economy)

```rust
let config = HumanoidConfig {
    height: 1.7,
    proportions: Proportions::Stylized {
        head_scale: 1.3,
        torso_scale: 1.1,
        limb_scale: 0.9,
    },
    poly_budget: 350,
    skeleton_detail: SkeletonDetail::Minimal,  // 16 bones
    texture_size: TextureSize::Standard,       // 128x128
    animations: vec![
        AnimPreset::Walk,
        AnimPreset::Idle,
        AnimPreset::Talk,
    ],
};
```

**Stats:**
- Triangles: 300-350
- Bones: 16
- Texture: 128x128 albedo, 64x64 MRE
- Animations: 3 clips

### Swarm Enemy (Minimal)

```rust
let config = HumanoidConfig {
    height: 1.5,
    proportions: Proportions::Simplified,
    poly_budget: 150,
    skeleton_detail: SkeletonDetail::Ultra,  // 10 bones
    texture_size: TextureSize::Minimal,      // 64x64
    animations: vec![
        AnimPreset::Walk,
        AnimPreset::Attack,
        AnimPreset::Death,
    ],
};
```

**Stats:**
- Triangles: 100-150
- Bones: 10
- Texture: 64x64 albedo only
- Animations: 3 clips

## Quadruped Presets

### Wolf/Dog (Standard)

```rust
let config = QuadrupedConfig {
    body_length: 1.2,
    body_height: 0.6,
    proportions: QuadProportions::Canine,
    poly_budget: 400,
    skeleton: QuadSkeleton::Standard,  // 18 bones
    tail_bones: 3,
    animations: vec![
        AnimPreset::QuadWalk,
        AnimPreset::QuadRun,
        AnimPreset::QuadIdle,
        AnimPreset::QuadAttack,
    ],
};
```

**Stats:**
- Triangles: 350-400
- Bones: 18
- Texture: 128x128
- Animations: 4 clips

### Horse/Mount (Large)

```rust
let config = QuadrupedConfig {
    body_length: 2.0,
    body_height: 1.5,
    proportions: QuadProportions::Equine,
    poly_budget: 600,
    skeleton: QuadSkeleton::Detailed,  // 24 bones
    tail_bones: 4,
    animations: vec![
        AnimPreset::QuadWalk,
        AnimPreset::QuadTrot,
        AnimPreset::QuadGallop,
        AnimPreset::QuadIdle,
        AnimPreset::QuadRear,
    ],
};
```

**Stats:**
- Triangles: 550-600
- Bones: 24
- Texture: 256x256
- Animations: 5 clips

### Small Creature (Economy)

```rust
let config = QuadrupedConfig {
    body_length: 0.4,
    body_height: 0.2,
    proportions: QuadProportions::Rodent,
    poly_budget: 150,
    skeleton: QuadSkeleton::Minimal,  // 12 bones
    tail_bones: 2,
    animations: vec![
        AnimPreset::QuadWalk,
        AnimPreset::QuadIdle,
    ],
};
```

**Stats:**
- Triangles: 100-150
- Bones: 12
- Texture: 64x64
- Animations: 2 clips

## Creature Presets

### Spider

```rust
let config = CreatureConfig {
    body_type: BodyType::Arthropod,
    body_size: Vec3::new(0.8, 0.3, 0.6),
    leg_count: 8,
    leg_segments: 3,
    poly_budget: 400,
    animations: vec![
        AnimPreset::SpiderWalk,
        AnimPreset::SpiderIdle,
        AnimPreset::SpiderAttack,
    ],
};
```

**Stats:**
- Triangles: 350-400
- Bones: 26 (body + 8×3 legs)
- Texture: 128x128
- Animations: 3 clips

### Bird

```rust
let config = CreatureConfig {
    body_type: BodyType::Avian,
    body_size: Vec3::new(0.3, 0.2, 0.4),
    wing_span: 0.8,
    poly_budget: 300,
    animations: vec![
        AnimPreset::BirdFly,
        AnimPreset::BirdGlide,
        AnimPreset::BirdLand,
        AnimPreset::BirdIdle,
    ],
};
```

**Stats:**
- Triangles: 250-300
- Bones: 16 (body + wings + legs)
- Texture: 128x128
- Animations: 4 clips

### Serpent/Snake

```rust
let config = CreatureConfig {
    body_type: BodyType::Serpent,
    body_length: 2.0,
    body_radius: 0.1,
    spine_segments: 8,
    poly_budget: 250,
    animations: vec![
        AnimPreset::SerpentSlither,
        AnimPreset::SerpentCoil,
        AnimPreset::SerpentStrike,
    ],
};
```

**Stats:**
- Triangles: 200-250
- Bones: 10 (spine chain)
- Texture: 128x64 (long format)
- Animations: 3 clips

## Mechanical Presets

### Humanoid Robot

```rust
let config = MechConfig {
    mech_type: MechType::Humanoid,
    height: 2.0,
    proportions: MechProportions::Heavy,
    poly_budget: 500,
    joint_type: JointType::Mechanical,  // No skinning
    animations: vec![
        AnimPreset::MechWalk,
        AnimPreset::MechIdle,
        AnimPreset::MechAttack,
    ],
};
```

**Stats:**
- Triangles: 450-500
- Bones: 18 (rigid body)
- Texture: 256x256
- Animations: 3 clips

### Vehicle

```rust
let config = MechConfig {
    mech_type: MechType::Vehicle,
    dimensions: Vec3::new(2.0, 1.0, 4.0),
    wheel_count: 4,
    poly_budget: 400,
    animations: vec![
        AnimPreset::WheelRoll,
        AnimPreset::Suspension,
    ],
};
```

**Stats:**
- Triangles: 350-400
- Bones: 6 (body + 4 wheels + steering)
- Texture: 256x256
- Animations: 2 procedural

## Usage

### Applying a Preset

```rust
fn create_from_preset(preset: CharacterPreset) -> CharacterAsset {
    match preset {
        CharacterPreset::PlayerHero => {
            let config = HumanoidConfig::player_hero();
            create_humanoid_character(config)
        }
        CharacterPreset::SwarmEnemy => {
            let config = HumanoidConfig::swarm_enemy();
            create_humanoid_character(config)
        }
        CharacterPreset::Wolf => {
            let config = QuadrupedConfig::wolf();
            create_quadruped_character(config)
        }
        // ...
    }
}
```

### Customizing Presets

```rust
// Start with preset, then modify
let mut config = HumanoidConfig::player_hero();
config.poly_budget = 800;  // Increase for main character
config.texture_size = TextureSize::Ultra;  // 512x512
config.animations.push(AnimPreset::Victory);  // Add animation

let character = create_humanoid_character(config);
```

## Budget Guidelines

### Memory Budget by Character Type

| Type | ROM Size | VRAM | Best For |
|------|----------|------|----------|
| Swarm | ~20KB | 8KB | Many on screen |
| Standard | ~50KB | 32KB | NPCs, enemies |
| Hero | ~100KB | 64KB | Player, bosses |

### Performance Considerations

| Bones | Skinning Cost | Recommendation |
|-------|---------------|----------------|
| 10 | Very Low | Swarm enemies |
| 20 | Low | Most characters |
| 35 | Medium | Detailed heroes |
| 50+ | High | Use sparingly |
