#!/usr/bin/env python3
"""Run a read-only audit command with exclusive-create command/output logs."""
import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HOME = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed17', action='store_true')
    ap.add_argument('label')
    ap.add_argument('command', nargs=argparse.REMAINDER)
    args = ap.parse_args()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    if args.seed17:
        env['PYTHONHASHSEED'] = '17'
    command = args.command
    if command[:1] == ['--']:
        command = command[1:]
    paths = [HOME / 'logs' / (args.label + suffix) for suffix in ('.stdout.log', '.stderr.log', '.command.json')]
    streams = [p.open('xb') for p in paths]
    started = time.monotonic()
    result = subprocess.run(command, cwd=HOME.parent.parent, env=env, stdout=streams[0], stderr=streams[1])
    metadata = {'argv': command, 'cwd': str(HOME.parent.parent), 'exit_code': result.returncode,
                'elapsed_seconds': time.monotonic() - started, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'env': {'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONHASHSEED': env.get('PYTHONHASHSEED')},
                'stdout': str(paths[0].relative_to(HOME)), 'stderr': str(paths[1].relative_to(HOME))}
    streams[2].write((json.dumps(metadata, sort_keys=True, indent=2) + '\n').encode())
    for stream in streams:
        stream.close()
    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
