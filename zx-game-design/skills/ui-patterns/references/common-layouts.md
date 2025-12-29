# Common UI Layouts

Extended patterns for HUD configurations, inventory grids, dialogue boxes, and specialized UI elements.

---

## HUD Configuration Templates

### Racing Game HUD

```rust
fn render_racing_hud(game: &RacingGame) {
    // Speedometer (bottom-right)
    render_speedometer(game.speed, 800.0, 420.0);

    // Lap counter (top-right)
    let lap_text = format!("LAP {}/{}", game.current_lap, game.total_laps);
    draw_text_str(&lap_text, 820.0, 20.0, 28.0, 0xFFFFFFFF);

    // Position (top-left)
    let pos_text = format!("{}ST", game.position);  // Handle 1st, 2nd, 3rd properly
    draw_text_str(&pos_text, 20.0, 20.0, 48.0, 0xFFFF00FF);

    // Minimap (bottom-left)
    render_track_minimap(game, 20.0, 380.0, 150.0, 150.0);

    // Boost meter
    render_boost_bar(game.boost, game.max_boost, 400.0, 500.0);
}

fn render_speedometer(speed: f32, x: f32, y: f32) {
    let radius = 60.0;

    // Background arc
    draw_circle_outline(x, y, radius, 8.0, 0x333333FF);

    // Speed text
    let speed_text = format!("{:.0}", speed);
    draw_text_str(&speed_text, x - 30.0, y - 15.0, 36.0, 0xFFFFFFFF);
    draw_text_str("km/h", x - 20.0, y + 20.0, 16.0, 0xAAAAAAFF);

    // Needle (rotate based on speed)
    let max_speed = 200.0;
    let angle = -135.0 + (speed / max_speed * 270.0);
    let rad = angle * 3.14159 / 180.0;
    let needle_len = radius - 10.0;
    draw_line(
        x, y,
        x + needle_len * rad.cos(),
        y + needle_len * rad.sin(),
        3.0, 0xFF0000FF
    );
}
```

### Fighting Game HUD

```rust
fn render_fighting_hud(p1: &Fighter, p2: &Fighter, timer: u32) {
    // Player 1 health (left side)
    render_fighting_health_bar(p1.health, p1.max_health, 50.0, 40.0, true);
    draw_text_str(p1.name, 50.0, 70.0, 24.0, 0xFFFFFFFF);

    // Player 2 health (right side, reversed)
    render_fighting_health_bar(p2.health, p2.max_health, 510.0, 40.0, false);
    draw_text_str(p2.name, 750.0, 70.0, 24.0, 0xFFFFFFFF);

    // Timer (center)
    let timer_text = format!("{:02}", timer);
    draw_text_str(&timer_text, 450.0, 30.0, 48.0, 0xFFFF00FF);

    // Super meters (bottom)
    render_super_meter(p1.super_meter, 50.0, 480.0, true);
    render_super_meter(p2.super_meter, 510.0, 480.0, false);

    // Win rounds
    render_round_indicators(p1.wins, 200.0, 15.0);
    render_round_indicators(p2.wins, 700.0, 15.0);
}

fn render_fighting_health_bar(health: i32, max: i32, x: f32, y: f32, left_align: bool) {
    let width = 400.0;
    let height = 25.0;
    let fill = (health as f32 / max as f32).clamp(0.0, 1.0);

    // Background
    draw_rect(x, y, width, height, 0x440000FF);

    // Health fill (from left or right based on alignment)
    if left_align {
        draw_rect(x, y, width * fill, height, 0x00AA00FF);
    } else {
        let fill_x = x + width * (1.0 - fill);
        draw_rect(fill_x, y, width * fill, height, 0x00AA00FF);
    }

    // Border
    draw_rect(x - 2.0, y - 2.0, width + 4.0, height + 4.0, 0xFFFFFF33);
}

fn render_round_indicators(wins: u8, x: f32, y: f32) {
    for i in 0..3 {
        let color = if i < wins { 0xFFFF00FF } else { 0x333333FF };
        draw_circle(x + i as f32 * 20.0, y, 6.0, color);
    }
}
```

### RPG HUD

