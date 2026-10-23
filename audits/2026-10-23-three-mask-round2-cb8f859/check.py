#!/usr/bin/env python3
"""Read-only second-round replay, including sealed predecessor custody."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def main():
    entry = json.loads((HERE / 'BASE.json').read_text())
    for record in entry['predecessor_files']:
        data = (REPO / record['path']).read_bytes()
        if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
            raise ValueError('sealed predecessor drift: ' + record['path'])
    routing = entry['entry_documents'] + json.loads((HERE / 'ADDITIONAL_ROUTING_ENTRY.json').read_text())
    for record in routing:
        data = (HERE / 'entry-snapshot' / record['path']).read_bytes()
        if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
            raise ValueError('routing snapshot drift: ' + record['path'])
    results = {}
    for branch, options in (('932', ['--check', '--negative']),
                            ('933', ['--negative']), ('941', [])):
        command = [sys.executable, '-B', str(HERE / branch / 'check.py'), *options]
        run = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
        if run.returncode:
            sys.stderr.write(run.stderr)
            raise SystemExit(run.returncode)
        result = json.loads(run.stdout)
        if not (result.get('status') == 'PASS' or result.get('result') == 'PASS' or result.get('ok') is True):
            raise ValueError('missing successful verdict: ' + branch)
        results[branch] = result
    print(json.dumps({'base': entry['base'], 'predecessor_files_checked': len(entry['predecessor_files']),
                      'predecessor_drift': 0, 'routing_snapshots_checked': len(routing),
                      'branch_results': results, 'general_932_933_941_excluded': False,
                      'smaller_bad_constructed': False, 'new_Lean': False}, sort_keys=True))


if __name__ == '__main__':
    main()
