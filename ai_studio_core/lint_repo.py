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
_PLUGIN_REF_RE = re.compile(r"\b([a-z0-9_-]+):([a-z0-9_-]+)\b")
_MD_LINK_RE = re.compile(r"\[[^\]]*]\(([^)]+)\)")


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


def _marketplace_plugin_sources(repo_root: Path) -> dict[str, Path]:
    marketplace = repo_root / ".claude-plugin" / "marketplace.json"
    if not marketplace.exists():
        return {}

    try:
        data = _read_json(marketplace)
    except Exception:  # noqa: BLE001
        return {}

    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        return {}

    out: dict[str, Path] = {}
    for plugin in plugins:
        if not isinstance(plugin, dict):
            continue
        name = plugin.get("name")
        source = plugin.get("source")
        if not isinstance(name, str) or not isinstance(source, str):
            continue
        out[name] = (repo_root / source).resolve()
    return out


def _iter_markdown_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for p in repo_root.rglob("*.md"):
        # Avoid scanning git internals if present.
        if ".git" in p.parts:
            continue
        files.append(p)
    return sorted(files)


def _lint_markdown_links(repo_root: Path, messages: list[LintMessage]) -> None:
    md_files = _iter_markdown_files(repo_root)
    for md_path in md_files:
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            messages.append(LintMessage("error", f"failed to read {md_path}: {e}"))
            continue

        for raw_target in _MD_LINK_RE.findall(text):
            target = raw_target.strip()
            if not target or target.startswith("#"):
                continue
            if "://" in target or target.startswith("mailto:"):
                continue

            # Strip anchors.
            target_path = target.split("#", 1)[0].strip()
            if not target_path:
                continue

            # Only check link targets that look like local files.
            if "." not in Path(target_path).name:
                continue

            resolved = (md_path.parent / target_path).resolve()
            if resolved == repo_root or repo_root in resolved.parents:
                if not resolved.exists():
                    rel = md_path.relative_to(repo_root)
                    messages.append(LintMessage("error", f"{rel}: broken link target: {target_path}"))
            else:
                # Link points outside the repo; don't fail CI for it.
                continue


def _lint_plugin_references(repo_root: Path, messages: list[LintMessage]) -> None:
    plugins = _marketplace_plugin_sources(repo_root)
    if not plugins:
        return

    plugin_names = set(plugins.keys())
    md_files = _iter_markdown_files(repo_root)

    for md_path in md_files:
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            messages.append(LintMessage("error", f"failed to read {md_path}: {e}"))
            continue

        for plugin, ref in _PLUGIN_REF_RE.findall(text):
            if plugin not in plugin_names:
                continue

            plugin_root = plugins[plugin]
            cmd_path = plugin_root / "commands" / f"{ref}.md"
            agent_path = plugin_root / "agents" / f"{ref}.md"
            skill_path = plugin_root / "skills" / ref / "SKILL.md"

            if not (cmd_path.exists() or agent_path.exists() or skill_path.exists()):
                rel = md_path.relative_to(repo_root)
                messages.append(
                    LintMessage(
                        "error",
                        f"{rel}: references '{plugin}:{ref}' but no matching file found in commands/, agents/, or skills/",
                    )
                )


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
    scaffold_root = repo_root / "ai_studio_core" / "templates" / "project" / "studio"
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
    _lint_markdown_links(repo_root, messages)
    _lint_plugin_references(repo_root, messages)
    _lint_spec_examples(repo_root, messages)
    _lint_scaffold(repo_root, messages)
    return messages
