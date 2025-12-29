# Hello World - C

Complete hello world example in C.

## Project Structure

```
hello-world-c/
├── Makefile
├── nether.toml
├── zx.h
└── game.c
```

## Makefile

```makefile
CC = clang
CFLAGS = --target=wasm32 -nostdlib -O2 -flto
LDFLAGS = -Wl,--no-entry -Wl,--export=init -Wl,--export=update -Wl,--export=render

TARGET = game.wasm
SRC = game.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean
```

## nether.toml

```toml
[game]
id = "hello-world-c"
title = "Hello World (C)"
author = "Developer"
version = "1.0.0"

[build]
script = "make"
wasm = "game.wasm"
```

## game.c

```c
#include "zx.h"

// Game state
static float player_x = 480.0f;
static float player_y = 270.0f;

void init(void) {
    set_clear_color(nczx_rgba(26, 26, 46, 255));  // Dark blue
    render_mode(NCZX_RENDER_UNLIT);
    NCZX_LOG("Hello World (C) initialized!");
}

void update(void) {
    float speed = 200.0f * delta_time();

    player_x += left_stick_x(0) * speed;
    player_y += left_stick_y(0) * speed;

    // Clamp to screen bounds
    if (player_x < 16.0f) player_x = 16.0f;
    if (player_x > 944.0f) player_x = 944.0f;
    if (player_y < 16.0f) player_y = 16.0f;
    if (player_y > 524.0f) player_y = 524.0f;

    // Jump on A button
    if (button_pressed(0, NCZX_BUTTON_A)) {
        NCZX_LOG("A button pressed!");
    }
}

void render(void) {
    // Draw player square
    draw_rect(player_x - 16.0f, player_y - 16.0f, 32.0f, 32.0f,
              nczx_rgba(255, 107, 107, 255));

    // Draw title
    NCZX_DRAW_TEXT("Hello, Nethercore ZX!", 300.0f, 50.0f, 32.0f,
                   NCZX_COLOR_WHITE);

    // Draw instructions
    NCZX_DRAW_TEXT("Use left stick to move", 340.0f, 500.0f, 16.0f,
                   nczx_rgba(255, 255, 255, 128));
}
```

## Build and Run

```bash
# Build (requires clang with wasm32 target)
make

# Package and run
nether run
```

## Reference

For the complete zx.h header, copy from:
```
nethercore/include/zx.h
```

Or reference existing examples:
```
nethercore/examples/1-getting-started/hello-world-c/
```

## Notes

- Requires clang with WebAssembly target support
- No standard library available (freestanding environment)
- All NCZX_ prefixed macros provide compile-time string length calculation
- Use `nczx_rgba()` for color packing
