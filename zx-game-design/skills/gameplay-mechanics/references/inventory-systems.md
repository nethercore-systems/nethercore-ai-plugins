# Inventory Systems Reference

Rollback-safe item and inventory implementations for Nethercore ZX RPGs, action games, and adventures.

## Simple Item Pickup

Basic pickup with collision detection.

```rust
use crate::ffi::*;

const PICKUP_RADIUS: f32 = 20.0;
const ITEM_BOBBLE_SPEED: f32 = 0.1;
const ITEM_BOBBLE_HEIGHT: f32 = 4.0;

#[derive(Clone, Copy, PartialEq)]
#[repr(u8)]
enum ItemType {
    None = 0,
    HealthPotion = 1,
    ManaPotion = 2,
    Key = 3,
    Coin = 4,
    Sword = 5,
    Shield = 6,
}

struct WorldItem {
    x: f32,
    y: f32,
    item_type: ItemType,
    active: bool,
    spawn_tick: u64,  // For bobble animation phase
}

impl WorldItem {
    fn update_visual(&self) -> f32 {
        // Bobbing animation using tick count
        let phase = (tick_count() - self.spawn_tick) as f32 * ITEM_BOBBLE_SPEED;
        phase.sin() * ITEM_BOBBLE_HEIGHT
    }

    fn check_pickup(&mut self, player_x: f32, player_y: f32) -> Option<ItemType> {
        if !self.active {
            return None;
        }

        let dx = player_x - self.x;
        let dy = player_y - self.y;
        let dist_sq = dx * dx + dy * dy;

        if dist_sq < PICKUP_RADIUS * PICKUP_RADIUS {
            self.active = false;
            Some(self.item_type)
        } else {
            None
        }
    }
}
```

### Magnetic Item Attraction

Items move toward player when close:

```rust
const ATTRACT_RADIUS: f32 = 60.0;
const ATTRACT_SPEED: f32 = 3.0;

fn update_item_attraction(item: &mut WorldItem, player_x: f32, player_y: f32) {
    if !item.active {
        return;
    }

    let dx = player_x - item.x;
    let dy = player_y - item.y;
    let dist_sq = dx * dx + dy * dy;

    if dist_sq < ATTRACT_RADIUS * ATTRACT_RADIUS && dist_sq > PICKUP_RADIUS * PICKUP_RADIUS {
        let dist = dist_sq.sqrt();
        // Move toward player, faster when closer
        let speed = ATTRACT_SPEED * (1.0 - dist / ATTRACT_RADIUS);
        item.x += (dx / dist) * speed;
        item.y += (dy / dist) * speed;
    }
}
```

---

## Fixed-Slot Inventory

Simple array-based inventory with fixed capacity.

```rust
const INVENTORY_SIZE: usize = 12;
const EMPTY_SLOT: u8 = 0xFF;

#[derive(Clone, Copy)]
struct Inventory {
    slots: [u8; INVENTORY_SIZE],
    selected: u8,
}

impl Inventory {
    fn new() -> Self {
        Self {
            slots: [EMPTY_SLOT; INVENTORY_SIZE],
            selected: 0,
        }
    }

    /// Try to add an item. Returns true if successful.
    fn add_item(&mut self, item_type: ItemType) -> bool {
        for slot in &mut self.slots {
            if *slot == EMPTY_SLOT {
                *slot = item_type as u8;
                return true;
            }
        }
        false  // Inventory full
    }

    /// Remove item from specific slot.
    fn remove_at(&mut self, index: usize) -> Option<ItemType> {
        if index >= INVENTORY_SIZE {
            return None;
        }

        let item = self.slots[index];
        if item != EMPTY_SLOT {
            self.slots[index] = EMPTY_SLOT;
            Some(unsafe { core::mem::transmute(item) })
        } else {
            None
        }
    }

    /// Get currently selected item.
    fn get_selected(&self) -> Option<ItemType> {
        let item = self.slots[self.selected as usize];
        if item != EMPTY_SLOT {
            Some(unsafe { core::mem::transmute(item) })
        } else {
            None
        }
    }

    /// Use the selected item.
    fn use_selected(&mut self) -> Option<ItemType> {
        self.remove_at(self.selected as usize)
    }

    /// Move selection with input.
    fn update_selection(&mut self) {
        if button_pressed(0, button::L1) && self.selected > 0 {
            self.selected -= 1;
        }
        if button_pressed(0, button::R1) && (self.selected as usize) < INVENTORY_SIZE - 1 {
            self.selected += 1;
        }
    }

    /// Count items of a specific type.
    fn count(&self, item_type: ItemType) -> u8 {
        let target = item_type as u8;
        self.slots.iter().filter(|&&s| s == target).count() as u8
    }

    /// Check if inventory has space.
    fn has_space(&self) -> bool {
        self.slots.iter().any(|&s| s == EMPTY_SLOT)
    }

    /// Get number of filled slots.
    fn item_count(&self) -> u8 {
        self.slots.iter().filter(|&&s| s != EMPTY_SLOT).count() as u8
    }
}
```