```rust
fn render_rpg_hud(player: &RPGPlayer) {
    // Character portrait (top-left)
    draw_sprite(player.portrait_texture, 10.0, 10.0, 64.0, 64.0);

    // HP/MP bars next to portrait
    draw_text_str("HP", 80.0, 15.0, 14.0, 0xFF6666FF);
    render_thin_bar(player.hp, player.max_hp, 100.0, 15.0, 150.0, 0x00CC00FF);

    draw_text_str("MP", 80.0, 40.0, 14.0, 0x6666FFFF);
    render_thin_bar(player.mp, player.max_mp, 100.0, 40.0, 150.0, 0x0066FFFF);

    // Experience bar (bottom of screen)
    let exp_ratio = player.exp as f32 / player.exp_to_next as f32;
    draw_rect(0.0, 530.0, 960.0, 10.0, 0x222222FF);
    draw_rect(0.0, 530.0, 960.0 * exp_ratio, 10.0, 0x9900FFFF);

    // Gold (top-right)
    let gold_text = format!("${}", player.gold);
    draw_text_str(&gold_text, 850.0, 15.0, 20.0, 0xFFCC00FF);

    // Minimap (corner)
    render_minimap(player.map_x, player.map_y, 800.0, 380.0, 150.0, 150.0);
}

fn render_thin_bar(current: i32, max: i32, x: f32, y: f32, w: f32, fill_color: u32) {
    let ratio = (current as f32 / max as f32).clamp(0.0, 1.0);
    draw_rect(x, y, w, 12.0, 0x333333FF);
    draw_rect(x, y, w * ratio, 12.0, fill_color);

    let text = format!("{}/{}", current, max);
    draw_text_str(&text, x + w + 5.0, y, 12.0, 0xFFFFFFFF);
}
```

---

## Inventory Grid System

### Basic Grid Inventory

```rust
const SLOT_SIZE: f32 = 48.0;
const SLOT_PADDING: f32 = 4.0;
const INVENTORY_COLS: usize = 8;
const INVENTORY_ROWS: usize = 4;

struct Inventory {
    items: [Option<Item>; INVENTORY_COLS * INVENTORY_ROWS],
    cursor_x: u8,
    cursor_y: u8,
}

impl Inventory {
    fn update(&mut self) {
        if button_pressed(0, button::LEFT) && self.cursor_x > 0 {
            self.cursor_x -= 1;
        }
        if button_pressed(0, button::RIGHT) && (self.cursor_x as usize) < INVENTORY_COLS - 1 {
            self.cursor_x += 1;
        }
        if button_pressed(0, button::UP) && self.cursor_y > 0 {
            self.cursor_y -= 1;
        }
        if button_pressed(0, button::DOWN) && (self.cursor_y as usize) < INVENTORY_ROWS - 1 {
            self.cursor_y += 1;
        }
    }

    fn render(&self, base_x: f32, base_y: f32) {
        // Background panel
        let panel_w = INVENTORY_COLS as f32 * (SLOT_SIZE + SLOT_PADDING) + SLOT_PADDING;
        let panel_h = INVENTORY_ROWS as f32 * (SLOT_SIZE + SLOT_PADDING) + SLOT_PADDING;
        draw_rect(base_x - 10.0, base_y - 10.0, panel_w + 20.0, panel_h + 20.0, 0x222244EE);

        for row in 0..INVENTORY_ROWS {
            for col in 0..INVENTORY_COLS {
                let x = base_x + col as f32 * (SLOT_SIZE + SLOT_PADDING);
                let y = base_y + row as f32 * (SLOT_SIZE + SLOT_PADDING);
                let idx = row * INVENTORY_COLS + col;
                let is_selected = col == self.cursor_x as usize && row == self.cursor_y as usize;

                // Slot background
                let bg_color = if is_selected { 0x4444AAFF } else { 0x333355FF };
                draw_rect(x, y, SLOT_SIZE, SLOT_SIZE, bg_color);

                // Item icon if present
                if let Some(item) = &self.items[idx] {
                    draw_sprite(item.icon_texture, x + 4.0, y + 4.0, 40.0, 40.0);

                    // Stack count
                    if item.count > 1 {
                        let count_text = format!("{}", item.count);
                        draw_text_str(&count_text, x + 34.0, y + 32.0, 14.0, 0xFFFFFFFF);
                    }
                }

                // Selection highlight
                if is_selected {
                    draw_line(x, y, x + SLOT_SIZE, y, 2.0, 0xFFFF00FF);
                    draw_line(x, y + SLOT_SIZE, x + SLOT_SIZE, y + SLOT_SIZE, 2.0, 0xFFFF00FF);
                    draw_line(x, y, x, y + SLOT_SIZE, 2.0, 0xFFFF00FF);
                    draw_line(x + SLOT_SIZE, y, x + SLOT_SIZE, y + SLOT_SIZE, 2.0, 0xFFFF00FF);
                }
            }
        }

        // Item description for selected slot
        let selected_idx = self.cursor_y as usize * INVENTORY_COLS + self.cursor_x as usize;
        if let Some(item) = &self.items[selected_idx] {
            let desc_y = base_y + panel_h + 20.0;
            draw_text_str(item.name, base_x, desc_y, 20.0, 0xFFFFFFFF);
            draw_text_str(item.description, base_x, desc_y + 25.0, 14.0, 0xAAAAAAFF);
        }
    }
}
```

