#!/usr/bin/env python3
"""Read-only replay of frozen authority and the fixed full-fibre certificate."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
manifest = json.loads((ROOT / 'INPUTS.json').read_text())
assert manifest['base'] == 'e1617a2756813327d7ad333cfdd0fd92fa9efc38'
assert manifest['initial_status'] == 'clean'
assert len({entry['path'] for entry in manifest['files']}) == len(manifest['files'])
for entry in manifest['files']:
    frozen = (ROOT / 'frozen' / entry['path']).read_bytes()
    assert hashlib.sha256(frozen).hexdigest() == entry['sha256'], entry['path']
    tracked = subprocess.check_output(
        ['git', 'show', manifest['base'] + ':' + entry['path']], cwd=REPO)
    assert tracked == frozen, entry['path']
    # Routing changes are permitted; old mathematical evidence remains unchanged.
    if entry['path'].startswith('audits/'):
        assert (REPO / entry['path']).read_bytes() == frozen, entry['path']
completed = subprocess.run(
    [sys.executable, '-B', str(ROOT / 'C/check.py'), '--check'],
    cwd=REPO, text=True, capture_output=True, check=True)
result = json.loads(completed.stdout)
assert result['ok']
assert result['target_source_realized'] is False
print(json.dumps({'ok': True, 'base': manifest['base'],
                  'frozen_inputs': len(manifest['files']), 'frozen_drift': 0,
                  'fixed_control': result}, sort_keys=True))
