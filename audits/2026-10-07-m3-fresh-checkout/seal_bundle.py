#!/usr/bin/env python3
"""Seal or independently recheck every fresh M3 delivery file except this manifest."""
import argparse
import hashlib
import json
from pathlib import Path


def inventory(root):
    return [{'path': str(p.relative_to(root)), 'bytes': p.stat().st_size,
             'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(root.rglob('*'))
            if p.is_file() and p.name != 'BUNDLE_INVENTORY.json' and '__pycache__' not in p.parts]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = root / 'BUNDLE_INVENTORY.json'
    files = inventory(root)
    assert all(p['bytes'] < 1000000 for p in files)
    if args.check:
        assert files == json.loads(manifest.read_text())['files'], 'bundle bytes or file set changed'
    else:
        result = {'candidate_sha': 'ba0b447f09617591d9f2ba81c988f537af771791',
                  'excluded': ['BUNDLE_INVENTORY.json itself', '__pycache__ execution cache'],
                  'file_count': len(files), 'file_bytes': sum(p['bytes'] for p in files),
                  'verify_command': ['python3', str(Path(__file__).resolve()), '--check'], 'files': files}
        manifest.write_text(json.dumps(result, indent=2) + '\n')
        assert inventory(root) == json.loads(manifest.read_text())['files']
    print(json.dumps({'status': 'PASS', 'action': 'check' if args.check else 'seal',
                      'files': len(files), 'bytes': sum(p['bytes'] for p in files),
                      'manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
