#!/usr/bin/env python3
"""Run an audit command, retaining exclusive logs and exit status."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--seed17', action='store_true')
parser.add_argument('name')
parser.add_argument('command', nargs=argparse.REMAINDER)
args = parser.parse_args()
base = Path(__file__).resolve().parents[1]
root = base.parents[1]
env = os.environ.copy()
if args.seed17:
    env['PYTHONHASHSEED'] = '17'
proc = subprocess.run(args.command, cwd=root, env=env, text=True, capture_output=True)
for suffix, value in [('stdout.log', proc.stdout), ('stderr.log', proc.stderr)]:
    with (base / 'logs' / (args.name + '.' + suffix)).open('x') as stream:
        stream.write(value)
row = {'name': args.name, 'command': args.command,
       'env': {'PYTHONHASHSEED': '17'} if args.seed17 else {},
       'exit_code': proc.returncode,
       'stdout': args.name + '.stdout.log', 'stderr': args.name + '.stderr.log'}
with (base / 'logs' / (args.name + '.receipt.json')).open('x') as stream:
    json.dump(row, stream, indent=2)
    stream.write('\n')
print(json.dumps(row))
print(proc.stdout[:2000], end='')
if proc.returncode:
    print(proc.stderr[-2000:], end='')
raise SystemExit(proc.returncode)
