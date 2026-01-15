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

## Validation

- Run `python3 scripts/lint_repo.py` before sending changes.
- CI runs the same script.

