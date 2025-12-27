//! Complete BVH (Biovision Hierarchy) parser for motion capture files
//!
//! Parses standard BVH format used by CMU, Mixamo, and other mocap databases.
//! Outputs skeleton hierarchy and per-frame animation data.

use std::collections::HashMap;

/// Channel types in BVH files
#[derive(Clone, Copy, PartialEq, Debug)]
pub enum Channel {
    Xposition,
    Yposition,
    Zposition,
    Xrotation,
    Yrotation,
    Zrotation,
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
        matches!(
            self,
            Channel::Xposition | Channel::Yposition | Channel::Zposition
        )
    }
}

/// A joint in the BVH skeleton hierarchy
#[derive(Clone, Debug)]
pub struct BvhJoint {
    pub name: String,
    pub offset: [f32; 3],
    pub channels: Vec<Channel>,
    pub children: Vec<usize>,
    pub parent: Option<usize>,
    pub channel_offset: usize,
}

/// Transform data for a single joint at a single frame
#[derive(Clone, Debug, Default)]
pub struct JointTransform {
    pub position: [f32; 3],
    pub rotation: [f32; 3], // Euler angles in degrees
}

/// A parsed BVH animation clip
#[derive(Clone, Debug)]
pub struct BvhClip {
    pub joints: Vec<BvhJoint>,
    pub frame_count: usize,
    pub frame_time: f32,
    pub motion_data: Vec<f32>,
    pub total_channels: usize,
    name_to_index: HashMap<String, usize>,
}

/// BVH parsing error
#[derive(Debug)]
pub struct BvhParseError {
    pub message: String,
    pub line: usize,
}

impl std::fmt::Display for BvhParseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "BVH parse error at line {}: {}", self.line, self.message)
    }
}

/// Simple tokenizer for BVH files
struct BvhTokenizer<'a> {
    chars: std::iter::Peekable<std::str::Chars<'a>>,
    line: usize,
}

impl<'a> BvhTokenizer<'a> {
    fn new(input: &'a str) -> Self {
        Self {
            chars: input.chars().peekable(),
            line: 1,
        }
    }

    fn skip_whitespace(&mut self) {
        while let Some(&c) = self.chars.peek() {
            if c == '\n' {
                self.line += 1;
                self.chars.next();
            } else if c.is_whitespace() {
                self.chars.next();
            } else {
                break;
            }
        }
    }

    fn next_token(&mut self) -> Option<String> {
        self.skip_whitespace();
        let mut token = String::new();

        while let Some(&c) = self.chars.peek() {
            if c.is_whitespace() {
                break;
            }
            if c == '{' || c == '}' {
                if token.is_empty() {
                    self.chars.next();
                    return Some(c.to_string());
                }
                break;
            }
            token.push(c);
            self.chars.next();
        }

        if token.is_empty() {
            None
        } else {
            Some(token)
        }
    }

    fn next_float(&mut self) -> Option<f32> {
        self.next_token()?.parse().ok()
    }

    fn next_int(&mut self) -> Option<usize> {
        self.next_token()?.parse().ok()
    }

    fn expect_token(&mut self, expected: &str) -> Result<(), BvhParseError> {
        match self.next_token() {
            Some(tok) if tok == expected => Ok(()),
            Some(tok) => Err(BvhParseError {
                message: format!("Expected '{}', got '{}'", expected, tok),
                line: self.line,
            }),
            None => Err(BvhParseError {
                message: format!("Expected '{}', got EOF", expected),
                line: self.line,
            }),
        }
    }
}

impl BvhClip {
    /// Parse BVH file content
    pub fn parse(content: &str) -> Result<Self, BvhParseError> {
        let mut tokenizer = BvhTokenizer::new(content);
        let mut joints = Vec::new();
        let mut channel_offset = 0usize;

        // Find HIERARCHY section
        loop {
            match tokenizer.next_token() {
                Some(tok) if tok == "HIERARCHY" => break,
                Some(_) => continue,
                None => {
                    return Err(BvhParseError {
                        message: "HIERARCHY section not found".into(),
                        line: tokenizer.line,
                    })
                }
            }
        }

        // Parse ROOT
        tokenizer.expect_token("ROOT")?;
        Self::parse_joint(&mut tokenizer, &mut joints, None, &mut channel_offset)?;

        let total_channels = channel_offset;

        // Find MOTION section
        loop {
            match tokenizer.next_token() {
                Some(tok) if tok == "MOTION" => break,
                Some(_) => continue,
                None => {
                    return Err(BvhParseError {
                        message: "MOTION section not found".into(),
                        line: tokenizer.line,
                    })
                }
            }
        }

        // Parse Frames:
        tokenizer.expect_token("Frames:")?;
        let frame_count = tokenizer.next_int().ok_or(BvhParseError {
            message: "Invalid frame count".into(),
            line: tokenizer.line,
        })?;

        // Parse Frame Time:
        tokenizer.expect_token("Frame")?;
        tokenizer.expect_token("Time:")?;
        let frame_time = tokenizer.next_float().ok_or(BvhParseError {
            message: "Invalid frame time".into(),
            line: tokenizer.line,
        })?;

        // Parse motion data
        let expected_floats = frame_count * total_channels;
        let mut motion_data = Vec::with_capacity(expected_floats);

        for i in 0..expected_floats {
            let val = tokenizer.next_float().ok_or(BvhParseError {
                message: format!(
                    "Insufficient motion data (got {}, expected {})",
                    i, expected_floats
                ),
                line: tokenizer.line,
            })?;
            motion_data.push(val);
        }

        // Build name lookup
        let name_to_index: HashMap<String, usize> = joints
            .iter()
            .enumerate()
            .map(|(i, j)| (j.name.clone(), i))
            .collect();

        Ok(BvhClip {
            joints,
            frame_count,
            frame_time,
            motion_data,
            total_channels,
            name_to_index,
        })
    }