### Equipment Slots

```rust
struct Equipment {
    weapon: Option<Item>,
    armor: Option<Item>,
    accessory: Option<Item>,
    selected: u8,
}

impl Equipment {
    fn render(&self, x: f32, y: f32) {
        let slots = [
            ("Weapon", &self.weapon),
            ("Armor", &self.armor),
            ("Accessory", &self.accessory),
        ];

        for (i, (label, item)) in slots.iter().enumerate() {
            let slot_y = y + i as f32 * 70.0;
            let is_selected = i == self.selected as usize;

            // Label
            draw_text_str(label, x, slot_y, 16.0, 0xAAAAAAFF);

            // Slot box
            let bg = if is_selected { 0x4444AAFF } else { 0x333355FF };
            draw_rect(x, slot_y + 20.0, 60.0, 40.0, bg);

            // Item or empty indicator
            if let Some(item) = item {
                draw_sprite(item.icon_texture, x + 10.0, slot_y + 24.0, 32.0, 32.0);
                draw_text_str(item.name, x + 70.0, slot_y + 30.0, 16.0, 0xFFFFFFFF);
            } else {
                draw_text_str("-", x + 25.0, slot_y + 30.0, 20.0, 0x666666FF);
            }

            if is_selected {
                // Selection border
                draw_line(x - 2.0, slot_y + 18.0, x + 62.0, slot_y + 18.0, 2.0, 0xFFFF00FF);
                draw_line(x - 2.0, slot_y + 62.0, x + 62.0, slot_y + 62.0, 2.0, 0xFFFF00FF);
            }
        }
    }
}
```

---

## Dialogue Box System

### Dialogue Box with Portrait

