# Animation Enhancement Techniques

Detailed techniques for upgrading animation quality through the tier system, based on the 12 Principles of Animation.

## Placeholder → Temp Upgrades

### Add Proper Timing

Transform linear motion into timed motion:

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any

class Interpolation(Enum):
    LINEAR = 'linear'
    EASE_IN_OUT = 'ease_in_out'

class Easing(Enum):
    LINEAR = 'linear'
    QUAD_IN = 'quad_in'
    QUAD_OUT = 'quad_out'
    QUAD_IN_OUT = 'quad_in_out'
    CUBIC_IN_OUT = 'cubic_in_out'
    SINE_IN_OUT = 'sine_in_out'
    SINE_OUT = 'sine_out'

@dataclass
class Keyframe:
    time: float
    value: Any
    easing: Easing = Easing.LINEAR

@dataclass
class Animation:
    keyframes: List[Keyframe] = field(default_factory=list)
    interpolation: Interpolation = Interpolation.LINEAR

    def set_interpolation(self, interp: Interpolation):
        self.interpolation = interp

    def set_all_easing(self, easing: Easing):
        for kf in self.keyframes:
            kf.easing = easing

# Before: Linear interpolation
animation = Animation()
animation.set_interpolation(Interpolation.LINEAR)

# After: Add basic easing
animation.set_interpolation(Interpolation.EASE_IN_OUT)

# Per-keyframe timing
animation.set_all_easing(Easing.QUAD_IN_OUT)
```

### Add Keyframes for Clarity

Placeholder animations often have too few keyframes:

```python
from dataclasses import dataclass
from typing import Dict

@dataclass
class Pose:
    """Represents a character pose with bone transforms."""
    bone_transforms: Dict[str, tuple]  # bone_name -> (position, rotation)

    @staticmethod
    def contact_right() -> 'Pose':
        return Pose({'right_foot': ((0, 0, 0), (0, 0, 0))})

    @staticmethod
    def passing_right() -> 'Pose':
        return Pose({'right_foot': ((0, 0.1, 0), (15, 0, 0))})

    @staticmethod
    def contact_left() -> 'Pose':
        return Pose({'left_foot': ((0, 0, 0), (0, 0, 0))})

    @staticmethod
    def passing_left() -> 'Pose':
        return Pose({'left_foot': ((0, 0.1, 0), (15, 0, 0))})

def add_walk_cycle_keyframes(animation: Animation):
    """Add walk cycle minimum keyframes."""
    walk_keyframes = [
        (0.0, Pose.contact_right()),    # Right foot contact
        (0.25, Pose.passing_right()),   # Right leg passing
        (0.5, Pose.contact_left()),     # Left foot contact
        (0.75, Pose.passing_left()),    # Left leg passing
        (1.0, Pose.contact_right()),    # Loop back
    ]

    for time, pose in walk_keyframes:
        animation.keyframes.append(Keyframe(time=time, value=pose))
```

### Fix Loop Points

Ensure seamless looping:

```python
import numpy as np
from dataclasses import dataclass
from typing import Dict

def poses_match(pose_a: Pose, pose_b: Pose, threshold: float = 0.01) -> bool:
    """Check if two poses are similar within threshold."""
    for bone in pose_a.bone_transforms:
        if bone not in pose_b.bone_transforms:
            return False
        pos_a, rot_a = pose_a.bone_transforms[bone]
        pos_b, rot_b = pose_b.bone_transforms[bone]
        pos_diff = np.linalg.norm(np.array(pos_a) - np.array(pos_b))
        rot_diff = np.linalg.norm(np.array(rot_a) - np.array(rot_b))
        if pos_diff > threshold or rot_diff > threshold:
            return False
    return True

