#!/usr/bin/env python3
"""Execute a command and exclusive-create its stdout/stderr/exit metadata."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

HOME = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--cwd", type=Path, default=HOME.parent.parent)
    ap.add_argument("--seed")
    ap.add_argument("command", nargs=argparse.REMAINDER)
    args = ap.parse_args()
    cmd = args.command[1:] if args.command and args.command[0] == "--" else args.command
    paths = [HOME / "logs" / (args.name + suffix) for suffix in (".stdout.log", ".stderr.log", ".command.json")]
    # Reserve every output before executing a mutation or a check.
    streams = [p.open("xb") for p in paths]
    env = os.environ.copy()
    if args.seed is not None:
        env["PYTHONHASHSEED"] = args.seed
    start = time.monotonic()
    try:
        result = subprocess.run(cmd, cwd=args.cwd, env=env, capture_output=True)
        streams[0].write(result.stdout)
        streams[1].write(result.stderr)
        record = {"command": cmd, "cwd": str(args.cwd.resolve()), "environment": {"PYTHONHASHSEED": args.seed},
                  "exit": result.returncode, "seconds": round(time.monotonic() - start, 6),
                  "stdout": str(paths[0].relative_to(HOME)), "stderr": str(paths[1].relative_to(HOME))}
        streams[2].write((json.dumps(record, indent=2, sort_keys=True) + "\n").encode())
        print(json.dumps(record, sort_keys=True))
        return result.returncode
    finally:
        for stream in streams:
            stream.close()


if __name__ == "__main__":
    raise SystemExit(main())
