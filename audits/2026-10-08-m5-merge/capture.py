#!/usr/bin/env python3
"""Capture M5 commands in fresh paths without rewriting prior evidence."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

folder = Path(__file__).resolve().parent
label, *argv = sys.argv[1:]
target = folder / "commands" / label
target.mkdir(parents=True, exist_ok=False)
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
start = time.monotonic()
proc = subprocess.run(argv, cwd="/home/ray/developer/ai/math", capture_output=True)
logs = {}
for stream in ("stdout", "stderr"):
    raw = getattr(proc, stream)
    name = stream + ".log"
    (target / name).write_bytes(raw)
    logs[stream] = {"path": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
record = {"label": label, "argv": argv, "cwd": "/home/ray/developer/ai/math",
          "started_utc": started, "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "seconds": time.monotonic() - start, "exit_code": proc.returncode, "logs": logs}
(target / "command.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(record, ensure_ascii=False))
for stream in ("stdout", "stderr"):
    raw = getattr(proc, stream)
    sink = getattr(sys, stream)
    if len(raw) > 4000:
        sink.write(raw[:1000].decode(errors="replace") + "\n[console preview; complete bytes saved in command logs]\n")
    else:
        sink.write(raw.decode(errors="replace"))
sys.exit(proc.returncode)