def blend_poses(pose_a: Pose, pose_b: Pose, factor: float) -> Pose:
    """Blend between two poses."""
    result = {}
    for bone in pose_a.bone_transforms:
        if bone in pose_b.bone_transforms:
            pos_a, rot_a = pose_a.bone_transforms[bone]
            pos_b, rot_b = pose_b.bone_transforms[bone]
            pos = tuple(a * (1 - factor) + b * factor for a, b in zip(pos_a, pos_b))
            rot = tuple(a * (1 - factor) + b * factor for a, b in zip(rot_a, rot_b))
            result[bone] = (pos, rot)
    return Pose(result)

def fix_loop_continuity(animation: Animation, threshold: float = 0.01):
    """Ensure animation loops seamlessly."""
    if not animation.keyframes:
        return

    start_pose = animation.keyframes[0].value
    end_pose = animation.keyframes[-1].value

    if not poses_match(start_pose, end_pose, threshold):
        # Add transition keyframe
        blended = blend_poses(end_pose, start_pose, 0.5)
        animation.keyframes.insert(-1, Keyframe(time=0.95, value=blended))
        animation.keyframes[-1].value = start_pose
```

---

## Temp → Final Upgrades

### Add Easing (Slow In/Slow Out)

Natural motion accelerates and decelerates:

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class BoneType(Enum):
    ROOT = 'root'
    SPINE = 'spine'
    HAND = 'hand'
    FOOT = 'foot'
    HEAD = 'head'
    OTHER = 'other'

@dataclass
class AnimationTrack:
    bone_name: str
    bone_type: BoneType
    keyframes: List[Keyframe]
    easing: Easing = Easing.LINEAR

    def set_easing(self, easing: Easing):
        self.easing = easing

@dataclass
class AnimationWithTracks:
    tracks: List[AnimationTrack]

def apply_easing_profile(animation: AnimationWithTracks):
    """Configure easing per bone/property."""
    for track in animation.tracks:
        if track.bone_type == BoneType.ROOT:
            # Root motion: smooth ease
            track.set_easing(Easing.CUBIC_IN_OUT)
        elif track.bone_type in (BoneType.HAND, BoneType.FOOT):
            # Extremities: snappier
            track.set_easing(Easing.QUAD_OUT)
        elif track.bone_type == BoneType.SPINE:
            # Spine: smooth follow-through
            track.set_easing(Easing.SINE_IN_OUT)
        else:
            track.set_easing(Easing.QUAD_IN_OUT)
```

### Add Secondary Motion

Body parts don't all move at once:

```python
from typing import Dict, Optional

def offset_track_time(track: AnimationTrack, delay: float):
    """Offset all keyframe times in a track."""
    for kf in track.keyframes:
        kf.time += delay

def get_track_by_name(animation: AnimationWithTracks,
                      bone_name: str) -> Optional[AnimationTrack]:
    """Get animation track by bone name."""
    for track in animation.tracks:
        if track.bone_name == bone_name:
            return track
    return None

def add_secondary_motion(animation: AnimationWithTracks):
    """Offset secondary elements for drag/follow-through effect."""
    offsets = [
        ("head", 0.02),        # Head follows slightly
        ("hair", 0.04),        # Hair lags more
        ("cape", 0.05),        # Cape lags most
        ("weapon", 0.03),      # Weapon has inertia
    ]

    for bone_name, delay in offsets:
        track = get_track_by_name(animation, bone_name)
        if track:
            offset_track_time(track, delay)
```

### Implement Arc Motion

Natural motion follows arcs, not straight lines:

