#!/usr/bin/env python3
"""Execute documented CLI contracts and semantic replays in two existing games."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def invoke(command: list[str], *, timeout: int = 45) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    if os.name == "nt":
        for key in ("TMP", "TEMP", "TMPDIR"):
            env[key] = tempfile.gettempdir()
    result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, env=env)
    return result


def check_documented_commands(nether: str) -> int:
    commands = set()
    pattern = r"nether (?:replay (?:run|compile|decompile|validate)|build|run|compile|pack|init)(?:\s.*)?"
    for doc in ROOT.rglob("*.md"):
        text = doc.read_text(encoding="utf-8")
        candidates = re.findall(r"`([^`\n]+)`", text)
        candidates += [line.strip() for line in text.splitlines() if line.startswith("nether ")]
        for candidate in candidates:
            candidate = candidate.split("#", 1)[0].strip()
            if re.fullmatch(pattern, candidate):
                commands.add(candidate)
    require(bool(commands), "No documented commands found")
    for command in sorted(commands):
        result = invoke([nether, *shlex.split(command)[1:], "--help"])
        require(result.returncode == 0, f"Unsupported documented command: {command}\n{result.stderr}")
    # Ensure this is actually validating arguments, not accepting any --help request.
    result = invoke([nether, "build", "--invalid-contract-option", "--help"])
    require(result.returncode != 0, "CLI help bypassed unknown-option validation")
    print(f"PASS: {len(commands)} documented CLI command forms")
    return len(commands)


def run_scenario(nether: str, rom: Path, script: Path, report: Path, *, success: bool) -> dict | None:
    report.write_text('{"summary":{"status":"PASSED"}}', encoding="utf-8")
    result = invoke([nether, "replay", "run", str(script), "--rom", str(rom),
                     "--headless", "--report", str(report), "--timeout", "20"])
    require((result.returncode == 0) == success,
            f"Unexpected exit {result.returncode}: {script}\n{result.stdout}\n{result.stderr}")
    data = json.loads(report.read_text(encoding="utf-8")) if report.exists() else None
    if success:
        require(data is not None, f"Missing successful report: {script}")
        require(data["summary"]["status"] == "PASSED", str(data))
        require(data["frames_executed"] == data["total_frames"], "Partial replay claimed success")
        require(data["summary"]["assertions_passed"] == 4, "Expected four semantic assertions")
        require(data["summary"]["assertions_failed"] == 0, "Failed semantic assertion")
        require(len(data["snapshots"]) == 4, "Expected four state snapshots")
        require(all(s["pre"] and s["post"] for s in data["snapshots"]), "Empty game state")
    elif data is not None:
        require(data["summary"]["status"] != "PASSED", "Failure report claimed PASSED")
    return data


def number(snapshot: dict, name: str) -> float:
    value = snapshot["post"][name]
    require(isinstance(value, dict) and len(value) == 1, f"Expected typed value: {value}")
    result = next(iter(value.values()))
    require(type(result) in (int, float), f"Expected numeric value: {value}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    suffix = ".exe" if os.name == "nt" else ""
    parser.add_argument("--nether", type=Path,
                        default=ROOT.parent / "nethercore" / "target" / "debug" / f"nether{suffix}")
    parser.add_argument("--games-root", type=Path, default=ROOT.parent)
    parser.add_argument("--rebuild-games", action="store_true",
                        help="Build sibling game WASM and pack temporary carts with this CLI")
    args = parser.parse_args()
    require(args.nether.is_file(), f"Build nether and nethercore-zx first: {args.nether}")
    nether = str(args.nether.resolve())
    check_documented_commands(nether)
    games = ("volley-fighter", "scrapheap-saints")
    for game in games:
        rom = args.games_root / game / f"{game}.nczx"
        require(args.rebuild_games or rom.is_file(), f"Required game ROM missing (not skipped): {rom}")
    with tempfile.TemporaryDirectory(prefix="nether-agent-workflow-") as scratch:
        scratch = Path(scratch)
        for game in games:
            rom = (args.games_root / game / f"{game}.nczx").resolve()
            if args.rebuild_games:
                project = (args.games_root / game).resolve()
                target = args.nether.resolve().parents[1]
                built = invoke(["cargo", "build", "--manifest-path", str(project / "Cargo.toml"),
                                "--target", "wasm32-unknown-unknown", "--release", "--locked",
                                "--target-dir", str(target)], timeout=180)
                require(built.returncode == 0, built.stdout + built.stderr)
                rom = scratch / f"{game}.nczx"
                wasm = target / "wasm32-unknown-unknown" / "release" / (game.replace("-", "_") + ".wasm")
                packed = invoke([nether, "pack", "--manifest", str(project / "nether.toml"),
                                 "--wasm", str(wasm), "--output", str(rom)])
                require(packed.returncode == 0, packed.stdout + packed.stderr)
            script = ROOT / "tests" / "replay" / f"{game}.ncrs"
            valid = invoke([nether, "replay", "validate", str(script)])
            require(valid.returncode == 0, valid.stdout + valid.stderr)
            runs = [run_scenario(nether, rom, script, scratch / f"{game}-{i}.json", success=True)
                    for i in range(2)]
            require(runs[0]["snapshots"] == runs[1]["snapshots"], f"State not repeatable: {game}")
            states = runs[0]["snapshots"]
            if game == "volley-fighter":
                require(number(states[0], "$match_phase") == 0, "Expected menu")
                require(number(states[1], "$match_phase") == 1, "Start input didn't enter serve")
                require(number(states[3], "$match_score_p1") == 1 and
                        number(states[3], "$match_score_p2") == 1, "Point actions didn't score")
            else:
                hp = [number(state, "$p1_hp") for state in states]
                require(0 < hp[1] < hp[0], "Set HP didn't lower health")
                require(hp[2] == hp[0] and hp[3] == hp[0], "Training reset didn't restore health")
            print(f"PASS: {game}: four semantic assertions, four nonempty snapshots, identical repeat")
            for label, directive in {
                "false-assertion": 'assert = "' + ("$match_phase" if game == "volley-fighter" else "$app_app_state") + ' == -999"',
                "unknown-action": 'action = "MISSING_AGENT_TEST_ACTION"',
                "unknown-variable": 'assert = "$MISSING_AGENT_TEST_VALUE == 0"',
            }.items():
                negative = scratch / f"{game}-{label}.ncrs"
                negative.write_text('console = "zx"\nseed = 1\nplayers = 1\n[[frames]]\nf = 0\n'
                                    + directive + '\n', encoding="utf-8")
                failure = run_scenario(nether, rom, negative, scratch / f"{game}-{label}.json", success=False)
                if label == "false-assertion":
                    require(failure["summary"]["status"] == "FAILED" and
                            failure["assertions"][0]["actual"] is not None,
                            "Negative control must evaluate live state, not merely fail parsing")
                print(f"PASS: {game}: {label} rejected")
        run_scenario(nether, scratch / "missing.nczx", script, scratch / "missing.json", success=False)
        print("PASS: missing ROM rejected")
    print("PASS: agent workflow across both real games; temporary reports removed")


if __name__ == "__main__":
    main()
