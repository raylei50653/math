#!/usr/bin/env python3
"""Verify byte-exact published originals after archive restoration."""
import argparse
import hashlib
import json
from pathlib import Path
import stat

here = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--checkout', type=Path, default=here.parent.parent)
parser.add_argument('--check', action='store_true', required=True)
args = parser.parse_args()
root = args.checkout.resolve()
plan = json.loads((here / 'plan.json').read_bytes())
expected = {pin['path']: pin for pin in plan['immutable_files']}
observed = set()
for directory in plan['selected_roots']:
    for path in (root / directory).rglob('*'):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        assert stat.S_ISREG(mode), str(path)
        relative = path.relative_to(root).as_posix()
        observed.add(relative)
        assert relative in expected, relative
        pin = expected[relative]
        raw = path.read_bytes()
        assert len(raw) == pin['bytes'], relative
        assert hashlib.sha256(raw).hexdigest() == pin['sha256'], relative
        assert stat.S_IMODE(mode) == pin['mode'], relative
assert observed == set(expected)
print(json.dumps({'status': 'pass', 'original_roots': len(plan['selected_roots']),
                  'original_files': len(expected), 'original_bytes': plan['immutable_bytes'],
                  'all_bytes_and_modes_exact': True, 'source_realizability_or_paper_soundness_checked': False}, sort_keys=True))