```python
import numpy as np
from typing import Tuple

@dataclass
class PositionKeyframe:
    time: float
    position: Tuple[float, float, float]
    easing: Easing = Easing.LINEAR

@dataclass
class PositionTrack:
    bone_name: str
    keyframes: List[PositionKeyframe]

    def insert_keyframe(self, time: float, position: Tuple[float, float, float],
                        easing: Easing):
        """Insert keyframe at specified time, maintaining sorted order."""
        kf = PositionKeyframe(time=time, position=position, easing=easing)
        # Find insertion point
        for i, existing in enumerate(self.keyframes):
            if existing.time > time:
                self.keyframes.insert(i, kf)
                return
        self.keyframes.append(kf)

def arcify_motion(track: PositionTrack):
    """Convert linear motion to arcs for natural movement."""
    # Work backwards to avoid index issues when inserting
    for i in range(len(track.keyframes) - 2, -1, -1):
        start = track.keyframes[i]
        end = track.keyframes[i + 1]

        start_pos = np.array(start.position)
        end_pos = np.array(end.position)

        # Calculate arc control point
        mid_time = (start.time + end.time) / 2.0
        arc_height = np.linalg.norm(end_pos - start_pos) * 0.2

        # Add arc keyframe (lift in Y direction)
        arc_pos = (start_pos + end_pos) / 2.0
        arc_pos[1] += arc_height  # Y is up

        track.insert_keyframe(mid_time, tuple(arc_pos), Easing.SINE_IN_OUT)
```

### Improve Weight and Timing

Different actions have different timing feels:

```python
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class ActionType(Enum):
    WALK = auto()
    RUN = auto()
    JUMP = auto()
    ATTACK = auto()

@dataclass
class TimingProfile:
    total_frames: int
    key_poses: List[int]
    contact_frame: int = 0
    passing_frame: Optional[int] = None
    anticipation_frames: Optional[int] = None
    air_frames: Optional[int] = None
    landing_frames: Optional[int] = None
    action_frames: Optional[int] = None
    follow_through_frames: Optional[int] = None

def get_timing_profile(action: ActionType) -> TimingProfile:
    """Get timing guidelines by action type."""
    profiles = {
        ActionType.WALK: TimingProfile(
            total_frames=16,
            contact_frame=0,
            passing_frame=4,
            key_poses=[0, 4, 8, 12],
        ),
        ActionType.RUN: TimingProfile(
            total_frames=12,
            contact_frame=0,
            passing_frame=3,
            key_poses=[0, 3, 6, 9],
        ),
        ActionType.JUMP: TimingProfile(
            total_frames=24,
            anticipation_frames=4,
            air_frames=16,
            landing_frames=4,
            key_poses=[0, 4, 12, 20, 24],
        ),
        ActionType.ATTACK: TimingProfile(
            total_frames=20,
            anticipation_frames=6,
            action_frames=4,
            follow_through_frames=10,
            key_poses=[0, 6, 10, 20],
        ),
    }
    return profiles.get(action, profiles[ActionType.WALK])
```

---

## Final → Hero Upgrades

### Add Anticipation

Preparation before main action:

```python
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class ArmPosition(Enum):
    NEUTRAL = 'neutral'
    BACK = 'back'
    FORWARD = 'forward'

@dataclass
class JumpPose:
    root_y: float = 0.0
    spine_rotation: float = 0.0
    knee_bend: float = 0.0
    arm_position: ArmPosition = ArmPosition.NEUTRAL

    def deeper(self, factor: float) -> 'JumpPose':
        """Return a deeper version of this pose."""
        return JumpPose(
            root_y=self.root_y * factor,
            spine_rotation=self.spine_rotation * factor,
            knee_bend=self.knee_bend * factor,
            arm_position=self.arm_position,
        )

@dataclass
class PunchPose:
    shoulder_rotation: float = 0.0
    elbow_bend: float = 0.0
    torso_rotation: float = 0.0
    weight_shift: float = 0.0

    def exaggerated(self, factor: float) -> 'PunchPose':
        """Return an exaggerated version of this pose."""
        return PunchPose(
            shoulder_rotation=self.shoulder_rotation * factor,
            elbow_bend=self.elbow_bend * factor,
            torso_rotation=self.torso_rotation * factor,
            weight_shift=self.weight_shift * factor,
        )

def add_jump_anticipation(animation: Animation):
    """Add anticipation before jump."""
    # Before jump: crouch down
    anticipation_pose = JumpPose(
        root_y=-0.1,           # Squat down
        spine_rotation=-5.0,   # Lean forward slightly
        knee_bend=30.0,        # Bend knees
        arm_position=ArmPosition.BACK,  # Arms back
    )

    # Insert anticipation before jump
    animation.keyframes.insert(0, Keyframe(time=0.0, value=anticipation_pose))
    animation.keyframes.insert(1, Keyframe(time=0.15, value=anticipation_pose.deeper(1.2)))
    # Original jump starts at 0.2

def add_punch_anticipation(animation: Animation):
    """Add anticipation before punch."""
    wind_up = PunchPose(
        shoulder_rotation=-30.0,  # Pull back
        elbow_bend=120.0,         # Coil arm
        torso_rotation=-15.0,     # Wind up body
        weight_shift=-0.1,        # Lean back
    )

    animation.keyframes.insert(0, Keyframe(time=0.0, value=wind_up))
    animation.keyframes.insert(1, Keyframe(time=0.1, value=wind_up.exaggerated(1.1)))
    # Strike starts at 0.15
```

