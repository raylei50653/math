#!/usr/bin/env python3
"""Exclusive log capture for this isolated audit; no mathematical proof oracle."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('label')
    parser.add_argument('--expected', type=int, default=0)
    parser.add_argument('--hash-seed', type=int)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command[:1] == ['--']:
        command = command[1:]
    if not command:
        parser.error('a command is required')
    if not args.label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in args.label):
        parser.error('label must use lowercase letters, digits and hyphens')
    logs = HERE / 'logs'
    logs.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    if args.hash_seed is not None:
        env['PYTHONHASHSEED'] = str(args.hash_seed)
    started = time.monotonic()
    with (logs / (args.label + '.stdout')).open('xb') as out:
        with (logs / (args.label + '.stderr')).open('xb') as err:
            result = subprocess.run(command, cwd=ROOT, env=env, stdout=out, stderr=err)
    receipt = {
        'command': command, 'cwd': str(ROOT), 'hash_seed': args.hash_seed,
        'exit_code': result.returncode, 'expected_exit_code': args.expected,
        'status': 'PASS' if result.returncode == args.expected else 'FAIL',
        'seconds': round(time.monotonic() - started, 3),
        'stdout': 'logs/' + args.label + '.stdout',
        'stderr': 'logs/' + args.label + '.stderr',
        'mathematical_proof_verifier': False,
    }
    with (logs / (args.label + '.json')).open('x') as stream:
        json.dump(receipt, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps(receipt, sort_keys=True))
    raise SystemExit(0 if receipt['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