### Inventory UI Rendering

```rust
const SLOT_SIZE: f32 = 48.0;
const SLOT_PADDING: f32 = 4.0;
const INVENTORY_X: f32 = 200.0;
const INVENTORY_Y: f32 = 400.0;

fn render_inventory(inventory: &Inventory, item_texture: u32) {
    texture_bind(item_texture);

    for i in 0..INVENTORY_SIZE {
        let col = (i % 6) as f32;
        let row = (i / 6) as f32;
        let x = INVENTORY_X + col * (SLOT_SIZE + SLOT_PADDING);
        let y = INVENTORY_Y + row * (SLOT_SIZE + SLOT_PADDING);

        // Draw slot background
        let bg_color = if i == inventory.selected as usize {
            0xFFFF00AA  // Yellow highlight
        } else {
            0x333333AA  // Dark gray
        };
        draw_rect(x, y, SLOT_SIZE, SLOT_SIZE, bg_color);

        // Draw item sprite if slot is filled
        let item = inventory.slots[i];
        if item != EMPTY_SLOT {
            // Assume 8x8 item sprite sheet, item type = sprite index
            let sprite_col = (item % 8) as f32;
            let sprite_row = (item / 8) as f32;
            draw_sprite_region(
                x + 8.0, y + 8.0,  // Center in slot
                32.0, 32.0,        // Sprite size
                sprite_col / 8.0, sprite_row / 8.0,
                1.0 / 8.0, 1.0 / 8.0,
                0xFFFFFFFF
            );
        }
    }
}
```

---

## Stackable Items

Items that stack in the same slot (coins, potions, ammo).

```rust
const MAX_STACK: u8 = 99;

#[derive(Clone, Copy)]
struct StackSlot {
    item_type: u8,
    count: u8,
}

impl StackSlot {
    fn empty() -> Self {
        Self { item_type: EMPTY_SLOT, count: 0 }
    }

    fn is_empty(&self) -> bool {
        self.item_type == EMPTY_SLOT || self.count == 0
    }
}

struct StackInventory {
    slots: [StackSlot; INVENTORY_SIZE],
    selected: u8,
}

impl StackInventory {
    fn new() -> Self {
        Self {
            slots: [StackSlot::empty(); INVENTORY_SIZE],
            selected: 0,
        }
    }

    /// Add items, stacking where possible.
    fn add_item(&mut self, item_type: ItemType, mut amount: u8) -> u8 {
        let type_id = item_type as u8;

        // First, try to stack with existing items
        for slot in &mut self.slots {
            if slot.item_type == type_id && slot.count < MAX_STACK {
                let can_add = (MAX_STACK - slot.count).min(amount);
                slot.count += can_add;
                amount -= can_add;
                if amount == 0 {
                    return 0;  // All added
                }
            }
        }

        // Then, use empty slots
        for slot in &mut self.slots {
            if slot.is_empty() {
                let can_add = MAX_STACK.min(amount);
                slot.item_type = type_id;
                slot.count = can_add;
                amount -= can_add;
                if amount == 0 {
                    return 0;
                }
            }
        }

        amount  // Return leftover that couldn't be added
    }

    /// Remove items from inventory.
    fn remove_item(&mut self, item_type: ItemType, mut amount: u8) -> u8 {
        let type_id = item_type as u8;
        let mut removed = 0u8;

        for slot in &mut self.slots {
            if slot.item_type == type_id {
                let can_remove = slot.count.min(amount);
                slot.count -= can_remove;
                amount -= can_remove;
                removed += can_remove;

                if slot.count == 0 {
                    slot.item_type = EMPTY_SLOT;
                }

                if amount == 0 {
                    break;
                }
            }
        }

        removed
    }

    /// Count total of an item type across all slots.
    fn count(&self, item_type: ItemType) -> u16 {
        let type_id = item_type as u8;
        self.slots.iter()
            .filter(|s| s.item_type == type_id)
            .map(|s| s.count as u16)
            .sum()
    }
}
```

---

## Equipment System