### Add Follow-Through

Motion continues after main action:

```python
from dataclasses import dataclass
from typing import List, Tuple, Union

@dataclass
class FollowThroughPose:
    arm_extension: float = 1.0
    shoulder_forward: float = 0.0
    torso_rotation: float = 0.0

def add_punch_follow_through(animation: Animation, impact_time: float):
    """Add follow-through after punch impact."""
    # After impact: arm continues, body follows
    follow_poses: List[Tuple[float, FollowThroughPose]] = [
        (0.05, FollowThroughPose(
            arm_extension=1.1,      # Overextend
            shoulder_forward=10.0,
            torso_rotation=20.0,
        )),
        (0.15, FollowThroughPose(
            arm_extension=1.05,     # Slight recoil
            shoulder_forward=5.0,
            torso_rotation=15.0,
        )),
        (0.3, FollowThroughPose(
            arm_extension=0.9,      # Return
            shoulder_forward=0.0,
            torso_rotation=5.0,
        )),
    ]

    for time_offset, pose in follow_poses:
        animation.keyframes.append(
            Keyframe(time=impact_time + time_offset, value=pose)
        )
```

### Overlapping Action

Different body parts move at different times:

```python
from typing import List, Tuple

def add_overlapping_turn(animation: AnimationWithTracks):
    """Add overlapping action for character turn.

    Order of movement: hips -> spine -> shoulders -> head -> hair
    """
    overlap_delays: List[Tuple[str, float]] = [
        ("hips", 0.0),
        ("spine_lower", 0.02),
        ("spine_upper", 0.04),
        ("shoulders", 0.06),
        ("neck", 0.08),
        ("head", 0.10),
        ("hair_base", 0.12),
        ("hair_tip", 0.15),
    ]

    for bone, delay in overlap_delays:
        track = get_track_by_name(animation, bone)
        if track:
            offset_track_time(track, delay)
            # Also ease the delayed motion
            track.set_easing(Easing.SINE_OUT)
```

### Exaggeration

Push poses beyond realistic for readability:

