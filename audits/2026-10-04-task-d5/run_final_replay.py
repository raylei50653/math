#!/usr/bin/env python3
"""Root-owned final independent replay; record source stability and command logs."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

from audit_bundle import digest, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--owner', choices=('a4', 'b4', 'c4'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root, out = args.repo.resolve(), args.output.resolve()
    assert not out.exists(), 'Preserve every earlier replay'
    out.mkdir(parents=True)
    base = root / 'audits/2026-10-04-task-d5'
    sources = sorted((base / args.owner).glob('*.py'))
    before = {p.name: digest(p) for p in sources}
    command = ['python3', str(base / args.owner / ('audit_' + args.owner + '.py')),
               '--repo', str(base / 'snapshot'), '--output', str(out / 'audit')]
    env = os.environ.copy()
    env.pop('PYTHONHASHSEED', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    started = time.monotonic()
    proc = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True)
    (out / 'run.log').write_text(proc.stdout + proc.stderr)
    after = {p.name: digest(p) for p in sources}
    result = {'all_checks_passed': proc.returncode == 0 and before == after,
              'owner': args.owner, 'command': command, 'exit_code': proc.returncode,
              'hashseed': 'default', 'elapsed_seconds': time.monotonic() - started,
              'source_sha256_before': before, 'source_sha256_after': after,
              'sources_stable_during_replay': before == after}
    write(out / 'execution.json', result)
    print(json.dumps(result))
    assert result['all_checks_passed']


if __name__ == '__main__':
    main()