```rust
struct DialogueBox {
    speaker_name: &'static str,
    text: &'static str,
    portrait_texture: u32,
    chars_shown: u32,
    finished: bool,
}

impl DialogueBox {
    const CHARS_PER_FRAME: u32 = 2;
    const BOX_X: f32 = 50.0;
    const BOX_Y: f32 = 380.0;
    const BOX_W: f32 = 860.0;
    const BOX_H: f32 = 140.0;
    const PORTRAIT_SIZE: f32 = 100.0;

    fn update(&mut self) {
        if !self.finished {
            self.chars_shown += Self::CHARS_PER_FRAME;
            if self.chars_shown >= self.text.len() as u32 {
                self.chars_shown = self.text.len() as u32;
                self.finished = true;
            }
        }

        // Skip on A press
        if button_pressed(0, button::A) {
            if !self.finished {
                self.chars_shown = self.text.len() as u32;
                self.finished = true;
            }
            // else: advance to next dialogue (handle externally)
        }
    }

    fn render(&self) {
        // Box background
        draw_rect(Self::BOX_X, Self::BOX_Y, Self::BOX_W, Self::BOX_H, 0x000000DD);

        // Border
        draw_line(Self::BOX_X, Self::BOX_Y, Self::BOX_X + Self::BOX_W, Self::BOX_Y, 2.0, 0xFFFFFFFF);
        draw_line(Self::BOX_X, Self::BOX_Y + Self::BOX_H, Self::BOX_X + Self::BOX_W, Self::BOX_Y + Self::BOX_H, 2.0, 0xFFFFFFFF);
        draw_line(Self::BOX_X, Self::BOX_Y, Self::BOX_X, Self::BOX_Y + Self::BOX_H, 2.0, 0xFFFFFFFF);
        draw_line(Self::BOX_X + Self::BOX_W, Self::BOX_Y, Self::BOX_X + Self::BOX_W, Self::BOX_Y + Self::BOX_H, 2.0, 0xFFFFFFFF);

        // Portrait
        draw_sprite(self.portrait_texture, Self::BOX_X + 10.0, Self::BOX_Y + 20.0, Self::PORTRAIT_SIZE, Self::PORTRAIT_SIZE);

        // Speaker name
        draw_text_str(self.speaker_name, Self::BOX_X + 130.0, Self::BOX_Y + 15.0, 22.0, 0xFFFF00FF);

        // Dialogue text (typewriter effect)
        let visible = &self.text[..self.chars_shown as usize];
        draw_text_str(visible, Self::BOX_X + 130.0, Self::BOX_Y + 50.0, 18.0, 0xFFFFFFFF);

        // Continue indicator
        if self.finished {
            let blink = (tick_count() / 20) % 2 == 0;
            if blink {
                draw_text_str("▼", Self::BOX_X + Self::BOX_W - 40.0, Self::BOX_Y + Self::BOX_H - 30.0, 20.0, 0xFFFFFFFF);
            }
        }
    }
}
```

### Choice System

```rust
struct ChoiceDialogue {
    prompt: &'static str,
    choices: &'static [&'static str],
    selected: u8,
}

impl ChoiceDialogue {
    fn update(&mut self) -> Option<u8> {
        if button_pressed(0, button::UP) && self.selected > 0 {
            self.selected -= 1;
        }
        if button_pressed(0, button::DOWN) && (self.selected as usize) < self.choices.len() - 1 {
            self.selected += 1;
        }

        if button_pressed(0, button::A) {
            return Some(self.selected);
        }
        None
    }

    fn render(&self) {
        let box_x = 200.0;
        let box_y = 200.0;
        let box_w = 560.0;
        let box_h = 50.0 + self.choices.len() as f32 * 35.0;

        // Background
        draw_rect(box_x, box_y, box_w, box_h, 0x000000EE);

        // Prompt
        draw_text_str(self.prompt, box_x + 20.0, box_y + 15.0, 20.0, 0xFFFFFFFF);

        // Choices
        for (i, choice) in self.choices.iter().enumerate() {
            let y = box_y + 50.0 + i as f32 * 35.0;
            let is_selected = i == self.selected as usize;

            if is_selected {
                draw_text_str(">", box_x + 20.0, y, 20.0, 0xFFFF00FF);
                draw_text_str(choice, box_x + 45.0, y, 20.0, 0xFFFF00FF);
            } else {
                draw_text_str(choice, box_x + 45.0, y, 20.0, 0xCCCCCCFF);
            }
        }
    }
}
```

---

## Minimap Patterns

### Top-Down Minimap

```rust
fn render_minimap(
    player_x: f32, player_y: f32,
    map_x: f32, map_y: f32,
    map_w: f32, map_h: f32,
    world_width: f32, world_height: f32,
    entities: &[Entity],
) {
    // Background
    draw_rect(map_x, map_y, map_w, map_h, 0x111122DD);

    // Border
    draw_line(map_x, map_y, map_x + map_w, map_y, 1.0, 0x444444FF);
    draw_line(map_x, map_y + map_h, map_x + map_w, map_y + map_h, 1.0, 0x444444FF);
    draw_line(map_x, map_y, map_x, map_y + map_h, 1.0, 0x444444FF);
    draw_line(map_x + map_w, map_y, map_x + map_w, map_y + map_h, 1.0, 0x444444FF);

    // Scale factor
    let scale_x = map_w / world_width;
    let scale_y = map_h / world_height;

    // Entities
    for entity in entities {
        let dot_x = map_x + entity.x * scale_x;
        let dot_y = map_y + entity.y * scale_y;
        let color = match entity.entity_type {
            EntityType::Enemy => 0xFF0000FF,
            EntityType::Item => 0x00FF00FF,
            EntityType::NPC => 0x00FFFFFF,
            _ => 0x888888FF,
        };
        draw_circle(dot_x, dot_y, 3.0, color);
    }

    // Player (always on top)
    let px = map_x + player_x * scale_x;
    let py = map_y + player_y * scale_y;
    draw_circle(px, py, 4.0, 0xFFFF00FF);
}
```

