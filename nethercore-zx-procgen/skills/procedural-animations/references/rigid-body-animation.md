# Rigid Body Animation

Animation techniques for non-deforming objects: vehicles, robots, mechanical assemblies, and props.

## Overview

Rigid body animation uses hierarchical transforms rather than skinning. Each part maintains its shape but moves relative to parent parts.

### When to Use Rigid Body vs Skinning

| Scenario | Approach |
|----------|----------|
| Characters with smooth skin | Skinning |
| Vehicles, machinery | Rigid body |
| Robots with distinct segments | Rigid body |
| Hinged/jointed objects | Rigid body |
| Cloth, tentacles | Skinning or physics |
| Low-poly characters | Either (rigid simpler) |

## Hierarchical Transform System

### Part Hierarchy

```rust
struct RigidPart {
    local_transform: Mat4,
    parent: Option<usize>,
    mesh: u32,
}

struct RigidAssembly {
    parts: Vec<RigidPart>,
}

impl RigidAssembly {
    fn render(&self, world_transform: Mat4) {
        let mut world_matrices = vec![Mat4::IDENTITY; self.parts.len()];

        for (i, part) in self.parts.iter().enumerate() {
            let parent_world = match part.parent {
                Some(p) => world_matrices[p],
                None => world_transform,
            };
            world_matrices[i] = parent_world * part.local_transform;

            // Render this part
            unsafe {
                transform_set(world_matrices[i].to_cols_array().as_ptr());
                draw_mesh(part.mesh);
            }
        }
    }
}
```

### Animated Hierarchy

```rust
struct AnimatedPart {
    base_transform: Mat4,
    animation_offset: Mat4,
}

impl AnimatedPart {
    fn update(&mut self, time: f32, animation: &PartAnimation) {
        self.animation_offset = animation.sample(time);
    }

    fn world_transform(&self, parent_world: Mat4) -> Mat4 {
        parent_world * self.base_transform * self.animation_offset
    }
}
```

## Vehicle Animation

### Car with Suspension

```rust
struct CarState {
    // Wheels
    wheel_rotations: [f32; 4],  // Rotation from travel
    wheel_steerings: [f32; 2],  // Front wheel steering
    suspensions: [SuspensionState; 4],

    // Body
    body_pitch: f32,
    body_roll: f32,
}

struct SuspensionState {
    compression: f32,
    velocity: f32,
}

impl CarState {
    fn update(&mut self, input: &CarInput, terrain: &Terrain, dt: f32) {
        // Update wheel rotation based on speed
        let wheel_speed = input.throttle * 360.0;  // degrees/second
        for i in 0..4 {
            self.wheel_rotations[i] += wheel_speed * dt;
        }

        // Update steering
        let steer_angle = input.steering * 35.0;  // Max 35 degrees
        self.wheel_steerings[0] = steer_angle;
        self.wheel_steerings[1] = steer_angle * 0.9;  // Ackermann-ish

        // Update suspension per wheel
        let wheel_positions = self.get_wheel_world_positions();
        for (i, pos) in wheel_positions.iter().enumerate() {
            let ground = terrain.height_at(pos.x, pos.z);
            self.update_suspension(i, ground, dt);
        }

        // Calculate body pose from suspension
        self.calculate_body_pose();
    }

    fn update_suspension(&mut self, wheel: usize, ground_height: f32, dt: f32) {
        let spring_k = 5000.0;
        let damping = 500.0;
        let rest_length = 0.3;

        let current_length = self.body_height() - ground_height;
        let compression = (rest_length - current_length).max(0.0);

        let spring_force = compression * spring_k;
        let damp_force = -self.suspensions[wheel].velocity * damping;

        let accel = (spring_force + damp_force) / 50.0;  // Wheel mass
        self.suspensions[wheel].velocity += accel * dt;
        self.suspensions[wheel].compression += self.suspensions[wheel].velocity * dt;
        self.suspensions[wheel].compression = self.suspensions[wheel].compression.clamp(0.0, 0.25);
    }

    fn calculate_body_pose(&mut self) {
        // Pitch from front/back suspension difference
        let front_avg = (self.suspensions[0].compression + self.suspensions[1].compression) / 2.0;
        let back_avg = (self.suspensions[2].compression + self.suspensions[3].compression) / 2.0;
        self.body_pitch = (back_avg - front_avg) * 20.0;  // Scale to degrees

        // Roll from left/right difference
        let left_avg = (self.suspensions[0].compression + self.suspensions[2].compression) / 2.0;
        let right_avg = (self.suspensions[1].compression + self.suspensions[3].compression) / 2.0;
        self.body_roll = (right_avg - left_avg) * 15.0;
    }

    fn render(&self, meshes: &CarMeshes) {
        // Body with pitch/roll
        unsafe {
            push_identity();
            push_rotate_x(self.body_pitch);
            push_rotate_z(self.body_roll);
            draw_mesh(meshes.body);
        }

        // Wheels
        for (i, &pos) in self.wheel_mount_positions().iter().enumerate() {
            unsafe {
                push_identity();

                // Position at mount point
                push_translate(pos.x, pos.y - self.suspensions[i].compression, pos.z);

                // Steering (front wheels only)
                if i < 2 {
                    push_rotate_y(self.wheel_steerings[i]);
                }

                // Wheel spin
                push_rotate_x(self.wheel_rotations[i]);

                draw_mesh(meshes.wheel);
            }
        }
    }
}
```

