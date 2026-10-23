#!/usr/bin/env python3
"""Capture a named read-only publication check without changing its exit status."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
label, *command = sys.argv[1:]
if not label.replace('-', '').isalnum() or not command:
    raise SystemExit('usage: run_local.py LABEL COMMAND [ARG ...]')
out = HERE / 'review' / 'local'
out.mkdir(parents=True, exist_ok=True)
started = time.monotonic()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
result = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, check=False)
(out / (label + '.stdout.txt')).write_bytes(result.stdout)
(out / (label + '.stderr.txt')).write_bytes(result.stderr)
record = dict(argv=command, exit_code=result.returncode,
              elapsed_seconds=round(time.monotonic() - started, 3),
              environment=dict(PYTHONDONTWRITEBYTECODE='1'))
(out / (label + '.json')).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(dict(label=label, **record)))
print(result.stdout.decode(errors='replace')[-1800:])
print(result.stderr.decode(errors='replace')[-1800:])
raise SystemExit(result.returncode)
