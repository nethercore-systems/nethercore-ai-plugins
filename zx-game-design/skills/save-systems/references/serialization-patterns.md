# Serialization Patterns for Save Data

Detailed patterns for binary serialization, checksums, version migration, and complex save structures on Nethercore ZX.

## bytemuck Fundamentals

The `bytemuck` crate enables zero-copy casting between byte arrays and structs. Essential for efficient save/load.

### Requirements

Add to `Cargo.toml`:
```toml
[dependencies]
bytemuck = { version = "1.14", features = ["derive"] }
```

### Struct Requirements

For a struct to work with `bytemuck`:

```rust
use bytemuck::{Pod, Zeroable};

#[repr(C)]                    // Required: consistent memory layout
#[derive(Copy, Clone)]        // Required: Pod requires Copy
#[derive(Pod, Zeroable)]      // Required: derive both traits
struct SaveData {
    // Only primitive types and arrays allowed
    value: u32,
    array: [u8; 16],
    // NO: String, Vec, Box, Option, enum (unless repr(u8))
}
```

### Supported Types

| Type | Pod-Safe | Notes |
|------|----------|-------|
| `u8, u16, u32, u64` | Yes | All integer types |
| `i8, i16, i32, i64` | Yes | Signed integers |
| `f32, f64` | Yes | Floats (use with caution for determinism) |
| `bool` | No | Use `u8` (0/1) instead |
| `[T; N]` | Yes* | If T is Pod |
| `enum` | No* | Unless `#[repr(u8)]` or similar |
| `Option<T>` | No | Use sentinel values |
| `String, Vec` | No | Use fixed arrays |

### Safe enum Pattern

```rust
#[repr(u8)]
#[derive(Copy, Clone, Pod, Zeroable)]
enum GameMode {
    Story = 0,
    Arcade = 1,
    Survival = 2,
}
```

### Avoiding bool

```rust
// WRONG: bool is not Pod
struct Bad {
    unlocked: bool,
}

// CORRECT: use u8
#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct Good {
    unlocked: u8,  // 0 = false, 1 = true
}

impl Good {
    fn is_unlocked(&self) -> bool { self.unlocked != 0 }
    fn set_unlocked(&mut self, v: bool) { self.unlocked = v as u8; }
}
```

## Alignment and Padding

Ensure proper alignment to avoid undefined behavior:

```rust
#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct Aligned {
    // 1 byte
    byte_val: u8,
    // 3 bytes padding added automatically
    // 4 bytes
    int_val: u32,
    // Total: 8 bytes
}

// Explicit padding is clearer:
#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct ExplicitPadding {
    byte_val: u8,
    _pad: [u8; 3],   // Explicit padding
    int_val: u32,
}
```

Calculate size accurately:
```rust
const SAVE_SIZE: usize = core::mem::size_of::<GameSave>();
```

## CRC32 Checksum

Detect corruption with CRC32:

```rust
const CRC32_TABLE: [u32; 256] = generate_crc32_table();

const fn generate_crc32_table() -> [u32; 256] {
    let mut table = [0u32; 256];
    let mut i = 0;
    while i < 256 {
        let mut crc = i as u32;
        let mut j = 0;
        while j < 8 {
            if crc & 1 != 0 {
                crc = (crc >> 1) ^ 0xEDB88320;
            } else {
                crc >>= 1;
            }
            j += 1;
        }
        table[i] = crc;
        i += 1;
    }
    table
}

fn crc32(data: &[u8]) -> u32 {
    let mut crc = 0xFFFFFFFF;
    for byte in data {
        let index = ((crc ^ *byte as u32) & 0xFF) as usize;
        crc = (crc >> 8) ^ CRC32_TABLE[index];
    }
    !crc
}
```

Apply checksum to save data:

```rust
fn create_save_with_checksum(save: &mut GameSave) {
    save.header.checksum = 0;  // Zero before calculating
    let bytes = bytemuck::bytes_of(save);

    // Calculate over data portion only (skip header)
    let data_start = core::mem::size_of::<SaveHeader>();
    save.header.checksum = crc32(&bytes[data_start..]);
}

fn verify_checksum(save: &GameSave) -> bool {
    let stored = save.header.checksum;

    // Create copy with zeroed checksum
    let mut temp = *save;
    temp.header.checksum = 0;
    let bytes = bytemuck::bytes_of(&temp);

    let data_start = core::mem::size_of::<SaveHeader>();
    let calculated = crc32(&bytes[data_start..]);

    stored == calculated
}
```

## Version Migration

Handle save format changes across game updates:

