# Skeleton Presets

Pre-defined skeleton configurations for common character types.

## Humanoid Skeleton (20 bones)

Standard bipedal humanoid suitable for most characters.

```rust
fn create_humanoid_20() -> Skeleton {
    let mut skel = Skeleton::new();

    // Bone definitions: (name, parent_name, local_offset)
    let bones = [
        // Core
        ("Root", None, [0.0, 0.0, 0.0]),
        ("Hips", Some("Root"), [0.0, 1.0, 0.0]),
        ("Spine", Some("Hips"), [0.0, 0.15, 0.0]),
        ("Chest", Some("Spine"), [0.0, 0.25, 0.0]),
        ("Neck", Some("Chest"), [0.0, 0.2, 0.0]),
        ("Head", Some("Neck"), [0.0, 0.15, 0.0]),

        // Left Arm
        ("L_Shoulder", Some("Chest"), [-0.15, 0.15, 0.0]),
        ("L_UpperArm", Some("L_Shoulder"), [-0.1, 0.0, 0.0]),
        ("L_LowerArm", Some("L_UpperArm"), [-0.25, 0.0, 0.0]),
        ("L_Hand", Some("L_LowerArm"), [-0.18, 0.0, 0.0]),

        // Right Arm
        ("R_Shoulder", Some("Chest"), [0.15, 0.15, 0.0]),
        ("R_UpperArm", Some("R_Shoulder"), [0.1, 0.0, 0.0]),
        ("R_LowerArm", Some("R_UpperArm"), [0.25, 0.0, 0.0]),
        ("R_Hand", Some("R_LowerArm"), [0.18, 0.0, 0.0]),

        // Left Leg
        ("L_UpperLeg", Some("Hips"), [-0.1, -0.05, 0.0]),
        ("L_LowerLeg", Some("L_UpperLeg"), [0.0, -0.4, 0.0]),
        ("L_Foot", Some("L_LowerLeg"), [0.0, -0.35, 0.05]),

        // Right Leg
        ("R_UpperLeg", Some("Hips"), [0.1, -0.05, 0.0]),
        ("R_LowerLeg", Some("R_UpperLeg"), [0.0, -0.4, 0.0]),
        ("R_Foot", Some("R_LowerLeg"), [0.0, -0.35, 0.05]),
    ];

    build_skeleton_from_definitions(&mut skel, &bones);
    skel
}
```

### Bone Index Reference

| Index | Bone | Parent |
|-------|------|--------|
| 0 | Root | - |
| 1 | Hips | Root |
| 2 | Spine | Hips |
| 3 | Chest | Spine |
| 4 | Neck | Chest |
| 5 | Head | Neck |
| 6 | L_Shoulder | Chest |
| 7 | L_UpperArm | L_Shoulder |
| 8 | L_LowerArm | L_UpperArm |
| 9 | L_Hand | L_LowerArm |
| 10 | R_Shoulder | Chest |
| 11 | R_UpperArm | R_Shoulder |
| 12 | R_LowerArm | R_UpperArm |
| 13 | R_Hand | R_LowerArm |
| 14 | L_UpperLeg | Hips |
| 15 | L_LowerLeg | L_UpperLeg |
| 16 | L_Foot | L_LowerLeg |
| 17 | R_UpperLeg | Hips |
| 18 | R_LowerLeg | R_UpperLeg |
| 19 | R_Foot | R_LowerLeg |

## Quadruped Skeleton (18 bones)

Four-legged creature (dog, cat, horse).

```rust
fn create_quadruped_18() -> Skeleton {
    let mut skel = Skeleton::new();

    let bones = [
        // Core
        ("Root", None, [0.0, 0.0, 0.0]),
        ("Pelvis", Some("Root"), [0.0, 0.8, 0.0]),
        ("Spine1", Some("Pelvis"), [0.0, 0.0, 0.3]),
        ("Spine2", Some("Spine1"), [0.0, 0.0, 0.3]),
        ("Chest", Some("Spine2"), [0.0, 0.0, 0.3]),
        ("Neck", Some("Chest"), [0.0, 0.1, 0.15]),
        ("Head", Some("Neck"), [0.0, 0.05, 0.2]),

        // Front Left Leg
        ("FL_UpperLeg", Some("Chest"), [-0.15, -0.1, 0.0]),
        ("FL_LowerLeg", Some("FL_UpperLeg"), [0.0, -0.3, 0.0]),
        ("FL_Paw", Some("FL_LowerLeg"), [0.0, -0.25, 0.0]),

        // Front Right Leg
        ("FR_UpperLeg", Some("Chest"), [0.15, -0.1, 0.0]),
        ("FR_LowerLeg", Some("FR_UpperLeg"), [0.0, -0.3, 0.0]),
        ("FR_Paw", Some("FR_LowerLeg"), [0.0, -0.25, 0.0]),

        // Back Left Leg
        ("BL_UpperLeg", Some("Pelvis"), [-0.12, -0.1, 0.0]),
        ("BL_LowerLeg", Some("BL_UpperLeg"), [0.0, -0.3, 0.0]),
        ("BL_Paw", Some("BL_LowerLeg"), [0.0, -0.25, 0.0]),

        // Back Right Leg
        ("BR_UpperLeg", Some("Pelvis"), [0.12, -0.1, 0.0]),
        ("BR_LowerLeg", Some("BR_UpperLeg"), [0.0, -0.3, 0.0]),
        ("BR_Paw", Some("BR_LowerLeg"), [0.0, -0.25, 0.0]),

        // Tail
        ("Tail1", Some("Pelvis"), [0.0, 0.0, -0.15]),
        ("Tail2", Some("Tail1"), [0.0, -0.05, -0.15]),
    ];

    build_skeleton_from_definitions(&mut skel, &bones);
    skel
}
```

