# Dialogue Systems Reference

Rollback-safe dialogue and text box implementations for Nethercore ZX RPGs, visual novels, and adventure games.

## Basic Text Box

Simple text display with background.

```rust
use crate::ffi::*;

const BOX_X: f32 = 50.0;
const BOX_Y: f32 = 380.0;
const BOX_WIDTH: f32 = 860.0;
const BOX_HEIGHT: f32 = 120.0;
const TEXT_MARGIN: f32 = 20.0;
const TEXT_SIZE: f32 = 24.0;
const LINE_HEIGHT: f32 = 30.0;

fn render_text_box(text: &str) {
    // Draw box background
    draw_rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT, 0x000000DD);

    // Draw border
    draw_rect(BOX_X, BOX_Y, BOX_WIDTH, 2.0, 0xFFFFFFFF);
    draw_rect(BOX_X, BOX_Y + BOX_HEIGHT - 2.0, BOX_WIDTH, 2.0, 0xFFFFFFFF);
    draw_rect(BOX_X, BOX_Y, 2.0, BOX_HEIGHT, 0xFFFFFFFF);
    draw_rect(BOX_X + BOX_WIDTH - 2.0, BOX_Y, 2.0, BOX_HEIGHT, 0xFFFFFFFF);

    // Draw text
    draw_text_str(
        text,
        BOX_X + TEXT_MARGIN,
        BOX_Y + TEXT_MARGIN,
        TEXT_SIZE,
        0xFFFFFFFF
    );
}
```

---

## Typewriter Effect (Complete)

Progressive character reveal for dramatic text display.

```rust
const CHARS_PER_FRAME: u32 = 2;
const FAST_CHARS_PER_FRAME: u32 = 8;  // When holding button

#[derive(Clone)]
struct TypewriterBox {
    text: &'static str,
    chars_shown: u32,
    finished: bool,
    waiting_for_advance: bool,
}

impl TypewriterBox {
    fn new(text: &'static str) -> Self {
        Self {
            text,
            chars_shown: 0,
            finished: false,
            waiting_for_advance: false,
        }
    }

    fn update(&mut self) {
        if self.waiting_for_advance {
            // Wait for button press to continue
            if button_pressed(0, button::A) {
                self.waiting_for_advance = false;
                self.finished = true;
            }
            return;
        }

        if self.chars_shown < self.text.len() as u32 {
            // Speed up when A held
            let speed = if button_held(0, button::A) {
                FAST_CHARS_PER_FRAME
            } else {
                CHARS_PER_FRAME
            };

            self.chars_shown = (self.chars_shown + speed).min(self.text.len() as u32);

            // Check if we've shown all text
            if self.chars_shown >= self.text.len() as u32 {
                self.waiting_for_advance = true;
            }
        }
    }

    fn render(&self) {
        // Draw box
        draw_rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT, 0x000000DD);

        // Draw visible portion of text
        let visible = &self.text[..self.chars_shown as usize];
        draw_text_str(
            visible,
            BOX_X + TEXT_MARGIN,
            BOX_Y + TEXT_MARGIN,
            TEXT_SIZE,
            0xFFFFFFFF
        );

        // Draw continue indicator when waiting
        if self.waiting_for_advance {
            let blink = (tick_count() / 20) % 2 == 0;
            if blink {
                draw_text_str(
                    "v",
                    BOX_X + BOX_WIDTH - 30.0,
                    BOX_Y + BOX_HEIGHT - 25.0,
                    TEXT_SIZE,
                    0xFFFF00FF
                );
            }
        }
    }

    fn is_finished(&self) -> bool {
        self.finished
    }

    fn skip_to_end(&mut self) {
        self.chars_shown = self.text.len() as u32;
        self.waiting_for_advance = true;
    }
}
```

### Multi-Line Typewriter

Handle text that spans multiple lines:

