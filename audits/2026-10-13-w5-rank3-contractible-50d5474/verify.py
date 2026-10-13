#!/usr/bin/env python3
"""Verify frozen BASE bytes, the sealed local delivery and gzip integrity.

Does not regenerate certificates, edit old audits, or change Git state.
Mathematical replay commands remain separate in REPORT.md.
"""
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    base = json.loads((ROOT/'BASE.json').read_text())
    catalogue = json.loads((ROOT/'CATALOGUE_INPUT.json').read_text())
    assert base['base'] == catalogue['base']
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO).decode().strip() == base['base']
    for record in base['inputs']+[catalogue]:
        original = subprocess.check_output(['git', 'show', base['base']+':'+record['path']], cwd=REPO)
        frozen = (ROOT/'frozen'/record['path']).read_bytes()
        assert original == frozen, record['path']
        assert len(frozen) == record['bytes'] and sha(frozen) == record['sha256'], record['path']
    delivery = json.loads((ROOT/'DELIVERY.json').read_text())
    for record in delivery['files']:
        path = REPO/record['path']
        data = path.read_bytes()
        assert len(data) == record['bytes'] and sha(data) == record['sha256'], record['path']
        if path.suffix == '.gz':
            with gzip.open(path, 'rb') as stream:
                for _ in iter(lambda: stream.read(1 << 20), b''):
                    pass
    # Old tracked audits and global storage metadata must stay byte-identical.
    changes = subprocess.check_output(['git', 'diff', '--name-only', base['base'], '--',
                                      'audits', 'artifacts/MANIFEST.json', '.gitignore'], cwd=REPO)
    assert not changes, changes.decode()
    assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=REPO)
    print(json.dumps({'status': 'PASS', 'base': base['base'], 'frozen_inputs': 20,
                      'sealed_files': len(delivery['files']), 'gzip_integrity': True,
                      'old_tracked_audits_unchanged': True, 'real_index_unchanged': True,
                      'new_Lean_theorem': False}, sort_keys=True))


if __name__ == '__main__':
    main()
