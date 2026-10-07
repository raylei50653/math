#!/usr/bin/env python3
"""Seal/check only the explicit M4 delivery paths, excluding caches and this seal."""
import argparse
import hashlib
import json
from pathlib import Path

FOLDERS = ['audits/2026-10-07-m2-u1-audit', 'audits/2026-10-07-m3-fresh-checkout',
           'audits/2026-10-07-merge-supervision', 'audits/2026-10-07-m4-local']
DOCUMENTS = ['docs/STATUS.md', 'docs/c5_kempe_guide.md', 'docs/history/2026-10-07-m4-local-delivery.md']
MANIFEST = 'audits/2026-10-07-m4-local/DELIVERY.json'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    repo = args.repo.resolve()
    paths = [repo / p for p in DOCUMENTS]
    paths += [p for folder in FOLDERS for p in (repo / folder).rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'
              and p.relative_to(repo).as_posix() != MANIFEST]
    entries = [{'path': p.relative_to(repo).as_posix(), 'bytes': p.stat().st_size,
                'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]
    assert len(entries) == len({e['path'] for e in entries})
    assert all(e['bytes'] < 1000000 for e in entries)
    result = {'task': 'M4-L', 'input_candidate_sha': 'ba0b447f09617591d9f2ba81c988f537af771791',
              'main_base_sha': '2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090',
              'final_delivery_sha': 'resolve with git rev-parse HEAD; seal omits its own hash',
              'explicit_folders': FOLDERS, 'explicit_documents': DOCUMENTS,
              'excluded': ['scratch', '__pycache__', '*.pyc', MANIFEST],
              'files': entries, 'file_count': len(entries), 'file_bytes': sum(e['bytes'] for e in entries)}
    target = repo / MANIFEST
    if args.check:
        assert result == json.loads(target.read_bytes()), 'delivery file set or bytes changed'
    else:
        target.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'action': 'check' if args.check else 'seal', 'status': 'PASS',
                      'files_without_seal': len(entries), 'bytes_without_seal': result['file_bytes'],
                      'seal_sha256': hashlib.sha256(target.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
