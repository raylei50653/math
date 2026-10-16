#!/usr/bin/env python3
"""Execute explicit read-only research replays with before/after custody checks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(plan, output):
    assert not output.exists(), 'exclusive output already exists'
    before = {name: digest(ROOT / name) for name in plan['immutable_files']}
    receipts = []
    for case in plan['cases']:
        env = os.environ.copy()
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        if case.get('seed17'):
            env['PYTHONHASHSEED'] = '17'
        start = time.monotonic()
        proc = subprocess.run(case['command'], cwd=ROOT, env=env,
                              text=True, capture_output=True, timeout=300)
        expected_success = case['expected'] == 'accept'
        receipts.append({**case, 'exit_code': proc.returncode,
                         'seconds': round(time.monotonic() - start, 3),
                         'stdout': proc.stdout, 'stderr': proc.stderr})
        assert (proc.returncode == 0) == expected_success, receipts[-1]
        print(case['name'] + ': ' + case['expected'], flush=True)
    after = {name: digest(ROOT / name) for name in plan['immutable_files']}
    assert before == after, 'read-only replay altered input'
    with output.open('x') as stream:
        json.dump({'status': 'PASS', 'plan': plan, 'receipts': receipts,
                   'hashes_before': before, 'hashes_after': after,
                   'input_drift': 0}, stream, indent=2)
        stream.write('\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    run(json.loads(args.plan.read_text()), args.output)


if __name__ == '__main__':
    main()
