# BVH File Format Reference

Complete specification for parsing BVH (Biovision Hierarchy) motion capture files.

## File Structure

```
HIERARCHY
ROOT Hips
{
    OFFSET 0.00 0.00 0.00
    CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
    JOINT Spine
    {
        OFFSET 0.00 10.55 0.00
        CHANNELS 3 Zrotation Xrotation Yrotation
        JOINT Spine1
        {
            ...
        }
    }
    JOINT LeftUpLeg
    {
        ...
        End Site
        {
            OFFSET 0.00 -40.00 0.00
        }
    }
}
MOTION
Frames: 120
Frame Time: 0.0333333
0.00 98.50 0.00 0.50 -2.30 1.20 ...
0.00 98.48 0.02 0.52 -2.28 1.18 ...
...
```

## HIERARCHY Section

### Keywords

| Keyword | Description |
|---------|-------------|
| `ROOT` | Root joint (only one per file) |
| `JOINT` | Child joint |
| `End Site` | Leaf node (no channels) |
| `OFFSET` | Position relative to parent |
| `CHANNELS` | Number and order of data channels |

### Channel Types

| Channel | Meaning | Units |
|---------|---------|-------|
| `Xposition` | Translation along X | Source units (usually cm) |
| `Yposition` | Translation along Y | Source units |
| `Zposition` | Translation along Z | Source units |
| `Xrotation` | Rotation around X | Degrees |
| `Yrotation` | Rotation around Y | Degrees |
| `Zrotation` | Rotation around Z | Degrees |

### Rotation Order

The order channels appear determines Euler application order:
- `Zrotation Xrotation Yrotation` → Apply Z, then X, then Y
- CMU typically uses ZXY order

## MOTION Section

### Header

```
MOTION
Frames: <frame_count>
Frame Time: <seconds_per_frame>
```

- **Frame Time:** Usually 0.0333333 (30fps) or 0.0083333 (120fps)

### Data Rows

Each row contains all channel values for one frame:
- Values in order of channel declaration
- Root channels first, then depth-first traversal
- Space-separated floating point numbers

## Parsing Implementation

### Data Structures

```rust
#[derive(Clone, Copy, PartialEq, Debug)]
pub enum Channel {
    Xposition, Yposition, Zposition,
    Xrotation, Yrotation, Zrotation,
}

impl Channel {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "Xposition" => Some(Channel::Xposition),
            "Yposition" => Some(Channel::Yposition),
            "Zposition" => Some(Channel::Zposition),
            "Xrotation" => Some(Channel::Xrotation),
            "Yrotation" => Some(Channel::Yrotation),
            "Zrotation" => Some(Channel::Zrotation),
            _ => None,
        }
    }

    pub fn is_position(&self) -> bool {
        matches!(self, Channel::Xposition | Channel::Yposition | Channel::Zposition)
    }
}

#[derive(Clone, Debug)]
pub struct BvhJoint {
    pub name: String,
    pub offset: [f32; 3],
    pub channels: Vec<Channel>,
    pub children: Vec<usize>,
    pub parent: Option<usize>,
    pub channel_offset: usize,  // Index into motion_data
}

#[derive(Clone, Debug)]
pub struct BvhClip {
    pub joints: Vec<BvhJoint>,
    pub frame_count: usize,
    pub frame_time: f32,
    pub motion_data: Vec<f32>,
    pub total_channels: usize,
}
```

### Tokenizer