```rust
const MAX_CHARS_PER_LINE: usize = 50;
const MAX_LINES: usize = 3;

struct MultiLineTypewriter {
    lines: [&'static str; MAX_LINES],
    line_count: usize,
    chars_shown: u32,
    total_chars: u32,
    finished: bool,
    waiting: bool,
}

impl MultiLineTypewriter {
    fn new(text: &'static str) -> Self {
        // Simple word-wrap (production code would be more sophisticated)
        let mut lines = [""; MAX_LINES];
        let mut line_count = 0;
        let mut current_line_start = 0;
        let mut last_space = 0;
        let mut char_count = 0;

        for (i, c) in text.char_indices() {
            char_count += 1;
            if c == ' ' {
                last_space = i;
            }

            if char_count >= MAX_CHARS_PER_LINE || c == '\n' {
                let end = if c == '\n' { i } else { last_space };
                if line_count < MAX_LINES {
                    lines[line_count] = &text[current_line_start..end];
                    line_count += 1;
                }
                current_line_start = end + 1;
                char_count = 0;
            }
        }

        // Add remaining text
        if current_line_start < text.len() && line_count < MAX_LINES {
            lines[line_count] = &text[current_line_start..];
            line_count += 1;
        }

        let total = lines[..line_count].iter().map(|l| l.len() as u32).sum();

        Self {
            lines,
            line_count,
            chars_shown: 0,
            total_chars: total,
            finished: false,
            waiting: false,
        }
    }

    fn render(&self) {
        draw_rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT, 0x000000DD);

        let mut chars_remaining = self.chars_shown;

        for (i, line) in self.lines[..self.line_count].iter().enumerate() {
            let line_len = line.len() as u32;
            let show_chars = chars_remaining.min(line_len) as usize;

            if show_chars > 0 {
                draw_text_str(
                    &line[..show_chars],
                    BOX_X + TEXT_MARGIN,
                    BOX_Y + TEXT_MARGIN + i as f32 * LINE_HEIGHT,
                    TEXT_SIZE,
                    0xFFFFFFFF
                );
            }

            chars_remaining = chars_remaining.saturating_sub(line_len);
        }
    }
}
```

---

## Choice Selection (Complete)

Menu for player choices in dialogue.

```rust
const MAX_CHOICES: usize = 4;
const CHOICE_HEIGHT: f32 = 32.0;
const ARROW_X: f32 = BOX_X + 15.0;
const CHOICE_TEXT_X: f32 = BOX_X + 35.0;

#[derive(Clone)]
struct ChoiceMenu {
    options: [&'static str; MAX_CHOICES],
    option_count: usize,
    selected: u8,
    confirmed: bool,
}

impl ChoiceMenu {
    fn new(options: &[&'static str]) -> Self {
        let mut menu = Self {
            options: [""; MAX_CHOICES],
            option_count: options.len().min(MAX_CHOICES),
            selected: 0,
            confirmed: false,
        };

        for (i, opt) in options.iter().take(MAX_CHOICES).enumerate() {
            menu.options[i] = opt;
        }

        menu
    }

    fn update(&mut self) {
        if self.confirmed {
            return;
        }

        // Navigate up/down
        if button_pressed(0, button::UP) && self.selected > 0 {
            self.selected -= 1;
        }
        if button_pressed(0, button::DOWN) && (self.selected as usize) < self.option_count - 1 {
            self.selected += 1;
        }

        // Confirm selection
        if button_pressed(0, button::A) {
            self.confirmed = true;
        }
    }

    fn render(&self) {
        let box_height = self.option_count as f32 * CHOICE_HEIGHT + TEXT_MARGIN * 2.0;
        draw_rect(BOX_X, BOX_Y, BOX_WIDTH, box_height, 0x000000DD);

        for i in 0..self.option_count {
            let y = BOX_Y + TEXT_MARGIN + i as f32 * CHOICE_HEIGHT;

            // Draw selection arrow
            if i == self.selected as usize {
                draw_text_str(">", ARROW_X, y, TEXT_SIZE, 0xFFFF00FF);
            }

            // Draw option text
            let color = if i == self.selected as usize {
                0xFFFF00FF  // Yellow for selected
            } else {
                0xCCCCCCFF  // Gray for unselected
            };

            draw_text_str(self.options[i], CHOICE_TEXT_X, y, TEXT_SIZE, color);
        }
    }

    fn get_selection(&self) -> Option<u8> {
        if self.confirmed {
            Some(self.selected)
        } else {
            None
        }
    }
}
```

