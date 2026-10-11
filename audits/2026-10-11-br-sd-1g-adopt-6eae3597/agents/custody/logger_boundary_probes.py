#!/usr/bin/env python3
"""Isolated verbatim logger copies with stale/broken/redirected outputs."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
ROOT = AUDIT.parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--input", type=Path, help="optional retained verbatim logger snapshot")
    args = parser.parse_args()
    if not args.label.replace("-", "").isalnum():
        raise ValueError("simple label required")
    source = (args.input or AUDIT / "record_check.py").read_bytes()
    archive = HERE / (args.label + "-logger-input.py")
    with archive.open("xb") as stream:
        stream.write(source)
    results = []
    for name in ("stale-log", "dangling-log-symlink", "directory-symlink"):
        sandbox = HERE / (args.label + "-" + name) / "audit"
        sandbox.mkdir(parents=True)
        copy = sandbox / "record_check.py"
        with copy.open("xb") as stream:
            stream.write(source)
        logs = sandbox / "logs"
        fixture = {"case": name}
        symlink = None
        if name == "directory-symlink":
            outside = sandbox.parent / "redirected-output"
            outside.mkdir()
            logs.symlink_to(outside, target_is_directory=True)
            symlink = logs
            fixture["symlink"] = {"path": str(logs), "target": str(outside)}
        else:
            logs.mkdir()
            if name == "stale-log":
                with (logs / "demo.stderr.log").open("xb") as stream:
                    stream.write(b"retained stale log\n")
            else:
                symlink = logs / "demo.stderr.log"
                missing = sandbox / "missing-output-target"
                symlink.symlink_to(missing)
                fixture["symlink"] = {"path": str(symlink), "target": str(missing)}
        marker = sandbox / "command-executed.txt"
        command = [sys.executable, "-B", "-c", "from pathlib import Path; Path(" + repr(str(marker)) + ").write_text('executed\\n')"]
        argv = [sys.executable, "-B", str(copy), "demo", *command]
        started = time.time()
        replay = subprocess.run(argv, cwd=ROOT, capture_output=True)
        row = {"case": name, "fixture": fixture, "argv": argv, "cwd": str(ROOT),
               "started_unix": started, "wall_seconds": time.time() - started,
               "exit_code": replay.returncode, "command_marker_exists": marker.exists(),
               "expected_condition": "nonzero exit before command execution",
               "expectation_met": replay.returncode != 0 and not marker.exists(),
               "scope": "verbatim isolated logger copy; all effects within custody"}
        for field in ("stdout", "stderr"):
            data = getattr(replay, field)
            path = HERE / (args.label + "-" + name + "." + field + ".log")
            with path.open("xb") as stream:
                stream.write(data)
            row[field + "_path"] = path.relative_to(AUDIT).as_posix()
            row[field + "_sha256"] = hashlib.sha256(data).hexdigest()
        # Runtime fixtures are replayable from this source and recorded targets;
        # no retained symlink can redirect the final audit's own custody scan.
        if symlink is not None:
            symlink.unlink()
        row["runtime_symlink_removed_after_probe"] = symlink is not None
        results.append(row)
    value = {"input_sha256": hashlib.sha256(source).hexdigest(), "cases": results,
             "all_expected_blocks": all(row["expectation_met"] for row in results)}
    with (HERE / (args.label + "-LOGGER_BOUNDARY_PROBES.json")).open("x") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps(value, sort_keys=True))

if __name__ == "__main__":
    main()
