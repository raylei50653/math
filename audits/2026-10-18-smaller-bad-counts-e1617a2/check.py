#!/usr/bin/env python3
"""Read-only connected replay; mathematical source realizability stays OPEN."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
manifest = json.loads((ROOT / 'INPUTS.json').read_text())
assert manifest['base'] == 'e1617a2756813327d7ad333cfdd0fd92fa9efc38'
paths = [entry['path'] for entry in manifest['files']]
assert len(paths) == len(set(paths)) == 89
for entry in manifest['files']:
    frozen = (ROOT / 'frozen' / entry['path']).read_bytes()
    assert hashlib.sha256(frozen).hexdigest() == entry['sha256'], entry['path']
    if entry['path'].startswith(('audits/', 'artifacts/')):
        assert frozen == (REPO / entry['path']).read_bytes(), entry['path']

commands = [
    ('frozen/audits/2026-10-18-smaller-bad-e1617a2/A/verify_kempe.py',),
    ('A/count_cone.py', '--check'),
    ('A/check_941.py',),
    ('B/check.py',),
    ('C/check.py', '--negative-controls'),
]
results = []
for name, *args in commands:
    result = subprocess.run([sys.executable, '-B', str(ROOT / name), *args],
                            cwd=REPO, capture_output=True, text=True)
    if result.returncode:
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit(result.returncode)
    results.append({'checker': name, 'exit_code': result.returncode,
                    'stdout': result.stdout.strip()})
print(json.dumps({'ok': True, 'frozen_inputs_checked': len(paths),
                  'frozen_drift': 0, 'checks': results,
                  'source932_all_three_candidates_in_K132': True,
                  'source932_933_four_row_candidate_route_excluded': True,
                  'source941_four_row_candidate_route': 'OPEN',
                  'smaller_bad_source_constructed': False}))
