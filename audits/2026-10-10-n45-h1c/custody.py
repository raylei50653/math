#!/usr/bin/env python3
"""Intake/final custody check; original untracked tree is outside this scope."""
import hashlib
import json
from pathlib import Path
import subprocess
import checker

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORKER = ROOT / 'audits/2026-10-10-n45-s-high1'


def main():
    checker.worker_unchanged()
    snapshot = json.loads((HERE/'custody-start.json').read_bytes())
    tracked = json.loads((WORKER/'tracked-custody.json').read_bytes())
    assert len(tracked) == 5899
    assert all(checker.sha(ROOT/p) == h for p,h in tracked.items()), 'original tracked bytes drift'
    assert checker.sha(WORKER/'tracked-custody.json') == snapshot['tracked_inventory_sha256']
    old = (WORKER/'git-status-start.txt').read_text().splitlines()
    now = subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=all'],cwd=ROOT,text=True).splitlines()
    allowed = snapshot['allowed_new_audit_prefixes'] + ['audits/2026-10-10-n45-s-high1/']
    clean = lambda xs: [x for x in xs if not any(p in x for p in allowed)]
    assert clean(old) == clean(now), 'Git delta outside explicitly allowed independent directories'
    assert hashlib.sha256(subprocess.check_output(['git','diff','--cached','--binary'],cwd=ROOT)).hexdigest() == snapshot['cached_diff_sha256']
    assert checker.sha(HERE/'negative/existing-certificate.json') == checker.sha(WORKER/'certificate.json'), 'exclusive-create fixture mutated'
    print(json.dumps(dict(status='PASS', worker_regular_files_bytes_modes_unchanged=94,
                          original_tracked_file_bytes_unchanged=5899,
                          Git_delta_outside_worker_and_explicit_independent_audit_prefixes=0,
                          original_cached_diff_unchanged=True, exclusive_create_fixture_unchanged=True,
                          old_untracked_tree='not inventoried; consulted inputs only',
                          parent_custody='separate independent supervision layer'),sort_keys=True))


if __name__ == '__main__':
    main()
