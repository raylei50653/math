#!/usr/bin/env python3
"""Supervision evidence only: inventory, BASE binding, logged read-only replay.

This script never imports worker checkers or decides a mathematical paper claim.
All outputs are exclusively created inside this supervision directory.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
BASE = "dc8e9aa7d6fccb51f63d30aa3f9c132296d44744"
WORKERS = {name: ROOT / f"audits/2026-10-09-n45-{name}" for name in ("pg", "pr", "pc")}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def put(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    data = value if isinstance(value, bytes) else (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(data)


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-optional-locks", *args], cwd=cwd)


def metadata(path):
    st = path.stat()
    return {"sha256": sha(path), "bytes": st.st_size, "mtime_ns": st.st_mtime_ns}


def payloads(root):
    result = set()
    for directory, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            p = Path(directory) / name
            if p.is_file():
                result.add(p.relative_to(root).as_posix())
    return result


def inventory(name, root):
    entries = {}
    for line in (root / "MANIFEST.sha256").read_text().splitlines():
        digest, rel = line.split("  ", 1)
        assert len(digest) == 64 and all(c in "0123456789abcdef" for c in digest)
        assert rel not in entries and not Path(rel).is_absolute() and ".." not in Path(rel).parts, rel
        entries[rel] = digest
    excluded = {"MANIFEST.sha256"}
    if name != "pg":
        excluded.add("delivery.json")
    assert payloads(root) == set(entries) | excluded, (name, "inventory mismatch")
    files = {rel: metadata(root / rel) for rel in sorted(set(entries) | excluded)}
    assert all(files[rel]["sha256"] == digest for rel, digest in entries.items()), name
    receipt = json.loads((root / "delivery.json").read_text())
    if "manifest_sha256" in receipt:
        assert files["MANIFEST.sha256"]["sha256"] == receipt["manifest_sha256"], name
    links = {}
    for directory, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d != ".git"]
        for item in dirs + names:
            p = Path(directory) / item
            if p.is_symlink():
                links[p.relative_to(root).as_posix()] = {"target": str(p.readlink()), "mtime_ns": p.lstat().st_mtime_ns}
    return {"manifest_entries": len(entries), "files": files, "symlinks": links}


def snapshot():
    workers = {name: inventory(name, root) for name, root in WORKERS.items()}
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    states = {}
    for name, root in WORKERS.items():
        source = root / ("source" if name == "pc" else "base-source")
        head = git("rev-parse", "HEAD", cwd=source).decode().strip()
        status = git("status", "--porcelain", cwd=source).decode()
        assert head == BASE and status == "", (name, head, status)
        states[name] = {"HEAD": head, "status": status}
    pr_inputs = json.loads((WORKERS["pr"] / "inputs.json").read_text())
    anchors = pr_inputs["anchors"]
    assert len(anchors) == 9
    for rel, digest in anchors.items():
        assert sha(ROOT / rel) == digest, ("live anchor", rel)
        for name, root in WORKERS.items():
            frozen = root / "frozen" / rel
            if frozen.exists():
                assert sha(frozen) == digest, (name, "frozen anchor", rel)
    dependencies = dict(pr_inputs["base_inputs"])
    supplement = json.loads((WORKERS["pr"] / "supplementary-inputs.json").read_text())
    dependencies.update({row["path"]: row for row in supplement["base_inputs"]})
    pc_inputs = json.loads((WORKERS["pc"] / "inputs.json").read_text())
    dependencies.update({row["path"]: row for row in pc_inputs["authority_files"]})
    base_bindings = {}
    for rel, record in sorted(dependencies.items()):
        blob = git("show", BASE + ":" + rel)
        digest = hashlib.sha256(blob).hexdigest()
        assert digest == record["sha256"], ("BASE declared hash", rel)
        for name, root in WORKERS.items():
            source = root / ("source" if name == "pc" else "base-source") / rel
            if source.exists():
                assert source.read_bytes() == blob, (name, "BASE bytes", rel)
        base_bindings[rel] = digest
    shared = set(anchors) | {"docs/HANDOFF.md", "docs/STATUS.md", "docs/c5_kempe_guide.md", "docs/c5_phase_b_common_lemmas.md", "artifacts/c5_excess_two_e4/REPORT.md", "docs/history/2026-10-09-n45-u-long-short-pair-tasks.md", "docs/history/2026-10-09-n2-45-54-parallel-tasks.md"}
    return {"BASE": BASE, "workers": workers, "source_states": states, "nine_anchors": anchors, "base_bindings": base_bindings,
            "shared_files": {rel: metadata(ROOT / rel) for rel in sorted(shared)}, "main_status": git("status", "--short").decode()}


def run(label, argv, seed17):
    assert label and all(c.isalnum() or c in "-_" for c in label)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if seed17:
        env["PYTHONHASHSEED"] = "17"
    start = time.monotonic()
    result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True)
    put("logs/" + label + ".stdout.log", result.stdout)
    put("logs/" + label + ".stderr.log", result.stderr)
    record = {"argv": argv, "cwd": str(ROOT), "PYTHONHASHSEED": env.get("PYTHONHASHSEED"), "actual_exit": result.returncode,
              "elapsed_seconds": round(time.monotonic() - start, 3)}
    put("logs/" + label + ".command.json", record)
    print(json.dumps({"label": label, **record, "stdout_tail": result.stdout.decode(errors="replace")[-1600:], "stderr_tail": result.stderr.decode(errors="replace")[-500:]}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["freeze", "run", "finalize"])
    parser.add_argument("--label")
    parser.add_argument("--seed17", action="store_true")
    parser.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.mode == "run":
        argv = args.argv[1:] if args.argv[:1] == ["--"] else args.argv
        assert argv
        run(args.label, argv, args.seed17)
        return
    current = snapshot()
    if args.mode == "freeze":
        put("inputs-before.json", current)
        print(json.dumps({"manifest_entries": {n: q["manifest_entries"] for n, q in current["workers"].items()}, "BASE_bindings": len(current["base_bindings"]), "anchors": 9}, sort_keys=True))
    else:
        before = json.loads((OUT / "inputs-before.json").read_text())
        put("inputs-after.json", current)
        for key in ("BASE", "workers", "source_states", "nine_anchors", "base_bindings", "shared_files"):
            assert before[key] == current[key], ("input drift", key)
        commands = {p.name.removesuffix(".command.json"): json.loads(p.read_text()) for p in sorted((OUT / "logs").glob("*.command.json"))}
        for label, record in commands.items():
            expected = 2 if label.startswith("pc-negative-") or label == "pc-valid-missing-LP" else 0
            assert record["actual_exit"] == expected, (label, record)
        for name in WORKERS:
            assert (OUT / f"logs/{name}-normal.stdout.log").read_bytes() == (OUT / f"logs/{name}-seed17.stdout.log").read_bytes(), (name, "normal/seed17 stdout drift")
        negative_index = json.loads((WORKERS["pc"] / "negative-inputs-v2/index.json").read_text())
        for item in negative_index:
            result = json.loads((OUT / ("logs/pc-negative-" + item["id"] + ".stdout.log")).read_text())
            assert result["source_contract"]["status"] == "counterexample"
            assert item["expected_error"] in result["source_contract"]["finding"]
        valid = json.loads((OUT / "logs/pc-valid-missing-LP.stdout.log").read_text())
        assert valid["source_contract"]["status"] == "not triggered" and valid["source_contract"]["missing_sufficient_premises"]
        put("checks.json", {"commands": commands, "worker_payloads_and_shared_inputs_unchanged": True,
                            "mathematical_adoption": "pending independent paper review", "LP_source_controls": "not triggered",
                            "scope": "exact inventories, BASE binding and worker fixed-domain replay; not an independent solver or arbitrary-size paper proof"})
        print(json.dumps({"commands": len(commands), "worker_payloads_and_shared_inputs_unchanged": True, "paper_adoption": "pending"}, sort_keys=True))


if __name__ == "__main__":
    main()
