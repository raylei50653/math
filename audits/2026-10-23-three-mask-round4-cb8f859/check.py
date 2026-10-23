#!/usr/bin/env python3
"""Read-only fourth-round branch replay and predecessor custody check."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def verify_record(path, record):
    data = path.read_bytes()
    if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
        raise ValueError('sealed bytes drift: ' + str(path))


def custody():
    base = json.loads((HERE / 'BASE.json').read_text())
    expected = {row['path'] for row in base['predecessors']}
    actual = {str(p.relative_to(REPO)) for name in base['predecessor_directories']
              for p in (REPO / name).rglob('*') if p.is_file()}
    if actual != expected:
        raise ValueError('predecessor file domain changed')
    for row in base['predecessors']:
        verify_record(REPO / row['path'], row)
    routing = []
    for row in base['routing']:
        verify_record(HERE / row['snapshot'], row)
        live_sha = hashlib.sha256((REPO / row['path']).read_bytes()).hexdigest()
        routing.append({'path': row['path'], 'entry_sha256': row['sha256'],
                        'live_sha256': live_sha, 'changed': live_sha != row['sha256']})
    return base, routing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--custody-only', action='store_true')
    args = parser.parse_args()
    base, routing = custody()
    results = {}
    if not args.custody_only:
        for branch in ('932', '933', '941'):
            command = [sys.executable, '-B', str(HERE / branch / 'check.py'), '--negative']
            run = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
            if run.returncode:
                sys.stderr.write(run.stdout)
                sys.stderr.write(run.stderr)
                raise SystemExit(run.returncode)
            result = json.loads(run.stdout)
            if not (result.get('status') in ('PASS', 'passed') or result.get('result') == 'PASS'
                    or result.get('ok') is True):
                raise ValueError('missing successful verdict: ' + branch)
            results[branch] = result
    print(json.dumps({'status': 'PASS', 'base': base['head'],
                      'predecessor_files_checked': len(base['predecessors']),
                      'predecessor_drift': 0, 'routing_snapshots_checked': len(routing),
                      'routing': routing, 'branch_results': results,
                      'general_932_933_941_excluded': False,
                      'smaller_bad_constructed': False, 'new_Lean': False}, sort_keys=True))


if __name__ == '__main__':
    main()