```rust
pub struct BvhTokenizer<'a> {
    chars: std::iter::Peekable<std::str::Chars<'a>>,
}

impl<'a> BvhTokenizer<'a> {
    pub fn new(input: &'a str) -> Self {
        Self { chars: input.chars().peekable() }
    }

    fn skip_whitespace(&mut self) {
        while let Some(&c) = self.chars.peek() {
            if c.is_whitespace() {
                self.chars.next();
            } else {
                break;
            }
        }
    }

    pub fn next_token(&mut self) -> Option<String> {
        self.skip_whitespace();
        let mut token = String::new();

        while let Some(&c) = self.chars.peek() {
            if c.is_whitespace() || c == '{' || c == '}' {
                if token.is_empty() && (c == '{' || c == '}') {
                    self.chars.next();
                    return Some(c.to_string());
                }
                break;
            }
            token.push(c);
            self.chars.next();
        }

        if token.is_empty() { None } else { Some(token) }
    }

    pub fn next_float(&mut self) -> Option<f32> {
        self.next_token()?.parse().ok()
    }
}
```

### Hierarchy Parser

```rust
impl BvhClip {
    pub fn parse(content: &str) -> Result<Self, String> {
        let mut tokenizer = BvhTokenizer::new(content);
        let mut joints = Vec::new();
        let mut channel_offset = 0usize;

        // Find HIERARCHY
        while let Some(tok) = tokenizer.next_token() {
            if tok == "HIERARCHY" { break; }
        }

        // Parse ROOT
        let root_kw = tokenizer.next_token();
        if root_kw.as_deref() != Some("ROOT") {
            return Err("Expected ROOT".into());
        }

        Self::parse_joint(&mut tokenizer, &mut joints, None, &mut channel_offset)?;

        // Find MOTION section
        while let Some(tok) = tokenizer.next_token() {
            if tok == "MOTION" { break; }
        }

        // Parse "Frames: N"
        tokenizer.next_token();  // "Frames:"
        let frame_count: usize = tokenizer.next_token()
            .ok_or("Missing frame count")?
            .parse()
            .map_err(|_| "Invalid frame count")?;

        // Parse "Frame Time: T"
        tokenizer.next_token();  // "Frame"
        tokenizer.next_token();  // "Time:"
        let frame_time: f32 = tokenizer.next_float()
            .ok_or("Missing frame time")?;

        // Parse motion data
        let total_channels = channel_offset;
        let expected_floats = frame_count * total_channels;
        let mut motion_data = Vec::with_capacity(expected_floats);

        for _ in 0..expected_floats {
            let val = tokenizer.next_float()
                .ok_or("Insufficient motion data")?;
            motion_data.push(val);
        }

        Ok(BvhClip {
            joints,
            frame_count,
            frame_time,
            motion_data,
            total_channels,
        })
    }

    fn parse_joint(
        tokenizer: &mut BvhTokenizer,
        joints: &mut Vec<BvhJoint>,
        parent: Option<usize>,
        channel_offset: &mut usize,
    ) -> Result<usize, String> {
        let name = tokenizer.next_token().ok_or("Expected joint name")?;
        let open_brace = tokenizer.next_token();
        if open_brace.as_deref() != Some("{") {
            return Err("Expected '{'".into());
        }

        let mut offset = [0.0f32; 3];
        let mut channels = Vec::new();
        let my_channel_offset = *channel_offset;

        loop {
            let tok = tokenizer.next_token().ok_or("Unexpected EOF")?;
            match tok.as_str() {
                "OFFSET" => {
                    offset[0] = tokenizer.next_float().ok_or("Missing X offset")?;
                    offset[1] = tokenizer.next_float().ok_or("Missing Y offset")?;
                    offset[2] = tokenizer.next_float().ok_or("Missing Z offset")?;
                }
                "CHANNELS" => {
                    let count: usize = tokenizer.next_token()
                        .ok_or("Missing channel count")?
                        .parse()
                        .map_err(|_| "Invalid channel count")?;
                    for _ in 0..count {
                        let ch_name = tokenizer.next_token()
                            .ok_or("Missing channel name")?;
                        let ch = Channel::from_str(&ch_name)
                            .ok_or(format!("Unknown channel: {}", ch_name))?;
                        channels.push(ch);
                    }
                    *channel_offset += count;
                }
                "JOINT" => {
                    let joint_idx = joints.len();
                    joints.push(BvhJoint {
                        name: name.clone(),
                        offset,
                        channels: channels.clone(),
                        children: Vec::new(),
                        parent,
                        channel_offset: my_channel_offset,
                    });
                    let child_idx = Self::parse_joint(
                        tokenizer, joints, Some(joint_idx), channel_offset
                    )?;
                    joints[joint_idx].children.push(child_idx);
                    continue;
                }
                "End" => {
                    tokenizer.next_token();  // "Site"
                    tokenizer.next_token();  // "{"
                    tokenizer.next_token();  // "OFFSET"
                    tokenizer.next_float();  // x
                    tokenizer.next_float();  // y
                    tokenizer.next_float();  // z
                    tokenizer.next_token();  // "}"
                }
                "}" => break,
                _ => {}
            }
        }

        let idx = joints.len();
        joints.push(BvhJoint {
            name,
            offset,
            channels,
            children: Vec::new(),
            parent,
            channel_offset: my_channel_offset,
        });
        Ok(idx)
    }
}
```

