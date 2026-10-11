#!/usr/bin/env python3
"""Record a publication command without modifying frozen deliveries."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

here = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--label', required=True)
parser.add_argument('--cwd', type=Path, default=here.parent.parent)
parser.add_argument('command', nargs=argparse.REMAINDER)
args = parser.parse_args()
assert args.label.replace('-', '').isalnum()
command = args.command[1:] if args.command[:1] == ['--'] else args.command
assert command
target = here / (args.label + '.json')
assert not target.exists()
started = time.monotonic()
result = subprocess.run(command, cwd=args.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
record = {'argv': command, 'cwd': str(args.cwd), 'exit_code': result.returncode,
          'elapsed_seconds': round(time.monotonic() - started, 3)}
for name, raw in [('stdout', result.stdout), ('stderr', result.stderr)]:
    record[name] = raw.decode('utf-8')
    record[name + '_bytes'] = len(raw)
    record[name + '_sha256'] = hashlib.sha256(raw).hexdigest()
with target.open('x') as stream:
    stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
print(json.dumps({'label': args.label, 'exit_code': result.returncode,
                  'elapsed_seconds': record['elapsed_seconds'], 'stdout_bytes': len(result.stdout),
                  'stderr_bytes': len(result.stderr)}, sort_keys=True))
if result.returncode:
    print(record['stdout'][:1600])
    print(record['stderr'][:1600])
