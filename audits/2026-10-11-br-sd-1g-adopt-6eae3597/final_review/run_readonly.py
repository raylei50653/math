#!/usr/bin/env python3
"""Final peer replays; stores receipts only in this reviewer directory."""
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[1]
REL = AUDIT.relative_to(ROOT).as_posix()
COMMANDS = [
    ("precheck", ["python3", "-B", REL + "/verify.py", "--precheck"], {}),
    ("finite", ["python3", "-B", REL + "/controls/independent_finite.py", "--check", REL + "/controls/CERTIFICATE.json"], {}),
    ("finite-hashseed17", ["python3", "-B", REL + "/controls/independent_finite.py", "--check", REL + "/controls/CERTIFICATE.json"], {"PYTHONHASHSEED": "17"}),
    ("immutable", ["python3", "-B", REL + "/agents/custody/independent_immutable_check.py"], {}),
    ("diff-check", ["git", "diff", "--check"], {}),
    ("boundary", ["python3", "-B", REL + "/boundary_readback.py"], {}),
]

def run(command):
    label, argv, overrides = command
    env = {"PYTHONDONTWRITEBYTECODE": "1"} | overrides
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    p = subprocess.run(argv, cwd=ROOT, env=os.environ | env, capture_output=True)
    row = {"label": label, "argv": argv, "cwd": str(ROOT), "env_overrides": env,
           "started_utc": start, "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "exit_code": p.returncode, "expected_exit_code": 0}
    for field in ("stdout", "stderr"):
        data = getattr(p, field)
        path = HERE / (label + "." + field + ".log")
        with path.open("xb") as stream:
            stream.write(data)
        row[field + "_path"] = path.name
        row[field + "_sha256"] = hashlib.sha256(data).hexdigest()
    return row

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(run, COMMANDS))
    with (HERE / "RUNS.json").open("x") as stream:
        json.dump(rows, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"results": [{"label": r["label"], "exit_code": r["exit_code"]} for r in rows],
                      "finite_seed_stdout_equal": (HERE / "finite.stdout.log").read_bytes() == (HERE / "finite-hashseed17.stdout.log").read_bytes()}, sort_keys=True))
    raise SystemExit(0 if all(r["exit_code"] == 0 for r in rows) else 1)
