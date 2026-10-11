#!/usr/bin/env python3
"""Exclusive command receipts within this audit; no shell interpolation."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seed17', action='store_true')
    p.add_argument('--expected', type=int, default=0)
    p.add_argument('--postseal', action='store_true')
    p.add_argument('label')
    p.add_argument('argv', nargs=argparse.REMAINDER)
    a = p.parse_args()
    if not re.fullmatch(r'[a-z0-9-]+', a.label) or not a.argv:
        p.error('label must be simple and argv nonempty')
    directory = AUDIT / ('postseal' if a.postseal else 'logs')
    if directory.is_symlink() or not directory.resolve().is_relative_to(AUDIT):
        p.error('receipt directory is a symlink or escapes audit; command was not run')
    directory.mkdir(exist_ok=True)
    receipt = directory / (a.label + '.json')
    planned = [receipt] + [directory / (a.label + '.' + field + '.log') for field in ('stdout', 'stderr')]
    if any(path.exists() or path.is_symlink() for path in planned):
        p.error('receipt or log already exists; command was not run')
    environment = dict(os.environ)
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    if a.seed17:
        environment['PYTHONHASHSEED'] = '17'
    start = datetime.datetime.now(datetime.timezone.utc)
    result = subprocess.run(a.argv, cwd=ROOT, env=environment, capture_output=True)
    record = {'argv': a.argv, 'cwd': str(ROOT),
              'env_overrides': {'PYTHONDONTWRITEBYTECODE': '1'} | ({'PYTHONHASHSEED': '17'} if a.seed17 else {}),
              'started_utc': start.isoformat(),
              'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'exit_code': result.returncode, 'expected_exit_code': a.expected}
    for field in ('stdout', 'stderr'):
        data = getattr(result, field)
        path = directory / (a.label + '.' + field + '.log')
        with path.open('xb') as stream:
            stream.write(data)
        record[field + '_path'] = path.relative_to(AUDIT).as_posix()
        record[field + '_sha256'] = hashlib.sha256(data).hexdigest()
    with receipt.open('x') as stream:
        json.dump(record, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'receipt': receipt.relative_to(AUDIT).as_posix(),
                      'actual_exit': result.returncode, 'expected_exit': a.expected,
                      'expectation_met': result.returncode == a.expected}, sort_keys=True))
    if result.stdout:
        sys.stdout.buffer.write(result.stdout)
    if result.stderr:
        sys.stderr.buffer.write(result.stderr)
    return 0 if result.returncode == a.expected else 1

if __name__ == '__main__':
    raise SystemExit(main())
