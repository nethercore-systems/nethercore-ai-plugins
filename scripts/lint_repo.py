#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


FORBIDDEN_ASSISTANT_WORDS = (
    "claude",
    "anthropic",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _has_yaml_front_matter(text: str) -> bool:
    if not text.startswith("---\n"):
        return False
    lines = text.splitlines()
    if len(lines) < 3:
        return False
    return "---" in lines[1:]


def _extract_front_matter(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", len("---\n"))
    if end == -1:
        return None
    return text[len("---\n") : end]


def _front_matter_has_keys(front_matter: str, keys: tuple[str, ...]) -> list[str]:
    missing: list[str] = []
    for key in keys:
        if not re.search(rf"(?m)^{re.escape(key)}\s*:", front_matter):
            missing.append(key)
    return missing


def _check_forbidden_words(path: Path, text: str) -> list[str]:
    lowered = text.lower()
    hits = [w for w in FORBIDDEN_ASSISTANT_WORDS if w in lowered]
    if not hits:
        return []
    return hits


def _find_reference_paths(text: str) -> list[str]:
    return sorted(set(re.findall(r"references/[A-Za-z0-9_./-]+\.md", text)))


def _check_plugin_metadata(plugin_dir: Path) -> list[str]:
    errors: list[str] = []
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
    if not plugin_json.exists():
        errors.append(f"Missing plugin metadata: {plugin_json}")
        return errors

    try:
        data = json.loads(_read_text(plugin_json))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON: {plugin_json} ({exc})")
        return errors

    expected_name = plugin_dir.name
    actual_name = data.get("name")
    if actual_name != expected_name:
        errors.append(
            f"Plugin name mismatch in {plugin_json}: expected {expected_name!r}, found {actual_name!r}"
        )

    return errors


def lint_repo(repo_root: Path) -> int:
    repo_root = repo_root.resolve()
    errors: list[str] = []

    plugin_dirs = [repo_root / "nethercore", repo_root / "zx"]
    for plugin_dir in plugin_dirs:
        if not plugin_dir.is_dir():
            errors.append(f"Missing plugin dir: {plugin_dir}")
            continue

        errors.extend(_check_plugin_metadata(plugin_dir))

        # Skills
        for skill_file in sorted(plugin_dir.glob("skills/*/SKILL.md")):
            text = _read_text(skill_file)

            fm = _extract_front_matter(text)
            if fm is None:
                errors.append(f"Missing/invalid YAML front matter: {skill_file}")
                continue

            missing = _front_matter_has_keys(fm, ("name", "description", "version"))
            if missing:
                errors.append(f"Missing front matter keys {missing} in {skill_file}")

            forbidden_hits = _check_forbidden_words(skill_file, text)
            if forbidden_hits:
                errors.append(f"Forbidden assistant words {forbidden_hits} in {skill_file}")

            for rel in _find_reference_paths(text):
                ref_path = skill_file.parent / rel
                if not ref_path.exists():
                    errors.append(f"Missing reference {rel!r} referenced by {skill_file}")

        # Agents
        for agent_file in sorted(plugin_dir.glob("agents/*.md")):
            text = _read_text(agent_file)
            fm = _extract_front_matter(text)
            if fm is None:
                errors.append(f"Missing/invalid YAML front matter: {agent_file}")
                continue

            missing = _front_matter_has_keys(fm, ("name", "description"))
            if missing:
                errors.append(f"Missing front matter keys {missing} in {agent_file}")

            forbidden_hits = _check_forbidden_words(agent_file, text)
            if forbidden_hits:
                errors.append(f"Forbidden assistant words {forbidden_hits} in {agent_file}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print("OK: lint checks passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint nethercore-ai-plugins prompt packs")
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to repo root (default: auto-detected)",
    )
    args = parser.parse_args()
    return lint_repo(Path(args.repo_root))


if __name__ == "__main__":
    raise SystemExit(main())