### Tank Tracks

Procedural track link animation:

```rust
struct TankTrack {
    links: Vec<TrackLinkState>,
    track_path: Vec<Vec3>,  // Path around wheels
    total_length: f32,
}

struct TrackLinkState {
    path_position: f32,  // 0.0 to 1.0 along path
}

impl TankTrack {
    fn update(&mut self, linear_speed: f32, dt: f32) {
        let path_speed = linear_speed / self.total_length;

        for link in &mut self.links {
            link.path_position = (link.path_position + path_speed * dt) % 1.0;
        }
    }

    fn render(&self, link_mesh: u32) {
        for link in &self.links {
            let (pos, tangent) = self.sample_path(link.path_position);
            // Rotate link mesh's forward (-Z) to face tangent direction
            let rotation = Quat::from_rotation_arc(Vec3::NEG_Z, tangent);

            unsafe {
                push_identity();
                transform_set(
                    Mat4::from_rotation_translation(rotation, pos)
                        .to_cols_array()
                        .as_ptr()
                );
                draw_mesh(link_mesh);
            }
        }
    }

    fn sample_path(&self, t: f32) -> (Vec3, Vec3) {
        let idx = (t * (self.track_path.len() - 1) as f32) as usize;
        let next_idx = (idx + 1) % self.track_path.len();
        let local_t = (t * (self.track_path.len() - 1) as f32).fract();

        let pos = self.track_path[idx].lerp(self.track_path[next_idx], local_t);
        let tangent = (self.track_path[next_idx] - self.track_path[idx]).normalize();

        (pos, tangent)
    }
}
```

## Robot Animation

### Articulated Robot Arm

6-DOF industrial robot arm:

