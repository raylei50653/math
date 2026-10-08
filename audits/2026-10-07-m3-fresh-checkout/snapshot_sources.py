#!/usr/bin/env python3
"""Inventory all candidate/restored source bytes, excluding execution caches."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('/tmp/math-m3-ba0b447'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--compare', type=Path)
    args = parser.parse_args()
    entries = {}
    for parent, directories, files in os.walk(args.root, followlinks=False):
        directories[:] = sorted(d for d in directories if d not in {'.git', '.lake', '.venv', '__pycache__'})
        for name in sorted(directories + files):
            path = Path(parent) / name
            relative = str(path.relative_to(args.root))
            if path.is_symlink():
                entries[relative] = {'kind': 'symlink', 'target': os.readlink(path)}
            elif path.is_file() and path.suffix != '.pyc':
                entries[relative] = {'kind': 'file', 'bytes': path.stat().st_size,
                                     'mode': oct(stat.S_IMODE(path.stat().st_mode)),
                                     'sha256': digest(path)}
    result = {'root': str(args.root), 'excluded_cache_names': ['.git', '.lake', '.venv', '__pycache__', '*.pyc'],
              'entries': entries, 'entry_count': len(entries),
              'file_bytes': sum(v.get('bytes', 0) for v in entries.values())}
    if args.compare:
        previous = json.loads(args.compare.read_text())['entries']
        result['added'] = sorted(set(entries) - set(previous))
        result['removed'] = sorted(set(previous) - set(entries))
        result['changed'] = [p for p in sorted(set(entries) & set(previous)) if entries[p] != previous[p]]
        result['zero_drift'] = not (result['added'] or result['removed'] or result['changed'])
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'entries'}, sort_keys=True))
    return 0 if result.get('zero_drift', True) else 1


if __name__ == '__main__':
    raise SystemExit(main())