```python
from enum import Enum, auto
from typing import List, Any
import numpy as np

class AnimationType(Enum):
    IDLE = auto()
    WALK = auto()
    RUN = auto()
    ATTACK = auto()
    HURT = auto()
    DEATH = auto()

def lerp_pose(neutral: Pose, target: Pose, factor: float) -> Pose:
    """Linearly interpolate between poses."""
    result = {}
    for bone in neutral.bone_transforms:
        if bone in target.bone_transforms:
            n_pos, n_rot = neutral.bone_transforms[bone]
            t_pos, t_rot = target.bone_transforms[bone]
            pos = tuple(n + (t - n) * factor for n, t in zip(n_pos, t_pos))
            rot = tuple(n + (t - n) * factor for n, t in zip(n_rot, t_rot))
            result[bone] = (pos, rot)
    return Pose(result)

def find_extreme_poses(animation: Animation) -> List[int]:
    """Find frames with extreme poses (local maxima/minima)."""
    # Simple heuristic: every 4th frame in the animation
    return list(range(0, len(animation.keyframes), 4))

def exaggerate_keyframes(animation: Animation, neutral_pose: Pose, amount: float):
    """Exaggerate key poses away from neutral."""
    key_frames = find_extreme_poses(animation)

    for frame_idx in key_frames:
        if frame_idx < len(animation.keyframes):
            pose = animation.keyframes[frame_idx].value
            if isinstance(pose, Pose):
                # Exaggerate away from neutral
                exaggerated = lerp_pose(neutral_pose, pose, 1.0 + amount)
                animation.keyframes[frame_idx].value = exaggerated

def get_exaggeration_amount(anim_type: AnimationType) -> float:
    """Get exaggeration amount by animation type."""
    amounts = {
        AnimationType.IDLE: 0.05,     # Subtle
        AnimationType.WALK: 0.1,      # Noticeable
        AnimationType.RUN: 0.15,      # Clear
        AnimationType.ATTACK: 0.25,   # Dramatic
        AnimationType.HURT: 0.3,      # Very dramatic
        AnimationType.DEATH: 0.35,    # Maximum
    }
    return amounts.get(anim_type, 0.1)
```

### Squash and Stretch

Volume preservation with deformation:

```python
from dataclasses import dataclass
from typing import Tuple
import numpy as np

STRETCH_THRESHOLD = 0.1

@dataclass
class ScaledPose:
    base_pose: Pose
    scale: Tuple[float, float, float]  # x, y, z scale

@dataclass
class PoseWithPosition:
    bone_transforms: dict
    root_position: Tuple[float, float, float]
    root_y: float

    def with_scale(self, scale: Tuple[float, float, float]) -> 'ScaledPose':
        return ScaledPose(base_pose=Pose(self.bone_transforms), scale=scale)

    def stretch_along(self, direction: np.ndarray, stretch: float) -> 'ScaledPose':
        # Stretch along motion direction, compress perpendicular
        scale_along = stretch
        scale_perp = 1.0 / np.sqrt(stretch)  # Preserve volume
        # Simplified: assume stretch is along Y
        return self.with_scale((scale_perp, scale_along, scale_perp))

def add_landing_squash(animation: Animation, impact_frame: int):
    """Add squash on landing impact."""
    if impact_frame < 1 or impact_frame >= len(animation.keyframes):
        return

    pre_impact = animation.keyframes[impact_frame - 1].value
    impact = animation.keyframes[impact_frame].value

    # Calculate squash based on fall velocity
    if hasattr(pre_impact, 'root_y') and hasattr(impact, 'root_y'):
        velocity = abs(impact.root_y - pre_impact.root_y)
        squash_amount = min(velocity * 2.0, 0.3)

        # Apply squash (compress Y, expand XZ)
        squashed = impact.with_scale((
            1.0 + squash_amount * 0.5,  # Wider
            1.0 - squash_amount,         # Shorter
            1.0 + squash_amount * 0.5,  # Deeper
        ))
        animation.keyframes[impact_frame].value = squashed

        # Recovery frames
        animation.keyframes.insert(
            impact_frame + 1,
            Keyframe(time=impact_frame + 2, value=impact.with_scale((0.95, 1.05, 0.95)))
        )
        animation.keyframes.insert(
            impact_frame + 2,
            Keyframe(time=impact_frame + 4, value=impact)
        )

def add_motion_stretch(animation: Animation):
    """Add stretch during fast motion."""
    for i in range(1, len(animation.keyframes) - 1):
        prev = animation.keyframes[i - 1].value
        curr = animation.keyframes[i].value

        if hasattr(prev, 'root_position') and hasattr(curr, 'root_position'):
            prev_pos = np.array(prev.root_position)
            curr_pos = np.array(curr.root_position)
            velocity = np.linalg.norm(curr_pos - prev_pos)

            if velocity > STRETCH_THRESHOLD:
                stretch = 1.0 + (velocity - STRETCH_THRESHOLD) * 0.5
                direction = (curr_pos - prev_pos) / velocity

                # Stretch along motion direction
                stretched = curr.stretch_along(direction, stretch)
                animation.keyframes[i].value = stretched
```