```rust
struct RobotArm {
    // Joint angles (degrees)
    base_yaw: f32,        // J1: Base rotation
    shoulder_pitch: f32,  // J2: Shoulder
    elbow_pitch: f32,     // J3: Elbow
    wrist_yaw: f32,       // J4: Wrist rotation
    wrist_pitch: f32,     // J5: Wrist bend
    tool_roll: f32,       // J6: Tool rotation

    // Segment lengths
    upper_arm: f32,
    forearm: f32,
    wrist_length: f32,
}

impl RobotArm {
    fn render(&self, meshes: &RobotArmMeshes) {
        unsafe {
            // Base (J1)
            push_identity();
            push_rotate_y(self.base_yaw);
            draw_mesh(meshes.base);

            // Shoulder (J2)
            push_translate(0.0, 0.5, 0.0);
            push_rotate_x(self.shoulder_pitch);
            draw_mesh(meshes.shoulder);

            // Upper arm + Elbow (J3)
            push_translate(0.0, self.upper_arm, 0.0);
            push_rotate_x(self.elbow_pitch);
            draw_mesh(meshes.elbow);

            // Forearm
            push_translate(0.0, self.forearm, 0.0);
            draw_mesh(meshes.forearm);

            // Wrist (J4)
            push_rotate_z(self.wrist_yaw);
            draw_mesh(meshes.wrist_base);

            // Wrist bend (J5)
            push_translate(0.0, self.wrist_length * 0.5, 0.0);
            push_rotate_x(self.wrist_pitch);
            draw_mesh(meshes.wrist_joint);

            // Tool (J6)
            push_translate(0.0, self.wrist_length * 0.5, 0.0);
            push_rotate_y(self.tool_roll);
            draw_mesh(meshes.tool);
        }
    }

    fn forward_kinematics(&self) -> Mat4 {
        // Calculate end effector world position
        Mat4::from_rotation_y(self.base_yaw.to_radians())
            * Mat4::from_translation(Vec3::new(0.0, 0.5, 0.0))
            * Mat4::from_rotation_x(self.shoulder_pitch.to_radians())
            * Mat4::from_translation(Vec3::new(0.0, self.upper_arm, 0.0))
            * Mat4::from_rotation_x(self.elbow_pitch.to_radians())
            * Mat4::from_translation(Vec3::new(0.0, self.forearm, 0.0))
            * Mat4::from_rotation_z(self.wrist_yaw.to_radians())
            * Mat4::from_translation(Vec3::new(0.0, self.wrist_length, 0.0))
    }
}
```

### Walking Robot (Spider/Hexapod)

```rust
struct HexapodLeg {
    hip_yaw: f32,
    hip_pitch: f32,
    knee: f32,
    ankle: f32,
}

struct Hexapod {
    legs: [HexapodLeg; 6],
    body_height: f32,
    body_pitch: f32,
    body_roll: f32,
}

impl Hexapod {
    fn walk(&mut self, time: f32, speed: f32) {
        // Tripod gait: 3 legs on ground, 3 moving
        for (i, leg) in self.legs.iter_mut().enumerate() {
            let phase = if i % 2 == 0 { 0.0 } else { 0.5 };
            let cycle = ((time * speed + phase) % 1.0) * 2.0 * PI;

            // Hip swings forward/back
            leg.hip_yaw = 15.0 * cycle.sin();

            // Leg lifts during swing phase
            let lift = (cycle.sin() + 1.0) / 2.0;  // 0 to 1
            leg.hip_pitch = -30.0 + 20.0 * lift;
            leg.knee = 60.0 - 30.0 * lift;
            leg.ankle = -30.0 + 20.0 * lift;
        }
    }

    fn render(&self, meshes: &HexapodMeshes) {
        // Body
        unsafe {
            push_identity();
            push_translate(0.0, self.body_height, 0.0);
            push_rotate_x(self.body_pitch);
            push_rotate_z(self.body_roll);
            draw_mesh(meshes.body);

            // Legs
            let leg_mounts = [
                (30.0, 0.4),   // Front right
                (30.0, -0.4),  // Front left
                (90.0, 0.5),   // Mid right
                (90.0, -0.5),  // Mid left
                (150.0, 0.4),  // Back right
                (150.0, -0.4), // Back left
            ];

            for (i, leg) in self.legs.iter().enumerate() {
                let (angle, offset) = leg_mounts[i];

                push_identity();
                push_translate(0.0, self.body_height, 0.0);
                push_rotate_y(angle);
                push_translate(0.0, 0.0, offset);

                // Coxa (hip rotation)
                push_rotate_y(leg.hip_yaw);
                draw_mesh(meshes.coxa);

                // Femur (hip pitch)
                push_translate(0.1, 0.0, 0.0);
                push_rotate_z(leg.hip_pitch);
                draw_mesh(meshes.femur);

                // Tibia (knee)
                push_translate(0.3, 0.0, 0.0);
                push_rotate_z(leg.knee);
                draw_mesh(meshes.tibia);

                // Tarsus (ankle)
                push_translate(0.3, 0.0, 0.0);
                push_rotate_z(leg.ankle);
                draw_mesh(meshes.tarsus);
            }
        }
    }
}
```

