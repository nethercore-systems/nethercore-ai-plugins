# nether CLI Commands

## Build Commands

| Command | Purpose |
|---------|---------|
| `nether init` | Create new nether.toml in current directory |
| `nether compile` | Compile WASM from source (runs build.script) |
| `nether pack` | Bundle WASM + assets into ROM |
| `nether build` | compile + pack combined |
| `nether build --release` | Optimized release build |
| `nether build --verbose` | Show detailed build output |

## Run Commands

| Command | Purpose |
|---------|---------|
| `nether run` | Build and launch in player |
| `nether run --sync-test` | Run determinism verification |
| `nether run --sync-test --frames N` | Test N frames |
| `nether run --record FILE` | Record replay |
| `nether run --replay FILE` | Playback replay |

## Examples

```bash
# Development cycle
nether build
nether run

# Release build
nether build --release

# Test determinism
nether run --sync-test --frames 3000

# Record and replay
nether run --record test.bin
nether run --replay test.bin
```