```rust
const CURRENT_VERSION: u32 = 3;

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct SaveV1 {
    header: SaveHeader,
    level: u8,
    health: u8,
    _pad: [u8; 2],
}

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct SaveV2 {
    header: SaveHeader,
    level: u8,
    health: u8,
    checkpoint: u8,     // Added in V2
    _pad: u8,
}

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct SaveV3 {
    header: SaveHeader,
    level: u8,
    health: u8,
    checkpoint: u8,
    difficulty: u8,      // Added in V3
    playtime: u32,       // Added in V3
}

fn migrate_save(raw_bytes: &[u8]) -> Option<SaveV3> {
    if raw_bytes.len() < size_of::<SaveHeader>() {
        return None;
    }

    let header: SaveHeader = *bytemuck::from_bytes(&raw_bytes[..size_of::<SaveHeader>()]);

    match header.version {
        1 => {
            let v1: SaveV1 = *bytemuck::from_bytes(&raw_bytes[..size_of::<SaveV1>()]);
            Some(SaveV3 {
                header: SaveHeader { version: 3, ..v1.header },
                level: v1.level,
                health: v1.health,
                checkpoint: 0,     // Default
                difficulty: 1,     // Default: Normal
                playtime: 0,       // Unknown
            })
        }
        2 => {
            let v2: SaveV2 = *bytemuck::from_bytes(&raw_bytes[..size_of::<SaveV2>()]);
            Some(SaveV3 {
                header: SaveHeader { version: 3, ..v2.header },
                level: v2.level,
                health: v2.health,
                checkpoint: v2.checkpoint,
                difficulty: 1,     // Default
                playtime: 0,       // Unknown
            })
        }
        3 => {
            Some(*bytemuck::from_bytes(&raw_bytes[..size_of::<SaveV3>()]))
        }
        _ => None,  // Unknown version
    }
}
```

### Forward Compatibility Strategy

Reserve space for future fields:

```rust
#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct FutureProofSave {
    header: SaveHeader,
    // Current fields
    level: u8,
    health: u8,
    checkpoint: u8,
    difficulty: u8,
    // Reserved for future use
    reserved: [u8; 64],
    // Extensible arrays
    items: [u8; 32],       // Item IDs, 0xFF = empty
    unlocks: [u8; 16],     // Bitflags for unlocks
}
```

## Complex Data Patterns

### Variable-Length Arrays

Use fixed arrays with count:

```rust
const MAX_ITEMS: usize = 32;
const EMPTY_ITEM: u8 = 0xFF;

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct Inventory {
    count: u8,
    _pad: [u8; 3],
    items: [u8; MAX_ITEMS],
}

impl Inventory {
    fn new() -> Self {
        Self {
            count: 0,
            _pad: [0; 3],
            items: [EMPTY_ITEM; MAX_ITEMS],
        }
    }

    fn add(&mut self, item: u8) -> bool {
        if (self.count as usize) >= MAX_ITEMS { return false; }
        self.items[self.count as usize] = item;
        self.count += 1;
        true
    }

    fn iter(&self) -> impl Iterator<Item = u8> + '_ {
        self.items[..self.count as usize].iter().copied()
    }
}
```

### Bitflags for Boolean Sets

```rust
#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct UnlockFlags {
    // Each bit = one unlock (supports 256 unlocks)
    flags: [u8; 32],
}

impl UnlockFlags {
    fn set(&mut self, id: u8) {
        let byte = (id / 8) as usize;
        let bit = id % 8;
        self.flags[byte] |= 1 << bit;
    }

    fn get(&self, id: u8) -> bool {
        let byte = (id / 8) as usize;
        let bit = id % 8;
        (self.flags[byte] & (1 << bit)) != 0
    }

    fn clear(&mut self, id: u8) {
        let byte = (id / 8) as usize;
        let bit = id % 8;
        self.flags[byte] &= !(1 << bit);
    }
}
```

### High Score Table

```rust
const MAX_SCORES: usize = 10;
const NAME_LEN: usize = 3;

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct HighScoreEntry {
    score: u32,
    name: [u8; NAME_LEN],
    level: u8,
}

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct HighScoreTable {
    count: u8,
    _pad: [u8; 3],
    entries: [HighScoreEntry; MAX_SCORES],
}

impl HighScoreTable {
    fn insert(&mut self, score: u32, name: [u8; 3], level: u8) -> Option<u8> {
        // Find insertion position
        let mut pos = self.count as usize;
        for i in 0..self.count as usize {
            if score > self.entries[i].score {
                pos = i;
                break;
            }
        }

        if pos >= MAX_SCORES { return None; }

        // Shift entries down
        for i in (pos..MAX_SCORES - 1).rev() {
            self.entries[i + 1] = self.entries[i];
        }

        // Insert new entry
        self.entries[pos] = HighScoreEntry { score, name, level };
        if (self.count as usize) < MAX_SCORES {
            self.count += 1;
        }

        Some(pos as u8)
    }

    fn qualifies(&self, score: u32) -> bool {
        (self.count as usize) < MAX_SCORES || score > self.entries[MAX_SCORES - 1].score
    }
}
```

### Settings with Defaults

