---
name: UI/UX Patterns for ZX
description: This skill should be used when the user asks about "menu", "HUD", "UI", "user interface", "pause menu", "title screen", "main menu", "game over screen", "health bar", "score display", "minimap", "button navigation", "focus states", "text rendering", "rom_font", or discusses implementing menus, heads-up displays, or UI navigation for Nethercore ZX games.
version: 1.0.0
---

# UI/UX Patterns for Nethercore ZX

ZX provides 2D drawing primitives (`draw_rect`, `draw_text`, `draw_line`, `draw_circle`) and font rendering (`rom_font`). Games implement their own UI systems. All UI code MUST be deterministic for rollback netcode compatibility.

## 2D Drawing FFI Quick Reference

| Function | Purpose |
|----------|---------|
| `draw_rect(x, y, w, h, color)` | Filled rectangle |
| `draw_text_str(text, x, y, size, color)` | Text with current font |
| `draw_line(x1, y1, x2, y2, thickness, color)` | Line segment |
| `draw_circle(x, y, radius, color)` | Filled circle |
| `draw_circle_outline(x, y, radius, thick, color)` | Circle outline |
| `rom_font_str(id)` | Bind ROM font for text |

**Color format:** `0xRRGGBBAA` (RGBA, 32-bit)

**Screen coordinates:** 960×540 pixels, origin at top-left

---

## Menu State Machine

Structure game flow as a state machine with explicit transitions.

### Basic State Machine

```rust
#[derive(Clone, Copy, PartialEq)]
enum GameState {
    Title,
    Playing,
    Paused,
    GameOver,
}

struct Game {
    state: GameState,
    menu_selection: u8,
    // ... game data
}

fn update(game: &mut Game) {
    match game.state {
        GameState::Title => update_title_menu(game),
        GameState::Playing => update_gameplay(game),
        GameState::Paused => update_pause_menu(game),
        GameState::GameOver => update_game_over(game),
    }
}

fn render(game: &Game) {
    match game.state {
        GameState::Title => render_title_screen(game),
        GameState::Playing => {
            render_gameplay(game);
            render_hud(game);
        }
        GameState::Paused => {
            render_gameplay(game);  // Frozen underneath
            render_pause_overlay(game);
        }
        GameState::GameOver => render_game_over(game),
    }
}
```

### Title Screen with Menu

```rust
const TITLE_OPTIONS: &[&str] = &["Start Game", "Options", "Credits"];

fn update_title_menu(game: &mut Game) {
    // Navigate with D-pad
    if button_pressed(0, button::UP) && game.menu_selection > 0 {
        game.menu_selection -= 1;
    }
    if button_pressed(0, button::DOWN) {
        if (game.menu_selection as usize) < TITLE_OPTIONS.len() - 1 {
            game.menu_selection += 1;
        }
    }

    // Confirm selection
    if button_pressed(0, button::A) {
        match game.menu_selection {
            0 => game.state = GameState::Playing,
            1 => { /* open options */ }
            2 => { /* show credits */ }
            _ => {}
        }
    }
}

fn render_title_screen(game: &Game) {
    // Background
    draw_rect(0.0, 0.0, 960.0, 540.0, 0x1a1a2eFF);

    // Title
    draw_text_str("MY GAME", 480.0 - 100.0, 120.0, 64.0, 0xFFFFFFFF);

    // Menu options
    let base_y = 280.0;
    for (i, option) in TITLE_OPTIONS.iter().enumerate() {
        let y = base_y + i as f32 * 50.0;
        let color = if i == game.menu_selection as usize {
            0xFFFF00FF  // Yellow = selected
        } else {
            0xAAAAAAFF  // Gray = unselected
        };
        draw_text_str(option, 400.0, y, 32.0, color);
    }

    // Selection indicator
    let indicator_y = base_y + game.menu_selection as f32 * 50.0;
    draw_text_str(">", 370.0, indicator_y, 32.0, 0xFFFF00FF);
}
```

### Pause Menu Overlay

