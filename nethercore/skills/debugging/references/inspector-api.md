# Debug Inspector API

Authority for ZX: `nethercore/include/zx.rs` plus `include/zx/debug.rs` and host registration implementations. Check current bindings rather than expanding a guessed family of functions.

Common raw signatures:

```rust
// Declarations shown for signature reference, not a replacement binding module.
// debug_register_i32(name_ptr: *const u8, name_len: u32, ptr: *const u8)
// debug_register_f32(name_ptr: *const u8, name_len: u32, ptr: *const u8)
// debug_register_bool(name_ptr: *const u8, name_len: u32, ptr: *const u8)
```

Storage must remain alive/aligned and match the registered representation. Use `core::ptr::addr_of!(STATE_FIELD).cast::<u8>()` where appropriate, not typed references with the wrong FFI pointer type. Names/lengths are UTF-8 bytes. Group begin takes name pointer/length; group end has no name argument.

The host inspector supports value/watch registration, groups and frame controls. Confirm current shortcuts/configuration; these are host development inputs, not console game input APIs. Never infer zero release overhead or deterministic synchronization of live edits.

## Logging

```rust
unsafe {
    let msg = b"entered damage state";
    log(msg.as_ptr(), msg.len() as u32);
}
```

For dynamic messages reuse an existing game formatting path; `format!` requires allocator support and is not a free `no_std` primitive. Logs during rollback can repeat; do not count them as unique gameplay events without frame/context.

## Actions and replay

Debug actions require valid exported callbacks and exact typed parameter registration. Read the current action declarations instead of copying outdated argument counts. Do not use a callback name's guessed byte length.

NCRS parsing accepts action/assertion fields, but execution requires a real wired caller. The audited CLI headless runner does not load game WASM; graphical replay should only be credited with actions/assertions after those paths are demonstrated. For authoritative checks use native rule tests or an existing real runtime harness. See the testing skill's replay reference.

Keep pause/step/time scaling in the host; do not change simulation timesteps or skip updates based on local debug controls.
