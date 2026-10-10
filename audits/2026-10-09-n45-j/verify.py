#!/usr/bin/env python3
"""Replays, provenance and supplied-source root-exchange regression checks."""
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HOME = Path(__file__).resolve().parent
ROOT = HOME.parents[1]
CHECKER = HOME / "checker.py"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def fingerprint(paths):
    return {str(p.relative_to(HOME)): {"sha256": sha256(p.read_bytes()).hexdigest(),
                                      "mtime_ns": p.stat().st_mtime_ns}
            for p in sorted(paths) if p.is_file()}


def run(logs, name, args, env=None, expected=0, expected_text=None):
    started = time.monotonic()
    result = subprocess.run(args, cwd=ROOT, env=env, text=True, capture_output=True)
    with (logs / (name + ".log")).open("x") as f:
        f.write("COMMAND: " + json.dumps(args, ensure_ascii=False) + "\n")
        f.write("STDOUT:\n" + result.stdout + "STDERR:\n" + result.stderr)
        f.write("EXIT: " + str(result.returncode) + "\n")
    need(result.returncode == expected, name + " unexpected exit")
    if expected_text:
        need(expected_text in result.stdout + result.stderr, name + " missing diagnostic")
    return {"id": name, "command": args, "cwd": str(ROOT), "exit": result.returncode,
            "expected_exit": expected, "seed": (env or os.environ).get("PYTHONHASHSEED", "unset"),
            "seconds": round(time.monotonic() - started, 4), "log": str((logs / (name + ".log")).relative_to(HOME)),
            "result": "expected rejection" if expected else "PASS"}


