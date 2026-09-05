# Optimization techniques

## Optimize the real artifact

1. Record baseline WASM/ROM sizes, decoded resource costs and host frame/rollback measurements.
2. Reuse release profile/LTO and measure `opt-level = "s"` versus `"z"` where worthwhile.
3. If an existing Binaryen `wasm-opt` is justified, write a distinct candidate WASM, verify its required exports/imports, point `[build].wasm` at it and run `nether pack`. Do not run `nether build` afterward and silently replace the optimized artifact with a fresh compile.
4. Verify the exact packed cart in the player and relevant sync/native checks. No promised percentage savings.

## Texture size

RGBA8: `width * height * 4` bytes. BC7: `ceil(width/4) * ceil(height/4) * 16` bytes (format block payload; inspect other allocation/mipmap overhead separately). On aligned dimensions this is one byte/pixel, a 4:1 reduction from RGBA8. PNG file size is not VRAM.

Set `[game].compress_textures` deliberately. Use the smallest texture that meets the visual brief; preserve atlas borders, UVs, alpha and material channel layout. Do not impose one universal 256x256 default or assume an atlas always reduces draw calls.

## Mesh/state/audio

Use packed stride helpers from `zx-common`, not float-input stride assumptions. Inspect actual mesh attributes and the imported object/material scope. Animated rigs must fit the packed animation ceiling (currently 255), even though skeletons support 256.

Bound allocations when useful; measure total linear memory, not only `size_of` the main state. Stable snapshot-covered vectors can be correct. Integer compaction needs range/overflow/scaling tests.

WAV memory depends on sample count/channels/width; tracker size depends on patterns and sample library, not song length alone. Deduplicate intentional shared samples, preserve names/loop behavior, and audition before accepting a smaller encoding. Do not resample twice without a reason.
