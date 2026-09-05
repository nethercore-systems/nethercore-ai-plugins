---
name: debugging
description: >-
  Runtime debugging tools for Nethercore games on all consoles. Covers the F4
  Debug Inspector, live value editing, watch variables, frame stepping, and
  time-scale controls. Use when tuning game parameters at runtime, tracking
  state over time, or stepping through frames to find bugs.
license: Apache-2.0
compatibility: Debug Inspector available in all Nethercore consoles. Works offline.
metadata:
  author: nethercore-systems
  version: "1.0.1"
---

# Nethercore Debugging

Use the player's Debug Inspector and the current console bindings. F4 is the documented default inspector shortcut; confirm active input configuration before relying on other shortcuts. Host keyboard controls are not guest keyboard/mouse APIs.

## Register stable state

ZX raw FFI uses name pointer + byte length + a byte pointer to correctly typed storage, not a two-argument convenience API. Register initialized, suitably aligned, long-lived memory in `init`. Do not leave dangling pointers to stack locals or resized vectors.

```rust
static mut GRAVITY: f32 = 9.8;

fn init() {
    unsafe {
        let name = b"Gravity";
        debug_register_f32_range(
            name.as_ptr(), name.len() as u32,
            core::ptr::addr_of!(GRAVITY).cast::<u8>(), 1.0, 50.0,
        );
    }
}
```

Use available `debug_watch_*` functions for read-only views; do not assume every registration type has a watch equivalent. Verify signatures in `nethercore/include/zx.rs`. See [inspector API](references/inspector-api.md).

## Simulation boundary

The host handles pause/step/time scale. Do not early-return from authoritative `update` based on a local debug pause, or multiply simulation `delta_time` by a local time-scale control: that can break rollback consistency. Debug edits/actions are local scenario tools, not automatic synchronized multiplayer inputs.

Do not claim zero release overhead without checking the build/registration path. Gate optional instrumentation using the project's existing mechanism when needed.

## Evidence

Log with pointer and byte length, inspect actual player state and reproduce with controlled inputs. Replay parser support does not prove assertions/actions are executed. Use the testing skill's real-player/native/runtime distinction, not a simplified headless report as a pass.
