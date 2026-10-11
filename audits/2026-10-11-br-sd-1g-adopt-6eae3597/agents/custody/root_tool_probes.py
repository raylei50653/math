#!/usr/bin/env python3
"""Isolated review probes of frozen new root tools; never modifies root tools."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
ROOT = AUDIT.parents[1]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    source = {}
    hashes = {}
    for name in ("verify.py", "record_check.py"):
        data = (AUDIT / name).read_bytes()
        source[name] = data
        hashes[name] = digest(data)
        archive = HERE / ("root-" + name + ".initial-review.v1.py")
        with archive.open("xb") as stream:
            stream.write(data)
    context = {"__file__": str(AUDIT / "verify.py"), "__name__": "root_tool_review_helper"}
    exec(compile(source["verify.py"], str(AUDIT / "verify.py"), "exec"), context)
    crafted_paths = {}
    for field in ("stdout", "stderr"):
        path = HERE / ("crafted-receipt." + field + ".log")
        with path.open("xb") as stream:
            stream.write(b"")
        crafted_paths[field + "_path"] = path.relative_to(AUDIT).as_posix()
        crafted_paths[field + "_sha256"] = digest(b"")
    results = []
    for label, argv, actual, expected in (
        ("wrong-command", ["/usr/bin/true"], 0, 0),
        ("self-declared-failure-success", ["/usr/bin/false"], 1, 1),
    ):
        crafted = {"argv": argv, "cwd": str(ROOT), "exit_code": actual,
                   "expected_exit_code": expected, "env_overrides": {}, **crafted_paths}
        try:
            context["receipt"](crafted)
            result = "accepted by receipt helper"
        except Exception as error:
            result = "rejected: " + str(error)
        results.append({"case": label, "synthetic_receipt": crafted, "result": result,
                        "scope": "local helper test; does not claim whole-audit acceptance"})
    sandbox = HERE / "logger-probe-sandbox" / "audit"
    sandbox.mkdir(parents=True)
    clone = sandbox / "record_check.py"
    with clone.open("xb") as stream:
        stream.write(source["record_check.py"])
    logs = sandbox / "logs"
    logs.mkdir()
    with (logs / "stale.stderr.log").open("xb") as stream:
        stream.write(b"pre-existing retained log\n")
    marker = sandbox / "command-executed.txt"
    command = [sys.executable, "-B", "-c", "from pathlib import Path; Path(" + repr(str(marker)) + ").write_text('executed despite stale output\\n')"]
    argv = [sys.executable, "-B", str(clone), "stale", *command]
    started = time.time()
    replay = subprocess.run(argv, cwd=ROOT, capture_output=True)
    receipt = {"argv": argv, "cwd": str(ROOT), "started_unix": started,
               "wall_seconds": time.time() - started, "exit_code": replay.returncode,
               "expected_exit_code": 1, "scope": "isolated verbatim logger copy; all effects in custody directory"}
    for field in ("stdout", "stderr"):
        data = getattr(replay, field)
        path = HERE / ("logger-stale-probe." + field + ".log")
        with path.open("xb") as stream:
            stream.write(data)
        receipt[field + "_path"] = path.relative_to(AUDIT).as_posix()
        receipt[field + "_sha256"] = digest(data)
    results.append({"case": "stale-log-preflight", "logger_exit_code": replay.returncode,
                    "command_marker_exists": marker.exists(),
                    "partial_stdout_exists": (logs / "stale.stdout.log").exists(),
                    "completed_receipt_exists": (logs / "stale.json").exists(),
                    "scope": "isolated verbatim logger copy"})
    value = {"root_tool_input_hashes": hashes, "results": results, "actual_replay_receipt": receipt}
    with (HERE / "ROOT_TOOL_PROBES.json").open("x") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps(value, sort_keys=True))

if __name__ == "__main__":
    main()
