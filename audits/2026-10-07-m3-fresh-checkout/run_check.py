#!/usr/bin/env python3
"""Record one fresh-checkout M3 command without changing its saved inputs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', type=Path, default=Path('/tmp/math-m3-ba0b447'))
    parser.add_argument('--name', required=True)
    parser.add_argument('--env', action='append', default=[])
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        parser.error('a command is required')
    output = Path(__file__).resolve().parent
    env = os.environ.copy()
    overrides = dict(value.split('=', 1) for value in args.env)
    env.update(overrides)
    record_path = output / 'commands' / (args.name + '.json')
    record_path.parent.mkdir(exist_ok=True)
    stdout = output / 'logs' / (args.name + '.stdout.log')
    stderr = output / 'logs' / (args.name + '.stderr.log')
    started = time.time()
    monotonic = time.monotonic()
    with stdout.open('xb') as out, stderr.open('xb') as err:
        result = subprocess.run(command, cwd=args.checkout, env=env, stdout=out, stderr=err)
    record = {'name': args.name, 'argv': command, 'cwd': str(args.checkout),
              'environment_overrides': overrides, 'started_unix': started,
              'exit_code': result.returncode, 'seconds': round(time.monotonic() - monotonic, 3),
              'logs': [{'path': str(p.relative_to(output)), 'bytes': p.stat().st_size,
                        'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                       for p in (stdout, stderr)]}
    with record_path.open('x') as stream:
        json.dump(record, stream, indent=2)
        stream.write('\n')
    print(json.dumps(record), flush=True)
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
