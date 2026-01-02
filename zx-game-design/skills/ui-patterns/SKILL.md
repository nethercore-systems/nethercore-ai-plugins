---
name: UI/UX Patterns for ZX
description: |
  Use this skill for game UI: "menu", "HUD", "UI", "pause menu", "title screen", "health bar", "score display", "button navigation", "focus states", "rom_font".

  **Load references when:**
  - Standard layouts, inventory grids → `references/common-layouts.md`
version: 1.1.0
---

# UI/UX Patterns for Nethercore ZX

ZX provides 2D drawing primitives. Games implement their own UI systems.

## 2D Drawing FFI

| Function | Purpose |
|----------|---------|
| `draw_rect(x, y, w, h, color)` | Filled rectangle |
| `draw_text_str(text, x, y, size, color)` | Text with current font |
| `draw_line(x1, y1, x2, y2, thick, color)` | Line segment |
| `draw_circle(x, y, radius, color)` | Filled circle |
| `rom_font_str(id)` | Bind ROM font |

**Color:** `0xRRGGBBAA` | **Screen:** 960×540, origin top-left

---

## Menu State Machine

```rust
enum GameState { Title, Playing, Paused, GameOver }

fn update(game: &mut Game) {
    match game.state {
        GameState::Title => update_title_menu(game),
        GameState::Playing => update_gameplay(game),
        // ...
    }
}
```

### Navigation Pattern

```rust
fn update_menu(sel: &mut u8, max: u8) {
    if button_pressed(0, button::UP) && *sel > 0 { *sel -= 1; }
    if button_pressed(0, button::DOWN) && *sel < max - 1 { *sel += 1; }
}
```

### Rendering Menu Options

```rust
fn render_options(options: &[&str], selected: u8, base_y: f32) {
    for (i, opt) in options.iter().enumerate() {
        let color = if i == selected as usize { 0xFFFF00FF } else { 0xAAAAAAFF };
        draw_text_str(opt, 400.0, base_y + i as f32 * 50.0, 32.0, color);
    }
    // Selection indicator
    draw_text_str(">", 370.0, base_y + selected as f32 * 50.0, 32.0, 0xFFFF00FF);
}
```

---

## HUD Elements

### Health Bar

```rust
fn render_health_bar(current: i32, max: i32, x: f32, y: f32, w: f32, h: f32) {
    let ratio = (current as f32 / max as f32).clamp(0.0, 1.0);
    let color = if ratio > 0.5 { 0x00CC00FF }
                else if ratio > 0.25 { 0xCCCC00FF }
                else { 0xCC0000FF };
    draw_rect(x, y, w, h, 0x333333FF);     // Background
    draw_rect(x, y, w * ratio, h, color);  // Fill
}
```

### Score Display

```rust
fn render_score(score: u32, x: f32, y: f32) {
    let text = format!("SCORE: {:08}", score);
    draw_text_str(&text, x, y, 24.0, 0xFFFFFFFF);
}
```

### Timer (with flash warning)

```rust
fn render_timer(ticks: u64, x: f32, y: f32) {
    let secs = ticks / 60;
    let text = format!("{:02}:{:02}", secs / 60, secs % 60);
    let color = if ticks < 600 && (ticks / 15) % 2 == 0 { 0xFF0000FF } else { 0xFFFFFFFF };
    draw_text_str(&text, x, y, 36.0, color);
}
```

---

## Focus System (Controller Navigation)

```rust
struct FocusGrid { columns: u8, rows: u8, current: u8 }

impl FocusGrid {
    fn update(&mut self) {
        let col = self.current % self.columns;
        let row = self.current / self.columns;
        if button_pressed(0, button::LEFT) && col > 0 { self.current -= 1; }
        if button_pressed(0, button::RIGHT) && col < self.columns - 1 { self.current += 1; }
        if button_pressed(0, button::UP) && row > 0 { self.current -= self.columns; }
        if button_pressed(0, button::DOWN) && row < self.rows - 1 { self.current += self.columns; }
    }
}
```

### Button with Focus State

```rust
fn render_button(text: &str, x: f32, y: f32, w: f32, h: f32, focused: bool) {
    let bg = if focused { 0x4444AAFF } else { 0x333366FF };
    let border = if focused { 0xFFFF00FF } else { 0x666699FF };
    draw_rect(x, y, w, h, bg);
    // Draw border lines...
    draw_text_str(text, x + 10.0, y + h/2.0 - 10.0, 20.0, 0xFFFFFFFF);
}
```

---

## Font Rendering

```rust
static mut MAIN_FONT: u32 = 0;

fn init() {
    unsafe { MAIN_FONT = rom_font_str("main_font"); }
}

fn draw_text_shadowed(text: &str, x: f32, y: f32, size: f32, color: u32) {
    let off = size * 0.08;
    draw_text_str(text, x + off, y + off, size, 0x000000AA);  // Shadow
    draw_text_str(text, x, y, size, color);
}
```

---

## Pause Overlay

```rust
fn render_pause_overlay(selected: u8) {
    draw_rect(0.0, 0.0, 960.0, 540.0, 0x00000099);  // Dim background
    draw_rect(330.0, 180.0, 300.0, 180.0, 0x222244FF);  // Box
    draw_text_str("PAUSED", 420.0, 200.0, 40.0, 0xFFFFFFFF);
    render_options(&["Resume", "Quit"], selected, 260.0);
}
```

---

## Complete HUD Layout

```
+--[HP BAR]-------------------[TIMER]-------------------[SCORE]--+
|                                                                  |
|                         GAME AREA                                |
|                                                                  |
+--[LIVES]--------------------------------------------------[AMMO]-+
```

See **`references/common-layouts.md`** for inventory, dialogue boxes, minimaps.

---

## Related Skills

- **`gameplay-mechanics`** — Dialogue and choice menus
- **`multiplayer-patterns`** — Per-player HUD for split-screen