## Sampling Animation

### Get Joint Transform at Frame

```rust
#[derive(Clone, Default)]
pub struct JointTransform {
    pub position: [f32; 3],
    pub rotation: [f32; 3],  // Euler angles in degrees
}

impl BvhClip {
    pub fn sample_joint(&self, joint_idx: usize, frame: usize) -> JointTransform {
        let joint = &self.joints[joint_idx];
        let base = frame * self.total_channels + joint.channel_offset;

        let mut transform = JointTransform::default();
        for (i, channel) in joint.channels.iter().enumerate() {
            let value = self.motion_data[base + i];
            match channel {
                Channel::Xposition => transform.position[0] = value,
                Channel::Yposition => transform.position[1] = value,
                Channel::Zposition => transform.position[2] = value,
                Channel::Xrotation => transform.rotation[0] = value,
                Channel::Yrotation => transform.rotation[1] = value,
                Channel::Zrotation => transform.rotation[2] = value,
            }
        }
        transform
    }

    /// Interpolate between frames
    pub fn sample_joint_lerp(
        &self,
        joint_idx: usize,
        time: f32,
    ) -> JointTransform {
        let frame_f = time / self.frame_time;
        let frame_a = (frame_f as usize).min(self.frame_count - 1);
        let frame_b = (frame_a + 1).min(self.frame_count - 1);
        let t = frame_f.fract();

        let a = self.sample_joint(joint_idx, frame_a);
        let b = self.sample_joint(joint_idx, frame_b);

        JointTransform {
            position: [
                lerp(a.position[0], b.position[0], t),
                lerp(a.position[1], b.position[1], t),
                lerp(a.position[2], b.position[2], t),
            ],
            rotation: [
                lerp_angle(a.rotation[0], b.rotation[0], t),
                lerp_angle(a.rotation[1], b.rotation[1], t),
                lerp_angle(a.rotation[2], b.rotation[2], t),
            ],
        }
    }
}

fn lerp(a: f32, b: f32, t: f32) -> f32 {
    a + (b - a) * t
}

fn lerp_angle(a: f32, b: f32, t: f32) -> f32 {
    let mut diff = b - a;
    while diff > 180.0 { diff -= 360.0; }
    while diff < -180.0 { diff += 360.0; }
    a + diff * t
}
```

## Common CMU Skeleton Structure

```
Hips (ROOT)
├── Spine
│   └── Spine1
│       └── Neck
│           └── Head
├── LeftShoulder
│   └── LeftArm
│       └── LeftForeArm
│           └── LeftHand
├── RightShoulder
│   └── RightArm
│       └── RightForeArm
│           └── RightHand
├── LeftUpLeg
│   └── LeftLeg
│       └── LeftFoot
│           └── LeftToeBase
└── RightUpLeg
    └── RightLeg
        └── RightFoot
            └── RightToeBase
```

**Note:** Actual bone names vary between CMU subjects. Some use "LHipJoint" instead of "LeftUpLeg".