## Bird Skeleton (16 bones)

Flying creature with wings.

```rust
fn create_bird_16() -> Skeleton {
    let mut skel = Skeleton::new();

    let bones = [
        // Core
        ("Root", None, [0.0, 0.0, 0.0]),
        ("Body", Some("Root"), [0.0, 0.5, 0.0]),
        ("Chest", Some("Body"), [0.0, 0.0, 0.15]),
        ("Neck", Some("Chest"), [0.0, 0.05, 0.1]),
        ("Head", Some("Neck"), [0.0, 0.05, 0.1]),

        // Left Wing
        ("L_Wing1", Some("Chest"), [-0.1, 0.0, 0.0]),
        ("L_Wing2", Some("L_Wing1"), [-0.3, 0.0, 0.0]),
        ("L_Wing3", Some("L_Wing2"), [-0.25, 0.0, 0.0]),

        // Right Wing
        ("R_Wing1", Some("Chest"), [0.1, 0.0, 0.0]),
        ("R_Wing2", Some("R_Wing1"), [0.3, 0.0, 0.0]),
        ("R_Wing3", Some("R_Wing2"), [0.25, 0.0, 0.0]),

        // Legs
        ("L_Leg", Some("Body"), [-0.08, -0.15, 0.0]),
        ("L_Foot", Some("L_Leg"), [0.0, -0.15, 0.0]),
        ("R_Leg", Some("Body"), [0.08, -0.15, 0.0]),
        ("R_Foot", Some("R_Leg"), [0.0, -0.15, 0.0]),

        // Tail
        ("Tail", Some("Body"), [0.0, 0.0, -0.2]),
    ];

    build_skeleton_from_definitions(&mut skel, &bones);
    skel
}
```

## Spider Skeleton (18 bones)

Eight-legged creature.

```rust
fn create_spider_18() -> Skeleton {
    let mut skel = Skeleton::new();

    let bones = [
        // Core
        ("Root", None, [0.0, 0.0, 0.0]),
        ("Cephalothorax", Some("Root"), [0.0, 0.3, 0.0]),
        ("Abdomen", Some("Cephalothorax"), [0.0, 0.0, -0.25]),

        // Legs (simplified - 2 bones per leg)
        // Front legs
        ("L_Leg1_Upper", Some("Cephalothorax"), [-0.1, 0.0, 0.1]),
        ("L_Leg1_Lower", Some("L_Leg1_Upper"), [-0.2, -0.15, 0.0]),
        ("R_Leg1_Upper", Some("Cephalothorax"), [0.1, 0.0, 0.1]),
        ("R_Leg1_Lower", Some("R_Leg1_Upper"), [0.2, -0.15, 0.0]),

        // Second pair
        ("L_Leg2_Upper", Some("Cephalothorax"), [-0.12, 0.0, 0.0]),
        ("L_Leg2_Lower", Some("L_Leg2_Upper"), [-0.22, -0.15, 0.0]),
        ("R_Leg2_Upper", Some("Cephalothorax"), [0.12, 0.0, 0.0]),
        ("R_Leg2_Lower", Some("R_Leg2_Upper"), [0.22, -0.15, 0.0]),

        // Third pair
        ("L_Leg3_Upper", Some("Cephalothorax"), [-0.12, 0.0, -0.1]),
        ("L_Leg3_Lower", Some("L_Leg3_Upper"), [-0.22, -0.15, 0.0]),
        ("R_Leg3_Upper", Some("Cephalothorax"), [0.12, 0.0, -0.1]),
        ("R_Leg3_Lower", Some("R_Leg3_Upper"), [0.22, -0.15, 0.0]),

        // Back legs
        ("L_Leg4_Upper", Some("Cephalothorax"), [-0.1, 0.0, -0.15]),
        ("L_Leg4_Lower", Some("L_Leg4_Upper"), [-0.2, -0.15, -0.1]),
        ("R_Leg4_Upper", Some("Cephalothorax"), [0.1, 0.0, -0.15]),
        ("R_Leg4_Lower", Some("R_Leg4_Upper"), [0.2, -0.15, -0.1]),
    ];

    build_skeleton_from_definitions(&mut skel, &bones);
    skel
}
```

