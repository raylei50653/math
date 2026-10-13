#!/usr/bin/env python3
"""Read-only integrity check. Live routing drift is reported, not rewritten.

The mathematical authority is the named Git BASE and frozen bytes. DELIVERY
excludes only itself, so no self-referential digest is claimed.
"""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent


def main():
    delivery = json.loads((ROOT/'DELIVERY.json').read_text())
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
              and p.name != 'DELIVERY.json'}
    assert actual == {x['path'] for x in delivery['files']}, 'delivery coverage mismatch'
    for entry in delivery['files']:
        data = (ROOT/entry['path']).read_bytes()
        assert len(data) == entry['bytes'], entry['path']
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
    base = json.loads((ROOT/'BASE.json').read_text())
    live_drift = []
    for entry in base['inputs']:
        frozen = (ROOT/'frozen'/entry['path']).read_bytes()
        blob = subprocess.check_output(['git', 'show', base['base']+':'+entry['path']], cwd=REPO)
        assert frozen == blob
        assert len(frozen) == entry['bytes']
        assert hashlib.sha256(frozen).hexdigest() == entry['sha256']
        if (REPO/entry['path']).read_bytes() != frozen:
            live_drift.append(entry['path'])
    print(json.dumps({'status': 'PASS immutable delivery and BASE authority',
                      'files': len(actual), 'frozen_inputs': len(base['inputs']),
                      'live_input_drift_not_used_as_authority': live_drift}, sort_keys=True))


if __name__ == '__main__':
    main()
