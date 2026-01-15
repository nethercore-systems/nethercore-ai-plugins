# Nethercore Plugin

Platform tooling for Nethercore game development. Console-agnostic - works with any Nethercore console.

## Skills

### development
Core development workflow: nether CLI, nether.toml manifest, determinism rules.

### testing
Testing for determinism: sync testing, replay testing, benchmarking.

### optimization
Size optimization: WASM, textures, meshes, audio, state.

### publishing
Release workflow: ROM packaging, platform upload, CI/CD automation.

### debugging
F4 Debug Inspector, live value editing, frame control (all consoles).

## Agents

### build-analyzer
Analyzes ROM builds to identify size optimization opportunities.

### replay-debugger
Debugs issues using replay files (NCRS format).

## Quick Start

```bash
# Create new project
nether init

# Build and run
nether build
nether run

# Test determinism
nether run --sync-test

# Release build
nether build --release
```
