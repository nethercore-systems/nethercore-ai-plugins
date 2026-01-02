# Dialogue Systems Reference

Rollback-safe dialogue implementations for Nethercore ZX.

## Basic Text Box

```rust
const BOX_X: f32 = 50.0;
const BOX_Y: f32 = 380.0;
const BOX_WIDTH: f32 = 860.0;
const BOX_HEIGHT: f32 = 120.0;

fn render_text_box(text: &str) {
    draw_rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT, 0x000000DD);
    draw_text_str(text, BOX_X + 20.0, BOX_Y + 20.0, 24.0, 0xFFFFFFFF);
}
```

---

## Typewriter Effect

Progressive character reveal with skip functionality.

```rust
const CHARS_PER_FRAME: u32 = 2;
const FAST_CHARS: u32 = 8;  // When holding button

struct TypewriterBox {
    text: &'static str,
    chars_shown: u32,
    finished: bool,
    waiting: bool,
}

impl TypewriterBox {
    fn update(&mut self) {
        if self.waiting {
            if button_pressed(0, button::A) { self.finished = true; }
            return;
        }
        let speed = if button_held(0, button::A) { FAST_CHARS } else { CHARS_PER_FRAME };
        self.chars_shown = (self.chars_shown + speed).min(self.text.len() as u32);
        if self.chars_shown >= self.text.len() as u32 { self.waiting = true; }
    }

    fn render(&self) {
        draw_rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT, 0x000000DD);
        draw_text_str(&self.text[..self.chars_shown as usize], BOX_X + 20.0, BOX_Y + 20.0, 24.0, 0xFFFFFFFF);
        if self.waiting && (tick_count() / 20) % 2 == 0 {
            draw_text_str("v", BOX_X + BOX_WIDTH - 30.0, BOX_Y + BOX_HEIGHT - 25.0, 24.0, 0xFFFF00FF);
        }
    }
}
```

---

## Choice Selection

Menu navigation with D-pad and A button.

```rust
const MAX_CHOICES: usize = 4;

struct ChoiceMenu {
    options: [&'static str; MAX_CHOICES],
    count: usize,
    selected: u8,
    confirmed: bool,
}

impl ChoiceMenu {
    fn update(&mut self) {
        if self.confirmed { return; }
        if button_pressed(0, button::UP) && self.selected > 0 { self.selected -= 1; }
        if button_pressed(0, button::DOWN) && (self.selected as usize) < self.count - 1 { self.selected += 1; }
        if button_pressed(0, button::A) { self.confirmed = true; }
    }

    fn render(&self) {
        let height = self.count as f32 * 32.0 + 40.0;
        draw_rect(BOX_X, BOX_Y, BOX_WIDTH, height, 0x000000DD);
        for (i, opt) in self.options[..self.count].iter().enumerate() {
            let y = BOX_Y + 20.0 + i as f32 * 32.0;
            let color = if i == self.selected as usize { 0xFFFF00FF } else { 0xCCCCCCFF };
            if i == self.selected as usize { draw_text_str(">", BOX_X + 15.0, y, 24.0, color); }
            draw_text_str(opt, BOX_X + 35.0, y, 24.0, color);
        }
    }

    fn selection(&self) -> Option<u8> { if self.confirmed { Some(self.selected) } else { None } }
}
```

---

## Dialogue Sequence

Chain text entries with optional branching.

```rust
enum DialogueEntry {
    Text(&'static str),
    Choice(&'static [&'static str], &'static [u8]),  // (options, jump targets)
    Jump(u8),
    End,
}

struct DialogueSequence {
    entries: &'static [DialogueEntry],
    index: u8,
    // Current typewriter or choice menu state...
}
```

**Pattern:** Text entries advance linearly. Choice entries jump to target index based on selection. Use `End` to terminate.

---

## Portrait System (Pattern)

Display character portrait alongside dialogue:
1. Reserve left portion of box for portrait (96x96 recommended)
2. Store portraits as sprite sheet (characters × emotions)
3. Index by `portrait_id * emotions_per_char + emotion_id`

---

## Dialogue State (For Save/Load)

Track story progress with bitflags and variables:

```rust
struct DialogueState {
    flags: [u8; 8],       // 64 bool flags (bit-packed)
    variables: [i16; 16], // Named variables
    current_scene: u16,
    current_node: u16,
}
```

**Operations:**
- `set_flag(id)`: Set bit at position
- `check_flag(id)`: Read bit
- `set_variable(id, val)`: Store value
- `get_variable(id)`: Read value

Use for: NPC reactions, unlocked content, endings calculation.

---

## Best Practices

1. **Keep lines short** — Players read faster than typewriter, long text gets skipped
2. **Test skip timing** — Ensure A button skips cleanly to end
3. **Save state carefully** — Track which nodes player has seen
4. **Use break points** — Natural pause points for save
