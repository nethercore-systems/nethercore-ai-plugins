# nethercore-ai-plugins

Claude Code/Codex plugin packs for Nethercore game development (skills, commands, agents). This repo is mostly Markdown/JSON/YAML + small scripts; there is no single “build”.

## Repo Shape

- One folder per plugin (e.g. `zx-dev/`, `zx-procgen/`, `ai-game-studio/`)
- Typical plugin layout:
  - `.claude-plugin/plugin.json` — manifest (name/version/entrypoints)
  - `skills/` — auto-loaded knowledge (keep core lean)
  - `commands/` — explicit slash commands
  - `agents/` — sub-agents for complex workflows

Start here: `README.md`, `CLAUDE.md`.

## Authoring Guidelines (Keep Context Small)

- Keep each `skills/**/SKILL.md` concise (prefer ~150–250 lines).
- Put long tables/how-tos in `references/` and add “Load references when:” hints in the skill `description`.
- Avoid copying FFI or API surfaces into skills; instead link to canonical sources in the `nethercore/` repo (e.g. `../nethercore/include/zx.rs`, `../nethercore/docs/book/`).
- Prefer adding/reusing scripts/templates under the plugin over generating large files via the chat (faster and more reliable).

## Local Maintenance

- Cache reset helpers: `clear-cache.bat`, `clear-cache.sh` (use when plugin changes aren’t picked up).
