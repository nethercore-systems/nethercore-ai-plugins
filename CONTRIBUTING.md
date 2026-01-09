# Contributing (nethercore-ai-plugins)

This repo contains **plugin packs** (skills, commands, agents) that wrap the standalone `ai-studio-core` CLI/library.

- Core repo (schemas/validators/CLI/templates): `ai-studio-core`
- Plugin repo (orchestration/prompts): `nethercore-ai-plugins`

## Local Setup

Install the pinned core dependency:

```bash
python3 -m pip install -r requirements-core.txt
ai-studio --help
```

## Validate Changes

Run the same checks as CI:

```bash
ai-studio lint-repo --repo-root .
```

## Adding or Updating a Plugin

Typical plugin layout:

- `.claude-plugin/plugin.json` — manifest
- `skills/<name>/SKILL.md` — skills (keep concise)
- `commands/<name>.md` — slash commands
- `agents/<name>.md` — sub-agents

When adding a new plugin:

1. Add the plugin folder (keep names lowercase with `-`).
2. Register it in `.claude-plugin/marketplace.json`.
3. If you add a new orchestrator subagent, update `zx-orchestrator/skills/agent-registry/SKILL.md`.
4. Run `ai-studio lint-repo --repo-root .` and fix any missing references.

## Adding a New Asset Type

Asset specs, schemas, validators, presets, and examples live in **`ai-studio-core`**.

- Follow the core repo contributing guide:
  - Workspace: `../ai-studio-core/CONTRIBUTING.md`
  - GitHub: `https://github.com/RobDavenport/ai-studio-core`
