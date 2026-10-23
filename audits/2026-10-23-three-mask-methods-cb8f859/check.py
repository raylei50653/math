#!/usr/bin/env python3
"""Read-only replay of the three separate named-source audits."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def main():
    base = json.loads((HERE / 'BASE.json').read_text())
    for record in base['entry_files']:
        frozen = (HERE / 'entry-snapshot' / record['path']).read_bytes()
        if len(frozen) != record['bytes'] or hashlib.sha256(frozen).hexdigest() != record['sha256']:
            raise ValueError('entry snapshot drift: ' + record['path'])
    results = {}
    for branch, options in (('932', ['--check', '--negative']),
                            ('933', ['--negative']), ('941', [])):
        command = [sys.executable, '-B', str(HERE / branch / 'check.py'), *options]
        completed = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
        if completed.returncode:
            sys.stderr.write(completed.stderr)
            raise SystemExit(completed.returncode)
        result = json.loads(completed.stdout)
        if not (result.get('status') == 'PASS' or result.get('result') == 'PASS' or result.get('ok') is True):
            raise ValueError('missing successful verdict: ' + branch)
        results[branch] = result
    print(json.dumps({'base': base['base'], 'entry_snapshots_verified': 4,
                      'branch_results': results,
                      'general_source_exclusions_claimed': False,
                      'smaller_bad_constructed': False, 'new_Lean': False}, sort_keys=True))


if __name__ == '__main__':
    main()