---

## Animation Type Guidelines

### Walk Cycle (Final → Hero)

| Aspect | Final | Hero Addition |
|--------|-------|---------------|
| Keyframes | 8-12 | 16-24 |
| Secondary motion | Arm swing | + shoulder, spine twist |
| Overlap | Basic | Full body chain |
| Weight | Implied | Clear weight shift |
| Personality | Neutral | Character-specific |

### Run Cycle (Final → Hero)

| Aspect | Final | Hero Addition |
|--------|-------|---------------|
| Keyframes | 8-10 | 12-16 |
| Air time | Present | Exaggerated float |
| Impact | Simple | Squash on contact |
| Arms | Basic pump | Full wind-up, overlap |
| Lean | Static | Dynamic based on speed |

### Attack Animation (Final → Hero)

| Aspect | Final | Hero Addition |
|--------|-------|---------------|
| Anticipation | 2-3 frames | 4-6 frames with wind-up |
| Strike | Clear | Smear frames, stretch |
| Follow-through | Present | Overlapping settle |
| Recovery | Simple | Weight-based return |
| Exaggeration | 15% | 25-30% |

### Jump Animation (Final → Hero)

| Aspect | Final | Hero Addition |
|--------|-------|---------------|
| Anticipation | Crouch | Deep squat, arm swing |
| Launch | Simple | Stretch, anticipation |
| Air | Static pose | Slight movement, arc arms |
| Landing | Contact | Squash, recovery bounce |
| Timing | Linear | Variable (hang time) |

---

## Frame Budget by Tier

### Standard Frame Counts

| Animation | Placeholder | Temp | Final | Hero |
|-----------|-------------|------|-------|------|
| Idle | 1 | 4-6 | 8-16 | 24-48 |
| Walk | 4 | 8 | 12-16 | 16-24 |
| Run | 4 | 6-8 | 10-12 | 12-16 |
| Jump | 3 | 6-8 | 12-16 | 20-30 |
| Attack | 4 | 8-10 | 14-18 | 20-30 |
| Hurt | 2 | 4-6 | 8-12 | 12-20 |
| Death | 4 | 8-12 | 16-24 | 30-48 |

### FPS Guidelines

| Tier | Target FPS | Notes |
|------|------------|-------|
| Placeholder | 10 | Just readable |
| Temp | 15 | Smooth enough |
| Final | 20-24 | Production quality |
| Hero | 24-30 | Maximum smoothness |

---

## Quality Checks

### Loop Continuity Check

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class LoopQuality:
    position_error: float
    rotation_error: float
    velocity_match: float
    acceleration_match: float

def check_velocity_continuity(animation: Animation) -> float:
    """Check if velocity is continuous at loop point."""
    if len(animation.keyframes) < 3:
        return 1.0

    # Velocity at start
    kf0, kf1 = animation.keyframes[0], animation.keyframes[1]
    if hasattr(kf0.value, 'root_position') and hasattr(kf1.value, 'root_position'):
        v_start = np.array(kf1.value.root_position) - np.array(kf0.value.root_position)
    else:
        return 1.0

    # Velocity at end
    kf_n1, kf_n = animation.keyframes[-2], animation.keyframes[-1]
    if hasattr(kf_n1.value, 'root_position') and hasattr(kf_n.value, 'root_position'):
        v_end = np.array(kf_n.value.root_position) - np.array(kf_n1.value.root_position)
    else:
        return 1.0

    diff = np.linalg.norm(v_end - v_start)
    return max(0.0, 1.0 - diff)