    fn parse_joint(
        tokenizer: &mut BvhTokenizer,
        joints: &mut Vec<BvhJoint>,
        parent: Option<usize>,
        channel_offset: &mut usize,
    ) -> Result<usize, BvhParseError> {
        let name = tokenizer.next_token().ok_or(BvhParseError {
            message: "Expected joint name".into(),
            line: tokenizer.line,
        })?;

        tokenizer.expect_token("{")?;

        let my_index = joints.len();
        let my_channel_offset = *channel_offset;

        let mut offset = [0.0f32; 3];
        let mut channels = Vec::new();
        let mut children = Vec::new();

        loop {
            let tok = tokenizer.next_token().ok_or(BvhParseError {
                message: "Unexpected EOF in joint".into(),
                line: tokenizer.line,
            })?;

            match tok.as_str() {
                "OFFSET" => {
                    offset[0] = tokenizer.next_float().ok_or(BvhParseError {
                        message: "Missing X offset".into(),
                        line: tokenizer.line,
                    })?;
                    offset[1] = tokenizer.next_float().ok_or(BvhParseError {
                        message: "Missing Y offset".into(),
                        line: tokenizer.line,
                    })?;
                    offset[2] = tokenizer.next_float().ok_or(BvhParseError {
                        message: "Missing Z offset".into(),
                        line: tokenizer.line,
                    })?;
                }
                "CHANNELS" => {
                    let count = tokenizer.next_int().ok_or(BvhParseError {
                        message: "Missing channel count".into(),
                        line: tokenizer.line,
                    })?;
                    for _ in 0..count {
                        let ch_name = tokenizer.next_token().ok_or(BvhParseError {
                            message: "Missing channel name".into(),
                            line: tokenizer.line,
                        })?;
                        let ch = Channel::from_str(&ch_name).ok_or(BvhParseError {
                            message: format!("Unknown channel: {}", ch_name),
                            line: tokenizer.line,
                        })?;
                        channels.push(ch);
                    }
                    *channel_offset += count;
                }
                "JOINT" => {
                    // Add placeholder for this joint before parsing child
                    joints.push(BvhJoint {
                        name: name.clone(),
                        offset,
                        channels: channels.clone(),
                        children: Vec::new(),
                        parent,
                        channel_offset: my_channel_offset,
                    });
                    let child_idx =
                        Self::parse_joint(tokenizer, joints, Some(my_index), channel_offset)?;
                    children.push(child_idx);
                }
                "End" => {
                    // End Site - no channels, just offset
                    tokenizer.expect_token("Site")?;
                    tokenizer.expect_token("{")?;
                    tokenizer.expect_token("OFFSET")?;
                    tokenizer.next_float(); // x
                    tokenizer.next_float(); // y
                    tokenizer.next_float(); // z
                    tokenizer.expect_token("}")?;
                }
                "}" => break,
                _ => {
                    // Unknown token, skip
                }
            }
        }

        // Update or add joint
        if my_index < joints.len() {
            joints[my_index].children = children;
        } else {
            joints.push(BvhJoint {
                name,
                offset,
                channels,
                children,
                parent,
                channel_offset: my_channel_offset,
            });
        }

        Ok(my_index)
    }

    /// Get joint index by name
    pub fn joint_index(&self, name: &str) -> Option<usize> {
        self.name_to_index.get(name).copied()
    }

    /// Sample joint transform at specific frame
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