def main():
    logs = HOME / "logs"
    logs.mkdir(exist_ok=False)
    paths = [HOME / "inputs.json", HOME / "TASK.md", HOME / "checker.py"]
    paths += list((HOME / "frozen").rglob("*"))
    paths += list((HOME / "results").rglob("*"))
    paths += list((HOME / "source_examples").rglob("*"))
    paths += list((HOME / "source-example-results").rglob("*"))
    before = fingerprint(paths)
    commands = []
    base_args = [sys.executable, "-B", str(CHECKER)]
    commands.append(run(logs, "fixed-normal", base_args + ["--check", "--live-base", "/tmp/math-n45-j-dc8e9aa7"]))
    seed = dict(os.environ, PYTHONHASHSEED="17")
    commands.append(run(logs, "fixed-seed17", base_args + ["--check", "--live-base", "/tmp/math-n45-j-dc8e9aa7"], seed))
    source = HOME / "source_examples/NA7-0002-named-root-swap.json"
    source_args = ["--source", str(source.relative_to(ROOT)), "--out", str((HOME / "source-example-results").relative_to(ROOT))]
    commands.append(run(logs, "source-normal", base_args + ["--check"] + source_args))
    commands.append(run(logs, "source-seed17", base_args + ["--check"] + source_args, seed))
    commands.append(run(logs, "exclusive-create-refusal", base_args, expected=1, expected_text="File exists"))
    after = fingerprint(paths)
    need(before == after, "read-only replay or refused generation changed input/output bytes or mtime")
    source_certificate = json.loads((HOME / "source-example-results/certificate.json").read_text())
    certificate = json.loads((HOME / "results/certificate.json").read_text())
    original = next(r for r in certificate["N2"] if r["id"] == "NA7-0002")
    named = source_certificate["records"][0]
    need(original["original"]["sigma"] == named["original"]["sigma"], "root exchange changes Sigma")
    compared_pairs = 0
    for row, swapped in zip(original["original"]["rows"], named["original"]["rows"]):
        need({tuple(p) for p in row["root_pairs"]} == {(p[1], p[0]) for p in swapped["root_pairs"]},
             "named root swap does not transpose complete relation")
        for r, name in ((5, "z"), (6, "w")):
            need(row["sides"][str(r)]["E"] == swapped["sides"][name]["E"], "named side E changes")
        compared_pairs += 16
    collision = next(x for x in original["collisions"]["records"] if x["kind"] == "shared_coordinate")
    p = next(p for p in original["pieces"] if p["id"] == collision["piece"])
    rel = original["relations"][collision["index"]][p["id"]]
    a, b = collision["pins"]
    need(not rel["fibres"][4 * a + b]["tuple_indices"], "diagnostic unexpectedly has a joint lift")
    t0, t1 = [rel["tuples"][i]["tuple"] for i in collision["incompatible_side_tuple_indices"]]
    need(any(t0[p["contact_order"].index(v)] != t1[p["contact_order"].index(v)] for v in p["shared_contacts"]),
         "shared-coordinate diagnostic does not expose shared literal disagreement")
    # Deliberately corrupt a new comparison copy, leaving fixed evidence unchanged.
    bad = HOME / "negative-replay"
    bad.mkdir(exist_ok=False)
    for name in ("certificate.json", "inventory.json"):
        (bad / name).symlink_to(Path("..") / "results" / name)
    altered = json.loads((HOME / "results/coverage.json").read_text())
    altered["N2"]["original_root_pair_queries"] += 1
    with (bad / "coverage.json").open("x") as f:
        json.dump(altered, f, sort_keys=True, ensure_ascii=False, indent=2)
        f.write("\n")
    commands.append(run(logs, "corrupted-certificate-refusal", base_args + ["--check", "--out", str(bad)],
                        expected=1, expected_text="certificate byte/payload drift: coverage.json"))
    need(before == fingerprint(paths), "negative replay changed frozen artifacts")
    live_manifest = json.loads((HOME / "inputs.json").read_text())
    drift = [x["path"] for x in live_manifest["files"]
             if sha256((Path(live_manifest["input_worktree"]) / x["path"]).read_bytes()).hexdigest() != x["sha256"]]
    need(not drift, "BASE inputs changed")
    input_status = subprocess.check_output(["git", "status", "--porcelain"],
                                            cwd=live_manifest["input_worktree"], text=True)
    need(not input_status, "independent input worktree changed")
    checks = {"task": "N45-J", "BASE": live_manifest["BASE"], "actual_HEAD": live_manifest["actual_HEAD"],
              "commands": commands, "read_only_replay": {"status": "PASS", "checked_files": len(before),
              "bytes_and_mtime_before_after_equal": True, "fingerprints": before},
              "source_interface": {"status": "PASS", "original_graph": "NA7-0002", "new_graph_search": False,
              "named_root_swap_transpose_queries": compared_pairs, "shared_coordinate_diagnostic": collision},
              "input_zero_byte_drift": {"status": "PASS", "paths": len(live_manifest["files"]), "changed": drift,
                                        "input_worktree_git_status": input_status},
              "not_run": [{"item": "Lean/lake build/axioms", "reason": "no new Lean; finite Python task"},
                          {"item": "E3/E4/E4C/ES/ER or U1-U4 full enumeration", "reason": "fixed source input and independent checker only"},
                          {"item": "S/U candidate checks", "reason": "no returned named new source graph or frozen claims"},
                          {"item": "whole-repository documentation checks", "reason": "writes restricted to N45-J audit; shared documentation unchanged"}],
              "initial_generation": [{"command": "python3 -B audits/2026-10-09-n45-j/checker.py --live-base /tmp/math-n45-j-dc8e9aa7",
                                      "exit": 0, "log": "tool output; later fixed-normal.log replays the identical bytes"},
                                     {"command": "python3 -B audits/2026-10-09-n45-j/checker.py --source audits/2026-10-09-n45-j/source_examples/NA7-0002-named-root-swap.json --out audits/2026-10-09-n45-j/source-example-results",
                                      "exit": 0, "log": "tool output; later source-normal.log replays the identical bytes"}]}
    with (HOME / "checks.json").open("x") as f:
        json.dump(checks, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")
    print(json.dumps({"status": "PASS", "replays": 4, "expected_rejections": 2,
                      "unchanged_fingerprints": len(before), "input_drift": drift,
                      "root_swap_queries": compared_pairs}))


if __name__ == "__main__":
    main()