```rust
const SETTINGS_MAGIC: u32 = 0x5A584346;  // "ZXCF" (config)

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct GameSettings {
    magic: u32,
    version: u32,
    // Audio
    master_volume: u8,    // 0-100
    music_volume: u8,     // 0-100
    sfx_volume: u8,       // 0-100
    // Display
    screen_shake: u8,     // 0 = off, 1 = on
    show_timer: u8,
    show_damage: u8,
    // Controls
    control_scheme: u8,   // 0 = default, 1-3 = presets
    vibration: u8,
    // Reserved
    reserved: [u8; 24],
}

impl Default for GameSettings {
    fn default() -> Self {
        Self {
            magic: SETTINGS_MAGIC,
            version: 1,
            master_volume: 80,
            music_volume: 70,
            sfx_volume: 100,
            screen_shake: 1,
            show_timer: 1,
            show_damage: 1,
            control_scheme: 0,
            vibration: 1,
            reserved: [0; 24],
        }
    }
}

fn load_or_default_settings() -> GameSettings {
    let mut buf = [0u8; size_of::<GameSettings>()];
    let read = unsafe { load(6, buf.as_mut_ptr(), buf.len() as u32) };

    if read == 0 {
        return GameSettings::default();
    }

    let settings: GameSettings = *bytemuck::from_bytes(&buf);
    if settings.magic != SETTINGS_MAGIC {
        return GameSettings::default();
    }

    settings
}
```

## Complete Save/Load Example

Full implementation with all patterns combined:

```rust
use bytemuck::{Pod, Zeroable, bytes_of, bytes_of_mut, from_bytes};

const SAVE_MAGIC: u32 = 0x5A585356;
const SAVE_VERSION: u32 = 1;
const MAX_SIZE: usize = 65536;

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct SaveHeader {
    magic: u32,
    version: u32,
    checksum: u32,
    timestamp: u32,  // Frames since game start
}

#[repr(C)]
#[derive(Copy, Clone, Pod, Zeroable)]
struct GameSave {
    header: SaveHeader,
    // Progress
    level: u8,
    checkpoint: u8,
    difficulty: u8,
    _pad1: u8,
    // Player state
    health: u16,
    max_health: u16,
    lives: u8,
    _pad2: [u8; 3],
    // Inventory
    inventory: Inventory,
    // Unlocks
    unlocks: UnlockFlags,
    // Stats
    playtime_frames: u32,
    enemies_defeated: u32,
    deaths: u16,
    secrets_found: u8,
    _pad3: u8,
}

static mut CURRENT_SLOT: u32 = 0;
static mut PENDING_SAVE: bool = false;

fn save_game(slot: u32, game: &GameState) -> Result<(), &'static str> {
    if slot > 7 { return Err("Invalid slot"); }

    let mut save = GameSave::zeroed();
    save.header.magic = SAVE_MAGIC;
    save.header.version = SAVE_VERSION;
    save.header.timestamp = unsafe { tick_count() };

    // Copy game state
    save.level = game.level;
    save.checkpoint = game.checkpoint;
    save.difficulty = game.difficulty;
    save.health = game.player.health;
    save.max_health = game.player.max_health;
    save.lives = game.lives;
    save.inventory = game.inventory;
    save.unlocks = game.unlocks;
    save.playtime_frames = game.playtime;
    save.enemies_defeated = game.stats.enemies;
    save.deaths = game.stats.deaths;
    save.secrets_found = game.stats.secrets;

    // Calculate checksum
    create_save_with_checksum(&mut save);

    let bytes = bytes_of(&save);
    match unsafe { save(slot, bytes.as_ptr(), bytes.len() as u32) } {
        0 => Ok(()),
        1 => Err("Invalid slot"),
        2 => Err("Data too large"),
        _ => Err("Unknown error"),
    }
}

fn load_game(slot: u32) -> Result<GameSave, &'static str> {
    if slot > 7 { return Err("Invalid slot"); }

    let mut save = GameSave::zeroed();
    let bytes = bytes_of_mut(&mut save);
    let read = unsafe { load(slot, bytes.as_mut_ptr(), bytes.len() as u32) };

    if read == 0 { return Err("Empty slot"); }
    if save.header.magic != SAVE_MAGIC { return Err("Invalid save"); }
    if !verify_checksum(&save) { return Err("Corrupted save"); }

    Ok(save)
}

#[no_mangle]
pub extern "C" fn render() {
    unsafe {
        if PENDING_SAVE {
            PENDING_SAVE = false;
            let _ = save_game(CURRENT_SLOT, &GAME);
        }
    }
    // ... render
}
```

## Size Budget Planning

With 64KB per slot, plan data carefully:

| Data Type | Size | Example Usage |
|-----------|------|---------------|
| Header | 16 bytes | Magic, version, checksum |
| Player stats | 32 bytes | Health, lives, position |
| Inventory | 128 bytes | 32 items × 4 bytes each |
| World state | 1 KB | 256 entities × 4 bytes |
| Unlocks | 128 bytes | 1024 unlock flags |
| High scores | 120 bytes | 10 entries × 12 bytes |
| Settings | 64 bytes | All game options |
| Reserved | 2 KB | Future expansion |
| **Comfortable budget** | **~4 KB** | Leaves 60KB margin |

Keep saves small for fast load times and corruption resilience.