    /// Interpolate joint transform at time (with lerp)
    pub fn sample_joint_lerp(&self, joint_idx: usize, time: f32) -> JointTransform {
        let frame_f = time / self.frame_time;
        let frame_a = (frame_f as usize).min(self.frame_count.saturating_sub(1));
        let frame_b = (frame_a + 1).min(self.frame_count.saturating_sub(1));
        let t = frame_f.fract();

        if frame_a == frame_b {
            return self.sample_joint(joint_idx, frame_a);
        }

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

    /// Get animation duration in seconds
    pub fn duration(&self) -> f32 {
        self.frame_count as f32 * self.frame_time
    }

    /// Get frames per second
    pub fn fps(&self) -> f32 {
        1.0 / self.frame_time
    }

    /// Print skeleton hierarchy for debugging
    pub fn print_hierarchy(&self) {
        fn print_joint(clip: &BvhClip, idx: usize, depth: usize) {
            let joint = &clip.joints[idx];
            let indent = "  ".repeat(depth);
            println!(
                "{}[{}] {} (offset: {:?}, channels: {})",
                indent,
                idx,
                joint.name,
                joint.offset,
                joint.channels.len()
            );
            for &child in &joint.children {
                print_joint(clip, child, depth + 1);
            }
        }

        if !self.joints.is_empty() {
            print_joint(self, 0, 0);
        }
    }
}

fn lerp(a: f32, b: f32, t: f32) -> f32 {
    a + (b - a) * t
}

fn lerp_angle(a: f32, b: f32, t: f32) -> f32 {
    let mut diff = b - a;
    while diff > 180.0 {
        diff -= 360.0;
    }
    while diff < -180.0 {
        diff += 360.0;
    }
    a + diff * t
}

// ============================================================================
// Usage Example
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    const SAMPLE_BVH: &str = r#"
HIERARCHY
ROOT Hips
{
    OFFSET 0.00 0.00 0.00
    CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
    JOINT Spine
    {
        OFFSET 0.00 10.00 0.00
        CHANNELS 3 Zrotation Xrotation Yrotation
        End Site
        {
            OFFSET 0.00 15.00 0.00
        }
    }
    JOINT LeftUpLeg
    {
        OFFSET -10.00 0.00 0.00
        CHANNELS 3 Zrotation Xrotation Yrotation
        JOINT LeftLeg
        {
            OFFSET 0.00 -40.00 0.00
            CHANNELS 3 Zrotation Xrotation Yrotation
            End Site
            {
                OFFSET 0.00 -40.00 0.00
            }
        }
    }
}
MOTION
Frames: 3
Frame Time: 0.033333
0.0 90.0 0.0 0.0 0.0 0.0 5.0 0.0 0.0 0.0 0.0 10.0 0.0 0.0 0.0
0.0 90.0 1.0 0.0 0.0 0.0 5.0 0.0 0.0 0.0 0.0 10.0 0.0 0.0 0.0
0.0 90.0 2.0 0.0 0.0 0.0 5.0 0.0 0.0 0.0 0.0 10.0 0.0 0.0 0.0
"#;

    #[test]
    fn test_parse_bvh() {
        let clip = BvhClip::parse(SAMPLE_BVH).expect("Failed to parse BVH");

        assert_eq!(clip.joints.len(), 4);
        assert_eq!(clip.frame_count, 3);
        assert!((clip.frame_time - 0.033333).abs() < 0.0001);

        // Check hierarchy
        assert_eq!(clip.joints[0].name, "Hips");
        assert_eq!(clip.joints[0].channels.len(), 6);

        // Check sampling
        let hips_frame_0 = clip.sample_joint(0, 0);
        assert_eq!(hips_frame_0.position[1], 90.0);

        clip.print_hierarchy();
    }

    #[test]
    fn test_interpolation() {
        let clip = BvhClip::parse(SAMPLE_BVH).expect("Failed to parse BVH");

        // Midway between frame 0 and 1
        let interp = clip.sample_joint_lerp(0, clip.frame_time * 0.5);
        assert!((interp.position[2] - 0.5).abs() < 0.01);
    }
}

fn main() {
    // Example: Load and sample a BVH file
    let bvh_content = std::fs::read_to_string("walk.bvh").expect("Failed to read BVH file");

    let clip = BvhClip::parse(&bvh_content).expect("Failed to parse BVH");

    println!("Loaded BVH:");
    println!("  Joints: {}", clip.joints.len());
    println!("  Frames: {}", clip.frame_count);
    println!("  Duration: {:.2}s", clip.duration());
    println!("  FPS: {:.0}", clip.fps());
    println!();

    clip.print_hierarchy();

    // Sample first frame
    println!("\nFrame 0:");
    for (i, joint) in clip.joints.iter().enumerate() {
        let transform = clip.sample_joint(i, 0);
        println!(
            "  {}: pos={:?}, rot={:?}",
            joint.name, transform.position, transform.rotation
        );
    }
}