## Fish/Serpent Skeleton (10 bones)

Spine-based creature for swimming/slithering.

```rust
fn create_serpent_10() -> Skeleton {
    let mut skel = Skeleton::new();

    let bones = [
        ("Root", None, [0.0, 0.0, 0.0]),
        ("Head", Some("Root"), [0.0, 0.0, 0.3]),
        ("Segment1", Some("Root"), [0.0, 0.0, -0.2]),
        ("Segment2", Some("Segment1"), [0.0, 0.0, -0.2]),
        ("Segment3", Some("Segment2"), [0.0, 0.0, -0.2]),
        ("Segment4", Some("Segment3"), [0.0, 0.0, -0.2]),
        ("Segment5", Some("Segment4"), [0.0, 0.0, -0.2]),
        ("Segment6", Some("Segment5"), [0.0, 0.0, -0.2]),
        ("Segment7", Some("Segment6"), [0.0, 0.0, -0.2]),
        ("TailTip", Some("Segment7"), [0.0, 0.0, -0.15]),
    ];

    build_skeleton_from_definitions(&mut skel, &bones);
    skel
}
```

## Mech/Robot Skeleton (12 bones)

Mechanical bipedal with rigid joints.

```rust
fn create_mech_12() -> Skeleton {
    let mut skel = Skeleton::new();

    let bones = [
        // Core (no spine - rigid body)
        ("Root", None, [0.0, 0.0, 0.0]),
        ("Torso", Some("Root"), [0.0, 1.2, 0.0]),
        ("Head", Some("Torso"), [0.0, 0.4, 0.0]),

        // Arms (simplified)
        ("L_Arm", Some("Torso"), [-0.4, 0.2, 0.0]),
        ("L_Forearm", Some("L_Arm"), [-0.35, 0.0, 0.0]),
        ("L_Hand", Some("L_Forearm"), [-0.25, 0.0, 0.0]),

        ("R_Arm", Some("Torso"), [0.4, 0.2, 0.0]),
        ("R_Forearm", Some("R_Arm"), [0.35, 0.0, 0.0]),
        ("R_Hand", Some("R_Forearm"), [0.25, 0.0, 0.0]),

        // Legs
        ("L_Thigh", Some("Root"), [-0.2, -0.1, 0.0]),
        ("L_Shin", Some("L_Thigh"), [0.0, -0.5, 0.0]),
        ("L_Foot", Some("L_Shin"), [0.0, -0.45, 0.1]),

        ("R_Thigh", Some("Root"), [0.2, -0.1, 0.0]),
        ("R_Shin", Some("R_Thigh"), [0.0, -0.5, 0.0]),
        ("R_Foot", Some("R_Shin"), [0.0, -0.45, 0.1]),
    ];

    build_skeleton_from_definitions(&mut skel, &bones);
    skel
}
```

## Helper Function

```rust
fn build_skeleton_from_definitions(
    skel: &mut Skeleton,
    bones: &[(&str, Option<&str>, [f32; 3])],
) {
    let mut name_to_idx: std::collections::HashMap<&str, usize> = std::collections::HashMap::new();

    for (name, parent_name, offset) in bones {
        let parent_idx = parent_name.and_then(|p| name_to_idx.get(p).copied());
        let idx = skel.add_bone(name, parent_idx, Vec3::from(*offset));
        name_to_idx.insert(name, idx);
    }
}
```

## Scaling Skeletons

Adjust skeleton size for different character scales:

```rust
impl Skeleton {
    fn scale(&mut self, factor: f32) {
        for bone in &mut self.bones {
            bone.local_position *= factor;
        }
    }

    fn scale_to_height(&mut self, target_height: f32) {
        let current_height = self.calculate_height();
        if current_height > 0.0 {
            self.scale(target_height / current_height);
        }
    }

    fn calculate_height(&self) -> f32 {
        let bind = self.calculate_bind_pose();
        bind.iter()
            .map(|m| m.w_axis.y)  // Y position
            .fold(f32::NEG_INFINITY, f32::max) -
        bind.iter()
            .map(|m| m.w_axis.y)
            .fold(f32::INFINITY, f32::min)
    }
}
```

## Usage

```rust
// Create and scale a skeleton
let mut skel = create_humanoid_20();
skel.scale_to_height(2.0);  // 2 meter tall character

// Calculate inverse bind matrices
let ibm = skel.calculate_inverse_bind_matrices();

// Use with skinned mesh...
```