def check_acceleration_continuity(animation: Animation) -> float:
    """Check if acceleration is continuous at loop point."""
    # Simplified: check velocity change rate
    return check_velocity_continuity(animation) * 0.9

def check_loop_quality(animation: Animation) -> LoopQuality:
    """Check loop quality metrics."""
    if not animation.keyframes:
        return LoopQuality(0, 0, 0, 0)

    start = animation.keyframes[0].value
    end = animation.keyframes[-1].value

    position_error = 0.0
    rotation_error = 0.0

    if hasattr(start, 'root_position') and hasattr(end, 'root_position'):
        position_error = float(np.linalg.norm(
            np.array(end.root_position) - np.array(start.root_position)
        ))

    if hasattr(start, 'root_rotation') and hasattr(end, 'root_rotation'):
        rotation_error = float(np.linalg.norm(
            np.array(end.root_rotation) - np.array(start.root_rotation)
        ))

    return LoopQuality(
        position_error=position_error,
        rotation_error=rotation_error,
        velocity_match=check_velocity_continuity(animation),
        acceleration_match=check_acceleration_continuity(animation),
    )
```

### Motion Arc Check

```python
import numpy as np
from typing import Optional

def get_position_at_time(track: PositionTrack, t: float) -> Optional[np.ndarray]:
    """Interpolate position at given time."""
    if not track.keyframes:
        return None

    # Find surrounding keyframes
    prev_kf = track.keyframes[0]
    next_kf = track.keyframes[-1]

    for i, kf in enumerate(track.keyframes):
        if kf.time >= t:
            next_kf = kf
            if i > 0:
                prev_kf = track.keyframes[i - 1]
            break
        prev_kf = kf

    # Linear interpolation
    if next_kf.time == prev_kf.time:
        return np.array(prev_kf.position)

    factor = (t - prev_kf.time) / (next_kf.time - prev_kf.time)
    factor = max(0, min(1, factor))

    prev_pos = np.array(prev_kf.position)
    next_pos = np.array(next_kf.position)
    return prev_pos + (next_pos - prev_pos) * factor

def check_arc_quality(track: PositionTrack) -> float:
    """Check how smoothly the motion follows arcs."""
    total_deviation = 0.0
    samples = 0

    # Sample motion path
    for i in range(100):
        t = i / 100.0
        prev = get_position_at_time(track, t - 0.01)
        curr = get_position_at_time(track, t)
        next_pos = get_position_at_time(track, t + 0.01)

        if prev is None or curr is None or next_pos is None:
            continue

        # Check if path curves smoothly
        expected_next = curr + (curr - prev)
        deviation = np.linalg.norm(next_pos - expected_next)
        total_deviation += deviation
        samples += 1

    if samples == 0:
        return 1.0

    return 1.0 - min(total_deviation / samples, 1.0)
```

### Timing Variation Check

```python
import numpy as np
from typing import List

def check_timing_quality(animation: Animation) -> float:
    """Check for timing variation (not constant velocity).

    Higher variance = better timing (more interesting movement).
    """
    velocities: List[float] = []

    for i in range(len(animation.keyframes) - 1):
        kf0 = animation.keyframes[i].value
        kf1 = animation.keyframes[i + 1].value

        if hasattr(kf0, 'root_position') and hasattr(kf1, 'root_position'):
            p0 = np.array(kf0.root_position)
            p1 = np.array(kf1.root_position)
            velocities.append(float(np.linalg.norm(p1 - p0)))

    if not velocities:
        return 0.0

    velocities_arr = np.array(velocities)
    mean = np.mean(velocities_arr)
    variance = np.var(velocities_arr)

    # Higher variance = better timing
    return min(variance / max(mean, 0.001), 1.0)
```
