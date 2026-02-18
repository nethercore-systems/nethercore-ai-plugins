# Nethercore AI Plugins (Agent Instructions)

This repo is a set of **prompt packs** (skills + task agents) for Nethercore development.
The on-disk layout is compatible with the Claude Code plugin loader (`.claude-plugin/`), but the **Markdown content should stay assistant-agnostic** so it can be reused in other tools.

## Repo Layout

- `nethercore/` — Console-agnostic Nethercore workflow (build/test/optimize/publish)
- `zx/` — ZX fantasy console specs + FFI reference

Each plugin pack typically contains:

- `.claude-plugin/plugin.json` — plugin metadata
- `skills/<skill>/SKILL.md` — concise “entrypoint” instructions
- `skills/<skill>/references/*.md` — deeper reference material (tables, long lists)
- `agents/*.md` — task-focused agents (e.g. build analysis, replay debugging)

## Writing Guidelines

- Keep `SKILL.md` files short; move long content into `references/`.
- Prefer **concrete steps**, checklists, and small tables over prose.
- Avoid naming specific assistants/vendors (e.g. “Claude”, “ChatGPT”) inside `skills/` and `agents/` bodies.
- Prefer workspace-relative paths when referencing other repos (example: `nethercore/include/zx.rs`).
- Don’t assume network access; instructions should work offline.

### SKILL.md Standard

All skills must comply with the [SKILL.md open standard](https://agentskills.io/specification):

1. `name` — lowercase-hyphenated, matches parent directory name exactly
2. `description` — explains WHAT + WHEN to use, max 1024 chars
3. `license` — `Apache-2.0` for this repo
4. `metadata.author` — `nethercore-systems`
5. `metadata.version` — semver string (e.g., `"1.0.0"`)
6. Body under 500 lines; move long content to `references/`
7. Run `python3 scripts/lint_repo.py --strict` before committing

## Validation

- Run `python3 scripts/lint_repo.py` before sending changes.
- CI runs the same script.