---

## Dialogue Sequence Manager

Chain multiple dialogue entries with optional choices.

```rust
const MAX_DIALOGUE_ENTRIES: usize = 32;

#[derive(Clone, Copy)]
enum DialogueEntry {
    Text(&'static str),
    Choice(&'static [&'static str], &'static [u8]),  // (options, jump targets)
    Jump(u8),      // Jump to entry index
    End,
}

struct DialogueSequence {
    entries: &'static [DialogueEntry],
    current_index: u8,
    typewriter: Option<TypewriterBox>,
    choice_menu: Option<ChoiceMenu>,
    finished: bool,
}

impl DialogueSequence {
    fn new(entries: &'static [DialogueEntry]) -> Self {
        let mut seq = Self {
            entries,
            current_index: 0,
            typewriter: None,
            choice_menu: None,
            finished: false,
        };
        seq.load_current();
        seq
    }

    fn load_current(&mut self) {
        if self.current_index as usize >= self.entries.len() {
            self.finished = true;
            return;
        }

        match self.entries[self.current_index as usize] {
            DialogueEntry::Text(text) => {
                self.typewriter = Some(TypewriterBox::new(text));
                self.choice_menu = None;
            }
            DialogueEntry::Choice(options, _) => {
                self.typewriter = None;
                self.choice_menu = Some(ChoiceMenu::new(options));
            }
            DialogueEntry::Jump(target) => {
                self.current_index = target;
                self.load_current();
            }
            DialogueEntry::End => {
                self.finished = true;
            }
        }
    }

    fn update(&mut self) {
        if self.finished {
            return;
        }

        // Handle typewriter
        if let Some(ref mut tw) = self.typewriter {
            tw.update();
            if tw.is_finished() {
                self.advance();
            }
        }

        // Handle choice menu
        if let Some(ref mut menu) = self.choice_menu {
            menu.update();
            if let Some(selection) = menu.get_selection() {
                // Get jump target from entry
                if let DialogueEntry::Choice(_, targets) = self.entries[self.current_index as usize] {
                    if (selection as usize) < targets.len() {
                        self.current_index = targets[selection as usize];
                    } else {
                        self.current_index += 1;
                    }
                    self.load_current();
                }
            }
        }
    }

    fn advance(&mut self) {
        self.current_index += 1;
        self.load_current();
    }

    fn render(&self) {
        if let Some(ref tw) = self.typewriter {
            tw.render();
        }
        if let Some(ref menu) = self.choice_menu {
            menu.render();
        }
    }

    fn is_finished(&self) -> bool {
        self.finished
    }
}
```

### Example Dialogue Definition

```rust
const INTRO_DIALOGUE: &[DialogueEntry] = &[
    DialogueEntry::Text("Welcome, adventurer!"),
    DialogueEntry::Text("I have a quest for you."),
    DialogueEntry::Choice(
        &["Accept quest", "Decline", "Ask for more info"],
        &[4, 6, 3]  // Jump targets for each choice
    ),
    DialogueEntry::Text("The kingdom needs your help..."),  // Index 3
    DialogueEntry::Jump(2),  // Back to choice
    DialogueEntry::Text("Excellent! Head to the forest."),  // Index 4 (Accept)
    DialogueEntry::End,
    DialogueEntry::Text("Very well. Come back if you change your mind."),  // Index 6 (Decline)
    DialogueEntry::End,
];
```

---

## Portrait System

Character portraits alongside dialogue.

