# CI workflow guidance

Adapt the project's existing CI; do not paste an unverified install/release workflow. A package named `nether-cli` on a registry is not proof it is the selected platform build. Pin the authorized Nethercore revision/tool artifact and provision its native dependencies explicitly.

## Small build job

After checkout, native toolchain setup, installation of `wasm32-unknown-unknown`, and provisioning the selected `nether` executable:

```bash
cargo fmt --check
cargo clippy --target wasm32-unknown-unknown -- -D warnings
nether build
```

Run native simulation tests with the actual host target if the game defaults to WASM. `cargo test` must not silently exercise zero useful tests or just fake FFI.

`nether build` is release by default. There is no `build --release` or `build --verbose` in the audited CLI. Keep generated assets and exact `[build].wasm` aligned with the packaging step.

## Runtime gates

On a runner with verified display/GPU/player support:

```bash
nether run --no-build --sync-test --check-distance 2 --players 1 --exit-after-frames 1000
nether run --no-build --replay tests/smoke.ncrs
```

Provide the existing script, outer timeouts, input scenarios and actual error/completion/capture checks. These rendered commands are **not** drop-in headless jobs. For semantic CI without a display, provision matching `nether` and `nethercore-zx` binaries and run:

```bash
nether replay validate tests/smoke.ncrs
nether replay run tests/smoke.ncrs --rom game.nczx --headless --report replay-report.json --timeout 30
```

Use the actual cart filename. Require zero exit, a completed `PASSED` report and meaningful assertions/nonempty state snapshots. Check a deliberate false assertion exits nonzero when establishing the gate. Use fresh report paths, and never accept an old report after an error. Keep rendered scripts inputs/screenshots-only; actions/assertions/semantic snapshots belong in headless scripts. Headless success does not assess graphics, sound or game feel.

## Release artifacts

Optimize WASM before packaging if justified; modifying it after `nether build` does not alter the already-packed ROM. Upload the verified final ROM under the real manifest game ID, not a guessed `game.nczx`. Release/tag/upload steps require explicit authorization and current provider configuration; verify the resulting remote artifact. Do not include automated publishing in a build-only job.
