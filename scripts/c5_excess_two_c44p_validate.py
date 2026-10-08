#!/usr/bin/env python3
"""Run the complete C44' replays and record actual commands, bytes and exits.

The mathematical generators own their exclusive creation and --check modes.
This driver checks their existing products without regenerating old C44 data.
validation.json is an execution ledger rather than a mathematical certificate.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_excess_two_c44p"
PYTHON = "/home/ray/developer/ai/math/.venv/bin/python"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def products() -> dict[str, str]:
    paths = list(OUT.rglob("*"))
    paths += list((ROOT / "scripts").glob("c5_excess_two_c44p_*.py"))
    return {str(p.relative_to(ROOT)): digest(p.read_bytes())
            for p in sorted(paths)
            if p.is_file() and p.name != "validation.json"}


def run(argv: list[str], seed: str | None, scope: str) -> dict:
    env = os.environ.copy()
    env.pop("PYTHONHASHSEED", None)
    if seed is not None:
        env["PYTHONHASHSEED"] = seed
    command = (f"PYTHONHASHSEED={seed} " if seed else "") + shlex.join(argv)
    start = time.monotonic()
    result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True)
    record = {
        "command": command,
        "command_sha256": digest(command.encode()),
        "cwd": str(ROOT),
        "scope": scope,
        "exit_code": result.returncode,
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "stdout": result.stdout.decode(errors="replace"),
        "stderr": result.stderr.decode(errors="replace"),
        "stdout_sha256": digest(result.stdout),
        "stderr_sha256": digest(result.stderr),
        "products_manifest_sha256": digest(json.dumps(products(), sort_keys=True).encode()),
    }
    print(f"{command}: exit {result.returncode}", flush=True)
    if result.returncode:
        print(record["stdout"] + record["stderr"], flush=True)
    return record


def main() -> int:
    ledger = OUT / "validation.json"
    old = json.loads(ledger.read_text()) if ledger.exists() else {}
    prior = old.get("pre_restore_checks", [])
    commands = []
    for seed in (None, "17"):
        for script in ("screen", "two_private", "independent"):
            commands.append(run(
                [PYTHON, f"scripts/c5_excess_two_c44p_{script}.py", "--check"], seed,
                f"Full {script} mathematical recomputation and byte comparison"))
    for argv, scope in (
        (["python3", "scripts/check_docs.py"], "Repository Markdown and report index checks"),
        (["python3", "tools/docgraph", "check"], "Repository documentation dependency checks"),
        (["git", "diff", "--check"], "Whitespace check for task changes"),
    ):
        commands.append(run(argv, None, scope))
    metadata = subprocess.run(
        [PYTHON, "-c", "import sys,networkx; print(sys.version); print('networkx',networkx.__version__)"],
        cwd=ROOT, capture_output=True, check=True).stdout.decode().strip()
    base = subprocess.run(["git", "rev-parse", "32c51fa"], cwd=ROOT,
                          capture_output=True, check=True).stdout.decode().strip()
    value = {
        "schema": "c44p-validation-v1",
        "base_commit": base,
        "branch": "task-c44p-screen",
        "worktree": str(ROOT),
        "python": PYTHON,
        "environment": metadata,
        "platform": platform.platform(),
        "research_job_ceiling": 16,
        "scientific_replay_execution": "Serial commands, one job per command",
        "new_source_search": False,
        "pre_restore_checks": prior,
        "commands": commands,
        "all_checks_passed": all(r["exit_code"] == 0 for r in commands),
        "artifacts_and_code_sha256": products(),
        "self_hash_omitted": "validation.json is excluded from its own digest map",
        "lean": "No Lean files changed; lake build was not run and no new Lean theorem is claimed",
        "publication": "Commit only on task-c44p-screen; no push or merge",
    }
    ledger.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    return 0 if value["all_checks_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
