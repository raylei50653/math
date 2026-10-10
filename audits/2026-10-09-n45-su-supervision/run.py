#!/usr/bin/env python3
"""Preserve a read-only command's exact outcome in this fresh supervisor folder."""
import argparse
import datetime
import json
import os
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
p = argparse.ArgumentParser()
p.add_argument('--name', required=True)
p.add_argument('--seed17', action='store_true')
p.add_argument('command', nargs=argparse.REMAINDER)
a = p.parse_args()
cmd = a.command[1:] if a.command and a.command[0] == '--' else a.command
(OUT / 'logs').mkdir(exist_ok=True)
paths = {k: OUT / 'logs' / (a.name + '.' + k) for k in ('stdout.log', 'stderr.log', 'json')}
handles = {k: path.open('x') for k, path in paths.items()}
overrides = {'PYTHONDONTWRITEBYTECODE': '1'}
if a.seed17:
    overrides['PYTHONHASHSEED'] = '17'
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
r = subprocess.run(cmd, cwd=ROOT, env=dict(os.environ, **overrides),
                   stdout=handles['stdout.log'], stderr=handles['stderr.log'])
record = dict(argv=cmd, cwd=str(ROOT), env_overrides=overrides, exit_code=r.returncode,
              started_UTC=started, finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              stdout=str(paths['stdout.log'].relative_to(OUT)), stderr=str(paths['stderr.log'].relative_to(OUT)))
json.dump(record, handles['json'], sort_keys=True, indent=2)
handles['json'].write('\n')
for h in handles.values():
    h.close()
print(json.dumps(record, sort_keys=True))
raise SystemExit(r.returncode)