---

## Notification System

### Toast Notifications

```rust
struct Toast {
    message: String,
    remaining_ticks: u32,
    toast_type: ToastType,
}

enum ToastType {
    Info,
    Success,
    Warning,
    Error,
}

struct ToastManager {
    toasts: Vec<Toast>,
}

impl ToastManager {
    fn show(&mut self, message: &str, toast_type: ToastType, duration_ticks: u32) {
        self.toasts.push(Toast {
            message: message.to_string(),
            remaining_ticks: duration_ticks,
            toast_type,
        });
    }

    fn update(&mut self) {
        self.toasts.retain_mut(|toast| {
            toast.remaining_ticks = toast.remaining_ticks.saturating_sub(1);
            toast.remaining_ticks > 0
        });
    }

    fn render(&self) {
        let base_y = 50.0;
        for (i, toast) in self.toasts.iter().enumerate() {
            let y = base_y + i as f32 * 45.0;

            // Fade out in last 30 frames
            let alpha = if toast.remaining_ticks < 30 {
                (toast.remaining_ticks as f32 / 30.0 * 255.0) as u32
            } else {
                255
            };

            let bg_color = match toast.toast_type {
                ToastType::Info => 0x334488,
                ToastType::Success => 0x228822,
                ToastType::Warning => 0x886622,
                ToastType::Error => 0x882222,
            } << 8 | alpha;

            draw_rect(700.0, y, 250.0, 35.0, bg_color);
            draw_text_str(&toast.message, 710.0, y + 8.0, 16.0, 0xFFFFFF00 | alpha);
        }
    }
}
```

---

## Modal Dialog

### Confirmation Dialog

```rust
struct ConfirmDialog {
    title: &'static str,
    message: &'static str,
    selected: bool,  // true = Yes, false = No
}

impl ConfirmDialog {
    fn update(&mut self) -> Option<bool> {
        if button_pressed(0, button::LEFT) || button_pressed(0, button::RIGHT) {
            self.selected = !self.selected;
        }

        if button_pressed(0, button::A) {
            return Some(self.selected);
        }
        if button_pressed(0, button::B) {
            return Some(false);  // Cancel always means No
        }

        None
    }

    fn render(&self) {
        // Dim background
        draw_rect(0.0, 0.0, 960.0, 540.0, 0x00000088);

        // Dialog box
        let box_x = 280.0;
        let box_y = 180.0;
        let box_w = 400.0;
        let box_h = 180.0;

        draw_rect(box_x, box_y, box_w, box_h, 0x222244FF);

        // Title
        draw_text_str(self.title, box_x + 20.0, box_y + 20.0, 28.0, 0xFFFFFFFF);

        // Message
        draw_text_str(self.message, box_x + 20.0, box_y + 70.0, 18.0, 0xCCCCCCFF);

        // Buttons
        let yes_color = if self.selected { 0x00AA00FF } else { 0x444444FF };
        let no_color = if !self.selected { 0xAA0000FF } else { 0x444444FF };

        draw_rect(box_x + 80.0, box_y + 120.0, 100.0, 40.0, yes_color);
        draw_text_str("Yes", box_x + 110.0, box_y + 130.0, 22.0, 0xFFFFFFFF);

        draw_rect(box_x + 220.0, box_y + 120.0, 100.0, 40.0, no_color);
        draw_text_str("No", box_x + 255.0, box_y + 130.0, 22.0, 0xFFFFFFFF);
    }
}
```