```rust
fn update_pause_menu(game: &mut Game) {
    // Toggle pause
    if button_pressed(0, button::START) {
        game.state = GameState::Playing;
        return;
    }

    // Navigate
    if button_pressed(0, button::UP) && game.menu_selection > 0 {
        game.menu_selection -= 1;
    }
    if button_pressed(0, button::DOWN) && game.menu_selection < 1 {
        game.menu_selection += 1;
    }

    if button_pressed(0, button::A) {
        match game.menu_selection {
            0 => game.state = GameState::Playing,  // Resume
            1 => game.state = GameState::Title,    // Quit
            _ => {}
        }
    }
}

fn render_pause_overlay(game: &Game) {
    // Semi-transparent overlay
    draw_rect(0.0, 0.0, 960.0, 540.0, 0x00000099);

    // Pause box
    draw_rect(330.0, 180.0, 300.0, 180.0, 0x222244FF);
    draw_text_str("PAUSED", 420.0, 200.0, 40.0, 0xFFFFFFFF);

    // Options
    let opts = ["Resume", "Quit to Title"];
    for (i, opt) in opts.iter().enumerate() {
        let y = 260.0 + i as f32 * 40.0;
        let color = if i == game.menu_selection as usize {
            0xFFFF00FF
        } else {
            0xCCCCCCFF
        };
        draw_text_str(opt, 400.0, y, 28.0, color);
    }
}
```

---

## HUD Layouts

### Health Bar

```rust
fn render_health_bar(current: i32, max: i32, x: f32, y: f32) {
    let bar_width = 200.0;
    let bar_height = 20.0;
    let fill_ratio = (current as f32 / max as f32).clamp(0.0, 1.0);

    // Background (dark)
    draw_rect(x, y, bar_width, bar_height, 0x333333FF);

    // Fill (color based on health percentage)
    let fill_color = if fill_ratio > 0.5 {
        0x00CC00FF  // Green
    } else if fill_ratio > 0.25 {
        0xCCCC00FF  // Yellow
    } else {
        0xCC0000FF  // Red
    };
    draw_rect(x, y, bar_width * fill_ratio, bar_height, fill_color);

    // Border
    draw_line(x, y, x + bar_width, y, 2.0, 0xFFFFFFFF);
    draw_line(x, y + bar_height, x + bar_width, y + bar_height, 2.0, 0xFFFFFFFF);
    draw_line(x, y, x, y + bar_height, 2.0, 0xFFFFFFFF);
    draw_line(x + bar_width, y, x + bar_width, y + bar_height, 2.0, 0xFFFFFFFF);

    // Text overlay
    let text = format!("{}/{}", current, max);
    draw_text_str(&text, x + 70.0, y + 2.0, 16.0, 0xFFFFFFFF);
}
```

### Score Display

```rust
fn render_score(score: u32, x: f32, y: f32) {
    // Format with leading zeros for arcade feel
    let text = format!("SCORE: {:08}", score);
    draw_text_str(&text, x, y, 24.0, 0xFFFFFFFF);
}

fn render_combo(combo: u32, x: f32, y: f32) {
    if combo > 1 {
        let text = format!("{}x COMBO!", combo);
        // Pulse effect based on combo size
        let size = 24.0 + (combo.min(10) as f32 * 2.0);
        draw_text_str(&text, x, y, size, 0xFF8800FF);
    }
}
```

### Timer Display

```rust
fn render_timer(remaining_ticks: u64, x: f32, y: f32) {
    // Convert ticks to seconds (assuming 60fps)
    let total_seconds = remaining_ticks / 60;
    let minutes = total_seconds / 60;
    let seconds = total_seconds % 60;

    let text = format!("{:02}:{:02}", minutes, seconds);

    // Flash red when low
    let color = if remaining_ticks < 600 {  // Last 10 seconds
        if (remaining_ticks / 15) % 2 == 0 {
            0xFF0000FF
        } else {
            0xFFFFFFFF
        }
    } else {
        0xFFFFFFFF
    };

    draw_text_str(&text, x, y, 36.0, color);
}
```

### Lives Display

```rust
fn render_lives(lives: u8, x: f32, y: f32, icon_texture: u32) {
    for i in 0..lives {
        let icon_x = x + i as f32 * 30.0;
        // Draw small player icon for each life
        draw_sprite(icon_texture, icon_x, y, 24.0, 24.0);
    }
}
```

---

## Controller Navigation

### Focus System

