#!/usr/bin/env python3
"""Save actual commands, complete streams and exit status inside this audit only."""
import argparse
import datetime
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--expect-exit', type=int, default=0)
    p.add_argument('log')
    p.add_argument('command', nargs=argparse.REMAINDER)
    args = p.parse_args()
    if not args.command:
        p.error('command required')
    target = (ROOT / args.log).resolve()
    if not target.is_relative_to(ROOT):
        p.error('log must be inside exclusive audit')
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        p.error('refuse to overwrite log')
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run(args.command, cwd=ROOT, capture_output=True, text=True)
    record = dict(command=args.command, cwd=str(ROOT), started_utc=started,
                  completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  stdout=r.stdout, stderr=r.stderr, exit_code=r.returncode,
                  expected_exit_code=args.expect_exit,
                  expected_exit_matched=r.returncode == args.expect_exit)
    with target.open('x') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps(dict(log=args.log, exit_code=r.returncode,
                         expected_exit_matched=r.returncode == args.expect_exit)))
    print(r.stdout, end='')
    print(r.stderr, end='', file=sys.stderr)
    return 0 if r.returncode == args.expect_exit else 1

if __name__ == '__main__':
    sys.exit(main())
