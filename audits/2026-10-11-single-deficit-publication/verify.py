#!/usr/bin/env python3
"""Verify immutable A/B deliveries; optionally replay A against frozen BASE docs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = "4dd11f422c6fa49265a412085116b088786d0344"
A = Path("audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd")
B = Path("audits/2026-10-11-single-deficit-applicability-804e3b0b1b")
DOCS = ("docs/HANDOFF.md", "docs/STATUS.md", "docs/c5_weak_list_cores.md",
        "docs/c5_degree5_guide.md")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe(folder, name):
    path = folder / name
    if Path(name).is_absolute() or ".." in Path(name).parts:
        raise ValueError(f"unsafe relative path: {name}")
    if path.is_symlink() or not path.resolve().is_relative_to(folder.resolve()):
        raise ValueError(f"unsafe payload path: {name}")
    return path


def base_bytes(name):
    return subprocess.check_output(["git", "show", f"{BASE}:{name}"], cwd=ROOT)


def custody():
    expected = json.loads((HERE / "custody-before.json").read_text())
    assert expected["base"] == BASE
    actual = []
    for folder in (A, B):
        for path in sorted((ROOT / folder).rglob("*")):
            if path.is_symlink():
                raise ValueError(f"unexpected symlink: {path}")
            if path.is_file():
                actual.append({"path": str(path.relative_to(ROOT)),
                               "bytes": path.stat().st_size, "sha256": sha(path)})
    assert actual == expected["files"], "original A/B inventory or bytes changed"
    return len(actual)


def frozen_a():
    folder = ROOT / A
    count = 0
    for line in (folder / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert sha(safe(folder, name)) == digest, name
        count += 1
    inputs = json.loads((folder / "authority/input-hashes.json").read_text())
    for item in inputs:
        assert hashlib.sha256(base_bytes(item["path"])).hexdigest() == item["sha256"]
        assert sha(safe(folder / "authority/base", item["path"])) == item["sha256"]
    return {"payload_files": count, "frozen_base_documents": len(inputs)}


def run(command, env, expected=0, rejection=None):
    proc = subprocess.run([str(x) for x in command], cwd=ROOT, env=env,
                          capture_output=True, text=True)
    if proc.returncode != expected:
        raise RuntimeError(f"unexpected exit {proc.returncode}: {command}\n{proc.stderr}")
    if rejection and rejection not in proc.stdout + proc.stderr:
        raise RuntimeError(f"negative control missed expected rejection: {command}")
    return {"exit": proc.returncode, "expected_exit": expected}


def replay_a(env, seed17):
    python = ROOT / ".venv/bin/python"
    if not python.is_file():
        raise RuntimeError("A replay requires an existing Python with NetworkX 3.5; no packages are installed")
    with tempfile.TemporaryDirectory(prefix="math-single-deficit-base-") as temporary:
        overlay = Path(temporary)
        shutil.copytree(ROOT / A, overlay / A)
        for name in DOCS:
            path = safe(overlay, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(base_bytes(name))
        premise = overlay / A / "agents/premise_controls/replay.py"
        minor = overlay / A / "agents/existing_results_overlap/minor_controls.py"
        results = {"premise": run([python, "-B", premise, "--check"], env),
                   "minor": run([python, "-B", minor, "--check", "--seed",
                                 "17" if seed17 else "0"], env)}
        bad = overlay / A / "agents/premise_controls/corrupted-degree-certificate-v1.json"
        results["corrupted_premise"] = run(
            [python, "-B", premise, "--check", "--output", bad], env, 1,
            "saved full certificate differs from replay")
        return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--seed17", action="store_true")
    args = parser.parse_args()
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"],
                   cwd=ROOT, check=True)
    env = os.environ.copy()
    if args.seed17:
        env["PYTHONHASHSEED"] = "17"
    files = custody()
    result = {"status": "PASS", "base": BASE, "original_payload_files": files,
              "A": frozen_a(), "claim": "immutable delivery and frozen BASE bytes; no current-live equality claim"}
    b_command = [sys.executable, "-B", ROOT / B / "verify_audit.py", "--check"]
    if args.seed17:
        b_command.append("--seed17")
    result["B"] = run(b_command, env)
    if args.replay:
        result["frozen_base_overlay"] = replay_a(env, args.seed17)
        bad = ROOT / B / "literal_controls/bad-certificate-empty-fibre-dropped.json"
        result["corrupted_B"] = run(
            [sys.executable, "-B", ROOT / B / "literal_controls/check_literal_controls.py",
             "--check", "--certificate", bad], env, 1,
            "recomputed complete graph/lift/claim record differs")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