```rust
#[derive(Clone, Copy)]
struct FocusGrid {
    columns: u8,
    rows: u8,
    current: u8,  // Linear index
}

impl FocusGrid {
    fn move_focus(&mut self, dx: i8, dy: i8) {
        let col = (self.current % self.columns) as i8;
        let row = (self.current / self.columns) as i8;

        let new_col = (col + dx).clamp(0, self.columns as i8 - 1) as u8;
        let new_row = (row + dy).clamp(0, self.rows as i8 - 1) as u8;

        self.current = new_row * self.columns + new_col;
    }

    fn update(&mut self) {
        if button_pressed(0, button::LEFT)  { self.move_focus(-1, 0); }
        if button_pressed(0, button::RIGHT) { self.move_focus(1, 0); }
        if button_pressed(0, button::UP)    { self.move_focus(0, -1); }
        if button_pressed(0, button::DOWN)  { self.move_focus(0, 1); }
    }

    fn is_focused(&self, index: u8) -> bool {
        self.current == index
    }
}
```

### Button Rendering with Focus

```rust
fn render_button(text: &str, x: f32, y: f32, w: f32, h: f32, focused: bool) {
    let bg_color = if focused { 0x4444AAFF } else { 0x333366FF };
    let border_color = if focused { 0xFFFF00FF } else { 0x666699FF };
    let text_color = if focused { 0xFFFFFFFF } else { 0xAAAAAAFF };

    // Background
    draw_rect(x, y, w, h, bg_color);

    // Border (thicker when focused)
    let thickness = if focused { 3.0 } else { 1.0 };
    draw_line(x, y, x + w, y, thickness, border_color);
    draw_line(x, y + h, x + w, y + h, thickness, border_color);
    draw_line(x, y, x, y + h, thickness, border_color);
    draw_line(x + w, y, x + w, y + h, thickness, border_color);

    // Centered text
    let text_x = x + w / 2.0 - (text.len() as f32 * 8.0);
    let text_y = y + h / 2.0 - 10.0;
    draw_text_str(text, text_x, text_y, 20.0, text_color);
}
```

---

## Font Rendering

### Loading ROM Fonts

```rust
static mut MAIN_FONT: u32 = 0;
static mut TITLE_FONT: u32 = 0;

fn init() {
    unsafe {
        MAIN_FONT = rom_font_str("main_font");
        TITLE_FONT = rom_font_str("title_font");
    }
}

fn render_with_fonts() {
    unsafe {
        // Switch to title font for headers
        bind_font(TITLE_FONT);
        draw_text_str("GAME TITLE", 300.0, 50.0, 72.0, 0xFFFFFFFF);

        // Switch back to main font for body
        bind_font(MAIN_FONT);
        draw_text_str("Press Start", 380.0, 400.0, 24.0, 0xCCCCCCFF);
    }
}
```

### Text with Shadow

```rust
fn draw_text_shadowed(text: &str, x: f32, y: f32, size: f32, color: u32) {
    // Shadow offset
    let offset = size * 0.08;

    // Draw shadow first (darker, offset)
    draw_text_str(text, x + offset, y + offset, size, 0x000000AA);

    // Draw main text
    draw_text_str(text, x, y, size, color);
}
```

---

## Complete HUD Example

```rust
struct HUD {
    health: i32,
    max_health: i32,
    score: u32,
    lives: u8,
    timer_ticks: u64,
}

fn render_hud(hud: &HUD) {
    // Top-left: Health
    draw_text_str("HP", 20.0, 20.0, 18.0, 0xFFFFFFFF);
    render_health_bar(hud.health, hud.max_health, 60.0, 18.0);

    // Top-center: Timer
    render_timer(hud.timer_ticks, 440.0, 20.0);

    // Top-right: Score
    render_score(hud.score, 720.0, 20.0);

    // Bottom-left: Lives
    draw_text_str("LIVES:", 20.0, 500.0, 18.0, 0xFFFFFFFF);
    // render_lives(hud.lives, 100.0, 498.0, life_icon);
}
```

---

## Additional Resources

### Reference Files

For detailed UI patterns and layouts:
- **`references/common-layouts.md`** — Standard HUD configurations, inventory grids, dialogue boxes

### Related Skills

- **`gameplay-mechanics`** — Dialogue systems and choice menus
- **`perspective-patterns`** — Camera and viewport for split-screen HUDs
- **`multiplayer-rendering`** — Per-player HUD layouts