```rust
const PORTRAIT_SIZE: f32 = 96.0;
const PORTRAIT_X: f32 = BOX_X + 10.0;
const PORTRAIT_Y: f32 = BOX_Y + 10.0;
const TEXT_WITH_PORTRAIT_X: f32 = PORTRAIT_X + PORTRAIT_SIZE + 20.0;

#[derive(Clone, Copy)]
struct DialogueWithPortrait {
    speaker: &'static str,
    text: &'static str,
    portrait_id: u8,
    portrait_emotion: u8,  // 0=neutral, 1=happy, 2=angry, etc.
}

struct PortraitTypewriter {
    entry: DialogueWithPortrait,
    chars_shown: u32,
    finished: bool,
    waiting: bool,
}

impl PortraitTypewriter {
    fn new(entry: DialogueWithPortrait) -> Self {
        Self {
            entry,
            chars_shown: 0,
            finished: false,
            waiting: false,
        }
    }

    fn update(&mut self) {
        if self.waiting {
            if button_pressed(0, button::A) {
                self.finished = true;
            }
            return;
        }

        let speed = if button_held(0, button::A) { 6 } else { 2 };
        self.chars_shown = (self.chars_shown + speed).min(self.entry.text.len() as u32);

        if self.chars_shown >= self.entry.text.len() as u32 {
            self.waiting = true;
        }
    }

    fn render(&self, portrait_texture: u32) {
        // Draw dialogue box
        draw_rect(BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT, 0x000000DD);

        // Draw portrait
        texture_bind(portrait_texture);
        let row = self.entry.portrait_id as f32;
        let col = self.entry.portrait_emotion as f32;
        let portraits_per_row = 4.0;
        draw_sprite_region(
            PORTRAIT_X, PORTRAIT_Y,
            PORTRAIT_SIZE, PORTRAIT_SIZE,
            col / portraits_per_row, row / portraits_per_row,
            1.0 / portraits_per_row, 1.0 / portraits_per_row,
            0xFFFFFFFF
        );

        // Draw speaker name
        draw_text_str(
            self.entry.speaker,
            TEXT_WITH_PORTRAIT_X,
            BOX_Y + 10.0,
            20.0,
            0xFFFF00FF
        );

        // Draw dialogue text
        let visible = &self.entry.text[..self.chars_shown as usize];
        draw_text_str(
            visible,
            TEXT_WITH_PORTRAIT_X,
            BOX_Y + 40.0,
            TEXT_SIZE,
            0xFFFFFFFF
        );

        // Continue indicator
        if self.waiting {
            let blink = (tick_count() / 15) % 2 == 0;
            if blink {
                draw_text_str("v", BOX_X + BOX_WIDTH - 25.0, BOX_Y + BOX_HEIGHT - 20.0, 20.0, 0xFFFF00FF);
            }
        }
    }
}
```

---

## Branching Dialogue State

Save and load dialogue progress for persistent games.

```rust
const MAX_FLAGS: usize = 64;
const MAX_VARIABLES: usize = 16;

/// Dialogue state that persists across saves
#[derive(Clone, Copy)]
#[repr(C)]
struct DialogueState {
    flags: [u8; MAX_FLAGS / 8],      // Bit flags for story events
    variables: [i16; MAX_VARIABLES], // Named variables
    current_scene: u16,
    current_node: u16,
}

impl DialogueState {
    fn new() -> Self {
        Self {
            flags: [0; MAX_FLAGS / 8],
            variables: [0; MAX_VARIABLES],
            current_scene: 0,
            current_node: 0,
        }
    }

    fn set_flag(&mut self, flag_id: u8) {
        let byte_idx = flag_id as usize / 8;
        let bit_idx = flag_id % 8;
        if byte_idx < self.flags.len() {
            self.flags[byte_idx] |= 1 << bit_idx;
        }
    }

    fn clear_flag(&mut self, flag_id: u8) {
        let byte_idx = flag_id as usize / 8;
        let bit_idx = flag_id % 8;
        if byte_idx < self.flags.len() {
            self.flags[byte_idx] &= !(1 << bit_idx);
        }
    }

    fn check_flag(&self, flag_id: u8) -> bool {
        let byte_idx = flag_id as usize / 8;
        let bit_idx = flag_id % 8;
        if byte_idx < self.flags.len() {
            (self.flags[byte_idx] & (1 << bit_idx)) != 0
        } else {
            false
        }
    }

    fn set_variable(&mut self, var_id: u8, value: i16) {
        if (var_id as usize) < MAX_VARIABLES {
            self.variables[var_id as usize] = value;
        }
    }

    fn get_variable(&self, var_id: u8) -> i16 {
        if (var_id as usize) < MAX_VARIABLES {
            self.variables[var_id as usize]
        } else {
            0
        }
    }

    fn add_variable(&mut self, var_id: u8, amount: i16) {
        if (var_id as usize) < MAX_VARIABLES {
            self.variables[var_id as usize] += amount;
        }
    }
}
```

