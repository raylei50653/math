#!/usr/bin/env python3
"""Record only read-only documentation checks; all logs stay in this audit."""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE_CHECKOUT = ROOT / 'audits/2026-10-10-n45-s-low1/base-source'


def main():
    definitions = [
        ('current-doc-links', ROOT, [sys.executable, '-B', 'scripts/check_docs.py'], 0),
        ('current-formal-docgraph', ROOT, [sys.executable, '-B', 'tools/docgraph', '--include', 'docs/**/*.md', 'check'], 0),
        ('retained-BASE-doc-links', BASE_CHECKOUT, [sys.executable, '-B', 'scripts/check_docs.py'], 1),
        ('retained-BASE-formal-docgraph', BASE_CHECKOUT, [sys.executable, '-B', 'tools/docgraph', '--include', 'docs/**/*.md', 'check'], 0),
        ('current-whole-docgraph', ROOT, [sys.executable, '-B', 'tools/docgraph', 'check'], 1),
        ('tracked-diff-check', ROOT, ['git', 'diff', '--check'], 0),
        ('cached-diff-check', ROOT, ['git', 'diff', '--cached', '--check'], 0),
    ]
    records = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for name, cwd, command, expected in definitions:
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True)
        for stream in ('stdout', 'stderr'):
            with (HERE / f'logs/{name}.{stream}.log').open('xb') as f:
                f.write(getattr(result, stream))
        records.append({'name': name, 'cwd': str(cwd), 'command': command,
                        'exit_code': result.returncode, 'expected_exit': expected,
                        'stdout': f'logs/{name}.stdout.log', 'stderr': f'logs/{name}.stderr.log'})
        print(json.dumps({'name': name, 'exit_code': result.returncode, 'expected_exit': expected}), flush=True)
    data = {'task': 'N45-S-LOW2', 'commands': records,
            'BASE_check_boundary': 'Read-only retained LOW1 BASE checkout, not a new full checkout; four named mathematical BASE blobs independently frozen and verified.',
            'finite_source_controls': 'not established; not executed; no trigger count',
            'lake_build': 'not run: no new Lean and exclusive audit boundary',
            'E4_provenance_replay': 'historical FAIL retained; not rerun',
            'sealed_results': 'receipt.json bound by delivery.json; no historical receipt pointer'}
    with (HERE / 'checks.json').open('x') as f:
        json.dump(data, f, indent=2, sort_keys=True); f.write('\n')
    return 0 if all(r['exit_code'] == r['expected_exit'] for r in records) else 1


if __name__ == '__main__':
    sys.exit(main())
