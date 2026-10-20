#!/usr/bin/env python3
"""Read-only integrated replay; no source construction is inferred from PASS."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
checked = 0
for owner in (ROOT, ROOT/'B'):
    manifest = json.loads((owner/'INPUTS.json').read_text())
    assert manifest['base'] == 'e1617a2756813327d7ad333cfdd0fd92fa9efc38'
    for entry in manifest['files']:
        data = (owner/'frozen'/entry['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
        if entry['provenance'] == 'BASE':
            assert data == subprocess.check_output(
                ['git', 'show', manifest['base']+':'+entry['path']], cwd=REPO)
        if entry['path'].startswith('audits/'):
            assert data == (REPO/entry['path']).read_bytes(), entry['path']
        checked += 1

commands = [('kempe_consistency.py', '--check'), ('A/verify_kempe.py',),
            ('candidate_projection.py', '--check'), ('C/check.py', '--check'),
            ('C/review_kempe.py', '--check'), ('B/check.py', '--negative-control')]
results = []
for path, *arguments in commands:
    p = subprocess.run([sys.executable, '-B', str(ROOT/path), *arguments],
                       cwd=REPO, capture_output=True, text=True, check=True)
    results.append({'checker': path, 'exit_code': p.returncode,
                    'stdout': p.stdout.strip()})
print(json.dumps({'ok': True, 'input_records_checked': checked, 'frozen_drift': 0,
                  'checks': results, 'smaller_bad_source_constructed': False}))
