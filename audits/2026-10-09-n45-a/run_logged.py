#!/usr/bin/env python3
"""Run one command and exclusively preserve its log and metadata."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--label', required=True)
p.add_argument('--cwd', default='/tmp/math-n45-a-20261009')
p.add_argument('--seed')
p.add_argument('command', nargs=argparse.REMAINDER)
a = p.parse_args()
command = a.command[1:] if a.command[:1] == ['--'] else a.command
assert command and '/' not in a.label
log = HERE / 'logs' / (a.label + '.log')
meta = HERE / 'logs' / (a.label + '.json')
assert not log.exists() and not meta.exists()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
if a.seed is not None:
    env['PYTHONHASHSEED'] = a.seed
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t = time.monotonic()
r = subprocess.run(command, cwd=a.cwd, env=env, stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT)
with log.open('xb') as f:
    f.write(r.stdout)
record = {'command': command, 'cwd': a.cwd, 'started_utc': started,
          'exit': r.returncode, 'elapsed_seconds': round(time.monotonic() - t, 3),
          'PYTHONHASHSEED': env.get('PYTHONHASHSEED'),
          'PYTHONDONTWRITEBYTECODE': '1', 'log': str(log.relative_to(HERE)),
          'log_sha256': hashlib.sha256(r.stdout).hexdigest()}
with meta.open('x') as f:
    json.dump(record, f, indent=2, sort_keys=True)
    f.write('\n')
print(json.dumps(record, sort_keys=True))
print(r.stdout.decode(errors='replace')[-3000:])
sys.exit(r.returncode)
