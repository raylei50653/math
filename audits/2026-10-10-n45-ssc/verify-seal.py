#!/usr/bin/env python3
"""Read-only exact regular-file and symlink-target seal checker."""
from pathlib import Path
import hashlib
import json
import re
import sys

OUT = Path(__file__).resolve().parent

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def require(value, reason):
    if not value:
        raise ValueError(reason)

def main():
    entries = {}
    for line in (OUT / 'MANIFEST.sha256').read_text().splitlines():
        digest, name = line.split('  ', 1)
        require(re.fullmatch('[0-9a-f]{64}', digest) and name not in entries, 'malformed seal entry')
        entries[name] = digest
    paths = {p.relative_to(OUT).as_posix(): p for p in OUT.rglob('*')
             if p.is_file() and not p.is_symlink() and p.relative_to(OUT).as_posix() not in {'MANIFEST.sha256', 'delivery.json'}
             and not p.relative_to(OUT).as_posix().startswith('seal-checks/')}
    require(set(paths) == set(entries), 'own payload inventory changed')
    for name, digest in entries.items():
        require(sha(paths[name]) == digest, 'own payload digest changed: ' + name)
    actual_links = {p.relative_to(OUT).as_posix(): str(p.readlink()) for p in OUT.rglob('*') if p.is_symlink()}
    require(actual_links == json.loads((OUT / 'SYMLINKS.json').read_bytes()), 'own symlink target inventory changed')
    receipt = json.loads((OUT / 'delivery.json').read_bytes())
    require(receipt['manifest_sha256'] == sha(OUT / 'MANIFEST.sha256'), 'own receipt manifest mismatch')
    require(receipt['payload_regular_files'] == len(entries) and receipt['symlink_count'] == len(actual_links), 'own receipt count mismatch')
    require(receipt['paper_adoption'] == 'NOT_ADJUDICATED', 'own receipt promoted mathematics')
    print(json.dumps({'task': 'N45-SSC', 'payload_regular_files': len(entries), 'symlink_count': len(actual_links),
                      'manifest_sha256': sha(OUT / 'MANIFEST.sha256'), 'judgment': 'PASS_SEAL_INTEGRITY_ONLY'}, indent=2, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
