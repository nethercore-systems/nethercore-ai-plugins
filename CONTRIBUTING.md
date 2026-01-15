# Contributing (nethercore-ai-plugins)

This repo contains **prompt packs** (skills + task agents) for Nethercore development.
Most changes are Markdown-only and should be written so they can be reused across different AI coding assistants.

## Repo Layout

- `nethercore/` — console-agnostic Nethercore workflow skills + agents
- `zx/` — ZX console-specific specs + FFI reference skills

Each plugin pack contains:

- `.claude-plugin/plugin.json` — plugin metadata
- `skills/<skill>/SKILL.md` — short entrypoint instructions
- `skills/<skill>/references/*.md` — deeper reference docs
- `agents/*.md` — task-focused agents

## Local Validation

Run the same checks as CI:

```bash
python3 scripts/lint_repo.py
```

## Adding or Updating a Skill

1. Create a folder: `skills/<skill-name>/`
2. Add `skills/<skill-name>/SKILL.md`:
   - Include YAML front matter (`name`, `description`, `version`).
   - Keep it concise; link to `references/` for deep dives.
3. Add optional `skills/<skill-name>/references/*.md` for longer tables/examples.

## Adding or Updating an Agent

1. Add a new file under `agents/` (example: `agents/build-analyzer.md`).
2. Keep the body assistant-agnostic:
   - Avoid naming specific vendors/tools in the instructions.
   - Prefer concrete steps and output formats.
3. If the front matter needs a model/tool selector for a specific loader, keep it minimal.

## Versioning

Bump the version in the relevant plugin’s `.claude-plugin/plugin.json` when you make a meaningful change to prompts/behavior.
