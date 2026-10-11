#!/usr/bin/env python3
"""Read-only final repository identity and write-boundary receipt."""
import json
from pathlib import Path
import subprocess

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
PREFIX = AUDIT.relative_to(ROOT).as_posix() + '/'
BASE = 'c15a635e17d4be814e19aeeeeb765f3d6024099a'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode()

head, main = git('rev-parse', 'HEAD').strip(), git('rev-parse', 'main').strip()
tracked = git('diff', '--name-status')
staged = git('diff', '--cached', '--name-status')
status = git('status', '--porcelain=v1', '--untracked-files=all')
valid = all(line.startswith('?? ' + PREFIX) for line in status.splitlines())
if head != BASE or main != BASE or tracked or staged or not valid:
    raise SystemExit('write boundary or fixed base drift')
print(json.dumps({'base': BASE, 'head': head, 'main': main, 'origin_main': git('rev-parse', 'origin/main').strip(),
                  'tracked_diff': tracked, 'staged_diff': staged, 'only_new_audit_untracked': valid,
                  'new_untracked_file_count': len(status.splitlines()), 'status': status,
                  'formal_adoption_executed': False}, sort_keys=True))
