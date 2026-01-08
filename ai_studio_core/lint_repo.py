from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LintMessage:
    level: str  # "error" | "warning"
    message: str


def _read_json(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: expected JSON object")
    return raw


def _lint_marketplace(repo_root: Path, messages: list[LintMessage]) -> None:
    marketplace = repo_root / ".claude-plugin" / "marketplace.json"
    if not marketplace.exists():
        messages.append(LintMessage("warning", "missing .claude-plugin/marketplace.json"))
        return

    try:
        data = _read_json(marketplace)
    except Exception as e:  # noqa: BLE001
        messages.append(LintMessage("error", f"failed to parse {marketplace}: {e}"))
        return

    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        messages.append(LintMessage("error", f"{marketplace}: plugins must be a list"))
        return

    for idx, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            messages.append(LintMessage("error", f"{marketplace}: plugins[{idx}] must be an object"))
            continue
        source = plugin.get("source")
        name = plugin.get("name", f"plugins[{idx}]")
        if not isinstance(source, str) or not source:
            messages.append(LintMessage("error", f"{marketplace}: {name}: missing/invalid source"))
            continue
        if not source.startswith("./"):
            messages.append(LintMessage("warning", f"{marketplace}: {name}: source should be relative ('./...')"))
        source_path = (repo_root / source).resolve()
        if not source_path.exists():
            messages.append(LintMessage("error", f"{marketplace}: {name}: source path not found: {source}"))
            continue
        plugin_manifest = source_path / ".claude-plugin" / "plugin.json"
        if not plugin_manifest.exists():
            messages.append(LintMessage("error", f"{marketplace}: {name}: missing plugin manifest: {plugin_manifest}"))


_SUBAGENT_RE = re.compile(r"`([a-z0-9_-]+):([a-z0-9_-]+)`")


def _lint_agent_registry(repo_root: Path, messages: list[LintMessage]) -> None:
    registry = repo_root / "zx-orchestrator" / "skills" / "agent-registry" / "SKILL.md"
    if not registry.exists():
        messages.append(LintMessage("warning", f"missing agent registry: {registry}"))
        return

    text = registry.read_text(encoding="utf-8")
    found = set(_SUBAGENT_RE.findall(text))
    if not found:
        messages.append(LintMessage("warning", f"no subagent_type entries found in {registry}"))
        return

    for plugin, agent in sorted(found):
        agent_path = repo_root / plugin / "agents" / f"{agent}.md"
        if not agent_path.exists():
            messages.append(LintMessage("error", f"agent-registry references missing agent file: {plugin}:{agent} -> {agent_path}"))


def _lint_spec_examples(repo_root: Path, messages: list[LintMessage]) -> None:
    specs_dir = repo_root / "templates" / "specs"
    if not specs_dir.exists():
        messages.append(LintMessage("warning", f"missing templates/specs directory: {specs_dir}"))
        return

    spec_files = sorted(specs_dir.glob("*.json"))
    if not spec_files:
        messages.append(LintMessage("warning", "no spec examples found under templates/specs/*.json"))
        return

    try:
        from ai_studio_core.specs import load_asset_spec_json
    except ModuleNotFoundError as e:
        if e.name == "pydantic":
            messages.append(LintMessage("error", "spec validation requires pydantic; install with: pip install -e ."))
            return
        raise

    for path in spec_files:
        try:
            spec = load_asset_spec_json(path)
        except Exception as e:  # noqa: BLE001
            messages.append(LintMessage("error", f"invalid spec example {path}: {e}"))
            continue

        asset_type = str(getattr(spec.asset_type, "value", spec.asset_type))
        if asset_type in ("mesh_3d_hardsurface", "character_3d_lowpoly"):
            preset = getattr(spec, "pipeline_preset", None)
            if isinstance(preset, str):
                preset_path = repo_root / "templates" / "presets" / f"{preset}.json"
                if not preset_path.exists():
                    messages.append(LintMessage("error", f"{path}: pipeline_preset '{preset}' missing preset file: {preset_path}"))


def _lint_scaffold(repo_root: Path, messages: list[LintMessage]) -> None:
    scaffold_root = repo_root / "zx-procgen" / "scaffold" / ".studio"
    required = [
        scaffold_root / "generate.py",
        scaffold_root / "parsers" / "__init__.py",
    ]
    for p in required:
        if not p.exists():
            messages.append(LintMessage("error", f"missing scaffold file: {p}"))


def lint_repo(repo_root: Path) -> list[LintMessage]:
    messages: list[LintMessage] = []
    _lint_marketplace(repo_root, messages)
    _lint_agent_registry(repo_root, messages)
    _lint_spec_examples(repo_root, messages)
    _lint_scaffold(repo_root, messages)
    return messages