### Conditional Dialogue

```rust
#[derive(Clone, Copy)]
enum DialogueCondition {
    None,
    FlagSet(u8),
    FlagClear(u8),
    VariableGreater(u8, i16),
    VariableLess(u8, i16),
    VariableEquals(u8, i16),
}

#[derive(Clone, Copy)]
struct ConditionalEntry {
    condition: DialogueCondition,
    entry: DialogueEntry,
}

fn evaluate_condition(condition: DialogueCondition, state: &DialogueState) -> bool {
    match condition {
        DialogueCondition::None => true,
        DialogueCondition::FlagSet(id) => state.check_flag(id),
        DialogueCondition::FlagClear(id) => !state.check_flag(id),
        DialogueCondition::VariableGreater(id, val) => state.get_variable(id) > val,
        DialogueCondition::VariableLess(id, val) => state.get_variable(id) < val,
        DialogueCondition::VariableEquals(id, val) => state.get_variable(id) == val,
    }
}

// Find first matching entry
fn get_conditional_entry(
    entries: &[ConditionalEntry],
    state: &DialogueState
) -> Option<&DialogueEntry> {
    for entry in entries {
        if evaluate_condition(entry.condition, state) {
            return Some(&entry.entry);
        }
    }
    None
}
```

---

## Complete Dialogue System

Full implementation with all features:

```rust
enum DialogueMode {
    Inactive,
    Playing(DialogueSequence),
    ChoiceActive(ChoiceMenu),
}

struct DialogueSystem {
    mode: DialogueMode,
    state: DialogueState,
    portrait_texture: u32,
}

impl DialogueSystem {
    fn new(portrait_texture: u32) -> Self {
        Self {
            mode: DialogueMode::Inactive,
            state: DialogueState::new(),
            portrait_texture,
        }
    }

    fn start(&mut self, entries: &'static [DialogueEntry]) {
        self.mode = DialogueMode::Playing(DialogueSequence::new(entries));
    }

    fn update(&mut self) {
        match &mut self.mode {
            DialogueMode::Inactive => {}
            DialogueMode::Playing(seq) => {
                seq.update();
                if seq.is_finished() {
                    self.mode = DialogueMode::Inactive;
                }
            }
            DialogueMode::ChoiceActive(menu) => {
                menu.update();
                if menu.get_selection().is_some() {
                    self.mode = DialogueMode::Inactive;
                }
            }
        }
    }

    fn render(&self) {
        match &self.mode {
            DialogueMode::Inactive => {}
            DialogueMode::Playing(seq) => seq.render(),
            DialogueMode::ChoiceActive(menu) => menu.render(),
        }
    }

    fn is_active(&self) -> bool {
        !matches!(self.mode, DialogueMode::Inactive)
    }

    fn save(&self) -> DialogueState {
        self.state
    }

    fn load(&mut self, state: DialogueState) {
        self.state = state;
    }
}
```

### Save/Load Integration

```rust
fn save_dialogue_state(system: &DialogueSystem, slot: u32) {
    let state = system.save();
    let bytes = unsafe {
        core::slice::from_raw_parts(
            &state as *const DialogueState as *const u8,
            core::mem::size_of::<DialogueState>()
        )
    };
    save(slot, bytes.as_ptr(), bytes.len() as u32);
}

fn load_dialogue_state(system: &mut DialogueSystem, slot: u32) {
    let mut state = DialogueState::new();
    let bytes = unsafe {
        core::slice::from_raw_parts_mut(
            &mut state as *mut DialogueState as *mut u8,
            core::mem::size_of::<DialogueState>()
        )
    };
    load(slot, bytes.as_mut_ptr(), bytes.len() as u32);
    system.load(state);
}
```
