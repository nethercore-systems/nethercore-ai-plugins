# ROM packaging

ZX `.nczx` contains WASM, packed assets and game metadata. Source: `nethercore/tools/nether-cli/src/pack/` and `zx-common`.

```bash
nether build --debug  # diagnostic compile + pack
nether build          # release compile + pack (default)
nether pack           # existing WASM + assets only
```

Set `[build].wasm` to the exact artifact. Do not let a renamed crate's stale WASM win discovery. If external optimization is needed, optimize first, pack second, verify the final cart third. Do not rebuild over the optimized file before packing.

Use the project's release profile (`lto`, appropriate size optimization, `panic = "abort"`) and measure instead of assuming fixed savings. Keep required game assets in the datapack rather than embedding them in snapshotted RAM without need.

ZX specification is 16 MiB ROM, 4 MiB linear RAM and 4 MiB VRAM; actual allocated/decoded resources differ from compressed file sizes. The larger file-reader safety cap is not cartridge capacity.

Current upload requirements belong to the platform UI/backend, not a stale table here. ZX gameplay screenshots are captured at its 960x540 framebuffer; that alone does not establish the platform's icon/banner/upload rules. Verify intended accepted formats, dimensions, metadata and rights before an authorized upload.
