---
name: publishing
description: >-
  Publishing Nethercore games to nethercore.systems. Covers ROM packaging with
  nether pack, release builds, platform upload requirements, versioning, and
  CI/CD pipeline setup with GitHub Actions. Use when preparing a game for
  release or setting up automated builds.
license: Apache-2.0
compatibility: Requires nether CLI. Needs network for upload.
metadata:
  author: nethercore-systems
  version: "1.0.1"
---

# Nethercore Publishing

Prepare a verified release artifact; publishing/upload is a separate externally visible action requiring user authorization.

```bash
nether build              # release by default: compile + pack
nether run --no-build     # verify the resulting cart
```

Use `nether build --debug` only for a diagnostic build, not `--release` (unsupported). `nether pack` does not compile: use it after a deliberate external WASM/asset preparation step.

## Release checks

- Explicit manifest version, build output, player count, tick rate and netplay intent.
- Actual console ROM/RAM/VRAM budgets and required resources verified; ZX ROM ceiling is 16 MiB.
- Native rule tests, real input/render/audio path, and relevant rollback checks against the exact final cart.
- Metadata/screenshots and asset rights checked. Read the current platform upload UI/backend contract before asserting icon/banner dimensions, accepted file types or screenshot counts; old prompt-pack values are not release requirements.
- Preserve required debugging/provenance information, not build caches. A successful build is not proof an upload was published.

Version in `[game].version`; update the project's existing changelog/tag workflow as requested. Do not auto-tag, release or upload merely because a game was built.

See [ROM packaging](references/rom-packaging.md) and [CI workflow guidance](references/ci-workflows.md).
