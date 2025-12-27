# Hello World - Zig

Complete hello world example in Zig.

## Project Structure

```
hello-world-zig/
├── build.zig
├── nether.toml
└── src/
    ├── main.zig
    └── zx.zig
```

## build.zig

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.resolveTargetQuery(.{
        .cpu_arch = .wasm32,
        .os_tag = .freestanding,
    });

    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "game",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    exe.entry = .disabled;
    exe.rdynamic = true;

    b.installArtifact(exe);
}
```

## nether.toml

```toml
[game]
id = "hello-world-zig"
title = "Hello World (Zig)"
author = "Developer"
version = "1.0.0"

[build]
script = "zig build -Doptimize=ReleaseFast"
wasm = "zig-out/bin/game.wasm"
```

## src/main.zig

```zig
const zx = @import("zx.zig");

// Game state
var player_x: f32 = 480.0;
var player_y: f32 = 270.0;

export fn init() void {
    zx.set_clear_color(zx.rgba(26, 26, 46, 255));
    zx.render_mode(zx.Render.unlit);
    zx.logStr("Hello World (Zig) initialized!");
}

export fn update() void {
    const speed: f32 = 200.0 * zx.delta_time();

    player_x += zx.left_stick_x(0) * speed;
    player_y += zx.left_stick_y(0) * speed;

    // Clamp to screen bounds
    player_x = @max(16.0, @min(944.0, player_x));
    player_y = @max(16.0, @min(524.0, player_y));

    // Button press detection
    if (zx.button_pressed(0, zx.Button.a) != 0) {
        zx.logStr("A button pressed!");
    }
}

export fn render() void {
    // Draw player square
    zx.draw_rect(
        player_x - 16.0,
        player_y - 16.0,
        32.0,
        32.0,
        zx.rgba(255, 107, 107, 255),
    );

    // Draw title
    zx.drawTextStr("Hello, Nethercore ZX!", 300.0, 50.0, 32.0, zx.color.white);

    // Draw instructions
    zx.drawTextStr("Use left stick to move", 340.0, 500.0, 16.0, zx.rgba(255, 255, 255, 128));
}
```

## Build and Run

```bash
# Build
zig build -Doptimize=ReleaseFast

# Package and run
nether run
```

## Reference

For the complete zx.zig module, copy from:
```
nethercore/include/zx.zig
```

Or reference existing examples:
```
nethercore/examples/1-getting-started/hello-world-zig/
```

## Notes

- Uses Zig's freestanding wasm32 target
- No standard library (freestanding)
- Slice-based helpers like `logStr()`, `drawTextStr()` handle string passing
- Namespaced constants: `zx.Button.a`, `zx.Render.pbr`
