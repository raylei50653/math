#!/usr/bin/env python3
"""Capture one command in this exclusive closeout directory."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

here = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--label', required=True)
parser.add_argument('command', nargs=argparse.REMAINDER)
args = parser.parse_args()
assert args.label.replace('-', '').replace('_', '').isalnum()
command = args.command[1:] if args.command[:1] == ['--'] else args.command
assert command
paths = {kind: here / 'logs' / (args.label + '.' + kind) for kind in ('stdout.log', 'stderr.log', 'command.json')}
assert not any(p.exists() for p in paths.values())
started = time.monotonic()
result = subprocess.run(command, cwd=here.parent.parent, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
streams = {}
for kind, raw in [('stdout.log', result.stdout), ('stderr.log', result.stderr)]:
    with paths[kind].open('xb') as stream:
        stream.write(raw)
    streams[kind] = {'path': paths[kind].relative_to(here).as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
record = {'argv': command, 'cwd': str(here.parent.parent), 'exit_code': result.returncode,
          'elapsed_seconds': round(time.monotonic() - started, 3), 'streams': streams}
with paths['command.json'].open('x') as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
print(json.dumps({'label': args.label, 'exit_code': result.returncode, 'elapsed_seconds': record['elapsed_seconds'],
                  'stdout_bytes': len(result.stdout), 'stderr_bytes': len(result.stderr)}, sort_keys=True))
if result.returncode:
    print(result.stdout.decode(errors='replace')[:2600])
    print(result.stderr.decode(errors='replace')[:2600])
