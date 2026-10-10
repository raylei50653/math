#!/usr/bin/env python3
"""Exclusive stdout/stderr/exit receipts. Writes only within this audit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--seed17', action='store_true')
    p.add_argument('name')
    p.add_argument('command', nargs=argparse.REMAINDER)
    a = p.parse_args()
    if not a.command or '/' in a.name or a.name in {'.', '..'}:
        p.error('safe log name and command required')
    targets = [OUT / 'logs' / (a.name + s) for s in
               ['.stdout.txt', '.stderr.txt', '.receipt.json']]
    if any(t.exists() for t in targets):
        raise SystemExit('STOP: existing log')
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    if a.seed17:
        env['PYTHONHASHSEED'] = '17'
    r = subprocess.run(a.command, cwd=ROOT, env=env, capture_output=True)
    for t, b in zip(targets[:2], [r.stdout, r.stderr]):
        with t.open('xb') as f:
            f.write(b)
    receipt = {'command': a.command, 'cwd': str(ROOT), 'exit': r.returncode,
               'environment': {k: env[k] for k in
                               ['PYTHONDONTWRITEBYTECODE', 'GIT_OPTIONAL_LOCKS']},
               'stdout_sha256': hashlib.sha256(r.stdout).hexdigest(),
               'stderr_sha256': hashlib.sha256(r.stderr).hexdigest()}
    if a.seed17:
        receipt['environment']['PYTHONHASHSEED'] = '17'
    with targets[2].open('x') as f:
        json.dump(receipt, f, sort_keys=True, indent=2)
        f.write('\n')
    print(json.dumps({'log': a.name, 'exit': r.returncode}, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