## Mechanical Props

### Door with Hinges

```rust
struct Door {
    hinge_angle: f32,
    target_angle: f32,
    angular_velocity: f32,
}

impl Door {
    fn update(&mut self, dt: f32) {
        // Spring toward target
        let spring_k = 5.0;
        let damping = 2.0;

        let spring_force = (self.target_angle - self.hinge_angle) * spring_k;
        let damp_force = -self.angular_velocity * damping;

        self.angular_velocity += (spring_force + damp_force) * dt;
        self.hinge_angle += self.angular_velocity * dt;
        self.hinge_angle = self.hinge_angle.clamp(0.0, 120.0);
    }

    fn render(&self, meshes: &DoorMeshes) {
        // Door frame (static)
        unsafe {
            push_identity();
            draw_mesh(meshes.frame);

            // Door (rotating around hinge)
            push_identity();
            push_translate(-0.05, 0.0, 0.0);  // Hinge offset
            push_rotate_y(self.hinge_angle);
            push_translate(0.05, 0.0, 0.0);   // Door center
            draw_mesh(meshes.door);

            // Handle
            push_translate(0.4, 1.0, 0.02);
            draw_mesh(meshes.handle);
        }
    }
}
```

### Crane with Cables

```rust
struct Crane {
    base_rotation: f32,
    boom_angle: f32,
    cable_length: f32,
    hook_swing: Vec2,  // Pendulum state
}

impl Crane {
    fn update(&mut self, input: &CraneInput, dt: f32) {
        self.base_rotation += input.rotate * 30.0 * dt;
        self.boom_angle = (self.boom_angle + input.boom * 20.0 * dt).clamp(10.0, 80.0);
        self.cable_length = (self.cable_length + input.cable * 2.0 * dt).clamp(1.0, 20.0);

        // Pendulum physics for hook
        let gravity = 9.8;
        let pendulum_freq = (gravity / self.cable_length).sqrt();

        // Damped harmonic oscillation
        self.hook_swing.x *= 0.99;  // Damping
        self.hook_swing.y *= 0.99;

        // Add swing from crane movement
        self.hook_swing.x += input.rotate * 0.1;
        self.hook_swing.y += input.boom * 0.05;
    }

    fn render(&self, meshes: &CraneMeshes) {
        unsafe {
            // Base
            push_identity();
            push_rotate_y(self.base_rotation);
            draw_mesh(meshes.base);

            // Boom
            push_translate(0.0, 3.0, 0.0);
            push_rotate_x(-self.boom_angle);
            draw_mesh(meshes.boom);

            // Cable attachment point
            let boom_tip = Vec3::new(0.0, 8.0, 0.0);
            push_translate(boom_tip.x, boom_tip.y, boom_tip.z);

            // Cable (multiple segments for sag effect)
            for i in 0..10 {
                let t = i as f32 / 10.0;
                let sag = 0.2 * (t * PI).sin();  // Catenary approximation
                push_translate(0.0, -self.cable_length / 10.0 + sag * 0.1, 0.0);
                draw_mesh(meshes.cable_segment);
            }

            // Hook with swing
            push_rotate_x(self.hook_swing.y * 10.0);
            push_rotate_z(self.hook_swing.x * 10.0);
            draw_mesh(meshes.hook);
        }
    }
}
```

