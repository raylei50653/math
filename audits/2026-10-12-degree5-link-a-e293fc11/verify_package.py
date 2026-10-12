#!/usr/bin/env python3
"""Verify this isolated package and its frozen BASE inputs without writing."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_inputs():
    data = json.loads((AUDIT / 'INPUTS.json').read_text())
    for row in data['inputs']:
        frozen = (AUDIT / row['frozen']).read_bytes()
        assert digest(frozen) == row['sha256'], f"Frozen drift: {row['path']}"
        original = subprocess.check_output(['git', 'show', data['base'] + ':' + row['path']], cwd=ROOT)
        assert original == frozen, f"BASE mismatch: {row['path']}"
    return len(data['inputs'])


def files():
    return {str(path.relative_to(AUDIT)): digest(path.read_bytes())
            for path in sorted(AUDIT.rglob('*'))
            if path.is_file() and path.name != 'MANIFEST.json'
            and '__pycache__' not in path.parts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-manifest', action='store_true')
    args = parser.parse_args()
    count = validate_inputs()
    actual = files()
    manifest = AUDIT / 'MANIFEST.json'
    if args.write_manifest:
        with manifest.open('x') as stream:
            json.dump({'schema': 'isolated-degree5-link-a-manifest-v1',
                       'excludes': ['MANIFEST.json', '**/__pycache__/**'],
                       'files': actual}, stream, sort_keys=True, indent=2)
            stream.write('\n')
    else:
        expected = json.loads(manifest.read_text())['files']
        assert expected == actual, 'Package drift or unlisted file'
    print(json.dumps({'status': 'PASS', 'frozen_base_files': count,
                      'package_files': len(actual), 'read_only': not args.write_manifest}, sort_keys=True))


if __name__ == '__main__':
    main()
