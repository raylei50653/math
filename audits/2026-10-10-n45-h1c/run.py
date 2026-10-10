#!/usr/bin/env python3
"""Exclusive actual-command log writer confined to this audit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seed17', action='store_true')
    p.add_argument('--expected-exit', type=int, default=0)
    p.add_argument('--stage')
    p.add_argument('label')
    p.add_argument('command', nargs=argparse.REMAINDER)
    a = p.parse_args()
    assert a.label and all(x.isalnum() or x == '-' for x in a.label)
    assert a.command
    env = os.environ.copy()
    environment = {'PYTHONHASHSEED': '17'} if a.seed17 else {}
    env.update(environment)
    result = subprocess.run(a.command, cwd=ROOT, env=env, capture_output=True)
    folder = HERE / 'logs'
    folder.mkdir(exist_ok=True)
    d = dict(id=a.label, command=a.command, cwd=str(ROOT), environment=environment,
             actual_exit=result.returncode, expected_exit=a.expected_exit,
             expected_rejection_stage=a.stage)
    for stream in ('stdout', 'stderr'):
        data = getattr(result, stream)
        filename = 'logs/' + a.label + '.' + stream + '.txt'
        with (HERE / filename).open('xb') as f:
            f.write(data)
        d[stream + '_file'] = filename
        d[stream + '_sha256'] = hashlib.sha256(data).hexdigest()
    if a.stage:
        reject = json.loads(result.stderr)
        d['observed_rejection_stage'] = reject['stage']
        d['rejection_stage_matches'] = reject['stage'] == a.stage
    with (folder / (a.label + '.json')).open('x') as f:
        f.write(json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
    print(json.dumps(d, sort_keys=True))
    return 0 if result.returncode == a.expected_exit and d.get('rejection_stage_matches', True) else 1


if __name__ == '__main__':
    sys.exit(main())