Separate equipment slots from inventory.

```rust
#[derive(Clone, Copy, PartialEq)]
#[repr(u8)]
enum EquipSlot {
    Weapon = 0,
    Armor = 1,
    Accessory = 2,
    COUNT = 3,
}

#[derive(Clone, Copy, Default)]
struct EquipmentStats {
    attack: i16,
    defense: i16,
    speed: i16,
    special: i16,
}

#[derive(Clone, Copy)]
struct Equipment {
    slots: [u8; EquipSlot::COUNT as usize],
}

impl Equipment {
    fn new() -> Self {
        Self {
            slots: [EMPTY_SLOT; EquipSlot::COUNT as usize],
        }
    }

    /// Equip an item, returning the previously equipped item.
    fn equip(&mut self, slot: EquipSlot, item: ItemType) -> Option<ItemType> {
        let prev = self.slots[slot as usize];
        self.slots[slot as usize] = item as u8;

        if prev != EMPTY_SLOT {
            Some(unsafe { core::mem::transmute(prev) })
        } else {
            None
        }
    }

    /// Unequip and return item from slot.
    fn unequip(&mut self, slot: EquipSlot) -> Option<ItemType> {
        let item = self.slots[slot as usize];
        if item != EMPTY_SLOT {
            self.slots[slot as usize] = EMPTY_SLOT;
            Some(unsafe { core::mem::transmute(item) })
        } else {
            None
        }
    }

    /// Get equipped item in slot.
    fn get(&self, slot: EquipSlot) -> Option<ItemType> {
        let item = self.slots[slot as usize];
        if item != EMPTY_SLOT {
            Some(unsafe { core::mem::transmute(item) })
        } else {
            None
        }
    }

    /// Calculate total stats from all equipment.
    fn total_stats(&self, item_db: &ItemDatabase) -> EquipmentStats {
        let mut total = EquipmentStats::default();

        for &slot_item in &self.slots {
            if slot_item != EMPTY_SLOT {
                if let Some(stats) = item_db.get_stats(slot_item) {
                    total.attack += stats.attack;
                    total.defense += stats.defense;
                    total.speed += stats.speed;
                    total.special += stats.special;
                }
            }
        }

        total
    }
}
```

### Item Database

Static item definitions:

```rust
struct ItemDef {
    name: &'static str,
    item_type: ItemType,
    equip_slot: Option<EquipSlot>,
    stats: EquipmentStats,
    consumable: bool,
    stackable: bool,
    max_stack: u8,
}

struct ItemDatabase {
    items: &'static [ItemDef],
}

impl ItemDatabase {
    fn get_stats(&self, item_id: u8) -> Option<&EquipmentStats> {
        self.items.get(item_id as usize).map(|def| &def.stats)
    }

    fn is_stackable(&self, item_id: u8) -> bool {
        self.items.get(item_id as usize).map(|def| def.stackable).unwrap_or(false)
    }

    fn get_equip_slot(&self, item_id: u8) -> Option<EquipSlot> {
        self.items.get(item_id as usize).and_then(|def| def.equip_slot)
    }
}

// Example database
const ITEM_DB: &[ItemDef] = &[
    ItemDef {
        name: "Health Potion",
        item_type: ItemType::HealthPotion,
        equip_slot: None,
        stats: EquipmentStats::default(),
        consumable: true,
        stackable: true,
        max_stack: 99,
    },
    ItemDef {
        name: "Iron Sword",
        item_type: ItemType::Sword,
        equip_slot: Some(EquipSlot::Weapon),
        stats: EquipmentStats { attack: 10, defense: 0, speed: 0, special: 0 },
        consumable: false,
        stackable: false,
        max_stack: 1,
    },
    // ... more items
];
```

---

## Consumables with Cooldowns

Items that can be used with a cooldown period.