### Gears and Mechanisms

```rust
struct GearTrain {
    input_rotation: f32,
    gear_ratios: Vec<f32>,
}

impl GearTrain {
    fn update(&mut self, input_speed: f32, dt: f32) {
        self.input_rotation += input_speed * dt;
    }

    fn render(&self, gear_meshes: &[u32], gear_positions: &[Vec3]) {
        let mut current_rotation = self.input_rotation;
        let mut direction = 1.0;

        for (i, (&mesh, &pos)) in gear_meshes.iter().zip(gear_positions).enumerate() {
            unsafe {
                push_identity();
                push_translate(pos.x, pos.y, pos.z);
                push_rotate_z(current_rotation * direction);
                draw_mesh(mesh);
            }

            // Next gear rotates opposite direction at different speed
            if i < self.gear_ratios.len() {
                current_rotation *= self.gear_ratios[i];
                direction *= -1.0;
            }
        }
    }
}

// Planetary gear system
struct PlanetaryGear {
    sun_rotation: f32,
    planet_orbits: f32,
    ring_rotation: f32,
}

impl PlanetaryGear {
    fn update(&mut self, sun_speed: f32, dt: f32) {
        self.sun_rotation += sun_speed * dt;

        // Planets orbit as sun rotates
        // Gear ratio determines relationship
        let sun_teeth = 20.0;
        let planet_teeth = 10.0;
        let ring_teeth = 40.0;

        self.planet_orbits = self.sun_rotation * sun_teeth / (sun_teeth + ring_teeth);
        self.ring_rotation = self.sun_rotation * sun_teeth / ring_teeth;
    }
}
```

## Animation Blending for Rigid Bodies

### State Machine

```rust
enum MechState {
    Idle,
    Walking,
    Running,
    Jumping,
}

struct MechAnimator {
    current_state: MechState,
    blend_progress: f32,
    blend_from: MechState,
}

impl MechAnimator {
    fn transition_to(&mut self, new_state: MechState) {
        if self.current_state != new_state {
            self.blend_from = self.current_state;
            self.current_state = new_state;
            self.blend_progress = 0.0;
        }
    }

    fn update(&mut self, dt: f32) {
        if self.blend_progress < 1.0 {
            self.blend_progress = (self.blend_progress + dt * 4.0).min(1.0);
        }
    }

    fn get_pose(&self, time: f32) -> MechPose {
        let from_pose = self.sample_state(self.blend_from, time);
        let to_pose = self.sample_state(self.current_state, time);

        from_pose.blend(&to_pose, ease_in_out_quad(self.blend_progress))
    }
}
```

### Additive Animation

Layer animations on top of base:

```rust
struct AdditiveLayer {
    base: MechPose,
    additive: Vec<(MechPose, f32)>,  // (pose, weight)
}

impl AdditiveLayer {
    fn compute(&self) -> MechPose {
        let mut result = self.base.clone();

        for (additive, weight) in &self.additive {
            result.left_arm += additive.left_arm * weight;
            result.right_arm += additive.right_arm * weight;
            // ... other joints
        }

        result
    }
}

// Example: Aiming overrides arm pose
fn apply_aim_layer(base: &MechPose, aim_direction: Vec3) -> MechPose {
    let mut result = base.clone();

    // Calculate arm angles to point at target
    let aim_yaw = aim_direction.x.atan2(aim_direction.z).to_degrees();
    let aim_pitch = (-aim_direction.y).atan2(
        (aim_direction.x.powi(2) + aim_direction.z.powi(2)).sqrt()
    ).to_degrees();

    // Override right arm
    result.right_arm.shoulder_yaw = aim_yaw;
    result.right_arm.shoulder_pitch = aim_pitch;
    result.right_arm.elbow = 0.0;  // Straight arm for aiming

    result
}
```