```rust
const MAX_CONSUMABLE_TYPES: usize = 8;

struct ConsumableCooldowns {
    cooldowns: [u32; MAX_CONSUMABLE_TYPES],
}

impl ConsumableCooldowns {
    fn new() -> Self {
        Self { cooldowns: [0; MAX_CONSUMABLE_TYPES] }
    }

    fn update(&mut self) {
        for cd in &mut self.cooldowns {
            if *cd > 0 {
                *cd -= 1;
            }
        }
    }

    fn can_use(&self, item_type: ItemType) -> bool {
        let idx = item_type as usize;
        if idx >= MAX_CONSUMABLE_TYPES {
            return true;
        }
        self.cooldowns[idx] == 0
    }

    fn start_cooldown(&mut self, item_type: ItemType, duration: u32) {
        let idx = item_type as usize;
        if idx < MAX_CONSUMABLE_TYPES {
            self.cooldowns[idx] = duration;
        }
    }

    fn get_cooldown(&self, item_type: ItemType) -> u32 {
        let idx = item_type as usize;
        if idx < MAX_CONSUMABLE_TYPES {
            self.cooldowns[idx]
        } else {
            0
        }
    }
}

// Usage
fn try_use_consumable(
    player: &mut Player,
    inventory: &mut Inventory,
    cooldowns: &mut ConsumableCooldowns,
) {
    if !button_pressed(0, button::X) {
        return;
    }

    if let Some(item) = inventory.get_selected() {
        if !cooldowns.can_use(item) {
            return;  // On cooldown
        }

        match item {
            ItemType::HealthPotion => {
                player.health = (player.health + 50).min(player.max_health);
                inventory.use_selected();
                cooldowns.start_cooldown(item, 60);  // 1 second cooldown
            }
            ItemType::ManaPotion => {
                player.mana = (player.mana + 30).min(player.max_mana);
                inventory.use_selected();
                cooldowns.start_cooldown(item, 60);
            }
            _ => {}
        }
    }
}
```

---

## Quick-Use Slots

Dedicated hotbar for fast item access.

```rust
const QUICKSLOT_COUNT: usize = 4;

struct QuickSlots {
    slots: [u8; QUICKSLOT_COUNT],  // Item type in each slot
}

impl QuickSlots {
    fn new() -> Self {
        Self { slots: [EMPTY_SLOT; QUICKSLOT_COUNT] }
    }

    /// Assign item to quickslot.
    fn assign(&mut self, slot: usize, item_type: ItemType) {
        if slot < QUICKSLOT_COUNT {
            self.slots[slot] = item_type as u8;
        }
    }

    /// Get item in quickslot.
    fn get(&self, slot: usize) -> Option<ItemType> {
        if slot >= QUICKSLOT_COUNT {
            return None;
        }
        let item = self.slots[slot];
        if item != EMPTY_SLOT {
            Some(unsafe { core::mem::transmute(item) })
        } else {
            None
        }
    }

    /// Clear a quickslot.
    fn clear(&mut self, slot: usize) {
        if slot < QUICKSLOT_COUNT {
            self.slots[slot] = EMPTY_SLOT;
        }
    }
}

fn update_quickslots(
    quickslots: &QuickSlots,
    inventory: &mut StackInventory,
    player: &mut Player,
    cooldowns: &mut ConsumableCooldowns,
) {
    // D-pad for quickslots
    let slot = if button_pressed(0, button::UP) { Some(0) }
              else if button_pressed(0, button::RIGHT) { Some(1) }
              else if button_pressed(0, button::DOWN) { Some(2) }
              else if button_pressed(0, button::LEFT) { Some(3) }
              else { None };

    if let Some(slot_idx) = slot {
        if let Some(item_type) = quickslots.get(slot_idx) {
            // Check if we have the item and can use it
            if inventory.count(item_type) > 0 && cooldowns.can_use(item_type) {
                // Use the item
                apply_item_effect(player, item_type);
                inventory.remove_item(item_type, 1);
                cooldowns.start_cooldown(item_type, get_cooldown_duration(item_type));
            }
        }
    }
}
```

---

## Complete Player Inventory System

Combining all systems:

```rust
struct PlayerInventory {
    items: StackInventory,
    equipment: Equipment,
    quickslots: QuickSlots,
    cooldowns: ConsumableCooldowns,
    gold: u32,
}

impl PlayerInventory {
    fn new() -> Self {
        Self {
            items: StackInventory::new(),
            equipment: Equipment::new(),
            quickslots: QuickSlots::new(),
            cooldowns: ConsumableCooldowns::new(),
            gold: 0,
        }
    }

    fn update(&mut self, player: &mut Player) {
        // Update cooldowns
        self.cooldowns.update();

        // Handle quickslot usage
        update_quickslots(&self.quickslots, &mut self.items, player, &mut self.cooldowns);
    }

    fn pickup(&mut self, item_type: ItemType, amount: u8) -> bool {
        match item_type {
            ItemType::Coin => {
                self.gold += amount as u32;
                true
            }
            _ => {
                self.items.add_item(item_type, amount) == 0
            }
        }
    }

    fn get_total_stats(&self, db: &ItemDatabase) -> EquipmentStats {
        self.equipment.total_stats(db)
    }
}
```
